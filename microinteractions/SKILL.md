---
name: microinteractions
description: 'Design the small details -- triggers, rules, feedback, loops and modes -- that separate good products from great ones. Use when the user mentions "microinteraction", "button feedback", "loading state", "toggle design", "animation detail", "interaction polish", "state transitions", "input feedback", "the interface feels dead", "make the UI feel responsive", or "add polish to interactions". Also trigger when designing form-validation responses, progress indicators, confirmation dialogs, or any element where the user expects immediate feedback. Covers trigger design, state rules, feedback mechanisms, and progressive loops. For overall UI polish, see refactoring-ui. For affordance design, see design-everyday-things.'
license: MIT
metadata:
  author: wondelai
  version: "1.3.0"
---

# Microinteractions Framework

Design the tiny, contained product moments users touch every day -- toggles, password fields, loading indicators, pull-to-refresh, like buttons. Based on Dan Saffer's four-part structure (Trigger, Rules, Feedback, Loops & Modes), this framework turns invisible details into the polish that separates forgettable products from beloved ones.

## Core Principle

**The difference between a product you tolerate and a product you love is almost always in the microinteractions.** A microinteraction is a contained moment built around a single use case -- changing a setting, syncing data, picking a password -- so small that users rarely think about it consciously, but they feel it. Every microinteraction follows the same four-part structure: a Trigger initiates it, Rules determine what happens, Feedback shows what is happening, and Loops & Modes define its long-term behavior.

## Scoring

**Goal: 10/10.** Rate microinteractions 0-10 against the principles below: a 10/10 gives every interactive moment a deliberate trigger, clear rules, immediate feedback, and thoughtful loop/mode behavior. Always state the current score and the specific improvements needed to reach 10/10.

## The Microinteraction Structure

Six areas of focus for designing world-class microinteractions:

### 1. Triggers

**Core concept:** The trigger initiates a microinteraction -- manual (tap, click, swipe, voice command) or system-initiated (time, location, incoming data, error state). It is the front door of every microinteraction.

**Why it works:** Without a clear trigger, users cannot discover or initiate the interaction, and the product cannot respond to changing conditions. Well-designed triggers make functionality discoverable and set accurate expectations.

**Key insights:**
- A trigger must communicate three things: that it exists, what it does, and what state it is in
- Match trigger prominence to action importance -- high-stakes actions need prominent triggers
- Pair invisible triggers (gestures, shake, proximity) with a visible alternative for discoverability
- Make trigger states -- default, hover, active, disabled, loading -- visually distinct

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Toggle controls** | Manual trigger with binary state | iOS Wi-Fi switch: tap to toggle, position shows state |
| **Pull-to-refresh** | Hidden gesture with visible affordance | Pull past threshold triggers refresh animation |
| **System alerts** | System trigger on condition met | Low battery notification at 20% threshold |

**Ethical boundary:** Never hide critical triggers behind gestures or invisible interactions without a visible fallback.

See: [references/trigger-design.md](references/trigger-design.md) for trigger affordances, states, placement, and reducing trigger complexity.

### 2. Rules

**Core concept:** Rules define what happens once a microinteraction is triggered -- the sequence of events, constraints, processing, and ending. Users never see rules directly, but they feel when rules are wrong.

**Why it works:** Rules create the mental model users build about how the interaction works. Consistent rules that match expectations feel natural; violations -- a toggle that does not toggle, a slider that jumps in value -- destroy trust.

**Key insights:**
- Define the goal of the microinteraction first, then derive rules from it
- Match existing mental models and platform conventions
- Constrain inputs to prevent errors: limit character counts, set value ranges, enforce formats
- Handle edge cases explicitly: zero, maximum, repeated triggers, interruption

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Password strength** | Rules evaluate input in real-time | Meter updates as user types; color shifts red to green |
| **Character counter** | Rule constrains and shows remaining | Twitter/X: counter decreases, turns red at limit |
| **Undo action** | Rule sets time window for reversal | Gmail "Undo send" available for 30 seconds |

**Ethical boundary:** Keep rules transparent and predictable -- never hide rules that manipulate behavior, such as making unsubscribe harder than subscribe.

