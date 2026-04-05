---
name: pragmatic-programmer
description: 'Apply meta-principles of software craftsmanship: DRY, orthogonality, tracer bullets, and design by contract. Use when the user mentions "best practices", "pragmatic approach", "broken windows", "tracer bullet", "software craftsmanship", "technical debt prevention", "prototype vs tracer bullet", or "code ownership". Also trigger when evaluating build-vs-buy decisions, designing estimation approaches, or choosing between reversible and irreversible architectural decisions. Covers estimation, domain languages, and reversibility. For code-level quality, see clean-code. For refactoring techniques, see refactoring-patterns.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# The Pragmatic Programmer Framework

A systems-level approach to software craftsmanship from Hunt & Thomas' "The Pragmatic Programmer" (20th Anniversary Edition). Apply these principles when designing systems, reviewing architecture, writing code, or advising on engineering culture. This framework addresses the meta-level: how to think about software, not just how to write it.

## Core Principle

**Care about your craft.** Software development is a craft that demands continuous learning, disciplined practice, and personal responsibility. Pragmatic programmers think beyond the immediate problem -- they consider context, trade-offs, and long-term consequences of every technical decision.

**The foundation:** Great software comes from great habits. A pragmatic programmer maintains a broad knowledge portfolio, communicates clearly, avoids duplication ruthlessly, keeps components orthogonal, and treats every line of code as a living asset that must earn its place. The goal is not perfection -- it is building systems that are easy to change, easy to understand, and easy to trust.

## Scoring

**Goal: 10/10.** When reviewing or creating software designs, architecture, or code, rate it 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## The Pragmatic Programmer Framework

Seven meta-principles for building software that lasts:

### 1. DRY (Don't Repeat Yourself)

**Core concept:** Every piece of knowledge must have a single, unambiguous, authoritative representation within a system. DRY is about knowledge, not code -- duplicated logic, business rules, or configuration are far more dangerous than duplicated syntax.

**Why it works:** When knowledge is duplicated, changes must be made in multiple places. Eventually one gets missed, introducing inconsistency. DRY reduces the surface area for bugs and makes systems easier to change.

