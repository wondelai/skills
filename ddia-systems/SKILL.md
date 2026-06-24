---
name: ddia-systems
description: 'Design data systems by understanding storage engines, replication, partitioning, transactions, and consistency models. Use when the user mentions "database choice", "which database should I use", "SQL or NoSQL", "replication lag", "partitioning strategy", "consistency vs availability", "stream processing", "ACID transactions", "eventual consistency", "my queries are slow at scale", or "data is inconsistent across replicas". Also trigger when choosing a datastore, designing data pipelines, or debugging distributed-system consistency issues. Covers data models, batch/stream processing, and distributed consensus. For system design, see system-design. For resilience, see release-it.'
license: MIT
metadata:
  author: wondelai
  version: "1.3.0"
---

# Designing Data-Intensive Applications Framework

A principled approach to building reliable, scalable, and maintainable data systems. Apply these principles when choosing databases, designing schemas, architecting distributed systems, or reasoning about consistency and fault tolerance.

## Core Principle

**Data outlives code.** Applications are rewritten and frameworks come and go, but data persists for decades -- prioritize the long-term correctness, durability, and evolvability of the data layer. Most applications are data-intensive, not compute-intensive: the hard problems are data volume, complexity, and rate of change, and explicit consistency/availability/latency trade-offs separate robust systems from fragile ones.

## Scoring

**Goal: 10/10.** Rate any data architecture 0-10 against the principles below: deliberate trade-off choices for data models, storage, replication, partitioning, transactions, and pipelines score high; accidental complexity and ignored failure modes score low. Report the current score and the improvements needed to reach 10/10.

## The DDIA Framework

Seven domains for reasoning about data-intensive systems:

### 1. Data Models and Query Languages

**Core concept:** The data model shapes how you think about the problem. Relational, document, and graph models each impose different constraints and enable different query patterns.

**Why it works:** Choosing the wrong data model forces application code to compensate for representational mismatch, adding accidental complexity that compounds over time.

**Key insights:**
- Relational models excel at many-to-many relationships and ad-hoc queries; document models at one-to-many relationships and locality; graph models at recursive traversals over interconnected data
- Schema-on-write (relational) catches errors early; schema-on-read (document) offers flexibility
- Polyglot persistence -- different stores for different access patterns -- is often the right answer
- Object-relational impedance mismatch is a real cost; document models reduce it for self-contained aggregates

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **User profiles with nested data** | Document model for self-contained aggregates | Profile, addresses, and preferences in one MongoDB document |
| **Social network connections** | Graph model for relationship traversal | Neo4j Cypher: `MATCH (a)-[:FOLLOWS*2]->(b)` for friend-of-friend |
| **Financial ledger with joins** | Relational model for referential integrity | PostgreSQL foreign keys between accounts, transactions, entries |

See: [references/data-models.md](references/data-models.md) for relational/document/graph trade-offs and query language comparisons.

### 2. Storage Engines

**Core concept:** Storage engines trade off read performance against write performance. Log-structured engines (LSM trees) optimize writes; page-oriented engines (B-trees) balance reads and writes.

**Why it works:** Understanding your database's storage engine lets you predict performance characteristics, choose appropriate indexes, and avoid pathological workloads.

**Key insights:**
- LSM trees: append-only writes, periodic compaction, excellent write throughput, higher read amplification
- B-trees: in-place updates, predictable read latency, write amplification from page splits
- Write amplification (one logical write causing multiple physical writes) matters for SSDs with limited write cycles
- Column-oriented storage dramatically improves analytical queries through compression and vectorized processing
- In-memory databases are fast because they avoid encoding overhead, not because they avoid disk

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **High write throughput** | LSM-tree engine | Cassandra or RocksDB for time-series ingestion at 100K+ writes/sec |
| **Mixed read/write OLTP** | B-tree engine | PostgreSQL B-tree indexes for transactional point lookups |
| **Analytical queries** | Column-oriented storage | ClickHouse or Parquet for scanning billions of rows, few columns |

See: [references/storage-engines.md](references/storage-engines.md) for LSM vs B-tree internals, compaction, and column storage.

### 3. Replication

**Core concept:** Replication keeps copies of data on multiple machines for fault tolerance, scalability, and latency reduction. The core challenge is handling changes consistently.

**Why it works:** Every replication strategy trades off consistency, availability, and latency. Making the trade-off explicit prevents subtle anomalies that surface only under load or failure.

