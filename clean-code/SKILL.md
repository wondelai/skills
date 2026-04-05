---
name: clean-code
description: 'Write readable, maintainable code through disciplined naming, small functions, and clean error handling. Use when the user mentions "code review", "naming conventions", "function too long", "code smells", "readable code", "boy scout rule", "single responsibility", or "unit test quality". Also trigger when reviewing pull requests for readability, refactoring messy functions, debating comment styles, or improving error handling patterns. Covers SRP, comment discipline, formatting, and unit testing. For refactoring techniques, see refactoring-patterns. For architecture, see clean-architecture.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Clean Code Framework

A disciplined approach to writing code that communicates intent, minimizes surprises, and welcomes change. Apply these principles when writing new code, reviewing pull requests, refactoring legacy systems, or advising on code quality improvements.

## Core Principle

**Code is read far more often than it is written. Optimize for the reader.** Every naming choice, function boundary, and formatting decision either adds clarity or adds cost. The ratio of time spent reading code to writing code is well over 10:1. Making code easier to read makes it easier to write, easier to debug, and easier to extend.

**The foundation:** Clean code is not about following rules mechanically -- it is about caring for the craft. A clean codebase reads like well-written prose: names reveal intent, functions tell a story one step at a time, and there are no surprises lurking in dark corners. The Boy Scout Rule applies: always leave the code cleaner than you found it.

## Scoring

**Goal: 10/10.** When reviewing or writing code, rate it 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

- **9-10:** Names reveal intent, functions are small and focused, error handling is consistent, tests are clean and comprehensive.
- **7-8:** Mostly clean with minor naming ambiguities or a few long functions. Tests exist but may lack edge cases.
- **5-6:** Mixed quality -- some good patterns alongside unclear names, duplicated logic, or inconsistent error handling.
- **3-4:** Significant readability issues -- long functions doing multiple things, misleading names, poor or missing tests.
- **1-2:** Code works but is nearly unreadable -- magic numbers, cryptic abbreviations, no structure, no tests.

## The Clean Code Framework

Six disciplines for writing code that communicates clearly and adapts to change:

### 1. Meaningful Names

**Core concept:** Names should reveal intent, avoid disinformation, and make the code read like prose. If a name requires a comment to explain it, the name is wrong.

**Why it works:** Names are the most pervasive form of documentation. A well-chosen name eliminates the need to read the implementation. A poorly chosen name forces every reader to reverse-engineer the author's intent.

**Key insights:**
- Names should answer why it exists, what it does, and how it is used
- Avoid single-letter variables except for loop counters in tiny scopes
- Avoid encodings, prefixes, and type information in names (no Hungarian notation)
- Class names should be nouns or noun phrases; method names should be verbs or verb phrases
- Use one word per concept consistently: don't mix `fetch`, `retrieve`, and `get`
- Longer scopes demand longer, more descriptive names
- Don't be afraid to rename -- IDEs make it trivial

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Variables** | Intention-revealing name | `elapsedTimeInDays` not `d` or `elapsed` |
| **Booleans** | Predicate phrasing | `isActive`, `hasPermission`, `canEdit` |
| **Functions** | Verb + noun describing action | `calculateMonthlyRevenue()` not `calc()` |
| **Classes** | Noun describing responsibility | `InvoiceGenerator` not `InvoiceManager` |
| **Constants** | Searchable, all-caps with context | `MAX_RETRY_ATTEMPTS = 3` not `3` inline |
| **Collections** | Plural nouns or descriptive phrases | `activeUsers` not `list` or `data` |

See: [references/naming-conventions.md](references/naming-conventions.md)

### 2. Functions

**Core concept:** Functions should be small, do one thing, and do it well. The ideal function is 4-6 lines long, takes zero to two arguments, and operates at a single level of abstraction.

**Why it works:** Small functions are easy to name, easy to understand, easy to test, and easy to reuse. When a function does one thing, its name can describe exactly what it does, eliminating the need to read the body. Long functions hide bugs, resist testing, and accumulate responsibilities over time.

