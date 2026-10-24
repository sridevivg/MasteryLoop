import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, JSON, UniqueConstraint
from app.core.database import Base


class LearnerSkillMastery(Base):
    """
    Skill-level mastery state for a learner.
    
    Metrics breakdown:
    - estimate: Posterior mastery probability [0.0 to 1.0] from Knowledge Tracing (BKT or SAKT).
    - confidence: Epistemic confidence in the estimate based on evidence volume & consistency.
    - raw_accuracy: Historical proportion of correct answers on this skill.
    - irt_ability: Calibrated IRT theta converted to local skill ability scale.
    - retention_estimate: Spaced-repetition memory retention probability [0.0 to 1.0] decaying over time.
    """
    __tablename__ = "learner_skill_mastery"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False, index=True)

    # Core Metrics
    estimate = Column(Float, default=0.50, nullable=False)        # KT posterior mastery probability [0-1]
    confidence = Column(Float, default=0.20, nullable=False)      # Confidence in assessment [0-1]
    raw_accuracy = Column(Float, default=0.0)                     # Simple fraction correct
    irt_ability = Column(Float, default=0.0)                      # Calibrated ability theta
    retention_estimate = Column(Float, default=1.0)               # Estimated memory retention

    # Activity Counters
    interaction_count = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    last_practiced_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    next_review_due = Column(DateTime, nullable=True)

    # Model provenance and audit history
    model_version = Column(String(50), default="BKT-1.0")
    history = Column(JSON, default=list)  # [{"timestamp": "...", "estimate": 0.65, "delta": +0.15, "event": "..."}]

    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill_mastery"),
    )
