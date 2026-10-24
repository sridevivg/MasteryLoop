from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.models.session import SessionKind


class SessionStartRequest(BaseModel):
    kind: SessionKind = SessionKind.ADAPTIVE
    domain_id: Optional[str] = None
    topic_id: Optional[str] = None
    target_skill_ids: Optional[List[str]] = None
    max_questions: Optional[int] = None


class LearnerItemView(BaseModel):
    """Sanitized item view for active test taking — NEVER leaks answer key or rationale before answering."""
    id: str
    item_type: str
    stem: str
    options: List[Dict[str, Any]]
    code_template: Optional[str] = None
    visible_test_cases: Optional[List[Dict[str, Any]]] = None
    question_number: int
    total_questions_estimated: int
    domain_name: Optional[str] = None
    topic_name: Optional[str] = None
    warning: Optional[str] = None
    selection_explanation: Optional[Dict[str, Any]] = None  # Explainable adaptive selection details


class SessionStartResponse(BaseModel):
    session_id: str
    kind: str
    domain_name: Optional[str] = None
    topic_name: Optional[str] = None
    total_questions_estimated: int = 15
    warning: Optional[str] = None
    first_item: Optional[LearnerItemView] = None
    started_at: str


class ActiveSessionStatusResponse(BaseModel):
    session_id: str
    kind: str
    status: str
    domain_name: Optional[str] = None
    topic_name: Optional[str] = None
    current_question_number: int
    total_questions_estimated: int
    questions_answered: int
    theta: float
    current_item: Optional[LearnerItemView] = None
    is_completed: bool = False
    warning: Optional[str] = None


class ItemSubmissionRequest(BaseModel):
    item_id: str
    response_value: str
    latency_ms: int
    confidence_rating: Optional[int] = 2  # 1: Low, 2: Medium, 3: High


class ItemSubmissionResponse(BaseModel):
    is_correct: bool
    correct_key: str
    explanation: Optional[str] = None
    misconception_feedback: Optional[str] = None
    updated_theta: float
    updated_se: float
    next_item: Optional[LearnerItemView] = None
    is_completed: bool = False
    report: Optional[Dict[str, Any]] = None