See: [references/rules-and-state.md](references/rules-and-state.md) for state management, constraints, error states, and edge cases.

### 3. Feedback

**Core concept:** Feedback communicates the rules to the user, answering "What is happening right now?" -- visually (color, animation, movement), aurally (clicks, chimes), or haptically (vibration). Show only what matters: minimal, meaningful, contextual.

**Why it works:** Without feedback, users cannot tell if their action registered, the system is working, or the operation succeeded. Too little feedback creates anxiety; too much creates noise; the right feedback at the right time makes interactions feel responsive and trustworthy.

**Key insights:**
- Feedback must be immediate -- under 100ms for direct manipulation
- Use the least noticeable feedback that still communicates, and prefer animating existing elements (the button itself, not a separate toast)
- Scale feedback to event significance: small action = small feedback, big result = big feedback
- Visual feedback is primary; audio and haptic are supplementary, never the only channel
- Progress indicators reduce perceived wait time even when actual time is unchanged

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Button press** | Visual state change on click | Button depresses, color shifts, text becomes "Saving..." |
| **Form validation** | Inline feedback as user types | Green checkmark next to valid email field |
| **Error state** | Contextual error near the source | Red border on field + "Password must be 8+ characters" |

**Ethical boundary:** Keep feedback honest -- no fake progress bars, manipulative countdowns, or deceptive completion percentages.

See: [references/feedback-patterns.md](references/feedback-patterns.md) for feedback channels, timing, and preventing overload.

### 4. Loops and Modes

**Core concept:** Loops are the meta-rules over time -- does the interaction change after the 100th use, expire, adapt? Modes are forks in the rules where the same control temporarily behaves differently (edit mode vs. view mode).

**Why it works:** Thoughtful loops let microinteractions mature gracefully -- reducing friction for power users while staying discoverable for new ones. Modes, used sparingly, let one control serve multiple purposes without cluttering the interface.

**Key insights:**
- Open loops continue until explicitly stopped (a repeating alarm); closed loops run once and end (a timer)
- Long loops change the interaction over time: first use shows a tooltip; the 50th does not
- Progressive reduction: strip away scaffolding as users demonstrate mastery
- Modes are dangerous -- they violate "same action, same result"; minimize them and make the current mode highly visible (Caps Lock indicator, edit banner)

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Onboarding tooltips** | Long loop removes hints after N uses | First 3 sessions show "Swipe to archive"; then stop |
| **Alarm clock** | Open loop repeats until disabled | Fires every weekday at 7am until toggled off |
| **Text editing** | Mode: view vs. edit | Banner reads "Editing" with a "Done" button to exit |

**Ethical boundary:** Loops should benefit the user, not the business -- never adapt loops to ramp up notifications or make opt-outs progressively harder.

See: [references/loops-modes.md](references/loops-modes.md) for long loops, mode errors, and progressive complexity.

### 5. Signature Moments

**Core concept:** A signature moment is a microinteraction so distinctive it becomes part of the product's identity -- the Facebook Like, slide-to-unlock, Slack's loading messages. Every product should have one or two; not every interaction should be one.

**Why it works:** Signature moments create emotional memory and make products feel crafted rather than assembled. They are what users demonstrate first when describing your product to others.

**Key insights:**
- Put signature moments on frequent, visible actions -- not buried settings
- Functional first, delightful second -- never sacrifice usability for novelty
- Animation, sound, and copy are the three most common tools
- Align with brand personality: playful brands get playful moments
- Apply the removal test: if users would not miss it, it is decoration, not signature

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Social reaction** | Animated response to engagement | Facebook Like: thumbs-up animates with particles |
| **Loading state** | Branded waiting experience | Slack: rotating quotes during load |
| **Completion** | Celebratory confirmation | Stripe payment: animated checkmark with confetti |

**Ethical boundary:** Never obscure important information or delay the user to show off an animation -- function precedes delight.

See: [references/signature-moments.md](references/signature-moments.md) for when to invest and making mundane interactions delightful.

### 6. Reducing and Simplifying

**Core concept:** The best microinteraction is barely noticed because it is so simple and fast. Reduce (fewer options, steps, decisions), then simplify what remains until it feels effortless.

