---
name: continuous-discovery
description: 'Build a weekly cadence of customer touchpoints using Opportunity Solution Trees, assumption mapping, and interview snapshots. Use when the user mentions "continuous discovery", "opportunity solution tree", "weekly interviews", "assumption testing", "discovery habits", "product trio", "outcome-based roadmap", "how do I talk to customers regularly", "we keep building things nobody uses", or "connect research to the roadmap". Also trigger when setting up regular customer feedback loops, prioritizing which experiments to run, or tying discovery insights to delivery work. Covers experience mapping, co-creation, and prioritizing opportunities. For interview technique, see mom-test. For team structure, see inspired-product.'
license: MIT
metadata:
  author: wondelai
  version: "1.3.0"
---

# Continuous Discovery Habits Framework

Framework for building a sustainable weekly practice of customer discovery that keeps product teams progressing toward desired outcomes. Discovery is not a phase before development — it is embedded in the ongoing rhythm of product work so every decision is informed by fresh evidence.

## Core Principle

**Good product discovery requires a continuous cadence, not a one-time event.** Teams that talk to customers every week, map opportunities visually, and test assumptions before building consistently outperform teams that rely on intuition, stakeholder opinions, or quarterly research cycles. The benchmark: at least one customer touchpoint per week, every week, by the product trio (product manager, designer, engineer).

## Scoring

**Goal: 10/10.** Rate any discovery practice 0-10: a 10/10 means a weekly interview cadence, a living Opportunity Solution Tree, systematic assumption testing, and evidence-driven build decisions. Report the current score and the specific improvements needed to reach 10/10.

## Framework

### 1. Opportunity Solution Trees

**Core concept:** An Opportunity Solution Tree (OST) visually connects a desired outcome (top) to customer opportunities (middle) to potential solutions and experiments (bottom), making implicit product thinking explicit and shared.

**Why it works:** Most teams jump from business outcome straight to solutions, skipping the customer need entirely; the OST forces understanding of the opportunity space first, preventing features nobody wants.

**Key insights:**
- Four layers: Outcome > Opportunities > Solutions > Experiments
- Opportunities are customer needs, pain points, and desires — framed from the customer's perspective
- The tree is a living artifact, updated weekly as the team learns
- Break large opportunities into smaller sub-opportunities to make them actionable
- Pursue multiple opportunities simultaneously — don't bet everything on one

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Quarterly planning | Map the opportunity space before committing to features | "Increase trial-to-paid conversion" → discover why users don't convert |
| Feature prioritization | Compare solutions across opportunities for the highest-leverage bet | Three solutions for "can't find content" vs. two for "confusing onboarding" |
| Stakeholder alignment | Use the tree as the shared strategy visual | Walk leadership through why you chose opportunity X over Y |

**Ethical boundary:** Never cherry-pick opportunities to justify a predetermined solution — the tree must reflect needs discovered through research.

See: [references/opportunity-trees.md](references/opportunity-trees.md)

### 2. Experience Mapping

**Core concept:** Current-state experience maps capture how customers accomplish a goal today, step by step, revealing pain points that become opportunities on the tree.

**Why it works:** Teams assume they understand the customer's current experience; mapping it from interview data exposes gaps, workarounds, and emotions invisible from inside the building.

**Key insights:**
- Map the current state, not a future ideal — understand reality first
- Include actions, thoughts, and feelings at each step
- Build collaboratively with the full trio, sourced from interview data, not assumptions
- Experience maps cover the customer's full experience; journey maps cover only your product's touchpoints
- Pain points and high-emotion moments become OST opportunities

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| New problem space | Map end-to-end before designing | How a small business owner handles invoicing, from creation to chasing payment |
| Churn analysis | Map churned users' experience to find failure points | Users abandon onboarding at step 4 — they lack data they need on hand |
| Cross-functional alignment | Build the map together | A three-hour collaborative session produces one shared reference artifact |

**Ethical boundary:** Maps must reflect real customer experiences from interviews, not the team's projection of what customers feel.

