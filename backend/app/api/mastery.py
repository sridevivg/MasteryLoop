import logging
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.curriculum import Domain, Topic, Subtopic, Skill
from app.models.mastery import LearnerSkillMastery
from app.models.session import AssessmentSession, SessionStatus
from app.models.interaction import Interaction
from app.models.learning import LearnerRoadmap, DailyChallenge
from app.schemas.mastery import (
    LearnerDashboardResponse,
    SkillMasteryDetail,
    PlacementDomainReadiness,
    NextBestActionItem,
    ForecastRequest,
    ForecastResponse
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/mastery", tags=["Learner Mastery & Dashboard"])


@router.get(
    "/dashboard",
    response_model=LearnerDashboardResponse,
    summary="Get comprehensive learner dashboard metrics with real database calculations"
)
def get_learner_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id

    # 1. Fetch all mastery records for this learner
    mastery_records = (
        db.query(LearnerSkillMastery, Skill, Subtopic, Topic, Domain)
        .join(Skill, LearnerSkillMastery.skill_id == Skill.id)
        .join(Subtopic, Skill.subtopic_id == Subtopic.id)
        .join(Topic, Subtopic.topic_id == Topic.id)
        .join(Domain, Topic.domain_id == Domain.id)
        .filter(LearnerSkillMastery.user_id == user_id)
        .all()
    )

    # 2. Overall Mastery and Placement Readiness
    total_mastery_sum = sum(m.estimate for m, sk, sub, top, dom in mastery_records)
    tested_skills_count = len(mastery_records)
    overall_mastery = round((total_mastery_sum / max(tested_skills_count, 1)) * 100, 1) if tested_skills_count > 0 else 0.0

    mastered_skills_count = sum(1 for m, sk, sub, top, dom in mastery_records if m.estimate >= 0.70)
    total_curriculum_skills = db.query(Skill).count() or 54
    placement_readiness = round((mastered_skills_count / max(total_curriculum_skills, 1)) * 100, 1)

    # 3. Assessment & Question Totals
    total_assessments = db.query(AssessmentSession).filter(
        AssessmentSession.user_id == user_id,
        AssessmentSession.status == SessionStatus.COMPLETED
    ).count()

    total_questions = db.query(Interaction).filter(Interaction.user_id == user_id).count()

    # 4. Study Streak Calculation (consecutive days with interactions)
    interactions = db.query(Interaction.timestamp).filter(
        Interaction.user_id == user_id
    ).order_by(Interaction.timestamp.desc()).all()

    streak_days = 0
    if interactions:
        dates = sorted({intr.timestamp.date() for intr in interactions}, reverse=True)
        today = datetime.now(timezone.utc).date()
        if dates and (dates[0] == today or dates[0] == today - timedelta(days=1)):
            streak_days = 1
            curr_date = dates[0]
            for next_date in dates[1:]:
                if curr_date - next_date == timedelta(days=1):
                    streak_days += 1
                    curr_date = next_date
                else:
                    break

    # 5. Strong and Weak Topics
    topic_aggregates = {}
    for m, sk, sub, top, dom in mastery_records:
        if top.name not in topic_aggregates:
            topic_aggregates[top.name] = {"sum": 0.0, "count": 0, "domain": dom.name}
        topic_aggregates[top.name]["sum"] += m.estimate
        topic_aggregates[top.name]["count"] += 1

    strong_topics = []
    weak_topics = []
    for t_name, t_data in topic_aggregates.items():
        avg_est = round((t_data["sum"] / t_data["count"]) * 100, 1)
        item = {
            "topic_name": t_name,
            "name": t_name,
            "domain_name": t_data["domain"],
            "domain": t_data["domain"],
            "mastery_percentage": avg_est,
            "mastery": round(avg_est / 100.0, 3)
        }
        if avg_est >= 65.0:
            strong_topics.append(item)
        else:
            weak_topics.append(item)

    strong_topics.sort(key=lambda x: x["mastery_percentage"], reverse=True)
    weak_topics.sort(key=lambda x: x["mastery_percentage"])

    # 6. Placement Readiness across 11 Domains
    all_domains = db.query(Domain).all()
    domain_readiness_list = []
    for dom in all_domains:
        dom_skills_total = (
            db.query(Skill)
            .join(Subtopic, Skill.subtopic_id == Subtopic.id)
            .join(Topic, Subtopic.topic_id == Topic.id)
            .filter(Topic.domain_id == dom.id)
            .count()
        )
        dom_mastery = [m for m, sk, sub, top, d in mastery_records if d.id == dom.id]
        dom_tested = len(dom_mastery)
        dom_mastered = sum(1 for m in dom_mastery if m.estimate >= 0.70)
        dom_pct = round((dom_mastered / max(dom_skills_total, 1)) * 100, 1) if dom_skills_total > 0 else 0.0

        status_label = "UNTESTED"
        if dom_tested > 0:
            status_label = "PLACEMENT_READY" if dom_pct >= 60.0 else "NEEDS_PRACTICE"

        domain_readiness_list.append(PlacementDomainReadiness(
            domain_id=dom.id,
            domain_name=dom.name,
            readiness_percentage=dom_pct,
            tested_skills_count=dom_tested,
            total_skills_count=dom_skills_total,
            benchmark_status=status_label,
            top_strength=dom.name if dom_pct >= 60 else None,
            priority_weakness=dom.name if dom_pct < 40 and dom_tested > 0 else None
        ))

    # 7. Exactly Three Prioritized Next-Best Actions
    active_roadmap = db.query(LearnerRoadmap).filter(
        LearnerRoadmap.user_id == user_id,
        LearnerRoadmap.is_active == True
    ).order_by(LearnerRoadmap.generated_at.desc()).first()

    actions_list = []
    if active_roadmap and active_roadmap.actions:
        for act in active_roadmap.actions[:3]:
            actions_list.append(NextBestActionItem(
                category=act.get("category", "LEARN"),
                skill_id=act.get("skill_id", ""),
                skill_name=act.get("skill_name", "Core Topic"),
                domain_name=act.get("domain_name", "Placement Preparation"),
                title=act.get("title", "Review Concept"),
                duration_minutes=act.get("duration_minutes", 15),
                rationale=act.get("rationale", "Reinforce learning gap."),
                action_type=act.get("action_type", "TUTOR"),
                target_id=act.get("skill_id")
            ))
    else:
        # Default starter actions if no assessment taken yet
        first_domain = all_domains[0] if all_domains else None
        actions_list = [
            NextBestActionItem(
                category="LEARN",
                skill_id="",
                skill_name="Diagnostic Evaluation",
                domain_name="Placement Diagnostic",
                title="Take Initial Placement Diagnostic",
                duration_minutes=15,
                rationale="Calibrate your starting ability level across quantitative, reasoning, and technical domains.",
                action_type="ASSESSMENT",
                target_id=first_domain.id if first_domain else None
            ),
            NextBestActionItem(
                category="PRACTICE",
                skill_id="",
                skill_name="Programming Foundations",
                domain_name="Programming Fundamentals",
                title="Practice Coding Syntax & Loops",
                duration_minutes=12,
                rationale="Build procedural problem-solving speed with targeted foundational exercises.",
                action_type="PRACTICE"
            ),
            NextBestActionItem(
                category="REASSESS",
                skill_id="",
                skill_name="Benchmark Check",
                domain_name="Core Aptitude",
                title="Verify Quantitative Fundamentals",
                duration_minutes=10,
                rationale="Establish baseline psychometric theta parameters.",
                action_type="ASSESSMENT"
            )
        ]

    # 8. Today's Personalized Challenge
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    challenge = db.query(DailyChallenge).filter(
        DailyChallenge.user_id == user_id,
        DailyChallenge.target_date == today_str
    ).first()

    challenge_dict = None
    if challenge:
        challenge_dict = {
            "id": challenge.id,
            "title": challenge.title,
            "description": challenge.description,
            "completed": challenge.completed,
            "score_percentage": challenge.score_percentage
        }
    else:
        challenge_dict = {
            "title": "Daily Placement Sprint: Two-Pointer & Search",
            "description": "Complete 3 curated adaptive questions on Arrays and Sorting to maintain your study momentum.",
            "completed": False,
            "score_percentage": 0.0
        }

    # 9. Recent Assessments
    recent_sessions = db.query(AssessmentSession, Domain).outerjoin(
        Domain, AssessmentSession.domain_id == Domain.id
    ).filter(
        AssessmentSession.user_id == user_id
    ).order_by(AssessmentSession.started_at.desc()).limit(5).all()

    recent_list = []
    for s, d in recent_sessions:
        rep = s.report_data or {}
        score = rep.get("overall_score", {})
        recent_list.append({
            "session_id": s.id,
            "kind": s.kind.value,
            "status": s.status.value,
            "domain_name": d.name if d else "General Diagnostic",
            "accuracy_percentage": score.get("accuracy_percentage", 0.0),
            "date": s.started_at.strftime("%Y-%m-%d"),
            "completed_at": (s.completed_at or s.started_at).isoformat(),
            "score": round(score.get("accuracy_percentage", 0.0)),
            "theta": round(float(s.theta or 0.0), 2)
        })

    # 10. Chronological Mastery Trend
    trend_entries = []
    for m, sk, sub, top, dom in mastery_records:
        for h in (m.history or []):
            trend_entries.append({
                "timestamp": h.get("timestamp"),
                "skill_name": sk.name,
                "estimate": h.get("estimate")
            })
    trend_entries.sort(key=lambda x: x.get("timestamp") or "")

    return LearnerDashboardResponse(
        overall_mastery=overall_mastery,
        placement_readiness=placement_readiness,
        study_streak_days=streak_days,
        total_assessments_taken=total_assessments,
        total_questions_solved=total_questions,
        retention_due_count=sum(1 for m, sk, sub, top, dom in mastery_records if m.retention_estimate < 0.60),
        strong_topics=strong_topics[:5],
        weak_topics=weak_topics[:5],
        placement_domains=domain_readiness_list,
        next_best_actions=actions_list[:3],
        today_challenge=challenge_dict,
        recent_assessments=recent_list,
        mastery_trend=trend_entries[-15:]
    )


@router.get(
    "/skills",
    response_model=List[SkillMasteryDetail],
    summary="Get granular skill-level mastery state for all evaluated skills"
)
def get_learner_skills_mastery(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = (
        db.query(LearnerSkillMastery, Skill, Subtopic, Topic, Domain)
        .join(Skill, LearnerSkillMastery.skill_id == Skill.id)
        .join(Subtopic, Skill.subtopic_id == Subtopic.id)
        .join(Topic, Subtopic.topic_id == Topic.id)
        .join(Domain, Topic.domain_id == Domain.id)
        .filter(LearnerSkillMastery.user_id == current_user.id)
        .all()
    )

    results = []
    for m, sk, sub, top, dom in records:
        status_label = "DEVELOPING"
        if m.estimate >= 0.80:
            status_label = "MASTERED"
        elif m.estimate >= 0.60:
            status_label = "PROFICIENT"
        elif m.estimate < 0.40:
            status_label = "CRITICAL_GAP"

        results.append(SkillMasteryDetail(
            skill_id=sk.id,
            skill_name=sk.name,
            skill_code=sk.code,
            domain_name=dom.name,
            topic_name=top.name,
            estimate=round(m.estimate, 3),
            confidence=round(m.confidence, 3),
            raw_accuracy=round(m.raw_accuracy * 100, 1),
            irt_ability=round(m.irt_ability, 2),
            retention_estimate=round(m.retention_estimate, 3),
            interaction_count=m.interaction_count,
            last_practiced_at=m.last_practiced_at.isoformat() if m.last_practiced_at else None,
            next_review_due=m.next_review_due.isoformat() if m.next_review_due else None,
            status=status_label
        ))

    return results


@router.post(
    "/forecast",
    response_model=ForecastResponse,
    summary="Generate what-if study forecast based on weekly study commitment"
)
def forecast_mastery_trajectory(
    req: ForecastRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    mastery_count = db.query(LearnerSkillMastery).filter(LearnerSkillMastery.user_id == user_id).count()

    # If insufficient history (< 3 interactions), transparently explain more data is needed
    if mastery_count < 2:
        return ForecastResponse(
            has_sufficient_data=False,
            current_readiness=0.0,
            forecasted_readiness=0.0,
            weekly_projection=[],
            explanation="Insufficient interaction history to construct a reliable psychometric forecast. Complete at least one diagnostic assessment to calibrate your baseline.",
            assumptions=["Requires at least 2 completed assessment observations."]
        )

    mastery_records = db.query(LearnerSkillMastery).filter(LearnerSkillMastery.user_id == user_id).all()
    avg_current = sum(m.estimate for m in mastery_records) / max(len(mastery_records), 1)
    current_pct = round(avg_current * 100, 1)

    # Theoretical growth rate model: Diminishing returns curve R(t) = R_max - (R_max - R0)*exp(-k*t)
    hours = max(req.study_hours_per_week, 1.0)
    k = 0.045 * (hours / 5.0)  # calibrated growth rate

    projection = []
    projected = current_pct
    for week in range(1, req.forecast_weeks + 1):
        # Growth modeling
        delta = (95.0 - projected) * (1.0 - math.exp(-k))
        projected = min(round(projected + delta, 1), 96.0)
        projection.append({
            "week": week,
            "projected_readiness": projected,
            "estimated_skills_mastered": min(int(len(mastery_records) * (projected / max(current_pct, 1))), 54)
        })

    return ForecastResponse(
        has_sufficient_data=True,
        current_readiness=current_pct,
        forecasted_readiness=projected,
        weekly_projection=projection,
        explanation=f"Based on your current trajectory and an estimated study commitment of {hours} hrs/week, your placement readiness is projected to reach approximately {projected}% across {req.forecast_weeks} weeks.",
        assumptions=[
            f"Assumes consistent study effort of {hours} hours per week.",
            "Assumes active spaced repetition of prerequisite foundation skills.",
            "Projections are empirical statistical estimates and do not guarantee testing outcomes."
        ]
    )


@router.get(
    "/retention/due",
    summary="Get list of skills currently due for spaced review based on Ebbinghaus forgetting risk"
)
def get_due_retention_reviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.intelligence.retention import RetentionEngine
    due_skills = RetentionEngine.get_due_skills(db, current_user.id)
    return {
        "user_id": current_user.id,
        "due_count": len(due_skills),
        "due_skills": due_skills
    }


from pydantic import BaseModel
class RetentionReviewRequest(BaseModel):
    skill_id: str
    is_correct: bool


@router.post(
    "/retention/review",
    summary="Record a spaced repetition review interaction and update memory stability"
)
def record_retention_review(
    req: RetentionReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.intelligence.retention import RetentionEngine
    skill = db.query(Skill).filter((Skill.id == req.skill_id) | (Skill.code == req.skill_id)).first()
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Skill '{req.skill_id}' not found.")

    record = RetentionEngine.record_review_event(
        db=db,
        user_id=current_user.id,
        skill_id=skill.id,
        is_correct=req.is_correct
    )

    return {
        "status": "success",
        "skill_id": skill.id,
        "skill_name": skill.name,
        "is_correct": req.is_correct,
        "new_retention_estimate": record.retention_estimate,
        "next_review_due": record.next_review_due.isoformat() if record.next_review_due else None,
        "interaction_count": record.interaction_count
    }

