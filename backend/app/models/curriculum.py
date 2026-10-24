import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Domain(Base):
    """Top-level learning domain (e.g. Data Structures, Quant, OS, DBMS)"""
    __tablename__ = "domains"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), default="BookOpen")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    topics = relationship("Topic", back_populates="domain", cascade="all, delete-orphan")


class Topic(Base):
    """Broad subject topic within a domain (e.g. Trees & Graphs in DSA)"""
    __tablename__ = "topics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    domain_id = Column(String(36), ForeignKey("domains.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)

    domain = relationship("Domain", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")


class Subtopic(Base):
    """Specific conceptual area within a topic (e.g. Binary Search Trees)"""
    __tablename__ = "subtopics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic_id = Column(String(36), ForeignKey("topics.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)

    topic = relationship("Topic", back_populates="subtopics")
    skills = relationship("Skill", back_populates="subtopic", cascade="all, delete-orphan")


class Skill(Base):
    """Atomic measurable learning objective/competency (e.g. BST In-order Traversal)"""
    __tablename__ = "skills"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    subtopic_id = Column(String(36), ForeignKey("subtopics.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    difficulty_level = Column(Float, default=0.5)  # 0.0 (easiest) to 1.0 (hardest)
    blooms_level = Column(String(50), default="Apply")  # Remember, Understand, Apply, Analyze, Evaluate

    subtopic = relationship("Subtopic", back_populates="skills")
    prerequisites = relationship(
        "SkillEdge",
        foreign_keys="SkillEdge.skill_id",
        back_populates="skill",
        cascade="all, delete-orphan"
    )
    dependents = relationship(
        "SkillEdge",
        foreign_keys="SkillEdge.prereq_id",
        back_populates="prerequisite",
        cascade="all, delete-orphan"
    )


class SkillEdge(Base):
    """Directed acyclic prerequisite edge between two skills."""
    __tablename__ = "skill_edges"

    prereq_id = Column(String(36), ForeignKey("skills.id"), primary_key=True)
    skill_id = Column(String(36), ForeignKey("skills.id"), primary_key=True)
    strength = Column(Float, default=1.0)  # 1.0 = strict prerequisite, 0.5 = recommended

    prerequisite = relationship("Skill", foreign_keys=[prereq_id], back_populates="dependents")
    skill = relationship("Skill", foreign_keys=[skill_id], back_populates="prerequisites")
