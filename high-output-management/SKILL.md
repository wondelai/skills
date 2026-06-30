---
name: high-output-management
description: 'Manage for output using Grove''s "High Output Management": a manager''s output is their organization''s output, raised by high-leverage activities. Use when the user mentions "high output management", "managerial leverage", "one-on-ones", "1:1 agenda", "OKRs", "performance review", "task-relevant maturity", "delegation", "meeting overload", "new manager", "how do I run a 1:1", or "just got promoted to manager". Also trigger when structuring a manager''s calendar and meeting cadence, designing team metrics, running planning, coaching delegation, or preparing performance reviews. Covers leverage, production principles, meetings as the medium of management, decisions, OKRs, and task-relevant maturity. For intrinsic motivation, see drive-motivation. For a company operating system, see traction-eos.'
license: MIT
metadata:
  author: wondelai
  version: "1.2.0"
---

# High Output Management

Manage teams the way Andy Grove ran Intel: a manager's output is not what the manager does — it is what their organization produces. This skill turns *High Output Management* into auditable practice: production principles for knowledge work, output indicators, managerial leverage, meetings as the medium of management, clean decisions, OKRs, and a management style matched to task-relevant maturity.

## Core Principle

**A manager's output = the output of their organization + the output of the neighboring organizations under their influence.** Nothing a manager does — emails, meetings, reviews, decisions — counts in itself; it counts only through how it raises that combined output. Since managerial time is the scarce input, the craft reduces to one question asked relentlessly: of everything I could do right now, what creates the most output per hour spent? Choose high-leverage activities; eliminate negative-leverage ones.

## Scoring

**Goal: 10/10.** Rate management practices, calendars, and processes 0-10 against the principles below. State the current score and the specific changes needed to reach 10/10.

- **9-10:** Output indicators with quality pairs, subordinate-owned 1:1s on a TRM-based cadence, delegation with task-level monitoring, OKRs that stretch without driving pay, calendar built around forecasted key events
- **7-8:** Process meetings run well, but a few activity metrics, ad hoc decision meetings, or skipped training sessions remain
- **5-6:** 1:1s happen irregularly, indicators track busyness, delegation is all-or-nothing, planning produces documents instead of actions
- **3-4:** Management by interruption: status theater, decisions made by rank, reviews as annual surprises
- **0-2:** No 1:1s, no indicators, firefighting as the operating mode, output invisible and unmeasured

## Framework

### 1. Production Principles for Knowledge Work

**Core concept:** Grove's breakfast factory — deliver a three-minute egg, buttered toast, and hot coffee simultaneously, at acceptable quality and lowest cost — contains all of production: build the flow around the limiting step (the egg), fix problems at the lowest-value stage, batch where setup costs dominate, and choose deliberately between building to forecast and building to order. Every team — engineering, support, recruiting — runs a production line, whether or not anyone has drawn it.

**Why it works:** Knowledge work hides its assembly line, and invisible flow invites firefighting. Production thinking makes flow visible: once you know the limiting step, everything else gets scheduled around it; once defects are caught at the egg stage instead of on the customer's plate, fixing them costs a fraction.

**Key insights:**
- Build around the limiting step: find the longest, hardest, or most expensive stage and offset everything else from it — often code review, staging access, or one overloaded specialist
- Fix problems at the lowest-value stage: kill a flawed spec in review, not after three sprints of building on it
- Batch work with high setup cost — interviews, code reviews, interrupt handling — so the setup amortizes across the batch
- Most knowledge work is built to forecast, not to order: staff the pipeline to the forecast and accept controlled risk, as the toast goes down before the customer orders
- You cannot watch all the work: treat it as a black box and cut windows into it with a handful of indicators

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Sprint flow | Schedule around the limiting step | Review is the bottleneck → protect reviewer hours before starting new work |
| Quality gates | Inspect at the lowest-value stage | Spec review kills a flawed design before a three-week build |
| Hiring pipeline | Batch and build to forecast | Phone screens batched Tue/Thu; interviewer capacity staffed to the offer-date forecast |

**Ethical boundary:** Run systems hot, not humans — production thinking optimizes the work, never treats people as interchangeable machines.