See: [references/experience-mapping.md](references/experience-mapping.md)

### 3. Interview Snapshots

**Core concept:** Story-based interviews capture specific past experiences (not opinions or predictions), and each interview is synthesized into a one-page snapshot the whole team can absorb and reference.

**Why it works:** Customers are poor predictors of their own future behavior; grounding insights in real past events reveals what they actually did and felt, and snapshots turn each interview into a growing library of evidence.

**Key insights:**
- Ask about specific past behavior: "Tell me about the last time you..." not "Would you use...?"
- Each snapshot captures the story, key quotes, opportunities identified, and an identifier
- The trio interviews together so insights aren't lost in translation
- Automate recruitment so interviews happen weekly without heroic effort
- Patterns across snapshots reveal opportunities; single interviews only reveal stories

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Weekly cadence | Standing 30-minute interview slots | Recruit via in-app prompt; rotate who leads |
| Opportunity discovery | Extract needs from stories onto the OST | A data-export workaround becomes an opportunity node |
| Team alignment | Share snapshots visibly | A board where snapshots accumulate and patterns emerge |

**Ethical boundary:** Never lead participants toward conclusions — ask open-ended questions about past behavior and let the story reveal what matters.

See: [references/interview-snapshots.md](references/interview-snapshots.md)

### 4. Assumption Testing

**Core concept:** Before building, identify the assumptions a solution depends on, map them by importance and evidence, then run small fast tests on the riskiest ones first.

**Why it works:** Every solution sits on a stack of desirability, viability, feasibility, and usability assumptions; most teams test none — or only the easy ones — and invest months in solutions built on false premises.

**Key insights:**
- Four assumption types: desirability (do they want it?), viability (can we sustain it?), feasibility (can we build it?), usability (can they use it?)
- Map on a 2x2: importance vs. evidence; high-importance, low-evidence = leap-of-faith assumptions to test first
- Design the smallest test that generates evidence: one-question surveys, painted-door tests, prototypes, data mining
- Set success criteria before running the test: "validated if..."
- One assumption test should take days, not weeks

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Before building | Test the riskiest assumption of the top candidates | "Users will share reports with their manager" → painted-door button before building sharing |
| Comparing solutions | Test each candidate's riskiest assumption to eliminate weak options fast | A's riskiest assumption fails, B's passes → pursue B |
| De-risking a roadmap | Find untested assumptions hiding in committed features | Q3 feature assumes users want real-time notifications — no evidence yet |

**Ethical boundary:** Never deceive participants — painted-door tests should say the feature is coming soon, not fake functionality without disclosure.

See: [references/assumption-mapping.md](references/assumption-mapping.md)

### 5. Prioritizing Opportunities

**Core concept:** Compare opportunities against each other — not in isolation — using opportunity size, market, company, and customer factors to find the highest-leverage bets.

**Why it works:** Teams default to the loudest stakeholder, recency bias, or gut feel; structured head-to-head comparison forces explicit tradeoff discussions and surfaces disagreements before implementation.

**Key insights:**
- Relative comparison beats independent scoring
- Size opportunities by how many customers are affected, how often, how severely
- Weigh strategy alignment, team capability, and existing evidence
- Make a good-enough decision quickly, then learn fast — avoid analysis paralysis
- Revisit the ranking as new evidence arrives

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Quarterly planning | Rank the top 5-7 OST opportunities | "Can't find content" vs. "no real-time collaboration" via structured criteria |
| Sprint planning | Pick the opportunity with the strongest current evidence | Choose where you have the most interview data and a testable solution |
| Portfolio decisions | Spread effort by risk and impact | 60% high-confidence, 30% medium, 10% exploratory |

**Ethical boundary:** Prioritization should surface real customer needs, not be gamed to justify features that serve business metrics at users' expense.

See: [references/prioritization-methods.md](references/prioritization-methods.md)

### 6. Building the Habit

**Core concept:** Continuous discovery only works as a sustainable weekly habit for the trio — automate recruitment, create lightweight rituals, and embed discovery into the existing workflow rather than treating it as extra work.

