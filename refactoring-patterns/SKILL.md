---
name: refactoring-patterns
description: 'Apply named refactoring transformations to improve code structure without changing behavior. Use when the user mentions "refactor this", "code smells", "extract method", "replace conditional", "technical debt", "move method", "inline variable", or "decompose conditional". Also trigger when cleaning up legacy code, preparing code for new features by restructuring, or identifying which transformation to apply to a specific code smell. Covers smell-driven refactoring, safe transformation sequences, and testing guards. For code quality foundations, see clean-code. For managing complexity, see software-design-philosophy.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Refactoring Patterns Framework

A disciplined approach to improving the internal structure of existing code without changing its observable behavior. Apply these named transformations when reviewing code, reducing technical debt, or preparing code for new features. Every refactoring follows the same loop: verify tests pass, apply one small structural change, verify tests still pass.

## Core Principle

**Refactoring is not rewriting. It is a sequence of small, behavior-preserving transformations, each backed by tests.** You never change what the code does -- you change how the code is organized. The discipline of taking tiny verified steps is what makes refactoring safe. Big-bang rewrites fail because they combine structural change with behavioral change, making it impossible to know which broke things.

**The foundation:** Bad code is not a character flaw -- it is a natural consequence of delivering features under time pressure. Code smells are objective signals that structure has degraded. Named refactorings are the proven mechanical recipes for fixing each smell. The catalog of smells tells you *where* to look; the catalog of refactorings tells you *what to do*.

## Scoring

**Goal: 10/10.** When reviewing or refactoring code, rate the structural quality 0-10 based on adherence to the principles below. A 10/10 means: no obvious smells remain, each function does one thing, names reveal intent, duplication is eliminated, and the test suite covers the refactored paths. Always provide the current score and specific refactorings needed to reach 10/10.

## The Refactoring Patterns Framework

Six areas of focus for systematically improving code structure:

### 1. Code Smells as Triggers

**Core concept:** Code smells are surface indicators of deeper structural problems. They are not bugs -- the code works -- but they signal that the design is making the code harder to understand, extend, or maintain. Each smell maps to one or more named refactorings that fix it.

**Why it works:** Without a shared vocabulary of smells, code review devolves into subjective "I don't like this." Named smells give teams objective criteria: "This is Feature Envy -- the method uses six fields from another class and only one of its own." The name points directly to the fix.

**Key insights:**
- Smells cluster into five families: Bloaters, Object-Orientation Abusers, Change Preventers, Dispensables, and Couplers
- Long Method is the most common smell and the gateway to most other refactorings
- Duplicate Code is the single biggest driver of maintenance cost
- A method that needs a comment to explain *what* it does is a smell -- extract and name the block instead
- Shotgun Surgery (one change requires edits in many classes) and Divergent Change (one class changes for many reasons) are opposites that both signal misplaced responsibilities
- Primitive Obsession -- using raw strings, ints, or arrays instead of small domain objects -- causes errors and duplication throughout the codebase

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Method > 10 lines** | Extract Method | Pull the loop body into `calculateLineTotal()` |
| **Class > 200 lines** | Extract Class | Move shipping logic into a `ShippingCalculator` |
| **Switch on type code** | Replace Conditional with Polymorphism | Create subclasses for each order type |
| **Multiple methods use same params** | Introduce Parameter Object | Group `startDate, endDate` into `DateRange` |
| **Method uses another object's data** | Move Method | Move `calculateDiscount()` to the `Customer` class |
| **Copy-pasted logic** | Extract Method + Pull Up Method | Share via a common method or base class |

See: [references/smell-catalog.md](references/smell-catalog.md)

### 2. Composing Methods

**Core concept:** Most refactoring starts here. Long methods are broken into smaller, well-named pieces. Each extracted piece should do one thing and its name should say what that thing is. The goal is methods you can read like prose -- a sequence of high-level steps, each delegating to a clearly named helper.

**Why it works:** Short methods with intention-revealing names eliminate the need for comments, make bugs obvious (each method is small enough to verify at a glance), and enable reuse. The cognitive cost of a method call is near zero when the name tells you everything.

