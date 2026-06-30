---
name: system-design
description: 'Design scalable distributed systems using structured approaches for load balancing, caching, database scaling, and message queues. Use when the user mentions "system design", "scale this", "high availability", "rate limiter", "design a URL shortener", "design Twitter", "design Uber", "design a news feed", "system design interview", "capacity planning", or "distributed architecture". Also trigger when estimating infrastructure requirements, choosing between microservices and monoliths, or designing for millions of concurrent users. Covers common system designs (TinyURL, feeds, chat) and back-of-the-envelope estimation. For data fundamentals, see ddia-systems. For resilience, see release-it.'
license: MIT
metadata:
  author: wondelai
  version: "1.4.1"
---

# System Design Framework

A structured approach to designing large-scale distributed systems. Apply these principles when architecting new services, reviewing designs, estimating capacity, or preparing for system design discussions.

## Core Principle

**Start with requirements, not solutions.** Jumping to architecture before understanding constraints produces over- or under-engineered systems. Scalable systems are assembled from well-understood building blocks (load balancers, caches, queues, databases, CDNs) — the skill lies in choosing the right blocks, sizing them with estimates, and owning the tradeoffs each choice introduces.

## Scoring

**Goal: 10/10.** Score a design by how many of the eight Quick Diagnostic rows it satisfies — `score = round(passed / 8 × 10)`: 9-10 = all/nearly all rows pass — explicit requirements, real estimates, redundancy, a stated DB-scaling and caching strategy, async via queues, monitoring, and a deployment plan, with tradeoffs named; 5-6 = the design works but skips estimation, redundancy, or operations; <=3 = architecture proposed before requirements or estimates exist. Always state the current score, name the failing diagnostic rows, and give the specific fix for each.

## The System Design Framework

Six areas for building reliable, scalable distributed systems:

### 1. The Four-Step Process

**Core concept:** Every design follows four stages: (1) understand the problem and establish scope, (2) propose a high-level design and get buy-in, (3) dive deep into critical components, (4) wrap up with tradeoffs and future improvements.

**Why it works:** Without structure, designs either stay too abstract or get lost in premature detail. The four steps invest time proportionally — broad strokes first, depth where it matters.

**Key insights:**
- Step 1 (~5-10 min): clarifying questions, functional and non-functional requirements, agreed scale (DAU, QPS, storage)
- Step 2 (~15-20 min): high-level diagram with APIs, services, data stores, data flow arrows
- Step 3 (~15-20 min): design the 2-3 hardest or most critical components in detail
- Step 4 (~5 min): tradeoffs, bottlenecks, future improvements
- Never skip Step 1 — ambiguous scope wastes all downstream effort; get explicit agreement on assumptions

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **New service kickoff** | One-page design doc covering all four steps before coding | Requirements, API contract, data model, capacity estimate, then implementation |
| **Architecture review** | Walk reviewers through the steps sequentially | Scope, diagram, deep-dive on riskiest component, open questions |
| **Incident postmortem** | Trace the failure through the four-step lens | Which requirement was missed? Which block failed? What tradeoff bit us? |

See [references/four-step-process.md](references/four-step-process.md) when running a design end-to-end — per-stage time allocation, example clarifying questions, and tips for each of the four steps.

### 2. Back-of-the-Envelope Estimation

**Core concept:** Use powers of two, latency numbers, and simple arithmetic to estimate QPS, storage, bandwidth, and server count before committing to an architecture.

**Why it works:** Estimation prevents over-provisioning (wasted money) and under-provisioning (outages under load). A 2-minute calculation can save weeks of rework.

**Key insights:**
- Powers of two: 2^10 ≈ 1 thousand, 2^20 ≈ 1 million, 2^30 ≈ 1 billion, 2^40 ≈ 1 trillion
- Latency: memory read ~100 ns, SSD read ~100 us, disk seek ~10 ms, same-datacenter round trip ~0.5 ms, cross-continent ~150 ms
- Availability nines: 99.9% = 8.77 hours downtime/year; 99.99% = 52.6 minutes/year
- QPS: DAU x actions-per-day / 86,400 seconds; peak is typically 2-5x average
- Storage: records-per-day x record-size x retention
- Round aggressively — the goal is order of magnitude, not precision

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Capacity planning** | Estimate QPS, multiply by growth factor | 100M DAU x 5 actions / 86400 = ~5,800 QPS avg, ~30K peak |
| **Storage budgeting** | Per-record size x volume x retention | 500M tweets/day x 300 bytes x 365 days = ~55 TB/year |
| **SLA definition** | Convert nines to allowed downtime | Four nines = ~52 minutes downtime per year |

