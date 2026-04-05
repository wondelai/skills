# Composing Methods

Detailed reference for the refactorings that break down long methods into well-named, cohesive pieces. These are the most frequently used refactorings and the foundation of all code improvement.

## Table of Contents
1. [Extract Method](#extract-method)
2. [Inline Method](#inline-method)
3. [Extract Variable](#extract-variable)
4. [Inline Variable](#inline-variable)
5. [Replace Temp with Query](#replace-temp-with-query)
6. [Split Temporary Variable](#split-temporary-variable)
7. [Remove Assignments to Parameters](#remove-assignments-to-parameters)
8. [Replace Method with Method Object](#replace-method-with-method-object)
9. [Decision Guide: Which Composing Refactoring to Use](#decision-guide-which-composing-refactoring-to-use)

---

## Extract Method

The single most important refactoring. Turn a code fragment into a method whose name explains the purpose of the fragment.

### Motivation

You have a code fragment that can be grouped together. The longer a method, the harder it is to understand. When you see a comment explaining what the next block does, that's a signal to extract. The comment becomes the method name.

### Mechanics

1. Create a new method and name it after the *intention* of the code (what it does, not how)
2. Copy the extracted code into the new method
3. Scan the extracted code for references to local variables -- these become parameters or return values
4. Declare any local-scope variables as local to the new method if they're only used within the extracted code
5. Pass any remaining local variables as parameters
6. If more than one value needs to be returned, consider returning an object or extracting further
7. Replace the original code with a call to the new method
8. Run tests

### Example

**Before:**
```javascript
function printOwing(invoice) {
  let outstanding = 0;

  // print banner
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");

  // calculate outstanding
  for (const order of invoice.orders) {
    outstanding += order.amount;
  }

  // print details
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
  console.log(`due: ${invoice.dueDate.toLocaleDateString()}`);
}
```

**After:**
```javascript
function printOwing(invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice, outstanding);
}

function printBanner() {
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
}

function calculateOutstanding(invoice) {
  let result = 0;
  for (const order of invoice.orders) {
    result += order.amount;
  }
  return result;
}

function printDetails(invoice, outstanding) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
  console.log(`due: ${invoice.dueDate.toLocaleDateString()}`);
}
```

### Naming Guidelines

| Bad Name | Good Name | Why |
|----------|-----------|-----|
| `doStuff()` | `calculateMonthlyTotal()` | Names the intent, not the vagueness |
| `process()` | `validateAndSaveOrder()` | Specific about what it does |
| `handleData()` | `parseCSVRow()` | Names the domain concept |
| `helper()` | `formatCurrencyForDisplay()` | Describes the transformation |
| `step2()` | `applyDiscountRules()` | Names the business concept |

**Rule of thumb:** If you can't find a good name, the extraction boundaries may be wrong. Try extracting a different fragment.

---

## Inline Method

The inverse of Extract Method. Replace a method call with the method's body when the body is as clear as the name, or when you need to regroup poorly factored code.

### Motivation

Sometimes a method body is as obvious as the method name. Indirection without value is noise. Also useful as an intermediate step: inline a badly decomposed method, then re-extract along better boundaries.

### Mechanics

1. Check that the method is not polymorphic (no subclass overrides it)
2. Find all callers
3. Replace each call with the method body
4. Delete the method
5. Run tests

### Example

**Before:**
```python
def get_rating(self):
    return 2 if self.more_than_five_late_deliveries() else 1

def more_than_five_late_deliveries(self):
    return self.late_deliveries > 5
```

**After:**
```python
def get_rating(self):
    return 2 if self.late_deliveries > 5 else 1
```

### When NOT to Inline

- When the method name communicates domain meaning the code doesn't
- When the method is used in multiple places (DRY)
- When the method is overridden in subclasses

---

## Extract Variable

Introduce a local variable for a complex expression to make it self-documenting.

### Motivation

Expressions can become hard to read. A well-named variable for a sub-expression acts as inline documentation and makes debugging easier.

### Mechanics

1. Identify a complex expression or sub-expression
2. Declare a variable named for the intent of the expression
3. Replace the expression with the variable
4. Run tests

### Example

**Before:**
```javascript
return order.quantity * order.itemPrice -
  Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
  Math.min(order.quantity * order.itemPrice * 0.1, 100);
```

**After:**
```javascript
const basePrice = order.quantity * order.itemPrice;
const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
const shippingCap = Math.min(basePrice * 0.1, 100);
return basePrice - quantityDiscount + shippingCap;
```

---

## Inline Variable

The inverse of Extract Variable. Remove a variable when the expression is just as clear.

### When to Use

- The variable name adds no information beyond what the expression says
- The variable is assigned once and used once
- The variable is blocking another refactoring (e.g., you need to inline it to then Extract Method)

### Example

**Before:**
```python
base_price = order.base_price()
return base_price > 1000
```

**After:**
```python
return order.base_price() > 1000
```

---

## Replace Temp with Query

Turn a temporary variable into a method call so the computation is reusable and the original method becomes shorter.

### Motivation

Temporaries can only be seen within a single method. If the same computation is needed elsewhere, it gets duplicated. A query method is visible to the whole class (or can be extracted to another class).

### Mechanics

1. Check that the variable is assigned once and the expression has no side effects
2. Extract the right-hand side of the assignment into a new method
3. Replace all references to the temp with calls to the new method
4. Remove the temp declaration and assignment
5. Run tests

### Example

**Before:**
```javascript
class Order {
  getPrice() {
    const basePrice = this.quantity * this.itemPrice;
    if (basePrice > 1000) {
      return basePrice * 0.95;
    } else {
      return basePrice * 0.98;
    }
  }
}
```

**After:**
```javascript
class Order {
  getPrice() {
    if (this.basePrice() > 1000) {
      return this.basePrice() * 0.95;
    } else {
      return this.basePrice() * 0.98;
    }
  }

  basePrice() {
    return this.quantity * this.itemPrice;
  }
}
```

### Performance Note

Calling the method multiple times instead of caching in a temp may seem wasteful. In practice, the performance impact is negligible for most code. Profile before optimizing. Refactored code is easier to optimize later because the hot path is isolated.

---

## Split Temporary Variable

When a temporary variable is assigned more than once (and it's not a loop counter or collecting variable), it's doing two different jobs. Give each job its own variable.

### Motivation

A temp assigned twice for different purposes misleads the reader into thinking the assignments are related. Each role deserves its own variable with a descriptive name.

### Mechanics

1. Rename the first assignment to reflect its purpose
2. Declare it as `const`/`final` if possible
3. Find all uses that refer to the first assignment's value and make sure they use the new name
4. Repeat for each subsequent assignment with a different name
5. Run tests

### Example

**Before:**
```javascript
let temp = 2 * (height + width);  // perimeter
console.log(temp);
temp = height * width;            // area
console.log(temp);
```

**After:**
```javascript
const perimeter = 2 * (height + width);
console.log(perimeter);
const area = height * width;
console.log(area);
```

---

## Remove Assignments to Parameters

Never assign to a parameter inside a method body. It confuses readers about whether the change is visible to the caller (it isn't in pass-by-value languages; it is in pass-by-reference for object mutations).

### Mechanics

1. Create a new local variable for the parameter
2. Replace all assignments to the parameter with assignments to the new variable
3. Run tests

### Example

**Before:**
```python
def discount(input_val, quantity):
    if quantity > 50:
        input_val -= 2
    if quantity > 100:
        input_val -= 1
    return input_val
```

**After:**
```python
def discount(input_val, quantity):
    result = input_val
    if quantity > 50:
        result -= 2
    if quantity > 100:
        result -= 1
    return result
```

---

## Replace Method with Method Object

When a method is too tangled with local variables to extract from, move the entire method into its own class where the local variables become fields. Then you can freely extract sub-methods.

### Motivation

Sometimes a long method has so many interrelated local variables that Extract Method is impossible (too many parameters would be needed). By turning the method into its own class, all locals become fields, accessible to any extracted method without parameters.

### Mechanics

1. Create a new class named after the method's purpose
2. Add a field for the original object and for every local variable and parameter
3. Create a constructor that takes the original object and all parameters
4. Copy the method body into a `compute()` (or similar) method
5. Replace the original method with: create the new object, call `compute()`
6. Now freely extract methods within the new class -- locals are fields, no parameter passing needed
7. Run tests

### Example

**Before:**
```python
class Account:
    def gamma(self, input_val, quantity, year_to_date):
        # 50 lines of tangled computation using all three params
        # plus self.fields -- too intertwined to extract
        ...
```

**After:**
```python
class GammaCalculation:
    def __init__(self, account, input_val, quantity, year_to_date):
        self.account = account
        self.input_val = input_val
        self.quantity = quantity
        self.year_to_date = year_to_date

    def compute(self):
        # Now extract freely -- all variables are fields
        self._apply_quantity_adjustment()
        self._apply_yearly_factor()
        return self.input_val

    def _apply_quantity_adjustment(self):
        # can access self.quantity, self.input_val freely
        ...

    def _apply_yearly_factor(self):
        ...

class Account:
    def gamma(self, input_val, quantity, year_to_date):
        return GammaCalculation(self, input_val, quantity, year_to_date).compute()
```

---

## Decision Guide: Which Composing Refactoring to Use

| Situation | Refactoring |
|-----------|-------------|
| Code block can be named by intent | Extract Method |
| Method body is trivial and name adds nothing | Inline Method |
| Complex expression needs explanation | Extract Variable |
| Variable adds no meaning beyond the expression | Inline Variable |
| Same computation needed in multiple methods | Replace Temp with Query |
| One variable serves two purposes | Split Temporary Variable |
| Parameter is reassigned inside method | Remove Assignments to Parameters |
| Long method with too many entangled locals | Replace Method with Method Object |
