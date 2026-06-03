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
        "title": "Variables, Data Types & Operators",
        "description": "Learn how to declare variables with var, let, and const, understand JavaScript's data types, and use arithmetic, comparison, logical, and assignment operators.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 1: Variables, Data Types & Operators

JavaScript is the programming language of the web. It runs in the browser and on servers (Node.js).

─── ADDING JAVASCRIPT TO A PAGE ───────────────────────────────────────────────
    // External file (recommended)
    <script src="app.js"></script>

    // Inline (inside HTML)
    <script>
        console.log("Hello, World!");
    </script>

─── VARIABLES ─────────────────────────────────────────────────────────────────
    var name = "Alice";    // function-scoped, hoisted, avoid in modern JS
    let age  = 25;         // block-scoped, reassignable
    const PI = 3.14159;    // block-scoped, cannot be reassigned

    Use const by default. Use let when you need to reassign. Avoid var.

─── DATA TYPES ────────────────────────────────────────────────────────────────
Primitive types (immutable, passed by value):
    string:    "Hello"  'World'  `Template ${literal}`
    number:    42  3.14  -7  Infinity  NaN
    boolean:   true  false
    null:      null       (intentional absence of value)
    undefined: undefined  (variable declared but not assigned)
    bigint:    9007199254740991n
    symbol:    Symbol("id")

Reference type (passed by reference):
    object:    { name: "Alice", age: 25 }
    array:     [1, 2, 3]    (special object)
    function:  function() {} (callable object)

─── typeof OPERATOR ───────────────────────────────────────────────────────────
    typeof "hello"     // "string"
    typeof 42          // "number"
    typeof true        // "boolean"
    typeof undefined   // "undefined"
    typeof null        // "object"  ← known JS quirk!
    typeof {}          // "object"
    typeof []          // "object"
    typeof function(){} // "function"

─── ARITHMETIC OPERATORS ──────────────────────────────────────────────────────
    +   addition / string concatenation
    -   subtraction
    *   multiplication
    /   division
    %   modulus (remainder)
    **  exponentiation  (2 ** 10 = 1024)
    ++  increment  (x++ or ++x)
    --  decrement  (x-- or --x)

─── COMPARISON OPERATORS ──────────────────────────────────────────────────────
    ==   loose equality   (coerces types: 5 == "5" → true)
    ===  strict equality  (no coercion: 5 === "5" → false) ← use this!
    !=   loose not-equal
    !==  strict not-equal  ← use this!
    >  <  >=  <=

─── LOGICAL OPERATORS ─────────────────────────────────────────────────────────
    &&   AND  (returns first falsy or last value)
    ||   OR   (returns first truthy or last value)
    !    NOT  (inverts boolean)
    ??   Nullish coalescing (returns right side only if left is null/undefined)

─── ASSIGNMENT OPERATORS ──────────────────────────────────────────────────────
    =   +=   -=   *=   /=   %=   **=   &&=   ||=   ??=

─── STRING TEMPLATE LITERALS ──────────────────────────────────────────────────
    const name = "World";
    console.log(`Hello, ${name}!`);   // Hello, World!
    console.log(`2 + 2 = ${2 + 2}`);  // 2 + 2 = 4

─── TYPE COERCION ─────────────────────────────────────────────────────────────
    "5" + 3   → "53"  (number becomes string)
    "5" - 3   → 2     (string becomes number)
    Boolean(0)         → false
    Boolean("")        → false
    Boolean(null)      → false
    Boolean(undefined) → false
    Boolean(NaN)       → false
    // Everything else is truthy
