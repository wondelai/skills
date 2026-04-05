---
name: continuous-discovery
description: 'Build a weekly cadence of customer touchpoints using Opportunity Solution Trees, assumption mapping, and interview snapshots. Use when the user mentions "continuous discovery", "opportunity solution tree", "weekly interviews", "assumption testing", "discovery habits", "product trio", or "outcome-based roadmap". Also trigger when setting up regular customer feedback loops, prioritizing which experiments to run, or connecting discovery insights to delivery work. Covers experience mapping, co-creation, and prioritizing opportunities. For interview technique, see mom-test. For team structure, see inspired-product.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Continuous Discovery Habits Framework

Framework for building a sustainable, weekly practice of customer discovery that keeps product teams making progress toward desired outcomes. Rather than treating discovery as a phase that happens before development, this framework embeds customer learning into the ongoing rhythm of product work so that every decision is informed by fresh evidence.

## Core Principle

**Good product discovery requires a continuous cadence, not a one-time event.** Teams that talk to customers every week, map opportunities visually, and test assumptions before building consistently outperform teams that rely on intuition, stakeholder opinions, or quarterly research cycles. The goal is at least one customer touchpoint per week, every week, by the product trio (product manager, designer, engineer).

## Scoring

**Goal: 10/10.** When reviewing or creating a product discovery practice, rate it 0-10 based on adherence to the principles below. A 10/10 means the team has a weekly interview cadence, maintains a living Opportunity Solution Tree, systematically tests assumptions, and uses evidence to decide what to build. Lower scores indicate gaps in cadence, structure, or rigor. Always provide the current score and specific improvements needed to reach 10/10.

## Framework

### 1. Opportunity Solution Trees

**Core concept:** An Opportunity Solution Tree (OST) is a visual map that connects a desired outcome at the top to customer opportunities in the middle and potential solutions at the bottom. It makes implicit product thinking explicit and shared.

**Why it works:** Most teams jump from a business outcome straight to solutions, skipping the customer need entirely. The OST forces teams to first understand the opportunity space -- the unmet needs, pain points, and desires customers have -- before generating solutions. This prevents building features nobody wants.

**Key insights:**
- The tree has four layers: Outcome > Opportunities > Solutions > Experiments
- Opportunities are customer needs, pain points, or desires -- framed from the customer's perspective
- A single outcome typically has many opportunities; a single opportunity can have many solutions
- The tree is a living artifact -- updated weekly as the team learns
- Breaking large opportunities into smaller sub-opportunities makes them actionable
- Teams should pursue multiple opportunities simultaneously, not bet everything on one

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Quarterly planning | Define the outcome, then map the opportunity space before committing to features | "Increase trial-to-paid conversion" as outcome, then discover why users don't convert |
| Feature prioritization | Compare solutions across different opportunities to find highest-leverage bets | Three solutions for "users can't find relevant content" vs. two for "onboarding is confusing" |
| Stakeholder alignment | Use the tree as a shared visual to align on strategy and tradeoffs | Walk leadership through the tree to show why you chose opportunity X over Y |

**Ethical boundary:** Never cherry-pick opportunities to justify a predetermined solution. The tree must reflect genuine customer needs discovered through research.

See: [references/opportunity-trees.md](references/opportunity-trees.md)

### 2. Experience Mapping

**Core concept:** Current-state experience maps capture how customers accomplish a goal today, step by step, revealing pain points and unmet needs that become opportunities on the tree.

**Why it works:** Teams often assume they understand the customer's current experience, but mapping it collaboratively from interview data reveals gaps, workarounds, and emotions that are invisible from the inside. The map generates opportunities you would never brainstorm from a conference room.

**Key insights:**
- Map the current state, not a future ideal -- you need to understand reality first
- Include actions, thoughts, and feelings at each step
- Build maps collaboratively with the full product trio
- Use interview data as the source, not assumptions
- Journey maps (your product's touchpoints) differ from experience maps (the customer's full experience regardless of your product)
- Pain points and moments of high emotion on the map become opportunities on the OST

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| New problem space | Map the end-to-end experience before designing anything | Map how a small business owner handles invoicing today, from creating to chasing payment |
| Churn analysis | Map the experience of users who churned to find failure points | Discover that users abandon onboarding at step 4 because they need data they don't have handy |
| Cross-functional alignment | Build the map together so engineering, design, and product share one view | Three-hour collaborative session produces a shared reference artifact |

**Ethical boundary:** Experience maps must reflect real customer experiences from interviews, not the team's projection of what they imagine customers feel.

See: [references/experience-mapping.md](references/experience-mapping.md)

### 3. Interview Snapshots

**Core concept:** Story-based interviews capture specific past experiences (not opinions or predictions), and each interview is synthesized into a one-page snapshot that the whole team can quickly absorb and reference.

**Why it works:** Traditional interview methods ask customers what they want -- but customers are poor predictors of their own future behavior. Story-based interviewing grounds insights in real past events, revealing what customers actually did and felt. The snapshot format makes synthesis fast and creates a growing library of customer evidence.

