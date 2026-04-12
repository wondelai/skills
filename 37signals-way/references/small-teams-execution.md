# Small Teams and Execution

## Table of Contents

- [The Three-Person Team](#the-three-person-team)
- [Team Autonomy](#team-autonomy)
- [Discovering Scopes](#discovering-scopes)
- [Hill Charts](#hill-charts)
- [Getting Real](#getting-real)
- [Async Communication](#async-communication)
- [Launch Now, Iterate Later](#launch-now-iterate-later)
- [Integrating Design and Programming](#integrating-design-and-programming)

## The Three-Person Team

The fundamental unit of work at 37signals is a team of three: one designer and two programmers, or one designer and one programmer for smaller bets. No project manager. No dedicated QA person. No scrum master. Three people who build the entire thing together.

**Why three:**

- **Communication overhead scales quadratically.** With 3 people, there are 3 communication paths. With 6 people, there are 15. With 10, there are 45. Small teams communicate naturally — in conversations, not meetings.
- **Shared context comes automatically.** Three people working on the same shaped pitch can hold the entire project in their heads. They do not need status documents to stay aligned.
- **Accountability is clear.** When three people own a bet, there is nowhere to hide. Everyone contributes, everyone is responsible.
- **Decision-making is fast.** Three people can make a decision in a five-minute conversation. Ten people need a meeting with an agenda and follow-up action items.

**What the three-person team does not have:**

| Role | Why It Is Absent | What Replaces It |
|------|-----------------|-----------------|
| Project manager | Shaped pitches eliminate ambiguity; small teams self-organize | The team manages itself using hill charts |
| Product manager (during the cycle) | Shaping happens before the cycle; the PM shapes, not manages | The shaper hands off the pitch; the team builds |
| QA engineer | Three people test as they build; scope is small enough to verify | Integrated testing by the building team |
| Scrum master | No sprints, no ceremonies, no process to facilitate | No process overhead — the team just builds |
| Tech lead (separate from the team) | The senior programmer on the team makes technical decisions | Technical leadership comes from within the team |

**What happens when a bet needs more than three people:** It does not get more people. It gets re-shaped. If a shaped pitch requires more than three people, the pitch is too big or too vague. Break it into smaller, independent bets that each fit a three-person team.

## Team Autonomy

Once a team receives a shaped pitch and the cycle begins, they are autonomous. No one assigns them tasks, checks their progress daily, or tells them how to build. They own the entire bet from start to finish.

**What autonomy means in practice:**

- The team decides the technical approach (which frameworks, which database schema, which architecture)
- The team decides the design details (layout, typography, interaction patterns)
- The team decides the build order (which scopes to tackle first, which to defer)
- The team decides when to cut scope (within the boundaries of the pitch's no-gos)
- The team decides when to ship (within the six-week constraint)

**What autonomy does not mean:**

- Ignoring the shaped pitch — the pitch defines the boundaries; the team fills in the details
- Skipping communication — the team posts hill chart updates and writes up decisions for transparency
- Expanding scope — autonomy is freedom within constraints, not freedom to redefine the bet
- Working in isolation — team members collaborate closely with each other; they just do not need external direction

**Why autonomy works:** When people own their work, they bring better judgment, more energy, and more creativity than when they are executing someone else's task list. Autonomy also attracts and retains talented people who want to do meaningful work, not follow instructions.

## Discovering Scopes

When a team receives a shaped pitch, their first job is to discover scopes — named chunks of work that can be built and tracked somewhat independently. Scopes are not pre-defined; the team discovers them by exploring the pitch.

**What a scope is:**

- A meaningful piece of the project that can move through the hill independently
- Named with a descriptive label (e.g., "User Invitations," "Permission Checks," "Email Notifications")
- Big enough to be meaningful (not a single task) but small enough to complete in days, not weeks
- Defined by the team based on their understanding of the work, not by the shaper

**How to discover scopes:**

1. **Read the pitch thoroughly.** Understand the problem, the solution, the rabbit holes, and the no-gos.
2. **Start building.** Do not spend days planning — start with the most uncertain part of the project.
3. **Notice natural boundaries.** As you work, pieces of the project naturally group together. A set of related database changes, a UI component, an integration point — these become scopes.
4. **Name them.** Give each scope a clear, descriptive name. The name should communicate what the scope is about to someone who has not read the code.
5. **Revise as you learn.** Scopes evolve during the cycle. Some merge, some split, some turn out to be unnecessary. This is normal and expected.

**Scopes vs. tasks:**

| Scopes | Tasks |
|--------|-------|
| Named by the team based on discovered structure | Assigned by a PM or tech lead based on a spec |
| Group related work together | Individual work items |
| Track on a hill chart (figuring out → done) | Track in a list (to-do → done) |
| Evolve during the cycle | Fixed at sprint planning |
| Communicate what area is progressing | Communicate whether a checklist item is ticked |

## Hill Charts

Hill charts are the 37signals alternative to burndown charts, percentage-complete metrics, and status meetings. A hill chart shows each scope as a dot on a hill. The left side of the hill is "uphill" (figuring things out), and the right side is "downhill" (executing known work).

**The shape of the hill:**

```
          ·  ← summit (figured out, ready to execute)
         / \
        /   \
uphill /     \ downhill
      /       \
     /         \
____/           \____
figuring out    executing
(uncertainty)   (certainty)
```

**How to read a hill chart:**

- **Dot on the far left:** The team has not started this scope yet.
- **Dot climbing uphill:** The team is exploring, figuring out the approach, encountering unknowns.
- **Dot near the summit:** The core approach is figured out but implementation has not started.
- **Dot going downhill:** The approach is clear and the team is executing — this is the "boring" productive work.
- **Dot at the far right:** The scope is done.

**Why hill charts work better than other progress tracking:**

| Method | Problem | Hill Chart Advantage |
|--------|---------|---------------------|
| Percentage complete | "80% done" can mean "80% of tasks done but the hard 20% remains" | Shows whether uncertainty is resolved or not |
| Burndown chart | Treats all tasks as equal; does not distinguish exploration from execution | Uphill/downhill distinction reveals where the real risk is |
| Status meeting | "It's going well" hides problems until it is too late | A dot stuck uphill for two weeks is a visible red flag |
| Task list | Checked boxes feel like progress even if the hardest work is untouched | Scopes stuck uphill force honest conversation about risk |

**Using hill charts to manage risk:**

The most important thing a hill chart reveals is which scopes are stuck uphill. A scope that has been uphill for more than two weeks is a warning sign — the team is struggling with uncertainty. This triggers a conversation: Is the scope too big? Is there a rabbit hole that was not identified during shaping? Does the scope need to be re-shaped or cut?

**How often to update hill charts:** At least twice per week. Updates should take less than two minutes — just drag the dots to their current position. No written status reports needed.

## Getting Real

"Getting real" is the 37signals principle of working with real materials as early as possible. In software, real materials are HTML, CSS, JavaScript, and real data — not wireframes, not prototypes, not mockups with lorem ipsum.

**What "getting real" looks like:**

- Build the actual interface in the browser on day one or two, not in a design tool
- Use real data (or realistic fake data), not "lorem ipsum" and placeholder content
- Make it functional as fast as possible, even if it is ugly — then improve the design
- Test with real interactions (clicking, typing, navigating), not static screenshots

**Why getting real works:**

- **You discover problems earlier.** Wireframes and mockups hide interaction problems that become obvious when you click through real HTML.
- **You make better design decisions.** Seeing real content in a real browser reveals what works and what does not in a way that static images cannot.
- **You avoid the handoff problem.** When designers work in Figma and engineers implement separately, translation losses are inevitable. When the designer and programmer build together in the browser, the output is the real thing.
- **You ship faster.** The prototype becomes the product. There is no throwaway work.

**Getting real does not mean skipping design:** It means the design happens in the medium of the final product (HTML/CSS) rather than in an intermediate medium (Figma/Sketch). The designer and programmer collaborate in the browser from day one.

## Async Communication

Meetings are toxic at 37signals. Not because meetings are always bad, but because they are almost always overused. A one-hour meeting with six people is not a one-hour meeting — it is six hours of collective time. And most of that time is wasted by the majority who are listening rather than contributing.

**The async-first approach:**

- **Write it up.** If you have something to share, write a message, a document, or a post. People can read it on their own schedule and respond thoughtfully.
- **Record a Loom.** If you need to show something visual, record a 5-minute video walkthrough. It is faster to make than a meeting is to schedule, and everyone can watch at 2x speed.
- **Use hill chart updates.** The hill chart replaces the daily standup. Anyone can see where the project stands by looking at the chart.
- **Reserve meetings for conversations.** Meetings are appropriate when you need real-time back-and-forth to resolve a disagreement or brainstorm. They are not appropriate for status updates, announcements, or information sharing.

**The 37signals communication hierarchy:**

| Need | Method | Why |
|------|--------|-----|
| Status update | Hill chart + async post | No meeting needed; people check on their own time |
| Decision announcement | Written post | Documentation is built-in; everyone gets the same information |
| Design feedback | Loom video + written comments | Async review is more thoughtful than real-time critique |
| Complex problem-solving | Real-time conversation (2-3 people) | Keep it small, keep it focused, keep it short |
| Team alignment | Written pitch or kickoff post | The shaped pitch IS the alignment document |

## Launch Now, Iterate Later

The 37signals philosophy strongly favors shipping over perfecting. Working software in the hands of real users generates more useful feedback in one day than months of internal review.

**What "launch now" means:**

- Ship at the end of the six-week cycle, even if some nice-to-have scopes were cut
- Ship to real users, not to a staging environment for internal review
- Accept that the first version will not be perfect — it should be good, but not perfect
- Plan to iterate in future cycles based on real usage data, not hypothetical feedback

**What "launch now" does not mean:**

- Ship broken software — everything that ships should work correctly
- Skip testing — the building team tests as they build
- Ignore quality — the shipped version should be polished within its reduced scope
- Never improve — iteration is expected; "launch now" is the beginning, not the end

**The iteration cycle:**

1. Ship the first version (end of six-week cycle)
2. Observe real usage during the cool-down period
3. If improvements are needed, shape a follow-up pitch
4. Bring the follow-up pitch to the next betting table
5. If it wins the bet, build the improvement in the next cycle

## Integrating Design and Programming

Traditional product development separates design and engineering into sequential phases: design first, then build. The 37signals approach integrates them from day one. The designer and programmer(s) work together on the same scopes simultaneously.

**How integration works in practice:**

- **Day 1-2:** The designer starts building real HTML/CSS for the core interaction. The programmer sets up the data model and backend. They sync frequently.
- **Day 3-5:** The designer refines the interface while the programmer connects it to real data. They work on the same scope, in the same codebase.
- **Week 2+:** Design and engineering decisions are made together, in context. "Should this be a modal or a page?" is answered by building both and seeing which one works.

**Why integration matters:**

- No handoff problems — the designer sees the real implementation, not a screenshot
- Faster decision-making — questions are resolved in minutes, not in a review meeting next week
- Better solutions — the designer understands technical constraints; the programmer understands design intent
- Single source of truth — the codebase is the design, not a Figma file that may be out of date

**What this requires from the team:**

- Designers must be comfortable working with HTML/CSS or closely pairing with a programmer
- Programmers must care about the user experience, not just the code
- Both must be willing to change their work based on what they learn together
