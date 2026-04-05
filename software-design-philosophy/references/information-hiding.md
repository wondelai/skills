# Information Hiding and Information Leakage

Information hiding is the most important technique for achieving deep modules. It was first articulated by David Parnas in 1971 and remains the foundation of good software design. Information leakage is its opposite -- and one of the most common sources of unnecessary complexity.


## Table of Contents
1. [The Information Hiding Principle](#the-information-hiding-principle)
2. [Information Leakage](#information-leakage)
3. [Reducing Information Leakage](#reducing-information-leakage)
4. [Case Study: HTTP Request Handling](#case-study-http-request-handling)
5. [Information Hiding Checklist](#information-hiding-checklist)
6. [Relationship to Other Principles](#relationship-to-other-principles)

---

## The Information Hiding Principle

**Each module should encapsulate a few design decisions, and its interface should reveal as little as possible about those decisions.**

The "information" being hidden includes:
- Data representations and storage formats
- Algorithms and implementation strategies
- Communication protocols and wire formats
- Caching strategies and performance optimizations
- Error handling details and recovery mechanisms
- Hardware and OS-specific details
- Concurrency and synchronization strategies
- Configuration and default values

### Why Information Hiding Reduces Complexity

1. **Reduces dependencies:** If callers don't know about an implementation detail, they can't depend on it. Changes to hidden information affect only the module that owns it.

2. **Reduces cognitive load:** Developers using the module need to understand only its interface, not its internals. The hidden information is complexity that is removed from their mental model.

3. **Eliminates unknown unknowns:** When information is properly hidden, there is nothing hidden that callers need to know. The interface is the complete contract.

4. **Enables independent evolution:** Hidden implementations can be changed, optimized, or replaced without affecting any caller.

## Information Leakage

**Information leakage occurs when a design decision is reflected in multiple modules.** It creates a dependency on that decision: if it changes, all modules that know about it must change too.

### Forms of Information Leakage

#### 1. Interface Leakage (Most Obvious)

The module's interface directly exposes implementation details.

```python
# Leaking: interface exposes file format details
class UserStore:
    def save_as_json(self, user, filepath):
        ...
    def load_from_json(self, filepath) -> User:
        ...

# Hiding: interface abstracts storage format
class UserStore:
    def save(self, user):
        ...
    def load(self, user_id) -> User:
        ...
```

In the leaking version, every caller knows the storage format is JSON. Switching to a database requires changing every caller. In the hiding version, the storage mechanism is an internal decision.

#### 2. Back-Door Leakage (Most Subtle)

Two modules share knowledge that is not part of either interface, often through shared data formats, file conventions, or implicit protocols.

```python
# Module A writes:
with open("data.csv") as f:
    f.write(f"{user.id},{user.name},{user.email}\n")

# Module B reads (far away in the codebase):
with open("data.csv") as f:
    for line in f:
        id, name, email = line.strip().split(",")
```

Both modules know the CSV format (comma-separated, field order: id, name, email). This knowledge is not in either module's interface. If the format changes, both must change, but there is no compiler error or type check to guide you. This is a classic unknown unknown.

**Fix:** Create a single module that owns the data format:

```python
class UserCsvStore:
    def write(self, user):
        ...
    def read_all(self) -> list[User]:
        ...
```

#### 3. Temporal Leakage

Code is split based on when things happen rather than what knowledge they share.

```python
# Temporal decomposition: split by time
class HttpRequestReader:
    def read_headers(self, socket) -> dict:
        # Knows HTTP header format
        ...

class HttpRequestParser:
    def parse_body(self, headers, socket) -> Body:
        # Also knows HTTP header format (Content-Length, Content-Type)
        ...

class HttpResponseWriter:
    def write_response(self, socket, status, headers, body):
        # Also knows HTTP format
        ...
```

All three modules know the HTTP format, even though they are split into "read," "parse," and "write" phases. The temporal decomposition forces shared knowledge across module boundaries.

**Fix:** Organize by knowledge, not by time:

```python
class HttpConnection:
    def receive_request(self, socket) -> HttpRequest:
        # All HTTP format knowledge lives here
        ...
    def send_response(self, socket, response: HttpResponse):
        # All HTTP format knowledge lives here
        ...
```

#### 4. Decorator Leakage

The Decorator pattern is a frequent source of leakage because the decorator must understand the full interface of the object it wraps.

```java
// The decorator knows everything about InputStream's interface
class LoggingInputStream extends InputStream {
    private InputStream wrapped;

    public int read() {
        log("reading one byte");
        return wrapped.read();  // Pass-through
    }

    public int read(byte[] b) {
        log("reading into buffer");
        return wrapped.read(b);  // Pass-through
    }

    public int read(byte[] b, int off, int len) {
        log("reading with offset");
        return wrapped.read(b, off, len);  // Pass-through
    }

    // Must implement every InputStream method...
}
```

The decorator is shallow: it adds minimal functionality (logging) but must duplicate the entire interface. Every change to `InputStream` propagates to every decorator.

**Better alternatives:**
- Add logging inside the original class (flag-controlled)
- Use aspect-oriented approaches that don't require interface duplication
- Add a hook/callback mechanism inside the deep module

### How to Detect Information Leakage

| Signal | What It Means |
|--------|--------------|
| Two modules that "always change together" | They share knowledge that should be in one place |
| A data format or protocol mentioned in multiple files | Format knowledge has leaked |
| Tests that break when internal implementation changes | Test code has leaked knowledge about internals |
| Comments like "must match format in module X" | Explicit acknowledgment of leakage |
| Global constants shared across modules | Shared knowledge that may indicate coupling |
| Similar parsing/formatting code in multiple modules | Format knowledge is duplicated |

## Reducing Information Leakage

### Strategy 1: Merge Modules That Share Knowledge

If two modules share knowledge about a design decision, consider merging them. The result is one module that encapsulates the decision, with a single interface for the rest of the system.

**Before:**
```python
class ConfigReader:
    def read(self, path) -> dict:
        # Knows config file format
        ...

class ConfigApplier:
    def apply(self, config: dict):
        # Also knows config structure
        ...
```

**After:**
```python
class ConfigManager:
    def load_and_apply(self, path):
        # All config knowledge in one place
        ...
```

### Strategy 2: Create a New Module for Shared Knowledge

If merging is not practical (the modules are genuinely different concerns), extract the shared knowledge into a new module that both depend on.

**Before:**
```python
# In api_handler.py:
def format_error(code, message):
    return {"error": {"code": code, "message": message, "timestamp": now()}}

# In webhook_handler.py:
def format_error(code, message):
    return {"error": {"code": code, "message": message, "timestamp": now()}}
```

**After:**
```python
# In error_format.py:
def format_error(code, message):
    return {"error": {"code": code, "message": message, "timestamp": now()}}

# Both api_handler and webhook_handler import from error_format
```

### Strategy 3: Push Knowledge Downward

Move knowledge from callers into the module they call. This deepens the module and simplifies its interface.

**Before:**
```python
# Caller must know about retry strategy
for attempt in range(3):
    try:
        result = api_client.call(endpoint, data)
        break
    except TransientError:
        time.sleep(2 ** attempt)
```

**After:**
```python
# Module handles retries internally
result = api_client.call(endpoint, data)
# Retries, backoff, and error classification are hidden inside api_client
```

### Strategy 4: Separate Interface from Implementation Physically

Use language mechanisms to enforce information hiding:

| Language | Mechanism | Effect |
|----------|----------|--------|
| Python | Underscore prefix (`_private_method`) | Convention-based hiding |
| Java/C# | `private`/`protected` keywords | Compiler-enforced hiding |
| Go | Lowercase names (unexported) | Package-level hiding |
| Rust | `pub` vs non-`pub` | Module-level hiding |
| TypeScript | `private`, `#field`, module scope | Multiple levels of hiding |

### Strategy 5: Design Interfaces Around Abstractions

An interface should describe **what** the module does at an abstract level, not **how** it does it.

```python
# Leaking (how):
class Cache:
    def get_from_lru(self, key): ...
    def put_with_ttl(self, key, value, ttl_seconds): ...
    def evict_lru_entries(self, count): ...

# Hiding (what):
class Cache:
    def get(self, key): ...
    def put(self, key, value): ...
    # LRU policy, TTL, eviction are internal decisions
```

## Case Study: HTTP Request Handling

A web server must read an HTTP request (headers and body), route it to a handler, process it, and send a response. Here is how temporal decomposition causes leakage versus how information-based decomposition avoids it.

### Temporal Decomposition (Problematic)

```
Phase 1: Read raw bytes from socket → knows HTTP header format
Phase 2: Parse headers → knows HTTP header format
Phase 3: Read body based on Content-Length → knows header meaning
Phase 4: Route to handler → knows URL format from headers
Phase 5: Build response → knows HTTP response format
Phase 6: Write response to socket → knows HTTP format
```

HTTP format knowledge is spread across 6 phases. Changing anything about the HTTP handling requires touching all of them.

### Information-Based Decomposition (Better)

```
HttpProtocol module:
  - Owns ALL knowledge of HTTP format (headers, body, status codes)
  - Reads socket → produces HttpRequest objects
  - Takes HttpResponse objects → writes to socket

Router module:
  - Owns URL pattern matching
  - Maps HttpRequest to handler function

Handler modules:
  - Work with high-level HttpRequest/HttpResponse objects
  - Know nothing about raw HTTP format
```

Now HTTP format knowledge lives in one place. The router knows only about URL patterns. Handlers know only about request/response objects. Each module hides its specific knowledge.

## Information Hiding Checklist

For each module in your system, ask:

| Question | Desired Answer |
|----------|---------------|
| What design decisions does this module hide? | At least one significant decision |
| Could the implementation be replaced without changing callers? | Yes |
| Does the interface mention implementation-specific concepts? | No |
| Do tests verify behavior or implementation? | Behavior |
| Are there other modules that share knowledge about the same implementation detail? | No |
| If this module's internal format changes, how many other modules must change? | Zero |

If any answer is unsatisfactory, information is leaking and the design should be reconsidered.

## Relationship to Other Principles

- **Deep modules** achieve depth primarily through information hiding -- the hidden information is what makes them deep
- **General-purpose interfaces** hide specific use cases, which is a form of information hiding
- **Comments** should describe the interface (what is visible) without revealing hidden implementation details
- **Strategic programming** is the mindset that makes developers willing to invest effort in proper information hiding rather than taking shortcuts that leak