See [references/estimation-numbers.md](references/estimation-numbers.md) when sizing a system — full latency table, availability-nines table, and worked QPS/storage/bandwidth calculations.

### 3. Building Blocks

**Core concept:** Scalable systems are assembled from a standard toolkit: DNS, CDN, load balancers, reverse proxies, application servers, caches, message queues, and consistent hashing.

**Why it works:** Each block trades one cost for another (a cache trades freshness for read speed; a queue trades latency for decoupling), so introduce a block only once its specific bottleneck appears — adding all of them up front just multiplies failure modes.

**Key insights:**
- Load balancers: L4 (transport layer — fast, simple) vs L7 (application layer — content-aware routing)
- Cache layers: client, CDN, web server, application (Redis/Memcached), database query cache
- Cache strategies: cache-aside (app manages), read-through, write-through (synchronous), write-behind (asynchronous)
- Message queues (Kafka, RabbitMQ, SQS): decouple producers from consumers, absorb spikes, enable async processing
- Consistent hashing: distributes keys across nodes with minimal redistribution when nodes change

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Read-heavy workload** | Cache-aside Redis in front of database | Cache user profiles with TTL; invalidate on write |
| **Traffic spikes** | Message queue between API and workers | Enqueue image-resize jobs; workers pull at their own pace |
| **Global users** | CDN for static assets | Serve JS/CSS/images from edge; origin serves only API |
| **Uneven load** | Consistent hashing for shard assignment | Adding a node moves only ~1/n keys |

See [references/building-blocks.md](references/building-blocks.md) when choosing components — how each of DNS, CDN, load balancers, caching strategies, message queues, and consistent hashing works and when to introduce it.

### 4. Database Design and Scaling

**Core concept:** Choose SQL vs NoSQL based on data shape and access patterns; scale vertically first, then horizontally (replication and sharding) when vertical limits are reached.

**Why it works:** The database is usually the first bottleneck. Understanding replication, sharding, and denormalization tradeoffs delays expensive re-architectures and makes growth deliberate.

**Key insights:**
- Vertical scaling is simpler but has a ceiling; horizontal is harder but nearly unlimited
- Replication: leader-follower (one writer, many readers) for read-heavy; multi-leader for multi-region writes
- Sharding: hash-based (even distribution, hard range queries), range-based (easy ranges, hotspot risk), directory-based (flexible, extra lookup)
- SQL for ACID transactions, joins, defined schema; NoSQL for flexible schema, horizontal scale, very high write throughput
- Denormalization trades storage and write complexity for read speed — use when reads dominate and data changes rarely
- Celebrity/hotspot problem: one hot shard needs secondary partitioning or a cache layer

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Read-heavy API** | Leader-follower with read replicas | Reads to replicas, writes to leader; accept slight lag |
| **User data at scale** | Hash-based sharding on user_id | hash(user_id) % num_shards; even, independent shards |
| **Analytics dashboard** | Denormalized materialized views | Pre-join and aggregate nightly; serve from materialized table |

See [references/database-scaling.md](references/database-scaling.md) when the database is the bottleneck — replication topologies, the three sharding strategies compared, denormalization tradeoffs, and a SQL-vs-NoSQL selection guide.

### 5. Common System Designs

**Core concept:** Most systems are variations of a small set of well-known designs: URL shortener, rate limiter, notification system, news feed, chat, search autocomplete, web crawler, unique ID generator.

**Why it works:** A mental library of known designs lets you recognize which pattern a new problem resembles and adapt it, rather than inventing from scratch.

**Key insights:**
- URL shortener: base62 encoding, key-value store, 301 vs 302 redirect tradeoff (caching vs analytics)
- Rate limiter: token bucket or sliding window at the gateway; return 429 with Retry-After
- News feed: fanout-on-write (push at post time) vs fanout-on-read (pull at read time); hybrid for celebrities
- Chat: WebSocket for real-time bidirectional messages, queue for delivery guarantees, heartbeat presence service
- Autocomplete: trie of top-k frequent queries; precompute and cache popular prefixes
- Web crawler: BFS with URL frontier, politeness (robots.txt, per-domain rate limit), dedup via content hash
- Unique IDs: UUID (simple, no coordination) vs Snowflake (64-bit, time-sortable, datacenter-aware)

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Short link service** | Base62-encode auto-increment ID or hash | `https://short.ly/a1B2c3` maps to a key-value row |
| **API protection** | Token bucket at gateway | 100 tokens/min per key; steady refill; reject with 429 |
| **Social feed** | Hybrid fanout | Precompute feeds for <10K-follower accounts; merge celebrity posts at read time |