See: [references/indicators-and-production.md](references/indicators-and-production.md) when finding a limiting step or building a dashboard — limiting-step analysis, worked indicator pairs, leading vs trend indicators, stagger charts, and how to run an operation review.

### 2. Indicators That Don't Lie

**Core concept:** Measure output, not activity — what the team shipped that survived, not how busy it looked. Pair every quantity indicator with a quality counterpart so neither can be optimized at the other's expense, favor leading indicators that buy time to act, and report forecasts in stagger charts that show how each forecast evolved.

**Why it works:** People do what management measures, so an unpaired indicator is an instruction to game it. The pair closes the loop: push throughput and the escape rate exposes the corner-cutting. Leading indicators and stagger charts convert measurement from autopsy to steering.

**Key insights:**
- Lines of code, hours logged, and tickets touched are activity; features alive in production and problems solved are output
- Pair quantity with quality: deploys/week with change-failure rate, ticket closes with reopens, velocity with incident count
- Leading indicators (review queue age, build flakiness, on-call page rate) warn before output drops; trend indicators compare output against your own history and forecast
- A stagger chart re-forecasts the same horizon every period; reading down a column shows whether forecasting is honest, optimistic, or sandbagged
- Administrative work measures like a factory: offers per recruiter-week, invoices processed per day — always with a quality pair

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Eng dashboard | Pair quantity with quality | Deploys/week paired with change-failure rate |
| Support ops | Output plus its quality shadow | Tickets resolved/day paired with reopen rate and CSAT |
| Quarterly forecast | Stagger chart | Re-forecast quarter-end ARR monthly; drift visible down each column |

**Ethical boundary:** Indicators measure the work, not the worker — used for surveillance, they teach people to optimize the number instead of the output.

### 3. Managerial Leverage

**Core concept:** Leverage is the output created per unit of managerial time. High-leverage activities affect many people at once (training, well-prepared decisions, information gathering) or redirect months of work with a small, well-timed nudge. The calendar is the manager's production system: forecast the key events, batch the rest, and say no at the source when capacity is full.

**Why it works:** Managerial activities differ by orders of magnitude in output per hour — ninety minutes preparing a review shapes a year of someone's work, while a day of meddling subtracts output. A manager who lets the calendar happen to them spends prime hours on whatever shouted loudest.

**Key insights:**
- Negative leverage is real: meddling (supervising an expert in detail), waffling (stalling a decision others wait on), and a manager's visible gloom all multiply downward through the team
- Delegate the tasks you know best — monitoring them costs you least — and remember that delegation without monitoring is abdication
- Monitor at the task level, not the person level: sample like incoming inspection, deeper at low task-relevant maturity, lighter as it rises
- Forecast your limiting steps: put 1:1s, staff meetings, reviews, and planning on the calendar first and let interrupts fill around them, not the reverse
- Run below 100% load: a fully booked manager turns every surprise into a delay for everyone downstream; saying no early is cheaper than failing late
- Batch interruptions with office hours and known checkpoints instead of letting them shred maker time

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Week design | Forecast fixed events, batch the rest | 1:1s Tue-Wed mornings, PR reviews batched daily at 4pm, Monday deep-work block |
| Delegation | Monitoring depth by TRM | New hire's first migration: plan review plus daily spot checks; veteran's: rollout plan only |
| Interrupts | Convert random pings to office hours | Two daily drop-in slots replace ad hoc Slack escalations |

**Ethical boundary:** Leverage means multiplying others' output, never hoarding information or approvals until you become the bottleneck everyone must visit.

See: [references/leverage-and-calendar.md](references/leverage-and-calendar.md) when auditing a calendar or setting up delegation — the weekly leverage audit, positive/negative-leverage catalog, delegation protocol with TRM-based monitoring depth, calendar-redesign procedure, and interruption management.

### 4. Meetings Are the Medium of Management

**Core concept:** A meeting is not a symptom of bad management; it is where managerial work — gathering information, imparting it, deciding, nudging — actually happens. Process-oriented meetings (one-on-ones, staff meetings, operation reviews) run on a regular cadence and should carry the bulk of that work, roughly a quarter of the calendar. Mission-oriented meetings are ad hoc and exist solely to produce a decision.

