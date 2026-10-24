import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, JSON, Boolean, Text, Enum as SQLEnum
from app.core.database import Base


class ActionCategory(str, Enum):
    LEARN = "LEARN"
    PRACTICE = "PRACTICE"
    REASSESS = "REASSESS"


class ResourceType(str, Enum):
    NOTES = "NOTES"
    PDF = "PDF"
    VIDEO = "VIDEO"
    DOCUMENTATION = "DOCUMENTATION"
    PRACTICE = "PRACTICE"


class LearnerRoadmap(Base):
    """Personalized prerequisite-aware roadmap with exactly 3 prioritized next-best actions."""
    __tablename__ = "learner_roadmaps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    domain_id = Column(String(36), ForeignKey("domains.id"), nullable=True, index=True)
    
    # List of exactly 3 next-best actions: [{"category": "LEARN", "skill_id": "...", "title": "...", "duration_minutes": 15, "rationale": "...", "action_url": "..."}]
    actions = Column(JSON, default=list, nullable=False)
    
    generated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)


class DailyChallenge(Base):
    """Personalized daily targeted challenge based on weak skills, goals, and recent errors."""
    __tablename__ = "daily_challenges"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    target_skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    item_ids = Column(JSON, default=list)  # 3-5 curated challenge questions
    completed = Column(Boolean, default=False)
    score_percentage = Column(Float, default=0.0)
    target_date = Column(String(10), nullable=False)  # YYYY-MM-DD
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Resource(Base):
    """Verified curriculum learning resource."""
    __tablename__ = "resources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    resource_type = Column(SQLEnum(ResourceType), default=ResourceType.NOTES, nullable=False)
    url = Column(String(500), nullable=True)
    content_summary = Column(Text, nullable=True)
    source_quality = Column(Float, default=0.90)  # Quality score 0.0 to 1.0
    estimated_read_time_min = Column(Integer, default=10)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ClassEnrollment(Base):
    """Enrollment mapping students to classes for teacher dashboards."""
    __tablename__ = "class_enrollments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    class_name = Column(String(100), nullable=False, index=True)
    teacher_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    student_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    enrolled_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
