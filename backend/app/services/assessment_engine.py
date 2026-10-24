"""
Adaptive Assessment Engine for MasteryLoop.
Implements maximum Fisher Information item selection, exposure control,
explainable selection rationale, deterministic scoring, BKT mastery updates,
EAP ability recalibration, and prerequisite-aware learning gap detection.
"""

import math
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.item import Item, ItemState, ItemType
from app.models.curriculum import Skill, Domain, Topic, Subtopic
from app.models.session import AssessmentSession, SessionKind, SessionStatus
from app.models.interaction import Interaction
from app.models.mastery import LearnerSkillMastery
from app.models.learning import LearnerRoadmap, ActionCategory
from app.psychocore.irt import (
    probability_2pl,
    fisher_information_2pl,
    estimate_ability_eap,
    standard_error
)
from app.kt.bkt import bkt_service
from app.services.skill_graph import SkillDependencyGraph
from app.schemas.session import LearnerItemView


class AssessmentEngine:
    """Core orchestrator for assessment session lifecycle, question delivery, and psychometrics."""

    @staticmethod
    def select_next_question(
        session: AssessmentSession,
        db: Session
    ) -> Tuple[Optional[Item], Optional[Dict[str, Any]]]:
        """
        Selects the next most informative item for the learner under exposure constraints.
        Returns (selected_item, selection_explanation).
        """
        asked_ids = set(session.asked_item_ids or [])

        # Candidate item query: active items in target domain not yet asked
        query = db.query(Item).filter(
            Item.state == ItemState.ACTIVE,
            ~Item.id.in_(asked_ids)
        )

        topic_id = getattr(session, "topic_id", None) or (session.state_data or {}).get("topic_id")
        if topic_id:
            query = query.join(Skill, Item.primary_skill_id == Skill.id)\
                         .join(Subtopic, Skill.subtopic_id == Subtopic.id)\
                         .filter(Subtopic.topic_id == topic_id)
        elif session.domain_id:
            query = query.join(Skill, Item.primary_skill_id == Skill.id)\
                         .join(Subtopic, Skill.subtopic_id == Subtopic.id)\
                         .join(Topic, Subtopic.topic_id == Topic.id)\
                         .filter(Topic.domain_id == session.domain_id)

        candidates = query.all()
        if not candidates:
            return (None, None)

        theta = session.theta or 0.0
        selected_item = None
        best_metric = -1.0
        rationale_dict = {}

        if session.kind == SessionKind.ADAPTIVE:
            # Maximum Fisher Information selection
            for item in candidates:
                # Apply exposure penalty if item has been served heavily
                exposure_penalty = max(0.5, 1.0 - (item.exposure_count / max(settings.EXPOSURE_CONTROL_CAP, 100)))
                info = fisher_information_2pl(theta, item.a, item.b) * exposure_penalty
                
                if info > best_metric:
                    best_metric = info
                    selected_item = item

            # Generate explainability details for the learner
            skill = db.query(Skill).filter(Skill.id == selected_item.primary_skill_id).first()
            rationale_dict = {
                "target_skill_code": skill.code if skill else "UNKNOWN",
                "target_skill_name": skill.name if skill else "General Concept",
                "current_estimated_ability": round(theta, 2),
                "item_difficulty": round(selected_item.b, 2),
                "fisher_information_units": round(best_metric, 3),
                "selection_strategy": "Maximum Fisher Information (Adaptive)",
                "explanation_text": (
                    f"Selected to maximize measurement precision for '{skill.name}' "
                    f"at your current estimated ability level (θ={round(theta, 2):+0.2f}). "
                    f"Question difficulty is calibrated at {round(selected_item.b, 2):+0.2f} logits."
                )
            }
        else:
            # Diagnostic / Fixed mode: balanced skill coverage around average difficulty (b ≈ 0.0)
            candidates.sort(key=lambda it: abs(it.b - 0.0))
            selected_item = candidates[0]
            skill = db.query(Skill).filter(Skill.id == selected_item.primary_skill_id).first()
            rationale_dict = {
                "target_skill_code": skill.code if skill else "UNKNOWN",
                "target_skill_name": skill.name if skill else "General Concept",
                "item_difficulty": round(selected_item.b, 2),
                "selection_strategy": "Balanced Curriculum Diagnostic",
                "explanation_text": f"Selected for comprehensive baseline coverage of {skill.name}."
            }

        return (selected_item, rationale_dict)

    @staticmethod
    def sanitize_item_for_learner(
        item: Item,
        question_number: int,
        total_questions_estimated: int,
        selection_explanation: Optional[Dict[str, Any]] = None,
        domain_name: Optional[str] = None,
        topic_name: Optional[str] = None,
        warning: Optional[str] = None
    ) -> LearnerItemView:
        """
        CRITICAL SECURITY BARRIER: Sanitizes an item to ensure answer keys, explanations,
        and distractor identities are NEVER leaked before the student answers.
        """
        sanitized_options = [
            {"id": opt.get("id"), "text": opt.get("text")}
            for opt in (item.options or [])
        ]

        # For coding items, include visible (non-hidden) example test cases
        visible_test_cases = None
        if item.test_cases:
            visible_test_cases = [
                {
                    "input": str(tc.get("input", "")),
                    "expected_output": str(tc.get("expected_output") if tc.get("expected_output") is not None else tc.get("expected", "")),
                    "is_hidden": False
                }
                for tc in item.test_cases
                if not (tc.get("is_hidden") or tc.get("hidden", False))
            ]

        return LearnerItemView(
            id=item.id,
            item_type=item.item_type.value if hasattr(item.item_type, 'value') else str(item.item_type),
            stem=item.stem,
            options=sanitized_options,
            code_template=item.code_template,
            visible_test_cases=visible_test_cases,
            question_number=question_number,
            total_questions_estimated=total_questions_estimated,
            domain_name=domain_name,
            topic_name=topic_name,
            warning=warning,
            selection_explanation=selection_explanation
        )

    @staticmethod
    def process_learner_response(
        session: AssessmentSession,
        item: Item,
        response_value: str,
        latency_ms: int,
        confidence_rating: int,
        db: Session
    ) -> Dict[str, Any]:
        """
        Deterministically evaluates response, records interaction, updates BKT mastery,
        recalibrates EAP ability, and evaluates stopping rules.
        """
        # 1. Deterministic Scoring
        if getattr(item, "item_type", None) in (ItemType.CODING, "CODING"):
            if response_value.strip().upper() == item.answer_key.strip().upper():
                is_correct = True
            elif item.test_cases:
                try:
                    from app.intelligence.coding_sandbox import execute_sandboxed_code
                    sandbox_res = execute_sandboxed_code(response_value, item.test_cases)
                    is_correct = bool(sandbox_res.get("all_passed", False))
                except Exception as e:
                    logger.warning(f"Coding sandbox evaluation error: {e}")
                    is_correct = False
            else:
                is_correct = False
        else:
            is_correct = (response_value.strip().upper() == item.answer_key.strip().upper())

        # 2. Append-only Interaction Record
        interaction = Interaction(
            session_id=session.id,
            user_id=session.user_id,
            item_id=item.id,
            skill_id=item.primary_skill_id,
            response_value=response_value.strip(),
            is_correct=is_correct,
            latency_ms=latency_ms,
            confidence_rating=confidence_rating,
            scored=True,
            pilot=False,
            theta_snapshot=session.theta,
            se_snapshot=session.se
        )
        db.add(interaction)
        db.flush()

        # Increment question exposure count
        item.exposure_count = (item.exposure_count or 0) + 1

        # Update asked items tracking in session
        asked_list = list(session.asked_item_ids or [])
        asked_list.append(item.id)
        session.asked_item_ids = asked_list

        # 3. Recalibrate Learner Ability (Theta & SE) via 2PL EAP
        scored_interactions = db.query(Interaction, Item).join(
            Item, Interaction.item_id == Item.id
        ).filter(
            Interaction.session_id == session.id,
            Interaction.scored == True
        ).all()

        responses_for_eap = [
            (it.a, it.b, intr.is_correct)
            for intr, it in scored_interactions
            if intr.id != interaction.id
        ]
        # Include current response in calculation exactly once
        responses_for_eap.append((item.a, item.b, is_correct))

        new_theta, new_se = estimate_ability_eap(responses_for_eap)
        session.theta = new_theta
        session.se = new_se

        # 4. Update Bayesian Knowledge Tracing (BKT) Mastery
        mastery_record = db.query(LearnerSkillMastery).filter(
            LearnerSkillMastery.user_id == session.user_id,
            LearnerSkillMastery.skill_id == item.primary_skill_id
        ).first()

        current_estimate = mastery_record.estimate if mastery_record else 0.40
        new_mastery = bkt_service.update_mastery(
            current_mastery=current_estimate,
            is_correct=is_correct,
            confidence_rating=confidence_rating
        )

        now_iso = datetime.now(timezone.utc).isoformat()
        if not mastery_record:
            history_entry = {
                "timestamp": now_iso,
                "estimate": new_mastery,
                "delta": round(new_mastery - 0.40, 4),
                "event": f"Session {session.id[:8]}",
                "is_correct": is_correct
            }
            mastery_record = LearnerSkillMastery(
                user_id=session.user_id,
                skill_id=item.primary_skill_id,
                estimate=new_mastery,
                confidence=0.25,
                raw_accuracy=1.0 if is_correct else 0.0,
                irt_ability=new_theta,
                interaction_count=1,
                correct_count=1 if is_correct else 0,
                history=[history_entry]
            )
            db.add(mastery_record)
        else:
            delta = round(new_mastery - mastery_record.estimate, 4)
            mastery_record.estimate = new_mastery
            mastery_record.interaction_count += 1
            if is_correct:
                mastery_record.correct_count += 1
            mastery_record.raw_accuracy = round(mastery_record.correct_count / mastery_record.interaction_count, 4)
            mastery_record.irt_ability = new_theta
            mastery_record.confidence = bkt_service.calculate_confidence(
                mastery_record.interaction_count,
                mastery_record.raw_accuracy,
                new_mastery
            )
            hist = list(mastery_record.history or [])
            hist.append({
                "timestamp": now_iso,
                "estimate": new_mastery,
                "delta": delta,
                "event": f"Session {session.id[:8]}",
                "is_correct": is_correct
            })
            mastery_record.history = hist

        # 5. Misconception Feedback Analysis
        misconception_text = None
        if not is_correct and item.distractor_explanations:
            misconception_text = item.distractor_explanations.get(response_value.strip().upper())

        # 6. Check Stopping Rule
        max_q = (session.state_data or {}).get("max_questions", settings.DEFAULT_TARGET_QUESTIONS)
        questions_answered = len(session.asked_item_ids)

        is_completed = False
        report_data = None

        if session.kind == SessionKind.ADAPTIVE:
            # If assessing a specific topic, deliver the target questions (e.g. 15 items, or available count)
            if session.topic_id or (session.state_data or {}).get("topic_id"):
                if questions_answered >= max_q:
                    is_completed = True
            else:
                # Full domain CAT: stop on precision threshold or item cap
                if questions_answered >= max_q:
                    is_completed = True
                elif new_se <= settings.DEFAULT_TARGET_SE and questions_answered >= settings.MIN_ADAPTIVE_QUESTIONS:
                    is_completed = True
        else:
            if questions_answered >= max_q:
                is_completed = True

        if is_completed:
            session.status = SessionStatus.COMPLETED
            session.completed_at = datetime.now(timezone.utc)
            report_data = AssessmentEngine.generate_performance_report(session, db)
            session.report_data = report_data

        db.commit()

        return {
            "is_correct": is_correct,
            "correct_key": item.answer_key,
            "explanation": item.explanation,
            "misconception_feedback": misconception_text,
            "updated_theta": new_theta,
            "updated_se": new_se,
            "is_completed": is_completed,
            "report": report_data
        }

    @staticmethod
    def generate_performance_report(session: AssessmentSession, db: Session) -> Dict[str, Any]:
        """
        Calculates deterministic skill-level performance report, isolates learning gaps
        via prerequisite DAG traversal, and generates exactly three prioritized Next-Best Actions.
        """
        interactions = db.query(Interaction, Item, Skill).join(
            Item, Interaction.item_id == Item.id
        ).join(
            Skill, Item.primary_skill_id == Skill.id
        ).filter(
            Interaction.session_id == session.id
        ).all()

        total_questions = len(interactions)
        correct_count = sum(1 for intr, it, sk in interactions if intr.is_correct)
        accuracy_pct = round((correct_count / max(total_questions, 1)) * 100, 1)
        total_time_ms = sum(intr.latency_ms for intr, it, sk in interactions)
        avg_time_ms = round(total_time_ms / max(total_questions, 1))

        # Skill-level breakdown
        skills_tested = {}
        for intr, it, sk in interactions:
            if sk.id not in skills_tested:
                skills_tested[sk.id] = {
                    "skill_id": sk.id,
                    "code": sk.code,
                    "name": sk.name,
                    "total": 0,
                    "correct": 0
                }
            skills_tested[sk.id]["total"] += 1
            if intr.is_correct:
                skills_tested[sk.id]["correct"] += 1

        skill_summaries = []
        weak_skill_ids = []
        strong_skill_ids = []

        for s_id, s_info in skills_tested.items():
            acc = round((s_info["correct"] / s_info["total"]) * 100, 1)
            mastery = db.query(LearnerSkillMastery).filter(
                LearnerSkillMastery.user_id == session.user_id,
                LearnerSkillMastery.skill_id == s_id
            ).first()
            est = mastery.estimate if mastery else 0.50

            summary = {
                "skill_id": s_id,
                "code": s_info["code"],
                "name": s_info["name"],
                "accuracy_percentage": acc,
                "current_mastery_estimate": round(est, 3),
                "questions_attempted": s_info["total"]
            }
            skill_summaries.append(summary)

            if est < 0.60 or acc < 50.0:
                weak_skill_ids.append(s_id)
            else:
                strong_skill_ids.append(s_id)

        # Graph gap analysis: Prerequisite bottlenecks
        graph = SkillDependencyGraph.from_db(db)
        mastered_set = set(strong_skill_ids)
        prerequisite_warnings = []

        for w_id in weak_skill_ids:
            unmastered_foundations = graph.get_unmastered_foundations(w_id, mastered_set)
            if unmastered_foundations:
                found_names = [graph.skills_by_id[fid].name for fid in unmastered_foundations if fid in graph.skills_by_id]
                prerequisite_warnings.append({
                    "struggling_skill": graph.skills_by_id[w_id].name,
                    "missing_foundations": found_names,
                    "guidance": f"Review foundations in {', '.join(found_names)} before retrying."
                })

        # Exactly 3 Prioritized Next-Best Actions (Learn, Practice, Reassess)
        next_actions = []

        # 1. ACTION: LEARN (Focus on weakest skill or foundational blocker)
        target_learn_skill = None
        if weak_skill_ids:
            target_learn_skill = graph.skills_by_id.get(weak_skill_ids[0])
        elif skill_summaries:
            target_learn_skill = graph.skills_by_id.get(skill_summaries[0]["skill_id"])

        if target_learn_skill:
            next_actions.append({
                "category": ActionCategory.LEARN.value,
                "skill_id": target_learn_skill.id,
                "skill_name": target_learn_skill.name,
                "title": f"Review Core Concepts: {target_learn_skill.name}",
                "duration_minutes": 15,
                "rationale": f"Detected learning gap with estimated mastery of {round(target_learn_skill.difficulty_level, 2)}. Work with the AI Socratic Tutor to reinforce foundational principles.",
                "action_type": "TUTOR"
            })

        # 2. ACTION: PRACTICE (Targeted drills on developing competency)
        target_practice_skill = None
        if len(weak_skill_ids) > 1:
            target_practice_skill = graph.skills_by_id.get(weak_skill_ids[1])
        elif target_learn_skill:
            target_practice_skill = target_learn_skill

        if target_practice_skill:
            next_actions.append({
                "category": ActionCategory.PRACTICE.value,
                "skill_id": target_practice_skill.id,
                "skill_name": target_practice_skill.name,
                "title": f"Targeted Practice: {target_practice_skill.name}",
                "duration_minutes": 12,
                "rationale": f"Reinforce recent mistakes through focused practice questions to build procedural fluency.",
                "action_type": "PRACTICE"
            })

        # 3. ACTION: REASSESS (Adaptive retention verification)
        next_actions.append({
            "category": ActionCategory.REASSESS.value,
            "skill_id": target_learn_skill.id if target_learn_skill else "",
            "skill_name": target_learn_skill.name if target_learn_skill else "Placement Check",
            "title": "Adaptive Reassessment Check",
            "duration_minutes": 8,
            "rationale": "Measure skill recovery and verify whether targeted study improved your mastery probability.",
            "action_type": "ASSESSMENT"
        })

        # Persist generated roadmap for learner
        roadmap = LearnerRoadmap(
            user_id=session.user_id,
            domain_id=session.domain_id,
            actions=next_actions
        )
        db.add(roadmap)

        return {
            "session_id": session.id,
            "status": "COMPLETED",
            "domain_id": session.domain_id,
            "domain_name": (session.state_data or {}).get("domain_name"),
            "topic_id": session.topic_id or (session.state_data or {}).get("topic_id"),
            "topic_name": (session.state_data or {}).get("topic_name"),
            "overall_score": {
                "total_questions": total_questions,
                "correct_answers": correct_count,
                "accuracy_percentage": accuracy_pct,
                "final_theta": round(session.theta, 2),
                "standard_error": round(session.se, 3),
                "average_latency_ms": avg_time_ms
            },
            "skill_breakdown": skill_summaries,
            "prerequisite_gap_warnings": prerequisite_warnings,
            "next_best_actions": next_actions
        }
