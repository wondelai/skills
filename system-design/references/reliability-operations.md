# Reliability and Operations

A system is only as good as its ability to stay up, recover from failures, and be observed. This reference covers the operational practices that turn a design diagram into a production system.


## Table of Contents
1. [Health Checks](#health-checks)
2. [Monitoring and Alerting](#monitoring-and-alerting)
3. [Logging](#logging)
4. [Deployment Strategies](#deployment-strategies)
5. [Disaster Recovery](#disaster-recovery)
6. [Data Center Redundancy](#data-center-redundancy)
7. [Autoscaling](#autoscaling)
8. [Operational Readiness Checklist](#operational-readiness-checklist)

---

## Health Checks

### Liveness vs Readiness

Two fundamentally different questions:

| Check | Question | What Happens on Failure |
|-------|----------|------------------------|
| **Liveness** | Is the process alive and not deadlocked? | Restart the process |
| **Readiness** | Can this instance serve traffic right now? | Remove from load balancer (but don't restart) |

### Implementation

**Liveness probe (`/healthz` or `/livez`):**
```
Returns 200 if:
  - Process is running
  - Main thread is responsive
  - No deadlock detected

Returns 503 if:
  - Event loop is blocked
  - Process is in an unrecoverable state
```

**Readiness probe (`/readyz` or `/ready`):**
```
Returns 200 if:
  - Database connection is active
  - Cache connection is active
  - Required downstream services are reachable
  - Startup initialization is complete

Returns 503 if:
  - Any critical dependency is unreachable
  - Still warming up (loading cache, running migrations)
```

### Best Practices

- Liveness checks should be simple and fast (< 100ms) -- don't check external dependencies
- Readiness checks should verify all critical dependencies
- Set appropriate thresholds: don't restart on a single failure (3 consecutive failures is typical)
- Include version and build info in health check response for debugging
- Separate health check endpoints for different concerns (database, cache, queue)

### Kubernetes Configuration

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /readyz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 2
```

---

## Monitoring and Alerting

### The Three Pillars of Observability

| Pillar | What It Captures | Tools | Use Case |
|--------|-----------------|-------|----------|
| **Metrics** | Numeric measurements over time | Prometheus, Datadog, CloudWatch | Dashboards, alerting, trend analysis |
| **Logs** | Discrete events with context | ELK (Elasticsearch, Logstash, Kibana), CloudWatch Logs, Splunk | Debugging, audit trails, error investigation |
| **Traces** | Request journey across services | Jaeger, Zipkin, AWS X-Ray, Datadog APM | Latency analysis, dependency mapping, bottleneck identification |

### Key Metrics to Track

#### The Four Golden Signals (Google SRE)

| Signal | What It Measures | Example Metric |
|--------|-----------------|----------------|
| **Latency** | Time to serve a request | P50, P95, P99 response time |
| **Traffic** | Demand on the system | Requests per second (QPS) |
| **Errors** | Rate of failed requests | 5xx error rate, timeout rate |
| **Saturation** | How full the system is | CPU utilization, memory usage, queue depth |

#### The RED Method (for request-driven services)

- **Rate:** Requests per second
- **Errors:** Errors per second
- **Duration:** Distribution of request latency

#### The USE Method (for resources)

- **Utilization:** Percentage of resource in use (CPU at 80%)
- **Saturation:** Work queued because resource is busy (run queue length)
- **Errors:** Error events on the resource (disk I/O errors)

### Alerting Best Practices

| Practice | Why | Example |
|----------|-----|---------|
| **Alert on symptoms, not causes** | Users care about latency, not CPU | Alert on "P99 latency > 500ms" not "CPU > 80%" |
| **Severity levels** | Not everything is a page | Critical (page on-call), Warning (ticket), Info (log) |
| **Include runbook link** | Responder needs context | Alert message includes link to troubleshooting steps |
| **Avoid alert fatigue** | Too many alerts = ignored alerts | Review and prune alerts quarterly; every alert must be actionable |
| **Set appropriate thresholds** | Too sensitive = noise; too lenient = missed issues | Use percentile-based thresholds (P99 > X) rather than averages |

### Dashboard Design

Every service should have a standard dashboard with:

1. **Request rate** (QPS) -- is traffic normal?
2. **Error rate** (4xx, 5xx) -- are requests failing?
3. **Latency** (P50, P95, P99) -- are requests slow?
4. **Saturation** (CPU, memory, disk, connections) -- are resources exhausted?
5. **Dependencies** (downstream error rate, latency) -- are dependencies healthy?

---

## Logging

### Log Levels

| Level | When to Use | Example |
|-------|------------|---------|
| **ERROR** | Something failed and needs attention | Database connection lost, payment processing failed |
| **WARN** | Something unexpected but handled | Retry succeeded, deprecated API called |
| **INFO** | Normal operational events | Request processed, user logged in, deployment started |
| **DEBUG** | Detailed diagnostic information | SQL queries, request/response bodies, cache hits/misses |

### Structured Logging

Always use structured (JSON) logging, not plain text:

**Bad:**
```
2024-01-15 10:23:45 ERROR Failed to process order 12345 for user 678
```

**Good:**
```json
{
  "timestamp": "2024-01-15T10:23:45Z",
  "level": "ERROR",
  "message": "Failed to process order",
  "order_id": "12345",
  "user_id": "678",
  "error": "payment_declined",
  "trace_id": "abc-123-def",
  "service": "order-service",
  "duration_ms": 2340
}
```

### Best Practices

- Include a correlation/trace ID in every log entry (links logs across services)
- Never log sensitive data (passwords, tokens, full credit card numbers, PII)
- Log at request boundaries (request received, response sent, downstream calls)
- Set appropriate retention (7 days for DEBUG, 30 days for INFO, 90+ days for ERROR)
- Use log aggregation (ELK, CloudWatch, Splunk) -- never rely on SSH-ing into servers

---

## Deployment Strategies

### Rolling Deployment

**How it works:** Replace instances one at a time. At any point, some instances run the old version and some run the new version.

| Pros | Cons |
|------|------|
| Zero downtime | Two versions running simultaneously (must be backward-compatible) |
| Simple to implement | Slow rollout for large fleets |
| Easy rollback (stop rolling, roll backward) | Mixed-version issues during deployment |

**Best for:** Stateless services, backward-compatible changes.

### Blue-Green Deployment

**How it works:** Run two identical environments (blue and green). Deploy new version to green. Switch traffic from blue to green. Keep blue as instant rollback.

| Pros | Cons |
|------|------|
| Instant rollback (switch back to blue) | Double the infrastructure cost |
| No mixed versions | Database schema changes are tricky (both versions need to work) |
| Full testing of green before switch | Requires sophisticated load balancer or DNS switching |

**Best for:** Critical services where instant rollback is essential.

### Canary Deployment

**How it works:** Route a small percentage of traffic (1-5%) to the new version. Compare metrics (latency, error rate) between old and new. Gradually increase traffic if metrics are healthy.

| Pros | Cons |
|------|------|
| Low risk (small blast radius) | More complex infrastructure |
| Real production testing | Requires good monitoring to detect issues |
| Data-driven promotion decisions | Two versions running simultaneously |

**Canary progression:**
1. Deploy to 1-2% of traffic
2. Wait 10-30 minutes, compare metrics
3. If healthy: increase to 10%, wait, compare
4. If healthy: increase to 50%, wait, compare
5. If healthy: promote to 100%
6. At any step: if metrics degrade, rollback to 0%

**Best for:** Large-scale services where you want data-driven confidence.

### Feature Flags

**How it works:** Deploy code with features behind flags. Enable features independently of deployment.

| Pros | Cons |
|------|------|
| Decouple deployment from release | Flag management complexity |
| Per-user or per-segment rollout | Dead flags accumulate (tech debt) |
| Instant disable without deployment | Testing combinatorial complexity |

**Best combined with:** Canary deployment. Deploy the code, then canary the feature flag.

---

## Disaster Recovery

### RPO and RTO

Two metrics define your disaster recovery requirements:

| Metric | Question | Example |
|--------|----------|---------|
| **RPO (Recovery Point Objective)** | How much data can you afford to lose? | RPO = 1 hour means you need at least hourly backups |
| **RTO (Recovery Time Objective)** | How long can you be down? | RTO = 15 minutes means automated failover is required |

### Disaster Recovery Strategies

| Strategy | RPO | RTO | Cost | How It Works |
|----------|-----|-----|------|-------------|
| **Backup and restore** | Hours | Hours | Low | Periodic backups to S3; restore on failure |
| **Pilot light** | Minutes | Minutes-hours | Medium | Minimal replica running; scale up on failure |
| **Warm standby** | Seconds-minutes | Minutes | High | Scaled-down replica always running; scale up on failure |
| **Multi-site active-active** | Near-zero | Near-zero | Very high | Full copy in each region; both serve traffic |

### Backup Best Practices

- **3-2-1 rule:** 3 copies, 2 different media types, 1 offsite
- **Test restores regularly** -- an untested backup is not a backup
- **Automate backup verification** -- checksum validation, test restore to staging
- **Encrypt backups** -- at rest and in transit
- **Define retention** -- daily for 7 days, weekly for 4 weeks, monthly for 12 months

---

## Data Center Redundancy

### Active-Passive

```
Primary DC: Serves all traffic
Secondary DC: Hot standby, receives replicated data
Failover: DNS or load balancer switches to secondary
```

| Pros | Cons |
|------|------|
| Simpler (one write path) | Wasted capacity in passive DC |
| No conflict resolution needed | Failover takes time (DNS TTL, warmup) |
| Clear data authority | Secondary may have replication lag |

### Active-Active

```
DC-A: Serves region A traffic, replicates to DC-B
DC-B: Serves region B traffic, replicates to DC-A
```

| Pros | Cons |
|------|------|
| Full utilization of both DCs | Write conflicts between DCs |
| Lower latency (users hit nearest DC) | Complex data synchronization |
| No failover needed (traffic redirects) | Must handle split-brain scenarios |

### Key Challenges

| Challenge | Solution |
|-----------|---------|
| **Data synchronization** | Async replication with conflict resolution (LWW, CRDTs) |
| **Session management** | Centralized session store (Redis) or stateless sessions (JWT) |
| **Cache consistency** | Accept eventual consistency or use distributed cache |
| **Traffic routing** | GeoDNS routes users to nearest DC; health-check-based failover |

---

## Autoscaling

### What to Scale On

| Metric | When to Use | Example |
|--------|------------|---------|
| **CPU utilization** | Compute-bound workloads | Scale up when CPU > 70% for 5 minutes |
| **Memory utilization** | Memory-bound workloads | Scale up when memory > 80% |
| **Request rate** | Traffic-driven scaling | Scale up when QPS > 1000 per instance |
| **Queue depth** | Worker-based processing | Scale up when queue > 10,000 messages |
| **Custom metrics** | Business-specific | Scale up when active WebSocket connections > 5,000 per instance |

### Scaling Configuration

| Parameter | Recommendation | Why |
|-----------|---------------|-----|
| **Min instances** | At least 2 (for redundancy) | Survives single instance failure |
| **Max instances** | Set a cap (cost protection) | Prevents runaway scaling from bugs or attacks |
| **Scale-up threshold** | 70% utilization | Leave headroom for traffic spikes during scale-up |
| **Scale-down threshold** | 30% utilization | Avoid flapping (scaling up and down repeatedly) |
| **Cooldown period** | 5-10 minutes | Prevents rapid oscillation |

### Scaling Strategies

| Strategy | How It Works | Best For |
|----------|-------------|----------|
| **Reactive** | Scale based on current metrics | Unpredictable traffic |
| **Scheduled** | Pre-scale for known patterns | Predictable peaks (morning rush, end-of-day batch) |
| **Predictive** | ML-based prediction of future load | Gradual ramps with some predictability |

### Common Autoscaling Mistakes

| Mistake | Consequence | Fix |
|---------|------------|-----|
| No max limit | Runaway costs or resource exhaustion | Always set max instances |
| Scaling on average, not percentile | Miss tail latency issues | Scale on P95/P99 latency or queue depth |
| Too aggressive cooldown | Flapping (scale up, scale down, repeat) | Set cooldown to 5-10 minutes |
| Scaling only the web tier | Database becomes bottleneck | Scale all tiers (web, cache, database connections) |
| No load testing | Unknown scaling behavior | Load test to find breaking points before production |

---

## Operational Readiness Checklist

Before going to production, verify:

| Category | Check |
|----------|-------|
| **Health** | Liveness and readiness probes configured |
| **Monitoring** | Dashboard with four golden signals |
| **Alerting** | Critical alerts with runbooks |
| **Logging** | Structured logs with trace IDs |
| **Deployment** | Rollback plan tested |
| **Scaling** | Autoscaling configured with min/max |
| **Backup** | Backup schedule defined, restore tested |
| **DR** | RPO/RTO defined, failover tested |
| **Security** | Secrets in vault, TLS everywhere, access controlled |
| **Documentation** | Architecture diagram, runbooks, on-call rotation |
