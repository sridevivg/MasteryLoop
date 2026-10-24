import pytest
from app.intelligence.coding_sandbox import (
    execute_sandboxed_code,
    screen_code_security,
    SecurityViolationError
)
from tests.conftest import get_authenticated_headers


def test_sandbox_valid_solution_passes():
    code = """
try:
    line = input().strip()
    if line:
        a, b = map(int, line.split())
        print(a + b)
except EOFError:
    pass
"""
    test_cases = [
        {"input": "2 3", "expected_output": "5", "is_hidden": False},
        {"input": "10 -4", "expected_output": "6", "is_hidden": True}
    ]

    res = execute_sandboxed_code(code, test_cases)
    assert res["success"] is True
    assert res["all_passed"] is True
    assert res["passed_count"] == 2
    # Hidden test case output must be masked
    assert res["test_results"][1]["actual_output"] == "[HIDDEN TEST CASE]"


def test_sandbox_failing_solution_detected():
    code = """
print(999)
"""
    test_cases = [
        {"input": "2 3", "expected_output": "5", "is_hidden": False}
    ]

    res = execute_sandboxed_code(code, test_cases)
    assert res["success"] is True
    assert res["all_passed"] is False
    assert res["passed_count"] == 0
    assert res["test_results"][0]["passed"] is False


def test_sandbox_ast_screening_blocks_os_and_subprocess():
    bad_code_1 = "import os\nos.system('dir')"
    with pytest.raises(SecurityViolationError) as exc_1:
        screen_code_security(bad_code_1)
    assert "restricted module 'os'" in str(exc_1.value)

    bad_code_2 = "from subprocess import Popen"
    with pytest.raises(SecurityViolationError) as exc_2:
        screen_code_security(bad_code_2)
    assert "restricted module 'subprocess'" in str(exc_2.value)


def test_sandbox_ast_screening_blocks_banned_builtins():
    bad_code_open = "f = open('config.py', 'r')"
    with pytest.raises(SecurityViolationError) as exc_open:
        screen_code_security(bad_code_open)
    assert "restricted built-in 'open()'" in str(exc_open.value)

    bad_code_eval = "res = eval('2 + 2')"
    with pytest.raises(SecurityViolationError) as exc_eval:
        screen_code_security(bad_code_eval)
    assert "restricted built-in 'eval()'" in str(exc_eval.value)


def test_sandbox_infinite_loop_timeout_killed():
    loop_code = """
while True:
    pass
"""
    test_cases = [{"input": "", "expected_output": "done", "is_hidden": False}]
    res = execute_sandboxed_code(loop_code, test_cases, timeout_seconds=1.0)
    assert res["success"] is True
    assert res["all_passed"] is False
    assert res["test_results"][0]["timed_out"] is True
    assert "timed out" in res["test_results"][0]["error"].lower()


def test_sandbox_output_truncation_cap():
    huge_output_code = """
for i in range(10000):
    print("A" * 50)
"""
    test_cases = [{"input": "", "expected_output": "small", "is_hidden": False}]
    res = execute_sandboxed_code(huge_output_code, test_cases, timeout_seconds=2.0)
    assert res["success"] is True
    # Output must be capped at 10,000 bytes
    assert len(res["test_results"][0]["actual_output"]) <= 10_000


def test_coding_api_execute_endpoint(client):
    headers = get_authenticated_headers(client, "coder_student@example.com")

    payload = {
        "code": "print('Hello MasteryLoop')",
        "language": "python",
        "test_cases": [
            {"input": "", "expected_output": "Hello MasteryLoop", "is_hidden": False}
        ]
    }

    res = client.post("/api/v1/coding/execute", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["all_passed"] is True
