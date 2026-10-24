"""
Repeatable, Idempotent Seed Process for MasteryLoop Placement Curriculum.
Covers 11 domains, topics, subtopics, skills, and prerequisite edges.
Validates DAG acyclicity with SkillDependencyGraph prior to committing.
"""

import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.models.curriculum import Domain, Topic, Subtopic, Skill, SkillEdge
from app.services.skill_graph import SkillDependencyGraph

logger = logging.getLogger("masteryloop.seed")


CURRICULUM_DATA = [
    # 1. Verbal Ability
    {
        "code": "VERBAL",
        "name": "Verbal Ability",
        "description": "Vocabulary, reading comprehension, contextual reasoning, and sentence correction for placement exams.",
        "icon": "BookOpen",
        "topics": [
            {
                "name": "Grammar & Sentence Correction",
                "subtopics": [
                    {
                        "name": "Core Syntax & Tenses",
                        "skills": [
                            {"code": "VRB_SUBJECT_VERB", "name": "Subject-Verb Agreement", "difficulty": 0.4, "blooms": "Understand"},
                            {"code": "VRB_TENSE_CONSIST", "name": "Tense Consistency & Conditionals", "difficulty": 0.5, "blooms": "Apply"},
                            {"code": "VRB_MODIFIERS", "name": "Parallelism & Dangling Modifiers", "difficulty": 0.6, "blooms": "Analyze"},
                        ]
                    }
                ]
            },
            {
                "name": "Reading Comprehension",
                "subtopics": [
                    {
                        "name": "Passage Analysis",
                        "skills": [
                            {"code": "VRB_MAIN_IDEA", "name": "Identifying Main Idea & Tone", "difficulty": 0.5, "blooms": "Understand"},
                            {"code": "VRB_INFERENCE", "name": "Drawing Inferences & Assumptions", "difficulty": 0.7, "blooms": "Analyze"},
                        ]
                    }
                ]
            }
        ]
    },
    # 2. Quantitative Aptitude
    {
        "code": "QUANT",
        "name": "Quantitative Aptitude",
        "description": "Arithmetic, algebra, geometry, probability, and numerical problem solving.",
        "icon": "Calculator",
        "topics": [
            {
                "name": "Arithmetic & Percentages",
                "subtopics": [
                    {
                        "name": "Ratios & Variations",
                        "skills": [
                            {"code": "QNT_NUMBERS", "name": "Number Properties & Divisibility", "difficulty": 0.35, "blooms": "Understand"},
                            {"code": "QNT_PERCENTAGES", "name": "Percentages & Profit-Loss", "difficulty": 0.45, "blooms": "Apply"},
                            {"code": "QNT_RATIO_PROP", "name": "Ratio, Proportion & Variation", "difficulty": 0.50, "blooms": "Apply"},
                            {"code": "QNT_TIME_WORK", "name": "Time, Speed, Distance & Work", "difficulty": 0.60, "blooms": "Apply"},
                        ]
                    }
                ]
            },
            {
                "name": "Combinatorics & Probability",
                "subtopics": [
                    {
                        "name": "Counting Principles",
                        "skills": [
                            {"code": "QNT_PERMUTATIONS", "name": "Permutations & Combinations", "difficulty": 0.65, "blooms": "Apply"},
                            {"code": "QNT_PROBABILITY", "name": "Conditional Probability & Bayes Rule", "difficulty": 0.75, "blooms": "Analyze"},
                        ]
                    }
                ]
            }
        ]
    },
    # 3. Logical Reasoning
    {
        "code": "REASONING",
        "name": "Logical Reasoning",
        "description": "Deductive logic, syllogisms, blood relations, seating arrangements, and analytical puzzles.",
        "icon": "Brain",
        "topics": [
            {
                "name": "Deductive Reasoning",
                "subtopics": [
                    {
                        "name": "Formal Logic",
                        "skills": [
                            {"code": "LOG_SYLLOGISMS", "name": "Syllogisms & Venn Representations", "difficulty": 0.50, "blooms": "Apply"},
                            {"code": "LOG_DEDUCTION", "name": "Critical Reasoning & Fallacy Detection", "difficulty": 0.65, "blooms": "Analyze"},
                        ]
                    }
                ]
            },
            {
                "name": "Arrangements & Puzzles",
                "subtopics": [
                    {
                        "name": "Constraint Satisfaction",
                        "skills": [
                            {"code": "LOG_SEATING", "name": "Linear & Circular Seating Arrangements", "difficulty": 0.60, "blooms": "Apply"},
                            {"code": "LOG_DATA_SUFF", "name": "Data Sufficiency Determination", "difficulty": 0.70, "blooms": "Analyze"},
                        ]
                    }
                ]
            }
        ]
    },
    # 4. Programming Fundamentals
    {
        "code": "PROG",
        "name": "Programming Fundamentals",
        "description": "Syntax, control flow, functions, memory management, pointers, and algorithm basics.",
        "icon": "Code",
        "topics": [
            {
                "name": "Syntax & Control Flow",
                "subtopics": [
                    {
                        "name": "Core Language Constructs",
                        "skills": [
                            {"code": "PRG_VARIABLES", "name": "Data Types, Operators & Precedence", "difficulty": 0.25, "blooms": "Understand"},
                            {"code": "PRG_CONDITIONALS", "name": "Conditionals & Branching", "difficulty": 0.35, "blooms": "Apply"},
                            {"code": "PRG_LOOPS", "name": "Iteration, While & Nested Loops", "difficulty": 0.45, "blooms": "Apply"},
                        ]
                    }
                ]
            },
            {
                "name": "Functions & Memory",
                "subtopics": [
                    {
                        "name": "Execution Context",
                        "skills": [
                            {"code": "PRG_FUNCTIONS", "name": "Functions, Scope & Parameter Passing", "difficulty": 0.50, "blooms": "Apply"},
                            {"code": "PRG_RECURSION", "name": "Recursion & Call Stack Dynamics", "difficulty": 0.65, "blooms": "Analyze"},
                            {"code": "PRG_POINTERS", "name": "Pointers & Dynamic Memory Allocation", "difficulty": 0.75, "blooms": "Analyze"},
                        ]
                    }
                ]
            }
        ]
    },
    # 5. Data Structures and Algorithms
    {
        "code": "DSA",
        "name": "Data Structures & Algorithms",
        "description": "Linear and non-linear data structures, searching, sorting, graph algorithms, and dynamic programming.",
        "icon": "Network",
        "topics": [
            {
                "name": "Linear Data Structures",
                "subtopics": [
                    {
                        "name": "Sequential Storage",
                        "skills": [
                            {"code": "DSA_ARRAYS", "name": "Arrays & Two-Pointer Techniques", "difficulty": 0.40, "blooms": "Apply"},
                            {"code": "DSA_LINKED_LISTS", "name": "Singly & Doubly Linked Lists", "difficulty": 0.55, "blooms": "Apply"},
                            {"code": "DSA_STACKS_QUEUES", "name": "Stacks, Queues & Monotonic Stacks", "difficulty": 0.60, "blooms": "Apply"},
                        ]
                    }
                ]
            },
            {
                "name": "Trees & Hierarchies",
                "subtopics": [
                    {
                        "name": "Tree Structures",
                        "skills": [
                            {"code": "DSA_BINARY_TREES", "name": "Binary Trees & Tree Traversals", "difficulty": 0.65, "blooms": "Analyze"},
                            {"code": "DSA_BST", "name": "Binary Search Trees & Balancing", "difficulty": 0.70, "blooms": "Analyze"},
                        ]
                    }
                ]
            },
            {
                "name": "Graphs & Algorithms",
                "subtopics": [
                    {
                        "name": "Graph Traversal & Optimization",
                        "skills": [
                            {"code": "DSA_GRAPH_BFS_DFS", "name": "Graph BFS & DFS Representations", "difficulty": 0.75, "blooms": "Apply"},
                            {"code": "DSA_DYNAMIC_PROG", "name": "Dynamic Programming: Memoization & Tabulation", "difficulty": 0.85, "blooms": "Evaluate"},
                        ]
                    }
                ]
            }
        ]
    },
    # 6. SQL
    {
        "code": "SQL",
        "name": "SQL & Relational Querying",
        "description": "Query authoring, multi-table joins, subqueries, aggregation, and index optimization.",
        "icon": "Database",
        "topics": [
            {
                "name": "Query Fundamentals",
                "subtopics": [
                    {
                        "name": "Data Selection & Filtering",
                        "skills": [
                            {"code": "SQL_BASIC_SELECT", "name": "SELECT, WHERE & Filtering Clauses", "difficulty": 0.30, "blooms": "Apply"},
                            {"code": "SQL_AGGREGATES", "name": "GROUP BY, HAVING & Aggregations", "difficulty": 0.50, "blooms": "Apply"},
                        ]
                    }
                ]
            },
            {
                "name": "Complex Queries & Optimization",
                "subtopics": [
                    {
                        "name": "Multi-Table Operations",
                        "skills": [
                            {"code": "SQL_JOINS", "name": "INNER, LEFT, RIGHT & FULL OUTER Joins", "difficulty": 0.60, "blooms": "Apply"},
                            {"code": "SQL_SUBQUERIES", "name": "Correlated Subqueries & CTEs", "difficulty": 0.70, "blooms": "Analyze"},
                            {"code": "SQL_INDEXING", "name": "B-Tree Indexes & EXPLAIN Plan Analysis", "difficulty": 0.80, "blooms": "Evaluate"},
                        ]
                    }
                ]
            }
        ]
    },
    # 7. Object-Oriented Programming
    {
        "code": "OOP",
        "name": "Object-Oriented Programming",
        "description": "Encapsulation, abstraction, inheritance, polymorphism, design principles, and design patterns.",
        "icon": "Box",
        "topics": [
            {
                "name": "Core OOP Pillars",
                "subtopics": [
                    {
                        "name": "Encapsulation & Inheritance",
                        "skills": [
                            {"code": "OOP_CLASSES", "name": "Classes, Objects & Constructors", "difficulty": 0.35, "blooms": "Understand"},
                            {"code": "OOP_INHERITANCE", "name": "Inheritance, Interfaces & Abstract Classes", "difficulty": 0.55, "blooms": "Apply"},
                            {"code": "OOP_POLYMORPHISM", "name": "Method Overloading & Dynamic Dispatch", "difficulty": 0.65, "blooms": "Analyze"},
                            {"code": "OOP_SOLID", "name": "SOLID Design Principles & Patterns", "difficulty": 0.75, "blooms": "Evaluate"},
                        ]
                    }
                ]
            }
        ]
    },
    # 8. DBMS
    {
        "code": "DBMS",
        "name": "Database Management Systems",
        "description": "Relational algebra, normalization (1NF-BCNF), transactions, ACID properties, and concurrency.",
        "icon": "HardDrive",
        "topics": [
            {
                "name": "Relational Theory & Design",
                "subtopics": [
                    {
                        "name": "Schema Design",
                        "skills": [
                            {"code": "DBMS_REL_MODEL", "name": "Relational Model & Key Constraints", "difficulty": 0.40, "blooms": "Understand"},
                            {"code": "DBMS_NORMALIZATION", "name": "Functional Dependencies & 1NF-BCNF", "difficulty": 0.65, "blooms": "Analyze"},
                        ]
                    }
                ]
            },
            {
                "name": "Transactions & Concurrency",
                "subtopics": [
                    {
                        "name": "ACID Compliance",
                        "skills": [
                            {"code": "DBMS_ACID", "name": "ACID Properties & Recovery Techniques", "difficulty": 0.60, "blooms": "Understand"},
                            {"code": "DBMS_CONCURRENCY", "name": "Two-Phase Locking & Serializability", "difficulty": 0.75, "blooms": "Analyze"},
                        ]
                    }
                ]
            }
        ]
    },
    # 9. Operating Systems
    {
        "code": "OS",
        "name": "Operating Systems",
        "description": "Process scheduling, thread synchronization, deadlocks, virtual memory, paging, and file systems.",
        "icon": "Cpu",
        "topics": [
            {
                "name": "Process Management",
                "subtopics": [
                    {
                        "name": "Processes & Threads",
                        "skills": [
                            {"code": "OS_PROCESSES", "name": "Process Lifecycle & Context Switching", "difficulty": 0.45, "blooms": "Understand"},
                            {"code": "OS_SCHEDULING", "name": "CPU Scheduling Algorithms (SJF, RR, Priority)", "difficulty": 0.55, "blooms": "Apply"},
                            {"code": "OS_SYNC_DEADLOCK", "name": "Mutexes, Semaphores & Deadlock Detection", "difficulty": 0.75, "blooms": "Analyze"},
                        ]
                    }
                ]
            },
            {
                "name": "Memory & Storage",
                "subtopics": [
                    {
                        "name": "Virtual Memory",
                        "skills": [
                            {"code": "OS_VIRTUAL_MEM", "name": "Virtual Memory, Paging & TLBs", "difficulty": 0.70, "blooms": "Understand"},
                            {"code": "OS_PAGE_REPLACE", "name": "Page Replacement Algorithms (LRU, FIFO)", "difficulty": 0.65, "blooms": "Apply"},
                        ]
                    }
                ]
            }
        ]
    },
    # 10. Computer Networks
    {
        "code": "NETWORKS",
        "name": "Computer Networks",
        "description": "OSI and TCP/IP protocol stacks, routing algorithms, transport protocols (TCP/UDP), and network security.",
        "icon": "Globe",
        "topics": [
            {
                "name": "Protocol Architectures",
                "subtopics": [
                    {
                        "name": "Layered Architecture",
                        "skills": [
                            {"code": "NET_OSI_MODEL", "name": "OSI & TCP/IP 5-Layer Stack", "difficulty": 0.40, "blooms": "Understand"},
                            {"code": "NET_APPLICATION", "name": "HTTP/HTTPS, DNS & Web Protocols", "difficulty": 0.50, "blooms": "Understand"},
                        ]
                    }
                ]
            },
            {
                "name": "Transport & Routing",
                "subtopics": [
                    {
                        "name": "End-to-End Transport",
                        "skills": [
                            {"code": "NET_TCP_UDP", "name": "TCP 3-Way Handshake, Flow & Congestion Control", "difficulty": 0.70, "blooms": "Analyze"},
                            {"code": "NET_IP_ROUTING", "name": "IPv4/IPv6 Subnetting & Routing Algorithms", "difficulty": 0.75, "blooms": "Apply"},
                        ]
                    }
                ]
            }
        ]
    },
    # 11. Machine Learning
    {
        "code": "ML",
        "name": "Machine Learning",
        "description": "Supervised learning, model evaluation metrics, unsupervised clustering, and neural network foundations.",
        "icon": "Sparkles",
        "topics": [
            {
                "name": "Supervised Learning",
                "subtopics": [
                    {
                        "name": "Predictive Modeling",
                        "skills": [
                            {"code": "ML_REGRESSION", "name": "Linear & Logistic Regression", "difficulty": 0.50, "blooms": "Apply"},
                            {"code": "ML_DECISION_TREES", "name": "Decision Trees & Random Forests", "difficulty": 0.65, "blooms": "Apply"},
                            {"code": "ML_EVALUATION", "name": "Precision, Recall, F1 & ROC-AUC Curves", "difficulty": 0.70, "blooms": "Analyze"},
                        ]
                    }
                ]
            },
            {
                "name": "Neural Foundations",
                "subtopics": [
                    {
                        "name": "Deep Learning Principles",
                        "skills": [
                            {"code": "ML_NEURAL_NETS", "name": "Perceptrons, Backpropagation & Activation Functions", "difficulty": 0.80, "blooms": "Analyze"},
                        ]
                    }
                ]
            }
        ]
    }
]