**Key insights:**
- Single-leader: simple, strong consistency possible, but the leader is a bottleneck and single point of failure
- Multi-leader: better write availability across data centers, but complex conflict resolution
- Leaderless: highest availability via quorum reads/writes, but needs careful conflict handling
- Replication lag causes read-your-writes, monotonic-read, and causality violations
- Synchronous replication guarantees durability but adds latency; asynchronous risks data loss on failover
- CRDTs and last-writer-wins resolve conflicts with very different correctness guarantees

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Read-heavy web app** | Single-leader with read replicas | PostgreSQL primary + read replicas behind pgBouncer |
| **Multi-region writes** | Multi-leader replication | CockroachDB or Spanner with bounded staleness |
| **Shopping cart availability** | Leaderless with merge | DynamoDB with last-writer-wins or application-level cart merge |

See: [references/replication.md](references/replication.md) for lag anomalies, conflict resolution, and CRDTs.

### 4. Partitioning

**Core concept:** Partitioning (sharding) distributes data across nodes so each handles a subset, enabling horizontal scaling beyond a single machine.

**Why it works:** Without partitioning, one node bottlenecks storage and throughput. Effective partitioning spreads load evenly and avoids hotspots.

**Key insights:**
- Key-range partitioning supports efficient range scans but risks hotspots on sequential keys
- Hash partitioning distributes load evenly but destroys sort order, making range queries expensive
- Local secondary indexes require scatter-gather queries; global secondary indexes require cross-partition updates
- Hotspots occur even with hashing when a single key is extremely popular (celebrity problem)
- Rebalancing strategies: fixed partition count, dynamic splitting, or proportional to nodes

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Time-series data** | Key-range partitioning by time + source | Partition by `(sensor_id, date)` to avoid current-day write hotspot |
| **User data at scale** | Hash partitioning on user ID | Cassandra consistent hashing on `user_id` for even distribution |
| **Celebrity/hot-key problem** | Key splitting with random suffix | Append random digit to hot key, fan out reads across 10 sub-partitions |

See: [references/partitioning.md](references/partitioning.md) for rebalancing, request routing, and secondary index strategies.

### 5. Transactions and Consistency

**Core concept:** Transactions provide safety guarantees (ACID) that simplify application code by letting you pretend failures and concurrency don't exist -- within the transaction's scope.

**Why it works:** Without transactions, every piece of application code must handle partial failures, races, and concurrent modification. Transactions move that complexity into the database, handled correctly once.

**Key insights:**
- Isolation levels are a spectrum: read uncommitted, read committed, snapshot isolation, serializable
- Most databases default to read committed or snapshot isolation -- NOT serializable -- so you must understand the anomalies this permits
- Write skew: two transactions read the same data, decide, and write different records -- no row lock prevents it
- Serializable snapshot isolation (SSI) gives full serializability optimistically: no blocking, but aborts on conflict; two-phase locking blocks and deadlocks under contention
- Distributed transactions (two-phase commit) are expensive and fragile; design around single-partition operations instead

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Account balance transfer** | Serializable transaction | `BEGIN; UPDATE accounts ... -100 WHERE id=1; UPDATE accounts ... +100 WHERE id=2; COMMIT;` |
| **Inventory reservation** | SELECT FOR UPDATE to prevent write skew | `SELECT stock FROM items WHERE id = X FOR UPDATE` before decrementing |
| **Cross-service operations** | Saga instead of distributed transaction | Charge card, reserve inventory; on failure, run compensating refund |

See: [references/transactions.md](references/transactions.md) for isolation-level anomalies and serializability techniques.

### 6. Batch and Stream Processing

**Core concept:** Batch processing transforms bounded datasets in bulk; stream processing transforms unbounded event streams continuously. Both compute derived data.

**Why it works:** Separating the system of record from derived data (caches, indexes, materialized views) lets each be optimized independently and rebuilt from source when requirements change.

**Key insights:**
- MapReduce is conceptually simple but operationally awkward; dataflow engines (Spark, Flink) generalize it with arbitrary DAGs
- Change data capture (CDC) turns database writes into a stream downstream systems can consume
- Stream-table duality: a stream is the changelog of a table; a table is the materialized state of a stream
- Exactly-once semantics require idempotent operations or transactional output
- Time windowing (tumbling, hopping, session) is essential for aggregating unbounded streams

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Daily analytics pipeline** | Batch processing with Spark | Read day's events from S3, aggregate, write to warehouse |
| **Real-time fraud detection** | Stream processing with Flink | Kafka payment events, rules over 5-second tumbling windows |
| **Syncing search index** | Change data capture | Debezium captures PostgreSQL WAL, Kafka feeds Elasticsearch |
| **Audit trail / event replay** | Event sourcing | Store `OrderPlaced`, `OrderShipped` events; rebuild state by replaying |

See: [references/batch-stream.md](references/batch-stream.md) for dataflow engines, CDC, and exactly-once semantics.

