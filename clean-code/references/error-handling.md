# Error Handling

Comprehensive guide to writing clean error handling that keeps business logic readable. Based on Robert C. Martin's *Clean Code*, Chapter 7.


## Table of Contents
1. [The Core Problem](#the-core-problem)
2. [Use Exceptions, Not Return Codes](#use-exceptions-not-return-codes)
3. [Write Your Try-Catch-Finally Statement First](#write-your-try-catch-finally-statement-first)
4. [Use Unchecked Exceptions](#use-unchecked-exceptions)
5. [Provide Context with Exceptions](#provide-context-with-exceptions)
6. [Define Exception Classes in Terms of the Caller's Needs](#define-exception-classes-in-terms-of-the-callers-needs)
7. [Don't Return Null](#dont-return-null)
8. [Don't Pass Null](#dont-pass-null)
9. [Error Handling Patterns Summary](#error-handling-patterns-summary)
10. [Common Error Handling Anti-Patterns](#common-error-handling-anti-patterns)

---

## The Core Problem

Error handling is important, but if it obscures logic, it's wrong. Code that mixes business logic with error handling is hard to read, test, and maintain. The goal is to write code where the happy path reads cleanly and error handling is a separate, well-organized concern.

---

## Use Exceptions, Not Return Codes

Return codes force the caller to check immediately after the call, cluttering the calling code with error-checking logic.

### Before: Return Codes

```java
// BAD: Error checking clutters the logic
public class DeviceController {
    public void sendShutDown() {
        DeviceHandle handle = getHandle(DEV1);
        if (handle != DeviceHandle.INVALID) {
            DeviceRecord record = retrieveDeviceRecord(handle);
            if (record.getStatus() != DEVICE_SUSPENDED) {
                pauseDevice(handle);
                clearDeviceWorkQueue(handle);
                closeDevice(handle);
            } else {
                logger.log("Device suspended. Unable to shut down.");
            }
        } else {
            logger.log("Invalid handle for: " + DEV1.toString());
        }
    }
}
```

### After: Exceptions

```java
// GOOD: Business logic is clean; errors handled separately
public class DeviceController {
    public void sendShutDown() {
        try {
            tryToShutDown();
        } catch (DeviceShutDownError e) {
            logger.log(e);
        }
    }

    private void tryToShutDown() throws DeviceShutDownError {
        DeviceHandle handle = getHandle(DEV1);
        DeviceRecord record = retrieveDeviceRecord(handle);
        pauseDevice(handle);
        clearDeviceWorkQueue(handle);
        closeDevice(handle);
    }
}
```

The business logic (shut down sequence) is now visible without wading through error checks.

---

## Write Your Try-Catch-Finally Statement First

Try-catch blocks define a scope within your program. The code in the `try` block can abort at any point and resume in the `catch`. This makes try blocks like transactions: the `catch` must leave the program in a consistent state.

**Practice:** When writing code that could throw exceptions, start with the try-catch-finally. This helps you define what the caller can expect, regardless of what goes wrong.

```python
# Start with the structure
def load_configuration(path):
    try:
        content = read_file(path)
        config = parse_yaml(content)
        validate_config(config)
        return config
    except FileNotFoundError:
        return default_configuration()
    except ParseError as e:
        raise ConfigurationError(f"Invalid config at {path}: {e}")
    finally:
        log_config_load_attempt(path)
```

---

## Use Unchecked Exceptions

Checked exceptions (Java's `throws` clause) violate the Open/Closed Principle. If you throw a checked exception from a low-level function, every function in the call chain between the throw and the catch must declare that exception. A single change at a low level forces signature changes all the way up.

| Aspect | Checked exceptions | Unchecked exceptions |
|--------|-------------------|---------------------|
| **Coupling** | Every caller must declare or catch | Only relevant callers catch |
| **Encapsulation** | Low-level details leak to high-level | Abstraction layers maintained |
| **Refactoring** | Adding new exception type cascades changes | New exceptions don't affect existing callers |
| **When appropriate** | Critical library APIs where caller MUST handle | Application code, most library code |

**In practice:** Use unchecked exceptions for application code. The cost of checked exceptions in dependency management outweighs their documentary benefit.

---

## Provide Context with Exceptions

Each exception should provide enough context to determine the source and location of the error.

### What to Include

| Context element | Why | Example |
|----------------|-----|---------|
| **Operation that failed** | Identifies what was attempted | "Failed to save invoice" |
| **Input that caused failure** | Enables reproduction | "Invoice #1234 for customer 'Acme'" |
| **Constraint that was violated** | Explains why it failed | "Total amount exceeds maximum of $1,000,000" |
| **Suggested recovery** | Helps caller respond | "Retry after 30 seconds" or "Check network connection" |

### Implementation Pattern

```python
# BAD: No context
raise ValueError("Invalid input")

# BAD: Raw technical error
raise Exception(str(e))

# GOOD: Contextual error message
raise InvoiceValidationError(
    f"Cannot create invoice for customer '{customer.name}': "
    f"requested amount ${amount:.2f} exceeds credit limit "
    f"of ${customer.credit_limit:.2f}"
)
```

### Custom Exception Classes

```python
class OrderError(Exception):
    """Base exception for order processing."""
    pass

class InsufficientInventoryError(OrderError):
    def __init__(self, product, requested, available):
        self.product = product
        self.requested = requested
        self.available = available
        super().__init__(
            f"Cannot fulfill order: {product.name} has "
            f"{available} units available, {requested} requested"
        )

class PaymentDeclinedError(OrderError):
    def __init__(self, order, reason):
        self.order = order
        self.reason = reason
        super().__init__(
            f"Payment declined for order #{order.id}: {reason}"
        )
```

---

## Define Exception Classes in Terms of the Caller's Needs

When wrapping a third-party API, define exception classes based on how the caller will handle them, not based on the types of errors the API throws.

### Before: Mirroring Third-Party Exceptions

```java
// BAD: Caller must handle every possible vendor exception
try {
    port.open();
} catch (DeviceResponseException e) {
    reportPortError(e);
    logger.log("Device response exception", e);
} catch (ATM1212UnlockedException e) {
    reportPortError(e);
    logger.log("Unlock exception", e);
} catch (GMXError e) {
    reportPortError(e);
    logger.log("Device response exception");
}
```

### After: Wrapping by Caller's Needs

```java
// GOOD: Single exception class wraps all vendor exceptions
public class LocalPort {
    private ACMEPort innerPort;

    public void open() {
        try {
            innerPort.open();
        } catch (DeviceResponseException e) {
            throw new PortDeviceFailure(e);
        } catch (ATM1212UnlockedException e) {
            throw new PortDeviceFailure(e);
        } catch (GMXError e) {
            throw new PortDeviceFailure(e);
        }
    }
}

// Caller only handles one type
try {
    port.open();
} catch (PortDeviceFailure e) {
    reportError(e);
    logger.log(e.getMessage(), e);
}
```

**Benefits of wrapping:**
- Minimizes dependencies on the third-party API
- Makes it easy to swap vendors
- Simplifies testing with mocks
- Keeps caller code clean

---

## Don't Return Null

Returning null from a method is an invitation for NullPointerExceptions. Every null return forces every caller to add a null check, and a single missed check crashes the application.

### Alternatives to Returning Null

| Instead of null | Return this | When |
|----------------|-------------|------|
| Null collection | Empty collection | Method returns a list, set, or map |
| Null string | Empty string `""` | Method returns text |
| Null object | Special case object | Object has default behavior |
| Null optional value | `Optional.empty()` | Value may legitimately be absent |
| Null on error | Throw exception | Absence indicates a problem |

### The Special Case Pattern

Instead of checking for null to handle a special case, create an object that handles the special case.

```python
# BAD: Null checks everywhere
def get_expenses(employee):
    expenses = db.find_expenses(employee)
    if expenses is None:
        return 0
    total = 0
    for expense in expenses:
        if expense is not None:
            total += expense.amount if expense.amount is not None else 0
    return total

# GOOD: No null checks needed
def get_expenses(employee):
    expenses = db.find_expenses(employee)  # Returns empty list, never None
    return sum(expense.amount for expense in expenses)
```

### Null Object Pattern

```python
class RealUser:
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions

    def has_permission(self, action):
        return action in self.permissions

class GuestUser:
    """Null Object -- behaves like a user with no permissions."""
    name = "Guest"
    permissions = frozenset()

    def has_permission(self, action):
        return False

def find_user(user_id):
    user = db.find(user_id)
    return user if user else GuestUser()

# Caller never needs to check for null
user = find_user(request.user_id)
if user.has_permission("edit"):
    allow_edit()
```

---

## Don't Pass Null

Returning null is bad. Passing null is worse. When you pass null as an argument, you are creating a requirement for the callee to check for null, and if they don't, you get a runtime error.

```java
// BAD: What should this do with null?
public double calculateMetric(Point p1, Point p2) {
    return Math.sqrt(
        Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2)
    );
}

// If someone calls calculateMetric(null, new Point(1, 2)) -- NullPointerException

// GOOD: Fail fast with clear message
public double calculateMetric(Point p1, Point p2) {
    Objects.requireNonNull(p1, "p1 must not be null");
    Objects.requireNonNull(p2, "p2 must not be null");
    return Math.sqrt(
        Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2)
    );
}
```

**The best policy:** Forbid passing null by default. Use static analysis tools (`@NonNull`, `@Nullable` annotations) and code review to enforce this.

---

## Error Handling Patterns Summary

| Pattern | When to use | Benefit |
|---------|-------------|---------|
| **Try-catch-finally first** | Any code that could fail | Defines transaction boundary upfront |
| **Wrap third-party APIs** | Calling external libraries | Isolates vendor dependencies |
| **Special Case pattern** | Default behavior for missing data | Eliminates null/error checks in callers |
| **Null Object pattern** | Polymorphic default behavior | No null checks in calling code |
| **Guard clauses** | Input validation | Fail fast with clear messages |
| **Custom exception hierarchy** | Domain-specific errors | Caller handles by intent, not implementation |
| **Exception with context** | All thrown exceptions | Enables diagnosis without debugging |
| **Empty over null** | Collections, strings, optionals | Eliminates NullPointerException risk |

---

## Common Error Handling Anti-Patterns

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| **Catch-and-ignore** | `catch (Exception e) { }` -- swallows all errors silently | At minimum log; usually re-throw or handle specifically |
| **Catch-and-log-and-rethrow** | Duplicates logging at every level | Catch at one level, let others propagate |
| **Returning error codes** | Forces immediate checking, clutters happy path | Use exceptions |
| **Returning -1 or sentinel values** | Magic values that callers forget to check | Use Optional or throw |
| **Exception for control flow** | Using try-catch instead of if-else for expected conditions | Use exceptions only for exceptional situations |
| **Overly broad catch** | `catch (Exception e)` catches bugs too | Catch specific exception types |
| **Nested try-catch** | Multiple try blocks in one function | Extract each try block into its own function |
| **Throws declaration cascade** | Checked exceptions forcing changes up the call stack | Use unchecked exceptions for application errors |
