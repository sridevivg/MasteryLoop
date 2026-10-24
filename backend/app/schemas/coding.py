from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class CodeSubmissionRequest(BaseModel):
    item_id: str
    code: str
    language: str = "python"


class TestCaseResult(BaseModel):
    test_number: int
    test_input: str
    expected_output: str
    actual_output: Optional[str] = None
    passed: bool
    execution_time_ms: float
    error_message: Optional[str] = None
    is_hidden: bool = False


class ComplexityAnalysis(BaseModel):
    time_complexity_static: str      # e.g. "O(N log N)"
    space_complexity_static: str     # e.g. "O(1)"
    bottleneck_explanation: str
    optimization_recommendation: str
    optimized_code_sample: Optional[str] = None


class CodeExecutionResponse(BaseModel):
    item_id: str
    all_passed: bool
    total_tests: int
    passed_tests: int
    results: List[TestCaseResult]
    complexity: ComplexityAnalysis
    recommended_followup_skill: Optional[str] = None
