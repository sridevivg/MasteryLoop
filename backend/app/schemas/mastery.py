from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class SkillMasteryDetail(BaseModel):
    skill_id: str
    skill_name: str
    skill_code: str
    domain_name: str
    topic_name: str
    estimate: float           # Posterior mastery probability [0.0 - 1.0]
    confidence: float         # Assessment certainty [0.0 - 1.0]
    raw_accuracy: float       # Percentage correct historically
    irt_ability: float        # Calibrated theta
    retention_estimate: float # Current memory retention [0.0 - 1.0]
    interaction_count: int
    last_practiced_at: Optional[str] = None
    next_review_due: Optional[str] = None
    status: str               # "MASTERED", "PROFICIENT", "DEVELOPING", "CRITICAL_GAP"


class PlacementDomainReadiness(BaseModel):
    domain_id: str
    domain_name: str
    readiness_percentage: float
    tested_skills_count: int
    total_skills_count: int
    benchmark_status: str     # "PLACEMENT_READY", "NEEDS_PRACTICE", "UNTESTED"
    top_strength: Optional[str] = None
    priority_weakness: Optional[str] = None


class NextBestActionItem(BaseModel):
    category: str             # "LEARN", "PRACTICE", "REASSESS"
    skill_id: str
    skill_name: str
    domain_name: str
    title: str
    duration_minutes: int
    rationale: str
    action_type: str          # "TUTOR", "PRACTICE", "ASSESSMENT"
    target_id: Optional[str] = None


class LearnerDashboardResponse(BaseModel):
    overall_mastery: float
    placement_readiness: float
    study_streak_days: int
    total_assessments_taken: int
    total_questions_solved: int
    retention_due_count: int
    strong_topics: List[Dict[str, Any]]
    weak_topics: List[Dict[str, Any]]
    placement_domains: List[PlacementDomainReadiness]
    next_best_actions: List[NextBestActionItem]
    today_challenge: Optional[Dict[str, Any]] = None
    recent_assessments: List[Dict[str, Any]]
    mastery_trend: List[Dict[str, Any]]


class ForecastRequest(BaseModel):
    study_hours_per_week: float = 5.0
    focus_domain_id: Optional[str] = None
    forecast_weeks: int = 4


class ForecastResponse(BaseModel):
    has_sufficient_data: bool
    current_readiness: float
    forecasted_readiness: float
    weekly_projection: List[Dict[str, Any]]
    explanation: str
    assumptions: List[str]
