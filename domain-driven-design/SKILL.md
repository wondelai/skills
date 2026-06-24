---
name: domain-driven-design
description: 'Model software around the business domain using bounded contexts, aggregates, and ubiquitous language. Use when the user mentions "domain modeling", "bounded context", "aggregate root", "ubiquitous language", "anti-corruption layer", "context mapping", "domain events", "strategic design", "model the business in code", "the code doesnt match the business", or "how do we split this big system". Also trigger when breaking a monolith into services, defining service boundaries, or aligning code structure with business processes. Covers entities vs value objects, domain events, and context mapping strategies. For architecture layers, see clean-architecture. For complexity, see software-design-philosophy.'
license: MIT
metadata:
  author: wondelai
  version: "1.3.0"
---

# Domain-Driven Design Framework

Framework for tackling software complexity by modeling code around the business domain. The greatest risk in software is not technical failure -- it is building a model that does not reflect how the business actually works.

## Core Principle

**The model is the code; the code is the model.** Software should embody a deep, shared understanding of the business domain. When domain experts and developers speak the same language and that language is directly expressed in the codebase, complexity becomes manageable and the system evolves gracefully as the business changes.

## Scoring

**Goal: 10/10.** Rate any domain model 0-10 against the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps. Report the current score and the specific improvements needed to reach 10/10.

## Framework

### 1. Ubiquitous Language

**Core concept:** A shared, rigorous language between developers and domain experts, used consistently in conversation, documentation, and code. When the language changes, the code changes -- and awkward naming in code feeds back into refining the language.

**Why it works:** Ambiguity is the root cause of most modeling failures. When a developer says "order" and an expert means "purchase request," bugs are inevitable; a ubiquitous language forces every name in code to map to a concept the business recognizes and validates.

**Key insights:**
- The language emerges from deep collaboration, not a glossary bolted on after the fact
- If a concept is hard to name, the model is likely wrong -- naming difficulty is a design signal
- Technical jargon (`DataProcessor` vs. `ClaimAdjudicator`) hides domain logic from the experts who could correct it
- Different bounded contexts may use the same word with different meanings -- and that is fine

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Class/method naming | Name after domain concepts and verbs | `LoanApplication`, `policy.underwrite()` -- not `RequestHandler`, `process()` |
| Module structure | Organize by domain concept | `shipping/`, `billing/` -- not `controllers/`, `services/` |
| Code review | Reject technical-only names | Flag `Manager`, `Helper`, `Processor`, `Utils` as naming smells |

See: [references/ubiquitous-language.md](references/ubiquitous-language.md) for glossary maintenance and language evolution practices.

### 2. Bounded Contexts and Context Mapping

**Core concept:** A bounded context is an explicit boundary within which a particular domain model applies. The same word ("Customer") can mean different things in different contexts; context maps define the relationships and translation strategies between them.

**Why it works:** Large systems that try to maintain a single unified model inevitably collapse into inconsistency. Bounded contexts accept that different parts of the business need different models; context maps manage the integration between them.

