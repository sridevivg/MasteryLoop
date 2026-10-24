import pytest
from app.models.user import UserRole
from app.models.item import ItemState, ItemType


def get_token_for_role(client, email: str, role: UserRole) -> dict:
    """Helper to provision a user with a specific role for testing RBAC."""
    # Register regular user
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": f"{role.value} User",
        "role": UserRole.TEACHER.value if role in [UserRole.TEACHER, UserRole.ADMIN] else UserRole.STUDENT.value
    })
    res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "Password123!"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_ai_draft_item_generation_and_screening(client):
    headers_teacher = get_token_for_role(client, "teacher_gen@example.com", UserRole.TEACHER)

    payload = {
        "skill_id": "DSA_BST",
        "difficulty_band": "medium",
        "item_type": ItemType.MCQ.value
    }
    response = client.post("/api/v1/items/generate", json=payload, headers=headers_teacher)
    assert response.status_code == 201
    data = response.json()

    assert data["origin"] == "AI"
    # Automated screening must promote to HUMAN_REVIEW (or REJECTED), never directly ACTIVE!
    assert data["state"] == "HUMAN_REVIEW"
    assert data["is_calibrated"] == 0  # Marked provisional

    # Verify Lineage & Blind Solver Check
    lineage = data["lineage"]
    assert lineage is not None
    assert "screening_scores" in lineage
    scores = lineage["screening_scores"]
    assert scores["blind_solver_check"] == "PASS"
    assert scores["distinct_options"] is True


def test_student_forbidden_from_item_generation_and_review(client):
    headers_student = get_token_for_role(client, "student_blocked@example.com", UserRole.STUDENT)

    # Attempt to generate item
    res_gen = client.post("/api/v1/items/generate", json={
        "skill_id": "DSA_BST",
        "difficulty_band": "medium"
    }, headers=headers_student)
    assert res_gen.status_code == 403

    # Attempt to view review queue
    res_queue = client.get("/api/v1/items/review-queue", headers=headers_student)
    assert res_queue.status_code == 403


def test_teacher_review_workflow_approval_and_lineage(client):
    headers_teacher = get_token_for_role(client, "teacher_reviewer@example.com", UserRole.TEACHER)

    # 1. Generate an item
    gen_res = client.post("/api/v1/items/generate", json={
        "skill_id": "SQL_JOINS",
        "difficulty_band": "hard"
    }, headers=headers_teacher)
    item_id = gen_res.json()["id"]

    # 2. Check review queue
    queue_res = client.get("/api/v1/items/review-queue", headers=headers_teacher)
    assert queue_res.status_code == 200
    queue_ids = [it["id"] for it in queue_res.json()]
    assert item_id in queue_ids

    # 3. Approve item
    review_payload = {
        "action": "APPROVE",
        "reason": "Clear stem and rigorous distractor explanations matching curriculum standards."
    }
    review_res = client.post(f"/api/v1/items/{item_id}/review", json=review_payload, headers=headers_teacher)
    assert review_res.status_code == 200
    assert review_res.json()["state"] == "APPROVED"

    # 4. Check Lineage and Review History
    lineage_res = client.get(f"/api/v1/items/{item_id}/lineage", headers=headers_teacher)
    assert lineage_res.status_code == 200
    lin_data = lineage_res.json()
    assert lin_data["state"] == "APPROVED"
    assert len(lin_data["review_history"]) >= 1
    first_rev = lin_data["review_history"][0]
    assert first_rev["action"] == "APPROVE"
    assert "curriculum standards" in first_rev["reason"]
