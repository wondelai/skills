# Interface Adapters and Frameworks

Interface Adapters and Frameworks & Drivers form the two outermost circles of Clean Architecture. Interface Adapters translate data between the forms convenient for Use Cases and Entities and the forms convenient for external agencies. Frameworks and Drivers are the glue code that connects the system to the outside world. Together, these layers contain all the volatile, technology-specific decisions -- the parts most likely to change over the life of a system.

This reference covers controllers, presenters, gateways, the nature of frameworks as details, database and web as details, keeping frameworks at arm's length, and the plugin architecture.


## Table of Contents
1. [Interface Adapters](#interface-adapters)
2. [Frameworks as Details](#frameworks-as-details)
3. [The Database Is a Detail](#the-database-is-a-detail)
4. [The Web Is a Detail](#the-web-is-a-detail)
5. [Plugin Architecture](#plugin-architecture)
6. [Keeping Frameworks at Arm's Length](#keeping-frameworks-at-arms-length)

---

## Interface Adapters

### Controllers

A Controller is an adapter that translates input from the delivery mechanism (HTTP, CLI, message queue, gRPC) into a form that the Use Case can understand. It constructs a Request Model and calls the Use Case's Input Port.

**Responsibilities of a Controller:**
- Parse and extract data from the delivery mechanism's native format
- Construct the Use Case's Request Model
- Call the Use Case's Input Port
- Handle delivery-mechanism-specific concerns (authentication, rate limiting) BEFORE calling the Use Case

**What a Controller must NOT do:**
- Contain business logic
- Directly access the database
- Format output for the response (that's the Presenter's job)
- Know about other controllers

```python
# Controller in the Adapters circle
class OrderController:
    def __init__(self, place_order: PlaceOrderInput):
        self._place_order = place_order

    def create(self, http_request: dict) -> None:
        # Translate HTTP data to Use Case request
        request = PlaceOrderRequest(
            customer_id=http_request["customer_id"],
            items=[
                OrderItemRequest(
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    unit_price=item["unit_price"],
                )
                for item in http_request["items"]
            ],
            shipping_address=AddressRequest(
                street=http_request["address"]["street"],
                city=http_request["address"]["city"],
                zip_code=http_request["address"]["zip"],
            ),
        )
        # Delegate to the Use Case
        self._place_order.execute(request)
```

The Controller knows about HTTP data format and knows about `PlaceOrderRequest`. It translates between the two. The Use Case never sees HTTP.

### Presenters

A Presenter translates Use Case output into a form suitable for the delivery mechanism. It implements the Use Case's Output Port and produces a View Model.

**The Presenter pattern separates two concerns:**
1. The Use Case decides WHAT data to present
2. The Presenter decides HOW to format it for display

```python
# Output Port defined in Use Case circle
class PlaceOrderOutput(ABC):
    @abstractmethod
    def present_success(self, response: OrderResponse) -> None:
        pass

    @abstractmethod
    def present_failure(self, message: str) -> None:
        pass

# Presenter in the Adapters circle
class JsonOrderPresenter(PlaceOrderOutput):
    def __init__(self):
        self.view_model: dict = {}
        self.status_code: int = 200

    def present_success(self, response: OrderResponse) -> None:
        self.status_code = 201
        self.view_model = {
            "data": {
                "id": response.order_id,
                "total": f"${response.total}",
                "status": response.status.capitalize(),
                "estimated_delivery": response.estimated_delivery,
            }
        }

    def present_failure(self, message: str) -> None:
        self.status_code = 400
        self.view_model = {"error": {"message": message}}
```

The Presenter knows about JSON structure, status codes, and string formatting. The Use Case knows nothing about any of this.

### Gateways

A Gateway implements a repository or service interface defined by the Use Case circle using a specific technology. It is the adapter between the abstract port and the concrete implementation.

```python
# Interface defined in Use Case circle
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def find_by_id(self, order_id: str) -> Order | None:
        pass

# Gateway in the Adapters circle
class PostgresOrderRepository(OrderRepository):
    def __init__(self, connection_pool):
        self._pool = connection_pool

    def save(self, order: Order) -> None:
        with self._pool.connection() as conn:
            conn.execute(
                "INSERT INTO orders (id, customer_id, total, status) VALUES (%s, %s, %s, %s)",
                (order.id, order.customer_id, str(order.calculate_total()), order.status.value),
            )
            for item in order.items:
                conn.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (order.id, item.product_id, item.quantity, str(item.price)),
                )

    def find_by_id(self, order_id: str) -> Order | None:
        with self._pool.connection() as conn:
            row = conn.execute("SELECT * FROM orders WHERE id = %s", (order_id,)).fetchone()
            if row is None:
                return None
            items = conn.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,)).fetchall()
            return self._to_domain(row, items)

    def _to_domain(self, row, item_rows) -> Order:
        # Map database rows back to domain entity
        items = [OrderItem(r["product_id"], r["quantity"], Money(r["price"])) for r in item_rows]
        return Order(order_id=row["id"], items=items, customer_id=row["customer_id"])
```

Notice the `_to_domain` method: it maps between the persistence format (database rows) and the domain format (entity objects). This mapping is the gateway's core responsibility.

### Adapter Types Summary

| Adapter | Translates From | Translates To | Direction |
|---------|----------------|---------------|-----------|
| **Controller** | External input (HTTP, CLI, event) | Use Case Request Model | Inward |
| **Presenter** | Use Case Response Model | View Model (JSON, HTML, CLI output) | Outward |
| **Gateway** | Repository/Service Interface | Concrete technology (SQL, API, file) | Outward |
| **Mapper** | Domain Entity | Persistence Model (ORM, document) | Both directions |

## Frameworks as Details

### The Framework Trap

Frameworks are powerful tools. They provide routing, dependency injection, ORM, template rendering, and dozens of other features. The temptation is to build your system on top of the framework -- to let the framework be the architecture.

This is a trap. When the framework IS the architecture:
- You cannot test business logic without the framework running
- You cannot change the framework without rewriting the application
- Framework bugs become your bugs, in your most critical code
- Framework upgrades force changes throughout the system
- Your code becomes an accessory to the framework rather than the framework serving your code

### Frameworks Want Marriage, You Want a Fling

Frameworks are authored by people who have a use case for them. They provide massive power and convenience -- but they ask for commitment. They want you to:

- Inherit from their base classes
- Put their annotations on your code
- Store your data in their preferred format
- Structure your project their way

Each of these is a coupling point. The more you comply, the harder it is to separate.

**The Clean Architecture approach:**
- Don't derive business objects from framework base classes
- Don't put framework annotations on domain entities
- Don't let the framework dictate your project structure
- Treat the framework as a tool in the outermost circle, not as the foundation

### Practical Framework Isolation

| Framework Feature | Coupled Approach | Decoupled Approach |
|-------------------|-----------------|-------------------|
| **Routing** | Business logic in route handlers | Route handlers call Controllers; Controllers call Use Cases |
| **ORM** | Domain entities ARE ORM models | Separate domain entities; map to/from ORM models in gateways |
| **Validation** | Framework validation decorators on entities | Validation in Use Case or domain layer using plain code |
| **Dependency injection** | `@Inject` annotations on domain classes | Constructor injection; wiring in Main component |
| **Configuration** | `Settings.get("key")` in business logic | Inject config values as constructor parameters |
| **Logging** | Framework logger called directly in Use Cases | Inject a logger interface; implement with framework in outer circle |

## The Database Is a Detail

The database is a detail. It is a mechanism for storing and retrieving data. From the perspective of the business rules, it doesn't matter whether data lives in PostgreSQL, MongoDB, flat files, or an in-memory data structure.

### Why It Matters

When business rules know about the database:
- Testing requires a database (slow, fragile tests)
- Database schema changes ripple into business logic
- Migrating to a different database means rewriting business rules
- The data model is driven by database capabilities rather than business needs

### Repository Pattern

The repository pattern is the primary mechanism for keeping the database at arm's length:

1. **Define the interface in the Use Case circle** -- it describes WHAT operations the business needs, not HOW data is stored
2. **Implement the interface in the Adapter circle** -- this is where SQL, ORM calls, and database-specific code live
3. **Inject the implementation at startup** -- Main wires the concrete repository into the use case

### ORM Considerations

ORMs are useful tools, but they must be contained in the outer circles:

**The two-model approach:**
- **Domain model**: Pure business entities with business methods and rules. No ORM annotations. Lives in the Entity circle.
- **Persistence model**: ORM-annotated classes that map to database tables. Lives in the Adapter circle. The gateway maps between the two.

This duplication is intentional and valuable. The domain model evolves with business rules; the persistence model evolves with the database schema. They change for different reasons at different times.

## The Web Is a Detail

The web is a delivery mechanism -- a way to transport data between the user and the application. The business rules should not know whether they are being accessed through a web browser, a mobile app, a CLI, or a message queue.

### Delivery Mechanism Independence

When use cases are independent of the delivery mechanism, you can:
- Serve the same business logic through REST, GraphQL, gRPC, CLI, and WebSocket simultaneously
- Test business logic without HTTP
- Migrate from one web framework to another by rewriting only the outer circle

### Multiple Delivery Mechanisms

```
REST Controller ----\
                     \
GraphQL Resolver ------> Use Case Interactor ---> Entity
                     /
CLI Command --------/
Message Handler ---/
```

Each delivery mechanism is an adapter in the outer circle. They all call the same Use Case Input Port. The business logic is written once and exposed through as many delivery mechanisms as needed.

## Plugin Architecture

The ultimate expression of Clean Architecture is the plugin architecture: the business rules are the core application, and everything else (database, web framework, external services, UI) is a plugin that connects to the core.

### How Plugins Work

1. **The core defines interfaces** (ports) that describe what it needs from the outside world
2. **Plugins implement those interfaces** using specific technologies
3. **Main assembles the plugins** and injects them into the core at startup
4. **The core never knows which plugins are attached** -- it only knows the interfaces

### The Main Component

Main is the dirtiest, most concrete component in the system. It knows about everything because it must instantiate and wire all the pieces together. But nothing depends on Main.

```python
# main.py -- the composition root
def create_app():
    # Concrete infrastructure
    db_pool = create_connection_pool(os.environ["DATABASE_URL"])
    email_client = SendGridClient(os.environ["SENDGRID_API_KEY"])

    # Gateways (implement interfaces)
    order_repo = PostgresOrderRepository(db_pool)
    email_service = SendGridEmailService(email_client)

    # Presenters
    order_presenter = JsonOrderPresenter()

    # Use Cases (wired with concrete dependencies)
    place_order = PlaceOrderInteractor(order_repo, order_presenter)
    cancel_order = CancelOrderInteractor(order_repo, email_service, order_presenter)

    # Controllers (wired with use cases)
    order_controller = OrderController(place_order, cancel_order)

    # Framework wiring
    app = Flask(__name__)
    app.route("/orders", methods=["POST"])(order_controller.create)
    app.route("/orders/<id>/cancel", methods=["POST"])(order_controller.cancel)

    return app
```

Main is the only place where the concrete classes from all circles come together. If you want to swap PostgreSQL for DynamoDB, you change Main and add a `DynamoOrderRepository`. No other file changes.

### Plugin Swappability in Practice

| Plugin | Interface | Implementation A | Implementation B |
|--------|-----------|-----------------|-----------------|
| **Persistence** | `OrderRepository` | `PostgresOrderRepository` | `DynamoOrderRepository` |
| **Email** | `EmailService` | `SendGridEmailService` | `SesEmailService` |
| **Payment** | `PaymentGateway` | `StripeGateway` | `BraintreeGateway` |
| **Search** | `ProductSearch` | `ElasticsearchProductSearch` | `AlgoliaProductSearch` |
| **Cache** | `CacheStore` | `RedisCacheStore` | `MemcachedCacheStore` |
| **File storage** | `FileStore` | `S3FileStore` | `LocalFileStore` |

Each swap is a single line change in Main plus a new implementation class. No business logic changes. No use case changes. No entity changes. This is the power of treating frameworks and infrastructure as plugins.

## Keeping Frameworks at Arm's Length

### The Wrapper Strategy

When a framework provides something useful but you don't want to couple to it directly, wrap it:

```python
# Interface in inner circle
class Clock(ABC):
    @abstractmethod
    def now(self) -> datetime:
        pass

# Wrapper in outer circle
class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.utcnow()

# Test double
class FakeClock(Clock):
    def __init__(self, fixed_time: datetime):
        self._time = fixed_time

    def now(self) -> datetime:
        return self._time
```

Now your business logic depends on `Clock` (an interface you control), not on `datetime.utcnow()` (a library call you don't control). You can test time-dependent logic deterministically.

### When NOT to Wrap

Not everything needs a wrapper. Apply the rule pragmatically:

- **Standard library types** (strings, lists, dates as data): Don't wrap. They are stable and ubiquitous.
- **Utility functions with no side effects**: Don't wrap `math.ceil()` or `json.dumps()`.
- **Anything with I/O or side effects** (database, network, filesystem, clock, random): Wrap it.
- **Anything from a framework you might swap**: Wrap it.

The test is: "Would I need to mock this in a test?" If yes, wrap it behind an interface.
