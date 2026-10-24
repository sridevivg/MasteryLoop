"""
Verbal Ability Question Bank.
Topic 1: Grammar & Sentence Correction (15 questions across VRB_SUBJECT_VERB, VRB_TENSE_CONSIST, VRB_MODIFIERS)
Topic 2: Reading Comprehension (15 questions across VRB_MAIN_IDEA, VRB_INFERENCE)
"""

VERBAL_ITEMS = [
    # =========================================================================
    # TOPIC 1: Grammar & Sentence Correction (15 items)
    # =========================================================================
    # --- VRB_SUBJECT_VERB (5 items) ---
    {
        "skill_code": "VRB_SUBJECT_VERB",
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
        "skill_code": "VRB_SUBJECT_VERB",
        "stem": "Choose the option that maintains correct subject-verb agreement:\n\n*\"A cluster of high-performance GPU nodes _____ provisioned to process the deep learning pipeline.\"*",
        "options": [
            {"id": "A", "text": "were", "is_distractor": True},
            {"id": "B", "text": "was", "is_distractor": False},
            {"id": "C", "text": "are", "is_distractor": True},
            {"id": "D", "text": "have been", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The head noun of the subject phrase is the collective singular noun 'cluster', not the plural prepositional object 'nodes'. Therefore, the singular verb 'was' is required.",
        "distractor_explanations": {
            "A": "Error: Proximity trap; mistook the intervening prepositional plural 'nodes' for the head noun.",
            "C": "Error: Plural present verb agreeing incorrectly with 'nodes'.",
            "D": "Error: Plural present perfect verb."
        },
        "a": 1.40,
        "b": -1.20,
        "point_biserial": 0.44
    },
    {
        "skill_code": "VRB_SUBJECT_VERB",
        "stem": "Which of the following sentences adheres strictly to standard subject-verb agreement rules?",
        "options": [
            {"id": "A", "text": "Neither the software architect nor the project lead know the root cause.", "is_distractor": True},
            {"id": "B", "text": "Neither the software architect nor the project lead knows the root cause.", "is_distractor": False},
            {"id": "C", "text": "Neither the software architect nor the project lead are knowing the root cause.", "is_distractor": True},
            {"id": "D", "text": "Neither of the architects know which deployment failed.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "When two singular subjects are joined by 'neither... nor', the verb must be singular ('knows'). Similarly, 'neither of...' takes a singular verb.",
        "distractor_explanations": {
            "A": "Error: Used plural verb 'know' with two singular subjects joined by 'neither... nor'.",
            "C": "Error: 'know' is a stative verb and should not be used in continuous progressive form here.",
            "D": "Error: 'Neither' as an indefinite pronoun is grammatically singular and requires 'knows'."
        },
        "a": 1.55,
        "b": 0.30,
        "point_biserial": 0.46
    },
    {
        "skill_code": "VRB_SUBJECT_VERB",
        "stem": "Identify the sentence where the subject and verb agree correctly:",
        "options": [
            {"id": "A", "text": "The committee, along with several external consultants, has published its audit report.", "is_distractor": False},
            {"id": "B", "text": "The committee, along with several external consultants, have published their audit report.", "is_distractor": True},
            {"id": "C", "text": "Each of the microservices deploy independently to production.", "is_distractor": True},
            {"id": "D", "text": "Ten gigabytes of RAM were sufficient for the background daemon.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Parenthetical phrases introduced by 'along with', 'as well as', or 'in addition to' do not change the number of the subject ('committee', singular). Thus 'has published' is correct.",
        "distractor_explanations": {
            "B": "Error: Treated 'along with external consultants' as a compound subject like 'and'.",
            "C": "Error: 'Each' is singular and requires 'deploys'.",
            "D": "Error: Quantities of measurement/storage treated as a single unit take a singular verb ('was sufficient')."
        },
        "a": 1.65,
        "b": 1.10,
        "point_biserial": 0.48
    },
    {
        "skill_code": "VRB_SUBJECT_VERB",
        "stem": "Select the sentence with impeccable subject-verb agreement:",
        "options": [
            {"id": "A", "text": "The number of concurrent database connections has exceeded the threshold.", "is_distractor": False},
            {"id": "B", "text": "The number of concurrent database connections have exceeded the threshold.", "is_distractor": True},
            {"id": "C", "text": "A number of critical bugs has been documented by QA.", "is_distractor": True},
            {"id": "D", "text": "Physics and mathematics is taught by the senior professor.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "'The number of' denotes a singular specific statistic and requires a singular verb ('has exceeded'), whereas 'a number of' acts as a quantifier meaning 'several' and takes a plural verb.",
        "distractor_explanations": {
            "B": "Error: 'The number' is singular; 'have' is plural.",
            "C": "Error: 'A number of' takes a plural verb ('have been documented').",
            "D": "Error: Two distinct subjects joined by 'and' require a plural verb ('are taught')."
        },
        "a": 1.70,
        "b": 1.50,
        "point_biserial": 0.49
    },

    # --- VRB_TENSE_CONSIST (5 items) ---
    {
        "skill_code": "VRB_TENSE_CONSIST",
        "stem": "Select the correct conditional sentence construction:\n\n*\"If the caching layer _____ operational during the traffic spike, the database would not have crashed.\"*",
        "options": [
            {"id": "A", "text": "was", "is_distractor": True},
            {"id": "B", "text": "would have been", "is_distractor": True},
            {"id": "C", "text": "had been", "is_distractor": False},
            {"id": "D", "text": "has been", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "This is a Third Conditional (unreal past condition). The protasis (if-clause) requires the past perfect ('had been') to pair with 'would not have crashed' in the apodosis.",
        "distractor_explanations": {
            "A": "Error: Simple past 'was' creates an ungrammatical mixed conditional.",
            "B": "Error: 'Would have' must never appear in the if-clause of a standard conditional.",
            "D": "Error: Present perfect cannot express counterfactual past hypotheses."
        },
        "a": 1.35,
        "b": -0.80,
        "point_biserial": 0.43
    },
    {
        "skill_code": "VRB_TENSE_CONSIST",
        "stem": "Which option maintains flawless tense sequence in indirect speech?\n\n*\"The lead engineer stated that the deployment script _____ successfully two hours prior.\"*",
        "options": [
            {"id": "A", "text": "runs", "is_distractor": True},
            {"id": "B", "text": "has run", "is_distractor": True},
            {"id": "C", "text": "had run", "is_distractor": False},
            {"id": "D", "text": "will run", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "When reporting a past statement ('stated') referring to an action completed prior to that statement ('two hours prior'), the past perfect ('had run') is required by the sequence of tenses.",
        "distractor_explanations": {
            "A": "Error: Simple present tense violates backshifting rules in indirect reporting.",
            "B": "Error: Present perfect cannot be used with a past reporting verb when describing an action preceding the speech.",
            "D": "Error: Future tense contradicts the chronological marker 'two hours prior'."
        },
        "a": 1.45,
        "b": -0.10,
        "point_biserial": 0.45
    },
    {
        "skill_code": "VRB_TENSE_CONSIST",
        "stem": "Identify the sentence that violates tense consistency:",
        "options": [
            {"id": "A", "text": "By the time the load testing concludes tomorrow, the DevOps team will have analyzed the telemetry.", "is_distractor": True},
            {"id": "B", "text": "As soon as the alert fired, the on-call engineer logs into the bastion server.", "is_distractor": False},
            {"id": "C", "text": "Whenever the build fails, the CI/CD pipeline triggers an automated Slack notification.", "is_distractor": True},
            {"id": "D", "text": "Had the failover mechanism activated, data loss would have been minimized.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Sentence B shifts unjustifiably from the past tense ('fired') to the simple present tense ('logs'). It should read: '...logged into the bastion server.'",
        "distractor_explanations": {
            "A": "Consistent: Correct use of future perfect ('will have analyzed') with a future temporal clause ('by the time... concludes').",
            "C": "Consistent: Habitual present conditional with matching present tenses.",
            "D": "Consistent: Inverted third conditional with past perfect subjunctive and conditional perfect."
        },
        "a": 1.50,
        "b": 0.40,
        "point_biserial": 0.46
    },
    {
        "skill_code": "VRB_TENSE_CONSIST",
        "stem": "Choose the correct verb form:\n\n*\"The product manager insisted that every feature branch _____ thoroughly reviewed before merging.\"*",
        "options": [
            {"id": "A", "text": "is", "is_distractor": True},
            {"id": "B", "text": "be", "is_distractor": False},
            {"id": "C", "text": "was", "is_distractor": True},
            {"id": "D", "text": "must be", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Verbs of demand or insistence ('insisted that...') take the mandative subjunctive mood, which uses the base form of the verb ('be reviewed') without inflections.",
        "distractor_explanations": {
            "A": "Error: Indicative present form used instead of the required subjunctive base form.",
            "C": "Error: Past indicative violates mandative subjunctive syntax.",
            "D": "Error: Redundant modal auxiliary in formal subjunctive clause."
        },
        "a": 1.65,
        "b": 0.95,
        "point_biserial": 0.48
    },
    {
        "skill_code": "VRB_TENSE_CONSIST",
        "stem": "Select the sentence with accurate sequence of tenses across compound clauses:",
        "options": [
            {"id": "A", "text": "Before the security patch was deployed, the vulnerability has been exploited repeatedly.", "is_distractor": True},
            {"id": "B", "text": "Before the security patch was deployed, the vulnerability had been exploited repeatedly.", "is_distractor": False},
            {"id": "C", "text": "Before the security patch is deployed, the vulnerability had been exploited repeatedly.", "is_distractor": True},
            {"id": "D", "text": "Before the security patch was deployed, the vulnerability will be exploited repeatedly.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The past perfect ('had been exploited') correctly denotes an action completed prior to another past event ('was deployed').",
        "distractor_explanations": {
            "A": "Error: Present perfect cannot be used for an event completed before another past event.",
            "C": "Error: Incompatible present and past perfect time frames.",
            "D": "Error: Future tense contradicts the past framework."
        },
        "a": 1.70,
        "b": 1.40,
        "point_biserial": 0.50
    },

    # --- VRB_MODIFIERS (5 items) ---
    {
        "skill_code": "VRB_MODIFIERS",
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
    {
        "skill_code": "VRB_MODIFIERS",
        "stem": "Which sentence demonstrates proper grammatical parallelism in technical writing?",
        "options": [
            {"id": "A", "text": "The candidate is skilled in writing clean code, architecting microservices, and to debug distributed systems.", "is_distractor": True},
            {"id": "B", "text": "The candidate is skilled in writing clean code, architecting microservices, and debugging distributed systems.", "is_distractor": False},
            {"id": "C", "text": "The candidate is skilled in writing clean code, microservices architecture, and debugs distributed systems.", "is_distractor": True},
            {"id": "D", "text": "The candidate is skilled in writing clean code, to architect microservices, and debugging distributed systems.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Parallelism requires all coordinate elements governed by 'in' to share the identical grammatical form (gerund phrases: 'writing...', 'architecting...', 'debugging...').",
        "distractor_explanations": {
            "A": "Error: Shifts from gerunds to an infinitive ('to debug').",
            "C": "Error: Mixes gerund, noun phrase, and conjugated verb.",
            "D": "Error: Inconsistent alternation between gerunds and infinitives."
        },
        "a": 1.30,
        "b": -0.90,
        "point_biserial": 0.41
    },
    {
        "skill_code": "VRB_MODIFIERS",
        "stem": "Identify the sentence free from misplaced adverbs or squinting modifiers:",
        "options": [
            {"id": "A", "text": "The developer only tested the API endpoints that handled authentication.", "is_distractor": True},
            {"id": "B", "text": "The developer tested only the API endpoints that handled authentication.", "is_distractor": False},
            {"id": "C", "text": "Students who study rarely fail comprehensive placement assessments.", "is_distractor": True},
            {"id": "D", "text": "Refactoring the legacy codebase rapidly became necessary.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The limiter 'only' should immediately precede the constituent it modifies ('only the API endpoints'). Placing it before 'tested' implies testing was the only action taken.",
        "distractor_explanations": {
            "A": "Misplaced limiter: 'only tested' suggests testing was done, but nothing else.",
            "C": "Squinting modifier: 'rarely' could modify 'study' or 'fail'.",
            "D": "Squinting modifier: 'rapidly' could modify 'refactoring' or 'became'."
        },
        "a": 1.55,
        "b": 0.70,
        "point_biserial": 0.47
    },
    {
        "skill_code": "VRB_MODIFIERS",
        "stem": "Select the sentence with impeccable parallel structure across correlative conjunctions:",
        "options": [
            {"id": "A", "text": "The new release not only improved database throughput but also security vulnerabilities were resolved.", "is_distractor": True},
            {"id": "B", "text": "The new release not only improved database throughput but also resolved security vulnerabilities.", "is_distractor": False},
            {"id": "C", "text": "The new release improved not only database throughput but also resolving security vulnerabilities.", "is_distractor": True},
            {"id": "D", "text": "The new release not only improved database throughput but security vulnerabilities were also resolved.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Elements balanced by 'not only ... but also' must have identical grammatical structure. 'Improved [noun phrase]' parallels 'resolved [noun phrase]'.",
        "distractor_explanations": {
            "A": "Error: A verb phrase ('improved...') is paired with a full passive clause ('security vulnerabilities were...').",
            "C": "Error: Noun phrase ('throughput') is paired with a gerund phrase ('resolving...').",
            "D": "Error: Misplaced 'also' breaks the correlative formula."
        },
        "a": 1.60,
        "b": 1.05,
        "point_biserial": 0.48
    },
    {
        "skill_code": "VRB_MODIFIERS",
        "stem": "Which option fixes the dangling modifier in the following excerpt?\n\n*\"By implementing distributed tracing, bottleneck identification became straightforward for the operations team.\"*",
        "options": [
            {"id": "A", "text": "By implementing distributed tracing, the operations team was able to identify bottlenecks straightforwardly.", "is_distractor": False},
            {"id": "B", "text": "By implementing distributed tracing, bottlenecks were straightforwardly identified by the operations team.", "is_distractor": True},
            {"id": "C", "text": "Implementing distributed tracing, bottleneck identification was made straightforward.", "is_distractor": True},
            {"id": "D", "text": "By implementing distributed tracing, it was straightforward for the operations team to identify bottlenecks.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The agent who implements distributed tracing is 'the operations team'. Placing 'the operations team' as the subject of the main clause eliminates the dangling modifier.",
        "distractor_explanations": {
            "B": "Error: Passive voice leaves 'bottlenecks' as the subject, implying bottlenecks implemented the tracing.",
            "C": "Error: Retains the dangling modifier with 'bottleneck identification' as subject.",
            "D": "Error: Dummy pronoun 'it' cannot logically perform the action of implementing."
        },
        "a": 1.70,
        "b": 1.60,
        "point_biserial": 0.51
    },

    # =========================================================================
    # TOPIC 2: Reading Comprehension (15 items)
    # =========================================================================
    # --- VRB_MAIN_IDEA (8 items) ---
    {
        "skill_code": "VRB_MAIN_IDEA",
        "stem": "Read the excerpt below:\n\n*\"While microservices offer distinct advantages in fault isolation and independent team velocity, they introduce significant cognitive overhead. Distributed transactions require saga patterns, network latency compounds across service meshes, and observability demands sophisticated tracing pipelines. For early-stage startups with uncertain product-market fit, a modular monolith frequently yields higher development throughput at a fraction of the operational cost.\"*\n\nWhat is the primary thesis of the author?",
        "options": [
            {"id": "A", "text": "Microservices are obsolete and should be replaced by monolithic designs in all engineering organizations.", "is_distractor": True},
            {"id": "B", "text": "The operational complexities of microservices often outweigh their benefits for early-stage organizations.", "is_distractor": False},
            {"id": "C", "text": "Distributed sagas and tracing pipelines are impossible to implement reliably in production.", "is_distractor": True},
            {"id": "D", "text": "Independent team velocity is the single most critical factor in software architecture selection.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The author contrasts microservice benefits with operational overhead, concluding that for startups with uncertain fit, a modular monolith provides superior velocity relative to operational costs.",
        "distractor_explanations": {
            "A": "Overstatement: The author acknowledges distinct advantages and does not argue for universal obsolescence.",
            "C": "Distortion: The passage notes that distributed sagas require sophistication, not that they are impossible.",
            "D": "Contradictory: The passage emphasizes balancing velocity against cognitive and operational overhead."
        },
        "a": 1.35,
        "b": -1.00,
        "point_biserial": 0.42
    },
    {
        "skill_code": "VRB_MAIN_IDEA",
        "stem": "Read the following passage:\n\n*\"Technical debt is frequently misunderstood as mere sloppy engineering. In reality, strategic technical debt resembles financial leverage: taking on architectural shortcuts can accelerate time-to-market and validate critical commercial hypotheses before capital runs dry. However, like financial debt, technical debt accrues compounding interest in the form of reduced feature velocity and elevated bug density. Sustainable engineering organizations treat technical debt not as a moral failing, but as a deliberate financial instrument requiring active principal repayment.\"*\n\nWhich statement best captures the central argument?",
        "options": [
            {"id": "A", "text": "Engineering teams must never permit technical debt into a production codebase under any circumstances.", "is_distractor": True},
            {"id": "B", "text": "Technical debt is a legitimate tactical tradeoff that accelerates early goals but demands disciplined ongoing remediation.", "is_distractor": False},
            {"id": "C", "text": "Financial debt and technical debt have identical mathematical formulas for interest computation.", "is_distractor": True},
            {"id": "D", "text": "Speed to market is always more valuable than writing bug-free software.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The author conceptualizes technical debt as a conscious tactical tool ('strategic leverage') that enables speed but requires scheduled repayment ('compounding interest').",
        "distractor_explanations": {
            "A": "Directly contradicts the passage's view of debt as a strategic financial instrument.",
            "C": "Literal fallacy: The passage uses financial debt as an analogy, not an identical mathematical formula.",
            "D": "Extreme claim unsupported by the balanced message of the passage."
        },
        "a": 1.40,
        "b": -0.40,
        "point_biserial": 0.44
    },
    {
        "skill_code": "VRB_MAIN_IDEA",
        "stem": "Read the passage:\n\n*\"Algorithmic bias in artificial intelligence is rarely the result of malicious programmers embedding overt prejudice. Rather, machine learning models function as high-dimensional mirrors, reflecting and amplifying historical socioeconomic disparities captured in observational training datasets. Addressing algorithmic unfairness thus requires rigorous data provenance audits, counterfactual fairness metrics, and interdisciplinary governance rather than purely post-hoc model tuning.\"*\n\nThe author's tone can be best characterized as:",
        "options": [
            {"id": "A", "text": "Alarmist and emotional", "is_distractor": True},
            {"id": "B", "text": "Objective, analytical, and prescriptive", "is_distractor": False},
            {"id": "C", "text": "Cynical and dismissive of AI research", "is_distractor": True},
            {"id": "D", "text": "Defensive of software engineers' culpability", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The author provides a balanced, scientific diagnosis ('mirrors reflecting historical disparities') followed by constructive recommendations ('counterfactual fairness metrics, governance').",
        "distractor_explanations": {
            "A": "The text lacks emotional or alarmist language, relying on measured academic vocabulary.",
            "C": "The text does not dismiss AI, but proposes specific methods to ensure algorithmic fairness.",
            "D": "The author explains causal mechanisms rather than offering an apology or defense."
        },
        "a": 1.50,
        "b": 0.20,
        "point_biserial": 0.46
    },
    {
        "skill_code": "VRB_MAIN_IDEA",
        "stem": "Read the excerpt:\n\n*\"The shift toward declarative infrastructure-as-code has transformed systems operations into a software discipline. Where sysadmins once executed imperative shell scripts and manually tweaked config files, modern site reliability teams define state targets in versioned manifests. This convergence enforces automated drift detection, ephemeral environments, and auditability. The primary challenge, however, has migrated from server provisioning to state management and pipeline security.\"*\n\nWhich heading best encapsulates the passage?",
        "options": [
            {"id": "A", "text": "Why Shell Scripts Are Superior for Production Systems", "is_distractor": True},
            {"id": "B", "text": "The Evolution from Imperative Sysadmin to Declarative Software Operations", "is_distractor": False},
            {"id": "C", "text": "How to Configure Versioned Manifests in Kubernetes", "is_distractor": True},
            {"id": "D", "text": "The Elimination of Operational Vulnerabilities via Git", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The passage outlines the historical paradigm shift from imperative manual administration to declarative software-driven infrastructure.",
        "distractor_explanations": {
            "A": "Contradicts the text: The author praises declarative manifests over imperative scripts.",
            "C": "Too narrow: The text discusses broad infrastructural concepts, not a specific tool implementation.",
            "D": "Inaccurate: The text explicitly notes that challenges remain around pipeline security."
        },
        "a": 1.45,
        "b": 0.50,
        "point_biserial": 0.45
    },
    {
        "skill_code": "VRB_MAIN_IDEA",
        "stem": "Consider the following passage:\n\n*\"A hallmark of resilient distributed systems is graceful degradation under load. When downstream dependencies experience brownouts or saturated thread pools, an unthrottled system cascades into catastrophic failure. Circuit breakers, deadline propagation, and load shedding protect core throughput by intentionally dropping non-critical traffic. Survival under pathological conditions requires accepting imperfect service rather than chasing total availability.\"*\n\nWhat is the core philosophical takeaway advocated by the text?",
        "options": [
            {"id": "A", "text": "Resilience in distributed computing necessitates planned compromises in non-essential functionality.", "is_distractor": False},
            {"id": "B", "text": "Every distributed service must guarantee 100% uptime for all endpoints without exception.", "is_distractor": True},
            {"id": "C", "text": "Circuit breakers cause more outages than they prevent by dropping traffic arbitrarily.", "is_distractor": True},
            {"id": "D", "text": "Saturated thread pools indicate that hardware resources should immediately be doubled.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The author concludes that 'survival under pathological conditions requires accepting imperfect service rather than chasing total availability.'",
        "distractor_explanations": {
            "B": "Contradicts the author's rejection of chasing total availability at the expense of resilience.",
            "C": "Contradicts the text: Circuit breakers are identified as protective resilience patterns.",
            "D": "Hardware scaling is not mentioned; the text focuses on architectural load shedding."
        },
        "a": 1.60,
        "b": 0.85,
        "point_biserial": 0.48
    },
    {
        "skill_code": "VRB_MAIN_IDEA",
        "stem": "Read the passage:\n\n*\"Cryptographic zero-knowledge proofs (ZKPs) resolve a foundational paradox of the digital information economy: how to verify authenticity without disclosing the underlying data. Whether proving account solvency without publishing balances or validating identity without exposing personal records, ZKPs replace trust in custodial intermediaries with mathematical certainty. In doing so, they lay the architectural bedrock for privacy-preserving verifiable computing.\"*\n\nThe primary function of this paragraph is to:",
        "options": [
            {"id": "A", "text": "Provide mathematical proofs for elliptical curve cryptography.", "is_distractor": True},
            {"id": "B", "text": "Explain the conceptual significance and practical value of zero-knowledge proofs.", "is_distractor": False},
            {"id": "C", "text": "Criticize custodial financial institutions for security failures.", "is_distractor": True},
            {"id": "D", "text": "Demonstrate the computation speed advantages of ZK-rollups.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The paragraph introduces zero-knowledge proofs, defines the fundamental paradox they resolve, and explains their value in establishing verifiable privacy.",
        "distractor_explanations": {
            "A": "No mathematical formulas or elliptic curve derivations are present.",
            "C": "The text focuses on ZKPs as an architectural paradigm rather than an attack on institutions.",
            "D": "Computation speed is not discussed; verification without disclosure is the subject."
        },
        "a": 1.55,
        "b": 1.15,
        "point_biserial": 0.47
    },
    {
        "skill_code": "VRB_MAIN_IDEA",
        "stem": "Read the passage:\n\n*\"The rapid rise of low-code and generative AI development tools does not presage the demise of software engineering; rather, it elevates the level of abstraction. Just as the transition from assembly language to high-level compilers eliminated tedious register allocation without diminishing the need for computer scientists, automated code synthesis shifts the engineer's role from mechanical syntax emission to rigorous system design, constraint specification, and verification.\"*\n\nWhich analogy best mirrors the author's perspective?",
        "options": [
            {"id": "A", "text": "Generative AI is to software engineering as calculators were to professional mathematicians.", "is_distractor": False},
            {"id": "B", "text": "Generative AI is to software engineering as automobiles were to horse-drawn carriages.", "is_distractor": True},
            {"id": "C", "text": "Generative AI is to software engineering as digital streaming was to physical film.", "is_distractor": True},
            {"id": "D", "text": "Generative AI is to software engineering as antibiotics were to infectious bacteria.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Calculators automated manual arithmetic while elevating mathematicians to higher-level theoretical problem solving, matching the author's argument that AI elevates engineers to higher abstraction levels.",
        "distractor_explanations": {
            "B": "Inapt analogy: Automobiles completely obsoleted horses, whereas the author argues engineering is NOT obsoleted.",
            "C": "Inapt analogy: Streaming completely replaced physical film, contradicting the retention of the core engineering role.",
            "D": "Inapt analogy: Antibiotics destroy bacteria; AI does not seek to eradicate software engineers."
        },
        "a": 1.65,
        "b": 1.45,
        "point_biserial": 0.49
    },
    {
        "skill_code": "VRB_MAIN_IDEA",
        "stem": "Read the passage:\n\n*\"Open-source software maintains the critical infrastructure of global digital commerce, yet its funding model remains chronically fragile. Massive corporations build multi-billion dollar platforms atop volunteer-maintained utility libraries without contributing back capital or engineering bandwidth. The tragedy of the digital commons persists because software consumes zero marginal cost to replicate, concealing the immense labor required to patch vulnerabilities, audit dependencies, and maintain backward compatibility.\"*\n\nWhat is the central problem highlighted by the author?",
        "options": [
            {"id": "A", "text": "Open-source software is intrinsically less secure than proprietary commercial software.", "is_distractor": True},
            {"id": "B", "text": "An asymmetric dependency where commercial enterprises extract value from under-resourced open-source infrastructure.", "is_distractor": False},
            {"id": "C", "text": "Software replication costs have increased dramatically due to cloud inflation.", "is_distractor": True},
            {"id": "D", "text": "Volunteers refuse to accept corporate funding due to ideological purity.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The text highlights the economic asymmetry between massive corporate beneficiaries and volunteer maintainers ('tragedy of the digital commons').",
        "distractor_explanations": {
            "A": "The author discusses economic fragility, not intrinsic inferiority of open-source software.",
            "C": "Contradicts the text: The author notes software has 'zero marginal cost to replicate'.",
            "D": "The text states corporations do not contribute capital, not that volunteers reject it."
        },
        "a": 1.70,
        "b": 1.70,
        "point_biserial": 0.52
    },

    # --- VRB_INFERENCE (7 items) ---
    {
        "skill_code": "VRB_INFERENCE",
        "stem": "Based on the statement below, what can be logically inferred?\n\n*\"All relational database transactions that execute under Serializable isolation are guaranteed to prevent phantom reads; however, system throughput drops by over 60% when write-heavy workloads induce lock contention.\"*\n\nWhich deduction must be true?",
        "options": [
            {"id": "A", "text": "A transaction with phantom reads was not executed under Serializable isolation.", "is_distractor": False},
            {"id": "B", "text": "Read-heavy workloads always experience a 60% throughput drop under Serializable isolation.", "is_distractor": True},
            {"id": "C", "text": "Phantom reads can never occur in non-relational document databases.", "is_distractor": True},
            {"id": "D", "text": "Serializable isolation eliminates all hardware contention.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "By modus tollens: If Serializable -> No phantom reads. Therefore, if phantom reads occur, the transaction was not under Serializable isolation.",
        "distractor_explanations": {
            "B": "The 60% drop is explicitly tied to 'write-heavy workloads', not read-heavy workloads.",
            "C": "Document databases are outside the domain of the premise.",
            "D": "Hardware contention is not eliminated; lock contention is explicitly mentioned."
        },
        "a": 1.45,
        "b": -0.70,
        "point_biserial": 0.43
    },
    {
        "skill_code": "VRB_INFERENCE",
        "stem": "Read the excerpt:\n\n*\"The incident post-mortem revealed that while the primary server farm had dual redundant power generators, the automated transfer switch controlling the fuel valves was powered exclusively by a single unprotected branch circuit. When the power grid dipped, the generators failed to ignite.\"*\n\nWhat underlying vulnerability does the author implicitly criticize?",
        "options": [
            {"id": "A", "text": "The insufficient wattage of modern diesel generators.", "is_distractor": True},
            {"id": "B", "text": "A hidden single point of failure invalidating the system's intended redundancy.", "is_distractor": False},
            {"id": "C", "text": "The excessive cost of municipal utility power contracts.", "is_distractor": True},
            {"id": "D", "text": "The lack of manual override training among facility staff.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The author points out that having redundant generators was useless because the single branch circuit controlling fuel was a hidden single point of failure (SPOF).",
        "distractor_explanations": {
            "A": "Wattage was not the issue; the generators failed to ignite because of fuel control circuit loss.",
            "C": "Utility pricing is irrelevant to the post-mortem engineering failure.",
            "D": "Manual override is not mentioned or implied as the root design flaw."
        },
        "a": 1.50,
        "b": -0.20,
        "point_biserial": 0.45
    },
    {
        "skill_code": "VRB_INFERENCE",
        "stem": "Read the statement:\n\n*\"The deployment failed because the new release relied on a non-backward-compatible database migration that ran concurrently with the existing v1.4 application instances. By the time v1.5 finished launching, v1.4 instances had crashed upon encountering unmapped schema columns.\"*\n\nWhich mitigation strategy is directly implied by this post-mortem finding?",
        "options": [
            {"id": "A", "text": "Database migrations should always be executed using a phased expand-and-contract pattern.", "is_distractor": False},
            {"id": "B", "text": "Database schemas should never be modified once deployed to production.", "is_distractor": True},
            {"id": "C", "text": "Application instances must be rewritten in an untyped language to ignore schema changes.", "is_distractor": True},
            {"id": "D", "text": "Database migrations should only be executed during daytime peak traffic hours.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The expand-and-contract pattern ensures database schema changes remain backward-compatible with active previous application versions during rolling deployments.",
        "distractor_explanations": {
            "B": "Freezing database schemas forever is impractical and prevents system evolution.",
            "C": "Untyped languages do not prevent runtime schema mismatch crashes.",
            "D": "Peak hour migrations increase blast radius, contrary to best practice."
        },
        "a": 1.60,
        "b": 0.35,
        "point_biserial": 0.47
    },
    {
        "skill_code": "VRB_INFERENCE",
        "stem": "Read the passage:\n\n*\"A study of 500 engineering organizations revealed that teams adopting static type systems experienced an initial 15% reduction in initial prototyping velocity. However, these same teams exhibited a 40% reduction in production hotfixes and spent 50% less engineering time on manual regression testing after the first six months of operation.\"*\n\nWhich conclusion is most strongly supported by the data?",
        "options": [
            {"id": "A", "text": "Static typing provides net long-term productivity and stability dividends despite front-loaded overhead.", "is_distractor": False},
            {"id": "B", "text": "Dynamic typing is objectively superior for maintaining mature enterprise systems.", "is_distractor": True},
            {"id": "C", "text": "Static type systems eliminate the necessity of automated unit testing.", "is_distractor": True},
            {"id": "D", "text": "Prototyping velocity is the only reliable predictor of startup longevity.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The initial cost (-15% speed) is outweighed over time by significant operational savings (-40% hotfixes, -50% regression debugging), proving net long-term dividends.",
        "distractor_explanations": {
            "B": "The data supports static typing for mature maintenance, contradicting option B.",
            "C": "The text mentions reduced manual regression testing, not the elimination of unit testing.",
            "D": "Prototyping velocity is not claimed to be the only predictor of longevity."
        },
        "a": 1.55,
        "b": 0.75,
        "point_biserial": 0.46
    },
    {
        "skill_code": "VRB_INFERENCE",
        "stem": "Read the statement:\n\n*\"Although company leadership asserted that productivity increased following the return-to-office mandate, voluntary resignations among senior staff surged by 35%, and the mean time to fill critical engineering vacancies doubled over the subsequent two quarters.\"*\n\nWhat can be reasonably inferred about the company's competitive talent positioning?",
        "options": [
            {"id": "A", "text": "The return-to-office policy had no measurable impact on human capital metrics.", "is_distractor": True},
            {"id": "B", "text": "The mandate degraded the firm's talent retention and recruiting efficiency in the senior engineering market.", "is_distractor": False},
            {"id": "C", "text": "Junior engineers were entirely unaffected by the policy changes.", "is_distractor": True},
            {"id": "D", "text": "Productivity gains will permanently compensate for the loss of institutional memory.", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Surging senior resignations (+35%) and doubled vacancy fill times directly reflect impaired retention and reduced attractiveness to senior engineering talent.",
        "distractor_explanations": {
            "A": "Directly contradicts the significant statistical changes reported.",
            "C": "The text provides no data about junior engineers, making this an unsubstantiated leap.",
            "D": "The text makes no projection regarding whether productivity compensates for losses."
        },
        "a": 1.65,
        "b": 1.10,
        "point_biserial": 0.48
    },
    {
        "skill_code": "VRB_INFERENCE",
        "stem": "Read the following observation:\n\n*\"When web server response times degraded from 200ms to 2.1 seconds, user bounce rates increased by 110%, while completed shopping cart checkout conversions plunged by 38%. Even after latency was restored to 200ms, conversion rates required three weeks to return to pre-incident baselines.\"*\n\nWhat does the persistent conversion lag imply about consumer psychology?",
        "options": [
            {"id": "A", "text": "Users perceive latency degradation instantly, but rebuilding user trust and behavioral momentum exhibits hysteresis.", "is_distractor": False},
            {"id": "B", "text": "Network latency has no direct correlation with commercial transaction volume.", "is_distractor": True},
            {"id": "C", "text": "A 2.1-second latency is considered optimal for e-commerce checkout funnels.", "is_distractor": True},
            {"id": "D", "text": "Users prefer slower web applications because it allows more time to deliberate purchasing decisions.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The delayed recovery ('three weeks to return to baseline' after instantaneous latency repair) exhibits hysteresis—a lag in effect behind change of input caused by damaged trust.",
        "distractor_explanations": {
            "B": "Directly contradicted by the -38% conversion plunge.",
            "C": "Contradicted by the severe bounce rate spike.",
            "D": "Absurd conclusion directly contradicted by the empirical data."
        },
        "a": 1.70,
        "b": 1.50,
        "point_biserial": 0.50
    },
    {
        "skill_code": "VRB_INFERENCE",
        "stem": "Read the passage:\n\n*\"In high-frequency trading networks, routing packets across microwave links rather than fiber-optic cables reduces transit latency between Chicago and New York by approximately 3 milliseconds. However, microwave signals suffer significant packet loss and attenuation during heavy rainfall, necessitating dynamic failover to fiber lines during adverse weather.\"*\n\nWhat tradeoff governs communication medium selection in this context?",
        "options": [
            {"id": "A", "text": "Microwave links offer latency advantages in clear atmospheric conditions at the cost of environmental volatility.", "is_distractor": False},
            {"id": "B", "text": "Fiber-optic cables are fundamentally unsuited for high-throughput financial telecommunications.", "is_distractor": True},
            {"id": "C", "text": "Trading algorithms prioritize zero cost over latency optimization.", "is_distractor": True},
            {"id": "D", "text": "Rainfall accelerates microwave signal velocity through atmospheric refraction.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The text explicitly contrasts the 3ms speed advantage of microwaves against their vulnerability to rainfall-induced attenuation.",
        "distractor_explanations": {
            "B": "Fiber-optic cables serve as the essential reliable failover substrate.",
            "C": "Cost is not discussed; sub-millisecond latency is the governing priority.",
            "D": "Rainfall causes attenuation and packet loss, not acceleration."
        },
        "a": 1.75,
        "b": 1.75,
        "point_biserial": 0.52
    }
]