**Key insights:**
- Extract Method is the single most important refactoring -- master it first
- If you feel the urge to write a comment, extract the code block and use the comment as the method name
- Inline Method when a method body is as clear as the name -- indirection without value is noise
- Replace Temp with Query when a temporary variable holds a computed value that is used in multiple places
- Split Temporary Variable when one variable is reused for two different purposes
- Replace Method with Method Object when a method is too tangled to extract from (many local variables referencing each other)

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Block with a comment** | Extract Method | `// check eligibility` becomes `isEligible()` |
| **Temp used once** | Inline Variable | Remove `const price = order.getPrice()` if used once |
| **Temp used in multiple places** | Replace Temp with Query | Replace `let discount = getDiscount()` with method calls |
| **Temp assigned twice for different reasons** | Split Temporary Variable | Introduce `perimeterWidth` and `perimeterHeight` |
| **Trivial delegating method** | Inline Method | Inline `moreThanFiveDeliveries()` if it's `return deliveries > 5` and only used once |
| **Complex method with many locals** | Replace Method with Method Object | Move the method into its own class where locals become fields |

See: [references/composing-methods.md](references/composing-methods.md)

### 3. Moving Features Between Objects

**Core concept:** The key decision in object-oriented design is where to put responsibilities. When a method or field is in the wrong class -- evidenced by Feature Envy, excessive coupling, or unbalanced class sizes -- move it to where it belongs.

**Why it works:** Well-placed responsibilities reduce coupling and increase cohesion. When a method lives in the class whose data it uses, changes to that data affect only one class. Misplaced methods create invisible dependencies that cause Shotgun Surgery.

**Key insights:**
- Move Method when a method uses more features of another class than its own
- Move Field when a field is used more by another class than the class it lives in
- Extract Class when one class does two things -- split along the axis of change
- Inline Class when a class does too little to justify its existence
- Hide Delegate to enforce the Law of Demeter -- a client shouldn't navigate a chain of objects
- Remove Middle Man when a class does nothing but forward calls
- The tension between Hide Delegate and Remove Middle Man is resolved case by case: hide the delegate when the chain is unstable; remove the middle man when forwarding becomes the entire class

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Method envies another class** | Move Method | Move `calculateShipping()` from `Order` to `ShippingPolicy` |
| **Field used by another class constantly** | Move Field | Move `discountRate` from `Order` to `Customer` |
| **God class with 500+ lines** | Extract Class | Pull `Address` fields and methods into their own class |
| **Tiny class with one field** | Inline Class | Merge `PhoneNumber` back into `Contact` if no behavior |
| **Client calls a.getB().getC()** | Hide Delegate | Add `a.getCThroughB()` so client doesn't know about C |
| **Class only forwards calls** | Remove Middle Man | Let client call the delegate directly |

See: [references/moving-features.md](references/moving-features.md)

### 4. Organizing Data

**Core concept:** Raw data -- magic numbers, exposed fields, type codes represented as integers, parallel arrays -- creates subtle bugs and scatters domain knowledge. Replace primitive representations with objects that encapsulate behavior and enforce invariants.

**Why it works:** An `int` representing a currency amount has no concept of rounding rules, currency codes, or formatting. A `Money` object encapsulates all of that. When domain concepts are represented as first-class objects, business rules live in one place, validation happens automatically, and the type system catches errors at compile time.

**Key insights:**
- Replace Magic Number with Symbolic Constant as the simplest data refactoring -- it names the intent
- Replace Data Value with Object (Primitive Obsession cure) -- wrap strings and numbers in domain objects (`EmailAddress`, `Money`, `Temperature`)
- Encapsulate Field -- never expose a raw field; a getter/setter allows you to add validation, logging, or computation later
- Encapsulate Collection -- return an unmodifiable view; never let callers mutate your internal list
- Replace Type Code with Subclasses when the type code affects behavior; use Strategy when subclassing is impractical
- Change Value to Reference when you need identity semantics (one shared `Customer` object, not copies)

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **`if (status == 2)`** | Replace Magic Number with Symbolic Constant | `if (status == ORDER_SHIPPED)` |
| **`String email` passed everywhere** | Replace Data Value with Object | Create `EmailAddress` class with validation |
| **Public field** | Encapsulate Field | Replace `order.total` with `order.getTotal()` |
| **Getter returns mutable list** | Encapsulate Collection | Return `Collections.unmodifiableList(items)` |
| **`int typeCode` with switch** | Replace Type Code with Subclasses | `Employee` -> `Engineer`, `Manager`, `Salesperson` |
| **Duplicated customer records** | Change Value to Reference | Share one `Customer` instance via a registry |

