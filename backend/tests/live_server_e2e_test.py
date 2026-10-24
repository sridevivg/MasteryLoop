"""
MasteryLoop Live Server End-to-End Integration Verification Script
Tests real HTTP requests against the live running backend (port 8000) and frontend (port 5173).
"""

import sys
import json
import urllib.request
import urllib.error

BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:5173"

def make_request(url, method="GET", headers=None, data=None):
    headers = headers or {}
    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
            status = resp.status
            try:
                body = json.loads(content)
            except Exception:
                body = content
            return status, body
    except urllib.error.HTTPError as e:
        err_content = e.read().decode("utf-8")
        try:
            err_body = json.loads(err_content)
        except Exception:
            err_body = err_content
        return e.code, err_body

def run_e2e_checks():
    results = []
    print("=== STARTING MASTERYLOOP LIVE SERVER VERIFICATION ===")

    # 1. Root Health Check
    status, body = make_request(f"{BACKEND_URL}/health")
    assert status == 200, f"Backend health failed with status {status}"
    assert body["status"] == "healthy"
    results.append(("[PASS] 1. Backend Health Probe", body))

    # 2. Register New E2E Learner
    test_user_email = "e2e_student_autonomous@masteryloop.ai"
    reg_payload = {
        "email": test_user_email,
        "password": "Password123!",
        "full_name": "Autonomous Tester",
        "role": "STUDENT"
    }
    status, reg_body = make_request(f"{BACKEND_URL}/api/v1/auth/register", method="POST", data=reg_payload)
    if status == 400 and "already exists" in str(reg_body):
        print("  User already exists, proceeding to login.")
    else:
        assert status in (200, 201), f"Registration failed: {reg_body}"
    results.append(("[PASS] 2. User Registration", "Success"))

    # 3. Login User
    login_payload = {
        "email": test_user_email,
        "password": "Password123!"
    }
    status, login_body = make_request(f"{BACKEND_URL}/api/v1/auth/login", method="POST", data=login_payload)
    assert status == 200, f"Login failed: {login_body}"
    token = login_body["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}
    results.append(("[PASS] 3. JWT Authentication Login", f"Token acquired for {login_body['user_id']}"))

    # 4. Get Current User Profile
    status, me_body = make_request(f"{BACKEND_URL}/api/v1/auth/me", headers=auth_headers)
    assert status == 200, f"Me endpoint failed: {me_body}"
    assert me_body["email"] == test_user_email
    results.append(("[PASS] 4. User Profile", me_body["full_name"]))

    # 5. List Curriculum Domains
    status, domains_body = make_request(f"{BACKEND_URL}/api/v1/curriculum/domains", headers=auth_headers)
    assert status == 200, f"Domains query failed: {domains_body}"
    assert len(domains_body) >= 11, f"Expected at least 11 domains, got {len(domains_body)}"
    results.append(("[PASS] 5. Curriculum Domains Query", f"Found {len(domains_body)} domains"))

    # 6. Skill Prerequisites
    status, prereq_body = make_request(f"{BACKEND_URL}/api/v1/curriculum/skills/DSA_GRAPH_BFS_DFS/prerequisites", headers=auth_headers)
    assert status == 200, f"Prerequisites query failed: {prereq_body}"
    assert "direct_prerequisites" in prereq_body
    results.append(("[PASS] 6. DAG Skill Prerequisites", f"DSA_GRAPH_BFS_DFS direct prereqs: {[p['code'] for p in prereq_body['direct_prerequisites']]}"))

    # 7. Start Computer Adaptive (CAT) Session
    session_start_payload = {
        "kind": "ADAPTIVE",
        "domain_id": "DSA",
        "max_questions": 5
    }
    status, sess_body = make_request(f"{BACKEND_URL}/api/v1/sessions", method="POST", headers=auth_headers, data=session_start_payload)
    assert status == 201, f"Session start failed: {sess_body}"
    session_id = sess_body["session_id"]
    first_item = sess_body["first_item"]
    assert first_item is not None
    assert "answer_key" not in first_item  # Key leak check
    results.append(("[PASS] 7. Adaptive Session Start", f"Session: {session_id}, Item: {first_item['id']} ({first_item['item_type']})"))

    # 8. Submit Response to First Question
    respond_payload = {
        "item_id": first_item["id"],
        "response_value": first_item["options"][0]["id"] if first_item["options"] else "[0, 1]",
        "latency_ms": 12500,
        "confidence_rating": 2
    }
    status, resp_body = make_request(f"{BACKEND_URL}/api/v1/sessions/{session_id}/respond", method="POST", headers=auth_headers, data=respond_payload)
    assert status == 200, f"Respond failed: {resp_body}"
    assert "is_correct" in resp_body
    assert "updated_theta" in resp_body
    results.append(("[PASS] 8. 2PL Response Evaluation & Theta Update", f"IsCorrect: {resp_body['is_correct']}, New Theta: {resp_body['updated_theta']}"))

    # 9. Coding Subprocess Sandbox Execution
    coding_payload = {
        "code": "print('Test Sandbox Autonomous')",
        "language": "python",
        "test_cases": [
            {"input": "", "expected_output": "Test Sandbox Autonomous", "is_hidden": False}
        ]
    }
    status, sandbox_body = make_request(f"{BACKEND_URL}/api/v1/coding/execute", method="POST", headers=auth_headers, data=coding_payload)
    assert status == 200, f"Coding sandbox failed: {sandbox_body}"
    assert sandbox_body["success"] is True
    assert sandbox_body["all_passed"] is True
    results.append(("[PASS] 9. Sandboxed Subprocess Code Execution", f"All passed in {sandbox_body['total_latency_ms']}ms"))

    # 10. Socratic AI Tutor Chat
    tutor_payload = {
        "message": "What is the difference between BFS and DFS traversal?",
        "mode": "TEACH_FROM_BASICS",
        "language": "ENGLISH",
        "history": []
    }
    status, tutor_body = make_request(f"{BACKEND_URL}/api/v1/tutor/chat", method="POST", headers=auth_headers, data=tutor_payload)
    assert status == 200, f"Tutor chat failed: {tutor_body}"
    assert "response" in tutor_body
    assert len(tutor_body["response"]) > 20
    results.append(("[PASS] 10. Socratic AI Tutor", f"Reply length: {len(tutor_body['response'])} chars, Provider: {tutor_body.get('provider_used')}"))

    # 11. Learner Dashboard Metrics
    status, dash_body = make_request(f"{BACKEND_URL}/api/v1/mastery/dashboard", headers=auth_headers)
    assert status == 200, f"Dashboard failed: {dash_body}"
    assert "overall_mastery" in dash_body
    assert "placement_readiness" in dash_body
    results.append(("[PASS] 11. Learner Mastery Dashboard", f"Mastery: {dash_body['overall_mastery']}%, Assessments: {dash_body['total_assessments_taken']}"))

    # 12. Ebbinghaus Spaced Repetition Due Skills
    status, due_body = make_request(f"{BACKEND_URL}/api/v1/mastery/retention/due", headers=auth_headers)
    assert status == 200, f"Retention due failed: {due_body}"
    assert "due_skills" in due_body
    results.append(("[PASS] 12. Retention Due Skills", f"{due_body['due_count']} due skills"))

    # 13. Record Spaced Review Event
    review_payload = {
        "skill_id": "DSA_ARRAYS",
        "is_correct": True
    }
    status, rev_res = make_request(f"{BACKEND_URL}/api/v1/mastery/retention/review", method="POST", headers=auth_headers, data=review_payload)
    assert status == 200, f"Record review failed: {rev_res}"
    assert rev_res["new_retention_estimate"] == 1.0
    results.append(("[PASS] 13. Spaced Review Reinforced", f"Next review due: {rev_res['next_review_due']}"))

    # 14. Frontend Dev Server Check (port 5173)
    status, front_html = make_request(f"{FRONTEND_URL}/")
    assert status == 200, f"Frontend server failed with status {status}"
    assert "<div id=\"root\">" in str(front_html)
    results.append(("[PASS] 14. Frontend Web App Serving", "HTML with #root container loaded successfully from Vite dev server"))

    print("\n--- ALL 14 E2E INTEGRATION CHECKS PASSED SUCCESSFULLY ---")
    for res, detail in results:
        print(f"{res}: {detail}")

if __name__ == "__main__":
    import traceback
    try:
        run_e2e_checks()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] E2E CHECK FAILED: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] E2E UNEXPECTED ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(2)