**Key insights:**
- DRY applies to knowledge and intent, not textual similarity -- two identical code blocks serving different business rules are NOT duplication
- Four types of duplication: imposed (environment forces it), inadvertent (developers don't realize), impatient (too lazy to abstract), inter-developer (multiple people duplicate)
- Code comments that restate the code violate DRY -- comments should explain *why*, not *what*
- Database schemas, API specs, and documentation are all sources of duplication if not generated from a single source
- The opposite of DRY is WET: "Write Everything Twice" or "We Enjoy Typing"

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Config values** | Single source of truth | Define DB connection in one env file, reference everywhere |
| **Validation rules** | Shared schema | Use JSON Schema or Zod schema for both client and server validation |
| **API contracts** | Generate from spec | OpenAPI spec generates types, docs, and client code |
| **Business logic** | Domain module | Tax calculation in one module, not scattered across controllers |
| **Database schema** | Migration-driven | Schema defined in migrations, ORM models generated from DB |

See: [references/dry-orthogonality.md](references/dry-orthogonality.md)

### 2. Orthogonality

**Core concept:** Two components are orthogonal if changes in one do not affect the other. Design systems where components are self-contained, independent, and have a single, well-defined purpose.

**Why it works:** Orthogonal systems are easier to test, easier to change, and produce fewer side effects. When you change the database layer, the UI should not break. When you change the auth provider, the business logic should not care.

**Key insights:**
- Ask: "If I dramatically change the requirements behind a particular function, how many modules are affected?" The answer should be one
- Eliminate effects between unrelated things -- a logging change should never break billing
- Layered architectures promote orthogonality: presentation, domain logic, data access
- Avoid global data -- every consumer of global state is coupled to it
- Toolkits and libraries that force you to inherit from framework classes reduce orthogonality

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Architecture** | Layered separation | Controller -> Service -> Repository, each replaceable |
| **Dependencies** | Dependency injection | Pass a `Notifier` interface, not a `SlackClient` concrete class |
| **Testing** | Isolated unit tests | Test business logic without database, network, or filesystem |
| **Configuration** | Environment-driven | Feature flags in config, not `if` branches in business logic |
| **Deployment** | Independent services | Deploy auth service without redeploying payment service |

See: [references/dry-orthogonality.md](references/dry-orthogonality.md)

### 3. Tracer Bullets and Prototypes

**Core concept:** Tracer bullets are end-to-end implementations that connect all layers of the system with minimal functionality. Unlike prototypes (which are throwaway), tracer bullet code is production code -- thin but real.

**Why it works:** Tracer bullets give immediate feedback. You see what the system looks like end-to-end before investing in filling out every feature. Users can see something real, developers have a framework to build on, and integration issues surface early.

**Key insights:**
- Tracer bullet: thin but complete path through the system (UI -> API -> DB) -- you keep it
- Prototype: focused exploration of a single risky aspect -- you throw it away
- Tracer bullets work when you're "shooting in the dark" -- requirements are vague, architecture is unproven
- If a tracer misses, adjust and fire again -- the cost of iteration is low
- Prototypes should be clearly labeled as throwaway -- never let a prototype become production code

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **New project** | Vertical slice | Build one feature end-to-end: button -> API -> DB -> response |
| **Uncertain tech** | Spike prototype | Test if WebSocket performance is sufficient before committing |
| **Framework eval** | Tracer through stack | Build login flow through the full framework before choosing it |
| **Microservice** | Walking skeleton | Deploy a hello-world service through the full CI/CD pipeline |
| **Data pipeline** | End-to-end flow | One record from ingestion through transformation to output |

See: [references/tracer-bullets.md](references/tracer-bullets.md)

### 4. Design by Contract and Assertive Programming

**Core concept:** Define and enforce the rights and responsibilities of software modules through preconditions (what must be true before), postconditions (what is guaranteed after), and class invariants (what is always true). When a contract is violated, fail immediately and loudly.

**Why it works:** Contracts make assumptions explicit. Instead of silently corrupting data or limping along in an invalid state, the system crashes at the point of the problem -- making bugs visible and traceable. Dead programs tell no lies.

**Key insights:**
- Preconditions: caller's responsibility -- "I accept only positive integers"
- Postconditions: routine's guarantee -- "I will return a sorted list"
- Invariants: always true -- "Account balance never goes negative"
- Crash early: a dead program does far less damage than a crippled one
- Use assertions for things that should never happen; use error handling for things that might
- In dynamic languages, implement contracts through runtime checks and guard clauses

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Function entry** | Precondition guard | `assert age >= 0, "Age cannot be negative"` at function start |
| **Function exit** | Postcondition check | Verify returned list is sorted before returning |
| **Class state** | Invariant validation | `validate!` method called after every state mutation |
| **API boundary** | Schema validation | Validate request body against schema before processing |
| **Data pipeline** | Stage assertions | Assert row count after ETL transform matches expectation |

See: [references/contracts-assertions.md](references/contracts-assertions.md)

### 5. The Broken Window Theory

**Core concept:** One broken window -- a badly designed piece of code, a poor management decision, a hack that "we'll fix later" -- starts the rot. Once a system shows neglect, entropy accelerates and discipline collapses.

**Why it works:** Psychology. When code is clean and well-maintained, developers feel social pressure to keep it that way. When code is already messy, the threshold for adding more mess drops to zero. Quality is a team habit, not an individual heroic effort.

**Key insights:**
- Don't leave broken windows (bad designs, wrong decisions, poor code) unrepaired
- If you can't fix it now, board it up: add a TODO with a ticket, disable the feature, replace with a stub
- Be a catalyst for change: show people a working glimpse of the future (stone soup)
- Watch for slow degradation (boiled frog) -- monitor tech debt metrics over time
- The first hack is the most expensive because it gives permission for all subsequent hacks

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Legacy code** | Board up windows | Wrap bad code in a clean interface before adding features |
| **Code review** | Zero-tolerance for new debt | Reject PRs that add `// TODO: fix later` without a ticket |
| **Tech debt** | Debt budget | Allocate 20% of each sprint to fixing broken windows |
| **New team member** | Clean onboarding path | First task: fix a broken window to learn the codebase |
| **Monitoring** | Entropy metrics | Track linting violations, test coverage trends over time |

See: [references/broken-windows.md](references/broken-windows.md)

### 6. Reversibility and Flexibility

**Core concept:** There are no final decisions. Build systems that make it easy to change your mind about databases, frameworks, vendors, architecture, and deployment targets. The cost of change should be proportional to the scope of change.

**Why it works:** Requirements change. Vendors get acquired. Technologies fall out of favor. If your architecture has hard-coded assumptions about any of these, every change becomes a rewrite. Flexible architecture treats decisions as configuration, not structure.

**Key insights:**
- Abstract third-party dependencies behind your own interfaces -- never let vendor APIs leak into business logic
- Use the "forking road" test: could you switch from Postgres to DynamoDB in a week? If not, you're coupled
- Metadata-driven systems (config files, feature flags) are more flexible than hard-coded logic
- YAGNI applies to premature abstraction too -- don't build flexibility you don't need yet
- Reversibility is not about predicting the future; it's about not painting yourself into a corner

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Database** | Repository pattern | Business logic calls `repo.save(user)`, not `pg.query(...)` |
| **External API** | Adapter/wrapper | `PaymentGateway` interface wraps Stripe; swap to Braintree later |
| **Feature flags** | Runtime toggles | New checkout flow behind a flag, rollback in seconds |
| **Architecture** | Event-driven decoupling | Services communicate via events, not direct HTTP calls |
| **Deployment** | Container abstraction | Dockerized app runs on AWS, GCP, or bare metal unchanged |

See: [references/reversibility.md](references/reversibility.md)

### 7. Estimation and Knowledge Portfolio

**Core concept:** Learn to estimate reliably by understanding scope, building models, decomposing into components, and assigning ranges. Manage your learning like a financial portfolio: invest regularly, diversify, and rebalance.

**Why it works:** Estimation builds trust with stakeholders when done honestly ("1-3 weeks" is better than "2 weeks exactly"). A knowledge portfolio ensures you stay relevant as technologies shift -- the programmer who stops learning stops being effective.

**Key insights:**
- Ask "what is this estimate for?" -- context determines precision (budget planning vs. sprint planning)
- Use PERT: Optimistic + 4x Most Likely + Pessimistic, divided by 6
- Break estimates into components and estimate each; the total is more accurate than a single guess
- Keep an estimation log: compare estimates to actuals and calibrate
- Knowledge portfolio rules: invest regularly (learn something every week), diversify (don't only learn your stack), manage risk (mix safe and speculative bets), buy low/sell high (learn emerging tech early)

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Sprint planning** | Range estimates | "3-5 days" with confidence level, not a single number |
| **New technology** | Time-boxed spike | "I'll spend 2 days evaluating; then I can estimate properly" |
| **Large project** | Bottom-up decomposition | Break into tasks < 1 day, sum with buffer for integration |
| **Learning** | Weekly investment | 1 hour/week on a new language, tool, or domain |
| **Career growth** | Portfolio diversification | Mix of depth (expertise) and breadth (adjacent skills) |

See: [references/estimation-portfolio.md](references/estimation-portfolio.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| DRY-ing similar-looking code that serves different purposes | Creates coupling between unrelated concepts; changes to one break the other | Only DRY knowledge, not coincidental code similarity |
| Skipping tracer bullets and building layer-by-layer | Integration issues surface late; no end-to-end feedback until the end | Build one thin vertical slice first |
| Ignoring broken windows "because we'll refactor later" | Entropy accelerates; later never comes; team morale drops | Fix immediately or board up with a tracked ticket |
| Estimates as single-point commitments | Creates false precision; erodes trust when missed | Always give ranges with confidence levels |
| Making everything "flexible" upfront | Over-engineering; YAGNI; abstraction without evidence of need | Add flexibility when you have concrete evidence you'll need it |
| Assertions in production removed "for performance" | Bugs that assertions would catch now silently corrupt data | Keep critical assertions; benchmark before removing any |
| Global state "for convenience" | Destroys orthogonality; every module coupled to everything | Use dependency injection and explicit parameters |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can I change the database without touching business logic? | Orthogonality violation | Introduce repository/adapter pattern |
| Do I have an end-to-end slice working? | Missing tracer bullet | Build one vertical slice before expanding |
| Is every business rule defined in exactly one place? | DRY violation | Identify the authoritative source and remove duplicates |
| Would a new developer call this codebase "clean"? | Broken windows present | Schedule a dedicated cleanup sprint |
| Do my estimates include ranges and confidence levels? | Estimation problem | Switch to PERT or range-based estimates |
| Can I roll back this deployment in under 5 minutes? | Reversibility gap | Add feature flags and blue-green deploys |
| Am I learning something new every week? | Knowledge portfolio stagnant | Schedule weekly learning time and track it |

## Reference Files

- [references/dry-orthogonality.md](references/dry-orthogonality.md) -- DRY knowledge vs. code duplication, four types of duplication, orthogonality in design and testing
- [references/tracer-bullets.md](references/tracer-bullets.md) -- Tracer bullet vs. prototype development, building walking skeletons, iterating on tracer code
- [references/contracts-assertions.md](references/contracts-assertions.md) -- Design by Contract, preconditions/postconditions/invariants, assertive programming patterns
- [references/broken-windows.md](references/broken-windows.md) -- Software entropy, broken window theory, stone soup strategy, fighting degradation
- [references/reversibility.md](references/reversibility.md) -- Flexible architecture, decoupling strategies, avoiding vendor lock-in, forking road decisions
- [references/estimation-portfolio.md](references/estimation-portfolio.md) -- PERT estimation, decomposition techniques, knowledge portfolio management

## Further Reading

- [The Pragmatic Programmer: Your Journey to Mastery, 20th Anniversary Edition](https://www.amazon.com/Pragmatic-Programmer-journey-mastery-Anniversary/dp/0135957052?tag=wondelai00-20) by Andrew Hunt and David Thomas

## About the Authors

**Andrew Hunt** is a programmer, author, and publisher. He co-founded the Pragmatic Bookshelf and was one of the 17 original authors of the Agile Manifesto. His work focuses on the human side of software development -- how teams learn, communicate, and maintain quality over time.

**David Thomas** is a programmer and author who co-founded the Pragmatic Bookshelf. He coined the term "DRY" (Don't Repeat Yourself) and "Code Kata." A pioneer in Ruby adoption outside Japan, he co-authored "Programming Ruby" (the Pickaxe book) and has spent decades advocating for developer pragmatism over dogma.
