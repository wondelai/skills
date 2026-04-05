# Stability Patterns

Stability patterns are the countermeasures to the anti-patterns that cause production failures. Each pattern addresses specific failure modes and, when combined, creates a defense-in-depth strategy that allows systems to absorb shocks, degrade gracefully, and recover automatically.

These patterns are not theoretical -- they are battle-tested responses to the recurring failure modes described in the anti-patterns reference.


## Table of Contents
1. [1. Circuit Breaker](#1-circuit-breaker)
2. [2. Bulkheads](#2-bulkheads)
3. [3. Timeouts](#3-timeouts)
4. [4. Retry with Backoff](#4-retry-with-backoff)
5. [5. Steady State](#5-steady-state)
6. [6. Fail Fast](#6-fail-fast)
7. [7. Let It Crash](#7-let-it-crash)
8. [8. Handshaking](#8-handshaking)
9. [Pattern Combinations](#pattern-combinations)

---

## 1. Circuit Breaker

The Circuit Breaker is the single most important stability pattern. It prevents a failing downstream dependency from taking down the calling service by short-circuiting requests when failures exceed a threshold.

### State Machine

```
     success                  failure count
    ┌───────┐              exceeds threshold
    │       │                    │
    ▼       │                    ▼
 ┌────────┐ │              ┌────────┐
 │ CLOSED │─┘              │  OPEN  │
 └────────┘                └────────┘
      ▲                         │
      │    success               │  timeout expires
      │                         ▼
      │                    ┌──────────┐
      └────────────────────│HALF-OPEN │
           (trial request  └──────────┘
            succeeds)           │
                                │  trial request fails
                                └──────────────────┐
                                                   │
                                              ┌────────┐
                                              │  OPEN  │
                                              └────────┘
```

### States Explained

| State | Behavior | Transitions |
|-------|----------|-------------|
| **Closed** | Requests pass through normally; failures are counted | Transitions to Open when failure count exceeds threshold within time window |
| **Open** | All requests fail immediately without calling downstream | Transitions to Half-Open after a recovery timeout expires |
| **Half-Open** | A limited number of trial requests are allowed through | Transitions to Closed if trials succeed; back to Open if trials fail |

### Configuration Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| **Failure threshold** | Number of failures before opening | 5-20 failures |
| **Time window** | Period over which failures are counted | 30-120 seconds |
| **Recovery timeout** | Time to wait in Open state before trying Half-Open | 15-60 seconds |
| **Trial requests** | Number of requests allowed in Half-Open | 1-5 requests |
| **Success threshold** | Consecutive successes needed to close | 3-5 successes |

### What Counts as a Failure

Not every error should trip the circuit breaker. Configure what counts:

| Should Trip | Should Not Trip |
|------------|----------------|
| Connection timeout | 400 Bad Request (client error) |
| Read timeout | 404 Not Found |
| 5xx server error | 429 Too Many Requests (handle with retry/backoff) |
| Connection refused | Business logic validation errors |
| Circuit breaker open on downstream | Request cancellation by client |

### Implementation Considerations

- **Granularity:** One circuit breaker per downstream service, or per endpoint within a service? Per-endpoint gives finer control but more complexity.
- **Fallback behavior:** When the circuit is open, what do you return? Cached data? Default value? Error response? The right answer depends on the use case.
- **Monitoring:** Every circuit breaker state change should emit a metric and a log entry. An open circuit breaker is a critical signal.
- **Coordination:** In a fleet of instances, each has its own circuit breaker state. Consider whether this is acceptable or if you need coordinated state (usually independent is fine).
- **Half-open thundering herd:** When the recovery timeout expires, only let one or two trial requests through -- not the full backlog.

### Code Pattern (Pseudocode)

```
class CircuitBreaker:
    state = CLOSED
    failure_count = 0
    last_failure_time = null

    function call(operation):
        if state == OPEN:
            if now() - last_failure_time > recovery_timeout:
                state = HALF_OPEN
            else:
                raise CircuitOpenException()

        try:
            result = operation()
            on_success()
            return result
        catch Exception:
            on_failure()
            raise

    function on_success():
        if state == HALF_OPEN:
            state = CLOSED
        failure_count = 0

    function on_failure():
        failure_count += 1
        last_failure_time = now()
        if failure_count >= threshold:
            state = OPEN
```

---

## 2. Bulkheads

Named after the watertight compartments in a ship's hull, bulkheads partition system resources so that a failure in one partition does not sink the entire system.

### Types of Bulkheads

| Type | Mechanism | Use Case |
|------|-----------|----------|
| **Thread pool isolation** | Separate thread pools per dependency | Service A gets 20 threads, Service B gets 20 threads; A's failure cannot exhaust B's pool |
| **Connection pool isolation** | Separate connection pools per downstream | Payment DB pool separate from analytics DB pool |
| **Process isolation** | Separate OS processes per workload | Background jobs in separate processes from request handling |
| **Container isolation** | Separate containers per service | Each microservice in its own container with resource limits |
| **Swim lanes** | Complete stack isolation for critical paths | Checkout flow runs on entirely separate infrastructure from browsing |

### Swim Lanes

Swim lanes are the most rigorous form of bulkheading. A swim lane is a complete, isolated stack -- from load balancer to database -- dedicated to a specific function.

**When to use swim lanes:**
- Revenue-critical paths (checkout, payment processing)
- Compliance-critical paths (authentication, audit logging)
- When a non-critical feature has historically caused outages affecting critical features

**Design rules for swim lanes:**
- No synchronous calls across swim lane boundaries
- No shared databases, caches, or message queues
- Asynchronous replication of data between lanes if needed
- Each lane has independent scaling, deployment, and monitoring

### Sizing Bulkheads

The key question: how many resources does each partition get?

- **Too generous:** Wasted resources; the partition rarely uses its full allocation
- **Too tight:** The partition cannot handle legitimate load spikes
- **Right-sized:** Based on measured throughput at p99 load, plus 20-30% headroom

**Approach:** Measure the actual concurrency for each dependency under peak load. Set the bulkhead size to p99 concurrency + 20% headroom. Set a queue/reject policy for requests beyond the limit.

---

## 3. Timeouts

Every outbound call needs a timeout. Every. Single. One. A missing timeout is a thread leak waiting to happen.

### Types of Timeouts

| Type | What It Controls | Typical Range |
|------|-----------------|---------------|
| **Connect timeout** | Time to establish a TCP connection | 500ms - 2s |
| **Read timeout** | Time to receive a response after connecting | 1s - 30s (depends on operation) |
| **Write timeout** | Time to send the request body | 1s - 10s |
| **Idle timeout** | Time a connection can sit unused in the pool | 30s - 5 min |
| **Request timeout** | Overall deadline for the entire operation | Varies by use case |

### Timeout Propagation

When Service A calls Service B, which calls Service C, timeouts must propagate down the chain. If the user's request has a 5-second deadline, Service A should not start a 10-second operation.

```
User request: 10s deadline
  → Service A: 8s deadline (2s for own processing)
    → Service B: 5s deadline (3s for A's processing)
      → Service C: 3s deadline (2s for B's processing)
```

**Implementation:** Pass the remaining deadline in a request header (e.g., `X-Request-Deadline` or gRPC deadline propagation). Each service subtracts its own processing time and passes the remainder downstream.

### Common Timeout Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using default OS timeout (120-300s) | Threads blocked for minutes | Set explicit timeouts on every call |
| Same timeout for all operations | Fast reads wait too long; slow writes fail prematurely | Tune timeouts per operation type |
| No timeout on DNS resolution | DNS failure blocks thread for OS default (30s+) | Use async DNS or set DNS timeout |
| Not timing out connection pool acquisition | Thread waits forever for a connection from the pool | Set pool checkout timeout (500ms-2s) |
| Timeout too aggressive | Legitimate slow responses treated as failures | Set timeout based on p99 latency + margin |

### Setting Timeout Values

1. Measure the p99 latency of the operation under normal load
2. Add a margin (typically 2-3x p99)
3. Consider the user-facing deadline -- if the user will wait only 5 seconds, your timeout must be less than 5 seconds
4. Monitor timeout rates -- if timeouts fire frequently, the downstream is degrading

---

## 4. Retry with Backoff

Retries are necessary because transient failures are real -- network blips, momentary overloads, and garbage collection pauses cause temporary unavailability that resolves on its own. But naive retries (immediate, unlimited) cause more harm than good.

### Retry Strategy Components

| Component | Purpose | Implementation |
|-----------|---------|----------------|
| **Exponential backoff** | Increase delay between retries to give the downstream time to recover | Delay = base * 2^attempt (e.g., 100ms, 200ms, 400ms, 800ms) |
| **Jitter** | Randomize the delay to prevent all clients from retrying at the same instant | Delay = random(0, base * 2^attempt) |
| **Maximum retries** | Limit total attempts to prevent infinite retry loops | Typically 3-5 retries |
| **Retry budget** | Limit the percentage of requests that are retries across the entire fleet | No more than 10-20% of total requests should be retries |
| **Idempotency** | Ensure the operation is safe to retry without side effects | Use idempotency keys for mutations |

### When to Retry

| Retry | Do Not Retry |
|-------|-------------|
| 503 Service Unavailable | 400 Bad Request |
| 429 Too Many Requests (with backoff) | 401/403 Authentication/Authorization |
| Connection timeout | 404 Not Found |
| Connection reset | 422 Validation Error |
| Read timeout (for idempotent operations) | Read timeout (for non-idempotent operations without idempotency key) |

### Retry Budget

A retry budget limits the total percentage of retried requests across your entire fleet. Without a budget, a fleet of 100 instances each retrying 3 times can amplify load on a struggling downstream by 300x.

**Implementation:**
- Track the ratio of retries to original requests over a sliding window (e.g., 1 minute)
- If retry ratio exceeds the budget (e.g., 20%), stop retrying and fail fast
- This provides fleet-level protection that per-instance retry limits cannot

### The Thundering Herd Problem with Retries

When a downstream service recovers, all clients retry simultaneously, overwhelming it again. Jitter solves this:

- **No jitter:** All 1,000 clients retry at exactly t+100ms, t+200ms, t+400ms
- **Full jitter:** Each client retries at random(0, 100ms), random(0, 200ms), random(0, 400ms) -- spreading the load evenly

---

## 5. Steady State

Production systems accumulate cruft over time. Log files grow. Sessions pile up. Temporary files linger. Database tables bloat. Without active management, this accumulation eventually exhausts a resource -- disk space, memory, database capacity -- and the system fails.

### What Accumulates

| Resource | Growth Mechanism | Consequence of Neglect |
|----------|-----------------|----------------------|
| **Log files** | Application logging, access logs | Disk full; application cannot write; crash |
| **Database rows** | Event logs, audit trails, temp records | Slow queries; backup failures; storage costs |
| **Sessions** | User sessions stored server-side | Memory exhaustion; swap thrashing |
| **Temp files** | Upload processing, report generation | Disk full |
| **Cache entries** | Application cache without TTL | Memory exhaustion |
| **Message queues** | Unprocessed or dead-letter messages | Queue backpressure; memory/disk exhaustion |

### Steady State Design

Every resource that grows must have a corresponding mechanism to shrink:

- **Log rotation:** Rotate by size (500MB) and time (daily); retain N files; compress rotated files
- **Data purging:** Delete or archive records older than retention period; run during off-peak hours
- **Session cleanup:** Set maximum session duration and idle timeout; evict expired sessions automatically
- **Cache eviction:** Use TTL-based expiration; implement LRU or LFU eviction when memory limit is reached
- **Queue management:** Set maximum queue depth; dead-letter after N delivery attempts; alert on growing queue size

---

## 6. Fail Fast

If a system knows it cannot process a request successfully, it should reject the request immediately rather than consuming resources in a doomed attempt.

### When to Fail Fast

| Condition | Fail-Fast Response |
|-----------|-------------------|
| Circuit breaker is open | Return 503 immediately |
| Required parameter missing | Return 400 immediately |
| User not authenticated | Return 401 immediately |
| Resource limit exceeded (rate limit) | Return 429 immediately |
| Request deadline already expired | Return 504 immediately |
| Required downstream service unavailable | Return 503 with degraded response |

### Why Fail Fast Is Kind

Failing fast is not hostile -- it is kind. A fast rejection lets the caller know immediately that this request will not work, freeing the caller to retry elsewhere, display an error, or degrade gracefully. A slow failure wastes the caller's time, threads, and hope.

---

## 7. Let It Crash

Borrowed from Erlang's "let it crash" philosophy: when a process enters an unrecoverable or uncertain state, it is safer to terminate and restart from a known-good state than to attempt in-process recovery.

### When to Let It Crash

- Corrupted in-memory state that cannot be validated
- Resource handles (file descriptors, connections) in an unknown state
- Unhandled exception in a critical path where recovery logic is complex and error-prone
- Process consuming excessive memory or CPU with no clear cause

### Prerequisites for Let It Crash

- **Fast restart:** Process must start in seconds, not minutes
- **Supervision:** A supervisor must detect the crash and restart the process
- **State recovery:** Critical state must be externalized (database, distributed cache) -- not lost on crash
- **Health checks:** Load balancer must detect the restart and route traffic away during startup
- **Crash budget:** Monitor crash frequency; excessive crashes indicate a deeper problem, not a healthy recovery mechanism

---

## 8. Handshaking

Handshaking is a protocol-level mechanism where the server tells the client whether it is ready to accept work before the client sends a full request. This prevents the server from being overwhelmed when it is already overloaded.

### Handshaking Mechanisms

| Level | Mechanism | Example |
|-------|-----------|---------|
| **TCP** | SYN/ACK with backlog queue | OS rejects connections when listen queue is full |
| **HTTP** | 100 Continue response | Server tells client to proceed with request body, or rejects early |
| **Application** | Health check + load shedding | Load balancer checks `/ready` endpoint; server returns 503 when overloaded |
| **gRPC** | Flow control with window updates | Server signals how much data it can receive |
| **Custom** | Pre-flight capacity check | Client asks "can you handle this request?" before sending payload |

### Application-Level Handshaking

Implement a readiness check that reflects actual capacity:

```
GET /ready

200 OK          → Server can accept work
503 Unavailable → Server is overloaded; do not send requests

Readiness considers:
- Thread pool utilization < 80%
- Connection pool utilization < 80%
- Response latency < SLO threshold
- No critical dependency failures
```

This allows load balancers and service meshes to route traffic away from overloaded instances before they fail, rather than after.

## Pattern Combinations

These patterns are most effective in combination. Common pairings:

| Combination | Effect |
|-------------|--------|
| **Timeout + Circuit Breaker** | Timeout detects slow failures; circuit breaker prevents repeated attempts |
| **Circuit Breaker + Fallback** | Circuit breaker trips; fallback provides degraded response |
| **Bulkhead + Circuit Breaker** | Bulkhead limits blast radius; circuit breaker stops the bleeding |
| **Retry + Timeout + Circuit Breaker** | Retry handles transient failures; timeout limits wait; circuit breaker stops persistent failures |
| **Fail Fast + Handshaking** | Server signals overload; client fails fast without sending work |
| **Steady State + Let It Crash** | Cleanup prevents resource exhaustion; crash recovers from unknown states |

The key principle: no single pattern is sufficient. Production-ready systems layer multiple patterns to create defense in depth.
