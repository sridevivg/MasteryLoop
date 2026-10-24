import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, DateTime, JSON, Enum as SQLEnum
from app.core.database import Base


class ItemState(str, Enum):
    GENERATED = "GENERATED"
    VALIDATING = "VALIDATING"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    APPROVED = "APPROVED"
    PILOT = "PILOT"
    CALIBRATED = "CALIBRATED"
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"
    REJECTED = "REJECTED"


class ItemOrigin(str, Enum):
    HUMAN = "HUMAN"
    AI = "AI"


class ItemType(str, Enum):
    MCQ = "MCQ"
    CODING = "CODING"
    NUMERIC = "NUMERIC"


class Item(Base):
    """Assessment item with full psychometric validation lifecycle and provenance."""
    __tablename__ = "items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_type = Column(SQLEnum(ItemType), default=ItemType.MCQ, nullable=False)
    primary_skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False, index=True)
    secondary_skill_ids = Column(JSON, default=list)  # list of skill ids

    # Content
    stem = Column(Text, nullable=False)  # Markdown text / question prompt
    options = Column(JSON, default=list)  # [{"id": "A", "text": "...", "is_distractor": True}]
    answer_key = Column(String(50), nullable=False)  # "A" or expected numeric/code answer
    explanation = Column(Text, nullable=True)
    distractor_explanations = Column(JSON, default=dict)  # {"B": "Calculation error", "C": "Misconception..."}

    # Coding specific fields
    code_template = Column(Text, nullable=True)
    test_cases = Column(JSON, default=list)  # [{"input": "...", "expected": "...", "hidden": False}]

    # Psychometrics (2PL IRT Parameters)
    a = Column(Float, default=1.0)  # Discrimination parameter (higher separates ability better)
    b = Column(Float, default=0.0)  # Difficulty parameter in logits (typically -3.0 to +3.0)
    point_biserial = Column(Float, default=0.35)  # Correlation with overall score
    param_version = Column(Integer, default=1)
    is_calibrated = Column(Integer, default=0)  # 0 = provisional, 1 = statistically calibrated
    exposure_count = Column(Integer, default=0)

    # Lifecycle & Provenance
    state = Column(SQLEnum(ItemState), default=ItemState.ACTIVE, index=True, nullable=False)
    origin = Column(SQLEnum(ItemOrigin), default=ItemOrigin.HUMAN, nullable=False)
    lineage = Column(JSON, default=dict)  # {prompt_id, screening_scores, solver_verdict, citations}

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class ItemParamHistory(Base):
    """Historical record of IRT calibration fits per question."""
    __tablename__ = "item_param_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String(36), ForeignKey("items.id"), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    point_biserial = Column(Float, nullable=True)
    n_responses = Column(Integer, default=0)
    calibration_method = Column(String(50), default="EM_2PL")
    fitted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
