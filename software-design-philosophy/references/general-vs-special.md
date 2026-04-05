# General-Purpose vs Special-Purpose Modules

One of the most important design decisions is how general-purpose or special-purpose a module's interface should be. Ousterhout advocates for a "somewhat general-purpose" approach: general enough to avoid special cases, specific enough to avoid over-engineering.


## Table of Contents
1. [The Spectrum](#the-spectrum)
2. [The Key Question](#the-key-question)
3. [Push Complexity Downward](#push-complexity-downward)
4. [Configuration Parameters: Complexity Amplifiers](#configuration-parameters-complexity-amplifiers)
5. [When Specialization Is Justified](#when-specialization-is-justified)
6. [Practical Guidelines](#practical-guidelines)
7. [The Relationship to Information Hiding](#the-relationship-to-information-hiding)
8. [Summary](#summary)

---

## The Spectrum

```
Too Special ←————————————————————————→ Too General
  (bloated     (sweet spot:              (wasted effort,
  with         "somewhat                  unnecessary
  special      general-purpose")          abstraction)
  cases)
```

### Too Special-Purpose

A module designed for one specific use case. Its interface includes details that tie it to a particular caller or scenario.

```python
# Too special: designed for one specific email use case
class WelcomeEmailSender:
    def send_welcome_email(self, user_name, user_email, plan_name):
        ...

class PasswordResetEmailSender:
    def send_reset_email(self, user_email, reset_token, expiry_minutes):
        ...

class InvoiceEmailSender:
    def send_invoice_email(self, user_email, invoice_id, amount, due_date):
        ...
```

Three classes doing essentially the same thing (sending email) with interfaces tied to specific use cases. Adding a fourth email type requires creating another class.

### Too General-Purpose

A module designed for every conceivable use case, including ones that may never arise.

```python
# Too general: anticipates every possible need
class UniversalMessageDispatcher:
    def dispatch(self, channel, template, recipients, variables,
                 priority, scheduling, retry_policy, attachments,
                 tracking_config, ab_test_config, localization_config,
                 rate_limiting_config, webhook_callbacks):
        ...
```

The interface is so general that using it requires understanding 13 parameters. Most callers will use only a fraction of them.

### Somewhat General-Purpose (The Sweet Spot)

```python
# Somewhat general: covers current needs with a simple interface
class EmailService:
    def send(self, to: str, subject: str, body: str,
             attachments: list = None):
        ...
```

This covers welcome emails, password resets, invoices, and any future email type with a single, simple interface. It is general enough to handle all current use cases without special-case methods, but it does not try to handle SMS, push notifications, or A/B testing.

## The Key Question

> **"What is the simplest interface that will cover all my current needs?"**

This question is the practical tool for finding the sweet spot. It has three important parts:

1. **Simplest interface:** Minimize the number of methods, parameters, and concepts
2. **All current needs:** Do not design for hypothetical future requirements
3. **Cover:** The interface must actually work for every current use case without workarounds

### Applying the Question

**Step 1:** List all current use cases for the module.

**Step 2:** For each use case, identify what the caller needs from the module.

**Step 3:** Find the minimal set of methods and parameters that satisfies all callers.

**Step 4:** Check that no use case requires awkward workarounds.

**Example:**

A text editor needs to support:
- Inserting text at a position
- Deleting a range of text
- Replacing a range of text

Special-purpose approach:
```python
class TextEditor:
    def insert_text(self, position, text): ...
    def delete_range(self, start, end): ...
    def replace_range(self, start, end, new_text): ...
    def insert_heading(self, position, level, text): ...
    def insert_bullet_point(self, position, text): ...
    def delete_word(self, position): ...
    def replace_word(self, position, new_word): ...
```

Somewhat general-purpose approach:
```python
class TextEditor:
    def insert(self, position, text): ...
    def delete(self, start, end): ...
```

The general-purpose approach covers all cases with two methods. `replace` is just `delete` followed by `insert`. Headings and bullet points are just text with formatting characters. The interface is simpler and covers all current needs.

## Push Complexity Downward

**Principle:** It is more important for a module to have a simple interface than a simple implementation.

When complexity must exist somewhere in the system, it is better to put it inside a module (deepening it) than in the module's interface (burdening all callers).

### Why Downward, Not Upward?

| Complexity Location | Who Bears the Cost | Multiplier Effect |
|--------------------|-------------------|-------------------|
| Inside the module | The module's developer, once | 1x |
| In the interface | Every caller, every time they use it | Nx (where N = number of callers) |

A module with a complex implementation but simple interface imposes complexity on one developer (the module author). A module with a simple implementation but complex interface imposes complexity on every developer who uses it.

### Example: Connection Pooling

**Complexity pushed up (to callers):**
```python
# Every caller must manage pool lifecycle
pool = ConnectionPool(host, port, min_size=5, max_size=20)
conn = pool.acquire(timeout=5)
try:
    result = conn.execute(query)
finally:
    pool.release(conn)
# Must also handle pool exhaustion, stale connections, reconnection...
```

**Complexity pushed down (into the module):**
```python
# Caller just makes queries; pooling is internal
db = Database(connection_string)
result = db.query(sql, params)
# Pool management, connection lifecycle, retries all handled internally
```

### Example: Error Handling

**Complexity pushed up:**
```python
result = parser.parse(input)
if result.has_syntax_error:
    handle_syntax_error(result.syntax_error)
elif result.has_semantic_error:
    handle_semantic_error(result.semantic_error)
elif result.has_ambiguity:
    handle_ambiguity(result.ambiguity)
else:
    process(result.value)
```

**Complexity pushed down:**
```python
try:
    result = parser.parse(input)
    process(result)
except ParseError as e:
    # Module classifies and wraps all error types with clear messages
    show_error(e.message, e.location)
```

## Configuration Parameters: Complexity Amplifiers

Configuration parameters are one of the most common ways modules push complexity upward to callers. Each parameter represents a decision the module is refusing to make.

### The Problem

```python
# 11 decisions pushed to the caller
cache = Cache(
    max_size=1000,
    eviction_policy="lru",
    ttl_seconds=3600,
    cleanup_interval=300,
    max_memory_mb=256,
    serializer="json",
    compression=True,
    compression_level=6,
    stats_enabled=True,
    stats_interval=60,
    thread_safe=True,
)
```

Every parameter is a question the caller must answer. Most callers don't know the right answer and will either copy values from examples or guess. Wrong values cause subtle performance problems or bugs that are hard to diagnose.

### Better Approaches

| Strategy | How It Helps | Example |
|----------|-------------|---------|
| **Sensible defaults** | Module makes the decision unless overridden | `Cache()` works with reasonable defaults; override only what you need |
| **Auto-detection** | Module determines the right value at runtime | Auto-size based on available memory; auto-select compression based on data characteristics |
| **Progressive disclosure** | Simple API for simple use; options for advanced use | `Cache()` for basic use; `Cache.builder().with_eviction(lru).build()` for custom |
| **Convention over configuration** | Follow well-known patterns | Database connection reads from `DATABASE_URL` environment variable; no parameter needed |
| **Elimination** | Remove the parameter entirely | Instead of `thread_safe` parameter, always be thread-safe (the cost is usually negligible) |

### When Configuration Is Justified

Configuration parameters are justified when:
1. **Different callers genuinely need different values** (not just "might someday need")
2. **The module cannot determine the right value** (it lacks the information)
3. **The wrong default would cause real harm** (not just suboptimal performance)
4. **The decision changes between deployments** (environment-specific settings)

### The Test

For each configuration parameter, ask:
- "Can the module figure this out on its own?" If yes, remove the parameter.
- "Do most callers use the same value?" If yes, make it the default.
- "Will the caller know the right value?" If no, the parameter is shifting complexity, not simplifying.

## When Specialization Is Justified

Despite the general preference for general-purpose design, specialization is appropriate in certain situations:

### 1. Domain-Specific Modules

When a module embodies domain-specific knowledge that does not generalize.

```python
# Justified specialization: tax rules are inherently domain-specific
class USTaxCalculator:
    def calculate_federal_tax(self, income, filing_status, deductions):
        ...
    def calculate_state_tax(self, income, state):
        ...
```

A "general-purpose tax calculator" would need to know about every country's tax system. Specialization to US taxes hides substantial domain complexity behind a focused interface.

### 2. Performance-Critical Paths

When general-purpose abstractions introduce unacceptable overhead.

```python
# General-purpose: flexible but slow for the hot path
def transform(data, transformer_pipeline):
    for transformer in transformer_pipeline:
        data = transformer.apply(data)
    return data

# Specialized: optimized for the specific hot path
def transform_pixel_rgb_to_hsv(pixels: np.ndarray) -> np.ndarray:
    # SIMD-optimized, no dynamic dispatch, no allocation
    ...
```

### 3. User-Facing Interfaces

When the interface is used by end users (not developers), specialized vocabulary improves usability.

```python
# General-purpose API: flexible but requires domain knowledge
scheduler.create_recurring_task(
    interval=timedelta(days=7),
    start=next_monday(),
    handler=send_report
)

# Specialized API: matches user mental model
scheduler.send_weekly_report(day="monday", time="09:00")
```

### 4. Adapters and Bridges

When connecting two systems with incompatible interfaces, the adapter is inherently specific to both.

```python
class StripeToInternalPaymentAdapter:
    def convert_stripe_event(self, stripe_event) -> InternalPaymentEvent:
        ...
```

## Practical Guidelines

### When Designing a New Module

1. List all current use cases
2. Ask: "What is the simplest interface that covers all of these?"
3. Resist adding methods for hypothetical future use cases
4. Push complexity into the implementation, away from the interface
5. Default to slightly more general than you think you need -- it is usually simpler

### When Reviewing an Existing Module

| Signal | Problem | Action |
|--------|---------|--------|
| Many methods that differ only in parameters | Over-specialization | Merge into fewer, more general methods |
| Methods named after specific callers | Coupling to use cases | Rename around the concept, not the caller |
| Long parameter lists | Complexity pushed upward | Add defaults, auto-detect, or absorb decisions |
| Multiple modules with similar functionality | Opportunity for generalization | Extract a shared general-purpose module |
| Configuration that "nobody touches" | Parameters that should be defaults | Make them defaults or remove them |

### When Adding a Feature

Before adding a new method or parameter:
1. Can an existing method handle this with its current interface?
2. Can a slight generalization of an existing method handle this?
3. Does the new method introduce a special case that could be avoided?

The best features are those that require no interface changes because the existing abstraction already supports them.

## The Relationship to Information Hiding

General-purpose interfaces hide **use-case-specific knowledge**. When an interface is general, callers don't need to know about other callers' use cases. This is a form of information hiding that reduces dependencies between callers.

A special-purpose interface like `sendWelcomeEmail()` creates a dependency: every developer who sees it must understand the welcome email use case. A general-purpose interface like `send(to, subject, body)` hides all specific use cases, reducing the information each developer must hold in mind.

## Summary

The goal is not the most general-purpose design possible. It is the **simplest interface that covers all current needs**. This sweet spot produces modules that are:
- Simple to use (few methods, few parameters)
- Flexible enough for current needs (no workarounds required)
- Future-friendly (new use cases often fit the existing abstraction)
- Deep (general interfaces tend to hide more implementation complexity)

When in doubt, lean slightly toward more general -- it is usually simpler. But stop well before building a framework for every conceivable future need.