""",
        "quiz_title": "Quiz 1 — Variables, Data Types & Operators",
        "quiz_description": "20 questions on var/let/const, primitive types, typeof, arithmetic, comparison, and logical operators.",
        "time_limit": 20,
        "questions": [
            {"q": "Which keyword declares a block-scoped variable that CAN be reassigned?", "o": ["var", "const", "let", "static"], "a": "let"},
            {"q": "Which keyword declares a block-scoped variable that CANNOT be reassigned?", "o": ["var", "let", "fixed", "const"], "a": "const"},
            {"q": "Which keyword is function-scoped and hoisted (avoid in modern JS)?", "o": ["let", "const", "var", "static"], "a": "var"},
            {"q": "What does typeof null return in JavaScript?", "o": ["\"null\"", "\"undefined\"", "\"boolean\"", "\"object\""], "a": "\"object\""},
            {"q": "What does typeof [] return?", "o": ["\"array\"", "\"list\"", "\"object\"", "\"undefined\""], "a": "\"object\""},
            {"q": "Which operator checks equality WITHOUT type coercion?", "o": ["==", "=", "!=", "==="], "a": "==="},
            {"q": "What does 5 == '5' evaluate to?", "o": ["false", "null", "undefined", "true"], "a": "true"},
            {"q": "What does 5 === '5' evaluate to?", "o": ["true", "null", "undefined", "false"], "a": "false"},
            {"q": "What does the % operator return?", "o": ["The percentage value", "The quotient", "The product", "The remainder of a division"], "a": "The remainder of a division"},
            {"q": "What does 2 ** 8 evaluate to?", "o": ["16", "256", "512", "64"], "a": "256"},
            {"q": "Which operator returns the right-hand value only when the left is null or undefined?", "o": ["||", "&&", "?.", "??"], "a": "??"},
            {"q": "What does Boolean(0) return?", "o": ["true", "null", "0", "false"], "a": "false"},
            {"q": "What does Boolean('') return?", "o": ["true", "null", "0", "false"], "a": "false"},
            {"q": "What is the result of '5' - 3 in JavaScript?", "o": ["'53'", "NaN", "'5-3'", "2"], "a": "2"},
            {"q": "What is the result of '5' + 3 in JavaScript?", "o": ["8", "NaN", "53", "'53'"], "a": "'53'"},
            {"q": "Which of these is NOT a primitive data type in JavaScript?", "o": ["string", "boolean", "number", "array"], "a": "array"},
            {"q": "How do you write a template literal in JavaScript?", "o": ["'Hello ${name}'", "\"Hello ${name}\"", "`Hello ${name}`", "(Hello ${name})"], "a": "`Hello ${name}`"},
            {"q": "What does NaN stand for?", "o": ["Null and Nothing", "No Assigned Number", "Negative and Null", "Not a Number"], "a": "Not a Number"},
            {"q": "What does undefined mean in JavaScript?", "o": ["A variable that doesn't exist", "A variable set to null", "A variable declared but not yet assigned a value", "A deleted variable"], "a": "A variable declared but not yet assigned a value"},
            {"q": "Which is the recommended modern approach for variable declarations?", "o": ["Always use var", "Always use let", "Use const by default, let when reassignment is needed", "Use var for global, let for local"], "a": "Use const by default, let when reassignment is needed"},
        ],
    },
    {
        "order": 2,
        "title": "Control Flow — Conditionals & Loops",
        "description": "Control program execution with if/else, switch, ternary operator, for, while, do-while, for...of, for...in loops, and break/continue.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 2: Control Flow — Conditionals & Loops

Control flow determines the order in which statements execute.

─── IF / ELSE IF / ELSE ───────────────────────────────────────────────────────
    if (condition) {
        // runs when condition is truthy
    } else if (otherCondition) {
        // runs when otherCondition is truthy
    } else {
        // fallback
    }

─── TERNARY OPERATOR ──────────────────────────────────────────────────────────
Shorthand for simple if/else:
    const result = condition ? valueIfTrue : valueIfFalse;

    const label = age >= 18 ? "Adult" : "Minor";

─── SWITCH STATEMENT ──────────────────────────────────────────────────────────
    switch (expression) {
        case "a":
            console.log("Letter A");
            break;
        case "b":
            console.log("Letter B");
            break;
        default:
            console.log("Unknown");
    }
    ⚠ Always add break; to prevent fall-through to the next case.

─── TRUTHY & FALSY VALUES ─────────────────────────────────────────────────────
    Falsy: false, 0, -0, 0n, "", null, undefined, NaN
    Everything else is truthy.

─── FOR LOOP ──────────────────────────────────────────────────────────────────
    for (let i = 0; i < 5; i++) {
        console.log(i);   // 0, 1, 2, 3, 4
    }

─── WHILE LOOP ────────────────────────────────────────────────────────────────
    let i = 0;
    while (i < 5) {
        console.log(i);
        i++;
    }
    ⚠ Ensure the condition eventually becomes false to avoid infinite loops.

─── DO...WHILE LOOP ───────────────────────────────────────────────────────────
    let i = 0;
    do {
        console.log(i);
        i++;
    } while (i < 5);
    The body runs AT LEAST ONCE before the condition is checked.

─── FOR...OF LOOP ─────────────────────────────────────────────────────────────
Iterates over iterable values (arrays, strings, Maps, Sets):
    const fruits = ["apple", "banana", "cherry"];
    for (const fruit of fruits) {
        console.log(fruit);
    }

─── FOR...IN LOOP ─────────────────────────────────────────────────────────────
Iterates over object KEYS (enumerable properties):
    const person = { name: "Alice", age: 25 };
    for (const key in person) {
        console.log(key, person[key]);
    }
    ⚠ Avoid for...in on arrays (use for...of or forEach instead).

─── BREAK & CONTINUE ──────────────────────────────────────────────────────────
    break;      — exits the loop entirely
    continue;   — skips the rest of the current iteration, continues to next

─── LABELED STATEMENTS ────────────────────────────────────────────────────────
    outer: for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            if (j === 1) break outer;  // exits the outer loop
        }
    }
""",
        "quiz_title": "Quiz 2 — Control Flow, Conditionals & Loops",
        "quiz_description": "20 questions on if/else, ternary, switch, for, while, do-while, for...of, for...in, break, and continue.",
        "time_limit": 20,
        "questions": [
            {"q": "What does the ternary operator syntax look like?", "o": ["condition ?? true : false", "if (condition) true else false", "condition ? valueIfTrue : valueIfFalse", "condition -> valueIfTrue || valueIfFalse"], "a": "condition ? valueIfTrue : valueIfFalse"},
            {"q": "What keyword prevents fall-through in a switch statement?", "o": ["stop", "exit", "return", "break"], "a": "break"},
            {"q": "What happens if you omit 'break' in a switch case?", "o": ["The program crashes", "That case is skipped", "Only the default runs", "Execution falls through to the next case"], "a": "Execution falls through to the next case"},
            {"q": "Which of these values is FALSY in JavaScript?", "o": ["'false'", "[]", "{}", "0"], "a": "0"},
            {"q": "Which of these values is TRUTHY in JavaScript?", "o": ["0", "null", "undefined", "[]"], "a": "[]"},
            {"q": "What is the key difference between while and do...while?", "o": ["while is faster", "do...while checks condition first", "while runs at least once", "do...while runs the body at least once before checking the condition"], "a": "do...while runs the body at least once before checking the condition"},
            {"q": "Which loop is best for iterating over the VALUES of an array?", "o": ["for...in", "while", "do...while", "for...of"], "a": "for...of"},
            {"q": "Which loop iterates over the KEYS of an object?", "o": ["for...of", "forEach", "for...values", "for...in"], "a": "for...in"},
            {"q": "What does the break statement do inside a loop?", "o": ["Pauses the loop", "Skips the current iteration", "Restarts the loop", "Exits the loop entirely"], "a": "Exits the loop entirely"},
            {"q": "What does the continue statement do inside a loop?", "o": ["Exits the loop", "Restarts the loop from the beginning", "Skips the rest of the current iteration and moves to the next", "Pauses execution"], "a": "Skips the rest of the current iteration and moves to the next"},
            {"q": "What are the three parts of a standard for loop?", "o": ["init, limit, direction", "start, end, step", "declaration, test, update", "init, condition, increment"], "a": "init, condition, increment"},
            {"q": "How many times does a do...while loop body run if the condition is false from the start?", "o": ["0 times", "2 times", "Infinite times", "1 time"], "a": "1 time"},
            {"q": "Which loop should you avoid using to iterate over arrays?", "o": ["for...of", "forEach", "for (classic)", "for...in"], "a": "for...in"},
            {"q": "What does the default case in a switch statement do?", "o": ["It is required and causes an error if missing", "It runs when no case matches", "It runs before any case", "It runs when the switch expression is null"], "a": "It runs when no case matches"},
            {"q": "What will this code print? for(let i=0;i<3;i++){if(i===1)continue; console.log(i);}", "o": ["0 1 2", "1 2", "0 1", "0 2"], "a": "0 2"},
            {"q": "What will this code print? for(let i=0;i<5;i++){if(i===3)break; console.log(i);}", "o": ["0 1 2 3", "0 1 2 3 4", "0 1 2", "1 2 3"], "a": "0 1 2"},
            {"q": "Which comparison operator should you use in if conditions to avoid type coercion issues?", "o": ["==", "=", "!=", "==="], "a": "==="},
            {"q": "Can a for...of loop iterate over a string?", "o": ["No, strings are not iterable", "Only with a special flag", "Only in Node.js", "Yes, it iterates over each character"], "a": "Yes, it iterates over each character"},
            {"q": "What is the switch statement equivalent to (in terms of comparison)?", "o": ["== comparisons", "typeof comparisons", ">= comparisons", "=== comparisons"], "a": "=== comparisons"},
            {"q": "What is a potential danger of a while loop?", "o": ["It can only run once", "It always skips the first iteration", "It runs slower than for loops", "An infinite loop if the condition never becomes false"], "a": "An infinite loop if the condition never becomes false"},
        ],
    },
    {
        "order": 3,
        "title": "Functions — Declarations, Expressions & Arrow Functions",
        "description": "Master function declarations, function expressions, arrow functions, default parameters, rest parameters, the arguments object, closures, and higher-order functions.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 3: Functions — Declarations, Expressions & Arrow Functions

Functions are the building blocks of JavaScript programs.

─── FUNCTION DECLARATION ──────────────────────────────────────────────────────
    function greet(name) {
        return `Hello, ${name}!`;
    }
    greet("Alice");  // "Hello, Alice!"

    ✔ Hoisted — can be called before the declaration in the code.

─── FUNCTION EXPRESSION ───────────────────────────────────────────────────────
    const greet = function(name) {
        return `Hello, ${name}!`;
    };

    ✗ NOT hoisted — must be defined before calling.

─── ARROW FUNCTION ────────────────────────────────────────────────────────────
    const greet = (name) => `Hello, ${name}!`;

    // Multi-line arrow function
    const add = (a, b) => {
        const result = a + b;
        return result;
    };

    // Single parameter: parentheses optional
    const double = n => n * 2;

    // No parameters: empty parentheses required
    const greetWorld = () => "Hello, World!";

Key differences from regular functions:
    • No own 'this' binding (inherits from surrounding scope)
    • Cannot be used as constructors (no new)
    • No 'arguments' object

─── DEFAULT PARAMETERS ────────────────────────────────────────────────────────
    function greet(name = "World") {
        return `Hello, ${name}!`;
    }
    greet();          // "Hello, World!"
    greet("Alice");   // "Hello, Alice!"

─── REST PARAMETERS ───────────────────────────────────────────────────────────
    function sum(...numbers) {
        return numbers.reduce((total, n) => total + n, 0);
    }
    sum(1, 2, 3, 4);  // 10
    ⚠ Rest parameter must be the LAST parameter.

─── THE ARGUMENTS OBJECT ──────────────────────────────────────────────────────
    function logAll() {
        console.log(arguments);  // array-like object of all arguments
    }
    ⚠ Not available in arrow functions. Use rest params instead.

─── RETURNING VALUES ──────────────────────────────────────────────────────────
    Functions return undefined by default.
    return exits the function immediately.
    A function can return any value (including another function).

─── CLOSURES ──────────────────────────────────────────────────────────────────
A closure is a function that remembers the variables from its outer scope even after the outer function has returned.

    function makeCounter() {
        let count = 0;
        return function() {
            count++;
            return count;
        };
    }
    const counter = makeCounter();
    counter();  // 1
    counter();  // 2
    counter();  // 3

─── HIGHER-ORDER FUNCTIONS ────────────────────────────────────────────────────
Functions that take or return other functions:
    function applyTwice(fn, value) {
        return fn(fn(value));
    }
    applyTwice(x => x * 2, 3);  // 12

─── IIFE (Immediately Invoked Function Expression) ────────────────────────────
    (function() {
        console.log("Runs immediately!");
    })();

─── PURE vs IMPURE FUNCTIONS ──────────────────────────────────────────────────
    Pure:   same inputs → always same output, no side effects
    Impure: modifies external state or produces side effects
""",
        "quiz_title": "Quiz 3 — Functions",
        "quiz_description": "20 questions on declarations, expressions, arrow functions, default/rest params, closures, and higher-order functions.",
        "time_limit": 20,
        "questions": [
            {"q": "Which type of function is hoisted and can be called before its definition?", "o": ["Arrow function", "Function expression", "IIFE", "Function declaration"], "a": "Function declaration"},
            {"q": "Which type of function is NOT hoisted?", "o": ["Function declaration", "Named function", "Hoisted function", "Function expression"], "a": "Function expression"},
            {"q": "What is the arrow function syntax for: function double(n) { return n * 2; }?", "o": ["double = n -> n * 2", "double = (n) => { n * 2 }", "double = n => n * 2", "double => n * 2"], "a": "double = n => n * 2"},
            {"q": "What does an arrow function use for 'this' binding?", "o": ["Its own this context", "The global this", "undefined", "The this of the surrounding (lexical) scope"], "a": "The this of the surrounding (lexical) scope"},
            {"q": "What is a default parameter?", "o": ["A parameter that overrides all others", "A required parameter", "A value used when no argument is provided for that parameter", "A parameter set to null"], "a": "A value used when no argument is provided for that parameter"},
            {"q": "What does the rest parameter (...args) do?", "o": ["Spreads an array into arguments", "Collects all remaining arguments into an array", "Makes all parameters optional", "Creates a copy of arguments"], "a": "Collects all remaining arguments into an array"},
            {"q": "Where must a rest parameter be placed in the parameter list?", "o": ["First", "Anywhere", "Second", "Last"], "a": "Last"},
            {"q": "Which function type does NOT have its own 'arguments' object?", "o": ["Function declaration", "Function expression", "Anonymous function", "Arrow function"], "a": "Arrow function"},
            {"q": "What does a function return if it has no explicit return statement?", "o": ["null", "0", "false", "undefined"], "a": "undefined"},
            {"q": "What is a closure in JavaScript?", "o": ["A function with no parameters", "A function that calls itself", "A sealed object", "A function that remembers variables from its outer scope after the outer function has returned"], "a": "A function that remembers variables from its outer scope after the outer function has returned"},
            {"q": "What is a higher-order function?", "o": ["A function that runs faster", "A function inside a class", "A function with more than 3 parameters", "A function that takes or returns another function"], "a": "A function that takes or returns another function"},
            {"q": "What is an IIFE?", "o": ["An arrow function", "A generator function", "A recursive function", "A function that is defined and called immediately"], "a": "A function that is defined and called immediately"},
            {"q": "Can an arrow function be used as a constructor with 'new'?", "o": ["Yes, always", "Only in strict mode", "Only with prototype", "No"], "a": "No"},
            {"q": "What is a pure function?", "o": ["A function with no parameters", "An arrow function", "A function that always returns the same output for the same input with no side effects", "A function declared with const"], "a": "A function that always returns the same output for the same input with no side effects"},
            {"q": "What does 'return' do when executed inside a function?", "o": ["Pauses the function", "Restarts the function", "Exits the function and returns a value to the caller", "Throws an error"], "a": "Exits the function and returns a value to the caller"},
            {"q": "Which syntax creates a function expression assigned to a variable?", "o": ["function myFn() {}", "const myFn = () => {}", "def myFn() {}", "Both 'const myFn = function() {}' and 'const myFn = () => {}'"], "a": "Both 'const myFn = function() {}' and 'const myFn = () => {}'"},
            {"q": "What is the output of: const add = (a, b=10) => a + b; console.log(add(5));", "o": ["5", "NaN", "undefined", "15"], "a": "15"},
            {"q": "What is function recursion?", "o": ["A function with no return", "A function passed as an argument", "A function that calls itself", "A function inside a loop"], "a": "A function that calls itself"},
            {"q": "What does the spread operator do in a function call?", "o": ["Collects arguments into an array", "Copies the function", "Creates a rest parameter", "Expands an array into individual arguments"], "a": "Expands an array into individual arguments"},
            {"q": "In a closure, where is the outer variable stored?", "o": ["On the global object", "In the call stack", "It is deleted after the outer function returns", "In the function's lexical environment (closure scope)"], "a": "In the function's lexical environment (closure scope)"},
        ],
    },
    {
        "order": 4,
        "title": "Arrays & Array Methods",
        "description": "Create and manipulate arrays using push, pop, shift, unshift, slice, splice, map, filter, reduce, find, findIndex, forEach, some, every, flat, and spread.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 4: Arrays & Array Methods

Arrays store ordered lists of values. JavaScript arrays are dynamic and can hold mixed types.

─── CREATING ARRAYS ───────────────────────────────────────────────────────────
    const fruits = ["apple", "banana", "cherry"];
    const empty  = [];
    const mixed  = [1, "two", true, null, { key: "val" }];

    Access: fruits[0]   // "apple"
    Length: fruits.length  // 3

─── MUTATING METHODS (modify the original array) ──────────────────────────────
    push(val)        — add to end, returns new length
    pop()            — remove from end, returns removed element
    unshift(val)     — add to beginning, returns new length
    shift()          — remove from beginning, returns removed element
    splice(start, deleteCount, ...items)  — remove/insert at any position
    reverse()        — reverses in place
    sort(compareFn)  — sorts in place

─── NON-MUTATING METHODS (return new array) ───────────────────────────────────
    slice(start, end)      — returns a portion (end not included)
    concat(arr2)           — merges arrays
    flat(depth)            — flattens nested arrays
    flatMap(fn)            — map then flat(1)

─── ITERATION METHODS ─────────────────────────────────────────────────────────
    forEach(fn)      — runs fn for each element, returns undefined
    map(fn)          — returns NEW array of transformed values
    filter(fn)       — returns NEW array of elements where fn returns true
    reduce(fn, init) — reduces to a single value
    find(fn)         — returns FIRST element that passes fn (or undefined)
    findIndex(fn)    — returns INDEX of first matching element (or -1)
    some(fn)         — returns true if ANY element passes fn
    every(fn)        — returns true if ALL elements pass fn
    includes(val)    — returns true if val is in the array
    indexOf(val)     — returns index of first occurrence (or -1)

─── EXAMPLES ──────────────────────────────────────────────────────────────────
    const nums = [1, 2, 3, 4, 5];

    nums.map(n => n * 2);          // [2, 4, 6, 8, 10]
    nums.filter(n => n % 2 === 0); // [2, 4]
    nums.reduce((acc, n) => acc + n, 0);  // 15
    nums.find(n => n > 3);         // 4
    nums.some(n => n > 4);         // true
    nums.every(n => n > 0);        // true

─── SPREAD OPERATOR WITH ARRAYS ───────────────────────────────────────────────
    const a = [1, 2, 3];
    const b = [4, 5, 6];
    const combined = [...a, ...b];  // [1, 2, 3, 4, 5, 6]
    const copy     = [...a];        // shallow copy

─── DESTRUCTURING ─────────────────────────────────────────────────────────────
    const [first, second, ...rest] = [1, 2, 3, 4, 5];
    // first = 1, second = 2, rest = [3, 4, 5]

─── ARRAY.FROM & ARRAY.OF ─────────────────────────────────────────────────────
    Array.from("hello")         // ["h", "e", "l", "l", "o"]
    Array.from({length: 3}, (_, i) => i)  // [0, 1, 2]
    Array.of(1, 2, 3)           // [1, 2, 3]

─── SORTING ───────────────────────────────────────────────────────────────────
    [3, 1, 2].sort()             // [1, 2, 3] (lexicographic by default!)
    [10, 9, 21].sort()           // [10, 21, 9]  ← wrong for numbers!
    [10, 9, 21].sort((a, b) => a - b)  // [9, 10, 21] ← correct numeric sort
""",
        "quiz_title": "Quiz 4 — Arrays & Array Methods",
        "quiz_description": "20 questions on array creation, mutation, map, filter, reduce, find, some, every, spread, and destructuring.",
        "time_limit": 20,
        "questions": [
            {"q": "Which array method adds an element to the END of an array?", "o": ["unshift", "shift", "append", "push"], "a": "push"},
            {"q": "Which array method removes the LAST element and returns it?", "o": ["shift", "splice", "unshift", "pop"], "a": "pop"},
            {"q": "Which array method adds an element to the BEGINNING of an array?", "o": ["push", "prepend", "shift", "unshift"], "a": "unshift"},
            {"q": "Which array method removes the FIRST element and returns it?", "o": ["pop", "splice", "unshift", "shift"], "a": "shift"},
            {"q": "Which method returns a NEW array with each element transformed by a function?", "o": ["forEach", "filter", "reduce", "map"], "a": "map"},
            {"q": "Which method returns a NEW array containing only elements that pass a test?", "o": ["map", "find", "some", "filter"], "a": "filter"},
            {"q": "Which method reduces an array to a SINGLE value?", "o": ["map", "filter", "find", "reduce"], "a": "reduce"},
            {"q": "Which method returns the FIRST element that satisfies a condition?", "o": ["findIndex", "filter", "some", "find"], "a": "find"},
            {"q": "Which method returns the INDEX of the first matching element (or -1)?", "o": ["find", "indexOf", "search", "findIndex"], "a": "findIndex"},
            {"q": "Which method returns true if AT LEAST ONE element passes the test?", "o": ["every", "find", "includes", "some"], "a": "some"},
            {"q": "Which method returns true if ALL elements pass the test?", "o": ["some", "find", "includes", "every"], "a": "every"},
            {"q": "What does forEach return?", "o": ["A new array", "The original array", "The last element", "undefined"], "a": "undefined"},
            {"q": "Which method returns a portion of an array WITHOUT modifying the original?", "o": ["splice", "cut", "chunk", "slice"], "a": "slice"},
            {"q": "Which method can remove AND insert elements at a specific position?", "o": ["slice", "split", "cut", "splice"], "a": "splice"},
            {"q": "What does [...arr] do?", "o": ["Sorts the array", "Reverses the array", "Creates a shallow copy of the array", "Flattens the array"], "a": "Creates a shallow copy of the array"},
            {"q": "What does Array.from('hello') return?", "o": ["'hello'", "[\"hello\"]", "['h','e','l','l','o']", "An error"], "a": "['h','e','l','l','o']"},
            {"q": "What is wrong with [10, 9, 21].sort() for numeric sorting?", "o": ["It throws an error", "It sorts in descending order", "It requires numbers to be strings", "It sorts lexicographically (as strings), giving wrong results for numbers"], "a": "It sorts lexicographically (as strings), giving wrong results for numbers"},
            {"q": "How do you correctly sort numbers in ascending order?", "o": [".sort()", ".sort((a,b) => b-a)", ".sort((a,b) => a+b)", ".sort((a,b) => a-b)"], "a": ".sort((a,b) => a-b)"},
            {"q": "What does the flat() method do?", "o": ["Converts array to string", "Sorts array elements", "Removes duplicate values", "Flattens nested arrays into a single array"], "a": "Flattens nested arrays into a single array"},
            {"q": "What does array destructuring const [a, b] = [1, 2, 3] result in?", "o": ["a=1, b=[2,3]", "a=[1,2,3], b=undefined", "a=1, b=2", "An error"], "a": "a=1, b=2"},
        ],
    },
    {
        "order": 5,
        "title": "Objects & Object Methods",
        "description": "Work with object literals, property access, methods, this keyword, object destructuring, spread, Object.keys/values/entries, optional chaining, and prototypes.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 5: Objects & Object Methods

Objects store key-value pairs and are central to JavaScript programming.

─── CREATING OBJECTS ──────────────────────────────────────────────────────────
    // Object literal (most common)
    const person = {
        firstName: "Alice",
        lastName:  "Smith",
        age:       30,
        greet() {
            return `Hi, I'm ${this.firstName}`;
        }
    };

─── ACCESSING PROPERTIES ──────────────────────────────────────────────────────
    person.firstName          // dot notation
    person["firstName"]       // bracket notation (use for dynamic keys)
    const key = "age";
    person[key]               // 30

─── ADDING / MODIFYING / DELETING ─────────────────────────────────────────────
    person.email = "alice@example.com";   // add
    person.age   = 31;                    // modify
    delete person.email;                  // delete

─── THE 'this' KEYWORD ────────────────────────────────────────────────────────
    Inside a regular method: 'this' refers to the object.
    Inside an arrow function: 'this' inherits from the surrounding scope.

─── OBJECT DESTRUCTURING ──────────────────────────────────────────────────────
    const { firstName, age } = person;
    const { firstName: name, age: years } = person;  // rename
    const { firstName, country = "Nigeria" } = person;  // default value

─── SPREAD WITH OBJECTS ───────────────────────────────────────────────────────
    const copy    = { ...person };                    // shallow copy
    const updated = { ...person, age: 31 };          // update a property
    const merged  = { ...obj1, ...obj2 };            // merge two objects

─── COMPUTED PROPERTY NAMES ───────────────────────────────────────────────────
    const key = "name";
    const obj = { [key]: "Alice" };  // { name: "Alice" }

─── SHORTHAND PROPERTIES ──────────────────────────────────────────────────────
    const name = "Alice";
    const age  = 30;
    const person = { name, age };  // { name: "Alice", age: 30 }

─── OBJECT STATIC METHODS ─────────────────────────────────────────────────────
    Object.keys(obj)        — array of own enumerable keys
    Object.values(obj)      — array of own enumerable values
    Object.entries(obj)     — array of [key, value] pairs
    Object.assign(target, src)  — copies properties into target
    Object.freeze(obj)      — makes object immutable
    Object.fromEntries(arr) — creates object from entries array

─── OPTIONAL CHAINING ─────────────────────────────────────────────────────────
Safely access deeply nested properties without throwing on null/undefined:
    person?.address?.city      // undefined instead of TypeError
    arr?.[0]                   // safe array access
    obj?.method?.()            // safe method call

─── CHECKING PROPERTIES ───────────────────────────────────────────────────────
    "firstName" in person      // true (checks own + prototype)
    person.hasOwnProperty("age")  // true (own properties only)

─── PROTOTYPES ────────────────────────────────────────────────────────────────
All objects have a prototype chain. Methods not found on the object are
looked up on its prototype (and up the chain).
    Object.getPrototypeOf(person)  // Person.prototype or Object.prototype
""",
        "quiz_title": "Quiz 5 — Objects & Object Methods",
        "quiz_description": "20 questions on object literals, property access, this, destructuring, spread, Object methods, and optional chaining.",
        "time_limit": 20,
        "questions": [
            {"q": "Which syntax is used to access a property with a dynamic/variable key?", "o": ["obj.key", "obj->key", "obj::key", "obj[key]"], "a": "obj[key]"},
            {"q": "Which keyword refers to the current object inside a regular method?", "o": ["self", "me", "object", "this"], "a": "this"},
            {"q": "What does 'this' refer to inside an arrow function method?", "o": ["The object the method belongs to", "null", "The global object always", "The surrounding (lexical) scope's this"], "a": "The surrounding (lexical) scope's this"},
            {"q": "Which operator removes a property from an object?", "o": ["remove", "null", "unset", "delete"], "a": "delete"},
            {"q": "What does Object.keys(obj) return?", "o": ["An array of values", "An array of [key, value] pairs", "A string of all keys", "An array of own enumerable property keys"], "a": "An array of own enumerable property keys"},
            {"q": "What does Object.values(obj) return?", "o": ["An array of keys", "An array of [key, value] pairs", "An array of own enumerable property values", "A copy of the object"], "a": "An array of own enumerable property values"},
            {"q": "What does Object.entries(obj) return?", "o": ["An array of keys only", "An array of values only", "A flat array of all values", "An array of [key, value] pairs"], "a": "An array of [key, value] pairs"},
            {"q": "What does Object.freeze(obj) do?", "o": ["Converts object to JSON", "Deletes all properties", "Copies the object", "Makes the object immutable (no changes allowed)"], "a": "Makes the object immutable (no changes allowed)"},
            {"q": "What does the spread operator do when used with objects: { ...obj }?", "o": ["Merges two arrays", "Deletes all keys", "Creates a deep clone", "Creates a shallow copy of the object"], "a": "Creates a shallow copy of the object"},
            {"q": "What is optional chaining (?.) used for?", "o": ["Creating optional properties", "Deleting nullable properties", "Short-circuit assignment", "Safely accessing nested properties without throwing on null/undefined"], "a": "Safely accessing nested properties without throwing on null/undefined"},
            {"q": "What does person?.address?.city return if address is undefined?", "o": ["Throws a TypeError", "null", "false", "undefined"], "a": "undefined"},
            {"q": "Which method checks if an object has a specific OWN property?", "o": ["obj.hasKey()", "obj.ownProperty()", "key in obj", "obj.hasOwnProperty()"], "a": "obj.hasOwnProperty()"},
            {"q": "What is the shorthand property syntax when variable and key names match?", "o": ["{ key = value }", "{ key: key }", "{ key: value }", "{ key }"], "a": "{ key }"},
            {"q": "What does { ...obj1, ...obj2 } do when both have the same key?", "o": ["Throws an error", "Creates an array", "The key from obj1 wins", "The key from obj2 overrides obj1's value"], "a": "The key from obj2 overrides obj1's value"},
            {"q": "What are computed property names used for?", "o": ["Making properties private", "Dynamically setting a property key from a variable or expression", "Freezing an object", "Sorting object keys"], "a": "Dynamically setting a property key from a variable or expression"},
            {"q": "What does Object.assign(target, source) do?", "o": ["Creates a deep clone", "Freezes the target", "Copies own enumerable properties from source into target", "Returns an array of keys"], "a": "Copies own enumerable properties from source into target"},
            {"q": "What is a prototype in JavaScript?", "o": ["A blueprint class", "A read-only property", "A copy of an object", "An object from which other objects inherit properties and methods"], "a": "An object from which other objects inherit properties and methods"},
            {"q": "How do you destructure and rename a property? e.g. rename 'name' to 'fullName':", "o": ["const { fullName = name } = obj", "const { name as fullName } = obj", "const { name => fullName } = obj", "const { name: fullName } = obj"], "a": "const { name: fullName } = obj"},
            {"q": "How do you provide a default value in object destructuring?", "o": ["const { key ?? 'default' } = obj", "const { key = 'default' } = obj", "const { key || 'default' } = obj", "const { key: 'default' } = obj"], "a": "const { key = 'default' } = obj"},
            {"q": "What does the 'in' operator check?", "o": ["Whether a key exists only in own properties", "Whether a value exists in an object", "Whether an object is empty", "Whether a property exists on the object OR its prototype chain"], "a": "Whether a property exists on the object OR its prototype chain"},
        ],
    },
    {
        "order": 6,
        "title": "The DOM — Selecting & Manipulating Elements",
        "description": "Use JavaScript to select DOM elements (getElementById, querySelector, etc.), read and change content, attributes, styles, create/append/remove elements, and traverse the DOM.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 6: The DOM — Selecting & Manipulating Elements

The DOM (Document Object Model) is the browser's tree representation of an HTML page.
JavaScript can read and modify any part of it.

─── SELECTING ELEMENTS ────────────────────────────────────────────────────────
    document.getElementById("id")
    document.getElementsByClassName("class")  // HTMLCollection (live)
    document.getElementsByTagName("div")       // HTMLCollection (live)
    document.querySelector(".class")           // first match (CSS selector)
    document.querySelectorAll(".class")        // NodeList of all matches

    ✔ querySelector / querySelectorAll accept any CSS selector.
    ✔ HTMLCollection is live; NodeList from querySelectorAll is static.

─── READING & CHANGING CONTENT ────────────────────────────────────────────────
    element.textContent    // get/set plain text (safe, no HTML parsing)
    element.innerHTML      // get/set HTML string (⚠ XSS risk with user data)
    element.innerText      // visible text (respects CSS display)

─── ATTRIBUTES ────────────────────────────────────────────────────────────────
    element.getAttribute("src")
    element.setAttribute("src", "new.jpg")
    element.removeAttribute("disabled")
    element.hasAttribute("disabled")
    element.dataset.userId     // access data-user-id attribute

─── CSS CLASSES ───────────────────────────────────────────────────────────────
    element.classList.add("active")
    element.classList.remove("active")
    element.classList.toggle("active")       // add if absent, remove if present
    element.classList.contains("active")     // returns true/false
    element.classList.replace("old", "new")

─── INLINE STYLES ─────────────────────────────────────────────────────────────
    element.style.color       = "red";
    element.style.fontSize    = "1.5rem";
    element.style.backgroundColor = "#fff";
    // CSS property names become camelCase in JS

─── CREATING & INSERTING ELEMENTS ─────────────────────────────────────────────
    const div = document.createElement("div");
    div.textContent = "Hello!";
    div.classList.add("card");

    parent.appendChild(div);             // append as last child
    parent.prepend(div);                 // insert as first child
    parent.insertBefore(div, refChild);  // insert before reference
    parent.insertAdjacentHTML("beforeend", "<p>New</p>");

─── REMOVING ELEMENTS ─────────────────────────────────────────────────────────
    element.remove();               // remove self
    parent.removeChild(element);    // remove child

─── DOM TRAVERSAL ─────────────────────────────────────────────────────────────
    element.parentElement
    element.children                 // HTMLCollection of child elements
    element.firstElementChild
    element.lastElementChild
    element.nextElementSibling
    element.previousElementSibling

─── ELEMENT DIMENSIONS & POSITION ────────────────────────────────────────────
    element.getBoundingClientRect()  // DOMRect: top, left, width, height, etc.
    element.offsetWidth / offsetHeight
    element.scrollTop / scrollLeft

─── DOCUMENT & WINDOW ─────────────────────────────────────────────────────────
    document.title = "New Title";
    document.body
    document.head
    window.innerWidth / window.innerHeight
    window.scrollTo(0, 0);
""",
        "quiz_title": "Quiz 6 — The DOM",
        "quiz_description": "20 questions on selecting, reading, modifying, creating, and traversing DOM elements.",
        "time_limit": 20,
        "questions": [
            {"q": "What does DOM stand for?", "o": ["Document Object Management", "Data Object Model", "Display Output Module", "Document Object Model"], "a": "Document Object Model"},
            {"q": "Which method selects the FIRST element matching a CSS selector?", "o": ["document.getElementById()", "document.getElementsByClassName()", "document.querySelectorAll()", "document.querySelector()"], "a": "document.querySelector()"},
            {"q": "Which method returns ALL elements matching a CSS selector as a NodeList?", "o": ["document.querySelector()", "document.getElementById()", "document.getElementsByTagName()", "document.querySelectorAll()"], "a": "document.querySelectorAll()"},
            {"q": "Which property gets or sets the plain text content of an element safely?", "o": ["element.innerHTML", "element.innerText", "element.value", "element.textContent"], "a": "element.textContent"},
            {"q": "Which property can set HTML markup inside an element (XSS risk)?", "o": ["element.textContent", "element.innerText", "element.markup", "element.innerHTML"], "a": "element.innerHTML"},
            {"q": "Which classList method ADDS a class if absent and REMOVES it if present?", "o": ["classList.swap()", "classList.flip()", "classList.switch()", "classList.toggle()"], "a": "classList.toggle()"},
            {"q": "How do you set the background-color of an element via JavaScript?", "o": ["element.style.background-color = 'red'", "element.css.backgroundColor = 'red'", "element.setStyle('background-color', 'red')", "element.style.backgroundColor = 'red'"], "a": "element.style.backgroundColor = 'red'"},
            {"q": "Which method creates a new HTML element?", "o": ["document.newElement()", "document.makeElement()", "document.build()", "document.createElement()"], "a": "document.createElement()"},
            {"q": "Which method appends a child element as the LAST child?", "o": ["parent.prepend()", "parent.insertBefore()", "parent.addChild()", "parent.appendChild()"], "a": "parent.appendChild()"},
            {"q": "Which method removes an element from the DOM?", "o": ["element.hide()", "element.destroy()", "element.delete()", "element.remove()"], "a": "element.remove()"},
            {"q": "How do you access a data-user-id attribute in JavaScript?", "o": ["element.getAttribute('user-id')", "element.data.userId", "element.userIdData", "element.dataset.userId"], "a": "element.dataset.userId"},
            {"q": "Which property gives you the parent element of a DOM node?", "o": ["element.parent", "element.parentNode only", "element.ancestor", "element.parentElement"], "a": "element.parentElement"},
            {"q": "Which property gives all direct child ELEMENTS (not text nodes)?", "o": ["element.childNodes", "element.kids", "element.nodes", "element.children"], "a": "element.children"},
            {"q": "Which method reads the value of a specific attribute?", "o": ["element.readAttribute()", "element.getProperty()", "element.attr()", "element.getAttribute()"], "a": "element.getAttribute()"},
            {"q": "What is the danger of using innerHTML with user-provided data?", "o": ["It removes all styles", "It converts text to uppercase", "It only works in Chrome", "Cross-Site Scripting (XSS) attacks"], "a": "Cross-Site Scripting (XSS) attacks"},
            {"q": "What does querySelectorAll return?", "o": ["A live HTMLCollection", "An array", "The first matching element", "A static NodeList"], "a": "A static NodeList"},
            {"q": "What does getElementsByClassName return?", "o": ["A static NodeList", "The first matching element", "An array", "A live HTMLCollection"], "a": "A live HTMLCollection"},
            {"q": "Which property navigates to the next sibling ELEMENT (skipping text nodes)?", "o": ["element.nextSibling", "element.sibling", "element.nextNode", "element.nextElementSibling"], "a": "element.nextElementSibling"},
            {"q": "What does element.getBoundingClientRect() return?", "o": ["The element's CSS classes", "The element's computed styles", "The element's child count", "A DOMRect with size and position relative to the viewport"], "a": "A DOMRect with size and position relative to the viewport"},
            {"q": "How do you insert HTML immediately before the closing tag of a parent element?", "o": ["parent.appendChild()", "parent.insertBefore()", "parent.prepend()", "parent.insertAdjacentHTML('beforeend', html)"], "a": "parent.insertAdjacentHTML('beforeend', html)"},
        ],
    },
    {
        "order": 7,
        "title": "Events & Event Handling",
        "description": "Handle user and browser events with addEventListener, event types, event object properties, event bubbling and capturing, stopPropagation, preventDefault, and event delegation.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 7: Events & Event Handling

Events are actions or occurrences that happen in the browser (clicks, keypresses, form submissions, etc.).

─── ADDING EVENT LISTENERS ────────────────────────────────────────────────────
    element.addEventListener(type, handler, options);

    const btn = document.querySelector("#btn");
    btn.addEventListener("click", function(event) {
        console.log("Clicked!", event);
    });

    // Arrow function handler
    btn.addEventListener("click", (e) => {
        console.log(e.target);
    });

─── REMOVING EVENT LISTENERS ──────────────────────────────────────────────────
    function handleClick(e) { console.log("clicked"); }
    btn.addEventListener("click", handleClick);
    btn.removeEventListener("click", handleClick);
    ⚠ Must pass the exact same function reference to remove it.

─── COMMON EVENT TYPES ────────────────────────────────────────────────────────
Mouse:      click, dblclick, mousedown, mouseup, mousemove, mouseenter,
            mouseleave, mouseover, mouseout, contextmenu
Keyboard:   keydown, keyup, keypress (deprecated)
Form:       submit, change, input, focus, blur, reset
Window:     load, DOMContentLoaded, resize, scroll, beforeunload
Touch:      touchstart, touchend, touchmove
Clipboard:  copy, cut, paste
Drag:       dragstart, dragend, dragover, drop

─── THE EVENT OBJECT ──────────────────────────────────────────────────────────
    event.type           // "click"
    event.target         // element that triggered the event
    event.currentTarget  // element the listener is attached to
    event.preventDefault()  // stop default browser behaviour (e.g. form submit)
    event.stopPropagation() // stop the event from bubbling up
    event.key            // keyboard key ("Enter", "a", "ArrowUp")
    event.clientX / clientY   // mouse position relative to viewport
    event.pageX / pageY       // mouse position relative to document

─── EVENT BUBBLING ────────────────────────────────────────────────────────────
By default, events bubble UP from the target through ancestors to the document.
    <div id="parent">
        <button id="child">Click</button>
    </div>
    Clicking the button fires: button → div → body → html → document

─── EVENT CAPTURING ───────────────────────────────────────────────────────────
With the third argument { capture: true } (or just true), the listener fires
on the way DOWN before reaching the target.
    parent.addEventListener("click", handler, { capture: true });

─── STOP PROPAGATION ──────────────────────────────────────────────────────────
    event.stopPropagation();       // stops bubbling (or capturing)
    event.stopImmediatePropagation(); // also stops other listeners on same element

─── PREVENT DEFAULT ───────────────────────────────────────────────────────────
    form.addEventListener("submit", (e) => {
        e.preventDefault();  // stop the page from reloading on submit
    });

─── EVENT DELEGATION ──────────────────────────────────────────────────────────
Attach ONE listener to a parent to handle events from many child elements.
Works because of bubbling.
    document.querySelector("#list").addEventListener("click", (e) => {
        if (e.target.matches("li")) {
            console.log("Clicked:", e.target.textContent);
        }
    });
    Benefits: more efficient, works for dynamically added elements.

─── ONCE OPTION ───────────────────────────────────────────────────────────────
    btn.addEventListener("click", handler, { once: true });
    The listener fires only ONCE then removes itself.
""",
        "quiz_title": "Quiz 7 — Events & Event Handling",
        "quiz_description": "20 questions on addEventListener, event types, event object, bubbling, capturing, delegation, preventDefault, and stopPropagation.",
        "time_limit": 20,
        "questions": [
            {"q": "Which method attaches an event listener to a DOM element?", "o": ["element.on()", "element.listen()", "element.attachEvent()", "element.addEventListener()"], "a": "element.addEventListener()"},
            {"q": "Which event object property refers to the element that TRIGGERED the event?", "o": ["event.currentTarget", "event.element", "event.source", "event.target"], "a": "event.target"},
            {"q": "Which event object property refers to the element the listener is ATTACHED TO?", "o": ["event.target", "event.origin", "event.listener", "event.currentTarget"], "a": "event.currentTarget"},
            {"q": "Which method prevents the browser's default action (e.g. form reload)?", "o": ["event.stopDefault()", "event.blockDefault()", "event.stopPropagation()", "event.preventDefault()"], "a": "event.preventDefault()"},
            {"q": "Which method stops an event from bubbling up to parent elements?", "o": ["event.preventDefault()", "event.cancelBubble()", "event.blockBubble()", "event.stopPropagation()"], "a": "event.stopPropagation()"},
            {"q": "What is event bubbling?", "o": ["An event that fires only on child elements", "An event fired multiple times", "An event that only works on inputs", "An event propagating from the target element up through its ancestors"], "a": "An event propagating from the target element up through its ancestors"},
            {"q": "What is event capturing?", "o": ["Recording events to a log", "Stopping event bubbling", "An event propagating from the document DOWN to the target", "Cloning an event"], "a": "An event propagating from the document DOWN to the target"},
            {"q": "What is event delegation?", "o": ["Blocking events on child elements", "Removing event listeners automatically", "Attaching separate listeners to every child element", "Attaching one listener on a parent to handle events from many children (via bubbling)"], "a": "Attaching one listener on a parent to handle events from many children (via bubbling)"},
            {"q": "What is a key benefit of event delegation?", "o": ["It fires events faster", "It works only in Chrome", "It disables bubbling", "It works for dynamically added elements and uses fewer listeners"], "a": "It works for dynamically added elements and uses fewer listeners"},
            {"q": "Which option makes an event listener fire only ONCE then auto-remove?", "o": ["{ single: true }", "{ once: true }", "{ limit: 1 }", "{ one: true }"], "a": "{ once: true }"},
            {"q": "What does event.key return for a keyboard event?", "o": ["The key's ASCII code", "The key's Unicode value", "The name of the key pressed (e.g. 'Enter', 'a')", "The key's position on the keyboard"], "a": "The name of the key pressed (e.g. 'Enter', 'a')"},
            {"q": "Which event fires when the HTML is parsed but before images/stylesheets are loaded?", "o": ["load", "ready", "complete", "DOMContentLoaded"], "a": "DOMContentLoaded"},
            {"q": "Which event fires when the ENTIRE page (including images and stylesheets) has loaded?", "o": ["DOMContentLoaded", "ready", "complete", "load"], "a": "load"},
            {"q": "Which form event fires every time an input value changes (on each keystroke)?", "o": ["change", "keydown", "modify", "input"], "a": "input"},
            {"q": "Which form event fires when an input loses focus?", "o": ["lose", "exit", "unfocus", "blur"], "a": "blur"},
            {"q": "How do you correctly remove an event listener?", "o": ["element.clearEventListener(type)", "element.removeEventListener(type) alone is enough", "element.off(type, handler)", "element.removeEventListener(type, handler) with the same function reference"], "a": "element.removeEventListener(type, handler) with the same function reference"},
            {"q": "What does event.clientX return?", "o": ["The element's left CSS position", "The scroll offset", "The element's width", "The mouse X position relative to the viewport"], "a": "The mouse X position relative to the viewport"},
            {"q": "Which method checks if the event target matches a CSS selector (useful in delegation)?", "o": ["event.target.querySelector()", "event.target.is()", "event.target.test()", "event.target.matches()"], "a": "event.target.matches()"},
            {"q": "What is the third parameter of addEventListener used for?", "o": ["Setting the event priority", "Naming the listener", "Passing data to the handler", "Options like capture, once, or passive"], "a": "Options like capture, once, or passive"},
            {"q": "Which event fires when the user right-clicks an element?", "o": ["rightclick", "auxclick", "mouseright", "contextmenu"], "a": "contextmenu"},
        ],
    },
    {
        "order": 8,
        "title": "Asynchronous JavaScript — Callbacks, Promises & Async/Await",
        "description": "Understand the event loop, callbacks, callback hell, Promises (then/catch/finally), Promise.all/race/allSettled, and modern async/await syntax for handling asynchronous operations.",
        "duration_minutes": 45,
        "content": """Welcome to Lesson 8: Asynchronous JavaScript — Callbacks, Promises & Async/Await

JavaScript is single-threaded but handles async tasks (network requests, timers, file I/O) without blocking.

─── THE EVENT LOOP ────────────────────────────────────────────────────────────
    Call Stack     — executes synchronous code
    Web APIs       — handle async tasks (setTimeout, fetch, etc.)
    Task Queue     — holds callbacks waiting to run
    Event Loop     — moves tasks from queue to stack when stack is empty

─── CALLBACKS ─────────────────────────────────────────────────────────────────
A function passed as an argument to be called later:
    setTimeout(() => {
        console.log("Runs after 1 second");
    }, 1000);

    setTimeout(fn, 0) still runs AFTER all synchronous code.

─── CALLBACK HELL ─────────────────────────────────────────────────────────────
Deeply nested callbacks become unreadable:
    getData(function(result) {
        processData(result, function(processed) {
            saveData(processed, function(saved) {
                // deeply nested...
            });
        });
    });

─── PROMISES ──────────────────────────────────────────────────────────────────
A Promise represents a future value. States: pending → fulfilled | rejected

Creating a promise:
    const promise = new Promise((resolve, reject) => {
        if (success) resolve("data");
        else         reject(new Error("failed"));
    });

Consuming a promise:
    promise
        .then(data  => console.log("Success:", data))
        .catch(err  => console.error("Error:",  err))
        .finally(() => console.log("Always runs"));

─── PROMISE CHAINING ──────────────────────────────────────────────────────────
    fetch("/api/users")
        .then(response => response.json())
        .then(users    => console.log(users))
        .catch(err     => console.error(err));

─── PROMISE STATIC METHODS ────────────────────────────────────────────────────
    Promise.resolve(value)         — creates an already-resolved promise
    Promise.reject(error)          — creates an already-rejected promise

    Promise.all([p1, p2, p3])     — waits for ALL; rejects if ANY rejects
    Promise.allSettled([p1, p2])  — waits for ALL; returns all results
    Promise.race([p1, p2])        — resolves/rejects with the FIRST to settle
    Promise.any([p1, p2])         — resolves with FIRST fulfilled; rejects if ALL reject

─── ASYNC / AWAIT ─────────────────────────────────────────────────────────────
async/await is syntactic sugar over Promises — cleaner, more readable:

    async function fetchUser(id) {
        try {
            const response = await fetch(`/api/users/${id}`);
            const user     = await response.json();
            return user;
        } catch (err) {
            console.error("Error:", err);
        }
    }

    // Arrow function
    const fetchUser = async (id) => {
        const res  = await fetch(`/api/users/${id}`);
        const data = await res.json();
        return data;
    };

Rules:
    • await can only be used INSIDE an async function.
    • async functions always return a Promise.
    • Use try/catch for error handling.

─── PARALLEL EXECUTION WITH ASYNC/AWAIT ───────────────────────────────────────
    // Sequential (slow — waits for each):
    const a = await fetchA();
    const b = await fetchB();

    // Parallel (fast — runs simultaneously):
    const [a, b] = await Promise.all([fetchA(), fetchB()]);

─── FETCH API ─────────────────────────────────────────────────────────────────
    const response = await fetch("https://api.example.com/data");
    const data     = await response.json();

    fetch("https://api.example.com/data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: "Alice" }),
    });
