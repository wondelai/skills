---
name: software-design-philosophy
description: 'Manage software complexity through deep modules, information hiding, and strategic programming. Use when the user mentions "module design", "API too complex", "shallow class", "complexity budget", "strategic vs tactical", "deep module", "information leakage", "pass-through method", "this code is over-engineered", "too many layers", "the abstraction isnt worth it", or "simplify this design". Also trigger when reviewing an interface for simplicity, evaluating whether an abstraction is pulling its weight, or choosing between general-purpose and special-purpose approaches. Covers deep vs shallow modules, red flags for complexity, and comments as design documentation. For code quality, see clean-code. For boundaries, see clean-architecture.'
license: MIT
metadata:
  author: wondelai
  version: "1.3.0"
---

# A Philosophy of Software Design Framework

A practical framework for managing the fundamental challenge of software engineering: complexity. Apply these principles when designing modules, reviewing APIs, refactoring code, or advising on architecture decisions.

## Core Principle

**The greatest limitation in writing software is our ability to understand the systems we are creating.** Complexity is the enemy: it makes systems hard to understand, hard to modify, and a source of bugs. Evaluate every design decision by asking "Does this increase or decrease the overall complexity of the system?" — the goal is not zero complexity, but minimizing unnecessary complexity and concentrating the necessary kind where it can be managed.

## Scoring

**Goal: 10/10.** When reviewing or creating software designs, rate them 0-10: a 10/10 means deep modules with clean abstractions, excellent information hiding, strategic thinking, and comments that capture design intent; lower scores indicate shallow modules, leakage, or tactical shortcuts. Always give the current score and the specific improvements needed to reach 10/10.

## The Software Design Framework

Six principles for managing complexity and producing systems that are easy to understand and modify:

### 1. Complexity and Its Causes

**Core concept:** Complexity is anything about a system's structure that makes it hard to understand and modify. It shows three symptoms — change amplification, cognitive load, and unknown unknowns — and has two causes: dependencies and obscurity.

**Why it works:** Naming the specific symptoms lets developers diagnose problems precisely instead of relying on vague notions of "messy code," and the two causes provide clear targets for improvement.

**Key insights:**
- Change amplification: a simple change requires edits in many places
- Cognitive load: a developer must hold too much in mind to make a change
- Unknown unknowns: it isn't obvious what must change or what information is relevant — the worst symptom
- Complexity is incremental — it accumulates from hundreds of small decisions ("death by a thousand cuts"), so every decision matters

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Change amplification | Centralize shared knowledge | Extract color constants instead of hardcoding `#ff0000` in 20 files |
| Cognitive load | Reduce what developers must know | `open(path)` instead of requiring buffer size, encoding, lock mode |
| Unknown unknowns | Make dependencies explicit | Type systems and interfaces surface what a change affects |
| Obscurity | Name things precisely | `numBytesReceived` not `n`; `retryDelayMs` not `delay` |

See: [references/complexity-symptoms.md](references/complexity-symptoms.md) for symptom diagnosis and how complexity accumulates.

### 2. Deep vs Shallow Modules

**Core concept:** The best modules are deep: powerful functionality behind a simple interface. Shallow modules have complex interfaces relative to the functionality they provide — they add complexity rather than hiding it.

**Why it works:** The interface is the complexity a module imposes on the rest of the system; the implementation is the functionality it provides. Deep modules maximize benefit per unit of interface cost.

**Key insights:**
- Depth = functionality provided / interface complexity imposed (Unix file I/O is deep; thin Java I/O wrappers are shallow)
- "Classitis": the disease of creating too many small, shallow classes — each interface adds cognitive load
- Small methods are not inherently good; depth matters more than size
- The best abstractions hide significant complexity behind a few simple concepts

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Deep module | Hide complexity behind simple API | `file.read(path)` hides disk blocks, caching, buffering, encoding |
| Classitis cure | Merge related shallow classes | `RequestParser` + `RequestValidator` + `RequestProcessor` → one `RequestHandler` |
| Interface simplicity | Fewer parameters, fewer methods | `config.get(key)` with sensible defaults, not 15 constructor parameters |

