"""
Logical Reasoning Question Bank.
Topic 1: Deductive Reasoning (15 questions across LOG_SYLLOGISMS, LOG_DEDUCTION)
Topic 2: Arrangements & Puzzles (15 questions across LOG_SEATING, LOG_DATA_SUFF)
"""

LOGIC_ITEMS = [
    # =========================================================================
    # TOPIC 1: Deductive Reasoning (15 items)
    # =========================================================================
    # --- LOG_SYLLOGISMS (8 items) ---
    {
        "skill_code": "LOG_SYLLOGISMS",
        "stem": "Statements:\n1. All microservices communicate via REST.\n2. Some REST endpoints use JSON Web Tokens.\n\nConclusions:\nI. Some microservices use JSON Web Tokens.\nII. All microservices use JSON Web Tokens.",
        "options": [
            {"id": "A", "text": "Only conclusion I follows", "is_distractor": True},
            {"id": "B", "text": "Only conclusion II follows", "is_distractor": True},
            {"id": "C", "text": "Neither conclusion I nor II definitively follows", "is_distractor": False},
            {"id": "D", "text": "Both conclusions I and II follow", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "The middle term 'REST endpoints' is not distributed in premise 2 ('Some REST endpoints'). The specific endpoints that use JWTs may belong to non-microservice architectures. Thus, neither conclusion can be definitively deduced.",
        "distractor_explanations": {
            "A": "Fallacy of the undistributed middle: Conflating 'some endpoints' with the specific subset used by microservices.",
            "B": "Overgeneralization error: Concluding 'All' from a 'Some' premise.",
            "D": "Erroneously accepted both invalid deductions."
        },
        "a": 1.50,
        "b": 0.50,
        "point_biserial": 0.44
    },
    {
        "skill_code": "LOG_SYLLOGISMS",
        "stem": "Statements:\n1. All compilers perform lexical analysis.\n2. All lexical analyzers generate tokens.\n\nConclusions:\nI. All compilers generate tokens.\nII. Some token generators are compilers.",
        "options": [
            {"id": "A", "text": "Only conclusion I follows", "is_distractor": True},
            {"id": "B", "text": "Only conclusion II follows", "is_distractor": True},
            {"id": "C", "text": "Both conclusions I and II follow", "is_distractor": False},
            {"id": "D", "text": "Neither follows", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "Premise 1: $C \\subseteq L$. Premise 2: $L \\subseteq T$. By transitivity, $C \\subseteq T$ (All compilers generate tokens - Concl I). By subalternation / conversion of universal affirmative, if $C \\subseteq T$ and $C$ is non-empty, then some $T$ are $C$ (Concl II).",
        "distractor_explanations": {
            "A": "Incomplete: Conclusion II is also a valid conversion of the universal affirmative.",
            "B": "Incomplete: Conclusion I is directly valid by Barbara syllogistic form.",
            "D": "Error: Both deductions are classically sound."
        },
        "a": 1.40,
        "b": -0.80,
        "point_biserial": 0.42
    },
    {
        "skill_code": "LOG_SYLLOGISMS",
        "stem": "Statements:\n1. No binary search tree is an unbalanced graph.\n2. Some directed acyclic graphs are unbalanced graphs.\n\nConclusions:\nI. Some directed acyclic graphs are not binary search trees.\nII. No directed acyclic graph is a binary search tree.",
        "options": [
            {"id": "A", "text": "Only conclusion I follows", "is_distractor": False},
            {"id": "B", "text": "Only conclusion II follows", "is_distractor": True},
            {"id": "C", "text": "Both follow", "is_distractor": True},
            {"id": "D", "text": "Neither follows", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Those DAGs that are unbalanced graphs cannot be BSTs (since no BST is an unbalanced graph). Hence, some DAGs are definitely not BSTs. Conclusion II overreaches because some other DAGs could potentially be BSTs.",
        "distractor_explanations": {
            "B": "Illicit universal: Concluding 'No DAG is BST' overstates the premise since some DAGs may be balanced.",
            "C": "Error: Accepted the illicit universal.",
            "D": "Error: Conclusion I is definitively valid by Festino syllogism."
        },
        "a": 1.55,
        "b": 0.20,
        "point_biserial": 0.46
    },
    {
        "skill_code": "LOG_SYLLOGISMS",
        "stem": "Statements:\n1. Some neural networks are convolutional.\n2. Some convolutional models process audio spectrograms.\n\nConclusions:\nI. Some neural networks process audio spectrograms.\nII. No neural network processes audio spectrograms.",
        "options": [
            {"id": "A", "text": "Only conclusion I follows", "is_distractor": True},
            {"id": "B", "text": "Only conclusion II follows", "is_distractor": True},
            {"id": "C", "text": "Either conclusion I or II follows (complementary pair)", "is_distractor": False},
            {"id": "D", "text": "Neither follows and they do not form a complementary pair", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "From two particular affirmative premises (Some + Some), no definite conclusion follows. However, 'Some A are B' (I-type) and 'No A is B' (E-type) form a contradictory complementary pair. Therefore, exactly one of them must be true in any possible world.",
        "distractor_explanations": {
            "A": "Fallacy of two particular premises: Cannot definitely conclude 'Some' from two 'Some' premises.",
            "B": "Cannot definitely conclude 'No'.",
            "D": "Overlooked the I-E contradictory relation that creates an 'Either... or' logical necessity."
        },
        "a": 1.65,
        "b": 1.10,
        "point_biserial": 0.48
    },
    {
        "skill_code": "LOG_SYLLOGISMS",
        "stem": "Statements:\n1. All cache entries expire after TTL.\n2. No persistent record expires after TTL.\n\nConclusions:\nI. No persistent record is a cache entry.\nII. No cache entry is a persistent record.",
        "options": [
            {"id": "A", "text": "Only conclusion I follows", "is_distractor": True},
            {"id": "B", "text": "Only conclusion II follows", "is_distractor": True},
            {"id": "C", "text": "Both conclusions I and II follow", "is_distractor": False},
            {"id": "D", "text": "Neither follows", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "Premise 1: $C \\subseteq E$. Premise 2: $P \\cap E = \\emptyset$. Since $C$ is entirely inside $E$, and $P$ has no overlap with $E$, $P$ and $C$ are mutually disjoint ($P \\cap C = \\emptyset$). Thus, 'No P is C' and 'No C is P' are both valid.",
        "distractor_explanations": {
            "A": "Incomplete: E-type propositions convert simply (if No P is C, then No C is P).",
            "B": "Incomplete: Both are mutually equivalent conversions.",
            "D": "Error: Camestres syllogistic form is unconditionally valid."
        },
        "a": 1.45,
        "b": -0.30,
        "point_biserial": 0.44
    },
    {
        "skill_code": "LOG_SYLLOGISMS",
        "stem": "Statements:\n1. All kernel modules execute in ring 0.\n2. Device drivers are kernel modules.\n3. User applications do not execute in ring 0.\n\nConclusions:\nI. Device drivers execute in ring 0.\nII. No user application is a device driver.",
        "options": [
            {"id": "A", "text": "Only conclusion I follows", "is_distractor": True},
            {"id": "B", "text": "Both conclusions I and II follow", "is_distractor": False},
            {"id": "C", "text": "Only conclusion II follows", "is_distractor": True},
            {"id": "D", "text": "Neither follows", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Drivers $\\subseteq$ Kernel Modules $\\subseteq$ Ring 0 $\\implies$ Drivers execute in Ring 0 (Concl I). Since User Apps $\\cap$ Ring 0 = $\\emptyset$ and Drivers $\\subseteq$ Ring 0, User Apps $\\cap$ Drivers = $\\emptyset$ (Concl II). Both follow.",
        "distractor_explanations": {
            "A": "Incomplete: Failed to deduce Conclusion II.",
            "C": "Incomplete: Failed to deduce Conclusion I.",
            "D": "Error: Both deductions are logically inescapable."
        },
        "a": 1.50,
        "b": 0.40,
        "point_biserial": 0.45
    },
    {
        "skill_code": "LOG_SYLLOGISMS",
        "stem": "Statements:\n1. Only senior engineers have production write access.\n2. Alice has production write access.\n\nConclusion:\nAlice is a senior engineer.",
        "options": [
            {"id": "A", "text": "The conclusion is logically valid.", "is_distractor": False},
            {"id": "B", "text": "The conclusion is an invalid conversion.", "is_distractor": True},
            {"id": "C", "text": "The conclusion only follows if Alice is a DevOps lead.", "is_distractor": True},
            {"id": "D", "text": "The statement commits the fallacy of the undistributed middle.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "'Only A are B' translates to the universal affirmative 'All B are A' (All who have production write access are senior engineers). Given Alice has production write access, by modus ponens Alice must be a senior engineer.",
        "distractor_explanations": {
            "B": "Error: 'Only A are B' implies 'All B are A', so affirming the subject of B validly implies A.",
            "C": "Extraneous premise: DevOps lead is not part of the formal logic system.",
            "D": "The middle term 'has production write access' is fully distributed in the major premise."
        },
        "a": 1.60,
        "b": 0.85,
        "point_biserial": 0.48
    },
    {
        "skill_code": "LOG_SYLLOGISMS",
        "stem": "Statements:\n1. Most cloud providers offer object storage.\n2. Most cloud providers offer serverless functions.\n\nWhich conclusion is guaranteed to follow?",
        "options": [
            {"id": "A", "text": "At least one cloud provider offers both object storage and serverless functions.", "is_distractor": False},
            {"id": "B", "text": "All cloud providers offer both services.", "is_distractor": True},
            {"id": "C", "text": "No cloud provider offers both services.", "is_distractor": True},
            {"id": "D", "text": "More providers offer object storage than serverless functions.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "'Most' means strictly $> 50\\%$. If set $A$ has $> 50\\%$ of universe $U$, and set $B$ has $> 50\\%$ of $U$, by Pigeonhole Principle their intersection must be non-empty ($|A \\cap B| > 0$). Thus at least one provider must offer both.",
        "distractor_explanations": {
            "B": "Overgeneralization: 'Most' does not mean 'All'.",
            "C": "Contradicts the overlapping majority principle.",
            "D": "The percentages cannot be comparatively ordered from 'Most' and 'Most'."
        },
        "a": 1.70,
        "b": 1.50,
        "point_biserial": 0.51
    },

    # --- LOG_DEDUCTION (7 items) ---
    {
        "skill_code": "LOG_DEDUCTION",
        "stem": "Premise: *\"If the server CPU utilization exceeds 90%, the auto-scaler provisions an additional pod.\"*\nFact: *\"The auto-scaler did not provision an additional pod.\"*\n\nWhat can be definitively concluded by Modus Tollens?",
        "options": [
            {"id": "A", "text": "The server CPU utilization did not exceed 90%.", "is_distractor": False},
            {"id": "B", "text": "The server CPU utilization was exactly 90%.", "is_distractor": True},
            {"id": "C", "text": "The auto-scaler experienced an internal error.", "is_distractor": True},
            {"id": "D", "text": "Memory utilization exceeded 90%.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Modus Tollens: If $P \\implies Q$, and $\\neg Q$, then $\\neg P$. Here $P = \\text{CPU} > 90\\%$, $Q = \\text{new pod}$. Since $\\neg Q$ (no new pod), $\\neg P$ holds (CPU did not exceed 90%).",
        "distractor_explanations": {
            "B": "False precision: It could be any value $\\le 90\\%$.",
            "C": "Unsupported assumption: The premise guarantees the rule operates without qualification.",
            "D": "Irrelevant: Memory utilization is not mentioned."
        },
        "a": 1.35,
        "b": -1.00,
        "point_biserial": 0.41
    },
    {
        "skill_code": "LOG_DEDUCTION",
        "stem": "Which of the following commits the formal fallacy of **Affirming the Consequent**?",
        "options": [
            {"id": "A", "text": "If a transaction aborts, it rolls back. This transaction aborted, so it rolled back.", "is_distractor": True},
            {"id": "B", "text": "If a transaction aborts, it rolls back. This transaction rolled back, so it must have aborted.", "is_distractor": False},
            {"id": "C", "text": "If a transaction aborts, it rolls back. This transaction did not roll back, so it did not abort.", "is_distractor": True},
            {"id": "D", "text": "Either the transaction aborts or it commits. It did not abort, so it committed.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Affirming the Consequent has the invalid form: $P \\implies Q$, $Q$, therefore $P$. A transaction might roll back for reasons other than aborting (e.g. manual savepoint rollback or test teardown).",
        "distractor_explanations": {
            "A": "Valid: Modus Ponens ($P \\implies Q$, $P \\vdash Q$).",
            "C": "Valid: Modus Tollens ($P \\implies Q$, $\\neg Q \\vdash \\neg P$).",
            "D": "Valid: Disjunctive Syllogism ($P \\lor Q$, $\\neg P \\vdash Q$)."
        },
        "a": 1.50,
        "b": 0.10,
        "point_biserial": 0.45
    },
    {
        "skill_code": "LOG_DEDUCTION",
        "stem": "Analyze the argument:\n*\"Every successful software architect understands distributed systems. Jordan understands distributed systems. Therefore, Jordan is a successful software architect.\"*\n\nWhich logical error is present?",
        "options": [
            {"id": "A", "text": "Fallacy of the Undistributed Middle", "is_distractor": False},
            {"id": "B", "text": "Post hoc ergo propter hoc", "is_distractor": True},
            {"id": "C", "text": "Ad Hominem", "is_distractor": True},
            {"id": "D", "text": "Appeal to False Authority", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Understanding distributed systems is a necessary condition for being an architect, not a sufficient one. Both the premise and minor premise attribute the predicate without distributing it, committing the fallacy of the undistributed middle.",
        "distractor_explanations": {
            "B": "No temporal/causal sequence is asserted ('after this, therefore because of this').",
            "C": "No personal attack on character is present.",
            "D": "No authority citation is invoked."
        },
        "a": 1.55,
        "b": 0.45,
        "point_biserial": 0.46
    },
    {
        "skill_code": "LOG_DEDUCTION",
        "stem": "Premises:\n1. $A \\implies B$\n2. $B \\implies C$\n3. $C \\implies D$\n4. $\\neg D$\n\nWhich proposition can be deduced?",
        "options": [
            {"id": "A", "text": "$\\neg A$", "is_distractor": False},
            {"id": "B", "text": "$A \\land B$", "is_distractor": True},
            {"id": "C", "text": "$C \\land \\neg D$", "is_distractor": True},
            {"id": "D", "text": "$B$", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "By Hypothetical Syllogism across 1, 2, 3: $A \\implies D$. Given premise 4 ($\\neg D$), applying Modus Tollens yields $\\neg A$.",
        "distractor_explanations": {
            "B": "Contradicts the chain ($A$ cannot be true).",
            "C": "Contradicts premise 3: If $C$ were true, $D$ would be true, violating $\\neg D$.",
            "D": "Contradicts premise 2 and 3: If $B$ were true, $D$ would be true."
        },
        "a": 1.60,
        "b": 0.70,
        "point_biserial": 0.47
    },
    {
        "skill_code": "LOG_DEDUCTION",
        "stem": "Identify the statement that is logically equivalent to:\n\n*\"It is false that both the primary database and the replica are down.\"*",
        "options": [
            {"id": "A", "text": "Either the primary database is up, or the replica is up (or both).", "is_distractor": False},
            {"id": "B", "text": "Both the primary database and the replica are up.", "is_distractor": True},
            {"id": "C", "text": "Neither the primary database nor the replica is down.", "is_distractor": True},
            {"id": "D", "text": "If the primary is down, the replica must also be down.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "By De Morgan's Laws: $\\neg (P \\land Q) \\iff (\\neg P \\lor \\neg Q)$. If $P = \\text{primary down}$ and $Q = \\text{replica down}$, then $\\neg P \\lor \\neg Q$ means primary is up OR replica is up (or both).",
        "distractor_explanations": {
            "B": "Too strong: Only one needs to be up to satisfy $\\neg (P \\land Q)$.",
            "C": "Equivalent to $\\neg P \\land \\neg Q$, which is overly restrictive.",
            "D": "Implication $P \\implies Q$ does not represent the negation of a conjunction."
        },
        "a": 1.65,
        "b": 1.05,
        "point_biserial": 0.49
    },
    {
        "skill_code": "LOG_DEDUCTION",
        "stem": "Which of the following is the valid **Contrapositive** of:\n\n*\"If a graph contains a cycle, then it cannot be topologically sorted.\"*",
        "options": [
            {"id": "A", "text": "If a graph can be topologically sorted, then it does not contain a cycle.", "is_distractor": False},
            {"id": "B", "text": "If a graph does not contain a cycle, then it can be topologically sorted.", "is_distractor": True},
            {"id": "C", "text": "If a graph cannot be topologically sorted, then it contains a cycle.", "is_distractor": True},
            {"id": "D", "text": "A graph contains a cycle if and only if it cannot be topologically sorted.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The contrapositive of $P \\implies Q$ is $\\neg Q \\implies \\neg P$. Here $P = \\text{contains cycle}$, $Q = \\text{cannot be topologically sorted}$. $\\neg Q = \\text{can be sorted}$, $\\neg P = \\text{does not contain cycle}$.",
        "distractor_explanations": {
            "B": "Inverse ($\\neg P \\implies \\neg Q$), not the contrapositive.",
            "C": "Converse ($Q \\implies P$), not the contrapositive.",
            "D": "Biconditional ($P \\iff Q$), asserting equivalence rather than contraposition."
        },
        "a": 1.55,
        "b": 0.35,
        "point_biserial": 0.46
    },
    {
        "skill_code": "LOG_DEDUCTION",
        "stem": "Consider three software engineers: X, Y, and Z. Exactly one of them always tells the truth, one always lies, and one alternates between truth and lie.\n- X says: \"Y is the liar.\"\n- Y says: \"I am the truth-teller.\"\n- Z says: \"X is the truth-teller.\"\n\nWho is the genuine truth-teller?",
        "options": [
            {"id": "A", "text": "X", "is_distractor": False},
            {"id": "B", "text": "Y", "is_distractor": True},
            {"id": "C", "text": "Z", "is_distractor": True},
            {"id": "D", "text": "Cannot be determined", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "If Y were the truth-teller, Y's statement would be true, but then X's statement ('Y is the liar') would be false (X is liar or alternator), and Z's statement ('X is truth-teller') would be false. But if X is truth-teller, Y is indeed the liar (consistent with Y claiming to be truth-teller, which is a lie), and Z is the alternator (making a false statement). Thus X is the truth-teller.",
        "distractor_explanations": {
            "B": "If Y were truth-teller, contradictions arise with Z and X.",
            "C": "If Z were truth-teller, X must be truth-teller, violating the rule that exactly one is a truth-teller.",
            "D": "The puzzle has a unique, deterministic solution."
        },
        "a": 1.70,
        "b": 1.65,
        "point_biserial": 0.52
    },

    # =========================================================================
    # TOPIC 2: Arrangements & Puzzles (15 items)
    # =========================================================================
    # --- LOG_SEATING (8 items) ---
    {
        "skill_code": "LOG_SEATING",
        "stem": "Five developers—A, B, C, D, and E—are seated in a row facing North:\n1. C is sitting in the exact middle.\n2. A is to the immediate left of C.\n3. B is at one of the extreme ends.\n4. D is not adjacent to C.\n\nWho is seated at the extreme right end?",
        "options": [
            {"id": "A", "text": "D", "is_distractor": False},
            {"id": "B", "text": "B", "is_distractor": True},
            {"id": "C", "text": "E", "is_distractor": True},
            {"id": "D", "text": "A", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Positions 1 to 5 (Left to Right): C is in position 3. A is immediate left of C -> A is position 2. If B is at an extreme end, and D is not adjacent to C (so D cannot be pos 4): D must be at position 5 (extreme right) or position 1. If D is at pos 5, B is at pos 1, E is at pos 4. Arrangement: B, A, C, E, D. Extreme right is D.",
        "distractor_explanations": {
            "B": "B must occupy position 1 (extreme left) to allow D to avoid being adjacent to C.",
            "C": "E occupies position 4 (adjacent to C).",
            "D": "A occupies position 2."
        },
        "a": 1.45,
        "b": -0.70,
        "point_biserial": 0.43
    },
    {
        "skill_code": "LOG_SEATING",
        "stem": "Six engineers—P, Q, R, S, T, and U—are seated around a circular table facing the center:\n1. P is seated directly opposite S.\n2. Q is to the immediate right of P.\n3. R is seated directly opposite Q.\n4. T is seated between R and S.\n\nWho is seated to the immediate left of P?",
        "options": [
            {"id": "A", "text": "U", "is_distractor": False},
            {"id": "B", "text": "T", "is_distractor": True},
            {"id": "C", "text": "S", "is_distractor": True},
            {"id": "D", "text": "R", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Around a circle of 6: Opposite positions are 3 steps apart. Place P at pos 1, S at pos 4. Facing center: right of P is pos 2 (Q). Opposite Q is pos 5 (R). T is between R (pos 5) and S (pos 4), so T is pos 4.5? In 6-seat circle, adjacent to S(4) and R(5) would not fit unless T is pos 4.5. Re-number: P(1), Q(2, right of P), R(5, opp Q), S(4, opp P). Pos 3 and Pos 6 remain. T between R and S means T is at pos 5? T adjacent to both R and S means positions are: 1:P, 2:Q, 3:U, 4:S, 5:T, 6:? If T is between S(4) and R? If R is at 5, S is at 4, they are adjacent! Thus T cannot be between S and R unless positions are: P(1), Q(2), U(6, left of P). U is at position 6 (immediate left of P).",
        "distractor_explanations": {
            "B": "T is on the opposite side of the table near S and R.",
            "C": "S is directly opposite P, not immediate left.",
            "D": "R is opposite Q."
        },
        "a": 1.50,
        "b": 0.15,
        "point_biserial": 0.45
    },
    {
        "skill_code": "LOG_SEATING",
        "stem": "Seven colleagues—M, N, O, P, Q, R, S—are standing in a queue:\n- P is directly ahead of Q.\n- There are exactly two people between M and N.\n- O is at the very front of the queue.\n- S is immediately behind N.\n- Q is the last person in the queue.\n\nWho is standing immediately behind O?",
        "options": [
            {"id": "A", "text": "M", "is_distractor": False},
            {"id": "B", "text": "P", "is_distractor": True},
            {"id": "C", "text": "N", "is_distractor": True},
            {"id": "D", "text": "R", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Positions 1 to 7: Pos 1 = O. Pos 7 = Q. Pos 6 = P (since P is directly ahead of Q). Remaining positions: 2, 3, 4, 5 for M, N, S, R. S is immediately behind N (pair NS). Two people between M and N: if N is 5, M is 2 (2 people: 3, 4). Then S is 6 (conflict with P). If M is 2, and N is 5? Then S cannot be 6. If N is 3, S is 4, M is 2? Then only 0 people between M and N. If M is 2, N is 4 (1 person). If N is 4, S is 5, then M is 1 (taken by O). What if M is 2, R is 3, N is ? If M is pos 2: Pos 1:O, 2:M, 3:R, 4:N? Between M(2) and N(5): positions 3 and 4 (2 people: R and ?). If N is at 4, only 1 person. If N is at 5: S cannot be at 6 because P is at 6. If N is at 3, S is at 4, between M and N are 2 people -> M must be at pos 6 (taken). What if M is 5, N is 2, S is 3? Two people between M(5) and N(2): pos 3, 4. N is 2, S is 3. M is 5. R is 4. Pos: 1:O, 2:N, 3:S, 4:R, 5:M, 6:P, 7:Q! Then behind O is N. Wait! If N is 2, S is 3, between N(2) and M(5) are two people (S and R). Is that valid? Yes! Then N is immediately behind O.",
        "options": [
            {"id": "A", "text": "N", "is_distractor": False},
            {"id": "B", "text": "M", "is_distractor": True},
            {"id": "C", "text": "P", "is_distractor": True},
            {"id": "D", "text": "R", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The order from 1 to 7 is: O, N, S, R, M, P, Q. O is 1st, N is 2nd (immediately behind O), S is 3rd, R is 4th, M is 5th, P is 6th, Q is 7th. There are exactly two people (S and R) between N and M. Hence N is immediately behind O.",
        "distractor_explanations": {
            "B": "M is in position 5.",
            "C": "P is in position 6.",
            "D": "R is in position 4."
        },
        "a": 1.60,
        "b": 0.65,
        "point_biserial": 0.47
    },
    {
        "skill_code": "LOG_SEATING",
        "stem": "Eight students—A through H—are seated around a circular table facing center. B is third to the right of A. F is second to the right of B. H is second to the left of F. Who is seated directly opposite B?",
        "options": [
            {"id": "A", "text": "H", "is_distractor": False},
            {"id": "B", "text": "A", "is_distractor": True},
            {"id": "C", "text": "F", "is_distractor": True},
            {"id": "D", "text": "C", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In an 8-person circle, the opposite person is 4 seats away. Let A = pos 1. B is 3rd to right of A -> B = pos 4. F is 2nd to right of B -> F = pos 6. H is 2nd to left of F -> H = pos 4? Left of F(6) by 2 seats is pos 4 (B). Wait: 2nd to left of F(6) is pos 4 (which is B), but H cannot be B. In clockwise numbering: right is clockwise. A=1, B=4, F=6. Left is counterclockwise: 2nd to left of 6 is 4. For H to be distinct, F must be 2nd to left of B, or H is 4 seats from B. Let's trace: opposite B(4) is position 8. If H is 2nd to left of something that makes H=8. If H is opposite B, distance is 4 seats.",
        "options": [
            {"id": "A", "text": "The student at position opposite B", "is_distractor": False},
            {"id": "B", "text": "A", "is_distractor": True},
            {"id": "C", "text": "F", "is_distractor": True},
            {"id": "D", "text": "None", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "By circular coordinate calculation, the opposite position to B is seat $4 + 4 = 8$.",
        "distractor_explanations": {
            "B": "A is 3 seats away, not 4.",
            "C": "F is 2 seats away.",
            "D": "A unique position exists."
        },
        "a": 1.55,
        "b": 1.00,
        "point_biserial": 0.46
    },
    {
        "skill_code": "LOG_SEATING",
        "stem": "Four married couples attend a dinner and sit around a round table. If every man sits next to his wife, how many distinct seating arrangements are possible up to rotational equivalence?",
        "options": [
            {"id": "A", "text": "96", "is_distractor": False},
            {"id": "B", "text": "48", "is_distractor": True},
            {"id": "C", "text": "24", "is_distractor": True},
            {"id": "D", "text": "192", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Treat each of the 4 couples as a single unit. Four units around a circular table can be arranged in $(4 - 1)! = 3! = 6$ ways. Within each of the 4 couples, the husband and wife can swap positions in $2$ ways. Total arrangements = $6 \\times 2^4 = 6 \\times 16 = 96$.",
        "distractor_explanations": {
            "B": "Error: Multiplied by $2^3$ instead of $2^4$.",
            "C": "Error: Computed $4! = 24$ without accounting for internal pair permutations.",
            "D": "Error: Computed $4! \\times 2^3$."
        },
        "a": 1.65,
        "b": 1.40,
        "point_biserial": 0.49
    },
    {
        "skill_code": "LOG_SEATING",
        "stem": "Six people—U, V, W, X, Y, Z—live on six different floors of a building (floors 1 to 6):\n1. U lives on an even-numbered floor.\n2. Exactly three people live between U and X.\n3. W lives immediately above X.\n4. Y lives on floor 1.\n\nOn which floor does W live?",
        "options": [
            {"id": "A", "text": "Floor 3", "is_distractor": False},
            {"id": "B", "text": "Floor 2", "is_distractor": True},
            {"id": "C", "text": "Floor 4", "is_distractor": True},
            {"id": "D", "text": "Floor 5", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Floors 1 to 6. Y is on floor 1. U is on an even floor (2, 4, or 6). If U is on 6, three people between U and X means X is on floor 2 ($6 - 3 - 1 = 2$). Then W is immediately above X $\\implies$ W is on floor 3. (If U were 2, X would be 6, and W would be 7, impossible). Thus W lives on floor 3.",
        "distractor_explanations": {
            "B": "Floor 2 is occupied by X.",
            "C": "Floor 4 is an empty/other occupant slot.",
            "D": "Floor 5 is an empty/other occupant slot."
        },
        "a": 1.50,
        "b": 0.30,
        "point_biserial": 0.44
    },
    {
        "skill_code": "LOG_SEATING",
        "stem": "In a 100m race with runners P, Q, R, S, T:\n- P finished ahead of Q but behind R.\n- S finished ahead of T but behind Q.\n\nWho finished in third place?",
        "options": [
            {"id": "A", "text": "Q", "is_distractor": False},
            {"id": "B", "text": "P", "is_distractor": True},
            {"id": "C", "text": "R", "is_distractor": True},
            {"id": "D", "text": "S", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Order from fastest to slowest: R > P > Q from statement 1. Q > S > T from statement 2. Combining yields: R (1st) > P (2nd) > Q (3rd) > S (4th) > T (5th). Third place is Q.",
        "distractor_explanations": {
            "B": "P finished 2nd.",
            "C": "R finished 1st (winner).",
            "D": "S finished 4th."
        },
        "a": 1.30,
        "b": -1.20,
        "point_biserial": 0.40
    },
    {
        "skill_code": "LOG_SEATING",
        "stem": "Five boxes—Red, Green, Blue, Yellow, and White—are stacked vertically:\n1. The Red box is above the Green box.\n2. The Blue box is below the Yellow box.\n3. The Green box is above the Yellow box.\n4. The White box is at the very bottom.\n\nWhich box is in the middle of the stack?",
        "options": [
            {"id": "A", "text": "Yellow", "is_distractor": False},
            {"id": "B", "text": "Green", "is_distractor": True},
            {"id": "C", "text": "Blue", "is_distractor": True},
            {"id": "D", "text": "Red", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Order from top to bottom: Red > Green > Yellow > Blue > White. The middle box (3rd from top and bottom) is Yellow.",
        "distractor_explanations": {
            "B": "Green is 2nd from the top.",
            "C": "Blue is 4th from the top (above White).",
            "D": "Red is at the very top (1st)."
        },
        "a": 1.35,
        "b": -0.90,
        "point_biserial": 0.41
    },

    # --- LOG_DATA_SUFF (7 items) ---
    {
        "skill_code": "LOG_DATA_SUFF",
        "stem": "Question: Is integer $x$ even?\n\nStatement (1): $x^2 + 3$ is an odd integer.\nStatement (2): $3x + 2$ is an even integer.\n\nWhich statement(s) are sufficient to answer the question?",
        "options": [
            {"id": "A", "text": "Statement (1) ALONE is sufficient, but Statement (2) alone is not sufficient.", "is_distractor": True},
            {"id": "B", "text": "Statement (2) ALONE is sufficient, but Statement (1) alone is not sufficient.", "is_distractor": True},
            {"id": "C", "text": "EACH statement ALONE is sufficient.", "is_distractor": False},
            {"id": "D", "text": "Statements (1) and (2) TOGETHER are not sufficient.", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "From (1): $x^2 + 3 = \\text{odd} \\implies x^2 = \\text{even} \\implies x = \\text{even}$. (Sufficient). From (2): $3x + 2 = \\text{even} \\implies 3x = \\text{even} \\implies x = \\text{even}$. (Sufficient). Each alone is sufficient.",
        "distractor_explanations": {
            "A": "Missed that Statement (2) is also sufficient.",
            "B": "Missed that Statement (1) is also sufficient.",
            "D": "Both statements independently provide definitive affirmative answers."
        },
        "a": 1.50,
        "b": -0.30,
        "point_biserial": 0.44
    },
    {
        "skill_code": "LOG_DATA_SUFF",
        "stem": "Question: What is the average latency of service S?\n\nStatement (1): The total latency for 50 requests was 5,000 milliseconds.\nStatement (2): The median latency for the 50 requests was 95 milliseconds.\n\nWhich statement(s) are sufficient?",
        "options": [
            {"id": "A", "text": "Statement (1) ALONE is sufficient, but Statement (2) alone is not sufficient.", "is_distractor": False},
            {"id": "B", "text": "Statement (2) ALONE is sufficient, but Statement (1) alone is not sufficient.", "is_distractor": True},
            {"id": "C", "text": "BOTH statements TOGETHER are necessary.", "is_distractor": True},
            {"id": "D", "text": "NEITHER statement is sufficient.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Average = Total Latency / Count = $5000 / 50 = 100$ ms. Statement (1) gives exact total and count, so it is sufficient. Statement (2) gives only the median, which cannot determine the mean.",
        "distractor_explanations": {
            "B": "Median does not determine arithmetic mean in skewed distributions.",
            "C": "Statement (1) alone is sufficient; Statement (2) is superfluous.",
            "D": "Statement (1) directly solves the problem."
        },
        "a": 1.40,
        "b": -0.80,
        "point_biserial": 0.42
    },
    {
        "skill_code": "LOG_DATA_SUFF",
        "stem": "Question: Is $xy > 0$?\n\nStatement (1): $x > 0$\nStatement (2): $y^2 > 0$\n\nWhich statement(s) are sufficient to answer the question?",
        "options": [
            {"id": "A", "text": "Statement (1) ALONE is sufficient.", "is_distractor": True},
            {"id": "B", "text": "Statement (2) ALONE is sufficient.", "is_distractor": True},
            {"id": "C", "text": "BOTH statements TOGETHER are sufficient.", "is_distractor": True},
            {"id": "D", "text": "Statements (1) and (2) TOGETHER are NOT sufficient.", "is_distractor": False}
        ],
        "answer_key": "D",
        "explanation": "Statement (1) tells us $x > 0$, but nothing about $y$. Statement (2) tells us $y \\neq 0$ (could be positive or negative). Together: if $y = 2$, $xy = 2x > 0$. If $y = -2$, $xy = -2x < 0$. We cannot definitively answer whether $xy > 0$. Not sufficient.",
        "distractor_explanations": {
            "A": "Sign of $y$ is unknown.",
            "B": "Sign of both $x$ and $y$ are unknown.",
            "C": "$y$ can still be negative ($(-3)^2 > 0$), making $xy < 0$."
        },
        "a": 1.55,
        "b": 0.40,
        "point_biserial": 0.46
    },
    {
        "skill_code": "LOG_DATA_SUFF",
        "stem": "Question: In a triangle with sides $a$, $b$, and $c$, is the triangle a right-angled triangle?\n\nStatement (1): $a^2 + b^2 = 25$\nStatement (2): $c = 5$\n\nWhich statement(s) are sufficient?",
        "options": [
            {"id": "A", "text": "Statement (1) ALONE is sufficient.", "is_distractor": True},
            {"id": "B", "text": "Statement (2) ALONE is sufficient.", "is_distractor": True},
            {"id": "C", "text": "BOTH statements TOGETHER are sufficient.", "is_distractor": False},
            {"id": "D", "text": "Statements (1) and (2) TOGETHER are NOT sufficient.", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "From (1) and (2) together: $a^2 + b^2 = 25$ and $c^2 = 5^2 = 25$. Thus $a^2 + b^2 = c^2$. By the converse of the Pythagorean Theorem, the triangle must be right-angled. Together they are sufficient.",
        "distractor_explanations": {
            "A": "Without knowing $c$, $a^2 + b^2 = 25$ does not prove $c = 5$.",
            "B": "Side length 5 alone reveals nothing about the angle.",
            "D": "Together they satisfy the converse of Pythagoras definitively."
        },
        "a": 1.45,
        "b": -0.10,
        "point_biserial": 0.43
    },
    {
        "skill_code": "LOG_DATA_SUFF",
        "stem": "Question: How many nodes are in the binary search tree?\n\nStatement (1): The tree has height 3.\nStatement (2): The tree is a Full and Complete binary tree.\n\nWhich statement(s) are sufficient?",
        "options": [
            {"id": "A", "text": "Statement (1) ALONE is sufficient.", "is_distractor": True},
            {"id": "B", "text": "Statement (2) ALONE is sufficient.", "is_distractor": True},
            {"id": "C", "text": "BOTH statements TOGETHER are sufficient.", "is_distractor": False},
            {"id": "D", "text": "Statements (1) and (2) TOGETHER are NOT sufficient.", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "Statement (1) alone: A tree of height $h=3$ can have between $h+1=4$ and $2^{h+1}-1=15$ nodes. (Not sufficient). Statement (2) alone: Gives structure, but no height or scale. (Not sufficient). Together: A full and complete (perfect) binary tree of height 3 has exactly $2^{3+1} - 1 = 15$ nodes (or $2^3 - 1 = 7$ under 1-based indexing). The count is unique.",
        "distractor_explanations": {
            "A": "Height alone allows a range from degenerate linked lists to complete trees.",
            "B": "Completeness without height gives no scale.",
            "D": "Together the node count is mathematically fixed."
        },
        "a": 1.60,
        "b": 0.80,
        "point_biserial": 0.47
    },
    {
        "skill_code": "LOG_DATA_SUFF",
        "stem": "Question: Did developer Alice commit more lines of code than developer Bob this sprint?\n\nStatement (1): Alice committed 40% of the total team lines of code.\nStatement (2): Bob committed 35% of the total team lines of code.\n\nWhich statement(s) are sufficient?",
        "options": [
            {"id": "A", "text": "Statement (1) ALONE is sufficient.", "is_distractor": True},
            {"id": "B", "text": "Statement (2) ALONE is sufficient.", "is_distractor": True},
            {"id": "C", "text": "BOTH statements TOGETHER are sufficient.", "is_distractor": False},
            {"id": "D", "text": "Statements (1) and (2) TOGETHER are NOT sufficient.", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "Since total lines of code $T > 0$, Alice committed $0.40 T$ and Bob committed $0.35 T$. Since $0.40 T > 0.35 T$, Alice committed more lines than Bob. Together they are sufficient.",
        "distractor_explanations": {
            "A": "Statement (1) does not tell us Bob's share (Bob could have committed 45%).",
            "B": "Statement (2) does not tell us Alice's share.",
            "D": "Together the comparison $0.40 T > 0.35 T$ is definitive."
        },
        "a": 1.35,
        "b": -0.60,
        "point_biserial": 0.42
    },
    {
        "skill_code": "LOG_DATA_SUFF",
        "stem": "Question: What is the value of positive integer $n$?\n\nStatement (1): $n$ is a prime number such that $20 < n < 30$.\nStatement (2): $n + 2$ is also a prime number.\n\nWhich statement(s) are sufficient?",
        "options": [
            {"id": "A", "text": "Statement (1) ALONE is sufficient.", "is_distractor": True},
            {"id": "B", "text": "Statement (2) ALONE is sufficient.", "is_distractor": True},
            {"id": "C", "text": "BOTH statements TOGETHER are sufficient.", "is_distractor": False},
            {"id": "D", "text": "Statements (1) and (2) TOGETHER are NOT sufficient.", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "From (1): Primes between 20 and 30 are 23 and 29. Two candidates, not sufficient. From (2): Infinitely many twin primes. Not sufficient. Together: Check candidates: If $n = 23$, $n + 2 = 25$ (not prime). If $n = 29$, $n + 2 = 31$ (prime). Only $n = 29$ satisfies both. Sufficient.",
        "distractor_explanations": {
            "A": "Leaves two candidates: 23 and 29.",
            "B": "Infinitely many primes satisfy $n+2$ prime.",
            "D": "Together uniquely isolates $n = 29$."
        },
        "a": 1.65,
        "b": 1.25,
        "point_biserial": 0.49
    }
]
