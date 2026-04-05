---
name: improve-retention
description: 'Diagnose and fix retention problems using behavior design (B=MAP). Use when the user mentions "users drop off", "activation rate", "onboarding friction", "retention metrics", "why users dont complete", "churn analysis", "user activation", or "aha moment". Also trigger when analyzing cohort retention curves, designing activation milestones, reducing time-to-value for new users, or investigating why users stop after their first session. Covers the Ability Chain, prompt design, and tiny behaviors that compound. For habit loops and variable rewards, see hooked-ux. For intrinsic motivation, see drive-motivation.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Behavior Design Framework

Framework for designing products that reliably change behavior. Based on a fundamental truth: behavior is not about willpower or motivation—it is a design problem with a predictable equation.

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

**The Action Line:** When motivation and ability are sufficient, a prompt causes the behavior. Below the line, no prompt works. The line curves: high motivation compensates for low ability, and high ability compensates for low motivation. The reliable strategy is to make behaviors easier (move right), not to pump up motivation (move up).

## Scoring

**Goal: 10/10.** When reviewing or creating product behavior design, rate them 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## The Three Elements

### 1. Motivation

**Core concept:** Motivation is the energy for action. It has three core motivators, each with two sides: Sensation (pleasure/pain), Anticipation (hope/fear), and Belonging (acceptance/rejection). Motivation is powerful but unreliable — it fluctuates like waves.