""",
        "quiz_title": "Quiz 8 — Async JavaScript, Promises & Async/Await",
        "quiz_description": "20 questions on callbacks, event loop, promises, then/catch, Promise.all, async/await, and the fetch API.",
        "time_limit": 20,
        "questions": [
            {"q": "What is a callback function?", "o": ["A function that returns another function", "A function that calls itself", "A function defined inside a class", "A function passed as an argument to be called later"], "a": "A function passed as an argument to be called later"},
            {"q": "What are the three possible states of a Promise?", "o": ["start, running, end", "new, processing, done", "waiting, success, failure", "pending, fulfilled, rejected"], "a": "pending, fulfilled, rejected"},
            {"q": "Which Promise method handles a SUCCESSFUL resolution?", "o": [".catch()", ".finally()", ".resolve()", ".then()"], "a": ".then()"},
            {"q": "Which Promise method handles a REJECTED promise?", "o": [".then()", ".finally()", ".error()", ".catch()"], "a": ".catch()"},
            {"q": "Which Promise method always runs regardless of success or failure?", "o": [".then()", ".catch()", ".always()", ".finally()"], "a": ".finally()"},
            {"q": "What does Promise.all([p1, p2, p3]) do?", "o": ["Resolves with the first to settle", "Ignores rejections", "Runs promises one after another", "Waits for ALL promises; rejects immediately if any one rejects"], "a": "Waits for ALL promises; rejects immediately if any one rejects"},
            {"q": "What does Promise.allSettled([p1, p2]) do?", "o": ["Rejects if any promise rejects", "Resolves with the first to settle", "Cancels remaining promises", "Waits for ALL promises and returns all results regardless of success/failure"], "a": "Waits for ALL promises and returns all results regardless of success/failure"},
            {"q": "What does Promise.race([p1, p2]) do?", "o": ["Waits for all to resolve", "Resolves with the slowest promise", "Runs promises sequentially", "Resolves or rejects with the FIRST promise to settle"], "a": "Resolves or rejects with the FIRST promise to settle"},
            {"q": "What does the 'await' keyword do inside an async function?", "o": ["Creates a new promise", "Runs code in parallel", "Skips the promise entirely", "Pauses execution until the promise settles, then returns the resolved value"], "a": "Pauses execution until the promise settles, then returns the resolved value"},
            {"q": "Where can the 'await' keyword be used?", "o": ["Anywhere in JavaScript", "Only inside .then() callbacks", "Only at the top level of a module", "Inside an async function (or at the top level of ES modules)"], "a": "Inside an async function (or at the top level of ES modules)"},
            {"q": "What does an async function always return?", "o": ["A plain value", "undefined", "An array", "A Promise"], "a": "A Promise"},
            {"q": "What is callback hell?", "o": ["Callbacks that never execute", "A single large callback function", "Callbacks that fire too quickly", "Deeply nested callbacks that are hard to read and maintain"], "a": "Deeply nested callbacks that are hard to read and maintain"},
            {"q": "How do you handle errors in an async/await function?", "o": ["Use .catch() after the call", "Use error: parameter", "Use if/else on the result", "Use try/catch blocks"], "a": "Use try/catch blocks"},
            {"q": "What is the event loop responsible for?", "o": ["Running synchronous code only", "Blocking all async operations", "Garbage collection", "Moving tasks from the callback queue to the call stack when the stack is empty"], "a": "Moving tasks from the callback queue to the call stack when the stack is empty"},
            {"q": "What does setTimeout(fn, 0) guarantee?", "o": ["fn runs immediately", "fn runs before all other code", "fn runs synchronously", "fn runs after all synchronous code in the current call stack has finished"], "a": "fn runs after all synchronous code in the current call stack has finished"},
            {"q": "What does fetch() return?", "o": ["The response data directly", "undefined", "A JSON object", "A Promise that resolves with a Response object"], "a": "A Promise that resolves with a Response object"},
            {"q": "Which method on the Response object parses the body as JSON?", "o": ["response.text()", "response.data()", "response.parse()", "response.json()"], "a": "response.json()"},
            {"q": "How do you run two async operations in PARALLEL with async/await?", "o": ["await op1; await op2", "await (op1, op2)", "async(op1); async(op2)", "const [a, b] = await Promise.all([op1(), op2()])"], "a": "const [a, b] = await Promise.all([op1(), op2()])"},
            {"q": "What is the modern replacement for callback-based async code?", "o": ["setTimeout chains", "Event emitters", "Synchronous loops", "Promises and async/await"], "a": "Promises and async/await"},
            {"q": "What does Promise.any([p1, p2, p3]) do?", "o": ["Rejects if any promise rejects", "Waits for all to settle", "Resolves with the first to settle (including rejections)", "Resolves with the FIRST FULFILLED promise; rejects only if ALL reject"], "a": "Resolves with the FIRST FULFILLED promise; rejects only if ALL reject"},
        ],
    },
    {
        "order": 9,
        "title": "ES6+ Modern JavaScript Features",
        "description": "Master modern JavaScript: destructuring, spread/rest, template literals, classes, modules (import/export), symbols, iterators, generators, WeakMap/WeakSet, optional chaining, nullish coalescing, and logical assignment.",
        "duration_minutes": 45,
        "content": """Welcome to Lesson 9: ES6+ Modern JavaScript Features

