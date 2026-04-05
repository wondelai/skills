---
name: clean-architecture
description: 'Structure software around the Dependency Rule: source code dependencies point inward from frameworks to use cases to entities. Use when the user mentions "architecture layers", "dependency rule", "ports and adapters", "hexagonal architecture", "use case boundary", "onion architecture", "screaming architecture", or "framework independence". Also trigger when decoupling business logic from databases or frameworks, defining module boundaries, or debating where to put business rules. Covers component principles, boundaries, and SOLID. For code quality, see clean-code. For domain modeling, see domain-driven-design.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Clean Architecture Framework

A disciplined approach to structuring software so that business rules remain independent of frameworks, databases, and delivery mechanisms. Apply these principles when designing system architecture, reviewing module boundaries, or advising on dependency management.

## Core Principle

**Source code dependencies must point inward -- toward higher-level policies.** Nothing in an inner circle can know anything about something in an outer circle. This single rule, applied consistently, produces systems that are testable, independent of frameworks, independent of the UI, independent of the database, and independent of any external agency.

**The foundation:** Software architecture is about drawing lines -- boundaries -- that separate things that matter from things that are details. Business rules are what matter. Databases, web frameworks, and delivery mechanisms are details. When details depend on policies (not the other way around), you can defer decisions, swap implementations, and test business logic in isolation.

## Scoring

**Goal: 10/10.** When reviewing or creating software architecture, rate it 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## The Clean Architecture Framework

Six principles for building systems that survive the passage of time:

### 1. Dependency Rule and Concentric Circles

**Core concept:** The architecture is organized as concentric circles. The innermost circle contains Entities (enterprise business rules). The next circle contains Use Cases (application business rules). Then Interface Adapters. The outermost circle contains Frameworks and Drivers. Source code dependencies always point inward.

**Why it works:** When high-level policies don't depend on low-level details, you can change the database from MySQL to MongoDB, swap a web framework, or replace a REST API with GraphQL -- all without touching business logic. The system becomes resilient to the most volatile parts of the technology stack.

**Key insights:**
- The Dependency Rule is the overriding rule: inner circles cannot mention outer circle names (classes, functions, variables, data formats)
- Data that crosses boundaries must be in a form convenient for the inner circle, never in a form dictated by the outer circle
- Dependency Inversion (interfaces defined inward, implemented outward) is the mechanism that enforces the rule
- The number of circles is not fixed -- four is typical, but you may have more; the rule stays the same
- Frameworks are details, not architecture -- they belong in the outermost circle

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Layer direction** | Inner circles define interfaces; outer circles implement them | `UserRepository` interface in Use Cases; `PostgresUserRepository` in Adapters |
| **Data crossing** | DTOs or simple structs cross boundaries, not ORM entities | Use Case returns `UserResponse` DTO, not an ActiveRecord model |
| **Framework isolation** | Wrap framework calls behind interfaces | `EmailSender` interface hides whether you use SendGrid or SES |
| **Database independence** | Repository pattern abstracts persistence | Business logic calls `repo.save(user)`, never raw SQL |
| **Dependency direction** | Import arrows on a diagram always point inward | Controller imports Use Case; Use Case never imports Controller |

See: [references/dependency-rule.md](references/dependency-rule.md)

### 2. Entities and Use Cases

**Core concept:** Entities encapsulate enterprise-wide business rules -- the most general, highest-level rules that would exist even if no software system existed. Use Cases contain application-specific business rules that orchestrate the flow of data to and from Entities.

**Why it works:** By separating what the business does (Entities) from how the application orchestrates it (Use Cases), you can reuse Entities across multiple applications and change application behavior without altering core business rules.

