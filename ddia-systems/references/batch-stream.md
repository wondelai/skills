# Batch and Stream Processing

Data processing systems fall into three categories: services (online systems that handle requests), batch processing (offline systems that process large volumes of accumulated data), and stream processing (near-real-time systems that process data as it arrives). Understanding when and how to use batch and stream processing is essential for building data pipelines, analytics systems, and derived data stores.


## Table of Contents
1. [Batch Processing: MapReduce and Beyond](#batch-processing-mapreduce-and-beyond)
2. [Dataflow Engines: Beyond MapReduce](#dataflow-engines-beyond-mapreduce)
3. [Event Sourcing](#event-sourcing)
4. [Change Data Capture (CDC)](#change-data-capture-cdc)
5. [Stream-Table Duality](#stream-table-duality)
6. [Exactly-Once Semantics](#exactly-once-semantics)
7. [Time Windowing](#time-windowing)
8. [Architecture Patterns](#architecture-patterns)

---

## Batch Processing: MapReduce and Beyond

### The MapReduce Paradigm

MapReduce, popularized by Google's 2004 paper, processes large datasets by breaking computation into two phases:

1. **Map phase:** Read input data, extract key-value pairs. Each mapper processes a portion of the input independently.
2. **Shuffle phase:** Framework groups all values by key, distributing them to reducers.
3. **Reduce phase:** For each key, combine all values into a result.

```
Input: ["the cat sat on the mat"]

Map:
  "the" -> 1
  "cat" -> 1
  "sat" -> 1
  "on"  -> 1
  "the" -> 1
  "mat" -> 1

Shuffle: Group by key
  "the" -> [1, 1]
  "cat" -> [1]
  "sat" -> [1]
  "on"  -> [1]
  "mat" -> [1]

Reduce: Sum values
  "the" -> 2
  "cat" -> 1
  "sat" -> 1
  "on"  -> 1
  "mat" -> 1
```

### MapReduce Strengths

- **Horizontal scalability:** Add more machines to process larger datasets; the framework handles distribution
- **Fault tolerance:** If a mapper or reducer fails, the framework re-executes that task on another machine. Input data is immutable, so re-execution is safe.
- **Simplicity:** The programmer only writes map and reduce functions; the framework handles parallelism, distribution, and fault tolerance

### MapReduce Weaknesses

- **High latency:** Each MapReduce job reads from and writes to distributed storage (HDFS), adding significant I/O overhead
- **Chaining is awkward:** Complex computations require chaining multiple MapReduce jobs, each with its own read/write cycle
- **No iteration support:** Machine learning algorithms that iterate over data must launch a new MapReduce job for each iteration
- **Limited expressiveness:** Not all computations fit the map-reduce pattern naturally

---

## Dataflow Engines: Beyond MapReduce

### Apache Spark

Spark replaces MapReduce with a more general computation model based on Resilient Distributed Datasets (RDDs) and directed acyclic graphs (DAGs) of operators.

**Key improvements over MapReduce:**
- **In-memory processing:** Intermediate results stay in memory instead of being written to disk between stages
- **Arbitrary DAGs:** Computations can have multiple stages with various operators (map, filter, join, group, sort), not just map and reduce
- **Lazy evaluation:** Spark builds a computation plan before executing, enabling the optimizer to eliminate unnecessary steps
- **Iterative algorithms:** RDDs can be cached in memory and reused across iterations

```python
# Spark: Word count
text_file = spark.read.text("hdfs://input/")
word_counts = (text_file
    .select(explode(split(col("value"), " ")).alias("word"))
    .groupBy("word")
    .count()
    .orderBy(desc("count")))
word_counts.write.parquet("hdfs://output/")
```

### Apache Flink

Flink treats batch processing as a special case of stream processing (a bounded stream). Its architecture is stream-first.

**Key features:**
- **True streaming:** Processes events one at a time (not micro-batches like Spark Streaming)
- **Event-time processing:** Handles out-of-order events based on when they occurred, not when they arrived
- **Exactly-once semantics:** Provides exactly-once processing guarantees through checkpointing
- **Savepoints:** Snapshot the entire pipeline state for upgrades, scaling, or debugging

### Comparison

| Feature | MapReduce | Spark | Flink |
|---------|-----------|-------|-------|
| **Processing model** | Batch only | Batch + micro-batch streaming | Batch + true streaming |
| **Intermediate storage** | Disk (HDFS) | Memory (spills to disk) | Memory (checkpoints to disk) |
| **Latency** | Minutes to hours | Seconds to minutes | Milliseconds to seconds |
| **Fault tolerance** | Re-execute failed tasks | Recompute lost RDD partitions | Checkpoint-based recovery |
| **Best for** | Very large batch jobs | Interactive analytics, ML | Real-time streaming, event-time processing |

---

## Event Sourcing

### Concept

Instead of storing the current state of an entity, store every state change as an immutable event. The current state is derived by replaying all events.

```
Traditional (mutable state):
  Account { id: 1, balance: 150 }

Event sourcing (immutable log):
  AccountCreated  { id: 1, balance: 0 }
  MoneyDeposited  { id: 1, amount: 200 }
  MoneyWithdrawn  { id: 1, amount: 50 }

  Current state = replay events: 0 + 200 - 50 = 150
```

### Benefits

- **Complete audit trail:** Every change is recorded with timestamp, actor, and context
- **Temporal queries:** "What was the balance on January 15?" Replay events up to that date
- **Event replay:** Rebuild read models, fix bugs by replaying with corrected logic, build new views from historical events
- **Debugging:** Reproduce any state by replaying the exact sequence of events
- **Decoupling:** Event producers and consumers can evolve independently

### Challenges

- **Event schema evolution:** Once events are stored, changing their schema is hard; use versioned event schemas
- **Eventual consistency:** Read models derived from events may lag behind the event log
- **Storage growth:** The event log grows forever; compaction or snapshotting is needed for old events
- **Complexity:** Building and maintaining projections (read models) adds architectural complexity

### Event Store Implementations

| Technology | Type | Key Feature |
|-----------|------|-------------|
| **EventStoreDB** | Purpose-built event store | Projections, subscriptions, optimistic concurrency |
| **Apache Kafka** | Distributed log | High throughput, log compaction, exactly-once semantics |
| **PostgreSQL** | Relational DB as event store | ACID transactions on event writes; LISTEN/NOTIFY for subscribers |
| **DynamoDB Streams** | Change stream | Automatic change capture from DynamoDB tables |

---

## Change Data Capture (CDC)

### Concept

CDC observes all writes to a database and extracts them as a stream of change events that can be consumed by other systems. This keeps derived data stores (search indexes, caches, analytics databases) in sync with the source of truth.

```
Application -> PostgreSQL (source of truth)
                   |
                   v (CDC)
              Kafka topic
              /    |    \
             v     v     v
    Elasticsearch  Redis  Data Warehouse
    (search)     (cache)  (analytics)
```

### CDC Implementation Approaches

| Approach | How It Works | Trade-off |
|----------|-------------|-----------|
| **Log-based (WAL parsing)** | Read the database's write-ahead log and extract changes | Most reliable; low overhead; captures all changes including those from direct SQL |
| **Trigger-based** | Database triggers write changes to an outbox table | Works with any database; adds write overhead; may miss changes from bulk operations |
| **Polling-based** | Periodically query for changed rows (using updated_at timestamp) | Simplest; misses deletes; can miss rapid changes between polls; adds query load |
| **Application-level** | Application explicitly writes events when modifying data | Full control; risk of forgetting to emit events; dual-write problem |

### CDC Tools

| Tool | Source Databases | Sink | Key Feature |
|------|-----------------|------|-------------|
| **Debezium** | PostgreSQL, MySQL, MongoDB, SQL Server, Oracle | Kafka | WAL-based; exactly-once; schema registry integration |
| **Maxwell** | MySQL only | Kafka, RabbitMQ, Redis | Lightweight; MySQL binlog parsing |
| **AWS DMS** | Most databases | Kafka, S3, Redshift, DynamoDB | Managed service; heterogeneous migration |
| **Fivetran/Airbyte** | Many sources | Data warehouses | Managed ELT platforms with CDC connectors |

### The Dual-Write Problem

A common anti-pattern is writing to two systems directly:

```
Application -> writes to PostgreSQL
           -> writes to Elasticsearch

Problem: If the Elasticsearch write fails after the PostgreSQL write succeeds,
the systems are now inconsistent. Retrying may cause duplicates.
```

**Solution:** Write to one system (PostgreSQL) and use CDC to propagate to the other. The CDC pipeline handles retries, ordering, and exactly-once delivery.

---

## Stream-Table Duality

### The Core Insight

A stream and a table are two sides of the same coin:

- **A stream is the changelog of a table.** If you record every INSERT, UPDATE, and DELETE to a table, that sequence of changes is a stream.
- **A table is the materialized state of a stream.** If you replay a stream of changes from the beginning, applying each change in order, you get the current table state.

```
Stream:
  INSERT user {id: 1, name: "Alice"}
  INSERT user {id: 2, name: "Bob"}
  UPDATE user {id: 1, name: "Alice Chen"}
  DELETE user {id: 2}

Table (materialized from stream):
  | id | name        |
  |----|-------------|
  | 1  | Alice Chen  |
```

### Practical Application: Kafka Log Compaction

Kafka's log compaction feature retains only the latest value for each key, effectively converting a stream into a table snapshot:

```
Before compaction:
  key=1, value="Alice"
  key=2, value="Bob"
  key=1, value="Alice Chen"
  key=2, value=null (tombstone)

After compaction:
  key=1, value="Alice Chen"
  (key=2 is deleted because value is null)
```

This allows a new consumer to read the compacted log and reconstruct the full current state without replaying the entire history.

---

## Exactly-Once Semantics

### The Challenge

In distributed systems, messages can be lost, duplicated, or reordered. "Exactly-once" means that the effect of processing each message is reflected exactly once in the output, even in the presence of failures.

### Achieving Exactly-Once

True exactly-once requires coordination between the messaging system and the processing logic:

| Approach | How It Works | Example |
|----------|-------------|---------|
| **Idempotent operations** | Design operations so that applying them multiple times has the same effect as applying once | `SET balance = 100` is idempotent; `INCREMENT balance BY 10` is not |
| **Transactional output** | Write output and update consumer offset in a single atomic transaction | Kafka Streams: transactional producer commits output records and consumer offsets together |
| **Deduplication** | Assign a unique ID to each message; recipient ignores messages it has already processed | Store processed message IDs in a set; check before processing |
| **Checkpointing** | Periodically save processing state; on failure, resume from last checkpoint | Flink savepoints: snapshot operator state and input positions |

---

## Time Windowing

### Why Windowing Matters

Unbounded streams have no natural "end," so you can't wait for all data before computing an aggregate. Windowing divides the stream into finite chunks for aggregation.

### Window Types

| Window Type | How It Works | Use Case |
|------------|-------------|----------|
| **Tumbling** | Fixed-size, non-overlapping windows (e.g., every 5 minutes) | Hourly metrics, daily summaries |
| **Hopping** | Fixed-size windows that overlap (e.g., 10-minute windows every 5 minutes) | Smoothed averages, sliding computations |
| **Session** | Variable-size windows based on activity gaps (e.g., a session ends after 30 minutes of inactivity) | User session analytics, click streams |
| **Global** | A single window for the entire stream | Running totals, all-time aggregates |

### Handling Late Events

Events may arrive after their window has closed (due to network delays, buffering, or clock skew):

- **Watermarks:** A timestamp that says "I believe all events before this time have arrived." Events arriving after the watermark are considered late.
- **Allowed lateness:** Accept late events up to a threshold (e.g., 1 hour after window closes), updating the window's result
- **Side outputs:** Route late events to a separate output for manual or delayed processing

```
Window: 10:00 - 10:05
Watermark: 10:06 (all events before 10:06 expected)
Allowed lateness: 1 hour

Event at 10:03 arriving at 10:07: accepted (within allowed lateness)
Event at 10:01 arriving at 11:30: discarded or sent to side output
```

---

## Architecture Patterns

### Lambda Architecture

Run both batch and stream processing pipelines in parallel:

```
Raw Data -> Batch Layer (Spark) -> Batch Views
         -> Speed Layer (Flink) -> Real-time Views

Query: Merge batch views + real-time views for complete result
```

**Pros:** Batch provides correctness; stream provides speed.
**Cons:** Maintaining two pipelines with the same logic is expensive and error-prone; results may differ between batch and stream.

### Kappa Architecture

Use a single stream processing pipeline for everything. Reprocess historical data by replaying the event log:

```
Event Log (Kafka) -> Stream Processor (Flink) -> Derived Views

Reprocessing: Start a new consumer from the beginning of the log
```

**Pros:** Single codebase; simpler architecture; easier to reason about.
**Cons:** Reprocessing large histories can be slow; requires a durable, replayable log (Kafka with long retention).

### Choosing Between Lambda and Kappa

Use **Lambda** when:
- Exact correctness is required and stream processing approximations are unacceptable
- You have existing batch infrastructure and are adding streaming incrementally

Use **Kappa** when:
- Your stream processing framework provides exactly-once guarantees
- You can afford to reprocess from the log when logic changes
- Simplicity and maintainability are priorities