**Why it works:** Motivation explains why people want to act, but it is the least reliable element in behavior design. It spikes (New Year's resolutions, product launches) and crashes (day 3, week 2). Products that depend on high motivation fail when the wave recedes. The best designs work even when motivation is at a trough.

**Key insights:**
- Three core motivators: Sensation (pleasure/pain), Anticipation (hope/fear), Belonging (acceptance/rejection)
- Motivation comes in waves — it is not a stable resource you can count on
- Design for low-motivation moments, not peak motivation
- "Motivation is unreliable. Ability is not." — BJ Fogg
- Motivation-first strategies (inspiring videos, aspirational messaging) produce spikes, not sustained behavior
- Match the required motivation level to the behavior's difficulty — hard behaviors need high motivation

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Onboarding** | Don't rely on new-user motivation spike lasting | Design first actions to work even when excitement fades |
| **Re-engagement** | Assume returning users have low motivation | Show immediate value before asking for effort |
| **Feature adoption** | Match motivation to difficulty | Simple features need low motivation; complex ones need motivation boosters |
| **Messaging** | Tap into the right motivator | Social fitness → belonging; financial tool → anticipation (hope) |
| **Churn prevention** | Diagnose if motivation dropped or was never high | Survey churned users for motivational misalignment |

**Copy patterns:**
- "Takes 30 seconds" (reduces motivation needed by signaling ease)
- "Join 50,000 teams who..." (belonging motivator)
- "See your progress instantly" (anticipation/hope motivator)
- "Don't lose your 7-day streak" (anticipation/fear motivator)
- Avoid motivation-heavy copy for routine actions — save it for hard asks

**Ethical boundary:** Never manufacture false hope or exploit fear to inflate motivation. Motivation tactics should connect users to genuine outcomes, not create anxiety that drives compulsive usage.

See: [references/motivation-waves.md](references/motivation-waves.md) for deep dive on the three motivators, motivation waves, and designing for troughs.

### 2. Ability

**Core concept:** Ability is the capacity to do the behavior. It is a function of the scarcest resource across six factors — the Ability Chain. If any single link is too weak (too expensive, too time-consuming, too confusing), the behavior breaks. Simplicity is not a single dimension — it is always relative to the person and context.

**Why it works:** Making behaviors easier is the most reliable strategy in behavior design. Unlike motivation, ability can be systematically engineered. Every field you remove, every step you eliminate, every default you set moves the behavior to the right on the Fogg Behavior Model, crossing the Action Line even at low motivation. The Ability Chain provides a diagnostic: find the weakest link and fix it.

**Key insights:**
- The Ability Chain has six factors: Time, Money, Physical Effort, Mental Effort, Social Deviance, Non-Routine
- Simplicity is a function of the scarcest resource — find the bottleneck
- "Simplicity changes behavior" — BJ Fogg
- A friction audit finds the weakest link in the Ability Chain for each key behavior
- Starter Steps: shrink the behavior to the tiniest version (2 minutes → 30 seconds → one field)
- Default settings are the most powerful ability tool — users rarely change defaults

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Signup** | Minimize Ability Chain cost across all six factors | One-click SSO eliminates time, mental effort, and non-routine |
| **Core action** | Find and fix the weakest link in the chain | If mental effort is the bottleneck, add smart defaults and templates |
| **Mobile experience** | Optimize for physical effort and time constraints | Pre-filled forms, thumb-friendly targets, minimal typing |
| **Enterprise adoption** | Address social deviance and non-routine factors | "Your team already uses this" reduces social risk |
| **Friction audit** | Systematically test each of the six factors | Walk through each factor for every key behavior and rate 1-5 |

**Copy patterns:**
- "One click to get started" (time + physical effort)
- "Free forever for small teams" (money)
- "No technical skills needed" (mental effort)
- "Used by teams at Google, Stripe, and Shopify" (social deviance — it's normal)
- "Works just like tools you already use" (non-routine)

**Ethical boundary:** Reducing friction should make genuinely valuable behaviors easier. Never reduce friction on harmful actions (e.g., making it too easy to overspend, over-share, or delete important data without confirmation).

See: [references/ability-chain.md](references/ability-chain.md) for the six factors in detail, friction audit templates, and simplification strategies.

### 3. Prompt

**Core concept:** The prompt is the call to action — the thing that says "do it now." Without a prompt, behavior doesn't happen regardless of motivation and ability. Three types: Person Prompts (internal reminders), Context Prompts (environmental cues), and Action Prompts (designed triggers from the product).

**Why it works:** Prompts are the most overlooked element. Many product teams assume that if motivation and ability are present, behavior will happen. It won't — not without a well-timed prompt. The key insight: prompts only work above the Action Line. Sending a push notification to someone who lacks ability or motivation is spam. The best prompts arrive when motivation and ability are already sufficient.

**Key insights:**
- Three prompt types: Person (internal thought), Context (environmental cue), Action (designed notification/CTA)
- Prompts only work when motivation and ability are already above the Action Line
- A prompt at the wrong moment is noise; a prompt at the right moment is magic
- Anchor moments: tie new behaviors to existing routines ("After I open Slack, I will...")
- The best Action Prompts feel like helpful reminders, not interruptions
- Prompt fatigue is real — every unnecessary prompt degrades the value of future prompts

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Notifications** | Only prompt when user is above the Action Line | Send digest when user has content to review, not on a schedule |
| **Onboarding** | Use action prompts to guide first behaviors | Tooltip: "Click here to create your first project" at the right moment |
| **Habit formation** | Design anchor-based prompts | "After your morning standup, review your dashboard" |
| **Re-engagement** | Context prompts tied to real events | "Your report is ready" (event-based, not time-based) |
| **Feature discovery** | Prompt when motivation and ability align | Show feature tour when user encounters the problem it solves |

**Copy patterns:**
- "Your weekly report is ready" (context prompt — tied to real event)
- "After you finish your coffee, take 30 seconds to..." (anchor prompt)
- "One thing left to complete your setup" (action prompt with progress)
- "Your team is waiting for your input" (social context prompt)
- Never: "We miss you!" (product need, not user need)

**Ethical boundary:** Respect prompt fatigue and user preferences. Every prompt should pass the test: "Would I appreciate receiving this right now?" Never use prompts to manipulate through anxiety or manufactured urgency.

See: [references/prompt-design.md](references/prompt-design.md) for prompt types, timing strategies, notification design, and anchor moments.

## Tiny Habits Method

The Tiny Habits method is the practical application of B=MAP: make behaviors so small they require almost no motivation, anchor them to existing routines, and celebrate immediately.

### The Recipe

```
After I [ANCHOR MOMENT], I will [TINY BEHAVIOR], then I [CELEBRATION].
```

**Anchor Moment:** An existing routine that reliably happens (opening an app, finishing a meeting, morning coffee).

**Tiny Behavior:** The smallest version of the target behavior — so small it's almost impossible to skip. Not "write a report" but "open the report template." Not "review analytics" but "glance at one metric."

**Celebration:** An immediate positive emotion after doing the behavior. Celebration wires the habit. Without it, repetition alone isn't enough — you need the feeling of success.

### Starter Steps

Every target behavior has a Starter Step — the tiniest meaningful version:

| Target Behavior | Starter Step | Why It Works |
|----------------|--------------|--------------|
| Complete onboarding | Fill in one field | Momentum from completion |
| Use analytics daily | Open the dashboard | Seeing data creates curiosity |
| Collaborate with team | Send one comment | Social reciprocity kicks in |
| Write documentation | Open the doc template | Blank page resistance removed |
| Review weekly metrics | Star one metric | Creates personal investment |

### Scaling Behaviors

Once the tiny behavior is wired, it naturally grows:

1. **Start tiny** → User opens the dashboard (Starter Step)
2. **Grows naturally** → User checks two or three metrics
3. **Expands** → User customizes the dashboard
4. **Habit formed** → User checks dashboard every morning automatically

The key: never force scaling. Let motivation and momentum drive expansion. The tiny version is not a failure — it is the foundation.

See: [references/tiny-habits.md](references/tiny-habits.md) for the full Tiny Habits recipe, celebration techniques, and scaling patterns.

## Behavior Design Process

Fogg's systematic process for creating lasting behavior change:

### Step 1: Clarify the Aspiration
What outcome does the user want? Not the product's goal — the user's aspiration.
- "I want to stay on top of my team's progress" (not "increase DAU")
- "I want to feel confident about my finances" (not "drive feature adoption")

### Step 2: Explore Behavior Options
List all possible behaviors that could achieve the aspiration. Be exhaustive — don't commit to one behavior yet.

### Step 3: Match Behaviors
For each behavior, assess: Does the user have enough motivation? Is it easy enough? Use the Focus Mapping technique — plot behaviors on a 2×2 of impact vs. feasibility.

### Step 4: Start Tiny
Take the best-matched behavior and shrink it to its Starter Step. Design the prompt. Add celebration.

### Step 5: Optimize
Once the tiny behavior is wired, expand it. Fix bottlenecks using the Ability Chain. Refine prompts based on timing data.

## The Action Line

The Action Line is the visual threshold in the Fogg Behavior Model. Above it, behaviors happen when prompted. Below it, they don't.

### Moving Behaviors Above the Action Line

Two reliable strategies:

**1. Increase Ability (move right)**
- Remove steps, pre-fill fields, add defaults
- Use templates, wizards, progressive disclosure
- This is the most reliable approach

**2. Find better Prompts (prompt at the right moment)**
- Trigger when motivation is naturally higher
- Use anchor moments tied to existing routines
- Event-based prompts > time-based prompts

**Unreliable strategy: Increase Motivation (move up)**
- Motivational messaging produces spikes, not sustained change
- Use motivation boosters sparingly and strategically
- If you need motivation tactics, the behavior is probably too hard

### Retention Diagnostics with B=MAP

Map B=MAP to product metrics:

| Metric | B=MAP Diagnosis | Action |
|--------|----------------|--------|
| **Low activation** | First action is below the Action Line | Shrink onboarding to Starter Step; fix weakest Ability Chain link |
| **Day-1 drop-off** | Prompt failed or mistimed | Redesign first-day prompts; anchor to existing user routine |
| **Day-7 drop-off** | Motivation wave receded, behavior too hard | Reduce core action difficulty; don't depend on initial excitement |
| **Day-30 drop-off** | Habit didn't form, no internal prompt | Create tiny habit recipe; add celebration/feedback loops |
| **Low feature adoption** | Feature is below Action Line for most users | Friction audit the feature; prompt only when motivation is present |
| **Notification fatigue** | Prompts sent below the Action Line | Reduce prompt volume; send only when user has motivation + ability |

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **Relying on motivation to drive retention** | Motivation is a wave — it always recedes. Products that need high motivation fail at the trough | Design for low-motivation moments; make behaviors tiny enough to survive motivation dips |
| **Ignoring the Ability Chain bottleneck** | You optimized time but the real barrier is mental effort or social deviance | Audit all six factors; fix the scarcest resource, not the most obvious one |
| **Sending prompts below the Action Line** | Push notifications to unmotivated users who lack ability is spam, not engagement | Only prompt when motivation + ability are sufficient; use event-based triggers |
| **Skipping celebration in onboarding** | Without positive emotion, repetition alone doesn't wire habits | Add immediate feedback, success states, and micro-celebrations after key actions |
| **Making the first action too ambitious** | "Complete your profile" is a project, not a behavior. Users abandon before starting | Shrink to Starter Step: "Add your name" or "Upload a photo" — one field, one action |
| **Copying successful products without diagnosing B=MAP** | What works for a high-motivation audience fails for yours if ability or prompts differ | Always diagnose your specific users' motivation, ability, and prompt context first |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can a new user complete the core action in under 60 seconds? | Ability is too low | Friction audit using the Ability Chain; shrink to Starter Step |
| Does the product work when user motivation is low? | Design depends on motivation spikes | Redesign core behaviors to require minimal motivation |
| Are prompts tied to real events or anchor moments? | Prompts feel like spam | Switch from time-based to event-based or anchor-based prompts |
| Is there immediate feedback after key actions? | No celebration = no habit wiring | Add success states, progress indicators, or social feedback |
| Have you identified the weakest link in the Ability Chain? | You're optimizing the wrong thing | Rate each of the six factors 1-5 for your core behavior |
| Do users naturally scale from tiny behaviors to full engagement? | Forcing complex behaviors too early | Implement Starter Steps and let behaviors grow organically |

## Reference Files

- [behavior-model.md](references/behavior-model.md): B=MAP deep dive, the Action Line, behavior types, failure diagnostics
- [ability-chain.md](references/ability-chain.md): Six simplicity factors, friction audit templates, simplification strategies
- [prompt-design.md](references/prompt-design.md): Three prompt types, timing strategies, notification design, anchor moments
- [tiny-habits.md](references/tiny-habits.md): Tiny Habits recipe, Starter Steps, celebration, scaling patterns
- [motivation-waves.md](references/motivation-waves.md): Three motivators, motivation waves, designing for troughs
- [product-applications.md](references/product-applications.md): B=MAP applied to SaaS, mobile, e-commerce, health, education
- [case-studies.md](references/case-studies.md): Instagram, Duolingo, Slack, Calm, Peloton through Fogg's lens

## Further Reading

This skill is based on the behavior design research developed by BJ Fogg. For the complete methodology, research, and case studies:

- [*"Tiny Habits: The Small Changes That Change Everything"*](https://www.amazon.com/Tiny-Habits-Small-Changes-Everything/dp/0358003326?tag=wondelai00-20) by BJ Fogg
- [*"Designing for Behavior Change: Applying Psychology and Behavioral Economics"*](https://www.amazon.com/Designing-Behavior-Change-Psychology-Behavioral/dp/1492056030?tag=wondelai00-20) by Stephen Wendel (companion: applying behavior science to product design)

## About the Author

**BJ Fogg, PhD** is the founder of the Behavior Design Lab at Stanford University, where he has directed research on behavior change since 1998. He created the Fogg Behavior Model (B=MAT/B=MAP), which has become the foundational framework used by product designers, health researchers, and behavior change professionals worldwide. Fogg coined the term "behavior design" and has trained thousands of innovators in his methods, including the founders of Instagram (Mike Krieger was a student). His research on "captology" (computers as persuasive technology) created an entirely new academic discipline. *Tiny Habits* distills two decades of research into a practical system for behavior change, demonstrating that lasting change comes not from motivation or willpower but from designing behaviors to be tiny, anchored, and celebrated. Fogg's methods have been adopted by product teams at companies from Silicon Valley startups to Fortune 500 enterprises, and his academic work has been cited over 20,000 times.
