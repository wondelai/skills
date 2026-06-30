---
name: lean-ux
description: 'Apply lean thinking to UX: hypothesis-driven design, collaborative sketching, and rapid experiments instead of heavy deliverables. Use when the user mentions "Lean UX", "design hypothesis", "outcome over output", "design studio method", "assumption mapping", "lightweight research", "too much design documentation", or "get the team designing together". Also trigger when reducing design-documentation overhead, getting cross-functional teams to co-design, or running fast usability experiments. Covers hypothesis statements, MVPs for UX, and cross-functional collaboration. For Build-Measure-Learn, see lean-startup. For usability audits, see ux-heuristics.'
license: MIT
metadata:
  author: wondelai
  version: "1.4.0"
---

# Lean UX Framework

A practice-driven approach to UX that replaces heavy deliverables with rapid experimentation, cross-functional collaboration, and continuous learning. Lean UX shifts the question from "What should we design?" to "What do we need to learn?"

## Core Principle

**Outcomes over outputs.** The value of a design is measured not by the fidelity of the deliverable but by the change in user behavior it produces.

**The foundation:** Traditional UX waterfalls requirements into wireframes, mockups, specs, and code—losing context and hiding untested assumptions at every handoff. Lean UX compresses the distance between idea and evidence: declare assumptions, form hypotheses, run the smallest possible experiment, and let real user behavior settle the argument. Shared understanding replaces documentation; learning velocity replaces pixel perfection.

## Scoring

**Goal: 10/10.** Score a UX process, design plan, or team workflow by the eight-row Quick Diagnostic below: award ~1.25 points per row answered "yes" (8 yeses = 10). Bands:

- **9-10** — assumptions declared, hypotheses with pre-committed success criteria, lowest-fidelity experiments, whole-team design, weekly research, outcome (not output) metrics, dual-track agile, and a recently invalidated hypothesis on the books.
- **5-6** — hypotheses exist but criteria are vague or fidelity is over-invested; design and research still partly siloed.
- **<=3** — heavy deliverables, untested assumptions, output-counting, no experiment log.

Always state the current score, the diagnostic rows that failed, and the specific fix for each.

## Framework

### 1. Declaring Assumptions

**Core concept:** Every design starts with assumptions. Lean UX makes them explicit so they can be prioritized and tested, rather than baked invisibly into specifications.

**Why it works:** Unspoken assumptions mean teams build on shaky ground and discover problems only after launch; surfacing them early focuses energy on the riskiest ones and reduces the cost of being wrong.

**Key insights:**
- Business assumptions define what must be true for the business (revenue model, market size, willingness to pay); user assumptions define who users are and how they behave
- Prioritize on two axes: risk (how damaging if wrong) and uncertainty (how little we know)
- Test high-risk, high-uncertainty assumptions first
- Write assumptions collaboratively as a team, not in isolation

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **New feature kick-off** | Assumption mapping workshop | "We assume users want to share reports with teammates" |
| **Roadmap planning** | Rank features by assumption risk | Prioritize features whose success depends on untested beliefs |
| **Stakeholder alignment** | Expose hidden assumptions across roles | PM assumes pricing works; engineer assumes scale; designer assumes flow |

**Ethical boundary:** Assumptions must be honest assessments, not post-hoc justifications—if leadership has already committed to a direction, acknowledge the constraint rather than pretending it's open to falsification.

See [references/hypothesis-canvas.md](references/hypothesis-canvas.md) when running an assumption workshop or writing a hypothesis — the risk/uncertainty prioritization matrix, business-vs-user assumption split, and fillable hypothesis and sub-hypothesis templates.

### 2. Hypothesis Statements

**Core concept:** A hypothesis translates an assumption into a testable prediction, linking a proposed change to a measurable outcome for a specific user segment.

**Why it works:** Hypotheses force precision—instead of "make onboarding better," the team commits to a prediction that can be proven or disproven, which prevents scope creep and makes the learn step unambiguous.

**Key insights:**
- Standard format: "We believe [outcome] will happen if [persona] achieves [action] with [feature]"
- Every hypothesis specifies persona, action, outcome, and measurable signal
- Sub-hypotheses break a large bet into independently testable parts
- Agree on what "validated" and "invalidated" look like before running the experiment

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Feature design** | Write hypothesis before wireframing | "We believe trial-to-paid conversion will rise 10% if new users complete a guided setup wizard" |
| **A/B tests** | Formalize test rationale | "We believe click-through will rise 15% if we move the CTA above the fold" |
| **Sprint planning** | Attach hypothesis to each story | Story: "filter by date." Hypothesis: "task completion time drops 30%" |

