---
name: refactoring-patterns
description: 'Apply named refactoring transformations to improve code structure without changing behavior. Use when the user mentions "refactor this", "code smells", "extract method", "replace conditional", "technical debt", "move method", "inline variable", "decompose conditional", or "clean up this messy code". Also trigger when cleaning up legacy code, preparing code for new features by restructuring, or identifying which transformation fits a specific code smell. Covers smell-driven refactoring, safe transformation sequences, and testing guards. For code-quality foundations, see clean-code. For managing complexity, see software-design-philosophy.'
license: MIT
metadata:
  author: wondelai
  version: "1.4.1"
---

# Refactoring Patterns Framework

A disciplined approach to improving the internal structure of existing code without changing its observable behavior. Every refactoring follows the same loop: verify tests pass, apply one small structural change, verify tests still pass.

## Core Principle

**Refactoring is not rewriting. It is a sequence of small, behavior-preserving transformations, each backed by tests.** You never change what the code does — only how it is organized. Big-bang rewrites fail because they combine structural change with behavioral change, making it impossible to know which broke things.

**The foundation:** Bad code is a natural consequence of delivering under time pressure, not a character flaw. Code smells are objective signals of degraded structure; the smell catalog tells you *where* to look, and the refactoring catalog tells you *what to do*.

## Scoring

