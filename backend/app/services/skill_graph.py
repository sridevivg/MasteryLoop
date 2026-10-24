"""
Deterministic Skill Dependency DAG Engine for MasteryLoop.
Implements validation, cycle detection, transitive prerequisite/dependent traversal,
and topological sorting using Kahn's algorithm and 3-color DFS.
"""

from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, deque
from sqlalchemy.orm import Session

from app.models.curriculum import Skill, SkillEdge


class SkillGraphError(Exception):
    """Base exception for skill graph operations."""
    pass


class SkillNotFoundError(SkillGraphError):
    """Raised when an edge references a skill that does not exist in the curriculum."""
    def __init__(self, skill_id: str, context: str = "graph"):
        super().__init__(f"Skill '{skill_id}' referenced in {context} was not found in curriculum.")
        self.skill_id = skill_id


class SelfDependencyError(SkillGraphError):
    """Raised when a skill declares a prerequisite relationship on itself."""
    def __init__(self, skill_id: str):
        super().__init__(f"Self-dependency detected: Skill '{skill_id}' cannot be a prerequisite of itself.")
        self.skill_id = skill_id


class CycleDetectedError(SkillGraphError):
    """Raised when a circular prerequisite dependency is detected."""
    def __init__(self, cycle_path: List[str]):
        path_str = " -> ".join(cycle_path)
        super().__init__(f"Circular dependency detected in skill prerequisite graph: {path_str}")
        self.cycle_path = cycle_path


