# Boundaries and Boundary Anatomy

Boundaries are the lines that separate software elements. In Clean Architecture, boundaries separate policies from details, stable code from volatile code, and high-level concerns from low-level mechanisms. How you draw boundaries, where you place them, and how you implement them determines whether a system remains maintainable over decades or degrades into an unmaintainable monolith.

This reference covers boundary anatomy, boundary crossing mechanisms, the Humble Object pattern, partial boundaries, layers and boundaries, services as boundaries, test boundaries, and the Main component as the ultimate plugin.


## Table of Contents
1. [Boundary Anatomy](#boundary-anatomy)
2. [Boundary Crossing](#boundary-crossing)
3. [The Humble Object Pattern](#the-humble-object-pattern)
4. [Partial Boundaries](#partial-boundaries)
5. [Services as Boundaries](#services-as-boundaries)
6. [Test Boundaries](#test-boundaries)
7. [The Main Component as a Plugin](#the-main-component-as-a-plugin)

---

## Boundary Anatomy

### What Is a Boundary?

A boundary is a separation between two groups of code where one side should not know about the other. At its core, a boundary is an interface plus a dependency inversion: the inner side defines an abstraction, and the outer side provides a concrete implementation.

### The Structure of a Full Boundary

A full boundary has components on both sides, connected through polymorphism:

```
[Client Side]                    [Boundary]                    [Implementation Side]
                                     |
Controller ----calls----> InputPort (interface)
                                     |
                              Interactor (implements InputPort)
                                     |
                              Interactor ----calls----> OutputPort (interface)
                                     |
                                                          Presenter (implements OutputPort)
```

**Both interfaces are defined on the inner side.** The Controller depends on `InputPort` (inward). The Presenter implements `OutputPort` (inward). The Interactor knows about neither the Controller nor the Presenter directly.

### Boundary Components

| Component | Circle | Role |
|-----------|--------|------|
| **Input Port** | Use Case | Interface that defines what the use case accepts |
| **Output Port** | Use Case | Interface that defines what the use case produces |
| **Interactor** | Use Case | Implements Input Port; calls Output Port |
| **Controller** | Adapter | Calls Input Port; translates from delivery mechanism |
| **Presenter** | Adapter | Implements Output Port; translates to display format |
| **Data Transfer Objects** | Use Case | Simple structures that carry data across the boundary |
| **Gateway Interface** | Use Case | Abstraction for data persistence or external services |
| **Gateway Implementation** | Adapter | Concrete persistence or service access |

## Boundary Crossing

### How Data Flows Across Boundaries

Data crosses boundaries as simple data structures -- DTOs, structs, or primitives. Never as framework objects, ORM entities, or complex objects that carry dependencies.

**Inbound crossing (Controller to Use Case):**

```python
# Controller creates a simple DTO and passes it inward
@dataclass(frozen=True)
class TransferFundsRequest:
    source_account_id: str
    destination_account_id: str
    amount: str  # String to avoid float precision issues
    currency: str

# Controller
class TransferController:
    def handle(self, http_body: dict) -> None:
        request = TransferFundsRequest(
            source_account_id=http_body["from"],
            destination_account_id=http_body["to"],
            amount=http_body["amount"],
            currency=http_body["currency"],
        )
        self._transfer_use_case.execute(request)
```

**Outbound crossing (Use Case to Presenter):**

```python
# Use Case creates a response DTO and passes it outward through the Output Port
@dataclass(frozen=True)
class TransferFundsResponse:
    transfer_id: str
    new_source_balance: str
    timestamp: str

# In the Interactor:
response = TransferFundsResponse(
    transfer_id=transfer.id,
    new_source_balance=str(source_account.balance),
    timestamp=transfer.created_at.isoformat(),
)
self._presenter.present_success(response)
```

### Flow of Control vs. Direction of Dependency

This is a subtle but critical distinction:

- **Flow of control:** Controller --> Interactor --> Presenter (left to right, outward at the end)
- **Source code dependency:** Controller --> InputPort <-- Interactor --> OutputPort <-- Presenter

The dependencies point inward on both sides of the Interactor. Control flows outward to the Presenter, but the dependency is inverted: the Presenter depends on (implements) an interface defined by the Use Case.

## The Humble Object Pattern

### The Problem

Some code is inherently hard to test because it's close to a boundary with something difficult to control -- a GUI, a database connection, a network socket. The Humble Object pattern splits such code into two parts:

1. **The Humble Object:** Contains the hard-to-test code, stripped of all logic. It's so simple that testing is unnecessary (or trivially easy).
2. **The Testable Object:** Contains all the logic, extracted from the hard-to-test context so it can be tested in isolation.

### Pattern Structure

```
[Testable Logic]              [Humble Object]
PresenterLogic    -produces->  ViewModel
(easy to test)                 (simple data)
                                    |
                                    v
                               View/Template
                               (hard to test, but so simple it doesn't matter)
```

### Examples of Humble Objects

**1. View (GUI boundary):**

```python
# Testable: Presenter that produces a ViewModel
class OrderPresenterLogic:
    def present(self, response: OrderResponse) -> OrderViewModel:
        return OrderViewModel(
            title=f"Order #{response.order_id}",
            total=f"${response.total:.2f}",
            status_color="green" if response.status == "completed" else "yellow",
            items=[f"{i.name} x{i.qty}" for i in response.items],
        )

# Humble: View that just renders the ViewModel (no logic to test)
class OrderView:
    def render(self, vm: OrderViewModel) -> str:
        return self._template.render(vm)  # Template rendering only
```

The Presenter is easily testable -- give it a response, assert the ViewModel. The View is humble -- it just passes the ViewModel to a template engine. No logic, no decisions.

**2. Database Gateway (persistence boundary):**

```python
# Testable: Use Case logic that decides what to persist
class ApproveExpenseInteractor:
    def execute(self, request: ApproveExpenseRequest) -> None:
        expense = self._repo.find_by_id(request.expense_id)
        expense.approve(request.approver_id)  # Business logic -- testable
        self._repo.save(expense)

# Humble: Repository that just maps and persists (minimal logic)
class SqlExpenseRepository:
    def save(self, expense: Expense) -> None:
        self._conn.execute(
            "UPDATE expenses SET status = %s, approved_by = %s WHERE id = %s",
            (expense.status.value, expense.approver_id, expense.id),
        )
```

The Interactor contains the decision logic (testable with a mock repo). The Repository is humble -- it just maps entity state to SQL parameters.

**3. Service Gateway (external service boundary):**

```python
# Testable: Logic that decides whether and how to send notifications
class NotificationService:
    def __init__(self, sender: NotificationSender):
        self._sender = sender

    def notify_order_shipped(self, order: Order) -> None:
        if order.customer_prefers_email():
            self._sender.send_email(
                to=order.customer_email,
                subject=f"Order {order.id} shipped",
                body=self._format_shipping_message(order),
            )

# Humble: Just sends the message (hard to test, but no logic)
class SmtpNotificationSender(NotificationSender):
    def send_email(self, to: str, subject: str, body: str) -> None:
        self._smtp.sendmail(self._from_addr, to, self._build_mime(subject, body))
```

### Where Humble Objects Appear in Clean Architecture

| Boundary | Humble Object | Testable Partner |
|----------|--------------|-----------------|
| GUI/View | Template renderer, React component | Presenter logic that produces ViewModel |
| Database | SQL execution, ORM save/load | Use Case logic, mapping logic |
| External API | HTTP client wrapper | Service logic that decides what to send |
| Filesystem | File read/write operations | Logic that decides what to read/write |
| Clock/Random | System clock, random generator | Logic that uses injected clock/random |

## Partial Boundaries

### When Full Boundaries Are Too Expensive

Full boundaries require interfaces on both sides (Input Port and Output Port), separate DTOs, and careful dependency management. Sometimes the anticipated need for a boundary doesn't justify the cost. In these cases, use a partial boundary.

### Three Forms of Partial Boundaries

**1. Skip the last step (prepare for full boundary later):**

Create the interfaces and separate the components, but deploy them together in the same package. You've done the intellectual work of separation but deferred the deployment separation.

```python
# Same package, but clearly separated with interfaces
# Can be split into separate packages later with minimal effort
class OrderService:
    def __init__(self, repo: OrderRepository):  # Interface exists
        self._repo = repo

class InMemoryOrderRepository(OrderRepository):  # Implementation exists
    ...

# Both live in the same package for now
```

**2. Strategy pattern (one-sided boundary):**

```python
# Only the outbound side has an interface
class ReportGenerator:
    def __init__(self, formatter: ReportFormatter):
        self._formatter = formatter

    def generate(self, data: ReportData) -> str:
        # Logic here
        return self._formatter.format(processed_data)

class PdfFormatter(ReportFormatter):
    def format(self, data) -> str: ...

class CsvFormatter(ReportFormatter):
    def format(self, data) -> str: ...
```

No Input Port, no Output Port -- just a simple strategy. Lighter weight than a full boundary.

**3. Facade pattern (simplest):**

```python
class OrderFacade:
    """Single entry point to order subsystem. Hides internal complexity."""
    def place_order(self, items, customer_id):
        # Delegates to internal classes
        order = self._order_factory.create(items, customer_id)
        self._order_repo.save(order)
        self._notifier.notify(order)
```

The Facade provides a simpler interface but doesn't enforce dependency direction. It's the weakest form of boundary -- better than nothing, but easily violated.

### Choosing Boundary Strength

| Situation | Boundary Type | Cost | Protection |
|-----------|--------------|------|------------|
| Will definitely need to swap implementations | Full boundary (ports on both sides) | High | Complete |
| Might need to swap; want the option | Partial (interfaces, same package) | Medium | Good |
| Multiple strategies but stable architecture | Strategy pattern | Low-medium | Moderate |
| Just want to simplify access to a subsystem | Facade | Low | Minimal |
| Uncertain -- need might never arise | None (but document the decision) | Zero | None |

## Services as Boundaries

### Services Are Not Inherently Architectural

A common misconception is that splitting a system into microservices automatically creates clean architectural boundaries. It does not. A microservice with a fat shared database or a shared data model is just a distributed monolith -- all the coupling of a monolith plus the complexity of network communication.

### When Services Create Real Boundaries

A service creates a genuine architectural boundary when:
- It has its own data store that no other service accesses directly
- It communicates through well-defined interfaces (API contracts)
- Its internal structure follows the Dependency Rule independently
- It can be developed, deployed, and scaled independently

### When Services Fail as Boundaries

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Shared database | Changes to the schema affect all services -- they're coupled |
| Shared data model library | All services import the same DTOs -- they change together |
| Synchronous orchestration | Service A calls B calls C calls D -- distributed monolith |
| Chatty communication | Services exchange many small calls -- performance and coupling |

### Services Should Contain Clean Architecture

Each service should have its own concentric circles internally:

```
Service Boundary
├── Entities (domain objects for this service's bounded context)
├── Use Cases (application logic for this service)
├── Adapters (controllers, gateways, presenters for this service)
└── Frameworks (HTTP server, database driver for this service)
```

The service boundary is a deployment boundary. The Clean Architecture circles within each service are architectural boundaries. Both are needed.

## Test Boundaries

### Tests as the Most Isolated Component

Tests are the most decoupled component in any system. They depend on the code being tested, but nothing in the production system depends on the tests. Tests always point inward -- they test entities, use cases, and adapters, but no production code imports test code.

### The Testing Boundary Structure

```
[Production Code]                [Test Code]
Entity ---------<depends-on------ EntityTest
UseCase --------<depends-on------ UseCaseTest
Adapter --------<depends-on------ AdapterTest

(No arrow from Production to Test)
```

### Testing Each Circle

| Circle | Test Strategy | Dependencies Needed |
|--------|--------------|-------------------|
| **Entities** | Unit tests with no mocks | None -- entities are self-contained |
| **Use Cases** | Unit tests with mocked ports | Mock repositories, mock presenters |
| **Adapters** | Integration tests | Real database (testcontainers), real HTTP |
| **Frameworks** | End-to-end tests | Full system running |

### The Fragile Test Problem

When tests depend on implementation details (private methods, internal data structures, specific framework behavior), they break when the code is refactored even though behavior hasn't changed. The Dependency Rule helps: tests should depend on the same interfaces that the production code depends on.

```python
# FRAGILE: Test depends on internal implementation
def test_order_internal_state():
    order = Order(items)
    assert order._internal_state == "pending"  # Private field -- fragile

# ROBUST: Test depends on public behavior (same interface as production code)
def test_order_is_pending_after_creation():
    order = Order(items)
    assert order.status == OrderStatus.PENDING  # Public behavior -- stable
```

## The Main Component as a Plugin

### Main Is the Dirtiest Component

The Main component (or composition root) is the one place where all concrete classes from all circles are known. It creates the concrete instances, wires them together, and starts the system. It is the most concrete, most dependent, and most volatile component.

**But nothing depends on Main.** It sits at the outermost edge of the system. It is a plugin to the application -- a configuration detail that determines which concrete implementations are used for each abstract port.

### Main's Responsibilities

1. **Instantiate concrete infrastructure** (database connections, API clients, caches)
2. **Instantiate concrete adapters** (repositories, presenters, gateways)
3. **Instantiate use case interactors** with injected dependencies
4. **Instantiate controllers** with injected use cases
5. **Configure the framework** (routes, middleware, error handlers)
6. **Start the application** (listen on port, begin event loop)

### Different Mains for Different Configurations

Because Main is a plugin, you can have multiple Main configurations:

```python
# main_production.py
def create_app():
    repo = PostgresOrderRepository(production_db_pool)
    emailer = SendGridEmailer(production_api_key)
    ...

# main_test.py
def create_app():
    repo = InMemoryOrderRepository()
    emailer = FakeEmailer()
    ...

# main_local.py
def create_app():
    repo = SqliteOrderRepository("local.db")
    emailer = ConsoleEmailer()  # Prints to stdout
    ...
```

The business logic (entities, use cases) is identical across all three. Only the wiring in Main changes. This is the ultimate demonstration that frameworks, databases, and external services are details -- plugins that can be swapped by changing the composition root.

### Main and Dependency Injection Frameworks

DI frameworks (Spring, Guice, tsyringe) can help wire dependencies in Main. But be careful:

- **Use DI framework annotations ONLY in Main or configuration classes** -- never in entities or use cases
- The DI framework is itself a framework detail -- it belongs in the outermost circle
- You should be able to wire the entire system manually in a test without the DI framework
- If removing the DI framework would require changes to business logic, you've coupled too tightly

### The Plugin Architecture Realized

When Main is the only place that knows about concrete implementations, the entire system becomes a plugin architecture:

```
                 Main (composition root)
                /    |     |      \
               /     |     |       \
    PostgresRepo  SendGrid  Express  Stripe
         |           |        |        |
         v           v        v        v
    [OrderRepo]  [Emailer]  [HTTP]  [Payment]
    (interface)  (interface) (route) (interface)
         \          |        |       /
          \         |        |      /
           Use Case Interactors
                    |
                 Entities
```

Entities and Use Cases sit at the center, defining what they need through interfaces. Main plugs in the concrete implementations. The business rules don't know or care which database, email provider, web framework, or payment processor is being used. They just work.