**Key insights:**
- Ask about specific past behavior, not hypothetical futures: "Tell me about the last time you..." not "Would you use a feature that...?"
- Each snapshot captures: the story, key quotes, opportunities identified, and a photo or identifier
- The product trio should interview together so insights aren't lost in translation
- Automate recruitment so interviews happen weekly without heroic effort
- Synthesize across snapshots to find patterns -- single interviews reveal stories, patterns reveal opportunities
- Aim for at least one interview per week; many teams do two or three

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Weekly cadence | Schedule three 30-minute interviews every Thursday | Recruit from existing users via in-app prompt; rotate who leads the conversation |
| Opportunity discovery | Extract customer needs from interview stories and add to the OST | User describes workaround for exporting data -- becomes an opportunity node |
| Team alignment | Share snapshots in a visible location so everyone absorbs the same evidence | Physical wall or digital board where snapshots accumulate and patterns emerge |

**Ethical boundary:** Never lead interview participants toward conclusions. Use open-ended questions about past behavior and let the story reveal what matters.

See: [references/interview-snapshots.md](references/interview-snapshots.md)

### 4. Assumption Testing

**Core concept:** Before building a solution, identify the underlying assumptions that must be true for it to succeed, map them by type and risk, then design small, fast tests to validate or invalidate the riskiest ones first.

**Why it works:** Every solution is built on a stack of assumptions about desirability, viability, feasibility, and usability. Most teams test none of them before building, or they test the easy ones instead of the risky ones. Systematic assumption mapping and testing prevents investing months in solutions built on false premises.

**Key insights:**
- Four assumption types: desirability (do they want it?), viability (can we sustain it?), feasibility (can we build it?), usability (can they use it?)
- Map assumptions on a 2x2: importance (how critical if wrong) vs. evidence (how much we know)
- Test high-importance, low-evidence assumptions first -- these are leap-of-faith assumptions
- Design the smallest possible test that generates evidence: one-question surveys, painted-door tests, prototype tests, data mining
- Set clear success criteria before running the test -- "we'll consider this validated if..."
- One assumption test should take days, not weeks

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Before building | Map assumptions for the top solution candidates and test the riskiest | "Users will share reports with their manager" -- test with a painted-door button before building sharing infrastructure |
| Comparing solutions | Test the riskiest assumption for each candidate to quickly eliminate weak options | Solution A's riskiest assumption fails; Solution B's passes -- pursue B |
| De-risking a roadmap | Work backward from the roadmap to identify untested assumptions hiding in committed features | Q3 feature assumes users want real-time notifications -- no evidence yet |

**Ethical boundary:** Never design assumption tests that deceive participants. Painted-door tests should explain that the feature is coming soon, not simulate functionality that doesn't exist without disclosure.

See: [references/assumption-mapping.md](references/assumption-mapping.md)

### 5. Prioritizing Opportunities

**Core concept:** Use structured methods to compare opportunities against each other rather than evaluating them in isolation. Assess opportunity size, market factors, company factors, and customer factors to find the highest-leverage bets.

**Why it works:** Teams default to prioritizing by loudest stakeholder voice, recency bias (whatever the last customer said), or gut feel. Structured comparison forces explicit tradeoff discussions and surfaces disagreements that would otherwise go unspoken until implementation is underway.

**Key insights:**
- Compare opportunities head-to-head rather than scoring them independently -- relative comparison produces better decisions
- Consider opportunity sizing: how many customers are affected, how often, how severely
- Assess alignment with company strategy and team capabilities
- Factor in what you already know -- opportunities with more supporting evidence are less risky to pursue
- Avoid analysis paralysis: the goal is to make a good-enough decision quickly, then learn fast
- Revisit prioritization as you learn -- new evidence may shift the ranking

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Quarterly planning | Rank the top 5-7 opportunities from the OST to decide team focus | Compare "users struggle to find content" vs. "users can't collaborate in real time" using structured criteria |
| Sprint planning | Choose which opportunity to tackle this iteration based on current evidence | Pick the opportunity where you have the most interview evidence and a testable solution |
| Portfolio decisions | Distribute team effort across opportunities by risk and potential impact | 60% on high-confidence opportunity, 30% on medium, 10% on exploratory |

**Ethical boundary:** Prioritization frameworks should surface real customer needs, not be gamed to justify features that serve business metrics at the expense of user value.

See: [references/prioritization-methods.md](references/prioritization-methods.md)

### 6. Building the Habit

**Core concept:** Continuous discovery only works if it becomes a sustainable weekly habit for the product trio. This requires automating recruitment, creating lightweight rituals, and embedding discovery into the existing workflow rather than treating it as extra work.

**Why it works:** Most teams do a burst of research at the start of a project and then stop. Continuous discovery requires structural support: automated participant recruitment, standing interview slots, shared synthesis artifacts, and team norms that make discovery non-negotiable. The habit compounds -- teams that maintain it for months develop deep customer intuition that transforms every decision.

