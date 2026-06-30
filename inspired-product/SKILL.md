---
name: inspired-product
description: 'Build empowered product teams using discovery and delivery dual-track. Use when the user mentions "product discovery", "empowered teams", "feature factory", "opportunity assessment", "product vision", "product strategy", "what should we build", or "our roadmap is just a feature list". Also trigger when restructuring teams away from output-driven models, or deciding what to build next based on outcomes. Covers discovery techniques, team structure, opportunity assessment, vision/strategy, and continuous delivery. For customer interviews, see mom-test. For ongoing discovery systems, see continuous-discovery.'
license: MIT
metadata:
  author: wondelai
  version: "1.4.0"
---

# Empowered Product Teams Framework

Framework for building products customers love through empowered teams that own continuous discovery and delivery. The best product companies don't ship features -- they solve problems, and they give teams the autonomy and accountability to figure out how.

## Core Principle

**Empowered product teams** = cross-functional groups given problems to solve (not features to build) who own discovery and delivery end-to-end.

Most product failures come not from bad engineering or design but from building things nobody wants. Feature teams receive roadmaps and execute; empowered teams receive objectives and discover solutions. The difference between a feature factory and an innovation engine is whether teams are missionaries (driven by vision and empathy) or mercenaries (driven by a handed-down backlog).

## Scoring

**Goal: 7/7.** Score product team structures, discovery practices, or delivery processes by the Quick Diagnostic below -- **1 point per satisfied row**, scored 0-7. Bands: **6-7** = empowered teams own outcomes and discovery runs continuously with engineers; **4-5** = discovery happens but inconsistently, or teams own output with partial outcome accountability; **<=3** = a feature factory: teams receive a roadmap of dated features and skip discovery. Always state the current score and the specific failed diagnostic rows to fix to reach 7/7.

## Framework

### 1. Product Discovery vs Delivery

**Core concept:** Product work runs on two parallel tracks: discovery determines what to build by addressing risks before engineering investment; delivery builds production-quality software. Most organizations skip discovery entirely, jumping from idea to backlog to sprint.

**Why it works:** Discovery is cheap and fast; delivery is expensive and slow. Validating ideas before committing engineering avoids the most common failure mode: building something nobody wants.

**Key insights:**
- Discovery answers four risks: value (will customers use it?), usability (can they figure it out?), feasibility (can we build it?), viability (does it work for the business?)
- Discovery output is validated ideas backed by evidence, not PRDs or specifications
- Run 10-20 discovery iterations per feature that reaches delivery -- most ideas won't work, so fail fast and cheap
- Discovery is not a phase; it runs continuously alongside delivery, with engineers participating

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| New feature | Validate all four risks before committing | Prototype-test onboarding flow with 5 users before building |
| Roadmap prioritization | Prioritize strongest discovery evidence | Ship the feature with 4/5 successful user tests, not the CEO's request |
| Sprint planning | Feed backlog from validated discovery output | Only discovery-tested items enter the sprint |

**Ethical boundary:** Never cherry-pick discovery evidence to justify a conclusion you already chose; report the tests that failed alongside the ones that passed.

See [references/discovery-techniques.md](references/discovery-techniques.md) when planning a discovery cycle -- the four-risks framework, a 5-stage interview script, prototyping techniques, and concrete evidence thresholds for "validated".

### 2. Empowered Product Teams

**Core concept:** A small, durable, cross-functional group (product manager, product designer, engineers) given a problem to solve, owning discovery and delivery, accountable for outcomes rather than output.

**Why it works:** The people closest to the customer and the technology find better solutions than a remote roadmap author -- and a team that discovered the solution itself defends and refines it under pressure, where a team handed a spec ships it and moves on.

**Key insights:**
- The PM is not a project manager or backlog administrator -- they own value and viability and need deep knowledge of customers, data, business, and industry
- The product designer owns the user experience holistically, not just visual design
- Engineers are the best source of innovation because they know what is technically possible
- Keep teams durable (stable membership) and highly collaborative
- Accountability means outcomes (adoption, retention, revenue), not output (stories shipped)

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Team structure | Organize around outcomes, not components | "New user activation" team owns the whole first-week experience |
| Hiring | Hire PMs for competence, not credentials | Evaluate customer knowledge, data fluency, business acumen |
| Performance | Measure results, not velocity | Track activation-rate improvement, not stories per sprint |