**Ethical boundary:** Never cherry-pick metrics after the fact to declare a hypothesis validated—pre-commit to success criteria.

See [references/outcome-metrics.md](references/outcome-metrics.md) when picking the measurable signal for a hypothesis or defining team success — outcomes-vs-outputs, leading-vs-lagging indicator pairs, UX OKRs, and the vanity metrics to avoid.

### 3. MVPs and Experiments

**Core concept:** An MVP in Lean UX is the smallest design artifact that can test a hypothesis with real users—a learning tool, not a product launch.

**Why it works:** A paper prototype tested with five users in a hallway can invalidate a hypothesis that would otherwise consume a full engineering sprint; matching experiment fidelity to assumption risk maximizes learning per unit of effort.

**Key insights:**
- Experiments range from low fidelity (paper prototypes, concierge tests) to high fidelity (coded A/B tests, Wizard of Oz)
- Choose the lowest-fidelity experiment that can answer the question
- A good experiment has a clear hypothesis, defined audience, measurable signal, and time box
- Proto-personas can stand in for full research when speed matters, but must be validated later

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Early concept validation** | Paper prototype or clickable mockup | Sketch 3 concepts, test with 5 users same day |
| **Demand validation** | Landing page smoke test | "Sign up for early access" measures real interest |
| **Usability validation** | Clickable prototype test | Figma prototype tested with 5-8 users |
| **Pricing validation** | Painted door test | Show pricing page, measure click-through before building billing |

**Ethical boundary:** Smoke tests and fake doors must not mislead users into believing a product exists—disclose test status and offer an opt-out.

See [references/experiment-patterns.md](references/experiment-patterns.md) when choosing or designing an experiment — the full catalog of experiment types with when/when-NOT-to-run notes, the experiment selection matrix and fidelity ladder, and a design template.

### 4. Collaborative Design

**Core concept:** Design is a team sport. Lean UX replaces the solitary designer-then-handoff model with cross-functional sessions where developers, PMs, and designers sketch solutions together.

**Why it works:** Developers who helped sketch the solution don't need a 40-page spec to build it—shared understanding replaces documentation, diverse perspectives generate more creative solutions, and handoff waste drops dramatically.

**Key insights:**
- Design Studio method: diverge (individual sketching), present, critique, converge (refined sketch), iterate
- The goal is informed commitment, not consensus: the team agrees on what to test, not what is "right"
- Cross-functional means engineers, QA, data analysts, and stakeholders sketch too
- Style guides and pattern libraries are living documents; reduce deliverables to the minimum needed for shared understanding (often a whiteboard photo)

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Sprint kick-off** | Design Studio session (90 minutes) | Whole team sketches solutions to the sprint's hypothesis |
| **Feature exploration** | Collaborative sketching workshop | 6-up sketches: each person draws 6 ideas in 5 minutes |
| **Remote teams** | Virtual whiteboard sessions | FigJam or Miro board with timed sketch rounds |

**Ethical boundary:** Collaboration must not become design by committee—a designated designer synthesizes input; the team does not vote on pixels.

See [references/collaborative-design.md](references/collaborative-design.md) when facilitating a Design Studio — the step-by-step workshop protocol (timings, materials, remote variants) and how to keep style guides as living documents.

### 5. Feedback and Research

**Core concept:** Continuous, lightweight research replaces big-bang usability studies—small research activities embedded in every sprint instead of quarterly reports.

**Why it works:** Findings only change a decision while it is still cheap to reverse, so research value decays with every sprint between learning and the decision it informs; small weekly studies keep that gap near zero, which a quarterly report never can.

**Key insights:**
- Research types: usability tests, customer interviews, A/B tests, analytics review, surveys, diary studies
- Five users uncover approximately 85% of usability problems (Nielsen)
- Continuous cadence: recruit weekly, test weekly, synthesize weekly
- The whole team should observe at least some sessions to build empathy
- Proto-personas are refined and eventually replaced by evidence-based personas

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Weekly usability testing** | Test prototype with 3-5 users every Thursday | "Testing Thursday" ritual with rotating facilitators |
| **Post-launch learning** | Monitor analytics + 3 follow-up interviews | Find drop-off points, interview churned users |
| **Persona validation** | Compare proto-persona assumptions to interview data | "We assumed power users are marketers; data shows ops managers" |

**Ethical boundary:** Conduct research with informed consent—participants should understand how their data is used and be free to withdraw.