ES6 (ECMAScript 2015) and beyond introduced major improvements to JavaScript.

─── DESTRUCTURING ─────────────────────────────────────────────────────────────
    // Array destructuring
    const [a, b, ...rest] = [1, 2, 3, 4, 5];

    // Object destructuring
    const { name, age = 0 } = person;
    const { name: fullName } = person;  // rename

─── SPREAD & REST ─────────────────────────────────────────────────────────────
    Spread (...) expands an iterable:
        const copy = [...arr];
        const merged = { ...obj1, ...obj2 };
        fn(...args);

    Rest (...) collects remaining items:
        const [first, ...others] = arr;
        const { a, ...remaining } = obj;
        function fn(...params) {}

─── TEMPLATE LITERALS ─────────────────────────────────────────────────────────
    const msg = `Hello, ${name}! You are ${age} years old.`;
    const html = `
        <div class="card">
            <h2>${title}</h2>
        </div>
    `;

─── CLASSES ───────────────────────────────────────────────────────────────────
    class Animal {
        #sound;                           // private field (ES2022)
        constructor(name, sound) {
            this.name   = name;
            this.#sound = sound;
        }
        speak() {
            return `${this.name} says ${this.#sound}`;
        }
        static create(name, sound) {      // static method
            return new Animal(name, sound);
        }
    }

    class Dog extends Animal {
        constructor(name) {
            super(name, "woof");
        }
        fetch() { return `${this.name} fetches!`; }
    }

    const dog = new Dog("Rex");

