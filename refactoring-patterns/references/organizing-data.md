# Organizing Data

Detailed reference for refactorings that improve how data is represented. Raw primitives, magic numbers, exposed fields, and mutable collections create subtle bugs and scatter domain knowledge. These refactorings replace primitive representations with objects that encapsulate behavior and enforce invariants.

## Table of Contents
1. [Replace Data Value with Object](#replace-data-value-with-object)
2. [Change Value to Reference](#change-value-to-reference)
3. [Replace Array with Object](#replace-array-with-object)
4. [Replace Magic Number with Symbolic Constant](#replace-magic-number-with-symbolic-constant)
5. [Encapsulate Field](#encapsulate-field)
6. [Encapsulate Collection](#encapsulate-collection)
7. [Replace Type Code with Class](#replace-type-code-with-class)
8. [Decision Guide: Which Data Refactoring to Use](#decision-guide-which-data-refactoring-to-use)

---

## Replace Data Value with Object

Wrap a primitive data item in a class when it has behavior or validation associated with it. This is the cure for Primitive Obsession.

### Motivation

A data value starts life as a simple string or number. Then you add validation. Then formatting. Then comparison logic. Then the same validation appears in three places. At that point, the value deserves to be an object.

### Mechanics

1. Create a class for the value with a constructor that takes the primitive
2. Add validation in the constructor
3. Add any behavior methods (formatting, comparison, etc.)
4. Change the field type from primitive to the new class
5. Update all code that sets the field to create an instance of the new class
6. Update all code that reads the field to use the object's methods
7. Run tests

### Example

**Before:**
```javascript
class Order {
  constructor(customer) {
    this.customer = customer; // just a string name
  }
}

// Scattered validation in multiple places:
if (order.customer === '') throw new Error('no customer');
if (otherOrder.customer === '') throw new Error('no customer');
```

**After:**
```javascript
class Customer {
  constructor(name) {
    if (!name || name.trim() === '') {
      throw new Error('Customer name is required');
    }
    this._name = name.trim();
  }

  get name() { return this._name; }

  equals(other) {
    return other instanceof Customer && this._name === other._name;
  }
}

class Order {
  constructor(customer) {
    this.customer = new Customer(customer);
  }
}
```

### Common Primitive-to-Object Upgrades

| Primitive | Object | Behavior It Gains |
|-----------|--------|-------------------|
| `String email` | `EmailAddress` | Format validation, domain extraction |
| `number cents` | `Money` | Currency, rounding rules, arithmetic |
| `String phone` | `PhoneNumber` | Formatting, country code parsing |
| `number lat, number lng` | `Coordinates` | Distance calculation, validation |
| `String startDate, String endDate` | `DateRange` | Contains, overlaps, duration |
| `number celsius` | `Temperature` | Unit conversion, comparison |
| `String hex` | `Color` | Parsing, lightness, contrast |
| `number status` | `OrderStatus` | Valid transitions, display name |

---

## Change Value to Reference

Convert a value object into a reference object when you need identity semantics -- when changes to one instance should be visible everywhere that instance is used.

### Motivation

When you have multiple copies of the same customer, changing the phone number on one doesn't change it on the others. If business rules require a single shared instance, convert value to reference using a registry or repository.

### Mechanics

1. Determine or create a factory method for the object
2. Set up a registry (map, repository, or lookup service) to store instances
3. Change the factory to check the registry before creating new instances
4. Change client code to use the factory instead of the constructor
5. Run tests

### Example

```javascript
// Registry pattern:
class CustomerRepository {
  constructor() {
    this._customers = new Map();
  }

  get(id) {
    if (!this._customers.has(id)) {
      this._customers.set(id, new Customer(id));
    }
    return this._customers.get(id);
  }
}

// All orders for customer #123 now share the same Customer object
const repo = new CustomerRepository();
const order1 = new Order(repo.get(123));
const order2 = new Order(repo.get(123));
// order1.customer === order2.customer  // true (same reference)
```

### Value vs. Reference: Decision Guide

| Question | Value | Reference |
|----------|-------|-----------|
| Do you need identity (same object everywhere)? | No | Yes |
| Is the object immutable? | Typically | May be mutable |
| Do you compare by content? | Yes (`equals()`) | No (identity `===`) |
| Examples | Money, DateRange, Color | Customer, Account, Product |

---

## Replace Array with Object

Replace an array used as a record (where each position has a different meaning) with an object with named fields.

### Motivation

`row[0]` is the name, `row[1]` is the age, `row[2]` is the department. This is fragile, unreadable, and type-unsafe. Named fields make the structure self-documenting.

### Mechanics

1. Create a class with a field for each array position
2. Add getters and setters for each field
3. Replace array creation with object construction
4. Replace positional access with named access
5. Run tests

### Example

**Before:**
```python
performance = ["Liverpool", 15, 2]
name = performance[0]
wins = performance[1]
losses = performance[2]
```

**After:**
```python
class Performance:
    def __init__(self, name, wins, losses):
        self.name = name
        self.wins = wins
        self.losses = losses

performance = Performance("Liverpool", 15, 2)
name = performance.name
wins = performance.wins
losses = performance.losses
```

---

## Replace Magic Number with Symbolic Constant

Replace a literal number that has a particular meaning with a named constant.

### Motivation

`9.81` means nothing in code. `GRAVITATIONAL_ACCELERATION = 9.81` communicates intent, prevents typos (the constant name is checked by the compiler), and centralizes the value for easy change.

### Mechanics

1. Declare a constant and set it to the magic number
2. Find all occurrences of the magic number
3. Replace each occurrence with the constant (check that each occurrence represents the same concept -- the number `100` might mean "percentage" in one place and "max items" in another)
4. Run tests

### Common Magic Number Categories

| Category | Before | After |
|----------|--------|-------|
| Physics | `9.81` | `GRAVITATIONAL_ACCELERATION` |
| Business rules | `0.08` | `SALES_TAX_RATE` |
| Limits | `255` | `MAX_RGB_VALUE` |
| HTTP | `404` | `HTTP_NOT_FOUND` |
| Time | `86400` | `SECONDS_PER_DAY` |
| Retry | `3` | `MAX_RETRY_ATTEMPTS` |
| Thresholds | `100` | `FREE_SHIPPING_THRESHOLD` |

### When NOT to Replace

- `0` and `1` in arithmetic are usually fine as literals
- Loop counters (`for i in range(10)`) are obvious from context
- Array index `[0]` for "first element" is idiomatic

---

## Encapsulate Field

Replace direct access to a public field with getter and setter methods.

### Motivation

A public field gives you no control over reads and writes. You can't add validation, logging, lazy initialization, or computed values later without changing every caller. Encapsulation creates a seam for future change.

### Mechanics

1. Create getter and setter methods for the field
2. Find all references to the field and replace reads with the getter, writes with the setter
3. Make the field private
4. Run tests

### Example

**Before:**
```python
class Person:
    def __init__(self, name):
        self.name = name  # public field

# Client:
person.name = "   Bob   "  # no validation, no trimming
```

**After:**
```python
class Person:
    def __init__(self, name):
        self._name = None
        self.name = name  # uses the setter

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
```

---

## Encapsulate Collection

Don't return a raw mutable collection from a getter. Instead, return an unmodifiable view or a copy, and provide explicit add/remove methods.

### Motivation

When a getter returns a mutable list, callers can add, remove, or clear items without the owning object knowing. This breaks encapsulation -- the object can't enforce invariants, fire events, or validate changes.

### Mechanics

1. Add `addItem()` and `removeItem()` methods on the owning class
2. Change the getter to return an unmodifiable view (or a copy)
3. Find all callers that mutate the collection through the getter and change them to use the add/remove methods
4. Run tests

### Example

**Before:**
```javascript
class Course {}

class Person {
  get courses() { return this._courses; }
  set courses(list) { this._courses = list; }
}

// Client can mutate freely:
person.courses.push(newCourse);        // bypasses Person
person.courses.splice(0, 1);           // bypasses Person
person.courses = [];                   // replaces internal state
```

**After:**
```javascript
class Person {
  get courses() {
    return [...this._courses]; // return a copy
  }

  addCourse(course) {
    this._courses.push(course);
  }

  removeCourse(course) {
    const index = this._courses.indexOf(course);
    if (index === -1) throw new RangeError('Course not found');
    this._courses.splice(index, 1);
  }

  get numberOfCourses() {
    return this._courses.length;
  }
}
```

### Language-Specific Patterns

| Language | Unmodifiable Return |
|----------|-------------------|
| Java | `Collections.unmodifiableList(list)` |
| JavaScript | `[...this._items]` or `Object.freeze([...this._items])` |
| Python | `tuple(self._items)` or `list(self._items)` (return a copy) |
| C# | `items.AsReadOnly()` |
| Go | Return a slice copy: `append([]T{}, items...)` |

---

## Replace Type Code with Class

Replace a type code (integer or string constant) that does not affect behavior with a proper class. Use when the type code is used for categorization but doesn't drive conditional logic.

### When to Use Which

| Situation | Refactoring |
|-----------|-------------|
| Type code is informational only (no behavior change) | Replace Type Code with Class |
| Type code drives behavior via conditionals | Replace Type Code with Subclasses |
| Type code can change at runtime | Replace Type Code with Strategy/State |
| Type code has few values and language supports it | Use an Enum |

### Replace Type Code with Subclasses

Used when the type code determines behavior through conditionals.

**Before:**
```javascript
class Employee {
  constructor(type) {
    this._type = type; // 'engineer', 'manager', 'salesperson'
  }

  calculatePay() {
    switch (this._type) {
      case 'engineer': return this.basePay;
      case 'manager': return this.basePay + this.bonus;
      case 'salesperson': return this.basePay + this.commission;
    }
  }

  canApproveExpenses() {
    return this._type === 'manager';
  }
}
```

**After:**
```javascript
class Employee {
  calculatePay() { throw new Error('abstract'); }
  canApproveExpenses() { return false; }
}

class Engineer extends Employee {
  calculatePay() { return this.basePay; }
}

class Manager extends Employee {
  calculatePay() { return this.basePay + this.bonus; }
  canApproveExpenses() { return true; }
}

class Salesperson extends Employee {
  calculatePay() { return this.basePay + this.commission; }
}
```

### Replace Type Code with Strategy/State

Used when the type code can change at runtime (an employee can be promoted from engineer to manager), so subclassing the employee itself is not possible.

**After (Strategy):**
```javascript
class Employee {
  constructor(type) {
    this._type = type; // EmployeeType strategy object
  }

  calculatePay() {
    return this._type.calculatePay(this);
  }

  promoteToManager() {
    this._type = new ManagerType();
  }
}

class EngineerType {
  calculatePay(employee) { return employee.basePay; }
}

class ManagerType {
  calculatePay(employee) { return employee.basePay + employee.bonus; }
}
```

---

## Decision Guide: Which Data Refactoring to Use

| Situation | Refactoring |
|-----------|-------------|
| Primitive value has associated behavior | Replace Data Value with Object |
| Need one shared instance across the system | Change Value to Reference |
| Array positions have different meanings | Replace Array with Object |
| Literal number has domain meaning | Replace Magic Number with Symbolic Constant |
| Public field needs future flexibility | Encapsulate Field |
| Getter returns mutable collection | Encapsulate Collection |
| Type code is informational | Replace Type Code with Class / Enum |
| Type code drives behavior | Replace Type Code with Subclasses |
| Type code changes at runtime | Replace Type Code with Strategy |
