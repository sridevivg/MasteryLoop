"""
Data Structures & Algorithms Question Bank.
Topic 1: Linear Data Structures (15 questions across DSA_ARRAYS, DSA_LINKED_LISTS, DSA_STACKS_QUEUES)
Topic 2: Trees & Hierarchies (15 questions across DSA_BINARY_TREES, DSA_BST)
Topic 3: Graphs & Algorithms (15 questions across DSA_GRAPH_BFS_DFS, DSA_DYNAMIC_PROG)
Total: 45 items.
"""

DSA_ITEMS = [
    # =========================================================================
    # TOPIC 1: Linear Data Structures (15 items)
    # =========================================================================
    # --- DSA_ARRAYS (5 items) ---
    {
        "skill_code": "DSA_ARRAYS",
        "stem": "What is the worst-case time complexity of finding a pair of elements that sum to a target $T$ in an **already sorted** array of size $N$ using the Two-Pointer technique?",
        "options": [
            {"id": "A", "text": "O(N^2)", "is_distractor": True},
            {"id": "B", "text": "O(N log N)", "is_distractor": True},
            {"id": "C", "text": "O(N)", "is_distractor": False},
            {"id": "D", "text": "O(1)", "is_distractor": True}
        ],
        "answer_key": "C",
        "explanation": "With left pointer at index 0 and right pointer at index N-1, each comparison moves either left forward or right backward. The pointers meet after at most N steps, achieving O(N) time and O(1) auxiliary space.",
        "distractor_explanations": {
            "A": "Misconception: Assumed nested loop comparison.",
            "B": "Error: Sorting takes O(N log N), but the array is already sorted.",
            "D": "Error: Only hash map lookup is O(1) amortized, but iterating over the array takes O(N)."
        },
        "a": 1.35,
        "b": -0.30,
        "point_biserial": 0.42
    },
    {
        "skill_code": "DSA_ARRAYS",
        "stem": "In Kadane's Algorithm for Maximum Subarray Sum, what is the core recurrence relation maintained at each index `i`?",
        "options": [
            {"id": "A", "text": "current_sum = max(arr[i], current_sum + arr[i])", "is_distractor": False},
            {"id": "B", "text": "current_sum = current_sum + arr[i]", "is_distractor": True},
            {"id": "C", "text": "current_sum = max(0, current_sum)", "is_distractor": True},
            {"id": "D", "text": "current_sum = min(arr[i], current_sum + arr[i])", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Kadane's algorithm decides at index `i` whether to extend the existing subarray (`current_sum + arr[i]`) or start a fresh subarray at `arr[i]` (`max(arr[i], current_sum + arr[i])`), executing in $O(N)$ time.",
        "distractor_explanations": {
            "B": "Does not restart when running sum becomes negative.",
            "C": "Omits the element at index `i`.",
            "D": "Calculates minimum subarray sum, not maximum."
        },
        "a": 1.45,
        "b": 0.10,
        "point_biserial": 0.45
    },
    {
        "skill_code": "DSA_ARRAYS",
        "stem": "What is the optimal time complexity to rotate an array of size $N$ to the right by $K$ positions using $O(1)$ auxiliary memory?",
        "options": [
            {"id": "A", "text": "O(N)", "is_distractor": False},
            {"id": "B", "text": "O(N * K)", "is_distractor": True},
            {"id": "C", "text": "O(N log N)", "is_distractor": True},
            {"id": "D", "text": "O(K)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The 3-step reversal algorithm (reverse entire array, reverse first $K$ elements, reverse remaining $N-K$ elements) achieves rotation in $O(N)$ time and $O(1)$ space.",
        "distractor_explanations": {
            "B": "Naive rotation shifting 1 element $K$ times takes $O(N \\times K)$.",
            "C": "No sorting is needed.",
            "D": "Every element must be repositioned, so lower bound is $\\Omega(N)$."
        },
        "a": 1.50,
        "b": 0.45,
        "point_biserial": 0.46
    },
    {
        "skill_code": "DSA_ARRAYS",
        "stem": "What is the amortized cost of inserting an element into a dynamic array (e.g. Python `list` or C++ `std::vector`) that doubles its capacity when full?",
        "options": [
            {"id": "A", "text": "O(1) amortized", "is_distractor": False},
            {"id": "B", "text": "O(N) amortized", "is_distractor": True},
            {"id": "C", "text": "O(log N) amortized", "is_distractor": True},
            {"id": "D", "text": "O(1) strict worst-case", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Doubling capacity spreads the $O(N)$ reallocation copy work over $N$ subsequent insertions. Total work for $N$ appends is $\\sum 2^k \\le 2N$, yielding $O(1)$ amortized cost per append.",
        "distractor_explanations": {
            "B": "The individual reallocation spike is $O(N)$, but the aggregate average is $O(1)$.",
            "C": "Capacity increases geometrically, making cost constant, not logarithmic.",
            "D": "The reallocation step takes $O(N)$ worst-case, so it is not $O(1)$ strict worst-case."
        },
        "a": 1.40,
        "b": -0.85,
        "point_biserial": 0.43
    },
    {
        "skill_code": "DSA_ARRAYS",
        "stem": "In the Dutch National Flag algorithm (3-way partitioning of 0s, 1s, and 2s), how many pointers are maintained to sort in a single pass?",
        "options": [
            {"id": "A", "text": "3 pointers: low, mid, high", "is_distractor": False},
            {"id": "B", "text": "2 pointers: left, right", "is_distractor": True},
            {"id": "C", "text": "4 pointers", "is_distractor": True},
            {"id": "D", "text": "1 pointer", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Dijkstra's Dutch National Flag algorithm uses `low`, `mid`, and `high` pointers to partition into three contiguous regions: $[0, low-1]$ (0s), $[low, mid-1]$ (1s), and $[high+1, N-1]$ (2s) in $O(N)$ time and $O(1)$ space.",
        "distractor_explanations": {
            "B": "Two pointers suffice for binary partition (0s and 1s), but 3 values require 3 pointers.",
            "C": "3 pointers are necessary and sufficient.",
            "D": "One pointer cannot partition three classes simultaneously."
        },
        "a": 1.60,
        "b": 0.90,
        "point_biserial": 0.48
    },

    # --- DSA_LINKED_LISTS (5 items) ---
    {
        "skill_code": "DSA_LINKED_LISTS",
        "stem": "Which algorithm detects a cycle in a Singly Linked List using $O(1)$ auxiliary space?",
        "options": [
            {"id": "A", "text": "Floyd's Tortoise and Hare (Slow/Fast Pointers)", "is_distractor": False},
            {"id": "B", "text": "Hash Set of visited node references", "is_distractor": True},
            {"id": "C", "text": "Breadth-First Search queue", "is_distractor": True},
            {"id": "D", "text": "Dijkstra's Shortest Path", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Floyd's Cycle-Finding Algorithm advances `slow` by 1 step and `fast` by 2 steps. If a cycle exists, they must collide inside the cycle in $O(N)$ time and $O(1)$ space.",
        "distractor_explanations": {
            "B": "Hash set achieves cycle detection in $O(N)$ time, but consumes $O(N)$ auxiliary space.",
            "C": "Queue consumes $O(N)$ memory.",
            "D": "Dijkstra's algorithm is for weighted shortest paths, not linked list cycle detection."
        },
        "a": 1.35,
        "b": -0.60,
        "point_biserial": 0.42
    },
    {
        "skill_code": "DSA_LINKED_LISTS",
        "stem": "What is the time complexity to find the $K$-th node from the end of a Singly Linked List of length $N$ in a single pass?",
        "options": [
            {"id": "A", "text": "O(N)", "is_distractor": False},
            {"id": "B", "text": "O(N^2)", "is_distractor": True},
            {"id": "C", "text": "O(log N)", "is_distractor": True},
            {"id": "D", "text": "O(K)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Advance a fast pointer $K$ steps ahead. Then advance slow and fast pointers together at identical speed until fast reaches the end. Slow will be at the $K$-th node from end in $O(N)$ time.",
        "distractor_explanations": {
            "B": "Two pointers avoid the naive quadratic search.",
            "C": "Linked lists lack random access, precluding logarithmic binary search.",
            "D": "The end of the list is at distance $N$, so $O(N)$ traversal is required."
        },
        "a": 1.45,
        "b": 0.20,
        "point_biserial": 0.45
    },
    {
        "skill_code": "DSA_LINKED_LISTS",
        "stem": "What is the primary advantage of a Doubly Linked List over a Singly Linked List?",
        "options": [
            {"id": "A", "text": "Deleting a given node given only its pointer can be accomplished in O(1) time without list traversal.", "is_distractor": False},
            {"id": "B", "text": "It uses less memory per node.", "is_distractor": True},
            {"id": "C", "text": "It allows O(1) random index access.", "is_distractor": True},
            {"id": "D", "text": "It eliminates the need for pointer management.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In a Doubly Linked List, every node has access to `node.prev` and `node.next`. Thus `node.prev.next = node.next` can be updated in $O(1)$ time without searching from head.",
        "distractor_explanations": {
            "B": "False: It requires an additional pointer per node, consuming MORE memory.",
            "C": "False: Linked lists cannot perform $O(1)$ random access.",
            "D": "False: Pointer management is more complex with two pointers."
        },
        "a": 1.40,
        "b": -0.40,
        "point_biserial": 0.43
    },
    {
        "skill_code": "DSA_LINKED_LISTS",
        "stem": "To reverse a Singly Linked List iteratively in place, how many pointer variables are required?",
        "options": [
            {"id": "A", "text": "3 pointers: prev, curr, next", "is_distractor": False},
            {"id": "B", "text": "1 pointer: curr", "is_distractor": True},
            {"id": "C", "text": "N pointers", "is_distractor": True},
            {"id": "D", "text": "0 pointers (pure recursion)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Standard iterative list reversal requires: `prev` (tracks reversed head), `curr` (node currently being redirected), and `next` (preserves remainder of original list before overwriting `curr.next`).",
        "distractor_explanations": {
            "B": "A single pointer cannot redirect backwards while simultaneously tracking forward progress.",
            "C": "Iterative reversal uses $O(1)$ space, not $O(N)$ pointers.",
            "D": "Pure recursion consumes $O(N)$ stack frames."
        },
        "a": 1.50,
        "b": 0.35,
        "point_biserial": 0.46
    },
    {
        "skill_code": "DSA_LINKED_LISTS",
        "stem": "In an unrolled linked list, each node stores:",
        "options": [
            {"id": "A", "text": "An array of elements rather than a single value, improving cache locality.", "is_distractor": False},
            {"id": "B", "text": "A binary search tree.", "is_distractor": True},
            {"id": "C", "text": "Only hash values.", "is_distractor": True},
            {"id": "D", "text": "Pointers to all subsequent nodes.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "An unrolled linked list is a variation where each node contains an array of elements. It drastically reduces pointer overhead and takes advantage of CPU L1/L2 cache locality.",
        "distractor_explanations": {
            "B": "Nodes store flat sequential arrays, not trees.",
            "C": "Nodes store actual data payloads.",
            "D": "Describes a skip list or fully connected structure."
        },
        "a": 1.65,
        "b": 1.15,
        "point_biserial": 0.49
    },

    # --- DSA_STACKS_QUEUES (5 items) ---
    {
        "skill_code": "DSA_STACKS_QUEUES",
        "stem": "Which data structure is optimal for solving the **Next Greater Element** problem for all elements of an array in $O(N)$ total time?",
        "options": [
            {"id": "A", "text": "Monotonic Stack", "is_distractor": False},
            {"id": "B", "text": "Min-Heap", "is_distractor": True},
            {"id": "C", "text": "Binary Search Tree", "is_distractor": True},
            {"id": "D", "text": "Circular Queue", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A monotonic decreasing stack maintains candidate greater elements. Each element is pushed and popped at most once, yielding $O(N)$ total linear time across the entire array.",
        "distractor_explanations": {
            "B": "A heap gives $O(N \\log N)$ time, sub-optimal compared to linear monotonic stack.",
            "C": "BST operations take $O(N \\log N)$ or $O(N^2)$ if unbalanced.",
            "D": "Queue FIFO ordering does not provide access to recent preceding candidates."
        },
        "a": 1.55,
        "b": 0.50,
        "point_biserial": 0.47
    },
    {
        "skill_code": "DSA_STACKS_QUEUES",
        "stem": "How can a Queue be implemented using two Stacks (Inbox and Outbox) to achieve $O(1)$ amortized `dequeue()`?",
        "options": [
            {"id": "A", "text": "Push to Inbox on enqueue; pop from Outbox on dequeue, refilling Outbox by popping all Inbox items only when Outbox is empty.", "is_distractor": False},
            {"id": "B", "text": "Transfer all elements between stacks on every single enqueue and dequeue.", "is_distractor": True},
            {"id": "C", "text": "Sort the inbox stack after every insertion.", "is_distractor": True},
            {"id": "D", "text": "Pop from both stacks simultaneously and take the minimum.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Each element is pushed to Inbox once, popped from Inbox to Outbox once, and popped from Outbox once. Total operations per element = 3, yielding $O(1)$ amortized cost.",
        "distractor_explanations": {
            "B": "Transferring every time degrades performance to $O(N)$ per operation.",
            "C": "Sorting is unnecessary and costly ($O(N \\log N)$).",
            "D": "Arbitrary comparison destroys FIFO queue order."
        },
        "a": 1.45,
        "b": -0.15,
        "point_biserial": 0.44
    },
    {
        "skill_code": "DSA_STACKS_QUEUES",
        "stem": "What is the minimum capacity required for a Circular Queue to distinguish between completely FULL and completely EMPTY conditions using `front` and `rear` pointers without an explicit size counter?",
        "options": [
            {"id": "A", "text": "One slot must be kept empty as a sentinel (capacity N holds at most N - 1 items).", "is_distractor": False},
            {"id": "B", "text": "The queue must be double the capacity.", "is_distractor": True},
            {"id": "C", "text": "front and rear must be initialized to -1.", "is_distractor": True},
            {"id": "D", "text": "Circular queues cannot be implemented without a counter.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Without a counter or boolean flag, `front == rear` signifies EMPTY, while `(rear + 1) % N == front` signifies FULL. This convention reserves one slot as an unfillable buffer.",
        "distractor_explanations": {
            "B": "Only 1 single unused slot is needed, not double capacity.",
            "C": "Initializing to -1 does not resolve ambiguity when indices wrap around.",
            "D": "Circular queues have used the 1-slot sentinel technique classically."
        },
        "a": 1.50,
        "b": 0.65,
        "point_biserial": 0.46
    },
    {
        "skill_code": "DSA_STACKS_QUEUES",
        "stem": "When evaluating the postfix expression `4 2 5 * + 1 -` using a stack, what is the final result?",
        "options": [
            {"id": "A", "text": "13", "is_distractor": False},
            {"id": "B", "text": "14", "is_distractor": True},
            {"id": "C", "text": "29", "is_distractor": True},
            {"id": "D", "text": "9", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Stack trace: Push 4, Push 2, Push 5. Operator `*`: pop 5, pop 2, push $2 \\times 5 = 10$. Operator `+`: pop 10, pop 4, push $4 + 10 = 14$. Push 1. Operator `-`: pop 1, pop 14, push $14 - 1 = 13$. Result = 13.",
        "distractor_explanations": {
            "B": "Forgot the final subtraction of 1.",
            "C": "Evaluated in incorrect order: $(4 + 2) \\times 5 - 1 = 29$.",
            "D": "Arithmetic error."
        },
        "a": 1.35,
        "b": -0.75,
        "point_biserial": 0.41
    },
    {
        "skill_code": "DSA_STACKS_QUEUES",
        "stem": "What is the time complexity to maintain the maximum element in a sliding window of size $K$ over an array of size $N$ using a Monotonic Double-Ended Queue (Deque)?",
        "options": [
            {"id": "A", "text": "O(N)", "is_distractor": False},
            {"id": "B", "text": "O(N * K)", "is_distractor": True},
            {"id": "C", "text": "O(N log K)", "is_distractor": True},
            {"id": "D", "text": "O(N^2)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In a monotonic decreasing deque, each array element is pushed to the back once and popped from the back/front at most once. Hence total work across the sliding window is $O(N)$ amortized.",
        "distractor_explanations": {
            "B": "Naive search in each window takes $O(N \\times K)$.",
            "C": "Max-heap achieves $O(N \\log K)$, but monotonic deque achieves $O(N)$.",
            "D": "Quadratic complexity represents brute force."
        },
        "a": 1.65,
        "b": 1.25,
        "point_biserial": 0.50
    },

    # =========================================================================
    # TOPIC 2: Trees & Hierarchies (15 items)
    # =========================================================================
    # --- DSA_BINARY_TREES (8 items) ---
    {
        "skill_code": "DSA_BINARY_TREES",
        "stem": "What is the maximum number of nodes in a binary tree of depth $H$ (where the root is at depth 0)?",
        "options": [
            {"id": "A", "text": "2^(H + 1) - 1", "is_distractor": False},
            {"id": "B", "text": "2^H", "is_distractor": True},
            {"id": "C", "text": "2^H - 1", "is_distractor": True},
            {"id": "D", "text": "2^(H - 1)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Sum of geometric progression: $\\sum_{i=0}^H 2^i = 2^{H+1} - 1$. For $H=0$, $2^1 - 1 = 1$ node (root).",
        "distractor_explanations": {
            "B": "Number of nodes at level $H$ only, not the cumulative total.",
            "C": "Off-by-one exponent error.",
            "D": "Nodes at level $H-1$."
        },
        "a": 1.35,
        "b": -0.80,
        "point_biserial": 0.42
    },
    {
        "skill_code": "DSA_BINARY_TREES",
        "stem": "Which tree traversal processes nodes level by level from top to bottom, left to right?",
        "options": [
            {"id": "A", "text": "Breadth-First Search (Level-Order Traversal)", "is_distractor": False},
            {"id": "B", "text": "In-Order Traversal", "is_distractor": True},
            {"id": "C", "text": "Pre-Order Traversal", "is_distractor": True},
            {"id": "D", "text": "Post-Order Traversal", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Level-order traversal uses a FIFO queue to visit all nodes at depth $d$ before proceeding to nodes at depth $d + 1$.",
        "distractor_explanations": {
            "B": "In-order visits Left, Root, Right recursively.",
            "C": "Pre-order visits Root, Left, Right in depth-first order.",
            "D": "Post-order visits Left, Right, Root in depth-first order."
        },
        "a": 1.25,
        "b": -1.20,
        "point_biserial": 0.40
    },
    {
        "skill_code": "DSA_BINARY_TREES",
        "stem": "Given the Pre-Order traversal `[A, B, D, E, C, F]` and In-Order traversal `[D, B, E, A, C, F]`, which node is the left child of `B`?",
        "options": [
            {"id": "A", "text": "D", "is_distractor": False},
            {"id": "B", "text": "E", "is_distractor": True},
            {"id": "C", "text": "A", "is_distractor": True},
            {"id": "D", "text": "C", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Pre-order identifies Root = A. In-order split: Left subtree = `[D, B, E]`, Right subtree = `[C, F]`. For `B` in In-order `[D, B, E]`, `D` is to the left of `B` (left child) and `E` is to the right (right child).",
        "distractor_explanations": {
            "B": "E is the right child of B.",
            "C": "A is the parent of B.",
            "D": "C is in the right subtree of the root A."
        },
        "a": 1.50,
        "b": 0.15,
        "point_biserial": 0.45
    },
    {
        "skill_code": "DSA_BINARY_TREES",
        "stem": "What is the **Diameter** of a binary tree?",
        "options": [
            {"id": "A", "text": "The length of the longest path between any two nodes in a tree, which may or may not pass through the root.", "is_distractor": False},
            {"id": "B", "text": "The total number of leaf nodes in the tree.", "is_distractor": True},
            {"id": "C", "text": "The distance from the root to the deepest leaf node.", "is_distractor": True},
            {"id": "D", "text": "The maximum number of nodes at any single level.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The diameter (or width) of a tree is defined as the number of edges (or nodes) on the longest path between any two arbitrary leaf or internal nodes.",
        "distractor_explanations": {
            "B": "Defines leaf count.",
            "C": "Defines tree height/depth.",
            "D": "Defines maximum tree breadth/width."
        },
        "a": 1.45,
        "b": -0.20,
        "point_biserial": 0.44
    },
    {
        "skill_code": "DSA_BINARY_TREES",
        "stem": "In Morris In-Order Traversal, how is $O(1)$ auxiliary space achieved without using recursion or an explicit stack?",
        "options": [
            {"id": "A", "text": "By establishing temporary threaded links from the in-order predecessor to the current node.", "is_distractor": False},
            {"id": "B", "text": "By storing parent pointers in each node.", "is_distractor": True},
            {"id": "C", "text": "By converting the tree into an array first.", "is_distractor": True},
            {"id": "D", "text": "By pruning leaf nodes as they are visited.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Morris Traversal creates a temporary thread from the rightmost node of the left subtree (in-order predecessor) pointing back to current, enabling backtrack without stack memory.",
        "distractor_explanations": {
            "B": "Nodes remain standard binary tree nodes without parent pointers.",
            "C": "Array storage would consume $O(N)$ space.",
            "D": "Tree structure is preserved and restored, not destroyed."
        },
        "a": 1.65,
        "b": 1.20,
        "point_biserial": 0.50
    },
    {
        "skill_code": "DSA_BINARY_TREES",
        "stem": "What is the Lowest Common Ancestor (LCA) of nodes `x` and `y` in a binary tree where both nodes are guaranteed to exist?",
        "options": [
            {"id": "A", "text": "The deepest node that has both x and y as descendants (where a node can be a descendant of itself).", "is_distractor": False},
            {"id": "B", "text": "The root of the binary tree always.", "is_distractor": True},
            {"id": "C", "text": "The parent of the root node.", "is_distractor": True},
            {"id": "D", "text": "The node with the lowest numeric key.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "LCA of $x$ and $y$ is formally defined as the lowest (deepest) node in $T$ that has both $x$ and $y$ as descendants.",
        "distractor_explanations": {
            "B": "Root is an ancestor, but not necessarily the lowest/deepest.",
            "C": "The root has no parent.",
            "D": "Key value is irrelevant in a general binary tree."
        },
        "a": 1.40,
        "b": 0.30,
        "point_biserial": 0.44
    },
    {
        "skill_code": "DSA_BINARY_TREES",
        "stem": "In a Full Binary Tree (where every node has either 0 or 2 children), if there are $L$ leaf nodes, how many internal nodes $I$ are there?",
        "options": [
            {"id": "A", "text": "I = L - 1", "is_distractor": False},
            {"id": "B", "text": "I = L + 1", "is_distractor": True},
            {"id": "C", "text": "I = 2L", "is_distractor": True},
            {"id": "D", "text": "I = L / 2", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "By mathematical induction on full binary trees: $L = I + 1$, which algebraically implies $I = L - 1$. Total nodes $N = 2L - 1$.",
        "distractor_explanations": {
            "B": "Sign error ($L = I + 1$, not $I = L + 1$).",
            "C": "Total nodes is roughly $2L$, but internal nodes is $L - 1$.",
            "D": "Incorrect ratio."
        },
        "a": 1.55,
        "b": 0.70,
        "point_biserial": 0.47
    },
    {
        "skill_code": "DSA_BINARY_TREES",
        "stem": "What is the time complexity of serializing and deserializing a binary tree of $N$ nodes using pre-order traversal with sentinel null markers?",
        "options": [
            {"id": "A", "text": "O(N) time and O(N) space", "is_distractor": False},
            {"id": "B", "text": "O(N log N) time", "is_distractor": True},
            {"id": "C", "text": "O(N^2) time", "is_distractor": True},
            {"id": "D", "text": "O(1) space", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Every node is visited once during pre-order serialization and reconstructed once during deserialization, with $N+1$ null markers. Time and space are strictly linear $O(N)$.",
        "distractor_explanations": {
            "B": "No comparison sorting is required.",
            "C": "Quadratic complexity is avoided by single-pass tokenization.",
            "D": "The serialized string and recursion stack require $O(N)$ space."
        },
        "a": 1.50,
        "b": 0.55,
        "point_biserial": 0.46
    },

    # --- DSA_BST (7 items) ---
    {
        "skill_code": "DSA_BST",
        "stem": "Which traversal of a valid Binary Search Tree (BST) produces the keys in strictly sorted ascending order?",
        "options": [
            {"id": "A", "text": "In-Order Traversal", "is_distractor": False},
            {"id": "B", "text": "Pre-Order Traversal", "is_distractor": True},
            {"id": "C", "text": "Post-Order Traversal", "is_distractor": True},
            {"id": "D", "text": "Level-Order Traversal", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "By definition of a BST, all keys in the left subtree are smaller than the root, and all keys in the right subtree are larger. In-Order visits Left, Root, Right, producing monotonic non-decreasing order.",
        "distractor_explanations": {
            "B": "Pre-order visits Root first, placing parent keys before left descendants.",
            "C": "Post-order visits children before parents.",
            "D": "Level-order traverses breadth-first across heights, not sorted by key value."
        },
        "a": 1.30,
        "b": -0.45,
        "point_biserial": 0.41
    },
    {
        "skill_code": "DSA_BST",
        "stem": "What is the worst-case time complexity of searching for an element in an **unbalanced** Binary Search Tree?",
        "options": [
            {"id": "A", "text": "O(N)", "is_distractor": False},
            {"id": "B", "text": "O(log N)", "is_distractor": True},
            {"id": "C", "text": "O(N log N)", "is_distractor": True},
            {"id": "D", "text": "O(1)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "If elements are inserted in monotonic sorted order, an unbalanced BST degenerates into a linear singly linked list of depth $N$, causing search time to degrade to $O(N)$.",
        "distractor_explanations": {
            "B": "$O(\\log N)$ applies only to balanced BSTs (like AVL or Red-Black trees).",
            "C": "Sorting complexity, not tree lookup.",
            "D": "Constant lookup is hash table performance, not tree search."
        },
        "a": 1.35,
        "b": -0.85,
        "point_biserial": 0.42
    },
    {
        "skill_code": "DSA_BST",
        "stem": "In an AVL Tree, what is the maximum permissible difference between the heights of the left and right subtrees of any node (Balance Factor)?",
        "options": [
            {"id": "A", "text": "1", "is_distractor": False},
            {"id": "B", "text": "0", "is_distractor": True},
            {"id": "C", "text": "2", "is_distractor": True},
            {"id": "D", "text": "log N", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The AVL invariant dictates that for every node, the balance factor $|Height(Left) - Height(Right)| \\le 1$. A balance factor of $\\pm 2$ triggers tree rotations.",
        "distractor_explanations": {
            "B": "A balance factor of 0 denotes a perfectly balanced tree, too strict to maintain efficiently.",
            "C": "A balance factor of 2 is an imbalance requiring immediate rebalancing rotations.",
            "D": "Height difference must be constant, not logarithmic."
        },
        "a": 1.50,
        "b": 0.40,
        "point_biserial": 0.45
    },
    {
        "skill_code": "DSA_BST",
        "stem": "When deleting a node with **two children** from a Binary Search Tree, what is the standard replacement node?",
        "options": [
            {"id": "A", "text": "In-order successor (smallest node in the right subtree) or in-order predecessor (largest in left subtree)", "is_distractor": False},
            {"id": "B", "text": "The root node of the entire tree", "is_distractor": True},
            {"id": "C", "text": "Any arbitrary leaf node", "is_distractor": True},
            {"id": "D", "text": "The rightmost child of the right subtree", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Replacing with the in-order successor or in-order predecessor preserves the fundamental BST property because all left subtree keys remain smaller and all right subtree keys remain larger.",
        "distractor_explanations": {
            "B": "Root cannot replace arbitrary sub-nodes without violating BST invariants.",
            "C": "Arbitrary leaf will violate BST ordering relations.",
            "D": "The rightmost node is the maximum key, which would violate ordering if placed as parent of remaining right children."
        },
        "a": 1.45,
        "b": 0.05,
        "point_biserial": 0.44
    },
    {
        "skill_code": "DSA_BST",
        "stem": "In a Red-Black Tree, what is the maximum possible height of a tree containing $N$ internal nodes?",
        "options": [
            {"id": "A", "text": "2 * log_2(N + 1)", "is_distractor": False},
            {"id": "B", "text": "log_2(N)", "is_distractor": True},
            {"id": "C", "text": "N", "is_distractor": True},
            {"id": "D", "text": "sqrt(N)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Because red nodes cannot have red children, the longest path from root to leaf (alternating red and black) is at most twice the length of the shortest path (all black), guaranteeing height $\\le 2 \\log_2(N + 1) = O(\\log N)$.",
        "distractor_explanations": {
            "B": "Height can exceed $\\log_2 N$ because Red-Black trees are less rigidly balanced than AVL trees.",
            "C": "Height cannot degrade to $O(N)$ due to color balancing invariants.",
            "D": "Height is strictly logarithmic, not square root."
        },
        "a": 1.65,
        "b": 1.30,
        "point_biserial": 0.50
    },
    {
        "skill_code": "DSA_BST",
        "stem": "Which rotation is required in an AVL tree when a new node is inserted into the left subtree of the right child of an unbalanced node (Right-Left case)?",
        "options": [
            {"id": "A", "text": "Right-Left double rotation (Right rotate on child, then Left rotate on parent)", "is_distractor": False},
            {"id": "B", "text": "Single Left rotation", "is_distractor": True},
            {"id": "C", "text": "Single Right rotation", "is_distractor": True},
            {"id": "D", "text": "Left-Right double rotation", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A zigzag Right-Left imbalance cannot be fixed by a single rotation. First, a Right rotation on the right child straightens the path into Right-Right, followed by a Left rotation on the parent.",
        "distractor_explanations": {
            "B": "Single Left rotation fixes only straight Right-Right imbalances.",
            "C": "Single Right rotation fixes Left-Left imbalances.",
            "D": "Left-Right rotation fixes the mirrored Left-Right case."
        },
        "a": 1.60,
        "b": 0.95,
        "point_biserial": 0.48
    },
    {
        "skill_code": "DSA_BST",
        "stem": "To validate whether a given binary tree is a valid BST, what range constraint must be verified recursively for node $X$ with allowed interval $(min, max)$?",
        "options": [
            {"id": "A", "text": "min < X.val < max, updating left recursive call with (min, X.val) and right with (X.val, max)", "is_distractor": False},
            {"id": "B", "text": "X.left.val < X.val and X.right.val > X.val locally at node X only", "is_distractor": True},
            {"id": "C", "text": "X.val > 0", "is_distractor": True},
            {"id": "D", "text": "X.left is not None", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Checking only direct parent-child relationships fails to detect deeper violations (e.g. a right child's left descendant smaller than root). Bounded interval propagation $(min, max)$ enforces global correctness in $O(N)$ time.",
        "distractor_explanations": {
            "B": "Classic trap: Local check misses ancestors' constraints.",
            "C": "BST keys can be negative.",
            "D": "Leaves and half-nodes are completely valid in BSTs."
        },
        "a": 1.55,
        "b": 0.60,
        "point_biserial": 0.47
    },

    # =========================================================================
    # TOPIC 3: Graphs & Algorithms (15 items)
    # =========================================================================
    # --- DSA_GRAPH_BFS_DFS (8 items) ---
    {
        "skill_code": "DSA_GRAPH_BFS_DFS",
        "stem": "What is the time complexity of Breadth-First Search (BFS) on a graph with $V$ vertices and $E$ edges represented by an **Adjacency List**?",
        "options": [
            {"id": "A", "text": "O(V + E)", "is_distractor": False},
            {"id": "B", "text": "O(V^2)", "is_distractor": True},
            {"id": "C", "text": "O(V * E)", "is_distractor": True},
            {"id": "D", "text": "O(E log V)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Every vertex is enqueued and dequeued at most once ($O(V)$), and its outgoing adjacency list is iterated over once ($O(E)$), totaling $O(V + E)$ time.",
        "distractor_explanations": {
            "B": "Adjacency Matrix representation requires $O(V^2)$, but Adjacency List is $O(V + E)$.",
            "C": "Vertices are visited once, avoiding $O(V \\times E)$.",
            "D": "Logarithmic factor occurs with priority queues in Dijkstra, not unweighted BFS."
        },
        "a": 1.30,
        "b": -0.70,
        "point_biserial": 0.41
    },
    {
        "skill_code": "DSA_GRAPH_BFS_DFS",
        "stem": "In an unweighted graph, which algorithm guarantees finding the shortest path (minimum edge count) between a source and destination?",
        "options": [
            {"id": "A", "text": "Breadth-First Search (BFS)", "is_distractor": False},
            {"id": "B", "text": "Depth-First Search (DFS)", "is_distractor": True},
            {"id": "C", "text": "Prim's Algorithm", "is_distractor": True},
            {"id": "D", "text": "Kruskal's Algorithm", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "BFS explores nodes in increasing order of distance from the source level by level, ensuring that the first time destination $D$ is popped from the queue, the path discovered has minimum edges.",
        "distractor_explanations": {
            "B": "DFS plunges arbitrarily deep and does not guarantee shortest paths.",
            "C": "Prim's finds Minimum Spanning Trees, not shortest paths.",
            "D": "Kruskal's finds Minimum Spanning Trees."
        },
        "a": 1.35,
        "b": -1.00,
        "point_biserial": 0.42
    },
    {
        "skill_code": "DSA_GRAPH_BFS_DFS",
        "stem": "What edge classification in a Depth-First Search (DFS) tree on a directed graph indicates the presence of a **directed cycle**?",
        "options": [
            {"id": "A", "text": "Back Edge", "is_distractor": False},
            {"id": "B", "text": "Forward Edge", "is_distractor": True},
            {"id": "C", "text": "Cross Edge", "is_distractor": True},
            {"id": "D", "text": "Tree Edge", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A back edge connects a vertex to an ancestor in the current DFS recursion stack. An edge pointing to an active ancestor completes a directed cycle.",
        "distractor_explanations": {
            "B": "Forward edges connect to a descendant already visited, not creating cycles.",
            "C": "Cross edges connect between parallel branches or trees.",
            "D": "Tree edges form the DFS spanning forest."
        },
        "a": 1.55,
        "b": 0.45,
        "point_biserial": 0.46
    },
    {
        "skill_code": "DSA_GRAPH_BFS_DFS",
        "stem": "What is the time complexity of Kahn's Algorithm (in-degree BFS) for Topological Sorting of a DAG with $V$ vertices and $E$ edges?",
        "options": [
            {"id": "A", "text": "O(V + E)", "is_distractor": False},
            {"id": "B", "text": "O(V^2)", "is_distractor": True},
            {"id": "C", "text": "O(E log V)", "is_distractor": True},
            {"id": "D", "text": "O(V log V)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Computing in-degrees takes $O(V + E)$. Enqueuing vertices with in-degree 0 and decrementing neighbors' in-degrees processes each edge and vertex once, achieving $O(V + E)$.",
        "distractor_explanations": {
            "B": "Adjacency matrix complexity.",
            "C": "Kahn's uses a standard queue, not a priority queue.",
            "D": "No sorting comparison is needed."
        },
        "a": 1.45,
        "b": 0.10,
        "point_biserial": 0.44
    },
    {
        "skill_code": "DSA_GRAPH_BFS_DFS",
        "stem": "How can 2-Colorability (Bipartiteness) of an undirected graph be tested efficiently?",
        "options": [
            {"id": "A", "text": "Run BFS/DFS and assign alternating colors (0 and 1) to adjacent nodes; if any edge connects two nodes of the same color, it is not bipartite.", "is_distractor": False},
            {"id": "B", "text": "Compute the Minimum Spanning Tree.", "is_distractor": True},
            {"id": "C", "text": "Check if total edge count is even.", "is_distractor": True},
            {"id": "D", "text": "Sort the degree sequence.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A graph is bipartite if and only if it contains no odd-length cycles. Standard BFS/DFS coloring diagnoses odd cycles in $O(V + E)$ time.",
        "distractor_explanations": {
            "B": "Every tree is bipartite, but MST does not determine if non-tree edges cause odd cycles.",
            "C": "Total edge parity is unrelated to cycle lengths.",
            "D": "Degree sequence does not characterize bipartiteness."
        },
        "a": 1.50,
        "b": 0.25,
        "point_biserial": 0.45
    },
    {
        "skill_code": "DSA_GRAPH_BFS_DFS",
        "stem": "In Tarjan's Strongly Connected Components (SCC) algorithm, what does `low[u]` represent?",
        "options": [
            {"id": "A", "text": "The lowest discovery time reachable from u using tree edges and at most one back edge.", "is_distractor": False},
            {"id": "B", "text": "The degree of vertex u.", "is_distractor": True},
            {"id": "C", "text": "The shortest path from root to u.", "is_distractor": True},
            {"id": "D", "text": "The number of children in u's DFS subtree.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "`low[u]` tracks the earliest visited vertex reachable from $u$'s subtree via back-edges. If `low[u] == disc[u]`, $u$ is the root of an SCC.",
        "distractor_explanations": {
            "B": "Degree is unhelpful for SCC cycle boundaries.",
            "C": "Shortest path is unrelated to DFS discovery times.",
            "D": "Subtree size is not the low-link value."
        },
        "a": 1.70,
        "b": 1.40,
        "point_biserial": 0.51
    },
    {
        "skill_code": "DSA_GRAPH_BFS_DFS",
        "stem": "What is an **Articulation Point** (Cut Vertex) in a connected undirected graph?",
        "options": [
            {"id": "A", "text": "A vertex whose removal increases the number of connected components in the graph.", "is_distractor": False},
            {"id": "B", "text": "A vertex with maximum degree.", "is_distractor": True},
            {"id": "C", "text": "A vertex connected to every other vertex.", "is_distractor": True},
            {"id": "D", "text": "A leaf node with degree 1.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "An articulation point is a critical bridge vertex. Removing it disconnects the graph into two or more disjoint components.",
        "distractor_explanations": {
            "B": "A hub vertex in a complete graph is not a cut vertex.",
            "C": "Defines a universal vertex.",
            "D": "Removing a degree 1 leaf never disconnects remaining nodes."
        },
        "a": 1.55,
        "b": 0.65,
        "point_biserial": 0.47
    },
    {
        "skill_code": "DSA_GRAPH_BFS_DFS",
        "stem": "What is the time complexity of Dijkstra's Algorithm implemented with a Min-Priority Queue (Binary Heap)?",
        "options": [
            {"id": "A", "text": "O((V + E) log V)", "is_distractor": False},
            {"id": "B", "text": "O(V^2)", "is_distractor": True},
            {"id": "C", "text": "O(V * E)", "is_distractor": True},
            {"id": "D", "text": "O(E^2)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Each vertex is extracted from the heap once ($O(V \\log V)$) and each edge can trigger a `decrease-key` / insertion ($O(E \\log V)$), totaling $O((V + E) \\log V)$.",
        "distractor_explanations": {
            "B": "Array implementation complexity without heap.",
            "C": "Bellman-Ford complexity.",
            "D": "Overestimates edge operations."
        },
        "a": 1.50,
        "b": 0.35,
        "point_biserial": 0.46
    },

    # --- DSA_DYNAMIC_PROG (7 items) ---
    {
        "skill_code": "DSA_DYNAMIC_PROG",
        "stem": "Which two core mathematical properties must a problem satisfy to be solvable via Dynamic Programming?",
        "options": [
            {"id": "A", "text": "Optimal Substructure and Overlapping Subproblems", "is_distractor": False},
            {"id": "B", "text": "Greedy Choice Property and Linearity", "is_distractor": True},
            {"id": "C", "text": "Associativity and Commutativity", "is_distractor": True},
            {"id": "D", "text": "Convexity and Differentiability", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Dynamic Programming requires: 1) Optimal Substructure (optimal solution to the problem contains optimal solutions to subproblems), and 2) Overlapping Subproblems (subproblems are computed repeatedly).",
        "distractor_explanations": {
            "B": "Defines greedy algorithms, not general dynamic programming.",
            "C": "Algebraic properties of operations.",
            "D": "Calculus/convex optimization properties."
        },
        "a": 1.35,
        "b": -0.65,
        "point_biserial": 0.42
    },
    {
        "skill_code": "DSA_DYNAMIC_PROG",
        "stem": "What is the time complexity of solving the **0/1 Knapsack Problem** with $N$ items and capacity $W$ using Dynamic Programming?",
        "options": [
            {"id": "A", "text": "O(N * W) (Pseudo-polynomial time)", "is_distractor": False},
            {"id": "B", "text": "O(2^N) strict polynomial time", "is_distractor": True},
            {"id": "C", "text": "O(N log W)", "is_distractor": True},
            {"id": "D", "text": "O(W^2)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The DP table has size $(N + 1) \\times (W + 1)$, filling each cell in $O(1)$ time, yielding $O(N \\times W)$. It is pseudo-polynomial because $W$ is proportional to $2^b$ where $b$ is the bit-length of capacity.",
        "distractor_explanations": {
            "B": "Brute force recursion is $O(2^N)$, which is exponential, not polynomial.",
            "C": "Dynamic programming fills a 2D table, not logarithmic.",
            "D": "Item count $N$ directly multiplies capacity $W$."
        },
        "a": 1.50,
        "b": 0.20,
        "point_biserial": 0.45
    },
    {
        "skill_code": "DSA_DYNAMIC_PROG",
        "stem": "What is the length of the Longest Common Subsequence (LCS) between strings **\"ABCDE\"** and **\"ACE\"**?",
        "options": [
            {"id": "A", "text": "3", "is_distractor": False},
            {"id": "B", "text": "2", "is_distractor": True},
            {"id": "C", "text": "4", "is_distractor": True},
            {"id": "D", "text": "5", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The characters 'A', 'C', 'E' appear in both strings in the exact same relative order. Hence \"ACE\" is a common subsequence of length 3.",
        "distractor_explanations": {
            "B": "Underestimates by missing 'E'.",
            "C": "Length cannot exceed length of the shorter string (3).",
            "D": "Length cannot exceed shorter string."
        },
        "a": 1.25,
        "b": -1.10,
        "point_biserial": 0.40
    },
    {
        "skill_code": "DSA_DYNAMIC_PROG",
        "stem": "What is the space-optimized auxiliary memory complexity for the Longest Common Subsequence of strings of lengths $M$ and $N$ when only the length is required?",
        "options": [
            {"id": "A", "text": "O(min(M, N))", "is_distractor": False},
            {"id": "B", "text": "O(M * N)", "is_distractor": True},
            {"id": "C", "text": "O(1)", "is_distractor": True},
            {"id": "D", "text": "O(M + N)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Computing row $i$ in the LCS table requires only the values from row $i - 1$. By keeping only two rows (current and previous) of size $\\min(M, N)$, memory reduces to $O(\\min(M, N))$.",
        "distractor_explanations": {
            "B": "Unoptimized full 2D matrix memory.",
            "C": "$O(1)$ is impossible because the preceding row must be maintained.",
            "D": "Two rows of the smaller string length are sufficient, $\\min(M, N)$."
        },
        "a": 1.60,
        "b": 0.80,
        "point_biserial": 0.48
    },
    {
        "skill_code": "DSA_DYNAMIC_PROG",
        "stem": "What is the optimal time complexity to find the **Longest Increasing Subsequence (LIS)** of an array of $N$ integers using Patience Sorting with binary search?",
        "options": [
            {"id": "A", "text": "O(N log N)", "is_distractor": False},
            {"id": "B", "text": "O(N^2)", "is_distractor": True},
            {"id": "C", "text": "O(N)", "is_distractor": True},
            {"id": "D", "text": "O(2^N)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "By maintaining an array of smallest tail elements of increasing subsequences, each of the $N$ elements is inserted using binary search (`bisect_left`) in $O(\\log N)$ time, yielding $O(N \\log N)$.",
        "distractor_explanations": {
            "B": "Standard $O(N^2)$ DP is improved to $O(N \\log N)$ via binary search.",
            "C": "Comparison lower bound is $\\Omega(N \\log N)$.",
            "D": "Brute force power set evaluation."
        },
        "a": 1.65,
        "b": 1.10,
        "point_biserial": 0.49
    },
    {
        "skill_code": "DSA_DYNAMIC_PROG",
        "stem": "In the Coin Change Problem (minimum coins to make amount $A$ with $N$ coin denominations), what is the optimal DP state transition?",
        "options": [
            {"id": "A", "text": "dp[a] = min(dp[a], 1 + dp[a - coin]) for all coins <= a", "is_distractor": False},
            {"id": "B", "text": "dp[a] = dp[a] + dp[a - coin]", "is_distractor": True},
            {"id": "C", "text": "dp[a] = max(dp[a], dp[a - coin])", "is_distractor": True},
            {"id": "D", "text": "dp[a] = a / max(coins)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "To minimize coins, the optimal choice among all eligible denominations is to take 1 coin and add the minimum coins needed for the remaining amount: $1 + dp[a - coin]$.",
        "distractor_explanations": {
            "B": "Computes total number of ways (combinations), not minimum coins.",
            "C": "Finds maximum coins, not minimum.",
            "D": "Greedy heuristic that fails for non-canonical coin systems."
        },
        "a": 1.45,
        "b": -0.10,
        "point_biserial": 0.44
    },
    {
        "skill_code": "DSA_DYNAMIC_PROG",
        "stem": "What is the time complexity of the Floyd-Warshall algorithm for All-Pairs Shortest Paths on a graph with $V$ vertices?",
        "options": [
            {"id": "A", "text": "O(V^3)", "is_distractor": False},
            {"id": "B", "text": "O(V^2)", "is_distractor": True},
            {"id": "C", "text": "O(V * E)", "is_distractor": True},
            {"id": "D", "text": "O(V^2 log V)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Floyd-Warshall executes three nested loops over vertices $k, i, j$ updating $dist[i][j] = \\min(dist[i][j], dist[i][k] + dist[k][j])$, requiring $O(V^3)$ time and $O(V^2)$ space.",
        "distractor_explanations": {
            "B": "Array size is $V^2$, but three nested loops over $V$ take $V^3$.",
            "C": "Bellman-Ford single-source complexity.",
            "D": "Dijkstra run from all vertices."
        },
        "a": 1.55,
        "b": 0.60,
        "point_biserial": 0.47
    }
]
