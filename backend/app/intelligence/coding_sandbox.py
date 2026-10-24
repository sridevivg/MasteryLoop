"""
Secure Subprocess Coding Execution Sandbox for MasteryLoop.
Enforces multi-layer execution defense:
1. AST Static Security Screening (detects and bans os, sys, subprocess, socket, open, eval, exec)
2. Ephemeral Sandboxed Environment (isolated temp directory wiped on exit)
3. Secret-Stripped Environment (never exposes host environment variables, DB credentials, or API keys)
4. Strict Subprocess Timeout (kills hanging infinite loops after 2.0s)
5. Output Truncation Limit (caps stdout/stderr at 10 KB to protect host memory)
"""

import ast
import os
import sys
import time
import logging
import tempfile
import subprocess
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Execution limits
DEFAULT_TIMEOUT_SECONDS = 2.0
MAX_OUTPUT_BYTES = 10_000

# Banned AST modules and builtins for untrusted student code
BANNED_MODULES = {
    "os", "sys", "subprocess", "shutil", "socket", "urllib", "requests",
    "http", "ftplib", "builtins", "__builtin__", "ctypes", "posix", "nt",
    "pty", "commands", "importlib", "signal", "multiprocessing"
}

BANNED_FUNCTIONS = {
    "eval", "exec", "open", "compile", "__import__", "globals", "locals"
}


class SecurityViolationError(Exception):
    """Raised when submitted code attempts to violate sandbox security boundaries."""
    pass


class ASTSecurityInspector(ast.NodeVisitor):
    """Pre-execution AST scanner that rejects dangerous system calls and imports."""

    def __init__(self):
        self.violations: List[str] = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            base_module = alias.name.split('.')[0]
            if base_module in BANNED_MODULES:
                self.violations.append(f"Import of restricted module '{alias.name}' is prohibited.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            base_module = node.module.split('.')[0]
            if base_module in BANNED_MODULES:
                self.violations.append(f"Import from restricted module '{node.module}' is prohibited.")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id in BANNED_FUNCTIONS:
                self.violations.append(f"Call to restricted built-in '{node.func.id}()' is prohibited.")
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in ("system", "popen", "spawn", "fork"):
                self.violations.append(f"Call to restricted system method '{node.func.attr}' is prohibited.")
        self.generic_visit(node)


def screen_code_security(code: str) -> None:
    """Parses code AST and raises SecurityViolationError if banned constructs are present."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in submitted code: {e}")

    inspector = ASTSecurityInspector()
    inspector.visit(tree)

    if inspector.violations:
        raise SecurityViolationError(" | ".join(inspector.violations))


def run_single_test_case(
    script_path: str,
    test_input: str,
    expected_output: str,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
) -> Dict[str, Any]:
    """Runs a single test case against the student script in an isolated subprocess."""
    start_time = time.perf_counter()

    # Secret-stripped environment
    clean_env = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1"
    }

    try:
        proc = subprocess.run(
            [sys.executable, script_path],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=clean_env,
            cwd=os.path.dirname(script_path)
        )
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        actual_stdout = proc.stdout[:MAX_OUTPUT_BYTES].strip()
        actual_stderr = proc.stderr[:MAX_OUTPUT_BYTES].strip()
        expected = expected_output.strip()

        passed = (proc.returncode == 0) and (actual_stdout == expected)

        return {
            "passed": passed,
            "actual_output": actual_stdout,
            "expected_output": expected,
            "error": actual_stderr if proc.returncode != 0 else None,
            "exit_code": proc.returncode,
            "latency_ms": elapsed_ms,
            "timed_out": False
        }
    except subprocess.TimeoutExpired:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "passed": False,
            "actual_output": "",
            "expected_output": expected_output.strip(),
            "error": f"Execution timed out after {timeout_seconds} seconds (infinite loop or high complexity detected).",
            "exit_code": -1,
            "latency_ms": elapsed_ms,
            "timed_out": True
        }
    except Exception as e:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "passed": False,
            "actual_output": "",
            "expected_output": expected_output.strip(),
            "error": f"Execution error: {str(e)}",
            "exit_code": -1,
            "latency_ms": elapsed_ms,
            "timed_out": False
        }


def execute_sandboxed_code(
    code: str,
    test_cases: List[Dict[str, Any]],
    language: str = "python",
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
) -> Dict[str, Any]:
    """
    Validates, writes, and executes code in an isolated temporary directory.
    Returns structured results for all test cases.
    """
    if language.lower() not in ("python", "py"):
        return {
            "success": False,
            "error": f"Language '{language}' is not supported in the sandbox. Supported: ['python'].",
            "test_results": [],
            "all_passed": False
        }

    # 1. AST Security Pre-Screening
    try:
        screen_code_security(code)
    except SecurityViolationError as sve:
        return {
            "success": False,
            "error": str(sve),
            "test_results": [],
            "all_passed": False,
            "is_security_violation": True
        }
    except ValueError as ve:
        return {
            "success": False,
            "error": str(ve),
            "test_results": [],
            "all_passed": False,
            "is_syntax_error": True
        }

    # 2. Ephemeral Sandbox Execution
    with tempfile.TemporaryDirectory(prefix="masteryloop_sandbox_") as tmpdir:
        script_path = os.path.join(tmpdir, "solution.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        results = []
        all_passed = True
        total_time_ms = 0.0

        for idx, tc in enumerate(test_cases):
            inp = str(tc.get("input", ""))
            exp = str(tc.get("expected_output") if tc.get("expected_output") is not None else tc.get("expected", ""))
            is_hidden = bool(tc.get("is_hidden") if tc.get("is_hidden") is not None else tc.get("hidden", False))

            tc_result = run_single_test_case(
                script_path=script_path,
                test_input=inp,
                expected_output=exp,
                timeout_seconds=timeout_seconds
            )
            total_time_ms += tc_result["latency_ms"]

            if not tc_result["passed"]:
                all_passed = False

            # Mask hidden test case input/output from learner feedback
            results.append({
                "test_case_number": idx + 1,
                "passed": tc_result["passed"],
                "latency_ms": tc_result["latency_ms"],
                "input": "[HIDDEN TEST CASE]" if is_hidden else inp,
                "expected_output": "[HIDDEN TEST CASE]" if is_hidden else exp,
                "actual_output": "[HIDDEN TEST CASE]" if is_hidden else tc_result["actual_output"],
                "error": tc_result["error"],
                "timed_out": tc_result["timed_out"],
                "is_hidden": is_hidden
            })

        return {
            "success": True,
            "error": None,
            "all_passed": all_passed,
            "passed_count": sum(1 for r in results if r["passed"]),
            "total_count": len(results),
            "total_latency_ms": round(total_time_ms, 2),
            "test_results": results
        }
