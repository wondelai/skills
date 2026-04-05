---
name: ddia-systems
description: 'Design data systems by understanding storage engines, replication, partitioning, transactions, and consistency models. Use when the user mentions "database choice", "replication lag", "partitioning strategy", "consistency vs availability", "stream processing", "ACID transactions", "eventual consistency", or "LSM tree vs B-tree". Also trigger when choosing between SQL and NoSQL, designing data pipelines, or debugging distributed system consistency issues. Covers data models, batch/stream processing, and distributed consensus. For system design, see system-design. For resilience, see release-it.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Designing Data-Intensive Applications Framework

A principled approach to building reliable, scalable, and maintainable data systems. Apply these principles when choosing databases, designing schemas, architecting distributed systems, or reasoning about consistency and fault tolerance.

## Core Principle

**Data outlives code.** Applications are rewritten, languages change, frameworks come and go -- but data and its structure persist for decades. Every architectural decision must prioritize the long-term correctness, durability, and evolvability of the data layer above all else.

**The foundation:** Most applications are data-intensive, not compute-intensive. The hard problems are the amount of data, its complexity, and the speed at which it changes. Understanding the trade-offs between consistency, availability, partition tolerance, latency, and throughput is what separates robust systems from fragile ones.

## Scoring

**Goal: 10/10.** When reviewing or designing data architectures, rate them 0-10 based on adherence to the principles below. A 10/10 means deliberate trade-off choices for data models, storage engines, replication, partitioning, transactions, and processing pipelines; lower scores indicate accidental complexity or ignored failure modes. Always provide the current score and specific improvements needed to reach 10/10.

## The DDIA Framework

Seven domains for reasoning about data-intensive systems:

### 1. Data Models and Query Languages

**Core concept:** The data model shapes how you think about the problem. Relational, document, and graph models each impose different constraints and enable different query patterns.

**Why it works:** Choosing the wrong data model forces application code to compensate for representational mismatch, adding accidental complexity that compounds over time.

**Key insights:**
- Relational models excel at many-to-many relationships and ad-hoc queries
- Document models excel at one-to-many relationships and data locality
- Graph models excel at highly interconnected data with recursive traversals
- Schema-on-write (relational) catches errors early; schema-on-read (document) offers flexibility
- Polyglot persistence -- use different stores for different access patterns -- is often the right answer
- Impedance mismatch between objects and relations is a real cost; document models reduce it for self-contained aggregates

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **User profiles with nested data** | Document model for self-contained aggregates | Store profile, addresses, and preferences in one MongoDB document |
| **Social network connections** | Graph model for relationship traversal | Neo4j Cypher query: `MATCH (a)-[:FOLLOWS*2]->(b)` for friend-of-friend |
| **Financial ledger with joins** | Relational model for referential integrity | PostgreSQL with foreign keys between accounts, transactions, and entries |
| **Mixed access patterns** | Polyglot persistence | PostgreSQL for transactions + Elasticsearch for full-text search + Redis for caching |

See: [references/data-models.md](references/data-models.md)

### 2. Storage Engines

**Core concept:** Storage engines make a fundamental trade-off between read performance and write performance. Log-structured engines (LSM trees) optimize writes; page-oriented engines (B-trees) balance reads and writes.

**Why it works:** Understanding the internals of your database's storage engine lets you predict performance characteristics, choose appropriate indexes, and avoid pathological workloads.

**Key insights:**
- LSM trees: append-only writes, periodic compaction, excellent write throughput, higher read amplification
- B-trees: in-place updates, predictable read latency, write amplification from page splits
- Write amplification means one logical write causes multiple physical writes -- critical for SSDs with limited write cycles
- Column-oriented storage dramatically improves analytical query performance through compression and vectorized processing
- In-memory databases are fast not because they avoid disk, but because they avoid encoding overhead

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **High write throughput** | LSM-tree engine | Cassandra or RocksDB for time-series ingestion at 100K+ writes/sec |
| **Mixed read/write OLTP** | B-tree engine | PostgreSQL B-tree indexes for transactional workloads with point lookups |
| **Analytical queries on large datasets** | Column-oriented storage | ClickHouse or Parquet files for scanning billions of rows with few columns |
| **Low-latency caching** | In-memory store | Redis for sub-millisecond lookups; Memcached for simple key-value caching |