**Why it works:** Regularity makes meetings cheap — standing agendas, shared expectations, zero setup cost — and starves the expensive kind: issues get caught small in 1:1s and staff meetings instead of exploding into emergency decision meetings. Grove's malorganization test: ad hoc mission-oriented meetings eating more than about a quarter of managerial time means the process is broken.

**Key insights:**
- The 1:1 is the subordinate's meeting: they own the agenda and bring it; the supervisor's job is to listen and learn what is really going on
- Set 1:1 frequency by task-relevant maturity, not seniority or affection: new-to-task weekly, veterans every few weeks — never less than monthly
- Both sides keep a "hold" list of non-urgent items for the next 1:1 — it batches interruptions away
- The supervisor takes the notes: writing down agreed actions signals commitment and forces follow-up
- "One more thing": after the agenda is done, ask what else is on their mind — the real issue often surfaces in the last five minutes
- Staff meetings are controlled free discussion — the manager moderates as a Socratic prodder, not a lecturer; a recurring "ad hoc" meeting is a process meeting in denial

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| New report | Weekly 1:1, their agenda | First 90 days: 60 minutes weekly; agenda arrives the day before |
| Team sync | Controlled free discussion | Two-minute updates, then debate on two pre-flagged issues |
| Recurring "urgent" meeting | Convert to process | Third ad hoc incident review this month becomes a standing ops review |

**Ethical boundary:** Hijacking the 1:1 for status extraction teaches people to stop bringing real problems — status belongs in writing.

See: [references/meetings-and-one-on-ones.md](references/meetings-and-one-on-ones.md) when designing a meeting cadence or running a 1:1 — the full 1:1 playbook with agenda templates, staff-meeting design, operation-review roles, and meeting-cost math for when to kill a meeting.

### 5. Decisions and Planning (incl. OKRs)

**Core concept:** The ideal decision moves through free discussion (all views aired, dissent welcome), a clear decision (stated crisply — the more contentious, the crisper), and full support (disagree and commit). Decisions belong at the lowest competent level, closest to current technical knowledge. Planning runs the same arc: assess environmental demand, face present status honestly, close the gap — because the output of planning is decisions and actions taken now, not documents.

**Why it works:** Free discussion surfaces knowledge that lives at the edges; a clear decision prevents the costliest outcome, ambiguity; full support lets the organization move without unanimity. And today's firefight is yesterday's planning failure — planning works on next year's gap, not this week's smoke.

**Key insights:**
- Peer-group syndrome — peers circling, waiting for someone senior to lean — is broken by peer-plus-one: one senior person in the room sanctioned to tip the decision
- Before any decision meeting, answer six questions: what decision, by when, who decides, who is consulted, who ratifies or vetoes, who is informed
- When no one person has both, pair the freshest technical knowledge with the strongest organizational judgment
- Reversing a decision quietly is waffling; reversing it openly on new facts is management
- MBO/OKRs answer two questions: where do I want to go (objective), and how will I pace myself to see I am getting there (key results)
- Keep objectives few and key results measurable enough to score without argument; cascade so one level's key results become the next level's objectives — and never wire them mechanically to compensation

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Architecture choice | Free discussion → clear decision → commit | RFC debated one week; tech lead decides; dissent recorded, then full support |
| Decision prep | Six-question brief | "Pick payments vendor by Jun 30; platform PM decides; eng and finance consulted; VP ratifies" |
| Quarterly planning | Cascading OKRs | Company KR "checkout p95 under 800ms" becomes the platform team's objective |

See: [references/decisions-planning-okrs.md](references/decisions-planning-okrs.md) when prepping a contentious decision or a planning cycle — the six-question brief, peer-group-syndrome counters, three-step planning, and a Grove-style OKR cascade with pitfalls.

### 6. Task-Relevant Maturity, Reviews, and Training

**Core concept:** There is no universally good management style. The right style depends on the subordinate's task-relevant maturity (TRM) — their experience, training, and confidence for this specific task: low TRM calls for structured "how" instruction, medium for mutual reasoning about "what and why", high for agreed objectives with light monitoring. TRM is task-specific, not seniority, so style must shift the moment the task does.

**Why it works:** Mismatched style fails in both directions — hands-off at low TRM is abandonment dressed as empowerment; detailed instruction at high TRM is meddling that destroys ownership. The performance review is where the cost of a mismatch compounds: a year's feedback delivered in the wrong register lands as either neglect or insult.

