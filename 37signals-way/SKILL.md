---
name: 37signals-way
description: 'Build lean, opinionated products using the 37signals philosophy from Getting Real, Rework, and Shape Up. Use when the user mentions "Getting Real", "Rework", "Shape Up", "37signals", "Basecamp method", "six-week cycles", "fixed time variable scope", "appetite vs estimates", "betting table", "breadboarding", "fat marker sketch", "build less", "underdo the competition", or "opinionated software". Also trigger when cutting scope to ship faster, running small teams, avoiding long-term roadmaps, or eliminating meetings. Covers shaping, betting, building, and the art of saying no. For MVP validation, see lean-startup. For design sprints, see design-sprint.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# The 37signals Product Development Framework

A complete system for building profitable software products without bloat, bureaucracy, or burnout. Over fifteen years, 37signals distilled their approach into three books: *Getting Real* (2006) established the "build less" ethos, *Rework* (2010) challenged conventional business wisdom, and *Shape Up* (2019) operationalized everything into a repeatable development process. Together they form a philosophy, a mindset, and a method for small teams that ship meaningful work on a predictable cadence.

## Table of Contents

- [Core Principle](#core-principle)
- [Scoring](#scoring)
- [1. Build Less, Underdo the Competition](#1-build-less-underdo-the-competition)
- [2. Shaping the Work](#2-shaping-the-work)
- [3. Betting and Cycles](#3-betting-and-cycles)
- [4. Small Teams and Execution](#4-small-teams-and-execution)
- [5. Opinionated Software and Clear Communication](#5-opinionated-software-and-clear-communication)
- [Common Mistakes](#common-mistakes)
- [Quick Diagnostic](#quick-diagnostic)
- [Reference Files](#reference-files)
- [Further Reading](#further-reading)
- [About the Authors](#about-the-authors)

## Core Principle

**Build less.** The best products are not the ones with the most features but the ones that do fewer things exceptionally well. Simplicity is not a starting point — it is the destination.

**The foundation:** Traditional product development adds. The 37signals way subtracts. Getting Real says: build half a product, not a half-assed product. Rework says: say no to almost everything by default. Shape Up says: fix the time, flex the scope. All three converge on the same truth — constraints are not obstacles to great work, they are what make great work possible. When you have six weeks, three people, and a shaped pitch, you cannot afford to build the wrong thing. You are forced to find the essential version. That is the advantage.

## Scoring

**Goal: 10/10.** When reviewing or creating product development plans, feature scopes, team processes, or product strategies, rate them 0-10 based on adherence to 37signals principles. A 10/10 means fixed-time cycles, shaped work, small autonomous teams, ruthless scope cutting, opinionated defaults, and clear honest communication. Lower scores indicate feature bloat, process overhead, or decision-deferring. Always provide the current score and specific improvements needed to reach 10/10.

- **9-10:** Fixed-time cycles, shaped pitches, small teams, no backlog, opinionated defaults, clear copy
- **7-8:** Mostly shaped work and small teams, but some scope creep or unnecessary process overhead
- **5-6:** Mixed — some shaping happens but backlogs persist, teams are too large, or preferences replace decisions
- **3-4:** Heavy process (standups, sprints, story points) with occasional simplicity efforts
- **0-2:** Feature factory with long-term roadmaps, large teams, estimation rituals, and no shaping

### 1. Build Less, Underdo the Competition

**Core concept:** Competitive advantage through deliberate omission. Fewer features, fewer preferences, fewer moving parts. Instead of matching competitors feature-for-feature, do less — but do it better. Build software you need yourself, and solve problems you understand deeply.

**Why it works:** Every feature you add has a maintenance cost, a cognitive cost to users, and an opportunity cost. Most features are used by a fraction of users but maintained by the entire team forever. By building less, you keep the product focused, the codebase manageable, and the team small. You also force yourself to identify what truly matters — the 20% of functionality that delivers 80% of the value.

**Key insights:**
- Solve your own problem first — the surest way to build something valuable is to build something you need
- Half a product is better than a half-assed product — do a few things well rather than many things poorly
- Embrace constraints — limited time, money, and people force creative solutions
- Be a curator, not a hoarder — your job is to say no to good ideas so the great ones can breathe
- Make tiny decisions — big decisions are hard to make and hard to reverse; small ones build momentum
- Underdo the competition — let them build the Swiss Army knife while you build the steak knife
- Less software means less to maintain, less to test, less to explain, and less to go wrong
- Focus on what will not change — speed, simplicity, reliability, and ease of use never go out of style

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Feature prioritization** | Default answer is no | A customer requests a reporting dashboard; instead, ship a CSV export that covers 90% of use cases |
| **MVP scoping** | Cut until it hurts, then cut more | Remove user accounts entirely for v1; use email-based magic links instead |
| **Competitive strategy** | Underdo, do not outdo | Competitor has 50 integrations; you ship 3 that work flawlessly |
| **Preference elimination** | Pick sensible defaults | Instead of 12 notification settings, ship one thoughtful default with an off switch |
| **Constraint adoption** | Use limits as creative fuel | Three-person team and six weeks forces you to find the simplest version that works |

**Ethical boundary:** Building less must serve users, not just save development time. Cut complexity, not accessibility or safety. "Less" means focused, not neglectful.

See: [references/build-less.md](references/build-less.md)

### 2. Shaping the Work

**Core concept:** Before work is given to a team, it must be shaped. Shaping means making the work rough (room to maneuver), solved (main elements figured out), and bounded (clear scope limits defined by appetite). Shaping is the critical step between a raw idea and a team project. It is done by a senior person who understands both the product and the technical landscape.

**Why it works:** Raw ideas are too vague — teams waste time figuring out what to build. Detailed specs are too rigid — teams become ticket-takers with no room for creative problem-solving. Shaping finds the sweet spot: enough definition to remove the biggest unknowns, enough freedom for the team to design the implementation. The appetite (how much time is this worth?) replaces traditional estimation (how long will this take?), flipping the dynamic from open-ended commitment to bounded investment.

**Key insights:**
- Appetite vs. estimates — start with how much time a problem is worth, not how long a solution will take
- Breadboarding maps the flow using places, affordances, and connection lines — no visual design, just structure
- Fat marker sketches are drawn at a level of abstraction that prevents bikeshedding on visual details
- Wireframes are too concrete too early — they invite pixel-level feedback before the concept is validated
- A shaped pitch has five elements: problem, appetite, solution, rabbit holes, and no-gos
- Rabbit holes are the known risks that could blow up the scope — address them in the pitch, not during the build
- No-gos explicitly define what the solution will not include — preventing scope creep by making boundaries visible
- The shaper is neither the building team nor management — it is a senior person who bridges both worlds

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Feature design** | Breadboard before mockup | Map "user invites teammate" as: Settings → Invite form → Email sent → Accept link → Dashboard |
| **Scope definition** | Set appetite first | "This is a 2-week appetite problem, not a 6-week one" — shapes what solution is appropriate |
| **Team briefing** | Hand off shaped pitches, not specs | Pitch includes problem, appetite, rough solution, rabbit holes, no-gos |
| **Design fidelity** | Fat marker, not pixel-perfect | Sketch on a tablet with a thick brush to keep abstraction high |
| **Risk management** | Call out rabbit holes in advance | "The permissions model could get complex — limit to owner/member for v1" |

**Ethical boundary:** Shaping must honestly bound the work. Do not define an appetite that is unrealistically small to pressure teams. The appetite should reflect the genuine value of the problem, not a desired deadline.

See: [references/shaping-work.md](references/shaping-work.md)

### 3. Betting and Cycles

**Core concept:** Replace backlogs and long-term roadmaps with a betting table. Senior stakeholders review shaped pitches and bet on the ones worth building in the next six-week cycle. If work is not done in six weeks, it does not automatically continue — the circuit breaker kills it. Two-week cool-down periods between cycles give teams breathing room.

**Why it works:** Backlogs grow forever, create a false sense of progress, and dilute focus. The betting table forces real prioritization: with limited slots in a six-week cycle, you can only pick a handful of shaped pitches. The circuit breaker prevents zombie projects that drain morale and block fresh bets. Cool-down periods let teams fix bugs, explore ideas, and recharge — preventing the burnout that continuous sprinting creates.

**Key insights:**
- Backlogs are a graveyard of good intentions — abolish them; if an idea is important, it will come back
- The betting table meets at the end of each cool-down to choose work for the next cycle
- Six-week cycles are long enough for meaningful work and short enough to maintain urgency
- The circuit breaker is non-negotiable: if it is not done in six weeks, it does not ship and gets re-evaluated
- Cool-down (two weeks) is unstructured time for bugs, exploration, and small improvements
- Plan one cycle at a time — long-term roadmaps create false commitments and reduce responsiveness
- Saying no is the default — most pitches do not get bet on, and that is healthy
- Variable scope means teams cut non-essential scope to hit the fixed deadline, not the other way around

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Roadmap replacement** | Betting table each cycle | Instead of a 12-month roadmap, pick 3-4 shaped pitches every 6 weeks |
| **Project scoping** | Six-week maximum | Break a large initiative into independent 6-week bets rather than a multi-month project |
| **Risk management** | Circuit breaker kills zombies | Feature at 70% after 6 weeks? It does not ship. Re-shape and re-bet next cycle if it still matters |
| **Capacity planning** | Cool-down periods | Two weeks between cycles for technical debt, bug fixes, and team recovery |
| **Stakeholder management** | Betting creates accountability | Senior people bet their credibility on pitches — no more invisible backlog shuffling |

**Ethical boundary:** The circuit breaker must be applied honestly. Do not use it to kill projects that are on track but politically inconvenient. Do not use six-week limits to create unsustainable pressure. The point is focus, not speed.

See: [references/betting-cycles.md](references/betting-cycles.md)

### 4. Small Teams and Execution

**Core concept:** Three-person teams (one designer, one or two programmers) work autonomously on shaped work. No daily standups, no project managers hovering, no status meetings. The team receives a shaped pitch with boundaries and figures out the tasks themselves. Progress is tracked with hill charts, not burndown charts or percentage-complete metrics.

**Why it works:** Small teams move faster because communication overhead is near zero. Three people can have a conversation; ten people need a meeting. When teams discover their own tasks from the shaped pitch, they develop real understanding of the problem rather than executing a list someone else wrote. Hill charts show the truth about where work stands — the uphill phase (figuring things out) is honest about uncertainty, and the downhill phase (executing known work) shows real progress.

**Key insights:**
- Three-person teams are the unit of work — one designer and one or two programmers
- The team figures out tasks by exploring the shaped pitch, not by reading a ticket list
- Hill charts have two phases: uphill (uncertainty, figuring out) and downhill (certainty, executing)
- Scopes replace tasks — group related work into named scopes that can move independently on the hill
- Meetings are toxic — use asynchronous communication by default; write it up instead of calling a meeting
- Get real: build with real HTML and real data as early as possible, not wireframes and lorem ipsum
- Launch now, iterate later — working software in users' hands beats theoretical plans in a slide deck
- Integrate design and programming from day one — no handoffs, no "design phase" followed by "dev phase"

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Team structure** | Three-person maximum | One designer + two programmers for a 6-week bet; no PM role needed |
| **Progress tracking** | Hill charts, not burndowns | "User Invitations" is uphill (still figuring out permissions); "Email Templates" is downhill (executing) |
| **Communication** | Async-first, write it up | Post a 5-minute Loom or a written update instead of scheduling a 30-minute meeting |
| **Design process** | Get real with HTML early | Build a working prototype in the browser on day 2, not a Figma mockup on day 5 |
| **Task discovery** | Team explores, not follows | Give the team the shaped pitch; they break it into scopes themselves |

**Ethical boundary:** Small teams must not mean overworked teams. Autonomy requires that scope is genuinely manageable. If a three-person team consistently works overtime to hit six-week deadlines, the problem is in the shaping, not the team.

See: [references/small-teams-execution.md](references/small-teams-execution.md)

### 5. Opinionated Software and Clear Communication

**Core concept:** Great software makes choices for the user instead of burying them in preferences. Every preference is a decision the team could not make — or would not make. Clear, honest copywriting reflects the same philosophy: say what you mean, skip the buzzwords, and respect the user's time. Teach everything you know openly.

**Why it works:** Software with too many preferences is software with no opinion. Users do not want 47 settings; they want software that works well out of the box. When you make decisions for users (pick the sensible default), you reduce cognitive load and create a more cohesive experience. The same applies to communication: clear copy builds trust, marketing-speak erodes it. And teaching your methods openly (like 37signals does with their books and blog) attracts customers who share your values.

**Key insights:**
- Every preference is a decision you are pushing to the user — pick the best default and ship it
- If it sounds like marketing, rewrite it — clear, honest language outperforms buzzwords
- Epicycles (adding feature on feature to fix problems created by earlier features) compound complexity
- Say no to most feature requests, even good ones — "not now" is a valid and healthy answer
- Focus on what will not change: speed, simplicity, reliability, and ease of use
- Out-teach the competition — share your philosophy, process, and knowledge openly
- Sell your by-products — the things you learn while building are valuable to others (books, blog posts, tools)
- Your app's interface copy is your best marketing — every label, error message, and confirmation is a chance to build trust

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Feature requests** | Default answer is no | "Thanks for the suggestion. We're not planning this right now." — no apology, no promise |
| **UI copy** | Plain language, no buzzwords | "Your file is saved" instead of "Your asset has been successfully persisted to the cloud" |
| **Preferences** | Eliminate, choose defaults | Remove the timezone selector; detect it from the browser. Remove the theme picker; ship one good theme |
| **Error messages** | Honest and helpful | "We couldn't send that email. Check the address and try again." — not "An unexpected error occurred" |
| **Documentation** | Teach openly | Blog about how you build, what you decided, and why — even if competitors read it |
| **Marketing** | Be honest, share your philosophy | "Basecamp is not for everyone. Here's who it's for and who it's not for." |

**Ethical boundary:** Being opinionated must not mean being dismissive of user needs. Listen carefully to what users struggle with, then curate thoughtfully. Opinionated means you have a point of view — not that you ignore feedback.

See: [references/opinionated-software.md](references/opinionated-software.md), [references/ux-ui-copy.md](references/ux-ui-copy.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Maintaining a backlog | Backlogs grow forever, create false sense of progress, and dilute focus | Abolish the backlog; bet on shaped pitches each cycle |
| Estimating instead of setting appetite | Estimates grow to fill available time and invite negotiation over hours | Start with appetite: "How much time is this problem worth?" |
| Pixel-perfect mockups before shaping | Too concrete too early; invites bikeshedding and kills creative exploration | Use breadboards and fat marker sketches at the right level of abstraction |
| Extending a six-week cycle | Zombie projects drain morale, block new bets, and teach teams that deadlines are fake | Apply the circuit breaker: if it is not done in six weeks, it does not ship |
| Adding preferences instead of deciding | Every preference adds complexity for all users to serve a few; compounds over time | Pick the best default and ship it; revisit only if data shows the default fails most users |
| Daily standups and status meetings | Interrupt maker flow, create reporting overhead, and slow teams down | Use hill charts for visibility and async updates for communication |
| Saying yes to good feature requests | Good features still add complexity; most are not essential for the core job | Default to no; only bet on what matters most this cycle |
| Planning more than one cycle ahead | Long-term plans become stale commitments that reduce responsiveness to what you learn | Plan one cycle at a time; stay responsive to new information |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Is there a fixed time constraint on this work? | Scope will expand indefinitely | Set a six-week appetite before starting |
| Has the work been shaped (rough, solved, bounded)? | Team will discover scope problems mid-build | Shape the pitch: define problem, appetite, solution, rabbit holes, no-gos |
| Can a team of 2-3 people do this? | Too big; needs decomposing | Break into independent scoped pieces that each fit a small team |
| Have you said no to at least 5 things this cycle? | Probably building too much | Review the betting table and cut ruthlessly |
| Is the team figuring out their own tasks? | Micromanaging; team is not empowered | Hand off shaped pitches, not task lists |
| Are you tracking progress with hill charts? | False precision masking real uncertainty | Switch to hill charts: uphill (figuring out) vs. downhill (executing) |
| Is there a cool-down after this cycle? | Teams will burn out; no time for cleanup | Schedule two weeks of unstructured time between cycles |
| Does your software have a clear opinion on this feature? | Deferring decisions to users via preferences | Pick the best default and remove the setting |

## Reference Files

- [references/build-less.md](references/build-less.md) — The philosophy of less: underdoing the competition, embracing constraints, curation over accumulation, and the art of cutting scope
- [references/shaping-work.md](references/shaping-work.md) — The shaping process: breadboarding, fat marker sketches, appetite setting, the pitch format, and identifying rabbit holes
- [references/betting-cycles.md](references/betting-cycles.md) — Six-week cycles, the betting table, the circuit breaker, cool-down periods, and why backlogs must die
- [references/small-teams-execution.md](references/small-teams-execution.md) — Three-person teams, hill charts, async communication, getting real with HTML, and launch-first thinking
- [references/opinionated-software.md](references/opinionated-software.md) — Defaults over preferences, clear copywriting, saying no to feature requests, and teaching openly
- [references/ux-ui-copy.md](references/ux-ui-copy.md) — The 37signals approach to UX, UI design, and interface copywriting: browser-first design, visual hierarchy, clear copy rules, empty states, error messages, and anti-patterns
- [references/case-studies.md](references/case-studies.md) — Three scenarios applying 37signals principles: adopting Shape Up, resisting feature creep, and replacing status meetings with hill charts

## Further Reading

- [*"Getting Real"*](https://www.amazon.com/Getting-Real-Smarter-Successful-Application/dp/0578012812?tag=wondelai00-20) by Jason Fried & David Heinemeier Hansson
- [*"Rework"*](https://www.amazon.com/Rework-Jason-Fried/dp/0307463745?tag=wondelai00-20) by Jason Fried & David Heinemeier Hansson
- [*"Shape Up: Stop Running in Circles and Ship Work that Matters"*](https://www.amazon.com/Shape-Up-Circles-Ship-Work/dp/B09ZSY1MWP?tag=wondelai00-20) by Ryan Singer
- [*"It Doesn't Have to Be Crazy at Work"*](https://www.amazon.com/Doesnt-Have-Crazy-Work/dp/0062874780?tag=wondelai00-20) by Jason Fried & David Heinemeier Hansson
- [*"Remote: Office Not Required"*](https://www.amazon.com/Remote-Office-Required-Jason-Fried/dp/0804137501?tag=wondelai00-20) by Jason Fried & David Heinemeier Hansson

## About the Authors

**Jason Fried** is the co-founder and CEO of 37signals, the company behind Basecamp and HEY. He has been building web-based software since the mid-1990s and is a prominent advocate for calm companies, remote work, and product simplicity. Fried co-authored *Getting Real*, *Rework*, *Remote*, and *It Doesn't Have to Be Crazy at Work*. He is known for his contrarian stance against venture capital, growth-at-all-costs culture, and unnecessary complexity in both software and business.

**David Heinemeier Hansson (DHH)** is the co-founder and CTO of 37signals and the creator of Ruby on Rails, one of the most influential web application frameworks ever built. Rails was extracted directly from Basecamp's codebase — a textbook example of the 37signals philosophy of building real software first and extracting reusable tools second. DHH co-authored *Getting Real*, *Rework*, *Remote*, and *It Doesn't Have to Be Crazy at Work*. He is known for challenging industry orthodoxies around microservices, TypeScript, cloud computing, and startup culture.

**Ryan Singer** is the former Head of Strategy at 37signals, where he spent over fifteen years shaping products and refining the development process that became Shape Up. His experience leading product work at Basecamp gave him unique insight into what makes small teams effective and how to structure work for maximum autonomy. Singer wrote *Shape Up* as a free online book (basecamp.com/shapeup), later published in print, codifying the methodology that 37signals had practiced for years.
