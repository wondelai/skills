# Betting and Cycles

## Table of Contents

- [Why Not Backlogs](#why-not-backlogs)
- [The Betting Table](#the-betting-table)
- [Six-Week Cycles](#six-week-cycles)
- [The Circuit Breaker](#the-circuit-breaker)
- [Cool-Down Periods](#cool-down-periods)
- [Fixed Time, Variable Scope](#fixed-time-variable-scope)
- [Cycle Planning in Practice](#cycle-planning-in-practice)
- [When to Use Small Batches](#when-to-use-small-batches)

## Why Not Backlogs

A backlog is a growing list of ideas, requests, and tasks that theoretically represent future work. In practice, backlogs create more problems than they solve.

**The problems with backlogs:**

1. **Backlogs grow forever.** Items are added faster than they are completed. A 200-item backlog is not a plan — it is an anxiety list.

2. **Backlogs create false obligations.** Once an idea is in the backlog, it feels like a commitment. Teams spend time grooming, prioritizing, and re-prioritizing items that may never be built.

3. **Backlogs dilute focus.** When everything is in the backlog, nothing stands out. The important is buried alongside the trivial.

4. **Backlogs discourage fresh thinking.** Instead of evaluating each cycle on its own merits, teams default to pulling from the backlog — recycling old ideas instead of responding to current reality.

5. **Backlogs are emotionally draining.** Team members see hundreds of items and feel perpetually behind. The list never gets shorter. Morale suffers.

**The 37signals alternative:** No backlogs. Ideas are either shaped into pitches and bet on for the next cycle, or they are let go. If an idea is truly important, it will come back — someone will bring it up again, or the problem will resurface. If it does not come back, it was not important enough to build.

**But what about good ideas we might forget?** Some ideas do deserve to be saved. The key is who saves them and how. Individual team members can keep their own informal lists. A senior person can maintain a short list of potential pitches to shape. But there is no shared, groomed backlog that creates obligations for the team.

## The Betting Table

The betting table is a meeting that happens at the end of each cool-down period, before the next cycle begins. A small group of senior stakeholders reviews shaped pitches and decides which ones to bet on.

**Who attends the betting table:**

- The CEO or product owner (final decision authority)
- A senior technical person (can assess feasibility)
- A senior designer or product strategist (can assess solution quality)
- Optionally, one or two other senior people with relevant context

This is not a democratic process. The betting table is small by design — 2-4 people, never more. Too many voices leads to compromise, and compromise produces mediocre bets.

**How the betting table works:**

1. **Review pitches.** The group reads the shaped pitches (written documents, not presentations). Each pitch takes 5-10 minutes to review.

2. **Discuss trade-offs.** For each pitch, discuss: Is this the right problem? Is the appetite appropriate? Does the solution address the problem well enough? Are the rabbit holes handled?

3. **Place bets.** Decide which pitches get a team for the next cycle. A bet means committing a team for 6 weeks. This is real commitment — once a bet is placed, the team is protected from interruption.

4. **Say no to the rest.** Most pitches do not get bet on. This is healthy and expected. The rejected pitches are not added to a backlog — they are simply not bet on this cycle.

**What makes a good bet:**

| Factor | Strong Bet | Weak Bet |
|--------|-----------|----------|
| Problem clarity | Specific, concrete user scenario | Vague goal ("improve engagement") |
| Solution quality | Shaped, with breadboards and no-gos | Half-baked idea or unshaped request |
| Appetite match | Solution clearly fits the time budget | Solution seems too big or too uncertain |
| Strategic fit | Aligns with current business priorities | Nice-to-have with no urgency |
| Risk level | Rabbit holes identified and addressed | Major unknowns unresolved |

## Six-Week Cycles

Six weeks is the standard cycle length at 37signals. It is long enough for a small team to build something meaningful, and short enough to maintain urgency and limit the damage of a wrong bet.

**Why six weeks, not two-week sprints:**

- **Two weeks is too short** for meaningful work. Teams spend a disproportionate amount of time on planning, estimating, and ceremony relative to actual building.
- **Six weeks is long enough** for a designer and one or two programmers to build a significant feature from start to finish, including design, code, testing, and polish.
- **Six weeks creates natural urgency.** In the first week or two, the team explores the problem and discovers tasks. By week three, they should be executing. By week five, they should be cutting scope and converging. Week six is finish and polish.

**Why not longer than six weeks:**

- **Projects longer than six weeks lose urgency.** The deadline feels distant, and teams defer hard decisions.
- **Longer timelines increase risk.** The more time you invest before shipping, the more you lose if the bet was wrong.
- **Large projects should be broken into independent six-week bets.** If a feature genuinely needs 12 weeks, shape it into two independent six-week pieces, each of which delivers value on its own.

**The rhythm of a six-week cycle:**

| Week | Phase | Activity |
|------|-------|----------|
| 1 | Exploration | Team reads the pitch, explores the problem, discovers scopes |
| 2 | Exploration → Building | Scopes take shape, first code and design emerge |
| 3 | Building | Core functionality coming together, biggest uncertainties resolved |
| 4 | Building | Integration, edge cases, testing begins |
| 5 | Convergence | Scope cutting begins — what is not essential gets cut |
| 6 | Convergence → Ship | Polish, final testing, deployment |

## The Circuit Breaker

The circuit breaker is the most important and most controversial element of the 37signals methodology. It is simple: if a project is not done at the end of its six-week cycle, it does not automatically continue. It stops.

**How the circuit breaker works:**

1. A team is given a six-week bet.
2. At the end of six weeks, the work is either done or it is not.
3. If it is done, it ships.
4. If it is not done, it does not get an automatic extension. The project is paused and returned to the shaping table.
5. If the problem is still important, a new pitch is shaped (possibly re-scoped) and brought to the next betting table. It competes with other pitches on its merits.

**Why the circuit breaker exists:**

- **Prevents zombie projects.** Without a circuit breaker, projects in trouble get extensions, then more extensions, consuming resources while delivering diminishing returns.
- **Forces honest shaping.** If you know the circuit breaker is real, you shape more carefully. You cut scope more aggressively. You identify rabbit holes more diligently.
- **Protects team morale.** Struggling teams are freed from death marches. A fresh start with better shaping is more humane and more effective than grinding through.
- **Keeps the betting table honest.** When bets that do not pay off are stopped, stakeholders take the betting process more seriously.

**When to invoke the circuit breaker:**

- The team has significant unfinished work that cannot be completed with a few extra days
- The core approach turned out to be wrong and needs re-thinking
- New information has changed the value of the project
- The team is demoralized and grinding rather than building with momentum

**When not to invoke it:**

- The work is 90%+ complete and needs only a few days of polish — some flexibility is reasonable
- External dependencies (not the team's fault) caused delays — address the dependency issue separately

**Common objections and responses:**

| Objection | Response |
|-----------|----------|
| "We'll lose all the work we did" | The code and knowledge remain. The next pitch can build on what was learned. |
| "It will demoralize the team" | Extending a struggling project is more demoralizing. A fresh start is a gift. |
| "We're so close, just one more week" | If one more week would fix it, the team would have found that scope cut during week 5. |
| "The customer is waiting" | Better to re-shape and deliver something good than to ship something half-finished. |

## Cool-Down Periods

Between every six-week cycle, there is a two-week cool-down period. This is not vacation time, but it is unstructured time — no assigned projects, no obligations, no pressure.

**What happens during cool-down:**

- **Bug fixes.** Small bugs that accumulated during the cycle get addressed.
- **Exploration.** Team members pursue ideas that interest them — potential future pitches, new technology experiments, side projects.
- **Technical maintenance.** Dependency updates, infrastructure improvements, small refactors.
- **Recovery.** After six weeks of focused building, people need time to decompress and reset.

**Why cool-down matters:**

- **Prevents burnout.** Back-to-back cycles with no breaks create unsustainable pace.
- **Creates slack for emergencies.** If something urgent arises, the cool-down absorbs it without disrupting a cycle.
- **Generates fresh ideas.** Unstructured time produces the insights and experiments that become future pitches.
- **Maintains quality.** Technical debt accumulates during focused cycles; cool-down is when it gets addressed.

**Cool-down is also when the betting table meets.** Senior people use the cool-down to review shaped pitches, discuss priorities, and decide what to bet on for the next cycle.

## Fixed Time, Variable Scope

This is the fundamental inversion that makes the 37signals methodology work. Traditional projects fix the scope and let the timeline flex. Shape Up fixes the timeline and lets the scope flex.

**How scope flexing works:**

1. A team receives a shaped pitch with a six-week appetite.
2. During weeks 1-2, they explore the pitch and discover scopes (named chunks of work).
3. During weeks 3-4, they build the core scopes.
4. During weeks 5-6, they evaluate remaining scopes. Nice-to-haves that do not fit are cut. Must-haves get the remaining time.
5. At the end of week 6, whatever is done ships. Whatever was cut was either not essential or can be addressed in a future bet.

**What makes scope cutting work:**

- **The pitch defines what is essential.** The shaped solution identifies the core problem and the core flow. Everything else is negotiable.
- **No-gos set explicit boundaries.** Things that are already excluded in the pitch cannot creep back in.
- **The team has autonomy.** Because the team discovered their own scopes, they understand which ones are essential and which are nice-to-have. They can make intelligent cut decisions.

**The beauty of variable scope:** When you fix the time and flex the scope, every bet has a bounded downside. The worst case is six weeks of work with a reduced scope shipped. The best case is the full solution in six weeks. Either way, the team moves on to the next cycle with a fresh start.

## Cycle Planning in Practice

**Before the cycle (cool-down period):**

1. Shapers prepare pitches for problems worth solving
2. Pitches are shared as written documents for asynchronous review
3. The betting table meets to review pitches and place bets
4. Bets are communicated to teams with the full shaped pitch

**During the cycle (six weeks):**

1. Week 1: Team reads the pitch, explores the territory, identifies scopes
2. Week 2: Scopes solidify, uphill work on biggest unknowns begins
3. Weeks 3-4: Core building, scopes move downhill, integration happens
4. Week 5: Scope cutting decisions, convergence begins
5. Week 6: Polish, testing, deployment

**After the cycle:**

1. Work ships (or the circuit breaker fires)
2. Cool-down begins — two weeks of unstructured time
3. The cycle repeats

## When to Use Small Batches

Not everything needs a six-week cycle. Small batches (1-2 week projects) are appropriate for:

- Bug fixes that need more than a quick patch
- Small improvements that users have been requesting
- Experiments or proofs of concept
- Internal tooling improvements

**How small batches fit the cycle:**

- Small batches are also bet on at the betting table
- Multiple small batches can run in a single cycle (one team does 3-4 small projects in six weeks)
- Small batches still have a fixed time constraint — 1-2 weeks per project
- The circuit breaker still applies — if a "1-week project" is not done in 1 week, stop and re-evaluate

**The key distinction:** Small batches are for work that is already well-understood and does not need extensive shaping. If a small project keeps growing, it probably needs to be shaped as a full six-week bet instead.
