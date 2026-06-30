---
name: improve-retention
description: 'Diagnose and fix retention problems using behavior design (B=MAP). Use when the user mentions "users sign up but dont stick around", "activation rate", "onboarding friction", "retention metrics", "why users dont complete", "churn analysis", or "aha moment". Also trigger when analyzing cohort retention curves, designing activation milestones, reducing time-to-value for new users, or investigating why users quit after their first session. Covers the Ability Chain, prompt design, and tiny behaviors that compound. For habit loops and variable rewards, see hooked-ux. For intrinsic motivation, see drive-motivation.'
license: MIT
metadata:
  author: wondelai
  version: "1.4.0"
---

# Behavior Design Framework

Framework for designing products that reliably change behavior. Behavior is not about willpower or motivation — it is a design problem with a predictable equation.

## Core Principle

**The Fogg Behavior Model** = B=MAP. Behavior happens when Motivation, Ability, and a Prompt converge at the same moment.

```
            HIGH ┃
                 ┃   ★ Behavior happens
                 ┃  (above the Action Line)
                 ┃
  Motivation     ┃━━━━━━━━━━━━━━━━━━━━━━━ ← Action Line
                 ┃
                 ┃   ✗ Behavior fails
                 ┃  (below the Action Line)
            LOW  ┃
                 ┗━━━━━━━━━━━━━━━━━━━━━━━━━
                 HARD                    EASY
                        Ability
```

**The Action Line:** When motivation and ability are sufficient, a prompt causes the behavior; below the line, no prompt works. High motivation compensates for low ability and vice versa. The reliable strategy is making behaviors easier (move right), not pumping up motivation (move up).

See: [references/behavior-model.md](references/behavior-model.md) when you need the curve mechanics behind this model — the full Action Line math, behavior types (dot/span/path), and a step-by-step failure diagnostic for a behavior that isn't happening.

## Scoring

**Goal: 10/10.** The six Quick Diagnostic rows are the single source of score-movers. Rate each pass/fail, then start at 10 and subtract per failing row: low motivation or below the Action Line (rows 1-2) cost **-2** each; prompts, celebration, bottleneck, and scaling (rows 3-6) cost **-1.5** each. A design that passes all six scores 10; one that fails every row scores 0. Map to bands: **9-10** = behavior reliably crosses the Action Line at low motivation, prompts are event/anchor-tied, key actions are celebrated; **5-6** = depends on a motivation spike or optimizes a non-bottleneck factor; **<=3** = core action below the Action Line, prompts are spam, no habit wiring. Always state the score and name the specific failing rows.

## The Three Elements

### 1. Motivation

**Core concept:** Motivation is the energy for action, driven by three core motivators, each with two sides: Sensation (pleasure/pain), Anticipation (hope/fear), Belonging (acceptance/rejection). It is powerful but unreliable.

