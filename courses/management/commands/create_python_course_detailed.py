import html as _html
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Category, Course, Lesson, Quiz, QuizQuestion

User = get_user_model()


def to_html_content(raw: str) -> str:
    """Convert plain-text lesson content to safe Quill/TipTap HTML."""
    lines = raw.strip().splitlines()
    parts: list[str] = []
    buffer: list[str] = []

    def flush_buffer():
        if buffer:
            escaped = _html.escape("\n".join(buffer))
            parts.append(f'<pre><code>{escaped}</code></pre>')
            buffer.clear()

    if lines and lines[0].startswith("Welcome to Lesson"):
        parts.append(f'<h2>{_html.escape(lines[0])}</h2>')
        lines = lines[1:]

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("───") or stripped.startswith("---"):
            flush_buffer()
            title = stripped.replace("─", "").replace("-", "").strip()
            if title:
                parts.append(f'<h3>{_html.escape(title)}</h3>')
        else:
            buffer.append(line)

    flush_buffer()
    return "\n".join(parts)


LESSONS = [
    {
        "order": 1,
        "title": "Python Basics — Syntax, Variables & Data Types",
        "description": "Learn Python syntax, how to run Python, variables, built-in data types (int, float, str, bool, None), type conversion, and basic input/output.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 1: Python Basics — Syntax, Variables & Data Types

Python is a high-level, interpreted, dynamically-typed language famous for its readable syntax.

─── RUNNING PYTHON ────────────────────────────────────────────────────────────
    python script.py          # run a file
    python                    # open interactive REPL
    python -c "print('hi')"   # run one-liner

─── PRINT & COMMENTS ──────────────────────────────────────────────────────────
    print("Hello, World!")
    print("a", "b", sep=", ", end="!\n")

    # This is a single-line comment

    """
    This is a
    multi-line string / docstring
    """

─── VARIABLES ─────────────────────────────────────────────────────────────────
Python is dynamically typed — no type declaration needed:
    name  = "Alice"
    age   = 30
    score = 98.5
    active = True

    # Multiple assignment
    x, y, z = 1, 2, 3
    a = b = c = 0

    # Augmented assignment
    x += 1   # x = x + 1
    x -= 2
    x *= 3
    x //= 2  # integer division assignment

─── NAMING CONVENTIONS ────────────────────────────────────────────────────────
    snake_case         for variables and functions
    PascalCase         for classes
    SCREAMING_SNAKE    for constants
    _private           convention for private names
    __dunder__         reserved for Python internals

─── BUILT-IN DATA TYPES ───────────────────────────────────────────────────────
    int        42   -7   0
    float      3.14   -0.5   1.0e10
    complex    3+4j
    str        "hello"   'world'   """multiline"""
    bool       True   False
    NoneType   None    (absence of value, like null)
    bytes      b"data"

─── TYPE CONVERSION ───────────────────────────────────────────────────────────
    int("42")          # 42
    float("3.14")      # 3.14
    str(100)           # "100"
    bool(0)            # False
    bool("")           # False
    bool(None)         # False
    list("abc")        # ['a', 'b', 'c']

─── CHECKING TYPES ────────────────────────────────────────────────────────────
    type(42)           # <class 'int'>
    isinstance(42, int)         # True
    isinstance(42, (int, float)) # True

─── INPUT / OUTPUT ────────────────────────────────────────────────────────────
    name = input("Enter your name: ")   # always returns a string
    age  = int(input("Enter age: "))

    print(f"Hello, {name}! You are {age} years old.")

─── F-STRINGS (Python 3.6+) ───────────────────────────────────────────────────
    name = "Alice"
    age  = 30
    print(f"Name: {name}, Age: {age}")
    print(f"Pi is approx {3.14159:.2f}")   # format spec
    print(f"10 + 5 = {10 + 5}")            # expressions allowed

─── ARITHMETIC OPERATORS ──────────────────────────────────────────────────────
    +   -   *   /    # standard (/ always returns float)
    //  floor division (integer result)
    %   modulus (remainder)
    **  exponentiation   2**10 = 1024

─── COMPARISON & LOGICAL ──────────────────────────────────────────────────────
    ==  !=  >  <  >=  <=
    and   or   not
    is    is not   (identity check)
    in    not in   (membership check)
""",
        "quiz_title": "Quiz 1 — Python Basics, Variables & Data Types",
        "quiz_description": "20 questions on Python syntax, variables, data types, type conversion, f-strings, and operators.",
        "time_limit": 20,
        "questions": [
            {"q": "What is the correct way to print 'Hello, World!' in Python?", "o": ["echo 'Hello, World!'", "console.log('Hello, World!')", "printf('Hello, World!')", "print('Hello, World!')"], "a": "print('Hello, World!')"},
            {"q": "Which of these is the correct Python comment syntax?", "o": ["// comment", "/* comment */", "<!-- comment -->", "# comment"], "a": "# comment"},
            {"q": "What does Python's dynamic typing mean?", "o": ["Variables are always strings", "Types are checked at compile time", "Variables cannot change type", "You don't need to declare a variable's type explicitly"], "a": "You don't need to declare a variable's type explicitly"},
            {"q": "What is the Python naming convention for variables and functions?", "o": ["camelCase", "PascalCase", "SCREAMING_SNAKE", "snake_case"], "a": "snake_case"},
            {"q": "What does int('42') return?", "o": ["'42'", "42.0", "Error", "42"], "a": "42"},
            {"q": "What does bool(0) return?", "o": ["True", "None", "0", "False"], "a": "False"},
            {"q": "What does bool('') return?", "o": ["True", "None", "''", "False"], "a": "False"},
            {"q": "What does type(3.14) return?", "o": ["<class 'int'>", "<class 'number'>", "<class 'decimal'>", "<class 'float'>"], "a": "<class 'float'>"},
            {"q": "Which function checks if a variable is an instance of a given type?", "o": ["checktype()", "typeof()", "type()", "isinstance()"], "a": "isinstance()"},
            {"q": "What does the // operator do in Python?", "o": ["Regular division", "Modulus", "Exponentiation", "Floor (integer) division"], "a": "Floor (integer) division"},
            {"q": "What does the ** operator do?", "o": ["Multiplication", "Modulus", "Floor division", "Exponentiation"], "a": "Exponentiation"},
            {"q": "What does 10 % 3 evaluate to?", "o": ["3", "0", "3.33", "1"], "a": "1"},
            {"q": "What does input() always return?", "o": ["int", "float", "bool", "str"], "a": "str"},
            {"q": "What is the correct f-string syntax in Python 3.6+?", "o": ["'Hello {name}'", "\"Hello\" + name", "format('Hello', name)", "f'Hello {name}'"], "a": "f'Hello {name}'"},
            {"q": "What is None in Python?", "o": ["False", "0", "An empty string", "The absence of a value (like null)"], "a": "The absence of a value (like null)"},
            {"q": "Which operator checks IDENTITY (same object in memory)?", "o": ["==", "===", "equals", "is"], "a": "is"},
            {"q": "Which operator checks MEMBERSHIP (value in a sequence)?", "o": ["has", "contains", "==", "in"], "a": "in"},
            {"q": "What is the result of 7 / 2 in Python 3?", "o": ["3", "4", "3.0", "3.5"], "a": "3.5"},
            {"q": "What is the result of 7 // 2 in Python 3?", "o": ["3.5", "4", "3.0", "3"], "a": "3"},
            {"q": "How do you assign the same value to multiple variables at once?", "o": ["x, y = 0", "x = y; = 0", "x == y == 0", "x = y = 0"], "a": "x = y = 0"},
        ],
    },
    {
        "order": 2,
        "title": "Control Flow — Conditionals & Loops",
        "description": "Control program execution with if/elif/else, while loops, for loops, range(), break, continue, pass, and the else clause on loops.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 2: Control Flow — Conditionals & Loops

Python uses indentation (not braces) to define code blocks.

─── IF / ELIF / ELSE ──────────────────────────────────────────────────────────
    age = 20
    if age >= 18:
        print("Adult")
    elif age >= 13:
        print("Teenager")
    else:
        print("Child")

─── TERNARY (CONDITIONAL EXPRESSION) ─────────────────────────────────────────
    label = "Adult" if age >= 18 else "Minor"

─── TRUTHY & FALSY VALUES ─────────────────────────────────────────────────────
    Falsy:  False, 0, 0.0, 0j, "", [], {}, set(), None, range(0)
    Everything else is truthy.

─── WHILE LOOP ────────────────────────────────────────────────────────────────
    count = 0
    while count < 5:
        print(count)
        count += 1

─── FOR LOOP ──────────────────────────────────────────────────────────────────
Iterates over any iterable (list, string, range, tuple, dict, etc.):
    for i in range(5):       # 0, 1, 2, 3, 4
        print(i)

    for char in "hello":
        print(char)

    for item in [10, 20, 30]:
        print(item)

─── RANGE() ───────────────────────────────────────────────────────────────────
    range(stop)              # 0 to stop-1
    range(start, stop)       # start to stop-1
    range(start, stop, step) # with step

    list(range(2, 10, 2))    # [2, 4, 6, 8]
    list(range(5, 0, -1))    # [5, 4, 3, 2, 1]

─── BREAK & CONTINUE ──────────────────────────────────────────────────────────
    break     — exit the loop immediately
    continue  — skip to the next iteration

    for n in range(10):
        if n == 3:
            continue    # skip 3
        if n == 7:
            break       # stop at 7
        print(n)        # prints 0,1,2,4,5,6

─── PASS ──────────────────────────────────────────────────────────────────────
    pass  — a no-op placeholder; makes an empty block valid
    if x > 0:
        pass    # TODO: handle positive case

─── ELSE ON LOOPS ─────────────────────────────────────────────────────────────
The else block runs when the loop COMPLETES WITHOUT hitting break:
    for n in range(2, 10):
        for i in range(2, n):
            if n % i == 0:
                break
        else:
            print(f"{n} is prime")  # runs only if no break occurred

─── ENUMERATE ─────────────────────────────────────────────────────────────────
Get index and value together:
    fruits = ["apple", "banana", "cherry"]
    for i, fruit in enumerate(fruits):
        print(i, fruit)   # 0 apple, 1 banana, 2 cherry

    for i, fruit in enumerate(fruits, start=1):
        print(i, fruit)   # 1 apple, 2 banana, 3 cherry

─── ZIP ───────────────────────────────────────────────────────────────────────
    names  = ["Alice", "Bob"]
    scores = [95, 87]
    for name, score in zip(names, scores):
        print(f"{name}: {score}")
""",
        "quiz_title": "Quiz 2 — Control Flow, Conditionals & Loops",
        "quiz_description": "20 questions on if/elif/else, ternary, while, for, range, break, continue, pass, enumerate, and zip.",
        "time_limit": 20,
        "questions": [
            {"q": "What defines a code block in Python?", "o": ["Curly braces {}", "Parentheses ()", "Square brackets []", "Indentation"], "a": "Indentation"},
            {"q": "What is the Python keyword for 'else if'?", "o": ["else if", "elseif", "otherwise", "elif"], "a": "elif"},
            {"q": "What is the Python ternary (conditional expression) syntax?", "o": ["condition ? a : b", "a if condition else b", "if condition then a else b", "condition -> a | b"], "a": "a if condition else b"},
            {"q": "Which of these is FALSY in Python?", "o": ["'False'", "[0]", "1", "[]"], "a": "[]"},
            {"q": "Which of these is TRUTHY in Python?", "o": ["0", "None", "''", "[0]"], "a": "[0]"},
            {"q": "What does range(2, 10, 2) produce?", "o": ["[2, 4, 6, 8, 10]", "[2, 3, 4, 5, 6, 7, 8, 9]", "[0, 2, 4, 6, 8]", "[2, 4, 6, 8]"], "a": "[2, 4, 6, 8]"},
            {"q": "What does range(5) produce?", "o": ["[1, 2, 3, 4, 5]", "[0, 1, 2, 3, 4, 5]", "[0, 1, 2, 3]", "[0, 1, 2, 3, 4]"], "a": "[0, 1, 2, 3, 4]"},
            {"q": "What does 'break' do inside a loop?", "o": ["Skips current iteration", "Restarts the loop", "Pauses execution", "Exits the loop immediately"], "a": "Exits the loop immediately"},
            {"q": "What does 'continue' do inside a loop?", "o": ["Exits the loop", "Ends the program", "Restarts the loop", "Skips to the next iteration"], "a": "Skips to the next iteration"},
            {"q": "What is 'pass' used for?", "o": ["Ending a function", "Exiting a loop", "Skipping an iteration", "A no-op placeholder for empty blocks"], "a": "A no-op placeholder for empty blocks"},
            {"q": "When does the 'else' clause on a loop execute?", "o": ["When the loop body raises an error", "Every iteration", "Never", "When the loop finishes without hitting break"], "a": "When the loop finishes without hitting break"},
            {"q": "What does enumerate(['a','b','c']) yield?", "o": ["(0,'a'),(1,'b'),(2,'c')", "['a','b','c']", "(1,'a'),(2,'b'),(3,'c')", "('a',0),('b',1),('c',2)"], "a": "(0,'a'),(1,'b'),(2,'c')"},
            {"q": "What does zip([1,2],[3,4]) yield?", "o": ["[1,2,3,4]", "[(1,3),(2,4)]", "[(1,2),(3,4)]", "{1:3, 2:4}"], "a": "[(1,3),(2,4)]"},
            {"q": "What happens when a while loop condition is False from the start?", "o": ["Runs once", "Runs infinitely", "Raises an error", "The body never executes"], "a": "The body never executes"},
            {"q": "How do you iterate over each character in a string?", "o": ["for i in range(len(s)): s[i]", "for char in list(s)", "while s:", "for char in s:"], "a": "for char in s:"},
            {"q": "What does range(5, 0, -1) produce?", "o": ["[0,1,2,3,4]", "[5,4,3,2,1,0]", "[1,2,3,4,5]", "[5,4,3,2,1]"], "a": "[5,4,3,2,1]"},
            {"q": "Can a for loop iterate directly over a dictionary in Python?", "o": ["No, use dict.items() only", "Yes, iterates over values", "Yes, iterates over (key, value) pairs", "Yes, iterates over keys by default"], "a": "Yes, iterates over keys by default"},
            {"q": "What does enumerate(fruits, start=1) do?", "o": ["Counts items from 0", "Skips the first item", "Starts index from -1", "Starts the index counter at 1"], "a": "Starts the index counter at 1"},
            {"q": "What is an infinite loop?", "o": ["A loop that runs exactly once", "A loop with no body", "A for loop with no range", "A loop whose condition never becomes False"], "a": "A loop whose condition never becomes False"},
            {"q": "What is the output of: for i in range(3): print(i) else: print('done')?", "o": ["0 1 2 done only if no break", "Syntax error", "0 1 2 (no 'done')", "0 1 2 done"], "a": "0 1 2 done"},
        ],
    },
    {
        "order": 3,
        "title": "Functions — Definitions, Arguments & Scope",
        "description": "Define functions with def, understand positional and keyword arguments, default parameters, *args/**kwargs, return values, variable scope (LEGB), lambda functions, and decorators.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 3: Functions — Definitions, Arguments & Scope

Functions let you package reusable logic and avoid repetition.

─── DEFINING & CALLING ────────────────────────────────────────────────────────
    def greet(name):
        \"\"\"Return a greeting string.\"\"\"
        return f"Hello, {name}!"

    result = greet("Alice")   # "Hello, Alice!"

─── PARAMETERS & ARGUMENTS ────────────────────────────────────────────────────
    def add(a, b):             # positional parameters
        return a + b

    add(3, 4)                  # positional args
    add(a=3, b=4)              # keyword args
    add(b=4, a=3)              # keyword args (order independent)

─── DEFAULT PARAMETERS ────────────────────────────────────────────────────────
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    greet("Alice")             # "Hello, Alice!"
    greet("Alice", "Hi")       # "Hi, Alice!"

    ⚠ Default values are evaluated ONCE at definition time.
    ⚠ Use None as default for mutable defaults:
        def append_to(val, lst=None):
            if lst is None:
                lst = []
            lst.append(val)
            return lst

─── *ARGS (VARIABLE POSITIONAL) ───────────────────────────────────────────────
    def total(*numbers):
        return sum(numbers)

    total(1, 2, 3, 4)   # 10

─── **KWARGS (VARIABLE KEYWORD) ───────────────────────────────────────────────
    def display(**info):
        for key, value in info.items():
            print(f"{key}: {value}")

    display(name="Alice", age=30)

─── PARAMETER ORDER ───────────────────────────────────────────────────────────
    def fn(pos, /, normal, *, kw_only):
        pass
    pos      — positional only (before /)
    normal   — positional or keyword
    kw_only  — keyword only (after *)

─── RETURN VALUES ─────────────────────────────────────────────────────────────
    def minmax(lst):
        return min(lst), max(lst)   # returns a tuple

    lo, hi = minmax([3, 1, 4, 1, 5])
    # Functions without return → return None

─── SCOPE (LEGB RULE) ─────────────────────────────────────────────────────────
Python resolves names in this order:
    L — Local (inside current function)
    E — Enclosing (outer function in nested functions)
    G — Global (module level)
    B — Built-in (Python builtins like print, len)

    x = "global"
    def outer():
        x = "enclosing"
        def inner():
            x = "local"
            print(x)   # "local"
        inner()

    global x    — declare that x refers to the module-level x
    nonlocal x  — declare that x refers to the enclosing scope

─── LAMBDA FUNCTIONS ──────────────────────────────────────────────────────────
Anonymous single-expression functions:
    double = lambda x: x * 2
    add    = lambda a, b: a + b
    square = lambda x: x ** 2

    nums = [3, 1, 4, 1, 5]
    nums.sort(key=lambda x: -x)   # sort descending

─── DECORATORS ────────────────────────────────────────────────────────────────
A decorator wraps a function to add behaviour:
    def uppercase(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper()
        return wrapper

    @uppercase
    def greet(name):
        return f"hello, {name}"

    greet("alice")   # "HELLO, ALICE"

─── DOCSTRINGS ────────────────────────────────────────────────────────────────
    def greet(name):
        \"\"\"Return a personalised greeting.

        Args:
            name (str): The person's name.
        Returns:
            str: The greeting string.
        \"\"\"
        return f"Hello, {name}!"

    help(greet)      # displays docstring
    greet.__doc__    # raw docstring string
""",
        "quiz_title": "Quiz 3 — Functions, Arguments & Scope",
        "quiz_description": "20 questions on def, default params, *args/**kwargs, return, LEGB scope, lambda, and decorators.",
        "time_limit": 20,
        "questions": [
            {"q": "Which keyword defines a function in Python?", "o": ["function", "func", "fn", "def"], "a": "def"},
            {"q": "What does a function return if it has no explicit return statement?", "o": ["0", "False", "An empty list", "None"], "a": "None"},
            {"q": "Which parameter type collects extra positional arguments into a tuple?", "o": ["**kwargs", "extra_args", "defaults", "*args"], "a": "*args"},
            {"q": "Which parameter type collects extra keyword arguments into a dictionary?", "o": ["*args", "extra_kwargs", "kw_dict", "**kwargs"], "a": "**kwargs"},
            {"q": "What is the correct order of parameters in a function signature?", "o": ["*args, positional, **kwargs", "**kwargs, *args, positional", "positional, **kwargs, *args", "positional, *args, **kwargs"], "a": "positional, *args, **kwargs"},
            {"q": "What is the LEGB rule?", "o": ["A Python style guide", "A memory allocation order", "A Python version naming scheme", "The order Python searches for variable names: Local, Enclosing, Global, Built-in"], "a": "The order Python searches for variable names: Local, Enclosing, Global, Built-in"},
            {"q": "Which keyword declares that a variable inside a function refers to the module-level global?", "o": ["outer", "nonlocal", "extern", "global"], "a": "global"},
            {"q": "Which keyword refers to a variable in the enclosing (outer) function's scope?", "o": ["global", "outer", "enclosing", "nonlocal"], "a": "nonlocal"},
            {"q": "What is a lambda function?", "o": ["A class method", "A built-in function", "A recursive function", "A small anonymous single-expression function"], "a": "A small anonymous single-expression function"},
            {"q": "What is a decorator in Python?", "o": ["A comment style", "A type hint", "A class attribute", "A function that wraps another function to extend its behaviour"], "a": "A function that wraps another function to extend its behaviour"},
            {"q": "What is the @ symbol used for in Python?", "o": ["Matrix multiplication operator AND decorator syntax", "Only decorator syntax", "Only matrix multiplication", "Email addresses in strings"], "a": "Matrix multiplication operator AND decorator syntax"},
            {"q": "What is a docstring?", "o": ["A comment inside a loop", "A special print statement", "A type annotation", "A string literal at the start of a function/class/module used as documentation"], "a": "A string literal at the start of a function/class/module used as documentation"},
            {"q": "Why should you avoid mutable default arguments like def fn(lst=[])?", "o": ["Lists cannot be default values", "It causes a syntax error", "It makes the function slower", "The default is shared across all calls — mutations persist between calls"], "a": "The default is shared across all calls — mutations persist between calls"},
            {"q": "Can Python functions return multiple values?", "o": ["No", "Only with a special keyword", "Only tuples", "Yes, returned as a tuple"], "a": "Yes, returned as a tuple"},
            {"q": "What does lambda x: x * 2 do?", "o": ["Defines a class", "Creates a list", "Prints x * 2", "Creates a function that doubles its argument"], "a": "Creates a function that doubles its argument"},
            {"q": "What happens when keyword arguments are passed out of order?", "o": ["Python raises a TypeError", "Python uses the definition order", "Only the first argument is used", "It works fine — keyword args are order-independent"], "a": "It works fine — keyword args are order-independent"},
            {"q": "What does def fn(a, /, b, *, c): mean?", "o": ["a and c are optional", "All are keyword-only", "a is keyword-only; c is positional-only", "a is positional-only; c is keyword-only"], "a": "a is positional-only; c is keyword-only"},
            {"q": "What is a first-class function in Python?", "o": ["A built-in function", "The first function defined", "A function that is faster", "A function that can be passed as an argument, returned, or assigned to a variable"], "a": "A function that can be passed as an argument, returned, or assigned to a variable"},
            {"q": "What does help(fn) display?", "o": ["Source code", "Function type", "Argument count", "The function's docstring"], "a": "The function's docstring"},
            {"q": "What is the result of: def add(a, b=5): return a + b; print(add(3))?", "o": ["Error", "3", "5", "8"], "a": "8"},
        ],
    },
    {
        "order": 4,
        "title": "Data Structures — Lists, Tuples, Sets & Dictionaries",
        "description": "Master Python's built-in data structures: lists (mutable sequences), tuples (immutable sequences), sets (unique collections), and dictionaries (key-value mappings).",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 4: Data Structures — Lists, Tuples, Sets & Dictionaries

Python's four main built-in collection types each serve different purposes.

─── LISTS ─────────────────────────────────────────────────────────────────────
Ordered, mutable, allows duplicates:
    fruits = ["apple", "banana", "cherry"]
    mixed  = [1, "two", 3.0, True]

    fruits[0]          # "apple"
    fruits[-1]         # "cherry"  (negative indexing)
    fruits[1:3]        # ["banana", "cherry"]  (slicing)

    fruits.append("date")        # add to end
    fruits.insert(1, "avocado")  # insert at index
    fruits.remove("banana")      # remove first occurrence by value
    fruits.pop()                 # remove & return last element
    fruits.pop(0)                # remove & return at index
    fruits.sort()                # sort in place
    fruits.reverse()             # reverse in place
    fruits.index("apple")        # find index of value
    fruits.count("apple")        # count occurrences
    len(fruits)                  # length
    "apple" in fruits            # True

    sorted(fruits)               # returns NEW sorted list
    fruits + ["elderberry"]      # concatenation (new list)
    fruits * 2                   # repetition

─── TUPLES ────────────────────────────────────────────────────────────────────
Ordered, IMMUTABLE, allows duplicates:
    point    = (3, 4)
    single   = (42,)        # trailing comma required for single item
    empty    = ()
    packed   = 1, 2, 3      # parentheses optional

    x, y = point            # unpacking
    a, *rest = (1, 2, 3, 4) # a=1, rest=[2,3,4]

    Tuples are faster than lists and safe to use as dictionary keys.

─── SETS ──────────────────────────────────────────────────────────────────────
Unordered, mutable, NO DUPLICATES:
    nums = {1, 2, 3, 3, 2}    # {1, 2, 3}
    empty_set = set()          # ⚠ {} creates a dict, not a set!

    nums.add(4)
    nums.discard(10)           # no error if missing
    nums.remove(2)             # KeyError if missing

    a = {1, 2, 3};  b = {2, 3, 4}
    a | b    # union:        {1, 2, 3, 4}
    a & b    # intersection: {2, 3}
    a - b    # difference:   {1}
    a ^ b    # symmetric difference: {1, 4}

─── DICTIONARIES ──────────────────────────────────────────────────────────────
Key-value pairs, ordered (Python 3.7+), mutable, keys must be unique & hashable:
    person = {"name": "Alice", "age": 30}

    person["name"]              # "Alice"
    person.get("email", "N/A")  # "N/A" if key missing (no KeyError)
    person["email"] = "a@b.com" # add or update
    del person["age"]           # delete key
    "name" in person            # True (checks keys)

    person.keys()               # dict_keys view
    person.values()             # dict_values view
    person.items()              # dict_items view of (key, value) pairs
    person.update({"age": 31})  # merge/update
    person.pop("age")           # remove and return value
    person.setdefault("city", "Lagos")  # add if key missing

    for key, val in person.items():
        print(key, val)

─── DICT COMPREHENSION ────────────────────────────────────────────────────────
    squares = {n: n**2 for n in range(1, 6)}
    # {1:1, 2:4, 3:9, 4:16, 5:25}

─── CHOOSING THE RIGHT STRUCTURE ──────────────────────────────────────────────
    list  — ordered sequence, need indexing, allow duplicates
    tuple — ordered, immutable, dict keys, function return values
    set   — unique values, fast membership tests, set operations
    dict  — key-value lookup, structured data, JSON-like
""",
        "quiz_title": "Quiz 4 — Lists, Tuples, Sets & Dictionaries",
        "quiz_description": "20 questions on list methods, slicing, tuples, sets, dictionaries, and choosing the right data structure.",
        "time_limit": 20,
        "questions": [
            {"q": "Which built-in data structure is ordered, mutable, and allows duplicates?", "o": ["tuple", "set", "dict", "list"], "a": "list"},
            {"q": "Which built-in data structure is ordered and IMMUTABLE?", "o": ["list", "set", "dict", "tuple"], "a": "tuple"},
            {"q": "Which built-in data structure is unordered and stores only UNIQUE values?", "o": ["list", "tuple", "dict", "set"], "a": "set"},
            {"q": "What does list.append(x) do?", "o": ["Inserts x at the beginning", "Inserts x at a given index", "Removes x from the list", "Adds x to the end of the list"], "a": "Adds x to the end of the list"},
            {"q": "What does list.pop() do with no argument?", "o": ["Removes the first element", "Returns but does not remove last element", "Raises an error", "Removes and returns the last element"], "a": "Removes and returns the last element"},
            {"q": "What does list[-1] return?", "o": ["An error", "None", "The first element", "The last element"], "a": "The last element"},
            {"q": "What does [1, 2, 3, 4, 5][1:4] return?", "o": ["[1, 2, 3]", "[2, 3, 4, 5]", "[1, 2, 3, 4]", "[2, 3, 4]"], "a": "[2, 3, 4]"},
            {"q": "How do you create an empty set in Python?", "o": ["{}", "set[]", "empty_set()", "set()"], "a": "set()"},
            {"q": "Why does {} create a dict and not a set?", "o": ["It is a Python bug", "Sets use [] brackets", "Sets require at least one element to be inferred", "Empty curly braces are always interpreted as an empty dict by Python"], "a": "Empty curly braces are always interpreted as an empty dict by Python"},
            {"q": "Which set operator produces the UNION of two sets?", "o": ["&", "-", "^", "|"], "a": "|"},
            {"q": "Which set operator produces the INTERSECTION of two sets?", "o": ["|", "-", "^", "&"], "a": "&"},
            {"q": "What does dict.get('key', default) do?", "o": ["Raises KeyError if missing", "Returns None always", "Adds the key if missing", "Returns the value or the default if the key is missing"], "a": "Returns the value or the default if the key is missing"},
            {"q": "What does 'key' in dict check?", "o": ["Whether the value exists", "Whether the key and value match", "Whether the dict is empty", "Whether the key exists in the dictionary"], "a": "Whether the key exists in the dictionary"},
            {"q": "What does dict.items() return?", "o": ["A list of keys", "A list of values", "A sorted dict", "A view of (key, value) pairs"], "a": "A view of (key, value) pairs"},
            {"q": "What makes tuples useful as dictionary keys?", "o": ["They are ordered", "They allow duplicates", "They are faster to iterate", "They are immutable and therefore hashable"], "a": "They are immutable and therefore hashable"},
            {"q": "What does list.sort() do vs sorted(list)?", "o": ["They are identical", "sorted() is faster", "list.sort() returns a new list; sorted() sorts in place", "list.sort() sorts in place; sorted() returns a new sorted list"], "a": "list.sort() sorts in place; sorted() returns a new sorted list"},
            {"q": "What is a dict comprehension?", "o": ["A way to loop over dict keys", "A method to merge dicts", "A way to copy a dict", "{key: value for item in iterable} creating a new dict"], "a": "{key: value for item in iterable} creating a new dict"},
            {"q": "How do you create a single-element tuple?", "o": ["(42)", "[42]", "{42}", "(42,)"], "a": "(42,)"},
            {"q": "What does set.discard(x) do if x is NOT in the set?", "o": ["Returns False", "Adds x instead", "Raises a KeyError", "Does nothing (no error)"], "a": "Does nothing (no error)"},
            {"q": "What does set.remove(x) do if x is NOT in the set?", "o": ["Returns None", "Adds x instead", "Does nothing", "Raises a KeyError"], "a": "Raises a KeyError"},
        ],
    },
    {
        "order": 5,
        "title": "Strings & String Methods",
        "description": "Work with Python strings: indexing, slicing, immutability, concatenation, f-strings, and essential methods like split, join, strip, replace, find, format, upper, lower, and more.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 5: Strings & String Methods

Strings in Python are immutable sequences of Unicode characters.

─── CREATING STRINGS ──────────────────────────────────────────────────────────
    s1 = 'single quotes'
    s2 = "double quotes"
    s3 = \"\"\"multi
    line\"\"\"
    raw = r"C:\\Users\\Alice"   # raw string — backslashes are literal
    byte = b"data"             # bytes literal

─── INDEXING & SLICING ────────────────────────────────────────────────────────
    s = "Hello, World!"
    s[0]      # 'H'
    s[-1]     # '!'
    s[7:12]   # 'World'
    s[:5]     # 'Hello'
    s[::2]    # every other character
    s[::-1]   # reverse the string

─── IMMUTABILITY ──────────────────────────────────────────────────────────────
    s = "hello"
    s[0] = "H"   # TypeError! Strings are immutable.
    s = "Hello"  # must reassign to change

─── CONCATENATION & REPETITION ────────────────────────────────────────────────
    "Hello" + ", " + "World"   # "Hello, World"
    "ha" * 3                    # "hahaha"
    ⚠ Use str.join() for many strings (much faster than + in a loop)

─── F-STRINGS & FORMAT ────────────────────────────────────────────────────────
    name = "Alice"; score = 95.678
    f"Name: {name}, Score: {score:.2f}"   # "Name: Alice, Score: 95.68"
    f"{2 ** 10 = }"    # "2 ** 10 = 1024"  (= for debugging)

    # .format() method
    "{} is {}".format("Alice", 30)
    "{name} is {age}".format(name="Alice", age=30)

─── COMMON STRING METHODS ─────────────────────────────────────────────────────
Case:
    s.upper()           # "HELLO"
    s.lower()           # "hello"
    s.title()           # "Hello World"
    s.capitalize()      # "Hello world"
    s.swapcase()        # swap upper/lower

Search & Test:
    s.find("lo")        # index of first occurrence (-1 if not found)
    s.index("lo")       # like find but raises ValueError if not found
    s.count("l")        # count occurrences
    s.startswith("He")  # True/False
    s.endswith("!")     # True/False
    s.isdigit()         # True if all characters are digits
    s.isalpha()         # True if all characters are letters
    s.isalnum()         # True if all characters are letters or digits
    s.isspace()         # True if all whitespace

Modify:
    s.strip()           # remove leading/trailing whitespace
    s.lstrip()          # remove leading whitespace
    s.rstrip()          # remove trailing whitespace
    s.replace("o","0")  # replace all occurrences
    s.split(",")        # split by delimiter → list
    s.split()           # split by whitespace (any amount)
    ",".join(["a","b","c"])  # "a,b,c"
    s.zfill(10)         # pad with zeros on the left

Alignment:
    s.center(20, "-")   # "----Hello World-----"
    s.ljust(20)         # left-align, pad right
    s.rjust(20)         # right-align, pad left

─── MULTILINE & ESCAPE SEQUENCES ─────────────────────────────────────────────
    \\n   newline
    \\t   tab
    \\\\   backslash
    \\'   single quote inside single-quoted string

─── STRING CHECKING ───────────────────────────────────────────────────────────
    "hello" in "say hello world"   # True (substring check)
    len("hello")                   # 5
    ord('A')                       # 65 (Unicode code point)
    chr(65)                        # 'A'
""",
        "quiz_title": "Quiz 5 — Strings & String Methods",
        "quiz_description": "20 questions on string indexing, slicing, immutability, f-strings, and key string methods.",
        "time_limit": 20,
        "questions": [
            {"q": "Are Python strings mutable?", "o": ["Yes, always", "Yes, but only with methods", "Only in Python 2", "No, strings are immutable"], "a": "No, strings are immutable"},
            {"q": "What does s[::-1] do?", "o": ["Returns every other character", "Returns last character", "Returns first character", "Reverses the string"], "a": "Reverses the string"},
            {"q": "What does 'hello'[1:4] return?", "o": ["'hell'", "'hel'", "'ello'", "'ell'"], "a": "'ell'"},
            {"q": "Which method removes leading and trailing whitespace?", "o": ["s.clean()", "s.trim()", "s.remove()", "s.strip()"], "a": "s.strip()"},
            {"q": "Which method splits a string into a list by a delimiter?", "o": ["s.break()", "s.partition()", "s.divide()", "s.split()"], "a": "s.split()"},
            {"q": "Which method joins a list of strings into one string?", "o": ["list.combine()", "str.concat()", "list.join()", "separator.join(list)"], "a": "separator.join(list)"},
            {"q": "What does s.replace('o', '0') do?", "o": ["Replaces only the first 'o'", "Removes all 'o's", "Replaces only the last 'o'", "Replaces ALL occurrences of 'o' with '0'"], "a": "Replaces ALL occurrences of 'o' with '0'"},
            {"q": "What does s.find('x') return if 'x' is not in the string?", "o": ["None", "0", "ValueError", "-1"], "a": "-1"},
            {"q": "What does s.index('x') do if 'x' is not in the string?", "o": ["Returns -1", "Returns None", "Returns 0", "Raises ValueError"], "a": "Raises ValueError"},
            {"q": "What does s.upper() return?", "o": ["The string with first letter capitalised", "An unchanged string", "A lowercased string", "The string converted to all uppercase"], "a": "The string converted to all uppercase"},
            {"q": "What does s.startswith('He') return?", "o": ["The first 2 characters", "The index of 'He'", "False always", "True if the string starts with 'He'"], "a": "True if the string starts with 'He'"},
            {"q": "What does s.isdigit() return?", "o": ["True if string has digits anywhere", "The digit count", "The first digit", "True if ALL characters are digits"], "a": "True if ALL characters are digits"},
            {"q": "What does len('hello') return?", "o": ["4", "6", "'hello'", "5"], "a": "5"},
            {"q": "What does a raw string r'C:\\\\path' do?", "o": ["Converts backslashes to forward slashes", "Raises a SyntaxError", "Strips all backslashes", "Treats backslashes as literal characters"], "a": "Treats backslashes as literal characters"},
            {"q": "What is the best way to concatenate many strings efficiently?", "o": ["Using + in a loop", "Using string multiplication", "Using format()", "Using ''.join(list_of_strings)"], "a": "Using ''.join(list_of_strings)"},
            {"q": "What does f'{score:.2f}' do with score = 3.14159?", "o": ["Rounds to nearest int", "Returns '3'", "Formats as a percentage", "Formats the float to 2 decimal places: '3.14'"], "a": "Formats the float to 2 decimal places: '3.14'"},
            {"q": "What does ord('A') return?", "o": ["'a'", "1", "'A'", "65"], "a": "65"},
            {"q": "What does chr(97) return?", "o": ["'A'", "97", "' '", "'a'"], "a": "'a'"},
            {"q": "Which method returns True if all characters are letters or digits?", "o": ["isalpha()", "isdigit()", "ischar()", "isalnum()"], "a": "isalnum()"},
            {"q": "What does 'ha' * 3 produce?", "o": ["3", "'ha ha ha'", "'haaa'", "'hahaha'"], "a": "'hahaha'"},
        ],
    },
    {
        "order": 6,
        "title": "File I/O & Exception Handling",
        "description": "Read and write files using open(), context managers (with), file modes, work with JSON and CSV, and handle errors with try/except/else/finally and custom exceptions.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 6: File I/O & Exception Handling

Python makes file operations and error handling clean and Pythonic.

─── OPENING FILES ─────────────────────────────────────────────────────────────
    # Always use context manager (with) — auto-closes file
    with open("data.txt", "r") as f:
        content = f.read()

    File modes:
        "r"   read (default)
        "w"   write (creates/overwrites)
        "a"   append (creates/adds to end)
        "x"   exclusive create (fails if exists)
        "rb"  read binary
        "wb"  write binary
        "r+"  read and write

─── READING FILES ─────────────────────────────────────────────────────────────
    with open("data.txt") as f:
        content   = f.read()          # entire file as one string
        lines     = f.readlines()     # list of lines (with \n)
        first_line = f.readline()     # read one line at a time

    # Most memory-efficient: iterate directly
    with open("data.txt") as f:
        for line in f:
            print(line.strip())

─── WRITING FILES ─────────────────────────────────────────────────────────────
    with open("output.txt", "w") as f:
        f.write("Hello, World!\n")
        f.writelines(["line 1\n", "line 2\n"])

─── JSON ──────────────────────────────────────────────────────────────────────
    import json

    # Python → JSON string
    data = {"name": "Alice", "age": 30}
    json_str = json.dumps(data, indent=2)

    # JSON string → Python
    parsed = json.loads(json_str)

    # Write to file
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

    # Read from file
    with open("data.json") as f:
        data = json.load(f)

─── CSV ───────────────────────────────────────────────────────────────────────
    import csv

    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Age"])
        writer.writerow(["Alice", 30])

    with open("data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row["Name"])

─── EXCEPTION HANDLING ────────────────────────────────────────────────────────
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("Cannot divide by zero")
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
    else:
        print("No error!")        # runs only if no exception
    finally:
        print("Always runs")     # cleanup code

─── COMMON BUILT-IN EXCEPTIONS ───────────────────────────────────────────────
    ValueError        — right type, wrong value (int("abc"))
    TypeError         — wrong type (1 + "a")
    IndexError        — list index out of range
    KeyError          — dict key not found
    AttributeError    — object has no such attribute
    NameError         — variable not defined
    FileNotFoundError — file does not exist
    ZeroDivisionError — division by zero
    StopIteration     — iterator exhausted
    RuntimeError      — generic runtime error

─── RAISING EXCEPTIONS ────────────────────────────────────────────────────────
    raise ValueError("Age must be positive")
    raise TypeError(f"Expected int, got {type(x).__name__}")

─── CUSTOM EXCEPTIONS ─────────────────────────────────────────────────────────
    class InsufficientFundsError(Exception):
        def __init__(self, amount, balance):
            super().__init__(f"Need {amount}, but balance is {balance}")
            self.amount  = amount
            self.balance = balance

    raise InsufficientFundsError(100, 50)

─── CONTEXT MANAGERS ──────────────────────────────────────────────────────────
The with statement ensures cleanup even if an error occurs.
Equivalent to try/finally for resource management.
    with open("file.txt") as f:
        data = f.read()
    # f.close() called automatically here
""",
        "quiz_title": "Quiz 6 — File I/O & Exception Handling",
        "quiz_description": "20 questions on file modes, reading/writing, JSON, CSV, try/except, common exceptions, and context managers.",
        "time_limit": 20,
        "questions": [
            {"q": "What is the recommended way to open files in Python?", "o": ["open().close()", "file = open(); file.close()", "try: open() finally: close()", "with open() as f:"], "a": "with open() as f:"},
            {"q": "Which file mode opens a file for WRITING and creates it if it doesn't exist?", "o": ['"r"', '"a"', '"x"', '"w"'], "a": '"w"'},
            {"q": "Which file mode APPENDS to a file without overwriting existing content?", "o": ['"w"', '"r+"', '"x"', '"a"'], "a": '"a"'},
            {"q": "What does f.read() return?", "o": ["A list of lines", "The first line only", "A list of characters", "The entire file contents as one string"], "a": "The entire file contents as one string"},
            {"q": "What does f.readlines() return?", "o": ["A single string", "An iterator", "The first line", "A list of all lines (including newlines)"], "a": "A list of all lines (including newlines)"},
            {"q": "Which json function converts a Python object to a JSON STRING?", "o": ["json.load()", "json.encode()", "json.dump()", "json.dumps()"], "a": "json.dumps()"},
            {"q": "Which json function writes a Python object to a JSON FILE?", "o": ["json.dumps()", "json.write()", "json.loads()", "json.dump()"], "a": "json.dump()"},
            {"q": "Which json function parses a JSON STRING into a Python object?", "o": ["json.load()", "json.decode()", "json.dump()", "json.loads()"], "a": "json.loads()"},
            {"q": "What does the 'else' block in try/except do?", "o": ["Runs when an exception occurs", "Always runs", "Runs before try", "Runs only when NO exception was raised"], "a": "Runs only when NO exception was raised"},
            {"q": "What does the 'finally' block in try/except do?", "o": ["Runs only on success", "Runs only on failure", "Is optional and rarely needed", "Always runs, whether an exception occurred or not"], "a": "Always runs, whether an exception occurred or not"},
            {"q": "Which exception is raised when a dictionary key is not found?", "o": ["IndexError", "ValueError", "AttributeError", "KeyError"], "a": "KeyError"},
            {"q": "Which exception is raised when a list index is out of range?", "o": ["KeyError", "ValueError", "OverflowError", "IndexError"], "a": "IndexError"},
            {"q": "Which exception is raised when you try to convert 'abc' to an int?", "o": ["TypeError", "ParseError", "CastError", "ValueError"], "a": "ValueError"},
            {"q": "Which exception is raised for operations on incompatible types (e.g. 1 + 'a')?", "o": ["ValueError", "CastError", "OperationError", "TypeError"], "a": "TypeError"},
            {"q": "How do you raise an exception manually?", "o": ["throw ValueError('msg')", "error ValueError('msg')", "except ValueError('msg')", "raise ValueError('msg')"], "a": "raise ValueError('msg')"},
            {"q": "How do you create a custom exception class?", "o": ["class MyError(BaseError):", "class MyError(RuntimeError):", "class MyError:", "class MyError(Exception):"], "a": "class MyError(Exception):"},
            {"q": "What is the benefit of using 'with open()' over manually calling close()?", "o": ["It reads faster", "It uses less memory", "It prevents duplicate reads", "The file is automatically closed even if an error occurs"], "a": "The file is automatically closed even if an error occurs"},
            {"q": "Which exception is raised when a file is not found?", "o": ["IOError", "OSError", "MissingFileError", "FileNotFoundError"], "a": "FileNotFoundError"},
            {"q": "What does csv.DictReader do?", "o": ["Writes CSV as a dict", "Reads CSV with the first row as column headers, each row as a dict", "Converts dict to CSV", "Creates an empty CSV"], "a": "Reads CSV with the first row as column headers, each row as a dict"},
            {"q": "Which exception is raised when referencing a variable that hasn't been defined?", "o": ["AttributeError", "TypeError", "ReferenceError", "NameError"], "a": "NameError"},
        ],
    },
    {
        "order": 7,
        "title": "Object-Oriented Programming — Classes & Objects",
        "description": "Understand OOP in Python: defining classes, __init__, instance and class attributes, methods, inheritance, super(), dunder methods, encapsulation, and polymorphism.",
        "duration_minutes": 45,
        "content": """Welcome to Lesson 7: Object-Oriented Programming — Classes & Objects

OOP organises code into objects that bundle data (attributes) and behaviour (methods).

─── DEFINING A CLASS ──────────────────────────────────────────────────────────
    class Dog:
        species = "Canis lupus"   # class attribute (shared by all instances)

        def __init__(self, name, breed):
            self.name  = name     # instance attribute
            self.breed = breed

        def bark(self):
            return f"{self.name} says Woof!"

        def __str__(self):
            return f"Dog({self.name}, {self.breed})"

    rex = Dog("Rex", "Labrador")
    rex.bark()           # "Rex says Woof!"
    str(rex)             # "Dog(Rex, Labrador)"

─── SELF ──────────────────────────────────────────────────────────────────────
    'self' refers to the current instance.
    It must be the first parameter of every instance method.
    Python passes it automatically — you never pass it explicitly.

─── CLASS vs INSTANCE ATTRIBUTES ─────────────────────────────────────────────
    Class attributes: defined at class level, shared by all instances.
    Instance attributes: defined inside __init__, unique to each instance.
    Instance attribute shadows class attribute if they share the same name.

─── INHERITANCE ───────────────────────────────────────────────────────────────
    class Animal:
        def __init__(self, name):
            self.name = name
        def speak(self):
            raise NotImplementedError

    class Cat(Animal):
        def speak(self):
            return f"{self.name} says Meow!"

    class Dog(Animal):
        def speak(self):
            return f"{self.name} says Woof!"

    animals = [Cat("Whiskers"), Dog("Rex")]
    for a in animals:
        print(a.speak())   # polymorphism

─── SUPER() ───────────────────────────────────────────────────────────────────
    class GoldenRetriever(Dog):
        def __init__(self, name):
            super().__init__(name, "Golden Retriever")
        def fetch(self):
            return f"{self.name} fetches the ball!"

─── DUNDER (MAGIC) METHODS ────────────────────────────────────────────────────
    __init__    — called on object creation
    __str__     — string representation (print(), str())
    __repr__    — unambiguous representation (repr(), REPL)
    __len__     — len(obj)
    __eq__      — obj == other
    __lt__      — obj < other
    __add__     — obj + other
    __contains__ — item in obj
    __getitem__ — obj[key]
    __call__    — obj()  (makes object callable)

─── ENCAPSULATION ─────────────────────────────────────────────────────────────
    self._protected   — convention: intended for internal use
    self.__private    — name-mangled: _ClassName__private (harder to access)

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value

─── CLASS METHODS & STATIC METHODS ───────────────────────────────────────────
    class Person:
        count = 0

        @classmethod
        def get_count(cls):       # receives class, not instance
            return cls.count

        @staticmethod
        def validate_age(age):    # no self or cls
            return 0 <= age <= 150

─── isinstance & issubclass ───────────────────────────────────────────────────
    isinstance(rex, Dog)        # True
    isinstance(rex, Animal)     # True (inheritance)
    issubclass(Dog, Animal)     # True
""",
        "quiz_title": "Quiz 7 — OOP: Classes & Objects",
        "quiz_description": "20 questions on class definition, __init__, self, inheritance, super, dunder methods, properties, classmethods, and staticmethods.",
        "time_limit": 20,
        "questions": [
            {"q": "Which method is automatically called when a new object is created?", "o": ["__new__", "__create__", "__start__", "__init__"], "a": "__init__"},
            {"q": "What does 'self' refer to in an instance method?", "o": ["The class itself", "The parent class", "The module", "The current instance of the class"], "a": "The current instance of the class"},
            {"q": "What is the difference between a class attribute and an instance attribute?", "o": ["No difference", "Class attributes are faster", "Class attrs are in __init__; instance attrs are outside", "Class attrs are shared by all instances; instance attrs are unique to each object"], "a": "Class attrs are shared by all instances; instance attrs are unique to each object"},
            {"q": "Which dunder method defines the string representation shown by print()?", "o": ["__repr__", "__format__", "__display__", "__str__"], "a": "__str__"},
            {"q": "Which dunder method defines the unambiguous developer representation shown in the REPL?", "o": ["__str__", "__format__", "__display__", "__repr__"], "a": "__repr__"},
            {"q": "What is inheritance in OOP?", "o": ["Copying an object's data", "Hiding private attributes", "Two classes sharing the same __init__", "A class (subclass) acquiring attributes and methods from another class (superclass)"], "a": "A class (subclass) acquiring attributes and methods from another class (superclass)"},
            {"q": "What does super().__init__() do in a subclass?", "o": ["Creates a new superclass instance", "Overrides the parent's __init__", "Deletes the parent class", "Calls the parent class's __init__ method"], "a": "Calls the parent class's __init__ method"},
            {"q": "What is polymorphism?", "o": ["Having multiple constructors", "Multiple inheritance", "Hiding data inside a class", "Different classes implementing the same method interface with different behaviour"], "a": "Different classes implementing the same method interface with different behaviour"},
            {"q": "What does @property do?", "o": ["Marks an attribute as shared", "Makes a method a class method", "Makes an attribute immutable", "Allows a method to be accessed like an attribute"], "a": "Allows a method to be accessed like an attribute"},
            {"q": "What does @classmethod receive as its first argument?", "o": ["self (the instance)", "Nothing", "The module", "cls (the class itself)"], "a": "cls (the class itself)"},
            {"q": "What does @staticmethod receive as its first argument?", "o": ["self", "cls", "The module", "Nothing — no implicit first argument"], "a": "Nothing — no implicit first argument"},
            {"q": "What does self.__private do to an attribute?", "o": ["Makes it truly inaccessible", "Deletes it on access", "Marks it as read-only", "Name-mangles it to _ClassName__private (harder but not impossible to access)"], "a": "Name-mangles it to _ClassName__private (harder but not impossible to access)"},
            {"q": "What does isinstance(obj, MyClass) return?", "o": ["The object's type string", "The class name", "Always True", "True if obj is an instance of MyClass or a subclass of it"], "a": "True if obj is an instance of MyClass or a subclass of it"},
            {"q": "What does issubclass(Dog, Animal) check?", "o": ["Whether Dog has the same methods as Animal", "Whether Dog and Animal are the same class", "Whether Animal inherits from Dog", "Whether Dog is a subclass of Animal"], "a": "Whether Dog is a subclass of Animal"},
            {"q": "Which dunder method is called when len(obj) is used?", "o": ["__size__", "__count__", "__length__", "__len__"], "a": "__len__"},
            {"q": "Which dunder method allows instances to be called like a function?", "o": ["__run__", "__execute__", "__invoke__", "__call__"], "a": "__call__"},
            {"q": "What is encapsulation in OOP?", "o": ["Calling super()", "Sharing attributes across classes", "Running multiple methods at once", "Bundling data and behaviour together and restricting direct access to internals"], "a": "Bundling data and behaviour together and restricting direct access to internals"},
            {"q": "What convention signals that an attribute is 'protected' (internal use)?", "o": ["__double_prefix", "No convention exists", "A trailing underscore attr_", "A single leading underscore _attr"], "a": "A single leading underscore _attr"},
            {"q": "Can a Python class inherit from multiple parent classes?", "o": ["No", "Only in Python 2", "Only with a special keyword", "Yes (multiple inheritance)"], "a": "Yes (multiple inheritance)"},
            {"q": "What does __eq__ define?", "o": ["The object's hash", "The string representation", "The object's sort order", "The == comparison behaviour between objects"], "a": "The == comparison behaviour between objects"},
        ],
    },
    {
        "order": 8,
        "title": "Modules, Packages & the Standard Library",
        "description": "Import and create modules, understand packages with __init__.py, use the standard library (os, sys, math, random, datetime, pathlib, collections, itertools), and manage dependencies with pip.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 8: Modules, Packages & the Standard Library

Python's module system lets you organise code and reuse the vast standard library.

─── IMPORTING MODULES ─────────────────────────────────────────────────────────
    import math                      # import entire module
    import math as m                 # alias
    from math import sqrt, pi        # import specific names
    from math import *               # import all (avoid — pollutes namespace)

    math.sqrt(16)    # 4.0
    sqrt(16)         # 4.0  (after from math import sqrt)

─── CREATING A MODULE ─────────────────────────────────────────────────────────
Any .py file is a module.
    # myutils.py
    def add(a, b):
        return a + b
    PI = 3.14159

    # main.py
    from myutils import add, PI

─── __name__ == "__main__" ────────────────────────────────────────────────────
    # mymodule.py
    def main():
        print("Running as script")

    if __name__ == "__main__":
        main()
    # Code inside this block only runs when the file is executed directly,
    # not when imported as a module.

─── PACKAGES ──────────────────────────────────────────────────────────────────
A package is a directory containing an __init__.py file:
    mypackage/
        __init__.py
        utils.py
        models.py

    from mypackage.utils import helper
    from mypackage import models

─── STANDARD LIBRARY HIGHLIGHTS ──────────────────────────────────────────────
    math:       sqrt, floor, ceil, pi, e, log, pow, factorial
    random:     random(), randint(1,10), choice(lst), shuffle(lst), sample()
    os:         os.getcwd(), os.listdir(), os.mkdir(), os.path.join()
    sys:        sys.argv, sys.exit(), sys.path, sys.version
    datetime:   datetime.now(), date.today(), timedelta(days=7)
    pathlib:    Path("file.txt").exists(), Path.cwd(), Path.glob("*.py")
    json:       dumps, loads, dump, load
    re:         re.search(), re.match(), re.findall(), re.sub()
    collections: Counter, defaultdict, namedtuple, deque, OrderedDict
    itertools:  chain, product, combinations, permutations, groupby, cycle
    functools:  reduce, partial, wraps, lru_cache
    typing:     List, Dict, Optional, Union, Tuple, Any (type hints)

─── COLLECTIONS MODULE ────────────────────────────────────────────────────────
    from collections import Counter, defaultdict, deque, namedtuple

    Counter("hello")          # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
    Counter([1,1,2,3]).most_common(1)  # [(1, 2)]

    dd = defaultdict(list)
    dd["key"].append(1)       # no KeyError for missing keys

    q = deque([1, 2, 3])
    q.appendleft(0)
    q.popleft()               # O(1) vs list.pop(0) which is O(n)

    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    p.x, p.y                  # 3, 4

─── INSTALLING THIRD-PARTY PACKAGES ──────────────────────────────────────────
    pip install requests
    pip install django==4.2
    pip list
    pip freeze > requirements.txt
    pip install -r requirements.txt

─── VIRTUAL ENVIRONMENTS ──────────────────────────────────────────────────────
    python -m venv venv          # create virtual environment
    venv\\Scripts\\activate         # activate (Windows)
    source venv/bin/activate     # activate (Mac/Linux)
    deactivate                   # deactivate
""",
        "quiz_title": "Quiz 8 — Modules, Packages & the Standard Library",
        "quiz_description": "20 questions on imports, creating modules, packages, standard library tools, collections, and pip.",
        "time_limit": 20,
        "questions": [
            {"q": "What is a Python module?", "o": ["A class with special methods", "A built-in function", "A compiled C extension", "Any .py file that can be imported"], "a": "Any .py file that can be imported"},
            {"q": "What makes a directory a Python package?", "o": ["A .pkg file", "A setup.py file", "A __main__.py file", "The presence of an __init__.py file"], "a": "The presence of an __init__.py file"},
            {"q": "Which import style is generally preferred for readability?", "o": ["from module import *", "import module (or from module import specific_name)", "import *", "exec(module)"], "a": "import module (or from module import specific_name)"},
            {"q": "What does 'if __name__ == \"__main__\":' check?", "o": ["Whether the module is installed", "Whether the function is called main", "Whether __main__ is defined", "Whether the file is being run directly (not imported)"], "a": "Whether the file is being run directly (not imported)"},
            {"q": "Which standard library module provides mathematical functions like sqrt and pi?", "o": ["numbers", "numeric", "calc", "math"], "a": "math"},
            {"q": "Which function from the random module picks a random integer in [a, b]?", "o": ["random.random(a, b)", "random.int(a, b)", "random.choice(a, b)", "random.randint(a, b)"], "a": "random.randint(a, b)"},
            {"q": "Which standard library module provides file system path manipulation?", "o": ["files", "filesystem", "os.path only", "pathlib"], "a": "pathlib"},
            {"q": "Which collections class counts hashable object occurrences?", "o": ["defaultdict", "namedtuple", "deque", "Counter"], "a": "Counter"},
            {"q": "Which collections class provides a dict with automatic default values?", "o": ["Counter", "namedtuple", "deque", "defaultdict"], "a": "defaultdict"},
            {"q": "Why is collections.deque better than a list for a queue?", "o": ["It uses less memory", "It supports more methods", "It can hold more items", "appendleft/popleft are O(1) vs list's O(n)"], "a": "appendleft/popleft are O(1) vs list's O(n)"},
            {"q": "What does namedtuple provide?", "o": ["A mutable record type", "A dict with named methods", "A list with named indices", "A tuple subclass with named fields"], "a": "A tuple subclass with named fields"},
            {"q": "Which command installs a third-party Python package?", "o": ["python install package", "import package", "python get package", "pip install package"], "a": "pip install package"},
            {"q": "What does 'pip freeze > requirements.txt' do?", "o": ["Deletes all packages", "Installs packages from a file", "Runs tests", "Saves all installed package versions to requirements.txt"], "a": "Saves all installed package versions to requirements.txt"},
            {"q": "What is a virtual environment?", "o": ["A sandboxed Python interpreter version", "A GUI for Python", "A type of package", "An isolated Python environment with its own packages independent of the system Python"], "a": "An isolated Python environment with its own packages independent of the system Python"},
            {"q": "Which module provides sys.argv?", "o": ["os", "argparse", "io", "sys"], "a": "sys"},
            {"q": "What does sys.argv contain?", "o": ["Python version info", "Environment variables", "Installed packages", "Command-line arguments passed to the script (as a list of strings)"], "a": "Command-line arguments passed to the script (as a list of strings)"},
            {"q": "Which itertools function chains multiple iterables together?", "o": ["itertools.combine()", "itertools.merge()", "itertools.zip()", "itertools.chain()"], "a": "itertools.chain()"},
            {"q": "Which functools decorator caches the results of a function call?", "o": ["@functools.cache_result", "@functools.memo", "@functools.cached", "@functools.lru_cache"], "a": "@functools.lru_cache"},
            {"q": "What does 'from math import *' do and why is it discouraged?", "o": ["Imports nothing", "Only imports built-ins", "Raises an ImportError", "Imports all public names — pollutes the namespace and makes it unclear where names come from"], "a": "Imports all public names — pollutes the namespace and makes it unclear where names come from"},
            {"q": "What does os.path.join('folder', 'file.txt') do?", "o": ["Reads the file", "Checks if the file exists", "Concatenates with +", "Creates an OS-appropriate file path string"], "a": "Creates an OS-appropriate file path string"},
        ],
    },
    {
        "order": 9,
        "title": "List Comprehensions, Generators & Functional Tools",
        "description": "Write concise list, dict, and set comprehensions, create memory-efficient generators, use yield, and apply functional tools: map, filter, zip, enumerate, sorted, functools.reduce, and partial.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 9: List Comprehensions, Generators & Functional Tools

Python provides powerful tools for processing collections concisely and efficiently.

─── LIST COMPREHENSIONS ───────────────────────────────────────────────────────
    [expression for item in iterable]
    [expression for item in iterable if condition]

    squares = [x**2 for x in range(1, 6)]
    # [1, 4, 9, 16, 25]

    evens = [x for x in range(10) if x % 2 == 0]
    # [0, 2, 4, 6, 8]

    matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
    # [[1,2,3],[2,4,6],[3,6,9]]

─── DICT COMPREHENSIONS ───────────────────────────────────────────────────────
    {key: value for item in iterable}

    squares = {x: x**2 for x in range(1, 6)}
    # {1:1, 2:4, 3:9, 4:16, 5:25}

    inverted = {v: k for k, v in original.items()}

─── SET COMPREHENSIONS ────────────────────────────────────────────────────────
    {expression for item in iterable}

    unique_lengths = {len(word) for word in words}

─── GENERATOR EXPRESSIONS ─────────────────────────────────────────────────────
Like list comprehensions but LAZY — values computed on demand:
    gen = (x**2 for x in range(1000000))   # no memory allocation yet
    next(gen)    # 0
    next(gen)    # 1
    sum(gen)     # computes lazily

    for val in (x**2 for x in range(5)):
        print(val)

─── GENERATOR FUNCTIONS ───────────────────────────────────────────────────────
    def count_up(start, stop):
        n = start
        while n < stop:
            yield n      # pauses here, returns n, resumes on next()
            n += 1

    gen = count_up(1, 4)
    next(gen)   # 1
    next(gen)   # 2
    list(gen)   # [3]

    yield from  — delegate to a sub-generator:
    def flatten(nested):
        for lst in nested:
            yield from lst

─── THE ITERATOR PROTOCOL ─────────────────────────────────────────────────────
An iterator must implement:
    __iter__()  — returns self
    __next__()  — returns next value or raises StopIteration

─── MAP, FILTER, ZIP, ENUMERATE ───────────────────────────────────────────────
    map(func, iterable)     — apply func to each item (returns iterator)
    filter(func, iterable)  — keep items where func returns True (iterator)
    zip(iter1, iter2)       — pair up items from multiple iterables
    enumerate(iter, start)  — add an index counter

    list(map(str.upper, ["a", "b"]))     # ["A", "B"]
    list(filter(None, [0, 1, "", "hi"])) # [1, "hi"]
    list(zip([1,2], ["a","b"]))          # [(1,"a"),(2,"b")]

    ✔ Prefer list/dict/set comprehensions over map/filter — more readable.

─── SORTED & REVERSED ─────────────────────────────────────────────────────────
    sorted(iterable, key=fn, reverse=True)
    sorted(people, key=lambda p: p["age"])
    sorted(words, key=str.lower)

    reversed(list)    # returns reverse iterator

─── FUNCTOOLS.REDUCE ──────────────────────────────────────────────────────────
    from functools import reduce
    reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)  # 10

─── FUNCTOOLS.PARTIAL ─────────────────────────────────────────────────────────
    from functools import partial
    double = partial(lambda x, n: x * n, n=2)
    double(5)   # 10

─── ANY & ALL ─────────────────────────────────────────────────────────────────
    any([False, True, False])   # True  (at least one truthy)
    all([True, True, True])     # True  (all truthy)
    any([])                     # False
    all([])                     # True  (vacuously true)

─── WALRUS OPERATOR (:=, Python 3.8+) ─────────────────────────────────────────
    # Assign and test in one expression
    while chunk := f.read(8192):
        process(chunk)

    results = [y for x in data if (y := transform(x)) is not None]
""",
        "quiz_title": "Quiz 9 — Comprehensions, Generators & Functional Tools",
        "quiz_description": "20 questions on list/dict/set comprehensions, generator functions, yield, map, filter, sorted, reduce, any, all, and walrus.",
        "time_limit": 20,
        "questions": [
            {"q": "What does [x**2 for x in range(5)] produce?", "o": ["[1, 4, 9, 16, 25]", "[0, 1, 2, 3, 4]", "[1, 2, 3, 4, 5]", "[0, 1, 4, 9, 16]"], "a": "[0, 1, 4, 9, 16]"},
            {"q": "What does [x for x in range(10) if x % 2 == 0] produce?", "o": ["[1,3,5,7,9]", "[0,2,4,6,8,10]", "[2,4,6,8]", "[0,2,4,6,8]"], "a": "[0,2,4,6,8]"},
            {"q": "What syntax creates a DICT comprehension?", "o": ["[k: v for ...]", "(k: v for ...)", "{k, v for ...}", "{k: v for ...}"], "a": "{k: v for ...}"},
            {"q": "What syntax creates a SET comprehension?", "o": ["[expr for ...]", "(expr for ...)", "{k: v for ...}", "{expr for ...}"], "a": "{expr for ...}"},
            {"q": "What is the key difference between a list comprehension and a generator expression?", "o": ["Generator expressions are slower", "No difference", "List comprehensions are lazy; generators are eager", "Generator expressions are lazy (values on demand); list comprehensions build the full list in memory"], "a": "Generator expressions are lazy (values on demand); list comprehensions build the full list in memory"},
            {"q": "What does the 'yield' keyword do in a function?", "o": ["Returns a value and ends the function", "Imports a module", "Raises a StopIteration", "Pauses the function and returns a value, resuming on the next call to next()"], "a": "Pauses the function and returns a value, resuming on the next call to next()"},
            {"q": "What does a generator function return when called?", "o": ["The first yielded value", "A list of all values", "None", "A generator object (iterator)"], "a": "A generator object (iterator)"},
            {"q": "What does next() do on a generator?", "o": ["Resets it", "Skips to the last value", "Creates a new generator", "Returns the next yielded value"], "a": "Returns the next yielded value"},
            {"q": "What exception is raised when a generator is exhausted?", "o": ["GeneratorExit", "IndexError", "RuntimeError", "StopIteration"], "a": "StopIteration"},
            {"q": "What does map(func, iterable) return in Python 3?", "o": ["A list", "None", "A tuple", "A lazy iterator"], "a": "A lazy iterator"},
            {"q": "What does filter(func, iterable) keep?", "o": ["Items where func returns False", "All items", "The first item that passes", "Items where func returns True (truthy)"], "a": "Items where func returns True (truthy)"},
            {"q": "What does sorted(items, reverse=True) do?", "o": ["Sorts in place descending", "Reverses the list", "Sorts in place ascending", "Returns a new list sorted in descending order"], "a": "Returns a new list sorted in descending order"},
            {"q": "What does any([False, False, True]) return?", "o": ["False", "None", "0", "True"], "a": "True"},
            {"q": "What does all([True, True, False]) return?", "o": ["True", "None", "1", "False"], "a": "False"},
            {"q": "What does all([]) return?", "o": ["None", "False", "Raises ValueError", "True (vacuously true)"], "a": "True (vacuously true)"},
            {"q": "What does functools.reduce(lambda a, b: a + b, [1,2,3,4], 0) return?", "o": ["0", "1", "24", "10"], "a": "10"},
            {"q": "What does 'yield from sub_gen' do?", "o": ["Imports sub_gen as a module", "Stops the generator", "Copies sub_gen's values into a list", "Delegates to sub_gen, yielding all its values one by one"], "a": "Delegates to sub_gen, yielding all its values one by one"},
            {"q": "What is the walrus operator (:=)?", "o": ["The floor division operator", "The not-equal operator", "The tuple packing operator", "An assignment expression that assigns AND returns a value"], "a": "An assignment expression that assigns AND returns a value"},
            {"q": "When should you prefer a generator over a list comprehension?", "o": ["When you need random access", "When you need to reverse the results", "When the list is small", "When working with large datasets where you don't need all values in memory at once"], "a": "When working with large datasets where you don't need all values in memory at once"},
            {"q": "What does functools.partial do?", "o": ["Splits a function into two", "Caches function results", "Makes a function lazy", "Creates a new function with some arguments pre-filled"], "a": "Creates a new function with some arguments pre-filled"},
        ],
    },
    {
        "order": 10,
        "title": "Final Review — Comprehensive Python Assessment",
        "description": "A 100-question comprehensive quiz covering all nine Python lessons from basics to advanced functional programming.",
        "duration_minutes": 100,
        "content": """Welcome to Lesson 10: Final Review — Comprehensive Python Assessment

This is your final assessment covering everything from Lessons 1 through 9.

Topics covered:
  1. Python basics — syntax, variables & data types
  2. Control flow — conditionals & loops
  3. Functions — definitions, arguments & scope
  4. Data structures — lists, tuples, sets & dictionaries
  5. Strings & string methods
  6. File I/O & exception handling
  7. Object-oriented programming — classes & objects
  8. Modules, packages & the standard library
  9. List comprehensions, generators & functional tools

You have 100 questions and 100 minutes. 70% required to pass.

Good luck!
""",
        "quiz_title": "Final Quiz — Comprehensive Python (100 Questions)",
        "quiz_description": "100-question comprehensive assessment covering all Python topics from the entire course.",
        "time_limit": 100,
        "questions": [
            # Basics (1–12)
            {"q": "Which function prints output in Python?", "o": ["echo()", "console.log()", "printf()", "print()"], "a": "print()"},
            {"q": "What does dynamic typing mean in Python?", "o": ["Variables can only hold numbers", "Types are checked at compile time", "Variables cannot change value", "You don't need to declare a variable's type"], "a": "You don't need to declare a variable's type"},
            {"q": "What does bool(0) return?", "o": ["True", "None", "1", "False"], "a": "False"},
            {"q": "What does typeof 3.14 return in Python?", "o": ["'float'", "Nothing — use type()", "'number'", "'decimal'"], "a": "Nothing — use type()"},
            {"q": "What does 2 ** 8 evaluate to?", "o": ["16", "64", "512", "256"], "a": "256"},
            {"q": "What does 10 % 3 evaluate to?", "o": ["3", "0", "3.33", "1"], "a": "1"},
            {"q": "What does int('42') return?", "o": ["'42'", "42.0", "Error", "42"], "a": "42"},
            {"q": "What is the result of 9 // 2?", "o": ["4.5", "5", "4.0", "4"], "a": "4"},
            {"q": "What is None in Python?", "o": ["False", "0", "Empty string", "Absence of a value"], "a": "Absence of a value"},
            {"q": "Which operator checks identity (same object)?", "o": ["==", "===", "equals()", "is"], "a": "is"},
            {"q": "What is the result of '2' + 2 in Python?", "o": ["'22'", "22", "4", "TypeError"], "a": "TypeError"},
            {"q": "What does isinstance(3.14, float) return?", "o": ["False", "None", "3.14", "True"], "a": "True"},
            # Control Flow (13–22)
            {"q": "What defines code blocks in Python?", "o": ["Curly braces", "Parentheses", "Keywords", "Indentation"], "a": "Indentation"},
            {"q": "What is the Python 'else if' keyword?", "o": ["else if", "elseif", "otherwise", "elif"], "a": "elif"},
            {"q": "What is Python's ternary expression?", "o": ["condition ? a : b", "a if condition else b", "if cond: a else: b", "cond -> a | b"], "a": "a if condition else b"},
            {"q": "Which is FALSY in Python?", "o": ["[0]", "'False'", "1", "{}"], "a": "{}"},
            {"q": "Which loop runs the body at least once?", "o": ["for", "while", "for...in", "do...while — Python has no do-while, while is closest"], "a": "do...while — Python has no do-while, while is closest"},
            {"q": "What does range(1, 6) produce?", "o": ["[0,1,2,3,4,5]", "[1,2,3,4,5,6]", "[0,1,2,3,4]", "[1,2,3,4,5]"], "a": "[1,2,3,4,5]"},
            {"q": "What does 'pass' do?", "o": ["Ends a function", "Skips a loop", "Exits the program", "A no-op placeholder for an empty block"], "a": "A no-op placeholder for an empty block"},
            {"q": "When does the loop's else clause run?", "o": ["Every iteration", "On error", "Never", "When the loop finishes without break"], "a": "When the loop finishes without break"},
            {"q": "What does enumerate(lst, start=1) do?", "o": ["Skips first item", "Counts from 0", "Sorts from index 1", "Starts the index at 1 instead of 0"], "a": "Starts the index at 1 instead of 0"},
            {"q": "What does zip(['a','b'],[1,2]) yield?", "o": ["['a','b',1,2]", "('a','b'),(1,2)", "('a',1,2)", "[('a',1),('b',2)]"], "a": "[('a',1),('b',2)]"},
            # Functions (23–32)
            {"q": "Which keyword defines a function?", "o": ["function", "func", "fn", "def"], "a": "def"},
            {"q": "What does a function return with no return statement?", "o": ["0", "False", "''", "None"], "a": "None"},
            {"q": "What does *args collect?", "o": ["Keyword arguments", "Named parameters", "All arguments as a dict", "Extra positional arguments as a tuple"], "a": "Extra positional arguments as a tuple"},
            {"q": "What does **kwargs collect?", "o": ["Positional arguments", "All args as a list", "Named params only", "Extra keyword arguments as a dict"], "a": "Extra keyword arguments as a dict"},
            {"q": "What is the LEGB rule?", "o": ["A style guide", "Memory allocation order", "A versioning scheme", "Variable lookup order: Local, Enclosing, Global, Built-in"], "a": "Variable lookup order: Local, Enclosing, Global, Built-in"},
            {"q": "What is a lambda function?", "o": ["A class method", "A recursive function", "A built-in function", "A small anonymous single-expression function"], "a": "A small anonymous single-expression function"},
            {"q": "What is a decorator?", "o": ["A comment style", "A type annotation", "A class attr", "A function that wraps another function to extend behaviour"], "a": "A function that wraps another function to extend behaviour"},
            {"q": "Why avoid mutable default arguments?", "o": ["They cause a syntax error", "They slow the function", "They are not allowed", "The default is shared across all calls — mutations persist"], "a": "The default is shared across all calls — mutations persist"},
            {"q": "Can Python functions return multiple values?", "o": ["No", "Only with keyword", "Only tuples explicitly", "Yes, as a tuple"], "a": "Yes, as a tuple"},
            {"q": "What does 'nonlocal' do?", "o": ["Creates a global var", "Imports from outer module", "Declares a class variable", "Refers to a variable in the enclosing (outer) function's scope"], "a": "Refers to a variable in the enclosing (outer) function's scope"},
            # Data Structures (33–44)
            {"q": "Which data structure is ordered, mutable, and allows duplicates?", "o": ["tuple", "set", "dict", "list"], "a": "list"},
            {"q": "Which data structure is ordered and IMMUTABLE?", "o": ["list", "set", "dict", "tuple"], "a": "tuple"},
            {"q": "Which data structure stores only UNIQUE values?", "o": ["list", "tuple", "dict", "set"], "a": "set"},
            {"q": "What does list.pop() do?", "o": ["Removes first element", "Returns but keeps last", "Raises an error", "Removes and returns the last element"], "a": "Removes and returns the last element"},
            {"q": "What does [1,2,3,4,5][1:4] return?", "o": ["[1,2,3]", "[2,3,4,5]", "[1,2,3,4]", "[2,3,4]"], "a": "[2,3,4]"},
            {"q": "How do you create an empty set?", "o": ["{}", "set[]", "empty_set()", "set()"], "a": "set()"},
            {"q": "Which set operator gives the INTERSECTION?", "o": ["|", "-", "^", "&"], "a": "&"},
            {"q": "What does dict.get('k', default) do?", "o": ["Raises KeyError", "Returns None always", "Adds key if missing", "Returns value or default if key is missing"], "a": "Returns value or default if key is missing"},
            {"q": "What does dict.items() return?", "o": ["Keys only", "Values only", "Flat values", "View of (key, value) pairs"], "a": "View of (key, value) pairs"},
            {"q": "What does list.sort() vs sorted(list) do?", "o": ["Same thing", "sorted() is in-place", "list.sort() returns new list", "list.sort() sorts in-place; sorted() returns a new list"], "a": "list.sort() sorts in-place; sorted() returns a new list"},
            {"q": "How do you create a single-element tuple?", "o": ["(42)", "[42]", "{42}", "(42,)"], "a": "(42,)"},
            {"q": "What does set.discard(x) do if x is missing?", "o": ["Returns False", "Adds x", "Raises KeyError", "Does nothing"], "a": "Does nothing"},
            # Strings (45–52)
            {"q": "Are Python strings mutable?", "o": ["Yes", "Only with methods", "In Python 2 only", "No"], "a": "No"},
            {"q": "What does 'hello'[::-1] produce?", "o": ["'h'", "'o'", "'hello'", "'olleh'"], "a": "'olleh'"},
            {"q": "Which method splits a string into a list?", "o": ["s.break()", "s.partition()", "s.divide()", "s.split()"], "a": "s.split()"},
            {"q": "Which method joins a list into a string?", "o": ["list.combine()", "str.concat()", "list.join()", "sep.join(list)"], "a": "sep.join(list)"},
            {"q": "What does s.strip() do?", "o": ["Splits the string", "Reverses it", "Lowercases it", "Removes leading and trailing whitespace"], "a": "Removes leading and trailing whitespace"},
            {"q": "What does s.find('x') return when 'x' is absent?", "o": ["None", "0", "ValueError", "-1"], "a": "-1"},
            {"q": "What does f'{3.14:.2f}' produce?", "o": ["'3'", "'3.1'", "'3.140'", "'3.14'"], "a": "'3.14'"},
            {"q": "What does 'ha' * 3 produce?", "o": ["3", "'ha ha ha'", "'haaa'", "'hahaha'"], "a": "'hahaha'"},
            # File I/O & Exceptions (53–62)
            {"q": "What is the recommended way to open files?", "o": ["open().close()", "file=open(); file.close()", "try/finally", "with open() as f:"], "a": "with open() as f:"},
            {"q": "Which mode APPENDS to a file?", "o": ['"w"', '"r"', '"x"', '"a"'], "a": '"a"'},
            {"q": "Which json function converts Python to a JSON string?", "o": ["json.load()", "json.encode()", "json.dump()", "json.dumps()"], "a": "json.dumps()"},
            {"q": "What does 'finally' do in try/except?", "o": ["Runs on success only", "Runs on failure only", "Is rarely needed", "Always runs regardless of exception"], "a": "Always runs regardless of exception"},
            {"q": "Which exception is raised for a missing dict key?", "o": ["IndexError", "ValueError", "AttributeError", "KeyError"], "a": "KeyError"},
            {"q": "Which exception is raised for a wrong type operation?", "o": ["ValueError", "CastError", "OperationError", "TypeError"], "a": "TypeError"},
            {"q": "How do you raise an exception?", "o": ["throw ValueError('msg')", "error ValueError('msg')", "except ValueError('msg')", "raise ValueError('msg')"], "a": "raise ValueError('msg')"},
            {"q": "How do you create a custom exception?", "o": ["class MyError(BaseError):", "class MyError(RuntimeError):", "class MyError:", "class MyError(Exception):"], "a": "class MyError(Exception):"},
            {"q": "Which exception is raised for undefined variable?", "o": ["AttributeError", "TypeError", "ReferenceError", "NameError"], "a": "NameError"},
            {"q": "What does the 'else' block in try/except do?", "o": ["Runs always", "Runs on any exception", "Runs before try", "Runs only when no exception occurred"], "a": "Runs only when no exception occurred"},
            # OOP (63–72)
            {"q": "Which method is called when an object is created?", "o": ["__new__", "__create__", "__start__", "__init__"], "a": "__init__"},
            {"q": "What does 'self' refer to?", "o": ["The class", "The parent class", "The module", "The current instance"], "a": "The current instance"},
            {"q": "Which dunder method is used by print()?", "o": ["__repr__", "__format__", "__display__", "__str__"], "a": "__str__"},
            {"q": "What does super().__init__() do?", "o": ["Creates new superclass instance", "Overrides parent __init__", "Deletes parent class", "Calls the parent's __init__"], "a": "Calls the parent's __init__"},
            {"q": "What is polymorphism?", "o": ["Multiple constructors", "Multiple inheritance", "Hiding data", "Different classes implementing the same interface differently"], "a": "Different classes implementing the same interface differently"},
            {"q": "What does @property allow?", "o": ["Shared attribute", "Class method", "Immutable attribute", "A method accessed like an attribute"], "a": "A method accessed like an attribute"},
            {"q": "What does @classmethod receive as first arg?", "o": ["self", "Nothing", "Module", "cls (the class)"], "a": "cls (the class)"},
            {"q": "What does @staticmethod receive as first arg?", "o": ["self", "cls", "Module", "Nothing"], "a": "Nothing"},
            {"q": "What does isinstance(obj, MyClass) return?", "o": ["Type string", "Class name", "Always True", "True if obj is instance of MyClass or subclass"], "a": "True if obj is instance of MyClass or subclass"},
            {"q": "Which dunder enables len(obj)?", "o": ["__size__", "__count__", "__length__", "__len__"], "a": "__len__"},
            # Modules (73–80)
            {"q": "What is a Python module?", "o": ["A compiled extension", "A built-in function", "A class", "Any .py file that can be imported"], "a": "Any .py file that can be imported"},
            {"q": "What makes a directory a package?", "o": [".pkg file", "setup.py", "__main__.py", "__init__.py"], "a": "__init__.py"},
            {"q": "What does 'if __name__ == \"__main__\":' check?", "o": ["Module is installed", "Function is main", "__main__ is defined", "File is run directly, not imported"], "a": "File is run directly, not imported"},
            {"q": "Which collections class counts occurrences?", "o": ["defaultdict", "namedtuple", "deque", "Counter"], "a": "Counter"},
            {"q": "Which collections class provides default values?", "o": ["Counter", "namedtuple", "deque", "defaultdict"], "a": "defaultdict"},
            {"q": "Which command installs a package?", "o": ["python install pkg", "import pkg", "python get pkg", "pip install pkg"], "a": "pip install pkg"},
            {"q": "What is a virtual environment?", "o": ["A Python GUI", "A type of package", "A sandboxed interpreter version", "Isolated Python environment with its own packages"], "a": "Isolated Python environment with its own packages"},
            {"q": "What does sys.argv contain?", "o": ["Python version", "Env variables", "Installed packages", "Command-line arguments as a list of strings"], "a": "Command-line arguments as a list of strings"},
            # Comprehensions & Generators (81–100)
            {"q": "What does [x**2 for x in range(4)] produce?", "o": ["[1,4,9,16]", "[0,1,2,3]", "[1,2,3,4]", "[0,1,4,9]"], "a": "[0,1,4,9]"},
            {"q": "What syntax creates a dict comprehension?", "o": ["[k:v for ...]", "(k:v for ...)", "{k,v for ...}", "{k:v for ...}"], "a": "{k:v for ...}"},
            {"q": "What syntax creates a generator expression?", "o": ["[expr for ...]", "{expr for ...}", "{k:v for ...}", "(expr for ...)"], "a": "(expr for ...)"},
            {"q": "What is the key advantage of a generator over a list?", "o": ["Faster random access", "Supports more methods", "Always sorted", "Lazy evaluation — values computed on demand, saving memory"], "a": "Lazy evaluation — values computed on demand, saving memory"},
            {"q": "What does yield do?", "o": ["Returns a value and ends function", "Imports a module", "Raises StopIteration", "Pauses function and returns a value; resumes on next()"], "a": "Pauses function and returns a value; resumes on next()"},
            {"q": "What does a generator function return when called?", "o": ["First yielded value", "A list of values", "None", "A generator object"], "a": "A generator object"},
            {"q": "What exception is raised when a generator is exhausted?", "o": ["GeneratorExit", "IndexError", "RuntimeError", "StopIteration"], "a": "StopIteration"},
            {"q": "What does map(func, lst) return in Python 3?", "o": ["A list", "None", "A tuple", "A lazy iterator"], "a": "A lazy iterator"},
            {"q": "What does filter(func, lst) keep?", "o": ["Items where func is False", "All items", "The first match", "Items where func returns truthy"], "a": "Items where func returns truthy"},
            {"q": "What does any([False, False, True]) return?", "o": ["False", "None", "0", "True"], "a": "True"},
            {"q": "What does all([True, False, True]) return?", "o": ["True", "None", "1", "False"], "a": "False"},
            {"q": "What does all([]) return?", "o": ["None", "False", "ValueError", "True"], "a": "True"},
            {"q": "What does functools.reduce(f, [1,2,3,4], 0) do with f = lambda a,b: a+b?", "o": ["Returns 0", "Returns [1,2,3,4]", "Returns 4", "Returns 10"], "a": "Returns 10"},
            {"q": "What does the walrus operator (:=) do?", "o": ["Floor division", "Not-equal", "Tuple packing", "Assigns and returns a value in one expression"], "a": "Assigns and returns a value in one expression"},
            {"q": "What does yield from sub_gen do?", "o": ["Imports sub_gen", "Stops the generator", "Copies values to a list", "Delegates to sub_gen, yielding all its values"], "a": "Delegates to sub_gen, yielding all its values"},
            {"q": "What does functools.partial do?", "o": ["Splits a function", "Caches results", "Makes function lazy", "Creates a function with some args pre-filled"], "a": "Creates a function with some args pre-filled"},
            {"q": "When should you use a generator instead of a list?", "o": ["For small datasets", "When you need indexing", "Always", "For large datasets where you don't need all values in memory at once"], "a": "For large datasets where you don't need all values in memory at once"},
            {"q": "What does sorted(lst, key=lambda x: -x) do?", "o": ["Sorts ascending", "Removes negatives", "Sorts by absolute value", "Sorts in descending order"], "a": "Sorts in descending order"},
            {"q": "What does functools.lru_cache do?", "o": ["Clears the cache on each call", "Logs function calls", "Makes the function run faster always", "Memoizes function results to avoid repeated computation"], "a": "Memoizes function results to avoid repeated computation"},
            {"q": "Which is more readable for simple transformations — map() or list comprehension?", "o": ["map() always", "They are identical in readability", "Neither — use for loops", "List comprehension is generally considered more readable in Python"], "a": "List comprehension is generally considered more readable in Python"},
        ],
    },
]


class Command(BaseCommand):
    help = "Create a detailed Introduction to Python course: 9 lessons with 20-question quizzes each, plus a 100-question final review."

    def handle(self, *args, **options):
        tutor = User.objects.filter(role="tutor").first()
        if not tutor:
            self.stdout.write(self.style.ERROR("No tutor found. Run create_sample_users first."))
            return
        self.stdout.write(f"Using tutor: {tutor.email}")

        category, _ = Category.objects.get_or_create(
            name="Programming",
            defaults={"description": "Programming languages including Python, JavaScript, and more", "color": "#3B82F6"},
        )

        course, created = Course.objects.get_or_create(
            title="Introduction to Python — Complete Beginner Course",
            instructor=tutor,
            defaults={
                "description": (
                    "A comprehensive, lesson-by-lesson introduction to Python. "
                    "Starting from basic syntax and data types, you progress through control flow, "
                    "functions, data structures, strings, file I/O, exception handling, "
                    "object-oriented programming, the standard library, and modern functional tools. "
                    "Each of the 9 content lessons has a 20-question quiz, "
                    "and the course ends with a 100-question comprehensive final assessment."
                ),
                "short_description": "Master Python from scratch — 9 detailed lessons, 9 quizzes, and a 100-question final exam.",
                "category": category,
                "price": 0.00,
                "is_free": True,
                "difficulty": "beginner",
                "duration_hours": 8,
                "language": "English",
                "status": "published",
            },
        )
        action = "Created" if created else "Found existing"
        self.stdout.write(self.style.SUCCESS(f"{action} course: {course.title}"))

        total_questions_created = 0

        for lesson_data in LESSONS:
            lesson, lesson_created = Lesson.objects.get_or_create(
                course=course,
                order=lesson_data["order"],
                defaults={
                    "title": lesson_data["title"],
                    "description": lesson_data["description"],
                    "lesson_type": "text",
                    "content": to_html_content(lesson_data["content"]),
                    "duration_minutes": lesson_data["duration_minutes"],
                    "is_published": True,
                },
            )
            lesson_action = "Created" if lesson_created else "Found"
            self.stdout.write(f"  {lesson_action} lesson {lesson_data['order']}: {lesson_data['title']}")

            quiz, _ = Quiz.objects.get_or_create(
                lesson=lesson,
                defaults={
                    "title": lesson_data["quiz_title"],
                    "description": lesson_data["quiz_description"],
                    "time_limit_minutes": lesson_data["time_limit"],
                    "passing_score": 70,
                    "max_attempts": 3,
                    "is_published": True,
                },
            )

            existing_q_count = quiz.questions.count()
            expected_q_count = len(lesson_data["questions"])

            if existing_q_count >= expected_q_count:
                self.stdout.write(f"    Quiz already has {existing_q_count} questions — skipping.")
                continue

            quiz.questions.all().delete()

            for i, q in enumerate(lesson_data["questions"], start=1):
                QuizQuestion.objects.create(
                    quiz=quiz,
                    question_text=q["q"],
                    question_type="multiple_choice",
                    order=i,
                    points=1,
                    options=q["o"],
                    correct_answer=q["a"],
                )
            total_questions_created += expected_q_count
            self.stdout.write(self.style.SUCCESS(f"    Added {expected_q_count} questions to: {lesson_data['quiz_title']}"))

        self.stdout.write(self.style.SUCCESS(
            f"\n{'='*60}\n"
            f"  Course   : {course.title}\n"
            f"  Lessons  : {len(LESSONS)} (9 content + 1 final review)\n"
            f"  Quizzes  : {len(LESSONS)} (20 Qs each for lessons 1-9, 100 for final)\n"
            f"  Questions: {total_questions_created} total created this run\n"
            f"  Price    : FREE\n"
            f"  Status   : Published\n"
            f"{'='*60}"
        ))
