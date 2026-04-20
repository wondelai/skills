---
name: laws-of-ux
description: 'Apply evidence-based UX laws to interaction design decisions. Use when you need to: (1) size and position interactive targets effectively, (2) reduce cognitive load and decision complexity, (3) design progress indicators, feedback timing, and memory-friendly interfaces, (4) resolve design trade-offs with psychological evidence. Based on Laws of UX by Jon Yablonski, synthesising research from psychology, cognitive science, and HCI.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Laws of UX

A framework of behavioural psychology principles applied to interface design. These laws describe how humans perceive, decide, and act -- use them to design interfaces that work with human cognition, not against it.

This skill focuses on behavioural laws (Fitts's, Hick's, Miller's, etc.). For usability heuristics, see `ux-heuristics`. For visual grouping principles, see `gestalt-ui`.

## Core Principle

**Design for how humans actually behave, not how they should behave.** Users don't read -- they scan. They don't optimise -- they satisfice. They don't remember -- they recognise. Every interaction design decision should be grounded in observable human behaviour, not designer assumptions.

## Scoring

**Goal: 10/10.** When reviewing or designing interactions, rate 0-10 based on alignment with these behavioural laws.

- **9-10:** Interactive targets are appropriately sized and placed. Choices are manageable. Response times feel instant. Progress is visible. Memory load is minimal.
- **7-8:** Most interactions follow the laws. Minor issues: a few small targets, one overloaded menu, occasional missing feedback.
- **5-6:** Some laws applied, others ignored. Noticeable friction: too many choices, missing progress indicators, slow feedback.
- **3-4:** Significant violations. Small touch targets, overwhelming option lists, no loading feedback, heavy memory demands.
- **1-2:** Laws systematically violated. Interface fights human cognition at every step.

## The Laws of UX Framework

### 1. Fitts's Law -- Size and Distance Matter

**Core concept:** The time to reach a target is a function of the distance to and size of the target. Larger, closer targets are faster and easier to hit.

**Why it works:** Motor control follows a logarithmic speed-accuracy trade-off. Smaller targets require slower, more precise movements.

**Key insights:**
- Minimum touch target: **44x44 CSS pixels** (10mm x 10mm physical, per MIT Touch Lab)
- Add padding between adjacent interactive elements to prevent mis-taps
- Screen edges and corners are effectively infinite-size targets (cursor stops at edge)
- Place frequently used actions near the cursor's resting position or thumb zone
- Primary actions should be the largest interactive elements in their context

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Mobile | Thumb-zone placement for primary actions | FAB button in bottom-right (right-handed), tab bar at bottom |
| Forms | Full-width submit buttons on mobile | "Continue" button spanning the viewport width |
| Navigation | Adequately sized menu items with padding | 44px minimum height per nav link, 8px gap between |
| Dialogs | Large, separated action buttons | "Delete" and "Cancel" with generous spacing and size |

**Ethical boundary:** Never make important actions (unsubscribe, delete account, reject cookies) deliberately small or hard to reach.

See: [references/motor-laws.md](references/motor-laws.md)

### 2. Hick's Law -- Fewer Choices, Faster Decisions

**Core concept:** Decision time increases logarithmically with the number and complexity of choices. More options = more cognitive effort = slower action.

**Why it works:** Each additional option requires evaluation and comparison. The brain processes choices sequentially, not in parallel.

**Key insights:**
- Limit top-level navigation to **5-7 items**
- Use progressive disclosure: show details on demand, not all at once
- Break complex processes into sequential steps (wizards over mega-forms)
- Highlight recommended options to reduce decision effort
- Categorise long lists instead of presenting flat lists
- "Choice overload" causes decision paralysis when options exceed ~4 meaningful alternatives

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Navigation | Maximum 5-7 top-level items | Main nav: Home, Products, Pricing, Docs, Blog |
| Pricing | 3 plans with highlighted recommendation | Free / Pro (recommended) / Enterprise |
| Settings | Grouped into categories, not one long list | Account, Notifications, Privacy, Billing -- each expandable |
| Onboarding | One question per screen | Step 1: Role → Step 2: Team size → Step 3: Goals |
| Search | Filtered results with facets | Category tabs + sort options, not 500 unsorted results |

See: [references/decision-laws.md](references/decision-laws.md)

### 3. Miller's Law -- Chunk Information

**Core concept:** Working memory holds approximately **7 +/- 2 items**. Beyond this, information overflows and is forgotten or confused.

**Why it works:** Short-term memory has a fixed capacity. Chunking groups individual items into meaningful units, effectively multiplying capacity.

**Key insights:**
- Break long sequences into chunks: `(555) 123-4567` not `5551234567`
- Limit items per group to 5-9 (navigation sections, tab groups, option lists)
- Use headings and visual separators to chunk content on a page
- Don't interpret this as "menus must have exactly 7 items" -- it's about cognitive load, not a magic number

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Phone numbers | Chunked with formatting | `+49 (171) 234-5678` |
| Credit cards | 4-digit groups | `4242 4242 4242 4242` |
| Long forms | Grouped into sections | Personal info (3 fields) → Address (4 fields) → Payment (3 fields) |
| Dashboards | Metrics grouped into panels | Revenue panel (3 KPIs), Users panel (3 KPIs), Performance panel (3 KPIs) |

See: [references/memory-laws.md](references/memory-laws.md)

### 4. Jakob's Law -- Users Expect Convention

**Core concept:** Users spend most of their time on **other** sites. They prefer your interface to work the same way as interfaces they already know.

**Why it works:** Familiar patterns leverage existing mental models. Users don't need to learn new interactions -- they transfer knowledge from past experience.

**Key insights:**
- Logo top-left links to home (universal convention)
- Search in the top-right or top-centre
- Shopping cart icon for e-commerce
- Hamburger menu = hidden navigation (mobile)
- "Settings" = gear icon; "Profile" = avatar/circle
- Innovate on content and value, not on basic interaction patterns
- When you must break convention, provide clear signifiers and instructions

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| E-commerce | Standard cart/checkout flow | Cart icon with badge → Cart page → Checkout → Confirmation |
| SaaS | Standard dashboard layout | Sidebar nav + top bar + main content area |
| Auth | Standard login/signup patterns | Email + password + "Forgot password?" + social login |
| Mobile | Platform-specific patterns | iOS: back in top-left; Android: back via system gesture |

**Critical rule:** Every deviation from convention must earn its place. If users need to learn something new, the benefit must clearly outweigh the learning cost.

See: [references/decision-laws.md](references/decision-laws.md)

### 5. Doherty Threshold -- Speed Builds Flow

**Core concept:** Productivity soars when response time is under **400ms**. Above this, users perceive a delay and lose their sense of flow.

**Why it works:** Below 400ms, the interaction feels instantaneous -- the brain doesn't register waiting. Above it, the user's attention shifts from the task to the system.

**Key insights:**
- < 100ms: Feels instantaneous. No feedback needed for direct manipulation (clicks, toggles)
- 100-400ms: Subtle indicator (button state change, micro-animation)
- 400ms-2s: Spinner or skeleton screen required
- 2-10s: Progress bar with percentage
- > 10s: Progress bar + status messages explaining what's happening
- Use optimistic UI: show the result immediately, sync in the background
- Animate transitions (300-500ms) to mask loading time

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Form submission | Optimistic success state | "Message sent!" appears immediately; actual API call happens in background |
| Page navigation | Skeleton screens | Grey placeholder blocks matching the layout, replaced by real content |
| Data loading | Progressive loading | Table header + first rows appear instantly; remaining rows stream in |
| Search | Debounced live results | Results update 200ms after user stops typing |

See: [references/motor-laws.md](references/motor-laws.md)

### 6. Von Restorff Effect -- Distinctiveness Creates Memory

**Core concept:** When multiple similar objects are present, the one that **differs** from the rest is most likely to be remembered.

**Why it works:** The brain allocates more attention and memory to novel or distinctive stimuli. Contrast is a survival mechanism.

**Key insights:**
- Make the primary CTA visually distinct from all other buttons
- Highlight the recommended pricing plan with a different style
- Use distinctive styling for important notifications or alerts
- Sparingly: if everything is highlighted, nothing stands out (see Focal Points in `gestalt-ui`)
- Accessibility: don't rely on colour alone for distinctiveness -- use size, shape, position, and text

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Pricing | Recommended plan visually different | "Pro" plan with coloured border, "Popular" badge, slightly larger |
| CTAs | Primary button distinct from secondary | Blue filled "Submit" among grey outlined "Cancel" and "Back" |
| Notifications | Critical alerts visually unique | Red banner for errors among blue info notifications |
| Tables | Important row highlighted | Overdue invoice row with coloured background |

### 7. Peak-End Rule -- Moments That Matter

**Core concept:** People judge an experience by its **peak moment** (most intense point) and its **ending**, not by the average of all moments.

**Why it works:** Memory is constructive, not comprehensive. The brain stores emotional highlights and the final state, then generalises from those.

**Key insights:**
- Optimise the first impression (landing, onboarding) and the final interaction (confirmation, thank-you)
- Error recovery is a peak moment -- handle it gracefully and users forgive other friction
- A frustrating checkout can ruin an otherwise excellent browsing experience
- Celebratory moments (achievement unlocked, order confirmed) create positive peaks
- The last step of any flow disproportionately influences overall satisfaction

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Onboarding | Delightful first experience | Personalised welcome, quick first success ("Your workspace is ready!") |
| Checkout | Smooth final step + celebration | Confetti animation on order confirmation |
| Error recovery | Helpful, specific error messages | "Payment failed -- try a different card or contact support" with direct link |
| Cancellation | Respectful exit experience | "We're sorry to see you go" with clear confirmation, no guilt-tripping |

### 8. Aesthetic-Usability Effect -- Beauty Buys Tolerance

**Core concept:** Users perceive aesthetically pleasing designs as **more usable**, even when they're objectively not.

**Why it works:** Visual appeal creates positive emotional responses that bias perception. Users are more patient, more forgiving, and more willing to explore beautiful interfaces.

**Key insights:**
- Visual polish increases tolerance for minor usability issues
- First impressions are disproportionately influenced by visual quality
- But: aesthetics cannot compensate for fundamentally broken interactions
- Invest in visual refinement **after** getting the interaction model right
- A beautiful but unusable interface is worse than an ugly but functional one

### 9. Tesler's Law -- Complexity Must Live Somewhere

**Core concept:** Every system has **irreducible complexity** that cannot be eliminated. The question is whether the user or the system deals with it.

**Why it works:** Complexity is conserved -- simplifying the user's experience means the system absorbs that complexity. The goal is to move complexity away from the user wherever possible.

**Key insights:**
- Smart defaults reduce decisions the user must make
- Auto-detection (location, language, currency, timezone) absorbs complexity
- Pre-filling forms with known data moves complexity to the system
- But: don't hide essential controls behind too much "magic" -- users need to feel in control
- The simplest UI is not always the best UI -- sometimes showing complexity is appropriate (power tools)

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Forms | Smart defaults | Country pre-selected based on IP, currency auto-set |
| Search | Auto-correct and suggestions | "Did you mean..." + filtered suggestions |
| Settings | Sensible defaults with override option | Notifications on by default, customisable per channel |
| Scheduling | Timezone auto-detection | "Meeting at 3pm your time (PST)" |

### 10. Postel's Law -- Be Forgiving with Input

**Core concept:** Be **liberal in what you accept**, conservative in what you send. Accommodate varied input; produce clean output.

**Why it works:** Users input data in unpredictable formats. Fighting their format creates friction. Accepting and normalising silently creates flow.

**Key insights:**
- Accept phone numbers with or without country code, spaces, dashes, parentheses
- Accept dates in multiple formats and normalise to one display format
- Trim whitespace, fix capitalisation, strip formatting silently
- Display output in a clean, consistent format regardless of input
- Forgive typos in search (fuzzy matching, "did you mean...?")

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Phone input | Accept any format | `+1 555 123 4567`, `(555) 123-4567`, `5551234567` all valid |
| Date input | Accept multiple formats | `12/25/2025`, `25.12.2025`, `Dec 25 2025` all parsed correctly |
| Search | Fuzzy matching | "javascrpt" → shows results for "javascript" |
| Names | Flexible validation | Accept O'Brien, García, 山田, hyphenated names |

### 11. Goal-Gradient Effect -- Proximity to Finish Motivates

**Core concept:** Motivation increases as users **approach their goal**. The closer to completion, the harder they'll work.

**Why it works:** Progress toward a visible goal triggers dopamine release. The brain rewards effort more as the finish line approaches.

**Key insights:**
- Show progress bars in multi-step processes
- Start progress slightly filled (artifical advancement increases completion)
- "Step 2 of 4" is more motivating than showing all steps as equally distant
- Checklists with some items pre-checked leverage this effect
- Loyalty programs and streaks use goal-gradient extensively

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Onboarding | Progress bar with steps completed | "Profile 60% complete -- add a photo to reach 80%" |
| Checkout | Step indicator with progress | Steps 1-4 with current position highlighted |
| Gamification | Achievement nearly unlocked | "3 more reviews to earn Gold Reviewer badge" |
| Forms | Section progress within long forms | "Section 2 of 3: Shipping Details" |

## Combining Laws

Laws work together. The strongest designs apply multiple laws simultaneously:

| Combination | Effect | Example |
|-------------|--------|---------|
| Fitts + Hick | Large targets + few choices = fast action | 3 large pricing plan buttons |
| Miller + Goal-Gradient | Chunked steps + progress visibility | 4-step wizard with progress bar |
| Jakob + Postel | Conventional layout + flexible input | Standard checkout flow accepting varied address formats |
| Doherty + Peak-End | Fast responses + celebratory ending | Instant "Added to cart" + confetti on order confirmation |
| Von Restorff + Fitts | Distinctive + large = unmissable CTA | One bright, large "Get Started" button on muted page |

## Common Mistakes

| Mistake | Law Violated | Fix |
|---------|-------------|-----|
| Tiny click/tap targets | Fitts's Law | Minimum 44x44px; add padding between targets |
| 15+ navigation items in one level | Hick's Law | Categorise into 5-7 groups; use progressive disclosure |
| Requiring users to remember values between screens | Miller's Law | Show context persistently; use breadcrumbs and summaries |
| Reinventing standard interaction patterns | Jakob's Law | Follow conventions; innovate on value, not on UI mechanics |
| No feedback for actions > 400ms | Doherty Threshold | Add spinners, skeleton screens, or optimistic UI |
| Every element equally emphasised | Von Restorff Effect | One focal point per context; mute everything else |
| Frustrating final step in a flow | Peak-End Rule | Polish the ending: confirmation, success animation, next steps |
| Rejecting valid but oddly-formatted input | Postel's Law | Parse and normalise silently; accept what you can |
| No progress indicator in multi-step process | Goal-Gradient Effect | Show step count, progress bar, or checklist |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Are all touch targets >= 44x44px? | Fitts violation | Increase size; add padding |
| Can users complete the primary task in < 3 decisions? | Hick violation | Reduce choices; use progressive disclosure |
| Is information chunked into groups of <= 7? | Miller violation | Group, chunk, and label information |
| Does the interface follow platform conventions? | Jakob violation | Audit against standard patterns; align |
| Is feedback visible within 400ms of every action? | Doherty violation | Add optimistic UI, skeletons, or spinners |
| Is there exactly one visually dominant CTA per view? | Von Restorff gap | Emphasise one; de-emphasise others |
| Is the final step of key flows polished and positive? | Peak-End gap | Add confirmation, celebration, clear next steps |

## Reference Files

- [references/motor-laws.md](references/motor-laws.md) -- Fitts's Law and Doherty Threshold with sizing tables and response time guidelines
- [references/decision-laws.md](references/decision-laws.md) -- Hick's Law, Jakob's Law, choice architecture, and progressive disclosure
- [references/memory-laws.md](references/memory-laws.md) -- Miller's Law, Serial Position Effect, Zeigarnik Effect, and chunking strategies

## Further Reading

- Jon Yablonski, [Laws of UX](https://lawsofux.com/)
- Paul Fitts, "The Information Capacity of the Human Motor System" (1954)
- William Hick, "On the Rate of Gain of Information" (1952)
- George Miller, "The Magical Number Seven" (1956)
