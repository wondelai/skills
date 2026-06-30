---
name: clean-code
description: 'Write readable, maintainable code through disciplined naming, small functions, and clean error handling. Use when the user mentions "clean up this code", "this function is too long", "code smells", "naming conventions", "boy scout rule", "single responsibility", or "unit test quality". Also trigger when reviewing a pull request for readability, untangling a messy function, debating comment styles, or improving error-handling patterns. Covers SRP, comment discipline, formatting, and unit testing. For refactoring techniques, see refactoring-patterns. For architecture and dependency rules, see clean-architecture.'
license: MIT
metadata:
  author: wondelai
  version: "1.4.0"
---

# Clean Code Framework

A disciplined approach to writing code that communicates intent, minimizes surprises, and welcomes change. Apply these principles when writing new code, reviewing pull requests, refactoring legacy systems, or advising on code quality.

## Core Principle

**Code is read far more often than it is written — optimize for the reader.** The read-to-write ratio is well over 10:1, so every naming choice, function boundary, and formatting decision either adds clarity or adds cost. Clean code reads like well-written prose: names reveal intent, functions tell a story one step at a time, and the Boy Scout Rule applies — always leave the code cleaner than you found it.

## Scoring

**Goal: 10/10.** Rate any code 0-10 against the principles below. Report the current score and the specific improvements needed to reach 10/10.

- **9-10:** Names reveal intent, functions are small and focused, error handling is consistent, tests are clean and comprehensive
- **7-8:** Mostly clean with minor naming ambiguities or a few long functions; tests may lack edge cases
- **5-6:** Mixed — good patterns alongside unclear names, duplicated logic, or inconsistent error handling
- **3-4:** Long multi-purpose functions, misleading names, poor or missing tests
- **1-2:** Nearly unreadable — magic numbers, cryptic abbreviations, no structure, no tests

## The Clean Code Framework

Six disciplines for writing code that communicates clearly and adapts to change:

### 1. Meaningful Names

**Core concept:** Names should reveal intent, avoid disinformation, and make the code read like prose. If a name requires a comment to explain it, the name is wrong.

**Why it works:** Names are the most pervasive form of documentation — a well-chosen name eliminates the need to read the implementation; a poor one forces every reader to reverse-engineer intent.

**Key insights:**
- A name should answer why it exists, what it does, and how it is used
- No encodings, prefixes, or type information (no Hungarian notation); single letters only for tiny-scope loop counters
- Classes are nouns; methods are verbs
- One word per concept: don't mix `fetch`, `retrieve`, and `get`
- Longer scope demands a longer, more descriptive name
- Rename freely — IDEs make it trivial

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Variables** | Intention-revealing | `elapsedTimeInDays` not `d` |
| **Booleans** | Predicate phrasing | `isActive`, `hasPermission`, `canEdit` |
| **Functions** | Verb + noun | `calculateMonthlyRevenue()` not `calc()` |
| **Classes** | Noun naming the responsibility | `InvoiceGenerator` not `InvoiceManager` |

See [references/naming-conventions.md](references/naming-conventions.md) when renaming or reviewing names — per-language conventions, pronounceable/searchable tables, and before/after examples.

### 2. Functions

**Core concept:** Functions should be small, do one thing, and do it well — ideally 4-6 lines, zero to two arguments, one level of abstraction.

**Why it works:** Small single-purpose functions are easy to name, understand, test, and reuse; long functions hide bugs, resist testing, and accumulate responsibilities.

**Key insights:**
- Step-Down Rule: code reads top-down, each function calling the next level of abstraction
- Argument count: zero best, one fine, two acceptable, three+ requires justification
- Flag arguments are a smell — the function does two things; split it
- Command-Query Separation: change state or return a value, never both
- Extract till you drop: if you can pull out a named function, do it
- No hidden side effects — the name must tell the whole truth

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Long function** | Extract named steps | `validateInput(); transformData(); saveRecord();` |
| **Flag argument** | Split into two functions | `renderForPrint()` / `renderForScreen()` not `render(isPrint)` |
| **Error cases** | Guard clauses at top | Early return for errors, single happy path |
| **Many arguments** | Introduce parameter object | `new DateRange(start, end)` not `report(start, end, format, locale)` |
| **Side effects** | Make effects explicit | `checkPassword()` that starts a session → rename or separate |

