import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, String, ForeignKey, DateTime, JSON, Text, Enum as SQLEnum
from app.core.database import Base


class ReviewActionType(str, Enum):
    APPROVE = "APPROVE"
    EDIT = "EDIT"
    REJECT = "REJECT"
    REQUEST_REGEN = "REQUEST_REGEN"


class IntegrityKind(str, Enum):
    RAPID_GUESSING = "RAPID_GUESSING"
    SIMILARITY = "SIMILARITY"
    ACCURACY_JUMP = "ACCURACY_JUMP"


class IntegrityStatus(str, Enum):
    OPEN = "OPEN"
    REVIEWED = "REVIEWED"
    DISMISSED = "DISMISSED"


class ReviewAction(Base):
    """Auditable log of SME / Teacher review decisions on generated or updated questions."""
    __tablename__ = "review_actions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String(36), ForeignKey("items.id"), nullable=False, index=True)
    reviewer_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    action = Column(SQLEnum(ReviewActionType), nullable=False)
    reason = Column(Text, nullable=False)
    diff = Column(JSON, default=dict)  # Records field-by-field modifications made during review

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class IntegrityCase(Base):
    """Advisory anomaly case flagged by response-time or pattern analytics for teacher review."""
    __tablename__ = "integrity_cases"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String(36), ForeignKey("assessment_sessions.id"), nullable=True, index=True)
    kind = Column(SQLEnum(IntegrityKind), nullable=False)
    evidence = Column(JSON, default=dict)  # Latency distributions, benchmark thresholds, similarities
    status = Column(SQLEnum(IntegrityStatus), default=IntegrityStatus.OPEN, nullable=False)
    reviewed_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
