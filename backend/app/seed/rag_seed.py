"""
Curriculum Knowledge Ingestion Seed Script.
Indexes verified pedagogical concepts, worked examples, formulas, common misconceptions,
and interview questions into Qdrant vector store with metadata filtering.
"""

import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.models.curriculum import Skill, Domain, Topic, Subtopic
from app.agentic.rag import vector_store

logger = logging.getLogger("masteryloop.rag_seed")

CURRICULUM_KNOWLEDGE_CHUNKS = [
    # 1. DSA: Two-Pointer & Arrays
    {
        "skill_code": "DSA_ARRAYS",
        "title": "Two-Pointer Technique on Sorted Arrays",
        "content_type": "CONCEPT",
        "content": (
            "The two-pointer technique uses two indices to traverse an array simultaneously. "
            "For finding a target sum in a sorted array, left starts at index 0 and right starts at N-1. "
            "If array[left] + array[right] == target, the pair is found in O(N) time and O(1) auxiliary space. "
            "If the sum is too small, increment left. If too large, decrement right. "
            "This eliminates the O(N^2) brute-force nested loop requirement."
        ),
        "source": "MasteryLoop Core DSA Handbook, Sec 3.1"
    },
    {
        "skill_code": "DSA_ARRAYS",
        "title": "Two-Pointer Common Misconception: Unsorted Inputs",
        "content_type": "MISCONCEPTION",
        "content": (
            "Common Misconception: Attempting to apply the opposite-end two-pointer technique directly on unsorted arrays. "
            "If the array is unsorted, incrementing left or decrementing right does not guarantee monotonically increasing "
            "or decreasing sums. The array MUST be sorted first, taking O(N log N) time, or an O(N) hash map must be used instead."
        ),
        "source": "MasteryLoop Diagnostic Misconception Catalog"
    },

    # 2. DSA: Binary Search Trees
    {
        "skill_code": "DSA_BST",
        "title": "Binary Search Tree Properties & In-Order Traversal",
        "content_type": "CONCEPT",
        "content": (
            "A Binary Search Tree (BST) is a node-based binary tree data structure where for every node: "
            "1. All keys in the left subtree are strictly less than the node's key. "
            "2. All keys in the right subtree are strictly greater than the node's key. "
            "3. Both left and right subtrees must also be binary search trees. "
            "An In-Order traversal (Left -> Node -> Right) visits keys in strictly ascending sorted order."
        ),
        "source": "MasteryLoop Data Structures Primer, Ch 7"
    },
    {
        "skill_code": "DSA_BST",
        "title": "BST Technical Interview Discussion Points",
        "content_type": "INTERVIEW",
        "content": (
            "Interview Question: 'Why does a BST search degrade to O(N) in the worst case, and how is this mitigated?' "
            "Key Answer Points: When elements are inserted in already-sorted order, a standard BST degenerates into a linear "
            "linked list of height N. Self-balancing binary search trees (AVL Trees or Red-Black Trees) enforce height balancing "
            "via tree rotations, guaranteeing O(log N) worst-case time for search, insertion, and deletion."
        ),
        "source": "MasteryLoop Placement Technical Interview Guide"
    },

    # 3. Dynamic Programming
    {
        "skill_code": "DSA_DYNAMIC_PROG",
        "title": "Dynamic Programming: Optimal Substructure & Overlapping Subproblems",
        "content_type": "CONCEPT",
        "content": (
            "Dynamic Programming (DP) solves complex problems by combining solutions to subproblems. "
            "It requires two essential conditions: "
            "1. Optimal Substructure: An optimal solution to the problem contains optimal solutions to subproblems. "
            "2. Overlapping Subproblems: The same subproblems are solved repeatedly rather than generating new ones. "
            "Approaches include Top-Down (Recursion + Memoization) and Bottom-Up (Tabulation)."
        ),
        "source": "MasteryLoop Algorithmic Optimization Notes"
    },

    # 4. Programming Fundamentals: Recursion
    {
        "skill_code": "PRG_RECURSION",
        "title": "Recursion, Base Cases, and the Call Stack",
        "content_type": "CONCEPT",
        "content": (
            "Recursion is a programming technique where a function calls itself to solve smaller instances of the same problem. "
            "Every recursive function requires: "
            "1. A Base Case: A terminating condition that stops recursion without further calls. "
            "2. A Recursive Step: Progress toward the base case. "
            "Each recursive call pushes an activation frame onto the call stack. Omitting a base case results in a Stack Overflow Error."
        ),
        "source": "MasteryLoop Programming Foundations, Unit 4"
    },

    # 5. SQL: Joins & Aggregates
    {
        "skill_code": "SQL_JOINS",
        "title": "Relational Multi-Table Joins: INNER vs LEFT vs FULL OUTER",
        "content_type": "CONCEPT",
        "content": (
            "SQL Joins combine columns from one or more tables based on a related column. "
            "- INNER JOIN: Returns only records with matching values in both tables. "
            "- LEFT JOIN (or LEFT OUTER JOIN): Returns all records from the left table and matched records from the right table; "
            "unmatched right-table columns contain NULL values. "
            "- FULL OUTER JOIN: Returns all records when there is a match in either left or right table."
        ),
        "source": "MasteryLoop Relational Database Manual"
    },
    {
        "skill_code": "SQL_JOINS",
        "title": "Common Misconception: LEFT JOIN vs Filtering in WHERE Clause",
        "content_type": "MISCONCEPTION",
        "content": (
            "A frequent error occurs when developers place right-table filter conditions in the WHERE clause instead of the ON clause. "
            "In `SELECT * FROM A LEFT JOIN B ON A.id = B.a_id WHERE B.status = 'active'`, any row from A with no match in B produces NULL, "
            "which causes the WHERE condition `B.status = 'active'` to evaluate to UNKNOWN/FALSE, inadvertently converting the LEFT JOIN into an INNER JOIN."
        ),
        "source": "MasteryLoop SQL Query Optimization Notes"
    },

    # 6. DBMS: Normalization
    {
        "skill_code": "DBMS_NORMALIZATION",
        "title": "Database Normalization Hierarchy: 1NF to BCNF",
        "content_type": "CONCEPT",
        "content": (
            "Normalization reduces data redundancy and prevents update anomalies. "
            "- 1NF: Atomic attribute values; no repeating groups. "
            "- 2NF: In 1NF and no partial dependencies (every non-prime attribute fully functionally dependent on whole candidate key). "
            "- 3NF: In 2NF and no transitive dependencies (non-prime -> non-prime). "
            "- BCNF (Boyce-Codd Normal Form): For every non-trivial functional dependency X -> Y, X must be a superkey."
        ),
        "source": "MasteryLoop DBMS Concepts, Module 5"
    },

    # 7. Operating Systems: Synchronization & Deadlocks
    {
        "skill_code": "OS_SYNC_DEADLOCK",
        "title": "Deadlock Characterization: Coffman's Four Conditions",
        "content_type": "CONCEPT",
        "content": (
            "A deadlock occurs when a set of processes are blocked because each holds a resource and waits for another. "
            "Four necessary Coffman conditions must hold simultaneously: "
            "1. Mutual Exclusion: At least one resource is held in non-shareable mode. "
            "2. Hold and Wait: A process holds at least one resource and requests additional ones. "
            "3. No Preemption: Resources cannot be forcibly taken from a process. "
            "4. Circular Wait: A closed chain of processes exists such that each waits for a resource held by the next."
        ),
        "source": "MasteryLoop Operating Systems Guide, Sec 6"
    },

    # 8. Computer Networks: TCP/IP Stack
    {
        "skill_code": "NET_TCP_UDP",
        "title": "TCP 3-Way Handshake and Reliable Connection Establishment",
        "content_type": "CONCEPT",
        "content": (
            "The Transmission Control Protocol (TCP) ensures reliable byte-stream delivery using a 3-way handshake: "
            "1. Step 1 (SYN): Client sends SYN packet with an initial sequence number (ISN_c). "
            "2. Step 2 (SYN-ACK): Server acknowledges receipt with ACK = ISN_c + 1, and sends its own SYN with ISN_s. "
            "3. Step 3 (ACK): Client acknowledges server sequence number with ACK = ISN_s + 1. "
            "Connection is now ESTABLISHED."
        ),
        "source": "MasteryLoop Networking Protocol Standards"
    },

    # 9. Machine Learning: Model Evaluation
    {
        "skill_code": "ML_EVALUATION",
        "title": "Evaluation Metrics for Imbalanced Datasets: Precision, Recall, and PR-AUC",
        "content_type": "CONCEPT",
        "content": (
            "On imbalanced classification tasks (e.g. 99% negative, 1% positive), accuracy is dangerously misleading. "
            "- Precision = TP / (TP + FP): Fraction of positive predictions that were correct. "
            "- Recall = TP / (TP + FN): Fraction of actual positive instances correctly retrieved. "
            "- F1-Score = 2 * (Precision * Recall) / (Precision + Recall): Harmonic mean balancing both. "
            "- Area Under Precision-Recall Curve (PR-AUC) evaluates classifier quality without distortion from true negatives."
        ),
        "source": "MasteryLoop Machine Learning Principles, Ch 4"
    },

    # 10. Quantitative Aptitude: Percentages & Compounding
    {
        "skill_code": "QNT_PERCENTAGES",
        "title": "Successive Percentage Changes and Compounding Formula",
        "content_type": "FORMULA",
        "content": (
            "Formula for Successive Percentage Changes: "
            "If a value undergoes successive changes of +a% and +b%, the effective net percentage change is: "
            "Net Change = a + b + (a * b / 100) %. "
            "Example: Increasing by 20% followed by a 20% discount yields: "
            "+20 - 20 + (20 * -20 / 100) = -4% net decrease, NOT 0%."
        ),
        "source": "MasteryLoop Quantitative Aptitude Handbook, Sec 2"
    }
]


