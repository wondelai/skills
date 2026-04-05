# Deployment Strategies

The distinction between deployment (placing code on infrastructure) and release (exposing code to users) is fundamental. Conflating the two means every deployment is a high-risk event. Separating them gives you the ability to deploy with confidence, test in production, and release when ready.

Most production outages are caused by changes. Deployment strategies exist to make changes safe.


## Table of Contents
1. [Zero-Downtime Deployment](#zero-downtime-deployment)
2. [Rolling Deployment](#rolling-deployment)
3. [Blue-Green Deployment](#blue-green-deployment)
4. [Canary Releases](#canary-releases)
5. [Feature Flags](#feature-flags)
6. [Database Migrations Without Downtime](#database-migrations-without-downtime)
7. [Immutable Infrastructure](#immutable-infrastructure)
8. [Infrastructure as Code](#infrastructure-as-code)
9. [Rollback Strategy](#rollback-strategy)

---

## Zero-Downtime Deployment

Zero-downtime deployment is not optional for any system with users. Users should never see an error page because you are deploying code.

### Prerequisites for Zero-Downtime Deployment

| Requirement | Why |
|-------------|-----|
| **Backward-compatible changes** | Old code and new code run simultaneously during deployment |
| **Graceful shutdown** | In-flight requests must complete before an instance is terminated |
| **Health checks** | Load balancer must know when a new instance is ready to receive traffic |
| **Session independence** | Requests from the same user can be routed to any instance |
| **Database compatibility** | Schema changes must work with both old and new application code |

---

## Rolling Deployment

The simplest zero-downtime strategy. Replace instances one at a time (or in small batches), verifying health after each replacement.

### How It Works

```
Cluster: [v1] [v1] [v1] [v1] [v1]

Step 1:  [v2] [v1] [v1] [v1] [v1]   ← Deploy to instance 1, verify health
Step 2:  [v2] [v2] [v1] [v1] [v1]   ← Deploy to instance 2, verify health
Step 3:  [v2] [v2] [v2] [v1] [v1]   ← Deploy to instance 3, verify health
Step 4:  [v2] [v2] [v2] [v2] [v1]   ← Deploy to instance 4, verify health
Step 5:  [v2] [v2] [v2] [v2] [v2]   ← Deploy to instance 5, verify health
```

### Configuration Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| **Max unavailable** | Maximum instances being replaced simultaneously | 1 or 25% |
| **Max surge** | Extra instances during deployment | 1 or 25% |
| **Readiness probe** | Health check before receiving traffic | HTTP 200 on `/ready` |
| **Min ready seconds** | How long instance must be healthy before proceeding | 30-60 seconds |

### Advantages and Limitations

| Advantage | Limitation |
|-----------|-----------|
| Simple to implement | Both versions run simultaneously (must be compatible) |
| Gradual rollout | Rollback requires re-deploying old version |
| No extra infrastructure | Reduced capacity during deployment |
| Built into Kubernetes | Slow for large clusters |

---

## Blue-Green Deployment

Maintain two identical production environments. One (blue) serves live traffic. Deploy to the other (green), verify, and switch the router.

### How It Works

```
                    ┌──────────────┐
Users → Router ────→│  Blue (v1)   │  ← Currently live
                    └──────────────┘
                    ┌──────────────┐
                    │  Green (v2)  │  ← Deploy here, test
                    └──────────────┘

After verification:

                    ┌──────────────┐
                    │  Blue (v1)   │  ← Standby (instant rollback)
                    └──────────────┘
                    ┌──────────────┐
Users → Router ────→│  Green (v2)  │  ← Now live
                    └──────────────┘
```

### Implementation Steps

1. Deploy new version to green environment
2. Run automated smoke tests against green
3. Optionally, route internal/test traffic to green for manual verification
4. Switch the router (load balancer, DNS, or service mesh) to green
5. Monitor for errors -- if problems arise, switch back to blue immediately
6. Keep blue running as the rollback target until the next deployment

### Advantages and Limitations

| Advantage | Limitation |
|-----------|-----------|
| Instant rollback (switch router back) | Requires double the infrastructure |
| Full testing in production-like environment | Database changes must be compatible with both versions |
| Zero capacity reduction during deployment | Stateful applications need careful session handling |
| Clear separation of deploy and release | Cost of maintaining two full environments |

---

## Canary Releases

Route a small percentage of production traffic to the new version. Monitor for errors. Gradually increase the percentage if healthy.

### How It Works

```
Phase 1: 5% → canary (v2), 95% → stable (v1)
Phase 2: 25% → canary (v2), 75% → stable (v1)
Phase 3: 50% → canary (v2), 50% → stable (v1)
Phase 4: 100% → canary (v2), 0% → stable (v1)
```

### Canary Evaluation Criteria

At each phase, evaluate before proceeding:

| Metric | Threshold | Action if Exceeded |
|--------|-----------|-------------------|
| **Error rate** | > 1% above baseline | Automatic rollback |
| **p99 latency** | > 2x baseline | Pause and investigate |
| **CPU usage** | > 80% sustained | Pause and investigate |
| **Memory usage** | Growing trend (potential leak) | Rollback |
| **Business metrics** | Conversion rate drops > 5% | Rollback |

### Automated Canary Analysis

Progressive delivery tools can automate canary evaluation:

1. Deploy canary with 5% traffic
2. Collect metrics for evaluation window (10-30 minutes)
3. Compare canary metrics against baseline (stable version) using statistical analysis
4. If pass: increase traffic percentage and repeat
5. If fail: automatic rollback and alert the team

### Canary vs. Blue-Green

| Aspect | Canary | Blue-Green |
|--------|--------|-----------|
| **Risk exposure** | Minimal (small % of traffic) | All-or-nothing switch |
| **Rollback speed** | Instant (route away from canary) | Instant (switch router) |
| **Infrastructure cost** | Minimal extra (small canary fleet) | Double infrastructure |
| **Verification depth** | Real user traffic at scale | Synthetic tests + internal traffic |
| **Complexity** | Higher (traffic splitting, metric comparison) | Lower (router switch) |

---

## Feature Flags

Feature flags (also called feature toggles) decouple deployment from release. Code is deployed but not activated until the flag is enabled.

### Types of Feature Flags

| Type | Lifetime | Purpose | Example |
|------|----------|---------|---------|
| **Release flag** | Days to weeks | Gate incomplete or untested features | `new_checkout_flow` |
| **Experiment flag** | Weeks to months | A/B testing and gradual rollout | `show_recommendations_v2` |
| **Ops flag** | Permanent | Runtime control over system behavior | `enable_expensive_query_cache` |
| **Kill switch** | Permanent | Disable features during incidents | `disable_search_suggestions` |

### Feature Flag Best Practices

**Do:**
- Use a centralized flag management system (not config files or environment variables)
- Set a default value for every flag (what happens if the flag service is down?)
- Clean up release flags after full rollout (flag debt is real technical debt)
- Log flag evaluations for debugging ("User X saw feature Y because flag Z was true")
- Test both flag states in your test suite

**Do not:**
- Use feature flags for long-lived branching (creates combinatorial testing nightmare)
- Nest feature flags (flag A enables feature which checks flag B -- unmaintainable)
- Deploy code that only works with the flag enabled (always support both states)
- Forget to remove old flags (accumulation makes the code unreadable)

### Feature Flag and Deployment Pipeline

```
1. Developer merges code with feature flag (default: off)
2. Code deploys to production (flag off -- no user impact)
3. QA enables flag for internal users and tests
4. Product enables flag for 5% of users (canary)
5. Monitor metrics for 24-48 hours
6. Ramp to 25%, 50%, 100% with monitoring at each stage
7. When 100% and stable, remove the flag and the old code path
```

---

## Database Migrations Without Downtime

Database schema changes are the most dangerous part of deployment because they are difficult to roll back and must be compatible with both old and new application code during the deployment window.

### The Expand-Contract Pattern

Never make a breaking schema change in a single step. Instead, expand (add), migrate data, then contract (remove).

### Example: Renaming a Column

**Wrong (causes downtime):**
```sql
ALTER TABLE users RENAME COLUMN name TO full_name;
-- Old code looking for "name" column fails immediately
```

**Right (zero-downtime expand-contract):**

| Step | Migration | Application Code |
|------|-----------|-----------------|
| 1. Expand | `ALTER TABLE users ADD COLUMN full_name VARCHAR(255);` | Writes to both `name` and `full_name` |
| 2. Backfill | `UPDATE users SET full_name = name WHERE full_name IS NULL;` | Reads from `full_name`, falls back to `name` |
| 3. Switch | No schema change | Reads and writes only `full_name` |
| 4. Contract | `ALTER TABLE users DROP COLUMN name;` | Only uses `full_name` |

Each step is a separate deployment. Each step is individually rollback-safe.

### Example: Adding a NOT NULL Column

**Wrong (locks table, breaks old code):**
```sql
ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'pending';
-- On large tables, this locks the table for minutes/hours
```

**Right (phased approach):**

| Step | Action |
|------|--------|
| 1 | Add column as nullable: `ALTER TABLE orders ADD COLUMN status VARCHAR(20);` |
| 2 | Deploy code that writes `status` on all new rows |
| 3 | Backfill existing rows: `UPDATE orders SET status = 'pending' WHERE status IS NULL;` (in batches) |
| 4 | Add NOT NULL constraint: `ALTER TABLE orders ALTER COLUMN status SET NOT NULL;` |

### Migration Safety Checklist

- [ ] Can the old code work with the new schema?
- [ ] Can the new code work with the old schema (for rollback)?
- [ ] Are large data migrations batched (not one giant UPDATE)?
- [ ] Is the migration tested against production-volume data?
- [ ] Is the migration reversible?
- [ ] Are table locks avoided (no ALTER TABLE on large tables without online DDL)?

---

## Immutable Infrastructure

Never patch, update, or modify a running server. Instead, build a new image with the changes, deploy it, and destroy the old one.

### Why Immutable

| Mutable Infrastructure | Immutable Infrastructure |
|----------------------|-------------------------|
| SSH into servers, apply patches | Build new image with patches baked in |
| Configuration drift over time | Every instance is identical |
| "Snowflake" servers that are irreplaceable | Instances are disposable and replaceable |
| "It works on that server" debugging | Consistent behavior across all instances |
| Manual changes accumulate and are undocumented | All changes are in version control |

### Immutable Infrastructure Pipeline

```
1. Code change committed to version control
2. CI builds application artifact (binary, JAR, bundle)
3. CI builds infrastructure image (Docker image, AMI, VM image)
4. Image is tagged with version and stored in registry
5. Deployment tool replaces old instances with new image
6. Old instances are terminated (not modified, not reused)
```

### Implementation Patterns

| Pattern | Technology | Use Case |
|---------|-----------|----------|
| **Container images** | Docker, OCI | Microservices, cloud-native applications |
| **Machine images** | AMI, GCE image | VM-based workloads |
| **Serverless packages** | Lambda ZIP, Cloud Function | Event-driven workloads |
| **Helm charts** | Kubernetes + Helm | Kubernetes-native applications |

---

## Infrastructure as Code

All infrastructure -- servers, networks, databases, load balancers, DNS entries -- is defined in version-controlled code, not manually configured through web consoles or SSH sessions.

### Principles

| Principle | Practice |
|-----------|----------|
| **Everything in code** | No manual changes; all config in Terraform, CloudFormation, Pulumi, or similar |
| **Version controlled** | Infrastructure code lives in git alongside application code |
| **Reviewed** | Infrastructure changes go through code review like application changes |
| **Tested** | Infrastructure changes are validated in staging before production |
| **Reproducible** | Any environment can be recreated from code in minutes |
| **Idempotent** | Applying the same code twice produces the same result |

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **ClickOps** | Changes made through web console are undocumented and unreproducible | Define all infrastructure in code |
| **SSH and modify** | Manual changes create drift between instances | Use immutable infrastructure |
| **Shared credentials** | No audit trail of who changed what | Individual credentials with role-based access |
| **No staging** | Infrastructure changes tested directly in production | Maintain a staging environment that mirrors production topology |
| **Monolithic templates** | One giant infrastructure file that is impossible to review | Modularize infrastructure into composable components |

---

## Rollback Strategy

Rollback must be faster and simpler than rolling forward. If rolling back takes 30 minutes of manual steps, teams will hesitate to deploy -- and when they do deploy, they will hesitate to roll back when things go wrong.

### Rollback Approaches

| Approach | Speed | Complexity | Limitation |
|----------|-------|-----------|-----------|
| **Traffic switch** (blue-green) | Seconds | Low | Requires both versions running |
| **Revert canary** | Seconds | Low | Only for canary percentage |
| **Redeploy previous version** | Minutes | Medium | Requires previous artifact available |
| **Feature flag disable** | Seconds | Low | Only for flag-gated features |
| **Database rollback** | Minutes to hours | High | May require data migration reversal |

### Rollback Checklist

- [ ] Is the previous version's artifact still available in the registry?
- [ ] Can the previous version work with the current database schema?
- [ ] Are feature flags in a state that supports rollback?
- [ ] Has the rollback procedure been tested (not just documented)?
- [ ] Can rollback be executed by the on-call engineer without escalation?
- [ ] Is the rollback time under 5 minutes?