See: [references/storage-engines.md](references/storage-engines.md)

### 3. Replication

**Core concept:** Replication keeps copies of data on multiple machines for fault tolerance, scalability, and latency reduction. The core challenge is handling changes to replicated data consistently.

**Why it works:** Every replication strategy trades off between consistency, availability, and latency. Making this trade-off explicit prevents subtle data anomalies that surface only under load or failure.

**Key insights:**
- Single-leader replication: simple, strong consistency possible, but the leader is a bottleneck and single point of failure
- Multi-leader replication: better write availability across data centers, but conflict resolution is complex
- Leaderless replication: highest availability, uses quorum reads/writes, but requires careful conflict handling
- Replication lag causes read-your-writes violations, monotonic read violations, and causality violations
- Synchronous replication guarantees durability but increases latency; asynchronous replication risks data loss on leader failure
- CRDTs and last-writer-wins are conflict resolution strategies with very different correctness guarantees

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Read-heavy web app** | Single-leader with read replicas | PostgreSQL primary + read replicas behind pgBouncer for read scaling |
| **Multi-region writes** | Multi-leader replication | CockroachDB or Spanner for geo-distributed writes with bounded staleness |
| **Shopping cart availability** | Leaderless with merge | DynamoDB with last-writer-wins or application-level merge for cart conflicts |
| **Collaborative editing** | CRDTs for conflict-free merging | Yjs or Automerge for real-time collaborative document editing |

See: [references/replication.md](references/replication.md)

### 4. Partitioning

**Core concept:** Partitioning (sharding) distributes data across multiple nodes so that each node handles a subset of the total data, enabling horizontal scaling beyond a single machine.

**Why it works:** Without partitioning, a single node becomes the bottleneck for storage capacity and throughput. Effective partitioning distributes load evenly and avoids hotspots.

**Key insights:**
- Key-range partitioning supports efficient range scans but risks hotspots on sequential keys
- Hash partitioning distributes load evenly but destroys sort order and makes range queries expensive
- Secondary indexes can be partitioned locally (each partition has its own index) or globally (index partitioned separately)
- Local secondary indexes require scatter-gather queries; global secondary indexes require cross-partition updates
- Hotspots can occur even with hash partitioning if a single key is extremely popular (celebrity problem)
- Rebalancing strategies: fixed number of partitions, dynamic splitting, or proportional to node count

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Time-series data** | Key-range partitioning by time + source | Partition by `(sensor_id, date)` to avoid write hotspot on current day |
| **User data at scale** | Hash partitioning on user ID | Cassandra consistent hashing on `user_id` for even distribution |
| **Global search index** | Global secondary index | Elasticsearch index sharded independently from primary data store |
| **Celebrity/hot-key problem** | Key splitting with random suffix | Append random digit to hot partition key, fan-out reads across 10 sub-partitions |

See: [references/partitioning.md](references/partitioning.md)

### 5. Transactions and Consistency

**Core concept:** Transactions provide safety guarantees (ACID) that simplify application code by letting you pretend failures and concurrency don't exist -- within the transaction's scope.

**Why it works:** Without transactions, every piece of application code must handle partial failures, race conditions, and concurrent modifications. Transactions move this complexity into the database where it can be handled correctly once.

