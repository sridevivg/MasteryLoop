import pytest


def test_register_student_success(client):
    payload = {
        "email": "student_alpha@example.com",
        "password": "Password123!",
        "full_name": "Test Student One",
        "role": "STUDENT",
        "cohort": "2026-AIML"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "student_alpha@example.com"
    assert data["full_name"] == "Test Student One"
    assert data["role"] == "STUDENT"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email_fails(client):
    payload = {
        "email": "student_dup@example.com",
        "password": "Password123!",
        "full_name": "Original Student",
        "role": "STUDENT"
    }
    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    # Second registration with identical email must fail with 400
    res2 = client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"].lower()


def test_register_admin_rejected(client):
    payload = {
        "email": "admin_attempt@example.com",
        "password": "Password123!",
        "full_name": "Attempted Admin",
        "role": "ADMIN"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code in [422, 403]


def test_login_success(client):
    # Register first
    client.post("/api/v1/auth/register", json={
        "email": "student_login@example.com",
        "password": "SecurePassword123!",
        "full_name": "Login Tester",
        "role": "STUDENT"
    })

    # Login
    response = client.post("/api/v1/auth/login", json={
        "email": "student_login@example.com",
        "password": "SecurePassword123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "STUDENT"
    assert data["full_name"] == "Login Tester"


def test_login_invalid_password(client):
    client.post("/api/v1/auth/register", json={
        "email": "student_badpass@example.com",
        "password": "CorrectPassword123!",
        "full_name": "Bad Pass Tester",
        "role": "STUDENT"
    })

    response = client.post("/api/v1/auth/login", json={
        "email": "student_badpass@example.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401
    assert "invalid email or password" in response.json()["detail"].lower()


def test_login_nonexistent_email(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "ghost_user_never_registered@example.com",
        "password": "Password123!"
    })
    assert response.status_code == 401


def test_auth_me_authenticated(client):
    # 1. Register & Login
    client.post("/api/v1/auth/register", json={
        "email": "student_me@example.com",
        "password": "Password123!",
        "full_name": "Me Tester",
        "role": "STUDENT"
    })
    login_res = client.post("/api/v1/auth/login", json={
        "email": "student_me@example.com",
        "password": "Password123!"
    })
    token = login_res.json()["access_token"]

    # 2. Access /auth/me with bearer token
    res = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "student_me@example.com"
    assert data["role"] == "STUDENT"
    assert "password" not in data
    assert "hashed_password" not in data


def test_auth_me_unauthorized(client):
    # Missing token
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401

    # Invalid token
    res2 = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.jwt.token"}
    )
    assert res2.status_code == 401
