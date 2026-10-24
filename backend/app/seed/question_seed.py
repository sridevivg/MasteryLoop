"""
Repeatable Seed Process for MasteryLoop Assessment Items Bank.
Seeds psychometrically-parameterized items (MCQ and Coding) across all 11 domains.
Each item includes stem, options, keyed answer, pedagogical explanation,
distractor error models, and 2PL IRT parameters (a, b, point_biserial).
"""

import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.models.curriculum import Skill
from app.models.item import Item, ItemState, ItemOrigin, ItemType

from app.seed.bank_verbal import VERBAL_ITEMS
from app.seed.bank_quant import QUANT_ITEMS
from app.seed.bank_logic import LOGIC_ITEMS
from app.seed.bank_prog import PROG_ITEMS
from app.seed.bank_dsa import DSA_ITEMS
from app.seed.bank_oop import OOP_ITEMS
from app.seed.bank_dbms import DBMS_ITEMS
from app.seed.bank_os import OS_ITEMS
from app.seed.bank_networks import NETWORKS_ITEMS
from app.seed.bank_sql import SQL_ITEMS
from app.seed.bank_ml import ML_ITEMS

logger = logging.getLogger("masteryloop.item_seed")

SEED_ITEMS = [
    # --- VERBAL ABILITY ---
    {
        "skill_code": "VRB_SUBJECT_VERB",
        "item_type": ItemType.MCQ,
        "stem": "Select the grammatically correct sentence regarding subject-verb agreement:\n\n*\"Either the system administrator or the network engineers _____ responsible for configuring the router.\"*",
        "options": [
            {"id": "A", "text": "is", "is_distractor": True},
            {"id": "B", "text": "are", "is_distractor": False},
            {"id": "C", "text": "was", "is_distractor": True},
            {"id": "D", "text": "has been", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "In an 'either... or' correlative conjunction, the verb agrees with the closer subject. Since 'network engineers' is plural, the plural verb 'are' is required.",
        "distractor_explanations": {
            "A": "Error: Assumed agreement with the initial singular subject 'system administrator' rather than the closer plural subject.",
            "C": "Error: Incorrect singular past tense; does not match the closer plural subject.",
            "D": "Error: Incorrect singular perfect verb phrase."
        },
        "a": 1.25,
        "b": -0.40,
        "point_biserial": 0.42
    },
    {
        "skill_code": "VRB_MODIFIERS",
        "item_type": ItemType.MCQ,
        "stem": "Identify the sentence that avoids a dangling or misplaced modifier:",
        "options": [
            {"id": "A", "text": "Having compiled the source code, the executable was deployed by the CI/CD pipeline.", "is_distractor": True},
            {"id": "B", "text": "Having compiled the source code, the developer deployed the executable to the staging server.", "is_distractor": False},
            {"id": "C", "text": "To improve performance, several database indexes were added by the server.", "is_distractor": True},
            {"id": "D", "text": "While debugging the memory leak, the laptop battery ran out.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "A participial phrase ('Having compiled the source code') must immediately modify the agent who performed the action ('the developer'). In option B, the developer is the subject performing the compilation.",
        "distractor_explanations": {
            "A": "Dangling modifier: 'the executable' is placed as the subject, implying the executable compiled itself.",
            "C": "Misplaced modifier: 'the server' cannot actively intend to improve performance.",
            "D": "Dangling modifier: implies the laptop battery was actively debugging the memory leak."
        },
        "a": 1.45,
        "b": 0.60,
        "point_biserial": 0.45
    },

    # --- QUANTITATIVE APTITUDE ---
    {
        "skill_code": "QNT_NUMBERS",
        "item_type": ItemType.MCQ,
        "stem": "What is the remainder when $2^{100}$ is divided by 7?",
        "options": [
            {"id": "A", "text": "1", "is_distractor": True},
            {"id": "B", "text": "2", "is_distractor": False},
            {"id": "C", "text": "4", "is_distractor": True},
            {"id": "D", "text": "6", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "By Fermat's Little Theorem or modular cyclicity: $2^1 \\equiv 2$, $2^2 \\equiv 4$, $2^3 = 8 \\equiv 1 \\pmod{7}$. The powers repeat with period 3. Since $100 = 3 \\times 33 + 1$, $2^{100} \\equiv (2^3)^{33} \\times 2^1 \\equiv 1^{33} \\times 2 \\equiv 2 \\pmod{7}$.",
        "distractor_explanations": {
            "A": "Error: Assumed $2^3 \\equiv 1$ implies $2^{100} \\equiv 1$, forgetting the remainder $100 \\pmod 3 = 1$.",
            "C": "Error: Confused the remainder with $2^2 \\equiv 4$.",
            "D": "Error: Calculation sign error."
        },
        "a": 1.60,
        "b": 0.35,
        "point_biserial": 0.46
    },
    {
        "skill_code": "QNT_PERCENTAGES",
        "item_type": ItemType.MCQ,
        "stem": "A cloud server's monthly billing rate was increased by 20%, and subsequently discounted by 20% during a promotional period. Compared to the original price, the net change is:",
        "options": [
            {"id": "A", "text": "No change (0%)", "is_distractor": True},
            {"id": "B", "text": "4% decrease", "is_distractor": False},
            {"id": "C", "text": "4% increase", "is_distractor": True},
            {"id": "D", "text": "2% decrease", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Successive percentage change formula: $Net = a + b + \\frac{ab}{100} = +20 - 20 + \\frac{(20)(-20)}{100} = -4\\%$. The price decreases by 4%.",
        "distractor_explanations": {
            "A": "Common misconception: Assuming equal positive and negative percentage changes cancel out linearly.",
            "C": "Error: Arithmetic sign error in compounding.",
            "D": "Error: Dividing net change by 2."
        },
        "a": 1.30,
        "b": -0.50,
        "point_biserial": 0.40
    },

    # --- LOGICAL REASONING ---
    {
        "skill_code": "LOG_SYLLOGISMS",
        "item_type": ItemType.MCQ,
        "stem": "Statements:\n1. All microservices communicate via REST.\n2. Some REST endpoints use JSON Web Tokens.\n\nConclusions:\nI. Some microservices use JSON Web Tokens.\nII. All microservices use JSON Web Tokens.",
        "options": [
            {"id": "A", "text": "Only conclusion I follows", "is_distractor": True},
            {"id": "B", "text": "Only conclusion II follows", "is_distractor": True},
            {"id": "C", "text": "Neither conclusion I nor II definitively follows", "is_distractor": False},
            {"id": "D", "text": "Both conclusions I and II follow", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "The term 'REST endpoints' is not distributed in premise 2 ('Some REST endpoints'). The specific endpoints that use JWTs may belong to non-microservice architectures. Thus, neither conclusion can be definitively deduced.",
        "distractor_explanations": {
            "A": "Fallacy of the undistributed middle: Conflating 'some endpoints' with the specific subset used by microservices.",
            "B": "Overgeneralization error: Concluding 'All' from a 'Some' premise.",
            "D": "Error: Assuming both affirmative syllogism extensions hold."
        },
        "a": 1.40,
        "b": 0.50,
        "point_biserial": 0.44
    },

    # --- PROGRAMMING FUNDAMENTALS ---
    {
        "skill_code": "PRG_VARIABLES",
        "item_type": ItemType.MCQ,
        "stem": "In Python, what is the output of the following snippet?\n\n```python\nx = [1, 2, 3]\ny = x\ny.append(4)\nprint(len(x))\n```",
        "options": [
            {"id": "A", "text": "3", "is_distractor": True},
            {"id": "B", "text": "4", "is_distractor": False},
            {"id": "C", "text": "Raises an AttributeError", "is_distractor": True},
            {"id": "D", "text": "None", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "In Python, variable assignment binds a reference to the existing object. 'y = x' does not copy the list; both x and y reference the same list in memory. Mutating y mutates x.",
        "distractor_explanations": {
            "A": "Misconception: Believed assignment creates an independent deep copy of the list.",
            "C": "Syntax error belief: Thought lists do not have an append method.",
            "D": "Confused the return value of append() with the length of x."
        },
        "a": 1.15,
        "b": -0.75,
        "point_biserial": 0.38
    },
    {
        "skill_code": "PRG_RECURSION",
        "item_type": ItemType.MCQ,
        "stem": "What is the return value of `mystery(4)`?\n\n```python\ndef mystery(n):\n    if n <= 1:\n        return 1\n    return n * mystery(n - 1)\n```",
        "options": [
            {"id": "A", "text": "10", "is_distractor": True},
            {"id": "B", "text": "16", "is_distractor": True},
            {"id": "C", "text": "24", "is_distractor": False},
            {"id": "D", "text": "120", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "This is the factorial function: mystery(4) = 4 * mystery(3) = 4 * 3 * mystery(2) = 4 * 3 * 2 * 1 = 24.",
        "distractor_explanations": {
            "A": "Error: Computed the triangular sum 4 + 3 + 2 + 1 = 10 instead of multiplication.",
            "B": "Error: Computed power $4^2 = 16$.",
            "D": "Error: Computed 5! = 120."
        },
        "a": 1.35,
        "b": -0.20,
        "point_biserial": 0.41
    },

    # --- DATA STRUCTURES & ALGORITHMS ---
    {
        "skill_code": "DSA_ARRAYS",
        "item_type": ItemType.MCQ,
        "stem": "What is the worst-case time complexity of finding a pair of numbers in a sorted array of size $N$ that sum to a target value using the two-pointer technique?",
        "options": [
            {"id": "A", "text": "O(1)", "is_distractor": True},
            {"id": "B", "text": "O(log N)", "is_distractor": True},
            {"id": "C", "text": "O(N)", "is_distractor": False},
            {"id": "D", "text": "O(N^2)", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "Because the array is already sorted, the two pointers start at opposite ends and move toward each other at most once per iteration. The array is traversed in a single pass of at most N steps: O(N).",
        "distractor_explanations": {
            "A": "Error: Constant time is impossible as all candidate pairs cannot be checked without reading elements.",
            "B": "Error: Confused with binary search for a single element.",
            "D": "Error: This is the brute-force nested loop complexity, missing the advantage of two pointers on sorted data."
        },
        "a": 1.40,
        "b": -0.30,
        "point_biserial": 0.43
    },
    {
        "skill_code": "DSA_BST",
        "item_type": ItemType.MCQ,
        "stem": "Which traversal of a valid Binary Search Tree (BST) produces keys in strictly ascending sorted order?",
        "options": [
            {"id": "A", "text": "Pre-order traversal", "is_distractor": True},
            {"id": "B", "text": "In-order traversal", "is_distractor": False},
            {"id": "C", "text": "Post-order traversal", "is_distractor": True},
            {"id": "D", "text": "Level-order traversal", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "In-order traversal visits (Left Subtree, Current Node, Right Subtree). By BST property (all left keys < root < all right keys), this recursively yields keys in strictly non-decreasing sorted order.",
        "distractor_explanations": {
            "A": "Error: Pre-order visits Root first, which does not output sorted order.",
            "C": "Error: Post-order visits Root last, often used for tree deletion.",
            "D": "Error: Level-order visits by tree depth breadth-first."
        },
        "a": 1.30,
        "b": -0.45,
        "point_biserial": 0.39
    },
    {
        "skill_code": "DSA_DYNAMIC_PROG",
        "item_type": ItemType.MCQ,
        "stem": "Which two core mathematical properties must a problem satisfy to be solvable via Dynamic Programming?",
        "options": [
            {"id": "A", "text": "Greedy choice property and linear data representation", "is_distractor": True},
            {"id": "B", "text": "Optimal substructure and overlapping subproblems", "is_distractor": False},
            {"id": "C", "text": "Divide-and-conquer divisibility and tail recursion", "is_distractor": True},
            {"id": "D", "text": "Monotonicity and acyclic state graphs only", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Optimal substructure means an optimal solution contains optimal solutions to subproblems. Overlapping subproblems means subproblems are repeatedly computed, allowing memoization or tabulation.",
        "distractor_explanations": {
            "A": "Error: Greedy choice property characterizes Greedy algorithms, not general DP.",
            "C": "Error: Divide and conquer handles non-overlapping subproblems (e.g. Merge Sort).",
            "D": "Error: Incomplete and inaccurate characterization."
        },
        "a": 1.65,
        "b": 0.70,
        "point_biserial": 0.47
    },

    # --- SQL ---
    {
        "skill_code": "SQL_JOINS",
        "item_type": ItemType.MCQ,
        "stem": "Consider tables `Students` (10 rows) and `Enrollments` (8 rows, where 6 match student IDs). How many rows does `SELECT * FROM Students LEFT JOIN Enrollments ON Students.id = Enrollments.student_id` return at minimum?",
        "options": [
            {"id": "A", "text": "6", "is_distractor": True},
            {"id": "B", "text": "8", "is_distractor": True},
            {"id": "C", "text": "10", "is_distractor": False},
            {"id": "D", "text": "14", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "A LEFT JOIN preserves all rows from the left table (`Students`). Since there are 10 students, every student appears at least once (with NULLs for unmatched enrollments). Thus, at least 10 rows are guaranteed.",
        "distractor_explanations": {
            "A": "Error: Confused LEFT JOIN with INNER JOIN (which returns only matching rows).",
            "B": "Error: Selected the size of the right table.",
            "D": "Error: Arbitrary addition of numbers."
        },
        "a": 1.40,
        "b": 0.20,
        "point_biserial": 0.44
    },

    # --- OBJECT-ORIENTED PROGRAMMING ---
    {
        "skill_code": "OOP_POLYMORPHISM",
        "item_type": ItemType.MCQ,
        "stem": "Which mechanism enables runtime (dynamic) polymorphism in object-oriented languages such as Java or C++?",
        "options": [
            {"id": "A", "text": "Method overloading at compile time", "is_distractor": True},
            {"id": "B", "text": "Virtual method tables (vtable) and method overriding", "is_distractor": False},
            {"id": "C", "text": "Private variable encapsulation", "is_distractor": True},
            {"id": "D", "text": "Multiple constructor declarations", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Dynamic polymorphism resolves the method call at runtime based on the actual object instance type, implemented via virtual method tables (vtables) and dynamic dispatch.",
        "distractor_explanations": {
            "A": "Error: Method overloading is static (compile-time) polymorphism, resolved by signature at compilation.",
            "C": "Error: Encapsulation relates to data hiding, not polymorphic dispatch.",
            "D": "Error: Constructor overloading is static initialization."
        },
        "a": 1.35,
        "b": 0.15,
        "point_biserial": 0.43
    },

    # --- DBMS ---
    {
        "skill_code": "DBMS_NORMALIZATION",
        "item_type": ItemType.MCQ,
        "stem": "A relational table is in Boyce-Codd Normal Form (BCNF) if and only if for every non-trivial functional dependency $X \\rightarrow Y$:",
        "options": [
            {"id": "A", "text": "$Y$ is a subset of a prime attribute", "is_distractor": True},
            {"id": "B", "text": "$X$ is a superkey", "is_distractor": False},
            {"id": "C", "text": "The table has no composite primary keys", "is_distractor": True},
            {"id": "D", "text": "No transitive dependencies exist from non-prime to prime attributes", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "BCNF requires that for every non-trivial functional dependency X -> Y, the determinant X must be a superkey. This is stricter than 3NF, which allows Y to be a prime attribute.",
        "distractor_explanations": {
            "A": "Error: This is the relaxed clause allowed in 3NF, but eliminated in BCNF.",
            "C": "Error: BCNF tables frequently have composite keys.",
            "D": "Error: Inaccurate definition of normalization rules."
        },
        "a": 1.50,
        "b": 0.65,
        "point_biserial": 0.46
    },

    # --- OPERATING SYSTEMS ---
    {
        "skill_code": "OS_SYNC_DEADLOCK",
        "item_type": ItemType.MCQ,
        "stem": "Which of the following is NOT one of Coffman's four necessary conditions for a system deadlock to occur?",
        "options": [
            {"id": "A", "text": "Mutual exclusion", "is_distractor": True},
            {"id": "B", "text": "Hold and wait", "is_distractor": True},
            {"id": "C", "text": "Preemption allowed by the kernel", "is_distractor": False},
            {"id": "D", "text": "Circular wait", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "Coffman's 4 conditions are: (1) Mutual Exclusion, (2) Hold and Wait, (3) No Preemption (resources cannot be forcibly confiscated), and (4) Circular Wait. Allowing preemption prevents or breaks deadlocks.",
        "distractor_explanations": {
            "A": "Mutual exclusion is a required Coffman condition.",
            "B": "Hold and wait is a required Coffman condition.",
            "D": "Circular wait is a required Coffman condition."
        },
        "a": 1.30,
        "b": 0.10,
        "point_biserial": 0.42
    },

    # --- COMPUTER NETWORKS ---
    {
        "skill_code": "NET_TCP_UDP",
        "item_type": ItemType.MCQ,
        "stem": "Which sequence correctly represents the flags exchanged during the standard TCP 3-way connection handshake?",
        "options": [
            {"id": "A", "text": "SYN -> ACK -> SYN-ACK", "is_distractor": True},
            {"id": "B", "text": "SYN -> SYN-ACK -> ACK", "is_distractor": False},
            {"id": "C", "text": "ACK -> SYN -> ACK", "is_distractor": True},
            {"id": "D", "text": "FIN -> ACK -> FIN-ACK", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "1. Client sends SYN (Synchronize sequence numbers). 2. Server responds with SYN-ACK (Synchronize and Acknowledge). 3. Client sends ACK (Acknowledge server sequence number).",
        "distractor_explanations": {
            "A": "Error: Inverted order of the second and third packets.",
            "C": "Error: A connection cannot be initiated with an ACK.",
            "D": "Error: FIN packets are used for connection teardown, not establishment."
        },
        "a": 1.20,
        "b": -0.60,
        "point_biserial": 0.40
    },

    # --- MACHINE LEARNING ---
    {
        "skill_code": "ML_EVALUATION",
        "item_type": ItemType.MCQ,
        "stem": "In an imbalanced fraud detection dataset where 99% of transactions are legitimate and 1% are fraudulent, which evaluation metric is most misleading if used as the primary measure of model performance?",
        "options": [
            {"id": "A", "text": "Precision", "is_distractor": True},
            {"id": "B", "text": "Recall", "is_distractor": True},
            {"id": "C", "text": "Raw Accuracy", "is_distractor": False},
            {"id": "D", "text": "Area under the Precision-Recall curve (PR-AUC)", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "A dummy classifier that predicts 'Legitimate' for every transaction achieves 99% raw accuracy while detecting zero fraud cases. PR-AUC, F1-score, or Recall on the minority class are required.",
        "distractor_explanations": {
            "A": "Precision specifically focuses on the correctness of positive predictions.",
            "B": "Recall measures the capture rate of true fraud instances.",
            "D": "PR-AUC is the recommended gold-standard metric for severely imbalanced datasets."
        },
        "a": 1.45,
        "b": -0.10,
        "point_biserial": 0.45
    },

    # --- CODING ITEM ---
    {
        "skill_code": "DSA_ARRAYS",
        "item_type": ItemType.CODING,
        "stem": "### Two Sum Problem\n\nGiven an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume each input has exactly one solution, and you may not use the same element twice. Return the indices sorted in ascending order `[i, j]`.\n\n**Example:**\n```python\nnums = [2, 7, 11, 15], target = 9\n# Output: [0, 1] because nums[0] + nums[1] == 9\n```",
        "options": [],
        "answer_key": "[0, 1]",
        "code_template": "def two_sum(nums: list[int], target: int) -> list[int]:\n    # Implement your O(N) solution here\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []\n",
        "test_cases": [
            {"input": "nums = [2, 7, 11, 15], target = 9", "expected": "[0, 1]", "hidden": False},
            {"input": "nums = [3, 2, 4], target = 6", "expected": "[1, 2]", "hidden": False},
            {"input": "nums = [3, 3], target = 6", "expected": "[0, 1]", "hidden": False},
            {"input": "nums = [1, 5, 8, 12, 19], target = 20", "expected": "[0, 4]", "hidden": True}
        ],
        "explanation": "Using a hash map allows looking up the required complement (target - num) in O(1) average time, reducing overall complexity from O(N^2) to O(N) time and O(N) space.",
        "distractor_explanations": {},
        "a": 1.70,
        "b": 0.40,
        "point_biserial": 0.48
    }
]


ALL_SEED_ITEMS = (
    SEED_ITEMS +
    VERBAL_ITEMS +
    QUANT_ITEMS +
    LOGIC_ITEMS +
    PROG_ITEMS +
    DSA_ITEMS +
    OOP_ITEMS +
    DBMS_ITEMS +
    OS_ITEMS +
    NETWORKS_ITEMS +
    SQL_ITEMS +
    ML_ITEMS
)


def seed_questions(db: Session) -> dict:
    """Idempotently seeds psychometrically validated assessment questions."""
    stats = {"created": 0, "skipped": 0}

    # Cache skills by code
    skills = db.query(Skill).all()
    skills_by_code = {s.code: s.id for s in skills}

    for item_data in ALL_SEED_ITEMS:
        skill_id = skills_by_code.get(item_data["skill_code"])
        if not skill_id:
            logger.warning(f"Skill code '{item_data['skill_code']}' not found in curriculum. Skipping item.")
            continue

        # Check if item with identical stem already exists to maintain idempotency
        existing = db.query(Item).filter(
            Item.primary_skill_id == skill_id,
            Item.stem == item_data["stem"]
        ).first()

        if existing:
            stats["skipped"] += 1
            continue

        item = Item(
            primary_skill_id=skill_id,
            item_type=item_data.get("item_type", ItemType.MCQ),
            stem=item_data["stem"],
            options=item_data["options"],
            answer_key=item_data["answer_key"],
            explanation=item_data["explanation"],
            distractor_explanations=item_data.get("distractor_explanations", {}),
            code_template=item_data.get("code_template"),
            test_cases=item_data.get("test_cases", []),
            a=item_data["a"],
            b=item_data["b"],
            point_biserial=item_data["point_biserial"],
            is_calibrated=1,  # Human seed items with benchmarked psychometrics
            state=ItemState.ACTIVE,
            origin=ItemOrigin.HUMAN
        )
        db.add(item)
        stats["created"] += 1

    db.commit()
    logger.info(f"Question seeding complete: {stats}")
    return stats


if __name__ == "__main__":
    init_db()
    with SessionLocal() as session:
        res = seed_questions(session)
        print("Questions seed result:", res)
