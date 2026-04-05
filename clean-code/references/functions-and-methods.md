# Functions and Methods

Comprehensive guide to writing small, focused functions that do one thing well. Based on Robert C. Martin's *Clean Code*, Chapters 3 and 4.


## Table of Contents
1. [The First Rule of Functions](#the-first-rule-of-functions)
2. [Do One Thing](#do-one-thing)
3. [Function Arguments](#function-arguments)
4. [Flag Arguments](#flag-arguments)
5. [Command-Query Separation](#command-query-separation)
6. [Side Effects](#side-effects)
7. [Extract Till You Drop](#extract-till-you-drop)
8. [Structured Programming](#structured-programming)
9. [DRY: Don't Repeat Yourself](#dry-dont-repeat-yourself)
10. [Function Organization Within a Class](#function-organization-within-a-class)
11. [Common Function Anti-Patterns](#common-function-anti-patterns)

---

## The First Rule of Functions

**Functions should be small.** The second rule of functions is that they should be smaller than that.

A well-written function:
- Fits on one screen (ideally 4-10 lines)
- Has a name that describes exactly what it does
- Takes few arguments (zero is best, three is the maximum)
- Has no side effects
- Operates at a single level of abstraction

---

## Do One Thing

**Functions should do one thing. They should do it well. They should do it only.**

### How to Know if a Function Does One Thing

If you can extract another function from it with a name that is not merely a restatement of its implementation, the function does more than one thing.

```python
# BAD: Does three things
def process_payment(order):
    # 1. Validate
    if not order.items:
        raise ValueError("Empty order")
    if order.total <= 0:
        raise ValueError("Invalid total")

    # 2. Charge
    payment_result = gateway.charge(order.customer.card, order.total)
    if not payment_result.success:
        raise PaymentError(payment_result.error)

    # 3. Notify
    email_service.send_receipt(order.customer.email, order)
    analytics.track("payment_completed", order.id)

# GOOD: Does one thing, delegates details
def process_payment(order):
    validate_order(order)
    charge_customer(order)
    send_notifications(order)
```

### The Step-Down Rule

Code should read like a top-down narrative. Every function should be followed by the next level of abstraction.

```
To process a payment:
    We validate the order.
    We charge the customer.
    We send notifications.

To validate the order:
    We check it has items.
    We check the total is positive.

To charge the customer:
    We call the payment gateway.
    We handle any payment failure.

To send notifications:
    We email the receipt.
    We track the analytics event.
```

This reads like a newspaper: the headline (top-level function) tells you the story, and each successive paragraph (sub-function) provides more detail.

---

## Function Arguments

The ideal number of arguments for a function is zero (niladic). Next comes one (monadic), followed closely by two (dyadic). Three arguments (triadic) should be avoided where possible. More than three (polyadic) requires very special justification.

### Argument Count Guide

| Count | Name | When acceptable | Example |
|-------|------|-----------------|---------|
| **0** | Niladic | Simple operations | `getCurrentTime()` |
| **1** | Monadic | Asking a question or transforming input | `isValid(email)`, `parse(json)` |
| **2** | Dyadic | Natural pairings | `Point(x, y)`, `assertEquals(expected, actual)` |
| **3** | Triadic | Rarely; consider object | `Color(r, g, b)` |
| **4+** | Polyadic | Almost never | Wrap in object: `new Config(...)` |

### Common Monadic Forms

Three common reasons to pass a single argument:

1. **Asking a question:** `boolean fileExists(path)` -- returns true/false about the argument
2. **Transforming it:** `InputStream fileOpen(path)` -- transforms the argument and returns the result
3. **Event:** `void passwordAttemptFailedNTimes(attempts)` -- uses the argument to alter system state (make this clear from the name)

### Why Many Arguments Are Problematic

```java
// BAD: What does each argument mean? What order?
createReport(title, startDate, endDate, format, includeCharts, sendEmail, recipients);

// GOOD: Parameter object groups related arguments
ReportConfig config = new ReportConfig.Builder()
    .title("Q4 Revenue")
    .dateRange(startDate, endDate)
    .format(PDF)
    .includeCharts(true)
    .build();
createReport(config);
```

Each argument increases the difficulty of understanding, testing, and calling the function. Arguments also create ordering dependencies that the reader must memorize.

---

## Flag Arguments

**Flag arguments are ugly.** Passing a boolean into a function loudly declares that the function does two things -- one thing if the flag is true, another if false.

```python
# BAD: Flag argument
def render(document, is_for_print):
    if is_for_print:
        # 20 lines of print rendering
        ...
    else:
        # 20 lines of screen rendering
        ...

# GOOD: Two clearly named functions
def render_for_print(document):
    ...

def render_for_screen(document):
    ...
```

If a function must behave differently based on a condition, split it into two named functions. If the behaviors share logic, extract the shared part into a private helper.

---

## Command-Query Separation

Functions should either do something (command) or answer something (query), but not both.

```java
// BAD: Does this set the attribute or check if it exists?
if (set("username", "unclebob")) { ... }

// GOOD: Separate query from command
if (attributeExists("username")) {
    setAttribute("username", "unclebob");
}
```

**Commands** change the state of an object. They should return void.
**Queries** return information about an object. They should not change state.

When a function both changes state and returns a value, the reader cannot tell from the call site what is happening.

---

## Side Effects

A side effect is when a function promises to do one thing but also does other hidden things.

### Common Hidden Side Effects

| Declared purpose | Hidden side effect | Danger |
|-----------------|-------------------|--------|
| `checkPassword(user, password)` | Initializes a session | Calling "check" unexpectedly logs user in |
| `getUser(id)` | Creates user if not found | "Get" implies read-only; caller doesn't expect writes |
| `toString()` | Modifies internal state | Debugging with print statements changes behavior |
| `validate(input)` | Sends analytics event | Validation during testing triggers real events |

### How to Fix Side Effects

1. **Make the side effect explicit in the name:** `checkPasswordAndInitSession()`
2. **Separate the concerns:** `checkPassword()` + `initSession()` as two calls
3. **Prefer option 2** -- separation makes testing easier and keeps functions honest

---

## Extract Till You Drop

If you can extract a named function from a block of code, you should. The extracted function's name adds documentation value, even if the function is only called from one place.

### When to Extract

| Signal | Action |
|--------|--------|
| A block inside an `if`, `else`, `for`, or `while` | Extract to named function |
| A comment explaining what the next lines do | Replace comment with named function |
| A function longer than 10 lines | Look for extraction opportunities |
| Nested indentation deeper than 2 levels | Extract inner blocks |
| Code that you'd need to re-read to understand | Name it so you don't have to |

### Extraction Example

```typescript
// BEFORE: Deeply nested, hard to follow
function processOrders(orders: Order[]) {
  for (const order of orders) {
    if (order.status === 'pending') {
      let total = 0;
      for (const item of order.items) {
        if (item.inStock) {
          total += item.price * item.quantity;
          if (item.quantity > 10) {
            total *= 0.9; // bulk discount
          }
        }
      }
      if (total > 0) {
        order.total = total;
        order.status = 'processed';
        db.save(order);
        emailService.sendConfirmation(order);
      }
    }
  }
}

// AFTER: Each function does one thing
function processOrders(orders: Order[]) {
  orders
    .filter(isPending)
    .forEach(processOrder);
}

function processOrder(order: Order) {
  const total = calculateOrderTotal(order);
  if (total > 0) {
    finalizeOrder(order, total);
  }
}

function calculateOrderTotal(order: Order): number {
  return order.items
    .filter(item => item.inStock)
    .reduce((sum, item) => sum + calculateItemPrice(item), 0);
}

function calculateItemPrice(item: Item): number {
  const basePrice = item.price * item.quantity;
  return item.quantity > BULK_DISCOUNT_THRESHOLD
    ? basePrice * BULK_DISCOUNT_RATE
    : basePrice;
}

function finalizeOrder(order: Order, total: number) {
  order.total = total;
  order.status = 'processed';
  db.save(order);
  emailService.sendConfirmation(order);
}
```

---

## Structured Programming

Dijkstra's rule states that every function should have one entry and one exit: one `return` statement, no `break` or `continue` in loops, and never `goto`.

**In practice, for small functions, multiple returns and early exits improve clarity:**

```python
# Guard clauses improve readability in small functions
def calculate_discount(customer):
    if customer is None:
        return 0
    if not customer.is_active:
        return 0
    if customer.total_purchases < MINIMUM_FOR_DISCOUNT:
        return 0

    return customer.total_purchases * DISCOUNT_RATE
```

Guard clauses handle the error cases at the top of the function, leaving the happy path unindented and clear. This pattern is preferable to deeply nested `if-else` chains.

---

## DRY: Don't Repeat Yourself

Duplication is the root of all evil in software. Every piece of knowledge should have a single, unambiguous, authoritative representation in the system.

### Types of Duplication

| Type | Example | Fix |
|------|---------|-----|
| **Exact duplication** | Same code block in three places | Extract to shared function |
| **Structural duplication** | Same algorithm with different data | Template Method or Strategy pattern |
| **Conceptual duplication** | Same business rule expressed differently | Consolidate into single source of truth |
| **Data duplication** | Same value computed in multiple places | Compute once, pass result |

### The Rule of Three

The first time you write something, just write it. The second time you see duplication, note it. The third time, refactor. This avoids premature abstraction while still catching genuine duplication.

---

## Function Organization Within a Class

### The Newspaper Metaphor

Organize functions the way a newspaper organizes articles:

1. **Headline at the top:** Public methods (the API) appear first
2. **Synopsis next:** High-level private methods called by the public methods
3. **Details last:** Low-level helper functions at the bottom

The reader can stop reading at any depth once they have enough understanding.

### Vertical Distance

**Dependent functions should be close.** If one function calls another, they should be vertically close in the source file, and the caller should be above the callee.

```java
// GOOD: Caller above callee, close together
public void processOrder(Order order) {
    validateOrder(order);
    chargeCustomer(order);
    shipOrder(order);
}

private void validateOrder(Order order) {
    // validation logic
}

private void chargeCustomer(Order order) {
    // payment logic
}

private void shipOrder(Order order) {
    // shipping logic
}
```

**Variables should be declared as close to their usage as possible.** Local variables at the top of the function. Loop variables inside the loop statement. Instance variables at the top of the class (everyone needs to know they exist).

---

## Common Function Anti-Patterns

| Anti-pattern | Problem | Refactoring |
|-------------|---------|-------------|
| **Output arguments** | `appendFooter(report)` -- is `report` input or output? | Make it a method: `report.appendFooter()` |
| **Selector arguments** | `calculate(MONTHLY)` enum switches behavior | Split: `calculateMonthly()`, `calculateAnnual()` |
| **Dead functions** | Never called, just sitting there | Delete them. Version control remembers. |
| **Switch statements** | Long switches violate SRP and OCP | Replace with polymorphism or strategy pattern |
| **Temporal coupling** | Functions must be called in a specific order | Make ordering explicit through return values or builder |
| **Leaky abstraction** | Function exposes implementation details | Hide internals, return domain objects |
