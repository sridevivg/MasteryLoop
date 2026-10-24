import logging
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.curriculum import Domain
from app.models.item import Item, ItemState
from app.models.session import AssessmentSession, SessionKind, SessionStatus
from app.schemas.session import (
    SessionStartRequest,
    SessionStartResponse,
    ItemSubmissionRequest,
    ItemSubmissionResponse
)
from app.services.assessment_engine import AssessmentEngine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sessions", tags=["Adaptive Assessment"])


@router.post(
    "",
    response_model=SessionStartResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start an adaptive, diagnostic, or fixed assessment session"
)
def start_assessment_session(
    request: SessionStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.models.curriculum import Topic, Subtopic, Skill
    from app.core.config import settings

    domain_id = None
    domain_name = None
    topic_id = None
    topic_name = None
    shortage_warning = None

    # 1. Resolve topic if provided
    if request.topic_id:
        topic = db.query(Topic).filter(
            (Topic.id == request.topic_id) | (Topic.name.ilike(request.topic_id))
        ).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Topic '{request.topic_id}' not found."
            )
        topic_id = topic.id
        topic_name = topic.name
        domain = db.query(Domain).filter(Domain.id == topic.domain_id).first()
        if domain:
            domain_id = domain.id
            domain_name = domain.name

        # Count active items belonging to this topic
        available_count = db.query(Item).join(Skill, Item.primary_skill_id == Skill.id)\
            .join(Subtopic, Skill.subtopic_id == Subtopic.id)\
            .filter(Subtopic.topic_id == topic.id, Item.state == ItemState.ACTIVE).count()

        if available_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No active assessment items available for topic '{topic.name}'."
            )

        target_q = request.max_questions or settings.DEFAULT_TARGET_QUESTIONS
        actual_target = min(target_q, available_count)

        if available_count < settings.MIN_USABLE_TOPIC_QUESTIONS:
            shortage_warning = (
                f"Topic '{topic.name}' has only {available_count} questions available "
                f"(recommended minimum: {settings.MIN_USABLE_TOPIC_QUESTIONS})."
            )
        elif available_count < target_q:
            shortage_warning = (
                f"Assessment targeting all {available_count} available questions for topic '{topic.name}'."
            )

    # 2. Resolve domain if topic not provided
    elif request.domain_id:
        domain = db.query(Domain).filter(
            (Domain.id == request.domain_id) | (Domain.code == request.domain_id.upper())
        ).first()
        if not domain:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Domain '{request.domain_id}' not found."
            )
        domain_id = domain.id
        domain_name = domain.name

        available_count = db.query(Item).join(Skill, Item.primary_skill_id == Skill.id)\
            .join(Subtopic, Skill.subtopic_id == Subtopic.id)\
            .join(Topic, Subtopic.topic_id == Topic.id)\
            .filter(Topic.domain_id == domain.id, Item.state == ItemState.ACTIVE).count()

        if available_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No active assessment items available for domain '{domain.name}'."
            )

        target_q = request.max_questions or settings.DEFAULT_TARGET_QUESTIONS
        actual_target = min(target_q, available_count)

    # 3. Comprehensive diagnostic if neither topic nor domain provided
    else:
        domain_name = "Placement Diagnostic"
        available_count = db.query(Item).filter(Item.state == ItemState.ACTIVE).count()
        target_q = request.max_questions or settings.DEFAULT_TARGET_QUESTIONS
        actual_target = min(target_q, available_count)

    # Create new session
    session = AssessmentSession(
        user_id=current_user.id,
        domain_id=domain_id,
        topic_id=topic_id,
        kind=request.kind,
        status=SessionStatus.ACTIVE,
        theta=0.0,
        se=1.0,
        asked_item_ids=[],
        state_data={
            "max_questions": actual_target,
            "target_questions": actual_target,
            "requested_questions": request.max_questions or settings.DEFAULT_TARGET_QUESTIONS,
            "available_questions": available_count,
            "topic_id": topic_id,
            "topic_name": topic_name,
            "domain_name": domain_name,
            "shortage_warning": shortage_warning
        }
    )
    db.add(session)
    db.flush()

    # Select the first question
    first_item, rationale = AssessmentEngine.select_next_question(session, db)
    if not first_item:
        scope_desc = f"topic '{topic_name}'" if topic_name else (f"domain '{domain_name}'" if domain_name else "curriculum")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No active assessment items available for the selected {scope_desc}."
        )

    # Sanitize item view — never leak answer key or explanation
    sanitized_first_item = AssessmentEngine.sanitize_item_for_learner(
        item=first_item,
        question_number=1,
        total_questions_estimated=actual_target,
        selection_explanation=rationale,
        domain_name=domain_name,
        topic_name=topic_name,
        warning=shortage_warning
    )

    db.commit()
    logger.info(
        f"Learner {current_user.email} started {session.kind.value} session {session.id[:8]} "
        f"(topic: {topic_name or 'N/A'}, domain: {domain_name or 'N/A'}, target: {actual_target} items)"
    )

    return SessionStartResponse(
        session_id=session.id,
        kind=session.kind.value,
        domain_name=domain_name,
        topic_name=topic_name,
        total_questions_estimated=actual_target,
        warning=shortage_warning,
        first_item=sanitized_first_item,
        started_at=session.started_at.isoformat()
    )


