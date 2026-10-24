"""
Question Bank Validator for MasteryLoop.
Audits every topic and question in the curriculum against psychometric and structural criteria:
- Total questions in database per topic
- Valid, usable active questions
- Questions with missing topic/skill relationships
- Questions with invalid difficulty (b) or discrimination (a) parameters
- Duplicate question records
- Adaptive-ready questions available for Fisher Information selection
"""

import re
from typing import Dict, List, Any, Optional
from collections import defaultdict
from sqlalchemy.orm import Session

from app.models.curriculum import Domain, Topic, Subtopic, Skill
from app.models.item import Item, ItemState, ItemType
from app.core.config import settings


class QuestionBankValidator:
    """Performs comprehensive psychometric and structural auditing of the question bank."""

    @staticmethod
    def normalize_stem(stem: str) -> str:
        """Normalizes question stem for duplicate detection."""
        if not stem:
            return ""
        # Normalize whitespace and strip punctuation while preserving alphanumeric words inside code snippets
        cleaned = re.sub(r"[$\n\r\t`]+", " ", stem)
        cleaned = re.sub(r"[^\w\s]", "", cleaned)
        return " ".join(cleaned.lower().split())

    @staticmethod
    def audit_item(item: Item, skill_to_topic: Dict[str, Any]) -> Dict[str, Any]:
        """Audits an individual item for validity, psychometric calibration, and topic mapping."""
        issues = []
        is_usable = True
        is_adaptive = True

        # Check topic mapping
        topic_info = skill_to_topic.get(item.primary_skill_id)
        if not topic_info:
            issues.append("Missing or unmapped primary_skill_id -> topic link")
            is_usable = False
            is_adaptive = False

        # Check stem
        if not item.stem or len(item.stem.strip()) < 10:
            issues.append("Question stem is empty or suspiciously short (<10 chars)")
            is_usable = False
            is_adaptive = False

        # Check options and answer key for MCQ
        if getattr(item, "item_type", None) == ItemType.MCQ:
            if not item.options or len(item.options) < 2:
                issues.append("MCQ has fewer than 2 answer choices")
                is_usable = False
                is_adaptive = False
            elif not item.answer_key or not any(opt.get("id") == item.answer_key for opt in (item.options or [])):
                issues.append(f"Answer key '{item.answer_key}' does not match any choice ID in options")
                is_usable = False
                is_adaptive = False
        elif getattr(item, "item_type", None) == ItemType.CODING:
            if not item.code_template and not item.test_cases:
                issues.append("Coding item has neither code_template nor test_cases")
                is_usable = False

        # Check psychometric parameters (2PL IRT)
        has_invalid_metadata = False
        if item.a is None or item.a <= 0.0:
            issues.append(f"Invalid discrimination a={item.a} (must be > 0)")
            has_invalid_metadata = True
            is_adaptive = False
        if item.b is None or item.b < -4.0 or item.b > 4.0:
            issues.append(f"Difficulty b={item.b} out of typical bounds [-4.0, 4.0]")
            has_invalid_metadata = True
            is_adaptive = False

        if item.state != ItemState.ACTIVE:
            is_usable = False
            is_adaptive = False

        return {
            "item_id": item.id,
            "topic_id": topic_info["topic_id"] if topic_info else None,
            "topic_name": topic_info["topic_name"] if topic_info else None,
            "domain_id": topic_info["domain_id"] if topic_info else None,
            "domain_name": topic_info["domain_name"] if topic_info else None,
            "is_usable": is_usable,
            "is_adaptive": is_adaptive,
            "has_invalid_metadata": has_invalid_metadata,
            "issues": issues,
            "state": item.state.value if hasattr(item.state, 'value') else str(item.state),
            "a": item.a,
            "b": item.b,
            "stem_normalized": QuestionBankValidator.normalize_stem(item.stem)
        }

    @classmethod
    def validate_all(cls, db: Session) -> Dict[str, Any]:
        """Runs validation audit across all topics and items in the database."""
        # 1. Build skill-to-topic and topic-to-domain map
        skills_query = (
            db.query(Skill, Subtopic, Topic, Domain)
            .join(Subtopic, Skill.subtopic_id == Subtopic.id)
            .join(Topic, Subtopic.topic_id == Topic.id)
            .join(Domain, Topic.domain_id == Domain.id)
            .all()
        )

        skill_to_topic = {}
        all_topics = {}
        for sk, st, top, dom in skills_query:
            skill_to_topic[sk.id] = {
                "skill_id": sk.id,
                "skill_code": sk.code,
                "skill_name": sk.name,
                "topic_id": top.id,
                "topic_name": top.name,
                "domain_id": dom.id,
                "domain_name": dom.name,
            }
            if top.id not in all_topics:
                all_topics[top.id] = {
                    "topic_id": top.id,
                    "topic_name": top.name,
                    "domain_id": dom.id,
                    "domain_name": dom.name,
                    "skill_ids": set(),
                }
            all_topics[top.id]["skill_ids"].add(sk.id)

        # Include any topics that might not have skills yet
        for top in db.query(Topic).all():
            if top.id not in all_topics:
                dom = db.query(Domain).filter(Domain.id == top.domain_id).first()
                all_topics[top.id] = {
                    "topic_id": top.id,
                    "topic_name": top.name,
                    "domain_id": dom.id if dom else None,
                    "domain_name": dom.name if dom else "Unknown",
                    "skill_ids": set(),
                }

        # 2. Audit all items
        items = db.query(Item).all()
        topic_stats = {
            t_id: {
                "topic_id": t_id,
                "topic_name": t_data["topic_name"],
                "domain_id": t_data["domain_id"],
                "domain_name": t_data["domain_name"],
                "total_questions": 0,
                "valid_usable_questions": 0,
                "adaptive_available_questions": 0,
                "missing_topic_questions": 0,
                "invalid_metadata_questions": 0,
                "duplicate_count": 0,
                "issues": [],
                "item_stems": defaultdict(list)
            }
            for t_id, t_data in all_topics.items()
        }

        unmapped_items = []

        for item in items:
            audit = cls.audit_item(item, skill_to_topic)
            t_id = audit["topic_id"]

            if not t_id or t_id not in topic_stats:
                unmapped_items.append({
                    "item_id": item.id,
                    "stem": item.stem[:80],
                    "issues": audit["issues"]
                })
                continue

            stat = topic_stats[t_id]
            stat["total_questions"] += 1
            if audit["is_usable"]:
                stat["valid_usable_questions"] += 1
            if audit["is_adaptive"]:
                stat["adaptive_available_questions"] += 1
            if audit["has_invalid_metadata"]:
                stat["invalid_metadata_questions"] += 1
            if audit["issues"]:
                stat["issues"].extend([f"Item {item.id[:8]}: {iss}" for iss in audit["issues"]])

            # Track duplicates
            stem_norm = audit["stem_normalized"]
            if stem_norm:
                stat["item_stems"][stem_norm].append(item.id)

        # 3. Compute duplicates per topic and determine health status
        for t_id, stat in topic_stats.items():
            duplicates = []
            for stem_norm, item_ids in stat["item_stems"].items():
                if len(item_ids) > 1:
                    duplicates.append({"stem_preview": stem_norm[:60], "count": len(item_ids), "item_ids": item_ids})
            stat["duplicate_count"] = len(duplicates)
            if duplicates:
                stat["issues"].append(f"Found {len(duplicates)} duplicate stem group(s).")
            # Remove item_stems from final payload for clean output
            del stat["item_stems"]

            usable = stat["valid_usable_questions"]
            if usable >= settings.DEFAULT_TARGET_QUESTIONS:
                stat["status"] = "OPTIMAL"  # 15+ questions
            elif usable >= settings.MIN_USABLE_TOPIC_QUESTIONS:
                stat["status"] = "SUFFICIENT"  # 10-14 questions
            else:
                stat["status"] = "SHORTAGE"  # < 10 questions
                stat["issues"].append(
                    f"Shortage: Only {usable} usable questions (minimum required: {settings.MIN_USABLE_TOPIC_QUESTIONS}, target: {settings.DEFAULT_TARGET_QUESTIONS})."
                )

        topic_list = sorted(topic_stats.values(), key=lambda t: (t["domain_name"] or "", t["topic_name"] or ""))

        # 4. Summary metrics
        total_items = len(items)
        usable_items = sum(t["valid_usable_questions"] for t in topic_list)
        adaptive_items = sum(t["adaptive_available_questions"] for t in topic_list)
        optimal_topics = sum(1 for t in topic_list if t["status"] == "OPTIMAL")
        sufficient_topics = sum(1 for t in topic_list if t["status"] == "SUFFICIENT")
        shortage_topics = sum(1 for t in topic_list if t["status"] == "SHORTAGE")

        return {
            "summary": {
                "total_items_in_database": total_items,
                "total_valid_usable_items": usable_items,
                "total_adaptive_available_items": adaptive_items,
                "unmapped_items_count": len(unmapped_items),
                "total_topics": len(topic_list),
                "topics_meeting_target_15": optimal_topics,
                "topics_meeting_minimum_10": sufficient_topics + optimal_topics,
                "topics_with_shortage": shortage_topics,
                "configured_target_questions": settings.DEFAULT_TARGET_QUESTIONS,
                "configured_min_questions": settings.MIN_USABLE_TOPIC_QUESTIONS,
            },
            "topics": topic_list,
            "unmapped_items": unmapped_items
        }