See [references/common-designs.md](references/common-designs.md) when a problem resembles a known design — full walkthroughs of URL shortener, rate limiter, news feed, chat, autocomplete, web crawler, and unique ID generator.

### 6. Reliability and Operations

**Core concept:** A system is only as good as its ability to stay up, recover, and be observed. Health checks, monitoring, logging, and deployment strategies are first-class design concerns, not afterthoughts.

**Why it works:** Production systems fail in ways diagrams never predict. Operational readiness — metrics, alerts, rollback plans, redundancy — determines whether a failure is a blip or an outage.

**Key insights:**
- Health checks: liveness (is the process alive?) and readiness (can it serve traffic?) — Kubernetes uses both
- Three pillars of observability: metrics (Prometheus, Datadog), logging (ELK, CloudWatch), tracing (Jaeger, Zipkin)
- Deployments: rolling (gradual), blue-green (instant switch between identical environments), canary (small percentage first)
- Disaster recovery: RPO (acceptable data loss) and RTO (acceptable recovery time) drive backup and failover strategy
- Multi-datacenter: active-passive (failover) or active-active (requires data sync and conflict resolution)
- Autoscaling: scale on CPU, memory, queue depth, or custom metrics; always set min and max counts

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Zero-downtime deploy** | Blue-green with health check gates | Switch to green after checks pass; keep blue as instant rollback |
| **Gradual rollout** | Canary with metric comparison | 5% traffic to new version; compare errors and latency; promote or rollback |
| **Data safety** | Define RPO/RTO, implement accordingly | RPO 1 hour = hourly backups; RTO 5 min = automated failover |

See [references/reliability-operations.md](references/reliability-operations.md) when hardening for production — health-check patterns, the observability pillars, deployment strategies, disaster-recovery (RPO/RTO), and autoscaling.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **Architecture before requirements** | Solves the wrong problem, misses constraints | Spend the first 5-10 minutes on scope: features, scale, SLA |
| **No estimation** | Provisioning off by orders of magnitude | Estimate QPS, storage, bandwidth before choosing components |
| **Single point of failure** | One component takes down the system | Redundancy at every layer: multi-server, multi-AZ, multi-region |
| **Premature sharding** | Huge operational complexity before it's needed | Vertical first, read replicas, cache aggressively, shard last |
| **Caching without invalidation** | Stale data causes bugs and confusion | Define TTL; cache-aside with explicit invalidation on writes |
| **Synchronous calls everywhere** | One slow service cascades latency to all callers | Queues for non-latency-critical paths; timeouts on sync calls |
| **Ignoring hotspots** | One shard or key hammered, others idle | Detect hot keys; add secondary partitioning or local caches |
| **No monitoring or alerting** | Users find failures before you do | Instrument metrics, logs, and traces from day one |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Are functional and non-functional requirements listed? | Design rests on assumptions | Write down features, DAU, QPS, storage, latency and availability SLAs |
| Is there a QPS and storage estimate? | Capacity is a guess | DAU x actions / 86400 for QPS; records x size x retention for storage |
| Is every component redundant? | Single points of failure | Add replicas, failover, or multi-AZ per component |
| Is the database scaling strategy defined? | You hit a wall under growth | Vertical first, then read replicas, then sharding with a clear shard key |
| Is there a cache for read-heavy paths? | Database takes unnecessary load | Redis/Memcached cache-aside with defined TTL |
| Are async paths using queues? | Tight coupling, cascading failures | Decouple with Kafka/SQS for jobs, notifications, analytics |
| Is there a monitoring and alerting plan? | Blind to production failures | Define metrics, log aggregation, tracing, alert thresholds |
| Is the deployment strategy defined? | Risky all-at-once releases | Rolling, blue-green, or canary with automated rollback |

## Further Reading

For the complete guides with detailed diagrams and walkthroughs:

- [*"System Design Interview -- An Insider's Guide"*](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF?tag=wondelai00-20) by Alex Xu (Volume 1)
- [*"System Design Interview -- An Insider's Guide: Volume 2"*](https://www.amazon.com/System-Design-Interview-Insiders-Guide/dp/1736049119?tag=wondelai00-20) by Alex Xu (Volume 2)
- [*"Designing Data-Intensive Applications"*](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321?tag=wondelai00-20) by Martin Kleppmann (data systems fundamentals)
- [ByteByteGo](https://bytebytego.com/) -- Alex Xu's platform with visual system design explanations

## About the Author

**Alex Xu** is a software engineer who previously worked at Twitter, Apple, and Oracle, and the creator of ByteByteGo. His two-volume *System Design Interview* series, with over 500,000 copies sold, turned system design into a learnable, repeatable skill through structured thinking, estimation, and clear communication.
