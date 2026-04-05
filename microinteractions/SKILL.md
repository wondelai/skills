---
name: microinteractions
description: 'Design the small details -- triggers, rules, feedback, loops and modes -- that separate good products from great ones. Use when the user mentions "microinteraction", "button feedback", "loading state", "toggle design", "animation detail", "interaction polish", "state transitions", or "input feedback". Also trigger when designing form validation responses, progress indicators, confirmation dialogs, or any UI element where the user expects immediate feedback. Covers trigger design, state rules, feedback mechanisms, and progressive loops. For overall UI polish, see refactoring-ui. For affordance design, see design-everyday-things.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Microinteractions Framework

A systematic approach to designing the tiny, contained product moments that users interact with every day -- toggles, password fields, loading indicators, pull-to-refresh, like buttons. Based on Dan Saffer's four-part structure (Trigger, Rules, Feedback, Loops & Modes), this framework turns invisible details into the polish that separates forgettable products from beloved ones.

## Core Principle

**The difference between a product you tolerate and a product you love is almost always in the microinteractions.** A microinteraction is a contained product moment built around a single use case: changing a setting, syncing data, setting an alarm, picking a password. They are so small that users rarely think about them consciously -- but they feel them. Every microinteraction follows the same four-part structure: a Trigger initiates it, Rules determine what happens, Feedback shows what is happening, and Loops & Modes define its long-term behavior.

## Scoring

**Goal: 10/10.** When reviewing or creating microinteractions, rate them 0-10 based on adherence to the principles below. A 10/10 means every interactive moment has a deliberate trigger, clear rules, immediate feedback, and thoughtful loop/mode behavior. Lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## The Microinteraction Structure

Six areas of focus for designing world-class microinteractions:

### 1. Triggers

**Core concept:** The trigger is what initiates a microinteraction. It can be manual (user-initiated -- a tap, click, swipe, voice command) or system-initiated (a condition is met -- time, location, incoming data, error state). The trigger is the front door of every microinteraction.

**Why it works:** Without a clear trigger, users cannot discover or initiate the interaction. Without a system trigger, the product cannot respond to changing conditions. Well-designed triggers make functionality discoverable and set accurate expectations for what will happen next.

**Key insights:**
- Manual triggers live inside existing UI controls: buttons, switches, icons, form fields, gestures
- System triggers fire automatically when conditions are met: time elapsed, threshold reached, data received
- A trigger must communicate three things: that it exists, what it does, and what state it is in
- Trigger affordance should match the importance of the action -- high-stakes actions need prominent triggers
- Invisible triggers (gestures, shake, proximity) must be paired with a visible alternative for discoverability
- Trigger states -- default, hover, active, disabled, loading -- must be visually distinct

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Toggle controls** | Manual trigger with binary state | iOS Wi-Fi switch: tap to toggle, position shows state |
| **Pull-to-refresh** | Hidden gesture trigger with visible affordance | Pulling down past threshold triggers refresh animation |
| **System alerts** | System trigger on condition met | Low battery notification at 20% threshold |
| **Search fields** | Manual trigger with auto-suggest system trigger | Typing initiates search; results appear as system trigger |
| **Hover reveals** | Manual trigger using proximity | Toolbar actions appear on card hover |

**Ethical boundary:** Never hide critical triggers behind gestures or invisible interactions without a visible fallback. Users should always be able to discover essential functionality.

See: [references/trigger-design.md](references/trigger-design.md)

### 2. Rules

**Core concept:** Rules determine what happens once a microinteraction is triggered. They define the sequence of events, the constraints on what can and cannot happen, the algorithm that processes input, and when the microinteraction ends. Rules are the invisible logic -- users never see them directly, but they feel when rules are wrong.

**Why it works:** Rules create the mental model users build about how the interaction works. When rules are consistent and match expectations, the interaction feels natural. When rules violate expectations -- a toggle that does not toggle, a slider that jumps in value -- users lose trust.

**Key insights:**
- Define the goal of the microinteraction first, then derive rules from it
- Rules should feel natural -- match existing mental models and platform conventions
- Constrain inputs to prevent errors: limit character counts, set value ranges, enforce formats
- Handle edge cases explicitly: what happens at zero, at maximum, on repeated triggers, on interruption
- Simple rules produce complex-feeling interactions; complex rules produce confusing interactions
- The best rules are invisible -- users do not think about them, they just work

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Password strength** | Rules evaluate input in real-time | Meter updates as user types; color shifts from red to green |
| **Character counter** | Rule constrains and displays remaining | Twitter/X: counter decreases, turns red at limit |
| **Volume control** | Rule maps input to output with constraints | Slider snaps to 5% increments; long-press mutes |
| **Shopping cart** | Rules manage quantity and state | Cannot go below 1; shows "max 10" at limit |
| **Undo action** | Rule sets time window for reversal | Gmail "Undo send" available for 30 seconds |

**Ethical boundary:** Rules should be transparent and predictable. Do not create hidden rules that manipulate user behavior, such as making unsubscribe require more steps than subscribe.

See: [references/rules-and-state.md](references/rules-and-state.md)

### 3. Feedback

