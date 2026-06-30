---
name: steve-jobs-design-review
description: 'Review designs, products, and features with Steve Jobs'' standards: ruthless simplicity, focus, and end-to-end excellence. Use when the user mentions "Steve Jobs review", "design review", "product review", "what would Steve do", "insanely great", "this feels too complicated", "too many features", "product taste", "saying no", or "is this good enough to ship". Also trigger when critiquing a UI, feature, or roadmap for focus and simplicity, cutting scope to the essential, or pressure-testing the whole experience from first run to daily use. Covers the simplicity audit, the no list, design-is-how-it-works, end-to-end ownership, demo culture, and a Jobs-style review protocol with binary verdicts. For visual design fundamentals, see refactoring-ui. For usability audits, see ux-heuristics. For detail polish, see microinteractions.'
license: MIT
metadata:
  author: wondelai
  version: "1.2.0"
---

# Steve Jobs Design Review

Run design and product reviews the way Steve Jobs ran them: start from the customer experience, subtract until only the essential remains, and refuse to call anything done that isn't insanely great.

## Core Principle

**"You've got to start with the customer experience and work backwards to the technology."** Review every product from what a customer sees, feels, and accomplishes — never from the feature list, the org chart, or the technology that happened to be available. And remember the standard: "Design is not just what it looks like and feels like. Design is how it works."

## Scoring

**Goal: 10/10.** Count how many of the 7 Quick Diagnostic rows the product passes, then map to 0-10: 7/7 = 10, 6/7 = 9, 5/7 = 7, 4/7 = 6, 3/7 = 4, ≤2/7 ≤ 3. Bands: **9-10** = insanely great, ships; **5-8** = real cuts and fixes required; **≤4** = not done, back to demos. There is no "pretty good"; state the score, the exact rows that failed, and the specific cuts or fixes required to reach 10/10.

## Framework

### 1. Simplicity Is the Ultimate Sophistication

**Core concept:** Simplicity is not the absence of features — it is complexity conquered. Keep subtracting until removing one more thing would break the product's purpose.

**Why it works:** Every element a user must perceive, parse, or decide about taxes attention and erodes confidence. Simplicity that survives deep understanding of the problem feels inevitable; simplicity achieved by hiding things feels broken.

**Key insights:**
- "It takes a lot of hard work to make something simple, to truly understand the underlying challenges and come up with elegant solutions"
- The iPod shipped with no on/off switch — the need was designed away, not the button hidden
- Measure steps-to-value: Jobs demanded any song in three presses; the original iDVD pitch was one window, drag video in, click "Burn"
- Prefer one good default over a setting; every preference is a decision you failed to make
- If you must explain it, redesign it — instructions are apologies

**Review applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Feature audit | Count steps to core value; cut anything off the main path | Signup → first value in 3 steps, not 9 |
| UI critique | Remove elements until the screen states one intent | One primary button per screen |
| Settings review | Replace options with opinionated defaults | Auto-save always on; no toggle |

**Review prompts:**
- "What can we remove and have this still work better?"
- "Why is this here? Who asked for it, and does the core user need it?"
- "Explain this screen in one sentence. Can't? It's two screens — or none."

**Ethical boundary:** Simplify by solving complexity for the user, never by burying necessary controls or costs (pricing, privacy, cancellation) where they can't be found.

See [references/simplicity-and-focus.md](references/simplicity-and-focus.md) when running a simplicity audit — the 5-step subtraction method, steps-to-value measurement, and the surface-vs-deep simplicity table.

### 2. Focus Means Saying No

**Core concept:** "Focusing is about saying no." Deciding what not to build is as important as deciding what to build — innovation is saying no to 1,000 things.

**Why it works:** Effort spread across many decent things produces nothing great. Killing good ideas concentrates the team's best people and attention on the few products that matter, and protects the product from becoming a committee's wish list.

**Key insights:**
- In 1997 Jobs cut dozens of Apple products to a 2×2 matrix: consumer/pro × desktop/portable — focus saved the company
- At retreats, the team's top-10 priority list got cut to three: "We can only do three"
- "I'm as proud of the things we haven't done as the things we have done"
- A roadmap with no recently killed items isn't focused, it's unexamined
- Saying no includes features already shipped — deletion is a feature

**Review applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Roadmap review | Force-rank, then cut everything below #3 | Q3 plan: 3 bets, not 14 backlog items |
| Scope creep | Require a kill for every add | New dashboard widget = retire one |
| Product line | Collapse overlapping SKUs/tiers | One plan per customer type |

**Review prompts:**
- "If we could ship only one thing this quarter, which — and why isn't the rest cut?"
- "What is this product deliberately bad at?"
- "What did we say no to this cycle? Nothing? Then we said yes to mediocrity."

**Ethical boundary:** Say no to scope, never to evidence — killing a feature is strategy; ignoring user pain that contradicts your vision is vanity.

See [references/review-protocol.md](references/review-protocol.md) for the saying-no rituals — the force-rank-to-three exercise, the kill-for-every-add rule, and how to run a no list in a live review.

### 3. Design Is How It Works

