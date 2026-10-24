"""
Object-Oriented Programming Question Bank.
Topic: Core OOP Pillars (15 questions across OOP_CLASSES, OOP_INHERITANCE, OOP_POLYMORPHISM, OOP_SOLID)
"""

OOP_ITEMS = [
    # =========================================================================
    # TOPIC: Core OOP Pillars (15 items)
    # =========================================================================
    # --- OOP_CLASSES (4 items) ---
    {
        "skill_code": "OOP_CLASSES",
        "stem": "What is the primary role of a constructor in object-oriented programming?",
        "options": [
            {"id": "A", "text": "To initialize the newly created object's state and allocate necessary internal resources.", "is_distractor": False},
            {"id": "B", "text": "To destroy the object when it goes out of scope.", "is_distractor": True},
            {"id": "C", "text": "To convert the object into a JSON string.", "is_distractor": True},
            {"id": "D", "text": "To enforce multiple inheritance at runtime.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A constructor is invoked automatically upon object instantiation to set initial values for instance variables and guarantee valid class invariants.",
        "distractor_explanations": {
            "B": "Defines the role of a destructor or finalizer.",
            "C": "Defines serialization.",
            "D": "Multiple inheritance is a compiler/language type hierarchy mechanism."
        },
        "a": 1.25,
        "b": -1.20,
        "point_biserial": 0.40
    },
    {
        "skill_code": "OOP_CLASSES",
        "stem": "In encapsulation, what is the purpose of declaring instance variables as `private` and exposing access via getters and setters?",
        "options": [
            {"id": "A", "text": "To protect internal state representation from external tampering and enforce business validation rules.", "is_distractor": False},
            {"id": "B", "text": "To accelerate runtime execution by eliminating function call overhead.", "is_distractor": True},
            {"id": "C", "text": "To automatically serialize data to the database.", "is_distractor": True},
            {"id": "D", "text": "To prevent other classes from subclassing.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Encapsulation hides the internal implementation details of an object behind a well-defined public interface, allowing internal refactoring without breaking callers.",
        "distractor_explanations": {
            "B": "Getters/setters add function call overhead (unless inlined by compiler).",
            "C": "Data serialization requires explicit ORM or serialization logic.",
            "D": "`final` or `sealed` prevents subclassing, not `private` fields."
        },
        "a": 1.35,
        "b": -0.70,
        "point_biserial": 0.42
    },
    {
        "skill_code": "OOP_CLASSES",
        "stem": "In Python, what is the difference between a class variable and an instance variable?",
        "options": [
            {"id": "A", "text": "Class variables are shared by all instances of the class; instance variables are unique to each instance.", "is_distractor": False},
            {"id": "B", "text": "Class variables are stored in the heap; instance variables are stored on the stack.", "is_distractor": True},
            {"id": "C", "text": "Class variables are immutable; instance variables are mutable.", "is_distractor": True},
            {"id": "D", "text": "Class variables cannot be accessed from instance methods.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A class variable is defined in the class body and bound to the class object, shared across all instances. An instance variable is bound to `self`, existing per object.",
        "distractor_explanations": {
            "B": "All Python objects and attributes reside on the heap managed by the Python memory allocator.",
            "C": "Both class and instance variables can be mutable or immutable.",
            "D": "Instance methods can access class variables via `self.__class__.var` or `ClassName.var`."
        },
        "a": 1.45,
        "b": -0.10,
        "point_biserial": 0.44
    },
    {
        "skill_code": "OOP_CLASSES",
        "stem": "What is the consequence of declaring a member function as `static` in a class?",
        "options": [
            {"id": "A", "text": "It can be invoked directly on the class without instantiating an object, and lacks an implicit `this` or instance pointer.", "is_distractor": False},
            {"id": "B", "text": "It cannot accept parameters.", "is_distractor": True},
            {"id": "C", "text": "It is automatically executed concurrently on a background thread.", "is_distractor": True},
            {"id": "D", "text": "It can access all non-static private instance variables.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Static methods belong to the class namespace rather than any individual instance. Consequently, they do not receive an implicit `this` reference and cannot access instance state.",
        "distractor_explanations": {
            "B": "Static methods accept parameters normally.",
            "C": "Static methods execute synchronously unless explicitly scheduled.",
            "D": "Static methods cannot access non-static instance fields without an explicit object reference."
        },
        "a": 1.50,
        "b": 0.35,
        "point_biserial": 0.45
    },

    # --- OOP_INHERITANCE (4 items) ---
    {
        "skill_code": "OOP_INHERITANCE",
        "stem": "What is the **Diamond Problem** in multiple inheritance?",
        "options": [
            {"id": "A", "text": "Ambiguity arising when a class inherits from two parent classes that both inherit from the same common ancestor.", "is_distractor": False},
            {"id": "B", "text": "An error when a class implements more than four interfaces.", "is_distractor": True},
            {"id": "C", "text": "A memory leak caused by cyclic pointer references.", "is_distractor": True},
            {"id": "D", "text": "Inability to override abstract methods in child classes.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "If Class D inherits from both B and C, which both inherit from A, it is ambiguous whether D inherits A's methods via B or C. Languages like C++ use virtual inheritance and Python uses C3 linearization (MRO) to resolve this.",
        "distractor_explanations": {
            "B": "Multiple interface implementation does not cause the diamond problem if interfaces have no state.",
            "C": "Describes cyclic reference garbage collection, not multiple inheritance ambiguity.",
            "D": "Abstract methods must be implemented by concrete subclasses."
        },
        "a": 1.45,
        "b": 0.15,
        "point_biserial": 0.44
    },
    {
        "skill_code": "OOP_INHERITANCE",
        "stem": "Why do modern software engineering principles advocate for **Composition over Inheritance**?",
        "options": [
            {"id": "A", "text": "Composition provides loose coupling, allows dynamic runtime behavior changes, and avoids fragile base class hierarchies.", "is_distractor": False},
            {"id": "B", "text": "Inheritance requires more lines of code in all cases.", "is_distractor": True},
            {"id": "C", "text": "Composition is the only way to achieve polymorphism in compiled languages.", "is_distractor": True},
            {"id": "D", "text": "Inheritance cannot be used with design patterns.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Inheritance creates tight compile-time coupling ('white-box reuse') that exposes parent implementation details. Composition ('has-a') enables modularity and runtime component swapping.",
        "distractor_explanations": {
            "B": "Inheritance often uses fewer lines initially, but incurs long-term maintenance fragility.",
            "C": "Polymorphism can be achieved through interfaces and abstract base classes.",
            "D": "Many design patterns (Template Method, Factory Method) utilize inheritance."
        },
        "a": 1.55,
        "b": 0.50,
        "point_biserial": 0.47
    },
    {
        "skill_code": "OOP_INHERITANCE",
        "stem": "What is an **Abstract Class**?",
        "options": [
            {"id": "A", "text": "A class that cannot be instantiated directly and serves as a blueprint containing one or more pure virtual/abstract methods.", "is_distractor": False},
            {"id": "B", "text": "A class that cannot be subclassed.", "is_distractor": True},
            {"id": "C", "text": "A class with only private members and no methods.", "is_distractor": True},
            {"id": "D", "text": "A class defined inside another function body.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Abstract classes define common interface contracts and shared implementation logic for derived subclasses, but cannot be instantiated directly with `new`.",
        "distractor_explanations": {
            "B": "Defines a final or sealed class, which is the exact opposite of an abstract class.",
            "C": "Describes an inaccessible dummy struct.",
            "D": "Defines a local class."
        },
        "a": 1.30,
        "b": -0.80,
        "point_biserial": 0.41
    },
    {
        "skill_code": "OOP_INHERITANCE",
        "stem": "In Python, which built-in function returns the **Method Resolution Order (MRO)** used to resolve attribute lookups under multiple inheritance?",
        "options": [
            {"id": "A", "text": "ClassName.mro() or ClassName.__mro__", "is_distractor": False},
            {"id": "B", "text": "ClassName.__dict__", "is_distractor": True},
            {"id": "C", "text": "ClassName.__bases__", "is_distractor": True},
            {"id": "D", "text": "type(ClassName)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "`ClassName.mro()` returns the list of classes in the exact order Python inspects them, computed via the C3 Linearization algorithm.",
        "distractor_explanations": {
            "B": "Returns the class namespace attribute dictionary, not the inheritance search order.",
            "C": "Returns only direct immediate base classes, not the full linearization chain.",
            "D": "Returns the metaclass `type`."
        },
        "a": 1.60,
        "b": 0.90,
        "point_biserial": 0.48
    },

    # --- OOP_POLYMORPHISM (4 items) ---
    {
        "skill_code": "OOP_POLYMORPHISM",
        "stem": "Which mechanism enables runtime (dynamic) polymorphism in object-oriented languages like C++ and Java?",
        "options": [
            {"id": "A", "text": "Virtual Method Tables (vtable) and dynamic method dispatch", "is_distractor": False},
            {"id": "B", "text": "Template specialization and macro expansion", "is_distractor": True},
            {"id": "C", "text": "Function overloading resolved at compile-time", "is_distractor": True},
            {"id": "D", "text": "Static type casting", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Runtime polymorphism relies on dynamic dispatch: objects containing virtual methods maintain a hidden pointer (vptr) to a table of function pointers (vtable). At runtime, the method is dispatched according to the actual underlying runtime object type.",
        "distractor_explanations": {
            "B": "Templates and macros are compile-time (static) mechanisms.",
            "C": "Function overloading is static compile-time polymorphism.",
            "D": "Static type casting does not perform dynamic method dispatch."
        },
        "a": 1.50,
        "b": 0.15,
        "point_biserial": 0.45
    },
    {
        "skill_code": "OOP_POLYMORPHISM",
        "stem": "What is the difference between **Method Overloading** and **Method Overriding**?",
        "options": [
            {"id": "A", "text": "Overloading occurs within the same class with different signatures (compile-time); Overriding redefines a base class method with the same signature (runtime).", "is_distractor": False},
            {"id": "B", "text": "Overloading requires inheritance; Overriding does not.", "is_distractor": True},
            {"id": "C", "text": "Overriding is resolved at compile time; Overloading is resolved at runtime.", "is_distractor": True},
            {"id": "D", "text": "They are synonymous terms for dynamic dispatch.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Method overloading provides multiple methods with the same name but distinct parameter types/counts (static polymorphism). Method overriding redefines an existing inherited virtual method with identical signature (dynamic polymorphism).",
        "distractor_explanations": {
            "B": "Overriding strictly requires inheritance, while overloading does not.",
            "C": "Reverses the compile-time and runtime phases.",
            "D": "They represent fundamentally distinct language mechanisms."
        },
        "a": 1.35,
        "b": -0.65,
        "point_biserial": 0.42
    },
    {
        "skill_code": "OOP_POLYMORPHISM",
        "stem": "What is **Duck Typing** in dynamically typed programming languages?",
        "options": [
            {"id": "A", "text": "An object's suitability is determined by the presence of certain methods and properties, rather than its explicit inheritance hierarchy (\"If it walks like a duck and quacks like a duck...\").", "is_distractor": False},
            {"id": "B", "text": "A static type check performed before compiling bytecode.", "is_distractor": True},
            {"id": "C", "text": "A design pattern for creating bird simulation games.", "is_distractor": True},
            {"id": "D", "text": "Enforcing that all subclasses implement a single root interface.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In languages like Python and Ruby, code interacts with an object based on its interface (callable methods) rather than requiring explicit nominal inheritance.",
        "distractor_explanations": {
            "B": "Duck typing is dynamic runtime typing, the opposite of static type checking.",
            "C": "Literal misunderstanding of the philosophical idiom.",
            "D": "Describes nominal typing in languages like Java."
        },
        "a": 1.40,
        "b": -0.25,
        "point_biserial": 0.43
    },
    {
        "skill_code": "OOP_POLYMORPHISM",
        "stem": "In C++, why should a base class intended for polymorphic deletion always declare a **virtual destructor**?",
        "options": [
            {"id": "A", "text": "To ensure that deleting an object through a base class pointer invokes the derived class destructor, preventing resource leaks and undefined behavior.", "is_distractor": False},
            {"id": "B", "text": "To prevent derived classes from having destructors.", "is_distractor": True},
            {"id": "C", "text": "To automatically deallocate all member pointers without calling delete.", "is_distractor": True},
            {"id": "D", "text": "Because non-virtual destructors cause compilation errors in all classes.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "If a base pointer `Base *ptr = new Derived();` is deleted, and `~Base()` is not virtual, only the `Base` destructor will be executed. The `Derived` destructor is skipped, leaking derived resources.",
        "distractor_explanations": {
            "B": "Derived classes must still have destructors to clean up their specific members.",
            "C": "Virtual destructors do not replace explicit deletion of owned raw pointers.",
            "D": "Non-virtual destructors compile cleanly and are standard for non-polymorphic types."
        },
        "a": 1.65,
        "b": 1.25,
        "point_biserial": 0.50
    },

    # --- OOP_SOLID (3 items) ---
    {
        "skill_code": "OOP_SOLID",
        "stem": "Which SOLID principle states that *\"Subtypes must be substitutable for their base types without altering the correctness of the program\"*?",
        "options": [
            {"id": "A", "text": "Liskov Substitution Principle (LSP)", "is_distractor": False},
            {"id": "B", "text": "Single Responsibility Principle (SRP)", "is_distractor": True},
            {"id": "C", "text": "Open/Closed Principle (OCP)", "is_distractor": True},
            {"id": "D", "text": "Interface Segregation Principle (ISP)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Formulated by Barbara Liskov, LSP requires that derived classes must honor the contracts of their base classes (preconditions cannot be strengthened, postconditions cannot be weakened).",
        "distractor_explanations": {
            "B": "SRP states a class should have only one reason to change.",
            "C": "OCP states software entities should be open for extension but closed for modification.",
            "D": "ISP states clients should not be forced to depend on interfaces they do not use."
        },
        "a": 1.50,
        "b": 0.40,
        "point_biserial": 0.45
    },
    {
        "skill_code": "OOP_SOLID",
        "stem": "A notification module directly instantiates `TwilioSmsClient` and `SendgridEmailClient` inside its business logic class. Which principle of SOLID is directly violated?",
        "options": [
            {"id": "A", "text": "Dependency Inversion Principle (DIP)", "is_distractor": False},
            {"id": "B", "text": "Single Responsibility Principle (SRP)", "is_distractor": True},
            {"id": "C", "text": "Liskov Substitution Principle (LSP)", "is_distractor": True},
            {"id": "D", "text": "Law of Demeter", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "DIP dictates that high-level modules should not depend on low-level modules; both should depend on abstractions (e.g. an `INotificationService` interface). Instantiating concrete clients creates tight coupling.",
        "distractor_explanations": {
            "B": "While related, the core structural violation is hardcoded dependency on concrete low-level implementations.",
            "C": "No invalid subclass substitution is occurring.",
            "D": "Law of Demeter concerns chaining calls ('don't talk to strangers')."
        },
        "a": 1.55,
        "b": 0.70,
        "point_biserial": 0.47
    },
    {
        "skill_code": "OOP_SOLID",
        "stem": "An interface `IWorker` contains methods `work()`, `eat()`, `sleep()`, and `chargeBattery()`. Forcing a `HumanWorker` class to implement `chargeBattery()` violates which SOLID principle?",
        "options": [
            {"id": "A", "text": "Interface Segregation Principle (ISP)", "is_distractor": False},
            {"id": "B", "text": "Open/Closed Principle (OCP)", "is_distractor": True},
            {"id": "C", "text": "Single Responsibility Principle (SRP)", "is_distractor": True},
            {"id": "D", "text": "Liskov Substitution Principle (LSP)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "ISP states that no client should be forced to depend on methods it does not use. Large 'fat' interfaces should be split into smaller, cohesive interfaces (`IWorkable`, `IRechargeable`).",
        "distractor_explanations": {
            "B": "OCP relates to extensibility without source modification.",
            "C": "SRP applies to classes and modules having a single actor/responsibility.",
            "D": "LSP concerns behavioral subtyping compliance."
        },
        "a": 1.60,
        "b": 0.95,
        "point_biserial": 0.48
    }
]