**Key insights:**
- A bounded context is not a microservice -- it is a linguistic and model boundary that may contain multiple services
- Context boundaries often align with team boundaries (Conway's Law)
- The nine context mapping patterns describe political and technical relationships between teams
- Anti-Corruption Layer is the most important defensive pattern -- never let a foreign model leak into your core domain
- Shared Kernel couples two teams; keep it small and explicitly governed
- Start by mapping what exists (Big Ball of Mud), then define target boundaries

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Service integration | Anti-Corruption Layer | Translate external API responses into your domain objects at the boundary |
| Legacy migration | Conformist / ACL | Wrap the legacy system behind an adapter that speaks your domain language |
| API design | Open Host Service + Published Language | Expose a well-documented REST API with a canonical schema |

See: [references/bounded-contexts.md](references/bounded-contexts.md) for the nine mapping patterns and integration strategies.

### 3. Entities, Value Objects, and Aggregates

**Core concept:** Entities have identity that persists across state changes. Value Objects are defined entirely by their attributes and are immutable. Aggregates are clusters of entities and value objects with a single root that enforces consistency boundaries.

**Why it works:** Without these distinctions, everything becomes a mutable, identity-bearing object -- tangled state, inconsistent updates, fragile concurrency. Aggregates draw the line: everything inside is guaranteed consistent; everything outside is eventually consistent.

**Key insights:**
- Entity test: "Am I the same thing even if all my attributes change?" (a person changes name and address -- still the same person)
- Value Object test: "Am I defined only by my attributes?" (any $10 bill is interchangeable with another)
- Most things should be Value Objects, not Entities -- prefer immutability
- Keep aggregates small (one root plus a minimal cluster); reference other aggregates by ID, not object reference
- Immediate consistency only within an aggregate; design for eventual consistency between aggregates

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Identity tracking | Entity with ID | `Order` identified by `orderId`, survives state changes |
| Immutable attributes | Value Object | `Address(street, city, zip)` -- replace, never mutate |
| Consistency boundary | Aggregate Root | `Order` is root; `OrderLine` items exist only through it |
| Concurrency control | Optimistic locking on root | Version field on `Order`; conflict if two edits race |

See: [references/building-blocks.md](references/building-blocks.md) for aggregate design rules and consistency boundaries.

### 4. Domain Events

**Core concept:** A domain event captures something that happened in the domain that experts care about, named in past tense (`OrderPlaced`, `PaymentReceived`) -- a fact that has already occurred.

**Why it works:** Domain events decouple cause from effect. When `OrderPlaced` is published, shipping, billing, and notifications each react independently without the ordering context knowing about them -- less coupling, eventual consistency, a natural audit trail.

**Key insights:**
- Events are immutable facts -- once published, they cannot be changed or retracted
- Domain events are internal to a bounded context; integration events cross boundaries
- Events enable temporal decoupling: the producer does not wait for the consumer
- Event sourcing stores the full event history as the source of truth, deriving current state by replay
- Not every state change deserves an event -- only publish what the domain cares about

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| State transitions | Raise event on domain action | `order.place()` raises `OrderPlaced` |
| Cross-context integration | Publish integration event | `OrderPlaced` triggers `ShippingLabelRequested` in shipping context |
| Eventual consistency | Async event handlers | Inventory handler updates stock asynchronously after `OrderPlaced` |

See: [references/domain-events.md](references/domain-events.md) for event naming, event sourcing, and integration events.

### 5. Repositories and Factories

**Core concept:** Repositories provide the illusion of an in-memory collection of domain objects, hiding persistence. Factories encapsulate complex creation logic so aggregates are always born in a valid state.

**Why it works:** Domain logic should never depend on how objects are stored or constructed. Repositories hide SQL and ORMs so domain code reads like business logic; factories ensure invariants hold from the moment an aggregate exists.

**Key insights:**
- The Repository interface belongs in the domain layer; its implementation belongs in infrastructure
- Repository methods speak the ubiquitous language: `findPendingOrders()`, not `getByStatusCode(3)`
- Collection-oriented repositories mimic `add`/`remove`; persistence-oriented ones use `save`
- Factories are warranted for complex rules or multi-part assembly; a two-field Value Object just needs a constructor
- The Specification pattern encapsulates query criteria as domain objects: `OverdueInvoiceSpecification`

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Data access abstraction | Repository interface | `OrderRepository.findByCustomer(customerId)` in domain; `PostgresOrderRepository` in infrastructure |
| Complex creation | Factory method | `Order.createFromQuote(quote)` validates and assembles from a `Quote` aggregate |
| Query encapsulation | Specification | `spec = OverdueBy(days=30); repo.findMatching(spec)` |

See: [references/repositories-factories.md](references/repositories-factories.md) for Repository, Factory, and Specification patterns.

### 6. Strategic Design and Distillation

**Core concept:** Not all parts of a system are equally important. Strategic design identifies the Core Domain -- where competitive advantage lives -- and distinguishes it from Supporting Subdomains (necessary, not differentiating) and Generic Subdomains (commodity).

**Why it works:** Applying the same rigor everywhere spreads your best talent thin and over-engineers commodity functionality. Identifying the Core Domain concentrates the best developers and deepest modeling where they matter most.

**Key insights:**
- Core Domain: invest your best people and deepest modeling; Supporting: build, but don't over-engineer; Generic (auth, email, payments): buy or use open-source
- Distillation extracts and highlights the Core Domain from surrounding complexity
- A Domain Vision Statement is a one-page description of the Core Domain's value proposition
- Revisit what is "core" as the business evolves -- today's differentiator may become tomorrow's commodity

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| Build vs. buy | Classify subdomain type | Build custom pricing engine (core); use Stripe for payments (generic) |
| Team allocation | Best developers on Core Domain | Seniors model underwriting rules; juniors integrate the email service |
| Code organization | Separate core from generic | `domain/pricing/` (deep model) vs. `infrastructure/email/` (thin adapter) |

See: [references/strategic-design.md](references/strategic-design.md) for subdomain classification and distillation techniques.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Technical names instead of domain language | Logic hidden behind `DataManager`; experts can't validate the model | Rename to domain terms (`ClaimAdjudicator`); if no domain term exists, the concept may be wrong |
| One model to rule them all | A single `Customer` class for billing, shipping, and marketing becomes bloated and contradictory | Bounded contexts: each gets its own `Customer` with only the attributes it needs |
| Giant aggregates | Concurrency conflicts, slow loads, transactional bottlenecks | Keep aggregates small; reference by ID; eventual consistency between them |
| Anemic domain model | Objects are data bags; rules scatter across services and duplicate | Move behavior into entities and value objects; services orchestrate only |
| No Anti-Corruption Layer | Foreign models leak in; code couples to external schemas | Wrap every external system behind a translation layer |
| Bounded context = microservice | Premature extraction; distributed complexity without benefit | A context is a model boundary, not a deployment unit; start with modules in a monolith |
| Skipping domain experts | Developers invent a model that doesn't match reality; expensive rework | Regular modeling sessions until experts say "yes, that is how it works" |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can a domain expert read your class names and understand them? | Technical jargon hides the model | Rename classes, methods, events to ubiquitous language |
| Are bounded context boundaries explicitly defined? | Models bleed; same term means different things | Draw a context map; define boundaries and translations |
| Are aggregates small (one root + minimal cluster)? | Slow loads, concurrency issues | Split aggregates; reference by ID; accept eventual consistency |
| Do domain objects contain behavior, not just data? | Anemic model; logic scattered in services | Move business rules into entities and value objects |
| Are domain events used for cross-aggregate communication? | Tight coupling, synchronous chains | Introduce events; let aggregates react asynchronously |
| Is there an Anti-Corruption Layer at every external integration? | Foreign models pollute your domain | Add a translation layer at each boundary |
| Have you identified which subdomain is core? | Best talent spread thin | Classify subdomains; focus deep modeling on the Core Domain |

## Reference Files

- [ubiquitous-language.md](references/ubiquitous-language.md): Building a shared language, glossary maintenance, naming in code, language evolution
- [bounded-contexts.md](references/bounded-contexts.md): Context boundaries, nine mapping patterns, team relationships, integration strategies
- [building-blocks.md](references/building-blocks.md): Entities, Value Objects, Aggregates, aggregate design rules, consistency boundaries
- [domain-events.md](references/domain-events.md): Event naming, event sourcing, event-driven architecture, integration events
- [repositories-factories.md](references/repositories-factories.md): Repository pattern, Factory pattern, Specification pattern, ports and adapters
- [strategic-design.md](references/strategic-design.md): Core Domain, Generic and Supporting Subdomains, distillation, build vs. buy

## Further Reading

For the complete methodology, patterns, and deeper insights:

- [*"Domain-Driven Design: Tackling Complexity in the Heart of Software"*](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215?tag=wondelai00-20) by Eric Evans

## About the Author

**Eric Evans** is a software design consultant and the originator of Domain-Driven Design, developed through work on large-scale systems in finance, insurance, and logistics. His 2003 book *Domain-Driven Design: Tackling Complexity in the Heart of Software* is one of the most influential software architecture books ever written, and he continues to evolve DDD through his consultancy, Domain Language.