**Why it works:** Every option, field, and decision adds cognitive load -- users do not want to configure a toggle, they want it to work. The most elegant microinteractions have zero configuration, one action, and immediate results.

**Key insights:**
- If a microinteraction needs instructions, it is too complex
- Remove options with smart defaults -- pick the best choice and commit to it
- Collapse multi-step interactions into a single action where possible
- Use progressive disclosure: show simple first, reveal complexity only on request
- Keep rule count proportional to frequency of use: common actions need few rules

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Smart defaults** | Eliminate configuration | Camera app opens in photo mode, not settings |
| **Single action** | One tap replaces multi-step flow | Double-tap to like instead of menu + select reaction |
| **Anticipatory design** | Predict and pre-fill | Shipping form fills city and state from ZIP code |

**Ethical boundary:** Do not auto-opt users into business-serving features or remove control over meaningful choices.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **No feedback on action** | Users cannot tell if their tap registered | Add immediate visual state change to every interactive element |
| **Overdesigning simple moments** | Complex animations slow frequent actions | Reserve rich animation for infrequent, high-impact moments |
| **Ignoring edge cases** | Interaction breaks at zero, max, or double-tap | Map every state: empty, loading, partial, full, error, disabled |
| **Invisible triggers** | Users cannot discover functionality | Pair gesture triggers with a visible alternative |
| **Mode errors** | Same action gives different results based on hidden state | Make current mode visible; minimize modes |
| **Ignoring long loops** | Interaction feels identical on day 1 and day 100 | Use progressive reduction for returning users |
| **Feedback overload** | Every action triggers a toast, sound, or animation | Use the smallest feedback that communicates |
| **Fake progress indicators** | Users feel deceived when they discover the bar is fake | Use honest, deterministic progress; indeterminate spinner when unknown |

## Quick Diagnostic

Audit any microinteraction:

| Question | If No | Action |
|----------|-------|--------|
| Is there a clear, discoverable trigger? | Users cannot initiate the interaction | Add a visible control or affordance |
| Does the trigger show its current state? | Users cannot tell if it is on, off, or loading | Add distinct visual states for every trigger state |
| Are the rules simple and predictable? | Users are confused by what happened | Simplify rules; match platform conventions |
| Is there immediate feedback? | Users question whether their action worked | Add visual response within 100ms |
| Does feedback match the event's significance? | Small actions feel dramatic, or big results feel trivial | Scale feedback to event importance |
| Does the interaction evolve over time? | Power users still see beginner hints | Add progressive reduction through long loops |
| Is the interaction free of unnecessary modes? | Users perform the wrong action in the wrong mode | Remove modes or make the current mode highly visible |
| Could a first-time user figure it out without help? | Interaction needs explanation | Simplify or add a one-time hint via long loop |

## Reference Files

- [trigger-design.md](references/trigger-design.md): Manual and system triggers, trigger affordances, trigger states, invisible trigger design, placement and visibility
- [rules-and-state.md](references/rules-and-state.md): Defining rules, state management, constraints, error states, edge cases
- [feedback-patterns.md](references/feedback-patterns.md): Visual, audio, and haptic feedback, timing, progressive disclosure, preventing overload
- [loops-modes.md](references/loops-modes.md): Open and closed loops, long loops, modes, mode errors, progressive complexity
- [signature-moments.md](references/signature-moments.md): Brand-defining microinteractions, examples, when to invest, making mundane interactions delightful
- [case-studies.md](references/case-studies.md): Detailed design breakdowns of form submission, toggle/switch, pull-to-refresh, loading states, and notifications

## Further Reading

This skill is based on Dan Saffer's definitive guide to designing with details:

- [*"Microinteractions: Designing with Details"*](https://www.amazon.com/Microinteractions-Full-Color-Designing-Details/dp/1491945923?tag=wondelai00-20) by Dan Saffer

## About the Author

**Dan Saffer** is a designer and design leader who has led teams at Twitter, Jawbone, and Smart Design. His book *Microinteractions* codified the framework design teams worldwide use to audit, design, and improve the small details that make products feel polished and alive. He also wrote *Designing for Interaction* and *Designing Gestural Interfaces*.
