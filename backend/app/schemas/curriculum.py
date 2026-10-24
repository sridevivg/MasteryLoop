from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class SkillBase(BaseModel):
    id: str
    name: str
    code: str
    description: Optional[str] = None
    difficulty_level: float
    blooms_level: str

    model_config = ConfigDict(from_attributes=True)


class SkillEdgeBase(BaseModel):
    prereq_id: str
    skill_id: str
    strength: float

    model_config = ConfigDict(from_attributes=True)


class SubtopicBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    order_index: int
    skills: List[SkillBase] = []

    model_config = ConfigDict(from_attributes=True)


class TopicBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    order_index: int
    subtopics: List[SubtopicBase] = []

    model_config = ConfigDict(from_attributes=True)


class DomainBase(BaseModel):
    id: str
    name: str
    code: str
    description: Optional[str] = None
    icon: str
    topics: List[TopicBase] = []

    model_config = ConfigDict(from_attributes=True)


class SkillGraphNode(BaseModel):
    id: str
    label: str
    code: str
    domain: str
    topic: str
    difficulty: float
    mastery_estimate: Optional[float] = None
    status: str = "UNTESTED"  # "MASTERED", "IN_PROGRESS", "NEEDS_ATTENTION", "UNTESTED"


class SkillGraphEdge(BaseModel):
    source: str
    target: str
    strength: float


class SkillGraphResponse(BaseModel):
    nodes: List[SkillGraphNode]
    edges: List[SkillGraphEdge]
