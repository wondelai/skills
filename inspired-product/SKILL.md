---
name: inspired-product
description: 'Build empowered product teams using discovery and delivery dual-track. Use when the user mentions "product discovery", "empowered teams", "feature factory", "product roadmap", "opportunity assessment", "product vision", "product-led growth", or "discovery vs delivery". Also trigger when restructuring product teams away from output-driven models, setting product strategy, or defining what to build next based on outcomes. Covers product discovery techniques, team structure, and continuous value delivery. For customer interviews, see mom-test. For ongoing discovery systems, see continuous-discovery.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Empowered Product Teams Framework

Framework for building products customers love by structuring empowered teams that solve hard problems through continuous discovery and delivery. Based on a fundamental truth: the best product companies don't ship features -- they solve problems, and they give their teams the autonomy and accountability to figure out how.

## Core Principle

**Empowered product teams** = cross-functional groups given problems to solve (not features to build) who own discovery and delivery end-to-end.

The root cause of most product failures is not bad engineering or poor design -- it is that teams are building things nobody wants. Feature teams receive roadmaps and execute; empowered teams receive objectives and discover solutions. The difference between a feature factory and an innovation engine is whether teams are missionaries (driven by vision and empathy) or mercenaries (driven by a backlog handed to them).

## Scoring

**Goal: 10/10.** When reviewing or creating product team structures, discovery practices, or delivery processes, rate them 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## Framework

### 1. Product Discovery vs Delivery

**Core concept:** Product work has two distinct tracks running in parallel. Discovery determines what to build (addressing risks before engineering investment). Delivery builds production-quality software at scale. Most organizations conflate these and skip discovery entirely, jumping from idea to backlog to sprint.

**Why it works:** Discovery is cheap and fast; delivery is expensive and slow. By validating ideas through discovery before committing engineering resources, teams avoid the most common failure mode: building something nobody wants. The dual-track approach lets discovery run ahead while delivery ships validated solutions continuously.

**Key insights:**
- Discovery answers four critical risks: value (will customers buy/use it?), usability (can they figure out how to use it?), feasibility (can engineers build it?), viability (does it work for the business?)
- Discovery output is validated ideas backed by evidence, not PRDs or specifications
- A team should be running 10-20 discovery iterations for every feature that reaches delivery
- Most ideas won't work -- the goal of discovery is to fail fast and cheap
- Discovery is not a phase; it runs continuously in parallel with delivery
- Engineers must participate in discovery, not just receive tickets

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| New feature evaluation | Run discovery to validate all four risks before committing | Prototype and test a new onboarding flow with 5 users before building it |
| Roadmap prioritization | Prioritize problems with strongest discovery evidence | Ship the feature with 4/5 successful user tests over the one the CEO requested |
| Sprint planning | Feed delivery backlog from validated discovery output | Only items that passed discovery testing enter the sprint backlog |

**Ethical boundary:** Never cherry-pick discovery evidence to justify a predetermined conclusion. Discovery must be honest inquiry, not confirmation theater.

See: [references/discovery-techniques.md](references/discovery-techniques.md)

### 2. Empowered Product Teams

**Core concept:** An empowered product team is a small, durable, cross-functional group (product manager, product designer, and engineers) given a problem to solve rather than features to build. They own both discovery and delivery and are accountable for outcomes, not output.

**Why it works:** When teams own problems end-to-end, they develop deep domain expertise, customer empathy, and creative solutions that no top-down roadmap can match. Feature teams are mercenaries executing someone else's plan; empowered teams are missionaries who believe in what they are building because they discovered the solution themselves.

**Key insights:**
- The product manager is not a project manager or backlog administrator -- they are responsible for value and viability
- The product designer owns the user experience holistically, not just visual design
- Engineers are not "resources" -- they are the best source of innovation because they know what is technically possible
- Teams should be durable (stable membership) and co-located or highly collaborative
- The product manager must have deep knowledge of customers, data, business, and industry
- Accountability means the team owns outcomes (adoption, retention, revenue) not output (stories shipped)

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Team structure | Organize around outcomes, not components | A "new user activation" team owns the entire first-week experience across all surfaces |
| Hiring | Hire product managers for competence, not credentials | Evaluate PM candidates on customer knowledge, data fluency, and business acumen |
| Performance measurement | Measure team results, not velocity or output | Track activation rate improvement, not number of stories completed per sprint |

**Ethical boundary:** Empowerment requires trust. Never claim to empower teams while overriding their discovery findings with executive mandates. If leadership dictates the solution, the team is not empowered.

See: [references/empowered-teams.md](references/empowered-teams.md)

### 3. Product Discovery Techniques

**Core concept:** Discovery is a systematic set of techniques for rapidly testing ideas against the four risks (value, usability, feasibility, viability). The core techniques include opportunity assessment, customer interviews, prototyping, and user testing -- all designed to produce evidence quickly and cheaply.

**Why it works:** Ideas are assumptions. Without rapid testing, teams invest months building on untested assumptions and discover failure only after launch. Discovery techniques are designed to compress learning cycles from months to days, using prototypes, experiments, and direct customer contact.

