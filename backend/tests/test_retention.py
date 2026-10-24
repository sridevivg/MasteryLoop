import pytest
from datetime import datetime, timezone, timedelta
from app.intelligence.retention import RetentionEngine, TARGET_RETENTION_THRESHOLD
from app.models.mastery import LearnerSkillMastery
from app.models.curriculum import Skill
from app.schemas.auth import UserRole
from tests.conftest import get_authenticated_headers


def test_ebbinghaus_retention_decay_calculation():
    now = datetime.now(timezone.utc)
    stability = 2.0  # 2 days

    # Immediate recall
    r_immediate = RetentionEngine.calculate_retention(now, stability, as_of=now)
    assert r_immediate == 1.0

    # 1 day elapsed
    r_1day = RetentionEngine.calculate_retention(now, stability, as_of=now + timedelta(days=1))
    assert 0.55 < r_1day < 0.65

    # 5 days elapsed (decayed)
    r_5days = RetentionEngine.calculate_retention(now, stability, as_of=now + timedelta(days=5))
    assert r_5days < 0.15
    assert r_5days > 0.0


def test_stability_growth_on_repeated_success(db_session):
    user_id = "test_retention_user_001"
    skill = db_session.query(Skill).first()
    assert skill is not None

    # First review: correct
    r1 = RetentionEngine.record_review_event(db_session, user_id, skill.id, is_correct=True)
    s1 = RetentionEngine.estimate_stability_from_history(r1)
    assert r1.interaction_count == 1
    assert r1.correct_count == 1

    # Second review: correct -> stability increases
    r2 = RetentionEngine.record_review_event(db_session, user_id, skill.id, is_correct=True)
    s2 = RetentionEngine.estimate_stability_from_history(r2)
    assert s2 > s1

    # Third review: incorrect -> stability penalty / memory lapse
    now_future = datetime.now(timezone.utc) + timedelta(days=3)
    r3 = RetentionEngine.record_review_event(db_session, user_id, skill.id, is_correct=False, reviewed_at=now_future)
    assert r3.correct_count == 2
    assert r3.interaction_count == 3


def test_due_skills_query_identifies_overdue_and_forgetting_risk(db_session):
    user_id = "test_retention_user_002"
    skills = db_session.query(Skill).limit(2).all()
    assert len(skills) >= 2

    # Skill 1 practiced 7 days ago (overdue)
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    RetentionEngine.record_review_event(db_session, user_id, skills[0].id, is_correct=True, reviewed_at=seven_days_ago)

    # Skill 2 practiced 5 minutes ago (fresh, not overdue)
    five_min_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
    RetentionEngine.record_review_event(db_session, user_id, skills[1].id, is_correct=True, reviewed_at=five_min_ago)

    due_list = RetentionEngine.get_due_skills(db_session, user_id)
    due_skill_ids = [d["skill_id"] for d in due_list]

    # Overdue skill must be present in due list
    assert skills[0].id in due_skill_ids
    # Fresh skill should have low forgetting risk and not be priority
    top_due = due_list[0]
    assert top_due["skill_id"] == skills[0].id
    assert top_due["forgetting_risk"] > 0.40


def test_retention_api_endpoints(client):
    headers = get_authenticated_headers(client, "retention_student@example.com")

    # 1. Query due reviews for new student (empty)
    res_due = client.get("/api/v1/mastery/retention/due", headers=headers)
    assert res_due.status_code == 200
    assert "due_skills" in res_due.json()

    # 2. Record review for a skill
    payload = {
        "skill_id": "DSA_ARRAYS",
        "is_correct": True
    }
    res_rev = client.post("/api/v1/mastery/retention/review", json=payload, headers=headers)
    assert res_rev.status_code == 200
    data = res_rev.json()
    assert data["status"] == "success"
    assert data["new_retention_estimate"] == 1.0
    assert "next_review_due" in data
