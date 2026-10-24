import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.item import Item
from app.intelligence.coding_sandbox import execute_sandboxed_code

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/coding", tags=["Coding Execution Sandbox"])


class CodingSubmissionRequest(BaseModel):
    code: str = Field(..., description="Student code to evaluate")
    language: str = Field("python", description="Programming language (e.g. python)")
    item_id: Optional[str] = Field(None, description="Optional Item ID to fetch associated test cases from question bank")
    test_cases: Optional[List[Dict[str, Any]]] = Field(None, description="Optional custom test cases if item_id not provided")


@router.post(
    "/execute",
    summary="Safely execute learner code submission against test cases in an isolated sandbox"
)
def execute_coding_submission(
    payload: CodingSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not payload.code or not payload.code.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submitted code cannot be empty."
        )

    test_cases = payload.test_cases or []

    # If item_id provided, load verified test cases from database item
    if payload.item_id:
        item = db.query(Item).filter(Item.id == payload.item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Coding item '{payload.item_id}' not found."
            )
        if item.test_cases:
            test_cases = item.test_cases

    if not test_cases:
        # Default fallback test case for simple stdout checking
        test_cases = [{"input": "", "expected_output": "", "is_hidden": False}]

    result = execute_sandboxed_code(
        code=payload.code,
        test_cases=test_cases,
        language=payload.language
    )

    return result