**Core concept:** Design is not a veneer applied at the end — it is the architecture of how the product behaves. Judge flows, speed, and failure states, not just the mockup's beauty.

**Why it works:** Users don't experience screenshots; they experience latency, errors, interruptions, and sequences. A beautiful product that stutters, loses work, or confuses on failure is badly designed no matter how it looks.

**Key insights:**
- The iPhone keyboard succeeded through behavior (aggressive autocorrect), not visuals — engineering and design are one discipline
- Review the slowest moment, not the happy path: cold start, empty state, offline, error recovery
- "It just works" is a design spec: zero configuration, zero manual, zero ceremony
- Beauty that fights function is decoration; reject it
- Latency is a design property — a 2-second wait is a design flaw, wherever it lives in the stack

**Review applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Mockup review | Demand the interaction, not the still | Click through states, not slides |
| Performance | Set experience budgets in the review | First screen < 1s or it fails review |
| Failure design | Walk error/empty/offline paths | Payment fails → user knows exactly what next |

**Review prompts:**
- "Show me what happens when it fails."
- "How does this feel after the 100th use, not the demo?"
- "Where does the user wait, and what did we do about it?"

See [references/end-to-end-experience.md](references/end-to-end-experience.md) when reviewing behavior over visuals — the daily-use and failure/support stages cover how to walk the slow moments, error paths, and offline states most demos skip.

### 4. Own the Whole Experience

**Core concept:** The product is every touchpoint: discovery, purchase, unboxing or first run, onboarding, daily use, failure, support, billing, and leaving. Review the whole widget, not the app in isolation.

**Why it works:** Customers judge the experience as one thing. Apple built unboxing rituals, its own stores, and the Genius Bar because a great device sold badly or supported rudely becomes a bad product in memory.

**Key insights:**
- Packaging got design-lab treatment at Apple — first impressions are part of the product
- The first run is your unboxing: what users see at minute zero deserves hero-screen care
- Support tickets, invoices, and cancellation flows are product surfaces — usually nobody designed them
- Every handoff between teams (marketing → onboarding → product → support) is where experience seams show
- Map the journey end to end; the worst touchpoint sets the perceived quality

**Review applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Launch review | Audit every touchpoint as one journey | Ad promise matches first-run reality |
| Onboarding | Treat first session as theater | First 60 seconds rehearsed like a keynote |
| Lifecycle | Review billing, support, offboarding | Cancellation takes one screen, keeps dignity |

**Review prompts:**
- "Walk me from hearing about this to recommending it — where does it crack?"
- "Who designed the invoice? The error email? The cancel flow?"
- "Does the experience keep its promise after the sale?"

**Ethical boundary:** Owning the whole experience means owning failures too — never design a polished entrance and a hostile exit.

See [references/end-to-end-experience.md](references/end-to-end-experience.md) when mapping the journey — the 7-stage touchpoint map from discovery to offboarding, the worst-touchpoint rule, and the org seams that produce undesigned surfaces.

### 5. Demo or It Doesn't Exist

**Core concept:** Review working artifacts, not specs or slideware. Concrete demos expose truth that documents hide; decisions are made by a decider reacting to the real thing.

**Why it works:** Abstractions let everyone imagine a different product and agree on nothing. A demo at real size on the real device forces specific feedback, surfaces dealbreakers early, and converges by decision rather than committee drift.

**Key insights:**
- Apple's software culture (Kocienda's "creative selection"): build a demo, show a decision-maker, get direct feedback, iterate — that loop is the process
- The iPhone keyboard was chosen by a derby of competing working demos, not a requirements doc
- Review on the target device at target data scale — a phone UI judged on a projector lies
- Prototype the riskiest moment first; a demo of the easy 80% proves nothing
- "Real artists ship": demos exist to force decisions, not to delay them

**Review applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Design review | Ban slide-only reviews | Figma prototype or build, never static deck |
| Competing ideas | Run a demo derby, pick one | Two nav models built, one verdict |
| Stakeholder alignment | Demo to the decider weekly | 30-min demo replaces 3 status docs |

**Review prompts:**
- "Don't tell me — show me. On the device."
- "Which of these two demos wins? Pick one; we're not shipping a compromise of both."
- "What's the riskiest assumption, and where's the demo that tests it?"

**Ethical boundary:** Demos must show honest state — a staged demo that hides known breakage is a lie with a UI.

See [references/demo-culture.md](references/demo-culture.md) when setting up a demo-driven review — the creative-selection loop, how to run a demo derby, the decider role, and honest-demo rules.

### 6. Taste and the Back of the Fence

**Core concept:** A great carpenter doesn't use plywood on the back of the cabinet, even though nobody will see it. Care invested in unseen surfaces — and the taste of the people applying it — is what quality actually is.

**Why it works:** Users sense craft subliminally: aligned pixels, coherent copy, graceful edge cases add up to trust. Teams that cut corners where "nobody looks" train themselves to cut corners everywhere; excellence is a habit enforced by standards, not inspections.

