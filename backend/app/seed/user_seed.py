"""
Demo Users Seed for MasteryLoop.
Ensures standard demo learner and educator accounts exist out of the box with known credentials.
"""

import logging
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.core.security import get_password_hash

logger = logging.getLogger("masteryloop.user_seed")

DEMO_USERS = [
    {
        "email": "student@masteryloop.ai",
        "full_name": "Alex Mercer (Demo Learner)",
        "password": "Password123!",
        "role": UserRole.STUDENT,
        "cohort": "2026-Batch"
    },
    {
        "email": "teacher@masteryloop.ai",
        "full_name": "Prof. Sarah Connor (SME Reviewer)",
        "password": "Password123!",
        "role": UserRole.TEACHER,
        "cohort": "Faculty-2026"
    },
    {
        "email": "varshini_e2e@masteryloop.ai",
        "full_name": "Varshini Raman",
        "password": "Password123!",
        "role": UserRole.STUDENT,
        "cohort": "2026-Batch"
    }
]


def seed_demo_users(db: Session) -> dict:
    stats = {"created": 0, "existing": 0}

    for u_data in DEMO_USERS:
        existing = db.query(User).filter(User.email == u_data["email"].lower()).first()
        if existing:
            stats["existing"] += 1
            continue

        new_user = User(
            email=u_data["email"].lower(),
            hashed_password=get_password_hash(u_data["password"]),
            full_name=u_data["full_name"],
            role=u_data["role"],
            cohort=u_data["cohort"]
        )
        db.add(new_user)
        stats["created"] += 1

    db.commit()
    logger.info(f"User seeding complete: {stats}")
    return stats