@router.post(
    "/{session_id}/respond",
    response_model=ItemSubmissionResponse,
    summary="Submit answer, score deterministically, update mastery, and fetch next adaptive question"
)
def submit_item_response(
    session_id: str,
    submission: ItemSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.core.config import settings

    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id,
        AssessmentSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment session not found or access denied."
        )

    if session.status != SessionStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Session is already {session.status.value}. Further responses cannot be recorded."
        )

    item = db.query(Item).filter(Item.id == submission.item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment item not found."
        )

    # Process response, update BKT mastery, and check stopping rules
    result = AssessmentEngine.process_learner_response(
        session=session,
        item=item,
        response_value=submission.response_value,
        latency_ms=submission.latency_ms,
        confidence_rating=submission.confidence_rating or 2,
        db=db
    )

    next_item_view = None
    if not result["is_completed"]:
        next_item, next_rationale = AssessmentEngine.select_next_question(session, db)
        if next_item:
            max_q = (session.state_data or {}).get("max_questions", settings.DEFAULT_TARGET_QUESTIONS)
            next_item_view = AssessmentEngine.sanitize_item_for_learner(
                item=next_item,
                question_number=len(session.asked_item_ids) + 1,
                total_questions_estimated=max_q,
                selection_explanation=next_rationale,
                domain_name=(session.state_data or {}).get("domain_name"),
                topic_name=(session.state_data or {}).get("topic_name"),
                warning=(session.state_data or {}).get("shortage_warning")
            )
        else:
            # Bank exhausted; complete session gracefully
            session.status = SessionStatus.COMPLETED
            session.completed_at = datetime.now(timezone.utc)
            report = AssessmentEngine.generate_performance_report(session, db)
            session.report_data = report
            db.commit()
            result["is_completed"] = True
            result["report"] = report

    return ItemSubmissionResponse(
        is_correct=result["is_correct"],
        correct_key=result["correct_key"],
        explanation=result["explanation"],
        misconception_feedback=result["misconception_feedback"],
        updated_theta=result["updated_theta"],
        updated_se=result["updated_se"],
        next_item=next_item_view,
        is_completed=result["is_completed"],
        report=result.get("report")
    )


@router.get(
    "/{session_id}/current",
    summary="Get current active session state and next question to resume without losing answers"
)
def get_current_session_state(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.core.config import settings

    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id,
        AssessmentSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment session not found or access denied."
        )

    max_q = (session.state_data or {}).get("max_questions", settings.DEFAULT_TARGET_QUESTIONS)
    domain_name = (session.state_data or {}).get("domain_name")
    topic_name = (session.state_data or {}).get("topic_name")
    shortage_warning = (session.state_data or {}).get("shortage_warning")
    questions_answered = len(session.asked_item_ids or [])

    if session.status != SessionStatus.ACTIVE:
        return {
            "session_id": session.id,
            "kind": session.kind.value,
            "status": session.status.value,
            "domain_name": domain_name,
            "topic_name": topic_name,
            "current_question_number": questions_answered,
            "total_questions_estimated": max_q,
            "questions_answered": questions_answered,
            "theta": round(session.theta, 2),
            "current_item": None,
            "is_completed": True,
            "warning": shortage_warning,
            "report": session.report_data
        }

    # If active, fetch the next unasked question
    next_item, next_rationale = AssessmentEngine.select_next_question(session, db)
    current_item_view = None
    if next_item:
        current_item_view = AssessmentEngine.sanitize_item_for_learner(
            item=next_item,
            question_number=questions_answered + 1,
            total_questions_estimated=max_q,
            selection_explanation=next_rationale,
            domain_name=domain_name,
            topic_name=topic_name,
            warning=shortage_warning
        )

    return {
        "session_id": session.id,
        "kind": session.kind.value,
        "status": session.status.value,
        "domain_name": domain_name,
        "topic_name": topic_name,
        "current_question_number": questions_answered + 1,
        "total_questions_estimated": max_q,
        "questions_answered": questions_answered,
        "theta": round(session.theta, 2),
        "current_item": current_item_view,
        "is_completed": current_item_view is None,
        "warning": shortage_warning
    }


@router.get(
    "/{session_id}/report",
    summary="Get comprehensive performance report and learning gap analysis for a completed session"
)
def get_session_report(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id,
        AssessmentSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or access denied."
        )

    if session.status != SessionStatus.COMPLETED or not session.report_data:
        # Generate on demand if completed
        report = AssessmentEngine.generate_performance_report(session, db)
        session.report_data = report
        db.commit()
        return report

    return session.report_data


@router.get(
    "/history/me",
    summary="Get recent assessment sessions history for the current learner"
)
def get_learner_session_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = (
        db.query(AssessmentSession, Domain)
        .outerjoin(Domain, AssessmentSession.domain_id == Domain.id)
        .filter(AssessmentSession.user_id == current_user.id)
        .order_by(AssessmentSession.started_at.desc())
        .limit(20)
        .all()
    )

    history = []
    for s, d in sessions:
        rep = s.report_data or {}
        score_info = rep.get("overall_score", {})
        history.append({
            "session_id": s.id,
            "kind": s.kind.value,
            "status": s.status.value,
            "domain_name": d.name if d else "General Diagnostic",
            "accuracy_percentage": score_info.get("accuracy_percentage"),
            "questions_answered": len(s.asked_item_ids or []),
            "estimated_ability_theta": round(s.theta, 2),
            "started_at": s.started_at.isoformat(),
            "completed_at": s.completed_at.isoformat() if s.completed_at else None
        })
    return history
