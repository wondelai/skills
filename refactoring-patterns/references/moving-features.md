# Moving Features Between Objects

Detailed reference for refactorings that redistribute responsibilities between classes. The fundamental question of object-oriented design is: where should this behavior live? These refactorings provide the mechanical steps to move things to the right place.

## Table of Contents
1. [Move Method](#move-method)
2. [Move Field](#move-field)
3. [Extract Class](#extract-class)
4. [Inline Class](#inline-class)
5. [Hide Delegate](#hide-delegate)
6. [Remove Middle Man](#remove-middle-man)
7. [Introduce Foreign Method](#introduce-foreign-method)
8. [Introduce Local Extension](#introduce-local-extension)
9. [Decision Guide: Where Does This Behavior Belong?](#decision-guide-where-does-this-behavior-belong)

---

## Move Method

Move a method to the class it uses most. A method that accesses more features of another class than its own has Feature Envy and belongs somewhere else.

### Motivation

The most common reason for moving a method is Feature Envy -- when a method spends most of its time talking to another object. Moving the method reduces coupling: the method now lives where its data lives, so changes to that data don't ripple outward.

### Mechanics

1. Examine all features (fields and methods) used by the method. Determine which class has the most features used by the method.
2. Check for related methods in the source class. If other methods also use the same target class, consider moving them together.
3. Check superclasses and subclasses for overrides or related declarations.
4. Declare the method in the target class. Copy the body and adjust references -- `this` now refers to the target; the source object may need to be passed as a parameter.
5. Turn the source method into a delegating method (call the target).
6. Run tests.
7. Consider removing the delegating method if no other callers need it.
8. Run tests.

### Example

**Before:**
```javascript
class Account {
  overdraftCharge() {
    if (this.type.isPremium()) {
      let result = 10;
      if (this.daysOverdrawn > 7) {
        result += (this.daysOverdrawn - 7) * 0.85;
      }
      return result;
    } else {
      return this.daysOverdrawn * 1.75;
    }
  }
}
```

The method depends heavily on `this.type` (an `AccountType` object). Move it there.

**After:**
```javascript
class AccountType {
  overdraftCharge(daysOverdrawn) {
    if (this.isPremium()) {
      let result = 10;
      if (daysOverdrawn > 7) {
        result += (daysOverdrawn - 7) * 0.85;
      }
      return result;
    } else {
      return daysOverdrawn * 1.75;
    }
  }
}

class Account {
  overdraftCharge() {
    return this.type.overdraftCharge(this.daysOverdrawn);
  }
}
```

### Decision Criteria

Move a method when:
- It uses more fields/methods of another class than its own
- The target class is likely to change in ways that affect this method
- Related methods already live in the target class

Don't move when:
- The method uses features from multiple classes equally (keep it in the most stable location)
- Polymorphism on the source class is needed

---

## Move Field

Move a field to the class that uses it more. Similar to Move Method but for data.

### Motivation

A field used more by another class signals that the data model is out of alignment with the behavior model. Moving the field keeps data and behavior together.

### Mechanics

1. If the field is public, encapsulate it first (Encapsulate Field)
2. Create the field in the target class with a getter and setter
3. Determine how to reference the target from the source (usually an existing association)
4. Update the source getter to delegate to the target
5. Run tests
6. Remove the field from the source class
7. Run tests

### Example

**Before:**
```python
class Customer:
    def __init__(self):
        self.discount_rate = 0.0

class Order:
    def discounted_total(self):
        return self.base_total() - (self.base_total() * self.customer.discount_rate)
```

`discount_rate` is only read by `Order` through `Customer`. If most logic involving `discount_rate` lives in the customer's pricing context, keep it in `Customer`. But if `Order` is the primary consumer and `discount_rate` is really about order pricing policy, consider moving it.

---

## Extract Class

Split a class that does two things into two classes that each do one thing.

### Motivation

A class with too many responsibilities grows too large and becomes hard to understand. If you can identify a coherent subset of fields and methods that relate to each other more than to the rest of the class, that subset deserves its own class.

### Mechanics

1. Identify the subset of responsibilities to split out
2. Create a new class named after the split-out responsibility
3. Add a link from the old class to the new class
4. Use Move Field for each field in the subset
5. Use Move Method for each method in the subset
6. Review the interfaces of both classes. Remove unneeded methods, rename as appropriate.
7. Decide whether to expose the new class or hide it behind the original
8. Run tests

### Example

**Before:**
```javascript
class Person {
  constructor() {
    this.name = '';
    this.officeAreaCode = '';
    this.officeNumber = '';
  }

  get telephoneNumber() {
    return `(${this.officeAreaCode}) ${this.officeNumber}`;
  }
}
```

**After:**
```javascript
class TelephoneNumber {
  constructor() {
    this.areaCode = '';
    this.number = '';
  }

  toString() {
    return `(${this.areaCode}) ${this.number}`;
  }
}

class Person {
  constructor() {
    this.name = '';
    this.telephoneNumber = new TelephoneNumber();
  }

  get telephone() {
    return this.telephoneNumber.toString();
  }
}
```

### Signals That Suggest Extraction

| Signal | What to Extract |
|--------|----------------|
| Field name prefix groups (e.g., `shippingStreet`, `shippingCity`) | `ShippingAddress` class |
| Methods that only use a subset of fields | The subset + its methods = new class |
| Subsets change at different rates | The faster-changing subset deserves its own class |
| Subsets have different collaborators | Each collaborator relationship = potential class boundary |

---

## Inline Class

The inverse of Extract Class. Merge a class that no longer carries its weight back into another class.

### Motivation

A class that does too little -- perhaps after previous refactorings moved its responsibilities elsewhere -- adds complexity without value. Fold it back into the class that uses it.

### Mechanics

1. For each public method and field of the source class, create a corresponding member in the target class
2. Change all references to the source class to use the target class instead
3. Run tests
4. Delete the source class
5. Run tests

### When to Use

- The class has only one or two trivial methods
- The class was created by Extract Class but subsequent refactorings emptied it
- The class adds indirection without any logic, validation, or behavior of its own

---

## Hide Delegate

Encapsulate the fact that one object delegates to another. Create a method on the server that hides the delegate from the client, enforcing the Law of Demeter.

### Motivation

When a client calls `person.getDepartment().getManager()`, the client knows about the `Department` class -- it's coupled to the navigation structure. If `Department` changes its interface, the client breaks. By adding `person.getManager()` (which internally calls `department.getManager()`), the client only knows about `Person`.

### Mechanics

1. For each method the client calls on the delegate, create a simple delegating method on the server
2. Change the client to call the server method instead
3. If no client needs the delegate accessor anymore, remove it
4. Run tests

### Example

**Before:**
```python
# Client code:
manager = person.department.manager
```

**After:**
```python
class Person:
    @property
    def manager(self):
        return self.department.manager

# Client code:
manager = person.manager
```

### The Trade-Off

Hiding every delegate leads to the Middle Man smell -- a class that does nothing but forward calls. The right balance:

| Situation | Action |
|-----------|--------|
| Delegate's interface is unstable | Hide it (protect callers from change) |
| Client uses many delegate methods | Consider Hide Delegate for each |
| Server is becoming pure forwarding | Remove Middle Man |
| Chain is deep (a.b.c.d) | Definitely hide |

---

## Remove Middle Man

The inverse of Hide Delegate. When a class consists primarily of methods that delegate to another class, let the client call the delegate directly.

### Motivation

As a system evolves, more and more delegating methods accumulate until the "server" class adds no value -- it's just a pass-through. At that point, remove the indirection.

### Mechanics

1. Create a getter for the delegate on the server (if one doesn't exist)
2. For each delegating method that adds no value, redirect the client to call the delegate directly
3. Remove the delegating method from the server
4. Run tests

### Example

**Before:**
```javascript
class Person {
  get manager() { return this.department.manager; }
  get budget() { return this.department.budget; }
  get headcount() { return this.department.headcount; }
  get location() { return this.department.location; }
  // ... 10 more forwarding methods
}
```

**After:**
```javascript
class Person {
  get department() { return this._department; }
}

// Client:
const manager = person.department.manager;
```

---

## Introduce Foreign Method

When a server class needs an additional method but you can't modify it (third-party library, frozen module), create the method in the client class and pass the server object as the first argument.

### Motivation

A utility method that "should" be on the server class but can't be added there. The foreign method is a workaround -- mark it as such, so if the server class is ever opened for modification, the method can be moved.

### Example

```python
# Server class (third-party, can't modify):
# date = Date(year, month, day)

# Foreign method in client:
def next_day(date):
    """Foreign method -- should be on Date class."""
    return Date(date.year, date.month, date.day + 1)
```

---

## Introduce Local Extension

When you need several foreign methods on a server class you can't modify, create a new class -- either a subclass or a wrapper -- that adds the missing methods.

### Subclass vs. Wrapper

| Approach | When to Use |
|----------|-------------|
| Subclass | When you can subclass the server; simplest approach |
| Wrapper (Decorator) | When you can't subclass (final class); forward all original methods |

### Example (Wrapper)

```javascript
class EnhancedDate {
  constructor(date) {
    this._original = date;
  }

  // Forward original methods
  getYear() { return this._original.getYear(); }
  getMonth() { return this._original.getMonth(); }

  // New methods
  nextDay() {
    return new EnhancedDate(
      new Date(this._original.getTime() + 86400000)
    );
  }

  isWeekend() {
    const day = this._original.getDay();
    return day === 0 || day === 6;
  }
}
```

---

## Decision Guide: Where Does This Behavior Belong?

Use these questions to decide whether and where to move code:

| Question | If Yes | Action |
|----------|--------|--------|
| Does this method use more of another class's features? | Feature Envy | Move Method to that class |
| Is this field used more by another class? | Misplaced data | Move Field to that class |
| Does this class have two groups of fields that don't interact? | Multiple responsibilities | Extract Class |
| Is this class just a thin wrapper with no logic? | Unnecessary indirection | Inline Class |
| Is the client navigating through an object chain? | Tight coupling | Hide Delegate |
| Is this class just forwarding calls? | Middle Man smell | Remove Middle Man |
| Need to add a method to a class you can't modify? | Missing feature | Introduce Foreign Method or Local Extension |

### The Responsibility Placement Heuristic

When unsure where to put a method, ask: **"If the data this method uses changes, which class should need to be updated?"** The method belongs in that class. This keeps data and behavior together, minimizing the ripple effect of change.
