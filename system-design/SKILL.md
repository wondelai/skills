---
name: system-design
description: 'Design scalable distributed systems using structured approaches for load balancing, caching, database scaling, and message queues. Use when the user mentions "system design", "scale this", "high availability", "rate limiter", "design a URL shortener", "system design interview", "capacity planning", or "distributed architecture". Also trigger when estimating infrastructure requirements, choosing between microservices and monoliths, or designing for millions of concurrent users. Covers common system designs and back-of-the-envelope estimation. For data fundamentals, see ddia-systems. For resilience, see release-it.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# System Design Framework

A structured approach to designing large-scale distributed systems. Apply these principles when architecting new services, reviewing system designs, estimating capacity, or preparing for system design discussions.

## Core Principle

**Start with requirements, not solutions.** Every system design begins by clarifying what you are building, for whom, and at what scale. Jumping to architecture before understanding constraints produces over-engineered or under-engineered systems.

**The foundation:** Scalable systems are not invented from scratch -- they are assembled from well-understood building blocks (load balancers, caches, queues, databases, CDNs) connected by clear data flows. The skill lies in choosing the right blocks, sizing them correctly, and understanding the tradeoffs each choice introduces. A four-step process -- scope, high-level design, deep dive, wrap-up -- keeps the design focused and communicable.

## Scoring

**Goal: 10/10.** When reviewing or creating system designs, rate them 0-10 based on adherence to the principles below. A 10/10 means the design clearly states requirements, includes back-of-the-envelope estimates, uses appropriate building blocks, addresses scaling and reliability, and acknowledges tradeoffs. Lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## The System Design Framework

Six areas for building reliable, scalable distributed systems:

### 1. The Four-Step Process

**Core concept:** Every system design follows four stages: (1) understand the problem and establish design scope, (2) propose a high-level design and get buy-in, (3) dive deep into critical components, (4) wrap up with tradeoffs and future improvements.

**Why it works:** Without a structured process, designs either stay too abstract or get lost in premature detail. The four-step approach ensures you invest time proportionally -- broad strokes first, depth where it matters.

**Key insights:**
- Step 1 consumes ~5-10 minutes: ask clarifying questions, list functional and non-functional requirements, agree on scale (DAU, QPS, storage)
- Step 2 consumes ~15-20 minutes: draw a high-level diagram with APIs, services, data stores, and data flow arrows
- Step 3 consumes ~15-20 minutes: pick 2-3 components that are hardest or most critical and design them in detail
- Step 4 consumes ~5 minutes: summarize tradeoffs, identify bottlenecks, suggest future improvements
- Never skip Step 1 -- ambiguity in scope leads to wasted design effort
- Get explicit agreement on assumptions before proceeding

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **New service kickoff** | Write a one-page design doc with all four steps before coding | Requirements, API contract, data model, capacity estimate, then implementation |
| **Architecture review** | Walk reviewers through the four steps sequentially | Present scope, high-level diagram, deep-dive on the riskiest component, open questions |
| **Incident postmortem** | Trace the failure back through the four-step lens | Which requirement was missed? Which building block failed? What tradeoff bit us? |

See: [references/four-step-process.md](references/four-step-process.md)

### 2. Back-of-the-Envelope Estimation

**Core concept:** Use powers of two, latency numbers, and simple arithmetic to estimate QPS, storage, bandwidth, and server count before committing to an architecture.

**Why it works:** Estimation prevents two failure modes: over-provisioning (wasting money) and under-provisioning (outages under load). A 2-minute calculation can save weeks of rework.