See: [references/deep-modules.md](references/deep-modules.md) when judging whether an abstraction pulls its weight.

### 3. Information Hiding and Leakage

**Core concept:** Each module should encapsulate knowledge not needed by other modules. Information leakage — one design decision reflected in multiple modules — is one of the most important red flags in software design.

**Why it works:** Hidden knowledge can change inside one module; leaked knowledge makes changes propagate through the system. Hiding attacks both causes of complexity: dependencies and obscurity.

**Key insights:**
- Temporal decomposition causes leakage: splitting code by *when* things happen forces shared knowledge across phases — organize by knowledge instead
- Back-door leakage through data formats, protocols, or shared assumptions is the subtlest form
- Decorators frequently leak — they expose the decorated interface
- If two modules share knowledge, merge them or create a new module that encapsulates it

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Format leakage | Centralize serialization | One module owns JSON encoding/decoding, not `json.dumps` everywhere |
| Temporal decomposition | Organize by knowledge, not time | Combine "read config" and "apply config" into one config module |
| Protocol leakage | Abstract transport details | `MessageBus.send(event)` hides HTTP vs. gRPC vs. queue |

See: [references/information-hiding.md](references/information-hiding.md) for leakage red flags and decorator pitfalls.

### 4. General-Purpose vs Special-Purpose Modules

**Core concept:** Design modules that are "somewhat general-purpose": an interface general enough to support multiple uses, with an implementation that handles current needs. Ask: "What is the simplest interface that will cover all my current needs?"

**Why it works:** General-purpose interfaces are usually simpler because they eliminate special cases, and new use cases often fit the existing abstraction — while over-generalization wastes effort on speculative complexity.

**Key insights:**
- "Somewhat general-purpose" is the sweet spot between too specific and too generic
- Push complexity downward: lower-level modules should handle hard cases so upper levels stay simple
- Configuration parameters often represent a failure to decide — each parameter is complexity pushed onto the caller
- When in doubt, implement the simpler, more general-purpose approach first

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| API generality | Design for the concept, not one use case | `text.insert(position, string)` instead of `text.addBulletPoint()` |
| Reduce configuration | Determine behavior automatically | Auto-detect file encoding instead of an `encoding` parameter |
| Avoid over-specialization | One general method over many specific ones | `store(key, value, options)` instead of `storeUser()`, `storeProduct()`, `storeOrder()` |

See: [references/general-vs-special.md](references/general-vs-special.md) when choosing how general an interface should be.

### 5. Comments as Design Documentation

**Core concept:** Comments should describe what is not obvious from the code: design intent, abstraction rationale, invariants, and assumptions. "Good code is self-documenting" is a myth for anything beyond low-level implementation detail.

**Why it works:** Code tells you what the program does, not why, what the alternatives were, or what it assumes — comments capture the designer's mental model, the most valuable and most perishable information in a system.

**Key insights:**
- Four types: interface comments (most important — they define the abstraction), data structure member comments, implementation comments, cross-module comments
- Write comments first (comment-driven design) to clarify thinking before code
- Don't repeat what the code makes clear; keep comments next to the code they describe and update them together
- If a comment is hard to write, the design may be too complex

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Interface comment | Describe the abstraction, not the implementation | "Returns the widget closest to position, or null if none within threshold" |
| Data structure comment | Explain invariants | "List is sorted by priority descending; ties broken by insertion order" |
| Implementation comment | Explain why, not what | "// Binary search: list is always sorted, can hold 100k+ items" |
| Cross-module comment | Link related decisions | "// This timeout must match the retry interval in RetryPolicy.java" |

See: [references/comments-as-design.md](references/comments-as-design.md) for comment-driven design and the self-documenting-code myth.

### 6. Strategic vs Tactical Programming

**Core concept:** Tactical programming gets features working quickly and accumulates complexity with each shortcut. Strategic programming invests 10-20% extra effort in good design, treating every change as an opportunity to improve structure.

**Why it works:** Tactical speed is borrowed: each shortcut makes future changes harder, while the strategic investment compounds — strategically designed systems are faster to work with within months.

