"""
Database Management Systems Question Bank.
Topic 1: Relational Theory & Design (15 questions across DBMS_REL_MODEL, DBMS_NORMALIZATION)
Topic 2: Transactions & Concurrency (15 questions across DBMS_ACID, DBMS_CONCURRENCY)
"""

DBMS_ITEMS = [
    # =========================================================================
    # TOPIC 1: Relational Theory & Design (15 items)
    # =========================================================================
    # --- DBMS_REL_MODEL (7 items) ---
    {
        "skill_code": "DBMS_REL_MODEL",
        "stem": "What is the difference between a **Candidate Key** and the **Primary Key** of a relational table?",
        "options": [
            {"id": "A", "text": "A candidate key is any minimal superkey capable of uniquely identifying tuples; the primary key is the specific candidate key selected by the database designer.", "is_distractor": False},
            {"id": "B", "text": "Candidate keys can contain duplicate values; primary keys cannot.", "is_distractor": True},
            {"id": "C", "text": "A table can have multiple primary keys but only one candidate key.", "is_distractor": True},
            {"id": "D", "text": "Candidate keys are defined exclusively in NoSQL databases.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A relation can have multiple candidate keys (all minimal superkeys with unique, non-null values). The database architect chooses one candidate key as the official Primary Key, leaving the others as Alternate Keys.",
        "distractor_explanations": {
            "B": "Candidate keys must strictly satisfy the uniqueness constraint.",
            "C": "A table has exactly one primary key, but can have multiple candidate keys.",
            "D": "Candidate keys are foundational to relational algebra and Codd's relational model."
        },
        "a": 1.30,
        "b": -0.80,
        "point_biserial": 0.41
    },
    {
        "skill_code": "DBMS_REL_MODEL",
        "stem": "What does **Referential Integrity** enforce in a relational schema?",
        "options": [
            {"id": "A", "text": "A foreign key value in a referencing table must match an existing primary key value in the referenced table, or else be NULL.", "is_distractor": False},
            {"id": "B", "text": "Every column in a table must have a distinct data type.", "is_distractor": True},
            {"id": "C", "text": "Primary keys must be auto-incrementing integers.", "is_distractor": True},
            {"id": "D", "text": "All tables in a database must contain equal row counts.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Referential integrity guarantees that relationships between tables remain consistent, preventing orphan records where a child row points to a non-existent parent entity.",
        "distractor_explanations": {
            "B": "Columns can share data types freely.",
            "C": "Primary keys can be UUIDs, composite keys, or text hashes.",
            "D": "Row counts across tables are completely independent."
        },
        "a": 1.35,
        "b": -0.50,
        "point_biserial": 0.42
    },
    {
        "skill_code": "DBMS_REL_MODEL",
        "stem": "In relational algebra, which fundamental operator filters rows based on a specified boolean predicate condition?",
        "options": [
            {"id": "A", "text": "Selection (sigma: $\\sigma$)", "is_distractor": False},
            {"id": "B", "text": "Projection (pi: $\\pi$)", "is_distractor": True},
            {"id": "C", "text": "Cartesian Product ($\\times$)", "is_distractor": True},
            {"id": "D", "text": "Join ($\\bowtie$)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Selection $\\sigma_{condition}(R)$ extracts horizontal slices (rows) satisfying the condition. Projection $\\pi_{attributes}(R)$ extracts vertical slices (columns).",
        "distractor_explanations": {
            "B": "Projection filters columns (attributes), not rows.",
            "C": "Cartesian product combines all pairs of rows between two relations.",
            "D": "Join pairs rows based on matching condition."
        },
        "a": 1.40,
        "b": -0.20,
        "point_biserial": 0.43
    },
    {
        "skill_code": "DBMS_REL_MODEL",
        "stem": "What is the result of the relational algebra expression $\\pi_{name}(Students) - \\pi_{name}(Graduates)$?",
        "options": [
            {"id": "A", "text": "Names of students who are not graduates (Set Difference)", "is_distractor": False},
            {"id": "B", "text": "Names common to both students and graduates", "is_distractor": True},
            {"id": "C", "text": "All names combined with duplicates", "is_distractor": True},
            {"id": "D", "text": "The Cartesian product of names", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The minus operator $-$ denotes set difference, returning all tuples in the first relation that do not appear in the second relation.",
        "distractor_explanations": {
            "B": "Intersection ($\\cap$) returns common names.",
            "C": "Union ($U$) returns combined names.",
            "D": "Cartesian product ($\\times$) pairs elements."
        },
        "a": 1.45,
        "b": 0.10,
        "point_biserial": 0.45
    },
    {
        "skill_code": "DBMS_REL_MODEL",
        "stem": "What is the consequence of setting a foreign key constraint to `ON DELETE CASCADE`?",
        "options": [
            {"id": "A", "text": "When a parent row is deleted, all matching referencing child rows in the child table are automatically deleted.", "is_distractor": False},
            {"id": "B", "text": "Deletion of the parent row is blocked if child rows exist.", "is_distractor": True},
            {"id": "C", "text": "Foreign key values in child rows are overwritten with NULL.", "is_distractor": True},
            {"id": "D", "text": "The entire child table is dropped.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "`ON DELETE CASCADE` propagates row deletions from referenced parent rows to referencing child rows, preventing orphan records automatically.",
        "distractor_explanations": {
            "B": "Describes `ON DELETE RESTRICT` or `ON DELETE NO ACTION`.",
            "C": "Describes `ON DELETE SET NULL`.",
            "D": "The child table schema remains intact; only matching rows are deleted."
        },
        "a": 1.50,
        "b": 0.40,
        "point_biserial": 0.46
    },
    {
        "skill_code": "DBMS_REL_MODEL",
        "stem": "What is a **Superkey** in relational database theory?",
        "options": [
            {"id": "A", "text": "Any set of one or more attributes that collectively allows a relation's tuples to be uniquely identified.", "is_distractor": False},
            {"id": "B", "text": "A key containing only foreign keys.", "is_distractor": True},
            {"id": "C", "text": "A key that cannot contain null values, but does not need to be unique.", "is_distractor": True},
            {"id": "D", "text": "The largest numeric column in a table.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A superkey is any attribute set $K$ such that no two distinct tuples have identical values for $K$. A Candidate Key is a minimal superkey.",
        "distractor_explanations": {
            "B": "Superkeys are about uniqueness, not foreign relations.",
            "C": "Superkeys must be strictly unique.",
            "D": "Data type is completely arbitrary."
        },
        "a": 1.55,
        "b": 0.75,
        "point_biserial": 0.47
    },
    {
        "skill_code": "DBMS_REL_MODEL",
        "stem": "In SQL, how does a `UNIQUE` constraint differ from a `PRIMARY KEY` constraint?",
        "options": [
            {"id": "A", "text": "A table can have multiple UNIQUE constraints and they permit NULL values; a table can have only one PRIMARY KEY which strictly forbids NULLs.", "is_distractor": False},
            {"id": "B", "text": "UNIQUE constraints create indexes; primary keys do not.", "is_distractor": True},
            {"id": "C", "text": "PRIMARY KEY allows duplicate values if indexed.", "is_distractor": True},
            {"id": "D", "text": "There is no difference in standard SQL.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Standard SQL permits multiple `UNIQUE` constraints per table and allows `NULL`s (since `NULL != NULL`). A table can have at most one `PRIMARY KEY`, which implicitly enforces `NOT NULL`.",
        "distractor_explanations": {
            "B": "Primary keys implicitly create a unique B-Tree index (often clustered).",
            "C": "Primary keys strictly forbid duplicates.",
            "D": "Differences are fundamental across all relational database engines."
        },
        "a": 1.60,
        "b": 1.05,
        "point_biserial": 0.48
    },

    # --- DBMS_NORMALIZATION (8 items) ---
    {
        "skill_code": "DBMS_NORMALIZATION",
        "stem": "A relational table is in Boyce-Codd Normal Form (BCNF) if and only if for every non-trivial functional dependency $X \\to Y$:",
        "options": [
            {"id": "A", "text": "X is a superkey of the relation.", "is_distractor": False},
            {"id": "B", "text": "Y is a prime attribute.", "is_distractor": True},
            {"id": "C", "text": "X is a single attribute (not composite).", "is_distractor": True},
            {"id": "D", "text": "All attributes are non-null.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "BCNF is a stricter form of 3NF. In 3NF, $X \\to Y$ is permitted if $X$ is a superkey OR $Y$ is prime. BCNF removes the second clause: $X$ must strictly be a superkey.",
        "distractor_explanations": {
            "B": "This is the relaxing condition permitted in 3NF, but eliminated in BCNF.",
            "C": "Superkeys can be composite.",
            "D": "Nullability is unrelated to BCNF functional dependencies."
        },
        "a": 1.60,
        "b": 0.65,
        "point_biserial": 0.48
    },
    {
        "skill_code": "DBMS_NORMALIZATION",
        "stem": "What is the primary requirement for a relation to be in **First Normal Form (1NF)**?",
        "options": [
            {"id": "A", "text": "Every column contains only atomic (indivisible) values, and there are no repeating groups.", "is_distractor": False},
            {"id": "B", "text": "There are no transitive dependencies.", "is_distractor": True},
            {"id": "C", "text": "All non-key attributes are fully functionally dependent on the entire primary key.", "is_distractor": True},
            {"id": "D", "text": "The table must have at least 3 foreign keys.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "1NF requires that each attribute domain contains only atomic scalar values (no nested lists, arrays, or repeating sets of values in a single cell).",
        "distractor_explanations": {
            "B": "Eliminating transitive dependencies is the requirement for 3NF.",
            "C": "Eliminating partial dependencies is the requirement for 2NF.",
            "D": "Foreign keys are not required for 1NF."
        },
        "a": 1.30,
        "b": -1.00,
        "point_biserial": 0.40
    },
    {
        "skill_code": "DBMS_NORMALIZATION",
        "stem": "A table is in 1NF. To achieve **Second Normal Form (2NF)**, what kind of dependency must be eliminated?",
        "options": [
            {"id": "A", "text": "Partial Functional Dependencies (where a non-prime attribute depends on a proper subset of a composite candidate key)", "is_distractor": False},
            {"id": "B", "text": "Transitive Dependencies", "is_distractor": True},
            {"id": "C", "text": "Multivalued Dependencies", "is_distractor": True},
            {"id": "D", "text": "Join Dependencies", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "2NF eliminates partial dependencies: every non-prime attribute must depend on the whole candidate key, not just a part of it.",
        "distractor_explanations": {
            "B": "Transitive dependencies are eliminated in 3NF.",
            "C": "Multivalued dependencies are eliminated in 4NF.",
            "D": "Join dependencies are eliminated in 5NF."
        },
        "a": 1.45,
        "b": -0.35,
        "point_biserial": 0.44
    },
    {
        "skill_code": "DBMS_NORMALIZATION",
        "stem": "If functional dependencies are $A \\to B$ and $B \\to C$, what type of dependency exists between $A$ and $C$?",
        "options": [
            {"id": "A", "text": "Transitive Dependency", "is_distractor": False},
            {"id": "B", "text": "Partial Dependency", "is_distractor": True},
            {"id": "C", "text": "Trivial Dependency", "is_distractor": True},
            {"id": "D", "text": "Multivalued Dependency", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "By the transitivity axiom of Armstrong's axioms: If $A \\to B$ and $B \\to C$, then $A \\to C$. When $B$ is not a candidate key, $A \\to C$ via $B$ is a transitive dependency that violates 3NF.",
        "distractor_explanations": {
            "B": "Partial dependencies involve subsets of composite candidate keys.",
            "C": "Trivial dependencies have the form $X \\to Y$ where $Y \\subseteq X$.",
            "D": "Multivalued dependencies involve independent multi-valued sets ($X \\twoheadrightarrow Y$)."
        },
        "a": 1.40,
        "b": -0.70,
        "point_biserial": 0.42
    },
    {
        "skill_code": "DBMS_NORMALIZATION",
        "stem": "Given relation $R(A, B, C, D)$ with functional dependencies $F = \\{A \\to B, B \\to C, C \\to D\\}$, what is the Candidate Key of $R$?",
        "options": [
            {"id": "A", "text": "A", "is_distractor": False},
            {"id": "B", "text": "B", "is_distractor": True},
            {"id": "C", "text": "AB", "is_distractor": True},
            {"id": "D", "text": "ABCD", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Compute attribute closure: $A^+ = \\{A, B, C, D\\}$ because $A \\to B \\implies B \\to C \\implies C \\to D$. Since $A^+$ contains all attributes and no proper subset of $A$ can, $A$ is the sole candidate key.",
        "distractor_explanations": {
            "B": "$B^+ = \\{B, C, D\\}$, missing $A$.",
            "C": "$AB$ is a superkey, but not minimal (not a candidate key).",
            "D": "$ABCD$ is a non-minimal superkey."
        },
        "a": 1.55,
        "b": 0.45,
        "point_biserial": 0.46
    },
    {
        "skill_code": "DBMS_NORMALIZATION",
        "stem": "Which of Armstrong's Axioms states that if $X \\to Y$, then $XZ \\to YZ$ for any set of attributes $Z$?",
        "options": [
            {"id": "A", "text": "Augmentation Axiom", "is_distractor": False},
            {"id": "B", "text": "Reflexivity Axiom", "is_distractor": True},
            {"id": "C", "text": "Transitivity Axiom", "is_distractor": True},
            {"id": "D", "text": "Decomposition Axiom", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The Augmentation rule states: If $X \\to Y$, then $XZ \\to YZ$. The three core Armstrong Axioms are Reflexivity, Augmentation, and Transitivity.",
        "distractor_explanations": {
            "B": "Reflexivity: If $Y \\subseteq X$, then $X \\to Y$.",
            "C": "Transitivity: If $X \\to Y$ and $Y \\to Z$, then $X \\to Z$.",
            "D": "Decomposition: If $X \\to YZ$, then $X \\to Y$ and $X \\to Z$."
        },
        "a": 1.60,
        "b": 0.90,
        "point_biserial": 0.48
    },
    {
        "skill_code": "DBMS_NORMALIZATION",
        "stem": "What is the primary operational tradeoff when decomposing relations into high normal forms (e.g. 3NF / BCNF)?",
        "options": [
            {"id": "A", "text": "Reduced data redundancy and update anomalies at the cost of requiring expensive JOIN operations during query execution.", "is_distractor": False},
            {"id": "B", "text": "Faster queries at the expense of disk storage.", "is_distractor": True},
            {"id": "C", "text": "Elimination of primary keys.", "is_distractor": True},
            {"id": "D", "text": "Disabling foreign key constraints.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Normalization eliminates redundancy, insert, update, and delete anomalies. However, querying normalized data requires joining multiple tables, which incurs CPU/IO overhead (often prompting deliberate denormalization in OLAP).",
        "distractor_explanations": {
            "B": "Denormalization speeds up queries by trading off disk storage.",
            "C": "Normalization requires primary keys on all decomposed tables.",
            "D": "Normalization introduces more foreign key relationships."
        },
        "a": 1.50,
        "b": 0.15,
        "point_biserial": 0.44
    },
    {
        "skill_code": "DBMS_NORMALIZATION",
        "stem": "Can a relation decomposed into BCNF always preserve all functional dependencies?",
        "options": [
            {"id": "A", "text": "No, BCNF decomposition is always lossless-join, but may not be dependency-preserving.", "is_distractor": False},
            {"id": "B", "text": "Yes, BCNF guarantees both lossless-join and dependency preservation in all cases.", "is_distractor": True},
            {"id": "C", "text": "No, BCNF never preserves dependencies.", "is_distractor": True},
            {"id": "D", "text": "BCNF decomposition does not support lossless joins.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "3NF guarantees both lossless-join and dependency preservation. BCNF guarantees lossless-join, but some relations cannot be decomposed into BCNF without losing functional dependencies (e.g. $AB \\to C, C \\to B$ with candidate key $AB$).",
        "distractor_explanations": {
            "B": "False: 3NF guarantees dependency preservation, but BCNF does not always.",
            "C": "BCNF preserves dependencies in many relations, but not universally.",
            "D": "BCNF decomposition algorithms strictly ensure the lossless-join property."
        },
        "a": 1.70,
        "b": 1.45,
        "point_biserial": 0.52
    },

    # =========================================================================
    # TOPIC 2: Transactions & Concurrency (15 items)
    # =========================================================================
    # --- DBMS_ACID (8 items) ---
    {
        "skill_code": "DBMS_ACID",
        "stem": "What does the **Atomicity** property of ACID guarantee?",
        "options": [
            {"id": "A", "text": "All operations in a transaction either complete successfully, or in the event of failure, all changes are rolled back (\"all-or-nothing\").", "is_distractor": False},
            {"id": "B", "text": "Concurrent transactions execute without interfering with one another.", "is_distractor": True},
            {"id": "C", "text": "Database constraints are preserved before and after execution.", "is_distractor": True},
            {"id": "D", "text": "Committed data survives system crashes and power failures.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Atomicity ensures transaction indivisibility: a multi-step operation is treated as a single atomic unit of work. If any step fails, the Write-Ahead Log (WAL) undoes partial mutations.",
        "distractor_explanations": {
            "B": "Describes Isolation (I).",
            "C": "Describes Consistency (C).",
            "D": "Describes Durability (D)."
        },
        "a": 1.25,
        "b": -1.15,
        "point_biserial": 0.40
    },
    {
        "skill_code": "DBMS_ACID",
        "stem": "Which database component is responsible for guaranteeing **Durability** in the face of sudden power loss?",
        "options": [
            {"id": "A", "text": "Write-Ahead Logging (WAL) / Redo Log flushed to non-volatile disk", "is_distractor": False},
            {"id": "B", "text": "Query Optimizer", "is_distractor": True},
            {"id": "C", "text": "In-memory cache pool", "is_distractor": True},
            {"id": "D", "text": "Lock Manager", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Durability requires that once a transaction commits, its modifications are permanently recorded on non-volatile media. Write-Ahead Logging (WAL) ensures log records are `fsync`'d before acknowledging commit.",
        "distractor_explanations": {
            "B": "The Query Optimizer produces efficient execution plans.",
            "C": "In-memory cache is volatile and cleared upon power failure.",
            "D": "The Lock Manager coordinates concurrency and isolation."
        },
        "a": 1.40,
        "b": -0.60,
        "point_biserial": 0.43
    },
    {
        "skill_code": "DBMS_ACID",
        "stem": "In the ARIES recovery algorithm, which phase scans the log backward from the checkpoint to undo the effects of uncommitted transactions?",
        "options": [
            {"id": "A", "text": "Undo Phase", "is_distractor": False},
            {"id": "B", "text": "Analysis Phase", "is_distractor": True},
            {"id": "C", "text": "Redo Phase", "is_distractor": True},
            {"id": "D", "text": "Checkpointing Phase", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "ARIES operates in 3 phases: 1) Analysis (determines dirty pages and active transactions), 2) Redo (repeats history forward), and 3) Undo (scans backward to reverse actions of uncommitted 'loser' transactions).",
        "distractor_explanations": {
            "B": "Analysis scans forward from checkpoint to end of log.",
            "C": "Redo scans forward to repeat history.",
            "D": "Checkpointing is an online maintenance activity, not a recovery phase."
        },
        "a": 1.65,
        "b": 1.20,
        "point_biserial": 0.49
    },
    {
        "skill_code": "DBMS_ACID",
        "stem": "What is the **Write-Ahead Logging (WAL) protocol** rule?",
        "options": [
            {"id": "A", "text": "A dirty database buffer page cannot be written to disk until the corresponding log record describing the update is written to non-volatile storage.", "is_distractor": False},
            {"id": "B", "text": "Log records are written only after all database tables are fully updated on disk.", "is_distractor": True},
            {"id": "C", "text": "Transactions must acquire all locks before writing any queries.", "is_distractor": True},
            {"id": "D", "text": "Read queries must be logged before write queries.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "WAL enforces that log records precede dirty page writes. This guarantees that if a crash occurs while flushing a page, the engine can undo the partial write using the log.",
        "distractor_explanations": {
            "B": "Reverses the protocol, which would make crash recovery impossible.",
            "C": "Describes Conservative 2PL, not WAL.",
            "D": "Read queries do not alter state and are typically not written to the WAL."
        },
        "a": 1.55,
        "b": 0.70,
        "point_biserial": 0.47
    },
    {
        "skill_code": "DBMS_ACID",
        "stem": "Which transaction isolation level allows **Dirty Reads** (reading uncommitted changes made by concurrent transactions)?",
        "options": [
            {"id": "A", "text": "Read Uncommitted", "is_distractor": False},
            {"id": "B", "text": "Read Committed", "is_distractor": True},
            {"id": "C", "text": "Repeatable Read", "is_distractor": True},
            {"id": "D", "text": "Serializable", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Read Uncommitted is the lowest ANSI SQL isolation level. Transactions can read modified rows before the modifying transaction commits or aborts.",
        "distractor_explanations": {
            "B": "Read Committed prevents dirty reads by reading only committed data.",
            "C": "Repeatable Read prevents both dirty reads and non-repeatable reads.",
            "D": "Serializable prevents dirty reads, non-repeatable reads, and phantom reads."
        },
        "a": 1.35,
        "b": -0.85,
        "point_biserial": 0.42
    },
    {
        "skill_code": "DBMS_ACID",
        "stem": "What is a **Phantom Read** anomaly in transaction processing?",
        "options": [
            {"id": "A", "text": "A transaction re-executes a range query with identical WHERE criteria and finds that new matching rows have been inserted by a committed concurrent transaction.", "is_distractor": False},
            {"id": "B", "text": "A transaction reads data that was rolled back.", "is_distractor": True},
            {"id": "C", "text": "A transaction reads a row, and upon re-reading the same row, finds that its column values were modified.", "is_distractor": True},
            {"id": "D", "text": "A deadlock occurs between two transactions.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Phantom reads involve range queries where the set of rows satisfying a condition changes due to concurrent `INSERT` or `DELETE` operations.",
        "distractor_explanations": {
            "B": "Defines a Dirty Read.",
            "C": "Defines a Non-Repeatable (Fuzzy) Read.",
            "D": "Deadlock is a concurrency conflict, not a read anomaly."
        },
        "a": 1.50,
        "b": 0.25,
        "point_biserial": 0.45
    },
    {
        "skill_code": "DBMS_ACID",
        "stem": "How does Multi-Version Concurrency Control (MVCC) eliminate read-write contention in PostgreSQL and InnoDB?",
        "options": [
            {"id": "A", "text": "Readers do not block writers, and writers do not block readers; readers see a consistent snapshot of data as of their transaction start timestamp.", "is_distractor": False},
            {"id": "B", "text": "By locking the entire table whenever any query is executed.", "is_distractor": True},
            {"id": "C", "text": "By rejecting all concurrent write transactions.", "is_distractor": True},
            {"id": "D", "text": "By executing all transactions sequentially on a single thread.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "MVCC creates a new version of a row on update instead of overwriting in place. Old versions remain visible to concurrent read transactions, decoupling read locks from write locks.",
        "distractor_explanations": {
            "B": "Describes table-level locking, the exact opposite of MVCC.",
            "C": "Writers are not rejected; they coordinate row locks with other writers.",
            "D": "Describes single-threaded execution (like Redis)."
        },
        "a": 1.60,
        "b": 0.85,
        "point_biserial": 0.48
    },
    {
        "skill_code": "DBMS_ACID",
        "stem": "In SQL, what is the effect of issuing a `SAVEPOINT` command within an active transaction?",
        "options": [
            {"id": "A", "text": "It creates a nested checkpoint allowing partial rollback of operations without aborting the entire transaction.", "is_distractor": False},
            {"id": "B", "text": "It commits the transaction permanently to disk.", "is_distractor": True},
            {"id": "C", "text": "It releases all locks held by the transaction.", "is_distractor": True},
            {"id": "D", "text": "It exports the database to an external backup file.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "`SAVEPOINT name` allows `ROLLBACK TO SAVEPOINT name`, enabling fine-grained error recovery without discarding work done prior to the savepoint.",
        "distractor_explanations": {
            "B": "`COMMIT` commits permanently, not `SAVEPOINT`.",
            "C": "Locks are retained until transaction completion (`COMMIT` or `ROLLBACK`).",
            "D": "Backup commands perform database exports."
        },
        "a": 1.45,
        "b": -0.15,
        "point_biserial": 0.43
    },

    # --- DBMS_CONCURRENCY (7 items) ---
    {
        "skill_code": "DBMS_CONCURRENCY",
        "stem": "What is the core rule of the **Two-Phase Locking (2PL)** protocol?",
        "options": [
            {"id": "A", "text": "A transaction must acquire all locks during a Growing Phase and cannot acquire any new lock once it releases its first lock in the Shrinking Phase.", "is_distractor": False},
            {"id": "B", "text": "A transaction locks two tables at a time.", "is_distractor": True},
            {"id": "C", "text": "A transaction acquires read locks in phase 1 and write locks in phase 2.", "is_distractor": True},
            {"id": "D", "text": "A transaction executes twice to verify consistency.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "2PL guarantees conflict serializability by separating lock management into: 1) Growing Phase (locks acquired, none released) and 2) Shrinking Phase (locks released, none acquired).",
        "distractor_explanations": {
            "B": "The name refers to two phases of locking, not two tables.",
            "C": "Both shared and exclusive locks can be acquired in the growing phase.",
            "D": "2PL does not execute transactions twice."
        },
        "a": 1.50,
        "b": 0.30,
        "point_biserial": 0.45
    },
    {
        "skill_code": "DBMS_CONCURRENCY",
        "stem": "What does **Strict Two-Phase Locking (Strict 2PL)** require compared to standard 2PL to prevent cascading rollbacks?",
        "options": [
            {"id": "A", "text": "All exclusive (write) locks held by a transaction must be retained until the transaction commits or aborts.", "is_distractor": False},
            {"id": "B", "text": "Shared locks can never be acquired.", "is_distractor": True},
            {"id": "C", "text": "All tables in the database are locked concurrently.", "is_distractor": True},
            {"id": "D", "text": "Transactions must execute in FIFO order.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In standard 2PL, releasing write locks before commit can cause concurrent transactions to read dirty data. Strict 2PL holds all write locks until transaction termination, guaranteeing cascade-free recovery.",
        "distractor_explanations": {
            "B": "Shared locks are standard in Strict 2PL for reads.",
            "C": "Row and page level locks are used, not whole database locks.",
            "D": "Strict 2PL does not enforce FIFO execution."
        },
        "a": 1.60,
        "b": 0.75,
        "point_biserial": 0.47
    },
    {
        "skill_code": "DBMS_CONCURRENCY",
        "stem": "In concurrency control, what graph structure is analyzed to detect deadlocks dynamically?",
        "options": [
            {"id": "A", "text": "Wait-For Graph (WFG), where cycles indicate deadlocks", "is_distractor": False},
            {"id": "B", "text": "B-Tree Index Graph", "is_distractor": True},
            {"id": "C", "text": "Minimum Spanning Tree", "is_distractor": True},
            {"id": "D", "text": "Call Stack Trace", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A Wait-For Graph has transactions as nodes and directed edges $T_1 \\to T_2$ meaning $T_1$ is waiting for a lock held by $T_2$. A cycle in this directed graph represents a deadlock.",
        "distractor_explanations": {
            "B": "B-Tree is a search index structure.",
            "C": "MST finds minimum weight spanning subgraphs.",
            "D": "Call stacks track function execution, not transaction lock dependencies."
        },
        "a": 1.45,
        "b": -0.20,
        "point_biserial": 0.44
    },
    {
        "skill_code": "DBMS_CONCURRENCY",
        "stem": "What is the difference between the **Wait-Die** and **Wound-Wait** deadlock prevention schemes based on transaction timestamps (where older = smaller timestamp)?",
        "options": [
            {"id": "A", "text": "In Wait-Die, older waits for younger, and younger dies; in Wound-Wait, older wounds (preempts) younger, and younger waits.", "is_distractor": False},
            {"id": "B", "text": "Wait-Die uses locks, while Wound-Wait uses optimistic concurrency.", "is_distractor": True},
            {"id": "C", "text": "Wound-Wait is only used in distributed databases.", "is_distractor": True},
            {"id": "D", "text": "Wait-Die permits cyclic graphs to exist.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Wait-Die is non-preemptive: older transaction waits for younger, but younger dies if it requests a lock held by older. Wound-Wait is preemptive: older transaction preempts ('wounds') younger transaction, forcing it to abort.",
        "distractor_explanations": {
            "B": "Both are timestamp-based locking deadlock prevention schemes.",
            "C": "Both are applicable to single-node and distributed DBMS.",
            "D": "Both strictly prevent deadlock cycles from forming."
        },
        "a": 1.65,
        "b": 1.15,
        "point_biserial": 0.49
    },
    {
        "skill_code": "DBMS_CONCURRENCY",
        "stem": "A schedule $S$ of transactions is **Conflict Serializable** if:",
        "options": [
            {"id": "A", "text": "It can be transformed into a serial schedule by swapping non-conflicting adjacent operations.", "is_distractor": False},
            {"id": "B", "text": "It contains no write operations.", "is_distractor": True},
            {"id": "C", "text": "All transactions commit simultaneously.", "is_distractor": True},
            {"id": "D", "text": "It is executed on a single CPU core.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Two operations conflict if they belong to different transactions, access the same item, and at least one is a write. A schedule is conflict serializable if its precedence (serialization) graph is acyclic.",
        "distractor_explanations": {
            "B": "Read-only schedules are trivially serializable, but conflict serializability fully supports writes.",
            "C": "Simultaneous commit is not required.",
            "D": "Hardware core count is independent of the mathematical property."
        },
        "a": 1.55,
        "b": 0.50,
        "point_biserial": 0.46
    },
    {
        "skill_code": "DBMS_CONCURRENCY",
        "stem": "In Multiple Granularity Locking, why are **Intent Locks** (e.g. Intent Shared IS, Intent Exclusive IX) placed on higher-level nodes (tables/databases)?",
        "options": [
            {"id": "A", "text": "To signal that fine-grained locks (e.g. row locks) are held lower in the hierarchy, preventing another transaction from locking the entire table concurrently.", "is_distractor": False},
            {"id": "B", "text": "To lock all rows in the table simultaneously.", "is_distractor": True},
            {"id": "C", "text": "To bypass the lock manager.", "is_distractor": True},
            {"id": "D", "text": "To enforce foreign key cascade operations.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Without Intent Locks, a transaction wanting an exclusive lock on a table would have to scan every row to check if any row is locked. An Intent Lock on the table warns of existing row locks in $O(1)$ time.",
        "distractor_explanations": {
            "B": "Table-level exclusive lock (X) locks all rows, not intent locks.",
            "C": "Intent locks are managed explicitly by the lock manager.",
            "D": "Cascades are integrity constraints, not hierarchy lock signals."
        },
        "a": 1.60,
        "b": 0.95,
        "point_biserial": 0.48
    },
    {
        "skill_code": "DBMS_CONCURRENCY",
        "stem": "In Optimistic Concurrency Control (OCC), what are the three execution phases?",
        "options": [
            {"id": "A", "text": "Read Phase, Validation Phase, Write Phase", "is_distractor": False},
            {"id": "B", "text": "Locking Phase, Growing Phase, Shrinking Phase", "is_distractor": True},
            {"id": "C", "text": "Prepare Phase, Commit Phase, Rollback Phase", "is_distractor": True},
            {"id": "D", "text": "Analysis Phase, Redo Phase, Undo Phase", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "OCC assumes conflicts are rare. It reads and writes to private workspace (Read Phase), checks for serializability conflicts (Validation Phase), and copies updates to database if valid (Write Phase).",
        "distractor_explanations": {
            "B": "Describes 2-Phase Locking (2PL).",
            "C": "Describes Two-Phase Commit (2PC).",
            "D": "Describes ARIES recovery algorithm."
        },
        "a": 1.50,
        "b": 0.35,
        "point_biserial": 0.45
    }
]
