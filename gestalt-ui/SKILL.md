---
name: gestalt-ui
description: 'Apply Gestalt principles of visual perception to UI design. Use when you need to: (1) group and organize UI elements effectively, (2) create intuitive visual relationships between components, (3) audit layouts for perceptual clarity, (4) design navigation, cards, forms, or dashboards that users understand instantly. Based on Gestalt psychology research applied to digital interfaces.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Gestalt Principles for UI Design

A framework for applying Gestalt psychology to interface design. Gestalt principles describe how humans automatically group, separate, and interpret visual elements -- use them intentionally to make interfaces self-explanatory.

## Core Principle

**Users don't see individual elements -- they see patterns and relationships.** Every spacing decision, border, colour choice, and alignment communicates grouping, hierarchy, and meaning whether you intend it to or not. Gestalt principles are always active. The question is whether you're using them deliberately or accidentally.

## Scoring

**Goal: 10/10.** When reviewing or designing interfaces, rate 0-10 based on deliberate application of Gestalt principles.

- **9-10:** Every grouping is intentional. Proximity, similarity, and common region work together. Visual relationships match semantic relationships perfectly.
- **7-8:** Most groupings are clear. Minor spacing inconsistencies or ambiguous element relationships in secondary areas.
- **5-6:** Groupings partially work but some elements feel disconnected or wrongly associated. Spacing is inconsistent.
- **3-4:** Significant grouping problems. Users must read labels to understand relationships because visual structure doesn't communicate them.
- **1-2:** No discernible visual grouping. Elements scattered without spatial logic. Users are lost.

## The Gestalt Framework

### 1. Proximity -- The Primary Grouping Mechanism

**Core concept:** Elements positioned close together are perceived as related. Spacing is the most fundamental tool for communicating structure.

**Why it works:** The brain groups nearby elements automatically, before conscious thought. This is faster than reading labels or borders.

**Key insights:**
- Related elements need less space between them than unrelated elements
- A label must be closer to its input field than to the previous field
- Section gaps should be noticeably larger than intra-section spacing
- Equal spacing everywhere makes everything look equally related -- destroying hierarchy

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Forms | Tighter spacing within field groups, larger gaps between groups | Shipping address fields grouped tightly, separated from billing by 2x gap |
| Navigation | Clustered items in header menus | Primary nav items grouped, utility links (login, search) spatially separated |
| Dashboards | Related metrics grouped by proximity | Revenue metrics clustered together, user metrics in a separate spatial zone |
| Cards | Content within cards tightly spaced | Title-description-meta as a tight unit, action buttons slightly separated |

**Common mistake:** Equal margins on all elements. If your form has identical gaps between every field, you've removed all visual grouping.

See: [references/proximity-similarity.md](references/proximity-similarity.md)

### 2. Similarity -- Visual Consistency Signals Function

**Core concept:** Elements sharing visual characteristics (colour, shape, size, weight, texture) are perceived as related and functionally equivalent.

**Why it works:** Once the brain identifies one element's meaning, it transfers that meaning to all visually similar elements. A blue underlined word learned as "clickable" makes all blue underlined words clickable.

**Key insights:**
- All interactive elements of the same type must look identical (links, buttons, inputs)
- Breaking similarity creates emphasis -- the Von Restorff Effect (see `laws-of-ux` skill)
- Icon families must use uniform stroke weight, dimensions, and style
- Typography hierarchy: same size and weight = same level of importance

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Navigation | Consistent link styling signals clickability | All nav links same colour, weight, and hover behaviour |
| Buttons | Same-level buttons share visual style | All secondary actions use outlined style, all primary use filled |
| Data tables | Consistent cell styling signals data type | All currency values right-aligned, same font, same colour |
| Status indicators | Consistent badge/tag styling | All "active" badges green, same size and shape |

**Critical rule:** Breaking similarity must be intentional. A red item in a list of blue items demands attention -- use this for CTAs, errors, or critical actions, never accidentally.

See: [references/proximity-similarity.md](references/proximity-similarity.md)

### 3. Common Region -- Boundaries Create Groups

**Core concept:** Elements enclosed within the same boundary are perceived as grouped and related, even if they're otherwise dissimilar.

**Why it works:** Borders, backgrounds, and cards create explicit containers. Common region can override proximity -- items far apart but within the same card appear more related than close items in different cards.

**Key insights:**
- Cards, panels, and bordered sections are common region in action
- Background colour changes signal section boundaries
- Common region is stronger than proximity -- use it to override spatial grouping when needed
- Too many containers create visual noise; use sparingly and with purpose

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Forms | Fieldsets with visible borders group related inputs | Address fields in a bordered fieldset, payment in another |
| Dashboards | Cards containing related metrics | "Revenue" card with total, growth, and chart -- visually one unit |
| Settings | Panels separating configuration areas | Account settings panel, notification preferences panel, privacy panel |
| Pricing | Plan cards enclosing features, price, and CTA | Each plan visually distinct as a complete unit |