### 7. Reliability and Fault Tolerance

**Core concept:** Faults are inevitable; failures are not. A reliable system continues operating correctly even when individual components fail. Design for faults, not against them.

**Why it works:** Hardware fails, software has bugs, humans make mistakes. Systems that assume perfect operation are brittle; systems that expect faults are resilient.

**Key insights:**
- A fault is one component deviating from spec; a failure is the whole system stopping -- fault tolerance prevents the former becoming the latter
- Hardware faults are random and independent; software faults are correlated and systematic (more dangerous)
- Human error is the leading cause of outages -- minimize opportunity for mistakes, maximize ability to recover
- Timeouts are the fundamental fault detector, but tuning is hard: too short causes false positives, too long delays recovery
- Safety properties (nothing bad happens) must always hold; liveness (something good eventually happens) may be temporarily violated
- Byzantine fault tolerance is rarely needed outside blockchain; assume crash-stop or crash-recovery

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Service communication** | Timeouts + retries with backoff | `retry(max=3, backoff=exponential(base=1s, max=30s))` with jitter |
| **Leader election** | Consensus algorithm (Raft/Paxos) | etcd or ZooKeeper for distributed locks and leader election |
| **Graceful degradation** | Circuit breaker | Resilience4j: open circuit after 50% failures in 10-second window |

See: [references/fault-tolerance.md](references/fault-tolerance.md) for consensus, timeout tuning, and safety/liveness guarantees.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **Choosing a database by popularity** | Engines have fundamentally different trade-offs | Match storage engine to actual read/write patterns |
| **Ignoring replication lag** | Stale reads, phantom reads, lost updates | Implement read-your-writes and monotonic-read guarantees |
| **Distributed transactions everywhere** | 2PC is slow, fragile; coordinator is a SPOF | Design single-partition operations; use sagas across services |
| **Hash partitioning everything** | Destroys range query ability | Key-range partitioning for time-series; composite keys for locality |
| **Assuming serializable isolation** | Defaults are weaker; write skew appears in production | Check the actual default; use explicit locking where needed |
| **Conflating batch and stream** | Wrong tool adds latency or wasted complexity | Match processing model to data boundedness and latency needs |
| **Treating all faults as recoverable** | Corruption and Byzantine faults need different handling | Classify faults; design a recovery strategy per class |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you explain why you chose this database over alternatives? | Choice was familiarity, not requirements | Evaluate data model fit, read/write ratio, consistency needs, scaling path |
| Do you know your database's default isolation level? | Latent concurrency bugs | Check docs; test for write skew and phantom reads |
| Is your replication strategy explicitly chosen? | Implicit consistency/durability assumptions | Document sync vs async, failover behavior, lag tolerance |
| Can your system handle a hot partition key? | One popular entity can down the cluster | Add key-splitting or load shedding for hot keys |
| Do you separate system of record from derived data? | Every change requires migrating everything | Introduce CDC or event sourcing to decouple |
| Are timeouts and retries tuned, not defaulted? | Cascading failures or needless delays | Measure p99; set timeouts above p99, below cascade threshold |
| Have you tested failover in production conditions? | Recovery plan is theoretical | Run chaos experiments: kill leaders, partition networks, fill disks |

## Reference Files

- [data-models.md](references/data-models.md): Relational vs document vs graph models, schema-on-read vs schema-on-write, query languages, polyglot persistence
- [storage-engines.md](references/storage-engines.md): LSM trees vs B-trees, write amplification, compaction, column-oriented storage, in-memory databases
- [replication.md](references/replication.md): Single-leader, multi-leader, leaderless replication, replication lag, conflict resolution, CRDTs
- [partitioning.md](references/partitioning.md): Key-range vs hash partitioning, secondary indexes, rebalancing, request routing, hotspots
- [transactions.md](references/transactions.md): ACID, isolation levels, write skew, two-phase locking, SSI, distributed transactions
- [batch-stream.md](references/batch-stream.md): MapReduce, dataflow engines, event sourcing, CDC, stream-table duality, exactly-once semantics
- [fault-tolerance.md](references/fault-tolerance.md): Faults vs failures, reliability metrics, timeouts, consensus, safety and liveness guarantees

## Further Reading

For the complete treatment with detailed diagrams and research references:

- [*"Designing Data-Intensive Applications"*](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321?tag=wondelai00-20) by Martin Kleppmann

## About the Author

**Martin Kleppmann** is a distributed-systems researcher at the University of Cambridge and a former engineer at LinkedIn and Rapportive, known for his work on CRDTs and local-first software. His book *Designing Data-Intensive Applications* (2017) is the definitive reference for engineers building data systems, praised for making distributed-systems concepts accessible and practical.
