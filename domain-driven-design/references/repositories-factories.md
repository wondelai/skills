# Repositories and Factories

Repositories and Factories are infrastructure-facing patterns in Domain-Driven Design that separate domain logic from persistence and object creation concerns. The Repository provides the illusion of an in-memory collection of aggregates. The Factory encapsulates complex creation logic. Together, they keep the domain model clean and focused on business rules.


## Table of Contents
1. [The Repository Pattern](#the-repository-pattern)
2. [The Factory Pattern](#the-factory-pattern)
3. [The Specification Pattern](#the-specification-pattern)
4. [Ports and Adapters Relationship](#ports-and-adapters-relationship)

---

## The Repository Pattern

A Repository mediates between the domain and data mapping layers, acting like an in-memory collection of domain objects. Domain code uses the repository to obtain aggregates without knowing how they are stored, queried, or reconstructed.

### Why Repositories Exist

Without repositories, domain logic becomes tangled with data access:

```
// Without repository -- domain logic polluted with SQL
def approve_claim(claim_id):
    row = db.execute("SELECT * FROM claims WHERE id = ?", claim_id)
    claim = Claim(row['id'], row['status'], row['amount'])
    claim.approve()
    db.execute("UPDATE claims SET status = ? WHERE id = ?", claim.status, claim.id)
```

```
// With repository -- domain logic is clean
def approve_claim(claim_id):
    claim = claim_repository.find_by_id(claim_id)
    claim.approve()
    claim_repository.save(claim)
```

The second version is readable by a domain expert. The first is not.

### Repository Interface Design

The repository interface belongs in the domain layer. It speaks the ubiquitous language:

**Good repository methods:**
- `find_by_id(order_id)` -- straightforward identity lookup
- `find_pending_orders()` -- uses domain language ("pending")
- `find_by_customer(customer_id)` -- domain-meaningful query
- `find_overdue_invoices(as_of_date)` -- business concept in the method name

**Bad repository methods:**
- `get_by_status_code(3)` -- magic number; what is status 3?
- `query(sql_string)` -- leaks persistence technology into the domain
- `find_all_with_joins()` -- technical concern, not domain language
- `get_by_column("status", "PENDING")` -- generic data access, not domain query

### Collection-Oriented vs. Persistence-Oriented Repositories

Eric Evans described two flavors of repository, each modeling a different metaphor:

#### Collection-Oriented Repository

Models the repository as an in-memory collection. You add objects to it and remove objects from it. Changes to retrieved objects are automatically tracked and persisted (like JPA/Hibernate managed entities).

```
interface OrderRepository:
    add(order)           # Like collection.add()
    remove(order)        # Like collection.remove()
    find_by_id(id)       # Like collection.find()
    # No explicit save() -- changes to retrieved objects are auto-tracked
```

**Best with:** ORMs that support change tracking (JPA/Hibernate, Entity Framework).

**Advantages:** Clean domain model; changes feel natural; no explicit save calls.

**Disadvantages:** "Magic" change tracking can surprise developers; harder to reason about when persistence happens.

#### Persistence-Oriented Repository

Models the repository as a storage mechanism. You explicitly save objects and the repository does not track changes automatically.

```
interface OrderRepository:
    save(order)          # Explicit persist/update
    delete(order_id)     # Explicit remove
    find_by_id(id)       # Retrieve
    # Must call save() explicitly after making changes
```

**Best with:** Frameworks without change tracking (most non-ORM approaches, event sourcing, document stores).

**Advantages:** Explicit control over when persistence happens; no surprises; easier to test.

**Disadvantages:** Must remember to call save(); risk of losing changes if save is forgotten.

**Which to choose:** If your persistence technology offers change tracking and your team is comfortable with it, use collection-oriented. Otherwise, use persistence-oriented. The persistence-oriented style is more common in modern applications because it is more explicit.

### Repository Implementation

The repository interface lives in the domain layer. The implementation lives in the infrastructure layer. This is the Dependency Inversion Principle in action:

```
domain/
    model/
        Order.py              # Aggregate root
        OrderLineItem.py      # Entity within aggregate
    repository/
        OrderRepository.py    # Interface (abstract class / protocol)

infrastructure/
    persistence/
        PostgresOrderRepository.py    # Implementation
        InMemoryOrderRepository.py    # Implementation for tests
```

The domain layer defines what it needs (the interface). The infrastructure layer provides it (the implementation). The domain never imports from infrastructure.

### What a Repository Returns

A repository always returns fully constituted aggregates -- not partial objects, not DTOs, not database rows. The aggregate returned from a repository must be in a valid state with all its invariants satisfied.

**Correct:** `order_repository.find_by_id(id)` returns an `Order` with all its `OrderLineItems` loaded, ready to have business operations performed on it.

**Incorrect:** `order_repository.find_by_id(id)` returns an `OrderDTO` with some fields populated and others lazily loaded. The caller must check which fields are available.

### Repository Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Generic repository (`Repository<T>`) | All aggregates look the same; domain-specific queries do not fit the generic interface | Create specific repository interfaces per aggregate type |
| Repository returns DTOs | DTOs are not domain objects; behavior cannot be called on them | Return full aggregates; use separate read models (CQRS) for queries |
| Repository per entity (not per aggregate) | Bypasses aggregate root; allows direct modification of internal entities | One repository per aggregate root only |
| Repository with business logic | Repository starts containing validation or transformation logic | Keep repositories as pure storage; domain logic belongs in the aggregate |
| Repository depends on domain services | Circular dependency between domain services and repositories | Repositories depend only on the domain model (aggregates, value objects) |

## The Factory Pattern

A Factory encapsulates the logic of creating a domain object, ensuring that the object is fully formed and valid from the moment it exists. In DDD, factories are used when object creation is complex enough to warrant its own abstraction.

### When to Use a Factory

| Situation | Factory Needed? | Why |
|-----------|----------------|-----|
| Creating a Value Object with 2-3 fields | No | A constructor suffices: `Money(100, "USD")` |
| Creating an aggregate with multiple parts and validation rules | Yes | The assembly logic is complex; a constructor would be enormous |
| Creating an object from an external representation (API response, file) | Yes | Translation from external format to domain object is a separate concern |
| Creating an object with conditional logic (different subtypes) | Yes | The decision of which subtype to create should not be in client code |
| Reconstituting an object from persistence | Maybe | If the repository handles it, a separate factory may not be needed |

### Factory Patterns in DDD

#### Factory Method on the Aggregate

The most common pattern: a static or class method on the aggregate itself:

```
class Order:
    @staticmethod
    def create_from_cart(cart, customer_id):
        # Validates cart is not empty
        # Converts cart items to OrderLineItems
        # Calculates initial total
        # Returns a fully valid Order
        order = Order(
            id=OrderId.generate(),
            customer_id=customer_id,
            status=OrderStatus.PENDING,
            items=[OrderLineItem.from_cart_item(item) for item in cart.items],
            total=cart.calculate_total()
        )
        order._raise_event(OrderCreated(...))
        return order
```

**Advantages:** Creation logic lives close to the aggregate. The aggregate controls its own birth.

#### Factory Method on Another Aggregate

When one aggregate creates another:

```
class Quote:
    def convert_to_order(self):
        # Quote knows how to create an Order from itself
        order = Order(
            id=OrderId.generate(),
            customer_id=self.customer_id,
            items=[OrderLineItem(item.product_id, item.quantity, item.quoted_price)
                   for item in self.line_items],
            source_quote_id=self.id
        )
        return order
```

#### Standalone Factory

When creation logic does not naturally belong to any existing aggregate:

```
class LoanApplicationFactory:
    def create_from_submission(self, submission, credit_report):
        # Complex assembly involving multiple inputs
        # Conditional logic based on loan type
        # Validation against business rules
        applicant = Applicant(submission.name, submission.ssn)
        risk_score = RiskScore.calculate(credit_report)

        if submission.loan_type == "mortgage":
            return MortgageApplication(applicant, risk_score, submission.property)
        elif submission.loan_type == "auto":
            return AutoLoanApplication(applicant, risk_score, submission.vehicle)
```

### Factory Invariants

The most critical rule of factories: **a factory must never produce an invalid object.** If the inputs are insufficient or violate business rules, the factory must fail (throw an exception), not produce a partially valid object.

```
# Good -- factory enforces invariants
class Order:
    @staticmethod
    def create(customer_id, items):
        if not items:
            raise EmptyOrderError("Cannot create an order with no items")
        if not customer_id:
            raise InvalidCustomerError("Order requires a customer")
        return Order(OrderId.generate(), customer_id, items)

# Bad -- factory produces potentially invalid objects
class Order:
    @staticmethod
    def create(customer_id=None, items=None):
        return Order(OrderId.generate(), customer_id, items or [])
        # caller can now have an order with no customer and no items
```

### Reconstitution vs. Creation

There is an important distinction between creating a new aggregate and reconstituting one from persistence:

| Aspect | Creation | Reconstitution |
|--------|---------|----------------|
| When | A new domain object comes into existence | An existing object is loaded from storage |
| Validation | Full business rule validation | No validation needed; data was validated on creation |
| Domain events | May raise creation events (`OrderCreated`) | Should NOT raise events; nothing new happened |
| Identity | Generate a new ID | Use the stored ID |
| Invariants | Enforce all invariants | Assume invariants hold (data was valid when stored) |

Reconstitution typically happens inside the repository implementation:

```
class PostgresOrderRepository:
    def find_by_id(self, order_id):
        row = self.db.query("SELECT * FROM orders WHERE id = ?", order_id)
        items = self.db.query("SELECT * FROM order_items WHERE order_id = ?", order_id)
        # Reconstitute -- no validation, no events
        return Order._reconstitute(
            id=row['id'],
            customer_id=row['customer_id'],
            status=row['status'],
            items=[OrderLineItem._reconstitute(i) for i in items]
        )
```

## The Specification Pattern

The Specification pattern encapsulates query criteria as first-class domain objects. Instead of building queries in service code, you express criteria as composable specification objects.

### Why Specifications

Without specifications, query logic scatters across the codebase:

```
# Query logic in a service -- not reusable, not composable
def find_risky_orders(self):
    return db.query("SELECT * FROM orders WHERE total > 10000 AND customer_risk > 7")

# Same logic duplicated elsewhere with slight variations
def find_very_risky_orders(self):
    return db.query("SELECT * FROM orders WHERE total > 50000 AND customer_risk > 9")
```

With specifications:

```
high_value = OrderValueExceeds(10000)
high_risk = CustomerRiskAbove(7)
risky_orders = order_repository.find_matching(high_value.and_(high_risk))

very_risky = OrderValueExceeds(50000).and_(CustomerRiskAbove(9))
very_risky_orders = order_repository.find_matching(very_risky)
```

### Specification Composition

Specifications compose using logical operators:

| Operator | Meaning | Example |
|----------|---------|---------|
| `and_` | Both must be true | `HighValue.and_(HighRisk)` |
| `or_` | Either must be true | `HighValue.or_(HighRisk)` |
| `not_` | Must not be true | `not_(Cancelled)` |

### Specifications in the Domain Layer

The specification interface lives in the domain layer. Implementations can be in the domain (for in-memory filtering) or infrastructure (for database queries):

```
# Domain layer -- specification interface
class Specification:
    def is_satisfied_by(self, candidate) -> bool:
        pass

class OverdueInvoice(Specification):
    def __init__(self, as_of_date):
        self.as_of_date = as_of_date

    def is_satisfied_by(self, invoice):
        return invoice.due_date < self.as_of_date and not invoice.is_paid
```

## Ports and Adapters Relationship

Repositories and Factories fit naturally into the Ports and Adapters (Hexagonal) architecture:

```
                    Domain Layer
                   ┌─────────────────────────┐
                   │  Aggregates             │
                   │  Value Objects           │
                   │  Domain Events           │
                   │  Repository Interfaces ──┼── Port (interface)
                   │  Factory Interfaces   ──┼── Port (interface)
                   └─────────────────────────┘
                              │
                              │ implements
                              ▼
                   Infrastructure Layer
                   ┌─────────────────────────┐
                   │  PostgresOrderRepo    ──┼── Adapter (implementation)
                   │  InMemoryOrderRepo    ──┼── Adapter (for tests)
                   │  S3DocumentFactory    ──┼── Adapter (implementation)
                   └─────────────────────────┘
```

**The key principle:** The domain defines what it needs (ports). Infrastructure provides it (adapters). Dependencies point inward -- infrastructure depends on domain, never the reverse.

This means:
- The domain layer has zero imports from infrastructure packages
- Repository interfaces use domain types (`Order`, `OrderId`), not infrastructure types (`Row`, `Document`)
- The application can swap persistence technologies by providing a new adapter without touching domain code
- Tests use in-memory adapters to test domain logic without databases