See: [references/region-connectedness.md](references/region-connectedness.md)

### 4. Figure-Ground -- Focus vs Context

**Core concept:** Elements separate into figure (focal element) and ground (background/context). The brain must decide what's foreground and what's behind -- make this decision obvious.

**Why it works:** Stable figure-ground relationships direct attention. Unstable ones create confusion about what to focus on.

**Key insights:**
- High-contrast elements become figure; low-contrast becomes ground
- Smaller overlapping objects tend to be figure; larger ones ground
- Shadows and elevation create clear figure-ground separation
- Modal overlays use dimmed backgrounds to force figure-ground clarity

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| CTAs | High-contrast button against neutral background | Bright "Sign Up" button on a muted hero section |
| Modals | Dimmed/blurred backdrop establishes overlay as figure | Dark scrim behind a confirmation dialog |
| Cards | Subtle shadows lift content off the page | Card with `box-shadow` on flat background |
| Navigation | Sidebar visually distinct from main content | Darker sidebar, lighter content area |

**Ethical boundary:** Never use ambiguous figure-ground to hide important information (dark patterns). Pricing, terms, and opt-outs must be clear figure elements.

See: [references/figure-ground-closure.md](references/figure-ground-closure.md)

### 5. Closure -- The Brain Completes Patterns

**Core concept:** We fill in missing visual information to perceive complete shapes. Partial information is enough when the pattern is recognisable.

**Why it works:** The brain wants coherence. Showing "enough" lets users infer the rest without overwhelming them with visual detail.

**Key insights:**
- Partially visible carousel items signal "more content available"
- Progress bars use closure -- an incomplete fill implies a complete target
- Truncated text with "..." signals expandable content
- Dotted or dashed lines suggest boundaries without solid visual weight

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Carousels | Partially visible cards at edges | Next card peeking 20% into view signals scrollability |
| Progress | Incomplete fills show remaining work | "3 of 5 steps completed" with partial bar |
| Lists | Truncated items signal more content | "Showing 5 of 23 results" with fade-out |
| Icons | Simplified shapes the brain completes | An incomplete circle still reads as "loading" |

See: [references/figure-ground-closure.md](references/figure-ground-closure.md)

### 6. Continuity -- Follow the Line

**Core concept:** Elements arranged on a line or curve appear related and sequential. The eye follows the path naturally.

**Why it works:** We continue perceiving shapes and paths beyond their visible endpoints. This creates flow and sequence.

**Key insights:**
- Aligned elements along invisible grid lines create order and cohesion
- Progress steppers guide users through sequences
- Breadcrumbs follow a linear path showing hierarchy
- Diagonal or curved layouts guide eye movement through content

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Wizards | Step indicators connected by a line | Steps 1-2-3-4 connected, showing progression |
| Timelines | Chronological events along a vertical line | Activity feed with connecting timeline |
| Breadcrumbs | Linear path showing navigation hierarchy | Home > Category > Product |
| Grid alignment | Elements aligned to invisible columns | Dashboard widgets snapped to a 12-column grid |

### 7. Uniform Connectedness -- The Strongest Grouping

**Core concept:** Visually connected elements are perceived as most strongly related. This is the most powerful Gestalt grouping principle.

**Why it works:** Explicit visual connections (lines, arrows, shared containers) create unambiguous relationships that override all other grouping cues.

**Key insights:**
- Connecting lines don't need direct contact with elements -- visual alignment is sufficient
- Stronger than proximity, similarity, and common region
- Use for explicit relationships that must be unambiguous
- Process flows, org charts, and data relationships benefit most

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Process flows | Lines connecting sequential steps | Checkout: Cart → Shipping → Payment → Confirm |
| Org charts | Lines showing reporting relationships | Tree structure with connecting branches |
| Data viz | Lines connecting related data points | Line charts, node graphs, dependency trees |
| Forms | Visual connectors between conditional fields | "If yes" → reveal connected sub-fields |

See: [references/region-connectedness.md](references/region-connectedness.md)

### 8. Common Fate -- Movement Creates Grouping

**Core concept:** Elements moving together or in the same direction are perceived as related, regardless of visual similarity or distance.

**Why it works:** Shared motion is a powerful grouping signal -- the brain assumes co-moving elements are part of the same system.

**Key insights:**
- Animated hover states affecting multiple elements simultaneously group them
- Parallax layers moving at the same speed appear related
- Swiping a card group as a unit signals they belong together
- Scroll-linked animations on multiple elements create perceived unity

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Hover effects | Related elements react together on hover | Hovering a card highlights its image, title, and CTA simultaneously |
| Loading | Grouped skeleton placeholders shimmer together | Three related cards pulsing in sync |
| Scroll effects | Co-moving elements during scroll | Header and subheader sliding up together |
| Drag and drop | Selected items moving as a group | Multi-select files dragging together |