See: [references/organizing-data.md](references/organizing-data.md)

### 5. Simplifying Conditional Logic

**Core concept:** Complex conditionals -- deeply nested if/else trees, long switch statements, null checks scattered everywhere -- are the hardest code to read and the most likely to contain bugs. Named refactorings decompose, consolidate, and replace conditionals with clearer structures.

**Why it works:** A conditional with six branches and nested sub-conditions requires the reader to simulate every path mentally. Decomposing the condition into well-named methods makes each branch self-documenting. Replacing conditionals with polymorphism eliminates entire categories of "forgot to handle this case" bugs.

**Key insights:**
- Decompose Conditional: extract the condition, the then-branch, and the else-branch into named methods
- Consolidate Conditional Expression: merge multiple conditions that lead to the same result into one named check
- Replace Nested Conditional with Guard Clauses: handle edge cases early and return, leaving the main path unindented
- Replace Conditional with Polymorphism: the gold standard for type-based conditionals -- each type knows its own behavior
- Introduce Special Case (Null Object): eliminate `if (x == null)` checks by providing an object that represents "nothing" with safe default behavior
- Introduce Assertion: make assumptions explicit so they fail fast in development

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Long `if` with complex condition** | Decompose Conditional | Extract `isSummer(date)` and `summerCharge()` |
| **Multiple `if`s return same value** | Consolidate Conditional | Combine into `isDisabled()` returning early |
| **Deeply nested `if/else`** | Replace with Guard Clauses | Check edge cases first, return early, flatten the main path |
| **Switch on object type** | Replace Conditional with Polymorphism | Each type implements its own `calculatePay()` |
| **`if (customer == null)` everywhere** | Introduce Special Case | Create `NullCustomer` with default behavior |
| **Hidden assumption in code** | Introduce Assertion | `assert quantity > 0` at method entry |

See: [references/simplifying-conditionals.md](references/simplifying-conditionals.md)

### 6. Safe Refactoring Workflow

**Core concept:** Refactoring is only safe when wrapped in tests. The workflow is mechanical: run tests (green), apply one small transformation, run tests (green), commit. If tests go red, revert the last change -- don't debug a broken refactoring.

**Why it works:** Small steps make it trivial to find what went wrong (it was the last thing you did). Reverting a failed step costs seconds. Debugging a failed big-bang rewrite costs days. Frequent commits create save points you can return to.

**Key insights:**
- The refactoring cycle: test -> refactor -> test -> commit (repeat)
- Rule of Three: tolerate duplication once, note it twice, refactor on the third occurrence
- Preparatory refactoring: restructure code to make the feature easy *before* adding the feature
- Comprehension refactoring: refactor to understand code as you read it -- leave it clearer than you found it
- Litter-pickup refactoring: small improvements whenever you touch a file (Boy Scout Rule)
- When NOT to refactor: when it's easier to rewrite from scratch, when there are no tests and adding them first isn't feasible, or when the code will be deleted soon
- Refactoring and performance: refactor for clarity first, then profile and optimize the measured bottleneck -- refactored code is easier to tune because the hot path is isolated
- Branch by Abstraction and Parallel Change enable large refactorings in production systems without feature branches

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **About to add a feature** | Preparatory Refactoring | Extract method to make new feature's insertion point clean |
| **Reading unfamiliar code** | Comprehension Refactoring | Rename variables and extract methods to understand intent |
| **Saw a small issue while working** | Litter-Pickup Refactoring | Fix the smell before moving on (Boy Scout Rule) |
| **Third copy of same logic** | Rule of Three | Extract the shared logic into a common method |
| **Large API change in production** | Branch by Abstraction | Introduce abstraction layer, migrate callers, remove old path |
| **Renaming a widely-used method** | Parallel Change | Add new name, deprecate old, migrate callers, remove old |

