# Entities and Use Cases

Entities and Use Cases form the two innermost circles of Clean Architecture. Entities contain Enterprise Business Rules -- the most general and highest-level rules. Use Cases contain Application Business Rules -- the automation rules specific to a particular application. Together, they represent the core value of the system, the code that is most worth protecting from external change.

This reference covers entity design, use case structure, the interactor pattern, input/output boundaries, request/response models, and strategies for keeping use cases focused.


## Table of Contents
1. [Enterprise Business Rules (Entities)](#enterprise-business-rules-entities)
2. [Application Business Rules (Use Cases)](#application-business-rules-use-cases)
3. [Request and Response Models](#request-and-response-models)
4. [Keeping Use Cases Focused](#keeping-use-cases-focused)

---

## Enterprise Business Rules (Entities)

### What Is an Entity?

An entity is an object within the system that embodies a small set of critical business rules operating on critical business data. The entity object either contains the critical business data or has easy access to it. The interface of the entity consists of the functions that implement the critical business rules.

**Critical distinction:** An entity is not a database row. It is not an ORM model. It is not a struct that merely holds data. An entity encapsulates business rules -- logic that would exist even if there were no computer system at all.

### Characteristics of Well-Designed Entities

**1. Framework-independent:**
Entities do not inherit from database base classes, do not carry ORM annotations, and do not import framework packages.

```python
# WRONG: Entity coupled to ORM
class Order(db.Model):  # Inherits from SQLAlchemy
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)

# RIGHT: Pure domain entity
class Order:
    def __init__(self, order_id: str, items: list[OrderItem], customer_id: str):
        self._id = order_id
        self._items = items
        self._customer_id = customer_id
        self._status = OrderStatus.PENDING

    def calculate_total(self) -> Money:
        subtotal = sum(item.price * item.quantity for item in self._items)
        return subtotal + self._calculate_tax(subtotal)

    def _calculate_tax(self, subtotal: Money) -> Money:
        # Business rule: tax calculation
        return subtotal * Decimal("0.08")
```

**2. Business-rule containers:**
The methods on an entity enforce business invariants. They are not getters and setters -- they represent meaningful business operations.

```python
class BankAccount:
    def withdraw(self, amount: Money) -> None:
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)
        if self._is_frozen:
            raise AccountFrozenError(self._account_id)
        self._balance -= amount
        self._record_transaction(TransactionType.WITHDRAWAL, amount)
```

The `withdraw` method encapsulates business rules: you cannot withdraw more than the balance, and you cannot withdraw from a frozen account. These rules exist regardless of whether the system is a web app, a mobile app, or a batch process.

**3. Stable over time:**
Entities change only when business rules change. A decision to migrate from PostgreSQL to DynamoDB should not require any entity modifications. A decision to change the web framework should not affect entities.

**4. Testable in complete isolation:**
You should be able to instantiate an entity and call its methods in a unit test with zero setup -- no database, no framework, no configuration files.

```python
def test_order_calculates_total_with_tax():
    items = [OrderItem("widget", Money("10.00"), quantity=3)]
    order = Order("order-1", items, "customer-1")
    assert order.calculate_total() == Money("32.40")  # 30.00 + 2.40 tax
```

### Entity Design Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Rich domain model** | Complex business rules with many invariants | `Order` with status transitions, validation, calculations |
| **Value objects** | Immutable concepts defined by their attributes | `Money(amount, currency)`, `Address(street, city, zip)` |
| **Aggregates** | Cluster of entities treated as a unit for data changes | `Order` aggregate contains `OrderItems`; external code accesses items only through `Order` |
| **Domain events** | Communicate that something meaningful happened | `Order.place()` produces `OrderPlaced` event |
| **Factory methods** | Complex construction that enforces invariants | `Order.create(items, customer)` validates and initializes |

### Common Entity Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Anemic entities (data-only, no behavior) | Business rules scatter into services; entity is just a DTO | Move business logic into entity methods |
| ORM annotations on domain entities | Entity depends on database framework | Separate domain entity from persistence model |
| Entity knows about its repository | Entity depends on infrastructure | Pass dependencies into use cases, not entities |
| Public setters on everything | No invariant protection; any code can put entity in invalid state | Use methods that enforce business rules; make fields private |

## Application Business Rules (Use Cases)

### What Is a Use Case?

A Use Case describes a single, specific application operation. It orchestrates entities and defines the application-specific rules for how data flows to and from those entities. It accepts input through a defined port, manipulates entities, and produces output through another defined port.

**Critical distinction:** Use Cases are not entities. An entity encapsulates a business rule that would exist without software. A Use Case automates a specific application workflow that only makes sense within the context of the software system.

### The Interactor Pattern

The Interactor is the concrete class that implements a Use Case. The pattern has three parts:

1. **Input Port (Input Boundary):** An interface that defines what the Use Case accepts. The Controller calls this interface.
2. **Interactor:** The concrete class that implements the Input Port and contains the application logic.
3. **Output Port (Output Boundary):** An interface that defines what the Use Case produces. The Presenter implements this interface.

```python
# Input Port -- defined in the Use Case circle
class PlaceOrderInput(ABC):
    @abstractmethod
    def execute(self, request: PlaceOrderRequest) -> None:
        pass

# Output Port -- defined in the Use Case circle
class PlaceOrderOutput(ABC):
    @abstractmethod
    def present_success(self, response: OrderResponse) -> None:
        pass

    @abstractmethod
    def present_validation_error(self, errors: list[str]) -> None:
        pass

    @abstractmethod
    def present_failure(self, message: str) -> None:
        pass

# Interactor -- implements Input Port, uses Output Port
class PlaceOrderInteractor(PlaceOrderInput):
    def __init__(self, order_repo: OrderRepository, presenter: PlaceOrderOutput):
        self._order_repo = order_repo
        self._presenter = presenter

    def execute(self, request: PlaceOrderRequest) -> None:
        errors = self._validate(request)
        if errors:
            self._presenter.present_validation_error(errors)
            return

        order = Order.create(
            items=[OrderItem(i.product_id, i.quantity, i.price) for i in request.items],
            customer_id=request.customer_id,
        )

        self._order_repo.save(order)

        response = OrderResponse(
            order_id=order.id,
            total=order.calculate_total(),
            status=order.status.value,
        )
        self._presenter.present_success(response)
```

### Input/Output Boundaries

The boundaries are the interfaces that separate the Use Case circle from the circles on either side. They are defined in the Use Case circle and implemented by the outer circles.

**Why boundaries matter:**
- The Controller depends on the Input Port (inward dependency -- correct)
- The Presenter depends on the Output Port (inward dependency -- correct)
- The Interactor depends on neither the Controller nor the Presenter (isolation preserved)

### Alternative: Return-Based Use Cases

Not every use case needs the full Output Port pattern. A simpler approach returns a result directly:

```python
class PlaceOrderInteractor:
    def __init__(self, order_repo: OrderRepository):
        self._order_repo = order_repo

    def execute(self, request: PlaceOrderRequest) -> Result[OrderResponse, OrderError]:
        errors = self._validate(request)
        if errors:
            return Failure(ValidationError(errors))

        order = Order.create(...)
        self._order_repo.save(order)
        return Success(OrderResponse(order.id, order.calculate_total()))
```

This is simpler and often sufficient. Use the full Output Port pattern when the presentation logic is complex or when you need to support multiple presentation formats from the same use case.

## Request and Response Models

### Request Models

Request models are simple data structures that carry input data across the boundary. They are defined in the Use Case circle.

**Rules for request models:**
- No framework types (no `HttpRequest`, no `Form`, no `JsonNode`)
- No entity types (the controller maps external data to the request model; the interactor maps the request model to entity calls)
- Contain only primitives, strings, and simple nested structures
- May contain validation hints but not validation logic dependent on external state

```python
@dataclass(frozen=True)
class PlaceOrderRequest:
    customer_id: str
    items: list[OrderItemRequest]
    shipping_address: AddressRequest
    coupon_code: str | None = None

@dataclass(frozen=True)
class OrderItemRequest:
    product_id: str
    quantity: int
    unit_price: str  # String to avoid floating-point; Use Case converts to Money
```

### Response Models

Response models carry output data across the boundary. They are defined in the Use Case circle.

**Rules for response models:**
- No entity types -- the Use Case extracts the relevant data from entities and populates the response
- No framework types -- the Presenter (outer circle) converts the response into whatever format the delivery mechanism needs
- Contain only the data the outer circle needs to fulfill its role

```python
@dataclass(frozen=True)
class OrderResponse:
    order_id: str
    total: str  # Formatted money value
    status: str
    estimated_delivery: str | None
    items: list[OrderItemResponse]

@dataclass(frozen=True)
class OrderItemResponse:
    product_name: str
    quantity: int
    line_total: str
```

### The Mapping Chain

Data transforms at each boundary:

```
HTTP Request (JSON)
    --> Controller maps to --> PlaceOrderRequest (DTO)
        --> Interactor maps to --> Entity method calls
            --> Entity produces result
        --> Interactor maps to --> OrderResponse (DTO)
    --> Presenter maps to --> ViewModel or JSON
--> HTTP Response
```

Each transformation is a boundary crossing. Each boundary is an opportunity to decouple.

## Keeping Use Cases Focused

### One Use Case, One Operation

Each Use Case should represent a single application operation. If you find a Use Case doing multiple things, split it.

**Signs of an unfocused Use Case:**
- The class name contains "And" (e.g., `CreateAndNotifyOrder`)
- The execute method has conditional branches for fundamentally different operations
- The class has more than 3-4 dependencies
- The test file has tests for unrelated scenarios

### Use Case Granularity Guidelines

| Granularity | Use Case Example | Notes |
|-------------|-----------------|-------|
| **Too coarse** | `ManageOrders` | Does everything -- create, update, cancel, refund |
| **Right level** | `PlaceOrder`, `CancelOrder`, `RefundOrder` | Each is a single operation with clear input and output |
| **Too fine** | `ValidateOrderItems`, `CalculateOrderTotal` | These are steps within a use case, not standalone operations |

### Composing Use Cases

Sometimes one application operation involves multiple steps that could be their own use cases. Two approaches:

**1. Use Case calls Use Case (simple composition):**

```python
class PlaceOrderAndSendConfirmation:
    def __init__(self, place_order: PlaceOrderInput, send_confirmation: SendConfirmationInput):
        self._place_order = place_order
        self._send_confirmation = send_confirmation

    def execute(self, request: PlaceOrderRequest) -> None:
        order_result = self._place_order.execute(request)
        if order_result.is_success:
            self._send_confirmation.execute(
                SendConfirmationRequest(order_result.order_id)
            )
```

**2. Domain events (loose coupling):**

The Use Case emits a domain event; another Use Case subscribes to it. This is better when the steps are truly independent and could happen asynchronously.

### Use Case Dependencies

A Use Case should depend on:
- **Entity types** (to call business rules)
- **Repository interfaces** (to load and persist entities)
- **Output port interfaces** (to present results)
- **Domain service interfaces** (for cross-entity business operations)

A Use Case should NOT depend on:
- **Framework types** (HTTP, ORM, message queue)
- **Concrete infrastructure classes** (database client, email service)
- **Other use case concrete classes** (use input port interfaces instead)
- **Configuration or environment variables** (inject configuration as constructor parameters)

### Testing Use Cases

Use Cases should be the most thoroughly tested part of the system because they contain the application's automation rules.

```python
def test_place_order_calculates_total_and_saves():
    # Arrange
    mock_repo = MockOrderRepository()
    mock_presenter = MockPlaceOrderPresenter()
    interactor = PlaceOrderInteractor(mock_repo, mock_presenter)

    request = PlaceOrderRequest(
        customer_id="cust-1",
        items=[OrderItemRequest("prod-1", quantity=2, unit_price="25.00")],
        shipping_address=AddressRequest("123 Main", "Springfield", "62704"),
    )

    # Act
    interactor.execute(request)

    # Assert
    assert mock_repo.saved_order is not None
    assert mock_repo.saved_order.calculate_total() == Money("54.00")  # 50 + 4 tax
    assert mock_presenter.success_response.order_id == mock_repo.saved_order.id
```

No database. No web server. No framework. Just the use case logic running in a plain unit test. This is the payoff of the Dependency Rule.
