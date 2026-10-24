import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)
from app.models.user import User, UserRole
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new learner or teacher account"
)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if email already registered
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    # 2. Prevent ADMIN role creation from public registration endpoint
    if user_in.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Creating administrative accounts via public registration is prohibited."
        )

    # 3. Create new user with hashed password
    hashed_pwd = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email.lower(),
        hashed_password=hashed_pwd,
        full_name=user_in.full_name.strip(),
        role=user_in.role,
        cohort=user_in.cohort or "2026-Batch"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info(f"Registered new user account: {db_user.email} (Role: {db_user.role})")
    return db_user


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate with email and password to receive access token"
)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email.lower()).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "role": user.role.value if hasattr(user.role, 'value') else str(user.role)},
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        role=user.role.value if hasattr(user.role, 'value') else str(user.role),
        full_name=user.full_name
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get authenticated user's profile"
)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user