**Key insights:**
- Entities are not database rows -- they are objects (or pure functions) that encapsulate critical business rules and data
- Use Cases describe application-specific automation rules; they orchestrate Entities but do not contain enterprise logic
- Use Cases accept Request Models and return Response Models -- never framework objects
- Each Use Case represents a single application operation (e.g., `CreateOrder`, `ApproveExpense`)
- The Interactor pattern: a Use Case class implements an input boundary interface and calls an output boundary interface
- Changes to a Use Case should never affect an Entity; changes to an Entity may require Use Case updates

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Entity design** | Encapsulate critical business rules with no framework dependencies | `Order.calculateTotal()` applies tax rules; knows nothing about HTTP |
| **Use Case boundary** | Define Input Port and Output Port interfaces | `CreateOrderInput` interface; `CreateOrderOutput` interface |
| **Request/Response** | Simple data structures cross the boundary | `CreateOrderRequest { items, customerId }` -- no ORM models |
| **Single responsibility** | One Use Case per application operation | `PlaceOrder`, `CancelOrder`, `RefundOrder` as separate classes |
| **Interactor** | Use Case class implements Input Port, calls Output Port | `PlaceOrderInteractor implements PlaceOrderInput` |

See: [references/entities-use-cases.md](references/entities-use-cases.md)

### 3. Interface Adapters and Frameworks

**Core concept:** Interface Adapters convert data between the format most convenient for Use Cases and Entities and the format required by external agencies (database, web, devices). Frameworks and Drivers are the outermost layer -- glue code that connects to the outside world.

**Why it works:** When the web framework, ORM, or message queue is confined to the outermost circles, replacing any of them becomes a localized change. The database is a detail. The web is a detail. The framework is a detail. Details should be plugins to your business rules, not the skeleton of your application.

**Key insights:**
- Controllers translate HTTP requests into Use Case input; Presenters translate Use Case output into view models
- Gateways implement repository interfaces defined by Use Cases -- the Use Case defines the contract, the gateway fulfills it
- The database is a detail: business rules don't need to know whether data is stored in SQL, NoSQL, or flat files
- The web is a detail: business rules don't know they're being delivered over HTTP
- Treat frameworks with suspicion -- they want you to couple to them; keep them at arm's length
- Plugin architecture: the system should be structured so that frameworks plug into business rules, not the reverse

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Controller** | Translates delivery mechanism to Use Case input | `OrderController.create(req)` builds `CreateOrderRequest` and calls Interactor |
| **Presenter** | Translates Use Case output to view model | `OrderPresenter.present(response)` formats data for JSON/HTML |
| **Gateway** | Implements repository interface using a specific DB | `SqlOrderRepository implements OrderRepository` |
| **Framework boundary** | Framework code calls inward, never called by inner circles | Express route handler calls Controller; Controller never imports Express |
| **Plugin architecture** | Main component wires dependencies at startup | `main()` instantiates concrete classes and injects them |

See: [references/adapters-frameworks.md](references/adapters-frameworks.md)

### 4. Component Principles

**Core concept:** Components are the units of deployment. Three cohesion principles govern what goes inside a component; three coupling principles govern relationships between components. Together they determine a system's releasability, maintainability, and stability.

**Why it works:** Poorly composed components create ripple effects: one change forces redeployment of unrelated code. The cohesion and coupling principles provide a systematic way to group classes and manage inter-component dependencies so that changes remain localized.

**Key insights:**
- REP (Reuse/Release Equivalence): classes in a component should be releasable together -- if you can't version and release them as a unit, they don't belong together
- CCP (Common Closure): classes that change for the same reason at the same time belong in the same component (SRP for components)
- CRP (Common Reuse): don't force users to depend on things they don't use -- if you must import a component, you should need most of its classes
- ADP (Acyclic Dependencies): the dependency graph of components must have no cycles; break cycles with DIP or by extracting a new component
- SDP (Stable Dependencies): depend in the direction of stability -- a component with many dependents should be hard to change
- SAP (Stable Abstractions): stable components should be abstract; unstable components should be concrete

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Component grouping** | Group classes that change together (CCP) | All order-related Use Cases in one component |
| **Breaking cycles** | Apply DIP to invert a dependency edge | Extract an interface into a new component to break a circular dependency |
| **Stability metrics** | Measure instability: I = Ce / (Ca + Ce) | A component with many incoming and no outgoing deps has I near 0 (stable) |
| **Abstractness balance** | Stable components should contain mostly interfaces | Core domain component is abstract; adapter component is concrete |
| **Release granularity** | Version and release components independently | `order-domain v2.1.0` released without touching `payment-adapter` |