**Key insights:**
- Functions should do one thing, do it well, and do it only
- The Step-Down Rule: code should read like a top-down narrative, each function calling the next level of abstraction
- Ideal argument count is zero (niladic), then one (monadic), then two (dyadic); three or more (polyadic) requires justification
- Flag arguments (booleans) are a code smell -- they mean the function does two things
- Command-Query Separation: a function should either change state or return a value, never both
- Extract till you drop: if you can extract a named function from a block, do it
- Functions should have no side effects -- no hidden changes to state

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Long function** | Extract into named steps | `validateInput(); transformData(); saveRecord();` |
| **Flag argument** | Split into two functions | `renderForPrint()` and `renderForScreen()` not `render(isPrint)` |
| **Deep nesting** | Extract inner blocks | Move nested `if`/`for` bodies into named functions |
| **Multiple returns** | Guard clauses at top | Early return for error cases, single happy path |
| **Many arguments** | Introduce parameter object | `new DateRange(start, end)` not `report(start, end, format, locale)` |
| **Side effects** | Make effects explicit | Rename `checkPassword()` to `checkPasswordAndInitSession()` or separate |

See: [references/functions-and-methods.md](references/functions-and-methods.md)

### 3. Comments and Formatting

**Core concept:** A comment is a failure to express yourself in code. Good code is self-documenting. When comments are necessary, they should explain *why*, never *what*. Formatting creates the visual structure that makes code scannable.

**Why it works:** Comments rot. Code changes but comments often do not, creating misleading documentation that is worse than no documentation. Clean formatting -- consistent indentation, vertical spacing between concepts, and logical ordering -- lets developers scan code the way readers scan a newspaper: headlines first, details on demand.

**Key insights:**
- The best comment is the code itself -- extract a well-named function instead of writing a comment
- Legal comments (copyright headers) and TODO comments are acceptable
- Javadoc for public APIs is valuable; Javadoc for internal code is noise
- Commented-out code should be deleted -- version control remembers it
- Journal comments (changelog in the file) are obsolete -- use git log
- Vertical openness: separate concepts with blank lines
- Vertical density: related code should appear close together
- Variables should be declared close to their usage
- Instance variables should be declared at the top of the class

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Explaining "what"** | Replace with better name | Rename `// check if eligible` to `isEligible()` |
| **Explaining "why"** | Keep as comment | `// RFC 7231 requires this header for proxies` |
| **Commented-out code** | Delete it | Trust version control to remember |
| **File organization** | Newspaper metaphor | High-level functions at top, details below |
| **Related code** | Group vertically | Keep caller near callee in the same file |
| **Team formatting** | Agree on rules once | Use automated formatters (Prettier, Black, gofmt) |

See: [references/comments-formatting.md](references/comments-formatting.md)

### 4. Error Handling

**Core concept:** Error handling is a separate concern from business logic. Use exceptions rather than return codes, provide context with every exception, and never return or pass null.

**Why it works:** Return codes force the caller to check immediately, cluttering the happy path with error-checking logic. Exceptions let you separate the happy path from error handling, making both easier to read. Returning null forces every caller to add null checks, and a single missing check produces a NullPointerException far from the source.

**Key insights:**
- Write your try-catch block first -- it defines a transaction boundary
- Use unchecked exceptions -- checked exceptions violate the Open/Closed Principle
- Create informative exception messages: include the operation that failed and the context
- Define exception classes in terms of the caller's needs, not the type of failure
- The Special Case Pattern: return a special-case object instead of null (e.g., empty list, guest user)
- Don't return null -- return empty collections, Optional, or throw
- Don't pass null -- no reasonable behavior exists for null arguments
- Wrap third-party APIs to translate their exceptions into your domain

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Null returns** | Return empty collection or Optional | `return Collections.emptyList()` not `return null` |
| **Error codes** | Replace with exceptions | `throw new InsufficientFundsException(balance, amount)` |
| **Third-party APIs** | Wrap with adapter | `PortfolioService` wraps vendor API, translates exceptions |
| **Null arguments** | Fail fast with assertion | `Objects.requireNonNull(user, "user must not be null")` |
| **Special cases** | Null Object pattern | `GuestUser` with default behavior instead of null checks |
| **Context in errors** | Include operation + state | `"Failed to save invoice #1234 for customer 'Acme'"` |