**Ethical boundary:** Never claim to empower teams while overriding their discovery findings with executive mandates -- if leadership dictates the solution, the team is not empowered.

See [references/empowered-teams.md](references/empowered-teams.md) when staffing or diagnosing a team -- role-by-role competence breakdowns with red flags, missionary vs mercenary dynamics, coaching, and a feature-factory-to-empowered transformation table.

### 3. Product Discovery Techniques

**Core concept:** Systematically test ideas against the four risks using opportunity assessment, customer interviews, prototyping, and user testing -- producing evidence quickly and cheaply.

**Why it works:** Ideas are assumptions; without rapid testing, teams build for months on untested assumptions and discover failure only after launch. Discovery techniques compress learning cycles from months to days.

**Key insights:**
- Prototypes are the primary tool: high-fidelity for usability, live-data for feasibility, Wizard of Oz for value
- Test with real target users, not colleagues; qualitative testing (5 users) reveals problems, quantitative validates at scale
- Interview for behavior (what they did), not opinion (what they say they want)
- Data reveals patterns but not causes -- pair it with qualitative discovery
- Feasibility spikes let engineers explore technical risk without full implementation

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Early idea | Opportunity assessment before design work | Who is it for, what problem, how will we measure success? |
| Usability | High-fidelity prototype with 5 target users | Clickable Figma prototype testing task completion |
| Value | Fake door or Wizard of Oz test | Button for unbuilt feature, measure click-through |
| Feasibility | Engineering spike | Two-day investigation of real-time sync risk |

**Ethical boundary:** Never deceive users beyond what valid results require -- Wizard of Oz prototypes are acceptable; collecting payment for non-existent products is not.

### 4. Opportunity Assessment

**Core concept:** Before investing in any opportunity, evaluate business value, customer need severity, market context, and organizational readiness against a structured set of questions.

**Why it works:** Organizations have far more ideas than capacity; without rigorous assessment, teams default to the loudest stakeholder or competitor parity. A shared framework kills bad ideas early and focuses resources on high-impact work.

**Key insights:**
- Key questions: What business objective does this serve? Who is the target customer? What problem? How will we know we succeeded? What alternatives exist?
- Severity of the customer problem matters more than elegance of the solution
- Market timing is critical -- too early is as dangerous as too late
- Check organizational readiness: skills, technology, go-to-market capability
- Share assessments broadly to build alignment before committing resources

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Quarterly planning | Score all candidates on consistent criteria | Customer severity, business impact, feasibility per opportunity |
| Stakeholder requests | Respond with assessment, not commitment | "Let me assess this and share findings before we commit engineering" |
| Resource allocation | Fund highest-assessed opportunities | Severe pain + clear business alignment beats the nice-to-have |

See [references/opportunity-assessment.md](references/opportunity-assessment.md) when sizing a new opportunity before design work -- the full evaluation-question set, market-timing assessment, and prioritization scoring.

See [references/stakeholder-management.md](references/stakeholder-management.md) when an executive or sales stakeholder hands you a solution or a HiPPO is steering the roadmap -- stakeholder mapping, turning a mandate into a problem to assess, evangelism, and building executive trust.

### 5. Product Vision and Strategy

**Core concept:** Vision describes the future you're building toward (2-5 years out); strategy sequences the target markets, problems, and solutions that will realize it. Together they give empowered teams the context to make good autonomous decisions.

**Why it works:** Without vision, teams make disconnected decisions; without strategy, they chase everything and achieve nothing. Vision inspires; strategy focuses.

**Key insights:**
- Vision is inspiring and customer-centric -- the world you want to create, not a feature list
- Strategy sequences the hard choices: which customers first, which problems first, which solutions first
- Product principles are guardrails for decisions the strategy doesn't cover
- OKRs translate strategy into measurable team objectives; outcome-based roadmaps communicate intent without prescribing solutions
- Revisit vision annually, strategy quarterly; principles change rarely

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Company alignment | Vision aligns all teams on a shared future | "Every small business can access world-class financial tools" |
| Team autonomy | Strategy scopes each team's focus | "This quarter: cut mid-market churn via top 3 pain points" |
| Decision-making | Principles resolve tradeoffs | "When in doubt, choose simplicity over power" |

