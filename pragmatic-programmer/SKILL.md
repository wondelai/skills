---
name: pragmatic-programmer
description: 'Apply meta-principles of software craftsmanship: DRY, orthogonality, tracer bullets, and design by contract. Use when the user mentions "best practices", "pragmatic approach", "broken windows", "tracer bullet", "software craftsmanship", "avoid technical debt", "code ownership", or "how do I become a better developer". Also trigger when evaluating build-vs-buy decisions, designing estimation approaches, or choosing between reversible and irreversible architectural decisions. Covers estimation, domain languages, and reversibility. For code-level quality, see clean-code. For refactoring techniques, see refactoring-patterns.'
license: MIT
metadata:
  author: wondelai
  version: "1.4.0"
---

# The Pragmatic Programmer Framework

A systems-level approach to software craftsmanship from Hunt & Thomas' "The Pragmatic Programmer" (20th Anniversary Edition). Apply these meta-principles when designing systems, reviewing architecture, writing code, or advising on engineering culture -- how to think about software, not just how to write it.

## Core Principle

**Care about your craft.** Software development demands continuous learning, disciplined practice, and personal responsibility -- pragmatic programmers think beyond the immediate problem to context, trade-offs, and long-term consequences. Great software comes from great habits: avoid duplication ruthlessly, keep components orthogonal, and treat every line of code as a living asset that must earn its place. The goal is not perfection -- it is systems that are easy to change, easy to understand, and easy to trust.

## Scoring

**Goal: 10/10.** Score against the seven Quick Diagnostic rows: award ~1.4 points per row answered "yes" (7 yes = 10). Then band the result:
- **9-10**: every principle holds -- DRY knowledge, orthogonal layers, a working tracer slice, contracts at boundaries, no broken windows, reversible vendor/DB choices, ranged estimates.
- **5-6**: 1-2 violations that cost real change-effort (e.g. business logic coupled to the DB, single-point estimates).
- **<=3**: pervasive duplication, global state, or accumulated broken windows -- entropy is winning.

Always state the score, name the failing diagnostic rows, and give the specific fix from the Action column to reach 10/10.

## The Seven Meta-Principles

Seven principles for building software that lasts:

### 1. DRY (Don't Repeat Yourself)

**Core concept:** Every piece of knowledge must have a single, unambiguous, authoritative representation within a system. DRY is about knowledge, not code -- duplicated logic, business rules, or configuration are far more dangerous than duplicated syntax.

**Why it works:** Duplicated knowledge must be changed in multiple places; eventually one gets missed, introducing inconsistency. DRY reduces the surface area for bugs and makes systems easier to change.