**Why it works:** Most teams do a research burst and stop; structural support (automated recruitment, standing slots, shared artifacts) makes the habit compound into deep customer intuition that transforms every decision.

**Key insights:**
- The whole trio participates — not just the PM
- Automate recruitment: in-app intercepts, advisory panels, scheduling tools that fill slots
- Block recurring calendar time — discovery that depends on "finding time" never happens
- Fill in the snapshot immediately after the interview, not days later
- Start with one interview per week; connect insights to the OST and from there into sprint planning

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Team kickoff | Establish cadence in week one | Automated recruitment, blocked Thursday slot, snapshot template |
| Scaling discovery | Grow from one to three interviews weekly | Add a churned-user slot and a prospect slot |
| Manager support | Leaders protect time and ask for evidence | "What did you learn from interviews this week?" in every 1:1 |

**Ethical boundary:** Respect participant time — keep interviews to 30 minutes, compensate fairly, and never disguise a sales pitch as discovery.

See: [references/case-studies.md](references/case-studies.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Discovery as a phase before development | Insights go stale; team builds on old assumptions | Embed discovery into every week alongside delivery |
| Only the PM talks to customers | Designer and engineer lose context in translation | The full trio interviews together |
| Jumping from outcome to solutions | Skips the opportunity space | Build an OST to make it explicit |
| Asking customers what they want | You get feature requests, not needs | Story-based interviewing: "Tell me about the last time..." |
| Testing easy assumptions, not risky ones | False confidence; the fatal assumption goes untested | Map by importance and evidence; test high-risk first |
| Scoring opportunities in isolation | Everything looks important | Compare head-to-head with structured criteria |
| Interview burst, then stopping | No compounding learning | Automate recruitment; block recurring time |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| One customer conversation per week minimum? | Decisions lack fresh evidence | Automate recruitment; block a weekly slot |
| A living Opportunity Solution Tree? | Strategy is implicit and unshared | Build an OST from your outcome and interview data |
| Full trio in interviews? | Insights filtered through one person | Invite the designer and engineer to the next one |
| Testing assumptions before building? | Betting on untested premises | Map your next feature's assumptions; test the riskiest |
| Can you trace a shipped feature to a customer opportunity? | Delivery disconnected from discovery | Link backlog items to OST opportunities |
| Interview snapshots visible to the whole team? | Knowledge trapped in one head | Shared snapshot board, filled after each interview |
| Comparing opportunities, not just listing them? | Prioritization by opinion | Run a structured comparison on your top 5 |

## Reference Files

- [opportunity-trees.md](references/opportunity-trees.md): OST structure, how to build and maintain one, mapping opportunities to solutions
- [interview-snapshots.md](references/interview-snapshots.md): Story-based interviewing, snapshot format, synthesis, automating recruitment
- [assumption-mapping.md](references/assumption-mapping.md): Assumption types, mapping technique, designing tests, leap-of-faith assumptions
- [experience-mapping.md](references/experience-mapping.md): Current-state maps, identifying pain points, collaborative mapping exercises
- [prioritization-methods.md](references/prioritization-methods.md): Opportunity scoring, compare-and-contrast, using data, avoiding analysis paralysis
- [case-studies.md](references/case-studies.md): Continuous discovery applied to B2B SaaS, consumer mobile, platform, and growth teams

## Further Reading

Based on the continuous discovery framework developed by Teresa Torres:

- [*"Continuous Discovery Habits: Discover Products that Create Customer Value and Business Value"*](https://www.amazon.com/Continuous-Discovery-Habits-Discover-Products/dp/1736633309?tag=wondelai00-20) by Teresa Torres

## About the Author

**Teresa Torres** is an author, speaker, and coach who has helped hundreds of product teams — from startups to Capital One and Calendly — adopt continuous discovery. She created the Opportunity Solution Tree, writes the widely read Product Talk blog, and distilled her coaching practice into *Continuous Discovery Habits*.