**Key insights:**
- The original Mac team signed the inside of the case; Jobs made engineers redo the circuit board layout for beauty no customer would see
- "Technology alone is not enough" — products live at the intersection of technology and the liberal arts
- Audit the back-of-fence surfaces: empty states, error copy, settings pages, loading screens, emails
- "Be a yardstick of quality" — A-players raise each other; tolerated mediocrity compounds
- Taste is trainable: study great products, articulate why they're great, apply the standard ruthlessly

**Review applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Detail audit | Review the screens nobody demos | 404 page held to homepage standard |
| Copy review | Read every string aloud | Error messages sound human, specific |
| Team standard | Critique to the best work, not the average | "Is this the best you've ever done?" |

**Review prompts:**
- "Show me the ugliest screen in the product — that's our real quality bar."
- "Would you sign your name inside this?"
- "Where did we use plywood?"

See [references/case-studies.md](references/case-studies.md) for worked examples of the standard in action — the original Mac circuit board redone for unseen beauty, the iMac's opinionated subtraction, plus the MobileMe and antenna-gate failure reviews and what each teaches a reviewer.

### 7. Running the Review

**Core concept:** Structure the review: experience the product cold as a customer, name the One Thing it must do, audit against principles 1-6, then deliver a binary verdict — insanely great, or not done — with a specific cut list and fix list.

**Why it works:** Reviews fail through vagueness and politeness. A fixed walkthrough order, brutal specificity, and a binary verdict prevent "good enough" from shipping while giving the team an exact path to 10/10. Products get judged against their own promise — "What is this supposed to do? Then why doesn't it do that?"

**Key insights:**
- Always experience the product cold before the meeting — first impressions can't be re-run
- Open with the promise: state what the product claims, then test only that
- Feedback must be specific and actionable: "this is confusing" fails review too — say what, where, why, and the fix direction
- End binary: ship-worthy or a ranked fix list; never "polish it a bit"
- One decider owns the verdict; input is wide, decision is narrow

ALWAYS output reviews in this format:

```
# Design Review: [Product/Feature]
**Verdict:** INSANELY GREAT / NOT DONE (score X/10)
**The One Thing:** [what this must do]
**Keeps its promise?** [yes/no — evidence]
**Cut list:** [what to remove]
**Fix list:** [ranked, specific, with fix direction]
**Back of the fence:** [unseen surfaces that fail the bar]
```

See [references/review-protocol.md](references/review-protocol.md) when running an actual review session — the timed 5-step agenda, the fix-item specificity test, the candor rules (brutal on work, decent on people), review cadence, and how to adapt the protocol for solo or async reviews.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Reviewing only aesthetics | Design is how it works; pretty-but-clunky still fails users | Walk flows, latency, and failure states |
| Fixing problems by adding | Each addition taxes attention and breeds more complexity | Subtract first; additions need a kill |
| Consensus verdicts | Committees average ideas into mush | One decider, wide input, narrow decision |
| Reviewing specs and slides | Abstractions hide dealbreakers; everyone imagines a different product | Demand working demos on the real device |
| "Good enough" verdicts | Mediocrity compounds into brand damage | Binary: insanely great or not done |
| Skipping unseen surfaces | Users sense plywood; teams learn to cut corners | Audit empty/error/settings/email states |
| Cosplaying cruelty | Fear stops demos and candor, killing the feedback loop | Be brutal about work, decent to people |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you state the One Thing this product must do in one sentence? | No focus — everything is the priority | Write it; cut what doesn't serve it |
| Does a new user reach core value in ≤3 steps? | Complexity is unconquered | Map steps-to-value; remove, don't reorder |
| Did the reviewer experience it cold, as a customer? | You reviewed the team's story, not the product | Use it before the meeting, no walkthrough |
| Is there a working demo on the real device? | You're approving an imagined product | Reschedule until there's a demo |
| Was anything removed this cycle? | Roadmap is accreting, not focusing | Add a cut list to every review |
| Do error, empty, and edge states match hero-screen quality? | Back of the fence is plywood | Audit and fix unseen surfaces |
| Would the team proudly use it daily and sign it? | The bar is "acceptable", not "insanely great" | Hold the binary verdict until pride is real |

## About the Author

Steve Jobs (1955-2011) co-founded Apple and led it to create the Mac, iPod, iPhone, and iPad, building the most valuable company in the world on design-led product development. This skill distills his documented review practices and standards from Walter Isaacson's authorized biography, Ken Segall's *Insanely Simple*, and Ken Kocienda's *Creative Selection*.

## Further Reading

This skill is based on documented accounts of Steve Jobs' product and design review practices:

- [*"Steve Jobs"*](https://www.amazon.com/Steve-Jobs-Walter-Isaacson/dp/1451648537?tag=wondelai00-20) by Walter Isaacson
- [*"Insanely Simple: The Obsession That Drives Apple's Success"*](https://www.amazon.com/Insanely-Simple-Obsession-Drives-Success/dp/1591846218?tag=wondelai00-20) by Ken Segall
- [*"Creative Selection: Inside Apple's Design Process During the Golden Age of Steve Jobs"*](https://www.amazon.com/Creative-Selection-Inside-Apples-Process/dp/1250194466?tag=wondelai00-20) by Ken Kocienda