**Key insights:**
- A star promoted into management is high-TRM on engineering and low-TRM on managing — structure the new task even for your best person
- The performance review is the single most important form of task-relevant feedback a supervisor gives; its only purpose is improving the recipient's performance
- Assess, don't blend: complete the written assessment first, then separately decide which three messages will actually change next year's output
- No surprises: anything that startles the recipient in a review is the supervisor's failure, logged in public
- The ace who is coasting deserves the most review effort — "keep it up" robs your best performer of their next level
- Once lower needs are met, only an ever-rising, self-set bar motivates (the athlete mindset) — and training is the manager's highest-leverage way to raise that bar: deliver it yourself, because outsourcing training outsources standards

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Newly promoted manager | Re-rate TRM per task | Weekly structured 1:1s on hiring and delegation, even for a star engineer |
| Review prep | Assess first, message second | Full written assessment, then the three messages that change next year |
| Team capability | Manager-taught training | EM personally teaches a four-session incident-response course |

See: [references/case-studies.md](references/case-studies.md) when preparing a review or coaching a newly promoted manager — three worked scenarios (meeting-drowned new manager, velocity-up/quality-down, a botched review repaired with TRM coaching).

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Measuring activity, not output | Busyness is gameable and says nothing about results | Count what shipped and survived; pair quantity with quality |
| Publishing unpaired indicators | The team optimizes the number at quality's expense | Add the quality counterpart before the metric goes live |
| Skipping 1:1s when busy | Cancels the highest-leverage 90 minutes on the calendar | Treat 1:1s as forecasted production steps: reschedule, never drop |
| Decisions by rank | Knowledge lives at the lowest competent level; rank silences it | Free discussion, then a clear decision by the named decider |
| OKRs as a compensation formula | Guarantees sandbagged, safe objectives | Keep OKRs a stretch tool; comp weighs more than OKR hit rate |
| One management style for everyone | Abandons the new, smothers the experienced | Match style to task-relevant maturity, task by task |
| Catching defects at the highest-value stage | Cost multiplies at every stage a flaw survives | Inspect specs and plans, not just production |
| Saving feedback for the annual review | It detonates all at once; trust and the year are both lost | No-surprises rule: deliver feedback when the event happens |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you state your team's output in one sentence? | You are managing activity | Define output; build 4-6 indicators around it |
| Does every quantity metric have a quality pair? | The number is being gamed already | Pair it: throughput with escapes, closes with reopens |
| Do you know your team's limiting step? | Flow is built around the wrong constraint | Find where work queues longest; schedule around it |
| Did your reports set the agendas of their last 1:1s? | You ran status meetings instead | Hand the agenda to the subordinate; you take the notes |
| Is 1:1 frequency set by task-relevant maturity? | Someone is over- or under-managed | Weekly for new-to-task, monthly for veterans |
| Was your last big decision made at the lowest competent level? | Rank decided; knowledge watched | Name decider, consulted, and ratifier before the meeting |
| Would your team set the same OKRs if pay weren't attached? | Objectives are sandbagged | Decouple OKRs from the compensation formula |
| Have you personally taught your team anything this quarter? | Highest-leverage activity skipped | Schedule a manager-taught course now |

## Further Reading

- [*"High Output Management"*](https://www.amazon.com/High-Output-Management-Andrew-Grove/dp/0679762884?tag=wondelai00-20) by Andrew S. Grove
- [*"Only the Paranoid Survive"*](https://www.amazon.com/Only-Paranoid-Survive-Exploit-Challenge/dp/0385483821?tag=wondelai00-20) by Andrew S. Grove
- [*"Measure What Matters"*](https://www.amazon.com/Measure-What-Matters-Google-Foundation/dp/0525536221?tag=wondelai00-20) by John Doerr

## About the Author

**Andrew S. Grove** (1936-2016) fled Hungary at twenty, became Intel's third employee, and rose to president, CEO, and chairman, driving the company's famous pivot from memory chips to microprocessors. Time's 1997 Man of the Year, he mentored a generation of Silicon Valley leaders, and his management-by-objectives system became the OKR method now standard across tech.
