---
name: domain-driven-design
description: 'Model software around the business domain using bounded contexts, aggregates, and ubiquitous language. Use when the user mentions "domain modeling", "bounded context", "aggregate root", "ubiquitous language", or "anti-corruption layer". Covers entities vs value objects, domain events, and context mapping strategies. For architecture layers, see clean-architecture. For complexity, see software-design-philosophy.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.1"
---

# Domain-Driven Design Framework

Framework for tackling software complexity by modeling code around the business domain. Based on a fundamental truth: the greatest risk in software is not technical failure -- it is building a model that does not reflect how the business actually works.

## Core Principle

**The model is the code; the code is the model.** Software should embody a deep, shared understanding of the business domain. When domain experts and developers speak the same language and that language is directly expressed in the codebase, complexity becomes manageable, requirements are captured precisely, and the system evolves gracefully as the business changes.

## Scoring

**Goal: 10/10.** When reviewing or creating domain models, rate them 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## Framework

### 1. Ubiquitous Language

**Core concept:** A shared, rigorous language between developers and domain experts that is used consistently in conversation, documentation, and code. When the language changes, the code changes. When the code reveals awkward naming, the language is refined.

**Why it works:** Ambiguity is the root cause of most modeling failures. When a developer says "order" and a domain expert means "purchase request," bugs are inevitable. A ubiquitous language forces alignment so that every class, method, and variable name maps to a concept the business recognizes and validates.

**Key insights:**
- The language is not a glossary bolted on after the fact -- it emerges from deep collaboration
- If a concept is hard to name, the model is likely wrong; naming difficulty is a design signal
- Code that uses technical jargon instead of domain terms (e.g., `DataProcessor` vs. `ClaimAdjudicator`) hides domain logic
- Language must be enforced in code: class names, method names, event names, module names
- Different bounded contexts may use the same word with different meanings -- and that is fine

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Class naming | Name classes after domain concepts | `LoanApplication`, not `RequestHandler` |
| Method naming | Use verbs the business uses | `policy.underwrite()`, not `policy.process()` |
| Event naming | Past-tense domain actions | `ClaimSubmitted`, not `DataSaved` |
| Module structure | Organize by domain concept | `shipping/`, `billing/`, not `controllers/`, `services/` |
| Code review | Reject technical-only names | Flag `Manager`, `Helper`, `Processor`, `Utils` as naming smells |

See: [references/ubiquitous-language.md](references/ubiquitous-language.md)

### 2. Bounded Contexts and Context Mapping

**Core concept:** A bounded context is an explicit boundary within which a particular domain model is defined and applicable. The same word (e.g., "Customer") can mean different things in different contexts. Context maps define the relationships and translation strategies between bounded contexts.

**Why it works:** Large systems that try to maintain a single unified model inevitably collapse into inconsistency. Bounded contexts accept that different parts of the business have different models and make the boundaries explicit. Context maps then manage integration so that each context preserves its internal consistency.

