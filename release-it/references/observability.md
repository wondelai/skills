# Observability

You cannot operate what you cannot observe. Observability is the ability to understand the internal state of a system by examining its external outputs. It is not an afterthought or a nice-to-have -- it is a first-class design concern that must be built into every service from day one.

A well-observed system lets you answer questions you did not anticipate at design time. A poorly observed system forces you to deploy new instrumentation during an outage -- exactly when you can least afford the risk.


## Table of Contents
1. [The Three Pillars of Observability](#the-three-pillars-of-observability)
2. [Health Check Patterns](#health-check-patterns)
3. [The RED Method](#the-red-method)
4. [The USE Method](#the-use-method)
5. [SLIs, SLOs, and SLAs](#slis-slos-and-slas)
6. [Alerting Strategy](#alerting-strategy)
7. [Dashboards That Matter](#dashboards-that-matter)

---

## The Three Pillars of Observability

### 1. Structured Logs

Logs answer the question: "What happened?"

**Structured logging** means emitting logs as key-value pairs (JSON), not free-form text. Structured logs are searchable, filterable, and aggregatable. Free-form text logs require regex parsing and break when the format changes.

**Essential log fields:**

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the event occurred | `2024-01-15T14:23:45.123Z` |
| `level` | Severity (DEBUG, INFO, WARN, ERROR) | `ERROR` |
| `service` | Which service emitted the log | `payment-service` |
| `trace_id` | Correlation ID across services | `abc123def456` |
| `span_id` | Specific operation within the trace | `span789` |
| `user_id` | Which user was affected (if applicable) | `user_42` |
| `message` | Human-readable description | `Payment processing failed` |
| `error` | Error type and stack trace | `TimeoutException: read timed out` |
| `duration_ms` | How long the operation took | `5230` |
| `request_id` | Unique identifier for the request | `req_abc123` |

**Logging best practices:**
- Log at service boundaries (incoming request, outgoing call, response)
- Include enough context to understand the event without reading code
- Use consistent field names across all services
- Do not log sensitive data (passwords, tokens, PII) -- use redaction
- Log errors with full context, not just the exception message
- Use sampling for high-volume debug logs in production
- Emit logs asynchronously to avoid blocking application threads

### 2. Metrics

Metrics answer the question: "How much?"

Metrics are numeric measurements collected over time. They are cheap to store, fast to query, and essential for dashboards and alerts.

**Metric types:**

| Type | What It Measures | Example |
|------|-----------------|---------|
| **Counter** | Cumulative count of events | `http_requests_total`, `errors_total` |
| **Gauge** | Current value that can go up or down | `active_connections`, `queue_depth`, `cpu_usage` |
| **Histogram** | Distribution of values | `request_duration_seconds` (with buckets for p50, p95, p99) |
| **Summary** | Pre-calculated percentiles | `request_duration_seconds{quantile="0.99"}` |

**Metric naming conventions:**
- Use snake_case: `http_request_duration_seconds`
- Include the unit in the name: `_seconds`, `_bytes`, `_total`
- Use labels for dimensions: `http_requests_total{method="GET", status="200", endpoint="/api/users"}`
- Do not use high-cardinality labels (user IDs, request IDs) -- these explode metric storage

### 3. Distributed Traces

Traces answer the question: "Where did the time go?"

A distributed trace follows a single request across multiple services, showing the sequence of operations, their durations, and their relationships.

**Trace anatomy:**

```
Trace: user request to checkout
├── Span: API Gateway (2ms)
│   ├── Span: Auth Service - validate token (15ms)
│   ├── Span: Cart Service - get cart (45ms)
│   │   └── Span: Database - SELECT cart items (12ms)
│   ├── Span: Inventory Service - check stock (120ms)  ← Bottleneck
│   │   └── Span: Database - SELECT inventory (95ms)
│   └── Span: Payment Service - charge card (230ms)
│       └── Span: Stripe API - create charge (180ms)
Total: 412ms
```

**Trace implementation:**
- Inject trace context (trace ID, span ID) into all outgoing requests (HTTP headers, message metadata)
- Extract trace context from all incoming requests
- Create a new span for each significant operation (service call, database query, cache lookup)
- Annotate spans with relevant metadata (query, parameters, result count)
- Use sampling in production (1-10% of requests) to manage cost and volume
- Always trace errors at 100% (do not sample error traces)

---

## Health Check Patterns

Health checks tell load balancers, orchestrators, and monitoring systems whether an instance is able to serve traffic.

### Shallow Health Check

A shallow health check verifies that the process is running and can respond to HTTP requests. It does not verify dependencies.

```
GET /health
200 OK {"status": "up"}
```

**Use for:** Liveness probes (is the process alive?). If this fails, the orchestrator should restart the process.

### Deep Health Check

A deep health check verifies that the instance can actually serve requests by checking connectivity to all critical dependencies.

```
GET /health/ready
200 OK {
  "status": "ready",
  "checks": {
    "database": {"status": "up", "latency_ms": 3},
    "cache": {"status": "up", "latency_ms": 1},
    "queue": {"status": "up", "latency_ms": 5},
    "disk": {"status": "up", "free_gb": 42}
  }
}

503 Service Unavailable {
  "status": "not_ready",
  "checks": {
    "database": {"status": "down", "error": "connection refused"},
    "cache": {"status": "up", "latency_ms": 1},
    "queue": {"status": "up", "latency_ms": 5},
    "disk": {"status": "up", "free_gb": 42}
  }
}
```

**Use for:** Readiness probes (can this instance serve traffic?). If this fails, the load balancer should stop routing traffic to this instance -- but should not restart it (the problem might be a downstream dependency, not this process).

### Health Check Design Rules

| Rule | Rationale |
|------|-----------|
| **Shallow checks should be fast (<100ms)** | Frequent liveness checks should not consume significant resources |
| **Deep checks should have their own timeout** | A hanging dependency check should not make the health endpoint hang |
| **Do not cache health check results** | Health checks must reflect current state, not cached state |
| **Separate liveness from readiness** | A process can be alive but not ready (warming up, dependency down) |
| **Include version information** | Helps verify deployment status: `"version": "2.3.1", "commit": "abc123"` |
| **Rate-limit deep checks** | Running deep checks every second can stress dependencies |

---

## The RED Method

The RED method is a monitoring framework for request-driven services (APIs, web applications).

### RED Metrics

| Metric | What It Measures | Why It Matters |
|--------|-----------------|---------------|
| **Rate** | Requests per second | Is traffic normal? Dropping? Spiking? |
| **Errors** | Error rate (errors / total requests) | Are users experiencing failures? |
| **Duration** | Latency distribution (p50, p95, p99) | Are users experiencing slowness? |

### Implementation

For every service endpoint, instrument:

```
# Rate
http_requests_total{service, method, endpoint, status}

# Errors
http_errors_total{service, method, endpoint, error_type}
# Error rate = http_errors_total / http_requests_total

# Duration
http_request_duration_seconds{service, method, endpoint}
# Report as histogram with p50, p95, p99 percentiles
```

### RED Dashboard

A RED dashboard for each service should answer three questions at a glance:
1. **Is traffic arriving?** (Rate graph -- sudden drops indicate upstream problems or DNS issues)
2. **Are requests succeeding?** (Error rate graph -- spikes indicate bugs or dependency failures)
3. **Are requests fast?** (Duration graph -- p99 latency increasing indicates saturation)

---

## The USE Method

The USE method is a monitoring framework for infrastructure resources (CPU, memory, disk, network).

### USE Metrics

| Metric | What It Measures | Why It Matters |
|--------|-----------------|---------------|
| **Utilization** | Percentage of resource currently in use | High utilization means approaching capacity |
| **Saturation** | Amount of work waiting (queue depth) | Saturation means demand exceeds capacity |
| **Errors** | Count of error events for this resource | Hardware errors, packet drops, OOM kills |

### USE by Resource

| Resource | Utilization | Saturation | Errors |
|----------|------------|------------|--------|
| **CPU** | % time busy | Run queue length | Machine check exceptions |
| **Memory** | % used | Swap usage, OOM events | ECC errors, OOM kills |
| **Disk** | % capacity used, IOPS utilization | I/O queue depth | Read/write errors |
| **Network** | Bandwidth utilization | TCP retransmit queue, dropped packets | Interface errors, CRC errors |
| **Thread pool** | Active threads / max threads | Queued tasks | Rejected tasks |
| **Connection pool** | Active connections / max connections | Wait count | Timeout errors |

---

## SLIs, SLOs, and SLAs

### Definitions

| Term | Definition | Example |
|------|-----------|---------|
| **SLI** (Service Level Indicator) | A quantitative measure of a specific aspect of service quality | 99.2% of requests complete in < 200ms |
| **SLO** (Service Level Objective) | A target value for an SLI | 99.5% of requests should complete in < 200ms |
| **SLA** (Service Level Agreement) | A contractual commitment with consequences for violation | 99.9% availability; credit issued if breached |

### Choosing SLIs

Good SLIs measure what users actually experience:

| SLI Type | What It Measures | Measurement Point |
|----------|-----------------|-------------------|
| **Availability** | Proportion of successful requests | Load balancer or edge proxy |
| **Latency** | Proportion of requests faster than threshold | Application instrumentation |
| **Correctness** | Proportion of requests returning correct results | End-to-end tests or data validation |
| **Freshness** | Proportion of data updated within threshold | Data pipeline monitoring |

### Error Budget

The error budget is the allowed amount of unreliability: `error_budget = 1 - SLO`.

For a 99.9% availability SLO:
- Error budget = 0.1% = 43.8 minutes/month of downtime
- If you have consumed 30 minutes of budget, you have 13.8 minutes remaining
- If the budget is exhausted, freeze deployments and focus on reliability

**Error budget policy:**
- Budget remaining > 50%: deploy freely, run experiments
- Budget remaining 20-50%: deploy with caution, increase monitoring
- Budget remaining < 20%: freeze non-critical deploys, prioritize reliability work
- Budget exhausted: halt all feature deploys until budget replenishes

---

## Alerting Strategy

### Alert on Symptoms, Not Causes

| Cause-Based Alert (Avoid) | Symptom-Based Alert (Prefer) |
|--------------------------|------------------------------|
| CPU > 80% | p99 latency > 500ms |
| Memory > 90% | Error rate > 1% |
| Disk > 85% | Availability < 99.9% |
| Queue depth > 1000 | User-facing errors increasing |

Cause-based alerts generate noise. CPU can be at 90% and users are fine. CPU can be at 50% and users are seeing errors because of a deadlock.

### Alert Severity Levels

| Level | Criteria | Response | Example |
|-------|----------|----------|---------|
| **Critical** | Users actively impacted; error budget burning fast | Page on-call immediately | Error rate > 5% for 5 minutes |
| **Warning** | Approaching threshold; action needed soon | Notify team during business hours | Error budget burn rate 2x normal |
| **Info** | Notable but not actionable | Log and dashboard only | Deployment completed; circuit breaker tripped and recovered |

### Alerting Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Alert on every metric** | Alert fatigue; team ignores pages | Only alert on user-facing symptoms |
| **No alert grouping** | 50 alerts fire for one incident | Group related alerts; alert on the root symptom |
| **No runbook** | On-call does not know what to do | Every alert links to a runbook with diagnostic steps |
| **Stale alerts** | Alerts for services that no longer exist | Review and prune alerts quarterly |
| **Missing alerts** | Critical failures go unnoticed | Regularly audit: "If X fails, would we know?" |

---

## Dashboards That Matter

A dashboard should answer "Is the system healthy right now?" within 5 seconds of looking at it.

### Dashboard Hierarchy

| Level | Audience | Content |
|-------|----------|---------|
| **Executive** | Leadership | SLO status (green/red), error budget remaining, incident count |
| **Service overview** | On-call engineer | RED metrics per service, dependency status |
| **Service deep-dive** | Service owner | Detailed metrics, resource utilization, deployment markers |
| **Debug** | Investigating engineer | Traces, log queries, specific metric breakdowns |

### Dashboard Design Rules

- **USE traffic lights:** Green (healthy), yellow (degraded), red (critical) at the top of every dashboard
- **Show trends, not just current values:** A metric at 70% is fine if it has been at 70% for a week; it is alarming if it was at 30% an hour ago
- **Mark deployments:** Overlay deployment events on metric graphs to correlate changes with behavior
- **Time range matters:** Default to 6 hours for operational dashboards; allow quick switching to 1h, 24h, 7d
- **Less is more:** A dashboard with 50 graphs is useless; a dashboard with 4 graphs that answer the right questions is invaluable
