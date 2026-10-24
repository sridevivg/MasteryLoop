from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel


class TutorMode(str, Enum):
    HINT = "HINT"
    TEACH_FROM_BASICS = "TEACH_FROM_BASICS"
    DEBUG = "DEBUG"
    INTERVIEW = "INTERVIEW"
    QUICK_REVISION = "QUICK_REVISION"
    EXAM = "EXAM"
    EXAM_MODE = "EXAM_MODE"


class TutorLanguage(str, Enum):
    ENGLISH = "ENGLISH"
    TAMIL = "TAMIL"
    TANGLISH = "TANGLISH"


class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str


class TutorChatRequest(BaseModel):
    message: str
    mode: TutorMode = TutorMode.TEACH_FROM_BASICS
    language: TutorLanguage = TutorLanguage.ENGLISH
    skill_id: Optional[str] = None
    item_id: Optional[str] = None
    history: List[ChatMessage] = []


class SourceCitation(BaseModel):
    title: str
    chunk_text: str
    relevance_score: float
    domain: Optional[str] = None


class TutorChatResponse(BaseModel):
    response: str
    mode: TutorMode
    language: TutorLanguage
    citations: List[SourceCitation] = []
    followup_suggestions: List[str] = []
    provider_used: Optional[str] = "mock:pedagogical-engine"
