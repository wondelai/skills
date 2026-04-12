# Case Studies: 37signals Principles in Practice

## Table of Contents

- [Case Study 1: From Scrum to Shape Up](#case-study-1-from-scrum-to-shape-up)
- [Case Study 2: Resisting Feature Creep](#case-study-2-resisting-feature-creep)
- [Case Study 3: Replacing Status Meetings with Hill Charts](#case-study-3-replacing-status-meetings-with-hill-charts)
- [Key Takeaways](#key-takeaways)

## Case Study 1: From Scrum to Shape Up

### Context

A 25-person B2B SaaS company builds project management software for construction firms. They have been running two-week Scrum sprints for three years. The team consists of 4 product managers, 12 engineers, 3 designers, and 6 people in other roles (QA, DevOps, support).

### The Problems

**Sprint planning consumed 20% of productive time.** Every two weeks, the team spent a full day on sprint planning: grooming the backlog, estimating story points, debating priorities, assigning tasks. With two-week sprints, this meant one day out of every ten was spent on ceremony rather than building.

**The backlog had 847 items.** Over three years, the backlog had grown from a focused list to an unmanageable graveyard. The team spent hours each month grooming items they would never build. The backlog created a constant sense of being behind — there was always more to do than could ever be done.

**Teams did not feel ownership.** Engineers received assigned tasks with detailed acceptance criteria. They executed the tasks but did not feel connected to the problems they were solving. Designer mockups were handed off to engineers who implemented them without understanding the design decisions. The result: technically correct but uninspired work.

**Projects regularly overran.** Despite careful estimation with story points, projects consistently took 1.5x to 3x longer than estimated. Extensions were the norm. "One more sprint" became a running joke.

### The Transition

**Phase 1: Abolish the backlog (Week 1)**

The product team exported the backlog to a spreadsheet (for reference, not obligation) and deleted it from the project management tool. The emotional reaction was mixed: some team members felt liberated, others felt anxious about losing their "to-do list." The leadership communicated clearly: "If something is important, it will come back. If it doesn't come back, we didn't need it."

**Phase 2: Learn to shape (Weeks 2-6)**

The two most senior product people (a PM and a designer) spent four weeks learning to shape. They read Shape Up, practiced breadboarding, and shaped three pitches as exercises. Key learnings:
- Shaping is harder than it looks — it requires holding business context, user needs, and technical reality simultaneously
- The appetite concept was the biggest mental shift: "How much is this worth?" instead of "How long will this take?"
- Breadboarding felt awkward at first but proved effective at clarifying flows without getting stuck on visual details

**Phase 3: First six-week cycle (Weeks 7-12)**

Three teams of three (one designer + two engineers) were formed. Each team received one shaped pitch. The remaining engineers handled small batch work (bug fixes, minor improvements) during the same cycle.

Results of the first cycle:
- Two of three teams shipped successfully within six weeks
- One team hit the circuit breaker — their project was not done and was paused
- The team that hit the circuit breaker initially resisted, but after reflecting, agreed the pitch needed reshaping (the rabbit holes were larger than anticipated)
- Total ceremony time dropped from 20% to approximately 3% (one betting table meeting every 8 weeks)

**Phase 4: Iterate and stabilize (Cycles 2-4)**

Over the next three cycles (18 weeks), the company refined their approach:
- Shaping improved — rabbit holes were caught earlier, appetites were more realistic
- Teams learned to cut scope proactively rather than requesting extensions
- Hill charts replaced standup meetings — the team posted updates twice per week
- The circuit breaker fired once more, and the team handled it without drama

### Results After 6 Months

| Metric | Before (Scrum) | After (Shape Up) |
|--------|---------------|-----------------|
| Planning overhead | ~20% of time | ~3% of time |
| Backlog size | 847 items | None (abolished) |
| Projects completed on time | ~40% | ~75% (within fixed cycles) |
| Team satisfaction (survey) | 6.2/10 | 8.1/10 |
| Features shipped per quarter | ~8 | ~10 (with better quality) |
| Time spent in meetings | ~8 hrs/week/person | ~2 hrs/week/person |

### Lessons Learned

1. **The backlog deletion was the hardest step emotionally but the most impactful practically.** Once the list was gone, the team stopped feeling perpetually behind.
2. **Shaping is a skill that takes practice.** The first shaped pitches were too vague. By cycle 3, they were consistently high quality.
3. **The circuit breaker must be applied consistently.** When the team first hit it, there was pressure to extend. Holding the line established credibility.
4. **Not every team adapts at the same speed.** Some engineers thrived with autonomy immediately; others needed a cycle or two to adjust to discovering their own tasks.

## Case Study 2: Resisting Feature Creep

### Context

A 10-person startup builds an email marketing tool for small businesses. After two years, the product has grown from a simple "create and send newsletters" tool to a complex platform with automation workflows, A/B testing, landing page builder, CRM, and advanced analytics. The team is struggling to maintain everything and shipping new features has slowed to a crawl.

### The Problems

**Every customer conversation added features.** Sales calls ended with "They'd sign up if we had X." Support tickets became feature requests. The team treated every request as a mandate, adding features without removing anything.

**Complexity was compounding.** The automation workflow builder interacted with the CRM which interacted with the landing page builder which interacted with the analytics. Changing anything required understanding everything. Bug fixes in one area caused regressions in another.

**New users were overwhelmed.** The onboarding flow required 12 steps. New users had to configure their CRM fields, set up automation rules, and connect their landing pages before they could send a single email. Activation rate had dropped from 60% to 28%.

**The core product was neglected.** The email editor — the thing every user needed — had not been improved in 8 months. All engineering time went to maintaining peripheral features or building new ones.

### The Intervention

The founders read Getting Real and Rework and decided to apply the "build less" philosophy retroactively.

**Step 1: Identify the core job**

They surveyed users with one question: "What is the one thing you use our product for?" 73% of responses mentioned some variation of "send emails to my list." Not automation, not CRM, not landing pages — sending emails.

**Step 2: Audit every feature**

They categorized every feature using the feature audit framework:

| Feature | Usage | Maintenance Cost | Decision |
|---------|-------|-----------------|----------|
| Email editor | High | Medium | Invest heavily |
| Subscriber management | High | Low | Keep, improve |
| Campaign scheduling | High | Low | Keep |
| Basic analytics (open/click) | High | Low | Keep |
| Automation workflows | Low (8% of users) | Very high | Remove |
| A/B testing | Low (5% of users) | Medium | Remove |
| Landing page builder | Low (3% of users) | High | Remove |
| CRM | Low (6% of users) | Very high | Remove |
| Advanced analytics | Low (4% of users) | Medium | Remove |

**Step 3: Cut**

They removed the automation workflow builder, the A/B testing feature, the landing page builder, the CRM module, and advanced analytics. This was painful — these features had taken months to build. But each one was used by fewer than 10% of customers and cost disproportionate engineering time to maintain.

They communicated the changes to affected users with honesty: "We're focusing on making the core email experience excellent. These features are being retired. Here are alternatives that specialize in [automation/CRM/landing pages]. We'll help you export your data."

**Step 4: Reinvest in the core**

With 60% of their codebase removed, the team spent two six-week cycles rebuilding the email editor, simplifying the onboarding (from 12 steps to 3), and making the core sending workflow faster and more reliable.

### Results After 4 Months

| Metric | Before | After |
|--------|--------|-------|
| Codebase size | ~180K lines | ~75K lines |
| Feature count | 14 | 5 |
| Onboarding steps | 12 | 3 |
| Activation rate | 28% | 64% |
| Customer churn | 6.2%/month | 3.8%/month |
| Bug reports per week | ~22 | ~5 |
| Time to ship a new improvement | 4-6 weeks | 1-2 weeks |
| Engineering time on maintenance | ~55% | ~20% |

### Lessons Learned

1. **Removing features is harder socially than technically.** The code deletion was easy; explaining it to affected customers was hard but necessary.
2. **A small percentage of vocal users drove most feature requests.** The 8% who used automation were the loudest, but the 92% who just wanted good email tools were the majority.
3. **Simplification improved everything.** Fewer features meant fewer bugs, faster development, easier onboarding, and lower churn. The product was better in every measurable way.
4. **You can always add later.** The fear was that removing features was permanent. In reality, the team retained the option to re-add features as independent, well-shaped bets if demand justified it. So far, demand has not.

## Case Study 3: Replacing Status Meetings with Hill Charts

### Context

A 15-person design and engineering team at a mid-size company builds internal tools. They have weekly one-hour status meetings where each of the 5 project leads presents their progress. In addition, there are daily 15-minute standups per team (3 teams, 15 minutes each).

### The Problems

**Status meetings were theater.** Project leads spent 30 minutes preparing slides for the weekly meeting. During the meeting, most attendees listened passively while one person presented. The information was stale by the time it was shared — things had changed since the slides were prepared.

**"Percentage complete" was meaningless.** Project leads reported progress as percentages: "We're 70% done." But 70% done could mean "the easy 70% is done and the hard 30% remains" or "we're 70% through the timeline but only 40% through the complexity." Percentages created a false sense of precision.

**Daily standups were ritualistic.** Team members recited "what I did yesterday, what I'll do today, any blockers" without genuine engagement. The standup ran on autopilot — it was a habit, not a tool. Real problems were discussed after the standup, in smaller groups.

**Problems were hidden until late.** Because percentage-complete tracked tasks (not understanding), a scope that was "on track" could suddenly be "in trouble" when the team hit an unexpected complexity. The status meeting format did not surface this risk early enough.

### The Transition

**Week 1: Introduce hill charts**

The team adopted hill charts for all active projects. Each project identified 4-8 scopes and placed them on the hill. Initial positions:

- Most scopes started on the left side of the hill (uphill — still figuring things out)
- A few scopes started near the summit or on the downhill side (approach was clear)

**Week 2: Replace standup with async updates**

Daily standups were replaced with twice-weekly hill chart updates. Each team updated their hill chart positions and optionally wrote a one-paragraph note for any scope that moved significantly or got stuck.

**Week 3: Replace weekly status meeting with hill chart review**

The one-hour weekly status meeting was replaced with a 20-minute hill chart review. Instead of presentations, the group looked at the hill charts and focused only on scopes that were:
- Stuck uphill for more than a week (risk signal)
- Moving backward (the team discovered something harder than expected)
- Missing from the chart (a scope the team had not started yet)

### How Hill Charts Changed the Conversation

**Before (percentage-complete):**

> "The reporting feature is about 60% complete. We're on track."
> "Great, any blockers?"
> "No blockers right now."
> (Two weeks later: "Actually, the reporting feature is going to need another sprint. We hit some complexity with the data aggregation layer.")

**After (hill charts):**

> "The 'Report Templates' scope is moving downhill — we know what to build and we're executing. But 'Data Aggregation' has been uphill for a week. We're still figuring out how to handle cross-timezone calculations."
> "That's a risk. Is the appetite still right for this, or does 'Data Aggregation' need to be re-scoped?"
> "Let's simplify — what if we only support one timezone per report for v1?"
> "That works. Move it to the summit."

The hill chart made the risk visible two weeks earlier and prompted a scope-cutting conversation that kept the project on track.

### Results After 3 Months

| Metric | Before | After |
|--------|--------|-------|
| Time in status meetings per week | 3.25 hrs/person (1hr weekly + 0.75hr standups) | 0.5 hrs/person (20min review + 10min async updates) |
| Time to surface a stuck scope | 1-2 weeks (at next status meeting) | 2-3 days (next hill chart update) |
| "Surprise" project problems per quarter | 4-5 | 0-1 |
| Meeting preparation time per week | 30 min (slides) | 2 min (drag dots) |
| Sense of progress (team survey) | "We report progress" | "We see progress" |

### What Made It Work

1. **Hill charts separate uncertainty from execution.** The uphill/downhill distinction gives an honest view of where the real risk is, which percentage-complete cannot.
2. **Async updates respect focus time.** Writing a one-paragraph update takes 2 minutes and does not interrupt anyone's flow. A standup interrupts everyone's morning.
3. **Short meetings focus on risk, not reports.** The 20-minute review only discusses scopes that are stuck or moving backward. Good news is visible on the chart — it does not need to be presented.
4. **Visual progress is motivating.** Seeing scopes move across the hill provides a tangible sense of progress that task lists and percentages do not.

## Key Takeaways

Across all three case studies, several themes emerge:

**1. Simplification improves outcomes.** In every case, removing process, removing features, or removing meetings led to better results. The instinct to add more is almost always wrong.

**2. Honesty enables speed.** Hill charts show real risk. Appetite forces honest scoping. The circuit breaker forces honest assessment of progress. When the team is honest about where things stand, problems are caught early and addressed quickly.

**3. Autonomy produces better work.** Teams that discover their own tasks, cut their own scope, and manage their own progress do better work than teams that follow instructions. Autonomy requires trust, and trust requires boundaries (shaped pitches, appetites, hill charts).

**4. Transitions are uncomfortable.** Every team experienced discomfort when changing their process. The backlog deletion felt risky. The first circuit breaker felt harsh. Removing status meetings felt like losing control. In every case, the discomfort faded within one or two cycles as the new approach proved itself.

**5. The framework adapts to context.** No team implemented Shape Up exactly as described in the book. Each adapted the principles to their size, domain, and culture. The six-week cycle is not sacred — the principles behind it (fixed time, variable scope, shaped work, small teams) are what matter.
