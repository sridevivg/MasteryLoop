import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.item import Item, ItemState
from app.models.review import ReviewAction, ReviewActionType
from app.schemas.item import (
    ItemResponse,
    GenerateItemRequest,
    ItemReviewRequest
)
from app.agentic.item_factory import ItemFactory

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/items", tags=["Question Bank & Quality Control Lifecycle"])


@router.post(
    "/generate",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Draft an AI-generated question grounded in curriculum chunks (Enters automated screening)"
)
def generate_draft_item(
    request: GenerateItemRequest,
    current_user: User = Depends(require_roles([UserRole.TEACHER.value, UserRole.ADMIN.value])),
    db: Session = Depends(get_db)
):
    try:
        item = ItemFactory.generate_draft_item(
            skill_id=request.skill_id,
            difficulty_band=request.difficulty_band,
            item_type=request.item_type,
            db=db,
            author_id=current_user.id
        )
        return item
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/review-queue",
    response_model=List[ItemResponse],
    summary="Get questions awaiting human SME review (HUMAN_REVIEW status)"
)
def get_items_in_review_queue(
    current_user: User = Depends(require_roles([UserRole.TEACHER.value, UserRole.ADMIN.value])),
    db: Session = Depends(get_db)
):
    items = db.query(Item).filter(Item.state == ItemState.HUMAN_REVIEW).order_by(Item.created_at.desc()).all()
    return items


@router.post(
    "/{item_id}/review",
    response_model=ItemResponse,
    summary="Submit SME review decision (APPROVE, EDIT, REJECT, REQUEST_REGEN)"
)
def submit_item_review(
    item_id: str,
    review_in: ItemReviewRequest,
    current_user: User = Depends(require_roles([UserRole.TEACHER.value, UserRole.ADMIN.value])),
    db: Session = Depends(get_db)
):
    try:
        action_enum = ReviewActionType[review_in.action.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid review action '{review_in.action}'. Allowed: APPROVE, EDIT, REJECT, REQUEST_REGEN"
        )

    try:
        updated_item = ItemFactory.review_item(
            item_id=item_id,
            action=action_enum,
            reason=review_in.reason,
            reviewer=current_user,
            db=db,
            edits=review_in.edits
        )
        return updated_item
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get(
    "/{item_id}/lineage",
    summary="Get complete psychometric lineage, screening scores, and review history for an item"
)
def get_item_lineage(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")

    reviews = db.query(ReviewAction, User).join(
        User, ReviewAction.reviewer_id == User.id
    ).filter(
        ReviewAction.item_id == item.id
    ).order_by(ReviewAction.created_at.asc()).all()

    review_history = [
        {
            "action": rev.action.value,
            "reviewer_name": u.full_name,
            "reviewer_role": u.role.value,
            "reason": rev.reason,
            "diff": rev.diff,
            "reviewed_at": rev.created_at.isoformat()
        }
        for rev, u in reviews
    ]

    return {
        "item_id": item.id,
        "state": item.state.value,
        "origin": item.origin.value,
        "is_calibrated": bool(item.is_calibrated),
        "a_discrimination": item.a,
        "b_difficulty": item.b,
        "point_biserial": item.point_biserial,
        "exposure_count": item.exposure_count,
        "lineage": item.lineage,
        "review_history": review_history
    }
