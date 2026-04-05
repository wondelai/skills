# Code Smells and Heuristics

Comprehensive catalog of code smells organized by category, with identification criteria and targeted refactorings. Based on Robert C. Martin's *Clean Code*, Chapter 17.


## Table of Contents
1. [What Is a Code Smell?](#what-is-a-code-smell)
2. [Comment Smells](#comment-smells)
3. [Environment Smells](#environment-smells)
4. [Function Smells](#function-smells)
5. [General Smells](#general-smells)
6. [Naming Smells](#naming-smells)
7. [Test Smells](#test-smells)
8. [Smell Detection Quick Reference](#smell-detection-quick-reference)

---

## What Is a Code Smell?

A code smell is a surface indication that usually corresponds to a deeper problem in the system. Smells are not bugs -- the code works. But they suggest fragility, rigidity, or unnecessary complexity that will cause problems as the codebase evolves. Learn to recognize smells quickly and you'll know where to focus refactoring effort.

---

## Comment Smells

Comments that indicate problems in the code:

### C1: Inappropriate Information

Comments that hold information better kept in other systems.

| Information type | Where it belongs | Not in comments |
|-----------------|-----------------|-----------------|
| Change history | Git log | Not `// Changed by John on 2024-01-15` |
| Author attribution | `git blame` | Not `// Author: john@company.com` |
| Issue tracking | Jira/GitHub Issues | Not `// Fixes bug #1234` (use commit message) |
| Build instructions | README or Makefile | Not `// Run with -Xmx512m flag` |

**Comments should only contain technical notes about the code itself.**

### C2: Obsolete Comments

Comments that have grown old and are no longer accurate. Code evolves; comments don't always follow.

```java
// BAD: This comment is now a lie
// Returns the total price including 5% tax
public double getTotal() {
    return subtotal * 1.08; // Tax rate changed to 8%, comment not updated
}
```

**Fix:** Delete the comment. If the information is important, express it in the code:

```java
private static final double TAX_RATE = 0.08;

public double getTotal() {
    return subtotal * (1 + TAX_RATE);
}
```

### C3: Redundant Comments

Comments that describe something that adequately describes itself.

```java
i++; // increment i
```

If the code is clear, the comment is noise. If the code is not clear, fix the code.

### C4: Poorly Written Comments

If you're going to write a comment, take the time to write it well. Don't ramble. Don't state the obvious. Use correct grammar and punctuation. Be brief and precise.

### C5: Commented-Out Code

```python
# result = old_algorithm(data)
# if result > threshold:
#     notify_admin(result)
result = new_algorithm(data)
```

Commented-out code rots. Others are afraid to delete it ("maybe someone needs it?"). It accumulates. **Delete it.** Version control is your safety net.

---

## Environment Smells

### E1: Build Requires More Than One Step

You should be able to build the entire system with a single command.

```bash
# GOOD: One command
make build
# or
npm run build
# or
./gradlew build
```

If building requires checkout, install, configure, set env vars, download dependencies separately, the build is fragile and developers will avoid running it.

### E2: Tests Require More Than One Step

You should be able to run all the tests with a single command.

```bash
# GOOD: One command
make test
# or
npm test
# or
pytest
```

If running tests requires starting databases, setting up fixtures manually, or running scripts in a specific order, developers won't run them.

---

## Function Smells

### F1: Too Many Arguments

More than three arguments is a smell. Arguments are hard to understand, hard to remember, and hard to test (every combination of arguments is a test case).

| Arguments | Assessment | Action |
|-----------|------------|--------|
| 0 | Ideal | Keep as is |
| 1 | Good | Common and clear |
| 2 | Acceptable | Ensure natural pairing |
| 3 | Questionable | Can any be grouped into an object? |
| 4+ | Refactor | Introduce parameter object or builder |

**Refactoring:**
```python
# BAD: Too many arguments
def create_user(first_name, last_name, email, phone, address, city, state, zip_code):
    ...

# GOOD: Parameter object
def create_user(personal_info: PersonalInfo, address: Address):
    ...
```

### F2: Output Arguments

Arguments that are modified by the function are confusing. Is the argument input or output?

```java
// BAD: Is report being read or modified?
appendFooter(report);

// GOOD: Method on the object being modified
report.appendFooter();
```

In general, output arguments should be avoided. If a function must change the state of something, have it change the state of the object it is called on.

### F3: Flag Arguments

Boolean arguments loudly declare that the function does two things.

```python
# BAD: Flag argument
def create_account(user_data, is_admin):
    if is_admin:
        # 15 lines of admin setup
    else:
        # 15 lines of regular setup

# GOOD: Separate functions
def create_admin_account(user_data):
    ...

def create_user_account(user_data):
    ...
```

### F4: Dead Functions

Functions that are never called should be deleted. Don't keep them around "just in case." Your version control system remembers them if you ever need them back.

**How to find dead functions:**
- IDE "Find Usages" reports zero callers
- Static analysis tools flag unreachable code
- Code coverage reports show 0% coverage
- Search for the function name across the codebase

---

## General Smells

### G1: Multiple Languages in One Source File

A single source file should contain one language. Mixing HTML, JavaScript, CSS, SQL, and server-side code in one file creates confusion.

| Acceptable | Problematic |
|------------|-------------|
| JavaScript in a `.js` file | SQL strings embedded in Java |
| CSS in a `.css` file | HTML templates inline in Python |
| SQL in a `.sql` migration file | CSS-in-JS with complex logic |

**Minimize** the extent and number of extra languages in source files.

### G2: Obvious Behavior Is Not Implemented

When the obvious behavior of a function is not implemented, readers lose trust in the author.

```python
# SURPRISING: dayOfWeek("Monday") should obviously return Day.MONDAY
def day_of_week(name):
    days = {"Monday": 1, "Tuesday": 2, ...}  # Missing "MONDAY", "monday"
    return days[name]  # Crashes on case variants
```

Follow the Principle of Least Surprise. Users and callers should not be surprised by what a function does.

### G3: Incorrect Behavior at the Boundaries

Don't rely on your intuition for boundary cases. **Write tests for every boundary condition.** Things that commonly fail at boundaries:

| Boundary | Common failure |
|----------|---------------|
| Empty input | NullPointerException, IndexOutOfBounds |
| Single element | Off-by-one in loops |
| Maximum capacity | Buffer overflow, performance cliff |
| Negative values | Unexpected results in calculations |
| Unicode | Encoding issues, wrong string length |
| Concurrent access | Race conditions, deadlocks |

### G4: Overridden Safeties

Turning off warnings, suppressing exceptions, or disabling tests is dangerous.

```python
# BAD: Ignoring the warning doesn't fix the problem
@SuppressWarnings("unchecked")  # Why is this unchecked?
warnings.filterwarnings("ignore")  # What are we hiding?
@pytest.mark.skip("Flaky")  # Fix it instead of skipping
```

Turning off compiler warnings or ignoring failing tests is like ignoring a check-engine light.

### G5: Duplication (DRY Violations)

Duplication is the single most important smell. Every instance represents a missed opportunity for abstraction.

| Duplication type | How to find it | Refactoring |
|-----------------|----------------|-------------|
| **Exact clones** | Copy-paste detection tools | Extract shared function |
| **Structural clones** | Same algorithm, different data | Template Method or Strategy pattern |
| **Conditional chains** | Repeated `if/else` or `switch` | Polymorphism |
| **Cross-module** | Same logic in multiple modules | Extract shared library or module |

**The Rule of Three:** First instance: just write it. Second instance: note the duplication. Third instance: refactor.

### G6: Code at Wrong Level of Abstraction

Functions and classes should operate at a single level of abstraction. Mixing high-level business logic with low-level implementation details creates confusion.

```python
# BAD: Mixed abstraction levels
def process_order(order):
    # High-level business logic
    validate_order(order)

    # Suddenly low-level database details
    connection = psycopg2.connect(host="db.example.com", port=5432)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO orders ...")
    connection.commit()

    # Back to high-level
    send_confirmation(order)

# GOOD: Consistent abstraction level
def process_order(order):
    validate_order(order)
    order_repository.save(order)
    send_confirmation(order)
```

### G7: Feature Envy

A method that uses more features of another class than its own class has "feature envy." It wants to be somewhere else.

```python
# BAD: This method envies the Order class
class ReportGenerator:
    def calculate_order_summary(self, order):
        subtotal = sum(item.price * item.quantity for item in order.items)
        tax = subtotal * order.tax_rate
        shipping = order.weight * order.shipping_rate
        return subtotal + tax + shipping

# GOOD: Move the method to where the data lives
class Order:
    def calculate_total(self):
        subtotal = sum(item.price * item.quantity for item in self.items)
        tax = subtotal * self.tax_rate
        shipping = self.weight * self.shipping_rate
        return subtotal + tax + shipping
```

### G8: Selector Arguments

Arguments used to select behavior (not just booleans, but enums and strings too).

```python
# BAD: Selector argument
def calculate(operation, a, b):
    if operation == "add": return a + b
    if operation == "subtract": return a - b
    if operation == "multiply": return a * b

# GOOD: Separate functions
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
```

### G9: Obscured Intent

Code that is designed to be compact at the expense of clarity.

```python
# BAD: What does this do?
def m(a):return sum(1 for c in a if c.s=='A'and c.d<dt.now()-td(30))

# GOOD: Clear intent
def count_recently_active_customers(customers):
    thirty_days_ago = datetime.now() - timedelta(days=30)
    return sum(
        1 for customer in customers
        if customer.status == 'ACTIVE'
        and customer.last_active_date < thirty_days_ago
    )
```

### G10: Magic Numbers

Raw numeric literals scattered through the code.

```python
# BAD: What do these numbers mean?
if len(password) < 8:
    raise ValueError("Too short")
time.sleep(86400)
price = amount * 0.08

# GOOD: Named constants explain intent
MIN_PASSWORD_LENGTH = 8
SECONDS_PER_DAY = 86400
SALES_TAX_RATE = 0.08

if len(password) < MIN_PASSWORD_LENGTH:
    raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
time.sleep(SECONDS_PER_DAY)
price = amount * SALES_TAX_RATE
```

### G11: Dead Code

Code that is never executed: unreachable conditions, unused variables, functions with no callers, impossible `catch` blocks.

**Types of dead code:**
- Conditions that can never be true
- `catch` blocks for exceptions that are never thrown
- Variables that are assigned but never read
- Functions that are never called
- Entire modules with no imports

**Fix:** Delete it. Every line of dead code is a line someone has to read, wonder about, and maintain. Version control is the safety net.

---

## Naming Smells

### N1: Choosing Descriptive Names

Names should be descriptive. Don't settle for the first name that comes to mind. Take time to choose a name that is as descriptive and unambiguous as possible.

### N2: Choosing Names at the Appropriate Level of Abstraction

Don't choose names that communicate implementation. Choose names that reflect the level of abstraction of the class or function you are working in.

```python
# BAD: Implementation-level name
class FTPFileDownloader:  # What if we switch to HTTP?

# GOOD: Abstraction-level name
class FileDownloader:  # The how is an implementation detail
```

### N3: Using Standard Nomenclature Where Possible

Use names from well-known patterns and conventions:
- `Factory`, `Strategy`, `Visitor`, `Iterator` for design patterns
- `Repository`, `Service`, `Controller` for architectural layers
- Domain terms from the business (Ubiquitous Language from DDD)

### N4: Unambiguous Names

Choose names that make the function or variable's workings unambiguous.

```python
# BAD: Ambiguous
def rename(old, new):  # Rename what? A file? A user? A variable?

# GOOD: Unambiguous
def rename_file(old_path, new_path)
```

### N5: Use Long Names for Long Scopes

The length of a name should be proportional to the size of the scope that contains it.

| Scope | Name length | Example |
|-------|-------------|---------|
| 1-line lambda | 1 char | `x` in `items.map(x => x.id)` |
| 5-line method | Short | `i`, `sum`, `item` |
| Class field | Medium | `retryCount`, `lastUpdate` |
| Module constant | Long | `MAX_CONNECTION_POOL_SIZE` |
| Global/public API | Very long | `DEFAULT_SESSION_TIMEOUT_MINUTES` |

### N6: Avoid Encodings

Don't use Hungarian notation, member prefixes, or interface prefixes.

| Encoding | Example | Better |
|----------|---------|--------|
| Hungarian | `strName`, `iCount` | `name`, `count` |
| Member prefix | `m_name`, `_name` | `name` (context is the class) |
| Interface prefix | `IUserService` | `UserService` (implementations get suffix: `UserServiceImpl`) |
| Type suffix | `nameString` | `name` |

---

## Test Smells

### T1: Insufficient Tests

A test suite should test everything that could possibly break. Test every condition, every boundary, every edge case.

### T2: Using a Coverage Tool

Code coverage tools report which lines are not tested. Use them as a guide, not a goal. 100% line coverage does not mean 100% correctness, but untested lines definitely contain potential bugs.

### T3: Don't Skip Trivial Tests

Trivial tests are easy to write and their documentary value is higher than the cost of writing them.

### T4: An Ignored Test Is a Question About an Ambiguity

If requirements are unclear, write the test with `@skip` and a note about what's uncertain. A skipped test is a question waiting to be answered.

### T5: Test Boundary Conditions

Boundaries are where bugs cluster. Test all edges: empty input, one element, max capacity, off-by-one, overflow.

### T6: Exhaustively Test Near Bugs

When you find a bug in a function, don't just fix it. Test the function exhaustively. Bugs tend to congregate -- if there's one, there are likely others nearby.

### T7: Patterns of Failure Are Revealing

If tests fail in a pattern (all tests with dates fail, all tests with unicode fail), the pattern reveals the nature of the bug. Use this diagnostic information.

### T8: Test Coverage Patterns Can Be Revealing

Look at which code is not covered. If a complex conditional has untested branches, those branches likely contain bugs.

### T9: Tests Should Be Fast

Slow tests don't get run. A test suite that takes 30 minutes will be run once a day at best. A suite that takes 10 seconds will be run after every change.

---

## Smell Detection Quick Reference

| Category | Key Smells | First Action |
|----------|-----------|--------------|
| **Comments** | Obsolete, redundant, commented-out code | Delete the comment; improve the code |
| **Environment** | Multi-step build or test | Script to single command |
| **Functions** | Too many args, flag args, dead functions | Extract object, split function, delete |
| **General** | Duplication, wrong abstraction level, feature envy | Extract, move, consolidate |
| **Names** | Ambiguous, wrong level, encoded | Rename to reveal intent |
| **Tests** | Insufficient, slow, skipped, no boundaries | Add tests, mock dependencies, fix or delete |

**Remember:** Not every smell requires immediate action. Use professional judgment. A smell in frequently-changed code demands attention. A smell in stable code that never changes may not be worth the risk of refactoring.
