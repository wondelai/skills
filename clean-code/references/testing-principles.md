# Testing Principles

Comprehensive guide to writing clean, maintainable tests that serve as executable documentation. Based on Robert C. Martin's *Clean Code*, Chapter 9.


## Table of Contents
1. [Why Tests Matter](#why-tests-matter)
2. [The Three Laws of TDD](#the-three-laws-of-tdd)
3. [Clean Tests](#clean-tests)
4. [One Concept Per Test](#one-concept-per-test)
5. [F.I.R.S.T. Principles](#first-principles)
6. [Test Naming](#test-naming)
7. [Test Patterns and Practices](#test-patterns-and-practices)
8. [Tests as Documentation](#tests-as-documentation)

---

## Why Tests Matter

Test code is just as important as production code. It is not a second-class citizen. It requires thought, design, and care. Dirty tests are equivalent to, if not worse than, having no tests. Tests that are hard to read, fragile, or slow become a liability that developers avoid and eventually delete.

**The fundamental equation:** Clean tests = confidence to refactor = clean production code. Without tests, every change is a potential bug. With dirty tests, every change requires fighting through incomprehensible test code. With clean tests, refactoring is fearless.

---

## The Three Laws of TDD

Test-Driven Development follows three simple rules:

| Law | Rule | What it means |
|-----|------|---------------|
| **First** | You may not write production code until you have written a failing unit test | Tests drive the design, not the other way around |
| **Second** | You may not write more of a unit test than is sufficient to fail (compilation failures count) | Write the minimum test that fails |
| **Third** | You may not write more production code than is sufficient to pass the currently failing test | Write the minimum code that passes |

### The Red-Green-Refactor Cycle

1. **Red:** Write a failing test (it should fail for the right reason)
2. **Green:** Write the simplest code that makes the test pass (even if ugly)
3. **Refactor:** Clean up both production code and test code while keeping all tests green

This cycle runs in seconds to minutes, not hours. Each cycle produces one small, tested increment.

### Benefits of TDD

| Benefit | Why |
|---------|-----|
| **Nearly 100% coverage** | Every line of production code was written to pass a test |
| **Tests as documentation** | Tests show exactly how the code is intended to be used |
| **Fearless refactoring** | You know immediately if a change breaks something |
| **Better design** | Hard-to-test code is hard to use; TDD pushes toward clean design |
| **Debugging reduction** | When a test fails, the bug is in the last few lines you wrote |

---

## Clean Tests

### What Makes a Test Clean?

**Readability.** The same thing that makes production code clean makes test code clean: readability. What makes tests readable? The same thing that makes all code readable: clarity, simplicity, and density of expression. In a test, you want to say a lot with as few expressions as possible.

### The Build-Operate-Check Pattern

Every clean test has three distinct phases:

```python
def test_should_apply_bulk_discount_when_quantity_exceeds_threshold():
    # BUILD: Create the test data
    order = an_order()
        .with_item(product="Widget", quantity=25, unit_price=10.00)
        .build()

    # OPERATE: Execute the behavior under test
    invoice = billing_service.generate_invoice(order)

    # CHECK: Verify the expected outcome
    assert invoice.total == 225.00  # 250 - 10% bulk discount
    assert invoice.discount_applied == "BULK_10"
```

Also known as **Arrange-Act-Assert** or **Given-When-Then**.

### Domain-Specific Testing Language

Build utility functions and helpers that read like a domain-specific language for your tests.

```python
# BAD: Raw setup code obscures the test's intent
def test_expired_subscription():
    user = User(
        id=uuid4(),
        name="Alice",
        email="alice@example.com",
        created_at=datetime(2024, 1, 1),
        subscription=Subscription(
            plan="pro",
            status="active",
            expires_at=datetime(2024, 1, 15),
        ),
    )
    user.subscription.check_expiry(current_date=datetime(2024, 2, 1))
    assert user.subscription.status == "expired"

# GOOD: Helpers create a readable narrative
def test_expired_subscription():
    user = a_user().with_pro_subscription(expires_on="2024-01-15").build()

    user.check_subscription_on("2024-02-01")

    assert_that(user).has_expired_subscription()
```

The test reads like a specification: "Given a user with a pro subscription expiring on Jan 15, when we check the subscription on Feb 1, then the subscription should be expired."

---

## One Concept Per Test

Each test function should test one concept. This does not necessarily mean one assert per test -- it means one logical assertion, one behavioral expectation.

### One Concept, Multiple Asserts (Acceptable)

```python
def test_should_create_valid_invoice_from_order():
    order = an_order().with_two_items().build()

    invoice = billing_service.generate_invoice(order)

    assert invoice.customer == order.customer
    assert invoice.line_items_count == 2
    assert invoice.total == order.calculated_total
    assert invoice.status == "pending"
```

All four asserts verify one concept: "generating an invoice from an order produces a valid invoice."

### Multiple Concepts (Split Into Separate Tests)

```python
# BAD: Two concepts in one test
def test_invoice_generation():
    order = an_order().build()
    invoice = billing_service.generate_invoice(order)
    assert invoice.total == order.calculated_total  # Concept 1: correct total

    invoice.mark_as_paid()
    assert invoice.status == "paid"  # Concept 2: payment status transition

# GOOD: Each test covers one concept
def test_should_calculate_correct_invoice_total():
    order = an_order().with_total(150.00).build()
    invoice = billing_service.generate_invoice(order)
    assert invoice.total == 150.00

def test_should_transition_to_paid_when_marked_as_paid():
    invoice = an_invoice().with_status("pending").build()
    invoice.mark_as_paid()
    assert invoice.status == "paid"
```

---

## F.I.R.S.T. Principles

Clean tests follow five principles that form the acronym F.I.R.S.T.:

### Fast

Tests should be fast. When tests run slowly, you won't run them frequently. When you don't run them frequently, you won't find problems early. When you don't find problems early, you won't fix them easily.

| Guideline | Target | How |
|-----------|--------|-----|
| Unit test suite | Under 10 seconds | Mock all external dependencies |
| Individual test | Under 100ms | No I/O, no network, no database |
| Integration tests | Separate suite | Run separately, not on every save |

### Independent

Tests should not depend on each other. One test should not set up conditions for the next. You should be able to run each test independently and in any order.

```python
# BAD: Test B depends on Test A's side effects
def test_a_create_user():
    global test_user
    test_user = UserService.create("Alice")

def test_b_update_user():
    UserService.update(test_user.id, name="Bob")  # Fails if A doesn't run first

# GOOD: Each test is self-contained
def test_create_user():
    user = UserService.create("Alice")
    assert user.name == "Alice"

def test_update_user():
    user = UserService.create("Alice")  # Own setup
    updated = UserService.update(user.id, name="Bob")
    assert updated.name == "Bob"
```

### Repeatable

Tests should produce the same result every time, in any environment -- development machine, CI server, production-like staging. Tests that depend on network availability, current time, or random data are flaky.

| Flaky dependency | Fix |
|-----------------|-----|
| Current time | Inject a clock; mock `datetime.now()` |
| Random data | Use seeded random or fixed test data |
| Network calls | Mock HTTP clients |
| Database state | Use transactions that roll back, or in-memory DB |
| File system | Use temp directories; clean up in teardown |
| Environment variables | Set explicitly in test setup |

### Self-Validating

Tests should have a boolean output: pass or fail. No manual interpretation required.

```python
# BAD: Requires human to check output
def test_report_generation():
    report = generate_report()
    print(report)  # Developer must read and visually verify

# GOOD: Automated assertion
def test_report_generation():
    report = generate_report()
    assert report.title == "Q4 Revenue Report"
    assert report.total_revenue == 142_500.00
    assert len(report.line_items) == 12
```

### Timely

Tests should be written just before the production code that makes them pass (TDD). Tests written after the fact are harder to write because the production code may not be designed for testability. You may decide that some production code is "too hard to test" -- which really means it's too coupled.

---

## Test Naming

Test names should describe the scenario being tested and the expected behavior.

### Naming Patterns

| Pattern | Example | When to use |
|---------|---------|-------------|
| `should_[expected]_when_[condition]` | `should_reject_login_when_password_expired` | Most common; clear cause-effect |
| `[method]_[scenario]_[expected]` | `withdraw_insufficient_funds_throws_exception` | When testing a specific method |
| `given_[state]_when_[action]_then_[result]` | `given_empty_cart_when_checkout_then_error` | BDD-style |
| `test_[behavior_description]` | `test_expired_tokens_are_rejected` | Simple, readable |

### Bad Test Names

| Bad name | Problem | Better name |
|----------|---------|-------------|
| `test1` | Meaningless | `test_empty_input_returns_empty_list` |
| `testProcess` | What about process? | `test_process_skips_inactive_users` |
| `testCalculate` | Too vague | `test_calculate_applies_weekend_surcharge` |
| `testBug1234` | Won't make sense in 6 months | `test_duplicate_orders_are_rejected` |

---

## Test Patterns and Practices

### Parameterized Tests

When testing the same behavior with different inputs, use parameterized tests instead of copy-pasting.

```python
@pytest.mark.parametrize("input_email,expected_valid", [
    ("user@example.com", True),
    ("user@sub.example.com", True),
    ("user@example", False),
    ("@example.com", False),
    ("user@.com", False),
    ("", False),
])
def test_email_validation(input_email, expected_valid):
    assert validate_email(input_email) == expected_valid
```

### Test Fixtures and Builders

Use the Builder pattern for test data to make tests readable and maintainable.

```python
class UserBuilder:
    def __init__(self):
        self._name = "Default User"
        self._email = "default@example.com"
        self._role = "viewer"
        self._active = True

    def with_name(self, name): self._name = name; return self
    def with_role(self, role): self._role = role; return self
    def inactive(self): self._active = False; return self
    def build(self):
        return User(
            name=self._name, email=self._email,
            role=self._role, active=self._active,
        )

def a_user():
    return UserBuilder()

# Usage in tests
admin = a_user().with_name("Alice").with_role("admin").build()
inactive_user = a_user().inactive().build()
```

### Testing Error Paths

Every error path in production code should have a corresponding test.

```python
def test_should_raise_on_negative_amount():
    account = an_account().with_balance(100).build()
    with pytest.raises(ValueError, match="Amount must be positive"):
        account.withdraw(-50)

def test_should_raise_on_insufficient_funds():
    account = an_account().with_balance(100).build()
    with pytest.raises(InsufficientFundsError):
        account.withdraw(150)
```

### Boundary Condition Tests

Test the edges, not just the middle.

| Boundary | Tests needed |
|----------|-------------|
| Empty input | `[]`, `""`, `None`, `{}` |
| Single element | List with one item, string with one char |
| Maximum values | `MAX_INT`, full capacity, max length |
| Off-by-one | `n-1`, `n`, `n+1` for any threshold |
| Transition points | Just below and just above limits |
| Overflow/underflow | Values that exceed type boundaries |

---

## Tests as Documentation

Clean tests serve as the most reliable documentation of how the system behaves. Unlike comments or wiki pages, tests are always up to date -- if they weren't, they'd be failing.

| Documentation type | Tests provide |
|-------------------|---------------|
| **API usage** | Test setup shows how to call the API |
| **Expected behavior** | Assertions describe what should happen |
| **Edge cases** | Boundary tests document special cases |
| **Error behavior** | Error path tests document failure modes |
| **Business rules** | Test names describe domain rules |

When a new developer asks "how does this work?", point them to the tests. Clean tests answer the question better than any comment or README.