**Key insights:**
- Know the powers of two: 2^10 = 1 thousand, 2^20 = 1 million, 2^30 = 1 billion, 2^40 = 1 trillion
- Memory read ~100 ns, SSD read ~100 us, disk seek ~10 ms, round-trip same datacenter ~0.5 ms, cross-continent ~150 ms
- Availability nines: 99.9% = 8.77 hours downtime/year, 99.99% = 52.6 minutes/year
- QPS estimation: DAU x average-actions-per-day / 86,400 seconds; peak QPS is typically 2-5x average
- Storage estimation: records-per-day x record-size x retention-period
- Always round aggressively -- the goal is order of magnitude, not precision

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Capacity planning** | Estimate QPS then multiply by growth factor | 100M DAU x 5 actions / 86400 = ~5,800 QPS avg, ~30K QPS peak |
| **Storage budgeting** | Estimate per-record size and multiply by volume and retention | 500M tweets/day x 300 bytes x 365 days = ~55 TB/year |
| **SLA definition** | Convert availability nines to allowed downtime | Four nines (99.99%) = ~52 minutes downtime per year |

See: [references/estimation-numbers.md](references/estimation-numbers.md)

### 3. Building Blocks

**Core concept:** Scalable systems are assembled from a standard toolkit: DNS, CDN, load balancers, reverse proxies, application servers, caches, message queues, and consistent hashing.

**Why it works:** Each block solves a specific scaling or reliability problem. Knowing when and why to introduce each block prevents both premature complexity and avoidable bottlenecks.

**Key insights:**
- DNS resolves domain names; CDN caches static assets at edge locations close to users
- Load balancers distribute traffic -- L4 (transport layer, fast, simple) vs L7 (application layer, content-aware routing)
- Caching layers: client-side, CDN, web server, application (e.g., Redis/Memcached), database query cache
- Cache strategies: cache-aside (app manages), read-through (cache manages reads), write-through (cache manages writes synchronously), write-behind (cache writes asynchronously)
- Message queues (Kafka, RabbitMQ, SQS) decouple producers from consumers, absorb traffic spikes, and enable async processing
- Consistent hashing distributes keys across nodes with minimal redistribution when nodes are added or removed

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Read-heavy workload** | Add cache-aside with Redis in front of the database | Cache user profiles with TTL; invalidate on write |
| **Traffic spikes** | Insert a message queue between API and workers | Enqueue image-resize jobs; workers pull at their own pace |
| **Global users** | Place a CDN in front of static assets | Serve JS/CSS/images from edge; origin only serves API |
| **Uneven load** | Use consistent hashing for shard assignment | Add a node and only ~1/n keys need to move |

See: [references/building-blocks.md](references/building-blocks.md)

### 4. Database Design and Scaling

**Core concept:** Choose SQL vs NoSQL based on data shape and access patterns, then scale vertically first, horizontally (replication and sharding) when vertical limits are reached.

**Why it works:** The database is usually the first bottleneck. Understanding replication, sharding strategies, and denormalization tradeoffs lets you delay expensive re-architectures and plan growth deliberately.

**Key insights:**
- Vertical scaling (bigger machine) is simpler but has a ceiling; horizontal scaling (more machines) is harder but nearly unlimited
- Replication: leader-follower (one writer, many readers) for read-heavy; multi-leader for multi-region writes
- Sharding strategies: hash-based (even distribution, hard range queries), range-based (efficient range queries, risk of hotspots), directory-based (flexible, extra lookup)
- SQL when you need ACID transactions, complex joins, and a well-defined schema; NoSQL when you need flexible schema, horizontal scale, or very high write throughput
- Denormalization trades storage and write complexity for faster reads -- use it when read performance is critical and data doesn't change frequently
- Celebrity/hotspot problem: if one shard gets disproportionate traffic, add a secondary partition or cache layer

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Read-heavy API** | Leader-follower replication with read replicas | Route reads to replicas, writes to leader; accept slight replication lag |
| **User data at scale** | Hash-based sharding on user_id | Shard key = hash(user_id) % num_shards; even distribution, each shard independent |
| **Analytics dashboard** | Denormalize into read-optimized materialized views | Pre-join and aggregate nightly; serve dashboards from the materialized table |
| **Multi-region app** | Multi-leader replication with conflict resolution | Each region has a leader; last-write-wins or application-level merge |

See: [references/database-scaling.md](references/database-scaling.md)

