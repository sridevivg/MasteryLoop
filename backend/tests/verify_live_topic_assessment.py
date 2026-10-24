"""
Live End-to-End Verification of Topic Question Count, IRT 2PL Adaptation,
and Session Progression on the running MasteryLoop servers (ports 8000 & 5173).
"""

import sys
import json
import urllib.request
import urllib.error

BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:5173"


def request_json(url, method="GET", headers=None, data=None):
    headers = headers or {}
    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
            try:
                body = json.loads(content)
            except Exception:
                body = content
            return resp.status, body
    except urllib.error.HTTPError as e:
        err_content = e.read().decode("utf-8")
        try:
            err_body = json.loads(err_content)
        except Exception:
            err_body = err_content
        return e.code, err_body


def main():
    print("=" * 75)
    print("      MASTERYLOOP LIVE ASSESSMENT & TOPIC QUESTION VERIFICATION")
    print("=" * 75)

    # 1. Probe Backend Health
    status, health = request_json(f"{BACKEND_URL}/health")
    assert status == 200, f"Health check failed: {status}"
    print(f"[PASS] 1. Backend Health Check: status={health.get('status')}")

    # 2. Probe Frontend Availability
    status, fe_html = request_json(FRONTEND_URL)
    assert status == 200, f"Frontend check failed: {status}"
    assert "MasteryLoop" in str(fe_html)
    print(f"[PASS] 2. Frontend Server Check: {FRONTEND_URL} serves index HTML correctly.")

    # 3. Verify Topic Question Counts Endpoint
    status, topics = request_json(f"{BACKEND_URL}/api/v1/curriculum/topics")
    assert status == 200, f"Failed to fetch topics: {status}"
    assert len(topics) == 22, f"Expected 22 topics, got {len(topics)}"
    print(f"[PASS] 3. Topic Listing: {len(topics)} topics discovered.")
    
    # Check that each topic has >= 15 questions
    all_at_least_15 = True
    for t in topics:
        q_count = t.get("question_count", 0)
        if q_count < 15:
            all_at_least_15 = False
            print(f"  [SHORTAGE] Topic '{t['name']}': {q_count} questions")
        else:
            print(f"  [OK 15+] Topic '{t['name']}': {q_count} questions ({t['domain_name']})")
    assert all_at_least_15, "Not all topics have reached the preferred 15 questions!"
    print("[PASS] 4. Question Bank Verification: All 22 topics have 15+ questions available.")

    # 4. Verify Question Bank Validation Report Endpoint
    status, report = request_json(f"{BACKEND_URL}/api/v1/curriculum/validation-report")
    assert status == 200, f"Failed to fetch validation report: {status}"
    assert report["summary"]["topics_with_shortage"] == 0
    assert report["summary"]["topics_meeting_target_15"] == 22
    print(f"[PASS] 5. Validation API Report: Optimal Topics: {report['summary']['topics_meeting_target_15']}/22, Shortages: 0.")

    # 5. Authenticate Live Test Learner
    email = "live_tester_adaptive@masteryloop.ai"
    password = "Password123!"
    reg_status, _ = request_json(f"{BACKEND_URL}/api/v1/auth/register", method="POST", data={
        "email": email,
        "password": password,
        "full_name": "Live Adaptive Tester",
        "role": "STUDENT"
    })
    
    login_status, login_res = request_json(f"{BACKEND_URL}/api/v1/auth/login", method="POST", data={
        "email": email,
        "password": password
    })
    assert login_status == 200, f"Login failed: {login_res}"
    token = login_res["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[PASS] 6. Authentication: Obtained access token for {email}")

    # 6. Start Live Assessment on a Specific Topic (e.g., Relational Theory & Design)
    target_topic = next((t for t in topics if t["name"] == "Relational Theory & Design"), topics[0])
    print(f"\n--- Starting 15-Question Adaptive Assessment on: '{target_topic['name']}' ---")

    start_status, session_data = request_json(
        f"{BACKEND_URL}/api/v1/sessions",
        method="POST",
        headers=headers,
        data={
            "kind": "ADAPTIVE",
            "topic_id": target_topic["id"]
        }
    )
    assert start_status == 201, f"Failed to start session: {session_data}"
    session_id = session_data["session_id"]
    estimated_total = session_data["total_questions_estimated"]
    assert estimated_total == 15, f"Expected 15 estimated questions, got {estimated_total}"
    assert session_data["topic_name"] == target_topic["name"]
    print(f"[PASS] 7. Session Created: ID={session_id[:8]}, Target={estimated_total} questions, Topic='{target_topic['name']}'")

    # 7. Test Session Resume Endpoint
    cur_status, cur_data = request_json(f"{BACKEND_URL}/api/v1/sessions/{session_id}/current", headers=headers)
    assert cur_status == 200, f"Failed to get current session: {cur_data}"
    assert cur_data["session_id"] == session_id
    assert cur_data["current_question_number"] == 1
    assert cur_data["total_questions_estimated"] == 15
    print(f"[PASS] 8. Session Resume: Endpoint correctly recovered active session on Question 1.")

    # 8. Play Through All 15 Questions Adaptively
    current_item = session_data["first_item"]
    seen_ids = []
    theta_progression = []
    step = 0

    while current_item:
        step += 1
        item_id = current_item["id"]
        assert item_id not in seen_ids, f"DUPLICATE QUESTION DETECTED: {item_id} repeated at step {step}!"
        seen_ids.append(item_id)

        # Submit answer (alternate A and B to test theta variance)
        answer_choice = "A" if step % 2 == 1 else "B"
        resp_status, resp_data = request_json(
            f"{BACKEND_URL}/api/v1/sessions/{session_id}/respond",
            method="POST",
            headers=headers,
            data={
                "item_id": item_id,
                "response_value": answer_choice,
                "latency_ms": 2800,
                "confidence_rating": 2
            }
        )
        assert resp_status == 200, f"Response submission failed at step {step}: {resp_data}"

        new_theta = resp_data["updated_theta"]
        new_se = resp_data["updated_se"]
        is_corr = resp_data["is_correct"]
        theta_progression.append((new_theta, new_se, is_corr))

        print(f"  Step {step:2d}/15 | Item {item_id[:8]} | Ans='{answer_choice}' | Correct={is_corr!s:<5} | Theta={new_theta:+.2f} | SE={new_se:.3f}")

        if resp_data.get("is_completed"):
            print(f"\n[PASS] Session Completed after exactly {step} questions.")
            break

        current_item = resp_data.get("next_item")

    assert step == 15, f"Expected exactly 15 questions answered, got {step}"
    assert len(set(seen_ids)) == 15, f"Expected 15 unique items, got {len(set(seen_ids))}"
    print(f"[PASS] 9. Question Delivery: Exactly 15 distinct questions delivered and answered.")

    # 9. Verify Performance Report
    rep_status, report = request_json(f"{BACKEND_URL}/api/v1/sessions/{session_id}/report", headers=headers)
    assert rep_status == 200, f"Failed to retrieve final report: {report}"
    overall = report["overall_score"]
    assert overall["total_questions"] == 15
    assert report["topic_name"] == target_topic["name"]
    print(f"[PASS] 10. Performance Report: Total={overall['total_questions']}, Accuracy={overall['accuracy_percentage']}%, Final Theta={overall['final_theta']}")

    print("\n" + "=" * 75)
    print("              ALL LIVE VERIFICATION CHECKS PASSED (10/10)")
    print("=" * 75)


if __name__ == "__main__":
    main()