See: [references/component-principles.md](references/component-principles.md)

### 5. SOLID Principles

**Core concept:** Five principles for managing dependencies at the class and module level: Single Responsibility (SRP), Open-Closed (OCP), Liskov Substitution (LSP), Interface Segregation (ISP), and Dependency Inversion (DIP). They are the mid-level building blocks that make the Dependency Rule possible.

**Why it works:** SOLID principles keep source code flexible, understandable, and amenable to change. They prevent the rigidity, fragility, and immobility that turn codebases into legacy nightmares. Each principle addresses a specific way that dependencies can go wrong.

**Key insights:**
- SRP: a module should have one, and only one, reason to change -- it serves one actor (not "does one thing")
- OCP: extend behavior by adding new code, not by modifying existing code; strategy and plugin patterns are the mechanism
- LSP: subtypes must be usable through the base type interface without the client knowing the difference; violated when subclass throws unexpected exceptions or ignores methods
- ISP: clients should not be forced to depend on methods they do not use; fat interfaces create unnecessary coupling
- DIP: high-level modules should not depend on low-level modules; both should depend on abstractions defined by the high-level module

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **SRP violation** | Class serves multiple actors | `Employee` handles pay calculation (CFO), reporting (COO), and persistence (CTO) |
| **OCP via strategy** | New behavior through new classes, not edits | Add `ExpressShipping` class implementing `ShippingStrategy`, no changes to `Order` |
| **LSP violation** | Subtype changes expected behavior | `Square extends Rectangle` breaks `setWidth()`/`setHeight()` contract |
| **ISP application** | Split fat interfaces into role interfaces | `Printer`, `Scanner`, `Fax` instead of one `MultiFunctionDevice` |
| **DIP wiring** | High-level defines interface; low-level implements | `OrderService` depends on `PaymentGateway` interface, not `StripeClient` |

See: [references/solid-principles.md](references/solid-principles.md)

### 6. Boundaries and Boundary Anatomy

**Core concept:** A boundary is a line drawn between things that matter and things that are details. Boundaries are implemented through polymorphism: source code dependencies cross the boundary pointing inward, while the flow of control may cross in either direction. The Humble Object pattern makes code at boundaries testable.

**Why it works:** Every boundary you draw gives you the option to defer a decision or swap an implementation. Boundaries separate the volatile from the stable, the concrete from the abstract. Early and strategic boundary placement determines whether a system is a joy or a pain to maintain over years.

**Key insights:**
- Full boundaries use reciprocal interfaces on both sides; partial boundaries use a simpler strategy pattern or facade
- The Humble Object pattern: split behavior at a boundary into two classes -- one hard to test (close to the boundary) and one easy to test (contains the logic)
- Services are not inherently architectural boundaries -- a microservice with a fat shared data model is just a monolith with network calls
- The Main component is a plugin: it creates all factories, strategies, and dependencies, then hands control to the high-level policy
- Test boundaries: tests are the most isolated component; they always depend inward and nothing depends on them
- Premature boundaries are expensive, but so are missing boundaries -- draw them when the cost of crossing is less than the cost of not having them

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Full boundary** | Input/Output port interfaces on both sides | Use Case defines both `PlaceOrderInput` and `PlaceOrderOutput` |
| **Partial boundary** | Strategy or Facade without full reciprocal interfaces | `ShippingCalculator` accepts a `ShippingStrategy` -- simpler than full ports |
| **Humble Object** | Separate testable logic from hard-to-test infrastructure | `PresenterLogic` (testable) produces `ViewModel`; `View` (humble) renders it |
| **Main as plugin** | Composition root assembles the system | `main()` wires all concrete implementations and starts the app |
| **Test boundary** | Tests depend on source; source never depends on tests | Test imports `PlaceOrderInteractor`; production code never imports test code |