**Key insights:**
- DRY applies to knowledge and intent, not textual similarity -- two identical code blocks serving different business rules are NOT duplication
- Four types of duplication: imposed (environment forces it), inadvertent (developers don't realize), impatient (too lazy to abstract), inter-developer (multiple people duplicate)
- Comments that restate the code violate DRY -- explain *why*, not *what*
- Database schemas, API specs, and documentation duplicate knowledge unless generated from a single source
- The opposite of DRY is WET: "Write Everything Twice" or "We Enjoy Typing"

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Config values** | Single source of truth | DB connection in one env file, referenced everywhere |
| **Validation rules** | Shared schema | One JSON Schema or Zod schema for client and server |
| **API contracts** | Generate from spec | OpenAPI spec generates types, docs, and client code |

See: [references/dry-orthogonality.md](references/dry-orthogonality.md) when classifying a specific duplication or deciding whether two code blocks are truly the same knowledge -- per-type examples and mitigations for the four duplication types.

### 2. Orthogonality

**Core concept:** Two components are orthogonal if changes in one do not affect the other. Design systems where components are self-contained, independent, and have a single, well-defined purpose.

**Why it works:** Decoupling localizes change -- a fix in one module can't ripple into unrelated ones, so blast radius stays bounded. Change the database layer and the UI should not break; change the auth provider and business logic should not care.

**Key insights:**
- Ask: "If I dramatically change the requirements behind a function, how many modules are affected?" The answer should be one
- Eliminate effects between unrelated things -- a logging change should never break billing
- Layered architectures promote orthogonality: presentation, domain logic, data access
- Avoid global data -- every consumer of global state is coupled to it
- Frameworks that force you to inherit from their classes reduce orthogonality

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Architecture** | Layered separation | Controller -> Service -> Repository, each replaceable |
| **Dependencies** | Dependency injection | Pass a `Notifier` interface, not a `SlackClient` concrete class |
| **Testing** | Isolated unit tests | Test business logic without database, network, or filesystem |

See: [references/dry-orthogonality.md](references/dry-orthogonality.md) when measuring coupling or refactoring toward decoupled layers -- the change-impact and stranger tests, layered-architecture diagram, and the helicopter analogy.

### 3. Tracer Bullets and Prototypes

**Core concept:** Tracer bullets are end-to-end implementations connecting all layers of the system with minimal functionality. Unlike prototypes (which are throwaway), tracer bullet code is production code -- thin but real.

**Why it works:** Tracer bullets give immediate end-to-end feedback before you invest in filling out every feature. Users see something real, developers have a framework to build on, and integration issues surface early.

**Key insights:**
- Tracer bullet: thin but complete path through the system (UI -> API -> DB) -- you keep it
- Prototype: focused exploration of a single risky aspect -- you throw it away
- Use tracer bullets when "shooting in the dark" -- vague requirements, unproven architecture
- If a tracer misses, adjust and fire again -- the cost of iteration is low
- Label prototypes clearly as throwaway -- never let one become production code

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **New project** | Vertical slice | One feature end-to-end: button -> API -> DB -> response |
| **Uncertain tech** | Spike prototype | Test WebSocket performance before committing |
| **Microservice** | Walking skeleton | Hello-world service through the full CI/CD pipeline |

See: [references/tracer-bullets.md](references/tracer-bullets.md) when deciding tracer vs. prototype on a new project or building a walking skeleton -- the shooting-in-the-dark decision, iteration loop, and common pitfalls.

### 4. Design by Contract and Assertive Programming

**Core concept:** Define and enforce the rights and responsibilities of software modules through preconditions (what must be true before), postconditions (what is guaranteed after), and invariants (what is always true). When a contract is violated, fail immediately and loudly.

**Why it works:** Contracts make assumptions explicit. Instead of silently corrupting data or limping along in an invalid state, the system crashes at the point of the problem -- dead programs tell no lies.

**Key insights:**
- Preconditions: caller's responsibility -- "I accept only positive integers"
- Postconditions: routine's guarantee -- "I will return a sorted list"
- Invariants: always true -- "Account balance never goes negative"
- Crash early: a dead program does far less damage than a crippled one
- Use assertions for things that should never happen; error handling for things that might
- In dynamic languages, implement contracts through runtime checks and guard clauses

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Function entry** | Precondition guard | `assert age >= 0, "Age cannot be negative"` at function start |
| **Class state** | Invariant validation | `validate!` called after every state mutation |
| **API boundary** | Schema validation | Validate request body against schema before processing |

See: [references/contracts-assertions.md](references/contracts-assertions.md) when adding contracts to a routine or deciding assertion vs. error handling -- worked pre/post/invariant patterns, dynamic-language guard clauses, and the assertions-vs-error-handling boundary.

### 5. The Broken Window Theory

**Core concept:** One broken window -- a badly designed piece of code, a poor management decision, a hack that "we'll fix later" -- starts the rot. Once a system shows neglect, entropy accelerates and discipline collapses.

**Why it works:** Psychology. When code is clean, developers feel social pressure to keep it that way; when code is already messy, the threshold for adding more mess drops to zero. Quality is a team habit, not an individual heroic effort.

**Key insights:**
- Don't leave broken windows (bad designs, wrong decisions, poor code) unrepaired
- If you can't fix it now, board it up: a TODO with a ticket, a disabled feature, a stub
- Be a catalyst for change: show people a working glimpse of the future (stone soup)
- Watch for slow degradation (boiled frog) -- monitor tech debt metrics over time
- The first hack is the most expensive because it gives permission for all subsequent hacks

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Legacy code** | Board up windows | Wrap bad code in a clean interface before adding features |
| **Code review** | Zero-tolerance for new debt | Reject PRs adding `// TODO: fix later` without a ticket |
| **Tech debt** | Debt budget | Allocate 20% of each sprint to fixing broken windows |

See: [references/broken-windows.md](references/broken-windows.md) when a team is normalizing neglect or you need to drive a turnaround -- repair strategies, the stone-soup catalyst play, and building a culture of quality.

### 6. Reversibility and Flexibility

**Core concept:** There are no final decisions. Build systems that make it easy to change your mind about databases, frameworks, vendors, architecture, and deployment targets -- the cost of change should be proportional to the scope of change.

**Why it works:** Requirements change, vendors get acquired, technologies fall out of favor. If your architecture hard-codes assumptions about any of these, every change becomes a rewrite; flexible architecture treats decisions as configuration, not structure.

**Key insights:**
- Abstract third-party dependencies behind your own interfaces -- never let vendor APIs leak into business logic
- The "forking road" test: could you switch from Postgres to DynamoDB in a week? If not, you're coupled
- Metadata-driven systems (config files, feature flags) are more flexible than hard-coded logic
- YAGNI applies to premature abstraction too -- don't build flexibility you don't need yet
- Reversibility is not predicting the future; it's not painting yourself into a corner

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Database** | Repository pattern | Business logic calls `repo.save(user)`, not `pg.query(...)` |
| **External API** | Adapter/wrapper | `PaymentGateway` interface wraps Stripe; swap to Braintree later |
| **Feature flags** | Runtime toggles | New checkout flow behind a flag, rollback in seconds |

See: [references/reversibility.md](references/reversibility.md) when committing to a vendor or framework, or weighing how reversible a decision must be -- per-layer reversibility patterns, the forking-road test, and when NOT to optimize for reversibility.

### 7. Estimation and Knowledge Portfolio

**Core concept:** Learn to estimate reliably by understanding scope, building models, decomposing into components, and assigning ranges. Manage your learning like a financial portfolio: invest regularly, diversify, and rebalance.

**Why it works:** Honest estimation builds trust with stakeholders ("1-3 weeks" beats a confidently wrong "2 weeks"). A knowledge portfolio keeps you relevant as technologies shift -- the programmer who stops learning stops being effective.

**Key insights:**
- Ask "what is this estimate for?" -- context determines precision (budget planning vs. sprint planning)
- Use PERT: (Optimistic + 4x Most Likely + Pessimistic) / 6
- Decompose into components and estimate each; the sum is more accurate than a single guess
- Keep an estimation log: compare estimates to actuals and calibrate
- Portfolio rules: invest regularly (learn weekly), diversify beyond your stack, mix safe and speculative bets, learn emerging tech early (buy low)

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Sprint planning** | Range estimates | "3-5 days" with confidence level, not a single number |
| **New technology** | Time-boxed spike | "2 days evaluating; then I can estimate properly" |
| **Learning** | Weekly investment | 1 hour/week on a new language, tool, or domain |

See: [references/estimation-portfolio.md](references/estimation-portfolio.md) when producing an estimate you'll be held to or calibrating past misses -- the PERT and decomposition procedures, an estimation-log calibration loop, and portfolio rebalancing.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| DRY-ing similar-looking code that serves different purposes | Couples unrelated concepts; changes to one break the other | Only DRY knowledge, not coincidental code similarity |
| Skipping tracer bullets, building layer-by-layer | Integration issues surface late; no end-to-end feedback | Build one thin vertical slice first |
| Ignoring broken windows "because we'll refactor later" | Entropy accelerates; later never comes; morale drops | Fix immediately or board up with a tracked ticket |
| Estimates as single-point commitments | False precision erodes trust when missed | Always give ranges with confidence levels |
| Making everything "flexible" upfront | Over-engineering; abstraction without evidence of need | Add flexibility when you have concrete evidence you'll need it |
| Removing production assertions "for performance" | Bugs assertions would catch now silently corrupt data | Keep critical assertions; benchmark before removing any |
| Global state "for convenience" | Destroys orthogonality; everything coupled to everything | Use dependency injection and explicit parameters |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can I change the database without touching business logic? | Orthogonality violation | Introduce repository/adapter pattern |
| Do I have an end-to-end slice working? | Missing tracer bullet | Build one vertical slice before expanding |
| Is every business rule defined in exactly one place? | DRY violation | Identify the authoritative source; remove duplicates |
| Would a new developer call this codebase "clean"? | Broken windows present | Schedule a dedicated cleanup sprint |
| Do my estimates include ranges and confidence levels? | Estimation problem | Switch to PERT or range-based estimates |
| Can I roll back this deployment in under 5 minutes? | Reversibility gap | Add feature flags and blue-green deploys |
| Am I learning something new every week? | Knowledge portfolio stagnant | Schedule weekly learning time and track it |

## Further Reading

- [The Pragmatic Programmer: Your Journey to Mastery, 20th Anniversary Edition](https://www.amazon.com/Pragmatic-Programmer-journey-mastery-Anniversary/dp/0135957052?tag=wondelai00-20) by Andrew Hunt and David Thomas

## About the Authors

**Andrew Hunt** and **David Thomas** co-founded the Pragmatic Bookshelf and were among the 17 original authors of the Agile Manifesto. Thomas coined "DRY" and "Code Kata" and co-authored *Programming Ruby* (the Pickaxe book); Hunt focuses on how teams learn, communicate, and maintain quality. Together they wrote *The Pragmatic Programmer*, one of the most influential software books ever published.