─── MODULES ───────────────────────────────────────────────────────────────────
    // math.js — named exports
    export const add = (a, b) => a + b;
    export const PI  = 3.14159;

    // app.js — named imports
    import { add, PI } from "./math.js";

    // default export
    export default function greet(name) { return `Hello, ${name}`; }
    import greet from "./greet.js";

    // import all
    import * as math from "./math.js";
    math.add(1, 2);

─── SYMBOLS ───────────────────────────────────────────────────────────────────
    const id = Symbol("id");   // unique, immutable value
    obj[id] = 123;             // not enumerable, hidden from for...in

─── ITERATORS & GENERATORS ────────────────────────────────────────────────────
    function* count() {
        yield 1;
        yield 2;
        yield 3;
    }
    const gen = count();
    gen.next();  // { value: 1, done: false }

─── MAP & SET ─────────────────────────────────────────────────────────────────
    const map = new Map();
    map.set("key", "value");
    map.get("key");        // "value"
    map.has("key");        // true

    const set = new Set([1, 2, 2, 3]);  // { 1, 2, 3 } — unique values
    set.add(4);
    set.has(2);

─── OPTIONAL CHAINING & NULLISH COALESCING ────────────────────────────────────
    user?.profile?.avatar   // no error if profile is null/undefined
    username ?? "Guest"     // "Guest" only if username is null or undefined
    count ??= 0             // assign 0 only if count is null/undefined

