# Comments as Design Documentation

Comments are one of the most debated topics in software engineering. Ousterhout argues that comments are not merely helpful -- they are essential design documentation that captures information that cannot be expressed in code. The belief that "good code is self-documenting" is partially true for implementation details, but dangerously wrong for abstractions, design decisions, and cross-cutting concerns.


## Table of Contents
1. [Why Comments Matter](#why-comments-matter)
2. [The Four Types of Comments](#the-four-types-of-comments)
3. [Comment-Driven Design](#comment-driven-design)
4. [The "Self-Documenting Code" Myth](#the-self-documenting-code-myth)
5. [Maintaining Comments](#maintaining-comments)
6. [Comments Anti-Patterns](#comments-anti-patterns)
7. [Summary](#summary)

---

## Why Comments Matter

Code tells you **what** the program does. Comments tell you:
- **Why** it does it that way
- **What** the abstraction promises (the contract)
- **What** assumptions the code makes
- **What** alternatives were considered and rejected
- **What** constraints link this code to other modules
- **What** is not obvious from reading the code

Without comments, this information exists only in the original developer's head. When that developer moves on, the information is lost. Future developers must reverse-engineer intent from implementation -- an error-prone process that leads to incorrect changes and accumulated complexity.

## The Four Types of Comments

### 1. Interface Comments

**Purpose:** Define the abstraction that a module, class, or function presents to its users.

**This is the most important type of comment.** Interface comments form the contract between a module and its callers. They should describe:
- What the function/method does (at an abstract level)
- What each parameter means and its constraints
- What the return value represents
- What side effects occur
- What exceptions can be thrown and under what conditions
- What the caller must ensure before calling (preconditions)
- What the caller can assume after the call (postconditions)

**Examples:**

```python
def find_nearest(target: Point, candidates: list[Point],
                 max_distance: float = inf) -> Point | None:
    """Find the candidate point closest to target.

    Returns the nearest point from candidates, or None if no candidate
    is within max_distance of target. If multiple candidates are
    equidistant, returns the one that appears first in the list.

    Args:
        target: The reference point to measure distances from.
        candidates: Points to search. Must not be empty.
        max_distance: Maximum Euclidean distance to consider.
            Points farther than this are ignored. Defaults to
            infinity (consider all points).

    Returns:
        The nearest Point, or None if all candidates exceed
        max_distance.

    Raises:
        ValueError: If candidates is empty.
    """
```

```java
/**
 * Acquire a database connection from the pool.
 *
 * Blocks until a connection is available or the timeout expires.
 * The returned connection is guaranteed to be valid (tested with
 * a lightweight query before returning). The caller MUST close
 * the connection when done, which returns it to the pool.
 *
 * @param timeout maximum time to wait for a connection
 * @return a valid, open database connection
 * @throws TimeoutException if no connection is available within timeout
 * @throws PoolExhaustedException if the pool is permanently full
 *     (all connections in use and at max capacity)
 */
public Connection acquire(Duration timeout)
```

**Key rules for interface comments:**
- Describe the abstraction, not the implementation
- If the comment mentions implementation details (algorithms, data structures, internal variables), it is too detailed
- A developer should be able to use the module correctly by reading only the interface comment, without reading any implementation code
- If you cannot write a clear interface comment, the interface may be poorly designed

### 2. Data Structure Member Comments

**Purpose:** Explain the meaning, constraints, and invariants of fields in a class or data structure.

Field names alone rarely convey all the information a developer needs. Comments should clarify:
- What the field represents (especially if the name is ambiguous)
- Units and encoding (milliseconds? seconds? UTC? local time?)
- Valid ranges and boundary conditions
- Relationships with other fields
- When the field is set and when it may be null/zero

**Examples:**

```python
class RetryConfig:
    # Maximum number of retry attempts before giving up.
    # Does not count the initial attempt, so total attempts = max_retries + 1.
    # Set to 0 to disable retries.
    max_retries: int

    # Base delay between retries in milliseconds.
    # Actual delay uses exponential backoff: base_delay_ms * 2^attempt.
    # Jitter of +/- 20% is applied to prevent thundering herd.
    base_delay_ms: int

    # Maximum delay cap in milliseconds. Exponential backoff will
    # not exceed this value regardless of attempt number.
    # Must be >= base_delay_ms.
    max_delay_ms: int
```

```java
class PageCache {
    // Maps page_id to cached page content. Entries are evicted
    // in LRU order when the cache exceeds maxEntries. A page
    // present in this map is guaranteed to match the on-disk
    // version as of the last sync (see lastSyncTime).
    private Map<Long, Page> cache;

    // Timestamp of the last cache synchronization with disk,
    // in epoch milliseconds (UTC). All cache entries are valid
    // as of this time. Writes after this time may not be reflected.
    private long lastSyncTime;

    // Upper bound on cache entries. When exceeded, the least
    // recently accessed entry is evicted before inserting a new one.
    // Invariant: cache.size() <= maxEntries at all times.
    private int maxEntries;
}
```

### 3. Implementation Comments

**Purpose:** Explain **why** the code does something a particular way, or clarify non-obvious logic.

Implementation comments should not describe **what** the code does -- that should be clear from reading the code itself. They should explain:
- Why this approach was chosen over alternatives
- What non-obvious constraint or edge case the code handles
- What would go wrong if the code were changed in an obvious-seeming way
- Performance considerations that drove the implementation choice

**Good implementation comments:**

```python
# Use binary search instead of linear scan because the list is sorted
# and can contain 100k+ entries. Linear scan caused 200ms latency
# in production (see incident #4521).
index = bisect.bisect_left(sorted_entries, target)
```

```python
# Process items in reverse order to avoid index invalidation when
# removing elements. Forward iteration would skip elements after
# each removal.
for i in range(len(items) - 1, -1, -1):
    if should_remove(items[i]):
        items.pop(i)
```

```python
# Intentionally catching broad Exception here because the third-party
# library can throw undocumented exceptions (observed RuntimeError,
# ValueError, and OSError in production). We log and continue rather
# than crash the batch job.
try:
    result = third_party_lib.process(data)
except Exception as e:
    logger.warning(f"Processing failed for {data.id}: {e}")
    result = default_result()
```

**Bad implementation comments (just repeat the code):**

```python
# Increment counter
counter += 1

# Check if user is active
if user.is_active:

# Loop through items
for item in items:

# Return the result
return result
```

These comments add no information. The code already says what it does. Remove them.

### 4. Cross-Module Comments

**Purpose:** Document dependencies and design decisions that span multiple modules.

These are the hardest comments to maintain but often the most critical, because cross-module relationships are the biggest source of unknown unknowns.

**Examples:**

```python
# This timeout value must be longer than the retry timeout in
# RetryPolicy (currently 30s with 3 retries = 90s max). If this
# timeout is shorter, the caller will give up before retries complete.
# See: src/retry/policy.py:RetryPolicy.MAX_TOTAL_DURATION
REQUEST_TIMEOUT_SECONDS = 120
```

```python
# The field order in this struct must match the binary protocol
# defined in docs/protocol-v3.md section 4.2. The client parser
# (client/src/parser.rs) reads fields in this exact order.
# Changing field order here requires updating both the docs and
# the client parser.
class ServerMessage:
    version: int      # 2 bytes, big-endian
    message_type: int # 1 byte
    payload_len: int  # 4 bytes, big-endian
    payload: bytes    # payload_len bytes
```

```java
/**
 * IMPORTANT: This method is called by the EventBus on a background
 * thread. It must not access the UI thread directly. Use
 * Platform.runLater() for any UI updates.
 *
 * The EventBus guarantees at-least-once delivery, so this handler
 * must be idempotent. See EventBus.subscribe() docs for details.
 */
public void onOrderCompleted(OrderCompletedEvent event) {
```

**Best practices for cross-module comments:**
- Place the comment in the most likely place a developer would look
- Reference the other module explicitly (file path, class name)
- Explain what would go wrong if the relationship were violated
- Consider using a shared constants file for values that must stay in sync

## Comment-Driven Design

**Write the comments before writing the code.**

This is one of Ousterhout's most practical recommendations. The process:

1. **Write the interface comment first:** Before writing any implementation, write the comment that describes what the function/class/module does, what its parameters mean, and what it returns.

2. **Evaluate the design:** If the interface comment is hard to write, unclear, or requires mentioning implementation details, the interface design is probably wrong. Redesign the interface until the comment is clean and simple.

3. **Write the implementation:** With a clear interface comment as your guide, the implementation has a clear target.

4. **Add implementation comments:** As you write code, add comments for any non-obvious decisions.

### Why Comment-Driven Design Works

| Benefit | Explanation |
|---------|-------------|
| Forces clear thinking | Writing what something does before how reveals confusion early |
| Catches bad abstractions | If you can't describe the interface simply, it's too complex |
| Produces better interfaces | The act of writing clarifies what callers actually need |
| Comments stay accurate | Written alongside the design, not retrofitted later |
| Saves time | Avoids implementing a design that turns out to be wrong |

### Example

**Step 1:** Write the interface comment.

```python
def merge_sorted_streams(*streams: Iterator[T],
                          key: Callable = None) -> Iterator[T]:
    """Merge multiple sorted iterators into a single sorted iterator.

    Each input stream must be sorted in ascending order (or by key
    if provided). The output yields all elements from all streams
    in globally sorted order. Memory usage is O(num_streams),
    regardless of stream length.

    Equal elements are yielded in the order their source streams
    appear in the arguments (stable merge).
    """
```

**Step 2:** Evaluate. Is this clear? Can a caller use this without reading the implementation? What about edge cases -- empty streams, single stream, duplicate elements? Add those details if needed.

**Step 3:** Implement. The comment now serves as the specification.

## The "Self-Documenting Code" Myth

The claim that "good code doesn't need comments" contains a kernel of truth but is dangerously incomplete.

### Where Self-Documenting Code Works

Code **can** document itself for low-level implementation details:

```python
# This is self-documenting -- no comment needed:
total_price = sum(item.price for item in cart.items)
is_eligible = user.age >= 18 and user.has_valid_id
filtered = [x for x in data if x.is_active and x.score > threshold]
```

Good variable names, clear control flow, and simple expressions make the **what** obvious. Comments that restate this are noise.

### Where Self-Documenting Code Fails

Code **cannot** document:

| Information | Why Code Can't Express It | Example |
|------------|--------------------------|---------|
| **Abstractions** | Code shows implementation, not the promise | An interface's contract and guarantees |
| **Why** | Code shows what happens, not why this approach | Why binary search instead of hash lookup |
| **Constraints** | Code enforces constraints but doesn't explain them | Why a timeout is set to 120 seconds |
| **Design alternatives** | Code shows the choice made, not choices rejected | Why we chose polling over webhooks |
| **Cross-module relationships** | Code in one module can't describe its relationship to another | This timeout must match the retry config |
| **Performance rationale** | Optimized code is often less readable | Why we denormalized this data structure |
| **Assumptions** | Code operates on assumptions it cannot state | "This list is always sorted by the caller" |

### The Practical Rule

**Use self-documenting code for the "what" (implementation). Use comments for the "why" (design decisions), the "what" at a higher level (abstractions/interfaces), and the "beware" (non-obvious constraints and relationships).**

## Maintaining Comments

Comments that are wrong are worse than no comments. Here are strategies for keeping them accurate:

### 1. Place Comments Near the Code

The closer a comment is to the code it describes, the more likely it will be updated when the code changes. Interface comments in the function signature are better than comments in a separate documentation file.

### 2. Avoid Duplicating Information

If the same information is stated in a comment and enforced in code, one will eventually become stale. State each fact once.

```python
# Bad: duplicates the type annotation
# max_retries is an integer representing the maximum number of retries
max_retries: int  # The type already says it's an int

# Good: adds information not in the code
# Set to 0 to disable retries. Values > 10 are capped at 10 to prevent
# excessive load on the downstream service during outages.
max_retries: int
```

### 3. Update Comments in the Same Commit

Make it a code review norm: if you change a function's behavior, you must update its interface comment in the same commit. Stale comments are a code review finding.

### 4. Use Comments as a Design Smell Detector

If a comment is hard to write, the code may be too complex. If a comment needs to be very long, the interface may be doing too much. If a comment keeps going out of date, the module's boundaries may be wrong. Difficult comments are a signal, not just a chore.

### 5. Treat Comment Quality as a Review Criterion

In code reviews, evaluate comments alongside code:
- Are interface comments complete and accurate?
- Do implementation comments explain why, not what?
- Are cross-module comments present where needed?
- Are there missing comments on non-obvious code?

## Comments Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Comment repeats the code** | Adds noise, no information | Delete it; let the code speak for implementation details |
| **Comment describes what, not why** | Misses the valuable information | Rewrite to explain the reasoning or design decision |
| **Comment on every line** | Obscures code, hard to maintain | Comment only non-obvious sections; trust clear code |
| **TODO without context** | "TODO: fix this" is useless months later | Include the issue number, the problem, and the fix direction |
| **Commented-out code** | Dead code that confuses readers | Delete it; version control preserves history |
| **Banner comments** | `/////// SECTION ///////` adds structure without information | Use meaningful function/class boundaries instead |
| **Apology comments** | "Sorry, this is a hack" acknowledges but doesn't fix | Fix the hack or add context on why it is necessary and when it can be fixed |
| **Stale comments** | Describe behavior that no longer exists | Update or remove in the same commit as the code change |

## Summary

Comments are not a sign of bad code. They are design documentation that captures the most valuable and perishable information in a system: the designer's intent, the abstraction's contract, and the non-obvious relationships between components. Write interface comments first, maintain them alongside code, and use them as a tool for thinking clearly about design.
