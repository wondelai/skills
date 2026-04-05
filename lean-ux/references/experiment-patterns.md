# Experiment Patterns for Lean UX

Experiments are the engine of learning in Lean UX. The right experiment answers the hypothesis with the least effort. Choosing the wrong experiment type wastes time, money, or both. This reference covers the full spectrum of UX experiments, from napkin sketches to coded A/B tests.


## Table of Contents
1. [Types of UX Experiments](#types-of-ux-experiments)
2. [Choosing the Right Experiment](#choosing-the-right-experiment)
3. [Experiment Design Template](#experiment-design-template)
4. [Minimum Viable Tests](#minimum-viable-tests)
5. [Running Experiments in Practice](#running-experiments-in-practice)
6. [Experiment Cheat Sheet](#experiment-cheat-sheet)

---

## Types of UX Experiments

### 1. Paper Prototypes

**What it is:** Hand-drawn screens on paper or index cards. A facilitator plays "computer," swapping screens as the user taps or points.

**Best for:** Early concept validation, flow testing, information architecture.

**Effort:** Very low (30 minutes to create).
**Fidelity:** Very low.
**Confidence:** Low-medium. Validates flow and concept, not visual design or interaction details.

**When to use:**
- You have multiple competing concepts and need to narrow down
- The hypothesis is about flow or content, not aesthetics
- You need to test today, not next week

**When NOT to use:**
- The hypothesis depends on visual design, animation, or micro-interactions
- Users need to interact with real data
- Stakeholders will not trust low-fidelity evidence

**How to run:**
1. Sketch each screen on a separate sheet or card
2. Write a realistic task scenario for the participant
3. Ask the participant to "tap" or point at what they would interact with
4. Swap screens manually based on their choices
5. Note where they hesitate, get confused, or go off-script

### 2. Clickable Prototypes

**What it is:** Interactive mockups built in tools like Figma, Sketch, or InVision. Users click through a realistic-looking interface, but no backend logic exists.

**Best for:** Usability testing, flow validation, stakeholder buy-in, developer communication.

**Effort:** Medium (1-3 days).
**Fidelity:** Medium-high.
**Confidence:** Medium-high. Validates flow, layout, and basic usability.

**When to use:**
- The hypothesis involves user navigation or task completion
- You need to test with users who expect a realistic experience
- The prototype will also serve as a design reference for developers

**When NOT to use:**
- A paper prototype would suffice (over-investing)
- The hypothesis is about performance, load times, or real data behavior
- You need to test with hundreds of users (use coded experiments instead)

**How to run:**
1. Build the key screens and link hotspots in your prototyping tool
2. Write 3-5 task scenarios
3. Recruit 5-8 participants matching your persona
4. Run moderated sessions (20-30 minutes each)
5. Track task completion, time on task, errors, and qualitative feedback

### 3. Concierge MVP

**What it is:** Deliver the service or experience manually, person-to-person, without building any technology. The user receives the full value, but the backend is entirely human-powered.

**Best for:** Validating that the solution genuinely solves the problem before investing in automation.

**Effort:** Medium (ongoing manual work per user).
**Fidelity:** High (the experience is real).
**Confidence:** High. Real behavior with real value delivery.

**When to use:**
- You are unsure whether the solution concept works at all
- The cost of building the automated version is high
- You want to deeply understand the user's experience and edge cases

**When NOT to use:**
- The hypothesis is about scale or technology performance
- You need to test with more than 10-20 users simultaneously
- The value proposition depends on speed that only automation can provide

**Example:** A meal-planning app manually emails personalized weekly meal plans and shopping lists to 10 users based on their dietary preferences, before building the algorithm.

### 4. Wizard of Oz

**What it is:** The user interacts with what appears to be a functioning product, but a human behind the scenes is performing the work the technology would eventually do.

**Best for:** Testing the user experience of an automated feature before building the automation.

**Effort:** Medium (build the frontend; humans operate the backend).
**Fidelity:** High from the user's perspective.
**Confidence:** High. Users interact with what feels like a real product.

**When to use:**
- The hypothesis depends on the user experience of an AI, algorithm, or automation feature
- Building the actual technology is expensive or risky
- You want to learn what the "right" output looks like before training a model

**When NOT to use:**
- The hypothesis is about system performance or response time
- Manual operation cannot replicate the technology's speed
- Ethical issues arise from deception (always disclose if legally required)

**Example:** A "smart" scheduling assistant that appears to use AI but is actually a team member reading requests and sending calendar invites manually.

### 5. Landing Page / Smoke Test

**What it is:** A single web page describing a product or feature that does not yet exist, with a call to action (sign up, pre-order, request access). Measures demand by tracking how many people take the action.

**Best for:** Demand validation before building anything.

**Effort:** Low (half a day to create).
**Fidelity:** Low (no product).
**Confidence:** Medium. Measures stated intent, not actual usage.

**When to use:**
- You need to validate demand before committing development resources
- The hypothesis is about whether people want this at all
- You want to build an early-access list for future testing

**When NOT to use:**
- You already know there is demand and need to validate usability
- The product concept is hard to explain without a demo
- Your audience is internal (use interviews instead)

**How to run:**
1. Create a landing page with a clear value proposition, 2-3 key benefits, and a CTA
2. Drive targeted traffic (ads, social media, email, communities)
3. Measure conversion rate (visitors to CTA clicks or sign-ups)
4. Set success threshold before launch (e.g., 5% sign-up rate from 500 visitors)
5. Follow up with sign-ups for qualitative interviews

### 6. A/B Test (Coded Experiment)

**What it is:** Two or more versions of a live feature are shown to different user segments. Statistical analysis determines which version performs better on a target metric.

**Best for:** Optimizing existing features, validating specific design changes with statistical rigor.

**Effort:** High (requires code, traffic, and statistical analysis).
**Fidelity:** Production-level.
**Confidence:** Very high (if properly powered).

**When to use:**
- You have sufficient traffic to reach statistical significance
- The hypothesis involves a measurable behavior change in an existing product
- You need high-confidence evidence to justify a significant investment

**When NOT to use:**
- Traffic is too low for statistical significance (fewer than 1,000 users per variant)
- The concept is entirely new (test with prototypes first)
- The change is too small to produce a detectable effect

## Choosing the Right Experiment

The decision depends on three factors: what you need to learn, how much confidence you need, and how much you can invest.

### Experiment Selection Matrix

| Question to Answer | Best Experiment | Fidelity | Time | Confidence |
|-------------------|-----------------|----------|------|------------|
| "Does anyone want this?" | Landing page smoke test | Low | 1-2 days | Medium |
| "Does the flow make sense?" | Paper prototype | Very low | 1 day | Low-Medium |
| "Can users complete this task?" | Clickable prototype | Medium | 3-5 days | Medium-High |
| "Does this solution actually work?" | Concierge MVP | High | 1-2 weeks | High |
| "Will the automated version feel right?" | Wizard of Oz | High | 1-2 weeks | High |
| "Which version performs better?" | A/B test | Production | 2-4 weeks | Very High |

### The Fidelity Ladder

Start at the lowest rung that can answer your question. Only climb higher when lower fidelity cannot provide the needed confidence.

```
Level 1: Paper prototype / Sketches
  ↓ (if concept validated, test usability)
Level 2: Clickable prototype (Figma, Sketch)
  ↓ (if usability validated, test real value)
Level 3: Concierge MVP / Wizard of Oz
  ↓ (if value validated, test at scale)
Level 4: Coded experiment / A/B test
  ↓ (if optimized, ship)
Level 5: Production release
```

## Experiment Design Template

Use this template for every experiment, regardless of type:

```
EXPERIMENT DESIGN
=================
Date: _______________
Hypothesis ID: _______________
Experimenter: _______________

HYPOTHESIS
We believe _______________
will happen if _______________
achieves _______________
with _______________.

EXPERIMENT TYPE
[ ] Paper prototype  [ ] Clickable prototype  [ ] Concierge MVP
[ ] Wizard of Oz     [ ] Landing page test    [ ] A/B test
[ ] Other: _______________

AUDIENCE
Target persona: _______________
Sample size: _______________
Recruitment method: _______________

DESIGN
What we will build/prepare: _______________
What the participant will do: _______________
What we will observe/measure: _______________

SUCCESS CRITERIA
Primary metric: _______________
Success threshold: _______________
Failure threshold: _______________

TIME BOX
Build time: _______________
Run time: _______________
Analysis time: _______________
Total: _______________

RESULTS (fill after experiment)
Primary metric result: _______________
Qualitative observations: _______________
Surprises: _______________
Decision: [ ] Validate  [ ] Iterate  [ ] Pivot  [ ] Kill
Next step: _______________
```

## Minimum Viable Tests

A minimum viable test (MVT) is the simplest possible experiment that can answer a specific question. The goal is to learn before you build, not to test what you have already built.

### MVT Examples by Question

| Question | Minimum Viable Test | Time | Cost |
|----------|-------------------|------|------|
| "Do people understand our value proposition?" | Show landing page to 5 people, ask them to explain it back | 2 hours | Free |
| "Will users find this navigation intuitive?" | Card sort with 10 users using index cards | 3 hours | Free |
| "Is this onboarding flow clear?" | Clickable prototype with 5 users | 2 days | Free |
| "Do users prefer layout A or B?" | First-click test on UsabilityHub | 4 hours | $50-100 |
| "Will users pay for this feature?" | Add pricing page with "buy" button that leads to waitlist | 1 day | $50 for ads |
| "Is this workflow faster than the current one?" | Time-on-task comparison: 5 users on old flow, 5 on prototype | 1 day | Free |

### The 5-User Rule

Jakob Nielsen's research shows that 5 users uncover approximately 85% of usability problems. For Lean UX experiments:

- **5 users** for qualitative usability tests (prototype tests, task analysis)
- **20+ users** for quantitative surveys or preference tests
- **1,000+ users per variant** for statistically significant A/B tests

Do not over-recruit for qualitative tests. Five users, tested quickly, are better than 50 users tested slowly.

## Running Experiments in Practice

### Weekly Experiment Cadence

A mature Lean UX team runs experiments every week. Here is a sample cadence:

| Day | Activity |
|-----|----------|
| **Monday** | Review last week's results. Write new hypotheses. Design this week's experiment. |
| **Tuesday** | Build experiment artifact (prototype, landing page, test script). |
| **Wednesday** | Recruit participants (or launch ad traffic for smoke tests). |
| **Thursday** | Run experiment sessions (usability tests, interviews). |
| **Friday** | Synthesize results. Update hypothesis log. Plan next experiment. |

### Remote Experiment Tips

- Use screen-sharing tools (Zoom, Lookback) for moderated prototype tests
- Unmoderated tools (Maze, UserTesting) scale to more participants but lose qualitative depth
- Record sessions (with consent) so the full team can watch asynchronously
- Use virtual whiteboards (FigJam, Miro) for collaborative synthesis

### Common Experiment Failures

| Failure | Cause | Prevention |
|---------|-------|------------|
| Leading questions | Facilitator hints at the "right" answer | Use neutral prompts: "What would you do next?" not "Would you click here?" |
| Confirmation bias | Team sees only evidence that supports their idea | Assign a devil's advocate; review raw data before discussing |
| Too few participants | Results are unreliable | Minimum 5 for qualitative, 1,000+ per variant for A/B |
| No success criteria | Any result is interpreted as success | Define thresholds before running the experiment |
| Testing too late | Feature is already built; team is reluctant to change | Test early with low-fidelity artifacts; never skip the prototype stage |
| Wrong audience | Testing with colleagues instead of real users | Recruit external participants matching the target persona |

## Experiment Cheat Sheet

Quick reference for choosing and running experiments:

| If you need to learn... | Use this experiment | Minimum time | Participants |
|------------------------|-------------------|-------------|-------------|
| Does the concept resonate? | Landing page smoke test | 2 days | 200+ visitors |
| Does the flow work? | Paper or clickable prototype | 1-2 days | 5 users |
| Is the solution valuable? | Concierge MVP | 1-2 weeks | 5-10 users |
| Does the "smart" feature feel right? | Wizard of Oz | 1-2 weeks | 5-10 users |
| Which design wins? | A/B test | 2-4 weeks | 1,000+ per variant |
| What do users really need? | Customer interview | 1 day | 5-8 users |
| How do users organize information? | Card sort | 3 hours | 10-15 users |
| What do users notice first? | First-click or 5-second test | 4 hours | 20+ users |