**Key insights:**
- Prototypes are the primary discovery tool: high-fidelity for usability testing, live-data for feasibility testing, Wizard of Oz for value testing
- Test with real target users, not colleagues or friends
- Qualitative testing (5 users) reveals usability and value problems; quantitative testing validates at scale
- Customer interviews should focus on behavior (what they did) not opinion (what they say they want)
- Data analysis reveals patterns but not causes -- combine with qualitative discovery
- Feasibility spikes let engineers explore technical risk without full implementation

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Early-stage idea | Run an opportunity assessment before any design work | Answer: who is it for, what problem does it solve, how will we measure success? |
| Usability validation | High-fidelity prototype tested with 5 target users | Clickable Figma prototype that looks real enough to test task completion |
| Value validation | Fake door test or Wizard of Oz prototype | Add a button for an unbuilt feature and measure click-through to gauge demand |
| Feasibility validation | Engineering spike to assess technical risk | Two-day investigation to determine if real-time sync is achievable with current infrastructure |

**Ethical boundary:** Never deceive users in discovery testing beyond what is necessary for valid results. Wizard of Oz prototypes are acceptable; collecting payment for non-existent products is not.

See: [references/discovery-techniques.md](references/discovery-techniques.md)

### 4. Opportunity Assessment

**Core concept:** Before investing in any product opportunity, evaluate it against a structured set of questions that assess business value, customer need severity, market context, and organizational readiness. The opportunity assessment prevents teams from chasing low-impact work.

**Why it works:** Most product organizations have far more ideas than capacity. Without rigorous assessment, teams default to building what the loudest stakeholder requests or what competitors have. The opportunity assessment creates a shared framework for evaluating and comparing opportunities objectively.

**Key insights:**
- The key questions: What business objective does this serve? Who is the target customer? What problem are we solving? How will we know if we succeeded? What alternatives exist?
- Severity of the customer problem matters more than the elegance of the solution
- Market timing is critical -- too early is as dangerous as too late
- Assess organizational readiness: does the team have the skills, technology, and go-to-market capability?
- A strong opportunity assessment kills bad ideas early and focuses resources on high-impact work
- Share opportunity assessments broadly to build alignment before committing resources

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Quarterly planning | Evaluate all candidate opportunities against consistent criteria | Score each opportunity on customer severity, business impact, and feasibility |
| Stakeholder requests | Respond with structured assessment, not reflexive commitment | "Let me assess this opportunity and share findings before we commit engineering" |
| Resource allocation | Direct capacity toward highest-assessed opportunities | Fund the opportunity with severe customer pain and clear business alignment over the nice-to-have |

See: [references/opportunity-assessment.md](references/opportunity-assessment.md)

### 5. Product Vision and Strategy

**Core concept:** Product vision describes the future the team is working toward (2-5 years out). Product strategy is the sequence of target markets, problems, and solutions that will realize the vision. Together, they provide the context that enables empowered teams to make good autonomous decisions.

**Why it works:** Without a compelling vision, teams lack purpose and make disconnected decisions. Without a clear strategy, teams chase too many opportunities at once and achieve none. Vision inspires; strategy focuses. When teams understand both, they can self-organize around the right problems without constant top-down direction.

**Key insights:**
- Vision should be inspiring and customer-centric, describing the world you want to create -- not a list of features
- Strategy sequences the hard choices: which customers first, which problems first, which solutions first
- Product principles are the guardrails that guide decision-making when the strategy doesn't specify an answer
- OKRs translate strategy into measurable team objectives -- outcomes, not output
- Outcome-based roadmaps communicate intent without prescribing solutions
- Revisit vision annually and strategy quarterly; principles change rarely

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Company alignment | Use vision to align all teams toward a shared future | "Every small business can access world-class financial tools" inspires without prescribing features |
| Team autonomy | Use strategy to scope what each team should focus on | "This quarter: reduce churn in mid-market segment by addressing top 3 pain points" |
| Decision-making | Use principles to resolve tradeoffs | "When in doubt, choose simplicity over power" resolves feature scope debates |

**Ethical boundary:** Never present a product vision that you know is unachievable to motivate teams or attract investment. Vision should be ambitious but honest.

See: [references/product-vision.md](references/product-vision.md)

### 6. Continuous Value Delivery

**Core concept:** Delivery is not a one-time launch event but a continuous process of shipping small, validated increments of value. The goal is to get working software in front of real users as frequently as possible to learn and iterate based on actual behavior.

**Why it works:** Large, infrequent releases accumulate risk, delay learning, and create coordination nightmares. Continuous delivery enables rapid iteration: ship a validated increment, measure its impact, learn from real usage, and adjust. The feedback loop between delivery and discovery creates a learning engine that compounds over time.

