import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from app.main import app
from app.core.database import engine, check_db_health
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token


@pytest.fixture
def client():
    return TestClient(app)


def test_password_hashing_and_verification():
    raw = "LearnerPass@2026!"
    hashed = get_password_hash(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_generation_and_decoding():
    payload = {"sub": "user-uuid-123", "role": "STUDENT"}
    token = create_access_token(payload)
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user-uuid-123"
    assert decoded["role"] == "STUDENT"
    assert "exp" in decoded


def test_database_health_check():
    health = check_db_health()
    assert health["status"] == "healthy"
    assert "latency_ms" in health
    assert health["latency_ms"] >= 0


def test_all_expected_tables_exist():
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    expected_tables = {
        "users",
        "domains",
        "topics",
        "subtopics",
        "skills",
        "skill_edges",
        "items",
        "item_param_history",
        "assessment_sessions",
        "interactions",
        "learner_skill_mastery",
        "review_actions",
        "integrity_cases",
        "learner_roadmaps",
        "daily_challenges",
        "resources",
        "class_enrollments"
    }
    missing = expected_tables - tables
    assert len(missing) == 0, f"Missing database tables: {missing}"


def test_health_api_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "MasteryLoop"
    assert data["database"]["status"] == "healthy"


def test_api_v1_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["features"]["knowledge_tracing"] == "ready"
    assert data["features"]["adaptive_assessment"] == "ready"