**Why it works:** Motivation comes in waves — it spikes (New Year's resolutions, product launches) and crashes (day 3, week 2). Products that depend on high motivation fail when the wave recedes; the best designs work at the trough.

**Key insights:**
- "Motivation is unreliable. Ability is not." — BJ Fogg
- Design for low-motivation moments, not peak excitement
- Motivation-first tactics (inspiring videos, aspirational messaging) produce spikes, not sustained behavior
- Match required motivation to behavior difficulty — hard behaviors need high motivation

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Onboarding** | Don't count on the new-user spike lasting | First actions work even when excitement fades |
| **Re-engagement** | Assume returning users have low motivation | Show immediate value before asking for effort |
| **Messaging** | Tap the right motivator | Social fitness → belonging; financial tool → hope |

**Copy patterns:**
- "Takes 30 seconds" (signals ease, lowers motivation needed)
- "Join 50,000 teams who..." (belonging motivator)
- "Don't lose your 7-day streak" (anticipation/fear motivator)

**Ethical boundary:** A fear motivator (the streak pattern above) is fair only when the loss is real and user-owned (their data, their progress); never invent a loss that exists solely to drive a session.

See: [references/motivation-waves.md](references/motivation-waves.md) for the three motivators, motivation waves, and designing for troughs.

### 2. Ability

**Core concept:** Ability is the capacity to do the behavior — a function of the scarcest resource across six factors (the Ability Chain). If any single link is too weak, the behavior breaks.

**Why it works:** Unlike motivation, ability can be systematically engineered: every removed field, eliminated step, and preset default moves the behavior right on the model, crossing the Action Line even at low motivation. The Ability Chain gives you the diagnostic — find the weakest link and fix it.

**Key insights:**
- Six factors: Time, Money, Physical Effort, Mental Effort, Social Deviance, Non-Routine
- Simplicity is a function of the scarcest resource — find the bottleneck, not the most obvious factor
- "Simplicity changes behavior" — BJ Fogg
- Starter Steps: shrink the behavior to the tiniest version (2 minutes → 30 seconds → one field)
- Defaults are the most powerful ability tool — users rarely change them

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Signup** | Cut cost across all six factors | One-click SSO removes time, mental effort, non-routine |
| **Core action** | Fix the weakest link | Mental-effort bottleneck → smart defaults and templates |
| **Enterprise adoption** | Address social deviance | "Your team already uses this" reduces social risk |

**Copy patterns:**
- "One click to get started" (time + physical effort)
- "No technical skills needed" (mental effort)
- "Works just like tools you already use" (non-routine)

**Ethical boundary:** Reduce friction only on genuinely valuable behaviors — never make it too easy to overspend, over-share, or delete important data without confirmation.

See: [references/ability-chain.md](references/ability-chain.md) for the six factors in detail, friction audit templates, and simplification strategies.

### 3. Prompt

**Core concept:** The prompt says "do it now." Without one, behavior doesn't happen regardless of motivation and ability. Three types: Person Prompts (internal reminders), Context Prompts (environmental cues), Action Prompts (designed triggers from the product).

**Why it works:** Teams assume motivation + ability is enough — it isn't, not without a well-timed prompt. But prompts only work above the Action Line: a push notification to someone lacking motivation or ability is spam.

**Key insights:**
- A prompt at the wrong moment is noise; at the right moment, magic
- Anchor moments tie new behaviors to existing routines ("After I open Slack, I will...")
- Prompt fatigue is real — every unnecessary prompt degrades the value of future ones

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Notifications** | Prompt only above the Action Line | Send digest when there's content to review, not on a schedule |
| **Re-engagement** | Tie prompts to real events | "Your report is ready" (event-based, not time-based) |
| **Feature discovery** | Prompt when motivation and ability align | Feature tour appears when user hits the problem it solves |

**Copy patterns:**
- "Your weekly report is ready" (context prompt — real event)
- "One thing left to complete your setup" (action prompt with progress)
- Never: "We miss you!" (product need, not user need)

**Ethical boundary:** Every prompt must pass the test "Would I appreciate receiving this right now?" — if it serves a product metric (DAU, re-engagement) but not the user's current goal, cut it.

See: [references/prompt-design.md](references/prompt-design.md) for prompt types, timing strategies, notification design, and anchor moments.

## Tiny Habits Method

The practical application of B=MAP: make behaviors so small they need almost no motivation, anchor them to existing routines, and celebrate immediately.

### The Recipe

```
After I [ANCHOR MOMENT], I will [TINY BEHAVIOR], then I [CELEBRATION].
```

- **Anchor Moment:** an existing routine that reliably happens (opening an app, finishing a meeting, morning coffee).
- **Tiny Behavior:** the smallest version of the target behavior — not "write a report" but "open the report template."
- **Celebration:** an immediate positive emotion that wires the habit. Repetition alone isn't enough — you need the feeling of success.

### Starter Steps

Every target behavior has a Starter Step — the tiniest meaningful version:

| Target Behavior | Starter Step | Why It Works |
|----------------|--------------|--------------|
| Complete onboarding | Fill in one field | Momentum from completion |
| Use analytics daily | Open the dashboard | Seeing data creates curiosity |
| Collaborate with team | Send one comment | Social reciprocity kicks in |

### Scaling Behaviors

Once wired, tiny behaviors grow naturally: open dashboard → check a few metrics → customize → automatic morning habit. Never force scaling — let motivation and momentum drive expansion. The tiny version is the foundation, not a failure.

See: [references/tiny-habits.md](references/tiny-habits.md) for the full Tiny Habits recipe, celebration techniques, and scaling patterns.

## Behavior Design Process

Fogg's systematic process for lasting behavior change:

### Step 1: Clarify the Aspiration
What outcome does the user want — their aspiration, not the product's goal ("stay on top of my team's progress", not "increase DAU").

### Step 2: Explore Behavior Options
List all possible behaviors that could achieve the aspiration. Be exhaustive — don't commit yet.

### Step 3: Match Behaviors
Assess each for motivation and ease; plot on a 2×2 of impact vs. feasibility (Focus Mapping).

### Step 4: Start Tiny
Shrink the best-matched behavior to its Starter Step; design the prompt; add celebration.

### Step 5: Optimize
Expand once wired. Fix bottlenecks with the Ability Chain; refine prompt timing from data.

See: [references/product-applications.md](references/product-applications.md) when applying this process to a specific category — B=MAP mapped to SaaS onboarding, mobile, e-commerce, health, and education with per-category motivation timelines and bottlenecks.

## The Action Line

### Moving Behaviors Above the Action Line

- **Increase Ability (move right)** — remove steps, pre-fill, defaults, templates, wizards. The most reliable approach.
- **Find better Prompts** — anchor to existing routines; event-based beats time-based; trigger when motivation is naturally higher.
- **Increasing Motivation (move up) is unreliable** — if you need motivation tactics, the behavior is probably too hard.

### Retention Diagnostics with B=MAP

Map B=MAP to product metrics:

| Metric | B=MAP Diagnosis | Action |
|--------|----------------|--------|
| **Low activation** | First action below the Action Line | Shrink onboarding to Starter Step; fix weakest Ability Chain link |
| **Day-1 drop-off** | Prompt failed or mistimed | Redesign first-day prompts; anchor to an existing routine |
| **Day-7 drop-off** | Motivation wave receded, behavior too hard | Reduce core action difficulty |
| **Day-30 drop-off** | Habit didn't form, no internal prompt | Create tiny habit recipe; add celebration loops |
| **Low feature adoption** | Feature below the Action Line for most users | Friction-audit it; prompt only when motivation is present |
| **Notification fatigue** | Prompts sent below the Action Line | Cut volume; send only with motivation + ability |

See: [references/case-studies.md](references/case-studies.md) for a worked diagnosis of Instagram, Duolingo, Slack, Calm, and Peloton — read it to see how M, A, and P are scored independently on a real product before diagnosing your own.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **Relying on motivation for retention** | Motivation always recedes; products needing it fail at the trough | Make behaviors tiny enough to survive motivation dips |
| **Ignoring the Ability Chain bottleneck** | You optimized time but the barrier is mental effort or social deviance | Audit all six factors; fix the scarcest resource |
| **Prompting below the Action Line** | Notifications to unmotivated/unable users = spam | Event-based triggers only when motivation + ability suffice |
| **Skipping celebration in onboarding** | Without positive emotion, repetition doesn't wire habits | Add success states and micro-celebrations after key actions |
| **First action too ambitious** | "Complete your profile" is a project, not a behavior | Shrink to Starter Step: one field, one action |
| **Copying products without diagnosing B=MAP** | A high-motivation audience's design fails yours | Diagnose your users' motivation, ability, and prompt context first |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can a new user do the core action in under 60 seconds? | Ability too low | Friction audit; shrink to Starter Step |
| Does the product work when motivation is low? | Design depends on spikes | Redesign core behaviors for minimal motivation |
| Are prompts tied to real events or anchors? | Prompts feel like spam | Switch to event-based or anchor-based prompts |
| Is there immediate feedback after key actions? | No celebration = no habit wiring | Add success states, progress, social feedback |
| Have you found the weakest Ability Chain link? | Optimizing the wrong thing | Rate each of the six factors 1-5 for the core behavior |
| Do users scale naturally from tiny behaviors? | Forcing complexity too early | Starter Steps; let behaviors grow organically |

## Further Reading

Based on BJ Fogg's behavior design research:

- [*"Tiny Habits: The Small Changes That Change Everything"*](https://www.amazon.com/Tiny-Habits-Small-Changes-Everything/dp/0358003326?tag=wondelai00-20) by BJ Fogg
- [*"Designing for Behavior Change: Applying Psychology and Behavioral Economics"*](https://www.amazon.com/Designing-Behavior-Change-Psychology-Behavioral/dp/1492056030?tag=wondelai00-20) by Stephen Wendel (companion: applying behavior science to product design)

## About the Author

**BJ Fogg, PhD** founded the Behavior Design Lab at Stanford University, where he has researched behavior change since 1998. He created the Fogg Behavior Model (B=MAP), coined the term "behavior design", and trained thousands of innovators — including Instagram co-founder Mike Krieger. *Tiny Habits* distills two decades of that research: lasting change comes from behaviors that are tiny, anchored, and celebrated.