**Core concept:** Feedback communicates the rules of the microinteraction to the user. It answers: "What is happening right now?" Feedback can be visual (color, animation, movement), auditory (clicks, chimes), or haptic (vibrations). The key constraint is showing only what matters -- minimal, meaningful, contextual.

**Why it works:** Without feedback, users cannot tell if their action registered, if the system is working, or if the operation succeeded. Feedback closes the Gulf of Evaluation. Too little feedback creates anxiety; too much creates noise. The right feedback at the right time makes interactions feel responsive, trustworthy, and alive.

**Key insights:**
- Feedback must be immediate -- under 100ms for direct manipulation
- Use the least noticeable feedback that still communicates: a subtle color change before a modal dialog
- Feedback should map to the significance of the event: small action = small feedback, big result = big feedback
- Visual feedback is primary; audio and haptic are supplementary and should never be the only channel
- Progress indicators reduce perceived wait time even when actual time stays the same
- Feedback should use existing elements when possible -- animate the button, not a separate notification

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Button press** | Visual state change on click | Button depresses, color shifts, text changes to "Saving..." |
| **Form validation** | Inline feedback as user types | Green checkmark appears next to valid email field |
| **File upload** | Progress indicator with percentage | Progress bar fills; percentage and estimated time shown |
| **Error state** | Contextual error near the source | Red border on field + message "Password must be 8+ characters" |
| **Success confirmation** | Brief, non-blocking affirmation | Checkmark animation replaces submit button for 1.5 seconds |

**Ethical boundary:** Feedback should be honest. Do not use fake progress bars, manipulative countdown timers, or deceptive completion percentages to create false urgency.

See: [references/feedback-patterns.md](references/feedback-patterns.md)

### 4. Loops and Modes

**Core concept:** Loops determine the meta-rules of a microinteraction -- what happens over time. Does the interaction change after the 100th use? Does it expire? Does it adapt? Modes are forks in the rules -- temporary states where the microinteraction behaves differently (e.g., edit mode vs. view mode).

**Why it works:** Products that never evolve feel stale. Products that shift behavior unpredictably feel unreliable. Thoughtful loops let microinteractions mature gracefully -- reducing friction for power users while remaining discoverable for new ones. Modes, when used sparingly, let a single control serve multiple purposes without cluttering the interface.

**Key insights:**
- Open loops continue until explicitly stopped (a repeating alarm); closed loops run once and end (a timer)
- Long loops change the microinteraction over time: first use might show a tooltip; 50th use does not
- Progressive reduction: strip away scaffolding as users demonstrate mastery
- Modes are dangerous -- they violate the principle that the same action should produce the same result
- If you must use modes, make the current mode extremely visible (Caps Lock indicator, edit mode banner)
- Avoid mode errors by minimizing the number of modes and making mode transitions deliberate

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Onboarding tooltips** | Long loop removes hints after N uses | First 3 sessions show "Swipe to archive"; then stop |
| **Alarm clock** | Open loop repeats daily until disabled | Alarm fires every weekday at 7am until toggled off |
| **Text editing** | Mode: view vs. edit | Banner reads "Editing" with a "Done" button to exit mode |
| **Smart defaults** | Long loop learns preferences | Email app learns you always CC your manager; suggests it |
| **Notification frequency** | Long loop adapts delivery | Reduces notifications if user ignores 5 in a row |

**Ethical boundary:** Loops should benefit the user, not the business. Do not use adaptive loops to increase notification frequency or make opt-outs progressively harder.

See: [references/loops-modes.md](references/loops-modes.md)

### 5. Signature Moments

**Core concept:** A signature moment is a microinteraction so distinctive that it becomes part of the product's identity. It transforms a functional necessity into a brand-defining detail -- the Facebook Like thumbs-up, the iPhone slide-to-unlock, Slack's loading messages. Not every microinteraction should be a signature moment, but every product should have one or two.

**Why it works:** Signature moments create emotional memory. They make products feel crafted rather than assembled. When users describe your product to others, signature moments are what they demonstrate first. They turn utility into personality.

**Key insights:**
- Signature moments work best on frequent, visible actions -- not buried settings
- They must be functional first, delightful second -- never sacrifice usability for novelty
- Animation, sound, and copy are the three most common tools for creating signature moments
- Signature moments should align with brand personality: playful brands get playful moments
- Restraint matters -- if everything is a signature moment, nothing is
- Test whether users would miss the detail if it were removed; if not, it is decoration, not signature

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Social reaction** | Animated response to engagement | Facebook Like: thumbs-up animates with particles |
| **Loading state** | Branded waiting experience | Slack: rotating quotes during load |
| **Completion** | Celebratory confirmation | Stripe payment: animated checkmark with confetti |
| **Empty state** | Personality in absence of content | Dropbox: illustrated scenes with friendly copy |
| **Error recovery** | Graceful failure with personality | GitHub 404: parallax Octocat illustration |

**Ethical boundary:** Signature moments should never obscure important information or delay the user to show off an animation. Function always precedes delight.

See: [references/signature-moments.md](references/signature-moments.md)

### 6. Reducing and Simplifying

