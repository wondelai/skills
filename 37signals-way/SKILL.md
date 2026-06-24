---
name: 37signals-way
description: 'Build lean, opinionated products using the 37signals philosophy from "Getting Real", "Rework", and "Shape Up". Use when the user mentions "Getting Real", "Rework", "Shape Up", "37signals", "Basecamp method", "six-week cycles", "fixed time variable scope", "appetite vs estimates", "betting table", "breadboarding", "fat marker sketch", "build less", "underdo the competition", "opinionated software", "we have too many meetings", "the project keeps growing", "how do we ship faster", or "stop overbuilding". Also trigger when cutting scope to ship sooner, fighting feature creep, running a small team, avoiding long-term roadmaps, or killing unnecessary meetings. Covers shaping, betting, building, and the art of saying no. For MVP validation, see lean-startup. For design sprints, see design-sprint.'
license: MIT
metadata:
  author: wondelai
  version: "1.2.0"
---

# The 37signals Product Development Framework

A system for building profitable software without bloat, bureaucracy, or burnout, distilled from three books: *Getting Real* (build less), *Rework* (say no by default), and *Shape Up* (fix time, flex scope). Use it to shape work, bet on six-week cycles, run small autonomous teams, and ship on a predictable cadence.

## Core Principle

**Build less.** The best products do fewer things exceptionally well — simplicity is the destination, not the starting point. Traditional development adds; the 37signals way subtracts: build half a product (not a half-assed product), say no by default, fix the time and flex the scope. Constraints are what make great work possible — six weeks, three people, and a shaped pitch force you to find the essential version.

## Scoring

**Goal: 10/10.** Rate product plans, feature scopes, and team processes 0-10 against these principles. Report the current score and the specific changes needed to reach 10/10.

- **9-10:** Fixed-time cycles, shaped pitches, small teams, no backlog, opinionated defaults, clear copy
- **7-8:** Mostly shaped work and small teams, but some scope creep or process overhead
- **5-6:** Some shaping happens, but backlogs persist, teams are too large, or preferences replace decisions
- **3-4:** Heavy process (standups, sprints, story points) with occasional simplicity efforts
- **0-2:** Feature factory: long-term roadmaps, large teams, estimation rituals, no shaping

### 1. Build Less, Underdo the Competition

**Core concept:** Win through deliberate omission — fewer features, fewer preferences, fewer moving parts, each done better than competitors do theirs. Build software you need yourself and solve problems you understand deeply.

**Why it works:** Every feature carries maintenance, cognitive, and opportunity costs forever, usually for a fraction of users. Building less keeps the product focused, the codebase manageable, and the team small.

**Key insights:**
- Half a product beats a half-assed product — do a few things well, not many things poorly
- Be a curator, not a hoarder: say no to good ideas so the great ones can breathe
- Make tiny decisions — big ones are hard to make and hard to reverse; small ones build momentum
- Underdo the competition: let them build the Swiss Army knife while you build the steak knife
- Focus on what won't change — speed, simplicity, reliability, ease of use

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Feature prioritization** | Default answer is no | Reporting dashboard requested → ship CSV export covering 90% of use cases |
| **MVP scoping** | Cut until it hurts, then cut more | Drop user accounts for v1; use email magic links |
| **Competitive strategy** | Underdo, don't outdo | Competitor has 50 integrations; ship 3 that work flawlessly |

**Ethical boundary:** Cut complexity, not accessibility or safety — "less" means focused, not neglectful.

See: [references/build-less.md](references/build-less.md)

### 2. Shaping the Work

**Core concept:** Before work reaches a team, a senior person who bridges product and technical worlds makes it rough (room to maneuver), solved (main elements figured out), and bounded (scope limited by appetite).

**Why it works:** Raw ideas waste team time; detailed specs turn teams into ticket-takers. Shaping removes the biggest unknowns while leaving design freedom, and appetite ("how much time is this worth?") replaces estimation ("how long will this take?") — bounded investment instead of open-ended commitment.

**Key insights:**
- A shaped pitch has five elements: problem, appetite, solution, rabbit holes, no-gos
- Breadboard flows as places, affordances, and connections — structure without visual design
- Fat marker sketches keep abstraction high; wireframes invite pixel-level feedback before the concept is validated
- Rabbit holes (scope-blowing risks) get addressed in the pitch, not during the build
- No-gos make boundaries visible, preventing scope creep before it starts

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Feature design** | Breadboard before mockup | "Invite teammate": Settings → invite form → email sent → accept link → dashboard |
| **Scope definition** | Set appetite first | "A 2-week appetite problem, not a 6-week one" shapes which solution fits |
| **Risk management** | Call out rabbit holes upfront | "Permissions could get complex — limit to owner/member for v1" |

