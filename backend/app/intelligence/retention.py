"""
Spaced Repetition and Cognitive Retention Engine for MasteryLoop.
Implements the Ebbinghaus Exponential Memory Decay and Half-Life Stability Model:
R(t) = exp(-t / S)
where:
  - t: Elapsed time since last practice (in days)
  - S: Memory stability factor (days until retention drops to 1/e ~ 36.8%)
  - R(t): Probability of successfully recalling the concept at time t

Provides:
  - Dynamic retention calculation based on UTC timestamps
  - Adaptive review interval scheduling (SM-2 / Half-life hybrid)
  - Forgetting-risk prioritization for learner dashboards
"""

import math
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.mastery import LearnerSkillMastery
from app.models.curriculum import Skill, Domain, Topic, Subtopic

logger = logging.getLogger(__name__)

# Target retention threshold when a review is recommended
TARGET_RETENTION_THRESHOLD = 0.70
MIN_STABILITY_DAYS = 0.5
MAX_STABILITY_DAYS = 180.0


class RetentionEngine:
    """Manages memory retention modeling and spaced repetition revision schedules."""

    @staticmethod
    def calculate_retention(last_practiced_at: Optional[datetime], stability_days: float, as_of: Optional[datetime] = None) -> float:
        """
        Calculates current retention probability R(t) in [0.0, 1.0].
        R(t) = exp(-elapsed_days / stability_days)
        """
        if not last_practiced_at:
            return 1.0

        now = as_of or datetime.now(timezone.utc)
        if last_practiced_at.tzinfo is None:
            # Assume UTC if naive
            last_practiced = last_practiced_at.replace(tzinfo=timezone.utc)
        else:
            last_practiced = last_practiced_at

        elapsed_seconds = max(0.0, (now - last_practiced).total_seconds())
        elapsed_days = elapsed_seconds / 86400.0

        stability = max(MIN_STABILITY_DAYS, stability_days)
        retention = math.exp(-elapsed_days / stability)
        return max(0.01, min(1.0, round(retention, 4)))

    @staticmethod
    def estimate_stability_from_history(mastery_record: LearnerSkillMastery) -> float:
        """
        Estimates memory stability S (in days) based on mastery estimate,
        interaction volume, and historical accuracy.
        """
        # Base stability starts at 1 day
        consecutive_success = max(0, mastery_record.correct_count)
        estimate = max(0.1, mastery_record.estimate)

        # Multiplicative scaling per practice: S = S_0 * (1.8 ^ successful_reviews) * estimate
        base_s = 1.0
        stability = base_s * math.pow(1.8, min(consecutive_success, 8)) * estimate
        return max(MIN_STABILITY_DAYS, min(MAX_STABILITY_DAYS, round(stability, 2)))

    @staticmethod
    def compute_next_due_date(last_practiced_at: datetime, stability_days: float) -> datetime:
        """
        Computes the UTC timestamp when retention will hit TARGET_RETENTION_THRESHOLD.
        R = exp(-t / S) => t = -S * ln(R)
        """
        if last_practiced_at.tzinfo is None:
            last_practiced = last_practiced_at.replace(tzinfo=timezone.utc)
        else:
            last_practiced = last_practiced_at

        days_until_threshold = -stability_days * math.log(TARGET_RETENTION_THRESHOLD)
        days_until_threshold = max(0.25, days_until_threshold)  # At least 6 hours
        return last_practiced + timedelta(days=days_until_threshold)

    @staticmethod
    def record_review_event(
        db: Session,
        user_id: str,
        skill_id: str,
        is_correct: bool,
        reviewed_at: Optional[datetime] = None
    ) -> LearnerSkillMastery:
        """
        Updates learner mastery retention after a practice or review interaction.
        Idempotent and persists updated due date and stability.
        """
        now = reviewed_at or datetime.now(timezone.utc)

        record = db.query(LearnerSkillMastery).filter(
            LearnerSkillMastery.user_id == user_id,
            LearnerSkillMastery.skill_id == skill_id
        ).first()

        if not record:
            record = LearnerSkillMastery(
                user_id=user_id,
                skill_id=skill_id,
                estimate=0.60 if is_correct else 0.40,
                confidence=0.30,
                interaction_count=1,
                correct_count=1 if is_correct else 0,
                last_practiced_at=now,
                history=[]
            )
            db.add(record)
            db.flush()
        else:
            record.interaction_count += 1
            if is_correct:
                record.correct_count += 1
            record.last_practiced_at = now

        # Update stability
        current_stability = RetentionEngine.estimate_stability_from_history(record)
        if not is_correct:
            # Memory lapse penalty: cut stability in half
            current_stability = max(MIN_STABILITY_DAYS, current_stability * 0.5)

        record.retention_estimate = 1.0  # Freshly reviewed
        record.next_review_due = RetentionEngine.compute_next_due_date(now, current_stability)

        # Append audit entry to history JSON
        audit_entry = {
            "event": "SPACED_REVIEW",
            "timestamp": now.isoformat(),
            "is_correct": is_correct,
            "stability_days": current_stability,
            "next_due": record.next_review_due.isoformat()
        }
        hist = list(record.history or [])
        hist.append(audit_entry)
        record.history = hist[-20:]  # Keep last 20 events

        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_due_skills(
        db: Session,
        user_id: str,
        as_of: Optional[datetime] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetches all skills due for spaced revision for a learner.
        Ranks by forgetting risk: (1.0 - current_retention) descending.
        """
        now = as_of or datetime.now(timezone.utc)

        records = (
            db.query(LearnerSkillMastery, Skill, Subtopic, Topic, Domain)
            .join(Skill, LearnerSkillMastery.skill_id == Skill.id)
            .join(Subtopic, Skill.subtopic_id == Subtopic.id)
            .join(Topic, Subtopic.topic_id == Topic.id)
            .join(Domain, Topic.domain_id == Domain.id)
            .filter(LearnerSkillMastery.user_id == user_id)
            .all()
        )

        due_items = []
        for mastery, skill, subtopic, topic, domain in records:
            stability = RetentionEngine.estimate_stability_from_history(mastery)
            current_retention = RetentionEngine.calculate_retention(
                mastery.last_practiced_at,
                stability,
                as_of=now
            )

            # Check if overdue by date OR retention fell below threshold
            is_overdue = False
            if mastery.next_review_due:
                due_tz = mastery.next_review_due.replace(tzinfo=timezone.utc) if mastery.next_review_due.tzinfo is None else mastery.next_review_due
                is_overdue = now >= due_tz
            else:
                is_overdue = current_retention < TARGET_RETENTION_THRESHOLD

            if is_overdue or current_retention < TARGET_RETENTION_THRESHOLD:
                forgetting_risk = round(1.0 - current_retention, 4)
                days_overdue = 0.0
                if mastery.next_review_due:
                    due_tz = mastery.next_review_due.replace(tzinfo=timezone.utc) if mastery.next_review_due.tzinfo is None else mastery.next_review_due
                    if now > due_tz:
                        days_overdue = round((now - due_tz).total_seconds() / 86400.0, 1)

                due_items.append({
                    "skill_id": skill.id,
                    "skill_code": skill.code,
                    "skill_name": skill.name,
                    "domain_name": domain.name,
                    "topic_name": topic.name,
                    "mastery_estimate": round(mastery.estimate, 3),
                    "retention_estimate": current_retention,
                    "current_retention": current_retention,
                    "forgetting_risk": forgetting_risk,
                    "stability_days": stability,
                    "is_overdue": is_overdue,
                    "days_overdue": days_overdue,
                    "interaction_count": mastery.interaction_count or 1,
                    "last_practiced_at": mastery.last_practiced_at.isoformat() if mastery.last_practiced_at else None,
                    "next_review_due": mastery.next_review_due.isoformat() if mastery.next_review_due else None,
                    "urgency": "HIGH" if forgetting_risk > 0.45 else "MEDIUM"
                })

        # Sort highest forgetting risk first
        due_items.sort(key=lambda x: x["forgetting_risk"], reverse=True)
        return due_items[:limit]