**Key insights:**
- Isolation levels are a spectrum: read uncommitted, read committed, snapshot isolation (repeatable read), serializable
- Most databases default to read committed or snapshot isolation -- not serializable -- and application developers must understand the anomalies this permits
- Write skew occurs when two transactions read the same data, make decisions based on it, and write different records -- no row-level lock prevents this
- Serializable snapshot isolation (SSI) provides full serializability with optimistic concurrency -- no blocking, but aborts on conflict
- Two-phase locking provides serializability but causes contention and deadlocks under high concurrency
- Distributed transactions (two-phase commit) are expensive and fragile; avoid them when possible by designing around single-partition operations

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Account balance transfer** | Serializable transaction | `BEGIN; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;` |
| **Inventory reservation** | SELECT FOR UPDATE to prevent write skew | `SELECT stock FROM items WHERE id = X FOR UPDATE` before decrementing |
| **Read-heavy dashboards** | Snapshot isolation for consistent reads | PostgreSQL MVCC provides point-in-time snapshot without blocking writers |
| **Cross-service operations** | Saga pattern instead of distributed transactions | Compensating transactions: charge card, reserve inventory, on failure refund card |

See: [references/transactions.md](references/transactions.md)

### 6. Batch and Stream Processing

**Core concept:** Batch processing transforms bounded datasets in bulk; stream processing transforms unbounded event streams continuously. Both are forms of derived data computation.

**Why it works:** Separating the system of record (source of truth) from derived data (caches, indexes, materialized views) allows each to be optimized independently and rebuilt from the source when requirements change.

**Key insights:**
- MapReduce is conceptually simple but operationally awkward; dataflow engines (Spark, Flink) generalize it with arbitrary DAGs
- Event sourcing stores every state change as an immutable event, enabling full audit trails and temporal queries
- Change data capture (CDC) turns database writes into a stream that downstream systems can consume
- Stream-table duality: a stream is the changelog of a table; a table is the materialized state of a stream
- Exactly-once semantics in stream processing require idempotent operations or transactional output
- Time windowing (tumbling, hopping, session) is essential for aggregating unbounded streams

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Daily analytics pipeline** | Batch processing with Spark | Read day's events from S3, aggregate metrics, write to data warehouse |
| **Real-time fraud detection** | Stream processing with Flink | Consume payment events from Kafka, apply rules within 5-second tumbling windows |
| **Syncing search index** | Change data capture | Debezium captures PostgreSQL WAL changes, publishes to Kafka, Elasticsearch consumer updates index |
| **Audit trail / event replay** | Event sourcing | Store `OrderPlaced`, `OrderShipped`, `OrderRefunded` events; rebuild current state by replaying |

See: [references/batch-stream.md](references/batch-stream.md)

### 7. Reliability and Fault Tolerance

**Core concept:** Faults are inevitable; failures are not. A reliable system continues operating correctly even when individual components fail. Design for faults, not against them.

**Why it works:** Hardware fails, software has bugs, humans make mistakes. Systems that assume perfect operation are brittle. Systems that expect and handle faults gracefully are resilient.

**Key insights:**
- A fault is one component deviating from spec; a failure is the system as a whole stopping. Fault tolerance prevents faults from becoming failures
- Hardware faults are random and independent; software faults are correlated and systematic (more dangerous)
- Human error is the leading cause of outages -- design systems that minimize opportunity for mistakes and maximize ability to recover
- Timeouts are the fundamental fault detector in distributed systems -- but choosing the right timeout is hard (too short causes false positives, too long delays recovery)
- Safety properties (nothing bad happens) must always hold; liveness properties (something good eventually happens) may be temporarily violated
- Byzantine fault tolerance is rarely needed outside blockchain -- most systems assume non-Byzantine (crash-stop or crash-recovery) models

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Service communication** | Timeouts + retries with exponential backoff | `retry(max=3, backoff=exponential(base=1s, max=30s))` with jitter |
| **Leader election** | Consensus algorithm (Raft/Paxos) | etcd or ZooKeeper for distributed lock and leader election |
| **Data pipeline reliability** | Idempotent operations + checkpointing | Kafka consumer commits offset only after successful processing |
| **Graceful degradation** | Circuit breaker pattern | Hystrix/Resilience4j: open circuit after 50% failures in 10-second window |