# Prerequisite Relationships (Source Skill Code -> Target Skill Code)
PREREQUISITE_EDGES = [
    # Verbal
    ("VRB_SUBJECT_VERB", "VRB_TENSE_CONSIST"),
    ("VRB_TENSE_CONSIST", "VRB_MODIFIERS"),
    ("VRB_MAIN_IDEA", "VRB_INFERENCE"),
    
    # Quant
    ("QNT_NUMBERS", "QNT_PERCENTAGES"),
    ("QNT_PERCENTAGES", "QNT_RATIO_PROP"),
    ("QNT_RATIO_PROP", "QNT_TIME_WORK"),
    ("QNT_NUMBERS", "QNT_PERMUTATIONS"),
    ("QNT_PERMUTATIONS", "QNT_PROBABILITY"),

    # Reasoning
    ("LOG_SYLLOGISMS", "LOG_DEDUCTION"),
    ("LOG_SEATING", "LOG_DATA_SUFF"),

    # Programming Fundamentals
    ("PRG_VARIABLES", "PRG_CONDITIONALS"),
    ("PRG_CONDITIONALS", "PRG_LOOPS"),
    ("PRG_LOOPS", "PRG_FUNCTIONS"),
    ("PRG_FUNCTIONS", "PRG_RECURSION"),
    ("PRG_FUNCTIONS", "PRG_POINTERS"),

    # DSA
    ("PRG_VARIABLES", "DSA_ARRAYS"),
    ("DSA_ARRAYS", "DSA_LINKED_LISTS"),
    ("DSA_LINKED_LISTS", "DSA_STACKS_QUEUES"),
    ("DSA_LINKED_LISTS", "DSA_BINARY_TREES"),
    ("DSA_BINARY_TREES", "DSA_BST"),
    ("DSA_BINARY_TREES", "DSA_GRAPH_BFS_DFS"),
    ("PRG_RECURSION", "DSA_DYNAMIC_PROG"),
    ("DSA_ARRAYS", "DSA_DYNAMIC_PROG"),

    # SQL
    ("SQL_BASIC_SELECT", "SQL_AGGREGATES"),
    ("SQL_BASIC_SELECT", "SQL_JOINS"),
    ("SQL_JOINS", "SQL_SUBQUERIES"),
    ("SQL_SUBQUERIES", "SQL_INDEXING"),

    # OOP
    ("PRG_FUNCTIONS", "OOP_CLASSES"),
    ("OOP_CLASSES", "OOP_INHERITANCE"),
    ("OOP_INHERITANCE", "OOP_POLYMORPHISM"),
    ("OOP_POLYMORPHISM", "OOP_SOLID"),

    # DBMS
    ("DBMS_REL_MODEL", "DBMS_NORMALIZATION"),
    ("DBMS_REL_MODEL", "DBMS_ACID"),
    ("DBMS_ACID", "DBMS_CONCURRENCY"),

    # Operating Systems
    ("OS_PROCESSES", "OS_SCHEDULING"),
    ("OS_PROCESSES", "OS_SYNC_DEADLOCK"),
    ("OS_VIRTUAL_MEM", "OS_PAGE_REPLACE"),

    # Computer Networks
    ("NET_OSI_MODEL", "NET_APPLICATION"),
    ("NET_OSI_MODEL", "NET_TCP_UDP"),
    ("NET_TCP_UDP", "NET_IP_ROUTING"),

    # Machine Learning
    ("QNT_PERCENTAGES", "ML_REGRESSION"),
    ("ML_REGRESSION", "ML_DECISION_TREES"),
    ("ML_REGRESSION", "ML_EVALUATION"),
    ("ML_REGRESSION", "ML_NEURAL_NETS"),
]


