import pytest
from app.models.session import SessionKind


def get_authenticated_headers(client, email="assessment_student@example.com") -> dict:
    """Helper fixture to register and log in a student, returning authorization headers."""
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "Assessment Learner",
        "role": "STUDENT"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "Password123!"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_start_session_sanitized_question(client):
    headers = get_authenticated_headers(client, "student_start@example.com")

    # Start adaptive session in DSA domain
    payload = {
        "kind": SessionKind.ADAPTIVE.value,
        "domain_id": "DSA",
        "max_questions": 5
    }
    response = client.post("/api/v1/sessions", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()

    assert "session_id" in data
    assert data["kind"] == "ADAPTIVE"
    first_item = data["first_item"]
    assert first_item is not None
    assert "id" in first_item
    assert "stem" in first_item
    if first_item["item_type"] == "MCQ":
        assert len(first_item["options"]) > 0
    elif first_item["item_type"] == "CODING":
        assert first_item["code_template"] is not None

    # CRITICAL SECURITY CHECK: Ensure answer key and internal explanations are NEVER leaked!
    assert "answer_key" not in first_item
    assert "explanation" not in first_item
    assert "distractor_explanations" not in first_item
    for opt in first_item["options"]:
        assert "is_distractor" not in opt

    # Check Explainable Selection Rationale
    explanation = first_item["selection_explanation"]
    assert explanation is not None
    assert "target_skill_name" in explanation
    assert "selection_strategy" in explanation
    assert "fisher_information_units" in explanation


def test_submit_correct_response_and_ability_update(client):
    headers = get_authenticated_headers(client, "student_correct@example.com")

    # 1. Start session
    start_res = client.post("/api/v1/sessions", json={
        "kind": SessionKind.ADAPTIVE.value,
        "domain_id": "DSA",
        "max_questions": 4
    }, headers=headers)
    session_id = start_res.json()["session_id"]
    first_item = start_res.json()["first_item"]

    # 2. Submit response (Item DSA_ARRAYS Two Sum has answer key C or options)
    submit_payload = {
        "item_id": first_item["id"],
        "response_value": "C",  # Two-pointer O(N) answer
        "latency_ms": 14200,
        "confidence_rating": 3  # High confidence
    }
    resp = client.post(f"/api/v1/sessions/{session_id}/respond", json=submit_payload, headers=headers)
    assert resp.status_code == 200
    res_data = resp.json()

    assert "is_correct" in res_data
    assert "correct_key" in res_data
    assert "explanation" in res_data
    assert "updated_theta" in res_data
    assert "updated_se" in res_data

    # If not completed, next question should be delivered sanitized
    if not res_data["is_completed"]:
        next_item = res_data["next_item"]
        assert next_item is not None
        assert "answer_key" not in next_item


def test_submit_misconception_response_feedback(client):
    headers = get_authenticated_headers(client, "student_miscon@example.com")

    # Start session in QUANT domain
    start_res = client.post("/api/v1/sessions", json={
        "kind": SessionKind.DIAGNOSTIC.value,
        "domain_id": "QUANT",
        "max_questions": 3
    }, headers=headers)
    session_id = start_res.json()["session_id"]
    first_item = start_res.json()["first_item"]

    # Deliberately submit wrong answer distractor 'A'
    submit_payload = {
        "item_id": first_item["id"],
        "response_value": "A",
        "latency_ms": 22000,
        "confidence_rating": 1  # Low confidence
    }
    resp = client.post(f"/api/v1/sessions/{session_id}/respond", json=submit_payload, headers=headers)
    assert resp.status_code == 200
    res_data = resp.json()

    assert res_data["is_correct"] is False
    # Misconception feedback should be provided if distractor has mapped diagnostic rationale
    if res_data["misconception_feedback"]:
        assert len(res_data["misconception_feedback"]) > 5


def test_complete_session_and_next_best_actions(client):
    headers = get_authenticated_headers(client, "student_report@example.com")

    # Start short 2-question session
    start_res = client.post("/api/v1/sessions", json={
        "kind": SessionKind.FIXED.value,
        "domain_id": "DSA",
        "max_questions": 2
    }, headers=headers)
    session_id = start_res.json()["session_id"]
    curr_item = start_res.json()["first_item"]

    # Answer question 1
    resp1 = client.post(f"/api/v1/sessions/{session_id}/respond", json={
        "item_id": curr_item["id"],
        "response_value": "B",
        "latency_ms": 18000,
        "confidence_rating": 2
    }, headers=headers)

    # Answer question 2 to trigger completion
    if not resp1.json()["is_completed"]:
        next_item = resp1.json()["next_item"]
        resp2 = client.post(f"/api/v1/sessions/{session_id}/respond", json={
            "item_id": next_item["id"],
            "response_value": "B",
            "latency_ms": 15000,
            "confidence_rating": 2
        }, headers=headers)
        assert resp2.json()["is_completed"] is True
        report = resp2.json()["report"]
    else:
        report = resp1.json()["report"]

    assert report is not None
    assert report["status"] == "COMPLETED"
    assert "overall_score" in report
    assert "skill_breakdown" in report

    # Verify exactly 3 Next-Best Actions are generated
    actions = report["next_best_actions"]
    assert len(actions) == 3
    action_categories = [a["category"] for a in actions]
    assert action_categories == ["LEARN", "PRACTICE", "REASSESS"]


def test_session_history_endpoint(client):
    headers = get_authenticated_headers(client, "student_hist@example.com")

    # Create a session
    client.post("/api/v1/sessions", json={
        "kind": SessionKind.ADAPTIVE.value,
        "domain_id": "VERBAL",
        "max_questions": 2
    }, headers=headers)

    # Fetch history
    res = client.get("/api/v1/sessions/history/me", headers=headers)
    assert res.status_code == 200
    history = res.json()
    assert len(history) >= 1
    assert "session_id" in history[0]
    assert history[0]["domain_name"] == "Verbal Ability"


def test_coding_item_session_submission(client, db_session):
    from app.models.item import Item, ItemType, ItemState

    headers = get_authenticated_headers(client, "student_coding_session@example.com")

    # Find the seeded coding item in DSA
    coding_item = db_session.query(Item).filter(Item.item_type == ItemType.CODING).first()
    assert coding_item is not None

    # Start session targeting DSA domain
    start_res = client.post("/api/v1/sessions", json={
        "kind": SessionKind.ADAPTIVE.value,
        "domain_id": "DSA",
        "max_questions": 3
    }, headers=headers)
    assert start_res.status_code == 201
    session_id = start_res.json()["session_id"]

    # Submit python code to the session
    resp = client.post(f"/api/v1/sessions/{session_id}/respond", json={
        "item_id": coding_item.id,
        "response_value": "[0, 1]",
        "latency_ms": 25000,
        "confidence_rating": 3
    }, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_correct"] is True
    assert data["correct_key"] == "[0, 1]"
    assert "updated_theta" in data