See: [references/fault-tolerance.md](references/fault-tolerance.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **Choosing a database based on popularity** | Different engines have fundamentally different trade-offs | Match storage engine characteristics to your actual read/write patterns |
| **Ignoring replication lag** | Users see stale data, phantom reads, or lost updates | Implement read-your-writes consistency; use monotonic read guarantees |
| **Using distributed transactions everywhere** | Two-phase commit is slow and fragile; coordinator is a single point of failure | Design for single-partition operations; use sagas for cross-service coordination |
| **Hash partitioning everything** | Destroys range query ability; some workloads need sorted access | Use key-range partitioning for time-series; composite keys for locality |
| **Assuming serializable isolation** | Most databases default to weaker isolation; write skew bugs appear in production | Check your database's actual default isolation level; use explicit locking where needed |
| **Conflating batch and stream** | Batch tools on streaming data add latency; stream tools on bounded data waste complexity | Match processing model to data boundedness and latency requirements |
| **Treating all faults as recoverable** | Some failures (data corruption, Byzantine) require fundamentally different handling | Classify faults and design specific recovery strategies for each class |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you explain why you chose this database over alternatives? | Decision was based on familiarity, not requirements | Evaluate data model fit, read/write ratio, consistency needs, and scaling path |
| Do you know your database's default isolation level? | You may have concurrency bugs you haven't found yet | Check documentation; test for write skew and phantom read scenarios |
| Is your replication strategy explicitly chosen (not defaulted)? | You have implicit assumptions about consistency and durability | Document trade-offs: sync vs async, failover behavior, lag tolerance |
| Can your system handle a hot partition key? | A single popular entity can bring down the cluster | Add key-splitting strategy or application-level load shedding for hot keys |
| Do you separate your system of record from derived data? | Schema changes or new features require migrating everything | Introduce CDC or event sourcing to decouple source from derived stores |
| Are your timeouts and retries tuned, not defaulted? | You get cascading failures or unnecessary delays | Measure p99 latency; set timeouts above p99 but below cascade threshold |
| Have you tested failover in production conditions? | Your recovery plan is theoretical, not validated | Run chaos engineering experiments: kill leaders, partition networks, fill disks |

## Reference Files

- [data-models.md](references/data-models.md): Relational vs document vs graph models, schema-on-read vs schema-on-write, query languages, polyglot persistence
- [storage-engines.md](references/storage-engines.md): LSM trees vs B-trees, write amplification, compaction, column-oriented storage, in-memory databases
- [replication.md](references/replication.md): Single-leader, multi-leader, leaderless replication, replication lag, conflict resolution, CRDTs
- [partitioning.md](references/partitioning.md): Key-range vs hash partitioning, secondary indexes, rebalancing, request routing, hotspots
- [transactions.md](references/transactions.md): ACID, isolation levels, write skew, two-phase locking, SSI, distributed transactions
- [batch-stream.md](references/batch-stream.md): MapReduce, dataflow engines, event sourcing, CDC, stream-table duality, exactly-once semantics
- [fault-tolerance.md](references/fault-tolerance.md): Faults vs failures, reliability metrics, timeouts, consensus, safety and liveness guarantees

## Further Reading

This skill is based on Martin Kleppmann's comprehensive guide to the principles and practicalities of data systems. For the complete treatment with detailed diagrams and research references:

- [*"Designing Data-Intensive Applications"*](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321?tag=wondelai00-20) by Martin Kleppmann

## About the Author

**Martin Kleppmann** is a researcher in distributed systems and a former software engineer at LinkedIn and Rapportive. He is a Senior Research Associate at the University of Cambridge and has worked extensively on CRDTs, Byzantine fault tolerance, and local-first software. *Designing Data-Intensive Applications* (2017) has become the definitive reference for engineers building data systems, praised for making complex distributed systems concepts accessible through clear explanations and practical examples. Kleppmann's research focuses on data consistency, decentralized collaboration, and ensuring correctness in distributed systems. He is also known for his conference talks and educational writing that bridge the gap between academic research and industrial practice.
