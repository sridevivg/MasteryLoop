import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.curriculum import Domain, Topic, Subtopic, Skill, SkillEdge
from app.schemas.curriculum import (
    DomainBase,
    SkillBase,
    SkillGraphResponse,
    SkillGraphNode,
    SkillGraphEdge
)
from app.services.skill_graph import SkillDependencyGraph, SkillNotFoundError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/curriculum", tags=["Curriculum & Skill Graph"])


@router.get(
    "/domains",
    summary="List all placement domains with counts of topics and skills"
)
def list_domains(db: Session = Depends(get_db)):
    domains = db.query(Domain).all()
    results = []
    for d in domains:
        topic_count = db.query(Topic).filter(Topic.domain_id == d.id).count()
        skill_count = (
            db.query(Skill)
            .join(Subtopic, Skill.subtopic_id == Subtopic.id)
            .join(Topic, Subtopic.topic_id == Topic.id)
            .filter(Topic.domain_id == d.id)
            .count()
        )
        results.append({
            "id": d.id,
            "code": d.code,
            "name": d.name,
            "description": d.description,
            "icon": d.icon,
            "topic_count": topic_count,
            "skill_count": skill_count
        })
    return results


@router.get(
    "/domains/{domain_id}",
    response_model=DomainBase,
    summary="Get full hierarchy (topics, subtopics, skills) for a domain"
)
def get_domain_hierarchy(domain_id: str, db: Session = Depends(get_db)):
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not domain:
        # Also allow querying by code (e.g. "DSA")
        domain = db.query(Domain).filter(Domain.code == domain_id.upper()).first()
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Domain '{domain_id}' not found."
        )
    return domain


@router.get(
    "/skills/{skill_id}",
    response_model=SkillBase,
    summary="Get single skill details"
)
def get_skill(skill_id: str, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        skill = db.query(Skill).filter(Skill.code == skill_id.upper()).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill '{skill_id}' not found."
        )
    return skill


@router.get(
    "/skills/{skill_id}/prerequisites",
    summary="Get direct and transitive prerequisite chains for a skill"
)
def get_skill_prerequisites(skill_id: str, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        skill = db.query(Skill).filter(Skill.code == skill_id.upper()).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill '{skill_id}' not found."
        )

    graph = SkillDependencyGraph.from_db(db)
    
    try:
        direct_prereq_ids = graph.get_direct_prerequisites(skill.id)
        all_prereq_ids = graph.get_all_prerequisites(skill.id)
        direct_dependent_ids = graph.get_direct_dependents(skill.id)
        all_dependent_ids = graph.get_all_dependents(skill.id)
    except SkillNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    def map_skills(ids: List[str]):
        return [
            {
                "id": s_id,
                "name": graph.skills_by_id[s_id].name,
                "code": graph.skills_by_id[s_id].code,
                "difficulty_level": graph.skills_by_id[s_id].difficulty_level
            }
            for s_id in ids
            if s_id in graph.skills_by_id
        ]

    return {
        "target_skill": {
            "id": skill.id,
            "code": skill.code,
            "name": skill.name,
            "difficulty_level": skill.difficulty_level
        },
        "direct_prerequisites": map_skills(direct_prereq_ids),
        "foundational_prerequisites_topological": map_skills(all_prereq_ids),
        "direct_dependents": map_skills(direct_dependent_ids),
        "all_downstream_dependents": map_skills(all_dependent_ids)
    }


@router.get(
    "/graph",
    response_model=SkillGraphResponse,
    summary="Retrieve nodes and directed edges for the skill dependency DAG visualization"
)
def get_skill_graph(domain_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = (
        db.query(Skill, Subtopic, Topic, Domain)
        .join(Subtopic, Skill.subtopic_id == Subtopic.id)
        .join(Topic, Subtopic.topic_id == Topic.id)
        .join(Domain, Topic.domain_id == Domain.id)
    )

    if domain_id:
        query = query.filter((Domain.id == domain_id) | (Domain.code == domain_id.upper()))

    records = query.all()
    node_ids = set()
    nodes = []

    for skill, subtopic, topic, domain in records:
        node_ids.add(skill.id)
        nodes.append(SkillGraphNode(
            id=skill.id,
            label=skill.name,
            code=skill.code,
            domain=domain.name,
            topic=topic.name,
            difficulty=skill.difficulty_level,
            status="UNTESTED"
        ))

    # Fetch edges between the visible nodes
    edges_query = db.query(SkillEdge).filter(
        SkillEdge.prereq_id.in_(node_ids),
        SkillEdge.skill_id.in_(node_ids)
    ).all()

    edges = [
        SkillGraphEdge(
            source=edge.prereq_id,
            target=edge.skill_id,
            strength=edge.strength
        )
        for edge in edges_query
    ]

    return SkillGraphResponse(nodes=nodes, edges=edges)


@router.get(
    "/validate-dag",
    summary="Run full DAG validation across the entire curriculum"
)
def validate_curriculum_dag(db: Session = Depends(get_db)):
    graph = SkillDependencyGraph.from_db(db)
    topo_order = graph.get_topological_order()
    return {
        "is_valid_dag": True,
        "total_skills": len(graph.skills_by_id),
        "total_prerequisite_edges": len(graph.edge_strengths),
        "topological_sequence_count": len(topo_order)
    }


@router.get(
    "/topics",
    summary="List all curriculum topics with domain info and usable question counts"
)
def list_curriculum_topics(domain_id: Optional[str] = None, db: Session = Depends(get_db)):
    from app.models.item import Item, ItemState
    query = (
        db.query(Topic, Domain)
        .join(Domain, Topic.domain_id == Domain.id)
    )
    if domain_id:
        query = query.filter((Domain.id == domain_id) | (Domain.code == domain_id.upper()))

    records = query.order_by(Domain.name, Topic.name).all()
    results = []

    for topic, domain in records:
        skills = (
            db.query(Skill)
            .join(Subtopic, Skill.subtopic_id == Subtopic.id)
            .filter(Subtopic.topic_id == topic.id)
            .all()
        )
        skill_ids = [s.id for s in skills]

        question_count = 0
        if skill_ids:
            question_count = (
                db.query(Item)
                .filter(Item.primary_skill_id.in_(skill_ids), Item.state == ItemState.ACTIVE)
                .count()
            )

        results.append({
            "id": topic.id,
            "name": topic.name,
            "domain_id": domain.id,
            "domain_code": domain.code,
            "domain_name": domain.name,
            "skill_count": len(skills),
            "question_count": question_count,
            "is_ready": question_count >= 10
        })

    return results


@router.get(
    "/validation-report",
    summary="Get complete psychometric and structural question bank validation report across all topics"
)
def get_question_bank_validation_report(db: Session = Depends(get_db)):
    from app.services.question_bank_validator import QuestionBankValidator
    return QuestionBankValidator.validate_all(db)

