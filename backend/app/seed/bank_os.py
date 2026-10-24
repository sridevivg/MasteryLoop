"""
Operating Systems Question Bank.
Topic 1: Process Management (15 questions across OS_PROCESSES, OS_SCHEDULING, OS_SYNC_DEADLOCK)
Topic 2: Memory & Storage (15 questions across OS_VIRTUAL_MEM, OS_PAGE_REPLACE)
"""

OS_ITEMS = [
    # =========================================================================
    # TOPIC 1: Process Management (15 items)
    # =========================================================================
    # --- OS_PROCESSES (5 items) ---
    {
        "skill_code": "OS_PROCESSES",
        "stem": "What is the primary difference between a **Process** and a **Thread** in modern operating systems?",
        "options": [
            {"id": "A", "text": "A process has its own isolated address space and memory; threads within the same process share code, data, and heap segments but have private stacks.", "is_distractor": False},
            {"id": "B", "text": "Threads can only run sequentially on a single core; processes always run in parallel.", "is_distractor": True},
            {"id": "C", "text": "Threads have independent page tables; processes share page tables.", "is_distractor": True},
            {"id": "D", "text": "Processes are managed exclusively in user space without kernel awareness.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A process is a heavyweight execution environment with dedicated virtual memory address space. Threads are lightweight execution units within a process that share heap, globals, and open file descriptors, while retaining separate stack frames and registers.",
        "distractor_explanations": {
            "B": "Threads can execute simultaneously across multiple physical CPU cores.",
            "C": "Processes have private page tables; threads within a process share the same page table.",
            "D": "Processes are managed by the kernel via the Process Control Block (PCB)."
        },
        "a": 1.30,
        "b": -0.90,
        "point_biserial": 0.40
    },
    {
        "skill_code": "OS_PROCESSES",
        "stem": "In Unix-like systems, what does the `fork()` system call return to the parent process upon successful creation of a child process?",
        "options": [
            {"id": "A", "text": "The Process ID (PID) of the newly created child process", "is_distractor": False},
            {"id": "B", "text": "0", "is_distractor": True},
            {"id": "C", "text": "-1", "is_distractor": True},
            {"id": "D", "text": "The parent's own PID", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "`fork()` returns 0 to the child process and returns the positive child PID to the parent process. If fork fails, it returns -1.",
        "distractor_explanations": {
            "B": "0 is returned to the child process, not the parent.",
            "C": "-1 is returned only if the fork call fails.",
            "D": "The parent already knows its own PID via `getpid()`."
        },
        "a": 1.45,
        "b": -0.25,
        "point_biserial": 0.44
    },
    {
        "skill_code": "OS_PROCESSES",
        "stem": "What is a **Zombie Process** in Unix?",
        "options": [
            {"id": "A", "text": "A terminated process whose entry remains in the process table because its parent has not yet read its exit status via `wait()`.", "is_distractor": False},
            {"id": "B", "text": "A process that runs infinitely without consuming CPU cycles.", "is_distractor": True},
            {"id": "C", "text": "A process whose parent terminated, leaving it adopted by PID 1 (init/systemd).", "is_distractor": True},
            {"id": "D", "text": "A process in the blocked I/O state.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "When a child process exits, its memory is reclaimed, but its PCB remains in the process table to hold the return code until the parent calls `wait()` or `waitpid()`. During this interval, it is a Zombie.",
        "distractor_explanations": {
            "B": "Infinite loops are active or sleeping processes, not zombies.",
            "C": "Defines an Orphan Process, which is adopted by init.",
            "D": "Blocked I/O processes are in sleeping/waiting state."
        },
        "a": 1.40,
        "b": 0.15,
        "point_biserial": 0.43
    },
    {
        "skill_code": "OS_PROCESSES",
        "stem": "What hardware and software state must be saved and restored during a **Context Switch** between two threads?",
        "options": [
            {"id": "A", "text": "Program Counter (PC), CPU general-purpose registers, stack pointer (SP), and floating-point registers", "is_distractor": False},
            {"id": "B", "text": "The entire contents of the RAM memory modules", "is_distractor": True},
            {"id": "C", "text": "The hard drive file system journal", "is_distractor": True},
            {"id": "D", "text": "Only the thread ID string", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Context switching preserves the active CPU execution state: the program counter (instruction pointer), CPU register file, stack pointer, and processor flags are written into the Thread Control Block (TCB).",
        "distractor_explanations": {
            "B": "RAM contents remain in physical memory; only registers and stack pointers are swapped.",
            "C": "Disk journals are unrelated to thread register context.",
            "D": "Saving only thread ID would lose execution state and instruction pointers."
        },
        "a": 1.50,
        "b": 0.50,
        "point_biserial": 0.46
    },
    {
        "skill_code": "OS_PROCESSES",
        "stem": "Which Inter-Process Communication (IPC) mechanism provides the fastest data exchange between two processes on the same host?",
        "options": [
            {"id": "A", "text": "Shared Memory", "is_distractor": False},
            {"id": "B", "text": "UNIX Domain Sockets", "is_distractor": True},
            {"id": "C", "text": "Pipes", "is_distractor": True},
            {"id": "D", "text": "Message Queues", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Shared memory maps the same physical memory frames into the address spaces of multiple processes. Once mapped, communication occurs at native memory bus speeds without kernel intervention or data copying.",
        "distractor_explanations": {
            "B": "Sockets involve kernel buffer copying and context switches.",
            "C": "Pipes require copying data from user space to kernel space and back.",
            "D": "Message queues incur kernel system call overhead."
        },
        "a": 1.55,
        "b": 0.85,
        "point_biserial": 0.48
    },

    # --- OS_SCHEDULING (5 items) ---
    {
        "skill_code": "OS_SCHEDULING",
        "stem": "Which CPU scheduling algorithm minimizes the average waiting time for a given set of stationary processes?",
        "options": [
            {"id": "A", "text": "Shortest Job First (SJF) / Shortest Remaining Time First (SRTF)", "is_distractor": False},
            {"id": "B", "text": "First-Come, First-Served (FCFS)", "is_distractor": True},
            {"id": "C", "text": "Round Robin (RR)", "is_distractor": True},
            {"id": "D", "text": "Priority Scheduling without aging", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "SJF is provably optimal in minimizing average waiting time because scheduling short bursts earlier moves more processes out of the waiting queue faster.",
        "distractor_explanations": {
            "B": "FCFS suffers from the Convoy Effect where short jobs wait behind a long burst.",
            "C": "Round Robin favors responsiveness, not minimum average waiting time.",
            "D": "Priority scheduling can lead to indefinite starvation of low-priority jobs."
        },
        "a": 1.35,
        "b": -0.75,
        "point_biserial": 0.42
    },
    {
        "skill_code": "OS_SCHEDULING",
        "stem": "What is the **Convoy Effect** in operating system CPU scheduling?",
        "options": [
            {"id": "A", "text": "Short CPU-bound or I/O-bound processes are delayed behind a single large CPU-intensive process in FCFS scheduling.", "is_distractor": False},
            {"id": "B", "text": "Processes form a cyclic deadlock dependency.", "is_distractor": True},
            {"id": "C", "text": "Context switches consume more time than actual CPU execution.", "is_distractor": True},
            {"id": "D", "text": "Multiple threads simultaneously write to a shared cache line.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The convoy effect occurs in non-preemptive FCFS when many short, quick processes queue up behind a lengthy CPU-hogging task, severely depressing device and CPU utilization.",
        "distractor_explanations": {
            "B": "Describes a deadlock.",
            "C": "Describes thrashing or excessive context-switching overhead.",
            "D": "Describes false sharing in multi-core caches."
        },
        "a": 1.40,
        "b": -0.20,
        "point_biserial": 0.43
    },
    {
        "skill_code": "OS_SCHEDULING",
        "stem": "In Round Robin scheduling, what happens if the time quantum (slice) is set to an extremely large value?",
        "options": [
            {"id": "A", "text": "It degenerates into First-Come, First-Served (FCFS) scheduling.", "is_distractor": False},
            {"id": "B", "text": "It degenerates into Shortest Job First (SJF).", "is_distractor": True},
            {"id": "C", "text": "The CPU halts due to timer interrupt failure.", "is_distractor": True},
            {"id": "D", "text": "Context switch overhead increases exponentially.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "If the time quantum exceeds the longest process burst time, no process is ever preempted by the timer. Each process runs to completion in arrival order, making it identical to FCFS.",
        "distractor_explanations": {
            "B": "SJF orders by burst length, whereas RR respects arrival order.",
            "C": "Timer interrupts simply fire less frequently; the CPU does not halt.",
            "D": "Context switch overhead decreases with larger quanta."
        },
        "a": 1.45,
        "b": 0.10,
        "point_biserial": 0.44
    },
    {
        "skill_code": "OS_SCHEDULING",
        "stem": "How does the technique of **Aging** solve the problem of process starvation in priority scheduling?",
        "options": [
            {"id": "A", "text": "By gradually increasing the priority of processes that wait in the ready queue for long durations.", "is_distractor": False},
            {"id": "B", "text": "By terminating old processes automatically after a fixed timeout.", "is_distractor": True},
            {"id": "C", "text": "By allocating larger time slices to older processes.", "is_distractor": True},
            {"id": "D", "text": "By moving older processes to disk swap space.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Aging dynamically elevates a waiting process's priority over time. Eventually, even the lowest-priority process becomes the highest-priority task and gains the CPU.",
        "distractor_explanations": {
            "B": "Termination destroys uncompleted work, which is not scheduling resolution.",
            "C": "Starvation is about not getting CPU at all, not the quantum duration.",
            "D": "Swapping to disk would exacerbate delays."
        },
        "a": 1.50,
        "b": 0.40,
        "point_biserial": 0.45
    },
    {
        "skill_code": "OS_SCHEDULING",
        "stem": "In the Linux Completely Fair Scheduler (CFS), on what metric are tasks prioritized for execution?",
        "options": [
            {"id": "A", "text": "Virtual Runtime (`vruntime`), selecting the task with the minimum `vruntime` via a red-black tree.", "is_distractor": False},
            {"id": "B", "text": "Simple priority queues 0 to 139.", "is_distractor": True},
            {"id": "C", "text": "Process memory footprint.", "is_distractor": True},
            {"id": "D", "text": "Shortest remaining code line count.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "CFS models an 'ideal multi-tasking CPU'. Each task tracks `vruntime` (normalized execution time scaled by nice value). CFS always picks the task with smallest `vruntime` in $O(\\log N)$ time using a red-black tree.",
        "distractor_explanations": {
            "B": "Priority array with active/expired lists was used in the older Linux O(1) scheduler.",
            "C": "Memory size is irrelevant to CPU scheduling fairness.",
            "D": "Source code lines are unknown to the kernel."
        },
        "a": 1.65,
        "b": 1.10,
        "point_biserial": 0.49
    },

    # --- OS_SYNC_DEADLOCK (5 items) ---
    {
        "skill_code": "OS_SYNC_DEADLOCK",
        "stem": "Which of the following is NOT one of Coffman's four necessary conditions for a Deadlock to occur?",
        "options": [
            {"id": "A", "text": "Preemption allowed (Resource Preemption)", "is_distractor": False},
            {"id": "B", "text": "Mutual Exclusion", "is_distractor": True},
            {"id": "C", "text": "Hold and Wait", "is_distractor": True},
            {"id": "D", "text": "Circular Wait", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Coffman's four necessary conditions are: 1) Mutual Exclusion, 2) Hold and Wait, 3) **No Preemption** (resources cannot be forcibly taken), and 4) Circular Wait. If preemption is allowed, deadlocks can be broken.",
        "distractor_explanations": {
            "B": "Mutual exclusion is a mandatory Coffman condition.",
            "C": "Hold and wait is a mandatory Coffman condition.",
            "D": "Circular wait is a mandatory Coffman condition."
        },
        "a": 1.40,
        "b": 0.10,
        "point_biserial": 0.43
    },
    {
        "skill_code": "OS_SYNC_DEADLOCK",
        "stem": "What is the primary difference between a **Mutex** and a **Counting Semaphore**?",
        "options": [
            {"id": "A", "text": "A mutex is a locking mechanism with ownership (only the thread that locked it can unlock it); a semaphore is a signaling mechanism with a counter.", "is_distractor": False},
            {"id": "B", "text": "A mutex can be accessed by multiple threads concurrently, whereas a semaphore is strictly binary.", "is_distractor": True},
            {"id": "C", "text": "Semaphores cannot cause deadlocks.", "is_distractor": True},
            {"id": "D", "text": "Mutexes are implemented entirely in user-space without kernel primitives.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A mutex has an owner: thread A locks it, and thread A must unlock it. A counting semaphore maintains an integer count representing resource permits, and any thread can post/signal.",
        "distractor_explanations": {
            "B": "A mutex is strictly binary (single owner), while counting semaphores allow multiple concurrent permits.",
            "C": "Semaphores can easily cause deadlocks if wait/signal sequences are inverted.",
            "D": "Fast user-space mutexes (futex) use kernel assistance when contested."
        },
        "a": 1.50,
        "b": 0.30,
        "point_biserial": 0.45
    },
    {
        "skill_code": "OS_SYNC_DEADLOCK",
        "stem": "In Dijkstra's **Banker's Algorithm** for Deadlock Avoidance, what does a \"Safe State\" mean?",
        "options": [
            {"id": "A", "text": "There exists at least one allocation sequence that allows every process to obtain its maximum declared resources and complete without deadlocking.", "is_distractor": False},
            {"id": "B", "text": "All processes currently have zero allocated resources.", "is_distractor": True},
            {"id": "C", "text": "No resource can ever be requested again.", "is_distractor": True},
            {"id": "D", "text": "The operating system has terminated all background processes.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A state is safe if the system can allocate resources up to each process's maximum declared limit in some safe sequence $P_1, P_2, \\dots, P_n$ such that everyone finishes.",
        "distractor_explanations": {
            "B": "Resources are actively allocated in a safe state.",
            "C": "Processes continue requesting resources up to their maximum claims.",
            "D": "Processes complete normally without premature termination."
        },
        "a": 1.60,
        "b": 0.80,
        "point_biserial": 0.47
    },
    {
        "skill_code": "OS_SYNC_DEADLOCK",
        "stem": "What is **Priority Inversion** in real-time operating systems?",
        "options": [
            {"id": "A", "text": "A high-priority task is indirectly preempted by a low-priority task because a medium-priority task preempts the low-priority task holding a shared lock.", "is_distractor": False},
            {"id": "B", "text": "The scheduler inverts priorities randomly to prevent starvation.", "is_distractor": True},
            {"id": "C", "text": "High priority tasks execute in reverse FIFO order.", "is_distractor": True},
            {"id": "D", "text": "A low-priority task terminates a high-priority task.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Priority inversion famously occurred on the Mars Pathfinder: High task $H$ waits for a mutex held by Low task $L$. Medium task $M$ (not needing the lock) preempts $L$. Thus $M$ indirectly delays $H$ indefinitely.",
        "distractor_explanations": {
            "B": "Priority inversion is an unintended concurrency hazard, not an intentional scheduling strategy.",
            "C": "Does not refer to reverse FIFO execution.",
            "D": "Tasks do not terminate each other."
        },
        "a": 1.65,
        "b": 1.25,
        "point_biserial": 0.50
    },
    {
        "skill_code": "OS_SYNC_DEADLOCK",
        "stem": "Which protocol eliminates priority inversion by temporarily elevating the priority of a low-priority lock holder to that of the highest-priority task waiting for the lock?",
        "options": [
            {"id": "A", "text": "Priority Inheritance Protocol", "is_distractor": False},
            {"id": "B", "text": "Round Robin Protocol", "is_distractor": True},
            {"id": "C", "text": "Peterson's Algorithm", "is_distractor": True},
            {"id": "D", "text": "Lamport's Bakery Algorithm", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Under Priority Inheritance, while high-priority task $H$ is blocked waiting for lock held by low task $L$, task $L$ inherits $H$'s high priority, preventing medium tasks from preempting $L$.",
        "distractor_explanations": {
            "B": "Round Robin does not address priority inversion.",
            "C": "Peterson's algorithm is a two-process mutual exclusion algorithm.",
            "D": "Bakery algorithm is an $N$-process mutual exclusion algorithm."
        },
        "a": 1.55,
        "b": 0.65,
        "point_biserial": 0.46
    },

    # =========================================================================
    # TOPIC 2: Memory & Storage (15 items)
    # =========================================================================
    # --- OS_VIRTUAL_MEM (8 items) ---
    {
        "skill_code": "OS_VIRTUAL_MEM",
        "stem": "What hardware component is responsible for translating Virtual Memory Addresses into Physical Memory Addresses?",
        "options": [
            {"id": "A", "text": "Memory Management Unit (MMU)", "is_distractor": False},
            {"id": "B", "text": "Direct Memory Access (DMA) Controller", "is_distractor": True},
            {"id": "C", "text": "Arithmetic Logic Unit (ALU)", "is_distractor": True},
            {"id": "D", "text": "Graphics Processing Unit (GPU)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The MMU contains the TLB and hardware page table walkers, translating virtual addresses generated by CPU execution into physical bus addresses on the fly.",
        "distractor_explanations": {
            "B": "DMA handles device I/O transfers without CPU intervention.",
            "C": "ALU performs integer arithmetic and bitwise calculations.",
            "D": "GPU performs parallel vector graphics and tensor computation."
        },
        "a": 1.30,
        "b": -0.85,
        "point_biserial": 0.41
    },
    {
        "skill_code": "OS_VIRTUAL_MEM",
        "stem": "What is the function of a **Translation Lookaside Buffer (TLB)** in virtual memory?",
        "options": [
            {"id": "A", "text": "A high-speed hardware cache of recent virtual-to-physical page table translations, avoiding main memory page table lookups.", "is_distractor": False},
            {"id": "B", "text": "A buffer for disk I/O write operations.", "is_distractor": True},
            {"id": "C", "text": "A stack holding return addresses for function calls.", "is_distractor": True},
            {"id": "D", "text": "A swap partition manager on SSDs.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Because page tables reside in main memory (requiring multiple RAM accesses for multi-level tables), the TLB provides an associative cache that resolves addresses in sub-nanosecond clock cycles.",
        "distractor_explanations": {
            "B": "Describes the OS page cache or disk buffer pool.",
            "C": "Describes the call stack.",
            "D": "Swap management is a kernel software subsystem."
        },
        "a": 1.45,
        "b": -0.30,
        "point_biserial": 0.44
    },
    {
        "skill_code": "OS_VIRTUAL_MEM",
        "stem": "What is a **Page Fault** in an operating system?",
        "options": [
            {"id": "A", "text": "A hardware interrupt raised by the MMU when a program accesses a virtual page whose 'present bit' is 0 (not loaded in physical RAM).", "is_distractor": False},
            {"id": "B", "text": "A physical RAM hardware failure resulting in corrupted bits.", "is_distractor": True},
            {"id": "C", "text": "An error when a hard disk runs out of storage space.", "is_distractor": True},
            {"id": "D", "text": "An invalid instruction opcode detected by the decoder.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "When the CPU references a page with present bit = 0, the MMU triggers a page fault trap. The OS kernel traps the exception, fetches the page from disk swap, updates the page table, and resumes execution.",
        "distractor_explanations": {
            "B": "Hardware bit corruption is an ECC RAM error or machine check exception.",
            "C": "Disk space exhaustion produces `ENOSPC`, not a page fault.",
            "D": "Illegal opcodes produce SIGILL / undefined instruction exceptions."
        },
        "a": 1.40,
        "b": -0.55,
        "point_biserial": 0.43
    },
    {
        "skill_code": "OS_VIRTUAL_MEM",
        "stem": "What is the difference between **Internal Fragmentation** and **External Fragmentation**?",
        "options": [
            {"id": "A", "text": "Internal fragmentation occurs when allocated memory blocks are larger than requested; external fragmentation occurs when free memory is broken into unusable small scattered chunks.", "is_distractor": False},
            {"id": "B", "text": "Internal fragmentation occurs in disk drives; external fragmentation occurs in RAM.", "is_distractor": True},
            {"id": "C", "text": "Internal fragmentation can be solved by paging; external fragmentation cannot.", "is_distractor": True},
            {"id": "D", "text": "They are synonymous terms for cache line misses.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Internal fragmentation is wasted space inside an allocated fixed-size block/page. External fragmentation occurs when total free memory is sufficient for a request, but no single contiguous block is large enough.",
        "distractor_explanations": {
            "B": "Both forms occur across both RAM and storage.",
            "C": "Paging eliminates external fragmentation, but still suffers from internal fragmentation on the last page.",
            "D": "Cache misses are memory hierarchy latency events, not fragmentation."
        },
        "a": 1.50,
        "b": 0.20,
        "point_biserial": 0.45
    },
    {
        "skill_code": "OS_VIRTUAL_MEM",
        "stem": "In a 32-bit architecture with 4 KB ($2^{12}$ bytes) page size, how many total virtual pages are there in a process's virtual address space?",
        "options": [
            {"id": "A", "text": "2^20 (1,048,576 pages)", "is_distractor": False},
            {"id": "B", "text": "2^32 pages", "is_distractor": True},
            {"id": "C", "text": "2^12 pages", "is_distractor": True},
            {"id": "D", "text": "4,096 pages", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Virtual address space is $2^{32}$ bytes. Each page is $4 \\text{ KB} = 2^{12}$ bytes. Number of virtual pages = $\\frac{2^{32}}{2^{12}} = 2^{20} = 1,048,576$ pages. The lower 12 bits represent the page offset, and the upper 20 bits index the page table.",
        "distractor_explanations": {
            "B": "Total byte count, not page count.",
            "C": "Size of the offset, not the number of pages.",
            "D": "Size of page in bytes, not page count."
        },
        "a": 1.55,
        "b": 0.55,
        "point_biserial": 0.46
    },
    {
        "skill_code": "OS_VIRTUAL_MEM",
        "stem": "Why are **Multi-Level Page Tables** used instead of a single flat linear page table on 64-bit architectures?",
        "options": [
            {"id": "A", "text": "To avoid allocating memory for non-existent or unmapped address ranges, dramatically reducing page table memory footprint.", "is_distractor": False},
            {"id": "B", "text": "To increase TLB hit ratios.", "is_distractor": True},
            {"id": "C", "text": "To eliminate the need for an MMU.", "is_distractor": True},
            {"id": "D", "text": "To allow page sizes to vary randomly on every memory write.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A flat page table for a 64-bit address space would require exabytes of memory just to store page table entries. Multi-level tables create intermediate directories, omitting subtrees for unallocated virtual space.",
        "distractor_explanations": {
            "B": "Multi-level tables actually increase lookup latency on TLB misses (requiring 4 to 5 memory hops).",
            "C": "The MMU is required to walk multi-level page tables.",
            "D": "Page sizes are fixed (e.g. 4KB, 2MB hugepages)."
        },
        "a": 1.65,
        "b": 1.15,
        "point_biserial": 0.49
    },
    {
        "skill_code": "OS_VIRTUAL_MEM",
        "stem": "What is **Thrashing** in virtual memory systems?",
        "options": [
            {"id": "A", "text": "A pathological state where the OS spends almost all its time swapping pages in and out of disk rather than executing user instructions.", "is_distractor": False},
            {"id": "B", "text": "Rapid CPU overclocking under heavy computational load.", "is_distractor": True},
            {"id": "C", "text": "Writing corrupted data to SSD blocks repeatedly.", "is_distractor": True},
            {"id": "D", "text": "Clearing the TLB cache on every context switch.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Thrashing occurs when the sum of working sets of active processes exceeds physical memory. Every page brought in evicts another needed page immediately, collapsing CPU utilization near zero.",
        "distractor_explanations": {
            "B": "Thrashing collapses CPU utilization, leaving CPU idle waiting on disk.",
            "C": "Thrashing involves valid swap writes, not hardware corruption.",
            "D": "TLB flushing occurs on address space changes, but is not called thrashing."
        },
        "a": 1.45,
        "b": -0.10,
        "point_biserial": 0.44
    },
    {
        "skill_code": "OS_VIRTUAL_MEM",
        "stem": "What is the **Working Set Model** designed to prevent?",
        "options": [
            {"id": "A", "text": "Thrashing, by ensuring a process is only scheduled if its entire active working set of pages fits in physical memory.", "is_distractor": False},
            {"id": "B", "text": "Deadlocks in multi-threaded code.", "is_distractor": True},
            {"id": "C", "text": "Stack overflow exceptions in recursion.", "is_distractor": True},
            {"id": "D", "text": "Hardware CPU overheating.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Peter Denning's Working Set Model defines $W(t, \\Delta)$ as the set of pages referenced in the last $\\Delta$ time units. If total working sets exceed RAM, the OS suspends a process to prevent thrashing.",
        "distractor_explanations": {
            "B": "Deadlocks are solved via Banker's algorithm or lock ordering.",
            "C": "Stack overflow is handled by guard pages and recursion depth limits.",
            "D": "Thermal throttling manages overheating."
        },
        "a": 1.60,
        "b": 0.85,
        "point_biserial": 0.48
    },

    # --- OS_PAGE_REPLACE (7 items) ---
    {
        "skill_code": "OS_PAGE_REPLACE",
        "stem": "What is **Bélády's Anomaly** in page replacement algorithms?",
        "options": [
            {"id": "A", "text": "For FIFO page replacement, increasing the number of physical page frames can paradoxically increase the number of page faults.", "is_distractor": False},
            {"id": "B", "text": "LRU page replacement fails on prime-numbered frames.", "is_distractor": True},
            {"id": "C", "text": "Optimal page replacement takes exponential time.", "is_distractor": True},
            {"id": "D", "text": "Disk swap space cannot exceed RAM capacity.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Bélády proved in 1969 that FIFO is not a stack algorithm; allocating more page frames (e.g. from 3 to 4 frames) on certain reference strings increases page faults (e.g. from 9 to 10 faults).",
        "distractor_explanations": {
            "B": "LRU is a stack algorithm and is mathematically immune to Bélády's Anomaly.",
            "C": "Optimal page replacement (MIN) requires future knowledge, but is not exponential.",
            "D": "Swap space routinely exceeds physical RAM size."
        },
        "a": 1.55,
        "b": 0.60,
        "point_biserial": 0.47
    },
    {
        "skill_code": "OS_PAGE_REPLACE",
        "stem": "How does the **Least Recently Used (LRU)** page replacement algorithm select a victim page for eviction?",
        "options": [
            {"id": "A", "text": "It evicts the page that has not been referenced for the longest period of time.", "is_distractor": False},
            {"id": "B", "text": "It evicts the oldest page brought into memory regardless of recent access.", "is_distractor": True},
            {"id": "C", "text": "It evicts the page that will not be used for the longest time in the future.", "is_distractor": True},
            {"id": "D", "text": "It evicts the page with the smallest memory size.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "LRU uses past temporal locality as a predictor of future access: the frame whose last access timestamp is the oldest is evicted.",
        "distractor_explanations": {
            "B": "Describes FIFO (First-In, First-Out).",
            "C": "Describes the theoretical Optimal (MIN) algorithm.",
            "D": "All pages have identical fixed sizes."
        },
        "a": 1.35,
        "b": -0.80,
        "point_biserial": 0.42
    },
    {
        "skill_code": "OS_PAGE_REPLACE",
        "stem": "Why cannot the **Optimal Page Replacement Algorithm (MIN/OPT)** be implemented in practical general-purpose operating systems?",
        "options": [
            {"id": "A", "text": "It requires impossible prescient knowledge of future page reference sequences.", "is_distractor": False},
            {"id": "B", "text": "It produces more page faults than FIFO.", "is_distractor": True},
            {"id": "C", "text": "It requires more than 64-bit address registers.", "is_distractor": True},
            {"id": "D", "text": "It is patented and legally restricted.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Bélády's OPT algorithm evicts the page that will not be referenced for the longest duration in the future. Because OS schedulers cannot predict future software execution paths, it serves only as a theoretical benchmark.",
        "distractor_explanations": {
            "B": "OPT provably produces the lowest possible number of page faults.",
            "C": "Word size is independent of the algorithm.",
            "D": "The obstacle is physical causality, not intellectual property."
        },
        "a": 1.40,
        "b": -0.45,
        "point_biserial": 0.43
    },
    {
        "skill_code": "OS_PAGE_REPLACE",
        "stem": "How does the **Clock (Second-Chance) Algorithm** approximate LRU efficiently in hardware/software?",
        "options": [
            {"id": "A", "text": "It maintains a circular list of frames with a reference bit; when sweeping, if bit=1 it clears to 0 and advances; if bit=0, it selects that frame as victim.", "is_distractor": False},
            {"id": "B", "text": "It reads the hardware real-time clock on every memory access.", "is_distractor": True},
            {"id": "C", "text": "It evicts pages on a fixed timer every 10 milliseconds.", "is_distractor": True},
            {"id": "D", "text": "It sorts all memory frames by creation timestamp using quicksort.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The Clock algorithm avoids costly timestamp maintenance on every read. A single 'reference bit' is set by MMU hardware on access. The clock hand gives pages a second chance before choosing a victim with bit=0.",
        "distractor_explanations": {
            "B": "Reading hardware clock on every memory access would destroy memory bus performance.",
            "C": "Eviction is triggered by page faults upon need, not arbitrary timers.",
            "D": "Sorting frames would be unacceptably slow."
        },
        "a": 1.50,
        "b": 0.35,
        "point_biserial": 0.45
    },
    {
        "skill_code": "OS_PAGE_REPLACE",
        "stem": "Given page reference string `1, 2, 3, 4, 1, 2` with 3 initially empty page frames using FIFO, how many total page faults occur?",
        "options": [
            {"id": "A", "text": "6 page faults", "is_distractor": False},
            {"id": "B", "text": "4 page faults", "is_distractor": True},
            {"id": "C", "text": "5 page faults", "is_distractor": True},
            {"id": "D", "text": "3 page faults", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Frames start empty []. Ref 1: Fault -> [1]. Ref 2: Fault -> [1, 2]. Ref 3: Fault -> [1, 2, 3]. Ref 4: Fault (evicts 1) -> [2, 3, 4]. Ref 1: Fault (evicts 2) -> [3, 4, 1]. Ref 2: Fault (evicts 3) -> [4, 1, 2]. All 6 references fault.",
        "distractor_explanations": {
            "B": "Missed the evictions of 1 and 2.",
            "C": "Miscalculated one hit.",
            "D": "Counted only initial cold misses."
        },
        "a": 1.55,
        "b": 0.70,
        "point_biserial": 0.47
    },
    {
        "skill_code": "OS_PAGE_REPLACE",
        "stem": "Why does the Enhanced Second-Chance algorithm consider both the **Reference Bit** and the **Dirty (Modify) Bit** $(R, M)$ when selecting an eviction victim?",
        "options": [
            {"id": "A", "text": "Evicting an unmodified clean page (M=0) requires no disk write, making it much faster than evicting a dirty page (M=1) that must be flushed to swap.", "is_distractor": False},
            {"id": "B", "text": "Dirty pages cannot be evicted under any circumstances.", "is_distractor": True},
            {"id": "C", "text": "Reference bits cannot be modified by the kernel.", "is_distractor": True},
            {"id": "D", "text": "It guarantees zero page faults in all loops.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Writing a dirty page back to disk requires expensive disk I/O. Prioritizing $(0, 0)$ (neither recently used nor modified) over $(0, 1)$ avoids unnecessary disk writes.",
        "distractor_explanations": {
            "B": "Dirty pages can be evicted; they are simply written back to disk first.",
            "C": "The kernel clears reference bits routinely.",
            "D": "No algorithm can guarantee zero page faults."
        },
        "a": 1.60,
        "b": 1.05,
        "point_biserial": 0.49
    },
    {
        "skill_code": "OS_PAGE_REPLACE",
        "stem": "Which mathematical property distinguishes **Stack Algorithms** (such as LRU and Optimal) from FIFO?",
        "options": [
            {"id": "A", "text": "The set of pages in memory with N frames is always a strict subset of the set of pages with N + 1 frames for any reference string ($M(N) \\subseteq M(N+1)$).", "is_distractor": False},
            {"id": "B", "text": "They use an explicit LIFO hardware stack.", "is_distractor": True},
            {"id": "C", "text": "They cannot run on multiprocessor architectures.", "is_distractor": True},
            {"id": "D", "text": "They require O(1) time complexity.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Mattson's inclusion property defines stack algorithms: the contents of an $N$-frame memory are always a subset of an $(N+1)$-frame memory. This inclusion property guarantees immunity from Bélády's Anomaly.",
        "distractor_explanations": {
            "B": "The name refers to the mathematical subset inclusion property, not hardware LIFO push/pop.",
            "C": "Stack algorithms are universal across uniprocessors and multiprocessors.",
            "D": "Theoretical optimal algorithm requires future scan, not $O(1)$."
        },
        "a": 1.70,
        "b": 1.50,
        "point_biserial": 0.52
    }
]
