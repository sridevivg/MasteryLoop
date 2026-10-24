import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime, JSON
from app.core.database import Base


class Interaction(Base):
    """Append-only store for learner responses (The Knowledge Tracing training feed)."""
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    interaction_uuid = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, index=True)
    session_id = Column(String(36), ForeignKey("assessment_sessions.id"), nullable=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    item_id = Column(String(36), ForeignKey("items.id"), nullable=False, index=True)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False, index=True)

    # Response Data
    response_value = Column(String(255), nullable=True)
    is_correct = Column(Boolean, nullable=False)
    latency_ms = Column(Integer, default=0)
    confidence_rating = Column(Integer, default=2)  # 1: Low, 2: Medium, 3: High

    # Psychometric flags
    scored = Column(Boolean, default=True)  # False if pilot item
    pilot = Column(Boolean, default=False)
    theta_snapshot = Column(Float, nullable=True)
    se_snapshot = Column(Float, nullable=True)

    # Explainability Data
    selection_rationale = Column(JSON, default=dict)

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