See: [references/error-handling.md](references/error-handling.md)

### 5. Unit Testing

**Core concept:** Tests are first-class code. They must be clean, readable, and maintained with the same discipline as production code. Dirty tests are worse than no tests -- they become a liability that slows every change.

**Why it works:** Clean tests serve as executable documentation, showing exactly how the system is intended to behave. They provide a safety net for refactoring and a regression check for every change. Without tests, every modification is a potential bug. With dirty tests, every modification requires fighting through incomprehensible test code.

**Key insights:**
- The Three Laws of TDD: (1) write a failing test first, (2) write only enough test to fail, (3) write only enough code to pass
- One concept per test -- not necessarily one assert, but one logical assertion
- Tests should be readable: use the Build-Operate-Check pattern (Arrange-Act-Assert)
- F.I.R.S.T. principles: Fast, Independent, Repeatable, Self-validating, Timely
- Test names should describe the scenario and expected behavior
- Test code deserves the same refactoring attention as production code
- Domain-specific testing language: build helper functions that read like a DSL

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Test structure** | Arrange-Act-Assert | Setup, execute, verify -- clearly separated |
| **Test naming** | Scenario + expected behavior | `shouldRejectExpiredToken` not `test1` |
| **Shared setup** | Extract builder/factory | `aUser().withRole(ADMIN).build()` |
| **Multiple scenarios** | Parameterized tests | One test method, multiple input/output pairs |
| **Flaky tests** | Remove external dependencies | Mock time, network, file system |
| **Test readability** | Domain-specific helpers | `assertThatInvoice(inv).isPaidInFull()` |

See: [references/testing-principles.md](references/testing-principles.md)

### 6. Code Smells and Heuristics

**Core concept:** Code smells are surface indicators of deeper design problems. Learn to recognize them quickly and apply targeted refactorings. Not every smell requires immediate action, but ignoring them accumulates technical debt.

**Why it works:** Smells are heuristics -- they point toward likely problems without requiring deep analysis. A developer who can quickly identify "this function has too many arguments" or "this class has feature envy" can make targeted improvements instead of vague "cleanup" efforts.

**Key insights:**
- Comments: inappropriate information, obsolete comments, redundant comments that repeat the code
- Functions: too many arguments, output arguments, flag arguments, dead functions never called
- General: obvious duplication, code at wrong level of abstraction, feature envy (method uses another class more than its own), magic numbers
- Names: names at wrong abstraction level, names that don't describe side effects, ambiguous short names
- Tests: insufficient tests, skipped tests, untested boundary conditions, no failure-path tests
- Apply the Boy Scout Rule: leave code cleaner than you found it
- Refactor in small, tested steps -- never refactor and add features simultaneously

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Duplication** | Extract shared logic | Common validation → `validateEmail()` helper |
| **Long parameter list** | Introduce parameter object | `SearchCriteria` groups related params |
| **Feature envy** | Move method to data's class | `order.calculateTotal()` not `calculator.total(order)` |
| **Dead code** | Delete it | Remove unused functions, unreachable branches |
| **Magic numbers** | Named constants | `MAX_LOGIN_ATTEMPTS = 5` not bare `5` |
| **Shotgun surgery** | Consolidate related changes | Group scattered logic into a single module |

