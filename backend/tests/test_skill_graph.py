import pytest
from app.models.curriculum import Skill, SkillEdge
from app.services.skill_graph import (
    SkillDependencyGraph,
    SkillNotFoundError,
    SelfDependencyError,
    CycleDetectedError
)


def make_skill(skill_id: str, name: str) -> Skill:
    s = Skill(
        id=skill_id,
        subtopic_id="subtopic-1",
        name=name,
        code=f"SKILL_{skill_id.upper()}",
        difficulty_level=0.5,
        blooms_level="Apply"
    )
    return s


def make_edge(prereq_id: str, skill_id: str, strength: float = 1.0) -> SkillEdge:
    return SkillEdge(prereq_id=prereq_id, skill_id=skill_id, strength=strength)


def test_valid_graph_traversal():
    # Linear chain: A (Variables) -> B (Loops) -> C (Functions) -> D (Recursion)
    s_a = make_skill("s_a", "Variables")
    s_b = make_skill("s_b", "Loops")
    s_c = make_skill("s_c", "Functions")
    s_d = make_skill("s_d", "Recursion")
    skills = [s_a, s_b, s_c, s_d]

    edges = [
        make_edge("s_a", "s_b"),
        make_edge("s_b", "s_c"),
        make_edge("s_c", "s_d"),
    ]

    graph = SkillDependencyGraph(skills, edges)

    # Direct prerequisites
    assert graph.get_direct_prerequisites("s_b") == ["s_a"]
    assert graph.get_direct_prerequisites("s_c") == ["s_b"]
    assert graph.get_direct_prerequisites("s_a") == []

    # Transitive prerequisites for Recursion
    prereqs_d = graph.get_all_prerequisites("s_d")
    assert set(prereqs_d) == {"s_a", "s_b", "s_c"}

    # Direct and transitive dependents
    assert graph.get_direct_dependents("s_b") == ["s_c"]
    assert set(graph.get_all_dependents("s_a")) == {"s_b", "s_c", "s_d"}

    # Topological order: s_a must precede s_b, which precedes s_c, which precedes s_d
    order = graph.get_topological_order()
    assert order.index("s_a") < order.index("s_b")
    assert order.index("s_b") < order.index("s_c")
    assert order.index("s_c") < order.index("s_d")


def test_missing_skill_reference_raises_error():
    s_a = make_skill("s_a", "Variables")
    skills = [s_a]
    edges = [make_edge("s_a", "s_nonexistent")]

    with pytest.raises(SkillNotFoundError) as exc_info:
        SkillDependencyGraph(skills, edges)
    assert "s_nonexistent" in str(exc_info.value)


def test_self_dependency_raises_error():
    s_a = make_skill("s_a", "Variables")
    skills = [s_a]
    edges = [make_edge("s_a", "s_a")]

    with pytest.raises(SelfDependencyError) as exc_info:
        SkillDependencyGraph(skills, edges)
    assert "s_a" in str(exc_info.value)


def test_direct_cycle_raises_error():
    s_a = make_skill("s_a", "Skill A")
    s_b = make_skill("s_b", "Skill B")
    skills = [s_a, s_b]
    edges = [
        make_edge("s_a", "s_b"),
        make_edge("s_b", "s_a"),
    ]

    with pytest.raises(CycleDetectedError) as exc_info:
        SkillDependencyGraph(skills, edges)
    assert "Circular dependency" in str(exc_info.value)


def test_multi_node_cycle_raises_error():
    # A -> B -> C -> A
    s_a = make_skill("s_a", "Skill A")
    s_b = make_skill("s_b", "Skill B")
    s_c = make_skill("s_c", "Skill C")
    skills = [s_a, s_b, s_c]
    edges = [
        make_edge("s_a", "s_b"),
        make_edge("s_b", "s_c"),
        make_edge("s_c", "s_a"),
    ]

    with pytest.raises(CycleDetectedError) as exc_info:
        SkillDependencyGraph(skills, edges)
    assert "Circular dependency" in str(exc_info.value)


def test_learner_readiness_and_gap_isolation():
    # Diamond graph:
    #      Base
    #     /    \
    #   Math   Logic
    #     \    /
    #    Proof
    s_base = make_skill("base", "Base Logic")
    s_math = make_skill("math", "Math Basics")
    s_logic = make_skill("logic", "Boolean Logic")
    s_proof = make_skill("proof", "Formal Proofs")
    skills = [s_base, s_math, s_logic, s_proof]

    edges = [
        make_edge("base", "math"),
        make_edge("base", "logic"),
        make_edge("math", "proof"),
        make_edge("logic", "proof"),
    ]

    graph = SkillDependencyGraph(skills, edges)

    # When learner only mastered "base" and "math":
    mastered = {"base", "math"}

    # Not ready for proof because "logic" is missing
    assert graph.is_learner_ready_for_skill("proof", mastered) is False

    # Ready for logic because "base" is mastered
    assert graph.is_learner_ready_for_skill("logic", mastered) is True

    # Identify unmastered foundations for proof
    missing = graph.get_unmastered_foundations("proof", mastered)
    assert "logic" in missing
    assert "base" not in missing
    assert "math" not in missing