See [references/functions-and-methods.md](references/functions-and-methods.md) when splitting a long function — argument-count rules, command-query separation, and step-down worked examples.

### 3. Comments and Formatting

**Core concept:** A comment is a failure to express yourself in code. When comments are necessary, they explain *why*, never *what*. Formatting creates the visual structure that makes code scannable.

**Why it works:** Comments rot — code changes but comments often don't, creating documentation worse than none. Clean formatting lets developers scan code like a newspaper: headlines first, details on demand.

**Key insights:**
- The best comment is a well-named extracted function
- Acceptable: legal headers, TODOs, public API docs, genuine "why" explanations
- Commented-out code and journal comments: delete — version control remembers
- Vertical openness between concepts; vertical density within them; declare variables near usage
- Newspaper metaphor: high-level functions at the top of the file, details below

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Explaining "what"** | Replace with better name | `// check if eligible` → `isEligible()` |
| **Explaining "why"** | Keep as comment | `// RFC 7231 requires this header for proxies` |
| **Commented-out code** | Delete it | Trust version control |
| **Team formatting** | Decide once, automate | Prettier, Black, gofmt |

See [references/comments-formatting.md](references/comments-formatting.md) when deciding whether a comment earns its place — good-vs-bad comment catalog and vertical-formatting rules.

### 4. Error Handling

**Core concept:** Error handling is a separate concern from business logic. Use exceptions rather than return codes, provide context with every exception, and never return or pass null.

**Why it works:** Return codes clutter the happy path with checks; exceptions separate the two cleanly. Returning null forces null checks on every caller, and one missing check crashes far from the source.

**Key insights:**
- Write the try-catch first — it defines a transaction boundary
- Prefer unchecked exceptions — checked ones violate the Open/Closed Principle
- Define exception classes by the caller's needs, not the failure type
- Don't return null (use empty collections, Optional, or throw); don't pass null either
- Special Case / Null Object pattern: return an object with default behavior instead of null

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Null returns** | Empty collection or Optional | `return Collections.emptyList()` not `return null` |
| **Error codes** | Replace with exceptions | `throw new InsufficientFundsException(balance, amount)` |
| **Third-party APIs** | Wrap with adapter | `PortfolioService` wraps the vendor API, translates its exceptions |
| **Special cases** | Null Object pattern | `GuestUser` with default behavior instead of null checks |
| **Context in errors** | Include operation + state | `"Failed to save invoice #1234 for customer 'Acme'"` |

See [references/error-handling.md](references/error-handling.md) when designing exception or null strategy — Special Case pattern and third-party-API wrapping examples.

### 5. Unit Testing

**Core concept:** Tests are first-class code, kept clean with the same discipline as production code. Dirty tests are worse than no tests — they become a liability that slows every change.

**Why it works:** Clean tests are executable documentation and a safety net for refactoring; dirty tests make every modification a fight through incomprehensible test code.

**Key insights:**
- Three Laws of TDD: write a failing test first; only enough test to fail; only enough code to pass
- One concept per test — one logical assertion, not necessarily one assert
- F.I.R.S.T.: Fast, Independent, Repeatable, Self-validating, Timely
- Build a domain-specific testing language: helpers that read like a DSL
- Refactor test code as readily as production code

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Test structure** | Arrange-Act-Assert | Setup, execute, verify — clearly separated |
| **Test naming** | Scenario + expected behavior | `shouldRejectExpiredToken` not `test1` |
| **Shared setup** | Builder/factory helpers | `aUser().withRole(ADMIN).build()` |
| **Flaky tests** | Remove external dependencies | Mock time, network, file system |

See [references/testing-principles.md](references/testing-principles.md) when writing or cleaning tests — TDD laws, F.I.R.S.T. expanded, and clean-test patterns.

### 6. Code Smells and Heuristics

**Core concept:** Smells are surface indicators of deeper design problems — learn to recognize them quickly and apply targeted refactorings instead of vague "cleanup".

**Why it works:** Smells are heuristics that point toward likely problems without deep analysis, turning code review instinct into specific, repeatable moves.

