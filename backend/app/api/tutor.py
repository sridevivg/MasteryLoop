import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.tutor import TutorChatRequest, TutorChatResponse
from app.agentic.tutor import tutor_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tutor", tags=["Socratic AI Tutor"])


@router.post(
    "/chat",
    response_model=TutorChatResponse,
    summary="Engage with the Socratic AI Tutor across 6 pedagogical modes and 3 languages"
)
def chat_with_tutor(
    request: TutorChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty."
        )

    # Convert conversation history
    history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history]

    response = tutor_service.generate_response(
        message=request.message.strip(),
        mode=request.mode,
        language=request.language,
        user=current_user,
        skill_id=request.skill_id,
        db=db,
        history=history_dicts
    )

    return response


@router.get(
    "/diagnostics",
    summary="Retrieve safe diagnostic status of active AI and retrieval providers"
)
def get_tutor_diagnostics(
    current_user: User = Depends(get_current_user)
):
    from app.agentic.llm_client import get_ai_diagnostics
    return get_ai_diagnostics()