**Ethical boundary:** Never present a vision you know is unachievable to motivate teams or attract investment.

See [references/product-vision.md](references/product-vision.md) when drafting or revisiting vision and strategy -- how to write each, product principles, translating strategy into OKRs, and building outcome-based roadmaps.

### 6. Continuous Value Delivery

**Core concept:** Delivery is not a launch event but a continuous flow of small, validated increments shipped to real users as frequently as possible.

**Why it works:** Large infrequent releases accumulate risk, delay learning, and create coordination nightmares. The feedback loop between delivery and discovery compounds into a learning engine: ship, measure, learn, adjust.

**Key insights:**
- Ship small and often; every release is a learning opportunity
- Instrumentation is not optional -- if you cannot measure it, you cannot learn from it
- Feature flags decouple deployment from release, enabling controlled rollouts and quick rollbacks
- MVP is the smallest release that tests a hypothesis, not a half-built product
- Manage technical debt like financial debt: conscious tradeoffs

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Release planning | Independently shippable increments | Basic search first, then filters, then saved searches |
| Risk management | Feature flags for controlled rollout | Ship to 5%, measure, expand or roll back |
| Learning loops | Instrument every release to feed discovery | Low search usage triggers a discovery investigation |

**Ethical boundary:** Never ship a change you cannot roll back; gate anything risky behind a flag you can flip off.

See [references/case-studies.md](references/case-studies.md) when you want a worked example before applying the framework -- these principles played out at startup, growth, and enterprise stages.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Treating PMs as project managers | Order-takers with no ownership of value or viability | Hire for customer knowledge, data fluency, business acumen; hold accountable for outcomes |
| Skipping discovery | Months of engineering on features nobody wants | Require validated evidence before ideas enter the delivery backlog |
| Measuring output, not outcomes | Teams optimize shipping speed over customer value | Define success as adoption, retention, revenue impact |
| Handing teams solutions, not problems | Feature factories with no motivation or creativity | Assign objectives and key results; let teams discover solutions |
| Isolating engineers from customers | Best source of innovation never sees the problem | Include engineers in interviews, discovery, prototype testing |
| Roadmaps of promised features with dates | Commitments calcify before discovery can validate | Use outcome-based roadmaps: problems to solve, not features |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can your PM cite the top 3 customer problems from direct observation? | PM lacks customer knowledge | Weekly customer contact: interviews, support shadowing, testing |
| Do you test ideas with real users before building? | Skipping discovery | Prototype-test with 5 target users for every significant idea |
| Are engineers involved in discovery, not just delivery? | Underusing your best innovators | Invite engineers to interviews and prototype sessions |
| Does the team own outcomes (metrics), not output (features)? | Feature factory | Replace feature roadmaps with outcome OKRs |
| Can team members explain the vision and strategy? | No context for autonomous decisions | Create and evangelize a vision doc and quarterly strategy |
| Do stakeholders bring problems, not solutions? | Leadership dictating features | Coach stakeholders on discovery; pre-sell with opportunity assessments |
| Do you ship validated increments at least every two weeks? | Too slow to learn | Smaller increments; invest in CI/CD and feature flags |

## Further Reading

For the complete methodology, case studies, and deeper insights:

- [*"Inspired: How to Create Tech Products Customers Love"*](https://www.amazon.com/INSPIRED-Create-Tech-Products-Customers/dp/1119387507?tag=wondelai00-20) by Marty Cagan
- [*"Empowered: Ordinary People, Extraordinary Products"*](https://www.amazon.com/EMPOWERED-Ordinary-People-Extraordinary-Products/dp/111969129X?tag=wondelai00-20) by Marty Cagan and Chris Jones

## About the Author

**Marty Cagan** is the founder of Silicon Valley Product Group (SVPG) and a former VP of Product at eBay, with senior product roles at HP, Netscape, and AOL. His book *Inspired* (2008; 2nd ed. 2017) became the definitive guide to modern product management, and *Empowered* (2020) extends the framework to product leadership. Through SVPG he coaches product teams from startups to Fortune 500 enterprises.
