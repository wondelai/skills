# Chaos Engineering

Chaos engineering is the discipline of experimenting on a system in order to build confidence in its ability to withstand turbulent conditions in production. It is not about breaking things for fun -- it is a rigorous, scientific approach to discovering weaknesses before they cause outages.

> **Safety note:** This reference describes chaos engineering *concepts and planning patterns*. All failure injection experiments must be performed by authorized engineers using dedicated chaos tooling (e.g., Gremlin, Litmus, AWS Fault Injection Simulator) with proper approvals, blast radius controls, monitoring, and rollback plans. Commands shown are for reference only -- never run them without authorization and safeguards.

The fundamental insight is simple: you cannot know how your system handles failure until it actually fails. Waiting for production incidents to discover weaknesses is reactive and expensive. Chaos engineering is proactive and controlled.


## Table of Contents
1. [Principles of Chaos Engineering](#principles-of-chaos-engineering)
2. [Chaos Experiment Design](#chaos-experiment-design)
3. [Failure Injection Techniques](#failure-injection-techniques)
4. [Chaos Monkey and Netflix's Approach](#chaos-monkey-and-netflixs-approach)
5. [GameDay Exercises](#gameday-exercises)
6. [Building Confidence Through Controlled Failure](#building-confidence-through-controlled-failure)

---

## Principles of Chaos Engineering

### 1. Define Steady State

Before you can detect abnormal behavior, you must define what normal looks like. Steady state is expressed as measurable business or system metrics that indicate the system is functioning correctly.

**Good steady state definitions:**

| Metric Type | Steady State Definition | Example |
|-------------|----------------------|---------|
| **Business metric** | Orders per minute within expected range | 100-150 orders/min during business hours |
| **Error rate** | Below defined threshold | < 0.1% 5xx errors |
| **Latency** | Within SLO bounds | p99 latency < 500ms |
| **Throughput** | Within expected range | 1000-2000 RPS |
| **Availability** | All critical paths responding | Health checks green on all services |

**Bad steady state definitions:**
- "The system is working" (not measurable)
- "No alerts firing" (absence of evidence is not evidence of absence)
- "CPU below 80%" (cause-based, not symptom-based)

### 2. Formulate a Hypothesis

Every chaos experiment starts with a hypothesis: a prediction about what will happen when you inject a specific failure.

**Hypothesis format:**
```
"We believe that when [failure condition], the system will [expected behavior],
as measured by [steady state metric] remaining within [acceptable bounds]."
```

**Example hypotheses:**

| Failure | Hypothesis | Metric |
|---------|-----------|--------|
| Terminate one API instance (via chaos tooling) | System continues serving traffic with no user-visible errors | Error rate stays < 0.1% |
| Add 500ms latency to database (via chaos tooling) | Response time degrades but stays within SLO; circuit breaker does not trip | p99 < 2s; no circuit breaker events |
| Payment service returns 503 (via fault injection proxy) | Checkout shows graceful error; other features unaffected | Non-checkout error rate unchanged |
| Disk at 95% capacity (via chaos tooling) | Log rotation triggers; alerts fire; no service disruption | Disk drops below 90% within 10 minutes |

### 3. Introduce Real-World Failures

Chaos experiments should simulate failures that actually happen in production, not theoretical edge cases.

**Common failure types to simulate (via dedicated chaos tooling):**

| Category | Failures | Tooling Examples |
|----------|----------|-----------------|
| **Infrastructure** | Instance crash, disk failure, network partition | Gremlin, Litmus, AWS FIS |
| **Network** | Latency, packet loss, DNS failure | Toxiproxy, Istio fault injection, tc (traffic control) |
| **Application** | Memory pressure, CPU saturation, thread contention | stress-ng (controlled), Gremlin resource attacks |
| **Dependency** | Service unavailable, slow response, corrupt response | Toxiproxy, Envoy fault injection, mock services |
| **Cloud** | AZ failure, region degradation, API throttling | AWS FIS, GCP Fault Injection, Azure Chaos Studio |

### 4. Run in Production

Staging environments do not reproduce the complexity of production. They lack real user traffic, real data volumes, real concurrency patterns, and real interactions between services. Chaos experiments in staging build false confidence.

**But safely:**
- Start with non-production, then graduate to production
- Use the smallest blast radius possible
- Have an emergency stop mechanism to halt the experiment immediately
- Run during business hours when the team is available to respond
- Inform the on-call team before running experiments
- Never experiment during peak traffic or known risky periods

### 5. Automate and Run Continuously

A chaos experiment that runs once proves resilience at one point in time. Automated, recurring experiments prove resilience continuously.

**Automation maturity levels:**

| Level | Practice | Confidence |
|-------|----------|-----------|
| **Manual** | Engineer runs experiment by hand, observes results | Low -- depends on who runs it and when |
| **Scripted** | Experiment codified in a script, run on schedule | Medium -- repeatable but requires human analysis |
| **Automated** | Experiment runs automatically, evaluates steady state, reports results | High -- continuous verification |
| **Integrated** | Experiments run in CI/CD pipeline; failing experiment blocks deployment | Very high -- resilience is a deployment gate |

---

## Chaos Experiment Design

### Experiment Template

```
Experiment: [Name]
Date: [When]
Team: [Who is running it]
Blast Radius: [What is affected]

Hypothesis:
  When [failure condition], we expect [behavior],
  as measured by [metric] remaining within [bounds].

Steady State:
  - Metric 1: [current value, acceptable range]
  - Metric 2: [current value, acceptable range]

Method:
  1. Verify steady state
  2. Inject [specific failure]
  3. Observe for [duration]
  4. Measure [metrics]
  5. Remove failure injection
  6. Verify recovery to steady state

Abort Conditions:
  - [Metric] exceeds [threshold]
  - On-call pages for [service]
  - Customer-visible impact detected

Results:
  - Hypothesis confirmed/refuted
  - Observations: [what happened]
  - Action items: [what to fix]
```

### Blast Radius Management

Blast radius is the scope of impact if the experiment causes unexpected damage. Always minimize blast radius and expand gradually.

**Blast radius levels:**

| Level | Scope | When to Use |
|-------|-------|-------------|
| **Development** | Single developer's environment | First-time experiments, unproven hypotheses |
| **Staging** | Staging environment | Validating experiment mechanics before production |
| **Canary** | Small subset of production (1-5%) | First production experiment for a new failure type |
| **Single AZ** | One availability zone in production | Testing AZ failure resilience |
| **Full production** | All production traffic | Well-understood experiments that have been run many times |

**Blast radius controls:**
- **Targeting:** Limit experiment to specific instances, user segments, or traffic percentage
- **Duration:** Set maximum experiment duration; auto-revert after timeout
- **Emergency stop:** One-button (or automatic) experiment termination
- **Monitoring:** Real-time dashboards showing experiment impact on steady state metrics
- **Rollback:** Pre-planned steps to undo the experiment if things go wrong

---

## Failure Injection Techniques

### Process-Level Failures

| Technique | What It Simulates | Chaos Tooling |
|-----------|-------------------|--------------|
| Instance termination | Crash | Gremlin process attack, Kubernetes pod disruption budget, Litmus ChaosEngine |
| Process freeze | Hang/unresponsive | Gremlin process attack (pause), Litmus pod-cpu-hog |
| CPU saturation | Compute pressure | Gremlin CPU attack, Litmus cpu-hog, stress-ng (controlled, authorized) |
| Memory pressure | Memory exhaustion | Gremlin memory attack, Litmus pod-memory-hog |
| Process flood | Process table exhaustion | Gremlin process attack with controlled parameters |

### Network-Level Failures

| Technique | What It Simulates | Chaos Tooling |
|-----------|-------------------|--------------|
| Latency injection | Slow network | Toxiproxy, Gremlin latency attack, Istio fault injection |
| Packet loss | Unreliable network | Gremlin packet loss attack, Toxiproxy, tc netem (authorized) |
| Network partition | Network split | Gremlin blackhole attack, Litmus pod-network-partition |
| DNS failure | DNS outage | Gremlin DNS attack, Litmus pod-dns-error |
| Bandwidth limit | Constrained network | Toxiproxy bandwidth limit, Gremlin bandwidth attack |

### Dependency-Level Failures

| Technique | What It Simulates | Chaos Tooling |
|-----------|-------------------|--------------|
| Error injection proxy | Downstream errors | Toxiproxy, Envoy fault injection |
| Latency injection | Slow dependency | Toxiproxy, Istio fault injection |
| Connection limit | Pool exhaustion | Toxiproxy connection limit, Gremlin blackhole |
| Response corruption | Data integrity issues | Custom fault injection proxy |
| Certificate expiration | TLS failures | Expired test certificate in staging |

### Disk-Level Failures

| Technique | What It Simulates | Chaos Tooling |
|-----------|-------------------|--------------|
| Disk pressure | Disk full | Gremlin disk attack, Litmus disk-fill |
| Slow I/O | Storage degradation | Gremlin IO attack, dm-delay (authorized) |
| Read-only filesystem | Mount failure | Gremlin disk attack (read-only mode) |
| Data corruption | Integrity issues | Controlled corruption of test data in staging |

---

## Chaos Monkey and Netflix's Approach

Netflix pioneered chaos engineering with Chaos Monkey, which randomly terminates production instances during business hours using automated, authorized tooling with built-in safeguards.

### The Netflix Chaos Engineering Stack

| Tool | What It Does | Scope |
|------|-------------|-------|
| **Chaos Monkey** | Terminates random instances (automated, authorized) | Single instance |
| **Chaos Kong** | Simulates entire region failure | Region |
| **Latency Monkey** | Injects network latency | Network |
| **Conformity Monkey** | Finds instances not following best practices | Compliance |
| **Chaos Automation Platform (ChAP)** | Runs automated experiments with steady state comparison | Full stack |

### Key Lessons from Netflix

1. **Start small:** Chaos Monkey terminates one instance at a time. Only after years of practice did Netflix graduate to region-level chaos (Chaos Kong).
2. **Business hours only:** Run experiments when the team is available to respond. Late-night chaos is just an outage.
3. **Opt-out, not opt-in:** By default, all services are enrolled. Teams must explicitly justify opting out.
4. **No blame:** Finding a weakness is a success, not a failure. Teams that discover and fix problems through chaos engineering are celebrated.
5. **Invest in tooling:** Manual chaos is not sustainable. Invest in platforms that automate experiment execution, evaluation, and reporting.

---

## GameDay Exercises

A GameDay is a scheduled exercise where a team practices responding to a realistic failure scenario. It combines chaos engineering (inject failure) with incident response practice (detect, diagnose, mitigate, resolve).

### GameDay Structure

| Phase | Duration | Activities |
|-------|----------|-----------|
| **Preparation** | 1-2 weeks before | Define scenario, brief participants, set up monitoring |
| **Pre-game** | 30 minutes | Verify steady state, confirm all participants are ready |
| **Execution** | 1-3 hours | Inject failure, observe team response, take notes |
| **Post-game** | 1 hour | Debrief, identify what worked and what did not |
| **Follow-up** | 1-2 weeks after | File action items, track remediation, schedule next GameDay |

### GameDay Scenarios

| Scenario | Complexity | What It Tests |
|----------|-----------|---------------|
| Terminate a single instance | Low | Auto-healing, health checks, load balancing |
| Simulate database failover | Medium | Connection handling, read replica routing, data consistency |
| Full AZ failure | High | Multi-AZ architecture, DNS failover, stateful service recovery |
| Dependency outage (payment provider) | Medium | Circuit breakers, fallback behavior, user communication |
| Security incident (compromised credentials) | High | Credential rotation, access logging, incident response process |
| Data corruption | High | Backup restoration, data validation, recovery time |

### GameDay Ground Rules

1. **Safety first:** A facilitator can halt the exercise at any time if real customer impact occurs
2. **No blame:** The goal is learning, not grading individual performance
3. **Document everything:** Notes, timestamps, decisions, and outcomes
4. **Include diverse roles:** Engineers, SREs, product managers, customer support
5. **Realistic but controlled:** Use production systems but with blast radius limits
6. **Schedule during business hours:** The team should be fully staffed and alert
7. **Announce to stakeholders:** Customer support and leadership should know a GameDay is happening

### GameDay Facilitation Tips

- **The facilitator does not fix things.** Their job is to inject failures, observe the response, and take notes.
- **Start with known weaknesses.** The first GameDay should test a scenario the team suspects might fail -- the learning is in confirming the suspicion and practicing the response.
- **Increase difficulty over time.** First GameDay: terminate one instance. Tenth GameDay: simultaneous database failover + network partition + on-call engineer is unavailable.
- **Celebrate findings.** Every weakness discovered in a GameDay is a weakness that will not cause a real outage. This is a win.

---

## Building Confidence Through Controlled Failure

### The Confidence Curve

```
Confidence
    ▲
    │                              ╭───────────
    │                         ╭────╯
    │                    ╭────╯
    │               ╭────╯
    │          ╭────╯
    │     ╭────╯
    │╭────╯
    └──────────────────────────────────────────→ Experiments
      0    10    20    30    40    50    60
```

Each successful chaos experiment increases confidence that the system will survive that failure in production. Each failed experiment (where the hypothesis was disproven) reveals a weakness that, once fixed, increases actual resilience.

### Maturity Model

| Level | Practice | Organization |
|-------|----------|-------------|
| **Level 0: Reactive** | No chaos engineering; learn from production incidents | Firefighting culture |
| **Level 1: Exploratory** | Manual, ad-hoc experiments; individual teams | Curious early adopters |
| **Level 2: Systematic** | Regular GameDays; documented experiments; shared learnings | Engineering-wide practice |
| **Level 3: Automated** | Continuous automated experiments; integrated into CI/CD | Platform team provides tooling |
| **Level 4: Cultural** | Chaos engineering is expected for all services; opt-out requires justification | Resilience is a core engineering value |

### Getting Started

If you have never done chaos engineering, start here:

1. **Pick one service** -- the one you are most worried about
2. **Define its steady state** -- what metrics prove it is working?
3. **Form one hypothesis** -- "If we terminate one instance, the service will continue serving traffic"
4. **Run the experiment in staging** -- verify your tooling and monitoring work
5. **Run the experiment in production** -- with minimal blast radius and an emergency stop mechanism
6. **Document the results** -- what happened? Was the hypothesis confirmed?
7. **Fix what you found** -- if the hypothesis was disproven, fix the weakness
8. **Repeat** -- expand to more failure types, more services, more complex scenarios

### Common Objections and Responses

| Objection | Response |
|-----------|---------|
| "We can't break production on purpose!" | You are already breaking production accidentally. Chaos engineering lets you do it on your terms, when you are prepared. |
| "Our system isn't resilient enough for chaos" | That is exactly why you need chaos engineering -- to find and fix the weaknesses. Start small. |
| "We don't have time for this" | You have time for incident response, post-mortems, and customer apologies. Chaos engineering reduces all three. |
| "What if we cause an outage?" | Start with minimal blast radius in staging. Terminate one process. If that causes an outage, you have learned something invaluable. |
| "Management won't approve this" | Frame it as risk reduction, not risk creation. Show the cost of recent outages vs. the cost of preventive experiments. |

### Anti-Fragility

The ultimate goal of chaos engineering is not just resilience (surviving failure) but anti-fragility (getting stronger from failure). A system is anti-fragile when each failure makes it more resistant to future failures.

**How chaos engineering builds anti-fragility:**
- Each experiment reveals a weakness
- Each fix removes that weakness permanently
- Each automated experiment continuously verifies the fix
- Over time, the system has been tested against every common failure mode
- New failure modes are discovered faster because the team has built the muscles and tooling to find them

This is the Release It! philosophy in action: production-ready software is not software that never fails. It is software that has been designed, tested, and operated to handle failure gracefully -- because failure is not a possibility, it is a certainty.