See: [references/refactoring-workflow.md](references/refactoring-workflow.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Refactoring without tests | No safety net -- you can't tell if behavior changed | Write characterization tests first, then refactor |
| Big-bang rewrite instead of incremental steps | Combines structural and behavioral changes; impossible to debug | Take the smallest step possible, run tests after each |
| Refactoring and adding features at the same time | Two hats at once -- you can't verify either change in isolation | Separate the hats: refactor first (commit), then add feature (commit) |
| Renaming without updating all callers | Breaks the build or introduces dead code | Use IDE rename refactoring; search for all references |
| Extracting too many tiny methods | Creates indirection without clarity when names are poor | Each extracted method must have a name that removes the need to read the body |
| Ignoring the smell catalog | Reinventing fixes instead of applying proven recipes | Learn the named smells; each one maps to specific refactorings |
| Refactoring code that will be deleted | Wasted effort -- polish on condemned code | Ask first: is this code's lifespan long enough to justify the investment? |
| Optimizing prematurely during refactoring | Conflates clarity with performance; optimized code is often harder to read | Refactor for clarity first, then profile, then optimize the measured hot path only |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Do tests pass before you start? | You have no safety net | Write or fix tests first -- do not refactor without green tests |
| Can you name the smell you're fixing? | You're refactoring by instinct, not by catalog | Identify the smell from the catalog, then apply its prescribed refactoring |
| Is each method under ~10 lines? | Long Methods are likely present | Apply Extract Method to break long methods into named steps |
| Does each class have a single reason to change? | Divergent Change or Large Class smell | Apply Extract Class to separate responsibilities |
| Are there duplicated code blocks? | Duplicate Code is the most expensive smell | Extract shared logic into a common method or base class |
| Do conditionals use polymorphism where appropriate? | Switch Statements or complex `if/else` trees remain | Apply Replace Conditional with Polymorphism |
| Are you committing after each refactoring step? | You risk losing work and mixing changes | Commit after every green-to-green transformation |
| Is the code easier to read after your change? | The refactoring may have added complexity | Revert and try a different approach |

## Reference Files

- [smell-catalog.md](references/smell-catalog.md): Comprehensive catalog of code smells organized by family -- Bloaters, Object-Orientation Abusers, Change Preventers, Dispensables, and Couplers -- with detection heuristics and fix mappings
- [composing-methods.md](references/composing-methods.md): Extract Method, Inline Method, Extract Variable, Inline Variable, Replace Temp with Query, Split Temporary Variable, Remove Assignments to Parameters, Replace Method with Method Object -- motivation, mechanics, and examples
- [moving-features.md](references/moving-features.md): Move Method, Move Field, Extract Class, Inline Class, Hide Delegate, Remove Middle Man -- when and how to redistribute responsibilities between objects
- [organizing-data.md](references/organizing-data.md): Replace Data Value with Object, Change Value to Reference, Replace Array with Object, Replace Magic Number, Encapsulate Field, Encapsulate Collection, Replace Type Code with Class/Subclasses/Strategy
- [simplifying-conditionals.md](references/simplifying-conditionals.md): Decompose Conditional, Consolidate Conditional, Replace Nested Conditional with Guard Clauses, Replace Conditional with Polymorphism, Introduce Special Case, Introduce Assertion -- with before/after examples
- [refactoring-workflow.md](references/refactoring-workflow.md): The refactoring cycle, when to refactor, when NOT to refactor, refactoring and performance, Branch by Abstraction, Parallel Change

## Further Reading

This skill is based on the definitive guide to improving the design of existing code:

- [*"Refactoring: Improving the Design of Existing Code (2nd Edition)"*](https://www.amazon.com/Refactoring-Improving-Existing-Addison-Wesley-Signature/dp/0134757599?tag=wondelai00-20) by Martin Fowler
- [*"Working Effectively with Legacy Code"*](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052?tag=wondelai00-20) by Michael Feathers (companion for code without tests)
- [*"Clean Code: A Handbook of Agile Software Craftsmanship"*](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882?tag=wondelai00-20) by Robert C. Martin (complementary naming and style principles)

## About the Author

**Martin Fowler** is the Chief Scientist at Thoughtworks and one of the most influential voices in software engineering. He is the author of *Refactoring: Improving the Design of Existing Code* (1999, 2nd edition 2018), which introduced the concept of named, catalog-based refactoring transformations to mainstream software development. Fowler is also the author of *Patterns of Enterprise Application Architecture*, *UML Distilled*, and numerous influential articles on software design, agile methodology, and continuous delivery. He was a signatory of the Agile Manifesto and has spent decades advocating for evolutionary design -- the practice of continuously improving code structure through disciplined, incremental refactoring rather than upfront big design. His refactoring catalog, originally written in Java, has been adapted to virtually every programming language and is built into the automated refactoring tools of every major IDE.
