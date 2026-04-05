# Deep vs Shallow Modules

The concept of module depth is one of the most powerful ideas in Ousterhout's philosophy. It provides a concrete way to evaluate whether a module is pulling its weight in the system.


## Table of Contents
1. [The Core Idea](#the-core-idea)
2. [Visualizing Module Depth](#visualizing-module-depth)
3. [Examples of Deep Modules](#examples-of-deep-modules)
4. [Examples of Shallow Modules](#examples-of-shallow-modules)
5. [The Disease of Classitis](#the-disease-of-classitis)
6. [When Shallow Is Acceptable](#when-shallow-is-acceptable)
7. [Designing for Depth](#designing-for-depth)
8. [Measuring Depth in Practice](#measuring-depth-in-practice)
9. [Common Objections](#common-objections)

---

## The Core Idea

Every module has two parts:
- **Interface:** The complexity it imposes on the rest of the system (the cost)
- **Implementation:** The functionality it provides (the benefit)

A module's value is determined by the ratio of functionality provided to interface complexity imposed.

```
Module Value = Functionality / Interface Complexity
```

**Deep modules** have high value: they provide a lot of functionality through a simple interface. **Shallow modules** have low value: their interface is nearly as complex as their implementation, so they add little net simplification to the system.

## Visualizing Module Depth

Think of a module as a rectangle:
- Width at the top = interface complexity
- Height = implementation depth (functionality hidden)

```
Deep Module:               Shallow Module:
┌──────┐                   ┌──────────────────────┐
│      │                   │                      │
│      │                   └──────────────────────┘
│      │
│      │
│      │
│      │
└──────┘
Narrow interface,          Wide interface,
deep implementation.       shallow implementation.
```

The goal is tall, narrow rectangles: modules that hide substantial complexity behind small interfaces.

## Examples of Deep Modules

### Unix File I/O

The Unix file I/O interface is one of the deepest abstractions in computing:

```c
int open(const char *path, int flags);
int close(int fd);
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
off_t lseek(int fd, off_t offset, int whence);
```

Five functions. Behind this simple interface, the implementation handles:
- Disk block allocation and management
- Directory traversal and path resolution
- File permissions and access control
- Buffer caching and write-back strategies
- Device driver communication
- File system journal and crash recovery
- Network file system protocols (NFS)
- Memory-mapped file coordination
- Concurrent access and locking

The interface is measured in a few functions; the implementation is hundreds of thousands of lines of code. This is extreme depth.

### Garbage Collectors

A garbage collector's interface is essentially invisible:

```
Interface: (none -- just allocate objects normally)
```

Behind this zero-complexity interface, the implementation handles:
- Reference tracking and reachability analysis
- Generational collection strategies
- Compaction and memory defragmentation
- Concurrent collection without stopping the world
- Weak references and finalization
- Heap sizing and growth heuristics

The deepest modules are those whose interfaces are so simple that callers may not even realize they exist.

### TCP/IP Networking

```python
socket.send(data)
socket.recv(buffer_size)
```

Behind this:
- Packet segmentation and reassembly
- Retransmission and acknowledgment
- Flow control and congestion avoidance
- Routing across networks
- Checksum verification
- Connection state management
- Out-of-order packet handling

### Hash Maps

```python
map[key] = value
value = map[key]
del map[key]
```

Behind this:
- Hash function computation
- Collision resolution (chaining, open addressing)
- Dynamic resizing and rehashing
- Memory allocation strategies
- Load factor management
- Iterator invalidation handling

## Examples of Shallow Modules

### Java I/O Classes (Classic Example)

To read a serialized object from a file in Java:

```java
FileInputStream fileStream = new FileInputStream(filename);
BufferedInputStream bufferedStream = new BufferedInputStream(fileStream);
ObjectInputStream objectStream = new ObjectInputStream(bufferedStream);
```

Three classes, each adding a thin layer:
- `FileInputStream`: reads bytes from a file (no buffering)
- `BufferedInputStream`: adds buffering (why isn't this default?)
- `ObjectInputStream`: deserializes objects

Each class is shallow: its interface is nearly as complex as its implementation. The total cognitive load of three interfaces is greater than what a single deep interface would impose. A deep design would look like:

```java
ObjectInputStream stream = new ObjectInputStream(filename);
// Handles file opening, buffering, and deserialization internally
```

### Thin Wrapper Classes

```python
class UserValidator:
    def validate(self, user):
        if not user.name:
            raise ValueError("Name required")
        if not user.email:
            raise ValueError("Email required")

class UserSaver:
    def save(self, user):
        self.db.insert(user)

class UserService:
    def create_user(self, data):
        user = User(data)
        self.validator.validate(user)
        self.saver.save(user)
```

Three classes where one would suffice:

```python
class UserService:
    def create_user(self, data):
        user = User(data)
        if not user.name:
            raise ValueError("Name required")
        if not user.email:
            raise ValueError("Email required")
        self.db.insert(user)
```

The three-class version creates two additional interfaces (and their tests, files, and import chains) without providing meaningful abstraction. The validation and persistence logic is too simple to justify separate modules.

### Pass-Through Methods

```python
class OrderController:
    def create_order(self, request):
        order_data = self.parse_request(request)
        return self.order_service.create_order(order_data)

class OrderService:
    def create_order(self, order_data):
        validated = self.validate(order_data)
        return self.order_repository.create_order(validated)

class OrderRepository:
    def create_order(self, order_data):
        return self.db.insert("orders", order_data)
```

Each layer adds almost nothing. The `create_order` method appears three times, each just passing data to the next layer. This is a sign of shallow decomposition.

## The Disease of Classitis

**Classitis** is the misguided belief that "classes should be small" applied without judgment. It produces systems with hundreds of tiny classes, each doing very little, connected by a web of interfaces.

### Symptoms of Classitis

| Symptom | Example |
|---------|---------|
| Many classes with 10-30 lines each | `StringHelper`, `DateFormatter`, `NullChecker` |
| Most methods are one-liners or delegates | `getName() { return this.name; }` |
| Understanding a feature requires reading 8+ classes | Controller, Service, Repository, Mapper, Validator, DTO, Entity, Factory |
| Class names end in -Helper, -Util, -Manager, -Handler | `UserManager`, `OrderHandler`, `DataHelper` |
| Most classes have only 1-2 methods | A `Validator` class with only `validate()` |

### Why Classitis Happens

1. **Misinterpreted "Single Responsibility Principle"**: SRP says "one reason to change," not "one thing it does." A module can do many things if they all change together.
2. **Cargo cult patterns**: Applying patterns (Strategy, Factory, Builder) reflexively without evaluating whether they add depth.
3. **Metrics worship**: Optimizing for "small class size" or "few methods per class" instead of depth.
4. **Test-driven granularity**: Creating classes just to make them independently testable, even when they have no independent meaning.

### The Cure

Ask for each class: **"Does this class hide significant complexity behind its interface?"**

If the answer is no, it is a candidate for merging with another class. Fewer, deeper classes almost always produce simpler systems than many shallow ones.

## When Shallow Is Acceptable

Not every module needs to be deep. Shallow modules are acceptable when:

| Situation | Why It's OK | Example |
|-----------|------------|---------|
| **Dispatchers** | Routing logic is inherently shallow | A URL router that maps paths to handlers |
| **Interface adapters** | Translating between two deep modules | Converting between internal and external data formats |
| **Language/framework requirements** | The framework demands the class | Java servlets, Python ABC implementations |
| **Genuine one-liner utilities** | The abstraction is the name itself | `isEven(n)`, `clamp(value, min, max)` |
| **Entry points** | Top-level wiring that connects modules | The `main()` function, dependency injection configuration |

The key is that these shallow modules should be **rare exceptions**, not the norm. If most of your modules are shallow, the design needs rethinking.

## Designing for Depth

### Strategy 1: Combine Related Functionality

Instead of:
```
RequestParser + RequestValidator + RequestAuthorizer + RequestHandler + ResponseBuilder
```

Consider:
```
RequestHandler (parses, validates, authorizes, handles, and builds response)
```

If these operations always happen together and share knowledge about the request format, combining them into one deep module eliminates four interfaces and produces a simpler system.

### Strategy 2: Hide Implementation Decisions

Ask: "What decisions does this module make that no one else needs to know about?"

Each hidden decision adds depth. Good examples:
- Buffer sizes and caching strategies
- Retry logic and backoff policies
- Connection pooling and lifecycle management
- Data format and serialization details
- Concurrency and locking strategies

### Strategy 3: Provide Defaults

Instead of requiring callers to specify everything:

```python
# Shallow: caller must know about all options
def connect(host, port, timeout, retry_count, retry_delay,
            ssl_cert, ssl_key, keepalive, buffer_size):

# Deep: sensible defaults hide decisions
def connect(host, port=5432, **options):
    # Internally determines timeout, retries, SSL, etc.
```

### Strategy 4: Absorb Complexity

When two approaches exist -- one that is simpler for the module but pushes complexity to callers, and one that is harder to implement but simpler for callers -- choose the one that makes life easier for callers.

```python
# Pushes complexity to caller:
entries = log.read_raw()  # Returns raw bytes; caller must parse
parsed = parse_log_format(entries)  # Caller needs format knowledge

# Absorbs complexity:
entries = log.read()  # Returns parsed, structured entries
```

### Strategy 5: Question Every Interface Element

For each method, parameter, or return value in an interface, ask:
- "Do callers actually need this?"
- "Can the module decide this internally?"
- "Is there a simpler way to express this?"

Remove anything that does not earn its place. Every element in an interface is a cost that must be justified by the functionality it enables.

## Measuring Depth in Practice

### Quick Assessment

| Question | Deep | Shallow |
|----------|------|---------|
| How many methods in the interface? | Few (3-7) | Many (15+) |
| How many parameters per method? | Few (1-3) | Many (5+) |
| How long is the implementation? | Significantly larger than interface | About the same as interface |
| Can you describe the module in one sentence? | Yes | Need a paragraph |
| Does the module hide a non-trivial decision? | Yes, several | Not really |
| Would removing it require callers to duplicate code? | Lots of duplication | Minimal duplication |

### Depth Ratio

A rough heuristic: compare the lines of interface documentation to lines of implementation. If they are close to equal, the module is likely shallow. If the implementation is 5-10x larger than the interface description, the module is likely deep.

This is not about lines of code per se -- it is about the amount of hidden complexity relative to the exposed interface. A one-line interface like `gc.collect()` that hides thousands of lines of garbage collection logic is extremely deep.

## Common Objections

### "But small classes are easier to test!"

Small classes are easier to **unit test** in isolation, but the system is harder to **integration test** because you have more interfaces to mock, more interactions to verify, and more wiring to get right. Deeper modules that own more behavior are often easier to test at the level that matters: "does this feature work?"

### "But the Single Responsibility Principle says..."

SRP says a module should have "one reason to change," which is about **cohesion**, not about size. A module that handles all aspects of file I/O (opening, reading, writing, buffering, closing) changes for one reason: when file I/O requirements change. That is a single responsibility implemented deeply.

### "But what about separation of concerns?"

Separation of concerns is about keeping unrelated things apart, not about splitting related things into tiny pieces. If parsing, validating, and processing a request are all concerned with "handling a request," they can live in one module. Separate concerns that are genuinely independent (e.g., logging and business logic), not every step of a single workflow.
