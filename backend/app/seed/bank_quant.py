"""
Quantitative Aptitude Question Bank.
Topic 1: Arithmetic & Percentages (15 questions across QNT_NUMBERS, QNT_PERCENTAGES, QNT_RATIO_PROP, QNT_TIME_WORK)
Topic 2: Combinatorics & Probability (15 questions across QNT_PERMUTATIONS, QNT_PROBABILITY)
"""

QUANT_ITEMS = [
    # =========================================================================
    # TOPIC 1: Arithmetic & Percentages (15 items)
    # =========================================================================
    # --- QNT_NUMBERS (4 items) ---
    {
        "skill_code": "QNT_NUMBERS",
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
        "skill_code": "QNT_NUMBERS",
        "stem": "How many trailing zeros are in the decimal representation of $100!$ (100 factorial)?",
        "options": [
            {"id": "A", "text": "20", "is_distractor": True},
            {"id": "B", "text": "24", "is_distractor": False},
            {"id": "C", "text": "25", "is_distractor": True},
            {"id": "D", "text": "28", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Trailing zeros are formed by factors of 10 = 2 * 5. Using Legendre's formula for the prime 5: $\\lfloor 100/5 \\rfloor + \\lfloor 100/25 \\rfloor + \\lfloor 100/125 \\rfloor = 20 + 4 + 0 = 24$.",
        "distractor_explanations": {
            "A": "Error: Computed only $\\lfloor 100/5 \\rfloor = 20$, omitting higher powers of 5 ($5^2 = 25$).",
            "C": "Error: Counted $\\lfloor 100/4 \\rfloor$ instead.",
            "D": "Error: Arithmetic compounding error."
        },
        "a": 1.50,
        "b": -0.80,
        "point_biserial": 0.44
    },
    {
        "skill_code": "QNT_NUMBERS",
        "stem": "Find the greatest common divisor (GCD) of 468 and 324 using the Euclidean algorithm.",
        "options": [
            {"id": "A", "text": "18", "is_distractor": True},
            {"id": "B", "text": "36", "is_distractor": False},
            {"id": "C", "text": "72", "is_distractor": True},
            {"id": "D", "text": "12", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Euclidean algorithm: $468 = 1 \\times 324 + 144$. $324 = 2 \\times 144 + 36$. $144 = 4 \\times 36 + 0$. The last non-zero remainder is 36.",
        "distractor_explanations": {
            "A": "Error: 18 is a common divisor, but not the greatest common divisor ($18 \\times 2 = 36$).",
            "C": "Error: 72 divides 144 but does not divide 324 ($324 / 72 = 4.5$).",
            "D": "Error: 12 is a smaller common divisor."
        },
        "a": 1.35,
        "b": -1.40,
        "point_biserial": 0.41
    },
    {
        "skill_code": "QNT_NUMBERS",
        "stem": "What is the unit digit of $7^{95} - 3^{58}$?",
        "options": [
            {"id": "A", "text": "0", "is_distractor": True},
            {"id": "B", "text": "4", "is_distractor": False},
            {"id": "C", "text": "6", "is_distractor": True},
            {"id": "D", "text": "8", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Cyclicity of powers of 7 has period 4: $7^1=7, 7^2=9, 7^3=3, 7^4=1$. $95 = 4 \\times 23 + 3 \\implies 7^{95}$ ends in 3. Cyclicity of 3 has period 4: $3^1=3, 3^2=9, 3^3=7, 3^4=1$. $58 = 4 \\times 14 + 2 \\implies 3^{58}$ ends in 9. $(...3) - (...9) = 13 - 9 = 4$.",
        "distractor_explanations": {
            "A": "Error: Assumed $95 - 58 = 37$ directly without evaluating modular cyclicity of bases.",
            "C": "Error: Subtracted $9 - 3 = 6$ in the reverse direction.",
            "D": "Error: Arithmetic borrow calculation mistake."
        },
        "a": 1.65,
        "b": 1.10,
        "point_biserial": 0.48
    },

    # --- QNT_PERCENTAGES (4 items) ---
    {
        "skill_code": "QNT_PERCENTAGES",
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
    {
        "skill_code": "QNT_PERCENTAGES",
        "stem": "If the price of commodity X increases by 25%, by what percentage must a household reduce its consumption so that the total expenditure remains unchanged?",
        "options": [
            {"id": "A", "text": "25%", "is_distractor": True},
            {"id": "B", "text": "20%", "is_distractor": False},
            {"id": "C", "text": "16.67%", "is_distractor": True},
            {"id": "D", "text": "22.5%", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Expenditure = Price * Consumption. If price becomes $1.25 = 5/4$, consumption must become $4/5 = 0.80$ to keep expenditure at 1.0. Reduction = $1 - 0.80 = 20\\%$. Formula: $\\frac{r}{100 + r} \\times 100 = \\frac{25}{125} \\times 100 = 20\\%$.",
        "distractor_explanations": {
            "A": "Error: Believed reduction percentage equals price increase percentage.",
            "C": "Error: Applied $r / (100 - r)$ formula incorrectly.",
            "D": "Error: Linear interpolation guess."
        },
        "a": 1.45,
        "b": -1.10,
        "point_biserial": 0.43
    },
    {
        "skill_code": "QNT_PERCENTAGES",
        "stem": "A merchant marks an item 40% above its cost price and offers a cash discount of 15%. What is the merchant's net profit percentage?",
        "options": [
            {"id": "A", "text": "25%", "is_distractor": True},
            {"id": "B", "text": "19%", "is_distractor": False},
            {"id": "C", "text": "21%", "is_distractor": True},
            {"id": "D", "text": "28%", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Let CP = 100. Marked Price (MP) = 140. Selling Price (SP) = $140 \\times (1 - 0.15) = 140 \\times 0.85 = 119$. Net profit = $119 - 100 = 19\\%$.",
        "distractor_explanations": {
            "A": "Error: Subtracted percentages directly: $40\\% - 15\\% = 25\\%$.",
            "C": "Error: Arithmetic error in calculating 15% of 140 as 19 instead of 21.",
            "D": "Error: Computed profit based on MP rather than CP."
        },
        "a": 1.50,
        "b": 0.20,
        "point_biserial": 0.45
    },
    {
        "skill_code": "QNT_PERCENTAGES",
        "stem": "In an engineering college, 60% of students passed Computer Science, 50% passed Mathematics, and 30% passed both. What percentage of students failed in both subjects?",
        "options": [
            {"id": "A", "text": "10%", "is_distractor": True},
            {"id": "B", "text": "20%", "is_distractor": False},
            {"id": "C", "text": "30%", "is_distractor": True},
            {"id": "D", "text": "15%", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Principle of Inclusion-Exclusion: $P(CS \\cup Math) = P(CS) + P(Math) - P(CS \\cap Math) = 60\\% + 50\\% - 30\\% = 80\\%$. Students who failed both = $100\\% - 80\\% = 20\\%$.",
        "distractor_explanations": {
            "A": "Error: Forgot to subtract intersection: $100 - (60 + 50 - 20)$.",
            "C": "Error: Confused failed percentage with the intersection percentage (30%).",
            "D": "Error: Calculation estimate mistake."
        },
        "a": 1.55,
        "b": 0.80,
        "point_biserial": 0.46
    },

    # --- QNT_RATIO_PROP (4 items) ---
    {
        "skill_code": "QNT_RATIO_PROP",
        "stem": "If $A : B = 3 : 4$ and $B : C = 8 : 9$, what is the compounded ratio $A : B : C$?",
        "options": [
            {"id": "A", "text": "3 : 8 : 9", "is_distractor": True},
            {"id": "B", "text": "6 : 8 : 9", "is_distractor": False},
            {"id": "C", "text": "3 : 4 : 9", "is_distractor": True},
            {"id": "D", "text": "6 : 8 : 12", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Equate the common term B: $A : B = (3 \\times 2) : (4 \\times 2) = 6 : 8$. Since $B : C = 8 : 9$, the combined ratio is $6 : 8 : 9$.",
        "distractor_explanations": {
            "A": "Error: Replaced B without scaling A.",
            "C": "Error: Juxtaposed ratios without equalizing the bridge term B.",
            "D": "Error: Scaled C incorrectly."
        },
        "a": 1.25,
        "b": -1.30,
        "point_biserial": 0.40
    },
    {
        "skill_code": "QNT_RATIO_PROP",
        "stem": "A mixture of 60 liters contains milk and water in the ratio 2 : 1. How much water must be added to make the ratio of milk to water 1 : 2?",
        "options": [
            {"id": "A", "text": "40 liters", "is_distractor": True},
            {"id": "B", "text": "60 liters", "is_distractor": False},
            {"id": "C", "text": "80 liters", "is_distractor": True},
            {"id": "D", "text": "50 liters", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Initial quantities: Milk = $60 \\times (2/3) = 40$ L, Water = $60 \\times (1/3) = 20$ L. Let $w$ liters of water be added. New ratio: $\\frac{40}{20 + w} = \\frac{1}{2} \\implies 20 + w = 80 \\implies w = 60$ liters.",
        "distractor_explanations": {
            "A": "Error: Solved for initial milk volume instead of added water.",
            "C": "Error: Solved for total new water volume (80 L) instead of added water ($80 - 20 = 60$ L).",
            "D": "Error: Arithmetic error."
        },
        "a": 1.45,
        "b": -0.20,
        "point_biserial": 0.44
    },
    {
        "skill_code": "QNT_RATIO_PROP",
        "stem": "Two numbers are in the ratio 5 : 7. If 6 is subtracted from each, the resulting ratio is 2 : 3. What is the difference between the two original numbers?",
        "options": [
            {"id": "A", "text": "10", "is_distractor": True},
            {"id": "B", "text": "12", "is_distractor": False},
            {"id": "C", "text": "14", "is_distractor": True},
            {"id": "D", "text": "18", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Let numbers be $5x$ and $7x$. $\\frac{5x - 6}{7x - 6} = \\frac{2}{3} \\implies 3(5x - 6) = 2(7x - 6) \\implies 15x - 18 = 14x - 12 \\implies x = 6$. The numbers are 30 and 42. Difference = $42 - 30 = 12$.",
        "distractor_explanations": {
            "A": "Error: Multiplied $x$ by $(7 - 5) - 2$.",
            "C": "Error: Arithmetic error in cross-multiplication.",
            "D": "Error: Computed $3x = 18$ instead of $2x = 12$."
        },
        "a": 1.55,
        "b": 0.50,
        "point_biserial": 0.47
    },
    {
        "skill_code": "QNT_RATIO_PROP",
        "stem": "The salaries of A, B, and C are in the ratio 2 : 3 : 5. If increments of 15%, 10%, and 20% are granted respectively, what is the new ratio of their salaries?",
        "options": [
            {"id": "A", "text": "23 : 33 : 60", "is_distractor": False},
            {"id": "B", "text": "25 : 35 : 65", "is_distractor": True},
            {"id": "C", "text": "23 : 30 : 50", "is_distractor": True},
            {"id": "D", "text": "21 : 33 : 60", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Let salaries be 200, 300, and 500. New A = $200 \\times 1.15 = 230$. New B = $300 \\times 1.10 = 330$. New C = $500 \\times 1.20 = 600$. Ratio = 230 : 330 : 600 = 23 : 33 : 60.",
        "distractor_explanations": {
            "B": "Error: Added percentages directly as integers to the base numbers.",
            "C": "Error: Failed to apply increment to C.",
            "D": "Error: Calculation error on A ($200 \\times 1.15 \\neq 210$)."
        },
        "a": 1.60,
        "b": 1.25,
        "point_biserial": 0.49
    },

    # --- QNT_TIME_WORK (3 items) ---
    {
        "skill_code": "QNT_TIME_WORK",
        "stem": "Worker A can complete a software module in 12 days, and Worker B can complete it in 18 days. If they collaborate, how many days will it take them to finish the module?",
        "options": [
            {"id": "A", "text": "7.5 days", "is_distractor": True},
            {"id": "B", "text": "7.2 days", "is_distractor": False},
            {"id": "C", "text": "6.8 days", "is_distractor": True},
            {"id": "D", "text": "8.0 days", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Work rate: $A = 1/12$, $B = 1/18$. Combined rate = $\\frac{1}{12} + \\frac{1}{18} = \\frac{3 + 2}{36} = \\frac{5}{36}$ module/day. Time required = $\\frac{36}{5} = 7.2$ days.",
        "distractor_explanations": {
            "A": "Error: Took simple average of 12 and 18 ($30 / 4 = 7.5$) or incorrect harmonic mean.",
            "C": "Error: Approximation error.",
            "D": "Error: Subtraction error."
        },
        "a": 1.35,
        "b": -0.90,
        "point_biserial": 0.42
    },
    {
        "skill_code": "QNT_TIME_WORK",
        "stem": "A train running at 72 km/h crosses a 180-meter long platform in 18 seconds. What is the length of the train?",
        "options": [
            {"id": "A", "text": "160 meters", "is_distractor": True},
            {"id": "B", "text": "180 meters", "is_distractor": False},
            {"id": "C", "text": "200 meters", "is_distractor": True},
            {"id": "D", "text": "220 meters", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Speed in m/s = $72 \\times \\frac{5}{18} = 20$ m/s. Total distance in 18s = $20 \\times 18 = 360$ meters. Total distance = Length(train) + Length(platform). Length(train) = $360 - 180 = 180$ meters.",
        "distractor_explanations": {
            "A": "Error: Used speed of 18 m/s instead of 20 m/s.",
            "C": "Error: Subtracted 160 from 360.",
            "D": "Error: Conversion factor error (used 18/5 instead of 5/18)."
        },
        "a": 1.45,
        "b": 0.10,
        "point_biserial": 0.45
    },
    {
        "skill_code": "QNT_TIME_WORK",
        "stem": "Pipe A can fill a tank in 8 hours, and Pipe B can empty it in 12 hours. If both pipes are opened simultaneously when the tank is empty, how long will it take to fill the tank?",
        "options": [
            {"id": "A", "text": "20 hours", "is_distractor": True},
            {"id": "B", "text": "24 hours", "is_distractor": False},
            {"id": "C", "text": "18 hours", "is_distractor": True},
            {"id": "D", "text": "16 hours", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Net filling rate per hour = $\\frac{1}{8} - \\frac{1}{12} = \\frac{3 - 2}{24} = \\frac{1}{24}$. Time to fill the entire tank = 24 hours.",
        "distractor_explanations": {
            "A": "Error: Added times or rates incorrectly.",
            "C": "Error: Arithmetic error in finding LCM of 8 and 12.",
            "D": "Error: Subtracted times directly: $12 - 8 = 4$, then multiplied by 4."
        },
        "a": 1.50,
        "b": 0.70,
        "point_biserial": 0.46
    },

    # =========================================================================
    # TOPIC 2: Combinatorics & Probability (15 items)
    # =========================================================================
    # --- QNT_PERMUTATIONS (8 items) ---
    {
        "skill_code": "QNT_PERMUTATIONS",
        "stem": "In how many distinct ways can the letters of the word **\"DATABASE\"** be arranged?",
        "options": [
            {"id": "A", "text": "40,320", "is_distractor": True},
            {"id": "B", "text": "6,720", "is_distractor": False},
            {"id": "C", "text": "13,440", "is_distractor": True},
            {"id": "D", "text": "20,160", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Total letters = 8. Frequencies: A appears 3 times, D, T, B, S, E each appear 1 time. Distinct permutations = $\\frac{8!}{3!} = \\frac{40320}{6} = 6720$.",
        "distractor_explanations": {
            "A": "Error: Computed $8! = 40320$ without dividing by $3!$ for the repeated letter 'A'.",
            "C": "Error: Divided by $3$ instead of $3! = 6$ ($40320 / 3 = 13440$).",
            "D": "Error: Divided by $2!$ instead of $3!$."
        },
        "a": 1.45,
        "b": -0.60,
        "point_biserial": 0.43
    },
    {
        "skill_code": "QNT_PERMUTATIONS",
        "stem": "A software team consists of 6 backend engineers and 4 frontend engineers. In how many ways can a committee of 5 members be chosen such that it contains exactly 3 backend and 2 frontend engineers?",
        "options": [
            {"id": "A", "text": "120", "is_distractor": False},
            {"id": "B", "text": "252", "is_distractor": True},
            {"id": "C", "text": "60", "is_distractor": True},
            {"id": "D", "text": "144", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Ways to choose 3 backend engineers from 6 = $\\binom{6}{3} = \\frac{6 \\times 5 \\times 4}{6} = 20$. Ways to choose 2 frontend engineers from 4 = $\\binom{4}{2} = \\frac{4 \\times 3}{2} = 6$. Total ways = $20 \\times 6 = 120$.",
        "distractor_explanations": {
            "B": "Error: Computed unconstrained $\\binom{10}{5} = 252$.",
            "C": "Error: Added combinations instead of multiplying ($20 + 6 = 26$) or divided by 2.",
            "D": "Error: Permutations used instead of combinations."
        },
        "a": 1.50,
        "b": -0.15,
        "point_biserial": 0.45
    },
    {
        "skill_code": "QNT_PERMUTATIONS",
        "stem": "In how many ways can 6 microservices developers be seated around a circular conference table?",
        "options": [
            {"id": "A", "text": "720", "is_distractor": True},
            {"id": "B", "text": "120", "is_distractor": False},
            {"id": "C", "text": "24", "is_distractor": True},
            {"id": "D", "text": "360", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Circular permutation of $n$ distinct items is given by $(n - 1)!$. For 6 people: $(6 - 1)! = 5! = 120$.",
        "distractor_explanations": {
            "A": "Error: Computed linear permutation $6! = 720$.",
            "C": "Error: Computed $(6 - 2)! = 4! = 24$.",
            "D": "Error: Divided $6!$ by 2 instead of 6."
        },
        "a": 1.35,
        "b": -1.10,
        "point_biserial": 0.42
    },
    {
        "skill_code": "QNT_PERMUTATIONS",
        "stem": "How many 4-digit PIN numbers can be formed using digits 0–9 if repetition of digits is strictly prohibited and the PIN cannot start with 0?",
        "options": [
            {"id": "A", "text": "5,040", "is_distractor": True},
            {"id": "B", "text": "4,536", "is_distractor": False},
            {"id": "C", "text": "9,000", "is_distractor": True},
            {"id": "D", "text": "3,024", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "First digit choices (1–9): 9 choices. Second digit (0–9 except first): 9 choices. Third digit: 8 choices. Fourth digit: 7 choices. Total PINs = $9 \\times 9 \\times 8 \\times 7 = 4536$.",
        "distractor_explanations": {
            "A": "Error: Allowed 0 as the leading digit ($10 \\times 9 \\times 8 \\times 7 = 5040$).",
            "C": "Error: Assumed replacement/repetition allowed ($9 \\times 10^3 = 9000$).",
            "D": "Error: Subtracted choices prematurely ($9 \\times 8 \\times 7 \\times 6 = 3024$)."
        },
        "a": 1.55,
        "b": 0.45,
        "point_biserial": 0.47
    },
    {
        "skill_code": "QNT_PERMUTATIONS",
        "stem": "In how many ways can 8 books be arranged on a shelf such that two specific computer science textbooks are always adjacent?",
        "options": [
            {"id": "A", "text": "40,320", "is_distractor": True},
            {"id": "B", "text": "10,080", "is_distractor": False},
            {"id": "C", "text": "5,040", "is_distractor": True},
            {"id": "D", "text": "20,160", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Tie the two specific books into a single super-item. Now there are 7 items to arrange: $7! = 5040$. The two books within the bundle can be arranged in $2! = 2$ ways. Total = $7! \\times 2! = 5040 \\times 2 = 10080$.",
        "distractor_explanations": {
            "A": "Error: Computed $8! = 40320$ without the adjacency constraint.",
            "C": "Error: Forgot to multiply by $2!$ for internal ordering of the two books.",
            "D": "Error: Multiplied by 4 instead of 2."
        },
        "a": 1.60,
        "b": 0.90,
        "point_biserial": 0.48
    },
    {
        "skill_code": "QNT_PERMUTATIONS",
        "stem": "How many diagonals can be drawn in a regular decagon (10-sided polygon)?",
        "options": [
            {"id": "A", "text": "45", "is_distractor": True},
            {"id": "B", "text": "35", "is_distractor": False},
            {"id": "C", "text": "40", "is_distractor": True},
            {"id": "D", "text": "25", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Total line segments connecting 10 vertices = $\\binom{10}{2} = \\frac{10 \\times 9}{2} = 45$. Of these, 10 are the polygon's sides. Diagonals = $\\binom{n}{2} - n = 45 - 10 = 35$ (or $\\frac{n(n - 3)}{2} = \\frac{10 \\times 7}{2} = 35$).",
        "distractor_explanations": {
            "A": "Error: Counted total line segments $\\binom{10}{2} = 45$, forgetting to subtract the 10 outer sides.",
            "C": "Error: Subtracted 5 instead of 10.",
            "D": "Error: Applied formula incorrectly."
        },
        "a": 1.50,
        "b": 0.25,
        "point_biserial": 0.46
    },
    {
        "skill_code": "QNT_PERMUTATIONS",
        "stem": "In how many ways can 12 identical resource tokens be distributed among 3 distinct cluster worker nodes such that each worker node receives at least 1 token?",
        "options": [
            {"id": "A", "text": "55", "is_distractor": False},
            {"id": "B", "text": "66", "is_distractor": True},
            {"id": "C", "text": "78", "is_distractor": True},
            {"id": "D", "text": "91", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Using Stars and Bars with positive integer solutions: number of solutions to $x_1 + x_2 + x_3 = 12$ where $x_i \\ge 1$ is $\\binom{n - 1}{k - 1} = \\binom{12 - 1}{3 - 1} = \\binom{11}{2} = \\frac{11 \\times 10}{2} = 55$.",
        "distractor_explanations": {
            "B": "Error: Computed non-negative solutions $\\binom{12 + 3 - 1}{3 - 1} = \\binom{14}{2} = 91$ or arithmetic mistake.",
            "C": "Error: Evaluated $\\binom{13}{2} = 78$.",
            "D": "Error: Evaluated unconstrained Stars and Bars for non-negative integers $\\binom{14}{2} = 91$."
        },
        "a": 1.65,
        "b": 1.35,
        "point_biserial": 0.50
    },
    {
        "skill_code": "QNT_PERMUTATIONS",
        "stem": "How many ways can 5 identical red balls and 3 identical blue balls be arranged in a line such that no two blue balls are adjacent?",
        "options": [
            {"id": "A", "text": "20", "is_distractor": False},
            {"id": "B", "text": "56", "is_distractor": True},
            {"id": "C", "text": "35", "is_distractor": True},
            {"id": "D", "text": "15", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Arrange the 5 identical red balls in a row: 1 way. This creates 6 available gaps (including ends): _ R _ R _ R _ R _ R _. To ensure no two blue balls are adjacent, place the 3 blue balls into 3 of the 6 gaps: $\\binom{6}{3} = \\frac{6 \\times 5 \\times 4}{6} = 20$.",
        "distractor_explanations": {
            "B": "Error: Computed total unconstrained arrangements $\\binom{8}{3} = 56$.",
            "C": "Error: Evaluated $\\binom{7}{3} = 35$ with 7 gaps instead of 6.",
            "D": "Error: Evaluated $\\binom{6}{2} = 15$."
        },
        "a": 1.70,
        "b": 1.65,
        "point_biserial": 0.52
    },

    # --- QNT_PROBABILITY (7 items) ---
    {
        "skill_code": "QNT_PROBABILITY",
        "stem": "Two fair six-sided dice are rolled simultaneously. What is the probability that the sum of the numbers is greater than 9?",
        "options": [
            {"id": "A", "text": "1/6", "is_distractor": False},
            {"id": "B", "text": "5/36", "is_distractor": True},
            {"id": "C", "text": "1/4", "is_distractor": True},
            {"id": "D", "text": "7/36", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Total outcomes = 36. Outcomes with sum > 9 (sums 10, 11, 12): Sum 10: (4,6), (5,5), (6,4) -> 3. Sum 11: (5,6), (6,5) -> 2. Sum 12: (6,6) -> 1. Total favorable = $3 + 2 + 1 = 6$. Probability = $6/36 = 1/6$.",
        "distractor_explanations": {
            "B": "Error: Missed one combination (computed 5 favorable outcomes).",
            "C": "Error: Computed sum $\\ge 9$ (which has 10 outcomes: 10/36).",
            "D": "Error: Arithmetic miscount."
        },
        "a": 1.35,
        "b": -0.85,
        "point_biserial": 0.41
    },
    {
        "skill_code": "QNT_PROBABILITY",
        "stem": "An algorithm has an independent 90% probability of passing any single test case. What is the probability that it passes at least one test case out of three independent runs?",
        "options": [
            {"id": "A", "text": "0.999", "is_distractor": False},
            {"id": "B", "text": "0.729", "is_distractor": True},
            {"id": "C", "text": "0.970", "is_distractor": True},
            {"id": "D", "text": "0.900", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Use complementary probability: $P(\\text{at least 1 pass}) = 1 - P(\\text{all fail})$. Failure probability per run = $1 - 0.90 = 0.10$. $P(\\text{all 3 fail}) = 0.10^3 = 0.001$. Probability = $1 - 0.001 = 0.999$.",
        "distractor_explanations": {
            "B": "Error: Calculated probability of passing ALL three test cases ($0.9^3 = 0.729$).",
            "C": "Error: Approximation error.",
            "D": "Error: Assumed probability remains 0.90 regardless of sample size."
        },
        "a": 1.45,
        "b": -0.40,
        "point_biserial": 0.44
    },
    {
        "skill_code": "QNT_PROBABILITY",
        "stem": "A box contains 5 red balls and 3 green balls. Two balls are drawn successively without replacement. What is the probability that both balls are green?",
        "options": [
            {"id": "A", "text": "3/28", "is_distractor": False},
            {"id": "B", "text": "9/64", "is_distractor": True},
            {"id": "C", "text": "3/14", "is_distractor": True},
            {"id": "D", "text": "1/8", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Total balls = 8. $P(\\text{first green}) = 3/8$. Since drawing is without replacement, 7 balls remain (2 green). $P(\\text{second green | first green}) = 2/7$. $P(\\text{both green}) = \\frac{3}{8} \\times \\frac{2}{7} = \\frac{6}{56} = \\frac{3}{28}$.",
        "distractor_explanations": {
            "B": "Error: Assumed drawing WITH replacement: $(3/8) \\times (3/8) = 9/64$.",
            "C": "Error: Computed $(3/8) + (2/7)$ or dropped a factor of 2.",
            "D": "Error: Calculation fraction error."
        },
        "a": 1.50,
        "b": 0.10,
        "point_biserial": 0.45
    },
    {
        "skill_code": "QNT_PROBABILITY",
        "stem": "A medical diagnostic test for a rare server vulnerability has a 99% true positive rate (sensitivity) and a 5% false positive rate. If only 0.1% of servers are infected, what is the posterior probability that a server flagged positive actually has the vulnerability? (Bayes' Theorem)",
        "options": [
            {"id": "A", "text": "Approximately 1.94%", "is_distractor": False},
            {"id": "B", "text": "Approximately 95.0%", "is_distractor": True},
            {"id": "C", "text": "Approximately 50.0%", "is_distractor": True},
            {"id": "D", "text": "Approximately 9.90%", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Bayes' Theorem: $P(I|+) = \\frac{P(+|I)P(I)}{P(+|I)P(I) + P(+|\\neg I)P(\\neg I)} = \\frac{0.99 \\times 0.001}{(0.99 \\times 0.001) + (0.05 \\times 0.999)} = \\frac{0.00099}{0.00099 + 0.04995} = \\frac{0.00099}{0.05094} \\approx 0.01943$ (1.94%).",
        "distractor_explanations": {
            "B": "Base-rate fallacy: Confusing test sensitivity/specificity with posterior probability ($1 - 0.05 = 95\\%$).",
            "C": "Intuitive guess assuming equal balance between false positives and infected cases.",
            "D": "Arithmetic error omitting the dominant uninfected population weight."
        },
        "a": 1.70,
        "b": 1.20,
        "point_biserial": 0.50
    },
    {
        "skill_code": "QNT_PROBABILITY",
        "stem": "A card is drawn from a standard deck of 52 playing cards. What is the probability that the card is either a King or a Heart?",
        "options": [
            {"id": "A", "text": "4/13", "is_distractor": False},
            {"id": "B", "text": "17/52", "is_distractor": True},
            {"id": "C", "text": "1/2", "is_distractor": True},
            {"id": "D", "text": "9/26", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "$P(K \\cup H) = P(K) + P(H) - P(K \\cap H) = \\frac{4}{52} + \\frac{13}{52} - \\frac{1}{52} = \\frac{16}{52} = \\frac{4}{13}$.",
        "distractor_explanations": {
            "B": "Error: Forgot to subtract the King of Hearts ($4 + 13 = 17/52$).",
            "C": "Error: Guessed 50%.",
            "D": "Error: Arithmetic error ($18/52 = 9/26$)."
        },
        "a": 1.40,
        "b": -0.55,
        "point_biserial": 0.43
    },
    {
        "skill_code": "QNT_PROBABILITY",
        "stem": "Three machines A, B, and C produce 50%, 30%, and 20% of the total output in a chip fabrication plant. Defective rates are 3%, 4%, and 5% respectively. If a randomly inspected chip is defective, what is the probability it came from machine A?",
        "options": [
            {"id": "A", "text": "15/37", "is_distractor": False},
            {"id": "B", "text": "1/2", "is_distractor": True},
            {"id": "C", "text": "12/37", "is_distractor": True},
            {"id": "D", "text": "10/37", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "$P(D) = (0.50)(0.03) + (0.30)(0.04) + (0.20)(0.05) = 0.015 + 0.012 + 0.010 = 0.037$. By Bayes' Rule: $P(A|D) = \\frac{P(D|A)P(A)}{P(D)} = \\frac{0.015}{0.037} = \\frac{15}{37}$.",
        "distractor_explanations": {
            "B": "Error: Assumed machine A produces 50% so posterior is 50%.",
            "C": "Error: Computed probability for machine B ($12/37$).",
            "D": "Error: Computed probability for machine C ($10/37$)."
        },
        "a": 1.65,
        "b": 1.40,
        "point_biserial": 0.49
    },
    {
        "skill_code": "QNT_PROBABILITY",
        "stem": "Let $X$ be a continuous random variable uniformly distributed on the interval $[0, 10]$. What is the conditional probability $P(X > 7 \\mid X > 4)$?",
        "options": [
            {"id": "A", "text": "1/2", "is_distractor": False},
            {"id": "B", "text": "3/10", "is_distractor": True},
            {"id": "C", "text": "3/7", "is_distractor": True},
            {"id": "D", "text": "2/5", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Conditioning on $X > 4$, the support reduces to $[4, 10]$ of length $10 - 4 = 6$. The sub-interval $X > 7$ is $[7, 10]$ of length $10 - 7 = 3$. $P(X > 7 \\mid X > 4) = \\frac{3}{6} = \\frac{1}{2}$.",
        "distractor_explanations": {
            "B": "Error: Computed unconditional probability $P(X > 7) = 3/10$.",
            "C": "Error: Normalized by 7 instead of the conditioning interval length 6.",
            "D": "Error: Arithmetic error."
        },
        "a": 1.60,
        "b": 0.75,
        "point_biserial": 0.48
    }
]
