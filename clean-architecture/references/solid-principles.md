# SOLID Principles

The SOLID principles are five design principles for managing dependencies at the class and module level. They were assembled and named by Robert C. Martin in the early 2000s, drawing on decades of software engineering wisdom. In Clean Architecture, SOLID principles serve as the mid-level building blocks that make the Dependency Rule possible. Without SOLID, the concentric circles would leak and the boundaries would crumble.

This reference covers each principle with definitions, code examples, common violations, and practical application guidance.


## Table of Contents
1. [SRP: The Single Responsibility Principle](#srp-the-single-responsibility-principle)
2. [OCP: The Open-Closed Principle](#ocp-the-open-closed-principle)
3. [LSP: The Liskov Substitution Principle](#lsp-the-liskov-substitution-principle)
4. [ISP: The Interface Segregation Principle](#isp-the-interface-segregation-principle)
5. [DIP: The Dependency Inversion Principle](#dip-the-dependency-inversion-principle)

---

## SRP: The Single Responsibility Principle

**"A module should have one, and only one, reason to change."**

More precisely: a module should be responsible to one, and only one, actor (a group of users or stakeholders who want the system to change in the same way).

### Understanding SRP

SRP is commonly misunderstood as "a function should do one thing." That's a good principle for functions, but SRP operates at a higher level. SRP says that the module (class) should serve one actor -- one group of people who would request changes.

### Classic Violation

```python
class Employee:
    def calculate_pay(self) -> Money:
        # Serves the CFO / accounting department
        regular_hours = self._get_regular_hours()
        overtime = self._get_overtime_hours()
        return regular_hours * self.hourly_rate + overtime * self.hourly_rate * 1.5

    def report_hours(self) -> HoursReport:
        # Serves the COO / operations department
        return HoursReport(
            regular=self._get_regular_hours(),
            overtime=self._get_overtime_hours(),
        )

    def save(self) -> None:
        # Serves the CTO / database administrators
        db.execute("INSERT INTO employees ...", self._to_dict())

    def _get_regular_hours(self) -> float:
        # Shared by calculate_pay and report_hours -- dangerous coupling
        return min(self.hours_worked, 40)

    def _get_overtime_hours(self) -> float:
        return max(self.hours_worked - 40, 0)
```

**The problem:** Three actors (CFO, COO, CTO) all have reasons to change this class. When the CFO wants to change how overtime is calculated, the shared `_get_regular_hours` method might be modified in a way that breaks the COO's reports.

### SRP-Compliant Design

```python
class PayCalculator:
    """Serves the CFO / accounting"""
    def calculate_pay(self, employee_data: EmployeeData) -> Money:
        regular = min(employee_data.hours_worked, 40)
        overtime = max(employee_data.hours_worked - 40, 0)
        return regular * employee_data.rate + overtime * employee_data.rate * 1.5

class HoursReporter:
    """Serves the COO / operations"""
    def report_hours(self, employee_data: EmployeeData) -> HoursReport:
        return HoursReport(
            regular=min(employee_data.hours_worked, 40),
            overtime=max(employee_data.hours_worked - 40, 0),
        )

class EmployeeRepository:
    """Serves the CTO / database administration"""
    def save(self, employee_data: EmployeeData) -> None:
        self._db.execute("INSERT INTO employees ...", employee_data.to_dict())
```

Each class now serves one actor. Changes requested by the CFO only affect `PayCalculator`. The COO's changes only affect `HoursReporter`. They can evolve independently.

### SRP Indicators

| Indicator | Likely Violation |
|-----------|-----------------|
| Class has methods serving different departments/teams | Multiple actors |
| "And" in the class name (`OrderValidatorAndNotifier`) | Multiple responsibilities |
| Class changes frequently for unrelated reasons | Multiple change drivers |
| Merge conflicts from unrelated feature branches | Multiple actors modifying same class |
| Unit tests require many unrelated mocks | Class does too many things |

## OCP: The Open-Closed Principle

**"A software artifact should be open for extension but closed for modification."**

You should be able to extend the behavior of a system without modifying existing code. New features are added by writing new code, not by changing old code.

### The Strategy Pattern Approach

```python
# Closed for modification -- this code doesn't change when new shipping methods are added
class OrderService:
    def __init__(self, shipping_strategy: ShippingStrategy):
        self._shipping = shipping_strategy

    def calculate_total(self, order: Order) -> Money:
        subtotal = order.subtotal()
        shipping = self._shipping.calculate(order)
        return subtotal + shipping

# Open for extension -- add new shipping methods without touching OrderService
class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, order: Order) -> Money:
        pass

class StandardShipping(ShippingStrategy):
    def calculate(self, order: Order) -> Money:
        return Money("5.99")

class ExpressShipping(ShippingStrategy):
    def calculate(self, order: Order) -> Money:
        return Money("14.99")

# New shipping method -- no existing code modified
class FreeShippingOver50(ShippingStrategy):
    def calculate(self, order: Order) -> Money:
        return Money("0.00") if order.subtotal() >= Money("50.00") else Money("5.99")
```

### Common OCP Violations

```python
# VIOLATION: Adding a new payment method requires modifying this function
def process_payment(method: str, amount: Money) -> PaymentResult:
    if method == "credit_card":
        return charge_credit_card(amount)
    elif method == "paypal":
        return charge_paypal(amount)
    elif method == "apple_pay":  # New method = new elif = modification
        return charge_apple_pay(amount)
```

**Fix with OCP:**

```python
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: Money) -> PaymentResult:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process(self, amount: Money) -> PaymentResult:
        return self._gateway.charge(amount)

# Adding Apple Pay = new class, no modification to existing code
class ApplePayProcessor(PaymentProcessor):
    def process(self, amount: Money) -> PaymentResult:
        return self._apple_client.charge(amount)
```

### OCP in Clean Architecture

OCP is foundational to the concentric circles model. The inner circles (entities, use cases) are closed for modification. The outer circles (adapters, frameworks) are open for extension. You extend the system by adding new adapters, new controllers, new gateways -- not by modifying business rules.

## LSP: The Liskov Substitution Principle

**"Subtypes must be substitutable for their base types."**

If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering the correctness of the program.

### The Classic Violation: Square/Rectangle

```python
class Rectangle:
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height

    def set_width(self, w: float) -> None:
        self._width = w

    def set_height(self, h: float) -> None:
        self._height = h

    def area(self) -> float:
        return self._width * self._height

class Square(Rectangle):
    def set_width(self, w: float) -> None:
        self._width = w
        self._height = w  # Must keep square invariant

    def set_height(self, h: float) -> None:
        self._width = h  # Must keep square invariant
        self._height = h
```

**The problem:** Code that works correctly with `Rectangle` breaks with `Square`:

```python
def test_area(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect.area() == 20  # Fails for Square! Area is 16 because set_height changed width
```

`Square` is NOT substitutable for `Rectangle`. LSP is violated.

### LSP in Practice

| Violation Pattern | Why It Breaks | Fix |
|-------------------|--------------|-----|
| Subclass throws unexpected exceptions | Callers don't handle exceptions they didn't expect from the base type | Subclass should honor the base type's exception contract |
| Subclass ignores methods (no-op override) | Callers rely on the method doing something | The class hierarchy is wrong; use composition or a different abstraction |
| Subclass strengthens preconditions | Callers that work with base type fail with subtype | Subtypes may weaken preconditions, never strengthen them |
| Subclass weakens postconditions | Callers expect guarantees the subtype doesn't provide | Subtypes may strengthen postconditions, never weaken them |

### LSP and Interfaces in Clean Architecture

LSP applies to interfaces as well as inheritance hierarchies. When a Use Case depends on `OrderRepository`, every implementation (`PostgresOrderRepository`, `MongoOrderRepository`, `InMemoryOrderRepository`) must behave consistently:

- `save()` must persist the entity (or fail with a defined exception)
- `find_by_id()` must return the entity if it exists or `None` if not
- No implementation should silently drop data, return stale data, or throw exceptions not defined in the interface contract

## ISP: The Interface Segregation Principle

**"No client should be forced to depend on methods it does not use."**

Fat interfaces create unnecessary coupling. When a client depends on an interface with methods it doesn't use, it becomes vulnerable to changes in those unused methods.

### Classic Violation

```python
class MultiFunctionDevice(ABC):
    @abstractmethod
    def print_document(self, doc: Document) -> None: pass

    @abstractmethod
    def scan_document(self) -> Image: pass

    @abstractmethod
    def fax_document(self, doc: Document, number: str) -> None: pass

    @abstractmethod
    def staple_pages(self, pages: list[Page]) -> None: pass

# A simple printer must implement fax and staple -- methods it can't fulfill
class SimplePrinter(MultiFunctionDevice):
    def print_document(self, doc: Document) -> None:
        # Actually prints
        ...

    def scan_document(self) -> Image:
        raise NotSupportedError()  # ISP violation!

    def fax_document(self, doc: Document, number: str) -> None:
        raise NotSupportedError()  # ISP violation!

    def staple_pages(self, pages: list[Page]) -> None:
        raise NotSupportedError()  # ISP violation!
```

### ISP-Compliant Design

```python
class Printer(ABC):
    @abstractmethod
    def print_document(self, doc: Document) -> None: pass

class Scanner(ABC):
    @abstractmethod
    def scan_document(self) -> Image: pass

class FaxMachine(ABC):
    @abstractmethod
    def fax_document(self, doc: Document, number: str) -> None: pass

# Simple printer only implements what it can do
class SimplePrinter(Printer):
    def print_document(self, doc: Document) -> None:
        ...

# Multi-function device implements all relevant interfaces
class OfficePrinter(Printer, Scanner, FaxMachine):
    def print_document(self, doc: Document) -> None: ...
    def scan_document(self) -> Image: ...
    def fax_document(self, doc: Document, number: str) -> None: ...
```

### ISP in Clean Architecture

ISP directly supports the Dependency Rule. Use Cases define narrow, focused input and output port interfaces. Each adapter implements only the interfaces it needs:

```python
# Focused interfaces (ISP-compliant)
class OrderReader(ABC):
    @abstractmethod
    def find_by_id(self, order_id: str) -> Order | None: pass

class OrderWriter(ABC):
    @abstractmethod
    def save(self, order: Order) -> None: pass

class OrderSearcher(ABC):
    @abstractmethod
    def search(self, criteria: SearchCriteria) -> list[Order]: pass

# Use Case that only reads doesn't depend on write methods
class GetOrderDetailsInteractor:
    def __init__(self, reader: OrderReader):  # Only depends on reading
        self._reader = reader
```

## DIP: The Dependency Inversion Principle

**"High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions."**

DIP is the mechanism that makes the Dependency Rule work. It inverts the natural direction of source code dependencies so that the volatile, concrete, outer-circle code depends on the stable, abstract, inner-circle code.

### Without DIP (Natural Dependencies)

```
OrderService --> PostgresDatabase
  (high-level)     (low-level)
```

The high-level policy (OrderService) depends on the low-level detail (PostgresDatabase). Changing the database means changing the service.

### With DIP (Inverted Dependencies)

```
OrderService --> OrderRepository (interface)
                       ^
                       |
              PostgresOrderRepository
```

Both the high-level service and the low-level database adapter depend on the abstraction (OrderRepository). The abstraction is defined by the high-level module, not by the low-level module.

### DIP Implementation Pattern

```python
# HIGH-LEVEL MODULE defines the abstraction
class OrderRepository(ABC):
    """Defined in the Use Case circle. The high-level policy dictates what it needs."""
    @abstractmethod
    def save(self, order: Order) -> None: pass

    @abstractmethod
    def find_by_id(self, order_id: str) -> Order | None: pass

# HIGH-LEVEL MODULE uses the abstraction
class PlaceOrderInteractor:
    def __init__(self, repo: OrderRepository):  # Depends on abstraction
        self._repo = repo

    def execute(self, request: PlaceOrderRequest) -> None:
        order = Order.create(request.items, request.customer_id)
        self._repo.save(order)  # Calls abstraction

# LOW-LEVEL MODULE implements the abstraction
class PostgresOrderRepository(OrderRepository):  # Depends on abstraction
    def __init__(self, pool):
        self._pool = pool

    def save(self, order: Order) -> None:
        # SQL details here -- low-level
        ...

# COMPOSITION ROOT wires them together
def main():
    pool = create_pool(DATABASE_URL)
    repo = PostgresOrderRepository(pool)
    interactor = PlaceOrderInteractor(repo)  # Inject concrete into abstract slot
```

### DIP: Who Owns the Interface?

This is the critical insight: **the interface belongs to the high-level module, not the low-level module.**

| Ownership | Meaning | Result |
|-----------|---------|--------|
| Interface owned by high-level module | The Use Case defines what it needs | Low-level module adapts to high-level needs |
| Interface owned by low-level module | The database defines its capabilities | High-level module must adapt to database -- dependency NOT inverted |

When the Use Case defines `OrderRepository`, it specifies methods like `save(order)` and `find_by_id(id)` -- business-oriented operations. The database adapter must conform to this business-oriented interface.

When the database adapter defines the interface, it specifies methods like `execute_query(sql)` and `fetch_rows(table)` -- technology-oriented operations. The Use Case must conform to the database's way of thinking. This is the natural dependency direction, NOT inverted.

### Common DIP Violations

| Violation | Example | Fix |
|-----------|---------|-----|
| Importing concrete classes in high-level modules | `from stripe import StripeClient` in Use Case | Define `PaymentGateway` interface in Use Case; implement with Stripe in adapter |
| Using static/global factory methods | `Database.get_instance()` in Use Case | Inject repository through constructor |
| Depending on framework types in domain | `@Autowired` on domain class | Use plain constructor injection; wire in Main |
| Low-level module defines the interface | `IStripeGateway` lives in the Stripe adapter package | Move interface to Use Case package; rename to `PaymentGateway` |
| New operator in high-level code | `repo = PostgresRepository()` inside Use Case | Inject through constructor; instantiate in Main |

### DIP and Clean Architecture

DIP is the engine of Clean Architecture. Every boundary in the concentric circles model is maintained through dependency inversion:

- **Use Case to Database:** `OrderRepository` interface (defined by Use Case) inverts the dependency so the database adapter depends inward
- **Use Case to Web:** `PlaceOrderOutput` interface (defined by Use Case) inverts the dependency so the presenter depends inward
- **Use Case to External Service:** `EmailService` interface (defined by Use Case) inverts the dependency so the email adapter depends inward

Without DIP, inner circles would depend on outer circles, the Dependency Rule would be violated, and the architecture would collapse into a ball of mud.