─── LOGICAL ASSIGNMENT ────────────────────────────────────────────────────────
    a ||= b   // a = a || b  (assign b if a is falsy)
    a &&= b   // a = a && b  (assign b if a is truthy)
    a ??= b   // a = a ?? b  (assign b if a is null/undefined)

─── TAGGED TEMPLATE LITERALS ──────────────────────────────────────────────────
    function highlight(strings, ...values) {
        return strings.reduce((acc, str, i) =>
            acc + str + (values[i] !== undefined ? `<b>${values[i]}</b>` : ""), "");
    }
    const name = "Alice";
    highlight`Hello, ${name}!`;  // "Hello, <b>Alice</b>!"
""",
        "quiz_title": "Quiz 9 — ES6+ Modern JavaScript",
        "quiz_description": "20 questions on classes, modules, destructuring, spread/rest, Map, Set, generators, symbols, and modern operators.",
        "time_limit": 20,
        "questions": [
            {"q": "Which ES6 feature allows you to extract values from arrays/objects into variables?", "o": ["Spread", "Rest", "Template literals", "Destructuring"], "a": "Destructuring"},
            {"q": "What does the spread operator (...) do when used with an array?", "o": ["Collects remaining elements", "Reverses the array", "Flattens nested arrays", "Expands the array into individual elements"], "a": "Expands the array into individual elements"},
            {"q": "What does the rest parameter (...args) collect?", "o": ["The first argument only", "Spread values", "Named parameters", "Remaining arguments into an array"], "a": "Remaining arguments into an array"},
            {"q": "What keyword defines a class in JavaScript?", "o": ["object", "struct", "type", "class"], "a": "class"},
            {"q": "Which method is automatically called when a class is instantiated with 'new'?", "o": ["init()", "setup()", "start()", "constructor()"], "a": "constructor()"},
            {"q": "Which keyword calls the parent class's constructor inside a subclass?", "o": ["parent()", "base()", "inherit()", "super()"], "a": "super()"},
            {"q": "Which keyword creates a class that extends another class?", "o": ["implements", "inherits", "from", "extends"], "a": "extends"},
            {"q": "How do you declare a PRIVATE class field in modern JavaScript (ES2022)?", "o": ["private fieldName;", "_fieldName (convention only)", "let #fieldName;", "#fieldName;"], "a": "#fieldName;"},
            {"q": "Which keyword exports a single default value from a module?", "o": ["export named", "module.exports", "export main", "export default"], "a": "export default"},
            {"q": "How do you import a named export called 'add' from './math.js'?", "o": ["import add from './math.js'", "require('./math.js').add", "import { add } from './math.js'", "import * add from './math.js'"], "a": "import { add } from './math.js'"},
            {"q": "What is a Symbol in JavaScript?", "o": ["A string constant", "A numeric identifier", "A private class field", "A unique and immutable primitive value"], "a": "A unique and immutable primitive value"},
            {"q": "What does a generator function use to pause execution and yield a value?", "o": ["return", "pause", "await", "yield"], "a": "yield"},
            {"q": "What does function* indicate?", "o": ["A recursive function", "An async function", "A pure function", "A generator function"], "a": "A generator function"},
            {"q": "What is a Map in JavaScript?", "o": ["A method to transform arrays", "An array of key-value pairs with numeric keys only", "A geographic map object", "A collection of key-value pairs where keys can be any type"], "a": "A collection of key-value pairs where keys can be any type"},
            {"q": "What is a Set in JavaScript?", "o": ["An ordered list like an array", "A key-value collection", "A type of object literal", "A collection of unique values with no duplicates"], "a": "A collection of unique values with no duplicates"},
            {"q": "What does the nullish coalescing operator (??) return?", "o": ["The left side if it is falsy", "The right side if the left is falsy", "null always", "The right side only if the left is null or undefined"], "a": "The right side only if the left is null or undefined"},
            {"q": "What is the difference between || and ?? operators?", "o": ["No difference", "?? is faster", "|| works only with booleans", "|| triggers on any falsy value (0, ''); ?? triggers only on null/undefined"], "a": "|| triggers on any falsy value (0, ''); ?? triggers only on null/undefined"},
            {"q": "What does import * as math from './math.js' do?", "o": ["Imports only the default export", "Imports all named exports into a namespace object called math", "Imports all exports and executes them", "Creates a copy of the module"], "a": "Imports all named exports into a namespace object called math"},
            {"q": "What is a static class method?", "o": ["A method that cannot be overridden", "A method that modifies private fields", "A method called on an instance", "A method called on the class itself, not on instances"], "a": "A method called on the class itself, not on instances"},
            {"q": "What does a??=b do?", "o": ["Sets a to b if a is falsy", "Sets a to b if a is truthy", "Assigns a + b to a", "Assigns b to a only if a is null or undefined"], "a": "Assigns b to a only if a is null or undefined"},
        ],
    },
    {
        "order": 10,
        "title": "Final Review — Comprehensive JavaScript Assessment",
        "description": "A 100-question comprehensive quiz covering all nine JavaScript lessons from variables to ES6+ modern features.",
        "duration_minutes": 100,
        "content": """Welcome to Lesson 10: Final Review — Comprehensive JavaScript Assessment