**Ethical boundary:** Set appetites that reflect the problem's genuine value — never artificially small to pressure teams.

See: [references/shaping-work.md](references/shaping-work.md)

### 3. Betting and Cycles

**Core concept:** Replace backlogs and roadmaps with a betting table: senior stakeholders bet shaped pitches into six-week cycles, separated by two-week cool-downs. Unfinished work hits the circuit breaker — it does not automatically continue.

**Why it works:** Backlogs grow forever, create false progress, and dilute focus; limited cycle slots force real prioritization. The circuit breaker kills zombie projects, and cool-downs prevent the burnout of continuous sprinting.

**Key insights:**
- Abolish the backlog — if an idea is important, it will come back
- Six weeks is long enough for meaningful work, short enough to feel the deadline
- Variable scope: teams cut non-essential scope to hit the fixed deadline, never the reverse
- Plan one cycle at a time — long-term roadmaps are stale commitments
- Most pitches don't get bet on, and that's healthy

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Roadmap replacement** | Bet each cycle | 3-4 shaped pitches every 6 weeks instead of a 12-month roadmap |
| **Risk management** | Circuit breaker kills zombies | 70% done at week 6? It doesn't ship — re-shape and re-bet if it still matters |
| **Capacity planning** | Cool-down between cycles | Two weeks for bugs, tech debt, exploration, recovery |

**Ethical boundary:** Apply the circuit breaker honestly — to kill zombies, not politically inconvenient projects; the point is focus, not unsustainable pressure.

See: [references/betting-cycles.md](references/betting-cycles.md)

### 4. Small Teams and Execution

**Core concept:** Three-person teams (one designer, one or two programmers) work a shaped pitch autonomously — no standups, no PMs hovering. They discover their own tasks and track progress on hill charts.

**Why it works:** Three people can have a conversation; ten need a meeting. Teams that discover tasks from a shaped pitch develop real problem understanding, and hill charts tell the truth: uphill = still figuring out, downhill = executing known work.

**Key insights:**
- Scopes replace tasks — group related work into named slices that move independently on the hill
- Meetings are toxic: write it up instead
- Get real: working HTML with real data on day 2 beats a Figma mockup on day 5
- Launch now, iterate later — software in users' hands beats plans in a deck
- Design and programming integrate from day one — no handoff phases

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Team structure** | Three people max, no PM | One designer + two programmers per 6-week bet |
| **Progress tracking** | Hill charts, not burndowns | "Invitations" uphill (permissions unclear); "Email templates" downhill (executing) |
| **Communication** | Async-first, write it up | A written update or 5-minute video instead of a 30-minute meeting |

**Ethical boundary:** Autonomy requires genuinely manageable scope — if a team consistently works overtime to hit six weeks, fix the shaping, not the team.

See: [references/small-teams-execution.md](references/small-teams-execution.md)

### 5. Opinionated Software and Clear Communication

**Core concept:** Great software makes choices instead of burying users in preferences — every preference is a decision the team could not or would not make. The same honesty applies to copy: say what you mean, skip buzzwords, teach what you know openly.

**Why it works:** Software with 47 settings has no opinion; sensible defaults reduce cognitive load and create cohesion. Clear copy builds trust where marketing-speak erodes it, and teaching openly attracts customers who share your values.

**Key insights:**
- Pick the best default and ship it — revisit only if data shows it fails most users
- Epicycles (features patching problems earlier features created) compound complexity
- "Not now" is a valid, healthy answer to good feature requests
- Out-teach the competition; sell your by-products (books, posts, tools)
- Interface copy is your best marketing — every label and error message builds or burns trust

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Feature requests** | Default no, no false promises | "Thanks for the suggestion. We're not planning this right now." |
| **UI copy** | Plain language | "Your file is saved" not "Your asset has been successfully persisted to the cloud" |
| **Error messages** | Honest and helpful | "We couldn't send that email. Check the address and try again." |
| **Preferences** | Eliminate; choose defaults | Detect timezone from the browser; ship one good theme |
| **Marketing** | Honest positioning | "Basecamp is not for everyone. Here's who it's for and who it's not for." |

**Ethical boundary:** Opinionated means having a point of view, not ignoring feedback — listen carefully, then curate thoughtfully.