**Key insights:**
- A bounded context is not a microservice -- it is a linguistic and model boundary that may contain multiple services
- Context boundaries often align with team boundaries (Conway's Law)
- The nine context mapping patterns describe political and technical relationships between teams
- Anti-Corruption Layer is the most important defensive pattern -- never let a foreign model leak into your core domain
- Shared Kernel is dangerous: it couples two teams and should be small and explicitly governed
- Start by mapping what exists (Big Ball of Mud), then define target boundaries

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Service integration | Anti-Corruption Layer | Translate external API responses into your domain objects at the boundary |
| Team collaboration | Shared Kernel | Two teams co-own a small `Money` value object library |
| Legacy migration | Conformist / ACL | Wrap legacy system behind an adapter that speaks your domain language |
| API design | Open Host Service + Published Language | Expose a well-documented REST API with a canonical schema |
| Module boundaries | Separate packages per context | `myapp.shipping` and `myapp.billing` packages with explicit translation |

See: [references/bounded-contexts.md](references/bounded-contexts.md)

### 3. Entities, Value Objects, and Aggregates

**Core concept:** Entities have identity that persists across state changes. Value Objects are defined entirely by their attributes and are immutable. Aggregates are clusters of entities and value objects with a single root entity that enforces consistency boundaries.

**Why it works:** Without these distinctions, systems treat everything as a mutable, identity-bearing object with database-level relationships, leading to tangled state, inconsistent updates, and fragile concurrency. Aggregates draw a consistency boundary: everything inside is guaranteed consistent; everything outside is eventually consistent.

**Key insights:**
- Entity: "Am I the same thing even if all my attributes change?" (a person changes name, address, job -- still the same person)
- Value Object: "Am I defined only by my attributes?" (a $10 bill is interchangeable with any other $10 bill)
- Most things in a domain model should be Value Objects, not Entities -- prefer immutability
- Aggregate Root is the single entry point: external objects may only hold references to the root
- Keep aggregates small -- one root entity plus a minimal cluster of closely related objects
- Reference other aggregates by ID, not by direct object reference
- Design for eventual consistency between aggregates; immediate consistency only within an aggregate

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Identity tracking | Entity with ID | `Order` identified by `orderId`, survives state changes |
| Immutable attributes | Value Object | `Address(street, city, zip)` -- replace, never mutate |
| Consistency boundary | Aggregate Root | `Order` is root; `OrderLine` items exist only through it |
| Cross-aggregate reference | Reference by ID | `Order` stores `customerId`, not a `Customer` object |
| Concurrency control | Optimistic locking on root | Version field on `Order`; conflict if two edits race |

See: [references/building-blocks.md](references/building-blocks.md)

### 4. Domain Events

**Core concept:** A domain event captures something that happened in the domain that domain experts care about. Events are named in past tense (`OrderPlaced`, `PaymentReceived`) and represent facts that have already occurred.

**Why it works:** Domain events decouple the cause from the effect. When `OrderPlaced` is published, the shipping context, billing context, and notification context can each react independently without the ordering context knowing about any of them. This reduces coupling, enables eventual consistency, and creates a natural audit trail.

**Key insights:**
- Name events in past tense: something that happened, not something that should happen
- Events are immutable facts -- once published, they cannot be changed or retracted
- Domain events differ from integration events: domain events are internal to a bounded context; integration events cross boundaries
- Events enable temporal decoupling: the producer does not wait for the consumer
- Event sourcing stores the full history of events as the source of truth, deriving current state by replaying them
- Not every state change needs an event -- only publish events that the domain cares about

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| State transitions | Raise event on domain action | `order.place()` raises `OrderPlaced` event |
| Cross-context integration | Publish integration event | `OrderPlaced` triggers `ShippingLabelRequested` in shipping context |
| Audit trail | Store events as history | Event log: `OrderPlaced` -> `PaymentReceived` -> `OrderShipped` |
| Eventual consistency | Async event handlers | `InventoryReserved` handler updates stock asynchronously after `OrderPlaced` |
| Event sourcing | Rebuild state from events | Replay all `Account*` events to derive current account balance |

See: [references/domain-events.md](references/domain-events.md)

### 5. Repositories and Factories

**Core concept:** Repositories provide the illusion of an in-memory collection of domain objects, hiding persistence details. Factories encapsulate complex object creation logic, ensuring that aggregates are always created in a valid state.

**Why it works:** Domain logic should never depend on how objects are stored or constructed. Repositories abstract away SQL, ORMs, and data access so that domain code reads like business logic. Factories ensure that invariants are satisfied from the moment an aggregate is born, preventing invalid objects from ever existing.

**Key insights:**
- A Repository interface belongs in the domain layer; its implementation belongs in infrastructure
- Repository methods should speak the ubiquitous language: `findPendingOrders()`, not `getByStatusCode(3)`
- Collection-oriented repositories mimic `add`/`remove`; persistence-oriented repositories use `save`
- Factories are warranted when object creation involves complex rules, conditional logic, or assembling multiple parts
- Simple creation (a Value Object with two fields) does not need a factory -- a constructor suffices
- The Specification pattern encapsulates query criteria as domain objects: `OverdueInvoiceSpecification`

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Data access abstraction | Repository interface | `OrderRepository.findByCustomer(customerId)` in domain layer |
| Complex creation | Factory method | `Order.createFromQuote(quote)` validates and assembles from a `Quote` aggregate |
| Query encapsulation | Specification | `spec = OverdueBy(days=30); repo.findMatching(spec)` |
| Reconstitution | Repository loads aggregate | Repository assembles `Order` + `OrderLines` from DB rows into a complete aggregate |
| Ports and adapters | Interface in domain, impl in infra | `interface OrderRepository` in domain; `PostgresOrderRepository` in infrastructure |

See: [references/repositories-factories.md](references/repositories-factories.md)

### 6. Strategic Design and Distillation

**Core concept:** Not all parts of a system are equally important. Strategic design identifies the Core Domain -- the part that provides competitive advantage -- and distinguishes it from Supporting Subdomains (necessary but not differentiating) and Generic Subdomains (commodity, buy or use off-the-shelf).

**Why it works:** Teams that apply the same rigor to every module spread their best talent thin and over-engineer commodity functionality. By identifying the Core Domain, organizations invest their best developers, deepest modeling, and most careful design where it matters most, while using simpler approaches or third-party solutions elsewhere.

**Key insights:**
- Core Domain: where competitive advantage lives; invest your best people and deepest modeling here
- Supporting Subdomain: necessary for the business but not a differentiator; build it, but don't over-engineer
- Generic Subdomain: commodity functionality (authentication, email, payments); buy or use open-source
- Domain distillation extracts and highlights the Core Domain from the surrounding complexity
- A Domain Vision Statement is a short document (one page) describing the Core Domain's value proposition
- The Highlighted Core marks the most critical parts of the model so they receive the most attention
- Revisit what is "core" as the business evolves -- today's differentiator may become tomorrow's commodity

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Build vs. buy decision | Classify subdomain type | Build custom pricing engine (core); use Stripe for payments (generic) |
| Team allocation | Best developers on Core Domain | Senior engineers model the underwriting rules; juniors integrate the email service |
| Code organization | Separate core from generic | `domain/pricing/` (deep model) vs. `infrastructure/email/` (thin adapter) |
| Simplification | Distill core concepts | Extract a `PolicyRatingEngine` from a monolithic `InsuranceService` |
| Documentation | Domain Vision Statement | One-page doc: "Our competitive advantage is real-time risk scoring using..." |

See: [references/strategic-design.md](references/strategic-design.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Using technical names instead of domain language | Domain logic is hidden behind `DataManager` and `ProcessorService`; experts cannot validate the model | Rename to domain terms: `ClaimAdjudicator`, `PolicyUnderwriter`; if no domain term exists, the concept may be wrong |
| One model to rule them all | A single `Customer` class serving billing, shipping, and marketing becomes bloated and contradictory | Define bounded contexts; each context gets its own `Customer` model with only the attributes it needs |
| Giant aggregates with many nested entities | Concurrency conflicts, slow loads, transactional bottlenecks | Keep aggregates small; reference other aggregates by ID; use eventual consistency between aggregates |
| Anemic domain model (all logic in services) | Domain objects are data bags; business rules scatter across service classes; duplication and inconsistency | Move behavior into entities and value objects; services only orchestrate, never contain domain logic |
| No Anti-Corruption Layer at integration points | Foreign models leak into your domain; your code becomes coupled to external schemas and naming | Wrap every external system behind a translation layer that converts to your ubiquitous language |
| Treating bounded contexts as microservices | Premature service extraction; distributed system complexity without the benefit | A bounded context is a model boundary, not a deployment unit; start with modules in a monolith |
| Skipping domain expert collaboration | Developers invent a model that does not match business reality; expensive rework | Regular modeling sessions with domain experts; refine the model until experts say "yes, that is how it works" |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can a domain expert read your class names and understand them? | Code uses technical jargon instead of domain language | Rename classes, methods, and events to use ubiquitous language |
| Are bounded context boundaries explicitly defined? | Models bleed across boundaries; the same term means different things | Draw a context map; define explicit boundaries and translation strategies |
| Are aggregates small (one root + minimal cluster)? | Aggregates are large, slow, and have concurrency issues | Break into smaller aggregates; reference by ID; accept eventual consistency |
| Do domain objects contain behavior, not just data? | Anemic model; logic scattered in service classes | Move business rules into entities and value objects |
| Are domain events used for cross-aggregate communication? | Tight coupling between aggregates; synchronous chains | Introduce domain events; let aggregates react to events asynchronously |
| Is there an Anti-Corruption Layer at every external integration? | Foreign models pollute your domain | Add a translation layer at each integration boundary |
| Have you identified which subdomain is core? | Equal effort on everything; best talent spread thin | Classify subdomains; focus deep modeling on the Core Domain |

## Reference Files

- [ubiquitous-language.md](references/ubiquitous-language.md): Building a shared language, glossary maintenance, naming in code, language evolution
- [bounded-contexts.md](references/bounded-contexts.md): Context boundaries, nine mapping patterns, team relationships, integration strategies
- [building-blocks.md](references/building-blocks.md): Entities, Value Objects, Aggregates, aggregate design rules, consistency boundaries
- [domain-events.md](references/domain-events.md): Event naming, event sourcing, event-driven architecture, integration events
- [repositories-factories.md](references/repositories-factories.md): Repository pattern, Factory pattern, Specification pattern, ports and adapters
- [strategic-design.md](references/strategic-design.md): Core Domain, Generic and Supporting Subdomains, distillation, build vs. buy

## Further Reading

This skill is based on the Domain-Driven Design methodology developed by Eric Evans. For the complete methodology, patterns, and deeper insights, read the original book:

- [*"Domain-Driven Design: Tackling Complexity in the Heart of Software"*](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215?tag=wondelai00-20) by Eric Evans

## About the Author

Eric Evans is a software design consultant and the originator of Domain-Driven Design. He has worked on large-scale systems in industries including finance, insurance, and logistics, where he developed the patterns and practices that became DDD. His 2003 book *Domain-Driven Design: Tackling Complexity in the Heart of Software* is widely regarded as one of the most influential software architecture books ever written. Evans founded Domain Language, a consulting firm that helps teams apply DDD to complex software projects. He is a frequent keynote speaker at software conferences worldwide and continues to refine and evolve DDD concepts through workshops, community engagement, and collaboration with practitioners. His work has shaped modern approaches to microservices, event sourcing, and strategic software design.
