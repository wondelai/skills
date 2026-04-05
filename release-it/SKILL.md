---
name: release-it
description: 'Build production-ready systems with stability patterns: circuit breakers, bulkheads, timeouts, and retry logic. Use when the user mentions "production outage", "circuit breaker", "timeout strategy", "deployment pipeline", "chaos engineering", "bulkhead pattern", "retry with backoff", or "health checks". Also trigger when designing resilient microservices, planning zero-downtime deployments, or investigating cascading failure scenarios. Covers capacity planning, health checks, and anti-fragility patterns. For data systems, see ddia-systems. For system architecture, see system-design.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Release It! Framework

Framework for designing, deploying, and operating production-ready software systems. Based on a fundamental truth: the software that passes QA is not the software that survives production. Production is a hostile environment -- and your system must be built to expect and handle failure at every level.

## Core Principle

**Every system will eventually be pushed beyond its design limits.** The question is not whether failures will happen, but whether your system degrades gracefully or collapses catastrophically. Production-ready software is not just correct -- it is resilient, observable, and designed to operate through partial failures without human intervention.

## Scoring

**Goal: 10/10.** When reviewing or creating production systems, rate them 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## The Release It! Framework

Six areas that determine whether software survives contact with production:

### 1. Stability Anti-Patterns

**Core concept:** Failures propagate through integration points, cascading across system boundaries. The most dangerous patterns are not bugs in your code -- they are emergent behaviors that arise when systems interact under stress.

**Why it works:** Recognizing anti-patterns lets you identify and eliminate the cracks before production traffic finds them. Every production outage traces back to one or more of these patterns. They are predictable, recurring, and preventable.

**Key insights:**
- Integration points are the number-one killer of production systems -- every socket, HTTP call, or queue is a risk
- Cascading failures spread when one system's failure causes its callers to fail, which causes their callers to fail
- Slow responses are worse than no response -- they tie up threads, exhaust pools, and propagate delays across the entire call chain
- Unbounded result sets turn a harmless query into an out-of-memory crash when data grows beyond test assumptions
- Users generate load patterns that no test suite can predict -- bots, retry storms, and flash crowds
- Self-denial attacks occur when your own marketing, coupons, or viral features overwhelm your infrastructure
- Blocked threads are the silent killer -- deadlocks and resource contention show no errors until everything stops

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **HTTP calls** | Assume every remote call can fail, hang, or return garbage | Wrap all external calls with timeout + circuit breaker |
| **Database queries** | Enforce result set limits on every query | Add `LIMIT` clause; paginate all list endpoints |
| **Thread pools** | Isolate pools per dependency to prevent cross-contamination | Separate thread pool for payment gateway vs. search |
| **Load testing** | Simulate realistic traffic including spikes and abuse patterns | Use production traffic replays, not synthetic happy-path scripts |
| **Marketing events** | Coordinate launches with capacity planning | Pre-scale before Black Friday; add queue for coupon redemption |

See: [references/anti-patterns.md](references/anti-patterns.md) for detailed analysis of each anti-pattern with failure scenarios and detection strategies.

### 2. Stability Patterns

**Core concept:** Counter each anti-pattern with a stability pattern. Circuit breakers stop cascading failures. Bulkheads isolate blast radius. Timeouts reclaim stuck resources. Together they create a system that bends under load but does not break.

**Why it works:** These patterns work because they accept failure as inevitable and design the system's response to failure, rather than trying to prevent all failures. A circuit breaker that trips is the system working correctly -- it is protecting itself from a downstream failure.

**Key insights:**
- Circuit Breaker: three states (closed, open, half-open) -- trips after threshold failures, periodically tests recovery
- Bulkheads: partition resources so one failing component cannot drain the entire system
- Timeouts: every outbound call needs both a connect timeout and a read timeout -- and timeouts must propagate up the call chain
- Retry with backoff: exponential backoff + jitter prevents thundering herd on recovery
- Fail Fast: if you know a request will fail, reject it immediately -- do not waste resources attempting it
- Steady State: systems accumulate cruft (logs, sessions, temp files) -- design for automatic cleanup
- Let It Crash: sometimes the safest recovery is to restart the process cleanly rather than limping along in an unknown state
- Handshaking: let the server tell the client whether it can accept work before the client sends it

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Service calls** | Circuit Breaker with threshold and recovery timeout | Open after 5 failures in 60s; half-open after 30s |
| **Resource isolation** | Bulkhead with dedicated pools per dependency | Separate connection pools for critical vs. non-critical services |
| **Network calls** | Timeout with propagation | Connect: 1s, read: 5s; propagate deadline to downstream calls |
| **Retries** | Exponential backoff + jitter + retry budget | Base 100ms, max 3 retries, 20% retry budget across fleet |
| **Data cleanup** | Steady State with automated purging | Delete sessions older than 24h; rotate logs at 500MB |

