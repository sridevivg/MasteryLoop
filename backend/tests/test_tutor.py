import pytest
from app.schemas.tutor import TutorMode, TutorLanguage


def get_authenticated_headers(client, email="tutor_student@example.com") -> dict:
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "Tutor Student",
        "role": "STUDENT"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "Password123!"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_tutor_hint_mode_progressive(client):
    headers = get_authenticated_headers(client, "hint_student@example.com")

    payload = {
        "message": "I am stuck on finding pairs with a target sum in a sorted array.",
        "mode": TutorMode.HINT.value,
        "language": TutorLanguage.ENGLISH.value,
        "skill_id": "DSA_ARRAYS"
    }
    res = client.post("/api/v1/tutor/chat", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "HINT"
    assert "Hint 1" in data["response"]
    assert "Hint 2" in data["response"]
    # Ensure answer key is not leaked directly
    assert "answer_key" not in data["response"]
    assert len(data["followup_suggestions"]) > 0


def test_tutor_teach_from_basics(client):
    headers = get_authenticated_headers(client, "basics_student@example.com")

    payload = {
        "message": "Can you explain binary search trees from the beginning?",
        "mode": TutorMode.TEACH_FROM_BASICS.value,
        "language": TutorLanguage.ENGLISH.value,
        "skill_id": "DSA_BST"
    }
    res = client.post("/api/v1/tutor/chat", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "First Principles" in data["response"] or "Fundamental" in data["response"]
    # Check that citations are attached
    assert len(data["citations"]) > 0
    assert "BST" in data["citations"][0]["title"] or "Binary" in data["citations"][0]["title"]


def test_tutor_debug_mode(client):
    headers = get_authenticated_headers(client, "debug_student@example.com")

    payload = {
        "message": "My two pointer while loop is giving index out of bounds error.",
        "mode": TutorMode.DEBUG.value,
        "language": TutorLanguage.ENGLISH.value,
        "skill_id": "DSA_ARRAYS"
    }
    res = client.post("/api/v1/tutor/chat", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "Debugging" in data["response"]
    assert "Boundaries" in data["response"] or "Off-by-One" in data["response"]


def test_tutor_interview_mode(client):
    headers = get_authenticated_headers(client, "interview_student@example.com")

    payload = {
        "message": "Ready for my DSA placement interview.",
        "mode": TutorMode.INTERVIEW.value,
        "language": TutorLanguage.ENGLISH.value,
        "skill_id": "DSA_BST"
    }
    res = client.post("/api/v1/tutor/chat", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "Interview" in data["response"]
    assert "Complexity" in data["response"] or "trade-offs" in data["response"]


def test_tutor_quick_revision_mode(client):
    headers = get_authenticated_headers(client, "rev_student@example.com")

    payload = {
        "message": "Give me quick notes on ACID and normalization.",
        "mode": TutorMode.QUICK_REVISION.value,
        "language": TutorLanguage.ENGLISH.value,
        "skill_id": "DBMS_NORMALIZATION"
    }
    res = client.post("/api/v1/tutor/chat", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "Quick Revision" in data["response"]
    assert "Key Takeaways" in data["response"]


def test_tutor_exam_mode_answer_protection(client):
    headers = get_authenticated_headers(client, "exam_student@example.com")

    payload = {
        "message": "Give me exam practice questions on deadlock conditions.",
        "mode": TutorMode.EXAM_MODE.value,
        "language": TutorLanguage.ENGLISH.value,
        "skill_id": "OS_SYNC_DEADLOCK"
    }
    res = client.post("/api/v1/tutor/chat", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "Exam Mode" in data["response"]
    # Verify explicitly that answer keys are not leaked in exam mode
    assert "answer key" not in data["response"].lower() or "restricted" in data["response"].lower()

    # Also test EXAM string value directly
    payload_exam = {
        "message": "Start mock exam for BST",
        "mode": TutorMode.EXAM.value,
        "language": TutorLanguage.ENGLISH.value,
        "skill_id": "DSA_BST"
    }
    res_exam = client.post("/api/v1/tutor/chat", json=payload_exam, headers=headers)
    assert res_exam.status_code == 200
    assert "Exam Mode" in res_exam.json()["response"]


def test_tutor_multilingual_tamil_and_tanglish(client):
    headers = get_authenticated_headers(client, "multi_student@example.com")

    # 1. Tamil
    res_ta = client.post("/api/v1/tutor/chat", json={
        "message": "Two pointer pathi solluங்க",
        "mode": TutorMode.HINT.value,
        "language": TutorLanguage.TAMIL.value,
        "skill_id": "DSA_ARRAYS"
    }, headers=headers)
    assert res_ta.status_code == 200
    assert res_ta.json()["language"] == "TAMIL"
    assert "குறிப்பு" in res_ta.json()["response"]

    # 2. Tanglish
    res_tg = client.post("/api/v1/tutor/chat", json={
        "message": "Two pointer epdi work aagum?",
        "mode": TutorMode.TEACH_FROM_BASICS.value,
        "language": TutorLanguage.TANGLISH.value,
        "skill_id": "DSA_ARRAYS"
    }, headers=headers)
    assert res_tg.status_code == 200
    assert res_tg.json()["language"] == "TANGLISH"
    assert "padikalam" in res_tg.json()["response"]


def test_tutor_empty_message_rejected(client):
    headers = get_authenticated_headers(client, "empty_student@example.com")

    res = client.post("/api/v1/tutor/chat", json={
        "message": "   ",
        "mode": TutorMode.HINT.value
    }, headers=headers)
    assert res.status_code == 400