def seed_rag_knowledge(db: Session) -> dict:
    """Idempotently ingests curriculum knowledge chunks into Qdrant."""
    skills = db.query(Skill).all()
    skill_by_code = {s.code: s for s in skills}

    stats = {"indexed": 0, "failed": 0}

    for idx, chunk in enumerate(CURRICULUM_KNOWLEDGE_CHUNKS):
        skill = skill_by_code.get(chunk["skill_code"])
        chunk_id = f"chunk_{chunk['skill_code']}_{idx}"

        metadata = {
            "title": chunk["title"],
            "skill_code": chunk["skill_code"],
            "skill_id": skill.id if skill else "",
            "content_type": chunk["content_type"],
            "source": chunk["source"],
            "domain": skill.subtopic.topic.domain.name if (skill and skill.subtopic and skill.subtopic.topic and skill.subtopic.topic.domain) else "General Placement",
            "topic": skill.subtopic.topic.name if (skill and skill.subtopic and skill.subtopic.topic) else "Foundations",
            "version": "1.0"
        }

        success = vector_store.upsert_chunk(
            chunk_id=chunk_id,
            content=chunk["content"],
            metadata=metadata
        )

        if success:
            stats["indexed"] += 1
        else:
            stats["failed"] += 1

    logger.info(f"RAG Knowledge Ingestion complete: {stats} (Total Qdrant points: {vector_store.get_chunk_count()})")
    return stats


if __name__ == "__main__":
    init_db()
    with SessionLocal() as session:
        res = seed_rag_knowledge(session)
        print("RAG Ingestion result:", res)