### 5. Common System Designs

**Core concept:** Most systems are variations of a small set of well-known designs: URL shortener, rate limiter, notification system, news feed, chat system, search autocomplete, web crawler, and unique ID generator.

**Why it works:** Studying common designs builds a mental library of patterns and tradeoffs. When a new problem arrives, you recognize which known design it most resembles and adapt rather than invent from scratch.

**Key insights:**
- URL shortener: base62 encoding, key-value store, 301 vs 302 redirect tradeoff, analytics via redirect logging
- Rate limiter: token bucket or sliding window algorithm, placed at API gateway or middleware, return 429 with Retry-After header
- News feed: fanout-on-write (push to followers' caches at post time) vs fanout-on-read (pull and merge at read time); hybrid for celebrity accounts
- Chat system: WebSocket for real-time bidirectional communication, message queue for delivery guarantees, presence service via heartbeat
- Search autocomplete: trie data structure, top-k frequent queries, precompute and cache results for popular prefixes
- Web crawler: BFS with URL frontier, politeness (robots.txt, rate limiting per domain), deduplication via content hash
- Unique ID generator: UUID (simple, no coordination) vs Snowflake (time-sortable, 64-bit, datacenter-aware)

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Short link service** | Base62 encode an auto-increment ID or hash | `https://short.ly/a1B2c3` maps to row in key-value store |
| **API protection** | Token bucket rate limiter at gateway | 100 tokens/min per API key; refill at steady rate; reject with 429 |
| **Social feed** | Hybrid fanout: push for normal users, pull for celebrities | Pre-compute feeds for accounts with < 10K followers; merge at read time for celebrity posts |
| **Distributed IDs** | Snowflake: timestamp + datacenter + machine + sequence | 64-bit, time-sortable, no coordination required between generators |

See: [references/common-designs.md](references/common-designs.md)

### 6. Reliability and Operations

**Core concept:** A system is only as good as its ability to stay up, recover from failures, and be observed. Health checks, monitoring, logging, and deployment strategies are not afterthoughts -- they are first-class design concerns.

**Why it works:** Production systems fail in ways that design diagrams never predict. Operational readiness -- metrics, alerts, rollback plans, and redundancy -- determines whether a failure becomes a minor blip or a major outage.

**Key insights:**
- Health checks: liveness (is the process alive?) and readiness (can it serve traffic?) -- Kubernetes uses both
- Monitoring stack: metrics (Prometheus, Datadog), logging (ELK, CloudWatch), tracing (Jaeger, Zipkin) -- the three pillars of observability
- Deployment strategies: rolling (gradual replacement), blue-green (two identical environments, instant switch), canary (small percentage first, then expand)
- Disaster recovery: RPO (how much data can you lose) and RTO (how long until recovery) define your backup and failover strategy
- Multi-datacenter: active-passive (failover) or active-active (both serving); active-active requires data synchronization and conflict resolution
- Autoscaling: scale on CPU, memory, queue depth, or custom metrics; always set both min and max instance counts

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Zero-downtime deploy** | Blue-green with health check gates | Route traffic to green after health checks pass; keep blue as instant rollback |
| **Gradual rollout** | Canary deploy with metric comparison | Send 5% of traffic to new version; compare error rate and latency; promote or rollback |
| **Failure detection** | Liveness and readiness probes | `/healthz` returns 200 if alive; `/ready` returns 200 if database connected and cache warm |
| **Data safety** | Define RPO/RTO and implement accordingly | RPO = 1 hour means hourly backups; RTO = 5 min means automated failover |

See: [references/reliability-operations.md](references/reliability-operations.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **Jumping to architecture without clarifying requirements** | You solve the wrong problem or miss critical constraints | Spend the first 5-10 minutes on scope: features, scale, SLA |
| **No back-of-the-envelope estimation** | Over-provision or under-provision by orders of magnitude | Estimate QPS, storage, and bandwidth before choosing components |
| **Single point of failure** | One component failure takes down the entire system | Add redundancy at every layer: multi-server, multi-AZ, multi-region |
| **Premature sharding** | Adds enormous operational complexity before it is needed | Scale vertically first, add read replicas, cache aggressively, shard last |
| **Caching without invalidation strategy** | Stale data causes bugs and user confusion | Define TTL, cache-aside with explicit invalidation on writes |
| **Synchronous calls everywhere** | One slow downstream service cascades latency to all callers | Use message queues for non-latency-critical paths; set timeouts on sync calls |
| **Ignoring the celebrity/hotspot problem** | One shard or cache key gets hammered, others idle | Detect hot keys, add secondary partitioning, or use local caches |
| **No monitoring or alerting** | You find out about failures from users, not dashboards | Instrument metrics, logs, and traces from day one |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Are functional and non-functional requirements explicitly listed? | Design is based on assumptions | Write down features, DAU, QPS, storage, latency SLA, availability SLA |
| Do you have a back-of-the-envelope estimate for QPS and storage? | Capacity is a guess | Calculate: DAU x actions / 86400 for QPS; records x size x retention for storage |
| Is every component in the diagram redundant? | Single points of failure exist | Add replicas, failover, or multi-AZ for each component |
| Is the database scaling strategy defined? | You will hit a wall under growth | Plan: vertical first, then read replicas, then sharding with a clear shard key |
| Is there a caching layer for read-heavy paths? | Database takes unnecessary load | Add Redis/Memcached with cache-aside and a defined TTL |
| Are async paths using message queues? | Tight coupling, cascading failures | Decouple with Kafka/SQS for background jobs, notifications, analytics |
| Is there a monitoring and alerting plan? | Blind to failures in production | Define metrics, log aggregation, tracing, and alert thresholds |
| Is the deployment strategy defined? | Risky all-at-once releases | Choose rolling, blue-green, or canary with automated rollback |

## Reference Files

- [four-step-process.md](references/four-step-process.md): The complete four-step process with time allocation, example questions, and tips for each stage
- [estimation-numbers.md](references/estimation-numbers.md): Powers of two, latency numbers, availability nines, QPS/storage/bandwidth estimation with worked examples
- [building-blocks.md](references/building-blocks.md): DNS, CDN, load balancers, caching strategies, message queues, consistent hashing
- [database-scaling.md](references/database-scaling.md): SQL vs NoSQL, replication, sharding strategies, denormalization, database selection guide
- [common-designs.md](references/common-designs.md): URL shortener, rate limiter, news feed, chat system, search autocomplete, web crawler, unique ID generator
- [reliability-operations.md](references/reliability-operations.md): Health checks, monitoring, logging, deployment strategies, disaster recovery, autoscaling

## Further Reading

This skill is based on Alex Xu's practical system design methodology. For the complete guides with detailed diagrams and walkthroughs:

- [*"System Design Interview -- An Insider's Guide"*](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF?tag=wondelai00-20) by Alex Xu (Volume 1)
- [*"System Design Interview -- An Insider's Guide: Volume 2"*](https://www.amazon.com/System-Design-Interview-Insiders-Guide/dp/1736049119?tag=wondelai00-20) by Alex Xu (Volume 2)
- [*"Designing Data-Intensive Applications"*](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321?tag=wondelai00-20) by Martin Kleppmann (deep dive into data systems fundamentals)
- [ByteByteGo](https://bytebytego.com/) -- Alex Xu's platform with visual system design explanations

## About the Author

**Alex Xu** is a software engineer and the creator of ByteByteGo, one of the most popular platforms for learning system design. His two-volume *System Design Interview* series has become the de facto preparation resource for engineers at all levels, with over 500,000 copies sold. Xu's approach emphasizes structured thinking, back-of-the-envelope estimation, and clear communication of design decisions. Before ByteByteGo, he worked at Twitter, Apple, and Oracle. His visual explanations and step-by-step frameworks have made system design accessible to a broad engineering audience, transforming what was traditionally an opaque topic into a learnable, repeatable skill.