**Goal: 10/10.** Score structural quality by how many of the eight [Quick Diagnostic](#quick-diagnostic) rows pass — `score = round(passed / 8 × 10)`, adjusting down when a single smell is severe. Bands:
- **9-10**: no obvious smells remain, each function does one thing, names reveal intent, duplication is eliminated, conditionals use polymorphism where apt, and tests cover the refactored paths.
- **5-6**: a few smells remain (a Long Method, some duplication) but structure is mostly sound.
- **≤3**: pervasive smells — tangled conditionals, God classes, duplication everywhere — or no tests to refactor safely.

Always state the current score, name the smells driving it down, and list the specific refactorings needed to reach 10/10.

## The Refactoring Patterns Framework

Six areas of focus for systematically improving code structure:

### 1. Code Smells as Triggers

**Core concept:** Code smells are surface indicators of deeper structural problems — not bugs, but signals that the design makes code harder to understand, extend, or maintain. Each smell maps to named refactorings that fix it.

**Why it works:** Named smells give teams objective criteria instead of subjective "I don't like this" — "This is Feature Envy" points directly at the fix.

**Key insights:**
- Smells cluster into five families: Bloaters, Object-Orientation Abusers, Change Preventers, Dispensables, Couplers
- Long Method is the most common smell; Duplicate Code is the most expensive
- A method that needs a comment to explain *what* it does is a smell — extract and name the block instead
- Shotgun Surgery (one change, many classes) and Divergent Change (one class, many reasons to change) are opposite signals of misplaced responsibilities
- Primitive Obsession — raw strings/ints instead of small domain objects — spreads errors and duplication

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Method > 10 lines | Extract Method | Pull loop body into `calculateLineTotal()` |
| One change touches many classes (Shotgun Surgery) | Move Method/Field | Gather the scattered behavior into one class |
| Same params in many methods | Introduce Parameter Object | `startDate, endDate` → `DateRange` |
| Copy-pasted logic | Extract Method + Pull Up Method | Share via common method or base class |

See [references/smell-catalog.md](references/smell-catalog.md) when you need to name a smell and its fix — all five families (Bloaters, OO Abusers, Change Preventers, Dispensables, Couplers) with detection heuristics and the refactoring each maps to.

### 2. Composing Methods

**Core concept:** Most refactoring starts here: break long methods into smaller, well-named pieces that read like prose — high-level steps delegating to clearly named helpers.

**Why it works:** Short methods with intention-revealing names eliminate comments, make bugs obvious at a glance, and enable reuse; a method call costs nothing to read when the name says everything.

**Key insights:**
- Extract Method is the single most important refactoring — master it first
- Urge to write a comment? Extract the block and use the comment as the method name
- Inline Method when the body is as clear as the name — indirection without value is noise
- Replace Temp with Query for computed values used in multiple places; Split Temporary Variable when one temp serves two purposes
- Replace Method with Method Object when locals are too tangled to extract — they become fields

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Block with a comment | Extract Method | `// check eligibility` → `isEligible()` |
| Temp used once | Inline Variable | Drop `const price = order.getPrice()` |
| Trivial delegating method | Inline Method | Inline `return deliveries > 5` if used once |
| Method with many tangled locals | Replace Method with Method Object | Locals become fields in a new class |

See [references/composing-methods.md](references/composing-methods.md) when applying any method-level transformation — step-by-step mechanics and before/after code for Extract/Inline Method, Extract/Inline Variable, Replace Temp with Query, Split Temporary Variable, and Replace Method with Method Object.

### 3. Moving Features Between Objects

**Core concept:** The key OO design decision is where responsibilities live. When Feature Envy, excessive coupling, or unbalanced class sizes show a method or field is in the wrong class, move it where it belongs.

**Why it works:** A method placed away from the data it uses creates invisible cross-class dependencies, so one logical change ripples across many files — Shotgun Surgery. Co-locating method and data confines the change to one class.

**Key insights:**
- Move Method when a method uses more of another class's features than its own; Move Field likewise
- Extract Class when one class does two things — split along the axis of change; Inline Class when one does too little
- Hide Delegate enforces the Law of Demeter; Remove Middle Man undoes it when forwarding becomes the whole class
- Resolve that tension case by case: hide the delegate when the chain is unstable, remove the middle man when it's pure forwarding

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Method envies another class | Move Method | `calculateShipping()` from `Order` to `ShippingPolicy` |
| God class 500+ lines | Extract Class | Pull `Address` fields/methods into own class |
| Client calls `a.getB().getC()` | Hide Delegate | Add `a.getCThroughB()` |
| Class only forwards calls | Remove Middle Man | Let client call the delegate directly |

See [references/moving-features.md](references/moving-features.md) when deciding where a responsibility belongs — mechanics for Move Method/Field, Extract/Inline Class, Hide Delegate, and Remove Middle Man.

### 4. Organizing Data

**Core concept:** Raw data — magic numbers, exposed fields, integer type codes — creates subtle bugs and scatters domain knowledge. Replace primitives with objects that encapsulate behavior and enforce invariants.

**Why it works:** An `int` amount has no rounding rules or currency code; a `Money` object encapsulates all of it, so business rules live in one place and the type system catches errors at compile time.

**Key insights:**
- Replace Magic Number with Symbolic Constant — the simplest data refactoring; it names intent
- Replace Data Value with Object cures Primitive Obsession (`EmailAddress`, `Money`, `Temperature`)
- Encapsulate Field and Encapsulate Collection — never expose raw fields or mutable internal lists
- Replace Type Code with Subclasses when the code affects behavior; with Strategy when subclassing is impractical
- Change Value to Reference when you need identity semantics (one shared `Customer`, not copies)

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| `if (status == 2)` | Replace Magic Number | `if (status == ORDER_SHIPPED)` |
| `String email` passed everywhere | Replace Data Value with Object | `EmailAddress` class with validation |
| Getter returns mutable list | Encapsulate Collection | Return `Collections.unmodifiableList(items)` |
| `int typeCode` with switch | Replace Type Code with Subclasses | `Employee` → `Engineer`, `Manager` |

See [references/organizing-data.md](references/organizing-data.md) when replacing primitives with objects — mechanics for Replace Data Value with Object, Change Value to Reference, Replace Magic Number, Encapsulate Field/Collection, and the Replace Type Code variants.

### 5. Simplifying Conditional Logic

**Core concept:** Deeply nested if/else trees, long switches, and scattered null checks are the hardest code to read and the most bug-prone. Named refactorings decompose, consolidate, and replace conditionals with clearer structures.

**Why it works:** A six-branch conditional forces readers to simulate every path mentally; well-named extracted branches are self-documenting, and polymorphism eliminates whole categories of "forgot this case" bugs.

**Key insights:**
- Decompose Conditional: extract condition, then-branch, and else-branch into named methods
- Consolidate Conditional Expression: merge conditions with the same result into one named check
- Replace Nested Conditional with Guard Clauses: handle edge cases early and return, keeping the main path unindented
- Replace Conditional with Polymorphism is the gold standard for type-based conditionals
- Introduce Special Case (Null Object) eliminates scattered `if (x == null)` checks; Introduce Assertion makes assumptions fail fast

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Long `if` with complex condition | Decompose Conditional | Extract `isSummer(date)` and `summerCharge()` |
| Deeply nested `if/else` | Replace with Guard Clauses | Edge cases first, return early, flat main path |
| Switch on object type | Replace Conditional with Polymorphism | Each type implements its own `calculatePay()` |
| `if (customer == null)` everywhere | Introduce Special Case | `NullCustomer` with safe default behavior |

See [references/simplifying-conditionals.md](references/simplifying-conditionals.md) when untangling branches — before/after examples for Decompose/Consolidate Conditional, Guard Clauses, Replace Conditional with Polymorphism, Special Case, and Assertions.

### 6. Safe Refactoring Workflow

**Core concept:** Refactoring is only safe when wrapped in tests. The workflow is mechanical: run tests (green), apply one small transformation, run tests (green), commit. If tests go red, revert — don't debug a broken refactoring.

**Why it works:** Small steps make the failure obvious (it was the last thing you did) and reverting costs seconds; debugging a failed big-bang rewrite costs days.

**Key insights:**
- Rule of Three: tolerate duplication once, note it twice, refactor on the third occurrence
- Preparatory refactoring: restructure to make the feature easy *before* adding it; comprehension and litter-pickup refactoring keep code improving as you read and touch it
- When NOT to refactor: rewriting is easier, no tests and adding them isn't feasible, or the code will be deleted soon
- Refactor for clarity first, then profile and optimize the measured bottleneck — clear code is easier to tune
- Branch by Abstraction and Parallel Change enable large refactorings in production without long-lived branches

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| About to add a feature | Preparatory Refactoring | Clean the insertion point first |
| Third copy of same logic | Rule of Three | Extract shared logic now |
| Large API change in production | Branch by Abstraction | Add abstraction layer, migrate callers, remove old path |
| Renaming a widely-used method | Parallel Change | Add new, deprecate old, migrate, remove |

See [references/refactoring-workflow.md](references/refactoring-workflow.md) before a large or risky refactoring — the full green-to-green cycle, when (not) to refactor, performance, Branch by Abstraction, and Parallel Change.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Refactoring without tests | No safety net to detect behavior change | Write characterization tests first |
| Big-bang rewrite | Mixes structural and behavioral change; undebuggable | Smallest possible steps, tests after each |
| Refactoring while adding features | Two hats at once — neither change verifiable | Refactor first (commit), then add feature (commit) |
| Renaming without updating callers | Broken build or dead code | Use IDE rename; search all references |
| Extracting too many tiny methods | Indirection without clarity when names are poor | Each name must remove the need to read the body |
| Ignoring the smell catalog | Reinvents fixes instead of applying proven recipes | Learn named smells; each maps to refactorings |
| Refactoring doomed code | Polish on condemned code is waste | Check the code's lifespan justifies the investment |
| Optimizing while refactoring | Conflates clarity with performance | Clarity first, then profile, then optimize hot path |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Do tests pass before you start? | No safety net | Write or fix tests first — never refactor red |
| Can you name the smell you're fixing? | Refactoring by instinct, not catalog | Identify the smell, apply its prescribed refactoring |
| Is each method under ~10 lines? | Long Methods likely | Extract Method into named steps |
| Does each class have one reason to change? | Divergent Change or Large Class | Extract Class to separate responsibilities |
| Are there duplicated code blocks? | The most expensive smell | Extract shared logic into common method/base class |
| Do conditionals use polymorphism where apt? | Switch Statements remain | Replace Conditional with Polymorphism |
| Are you committing after each step? | Risk losing work, mixing changes | Commit after every green-to-green transformation |
| Is the code easier to read after your change? | Refactoring added complexity | Revert and try a different approach |

## Further Reading

The definitive guides to improving existing code:

- [*"Refactoring: Improving the Design of Existing Code (2nd Edition)"*](https://www.amazon.com/Refactoring-Improving-Existing-Addison-Wesley-Signature/dp/0134757599?tag=wondelai00-20) by Martin Fowler
- [*"Working Effectively with Legacy Code"*](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052?tag=wondelai00-20) by Michael Feathers (companion for code without tests)
- [*"Clean Code: A Handbook of Agile Software Craftsmanship"*](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882?tag=wondelai00-20) by Robert C. Martin (complementary naming and style principles)

## About the Author

**Martin Fowler** is Chief Scientist at Thoughtworks, a signatory of the Agile Manifesto, and author of *Refactoring: Improving the Design of Existing Code* (1999; 2nd edition 2018), which introduced catalog-based, named refactorings to mainstream development. His catalog underpins the automated refactoring tools in every major IDE.