**Key insights:**
- Tactical tornado: a developer who ships fast but leaves wreckage — celebrated short-term, destructive long-term
- Your primary job is a great design that happens to work, not working code that happens to have a design
- Startups need strategic programming most — early shortcuts compound into crippling debt as the team grows
- Every change is an investment opportunity: leave the code a little better; refactoring is part of every feature, not a special event

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Tactical trap | Resist quick-and-dirty fixes | Don't add a boolean parameter for "just this one special case" |
| Strategic investment | Improve structure during feature work | Refactor an awkward module interface while adding the feature |
| Design reviews | Evaluate structure, not just correctness | Ask "does this make the system simpler?" not just "does it work?" |

See: [references/strategic-programming.md](references/strategic-programming.md) for the investment mindset and startup considerations.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| **Creating too many small classes** | Classitis adds interfaces without depth; each boundary is cognitive overhead | Merge related shallow classes into deeper modules |
| **Splitting modules by temporal order** | "Read, then process, then write" forces shared knowledge across modules | Group code that shares knowledge into one module |
| **Exposing implementation in interfaces** | Callers depend on internals; changes propagate | Design interfaces around abstractions; hide formats and protocols |
| **Treating comments as optional** | Design intent and assumptions are lost; newcomers guess wrong | Write interface comments first; maintain with the code |
| **Configuration parameters for everything** | Each parameter pushes a decision onto the caller | Determine behavior automatically; provide sensible defaults |
| **Quick-and-dirty tactical fixes** | Shortcuts compound until the system is unworkable | Invest 10-20% extra; treat every change as a design opportunity |
| **Pass-through methods** | Delegation-only methods add interface without depth | Merge the pass-through into the caller or the callee |
| **Designing for specific use cases** | Special-purpose interfaces accumulate special cases | Ask: simplest interface covering all current needs? |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you describe each module in one sentence? | Modules do too much or lack purpose | Split into coherent, describable responsibilities |
| Are interfaces simpler than implementations? | Modules are shallow — complexity leaks outward | Hide more; merge shallow classes into deeper ones |
| Can you change an implementation without affecting callers? | Information is leaking across boundaries | Encapsulate the leaked knowledge in one module |
| Do interface comments describe the abstraction? | Design intent lost; module will be misused | Document what the module promises, not how it works |
| Is design discussion part of code reviews? | Reviews catch bugs but not complexity growth | Add "does this reduce complexity?" to review criteria |
| Does each module hide an important design decision? | Modules organized around code, not information | Reorganize so each module owns specific knowledge |
| Can a newcomer understand module boundaries without reading implementations? | Abstractions undocumented or leaky | Improve interface comments; simplify interfaces |
| Are you spending 10-20% of time on design improvement? | Debt accumulates with every feature | Include design improvement in every PR |

## Reference Files

- [complexity-symptoms.md](references/complexity-symptoms.md): Three symptoms of complexity, two causes, measuring complexity, its incremental nature
- [deep-modules.md](references/deep-modules.md): Deep vs shallow modules, interface-to-functionality ratio, classitis, designing for depth
- [information-hiding.md](references/information-hiding.md): Information hiding principle, leakage red flags, temporal decomposition, decorator pitfalls
- [general-vs-special.md](references/general-vs-special.md): Somewhat general-purpose approach, pushing complexity down, configuration parameter antipattern
- [comments-as-design.md](references/comments-as-design.md): Four comment types, comment-driven design, self-documenting code myth, maintaining comments
- [strategic-programming.md](references/strategic-programming.md): Strategic vs tactical mindset, tactical tornado, investment approach, startup considerations

## Further Reading

For the complete methodology with detailed examples:

- [*"A Philosophy of Software Design"*](https://www.amazon.com/Philosophy-Software-Design-2nd/dp/173210221X?tag=wondelai00-20) by John Ousterhout (2nd edition)

## About the Author

**John Ousterhout** is the Bosack Lerner Professor of Computer Science at Stanford and the creator of the Tcl scripting language and Tk toolkit. He developed *A Philosophy of Software Design* from his Stanford CS 190 course, distilling decades of systems-building experience into principles that apply across languages and scales.
