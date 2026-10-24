import pytest
from app.models.session import SessionKind


def get_authenticated_headers(client, email="mastery_student@example.com") -> dict:
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "Mastery Tester",
        "role": "STUDENT"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "Password123!"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_learner_dashboard_endpoint(client):
    headers = get_authenticated_headers(client, "dash_student@example.com")

    response = client.get("/api/v1/mastery/dashboard", headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert "overall_mastery" in data
    assert "placement_readiness" in data
    assert "study_streak_days" in data
    assert "total_assessments_taken" in data
    assert "total_questions_solved" in data

    # Check that 11 placement domains are represented
    assert len(data["placement_domains"]) == 11
    domain_names = {d["domain_name"] for d in data["placement_domains"]}
    assert "Data Structures & Algorithms" in domain_names
    assert "Machine Learning" in domain_names
    assert "Operating Systems" in domain_names

    # Check that exactly 3 Next-Best Actions are present
    actions = data["next_best_actions"]
    assert len(actions) == 3
    categories = [a["category"] for a in actions]
    assert categories == ["LEARN", "PRACTICE", "REASSESS"]

    # Check today's challenge
    assert data["today_challenge"] is not None
    assert "title" in data["today_challenge"]


def test_learner_skills_mastery_detail(client):
    headers = get_authenticated_headers(client, "skills_student@example.com")

    # Take a 1-question session to establish mastery record
    start_res = client.post("/api/v1/sessions", json={
        "kind": SessionKind.ADAPTIVE.value,
        "domain_id": "DSA",
        "max_questions": 1
    }, headers=headers)
    session_id = start_res.json()["session_id"]
    item = start_res.json()["first_item"]

    client.post(f"/api/v1/sessions/{session_id}/respond", json={
        "item_id": item["id"],
        "response_value": "B",
        "latency_ms": 12000,
        "confidence_rating": 3
    }, headers=headers)

    # Fetch granular skills mastery
    res = client.get("/api/v1/mastery/skills", headers=headers)
    assert res.status_code == 200
    skills = res.json()
    assert len(skills) >= 1

    first_s = skills[0]
    assert "skill_id" in first_s
    assert "skill_name" in first_s
    assert "estimate" in first_s
    assert "confidence" in first_s
    assert "raw_accuracy" in first_s
    assert "status" in first_s
    assert first_s["interaction_count"] >= 1


def test_mastery_forecast_endpoint(client):
    headers = get_authenticated_headers(client, "forecast_student@example.com")

    # Call forecast
    payload = {
        "study_hours_per_week": 6.0,
        "forecast_weeks": 4
    }
    res = client.post("/api/v1/mastery/forecast", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "has_sufficient_data" in data
    assert "explanation" in data
    assert "assumptions" in data
    assert len(data["assumptions"]) > 0