See: [references/stability-patterns.md](references/stability-patterns.md) for implementation details, state machines, threshold tuning, and pattern combinations.

### 3. Capacity and Availability

**Core concept:** Capacity is not a single number -- it is a multi-dimensional function of CPU, memory, network, disk I/O, connection pools, and thread counts. Capacity planning means understanding which resource becomes the bottleneck first and at what load level.

**Why it works:** Systems that are not capacity-tested fail in production at the worst possible moment -- during peak load. Understanding your system's actual limits (not theoretical limits) lets you set realistic SLAs and plan scaling before users hit the wall.

**Key insights:**
- Performance testing taxonomy: load test (expected traffic), stress test (beyond limits), soak test (sustained load over time), spike test (sudden bursts)
- The Universal Scalability Law: throughput does not scale linearly -- contention and coherence costs cause diminishing returns
- Connection pools are finite and precious -- a pool exhaustion looks identical to a database outage from the application's perspective
- Thread pools must be sized based on measured throughput, not guesses -- too few starve the system, too many cause context-switching overhead
- Myths: "The cloud is infinitely scalable" -- auto-scaling has lag time, cold-start costs, and hard limits
- Resource pools need health checks, eviction policies, and maximum lifetime limits

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Load testing** | Ramp to expected peak, then 2x, observe degradation curve | Gradually increase RPS until latency exceeds SLO |
| **Connection pools** | Size based on measured concurrency, not defaults | Measure active connections under load; set pool to P99 + 20% headroom |
| **Auto-scaling** | Define scaling triggers with appropriate cooldown | Scale on CPU > 70% sustained 3 min; cooldown 5 min |
| **Soak testing** | Run at 80% capacity for 24-72 hours | Catch memory leaks, connection leaks, file handle exhaustion |
| **Capacity model** | Document resource bottleneck per service | "Service X is memory-bound at 2000 RPS; needs 4GB per instance" |

See: [references/capacity-planning.md](references/capacity-planning.md) for testing methodologies, resource pool management, and scalability modeling.

### 4. Deployment and Release

**Core concept:** Deployment (putting code on servers) and release (exposing code to users) are separate operations that should be decoupled. Separating them gives you the ability to deploy without risk and release with confidence.

**Why it works:** Most outages are caused by changes -- deployments, configuration updates, database migrations. Decoupling deployment from release means you can deploy code to production, verify it works, and only then route traffic to it. If something goes wrong, you roll back the release, not the deployment.

**Key insights:**
- Zero-downtime deployment is non-negotiable for any system with users -- rolling deploys, blue-green, or canary
- Feature flags decouple deployment from release -- dark-launch code and enable it independently
- Database migrations must be backward-compatible -- the old code and new code will run simultaneously during deployment
- Immutable infrastructure: never patch a running server -- build a new image, deploy it, destroy the old one
- Canary releases limit blast radius by routing a small percentage of traffic to the new version first
- Rollback must be faster than roll-forward -- if rollback takes 30 minutes, you will avoid deploying

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Deploys** | Blue-green with health check gate | Deploy to green; run smoke tests; swap router |
| **Progressive rollout** | Canary with automated rollback | Route 5% traffic to canary; auto-rollback if error rate > 1% |
| **Feature launch** | Feature flags with emergency off switch | Ship code behind flag; enable for 10% of users; monitor; ramp |
| **Schema changes** | Expand-contract migration pattern | Add new column; deploy code that writes both; backfill; drop old column |
| **Rollback** | Instant rollback via traffic routing | Keep previous version running; rollback = switch load balancer target |