### 6. Integration with Agile

**Core concept:** Lean UX works inside Agile via dual-track development: discovery (learning what to build) and delivery (building it) run in parallel.

**Why it works:** Design work doesn't fit neatly into a delivery sprint; running discovery one sprint ahead means validated designs are ready when the delivery sprint begins, instead of design forever catching up.

**Key insights:**
- The discovery track (research + design) feeds the delivery track (engineering + QA), staggered one sprint ahead
- User stories gain a hypothesis and success metric alongside acceptance criteria
- "Definition of Done" for UX includes validated learning, not just shipped pixels
- Backlog items from invalidated hypotheses are removed, not deferred

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Sprint planning** | Include hypothesis validation in sprint goals | "Sprint goal: validate that inline editing cuts task time 20%" |
| **Backlog refinement** | Attach experiment results to stories | Story moves to delivery only after hypothesis is validated |
| **Retrospectives** | Review learning velocity alongside delivery velocity | "We validated 4 hypotheses and invalidated 2 this sprint" |

**Ethical boundary:** Never use Lean UX as an excuse to skip accessibility, security, or compliance—these are non-negotiable quality standards, not assumptions to test.

See [references/agile-integration.md](references/agile-integration.md) when fitting discovery into a delivery cadence — the staggered dual-track sprint mechanics, how stories carry a hypothesis, and a UX Definition of Done.

See [references/case-studies.md](references/case-studies.md) when you want a worked end-to-end example to model an engagement on — four composite scenarios (enterprise, startup, agency, internal tools) showing assumptions, experiments, and before/after outcome metrics.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **Treating MVPs as launches** | Over-building by conflating MVP with first release | Reframe: MVP = learning tool, not product launch |
| **Skipping assumption declaration** | Hidden assumptions become expensive surprises | Run a 30-minute assumption mapping session at kick-off |
| **Hypothesis without success criteria** | Can't tell if the experiment passed | Pre-commit to metric, threshold, and sample size |
| **Designer-only design** | Handoff waste, misalignment, slow iteration | Run Design Studio sessions with the full team |
| **Research as a phase** | Feedback arrives too late to matter | Embed lightweight research in every sprint |
| **Ignoring invalidated hypotheses** | Building features that failed testing | Remove invalidated items from the backlog; pivot or drop |
| **Documenting instead of collaborating** | 40-page specs nobody reads | Replace specs with shared understanding from co-design |
| **Measuring outputs not outcomes** | Shipping features that don't change behavior | Define success as behavior change, not delivery |

## Quick Diagnostic

Audit any UX process or design plan:

| Question | If No | Action |
|----------|-------|--------|
| Are assumptions explicitly declared? | Hidden assumptions drive decisions | Run an assumption mapping workshop |
| Is there a testable hypothesis? | Building on opinion | Write hypothesis in standard format before designing |
| Is the experiment the lowest fidelity that answers the question? | Over-investing before learning | Downgrade to paper prototype or smoke test |
| Does the whole team participate in design? | Handoff waste and misalignment | Schedule a Design Studio session |
| Is research happening every sprint? | Feedback loop too slow | Establish a weekly testing cadence |
| Are you tracking outcomes, not just outputs? | Shipping without learning | Define behavior-change metrics per feature |
| Does UX work feed into Agile smoothly? | Design bottleneck or sprint-zero trap | Implement dual-track agile with staggered sprints |
| Can you point to a recently invalidated hypothesis? | Not learning; confirmation bias | Review the experiment log and celebrate a pivot |

## Further Reading

For the complete methodology, research, and case studies:

- [*"Lean UX: Designing Great Products with Agile Teams"*](https://www.amazon.com/Lean-UX-Designing-Great-Products/dp/1098116305?tag=wondelai00-20) by Jeff Gothelf & Josh Seiden
- [*"Sense and Respond"*](https://www.amazon.com/Sense-Respond-Successful-Organizations-Continuously/dp/1633691888?tag=wondelai00-20) by Jeff Gothelf & Josh Seiden (scaling outcome-focused thinking across organizations)

## About the Authors

**Jeff Gothelf** is an organizational designer, coach, and author who spent over 15 years leading UX teams at companies including TheLadders and Neo Innovation; watching teams waste months on unvalidated deliverables led him to create Lean UX. **Josh Seiden** is a designer and product strategist with 25+ years of experience who co-founded the interaction design practice at Cooper and was Managing Director at Neo Innovation. Together they co-authored *Lean UX* and *Sense and Respond*.