See: [references/code-smells.md](references/code-smells.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **Abbreviating names** | Saves seconds writing, costs hours reading | Use full, descriptive names; IDEs autocomplete |
| **"Clever" one-liners** | Impressive to write, impossible to debug | Expand into readable steps with clear names |
| **Comments instead of refactoring** | Comments rot; code is the truth | Extract well-named function instead of commenting |
| **Catching generic exceptions** | Swallows bugs along with expected errors | Catch specific exceptions, let unexpected ones propagate |
| **No tests for error paths** | Happy path works, edge cases crash | Test every branch, boundary, and failure mode |
| **Premature optimization** | Obscures intent for marginal performance | Write clean code first, optimize measured bottlenecks |
| **God classes** | One class, 2000 lines, does everything | Apply SRP -- split by responsibility |
| **Refactoring without tests** | No safety net to catch regressions | Write characterization tests before refactoring |
| **Inconsistent conventions** | Every file feels like a different codebase | Agree on style, enforce with linters and formatters |
| **Returning null everywhere** | Null checks spread like a virus | Use Optional, empty collections, or Null Object pattern |

## Quick Diagnostic

Audit any codebase:

| Question | If No | Action |
|----------|-------|--------|
| Can you understand each function without reading its body? | Names don't reveal intent | Rename functions to describe what they do |
| Are all functions under 20 lines? | Functions do too many things | Extract sub-operations into named helpers |
| Are there zero commented-out code blocks? | Dead code creating confusion | Delete them -- version control has history |
| Is error handling separate from business logic? | Try-catch blocks cluttering main flow | Extract error handling; use exceptions not return codes |
| Does every class have a single responsibility? | Classes accumulate unrelated duties | Split into focused classes with clear names |
| Is there a test for every public method? | No safety net for changes | Add tests before making further changes |
| Are test names descriptive of behavior? | Tests are hard to understand when they fail | Rename to `shouldDoXWhenY` pattern |
| Is duplication below 3 occurrences? | Copy-paste spreading bugs | Extract into shared function or module |
| Are magic numbers replaced with named constants? | Intent is hidden behind raw values | Extract constants with descriptive names |
| Can you run all tests in under 10 seconds? | Slow tests discourage running them | Mock external deps, split integration tests |

## Reference Files

- [naming-conventions.md](references/naming-conventions.md): Intention-revealing names, avoiding disinformation, class vs. method naming, before/after examples
- [functions-and-methods.md](references/functions-and-methods.md): Small functions, argument counts, command-query separation, the step-down rule, side effects
- [comments-formatting.md](references/comments-formatting.md): Good vs. bad comments, the newspaper metaphor, vertical formatting, team rules
- [error-handling.md](references/error-handling.md): Exceptions over return codes, null handling, Special Case pattern, wrapping third-party APIs
- [testing-principles.md](references/testing-principles.md): TDD laws, F.I.R.S.T. principles, clean test patterns, test readability
- [code-smells.md](references/code-smells.md): Comprehensive smell catalog organized by category, with targeted refactorings

## Further Reading

This skill is based on Robert C. Martin's seminal guide to software craftsmanship:

- [*"Clean Code: A Handbook of Agile Software Craftsmanship"*](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882?tag=wondelai00-20) by Robert C. Martin
- [*"The Clean Coder: A Code of Conduct for Professional Programmers"*](https://www.amazon.com/Clean-Coder-Conduct-Professional-Programmers/dp/0137081073?tag=wondelai00-20) by Robert C. Martin
- [*"Clean Architecture: A Craftsman's Guide to Software Structure and Design"*](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164?tag=wondelai00-20) by Robert C. Martin
- [*"Refactoring: Improving the Design of Existing Code"*](https://www.amazon.com/Refactoring-Improving-Existing-Addison-Wesley-Signature/dp/0134757599?tag=wondelai00-20) by Martin Fowler

## About the Author

**Robert C. Martin** ("Uncle Bob") is a software engineer, instructor, and author who has been programming since 1970. He is a co-author of the Agile Manifesto and the founder of Uncle Bob Consulting LLC and Clean Coders. His books -- *Clean Code* (2008), *The Clean Coder* (2011), *Clean Architecture* (2017), and *Clean Agile* (2019) -- have shaped how an entire generation of developers think about code quality, professional responsibility, and software design. Martin is known for his uncompromising stance that developers are professionals who must take responsibility for the quality of their work, and that the only way to go fast is to go well.