See: [references/boundaries.md](references/boundaries.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| **Letting the ORM leak into business logic** | Entities become coupled to the database schema; changing the DB means rewriting business rules | Separate domain entities from persistence models; map between them at the adapter layer |
| **Putting business rules in controllers** | Logic becomes untestable without spinning up HTTP; duplication across endpoints | Move all business logic into Use Case Interactors; controllers only translate and delegate |
| **Framework-first architecture** | The framework dictates folder structure and dependency flow; swapping frameworks means a rewrite | Treat the framework as a plugin in the outermost circle; structure code by business capability |
| **Circular dependencies between components** | Changes ripple unpredictably; impossible to release independently | Apply DIP to break cycles or extract a shared abstraction component |
| **One giant Use Case per feature** | Use Cases become bloated orchestrators with thousands of lines | Split into focused Use Cases with single application operations |
| **Skipping boundaries "because it's simple"** | Coupling accumulates silently; by the time you need a boundary, the cost is enormous | Draw boundaries proactively at points of likely volatility |
| **Treating microservices as automatic good architecture** | A distributed monolith with shared databases and tight coupling is worse than a well-structured monolith | Apply the Dependency Rule within and across services; services are deployment boundaries, not architectural ones |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you test business rules without a database, web server, or framework? | Business rules are coupled to infrastructure | Extract entities and use cases behind interfaces; mock the outer layers |
| Do source code dependencies point inward on every import? | The Dependency Rule is violated | Introduce interfaces at the boundary; invert the offending dependency |
| Can you swap the database without changing business logic? | Persistence is leaking inward | Implement the Repository pattern; isolate persistence in adapters |
| Are Use Cases independent of the delivery mechanism? | Use Cases know about HTTP, CLI, or message queues | Remove delivery-specific types from Use Case signatures; use plain DTOs |
| Is the framework confined to the outermost circle? | The framework is your architecture instead of a detail | Wrap framework calls behind interfaces; push framework code to the edges |
| Can you identify the component dependency graph and confirm it has no cycles? | Circular dependencies exist | Apply ADP: use DIP or extract new components to break every cycle |
| Does Main (or the composition root) wire all dependencies? | Concrete classes are instantiated in inner circles | Move all construction logic to Main; use dependency injection or factories |

## Reference Files

- [dependency-rule.md](references/dependency-rule.md): The Dependency Rule explained, concentric circles, data crossing boundaries, keeping the inner circle pure
- [entities-use-cases.md](references/entities-use-cases.md): Enterprise Business Rules, Application Business Rules, the Interactor pattern, request/response models
- [adapters-frameworks.md](references/adapters-frameworks.md): Interface adapters, frameworks as details, database as a detail, plugin architecture
- [component-principles.md](references/component-principles.md): REP, CCP, CRP, ADP, SDP, SAP -- component cohesion and coupling
- [solid-principles.md](references/solid-principles.md): SRP, OCP, LSP, ISP, DIP with code examples and common violations
- [boundaries.md](references/boundaries.md): Boundary anatomy, Humble Object pattern, partial boundaries, Main as a plugin, test boundaries

## Further Reading

This skill is based on Robert C. Martin's definitive guide to software architecture. For the complete methodology with detailed examples and case studies:

- [*"Clean Architecture: A Craftsman's Guide to Software Structure and Design"*](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164?tag=wondelai00-20) by Robert C. Martin

## About the Author

**Robert C. Martin ("Uncle Bob")** is a software engineer, author, and one of the founding signatories of the Agile Manifesto. He has been programming since 1970 and has consulted for and trained development teams worldwide. Martin is the author of *Clean Code*, *The Clean Coder*, *Clean Architecture*, and *Clean Agile*, among other books. He is the founder of Uncle Bob Consulting LLC and cleancoder.com. His SOLID principles have become foundational vocabulary in object-oriented design, and his advocacy for craftsmanship and discipline in software development has influenced generations of programmers. Martin's work consistently argues that software architecture is about managing dependencies, drawing boundaries, and keeping business rules independent of delivery mechanisms and infrastructure details.
