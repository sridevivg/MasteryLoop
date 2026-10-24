from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from app.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    full_name: str = Field(..., min_length=2, max_length=150)
    role: UserRole = UserRole.STUDENT
    cohort: Optional[str] = "2026-Batch"

    @field_validator("role")
    @classmethod
    def prevent_admin_self_registration(cls, v: UserRole) -> UserRole:
        if v == UserRole.ADMIN:
            raise ValueError("Registration as ADMIN is not permitted via public registration.")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    full_name: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    cohort: str

    model_config = ConfigDict(from_attributes=True)