See: [references/opinionated-software.md](references/opinionated-software.md), [references/ux-ui-copy.md](references/ux-ui-copy.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Maintaining a backlog | Grows forever; false progress; diluted focus | Abolish it; bet on shaped pitches each cycle |
| Estimating instead of setting appetite | Estimates grow to fill time and invite negotiation | Ask "how much time is this problem worth?" |
| Pixel-perfect mockups before shaping | Too concrete too early; invites bikeshedding | Breadboards and fat marker sketches first |
| Extending a six-week cycle | Zombie projects teach teams deadlines are fake | Circuit breaker: not done means not shipped |
| Adding preferences instead of deciding | Complexity for all users to serve a few | Pick the best default and ship it |
| Daily standups and status meetings | Interrupt maker flow; reporting overhead | Hill charts for visibility; async updates |
| Saying yes to good feature requests | Good features still add non-essential complexity | Default to no; bet only on what matters this cycle |
| Planning multiple cycles ahead | Stale commitments reduce responsiveness | Plan one cycle at a time |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Is there a fixed time constraint on this work? | Scope expands indefinitely | Set a six-week (or smaller) appetite first |
| Is the work shaped (rough, solved, bounded)? | Scope problems surface mid-build | Define problem, appetite, solution, rabbit holes, no-gos |
| Can a team of 2-3 people do this? | Too big | Break into independent six-week bets |
| Said no to at least 5 things this cycle? | Building too much | Cut ruthlessly at the betting table |
| Is the team figuring out its own tasks? | Micromanagement; team not empowered | Hand off shaped pitches, not task lists |
| Tracking progress with hill charts? | False precision masks uncertainty | Switch to uphill (figuring out) vs. downhill (executing) |
| Is there a cool-down after this cycle? | Burnout; no cleanup time | Schedule two unstructured weeks between cycles |
| Does the software have a clear opinion here? | Decisions deferred to users via preferences | Pick the best default; remove the setting |

## Reference Files

- [references/build-less.md](references/build-less.md) — Underdoing the competition, embracing constraints, curation over accumulation, the art of cutting scope
- [references/shaping-work.md](references/shaping-work.md) — Breadboarding, fat marker sketches, appetite setting, the pitch format, identifying rabbit holes
- [references/betting-cycles.md](references/betting-cycles.md) — Six-week cycles, the betting table, the circuit breaker, cool-downs, why backlogs must die
- [references/small-teams-execution.md](references/small-teams-execution.md) — Three-person teams, hill charts, async communication, getting real with HTML, launch-first thinking
- [references/opinionated-software.md](references/opinionated-software.md) — Defaults over preferences, clear copywriting, saying no to feature requests, teaching openly
- [references/ux-ui-copy.md](references/ux-ui-copy.md) — Browser-first design, visual hierarchy, clear copy rules, empty states, error messages, anti-patterns
- [references/case-studies.md](references/case-studies.md) — Three scenarios: adopting Shape Up, resisting feature creep, replacing status meetings with hill charts

## Further Reading

- [*"Getting Real"*](https://www.amazon.com/Getting-Real-Smarter-Successful-Application/dp/0578012812?tag=wondelai00-20) by Jason Fried & David Heinemeier Hansson
- [*"Rework"*](https://www.amazon.com/Rework-Jason-Fried/dp/0307463745?tag=wondelai00-20) by Jason Fried & David Heinemeier Hansson
- [*"Shape Up: Stop Running in Circles and Ship Work that Matters"*](https://www.amazon.com/Shape-Up-Circles-Ship-Work/dp/B09ZSY1MWP?tag=wondelai00-20) by Ryan Singer
- [*"It Doesn't Have to Be Crazy at Work"*](https://www.amazon.com/Doesnt-Have-Crazy-Work/dp/0062874780?tag=wondelai00-20) by Jason Fried & David Heinemeier Hansson
- [*"Remote: Office Not Required"*](https://www.amazon.com/Remote-Office-Required-Jason-Fried/dp/0804137501?tag=wondelai00-20) by Jason Fried & David Heinemeier Hansson

## About the Authors

**Jason Fried** is co-founder and CEO of 37signals (Basecamp, HEY) and a leading advocate for calm companies and product simplicity. **David Heinemeier Hansson (DHH)** is 37signals co-founder and creator of Ruby on Rails, extracted from Basecamp's codebase; together they wrote *Getting Real*, *Rework*, *Remote*, and *It Doesn't Have to Be Crazy at Work*. **Ryan Singer** spent 15+ years shaping product at 37signals and codified the methodology in *Shape Up*.
