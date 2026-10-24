from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.models.item import ItemState, ItemOrigin, ItemType


class ItemOption(BaseModel):
    id: str  # "A", "B", "C", "D"
    text: str
    is_distractor: bool = True


class ItemCreate(BaseModel):
    item_type: ItemType = ItemType.MCQ
    primary_skill_id: str
    secondary_skill_ids: List[str] = []
    stem: str
    options: List[ItemOption] = []
    answer_key: str
    explanation: Optional[str] = None
    distractor_explanations: Dict[str, str] = {}
    code_template: Optional[str] = None
    test_cases: List[Dict[str, Any]] = []
    a: float = 1.0
    b: float = 0.0


class ItemResponse(BaseModel):
    id: str
    item_type: str
    primary_skill_id: str
    stem: str
    options: List[Dict[str, Any]]
    explanation: Optional[str] = None
    distractor_explanations: Optional[Dict[str, str]] = None
    code_template: Optional[str] = None
    test_cases: Optional[List[Dict[str, Any]]] = None
    a: float
    b: float
    point_biserial: float
    is_calibrated: int
    exposure_count: int
    state: str
    origin: str
    lineage: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class ItemReviewRequest(BaseModel):
    action: str  # "APPROVE", "EDIT", "REJECT", "REQUEST_REGEN"
    reason: str
    edits: Optional[Dict[str, Any]] = None


class GenerateItemRequest(BaseModel):
    skill_id: str
    count: int = 1
    difficulty_band: str = "medium"  # "easy" (-1.5 to -0.5), "medium" (-0.5 to +0.5), "hard" (+0.5 to +1.8)
    item_type: ItemType = ItemType.MCQ