This is your final assessment covering everything from Lessons 1 through 9.

Topics covered:
  1. Variables, data types & operators
  2. Control flow — conditionals & loops
  3. Functions — declarations, expressions & arrow functions
  4. Arrays & array methods
  5. Objects & object methods
  6. The DOM — selecting & manipulating elements
  7. Events & event handling
  8. Asynchronous JS — callbacks, promises & async/await
  9. ES6+ modern JavaScript features

You have 100 questions and 100 minutes. 70% required to pass.

Good luck!
""",
        "quiz_title": "Final Quiz — Comprehensive JavaScript (100 Questions)",
        "quiz_description": "100-question comprehensive assessment covering all JavaScript topics from the entire course.",
        "time_limit": 100,
        "questions": [
            # Variables & Data Types (1–12)
            {"q": "Which keyword declares a block-scoped, reassignable variable?", "o": ["var", "const", "static", "let"], "a": "let"},
            {"q": "Which keyword declares a block-scoped, non-reassignable variable?", "o": ["var", "let", "fixed", "const"], "a": "const"},
            {"q": "What does typeof null return?", "o": ["\"null\"", "\"undefined\"", "\"boolean\"", "\"object\""], "a": "\"object\""},
            {"q": "What does typeof [] return?", "o": ["\"array\"", "\"list\"", "\"undefined\"", "\"object\""], "a": "\"object\""},
            {"q": "Which operator checks value AND type equality?", "o": ["==", "=", "!=", "==="], "a": "==="},
            {"q": "What does 5 === '5' return?", "o": ["true", "null", "undefined", "false"], "a": "false"},
            {"q": "What does 2 ** 10 evaluate to?", "o": ["20", "200", "512", "1024"], "a": "1024"},
            {"q": "Which operator returns the right side only if the left is null or undefined?", "o": ["||", "&&", "?.", "??"], "a": "??"},
            {"q": "What does Boolean('') return?", "o": ["true", "null", "1", "false"], "a": "false"},
            {"q": "What is the result of '3' + 4 in JavaScript?", "o": ["7", "NaN", "34", "'34'"], "a": "'34'"},
            {"q": "What is the result of '6' - 2 in JavaScript?", "o": ["'62'", "NaN", "'6-2'", "4"], "a": "4"},
            {"q": "Which of these is a primitive type in JavaScript?", "o": ["array", "object", "function", "symbol"], "a": "symbol"},
            # Control Flow (13–22)
            {"q": "What is the ternary operator syntax?", "o": ["condition ?? a : b", "if (cond) a else b", "condition -> a || b", "condition ? a : b"], "a": "condition ? a : b"},
            {"q": "What prevents fall-through in a switch statement?", "o": ["stop", "exit", "return", "break"], "a": "break"},
            {"q": "Which of these is FALSY?", "o": ["'false'", "[]", "{}", "0"], "a": "0"},
            {"q": "Which loop always runs its body at least once?", "o": ["for", "while", "for...of", "do...while"], "a": "do...while"},
            {"q": "Which loop iterates over the VALUES of an array?", "o": ["for...in", "while", "do...while", "for...of"], "a": "for...of"},
            {"q": "Which loop iterates over the KEYS of an object?", "o": ["for...of", "forEach", "for...values", "for...in"], "a": "for...in"},
            {"q": "What does 'continue' do in a loop?", "o": ["Exits the loop", "Restarts from beginning", "Pauses execution", "Skips the rest of the current iteration"], "a": "Skips the rest of the current iteration"},
            {"q": "What does 'break' do in a loop?", "o": ["Pauses the loop", "Skips current iteration", "Restarts the loop", "Exits the loop entirely"], "a": "Exits the loop entirely"},
            {"q": "Switch uses which type of comparison?", "o": ["==", ">=", "!=", "==="], "a": "==="},
            {"q": "What is the danger of a while loop?", "o": ["It runs slower than for", "It can only run once", "It always skips first iteration", "An infinite loop if condition never becomes false"], "a": "An infinite loop if condition never becomes false"},
            # Functions (23–32)
            {"q": "Which function type is hoisted?", "o": ["Arrow function", "Function expression", "IIFE", "Function declaration"], "a": "Function declaration"},
            {"q": "What does an arrow function use for 'this'?", "o": ["Its own this", "The global this", "undefined", "The surrounding scope's this (lexical)"], "a": "The surrounding scope's this (lexical)"},
            {"q": "What is a default parameter?", "o": ["A required parameter", "A parameter overriding others", "A parameter set to null", "A fallback value when no argument is provided"], "a": "A fallback value when no argument is provided"},
            {"q": "Where must a rest parameter appear?", "o": ["First", "Anywhere", "Second", "Last"], "a": "Last"},
            {"q": "What does a function return with no explicit return statement?", "o": ["null", "0", "false", "undefined"], "a": "undefined"},
            {"q": "What is a closure?", "o": ["A function with no parameters", "A sealed object", "A self-calling function", "A function remembering variables from its outer scope"], "a": "A function remembering variables from its outer scope"},
            {"q": "What is a higher-order function?", "o": ["A faster function", "A function inside a class", "A function with many parameters", "A function that takes or returns another function"], "a": "A function that takes or returns another function"},
            {"q": "Can an arrow function be used with 'new'?", "o": ["Yes, always", "Only in strict mode", "Only with prototype", "No"], "a": "No"},
            {"q": "What is an IIFE?", "o": ["A generator function", "An arrow function", "A recursive function", "A function defined and immediately invoked"], "a": "A function defined and immediately invoked"},
            {"q": "What does the spread operator do in a function call?", "o": ["Collects arguments", "Copies the function", "Creates rest params", "Expands an array into individual arguments"], "a": "Expands an array into individual arguments"},
            # Arrays (33–42)
            {"q": "Which method adds to the END of an array?", "o": ["unshift", "shift", "append", "push"], "a": "push"},
            {"q": "Which method removes from the END of an array?", "o": ["shift", "splice", "unshift", "pop"], "a": "pop"},
            {"q": "Which method returns a NEW array of transformed values?", "o": ["forEach", "filter", "reduce", "map"], "a": "map"},
            {"q": "Which method returns a NEW array of elements that pass a test?", "o": ["map", "find", "some", "filter"], "a": "filter"},
            {"q": "Which method reduces an array to a single accumulated value?", "o": ["map", "filter", "find", "reduce"], "a": "reduce"},
            {"q": "Which method returns the FIRST element passing a test?", "o": ["findIndex", "filter", "some", "find"], "a": "find"},
            {"q": "What does forEach return?", "o": ["New array", "Original array", "Last element", "undefined"], "a": "undefined"},
            {"q": "Which method returns true if ALL elements pass a test?", "o": ["some", "find", "includes", "every"], "a": "every"},
            {"q": "Which method returns a portion of an array without modifying the original?", "o": ["splice", "cut", "chunk", "slice"], "a": "slice"},
            {"q": "What does [...arr] create?", "o": ["Sorts the array", "Reverses it", "Flattens it", "A shallow copy"], "a": "A shallow copy"},
            # Objects (43–52)
            {"q": "Which syntax accesses a property with a dynamic key?", "o": ["obj.key", "obj->key", "obj::key", "obj[key]"], "a": "obj[key]"},
            {"q": "What does 'this' refer to inside a regular object method?", "o": ["global object", "undefined", "null", "The object the method belongs to"], "a": "The object the method belongs to"},
            {"q": "Which operator removes a property from an object?", "o": ["remove", "null", "unset", "delete"], "a": "delete"},
            {"q": "What does Object.keys(obj) return?", "o": ["Values array", "[key,value] pairs", "Key string", "Array of own enumerable keys"], "a": "Array of own enumerable keys"},
            {"q": "What does Object.freeze(obj) do?", "o": ["Converts to JSON", "Deletes properties", "Copies the object", "Makes it immutable"], "a": "Makes it immutable"},
            {"q": "What does optional chaining (?.) return if a value is null/undefined?", "o": ["null", "false", "Throws TypeError", "undefined"], "a": "undefined"},
            {"q": "What does { ...obj } create?", "o": ["Deep clone", "Reversed object", "JSON string", "Shallow copy"], "a": "Shallow copy"},
            {"q": "How do you rename a property in object destructuring?", "o": ["{ name as full }", "{ name => full }", "{ name = full }", "{ name: full }"], "a": "{ name: full }"},
            {"q": "What does Object.entries(obj) return?", "o": ["Keys only", "Values only", "Flat values array", "Array of [key, value] pairs"], "a": "Array of [key, value] pairs"},
            {"q": "Does the 'in' operator check the prototype chain?", "o": ["No, own properties only", "Only in strict mode", "Only for arrays", "Yes"], "a": "Yes"},
            # DOM (53–62)
            {"q": "What does DOM stand for?", "o": ["Data Object Management", "Display Output Module", "Document Object Management", "Document Object Model"], "a": "Document Object Model"},
            {"q": "Which method returns the FIRST element matching a CSS selector?", "o": ["getElementById", "getElementsByClassName", "querySelectorAll", "querySelector"], "a": "querySelector"},
            {"q": "Which property safely sets plain text content?", "o": ["innerHTML", "innerText", "value", "textContent"], "a": "textContent"},
            {"q": "What is the XSS risk associated with?", "o": ["textContent", "innerText", "value", "innerHTML with user data"], "a": "innerHTML with user data"},
            {"q": "Which classList method toggles a class on/off?", "o": ["swap()", "flip()", "switch()", "toggle()"], "a": "toggle()"},
            {"q": "Which method creates a new HTML element?", "o": ["newElement()", "makeElement()", "build()", "createElement()"], "a": "createElement()"},
            {"q": "Which method appends a child as the last child?", "o": ["prepend()", "insertBefore()", "addChild()", "appendChild()"], "a": "appendChild()"},
            {"q": "Which method removes an element from the DOM?", "o": ["hide()", "destroy()", "delete()", "remove()"], "a": "remove()"},
            {"q": "How do you access a data-item-id attribute in JavaScript?", "o": ["getAttribute('item-id')", "data.itemId", "itemIdData", "dataset.itemId"], "a": "dataset.itemId"},
            {"q": "Which property navigates to the parent element?", "o": ["element.parent", "parentNode only", "ancestor", "parentElement"], "a": "parentElement"},
            # Events (63–72)
            {"q": "Which method attaches an event listener?", "o": ["element.on()", "element.listen()", "element.attachEvent()", "element.addEventListener()"], "a": "element.addEventListener()"},
            {"q": "Which property is the element that TRIGGERED the event?", "o": ["event.currentTarget", "event.element", "event.source", "event.target"], "a": "event.target"},
            {"q": "Which method prevents the browser's default behaviour?", "o": ["stopDefault()", "blockDefault()", "stopPropagation()", "preventDefault()"], "a": "preventDefault()"},
            {"q": "Which method stops an event from bubbling?", "o": ["preventDefault()", "cancelBubble()", "blockBubble()", "stopPropagation()"], "a": "stopPropagation()"},
            {"q": "What is event delegation?", "o": ["A listener on every child", "Auto-removal after use", "Blocking child events", "One listener on a parent handling events from many children via bubbling"], "a": "One listener on a parent handling events from many children via bubbling"},
            {"q": "Which listener option fires it only once then removes it?", "o": ["{ single: true }", "{ once: true }", "{ limit: 1 }", "{ one: true }"], "a": "{ once: true }"},
            {"q": "Which event fires when HTML is parsed (before images load)?", "o": ["load", "ready", "complete", "DOMContentLoaded"], "a": "DOMContentLoaded"},
            {"q": "Which form event fires on every keystroke in an input?", "o": ["change", "keydown", "modify", "input"], "a": "input"},
            {"q": "Which event fires when an input loses focus?", "o": ["lose", "exit", "unfocus", "blur"], "a": "blur"},
            {"q": "How must you pass the handler to removeEventListener?", "o": ["Any function with the same name", "An inline arrow function", "A new function with the same body", "The exact same function reference used in addEventListener"], "a": "The exact same function reference used in addEventListener"},
            # Async (73–82)
            {"q": "What are the three states of a Promise?", "o": ["start, running, end", "new, processing, done", "waiting, success, failure", "pending, fulfilled, rejected"], "a": "pending, fulfilled, rejected"},
            {"q": "Which Promise method handles a successful result?", "o": [".catch()", ".finally()", ".resolve()", ".then()"], "a": ".then()"},
            {"q": "Which Promise method handles rejection?", "o": [".then()", ".finally()", ".error()", ".catch()"], "a": ".catch()"},
            {"q": "What does Promise.all() do when ONE promise rejects?", "o": ["Continues with remaining", "Resolves with partial results", "Returns undefined", "Rejects immediately"], "a": "Rejects immediately"},
            {"q": "What does Promise.allSettled() do?", "o": ["Rejects if any rejects", "Resolves with first to settle", "Cancels remaining", "Waits for all and returns all results regardless"], "a": "Waits for all and returns all results regardless"},
            {"q": "What must every async function return?", "o": ["A plain value", "undefined", "An array", "A Promise"], "a": "A Promise"},
            {"q": "Where can 'await' be used?", "o": ["Anywhere", "Only in .then()", "Only at top-level", "Inside async functions"], "a": "Inside async functions"},
            {"q": "How do you handle errors in async/await?", "o": ["Use .catch()", "Use error: param", "Use if/else", "Use try/catch"], "a": "Use try/catch"},
            {"q": "What does fetch() return?", "o": ["Response data", "undefined", "JSON object", "A Promise resolving to a Response"], "a": "A Promise resolving to a Response"},
            {"q": "How do you run two async ops in PARALLEL?", "o": ["await a; await b", "await (a, b)", "async(a); async(b)", "await Promise.all([a(), b()])"], "a": "await Promise.all([a(), b()])"},
            # ES6+ (83–100)
            {"q": "What is destructuring?", "o": ["Deleting an object", "Cloning values", "Merging arrays", "Extracting values from arrays/objects into variables"], "a": "Extracting values from arrays/objects into variables"},
            {"q": "Which keyword defines a class?", "o": ["object", "struct", "type", "class"], "a": "class"},
            {"q": "Which method is called when 'new' is used with a class?", "o": ["init()", "setup()", "start()", "constructor()"], "a": "constructor()"},
            {"q": "Which keyword calls the parent class constructor in a subclass?", "o": ["parent()", "base()", "inherit()", "super()"], "a": "super()"},
            {"q": "Which keyword extends a class?", "o": ["implements", "inherits", "from", "extends"], "a": "extends"},
            {"q": "How do you declare a private class field?", "o": ["private field;", "_field", "let #field;", "#field;"], "a": "#field;"},
            {"q": "How do you import a named export 'add' from './math.js'?", "o": ["import add from './math.js'", "require('./math.js').add", "import * add from './math.js'", "import { add } from './math.js'"], "a": "import { add } from './math.js'"},
            {"q": "What is a Symbol?", "o": ["A string constant", "A numeric id", "A private field", "A unique immutable primitive value"], "a": "A unique immutable primitive value"},
            {"q": "What keyword pauses a generator function?", "o": ["return", "pause", "await", "yield"], "a": "yield"},
            {"q": "What is a Map vs a plain object?", "o": ["No difference", "Maps are arrays", "Objects allow any key type", "Maps allow any type as key, including objects and functions"], "a": "Maps allow any type as key, including objects and functions"},
            {"q": "What does a Set guarantee about its values?", "o": ["Sorted order", "String values only", "Indexed access", "All values are unique — no duplicates"], "a": "All values are unique — no duplicates"},
            {"q": "What is the difference between || and ??", "o": ["No difference", "?? is faster", "|| works only with booleans", "|| triggers on any falsy; ?? triggers only on null/undefined"], "a": "|| triggers on any falsy; ?? triggers only on null/undefined"},
            {"q": "What is a static class method?", "o": ["A method that cannot be overridden", "A method modifying private fields", "A method called on instances", "A method called on the class itself"], "a": "A method called on the class itself"},
            {"q": "What does export default do?", "o": ["Exports an array", "Exports all named exports", "Imports a module", "Exports one primary value from a module"], "a": "Exports one primary value from a module"},
            {"q": "What does a??=b do?", "o": ["Sets a to b if falsy", "Sets a to b if truthy", "Adds a and b", "Assigns b to a only if a is null or undefined"], "a": "Assigns b to a only if a is null or undefined"},
            {"q": "What does import * as utils from './utils.js' do?", "o": ["Imports only default", "Executes all exports", "Creates a module copy", "Imports all named exports into a namespace object called utils"], "a": "Imports all named exports into a namespace object called utils"},
            {"q": "What does Promise.race([p1, p2]) do?", "o": ["Waits for all", "Resolves with slowest", "Runs sequentially", "Resolves/rejects with the FIRST promise to settle"], "a": "Resolves/rejects with the FIRST promise to settle"},
            {"q": "What is callback hell?", "o": ["Callbacks firing too fast", "Callbacks that never execute", "A single large callback", "Deeply nested callbacks that are unreadable and hard to maintain"], "a": "Deeply nested callbacks that are unreadable and hard to maintain"},
        ],
    },
]


class Command(BaseCommand):
    help = "Create a detailed Introduction to JavaScript course: 9 lessons each with a 20-question quiz, plus a 100-question final review."

    def handle(self, *args, **options):
        tutor = User.objects.filter(role="tutor").first()
        if not tutor:
            self.stdout.write(self.style.ERROR("No tutor found. Run create_sample_users first."))
            return
        self.stdout.write(f"Using tutor: {tutor.email}")

        category, _ = Category.objects.get_or_create(
            name="Web Development",
            defaults={"description": "Web technologies including HTML, CSS, and JavaScript", "color": "#F97316"},
        )

        course, created = Course.objects.get_or_create(
            title="Introduction to JavaScript — Complete Beginner Course",
            instructor=tutor,
            defaults={
                "description": (
                    "A comprehensive, lesson-by-lesson introduction to JavaScript. "
                    "Starting from variables and data types, you will progress through control flow, "
                    "functions, arrays, objects, DOM manipulation, events, asynchronous programming, "
                    "and modern ES6+ features. "
                    "Each of the 9 content lessons is followed by a 20-question quiz to reinforce learning, "
                    "and the course ends with a 100-question comprehensive final assessment."
                ),
                "short_description": "Master JavaScript from scratch — 9 detailed lessons, 9 quizzes, and a 100-question final exam.",
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