**Core concept:** The best microinteraction is one the user barely notices because it is so simple and fast. Reduction means doing less -- fewer options, fewer steps, fewer decisions. Simplifying means making what remains feel effortless. The goal is to distill every microinteraction to its absolute essence.

**Why it works:** Every option, field, and decision adds cognitive load. Users do not want to configure a toggle switch. They want the toggle to work. Reduction fights feature creep at the smallest level. The most elegant microinteractions have zero configuration, one action, and immediate results.

**Key insights:**
- If a microinteraction needs instructions, it is too complex
- Remove options by choosing smart defaults -- pick the best choice and commit to it
- Collapse multi-step interactions into a single action where possible
- Use progressive disclosure: show simple first, reveal complexity only when requested
- Avoid "settings within settings" -- if a microinteraction has its own preferences, reconsider
- The number of rules should be proportional to the frequency of use: common actions need few rules

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Smart defaults** | Eliminate configuration | Camera app defaults to photo mode, not settings |
| **Inline editing** | Remove modal, edit in place | Spreadsheet cell: click to edit, Enter to save |
| **Auto-detection** | System handles instead of user | Credit card type detected from first digits |
| **Single action** | One tap replaces multi-step flow | Double-tap to like instead of open menu, select reaction |
| **Anticipatory design** | Predict and pre-fill | Shipping form pre-fills city and state from ZIP code |

**Ethical boundary:** Simplification should not remove user control over meaningful choices. Do not auto-opt users into features that benefit the business at the user's expense.

See: [references/trigger-design.md](references/trigger-design.md) for reducing trigger complexity.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **No feedback on action** | Users do not know if their tap registered | Add immediate visual state change to every interactive element |
| **Overdesigning simple moments** | Complex animations slow down frequent actions | Reserve rich animation for infrequent, high-impact moments |
| **Ignoring edge cases** | Interaction breaks at zero, at max, or on double-tap | Map every state: empty, loading, partial, full, error, disabled |
| **Invisible triggers** | Users cannot discover functionality | Pair gesture triggers with a visible alternative |
| **Mode errors** | Same action produces different results depending on hidden state | Make current mode visible; minimize number of modes |
| **Ignoring long loops** | Interaction feels the same on day 1 and day 100 | Use progressive reduction to streamline for returning users |
| **Feedback overload** | Every action triggers a toast, sound, or animation | Use the smallest feedback that communicates; reserve big feedback for big events |
| **Fake progress indicators** | Users feel deceived when they discover the bar is fake | Use honest, deterministic progress; show indeterminate spinner when unknown |

## Quick Diagnostic

Audit any microinteraction:

| Question | If No | Action |
|----------|-------|--------|
| Is there a clear, discoverable trigger? | Users cannot initiate the interaction | Add a visible control or affordance |
| Does the trigger show its current state? | Users cannot tell if it is on, off, or loading | Add distinct visual states for every trigger state |
| Are the rules simple and predictable? | Users are confused by what happened | Simplify rules; match platform conventions |
| Is there immediate feedback? | Users question whether their action worked | Add visual response within 100ms |
| Does feedback match the significance of the event? | Small actions feel dramatic or big actions feel trivial | Scale feedback to match event importance |
| Does the interaction evolve over time? | Power users are still seeing beginner hints | Add progressive reduction through long loops |
| Is the interaction free of unnecessary modes? | Users perform wrong action in wrong mode | Remove modes or make current mode highly visible |
| Could a first-time user figure it out without help? | Interaction needs explanation | Simplify or add a one-time hint via long loop |

## Reference Files

- [trigger-design.md](references/trigger-design.md): Manual and system triggers, trigger affordances, trigger states, invisible trigger design, placement and visibility
- [rules-and-state.md](references/rules-and-state.md): Defining rules, state management, constraints, error states, edge cases
- [feedback-patterns.md](references/feedback-patterns.md): Visual, audio, and haptic feedback, timing, progressive disclosure, preventing overload
- [loops-modes.md](references/loops-modes.md): Open and closed loops, long loops, modes, mode errors, progressive complexity
- [signature-moments.md](references/signature-moments.md): Brand-defining microinteractions, examples, when to invest, making mundane interactions delightful
- [case-studies.md](references/case-studies.md): Detailed design breakdowns of form submission, toggle/switch, pull-to-refresh, loading states, and notifications

## Further Reading

This skill is based on Dan Saffer's definitive guide to designing the details that separate good products from great ones:

- [*"Microinteractions: Designing with Details"*](https://www.amazon.com/Microinteractions-Full-Color-Designing-Details/dp/1491945923?tag=wondelai00-20) by Dan Saffer

## About the Author

**Dan Saffer** is a designer, author, and design leader who has led design teams at Twitter, Jawbone, and Smart Design. He is known for his work on interaction design at the detail level -- the small, contained moments that make up the bulk of user experience. *Microinteractions* codified a framework that design teams at companies worldwide use to audit, design, and improve the small details that make products feel polished and alive. Saffer has also authored *Designing for Interaction* and *Designing Gestural Interfaces*, and he speaks regularly at design conferences on the craft of interaction design.
