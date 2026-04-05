# Reliability and Fault Tolerance

Reliability means the system continues to work correctly even when things go wrong. Things going wrong are called faults, and a system that can cope with faults is called fault-tolerant. The distinction between a fault and a failure is critical: a fault is when one component of the system deviates from its specification, while a failure is when the system as a whole stops providing the required service.


## Table of Contents
1. [Faults vs. Failures](#faults-vs-failures)
2. [Types of Faults](#types-of-faults)
3. [Reliability Metrics](#reliability-metrics)
4. [Detecting Faults in Distributed Systems](#detecting-faults-in-distributed-systems)
5. [Byzantine Faults](#byzantine-faults)
6. [Safety and Liveness](#safety-and-liveness)
7. [Designing for Reliability](#designing-for-reliability)
8. [Practical Reliability Patterns](#practical-reliability-patterns)

---

## Faults vs. Failures

| Term | Definition | Example |
|------|-----------|---------|
| **Fault** | One component deviating from its specification | A disk sector becomes unreadable |
| **Failure** | The system as a whole stops providing the required service | The entire website goes down |
| **Fault tolerance** | Designing the system so that faults don't become failures | RAID mirrors data across disks so one disk fault doesn't cause data loss |

The goal is not to prevent all faults (that is impossible) but to design systems that prevent faults from causing failures.

---

## Types of Faults

### Hardware Faults

Hardware faults are random and largely independent. The probability that two unrelated hardware components fail at the same time is very low.

| Component | Typical Failure Rate | Mitigation |
|-----------|---------------------|------------|
| **Hard disk** | MTTF ~10-50 years per drive | RAID, replicated storage |
| **RAM** | ~0.2% of DIMMs per year | ECC memory, replication |
| **Power supply** | Varies by quality | Dual power supplies, UPS, generators |
| **Network** | Partial failures common | Redundant paths, failover routing |
| **CPU** | Extremely rare | Multi-node redundancy |

**Key insight:** As cluster sizes grow, hardware faults become common events. With 10,000 disks (MTTF 10 years), expect roughly 3 disk failures per day. Systems must handle hardware faults as routine events, not exceptional emergencies.

### Software Faults

Software faults are systematic and correlated. A bug that crashes one node is likely to crash all nodes running the same software. Software faults are more dangerous than hardware faults because they are correlated -- they affect many nodes simultaneously.

**Common software faults:**
- A bug triggered by unusual input that crashes every instance processing that input
- A runaway process consuming all CPU, memory, or disk on every machine
- A cascading failure where one service's slowdown triggers timeouts in dependent services
- A leap second bug that affects every NTP-synchronized server simultaneously

**Mitigations:**
- **Process isolation:** Run services in separate processes or containers so a crash in one doesn't affect others
- **Input validation:** Reject malformed input at the boundary before it reaches core logic
- **Circuit breakers:** Detect when a dependency is failing and stop sending requests, preventing cascade
- **Chaos engineering:** Deliberately inject faults to discover weaknesses before they cause outages
- **Gradual rollouts:** Deploy new code to a small percentage of servers first; monitor before rolling out widely

### Human Errors

Humans are the leading cause of outages. Studies show that configuration errors cause the majority of production incidents -- not hardware or software failures.

**Mitigations:**
- **Design systems that minimize opportunity for error:** Well-designed APIs, admin interfaces, and configurations make it hard to do the wrong thing. Sensible defaults, validation, and dry-run modes.
- **Provide sandbox environments:** Allow engineers to experiment and test safely without affecting production.
- **Test at all levels:** Unit tests, integration tests, property-based tests, chaos tests. Automated testing catches errors that humans introduce.
- **Quick rollback:** Make it fast and easy to roll back a bad deployment. Feature flags allow disabling new code without redeploying.
- **Monitoring and alerting:** Detect problems early through metrics, dashboards, and alerts. If something goes wrong, you want to know in minutes, not hours.
- **Blameless postmortems:** Focus on systemic improvements, not individual blame. If a human error caused an outage, ask why the system allowed that error to cause an outage.

---

## Reliability Metrics

### Availability

Availability is the percentage of time the system is operational:

```
Availability = Uptime / (Uptime + Downtime)
```

| Availability | Downtime per Year | Downtime per Month |
|-------------|-------------------|--------------------|
| **99% (two nines)** | 3.65 days | 7.3 hours |
| **99.9% (three nines)** | 8.76 hours | 43.8 minutes |
| **99.99% (four nines)** | 52.6 minutes | 4.38 minutes |
| **99.999% (five nines)** | 5.26 minutes | 26.3 seconds |

**Key insight:** Each additional nine is roughly 10x harder to achieve. Going from 99.9% to 99.99% requires fundamentally different architecture, not just better operations.

### Durability

Durability is the probability that data, once written, will not be lost:

- **S3 Standard:** 99.999999999% (11 nines) durability -- designed to sustain the loss of data in two facilities simultaneously
- **Single-disk:** ~99.5% over 5 years (depending on disk failure rate)
- **RAID-1:** ~99.99% over 5 years
- **Replicated across 3 data centers:** Approaches 11+ nines

### Mean Time Between Failures (MTBF) and Mean Time To Recovery (MTTR)

```
Availability = MTBF / (MTBF + MTTR)
```

**Implication:** You can improve availability by either increasing MTBF (making failures less frequent) or decreasing MTTR (recovering faster). In practice, reducing MTTR is often more cost-effective because you can't eliminate all faults, but you can recover from them faster.

---

## Detecting Faults in Distributed Systems

### Timeouts

Timeouts are the primary mechanism for detecting faults in distributed systems. If a node doesn't respond within the timeout period, it is considered failed.

**The timeout dilemma:**
- **Too short:** False positives -- a slow but healthy node is declared dead, causing unnecessary failover, load redistribution, and potentially split-brain
- **Too long:** Slow detection -- a truly dead node continues to receive requests that fail, increasing latency and error rates for users

**Choosing timeouts:**
- Measure the p99 response time of healthy nodes
- Set the timeout to p99 * 2 or p99 + a fixed margin (e.g., 1 second)
- Use adaptive timeouts that adjust based on observed latency (Phi Accrual Failure Detector)

### Heartbeats

Nodes periodically send heartbeat messages to indicate they are alive. If a heartbeat is missed, the node may be considered failed.

```
Node A -> Heartbeat every 1 second -> Monitor
Node B -> Heartbeat every 1 second -> Monitor

If Monitor receives no heartbeat from Node B for 3 seconds:
  -> Declare Node B potentially failed
  -> Trigger health check or failover
```

**Heartbeat patterns:**
- **Push-based:** Each node sends heartbeats to a central monitor or to other nodes
- **Pull-based:** A monitor periodically polls each node for status
- **Gossip-based:** Each node gossips its status to random peers; failure information spreads epidemically

### Failure Detectors

A failure detector is an abstraction that encapsulates the logic of deciding whether a node is alive or dead. Properties of failure detectors:

| Property | Meaning |
|----------|---------|
| **Completeness** | Every failed node is eventually detected |
| **Accuracy** | No healthy node is incorrectly declared failed |

In asynchronous networks, no failure detector can guarantee both properties simultaneously. Practical failure detectors sacrifice accuracy (may occasionally declare healthy nodes as failed) to ensure completeness (never miss a truly failed node).

---

## Byzantine Faults

### What Are Byzantine Faults?

A Byzantine fault occurs when a node behaves in an arbitrary and potentially malicious way: sending conflicting information to different peers, lying about its state, or corrupting data intentionally.

### When Byzantine Fault Tolerance Matters

| Context | Needed? | Why |
|---------|---------|-----|
| **Internal datacenter** | No | You trust your own servers; if one is compromised, you have bigger problems |
| **Public blockchain** | Yes | Participants are mutually untrusting; any node may be malicious |
| **Aerospace/nuclear systems** | Sometimes | Radiation can flip bits, causing non-crash arbitrary behavior |
| **Multi-organization systems** | Sometimes | If organizations don't trust each other, Byzantine tolerance may be needed |

### Why Most Systems Ignore Byzantine Faults

Byzantine fault tolerance requires 3f + 1 nodes to tolerate f Byzantine faults. This means tolerating 1 malicious node requires 4 nodes, and tolerating 2 requires 7. The overhead is substantial.

Most systems instead assume a crash-stop or crash-recovery model:
- **Crash-stop:** A faulty node simply stops and never comes back
- **Crash-recovery:** A faulty node stops but may come back with its state intact (from durable storage)

These simpler fault models are sufficient for the vast majority of data systems.

---

## Safety and Liveness

### Definitions

| Property | Definition | Example |
|----------|-----------|---------|
| **Safety** | Nothing bad happens | No two nodes are elected leader simultaneously (no split-brain) |
| **Liveness** | Something good eventually happens | A failed node is eventually detected; a client request eventually receives a response |

### Why the Distinction Matters

In distributed systems, you can always guarantee safety properties, but liveness properties may be temporarily violated:

- **Safety must always hold.** If a safety property is violated even once, the violation is irrecoverable. You can point to a specific moment when the property was violated.
- **Liveness may be temporarily violated.** A liveness violation means something hasn't happened yet, but it may happen in the future. You can't point to a specific moment when it was violated.

**Example: Leader election**
- Safety: At most one leader at any time (must always hold)
- Liveness: A leader is eventually elected (may be temporarily violated during an election)

### Practical Implications

When designing distributed systems, prioritize safety over liveness:
- It is better for the system to be temporarily unavailable (liveness violation) than to produce incorrect results (safety violation)
- A consensus algorithm that never elects a leader is safe (no split-brain) but useless (no liveness)
- The art is achieving both safety and liveness under realistic assumptions about network and node behavior

---

## Designing for Reliability

### Defense in Depth

No single mechanism provides complete reliability. Layer multiple defenses:

```
Layer 1: Input validation and sanitization
Layer 2: Application-level error handling and retries
Layer 3: Database transactions and constraints
Layer 4: Replication and failover
Layer 5: Backups and disaster recovery
Layer 6: Monitoring, alerting, and incident response
```

### Failure Mode Analysis

For each component, ask:
1. **How can it fail?** (crash, slow down, return wrong answer, become unreachable)
2. **What happens when it fails?** (impact on dependent components and users)
3. **How will we detect the failure?** (monitoring, health checks, alerts)
4. **How will we recover?** (automatic failover, manual intervention, restore from backup)
5. **How do we prevent it?** (redundancy, testing, capacity planning)

### Chaos Engineering Principles

Chaos engineering proactively injects faults to discover weaknesses:

| Experiment | What It Tests | Tools |
|-----------|--------------|-------|
| **Kill a node** | Failover and recovery | Chaos Monkey, kill -9 |
| **Network partition** | Partition tolerance, split-brain prevention | tc (traffic control), iptables, Toxiproxy |
| **Clock skew** | Time-dependent logic, lease expiration | libfaketime, NTP manipulation |
| **Disk full** | Logging, WAL, temporary files | dd, fallocate |
| **Slow responses** | Timeout handling, circuit breakers | Toxiproxy, tc netem |
| **DNS failure** | Service discovery fallback | iptables blocking port 53 |
| **Certificate expiration** | TLS handling, renewal processes | Short-lived test certificates |

### The Recovery-Oriented Computing Approach

Instead of trying to prevent all failures, optimize for fast recovery:

1. **Micro-reboots:** Restart individual components instead of entire systems
2. **Undo support:** Every action has an undo; rollback is always available
3. **Redundancy at every level:** No single point of failure from hardware to application
4. **Monitoring is a first-class feature:** Not an afterthought; built into every component from day one
5. **Automation over documentation:** Runbooks become scripts; manual procedures become automated workflows

---

## Practical Reliability Patterns

### Retry with Exponential Backoff and Jitter

```python
def retry_with_backoff(operation, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return operation()
        except TransientError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            jitter = random.uniform(0, delay * 0.5)
            time.sleep(delay + jitter)
```

Jitter prevents thundering herd: if 1000 clients all retry at exactly the same time, they overload the recovering service.

### Circuit Breaker

```
States: CLOSED -> OPEN -> HALF-OPEN -> CLOSED

CLOSED: Requests pass through normally
  -> If failure rate exceeds threshold: transition to OPEN

OPEN: All requests immediately fail (fast fail, no network call)
  -> After timeout period: transition to HALF-OPEN

HALF-OPEN: Allow a small number of test requests
  -> If test requests succeed: transition to CLOSED
  -> If test requests fail: transition back to OPEN
```

### Bulkhead Pattern

Isolate components so that a failure in one doesn't exhaust shared resources:

```
Thread Pool A (20 threads): Service A calls
Thread Pool B (20 threads): Service B calls
Thread Pool C (10 threads): Service C calls

If Service B becomes slow and exhausts its 20 threads,
Services A and C are unaffected -- they have their own pools.
```

### Health Check Endpoints

Every service should expose a health check endpoint that reports:

```json
{
  "status": "healthy",
  "checks": {
    "database": {"status": "healthy", "latency_ms": 5},
    "redis": {"status": "healthy", "latency_ms": 1},
    "disk": {"status": "healthy", "free_gb": 42},
    "memory": {"status": "healthy", "used_percent": 65}
  },
  "version": "2.3.1",
  "uptime_seconds": 86400
}
```

Load balancers and orchestrators (Kubernetes) use health checks to route traffic away from unhealthy instances and restart failing ones.