**Key insights:**
- The product trio (PM, designer, engineer) should participate together -- not just the PM
- Automate recruitment: in-app intercepts, customer advisory panels, or scheduling tools that fill slots automatically
- Block recurring calendar time -- discovery that depends on "finding time" will never happen
- Keep synthesis lightweight: fill in the snapshot immediately after the interview, not days later
- Start small: one interview per week is enough to build the habit; scale from there
- Connect discovery to delivery: insights should flow into the OST and from there into sprint planning

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Team kickoff | Establish the weekly cadence in the first week of a new team or initiative | Set up automated recruitment, block Thursday afternoons, create snapshot template |
| Scaling discovery | Expand from one interview per week to three as the habit solidifies | Add a second slot on Tuesday for churned-user interviews and a Friday slot for prospect interviews |
| Manager support | Leaders protect discovery time and ask for evidence in planning discussions | "What did you learn from interviews this week?" becomes a standing question in 1:1s |

**Ethical boundary:** Respect participant time. Keep interviews to 30 minutes, compensate fairly, and never use discovery interviews as a disguised sales pitch.

See: [references/case-studies.md](references/case-studies.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Treating discovery as a phase before development | Insights go stale; team builds on outdated assumptions | Embed discovery into every week alongside delivery |
| Only the PM talks to customers | Designer and engineer miss context; insights lost in translation | The full product trio interviews together |
| Jumping from outcome to solutions | Skips the opportunity space; team builds features nobody needs | Build an Opportunity Solution Tree to make the opportunity space explicit |
| Asking customers what they want | Customers predict poorly; you get feature requests, not needs | Use story-based interviewing: "Tell me about the last time..." |
| Testing easy assumptions instead of risky ones | False confidence; the fatal assumption goes untested | Map assumptions by importance and evidence; test high-risk first |
| Scoring opportunities in isolation | No tradeoff discussion; everything looks important | Compare opportunities head-to-head with structured criteria |
| Doing a burst of interviews then stopping | No compounding learning; team reverts to guessing | Automate recruitment and block recurring calendar time |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Does the team talk to at least one customer per week? | You're making decisions without fresh evidence | Automate recruitment and block a weekly interview slot |
| Do you have a living Opportunity Solution Tree? | Strategy is implicit and unshared | Build an OST from your current outcome and interview data |
| Does the full trio participate in interviews? | Insights are filtered through one person | Invite designer and engineer to the next interview |
| Are you testing assumptions before building? | You're betting on untested premises | Map assumptions for your next feature and test the riskiest one |
| Can you trace a shipped feature back to a customer opportunity? | Delivery is disconnected from discovery | Connect your backlog items to opportunities on the OST |
| Do you have interview snapshots the whole team can see? | Knowledge is trapped in one person's head | Create a shared snapshot board and fill it after each interview |
| Are you comparing opportunities, not just listing them? | Prioritization is driven by opinion, not evidence | Run a structured comparison exercise on your top 5 opportunities |

## Reference Files

- [opportunity-trees.md](references/opportunity-trees.md): Opportunity Solution Tree structure, how to build and maintain one, mapping opportunities to solutions
- [interview-snapshots.md](references/interview-snapshots.md): Story-based interviewing, snapshot format, synthesis across interviews, automating recruitment
- [assumption-mapping.md](references/assumption-mapping.md): Assumption types, mapping technique, designing tests, leap-of-faith assumptions
- [experience-mapping.md](references/experience-mapping.md): Current-state experience maps, identifying pain points, collaborative mapping exercises
- [prioritization-methods.md](references/prioritization-methods.md): Opportunity scoring, compare-and-contrast, using data, avoiding analysis paralysis
- [case-studies.md](references/case-studies.md): Realistic scenarios showing continuous discovery applied to B2B SaaS, consumer mobile, platform, and growth teams

## Further Reading

This skill is based on the continuous discovery framework developed by Teresa Torres. For the complete methodology, templates, and case studies:

- [*"Continuous Discovery Habits: Discover Products that Create Customer Value and Business Value"*](https://www.amazon.com/Continuous-Discovery-Habits-Discover-Products/dp/1736633309?tag=wondelai00-20) by Teresa Torres

## About the Author

**Teresa Torres** is an internationally acclaimed author, speaker, and coach who helps product teams adopt continuous discovery practices. She has coached hundreds of product teams at companies ranging from early-stage startups to global enterprises including Capital One, Calendly, and Reforge. Torres created the Opportunity Solution Tree as a visual tool for connecting business outcomes to customer opportunities and potential solutions. Her blog, Product Talk, is one of the most widely read resources for product managers, and her coaching programs have trained thousands of product trios worldwide. Before becoming a coach, Torres spent over a decade as a product leader and has been active in the product management community since 2006. *Continuous Discovery Habits* distills her years of coaching into a practical, repeatable framework that any product team can adopt.
