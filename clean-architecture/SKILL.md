---
name: clean-architecture
description: 'Structure software around the Dependency Rule: source code dependencies point inward from frameworks to use cases to entities. Use when the user mentions "architecture layers", "dependency rule", "ports and adapters (hexagonal)", "onion architecture", "screaming architecture", "where should business logic go", "decouple from the database", "swap the framework without a rewrite", or "keep business rules independent". Also trigger when deciding which layer code belongs in, isolating core logic from infrastructure, defining module boundaries, or debating whether the framework should call your code or the reverse. Covers component principles, boundaries, and SOLID. For code-level quality, see clean-code. For domain modeling, see domain-driven-design.'
license: MIT
metadata:
  author: wondelai
  version: "1.4.0"
---

# Clean Architecture Framework

A disciplined approach to structuring software so that business rules remain independent of frameworks, databases, and delivery mechanisms. Apply these principles when designing system architecture, reviewing module boundaries, or advising on dependency management.

## Core Principle

**Source code dependencies must point inward — toward higher-level policies.** Nothing in an inner circle can know anything about an outer circle. This single rule produces systems that are testable and independent of frameworks, UI, database, and any external agency. Business rules are what matter; databases, web frameworks, and delivery mechanisms are details — when details depend on policies, you can defer decisions, swap implementations, and test business logic in isolation.

## Scoring

**Goal: 10/10.** Score one point for each of the seven Quick Diagnostic rows the architecture satisfies (0-7), then map to a 0-10 band: 6-7 satisfied = **9-10** (Dependency Rule holds, business logic is framework- and DB-independent); 4-5 = **6-8** (core is testable but some details leak inward); 2-3 = **3-5** (framework or persistence dictates structure); 0-1 = **0-2** (no boundaries — business rules live in controllers and ORM models). Report the score, the failed diagnostic rows, and the specific inversion needed to fix each.

### 1. Dependency Rule and Concentric Circles

**Core concept:** Organize the architecture as concentric circles — Entities (enterprise business rules) innermost, then Use Cases (application business rules), then Interface Adapters, with Frameworks and Drivers outermost. Source code dependencies always point inward.

**Why it works:** When high-level policies don't depend on low-level details, you can swap the database, web framework, or API style without touching business logic — the system becomes resilient to the most volatile parts of the stack.

**Key insights:**
- Inner circles cannot mention outer circle names — no classes, functions, variables, or data formats from outside
- Data crossing a boundary must be in the form most convenient for the inner circle, never dictated by the outer
- Dependency Inversion (interfaces defined inward, implemented outward) is the mechanism that enforces the rule
- The number of circles is not fixed — four is typical; the rule stays the same
- Frameworks are details, not architecture — they belong in the outermost circle

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Layer direction** | Inner circles define interfaces; outer implement | `UserRepository` interface in Use Cases; `PostgresUserRepository` in Adapters |
| **Data crossing** | DTOs cross boundaries, not ORM entities | Use Case returns `UserResponse` DTO, not an ActiveRecord model |
| **Dependency direction** | Import arrows always point inward | Controller imports Use Case; Use Case never imports Controller |

See [references/dependency-rule.md](references/dependency-rule.md) when an inner-circle import points outward and you need the four-circle code walkthrough, the data-crossing rules, and the four-step dependency-inversion procedure to fix it.

### 2. Entities and Use Cases

**Core concept:** Entities encapsulate enterprise-wide business rules — rules that would exist even without software. Use Cases contain application-specific rules that orchestrate the flow of data to and from Entities.

**Why it works:** Separating what the business does (Entities) from how the application orchestrates it (Use Cases) lets you reuse Entities across applications and change application behavior without altering core business rules.

**Key insights:**
- Entities are not database rows — they are objects or pure functions encapsulating critical business rules
- Use Cases accept Request Models and return Response Models — never framework objects
- Each Use Case is a single application operation (`CreateOrder`, `ApproveExpense`)
- The Interactor pattern: a Use Case class implements an input boundary interface and calls an output boundary interface
- Changes to a Use Case should never affect an Entity; Entity changes may ripple to Use Cases

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Entity design** | Critical business rules, zero framework dependencies | `Order.calculateTotal()` applies tax rules; knows nothing about HTTP |
| **Request/Response** | Simple data structures cross the boundary | `CreateOrderRequest { items, customerId }` — no ORM models |
| **Single responsibility** | One Use Case per operation | `PlaceOrder`, `CancelOrder`, `RefundOrder` as separate classes |
| **Interactor** | Implements Input Port, calls Output Port | `PlaceOrderInteractor implements PlaceOrderInput` |

