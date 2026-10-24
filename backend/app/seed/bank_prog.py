"""
Programming Fundamentals Question Bank.
Topic 1: Syntax & Control Flow (15 questions across PRG_VARIABLES, PRG_CONDITIONALS, PRG_LOOPS)
Topic 2: Functions & Memory (15 questions across PRG_FUNCTIONS, PRG_RECURSION, PRG_POINTERS)
"""

PROG_ITEMS = [
    # =========================================================================
    # TOPIC 1: Syntax & Control Flow (15 items)
    # =========================================================================
    # --- PRG_VARIABLES (5 items) ---
    {
        "skill_code": "PRG_VARIABLES",
        "stem": "In Python, what is the output of the following snippet?\n\n```python\na = [1, 2, 3]\nb = a\nb.append(4)\nprint(len(a))\n```",
        "options": [
            {"id": "A", "text": "3", "is_distractor": True},
            {"id": "B", "text": "4", "is_distractor": False},
            {"id": "C", "text": "None", "is_distractor": True},
            {"id": "D", "text": "Raises an AttributeError", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "In Python, assigning `b = a` creates a reference to the existing mutable list object in memory, not a copy. Mutating `b` via `append()` mutates the same object referenced by `a`. Hence `len(a)` is 4.",
        "distractor_explanations": {
            "A": "Misconception: Assuming variable assignment performs a deep or shallow copy.",
            "C": "Error: `append()` returns `None`, but `len(a)` evaluates to an integer.",
            "D": "Error: `append()` is a valid list method."
        },
        "a": 1.25,
        "b": -0.75,
        "point_biserial": 0.42
    },
    {
        "skill_code": "PRG_VARIABLES",
        "stem": "In Python, what will the expression `bool([]) == bool([False])` evaluate to?",
        "options": [
            {"id": "A", "text": "True", "is_distractor": True},
            {"id": "B", "text": "False", "is_distractor": False},
            {"id": "C", "text": "Raises a TypeError", "is_distractor": True},
            {"id": "D", "text": "None", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "An empty list `[]` evaluates to `False` in boolean context (`bool([]) == False`). A non-empty list `[False]` has length 1, so it evaluates to `True` (`bool([False]) == True`). Therefore, `False == True` evaluates to `False`.",
        "distractor_explanations": {
            "A": "Common misconception: Assuming `[False]` evaluates to `False` because its sole element is `False`.",
            "C": "Equality comparison between booleans is completely valid.",
            "D": "The expression evaluates to a boolean, not None."
        },
        "a": 1.45,
        "b": -0.20,
        "point_biserial": 0.44
    },
    {
        "skill_code": "PRG_VARIABLES",
        "stem": "What is the result of evaluating `2 ** 3 ** 2` in Python?",
        "options": [
            {"id": "A", "text": "64", "is_distractor": True},
            {"id": "B", "text": "512", "is_distractor": False},
            {"id": "C", "text": "36", "is_distractor": True},
            {"id": "D", "text": "256", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The exponentiation operator `**` has right-to-left associativity in Python. Thus, `2 ** 3 ** 2` is evaluated as `2 ** (3 ** 2) = 2 ** 9 = 512`.",
        "distractor_explanations": {
            "A": "Error: Evaluated left-to-right as `(2 ** 3) ** 2 = 8 ** 2 = 64`.",
            "C": "Error: Multiplied bases and exponents ($2 \\times 3 \\times 2 = 12$).",
            "D": "Error: Confused power with $2^8 = 256$."
        },
        "a": 1.55,
        "b": 0.35,
        "point_biserial": 0.46
    },
    {
        "skill_code": "PRG_VARIABLES",
        "stem": "In C/C++, what is the size in bytes of the following struct on a 64-bit architecture with standard natural alignment?\n\n```c\nstruct Record {\n    char a;\n    int b;\n    char c;\n};\n```",
        "options": [
            {"id": "A", "text": "6 bytes", "is_distractor": True},
            {"id": "B", "text": "12 bytes", "is_distractor": False},
            {"id": "C", "text": "8 bytes", "is_distractor": True},
            {"id": "D", "text": "16 bytes", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "`char a` occupies byte 0. `int b` requires 4-byte alignment, so 3 padding bytes are inserted (bytes 1-3), placing `b` at bytes 4-7. `char c` occupies byte 8. The struct's largest member is 4 bytes, so trailing padding of 3 bytes is added (bytes 9-11) to make total size a multiple of 4: $12$ bytes.",
        "distractor_explanations": {
            "A": "Error: Naive sum of member sizes without padding ($1 + 4 + 1 = 6$).",
            "C": "Error: Assumed `int` alignment packed without trailing struct alignment.",
            "D": "Error: Assumed 8-byte pointer alignment across all members."
        },
        "a": 1.65,
        "b": 1.05,
        "point_biserial": 0.49
    },
    {
        "skill_code": "PRG_VARIABLES",
        "stem": "In Python, which of the following object types is **mutable**?",
        "options": [
            {"id": "A", "text": "tuple", "is_distractor": True},
            {"id": "B", "text": "frozenset", "is_distractor": True},
            {"id": "C", "text": "bytearray", "is_distractor": False},
            {"id": "D", "text": "str", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "`bytearray` is a mutable sequence of integers in range 0 <= x < 256. `tuple`, `frozenset`, and `str` are strictly immutable built-in types in Python.",
        "distractor_explanations": {
            "A": "Tuples are immutable; their elements cannot be reassigned in place.",
            "B": "Frozensets are immutable variants of sets that can be used as dictionary keys.",
            "D": "Strings in Python are immutable; string operations return new string instances."
        },
        "a": 1.40,
        "b": -0.60,
        "point_biserial": 0.43
    },

    # --- PRG_CONDITIONALS (5 items) ---
    {
        "skill_code": "PRG_CONDITIONALS",
        "stem": "What is the output of the following Python snippet?\n\n```python\nx = 10\ny = 20 if x > 5 else 30\nprint(y)\n```",
        "options": [
            {"id": "A", "text": "10", "is_distractor": True},
            {"id": "B", "text": "20", "is_distractor": False},
            {"id": "C", "text": "30", "is_distractor": True},
            {"id": "D", "text": "SyntaxError", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Python's ternary conditional expression evaluates the condition `x > 5`. Since $10 > 5$ is `True`, it evaluates and assigns the value preceding `if`, which is 20.",
        "distractor_explanations": {
            "A": "Assumed `x` value is returned.",
            "C": "Assumed the `else` branch is taken.",
            "D": "The syntax `val_true if cond else val_false` is valid Python ternary expression."
        },
        "a": 1.25,
        "b": -1.20,
        "point_biserial": 0.40
    },
    {
        "skill_code": "PRG_CONDITIONALS",
        "stem": "Due to short-circuit evaluation in Python, what will be printed?\n\n```python\ndef check():\n    print(\"Evaluated!\", end=\" \")\n    return True\n\nres = False and check()\nres2 = True or check()\nprint(\"Done\")\n```",
        "options": [
            {"id": "A", "text": "Evaluated! Evaluated! Done", "is_distractor": True},
            {"id": "B", "text": "Evaluated! Done", "is_distractor": True},
            {"id": "C", "text": "Done", "is_distractor": False},
            {"id": "D", "text": "True Done", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "In `False and check()`, the first operand is `False`, so Python short-circuits and never executes `check()`. In `True or check()`, the first operand is `True`, so it short-circuits and never executes `check()`. Thus, `check()` is never invoked, printing only `Done`.",
        "distractor_explanations": {
            "A": "Assumed both operands of logical operators are always eagerly evaluated.",
            "B": "Assumed one of the two short-circuits failed.",
            "D": "Boolean values are not printed directly."
        },
        "a": 1.45,
        "b": -0.10,
        "point_biserial": 0.44
    },
    {
        "skill_code": "PRG_CONDITIONALS",
        "stem": "In C, what is the output of the following switch-case snippet?\n\n```c\nint k = 2;\nswitch (k) {\n    case 1: printf(\"A\");\n    case 2: printf(\"B\");\n    case 3: printf(\"C\");\n    default: printf(\"D\");\n}\n```",
        "options": [
            {"id": "A", "text": "B", "is_distractor": True},
            {"id": "B", "text": "BCD", "is_distractor": False},
            {"id": "C", "text": "BC", "is_distractor": True},
            {"id": "D", "text": "D", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Because there are no `break` statements after `case 2`, execution falls through from `case 2` into `case 3` and then into `default`. Hence 'B', 'C', and 'D' are all printed.",
        "distractor_explanations": {
            "A": "Common misconception: Assuming cases automatically break when their body finishes.",
            "C": "Error: Default case is also executed upon fall-through.",
            "D": "Assumed only default executes."
        },
        "a": 1.50,
        "b": 0.30,
        "point_biserial": 0.45
    },
    {
        "skill_code": "PRG_CONDITIONALS",
        "stem": "What is the output of the following expression in Python 3.10+ match-case?\n\n```python\nval = (404, \"Not Found\")\nmatch val:\n    case (200, _):\n        res = \"OK\"\n    case (404, msg):\n        res = f\"Error: {msg}\"\n    case _:\n        res = \"Unknown\"\nprint(res)\n```",
        "options": [
            {"id": "A", "text": "OK", "is_distractor": True},
            {"id": "B", "text": "Error: Not Found", "is_distractor": False},
            {"id": "C", "text": "Unknown", "is_distractor": True},
            {"id": "D", "text": "SyntaxError", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Structural pattern matching matches the tuple `(404, \"Not Found\")` against `case (404, msg)`, binding `msg` to `\"Not Found\"`. The branch executes and sets `res = \"Error: Not Found\"`.",
        "distractor_explanations": {
            "A": "404 does not match 200.",
            "C": "Wildcard pattern `case _` is only reached if no preceding pattern matches.",
            "D": "Structural pattern matching is standard syntax in Python 3.10+."
        },
        "a": 1.55,
        "b": 0.70,
        "point_biserial": 0.47
    },
    {
        "skill_code": "PRG_CONDITIONALS",
        "stem": "Which of the following conditions correctly tests whether an integer `n` is a power of 2 (assuming $n > 0$) using bitwise operations?",
        "options": [
            {"id": "A", "text": "(n & (n - 1)) == 0", "is_distractor": False},
            {"id": "B", "text": "(n | (n - 1)) == 0", "is_distractor": True},
            {"id": "C", "text": "(n ^ (n - 1)) == 0", "is_distractor": True},
            {"id": "D", "text": "(n & (n + 1)) == 0", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A positive integer power of 2 has exactly one set bit in binary (e.g. $8 = 1000_2$). Subtracting 1 flips all bits up to that bit ($7 = 0111_2$). Bitwise AND `n & (n - 1)` clears that bit to 0. Thus `(n & (n - 1)) == 0` is true if and only if $n$ is a power of 2.",
        "distractor_explanations": {
            "B": "Bitwise OR will produce $2n - 1$, never 0 for positive integers.",
            "C": "Bitwise XOR produces $2n - 1$, which is non-zero.",
            "D": "`n & (n + 1)` clears trailing ones, not the lowest set bit."
        },
        "a": 1.65,
        "b": 1.20,
        "point_biserial": 0.50
    },

    # --- PRG_LOOPS (5 items) ---
    {
        "skill_code": "PRG_LOOPS",
        "stem": "What is the output of the following loop in Python?\n\n```python\ntotal = 0\nfor i in range(1, 6, 2):\n    total += i\nprint(total)\n```",
        "options": [
            {"id": "A", "text": "15", "is_distractor": True},
            {"id": "B", "text": "9", "is_distractor": False},
            {"id": "C", "text": "6", "is_distractor": True},
            {"id": "D", "text": "4", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "`range(1, 6, 2)` generates values 1, 3, 5 (stopping before 6). Total = $1 + 3 + 5 = 9$.",
        "distractor_explanations": {
            "A": "Error: Computed sum of all numbers 1 to 5 ($1+2+3+4+5=15$).",
            "C": "Error: Stopped after second iteration ($1 + 3 = 4$ or $1 + 5 = 6$).",
            "D": "Error: Summed 1 and 3 only."
        },
        "a": 1.25,
        "b": -1.30,
        "point_biserial": 0.39
    },
    {
        "skill_code": "PRG_LOOPS",
        "stem": "What is the output of the `for...else` block in Python when `break` is not encountered?\n\n```python\nfor i in range(3):\n    if i == 5:\n        break\nelse:\n    print(\"Completed\", end=\" \")\nprint(\"End\")\n```",
        "options": [
            {"id": "A", "text": "End", "is_distractor": True},
            {"id": "B", "text": "Completed End", "is_distractor": False},
            {"id": "C", "text": "Completed", "is_distractor": True},
            {"id": "D", "text": "SyntaxError", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "In Python, the `else` block of a loop executes if and only if the loop terminates normally without encountering a `break` statement. Since `i == 5` is never satisfied, the loop finishes normally, executing the `else` clause and printing `Completed End`.",
        "distractor_explanations": {
            "A": "Misconception: Believed loop `else` executes only when condition is initially false.",
            "C": "Missed the trailing `print(\"End\")` statement.",
            "D": "`for...else` is standard Python syntax."
        },
        "a": 1.45,
        "b": -0.25,
        "point_biserial": 0.43
    },
    {
        "skill_code": "PRG_LOOPS",
        "stem": "What is the time complexity of the following nested loop?\n\n```python\ni = 1\ncount = 0\nwhile i < n:\n    j = 1\n    while j < n:\n        count += 1\n        j *= 2\n    i *= 2\n```",
        "options": [
            {"id": "A", "text": "$O(n^2)$", "is_distractor": True},
            {"id": "B", "text": "$O(n \\log n)$", "is_distractor": True},
            {"id": "C", "text": "$O((\\log n)^2)$", "is_distractor": False},
            {"id": "D", "text": "$O(\\log n)$", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "The outer loop doubles `i` each step, executing $\\log_2 n$ times. The inner loop doubles `j` each step, executing $\\log_2 n$ times. Total iterations = $(\\log_2 n) \\times (\\log_2 n) = O((\\log n)^2)$.",
        "distractor_explanations": {
            "A": "Assumed linear increments of $i$ and $j$.",
            "B": "Assumed one loop is linear and the other logarithmic.",
            "D": "Forgot to multiply outer and inner loop iteration counts."
        },
        "a": 1.60,
        "b": 0.65,
        "point_biserial": 0.47
    },
    {
        "skill_code": "PRG_LOOPS",
        "stem": "What will be printed by the following code?\n\n```python\nx = [1, 2, 3]\nfor item in x:\n    x.remove(item)\nprint(x)\n```",
        "options": [
            {"id": "A", "text": "[]", "is_distractor": True},
            {"id": "B", "text": "[2]", "is_distractor": False},
            {"id": "C", "text": "[1, 3]", "is_distractor": True},
            {"id": "D", "text": "Raises a RuntimeError", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Modifying a list while iterating over it causes the internal index pointer to skip elements. In step 1: index 0 (item 1) is removed; list becomes `[2, 3]`. In step 2: iterator moves to index 1, which now holds 3 (skipping 2!). Item 3 is removed; list becomes `[2]`. Loop terminates.",
        "distractor_explanations": {
            "A": "Assumed all elements are visited and removed.",
            "C": "Error in manual simulation of list index shifting.",
            "D": "Python allows list removal during iteration without throwing `RuntimeError` (unlike dict size changes)."
        },
        "a": 1.65,
        "b": 1.15,
        "point_biserial": 0.49
    },
    {
        "skill_code": "PRG_LOOPS",
        "stem": "In C, how many times will the body of the `do-while` loop execute?\n\n```c\nint count = 10;\ndo {\n    count += 2;\n} while (count < 10);\n```",
        "options": [
            {"id": "A", "text": "0 times", "is_distractor": True},
            {"id": "B", "text": "1 time", "is_distractor": False},
            {"id": "C", "text": "Infinite loop", "is_distractor": True},
            {"id": "D", "text": "2 times", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "A `do-while` loop is an exit-controlled loop; the body executes at least once before the condition is evaluated. Inside, `count` becomes 12. Then `12 < 10` evaluates to `false`, terminating the loop after exactly 1 execution.",
        "distractor_explanations": {
            "A": "Confused `do-while` with an entry-controlled `while` loop.",
            "C": "The condition becomes false immediately, so it does not loop infinitely.",
            "D": "Condition fails on first check, so a second iteration never occurs."
        },
        "a": 1.35,
        "b": -0.80,
        "point_biserial": 0.41
    },

    # =========================================================================
    # TOPIC 2: Functions & Memory (15 items)
    # =========================================================================
    # --- PRG_FUNCTIONS (5 items) ---
    {
        "skill_code": "PRG_FUNCTIONS",
        "stem": "In Python, what is the danger of using a mutable default argument in a function definition?\n\n```python\ndef append_to(element, target_list=[]):\n    target_list.append(element)\n    return target_list\n```",
        "options": [
            {"id": "A", "text": "Default arguments are evaluated once at function definition time, sharing the same list across all subsequent invocations.", "is_distractor": False},
            {"id": "B", "text": "The function will raise a TypeError when called without arguments.", "is_distractor": True},
            {"id": "C", "text": "The list is garbage collected immediately upon function return.", "is_distractor": True},
            {"id": "D", "text": "Default arguments in Python cannot be lists.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Default parameter expressions in Python are evaluated once when the function definition is executed, binding the default value to the function object. Subsequent calls that omit the parameter share that exact same list in memory.",
        "distractor_explanations": {
            "B": "The call is syntactically valid and executes without raising TypeError.",
            "C": "The list persists as long as the function object itself remains referenced.",
            "D": "Lists are syntactically permitted as default arguments, but dangerous if mutated."
        },
        "a": 1.50,
        "b": -0.40,
        "point_biserial": 0.45
    },
    {
        "skill_code": "PRG_FUNCTIONS",
        "stem": "What is the output of the following closure in Python?\n\n```python\ndef make_multiplier(x):\n    def multiplier(n):\n        return x * n\n    return multiplier\n\ndbl = make_multiplier(2)\nprint(dbl(5))\n```",
        "options": [
            {"id": "A", "text": "10", "is_distractor": False},
            {"id": "B", "text": "7", "is_distractor": True},
            {"id": "C", "text": "25", "is_distractor": True},
            {"id": "D", "text": "None", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "`make_multiplier(2)` returns a closure `multiplier` retaining lexical binding `x = 2`. Calling `dbl(5)` executes `2 * 5 = 10`.",
        "distractor_explanations": {
            "B": "Added instead of multiplied ($2 + 5 = 7$).",
            "C": "Squared the argument ($5^2 = 25$).",
            "D": "The function returns an integer result."
        },
        "a": 1.30,
        "b": -1.00,
        "point_biserial": 0.41
    },
    {
        "skill_code": "PRG_FUNCTIONS",
        "stem": "In Python, which keyword allows an inner nested function to rebind a variable defined in its immediate outer enclosing scope?",
        "options": [
            {"id": "A", "text": "global", "is_distractor": True},
            {"id": "B", "text": "nonlocal", "is_distractor": False},
            {"id": "C", "text": "extern", "is_distractor": True},
            {"id": "D", "text": "static", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "The `nonlocal` keyword allows assignment to variables in an outer enclosing (non-global) function scope. `global` targets module-level namespace.",
        "distractor_explanations": {
            "A": "`global` binds to the module global namespace, skipping enclosing function scopes.",
            "C": "`extern` is a C/C++ storage class specifier, not valid Python.",
            "D": "`static` is not used for scope declaration in Python."
        },
        "a": 1.45,
        "b": 0.10,
        "point_biserial": 0.44
    },
    {
        "skill_code": "PRG_FUNCTIONS",
        "stem": "In C, what is the calling convention mechanism when arguments are passed **by value**?",
        "options": [
            {"id": "A", "text": "A copy of the argument value is pushed onto the call stack or passed in registers; changes inside the callee do not affect the caller's variable.", "is_distractor": False},
            {"id": "B", "text": "A reference to the original memory address is shared directly with the callee.", "is_distractor": True},
            {"id": "C", "text": "The variable is migrated to the heap for the duration of the function execution.", "is_distractor": True},
            {"id": "D", "text": "All parameters are converted to pointers automatically by the compiler.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In pass-by-value, the argument's data is copied to the stack frame or register allocated for the callee. Modifications within the callee operate strictly on the local copy.",
        "distractor_explanations": {
            "B": "Describes pass-by-reference, not pass-by-value.",
            "C": "Heap allocation is not involved in standard parameter passing.",
            "D": "Arrays decay to pointers, but primitive values do not."
        },
        "a": 1.55,
        "b": 0.60,
        "point_biserial": 0.46
    },
    {
        "skill_code": "PRG_FUNCTIONS",
        "stem": "What is the output of the following lambda and map expression in Python?\n\n```python\nnums = [1, 2, 3, 4]\nres = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, nums)))\nprint(res)\n```",
        "options": [
            {"id": "A", "text": "[1, 4, 9, 16]", "is_distractor": True},
            {"id": "B", "text": "[4, 16]", "is_distractor": False},
            {"id": "C", "text": "[2, 4]", "is_distractor": True},
            {"id": "D", "text": "[1, 9]", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "`filter` retains only even numbers: `[2, 4]`. `map` squares each element: $2^2 = 4, 4^2 = 16$. Result = `[4, 16]`.",
        "distractor_explanations": {
            "A": "Forgot the filtering step, squaring all numbers.",
            "C": "Forgot the map squaring step, outputting the filtered evens.",
            "D": "Filtered odds instead of evens."
        },
        "a": 1.40,
        "b": -0.50,
        "point_biserial": 0.43
    },

    # --- PRG_RECURSION (5 items) ---
    {
        "skill_code": "PRG_RECURSION",
        "stem": "What is the return value of `mystery(4)`?\n\n```python\ndef mystery(n):\n    if n <= 1:\n        return 1\n    return n * mystery(n - 1)\n```",
        "options": [
            {"id": "A", "text": "10", "is_distractor": True},
            {"id": "B", "text": "24", "is_distractor": False},
            {"id": "C", "text": "12", "is_distractor": True},
            {"id": "D", "text": "16", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "This is standard factorial: `mystery(4) = 4 * mystery(3) = 4 * 3 * 2 * 1 = 24`.",
        "distractor_explanations": {
            "A": "Error: Summed instead of multiplied ($4 + 3 + 2 + 1 = 10$).",
            "C": "Error: Truncated recursion prematurely.",
            "D": "Error: Multiplied $4 \\times 4 = 16$."
        },
        "a": 1.25,
        "b": -1.25,
        "point_biserial": 0.40
    },
    {
        "skill_code": "PRG_RECURSION",
        "stem": "What condition causes a recursive function to exceed the maximum call stack limit and trigger a StackOverflow / RecursionError?",
        "options": [
            {"id": "A", "text": "A missing, unreachable, or incorrect base case condition.", "is_distractor": False},
            {"id": "B", "text": "Allocating memory using malloc inside the heap.", "is_distractor": True},
            {"id": "C", "text": "Using tail-call optimization.", "is_distractor": True},
            {"id": "D", "text": "Passing parameters by reference.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Every recursive call allocates a stack frame. If the base case is omitted or never reached, recursive calls continue indefinitely until stack memory is exhausted.",
        "distractor_explanations": {
            "B": "Heap allocation exhausts heap memory, not call stack frames.",
            "C": "Tail-call optimization reuses existing stack frames to prevent stack overflow.",
            "D": "Passing by reference reduces stack copy size."
        },
        "a": 1.40,
        "b": -0.70,
        "point_biserial": 0.42
    },
    {
        "skill_code": "PRG_RECURSION",
        "stem": "What is the output of the recursive countdown function?\n\n```python\ndef count(n):\n    if n == 0:\n        return\n    count(n - 1)\n    print(n, end=\" \")\n\ncount(3)\n```",
        "options": [
            {"id": "A", "text": "3 2 1", "is_distractor": True},
            {"id": "B", "text": "1 2 3", "is_distractor": False},
            {"id": "C", "text": "3 2 1 0", "is_distractor": True},
            {"id": "D", "text": "0 1 2 3", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "Because the recursive call `count(n - 1)` occurs before the `print` statement, calls are pushed onto the call stack down to `n=0`. As the stack frames unwind during return, printing occurs in reverse: 1, then 2, then 3.",
        "distractor_explanations": {
            "A": "Error: Assumed printing happens before the recursive descent (head recursion).",
            "C": "Base case returns at 0 before printing.",
            "D": "0 is not printed due to early return in base case."
        },
        "a": 1.55,
        "b": 0.40,
        "point_biserial": 0.46
    },
    {
        "skill_code": "PRG_RECURSION",
        "stem": "What is the time complexity of the naive unmemoized Fibonacci algorithm?\n\n```python\ndef fib(n):\n    if n <= 1:\n        return n\n    return fib(n - 1) + fib(n - 2)\n```",
        "options": [
            {"id": "A", "text": "$O(n)$", "is_distractor": True},
            {"id": "B", "text": "$O(n^2)$", "is_distractor": True},
            {"id": "C", "text": "$O(2^n)$", "is_distractor": False},
            {"id": "D", "text": "$O(\\log n)$", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "The recurrence relation is $T(n) = T(n - 1) + T(n - 2) + O(1)$, which generates a recursion tree of depth $n$ where the number of nodes doubles at each level, yielding exponential complexity $O(2^n)$ (specifically $O(\\phi^n)$ where $\\phi \\approx 1.618$).",
        "distractor_explanations": {
            "A": "Achievable only with memoization or iterative dynamic programming.",
            "B": "Polynomial complexity is incorrect; the tree branching factor is 2.",
            "D": "Logarithmic complexity is achievable via matrix exponentiation, not naive recursion."
        },
        "a": 1.60,
        "b": 0.85,
        "point_biserial": 0.48
    },
    {
        "skill_code": "PRG_RECURSION",
        "stem": "Which recursive function implementation is **tail-recursive**?",
        "options": [
            {"id": "A", "text": "def fact(n):\n    return n * fact(n - 1) if n > 1 else 1", "is_distractor": True},
            {"id": "B", "text": "def fact(n, acc=1):\n    return fact(n - 1, acc * n) if n > 1 else acc", "is_distractor": False},
            {"id": "C", "text": "def fib(n):\n    return fib(n-1) + fib(n-2)", "is_distractor": True},
            {"id": "D", "text": "def rev(s):\n    return rev(s[1:]) + s[0]", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "A function is tail-recursive if the recursive call is the final operation executed before returning. In option B, `fact(n - 1, acc * n)` is returned directly with no pending multiplication. In option A, multiplication by `n` must wait for `fact(n - 1)` to return.",
        "distractor_explanations": {
            "A": "Not tail-recursive: Pending multiplication by `n` remains on the stack frame.",
            "C": "Not tail-recursive: Addition requires results from both recursive calls.",
            "D": "Not tail-recursive: String concatenation `+ s[0]` is pending."
        },
        "a": 1.70,
        "b": 1.35,
        "point_biserial": 0.51
    },

    # --- PRG_POINTERS (5 items) ---
    {
        "skill_code": "PRG_POINTERS",
        "stem": "In C, what is the output of the following pointer dereferencing code?\n\n```c\nint x = 42;\nint *ptr = &x;\n*ptr = 99;\nprintf(\"%d\", x);\n```",
        "options": [
            {"id": "A", "text": "42", "is_distractor": True},
            {"id": "B", "text": "99", "is_distractor": False},
            {"id": "C", "text": "Address of x", "is_distractor": True},
            {"id": "D", "text": "0", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "`*ptr = 99` writes the value 99 directly into the memory location pointed to by `ptr` (which is the address of `x`). Hence `x` becomes 99.",
        "distractor_explanations": {
            "A": "Assumed modifying the pointer dereference leaves the original variable untouched.",
            "C": "`x` is an integer, printed with `%d`, not an address.",
            "D": "Memory is not zeroed."
        },
        "a": 1.30,
        "b": -0.85,
        "point_biserial": 0.41
    },
    {
        "skill_code": "PRG_POINTERS",
        "stem": "In C, if `int arr[5] = {10, 20, 30, 40, 50};` and `int *p = arr;`, what is the value of `*(p + 2)`?",
        "options": [
            {"id": "A", "text": "10", "is_distractor": True},
            {"id": "B", "text": "20", "is_distractor": True},
            {"id": "C", "text": "30", "is_distractor": False},
            {"id": "D", "text": "40", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "Pointer arithmetic scales by the size of the underlying type (`sizeof(int)`). `p + 2` points to index 2 (`arr[2]`), whose value is 30.",
        "distractor_explanations": {
            "A": "`*p` or `arr[0]` is 10.",
            "B": "`*(p + 1)` or `arr[1]` is 20.",
            "D": "`*(p + 3)` or `arr[3]` is 40."
        },
        "a": 1.45,
        "b": -0.15,
        "point_biserial": 0.44
    },
    {
        "skill_code": "PRG_POINTERS",
        "stem": "What is a **dangling pointer** in systems programming?",
        "options": [
            {"id": "A", "text": "A pointer that points to a memory location that has already been deallocated or freed.", "is_distractor": False},
            {"id": "B", "text": "A pointer initialized to NULL.", "is_distractor": True},
            {"id": "C", "text": "A pointer pointing to read-only constant memory.", "is_distractor": True},
            {"id": "D", "text": "A pointer that has not yet been declared.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A dangling pointer arises when memory is deallocated (via `free()` or stack unwinding) without resetting the pointer to NULL. Dereferencing it yields undefined behavior.",
        "distractor_explanations": {
            "B": "A pointer initialized to NULL is a null pointer, not a dangling pointer.",
            "C": "Pointers to string literals point to constant memory, not dangling memory.",
            "D": "Undeclared identifiers produce compiler errors."
        },
        "a": 1.50,
        "b": 0.35,
        "point_biserial": 0.45
    },
    {
        "skill_code": "PRG_POINTERS",
        "stem": "Which C library function allocates memory on the heap and initializes all allocated bytes to zero?",
        "options": [
            {"id": "A", "text": "malloc", "is_distractor": True},
            {"id": "B", "text": "calloc", "is_distractor": False},
            {"id": "C", "text": "realloc", "is_distractor": True},
            {"id": "D", "text": "alloca", "is_distractor": True}
        ],
        "answer_key": "B",
        "explanation": "`calloc(num, size)` allocates contiguous memory on the heap and explicitly zeroes out every byte. `malloc` allocates memory without zero-initialization (containing garbage values).",
        "distractor_explanations": {
            "A": "`malloc` does not zero-initialize allocated memory.",
            "C": "`realloc` resizes an existing heap allocation.",
            "D": "`alloca` allocates memory on the stack, not the heap."
        },
        "a": 1.55,
        "b": 0.75,
        "point_biserial": 0.47
    },
    {
        "skill_code": "PRG_POINTERS",
        "stem": "In C, what is the declaration for a pointer to a function that takes two `int` parameters and returns a `double`?",
        "options": [
            {"id": "A", "text": "double (*func_ptr)(int, int);", "is_distractor": False},
            {"id": "B", "text": "double *func_ptr(int, int);", "is_distractor": True},
            {"id": "C", "text": "(double*) func_ptr(int, int);", "is_distractor": True},
            {"id": "D", "text": "double func_ptr*(int, int);", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Parentheses around `(*func_ptr)` are mandatory because `()` has higher precedence than `*`. `double (*func_ptr)(int, int);` declares a pointer to a function. Without parentheses, `double *func_ptr(int, int);` declares a function returning a pointer to double.",
        "distractor_explanations": {
            "B": "Declares a function named `func_ptr` that returns a `double*`.",
            "C": "Invalid syntax for a function pointer declaration.",
            "D": "Invalid C declaration syntax."
        },
        "a": 1.70,
        "b": 1.45,
        "point_biserial": 0.51
    }
]
