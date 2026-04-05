# Code Smell Catalog

A comprehensive catalog of code smells organized by family. Each smell includes a description, detection heuristics, and the named refactorings that fix it.


## Table of Contents
1. [What Is a Code Smell?](#what-is-a-code-smell)
2. [Family 1: Bloaters](#family-1-bloaters)
3. [Family 2: Object-Orientation Abusers](#family-2-object-orientation-abusers)
4. [Family 3: Change Preventers](#family-3-change-preventers)
5. [Family 4: Dispensables](#family-4-dispensables)
6. [Family 5: Couplers](#family-5-couplers)
7. [Smell-to-Refactoring Quick Reference](#smell-to-refactoring-quick-reference)

---

## What Is a Code Smell?

A code smell is a surface indication that usually corresponds to a deeper structural problem. Smells are not bugs -- the code works correctly -- but they make the code harder to understand, extend, and maintain. The term was coined by Kent Beck and popularized by Martin Fowler.

**Key principles:**
- Smells are heuristics, not rules -- use judgment
- A smell that causes no real problem in context can be left alone
- Smells cluster: fixing one often reveals others nearby
- The "smell → refactoring" mapping is many-to-many; one smell may require several refactorings

---

## Family 1: Bloaters

Smells where code grows too large to work with effectively.

### Long Method

**Description:** A method that tries to do too much. The longer a method is, the harder it is to understand, test, and reuse.

**Detection heuristics:**
- More than 10-15 lines of executable code
- Multiple levels of indentation
- Comments separating "sections" within the method
- Multiple responsibilities visible in one scan
- Difficulty naming the method because it does several things

**Typical fixes:**
- Extract Method -- pull each logical section into a named method
- Replace Temp with Query -- eliminate temporaries that block extraction
- Replace Method with Method Object -- when extraction is blocked by tangled local variables
- Decompose Conditional -- when the length comes from complex branching

**Example smell:**
```
function processOrder(order) {
  // validate order
  if (!order.items || order.items.length === 0) { ... }
  if (!order.customer) { ... }
  // calculate totals
  let subtotal = 0;
  for (const item of order.items) { subtotal += item.price * item.qty; }
  let tax = subtotal * 0.08;
  let shipping = subtotal > 100 ? 0 : 9.99;
  // apply discounts
  if (order.customer.isPremium) { ... }
  // save to database
  db.save({ ...order, subtotal, tax, shipping });
  // send confirmation
  emailService.send(order.customer.email, ...);
}
```

Each comment block should be its own method: `validateOrder()`, `calculateTotals()`, `applyDiscounts()`, `saveOrder()`, `sendConfirmation()`.

### Large Class

**Description:** A class that has too many fields, too many methods, or too many responsibilities. Often called a "God Class" or "Blob."

**Detection heuristics:**
- More than 200-300 lines
- More than 10-15 fields
- Fields that cluster into subgroups (e.g., address fields, billing fields)
- Methods that only use a subset of the fields
- The class name is vague (`Manager`, `Handler`, `Processor`, `Utils`)

**Typical fixes:**
- Extract Class -- split along the axis of change
- Extract Subclass -- when behavior varies by type
- Replace Data Value with Object -- when field clusters represent a concept

### Long Parameter List

**Description:** A method that takes more than three or four parameters, making calls confusing and error-prone.

**Detection heuristics:**
- More than 3-4 parameters
- Boolean parameters that switch behavior
- Parameters that always travel together
- Callers passing `null` for unused parameters

**Typical fixes:**
- Introduce Parameter Object -- group related params into `DateRange`, `Address`, `Options`
- Preserve Whole Object -- pass the object instead of extracting its fields
- Replace Parameter with Method -- have the method fetch data it needs

### Data Clumps

**Description:** Groups of variables that appear together in multiple places -- method parameters, field declarations, or local variables.

**Detection heuristics:**
- Same three or more fields appear together in multiple classes
- Same group of parameters appears in multiple method signatures
- Deleting one member of the group would make no sense without the others

**Typical fixes:**
- Extract Class -- create a new class for the clump (`Address`, `DateRange`, `Coordinates`)
- Introduce Parameter Object -- replace parameter groups with the new class
- Preserve Whole Object -- pass the object instead of its decomposed fields

### Primitive Obsession

**Description:** Using primitive types (strings, ints, arrays) to represent domain concepts instead of small objects.

**Detection heuristics:**
- Constants or magic numbers used to represent types (`int ADMIN = 1`)
- Strings used for structured data (phone numbers, zip codes, currencies)
- Arrays or tuples used instead of named structures
- Validation logic for the same type scattered across multiple locations

**Typical fixes:**
- Replace Data Value with Object -- `String email` becomes `EmailAddress`
- Replace Type Code with Subclasses -- when the type code drives behavior
- Replace Type Code with Strategy -- when subclassing is impractical
- Replace Magic Number with Symbolic Constant -- names instead of numbers

---

## Family 2: Object-Orientation Abusers

Smells where object-oriented features are used incorrectly or not at all.

### Switch Statements

**Description:** The same switch/case or if/else chain on a type code appears in multiple places. When a new type is added, every switch must be updated.

**Detection heuristics:**
- `switch` on a type or status field that appears in more than one place
- `if/else if` chain checking `instanceof` or type strings
- Adding a new type requires editing multiple files

**Typical fixes:**
- Replace Conditional with Polymorphism -- each type implements its own behavior
- Replace Type Code with Subclasses + Replace Conditional with Polymorphism
- Replace Type Code with Strategy when the type can change at runtime

**Example:**
```
// SMELL: same switch in calculatePay(), generateReport(), getPermissions()
switch (employee.type) {
  case 'engineer': return basePay;
  case 'manager': return basePay + bonus;
  case 'salesperson': return basePay + commission;
}

// FIX: polymorphism
class Engineer extends Employee {
  calculatePay() { return this.basePay; }
}
class Manager extends Employee {
  calculatePay() { return this.basePay + this.bonus; }
}
```

### Refused Bequest

**Description:** A subclass inherits methods or data it does not want. It overrides parent methods to do nothing or throws "not supported" exceptions.

**Detection heuristics:**
- Subclass overrides a method to do nothing or throw
- Subclass uses only a small fraction of inherited methods
- The "is-a" relationship feels forced

**Typical fixes:**
- Push Down Method / Push Down Field -- move unwanted members to the sibling that actually uses them
- Replace Inheritance with Delegation -- the child holds a reference to the parent instead of extending it

### Alternative Classes with Different Interfaces

**Description:** Two classes do essentially the same job but have different method names and signatures, preventing interchangeability.

**Detection heuristics:**
- Two classes with similar purpose but different method names
- Callers choose between them but can't treat them polymorphically
- Duplication of logic because no shared interface exists

**Typical fixes:**
- Rename Method -- align names across both classes
- Extract Superclass or Extract Interface -- define a shared contract
- Move Method -- equalize what each class offers

---

## Family 3: Change Preventers

Smells that make changes expensive by scattering related logic.

### Divergent Change

**Description:** One class changes for multiple unrelated reasons. It is the opposite of the Single Responsibility Principle.

**Detection heuristics:**
- You edit the same class for different kinds of changes (new database, new report format, new business rule)
- The class has methods that cluster into groups with no interaction between them
- Different team members edit the same file for different features

**Typical fixes:**
- Extract Class -- split the class along its axes of change
- Each resulting class should change for exactly one reason

### Shotgun Surgery

**Description:** A single logical change requires edits in many different classes. It is the opposite of Divergent Change.

**Detection heuristics:**
- A small functional change touches 5+ files
- A new field must be added to multiple classes
- A format change requires edits in scattered locations

**Typical fixes:**
- Move Method / Move Field -- consolidate related logic into one class
- Inline Class -- if scattered pieces are too small, merge them into the class that should own the responsibility

---

## Family 4: Dispensables

Smells where something exists but shouldn't.

### Lazy Class

**Description:** A class that does too little to justify its existence. Each class costs complexity; if it doesn't carry its weight, merge it.

**Typical fixes:** Inline Class, Collapse Hierarchy

### Dead Code

**Description:** Code that is never executed -- unreachable branches, unused variables, unneeded parameters, methods no one calls.

**Typical fixes:** Delete it. Version control remembers.

### Speculative Generality

**Description:** Abstractions, parameters, hooks, or classes created "in case we need them someday." YAGNI -- You Aren't Gonna Need It.

**Detection heuristics:**
- Abstract classes with only one subclass
- Parameters that are always passed the same value
- Methods that are only called by tests
- Framework infrastructure with no current use

**Typical fixes:**
- Collapse Hierarchy -- remove unneeded abstract class
- Remove Parameter -- delete unused params
- Inline Class / Inline Method -- collapse unneeded indirection

### Duplicate Code

**Description:** The same or nearly identical code structure appears in more than one place. The most common and most expensive smell.

**Detection heuristics:**
- Copy-pasted blocks with minor variations
- Methods in different classes that do the same thing
- Conditional branches with identical bodies

**Typical fixes:**
- Extract Method -- share the common code
- Pull Up Method -- move shared method to a common base class
- Extract Superclass / Extract Class -- when duplication spans classes
- Form Template Method -- when method structure is identical but details differ

---

## Family 5: Couplers

Smells where classes are too tightly bound to each other.

### Feature Envy

**Description:** A method that uses more features (fields and methods) of another class than its own. It "envies" the other class's data.

**Detection heuristics:**
- A method that calls 3+ getters on one foreign object
- A method that could be moved to the other class and would need fewer parameters

**Typical fixes:**
- Move Method -- relocate the method to the class it envies
- Extract Method + Move Method -- extract the envious part, then move it

### Inappropriate Intimacy

**Description:** Two classes are overly entangled -- accessing each other's private details, forming a bidirectional dependency.

**Typical fixes:**
- Move Method / Move Field to reduce the cross-boundary traffic
- Extract Class to put the shared concern in a neutral place
- Replace Inheritance with Delegation when subclass accesses too many parent internals

### Message Chains

**Description:** A client asks object A for B, then asks B for C, then asks C for D: `a.getB().getC().getD()`. The client is coupled to the entire navigation structure.

**Typical fixes:**
- Hide Delegate -- have A provide the answer directly
- Extract Method + Move Method -- push the chain into the object that should know the answer

### Middle Man

**Description:** A class whose methods do nothing but delegate to another class. It adds indirection without value.

**Detection heuristics:**
- More than half of a class's methods are one-line delegations
- The class has no logic of its own

**Typical fixes:**
- Remove Middle Man -- let the client call the delegate directly
- Inline Method -- merge the trivial forwarding methods into the caller

---

## Smell-to-Refactoring Quick Reference

| Smell | Primary Refactoring | Secondary Refactoring |
|-------|--------------------|-----------------------|
| Long Method | Extract Method | Replace Temp with Query |
| Large Class | Extract Class | Extract Subclass |
| Long Parameter List | Introduce Parameter Object | Preserve Whole Object |
| Data Clumps | Extract Class | Introduce Parameter Object |
| Primitive Obsession | Replace Data Value with Object | Replace Type Code with Subclasses |
| Switch Statements | Replace Conditional with Polymorphism | Replace Type Code with Strategy |
| Refused Bequest | Replace Inheritance with Delegation | Push Down Method |
| Divergent Change | Extract Class | -- |
| Shotgun Surgery | Move Method / Move Field | Inline Class |
| Lazy Class | Inline Class | Collapse Hierarchy |
| Dead Code | Delete it | -- |
| Speculative Generality | Collapse Hierarchy | Inline Class |
| Duplicate Code | Extract Method | Pull Up Method |
| Feature Envy | Move Method | Extract Method + Move Method |
| Inappropriate Intimacy | Move Method / Move Field | Extract Class |
| Message Chains | Hide Delegate | Extract Method |
| Middle Man | Remove Middle Man | Inline Method |