**Key insights:**
- Function smells: too many arguments, output arguments, flag arguments, dead functions
- General smells: duplication, wrong level of abstraction, feature envy, magic numbers
- Test smells: insufficient coverage, skipped tests, untested boundary conditions and failure paths
- Refactor in small, tested steps — never refactor and add features simultaneously
- Boy Scout Rule: leave the code cleaner than you found it

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Duplication** | Extract shared logic | Common validation → `validateEmail()` helper |
| **Feature envy** | Move method to the data's class | `order.calculateTotal()` not `calculator.total(order)` |
| **Dead code** | Delete it | Remove unused functions, unreachable branches |
| **Magic numbers** | Named constants | `MAX_LOGIN_ATTEMPTS = 5` not bare `5` |
| **Shotgun surgery** | Consolidate related changes | Group scattered logic into a single module |

See [references/code-smells.md](references/code-smells.md) when a smell is hard to name — the full catalog by category, each paired with its targeted refactoring.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **Abbreviating names** | Saves seconds writing, costs hours reading | Full descriptive names; IDEs autocomplete |
| **"Clever" one-liners** | Impressive to write, impossible to debug | Expand into readable named steps |
| **Comments instead of refactoring** | Comments rot; code is the truth | Extract a well-named function instead |
| **Catching generic exceptions** | Swallows bugs along with expected errors | Catch specific exceptions; let the rest propagate |
| **No tests for error paths** | Happy path works, edge cases crash | Test every branch, boundary, and failure mode |
| **Premature optimization** | Obscures intent for marginal gains | Clean first; optimize measured bottlenecks |
| **God classes** | One 2000-line class does everything | Apply SRP — split by responsibility |
| **Refactoring without tests** | No safety net for regressions | Write characterization tests first |
| **Inconsistent conventions** | Every file feels like a different codebase | Agree on style; enforce with linters and formatters |
| **Returning null everywhere** | Null checks spread like a virus | Optional, empty collections, or Null Object |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you understand each function without reading its body? | Names don't reveal intent | Rename to describe what it does |
| Are all functions under 20 lines? | Functions do too many things | Extract sub-operations into named helpers |
| Zero commented-out code blocks? | Dead code creating confusion | Delete — version control has history |
| Is error handling separate from business logic? | Try-catch clutters the main flow | Extract handlers; exceptions over return codes |
| Does every class have a single responsibility? | Classes accumulate unrelated duties | Split into focused, well-named classes |
| Is there a test for every public method? | No safety net for changes | Add tests before changing further |
| Are test names descriptive of behavior? | Failures are hard to interpret | Rename to `shouldDoXWhenY` |
| Is duplication below 3 occurrences? | Copy-paste spreading bugs | Extract shared logic (§6) |
| Are magic numbers named constants? | Intent hidden behind raw values | Name the constant (§6) |
| Do all tests run in under 10 seconds? | Slow tests don't get run | Mock external deps; split integration tests |

## Further Reading

Based on Robert C. Martin's seminal guide to software craftsmanship:

- [*"Clean Code: A Handbook of Agile Software Craftsmanship"*](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882?tag=wondelai00-20) by Robert C. Martin
- [*"The Clean Coder: A Code of Conduct for Professional Programmers"*](https://www.amazon.com/Clean-Coder-Conduct-Professional-Programmers/dp/0137081073?tag=wondelai00-20) by Robert C. Martin
- [*"Clean Architecture: A Craftsman's Guide to Software Structure and Design"*](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164?tag=wondelai00-20) by Robert C. Martin
- [*"Refactoring: Improving the Design of Existing Code"*](https://www.amazon.com/Refactoring-Improving-Existing-Addison-Wesley-Signature/dp/0134757599?tag=wondelai00-20) by Martin Fowler

## About the Author

**Robert C. Martin ("Uncle Bob")** has been programming since 1970, co-authored the Agile Manifesto, and founded Uncle Bob Consulting and Clean Coders. His books — *Clean Code*, *The Clean Coder*, *Clean Architecture*, and *Clean Agile* — shaped how a generation of developers think about code quality, and his core stance is that the only way to go fast is to go well.
