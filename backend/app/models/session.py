import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, JSON, Enum as SQLEnum
from app.core.database import Base


class SessionKind(str, Enum):
    DIAGNOSTIC = "DIAGNOSTIC"
    FIXED = "FIXED"
    ADAPTIVE = "ADAPTIVE"
    PRACTICE = "PRACTICE"


class SessionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class AssessmentSession(Base):
    """An assessment or practice test session taken by a learner."""
    __tablename__ = "assessment_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    domain_id = Column(String(36), ForeignKey("domains.id"), nullable=True, index=True)
    topic_id = Column(String(36), ForeignKey("topics.id"), nullable=True, index=True)
    kind = Column(SQLEnum(SessionKind), default=SessionKind.ADAPTIVE, nullable=False)
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.ACTIVE, nullable=False)

    # Current Ability Estimate (IRT Theta) and Standard Error (SE)
    theta = Column(Float, default=0.0)  # logit ability (0.0 = average)
    se = Column(Float, default=1.0)     # standard error (decreases as more items answered)

    # State tracking
    asked_item_ids = Column(JSON, default=list)  # List of UUID strings
    state_data = Column(JSON, default=dict)      # Internal state (target_se, item_cap, pilot_count, etc.)
    report_data = Column(JSON, default=dict)     # Final generated report after completion

    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