See: [references/deployment-strategies.md](references/deployment-strategies.md) for deployment patterns, migration strategies, and infrastructure-as-code practices.

### 5. Health Checks and Observability

**Core concept:** You cannot operate what you cannot observe. Observability is not an afterthought -- it is a first-class design concern. Health checks, metrics, logs, and traces are the sensory organs of your system in production.

**Why it works:** Production systems fail in ways that are invisible without proper instrumentation. A health check that only returns "OK" tells you nothing. Metrics without context are noise. Observability done right gives you the ability to answer questions about your system that you did not anticipate at design time.

**Key insights:**
- Health checks come in two flavors: shallow (process alive) and deep (dependencies reachable, resources available)
- The three pillars of observability: structured logs (what happened), metrics (how much), distributed traces (where and how long)
- RED method for services: Rate (requests/sec), Errors (error rate), Duration (latency distribution)
- USE method for resources: Utilization (%), Saturation (queue depth), Errors (error count)
- SLIs measure user experience; SLOs set targets; SLAs create contractual obligations -- define them in that order
- Alerting on symptoms (user-facing errors) beats alerting on causes (CPU usage) -- alert on what users feel
- Dashboards should answer "Is the system healthy right now?" within 5 seconds of looking

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Health endpoints** | Deep health check with dependency status | `/health` returns status of DB, cache, queue, and disk space |
| **Service metrics** | RED method instrumentation | Track request rate, error rate, and p50/p95/p99 latency per endpoint |
| **Resource metrics** | USE method for infrastructure | Track CPU utilization, request queue depth, and error counts per host |
| **Distributed tracing** | Propagate trace context across service boundaries | Inject trace ID in headers; correlate logs across services |
| **Alerting** | Alert on SLO burn rate, not raw thresholds | "Error budget burning 10x normal rate" vs. "CPU > 80%" |

See: [references/observability.md](references/observability.md) for health check design, metrics instrumentation, SLO frameworks, and alerting strategies.

### 6. Adaptation and Chaos Engineering

> **Safety note:** Chaos engineering experiments are design-time planning activities. The patterns below describe *what to test* and *what to verify*, not actions for an AI agent to execute autonomously. All failure injection must be performed by authorized engineers using dedicated tooling (e.g., Gremlin, Litmus, AWS FIS) with proper approvals, rollback plans, and blast radius controls in place.

**Core concept:** Confidence in your system's resilience comes from testing it under realistic failure conditions. Chaos engineering is the discipline of experimenting on a system in a controlled environment to build confidence in its ability to withstand turbulent conditions.

**Why it works:** You cannot know how your system handles failure until it actually fails. Waiting for production incidents to discover weaknesses is reactive and expensive. Chaos engineering proactively injects failures in a controlled way, turning unknown-unknowns into known-knowns before they cause real outages.

**Key insights:**
- Define steady state first -- you need a measurable baseline to detect when behavior deviates
- Start small in non-production environments: terminate a single process, add latency to one call -- then escalate gradually with approvals
- Minimize blast radius: use canary populations, feature flags, and emergency stop mechanisms for experiments
- Production experiments require explicit authorization, monitoring, and immediate rollback capability
- Automate recurring experiments so resilience is continuously verified, not a one-time event
- GameDay exercises combine chaos engineering with incident response practice -- test both the system and the team
- Every experiment should have a hypothesis: "We believe that when X fails, the system will Y"
- Build a culture where finding weaknesses is celebrated, not punished

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Process failure** | Controlled instance termination (via chaos tooling) | Terminate one pod using Gremlin/Litmus; verify service recovers within SLO |
| **Network failure** | Inject latency or partition between services (via chaos tooling) | Add 500ms latency to DB calls; verify circuit breaker trips |
| **Dependency failure** | Simulate downstream service outage (via chaos tooling) | Return 503 from payment API; verify graceful degradation |
| **Resource exhaustion** | Simulate resource pressure (via chaos tooling) | Stress-test memory limits; verify process restarts cleanly |
| **GameDay** | Scheduled team exercise with realistic failure scenario | "Primary database goes read-only at 2pm" -- practice response |

