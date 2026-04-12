# Shaping the Work

## Table of Contents

- [What Shaping Is](#what-shaping-is)
- [Properties of Shaped Work](#properties-of-shaped-work)
- [Setting the Appetite](#setting-the-appetite)
- [Breadboarding](#breadboarding)
- [Fat Marker Sketches](#fat-marker-sketches)
- [The Pitch Format](#the-pitch-format)
- [Identifying Rabbit Holes](#identifying-rabbit-holes)
- [Defining No-Gos](#defining-no-gos)
- [Who Does the Shaping](#who-does-the-shaping)
- [Shaping in Practice](#shaping-in-practice)

## What Shaping Is

Shaping is the work you do before the work. It happens at the intersection of product strategy, design thinking, and technical reality. The goal is to take a raw idea — a customer request, a business opportunity, a nagging problem — and transform it into something a small team can build in a fixed amount of time.

Shaping is not writing a spec. Specs are too detailed — they remove the team's ability to make creative decisions. Shaping is not writing a user story. User stories are too vague — they leave too many open questions for the team to resolve under time pressure. Shaping sits in between: detailed enough that the main approach is clear, rough enough that the team has room to work out the specifics.

**What shaping replaces:**

| Traditional Approach | Problem | Shaping Alternative |
|---------------------|---------|-------------------|
| Detailed specification | Too rigid; team becomes ticket-takers | Shaped pitch with room to maneuver |
| User story ("As a user I want...") | Too vague; team discovers scope problems mid-sprint | Shaped pitch with solution sketched out |
| Wireframes and mockups | Too concrete; invites pixel-level debate too early | Breadboards and fat marker sketches |
| Story point estimation | Focuses on how long, not how much it is worth | Appetite: "This is worth 2 weeks of work" |
| Sprint planning with a backlog | Picks from an ever-growing list of undifferentiated items | Betting table selects from freshly shaped pitches |

## Properties of Shaped Work

Shaped work has three essential properties. If any one is missing, the work is not ready to bet on.

**1. Rough.** The solution is sketched at the right level of abstraction. There are no wireframes, no pixel-level designs, no detailed task lists. The team has room to interpret the solution and make their own design and technical decisions. Roughness is intentional — it signals to the team that they own the details.

**2. Solved.** Despite being rough, the main elements of the solution are worked out. The shaper has thought through the core flow, identified the key interactions, and resolved the biggest design questions. The team should not have to figure out the fundamental approach — that is the shaper's job. They should figure out the details within that approach.

**3. Bounded.** The scope is explicitly limited. The appetite sets a time boundary. No-gos set feature boundaries. Rabbit holes are identified and addressed. The team knows what they are building and — just as importantly — what they are not building.

**How to tell if work is properly shaped:**

- Can you explain the solution in under 5 minutes using only words and rough sketches?
- Does the solution address the customer's core problem without unnecessary extras?
- Could a small team start building on day one without asking "but what about...?"
- Are the known risks called out and addressed?
- Is it clear what is out of scope?

If the answer to any of these is no, the work needs more shaping.

## Setting the Appetite

The appetite is a time budget that reflects how much the problem is worth. This is fundamentally different from estimation.

**Estimation asks:** "How long will this take?" The answer depends on the solution, which depends on scope, which depends on what the team discovers, which means the answer is a guess that grows under pressure.

**Appetite asks:** "How much time is this problem worth to us?" The answer is a strategic decision made before a solution exists. It constrains the solution rather than the solution dictating the timeline.

**Appetite sizes:**

| Size | Duration | Team | Typical Use |
|------|----------|------|-------------|
| Small batch | 1-2 weeks | 1-2 people | Bug fixes, small improvements, experiments |
| Large batch | 6 weeks | 2-3 people | New features, significant improvements, redesigns |

There is no "3-week appetite" or "4-month appetite." The constraint of fixed sizes forces honest classification: either this is small enough for a quick batch, or it is worth a full cycle. If it seems like it is in between, it needs more shaping to fit one size or the other.

**How appetite changes the conversation:**

- Without appetite: "How long will the reporting feature take?" "6-8 weeks." "Can you do it in 4?" (negotiation over fiction)
- With appetite: "We think a basic reporting feature is worth a 6-week bet. Can you shape something that solves the core need within that appetite?" (creative problem-solving within constraints)

## Breadboarding

A breadboard is an interaction design sketch that uses only words and arrows. No layout, no visual design, no color, no images. Just three elements:

**Places** — screens, dialogs, or pages the user can navigate to. Written as nouns.

**Affordances** — things the user can interact with at each place. Written as verbs or interactive elements (buttons, fields, links).

**Connection lines** — arrows showing how affordances lead to other places.

**Example breadboard: "User invites a teammate"**

```
[Project Settings]
  - "Invite" button
      ↓
[Invite Form]
  - Email field
  - Role selector (Admin / Member)
  - "Send Invite" button
      ↓
[Confirmation]
  - "Invitation sent to {email}" message
  - "Send another" link → [Invite Form]
  - "Done" link → [Project Settings]
```

**Why breadboards work:**

- They force you to think about flow before layout
- They are fast to create and easy to change
- They prevent premature conversations about visual design
- They reveal missing steps and edge cases in the interaction
- Anyone can read them — no design tools required

**When not to use breadboards:** When the challenge is primarily visual (a new data visualization, a complex responsive layout), a fat marker sketch is more appropriate.

## Fat Marker Sketches

A fat marker sketch is a visual sketch drawn at low fidelity — as if you were using a thick marker on a whiteboard. The thick line prevents you from drawing details like specific fonts, exact spacing, or precise button sizes. It forces you to think about arrangement and emphasis rather than polish.

**Rules for fat marker sketches:**

1. Draw on paper or a tablet with a thick brush — never in a design tool
2. No text labels (or very few) — use blocks and shapes to represent content areas
3. No color — grayscale only
4. No precise alignment — rough positioning is the point
5. Show the most important element prominently; let everything else recede

**What fat marker sketches communicate:**

- The relative priority of elements on a page (what is big, what is small)
- The general layout approach (sidebar? stacked? tabbed?)
- Which elements exist and which do not
- The relationship between content areas

**What they intentionally do not communicate:**

- Exact spacing, sizing, or alignment
- Typography choices
- Color or visual styling
- Responsive behavior
- Interaction states

This intentional vagueness is a feature. It gives the building team freedom to design the details while keeping the strategic layout decisions intact.

## The Pitch Format

A pitch is the shaped work packaged for the betting table. It is a written document — not a slide deck, not a verbal presentation — because writing forces clarity and allows asynchronous review.

**Five elements of a pitch:**

**1. Problem.** What is the problem or opportunity? Describe it from the user's perspective. Include a specific story or scenario that makes the problem concrete. Avoid abstract descriptions.

**2. Appetite.** How much time is this worth? Small batch (1-2 weeks) or large batch (6 weeks). This is a strategic decision, not a technical estimate.

**3. Solution.** The shaped solution, presented with breadboards and/or fat marker sketches. Show the core flow and key interactions. Keep it rough — enough to understand the approach, not enough to copy pixel-by-pixel.

**4. Rabbit holes.** Known risks and complexities that could blow up the scope. For each rabbit hole, explain how the solution addresses it or avoids it. If a rabbit hole cannot be mitigated, it may mean the pitch is not ready.

**5. No-gos.** Explicit statements about what the solution will not include. These prevent scope creep by making boundaries visible and non-negotiable. "We will not support bulk invitations in this version" is a no-go.

**Pitch length:** A pitch should take 5-10 minutes to read. If it takes longer, the solution is probably not shaped well enough — it is either too detailed or too complex.

## Identifying Rabbit Holes

Rabbit holes are the parts of a project that look simple on the surface but contain hidden complexity that can consume weeks of work. The shaper's job is to identify them before the team encounters them.

**Common rabbit hole patterns:**

| Pattern | Example | How to Address |
|---------|---------|---------------|
| Permissions complexity | "Who can see what when a user is shared across projects?" | Simplify the permission model; define only 2 roles for v1 |
| Data migration | "Existing users have data in the old format" | Define a simple migration path or make new feature new-only |
| Edge case explosion | "What if the user has 10,000 items?" | Set a practical limit and document it as a no-go |
| Integration dependency | "This needs the payment provider to support X" | Verify support exists before betting; if not, it is a no-go |
| Performance cliff | "This query will be slow at scale" | Shape the solution to avoid the expensive query (pagination, caching) |

**How to spot rabbit holes during shaping:**

1. Walk through the solution step by step and ask "What could go wrong here?"
2. For each interaction, ask "Is there a simpler version that achieves 80% of the value?"
3. Look for words like "just," "simply," or "obviously" in your own thinking — they often mask complexity
4. Ask an engineer to review the pitch for technical rabbit holes
5. Ask a designer to review for interaction rabbit holes

## Defining No-Gos

No-gos are explicit boundaries that prevent scope creep during the build. They state what the solution will not include, even if those exclusions seem like obvious additions.

**Why no-gos matter:**

- They prevent the building team from expanding scope based on their own good judgment
- They make trade-offs visible to the betting table
- They give teams permission to not build something without feeling like they are cutting corners
- They make the appetite honest — the solution fits the time budget because these things are excluded

**Good no-go examples:**

- "No bulk operations in v1 — users invite one person at a time"
- "No custom notification schedules — we pick a sensible default"
- "No mobile-responsive version for this feature — desktop only"
- "No CSV import — users enter data manually or use the API"
- "No undo — actions are confirmed before execution"

**Bad no-go examples (too vague):**

- "No over-engineering"
- "Keep it simple"
- "Don't spend too much time on edge cases"

No-gos must be specific and concrete. A team member should be able to look at a no-go and immediately know whether their current work violates it.

## Who Does the Shaping

Shaping is a senior role. The shaper needs to understand the business context (which problems are worth solving), the user perspective (what workflows look like), and the technical landscape (what is easy and what is hard to build). This rare combination usually means shaping is done by a founder, a senior product person, or a senior designer who is technically fluent.

**Shaping is not a committee activity.** One or two people shape a pitch. They may consult others — an engineer for technical feasibility, a support person for common complaints — but the shaping itself is done by a small number of people who can hold the whole picture in their head.

**Shaping is not the building team's job.** If the team doing the building also does the shaping, they end up shaping during the build, which defeats the purpose. The building team's job is to take a shaped pitch and figure out the implementation details. The shaper's job is to make sure the pitch is ready for that.

## Shaping in Practice

**Step 1: Set the appetite.** Before exploring solutions, decide how much time the problem is worth. This prevents the shaper from accidentally designing a 3-month solution for a 2-week problem.

**Step 2: Narrow the problem.** Move from a broad problem ("reporting is bad") to a specific scenario ("managers need to know which projects are behind schedule this week"). The narrower the problem, the easier it is to shape a bounded solution.

**Step 3: Sketch the solution.** Use breadboards for flow-heavy problems and fat marker sketches for layout-heavy problems. Work quickly — if the sketch takes more than 30 minutes, the problem might need more narrowing.

**Step 4: Identify rabbit holes.** Walk through the solution and flag anything that could blow up. Address each one: simplify, exclude, or find a workaround.

**Step 5: Define no-gos.** Write down what the solution will not include. Be specific.

**Step 6: Write the pitch.** Package everything into the five-element pitch format. Share it for review before bringing it to the betting table.

**Time investment:** Shaping a single pitch typically takes 1-3 days of focused work, spread over a week or two. This is a fraction of the time the building team will spend, but it dramatically reduces the risk of building the wrong thing.