### 9. Focal Points -- What Stands Out Gets Attention

**Core concept:** Elements with contrast, emphasis, or visual distinction capture attention. The eye is drawn to what differs from its surroundings.

**Why it works:** Focal points require a baseline of similarity -- without uniform surrounding elements, nothing can stand out. Contrast is relative.

**Key insights:**
- A highlighted CTA only works if surrounding elements are visually quieter
- Larger text draws attention to key information
- Colour contrast makes specific elements stand out
- Unique shapes among uniform elements attract the eye
- If everything is emphasised, nothing is emphasised

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| CTAs | Contrasting colour on primary action | Blue "Submit" button among grey secondary buttons |
| Pricing | Recommended plan visually distinct | "Popular" plan larger, different colour, highlighted border |
| Alerts | Prominent styling for important messages | Red banner for errors among neutral content |
| Data | Key metric highlighted | Dashboard KPI in large, bold font; supporting data in standard size |

### 10. Pragnanz (Simplicity) -- Simple Wins

**Core concept:** People perceive complex arrangements in the simplest possible form. We prefer clear, ordered, symmetrical structures because they require less cognitive effort.

**Why it works:** Simpler interpretations are processed faster and feel safer. This is the meta-principle underlying all other Gestalt principles.

**Key insights:**
- Clean, uncluttered interfaces are processed faster
- Break complex information into simple, scannable components
- Favour straightforward iconography over detailed illustrations
- When in doubt, simplify -- if users must think about the structure, it's too complex

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Navigation | Hierarchical organisation over flat lists | Categorised menu instead of 40 links |
| Icons | Simple, recognisable shapes | Magnifying glass for search, not a detailed binoculars illustration |
| Layouts | Clean grids over chaotic arrangements | Uniform card grid instead of scattered elements |
| Onboarding | Step-by-step over all-at-once | Wizard with 4 clear steps instead of one overwhelming form |

## Principle Interactions

Gestalt principles don't work in isolation. They interact, reinforce, and sometimes conflict.

### Reinforcement (Stronger Together)

| Combination | Effect |
|-------------|--------|
| Proximity + Similarity | Elements that are close AND look alike are very strongly grouped |
| Common Region + Proximity | Cards with tight internal spacing -- double grouping signal |
| Continuity + Uniform Connectedness | Steps connected by a line AND aligned -- maximum sequence clarity |
| Figure-Ground + Focal Points | High-contrast CTA on dimmed background -- maximum attention |

### Conflicts (Resolution Required)

| Conflict | Resolution |
|----------|------------|
| Proximity suggests group A, but Similarity suggests group B | Common Region overrides both -- use a container |
| Uniform Connectedness creates unwanted association | Increase spacing (Proximity) AND change styling (Similarity) to counteract |
| Closure implies content exists but it doesn't | Remove the visual cue -- don't show a partial card if there's nothing to scroll to |

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Equal spacing everywhere | Removes all visual grouping -- everything looks equally related | Use a spacing scale: tighter within groups, looser between |
| Too many containers/borders | Visual noise, every element screams "I'm a group" | Use proximity and whitespace first; add borders only when needed |
| Inconsistent interactive styling | Users can't predict what's clickable | Audit all links, buttons, and interactive elements for visual consistency |
| Ambiguous figure-ground | Users don't know where to focus | Increase contrast on focal elements; dim/blur backgrounds |
| Accidental similarity | Unrelated elements look alike, implying false relationships | Vary colour, size, or shape to differentiate distinct element types |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you tell which elements are grouped without reading labels? | Spacing doesn't communicate structure | Adjust proximity: tighter within groups, larger gaps between |
| Do all interactive elements of the same type look the same? | Inconsistent similarity | Audit and unify link, button, and input styling |
| Is there one clear focal point per screen/section? | Everything competes for attention | Reduce visual weight on secondary elements; increase on primary |
| Do cards/containers have clear internal hierarchy? | Flat visual weight inside containers | Apply figure-ground and size contrast within cards |
| Can users predict what happens when they interact with an element? | Weak signifiers | Strengthen similarity with other interactive elements of the same type |

## Reference Files

- [references/proximity-similarity.md](references/proximity-similarity.md) -- Deep dive on Proximity and Similarity with spacing scale guidelines and examples
- [references/figure-ground-closure.md](references/figure-ground-closure.md) -- Figure-Ground relationships, Closure patterns, and elevation hierarchy
- [references/region-connectedness.md](references/region-connectedness.md) -- Common Region, Uniform Connectedness, and container design patterns

## Further Reading

- [Smashing Magazine: Design Principles — Visual Perception and the Principles of Gestalt](https://www.smashingmagazine.com/2014/03/design-principles-visual-perception-and-the-principles-of-gestalt/)
- [Laws of UX](https://lawsofux.com/)
- [Interaction Design Foundation: Gestalt Principles](https://www.interaction-design.org/literature/topics/gestalt-principles)