See: [references/chaos-engineering.md](references/chaos-engineering.md) for experiment design, blast radius management, and building a chaos engineering practice.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **No timeouts on outbound calls** | One slow dependency freezes the entire system | Set connect and read timeouts on every external call |
| **Unbounded retries** | Retry storms amplify failures instead of recovering from them | Use exponential backoff, jitter, and fleet-wide retry budgets |
| **Shared thread/connection pools** | One failing dependency drains resources from all features | Bulkhead: isolate pools per dependency or feature |
| **Shallow health checks only** | Load balancer routes traffic to instances with broken dependencies | Implement deep health checks that verify downstream connectivity |
| **Testing only the happy path** | System works perfectly until the first real failure | Load test, soak test, and chaos test before every major release |
| **Coupling deploy and release** | Every deployment is a high-risk event with all-or-nothing rollout | Use feature flags, canary releases, and blue-green deployments |
| **Alerting on causes, not symptoms** | High CPU alerts fire but users are fine; errors spike but no alert fires | Alert on user-facing SLIs: error rate, latency, availability |
| **No capacity model** | System falls over at 2x load during an event nobody planned for | Model bottleneck resources; load test to 3x expected peak |

## Quick Diagnostic

Audit any production system:

| Question | If No | Action |
|----------|-------|--------|
| Does every outbound call have a timeout? | Calls can hang indefinitely, blocking threads | Add connect and read timeouts to all external calls |
| Are circuit breakers in place for critical dependencies? | One dependency failure takes down the whole system | Add circuit breakers with appropriate thresholds |
| Are thread/connection pools isolated per dependency? | Shared pools allow cross-contamination of failures | Implement bulkhead pattern with dedicated pools |
| Can you deploy without downtime? | Deployments cause user-visible outages | Implement rolling, blue-green, or canary deployment |
| Do health checks verify dependency connectivity? | Dead instances receive traffic; partial failures go undetected | Add deep health checks that test DB, cache, queue |
| Are logs, metrics, and traces correlated? | Debugging requires manual log searching across services | Implement distributed tracing with correlated IDs |
| Have you load-tested beyond expected peak? | Unknown failure mode under real load | Load test to 2-3x expected peak; document breaking point |
| Do you practice failure injection? | Resilience is theoretical, not verified | Start chaos engineering with low-risk experiments |

## Reference Files

- [anti-patterns.md](references/anti-patterns.md): Integration point failures, cascading failures, blocked threads, unbounded result sets, self-denial attacks, slow responses
- [stability-patterns.md](references/stability-patterns.md): Circuit Breaker, Bulkhead, Timeout, Retry, Fail Fast, Steady State, Let It Crash, Handshaking
- [capacity-planning.md](references/capacity-planning.md): Load/stress/soak testing, connection pool sizing, thread pool tuning, Universal Scalability Law
- [deployment-strategies.md](references/deployment-strategies.md): Blue-green, canary, rolling deploys, feature flags, database migrations, immutable infrastructure
- [observability.md](references/observability.md): Health checks, RED/USE methods, SLIs/SLOs/SLAs, distributed tracing, alerting strategy
- [chaos-engineering.md](references/chaos-engineering.md): Steady state hypothesis, failure injection, GameDay exercises, blast radius management

## Further Reading

This skill is based on Michael Nygard's essential guide to building production-ready software. For the complete methodology, war stories, and implementation details:

- [*"Release It! Design and Deploy Production-Ready Software"* (2nd Edition)](https://www.amazon.com/Release-Design-Deploy-Production-Ready-Software/dp/1680502395?tag=wondelai00-20) by Michael T. Nygard

## About the Author

**Michael T. Nygard** is a software architect and author with over 30 years of experience building and operating large-scale production systems. He has worked across industries including finance, retail, and government, and has been responsible for systems handling millions of transactions per day. Nygard is known for bridging the gap between development and operations, advocating that architects must be responsible for the systems they design long after the code is written. The first edition of *Release It!* (2007) became a foundational text in the DevOps and site reliability engineering movements. The second edition (2018) expands coverage to cloud-native architectures, containerization, and modern deployment practices. Nygard is a frequent conference speaker and has contributed to the broader conversation about resilience engineering, sociotechnical systems, and the human factors that influence production stability.