def seed_curriculum(db: Session) -> dict:
    """
    Executes idempotent seeding of the curriculum graph.
    Returns counts of domains, topics, subtopics, skills, and edges created.
    """
    stats = {"domains": 0, "topics": 0, "subtopics": 0, "skills": 0, "edges": 0}
    skill_code_to_id = {}

    for d_idx, d_data in enumerate(CURRICULUM_DATA):
        # 1. Upsert Domain
        domain = db.query(Domain).filter(Domain.code == d_data["code"]).first()
        if not domain:
            domain = Domain(
                code=d_data["code"],
                name=d_data["name"],
                description=d_data["description"],
                icon=d_data["icon"]
            )
            db.add(domain)
            db.flush()
            stats["domains"] += 1

        # 2. Upsert Topics
        for t_idx, t_data in enumerate(d_data["topics"]):
            topic = db.query(Topic).filter(Topic.domain_id == domain.id, Topic.name == t_data["name"]).first()
            if not topic:
                topic = Topic(
                    domain_id=domain.id,
                    name=t_data["name"],
                    order_index=t_idx
                )
                db.add(topic)
                db.flush()
                stats["topics"] += 1

            # 3. Upsert Subtopics
            for st_idx, st_data in enumerate(t_data["subtopics"]):
                subtopic = db.query(Subtopic).filter(Subtopic.topic_id == topic.id, Subtopic.name == st_data["name"]).first()
                if not subtopic:
                    subtopic = Subtopic(
                        topic_id=topic.id,
                        name=st_data["name"],
                        order_index=st_idx
                    )
                    db.add(subtopic)
                    db.flush()
                    stats["subtopics"] += 1

                # 4. Upsert Skills
                for sk_data in st_data["skills"]:
                    skill = db.query(Skill).filter(Skill.code == sk_data["code"]).first()
                    if not skill:
                        skill = Skill(
                            subtopic_id=subtopic.id,
                            code=sk_data["code"],
                            name=sk_data["name"],
                            difficulty_level=sk_data["difficulty"],
                            blooms_level=sk_data["blooms"]
                        )
                        db.add(skill)
                        db.flush()
                        stats["skills"] += 1
                    skill_code_to_id[sk_data["code"]] = skill.id

    # 5. Populate and validate prerequisite edges
    edges_to_validate = []
    for prereq_code, skill_code in PREREQUISITE_EDGES:
        prereq_id = skill_code_to_id.get(prereq_code)
        target_id = skill_code_to_id.get(skill_code)

        if not prereq_id or not target_id:
            logger.warning(f"Skipping edge: {prereq_code} -> {skill_code} (missing skill)")
            continue

        existing_edge = db.query(SkillEdge).filter(
            SkillEdge.prereq_id == prereq_id,
            SkillEdge.skill_id == target_id
        ).first()

        if not existing_edge:
            edge = SkillEdge(prereq_id=prereq_id, skill_id=target_id, strength=1.0)
            db.add(edge)
            edges_to_validate.append(edge)
            stats["edges"] += 1

    db.flush()

    # 6. Validate DAG Acyclicity using SkillDependencyGraph prior to committing
    all_skills = db.query(Skill).all()
    all_edges = db.query(SkillEdge).all()
    graph = SkillDependencyGraph(all_skills, all_edges)
    # verify topological sort can be computed
    topo_order = graph.get_topological_order()
    logger.info(f"Curriculum graph validated successfully! Topological order contains {len(topo_order)} skills.")

    db.commit()
    logger.info(f"Curriculum seed complete: {stats}")
    return stats


if __name__ == "__main__":
    init_db()
    with SessionLocal() as session:
        result = seed_curriculum(session)
        print("Seed result:", result)
