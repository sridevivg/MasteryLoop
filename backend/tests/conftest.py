import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app
from app.seed.curriculum_seed import seed_curriculum
from app.seed.question_seed import seed_questions
from app.seed.rag_seed import seed_rag_knowledge

# Use in-memory SQLite with StaticPool so all threads share the exact same in-memory database instance
TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create all tables and seed curriculum in the shared in-memory test database."""
    import app.models  # ensure models are registered
    Base.metadata.create_all(bind=test_engine)
    with TestingSessionLocal() as session:
        seed_curriculum(session)
        seed_questions(session)
        seed_rag_knowledge(session)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    """Provides a transactional database session for an individual test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Provides a TestClient with overridden get_db dependency pointing to test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def get_authenticated_headers(client, email="test_user@example.com", role="STUDENT") -> dict:
    """Helper to register and login user, returning Authorization Bearer headers."""
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "Test User",
        "role": role,
        "cohort": "2026-Batch"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "Password123!"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