**Key insights:**
- Ship small and often; every release is a learning opportunity
- Instrumentation is not optional -- if you cannot measure it, you cannot learn from it
- Feature flags enable decoupling deployment from release, allowing controlled rollouts and quick rollbacks
- Minimum viable product (MVP) is the smallest release that tests a hypothesis, not a half-built product
- Delivery velocity enables discovery velocity -- slow delivery means slow learning
- Technical debt is a strategic choice; manage it like financial debt with conscious tradeoffs

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Release planning | Break large features into independently shippable increments | Release basic search first, then add filters, then add saved searches -- each delivering value |
| Risk management | Use feature flags for controlled rollout | Ship to 5% of users, measure impact, then expand or roll back based on data |
| Learning loops | Instrument every release to feed back into discovery | If search usage is lower than expected, trigger a discovery investigation into why |

**Ethical boundary:** Never ship untested changes to users without the ability to roll back. Continuous delivery requires continuous responsibility for the user experience.

See: [references/case-studies.md](references/case-studies.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Treating product managers as project managers | Teams become order-takers with no ownership of value or viability | Hire PMs for customer knowledge, data fluency, and business acumen; hold them accountable for outcomes |
| Skipping discovery and going straight to delivery | Teams build features nobody wants, wasting months of engineering effort | Require validated evidence (prototype tests, data analysis) before any idea enters the delivery backlog |
| Measuring output (velocity, stories shipped) instead of outcomes | Teams optimize for shipping speed rather than customer value | Define success metrics around business and customer outcomes: adoption, retention, revenue impact |
| Handing teams solutions instead of problems | Teams become feature factories with no motivation or creativity | Assign objectives and key results, not feature lists; let teams discover the best solution |
| Isolating engineers from customers | The best source of innovation never encounters the actual problem | Include engineers in customer visits, discovery sessions, and prototype testing |
| Creating a product roadmap of promised features with dates | Commitments calcify before discovery can validate; stakeholders expect delivery regardless of evidence | Use outcome-based roadmaps that communicate problems to solve, not features to build |
| Running discovery as a one-time phase before "execution" | Learning stops once building starts; teams cannot adapt to new evidence | Run discovery continuously in parallel with delivery; never stop learning |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can your PM articulate the top 3 customer problems from direct observation? | PM lacks customer knowledge | Schedule weekly customer interactions: interviews, support shadowing, user testing |
| Does your team test ideas with real users before building? | You are skipping discovery | Implement prototype testing with 5 target users for every significant idea |
| Are engineers involved in discovery, not just delivery? | You are underutilizing your best innovators | Invite engineers to customer interviews and prototype sessions |
| Does your team own outcomes (metrics) rather than output (features)? | You have a feature factory | Replace feature roadmaps with OKRs tied to business and customer outcomes |
| Can team members explain the product vision and strategy? | Teams lack context for autonomous decisions | Create and evangelize a compelling vision document and quarterly strategy |
| Do stakeholders bring problems, not solutions, to the team? | Leadership is dictating features | Coach stakeholders on the discovery process; pre-sell with opportunity assessments |
| Do you ship validated increments at least every two weeks? | Delivery is too slow for effective learning | Break work into smaller increments; invest in CI/CD and feature flags |

## Reference Files

- [discovery-techniques.md](references/discovery-techniques.md): Opportunity discovery, solution discovery, prototyping techniques, user testing, and the four risks framework
- [empowered-teams.md](references/empowered-teams.md): Product team structure, roles, missionary vs mercenary teams, coaching, and accountability
- [opportunity-assessment.md](references/opportunity-assessment.md): Evaluating product opportunities, business alignment, market assessment, and prioritization
- [product-vision.md](references/product-vision.md): Creating product vision, strategy, principles, OKRs, and outcome-based roadmaps
- [stakeholder-management.md](references/stakeholder-management.md): Managing stakeholders, evangelism, getting buy-in, dealing with HiPPOs, and building executive trust
- [case-studies.md](references/case-studies.md): Scenarios showing empowered product team principles applied to different company stages

## Further Reading

This skill is based on the empowered product teams framework developed by Marty Cagan. For the complete methodology, case studies, and deeper insights:

- [*"Inspired: How to Create Tech Products Customers Love"*](https://www.amazon.com/INSPIRED-Create-Tech-Products-Customers/dp/1119387507?tag=wondelai00-20) by Marty Cagan
- [*"Empowered: Ordinary People, Extraordinary Products"*](https://www.amazon.com/EMPOWERED-Ordinary-People-Extraordinary-Products/dp/111969129X?tag=wondelai00-20) by Marty Cagan and Chris Jones

## About the Author

**Marty Cagan** is the founder of the Silicon Valley Product Group (SVPG) and one of the most influential voices in modern product management. Before founding SVPG, Cagan served as VP of Product at eBay, where he led the product team during the company's rapid growth. He held senior product and technology roles at Hewlett-Packard, Netscape Communications, and America Online. Cagan has spent decades studying what separates the best product companies -- including Google, Amazon, Apple, and Netflix -- from the rest. His book *Inspired* (first edition 2008, second edition 2017) became the definitive guide to modern product management and is required reading at product organizations worldwide. His follow-up, *Empowered* (2020), extends the framework to address the organizational and leadership changes required to build truly empowered product teams. Through SVPG, Cagan coaches product leaders and teams at companies ranging from startups to Fortune 500 enterprises, advocating for the empowered team model over the feature-factory approach that dominates most organizations.
