# Simplifying Conditional Logic

Detailed reference for refactorings that tame complex conditional structures. Conditionals are the hardest code to read and the most likely to harbor bugs. These refactorings decompose, consolidate, and replace conditionals with clearer alternatives.

## Table of Contents
1. [Decompose Conditional](#decompose-conditional)
2. [Consolidate Conditional Expression](#consolidate-conditional-expression)
3. [Replace Nested Conditional with Guard Clauses](#replace-nested-conditional-with-guard-clauses)
4. [Replace Conditional with Polymorphism](#replace-conditional-with-polymorphism)
5. [Introduce Special Case (Null Object)](#introduce-special-case-null-object)
6. [Introduce Assertion](#introduce-assertion)
7. [Decision Guide: Which Conditional Refactoring to Use](#decision-guide-which-conditional-refactoring-to-use)

---

## Decompose Conditional

Extract the condition, the then-branch, and the else-branch of a complex conditional into well-named methods.

### Motivation

A long `if` statement with a compound condition and multi-line branches forces the reader to simulate every path mentally. By naming each part, you turn the conditional into readable prose.

### Mechanics

1. Extract the condition into a method whose name describes the meaning (not the mechanics)
2. Extract the then-body into a method whose name describes what happens
3. Extract the else-body into a method whose name describes what happens
4. Run tests

### Example

**Before:**
```javascript
function calculateCharge(date, quantity, plan) {
  let charge;
  if (date.getMonth() >= 6 && date.getMonth() <= 8) {
    charge = quantity * plan.summerRate;
  } else {
    charge = quantity * plan.regularRate + plan.regularServiceCharge;
  }
  return charge;
}
```

**After:**
```javascript
function calculateCharge(date, quantity, plan) {
  if (isSummer(date)) {
    return summerCharge(quantity, plan);
  } else {
    return regularCharge(quantity, plan);
  }
}

function isSummer(date) {
  return date.getMonth() >= 6 && date.getMonth() <= 8;
}

function summerCharge(quantity, plan) {
  return quantity * plan.summerRate;
}

function regularCharge(quantity, plan) {
  return quantity * plan.regularRate + plan.regularServiceCharge;
}
```

### Naming the Condition

| Condition Expression | Good Name |
|---------------------|-----------|
| `date.getMonth() >= 6 && date.getMonth() <= 8` | `isSummer(date)` |
| `user.age >= 18 && user.hasConsent` | `isEligible(user)` |
| `cart.total > 100 && !cart.hasPromo` | `qualifiesForDiscount(cart)` |
| `retries < MAX && !response.ok` | `shouldRetry(retries, response)` |
| `file.size > 0 && file.ext === '.csv'` | `isValidUpload(file)` |

The condition name should answer a yes/no question using the domain vocabulary.

---

## Consolidate Conditional Expression

Combine a series of conditional checks that all lead to the same result into a single conditional with a descriptive name.

### Motivation

When multiple conditions return the same value, combining them into one named check makes the logic clearer: "All of these mean the same thing -- this situation is X."

### Mechanics

1. Verify that all the conditionals have no side effects
2. Combine using logical operators (`&&`, `||`)
3. Extract the combined condition into a named method
4. Run tests

### Example

**Before:**
```python
def disability_amount(employee):
    if employee.seniority < 2:
        return 0
    if employee.months_disabled > 12:
        return 0
    if employee.is_part_time:
        return 0
    # compute disability amount...
    return base_amount * 1.5
```

**After:**
```python
def disability_amount(employee):
    if is_not_eligible_for_disability(employee):
        return 0
    return base_amount * 1.5

def is_not_eligible_for_disability(employee):
    return (employee.seniority < 2
            or employee.months_disabled > 12
            or employee.is_part_time)
```

### When to Consolidate vs. Keep Separate

| Situation | Action |
|-----------|--------|
| All conditions mean the same business concept | Consolidate into one named check |
| Conditions are independent with different reasons | Keep separate (each deserves its own name) |
| Conditions should be evaluated in sequence for performance | Keep separate for short-circuit clarity |

---

## Replace Nested Conditional with Guard Clauses

Handle special cases and edge conditions at the top of the method and return early, leaving the main path of execution flat and unindented.

### Motivation

Deeply nested `if/else` structures obscure the normal path. Guard clauses make it clear: "These are the edge cases. Now here's the main logic." The main path runs at the lowest indentation level.

### Mechanics

1. Identify each edge case or special condition
2. Move it to the top of the method as an `if (condition) return earlyValue;`
3. Remove the corresponding `else` and reduce indentation
4. Run tests

### Example

**Before:**
```javascript
function payAmount(employee) {
  let result;
  if (employee.isSeparated) {
    result = { amount: 0, reasonCode: 'SEP' };
  } else {
    if (employee.isRetired) {
      result = { amount: 0, reasonCode: 'RET' };
    } else {
      // main calculation
      result = {
        amount: employee.salary * employee.rate,
        reasonCode: 'REG'
      };
    }
  }
  return result;
}
```

**After:**
```javascript
function payAmount(employee) {
  if (employee.isSeparated) return { amount: 0, reasonCode: 'SEP' };
  if (employee.isRetired) return { amount: 0, reasonCode: 'RET' };

  return {
    amount: employee.salary * employee.rate,
    reasonCode: 'REG'
  };
}
```

### Guard Clause Patterns

| Pattern | Example |
|---------|---------|
| Null check | `if (input == null) return defaultValue;` |
| Empty check | `if (items.length === 0) return [];` |
| Permission check | `if (!user.canEdit) throw new ForbiddenError();` |
| Boundary check | `if (index < 0 \|\| index >= size) throw new RangeError();` |
| Status check | `if (order.isCancelled) return zeroPay();` |

### "One return" vs. Guard Clauses

Some coding standards mandate a single return statement per method. This leads to deeply nested conditionals and temporary result variables. Guard clauses with early returns produce clearer, flatter code. Fowler explicitly recommends guard clauses over single-return for methods with special cases.

---

## Replace Conditional with Polymorphism

Replace a conditional that checks a type, status, or category and branches to different behavior with polymorphic classes where each type provides its own implementation.

### Motivation

This is the gold standard for eliminating type-based conditionals. Instead of one function that knows about every type, each type knows about itself. Adding a new type means adding a new class -- not editing existing conditionals in multiple places (Open/Closed Principle).

### Mechanics

1. If the conditional is based on a type code, apply Replace Type Code with Subclasses first
2. Create a base method (possibly abstract) in the superclass
3. Copy each branch of the conditional into the corresponding subclass as an override
4. Remove the conditional from the superclass (or make it the default case)
5. Run tests

### Example

**Before:**
```python
class Bird:
    def __init__(self, bird_type, voltage=0, coconut_count=0):
        self.type = bird_type
        self.voltage = voltage
        self.coconut_count = coconut_count

    def speed(self):
        if self.type == 'european':
            return 35 - (self.voltage / 10)
        elif self.type == 'african':
            return 40 - (2 * self.coconut_count)
        elif self.type == 'norwegian_blue':
            return 0 if self.voltage > 100 else 10 + (self.voltage / 10)
        else:
            raise ValueError(f"Unknown bird type: {self.type}")
```

**After:**
```python
class Bird:
    def speed(self):
        raise NotImplementedError

class EuropeanSwallow(Bird):
    def speed(self):
        return 35 - (self.voltage / 10)

class AfricanSwallow(Bird):
    def speed(self):
        return 40 - (2 * self.coconut_count)

class NorwegianBlueParrot(Bird):
    def speed(self):
        return 0 if self.voltage > 100 else 10 + (self.voltage / 10)
```

### When to Use Polymorphism vs. Keep the Conditional

| Situation | Recommendation |
|-----------|---------------|
| Conditional appears in multiple methods | Polymorphism -- types know their own behavior |
| Only one method has the conditional | May be overkill -- Decompose Conditional may suffice |
| New types are added frequently | Polymorphism -- Open/Closed Principle |
| The set of types is fixed and small (e.g., 2-3) | Conditional may be simpler |
| Behavior varies by a code that changes at runtime | Use Strategy pattern instead of inheritance |

---

## Introduce Special Case (Null Object)

Instead of checking for a special case (usually null) in every caller, create a class that encapsulates the special-case behavior.

### Motivation

`if (customer == null)` checks scattered through the codebase add noise and are easy to forget. A `NullCustomer` or `UnknownCustomer` object responds to all the same methods with safe default behavior.

### Mechanics

1. Create a subclass or separate class for the special case
2. Add a method to the superclass or factory that creates the special case (e.g., `Customer.unknown()`)
3. Implement each method in the special case with the default behavior that callers currently use after their null checks
4. Change callers to use the special case object instead of null
5. Remove the null checks from callers
6. Run tests

### Example

**Before:**
```javascript
// Scattered throughout the codebase:
const customerName = (customer !== null) ? customer.name : 'Occupant';
const billingPlan = (customer !== null) ? customer.billingPlan : BillingPlan.basic();
const paymentHistory = (customer !== null) ? customer.paymentHistory : new NullPaymentHistory();
```

**After:**
```javascript
class UnknownCustomer {
  get name() { return 'Occupant'; }
  get billingPlan() { return BillingPlan.basic(); }
  get paymentHistory() { return new NullPaymentHistory(); }
  get isUnknown() { return true; }
}

class Customer {
  get isUnknown() { return false; }
  // ... normal implementation
}

// Callers (no more null checks):
const customerName = customer.name;
const billingPlan = customer.billingPlan;
```

### Common Special Cases

| Domain | Special Case Object | Default Behavior |
|--------|-------------------|------------------|
| Customer | `UnknownCustomer` | Returns "Occupant", basic plan |
| Currency | `NullMoney` | Zero amount, no currency |
| Logger | `NullLogger` | Silently discards all messages |
| Permission | `DeniedPermission` | Returns false for all checks |
| Config | `DefaultConfig` | Returns sensible defaults |
| User | `AnonymousUser` | Read-only, no privileges |

---

## Introduce Assertion

Make an assumption explicit by inserting an assertion that will fail fast if the assumption is violated.

### Motivation

Assertions document what the code expects to be true. They are executable documentation that catches bugs during development. Unlike comments, assertions are verified by the runtime.

### Mechanics

1. Identify an assumption in the code (a condition that should always be true)
2. Insert an assertion at the point where the assumption is made
3. Ensure the assertion does not have side effects
4. Run tests (they should still pass -- if an assertion fails, you found a bug)

### Example

**Before:**
```python
def apply_discount(product, discount_rate):
    # discount should be between 0 and 1
    price = product.base_price * (1 - discount_rate)
    return price
```

**After:**
```python
def apply_discount(product, discount_rate):
    assert 0 <= discount_rate <= 1, f"Discount rate must be 0-1, got {discount_rate}"
    price = product.base_price * (1 - discount_rate)
    return price
```

### Assertion Guidelines

| Guideline | Rationale |
|-----------|-----------|
| Never use assertions for input validation | Assertions can be disabled in production; use exceptions for untrusted input |
| Use assertions for programmer errors | Conditions that should never occur if the code is correct |
| Keep assertion messages descriptive | Include the actual value and the expected constraint |
| Don't put side effects in assertions | `assert items.remove(x)` breaks when assertions are disabled |

---

## Decision Guide: Which Conditional Refactoring to Use

| Situation | Refactoring |
|-----------|-------------|
| Long, complex condition expression | Decompose Conditional |
| Multiple conditions lead to same result | Consolidate Conditional Expression |
| Nested if/else with special cases | Replace Nested Conditional with Guard Clauses |
| Switch/if on type code in multiple places | Replace Conditional with Polymorphism |
| Null checks scattered everywhere | Introduce Special Case (Null Object) |
| Hidden assumption in code logic | Introduce Assertion |
| Condition appears once, set of types is small | Keep the conditional, but Decompose it |
| Condition varies at runtime | Use Strategy pattern |