See [references/entities-use-cases.md](references/entities-use-cases.md) when designing an Interactor or deciding what belongs in an Entity versus a Use Case — full Enterprise vs. Application Business Rules treatment with request/response model examples.

### 3. Interface Adapters and Frameworks

**Core concept:** Interface Adapters convert data between the form convenient for Use Cases/Entities and the form required by external agencies. Frameworks and Drivers are the outermost layer — glue code to the outside world.

**Why it works:** When the web framework, ORM, or message queue is confined to the outer circles, replacing any of them is a localized change. The database is a detail; the web is a detail; details should be plugins to your business rules, not the skeleton of the application.

**Key insights:**
- Controllers translate HTTP into Use Case input; Presenters translate Use Case output into view models
- Gateways implement repository interfaces defined by Use Cases — the inner circle defines the contract, the outer fulfills it
- Business rules never know whether data lives in SQL, NoSQL, or flat files, or that delivery is HTTP
- Treat frameworks with suspicion — they want you to couple to them; keep them at arm's length

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Controller** | Delivery mechanism → Use Case input | `OrderController.create(req)` builds `CreateOrderRequest`, calls Interactor |
| **Presenter** | Use Case output → view model | `OrderPresenter.present(response)` formats for JSON/HTML |
| **Gateway** | Repository interface implemented per DB | `SqlOrderRepository implements OrderRepository` |
| **Framework boundary** | Framework calls inward, never the reverse | Express route handler calls Controller; Controller never imports Express |

See [references/adapters-frameworks.md](references/adapters-frameworks.md) when wiring controllers, presenters, or gateways, or arguing that the database/web is a detail — covers plugin architecture and how to confine a framework to the edges.

### 4. Component Principles

**Core concept:** Components are the units of deployment. Three cohesion principles govern what goes inside a component; three coupling principles govern relationships between components.

**Why it works:** Poorly composed components create ripple effects where one change forces redeployment of unrelated code; the principles keep changes localized and releases independent.

**Key insights:**
- REP (Reuse/Release Equivalence): classes in a component must be versionable and releasable as a unit
- CCP (Common Closure): classes that change for the same reason at the same time belong together — SRP for components
- CRP (Common Reuse): don't force users to depend on classes they don't use
- ADP (Acyclic Dependencies): the component graph must have no cycles — break them with DIP or a new component
- SDP (Stable Dependencies): depend in the direction of stability
- SAP (Stable Abstractions): stable components should be abstract; unstable ones concrete

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Component grouping** | Group classes that change together (CCP) | All order-related Use Cases in one component |
| **Breaking cycles** | Apply DIP to invert a dependency edge | Extract an interface into a new component to break the cycle |
| **Stability metrics** | Instability I = Ce / (Ca + Ce) | Many incoming, no outgoing deps → I near 0 (stable) |

See [references/component-principles.md](references/component-principles.md) when grouping classes into deployable components or breaking a dependency cycle — each of REP, CCP, CRP, ADP, SDP, SAP worked through with the instability metric.

### 5. SOLID Principles

**Core concept:** Five class-and-module-level principles — Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion — the mid-level building blocks that make the Dependency Rule possible.

**Why it works:** Each principle addresses a specific way dependencies go wrong, preventing the rigidity, fragility, and immobility that turn codebases into legacy nightmares.

**Key insights:**
- SRP: a module has one reason to change — it serves one actor (not "does one thing")
- OCP: extend behavior by adding new code, not modifying existing code — strategy and plugin patterns
- LSP: subtypes must be usable through the base interface without the client knowing — violated by unexpected exceptions or ignored methods
- ISP: clients should not depend on methods they don't use — fat interfaces create needless coupling
- DIP: high-level modules and low-level modules both depend on abstractions defined by the high-level module

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **SRP violation** | Class serves multiple actors | `Employee` handles pay (CFO), reporting (COO), persistence (CTO) |
| **OCP via strategy** | New behavior through new classes | Add `ExpressShipping` implementing `ShippingStrategy`; `Order` untouched |
| **LSP violation** | Subtype changes expected behavior | `Square extends Rectangle` breaks the `setWidth()`/`setHeight()` contract |
| **ISP application** | Split fat interfaces into role interfaces | `Printer`, `Scanner`, `Fax` instead of one `MultiFunctionDevice` |
| **DIP wiring** | High-level defines interface; low-level implements | `OrderService` depends on `PaymentGateway`, not `StripeClient` |