class SkillDependencyGraph:
    """
    In-memory representation and deterministic graph analysis engine for skill dependencies.
    Directed edge: prereq_id -> skill_id (prerequisite MUST be mastered before skill).
    """

    def __init__(self, skills: List[Skill], edges: List[SkillEdge]):
        self.skills_by_id: Dict[str, Skill] = {s.id: s for s in skills}
        
        # Adjacency lists
        # outgoing: prereq_id -> [downstream_skills]
        self.downstream: Dict[str, List[str]] = defaultdict(list)
        # incoming: skill_id -> [prerequisite_skills]
        self.prerequisites: Dict[str, List[str]] = defaultdict(list)
        # edge strengths
        self.edge_strengths: Dict[Tuple[str, str], float] = {}

        # Load and validate edges
        self._raw_edges = edges
        self._build_and_validate(edges)

    @classmethod
    def from_db(cls, db: Session, domain_id: Optional[str] = None) -> "SkillDependencyGraph":
        """Factory method to construct graph from SQLAlchemy database session."""
        if domain_id:
            from app.models.curriculum import Topic, Subtopic
            skills = (
                db.query(Skill)
                .join(Subtopic, Skill.subtopic_id == Subtopic.id)
                .join(Topic, Subtopic.topic_id == Topic.id)
                .filter(Topic.domain_id == domain_id)
                .all()
            )
            skill_ids = {s.id for s in skills}
            edges = (
                db.query(SkillEdge)
                .filter(SkillEdge.prereq_id.in_(skill_ids), SkillEdge.skill_id.in_(skill_ids))
                .all()
            )
        else:
            skills = db.query(Skill).all()
            edges = db.query(SkillEdge).all()

        return cls(skills, edges)

    def _build_and_validate(self, edges: List[SkillEdge]):
        """Populates adjacency lists and verifies graph integrity and acyclicity."""
        # 1. Check all skills exist & check self-dependencies
        for edge in edges:
            prereq = edge.prereq_id
            target = edge.skill_id

            if prereq not in self.skills_by_id:
                raise SkillNotFoundError(prereq, context="prerequisite edge")
            if target not in self.skills_by_id:
                raise SkillNotFoundError(target, context="dependent skill edge")
            if prereq == target:
                raise SelfDependencyError(prereq)

            self.downstream[prereq].append(target)
            self.prerequisites[target].append(prereq)
            self.edge_strengths[(prereq, target)] = edge.strength

        # 2. Cycle detection using 3-color DFS (WHITE=0, GREY=1, BLACK=2)
        WHITE, GREY, BLACK = 0, 1, 2
        color = {s_id: WHITE for s_id in self.skills_by_id}
        parent = {}

        def dfs(node: str, current_path: List[str]):
            color[node] = GREY
            current_path.append(node)

            for neighbor in self.downstream.get(node, []):
                if color[neighbor] == GREY:
                    # Found cycle: extract cycle path
                    idx = current_path.index(neighbor)
                    cycle = current_path[idx:] + [neighbor]
                    raise CycleDetectedError(cycle)
                elif color[neighbor] == WHITE:
                    parent[neighbor] = node
                    dfs(neighbor, current_path)

            current_path.pop()
            color[node] = BLACK

        for s_id in self.skills_by_id:
            if color[s_id] == WHITE:
                dfs(s_id, [])

    def get_direct_prerequisites(self, skill_id: str) -> List[str]:
        """Returns direct prerequisite skill IDs for the target skill."""
        if skill_id not in self.skills_by_id:
            raise SkillNotFoundError(skill_id)
        return list(self.prerequisites.get(skill_id, []))

    def get_all_prerequisites(self, skill_id: str) -> List[str]:
        """
        Returns all transitive prerequisites (foundational skills) in topological order.
        Earliest foundations appear first.
        """
        if skill_id not in self.skills_by_id:
            raise SkillNotFoundError(skill_id)

        visited = set()
        order = []

        def dfs_ancestors(node: str):
            for prereq in self.prerequisites.get(node, []):
                if prereq not in visited:
                    visited.add(prereq)
                    dfs_ancestors(prereq)
                    order.append(prereq)

        dfs_ancestors(skill_id)
        return order

    def get_direct_dependents(self, skill_id: str) -> List[str]:
        """Returns skills that directly depend on the given skill."""
        if skill_id not in self.skills_by_id:
            raise SkillNotFoundError(skill_id)
        return list(self.downstream.get(skill_id, []))

    def get_all_dependents(self, skill_id: str) -> List[str]:
        """Returns all skills that transitively depend on this skill."""
        if skill_id not in self.skills_by_id:
            raise SkillNotFoundError(skill_id)

        visited = set()
        queue = deque([skill_id])
        dependents = []

        while queue:
            curr = queue.popleft()
            for nxt in self.downstream.get(curr, []):
                if nxt not in visited:
                    visited.add(nxt)
                    dependents.append(nxt)
                    queue.append(nxt)

        return dependents

    def get_topological_order(self) -> List[str]:
        """
        Computes a valid topological ordering of all skills using Kahn's algorithm.
        Foundational skills with zero unsatisfied prerequisites appear first.
        """
        in_degree = {s_id: 0 for s_id in self.skills_by_id}
        for s_id in self.skills_by_id:
            for child in self.downstream.get(s_id, []):
                in_degree[child] += 1

        queue = deque([s_id for s_id, deg in in_degree.items() if deg == 0])
        topo_order = []

        while queue:
            curr = queue.popleft()
            topo_order.append(curr)

            for child in self.downstream.get(curr, []):
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    queue.append(child)

        if len(topo_order) != len(self.skills_by_id):
            raise CycleDetectedError(["Graph contains unresolved cycles"])

        return topo_order

    def is_learner_ready_for_skill(self, skill_id: str, mastered_skill_ids: Set[str]) -> bool:
        """
        Checks if the learner has mastered all direct prerequisites for the target skill.
        Avoids recommending advanced topics when essential foundations are weak.
        """
        direct_prereqs = self.get_direct_prerequisites(skill_id)
        return all(p in mastered_skill_ids for p in direct_prereqs)

    def get_unmastered_foundations(
        self,
        skill_id: str,
        mastered_skill_ids: Set[str]
    ) -> List[str]:
        """
        Returns transitive prerequisites that are NOT yet mastered.
        Used to diagnose why a learner is struggling with an advanced skill.
        """
        all_prereqs = self.get_all_prerequisites(skill_id)
        return [p for p in all_prereqs if p not in mastered_skill_ids]
