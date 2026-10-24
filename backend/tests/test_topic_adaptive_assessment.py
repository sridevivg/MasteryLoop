"""
Automated Test Suite for MasteryLoop Topic Question Count & Adaptive Assessment Verification.

Covers:
1. Selecting a topic requests the configured question count (target 15).
2. An assessment with 15+ available questions returns 15 distinct questions without repetition.
3. An assessment with 12 valid questions handles shortage correctly (targets 12 with warning).
4. Fewer than 10 available questions produces a clear warning.
5. All returned questions belong exclusively to the selected topic (strict topic isolation).
6. Response recording and database persistence.
7. Adaptive question selection responds dynamically to updated ability estimates (IRT 2PL + EAP).
8. Active session status and resumption across page refreshes.
"""

import pytest
from app.models.curriculum import Domain, Topic, Subtopic, Skill
from app.models.item import Item, ItemState, ItemType
from app.models.session import SessionKind, AssessmentSession
from app.core.config import settings
from app.psychocore.irt import fisher_information_2pl, estimate_ability_eap
from app.services.assessment_engine import AssessmentEngine
from tests.conftest import get_authenticated_headers


def test_topic_assessment_requests_configured_target(client, db_session):
    """Verify that starting an assessment on a topic targets 15 questions."""
    headers = get_authenticated_headers(client, "test_target15@example.com")

    topic = db_session.query(Topic).first()
    assert topic is not None, "At least one topic must exist in the seeded curriculum."

    payload = {
        "kind": SessionKind.ADAPTIVE.value,
        "topic_id": topic.id,
    }
    response = client.post("/api/v1/sessions", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()

    assert data["session_id"] is not None
    assert data["topic_name"] == topic.name
    assert data["total_questions_estimated"] == settings.DEFAULT_TARGET_QUESTIONS
    assert data["first_item"]["total_questions_estimated"] == settings.DEFAULT_TARGET_QUESTIONS


def test_assessment_delivers_15_distinct_questions_strictly_within_topic(client, db_session):
    """
    Verify that an assessment on a topic with 15+ items:
    - Delivers 15 distinct questions.
    - Never repeats a question.
    - All questions belong to the selected topic.
    - Persists session, answers, and ability estimates to completion.
    """
    headers = get_authenticated_headers(client, "test_15distinct@example.com")

    # Pick a topic with 15+ items (e.g., Linear Data Structures)
    topic = db_session.query(Topic).filter(Topic.name == "Linear Data Structures").first()
    if not topic:
        topic = db_session.query(Topic).first()

    # Get all valid skill IDs for this topic
    topic_skill_ids = set()
    for sub in topic.subtopics:
        for sk in sub.skills:
            topic_skill_ids.add(sk.id)

    # Start session
    start_res = client.post("/api/v1/sessions", json={
        "kind": SessionKind.ADAPTIVE.value,
        "topic_id": topic.id,
    }, headers=headers)
    assert start_res.status_code == 201
    session_data = start_res.json()
    session_id = session_data["session_id"]
    current_item = session_data["first_item"]

    seen_item_ids = []
    question_count = 0

    # Answer all questions until completion
    while current_item and not session_data.get("is_completed"):
        question_count += 1
        item_id = current_item["id"]
        assert item_id not in seen_item_ids, f"Question {item_id} was repeated at step {question_count}!"
        seen_item_ids.append(item_id)

        # Verify item belongs to selected topic
        db_item = db_session.query(Item).filter(Item.id == item_id).first()
        assert db_item is not None
        assert db_item.primary_skill_id in topic_skill_ids, (
            f"Item {item_id} belongs to skill {db_item.primary_skill_id}, not in topic {topic.name}!"
        )

        # Submit answer (alternating A and B)
        resp = client.post(f"/api/v1/sessions/{session_id}/respond", json={
            "item_id": item_id,
            "response_value": "A",
            "latency_ms": 3500,
            "confidence_rating": 2
        }, headers=headers)
        assert resp.status_code == 200
        resp_data = resp.json()

        if resp_data.get("is_completed"):
            break
        current_item = resp_data.get("next_item")

    assert question_count == 15, f"Expected exactly 15 questions answered, but got {question_count}"
    assert len(set(seen_item_ids)) == 15, "All 15 questions must be unique"

    # Verify report is accessible and accurate
    report_res = client.get(f"/api/v1/sessions/{session_id}/report", headers=headers)
    assert report_res.status_code == 200
    report = report_res.json()
    assert report["overall_score"]["total_questions"] == 15
    assert report["topic_name"] == topic.name


def test_shortage_handling_with_12_available_questions(client, db_session):
    """
    Verify that when a topic has only 12 valid questions:
    - Session targets 12 questions.
    - Emits a warning explaining the shortage below preferred 15.
    - Delivers exactly 12 distinct questions without crash or repetition.
    """
    headers = get_authenticated_headers(client, "test_shortage12@example.com")

    # Create a dedicated test topic with 12 items
    domain = db_session.query(Domain).first()
    test_topic = Topic(domain_id=domain.id, name="Test Shortage 12 Topic", order_index=99)
    db_session.add(test_topic)
    db_session.flush()

    subtopic = Subtopic(topic_id=test_topic.id, name="Shortage Subtopic", order_index=1)
    db_session.add(subtopic)
    db_session.flush()

    skill = Skill(subtopic_id=subtopic.id, code="SKILL_SHORT_12", name="Shortage Skill 12", difficulty_level=0.5)
    db_session.add(skill)
    db_session.flush()

    # Add exactly 12 items
    for i in range(12):
        item = Item(
            primary_skill_id=skill.id,
            item_type=ItemType.MCQ,
            stem=f"Shortage question number {i + 1} for 12-item topic test?",
            options=[{"id": "A", "text": "Option A"}, {"id": "B", "text": "Option B"}],
            answer_key="A",
            explanation="Explanation",
            a=1.2,
            b=-1.0 + (i * 0.15),
            point_biserial=0.4,
            is_calibrated=1,
            state=ItemState.ACTIVE,
        )
        db_session.add(item)
    db_session.commit()

    # Start session on the 12-item topic
    start_res = client.post("/api/v1/sessions", json={
        "kind": SessionKind.ADAPTIVE.value,
        "topic_id": test_topic.id,
    }, headers=headers)
    assert start_res.status_code == 201
    data = start_res.json()

    assert data["total_questions_estimated"] == 12
    assert "warning" in data
    assert "all 12 available questions" in data["warning"]

    # Play through all 12 questions
    session_id = data["session_id"]
    current_item = data["first_item"]
    seen = []

    while current_item:
        seen.append(current_item["id"])
        resp = client.post(f"/api/v1/sessions/{session_id}/respond", json={
            "item_id": current_item["id"],
            "response_value": "A",
            "latency_ms": 2000,
        }, headers=headers)
        assert resp.status_code == 200
        r_data = resp.json()
        if r_data.get("is_completed"):
            break
        current_item = r_data.get("next_item")

    assert len(seen) == 12
    assert len(set(seen)) == 12


def test_shortage_warning_below_10_questions(client, db_session):
    """Verify that when a topic has fewer than 10 questions, a shortage warning is issued."""
    headers = get_authenticated_headers(client, "test_shortage5@example.com")

    domain = db_session.query(Domain).first()
    test_topic = Topic(domain_id=domain.id, name="Test Shortage 5 Topic", order_index=100)
    db_session.add(test_topic)
    db_session.flush()

    subtopic = Subtopic(topic_id=test_topic.id, name="Shortage 5 Subtopic", order_index=1)
    db_session.add(subtopic)
    db_session.flush()

    skill = Skill(subtopic_id=subtopic.id, code="SKILL_SHORT_5", name="Shortage Skill 5", difficulty_level=0.5)
    db_session.add(skill)
    db_session.flush()

    # Add only 5 items (< 10)
    for i in range(5):
        item = Item(
            primary_skill_id=skill.id,
            item_type=ItemType.MCQ,
            stem=f"Severe shortage question {i + 1}?",
            options=[{"id": "A", "text": "Option A"}, {"id": "B", "text": "Option B"}],
            answer_key="A",
            explanation="Explanation",
            a=1.2,
            b=-0.5 + (i * 0.2),
            point_biserial=0.4,
            is_calibrated=1,
            state=ItemState.ACTIVE,
        )
        db_session.add(item)
    db_session.commit()

    start_res = client.post("/api/v1/sessions", json={
        "kind": SessionKind.ADAPTIVE.value,
        "topic_id": test_topic.id,
    }, headers=headers)
    assert start_res.status_code == 201
    data = start_res.json()

    assert data["total_questions_estimated"] == 5
    assert "warning" in data
    assert "recommended minimum: 10" in data["warning"]


def test_adaptive_selection_responds_to_ability_estimates(db_session):
    """
    Demonstrate that Item Response Theory (IRT) 2PL Fisher Information selection
    actually selects different items when ability estimate theta changes.

    Given a pool of items ranging from easy (b = -1.5) to hard (b = +1.5):
    - When ability theta is low (-1.5), the easy item provides maximum Fisher information.
    - When ability theta is high (+1.5), the hard item provides maximum Fisher information.
    """
    domain = db_session.query(Domain).first()
    topic = Topic(domain_id=domain.id, name="IRT Adaptive Unit Topic", order_index=101)
    db_session.add(topic)
    db_session.flush()

    sub = Subtopic(topic_id=topic.id, name="IRT Subtopic", order_index=1)
    db_session.add(sub)
    db_session.flush()

    skill = Skill(subtopic_id=sub.id, code="SKILL_IRT_TEST", name="IRT Skill", difficulty_level=0.5)
    db_session.add(skill)
    db_session.flush()

    # Create 3 controlled items: Easy, Medium, Hard with identical discrimination a=1.5
    easy_item = Item(
        primary_skill_id=skill.id,
        item_type=ItemType.MCQ,
        stem="Easy IRT Item (b = -1.5)?",
        options=[{"id": "A", "text": "A"}],
        answer_key="A",
        explanation="Exp",
        a=1.5,
        b=-1.5,
        point_biserial=0.4,
        is_calibrated=1,
        state=ItemState.ACTIVE,
    )
    medium_item = Item(
        primary_skill_id=skill.id,
        item_type=ItemType.MCQ,
        stem="Medium IRT Item (b = 0.0)?",
        options=[{"id": "A", "text": "A"}],
        answer_key="A",
        explanation="Exp",
        a=1.5,
        b=0.0,
        point_biserial=0.4,
        is_calibrated=1,
        state=ItemState.ACTIVE,
    )
    hard_item = Item(
        primary_skill_id=skill.id,
        item_type=ItemType.MCQ,
        stem="Hard IRT Item (b = +1.5)?",
        options=[{"id": "A", "text": "A"}],
        answer_key="A",
        explanation="Exp",
        a=1.5,
        b=+1.5,
        point_biserial=0.4,
        is_calibrated=1,
        state=ItemState.ACTIVE,
    )
    db_session.add_all([easy_item, medium_item, hard_item])
    db_session.commit()

    candidates = [easy_item, medium_item, hard_item]

    # Part A: Direct IRT 2PL Fisher Information mathematical proof
    # Test 1: Low ability student (theta = -1.5)
    info_map_low = {it.id: fisher_information_2pl(-1.5, it.a, it.b) for it in candidates}
    best_low_id = max(info_map_low, key=info_map_low.get)
    assert best_low_id == easy_item.id, (
        f"For theta=-1.5, easy item (b=-1.5) must maximize Fisher information. Got {info_map_low}"
    )

    # Test 2: High ability student (theta = +1.5)
    info_map_high = {it.id: fisher_information_2pl(+1.5, it.a, it.b) for it in candidates}
    best_high_id = max(info_map_high, key=info_map_high.get)
    assert best_high_id == hard_item.id, (
        f"For theta=+1.5, hard item (b=+1.5) must maximize Fisher information. Got {info_map_high}"
    )

    # Test 3: Average ability student (theta = 0.0)
    info_map_mid = {it.id: fisher_information_2pl(0.0, it.a, it.b) for it in candidates}
    best_mid_id = max(info_map_mid, key=info_map_mid.get)
    assert best_mid_id == medium_item.id, (
        f"For theta=0.0, medium item (b=0.0) must maximize Fisher information. Got {info_map_mid}"
    )

    # Part B: EAP ability update responds correctly to responses
    theta_prior, se_prior = estimate_ability_eap([])
    # Correct response to easy item increases ability estimate
    theta_correct, se_correct = estimate_ability_eap([(easy_item.a, easy_item.b, True)])
    assert theta_correct > theta_prior, "Correct response must increase ability estimate theta."

    # Incorrect response to hard item decreases ability estimate
    theta_wrong, se_wrong = estimate_ability_eap([(hard_item.a, hard_item.b, False)])
    assert theta_wrong < theta_prior, "Incorrect response must decrease ability estimate theta."


def test_session_resume_endpoint_preserves_state(client, db_session):
    """Verify GET /api/v1/sessions/{session_id}/current recovers active session progress on page refresh."""
    headers = get_authenticated_headers(client, "test_resume@example.com")

    topic = db_session.query(Topic).first()
    start_res = client.post("/api/v1/sessions", json={
        "kind": SessionKind.ADAPTIVE.value,
        "topic_id": topic.id,
    }, headers=headers)
    assert start_res.status_code == 201
    s_data = start_res.json()
    session_id = s_data["session_id"]
    item_id = s_data["first_item"]["id"]

    # Submit first answer
    resp = client.post(f"/api/v1/sessions/{session_id}/respond", json={
        "item_id": item_id,
        "response_value": "A",
        "latency_ms": 3000,
    }, headers=headers)
    assert resp.status_code == 200
    r_data = resp.json()

    # Now simulate browser refresh by calling GET /sessions/{session_id}/current
    current_res = client.get(f"/api/v1/sessions/{session_id}/current", headers=headers)
    assert current_res.status_code == 200
    cur_data = current_res.json()

    assert cur_data["session_id"] == session_id
    assert cur_data["current_question_number"] == 2
    assert cur_data["total_questions_estimated"] == 15
    assert cur_data["topic_name"] == topic.name
    assert cur_data["is_completed"] is False
    assert cur_data["current_item"] is not None
    assert cur_data["current_item"]["id"] == r_data["next_item"]["id"]