See [references/solid-principles.md](references/solid-principles.md) when applying SRP/OCP/LSP/ISP/DIP to a specific class or diagnosing a violation — each principle worked through with code examples and the smell it prevents.

### 6. Boundaries and Boundary Anatomy

**Core concept:** A boundary is a line between things that matter and things that are details, implemented through polymorphism: dependencies cross pointing inward while control flow may cross either way.

**Why it works:** Every boundary buys the option to defer a decision or swap an implementation; strategic boundary placement determines whether a system is a joy or a pain to maintain over years.

**Key insights:**
- Full boundaries use reciprocal interfaces on both sides; partial boundaries use a simpler strategy or facade
- Humble Object pattern: split boundary code into a hard-to-test part (close to the boundary) and an easy-to-test part (the logic)
- Services are not automatically architectural boundaries — a microservice with a fat shared data model is a monolith with network calls
- Tests are the most isolated component: they depend inward, nothing depends on them
- Premature boundaries are expensive, but so are missing ones — draw them at points of likely volatility

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Full vs. partial boundary** | Reciprocal ports, or a lone strategy | Use Case defines `PlaceOrderInput`/`PlaceOrderOutput`; simpler cases take a `ShippingStrategy` |
| **Humble Object** | Separate testable logic from infrastructure | `PresenterLogic` (testable) produces `ViewModel`; `View` (humble) renders it |
| **Main as plugin** | Composition root assembles the system | `main()` wires all concrete implementations and starts the app |

See [references/boundaries.md](references/boundaries.md) when deciding where to draw a boundary, choosing full vs. partial, or applying the Humble Object pattern — also covers services as boundaries, test boundaries, and Main as the ultimate plugin.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| **ORM leaking into business logic** | Entities couple to the schema; DB changes rewrite business rules | Separate domain entities from persistence models; map at the adapter layer |
| **Business rules in controllers** | Untestable without HTTP; duplicated across endpoints | Move logic into Use Case Interactors; controllers only translate and delegate |
| **Framework-first architecture** | Framework dictates structure; swapping means a rewrite | Treat the framework as a plugin; structure code by business capability |
| **Circular component dependencies** | Changes ripple unpredictably; no independent releases | Apply DIP or extract a shared abstraction component |
| **One giant Use Case per feature** | Bloated thousand-line orchestrators | Split into focused single-operation Use Cases |
| **Skipping boundaries "because it's simple"** | Coupling accumulates silently until the cost is enormous | Draw boundaries proactively at points of likely volatility |
| **Microservices as automatic good architecture** | A distributed monolith is worse than a clean monolith | Apply the Dependency Rule within and across services; services are deployment boundaries, not architectural ones |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you test business rules without DB, web server, or framework? | Rules coupled to infrastructure | Extract entities and use cases behind interfaces; mock outer layers |
| Do all source dependencies point inward? | Dependency Rule violated | Introduce boundary interfaces; invert the offending dependency |
| Can you swap the database without touching business logic? | Persistence leaking inward | Repository pattern; isolate persistence in adapters |
| Are Use Cases independent of delivery mechanism? | Use Cases know HTTP/CLI/queues | Use plain DTOs in Use Case signatures |
| Is the framework confined to the outermost circle? | Framework is your architecture | Wrap framework calls behind interfaces; push to the edges |
| Is the component graph cycle-free? | Circular dependencies exist | Apply ADP: DIP or new components to break every cycle |
| Does Main (composition root) wire all dependencies? | Concrete classes instantiated in inner circles | Move construction to Main; use DI or factories |

## Further Reading

Based on Robert C. Martin's definitive guide to software architecture:

- [*"Clean Architecture: A Craftsman's Guide to Software Structure and Design"*](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164?tag=wondelai00-20) by Robert C. Martin

## About the Author

**Robert C. Martin ("Uncle Bob")** is a software engineer programming since 1970, a founding signatory of the Agile Manifesto, and the author of *Clean Code*, *The Clean Coder*, *Clean Architecture*, and *Clean Agile*. His SOLID principles are foundational vocabulary in object-oriented design, and his work argues that architecture is about managing dependencies and keeping business rules independent of infrastructure details.
