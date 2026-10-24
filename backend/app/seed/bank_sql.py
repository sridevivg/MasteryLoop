"""
SQL & Relational Querying Question Bank.
Topics:
1. Query Fundamentals (15 questions across SQL_BASIC_SELECT, SQL_AGGREGATES)
2. Complex Queries & Optimization (15 questions across SQL_JOINS, SQL_SUBQUERIES, SQL_INDEXING)
"""

SQL_ITEMS = [
    # =========================================================================
    # TOPIC 1: Query Fundamentals (15 items)
    # =========================================================================
    # --- SQL_BASIC_SELECT (8 items) ---
    {
        "skill_code": "SQL_BASIC_SELECT",
        "stem": "Which SQL clause is used to eliminate duplicate rows from the result set of a query?",
        "options": [
            {"id": "A", "text": "DISTINCT", "is_distractor": False},
            {"id": "B", "text": "UNIQUE", "is_distractor": True},
            {"id": "C", "text": "GROUP BY", "is_distractor": True},
            {"id": "D", "text": "DIFFERENT", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The SELECT DISTINCT statement is used to return only distinct (different) values, filtering out duplicate tuples across specified columns.",
        "distractor_explanations": {
            "B": "UNIQUE is a table constraint or column modifier, not a SELECT filter keyword.",
            "C": "GROUP BY aggregates rows sharing identical values into summary rows.",
            "D": "DIFFERENT is not a valid standard SQL keyword."
        },
        "a": 1.20,
        "b": -1.80,
        "point_biserial": 0.38
    },
    {
        "skill_code": "SQL_BASIC_SELECT",
        "stem": "In SQL pattern matching with the `LIKE` operator, which wildcard character matches exactly one single character?",
        "options": [
            {"id": "A", "text": "The underscore character (`_`)", "is_distractor": False},
            {"id": "B", "text": "The percent sign (`%`)", "is_distractor": True},
            {"id": "C", "text": "The asterisk sign (`*`)", "is_distractor": True},
            {"id": "D", "text": "The question mark (`?`)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In ANSI SQL, underscore (`_`) matches exactly one character, while percent (`%`) represents zero, one, or multiple characters.",
        "distractor_explanations": {
            "B": "`%` matches zero or more arbitrary characters.",
            "C": "`*` is used in regex or filesystem globbing, not standard SQL LIKE.",
            "D": "`?` is used in regex or globbing, not standard SQL LIKE."
        },
        "a": 1.30,
        "b": -1.20,
        "point_biserial": 0.40
    },
    {
        "skill_code": "SQL_BASIC_SELECT",
        "stem": "How does SQL evaluate the comparison expression `salary = NULL`?",
        "options": [
            {"id": "A", "text": "It evaluates to UNKNOWN (Three-Valued Logic), never TRUE.", "is_distractor": False},
            {"id": "B", "text": "It evaluates to TRUE if the salary column contains a NULL value.", "is_distractor": True},
            {"id": "C", "text": "It raises a syntax compilation error.", "is_distractor": True},
            {"id": "D", "text": "It evaluates to FALSE regardless of the column value.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In SQL Three-Valued Logic (3VL), comparisons with NULL yield UNKNOWN. To test for NULL presence, one must use `IS NULL` or `IS NOT NULL`.",
        "distractor_explanations": {
            "B": "Equality operator `=` cannot match NULL because NULL represents absence of value.",
            "C": "It is syntactically valid SQL, but logically incorrect.",
            "D": "It evaluates to UNKNOWN, which in a WHERE clause filters out rows, but UNKNOWN is distinct from FALSE in boolean truth tables (e.g., NOT UNKNOWN is UNKNOWN)."
        },
        "a": 1.45,
        "b": -0.60,
        "point_biserial": 0.44
    },
    {
        "skill_code": "SQL_BASIC_SELECT",
        "stem": "Consider the query: `SELECT * FROM employees WHERE department_id IN (10, 20, NULL)`. How does SQL evaluate rows where `department_id = 30`?",
        "options": [
            {"id": "A", "text": "The expression evaluates to UNKNOWN, so the row is omitted from the result set.", "is_distractor": False},
            {"id": "B", "text": "The query fails with a type coercion runtime error.", "is_distractor": True},
            {"id": "C", "text": "The row is returned because NULL bypasses the filter.", "is_distractor": True},
            {"id": "D", "text": "The expression evaluates to FALSE.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "`30 IN (10, 20, NULL)` is equivalent to `(30=10) OR (30=20) OR (30=NULL)` -> `FALSE OR FALSE OR UNKNOWN` -> `UNKNOWN`. WHERE clauses only keep rows where the predicate is TRUE.",
        "distractor_explanations": {
            "B": "NULL is compatible with any type; no error occurs.",
            "C": "Rows evaluating to UNKNOWN are omitted by WHERE.",
            "D": "In 3VL, FALSE OR UNKNOWN yields UNKNOWN, not FALSE."
        },
        "a": 1.50,
        "b": 0.10,
        "point_biserial": 0.46
    },
    {
        "skill_code": "SQL_BASIC_SELECT",
        "stem": "What is the logical query processing execution order of the major SQL clauses in a single SELECT statement?",
        "options": [
            {"id": "A", "text": "FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY", "is_distractor": False},
            {"id": "B", "text": "SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY", "is_distractor": True},
            {"id": "C", "text": "FROM -> WHERE -> SELECT -> GROUP BY -> HAVING -> ORDER BY", "is_distractor": True},
            {"id": "D", "text": "WHERE -> FROM -> GROUP BY -> HAVING -> SELECT -> ORDER BY", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Logical query execution begins with table ingestion (FROM/JOIN), row filtering (WHERE), row aggregation (GROUP BY), group filtering (HAVING), projection (SELECT), and final sorting (ORDER BY).",
        "distractor_explanations": {
            "B": "Written order begins with SELECT, but logical evaluation starts at FROM.",
            "C": "SELECT cannot precede GROUP BY/HAVING because aggregation happens on source columns before projection.",
            "D": "WHERE cannot run before FROM because source tables and join criteria must exist first."
        },
        "a": 1.55,
        "b": 0.60,
        "point_biserial": 0.48
    },
    {
        "skill_code": "SQL_BASIC_SELECT",
        "stem": "In SQL, why can you NOT use a column alias defined in the `SELECT` clause directly in the `WHERE` clause of the same query block?",
        "options": [
            {"id": "A", "text": "Because the `WHERE` clause is logically evaluated before the `SELECT` clause projections.", "is_distractor": False},
            {"id": "B", "text": "Because aliases are strictly reserved for table names in FROM clauses.", "is_distractor": True},
            {"id": "C", "text": "Because SQL engines do not allow arithmetic expressions inside WHERE clauses.", "is_distractor": True},
            {"id": "D", "text": "Because column aliases are only accessible inside stored procedures.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Since `WHERE` executes before `SELECT`, the column alias created in `SELECT` has not yet materialized in the execution pipeline when `WHERE` is evaluated.",
        "distractor_explanations": {
            "B": "Column aliases are standard and supported; their scope is post-projection.",
            "C": "Arithmetic expressions are fully valid in WHERE clauses.",
            "D": "Aliases are standard across ad-hoc queries, not limited to stored procedures."
        },
        "a": 1.60,
        "b": 0.90,
        "point_biserial": 0.49
    },
    {
        "skill_code": "SQL_BASIC_SELECT",
        "stem": "What does the query `SELECT COALESCE(bonus, commission, 0) FROM payroll` return for a row where `bonus` is NULL and `commission` is 250?",
        "options": [
            {"id": "A", "text": "250", "is_distractor": False},
            {"id": "B", "text": "0", "is_distractor": True},
            {"id": "C", "text": "NULL", "is_distractor": True},
            {"id": "D", "text": "An error due to mixed parameter counts", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "COALESCE evaluates its arguments from left to right and returns the first non-NULL expression encountered.",
        "distractor_explanations": {
            "B": "0 is returned only if both `bonus` and `commission` are NULL.",
            "C": "COALESCE only returns NULL if all arguments are NULL.",
            "D": "COALESCE accepts variable numbers of arguments."
        },
        "a": 1.35,
        "b": -0.80,
        "point_biserial": 0.41
    },
    {
        "skill_code": "SQL_BASIC_SELECT",
        "stem": "What is the result of `ORDER BY column_name ASC` regarding NULL values in ANSI SQL standard?",
        "options": [
            {"id": "A", "text": "The standard specifies NULLs are either all first or all last; databases provide NULLS FIRST / NULLS LAST to control this.", "is_distractor": False},
            {"id": "B", "text": "NULL values are strictly filtered out and omitted from sorted output.", "is_distractor": True},
            {"id": "C", "text": "NULL values trigger a runtime error during index scanning.", "is_distractor": True},
            {"id": "D", "text": "NULL is always treated as the mathematical integer 0.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "ANSI SQL states that NULL values should be ordered together (either all first or all last). Dialects like PostgreSQL place NULLs last by default in ASC, Oracle places them last, while MySQL/SQL Server place them first. `NULLS FIRST/LAST` overrides this.",
        "distractor_explanations": {
            "B": "ORDER BY does not filter rows; WHERE does.",
            "C": "NULL sorting is valid and supported by all relational engines.",
            "D": "NULL represents unknown/missing value, never 0."
        },
        "a": 1.45,
        "b": 0.30,
        "point_biserial": 0.43
    },

    # --- SQL_AGGREGATES (7 items) ---
    {
        "skill_code": "SQL_AGGREGATES",
        "stem": "What is the primary operational difference between the `WHERE` clause and the `HAVING` clause?",
        "options": [
            {"id": "A", "text": "`WHERE` filters individual rows before grouping; `HAVING` filters aggregated group records after grouping.", "is_distractor": False},
            {"id": "B", "text": "`WHERE` is used only for numeric data; `HAVING` is used for text data.", "is_distractor": True},
            {"id": "C", "text": "`WHERE` can contain aggregate functions; `HAVING` cannot.", "is_distractor": True},
            {"id": "D", "text": "`HAVING` executes before `GROUP BY` in logical query processing.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "WHERE filters base table tuples prior to grouping and aggregation. HAVING filters grouped rows using aggregate expressions (e.g., `COUNT(*) > 5`).",
        "distractor_explanations": {
            "B": "Both clauses support any valid SQL data type.",
            "C": "Aggregate functions cannot appear in WHERE clauses (e.g., `WHERE COUNT(*) > 1` is invalid).",
            "D": "HAVING executes after GROUP BY, not before."
        },
        "a": 1.30,
        "b": -1.10,
        "point_biserial": 0.40
    },
    {
        "skill_code": "SQL_AGGREGATES",
        "stem": "Given a table `employees` containing 10 rows where column `commission` has 6 numeric values and 4 `NULL` values. What does `COUNT(commission)` return?",
        "options": [
            {"id": "A", "text": "6", "is_distractor": False},
            {"id": "B", "text": "10", "is_distractor": True},
            {"id": "C", "text": "0", "is_distractor": True},
            {"id": "D", "text": "NULL", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "`COUNT(expression)` counts only non-NULL occurrences. `COUNT(*)` counts all rows including NULLs.",
        "distractor_explanations": {
            "B": "10 is returned by `COUNT(*)`, not `COUNT(commission)`.",
            "C": "Aggregate COUNT returns 0 only when no non-NULL rows exist.",
            "D": "COUNT never returns NULL; it returns 0 for an empty non-NULL match."
        },
        "a": 1.40,
        "b": -0.50,
        "point_biserial": 0.42
    },
    {
        "skill_code": "SQL_AGGREGATES",
        "stem": "If a table contains values [10, 20, 30, NULL] in column `score`, what is the result of `AVG(score)`?",
        "options": [
            {"id": "A", "text": "20.0", "is_distractor": False},
            {"id": "B", "text": "15.0", "is_distractor": True},
            {"id": "C", "text": "NULL", "is_distractor": True},
            {"id": "D", "text": "Runtime Division by Zero Error", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Standard aggregate functions (SUM, AVG, MIN, MAX) automatically ignore NULL values. The sum (60) is divided by the count of non-NULL values (3), yielding 20.0.",
        "distractor_explanations": {
            "B": "15.0 would result if NULL were treated as 0 (60 / 4), which SQL does not do.",
            "C": "AVG only returns NULL if the input multiset contains exclusively NULL values.",
            "D": "There are 3 valid items; no division by zero occurs."
        },
        "a": 1.45,
        "b": -0.20,
        "point_biserial": 0.44
    },
    {
        "skill_code": "SQL_AGGREGATES",
        "stem": "What is the effect of the following query? `SELECT department_id, COUNT(*) FROM employees GROUP BY department_id HAVING COUNT(*) > 5`",
        "options": [
            {"id": "A", "text": "It returns only department IDs that have strictly more than 5 employees along with their employee counts.", "is_distractor": False},
            {"id": "B", "text": "It filters out the top 5 employees from each department.", "is_distractor": True},
            {"id": "C", "text": "It raises a syntax error because aggregate functions cannot appear in HAVING.", "is_distractor": True},
            {"id": "D", "text": "It returns all departments but caps the count output at 5.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The HAVING clause acts as a predicate on aggregated group records, filtering out any department group whose member count does not exceed 5.",
        "distractor_explanations": {
            "B": "HAVING does not filter individual employees within groups.",
            "C": "Aggregate functions are specifically designed to be used in HAVING.",
            "D": "It filters entire department groups, not capping the count."
        },
        "a": 1.35,
        "b": -0.40,
        "point_biserial": 0.41
    },
    {
        "skill_code": "SQL_AGGREGATES",
        "stem": "Why does the query `SELECT department_id, employee_name, AVG(salary) FROM employees GROUP BY department_id` fail in standard SQL (without functional dependency detection)?",
        "options": [
            {"id": "A", "text": "`employee_name` is neither included in the `GROUP BY` clause nor enclosed within an aggregate function.", "is_distractor": False},
            {"id": "B", "text": "`AVG(salary)` cannot be computed across grouped departments.", "is_distractor": True},
            {"id": "C", "text": "`GROUP BY` requires all projected columns to be aggregate functions.", "is_distractor": True},
            {"id": "D", "text": "The query requires a HAVING clause to be syntactically valid.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In standard SQL, every column in the SELECT list must either appear in the GROUP BY clause or be encapsulated within an aggregate function, preventing ambiguity when multiple employee names map to one group.",
        "distractor_explanations": {
            "B": "AVG(salary) is perfectly valid when grouped by department_id.",
            "C": "Grouping columns themselves are allowed in the SELECT list.",
            "D": "HAVING is optional."
        },
        "a": 1.55,
        "b": 0.40,
        "point_biserial": 0.47
    },
    {
        "skill_code": "SQL_AGGREGATES",
        "stem": "What does `COUNT(DISTINCT department_id)` evaluate to for a table with values [1, 1, 2, NULL, 3, 3]?",
        "options": [
            {"id": "A", "text": "3", "is_distractor": False},
            {"id": "B", "text": "4", "is_distractor": True},
            {"id": "C", "text": "5", "is_distractor": True},
            {"id": "D", "text": "6", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Distinct non-NULL values are {1, 2, 3}. NULL is ignored by COUNT(DISTINCT col), giving a count of 3.",
        "distractor_explanations": {
            "B": "4 would include NULL as a distinct category, but SQL COUNT(col) ignores NULL.",
            "C": "5 is the count of non-NULL values without deduplication.",
            "D": "6 is the total row count `COUNT(*)`."
        },
        "a": 1.45,
        "b": 0.20,
        "point_biserial": 0.45
    },
    {
        "skill_code": "SQL_AGGREGATES",
        "stem": "What is the difference between `GROUP BY ROLLUP(year, region)` and standard `GROUP BY year, region`?",
        "options": [
            {"id": "A", "text": "`ROLLUP` generates hierarchical subtotals for (year, region), (year), and a grand total (), whereas standard `GROUP BY` produces only (year, region).", "is_distractor": False},
            {"id": "B", "text": "`ROLLUP` sorts the result set descending by default.", "is_distractor": True},
            {"id": "C", "text": "`ROLLUP` eliminates all rows where values are NULL.", "is_distractor": True},
            {"id": "D", "text": "`ROLLUP` runs on a separate worker thread to increase throughput.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "ROLLUP creates progressive hierarchical grouping sets from left to right: (year, region), (year), and (), generating intermediate subtotals and an overall grand total.",
        "distractor_explanations": {
            "B": "ROLLUP defines grouping sets, not sorting order.",
            "C": "ROLLUP introduces NULLs into group columns to represent subtotal and grand total rows.",
            "D": "It is an analytical SQL extension, not a threading directive."
        },
        "a": 1.65,
        "b": 1.20,
        "point_biserial": 0.52
    },

    # =========================================================================
    # TOPIC 2: Complex Queries & Optimization (15 items)
    # =========================================================================
    # --- SQL_JOINS (5 items) ---
    {
        "skill_code": "SQL_JOINS",
        "stem": "Given table A with 4 rows and table B with 5 rows. If there are no common matching keys between them, how many rows are returned by `SELECT * FROM A FULL OUTER JOIN B ON A.id = B.a_id`?",
        "options": [
            {"id": "A", "text": "9 rows", "is_distractor": False},
            {"id": "B", "text": "0 rows", "is_distractor": True},
            {"id": "C", "text": "20 rows", "is_distractor": True},
            {"id": "D", "text": "5 rows", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A FULL OUTER JOIN retains all rows from both tables. With zero matching keys, each of the 4 rows from A appears with NULLs for B's columns (4 rows), and each of the 5 rows from B appears with NULLs for A's columns (5 rows), totaling 4 + 5 = 9 rows.",
        "distractor_explanations": {
            "B": "0 rows would be returned by an INNER JOIN.",
            "C": "20 rows (4 * 5) would be returned by a CROSS JOIN (Cartesian product).",
            "D": "5 rows would be returned by a RIGHT JOIN where B is the right table."
        },
        "a": 1.40,
        "b": -0.30,
        "point_biserial": 0.42
    },
    {
        "skill_code": "SQL_JOINS",
        "stem": "What is the difference between filtering in the `ON` clause versus the `WHERE` clause in a `LEFT JOIN` query?",
        "options": [
            {"id": "A", "text": "The `ON` condition determines which right-table rows match the left-table row; the `WHERE` condition filters the entire result set after the join is performed.", "is_distractor": False},
            {"id": "B", "text": "The `ON` clause is strictly faster than the `WHERE` clause because it bypasses indexes.", "is_distractor": True},
            {"id": "C", "text": "They produce identical results under all circumstances.", "is_distractor": True},
            {"id": "D", "text": "The `ON` clause filters before reading tables; `WHERE` filters after returning to client.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In an outer join, predicate in the `ON` clause only restricts the optional table (non-matching rows still output with NULLs). Predicates in `WHERE` filter the combined row after joining, turning non-matching NULLs into FALSE and effectively converting the outer join into an inner join.",
        "distractor_explanations": {
            "B": "Both leverage indexes during query optimization.",
            "C": "They produce different results whenever filtering the right table on non-NULL conditions.",
            "D": "Both are executed within the database engine during query execution."
        },
        "a": 1.55,
        "b": 0.50,
        "point_biserial": 0.48
    },
    {
        "skill_code": "SQL_JOINS",
        "stem": "Which join type returns all rows from the left table and matched rows from the right table, replacing unmatched right-table values with NULL?",
        "options": [
            {"id": "A", "text": "LEFT OUTER JOIN", "is_distractor": False},
            {"id": "B", "text": "INNER JOIN", "is_distractor": True},
            {"id": "C", "text": "CROSS JOIN", "is_distractor": True},
            {"id": "D", "text": "NATURAL JOIN", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "LEFT OUTER JOIN preserves every tuple from the left relation, pairing with matching tuples from the right relation or projecting NULLs where no join match exists.",
        "distractor_explanations": {
            "B": "INNER JOIN discards unmatched rows from both tables.",
            "C": "CROSS JOIN produces the Cartesian product of both tables.",
            "D": "NATURAL JOIN joins on all matching column names and defaults to an INNER JOIN."
        },
        "a": 1.25,
        "b": -1.40,
        "point_biserial": 0.39
    },
    {
        "skill_code": "SQL_JOINS",
        "stem": "What is a self-join in SQL?",
        "options": [
            {"id": "A", "text": "A join in which a table is joined with itself using distinct table aliases.", "is_distractor": False},
            {"id": "B", "text": "A join that automatically infers foreign keys without an ON clause.", "is_distractor": True},
            {"id": "C", "text": "A join between two identical schema tables across different databases.", "is_distractor": True},
            {"id": "D", "text": "A join created exclusively within a stored procedure.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A self-join references the same table multiple times (e.g., `employees e JOIN employees m ON e.manager_id = m.id`) to model recursive or hierarchical relationships.",
        "distractor_explanations": {
            "B": "Describes NATURAL JOIN.",
            "C": "Describes a cross-database or federated join.",
            "D": "Self-joins are standard ad-hoc SQL queries."
        },
        "a": 1.35,
        "b": -0.60,
        "point_biserial": 0.41
    },
    {
        "skill_code": "SQL_JOINS",
        "stem": "In database query execution engines, when is a **Hash Join** preferred over a **Nested Loop Join**?",
        "options": [
            {"id": "A", "text": "When joining large, unsorted datasets without relevant index support on the join condition.", "is_distractor": False},
            {"id": "B", "text": "When the inner table is very small and has a unique index on the join key.", "is_distractor": True},
            {"id": "C", "text": "When the join condition uses non-equality operators like `<` or `BETWEEN`.", "is_distractor": True},
            {"id": "D", "text": "When both input relations are already sorted on the join key.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Hash join builds an in-memory hash table on the smaller table and probes with the larger table in O(M + N) time, making it ideal for large unsorted inputs with equi-joins where indexes are absent.",
        "distractor_explanations": {
            "B": "Index Nested Loop Join is optimal when the inner table has an index and outer table is small.",
            "C": "Hash joins only support equi-joins (`=`), not range or inequality joins.",
            "D": "Merge Join is optimal when both inputs are already sorted on the join key."
        },
        "a": 1.65,
        "b": 1.30,
        "point_biserial": 0.53
    },

    # --- SQL_SUBQUERIES (5 items) ---
    {
        "skill_code": "SQL_SUBQUERIES",
        "stem": "What distinguishes a **correlated subquery** from an **uncorrelated (independent) subquery**?",
        "options": [
            {"id": "A", "text": "A correlated subquery references columns from the outer query and is conceptually evaluated for each row processed by the outer query.", "is_distractor": False},
            {"id": "B", "text": "A correlated subquery executes once before the outer query runs.", "is_distractor": True},
            {"id": "C", "text": "A correlated subquery can only return multiple columns whereas an independent subquery cannot.", "is_distractor": True},
            {"id": "D", "text": "Correlated subqueries cannot be used inside WHERE clauses.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A correlated subquery depends on values from the current candidate row of the outer query, meaning it cannot be executed in isolation independently of the outer query context.",
        "distractor_explanations": {
            "B": "Independent (uncorrelated) subqueries execute once before the outer query.",
            "C": "Correlated subqueries can return scalar values, single columns, or boolean presence via EXISTS.",
            "D": "WHERE clauses frequently utilize correlated subqueries (e.g., `WHERE EXISTS (...)`)."
        },
        "a": 1.50,
        "b": 0.20,
        "point_biserial": 0.46
    },
    {
        "skill_code": "SQL_SUBQUERIES",
        "stem": "What is the primary performance benefit of using `EXISTS` over `COUNT(*) > 0` in a subquery checking for row existence?",
        "options": [
            {"id": "A", "text": "`EXISTS` short-circuits and terminates scanning as soon as the first matching row is found.", "is_distractor": False},
            {"id": "B", "text": "`EXISTS` bypasses table locks whereas `COUNT(*)` requires exclusive locks.", "is_distractor": True},
            {"id": "C", "text": "`COUNT(*)` forces all rows into temporary disk storage.", "is_distractor": True},
            {"id": "D", "text": "`EXISTS` returns integer row counts faster.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "`EXISTS` stops evaluation immediately upon locating the first matching tuple (boolean short-circuit), whereas `COUNT(*)` must count all matching tuples across the table.",
        "distractor_explanations": {
            "B": "Both operate under standard transaction isolation read locks.",
            "C": "COUNT(*) aggregates in-memory unless working sets exceed buffer pools.",
            "D": "EXISTS returns a boolean (TRUE/FALSE), not an integer count."
        },
        "a": 1.45,
        "b": -0.10,
        "point_biserial": 0.44
    },
    {
        "skill_code": "SQL_SUBQUERIES",
        "stem": "In SQL, what is a **Common Table Expression (CTE)** defined using the `WITH` clause?",
        "options": [
            {"id": "A", "text": "A named, temporary result set defined within the execution scope of a single SELECT, INSERT, UPDATE, or DELETE statement.", "is_distractor": False},
            {"id": "B", "text": "A permanent view stored in the database catalog schema.", "is_distractor": True},
            {"id": "C", "text": "A materialized table that persists across multiple client sessions.", "is_distractor": True},
            {"id": "D", "text": "A trigger that executes automatically upon table modification.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A CTE provides a readable, modular way to write auxiliary statements for use in a larger query. It exists only for the lifetime of that statement.",
        "distractor_explanations": {
            "B": "A VIEW is cataloged permanently; a CTE is transient to the query.",
            "C": "Temporary or physical tables persist across sessions, unlike CTEs.",
            "D": "Triggers are procedural event-driven database objects."
        },
        "a": 1.35,
        "b": -0.70,
        "point_biserial": 0.40
    },
    {
        "skill_code": "SQL_SUBQUERIES",
        "stem": "What is the danger of using `NOT IN (SELECT department_id FROM ...)` if the subquery returns even a single `NULL` value?",
        "options": [
            {"id": "A", "text": "The entire `NOT IN` expression evaluates to UNKNOWN for all rows, causing the outer query to return zero rows.", "is_distractor": False},
            {"id": "B", "text": "It raises a syntax compilation error.", "is_distractor": True},
            {"id": "C", "text": "It automatically ignores the NULL and matches the remaining values.", "is_distractor": True},
            {"id": "D", "text": "It causes an infinite loop in the query planner.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "`val NOT IN (1, NULL)` expands to `val <> 1 AND val <> NULL`. Since `val <> NULL` evaluates to UNKNOWN, `TRUE AND UNKNOWN` yields UNKNOWN. Thus, no row satisfies the WHERE predicate.",
        "distractor_explanations": {
            "B": "It is valid syntax, making this a notorious logical bug.",
            "C": "NOT IN does NOT ignore NULLs; NOT EXISTS does ignore them safely.",
            "D": "The query executes and terminates, but returns an empty result set."
        },
        "a": 1.65,
        "b": 0.95,
        "point_biserial": 0.51
    },
    {
        "skill_code": "SQL_SUBQUERIES",
        "stem": "What is a **Recursive CTE** commonly used for in relational databases?",
        "options": [
            {"id": "A", "text": "Querying hierarchical or graph-structured data such as organizational charts or bill-of-materials.", "is_distractor": False},
            {"id": "B", "text": "Performing parallel bulk data exports to CSV files.", "is_distractor": True},
            {"id": "C", "text": "Bypassing ACID transaction guarantees during bulk updates.", "is_distractor": True},
            {"id": "D", "text": "Creating clustered index hierarchies on partitioned tables.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Recursive CTEs contain an anchor member and a recursive member unioned together, repeatedly executing until no new child rows are generated, ideal for trees and directed graphs.",
        "distractor_explanations": {
            "B": "Bulk export utilities (e.g., COPY, bcp) handle exports.",
            "C": "Recursive CTEs run under standard ACID transaction isolation.",
            "D": "Index creation is a DDL operation."
        },
        "a": 1.55,
        "b": 0.80,
        "point_biserial": 0.49
    },

    # --- SQL_INDEXING (5 items) ---
    {
        "skill_code": "SQL_INDEXING",
        "stem": "What is the primary difference between a **Clustered Index** and a **Non-Clustered (Secondary) Index** in B-Tree storage?",
        "options": [
            {"id": "A", "text": "A clustered index defines the physical order of data rows in the table; leaf nodes contain actual data pages. Non-clustered index leaf nodes contain pointers/keys to data rows.", "is_distractor": False},
            {"id": "B", "text": "A table can have up to 16 clustered indexes but only 1 non-clustered index.", "is_distractor": True},
            {"id": "C", "text": "Clustered indexes are stored in RAM; non-clustered indexes are stored on SSD.", "is_distractor": True},
            {"id": "D", "text": "Clustered indexes can only index integer columns.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Because table rows can only be physically sorted in one order, a table can have only one clustered index. Non-clustered indexes maintain separate B-trees holding search keys and row locators (RID or clustered key).",
        "distractor_explanations": {
            "B": "A table can have exactly one clustered index and many non-clustered indexes.",
            "C": "Both are stored on persistent storage and cached in the buffer pool.",
            "D": "Clustered indexes can be built on date, string, or composite columns."
        },
        "a": 1.50,
        "b": 0.10,
        "point_biserial": 0.46
    },
    {
        "skill_code": "SQL_INDEXING",
        "stem": "Given a composite index on `(last_name, first_name, department_id)`, which query predicate can fully utilize this index via the leftmost prefix rule?",
        "options": [
            {"id": "A", "text": "`WHERE last_name = 'Smith' AND first_name = 'John'`", "is_distractor": False},
            {"id": "B", "text": "`WHERE first_name = 'John' AND department_id = 4`", "is_distractor": True},
            {"id": "C", "text": "`WHERE department_id = 4`", "is_distractor": True},
            {"id": "D", "text": "`WHERE first_name = 'John'`", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "B-Tree composite indexes require leading columns of the index to be present in the query predicate (the leftmost prefix rule). Query A uses the first two columns (`last_name`, `first_name`).",
        "distractor_explanations": {
            "B": "Skips the leading column `last_name`; the index cannot be searched efficiently.",
            "C": "Skips both leading columns.",
            "D": "Skips the leading column `last_name`."
        },
        "a": 1.60,
        "b": 0.70,
        "point_biserial": 0.50
    },
    {
        "skill_code": "SQL_INDEXING",
        "stem": "What is a **Covering Index** in database query optimization?",
        "options": [
            {"id": "A", "text": "An index that contains all columns requested by a query (in keys or included columns), allowing the query engine to satisfy the request without reading table heap/data pages.", "is_distractor": False},
            {"id": "B", "text": "An index that automatically covers and encrypts sensitive table data.", "is_distractor": True},
            {"id": "C", "text": "An index that spans all tables within an entire database catalog.", "is_distractor": True},
            {"id": "D", "text": "An index that replaces the database write-ahead log.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "An index covers a query if the engine can satisfy SELECT, WHERE, and ORDER BY clauses directly from index leaf nodes, eliminating expensive bookmark lookups (RID/key lookups) into data pages.",
        "distractor_explanations": {
            "B": "Encryption is handled by TDE (Transparent Data Encryption), not index coverage.",
            "C": "Indexes are table-specific objects.",
            "D": "WAL handles durability and atomicity, not indexing."
        },
        "a": 1.65,
        "b": 1.10,
        "point_biserial": 0.52
    },
    {
        "skill_code": "SQL_INDEXING",
        "stem": "In query execution plans, what is the meaning of a **Table Scan** (or Sequential Scan)?",
        "options": [
            {"id": "A", "text": "The query engine reads every data page and evaluates every row in the table from start to finish.", "is_distractor": False},
            {"id": "B", "text": "The query engine traverses a balanced B-Tree from root to leaf node.", "is_distractor": True},
            {"id": "C", "text": "The database verifies table constraints before inserting rows.", "is_distractor": True},
            {"id": "D", "text": "The engine scans memory caches to detect corrupted pages.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A Sequential/Table Scan examines every block in a table heap sequentially. While efficient for retrieving large percentages of a table, it is O(N) and expensive for selective queries.",
        "distractor_explanations": {
            "B": "Describes an Index Seek.",
            "C": "Describes constraint validation.",
            "D": "Describes a page checksum or DBCC check."
        },
        "a": 1.30,
        "b": -1.00,
        "point_biserial": 0.38
    },
    {
        "skill_code": "SQL_INDEXING",
        "stem": "Why does applying a function to an indexed column, such as `WHERE UPPER(email) = 'USER@EXAMPLE.COM'`, typically prevent the query planner from using a standard B-Tree index on `email`?",
        "options": [
            {"id": "A", "text": "The predicate becomes non-sargable (Search Argument Able); the B-Tree is ordered by the raw string values, not transformed function outputs.", "is_distractor": False},
            {"id": "B", "text": "Because SQL prohibits string comparison functions on indexed columns.", "is_distractor": True},
            {"id": "C", "text": "Because `UPPER()` alters the collation of the underlying database table.", "is_distractor": True},
            {"id": "D", "text": "Because B-Trees can only store uppercase ASCII characters.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Standard B-tree indexes are sorted by raw column values. Wrapping the column in a function prevents direct seek operations unless a function-based/expression index (`CREATE INDEX ... ON employees(UPPER(email))`) is created.",
        "distractor_explanations": {
            "B": "Functions are permitted in queries; they just invalidate index seek operations.",
            "C": "UPPER() transforms characters in memory; it does not alter table collation.",
            "D": "B-Trees store arbitrary binary/text byte sequences under collation rules."
        },
        "a": 1.70,
        "b": 1.40,
        "point_biserial": 0.54
    }
]
