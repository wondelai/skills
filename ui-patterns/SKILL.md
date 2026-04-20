---
name: ui-patterns
description: 'Apply proven UI component patterns and scanning behaviour to build effective interfaces. Use when you need to: (1) design navigation, forms, buttons, cards, modals, or tables, (2) understand how users scan pages and place content accordingly, (3) choose between competing UI patterns (dropdown vs radio, modal vs inline, carousel vs static), (4) build loading states, notifications, and search interfaces. Complements gestalt-ui (visual grouping) and laws-of-ux (behavioural principles) with concrete component-level guidance.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# UI Patterns

Concrete, evidence-based patterns for building common UI components. This skill answers the question: **"How should I build this specific component?"**

For visual grouping theory, see `gestalt-ui`. For behavioural psychology laws, see `laws-of-ux`. For visual hierarchy and spacing systems, see `refactoring-ui`. For usability audits, see `ux-heuristics`.

## Core Principle

**Follow proven patterns. Innovate on value, not on interaction mechanics.** Users spend most of their time on other sites (Jakob's Law). Every component you build should feel familiar unless you have strong evidence that a novel pattern is significantly better.

## Scoring

**Goal: 10/10.** When reviewing or building components, rate 0-10 based on adherence to proven patterns.

- **9-10:** Every component follows established patterns. Scanning flow is optimised. Decision reference followed for all pattern choices.
- **7-8:** Most components are well-patterned. Minor issues: one unconventional choice, missing loading state.
- **5-6:** Mixed adherence. Some components feel right, others require learning or cause confusion.
- **3-4:** Significant pattern violations. Users struggle to predict behaviour.
- **1-2:** Components invented from scratch. Nothing feels familiar or predictable.

## The UI Patterns Framework

### 1. Scanning Patterns -- How Users Actually Look at Pages

**Core concept:** Users don't read pages linearly -- they scan in predictable patterns. Place content where the eye naturally goes.

**Why it works:** Eye-tracking research reveals consistent scanning behaviours driven by reading habits and cognitive efficiency.

**Key insights:**

#### F-Pattern (Text-Heavy Pages)

The eye moves:
1. Horizontal scan across the top (headline area)
2. Shorter horizontal scan slightly below (subheading / first paragraph)
3. Vertical scan down the left edge, looking for visual cues

**Design rules for F-pattern pages:**
- First two paragraphs carry the most important information
- Start headings and bullet points with information-carrying words ("Users" not "In the case of users")
- Left-aligned content gets 2-3x more fixation than right-aligned
- Break walls of text with bold keywords, headings, and bullet points
- The F-pattern is the **default** when no visual cues exist -- good design breaks it

#### Z-Pattern (Minimal-Text Pages)

The eye moves: top-left → top-right → diagonal to bottom-left → bottom-right.

**Design rules for Z-pattern pages:**
- Logo/brand: top-left
- CTA or key action: top-right
- Key message or value proposition: along the diagonal
- Primary CTA or conversion action: bottom-right

Best for: landing pages, hero sections, splash screens, marketing pages.

#### Visual Weight Factors

Elements attract attention based on (strongest to weakest):
1. **Size** -- larger elements dominate
2. **Colour and contrast** -- vivid/saturated over muted
3. **Whitespace** -- isolated elements gain prominence
4. **Shape** -- distinctive shapes among uniform ones
5. **Position** -- top-left dominance in LTR languages
6. **Imagery** -- photos of people naturally attract the eye

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Landing pages | Z-pattern with CTA bottom-right | Hero image → headline → feature blocks → "Start free trial" |
| Blog / docs | F-pattern with scannable headings | Bold heading → summary → bulleted details → next heading |
| Dashboards | Top-left for most critical KPI | Revenue chart in top-left, secondary metrics below |
| Search results | Left-aligned titles, information-dense | Title (bold) → URL → description → metadata |

See: [references/scanning-patterns.md](references/scanning-patterns.md)

### 2. Navigation Patterns

**Core concept:** Every page must answer three questions: (1) Where am I? (2) Where can I go? (3) Where have I been?

**Why it works:** Users need orientation, options, and history. Most responsive navigation handles only "where can I go?" and forgets the other two.

**Key insights:**

| Pattern | Use when | Avoid when |
|---------|----------|------------|
| **Persistent top nav** | <= 7 items, flat hierarchy | Complex multi-level structures |
| **Simple toggle (hamburger)** | Single-level, many items on mobile | Multi-level hierarchies |
| **Multi-level toggle** | 2-level hierarchy (sweet spot for most sites) | > 2 levels of depth |
| **Off-canvas / drawer** | Complex menus, mobile-first | Desktop with sufficient space |
| **Tab bar (mobile)** | 3-5 primary destinations | > 5 items |
| **Sidebar** | Many sections, persistent access (apps, dashboards) | Content-focused sites (blogs, marketing) |

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| SaaS dashboard | Sidebar nav + top bar | Slack, Notion, Linear |
| E-commerce | Top nav with categories + breadcrumbs | Product categories as top-level, breadcrumbs on product pages |
| Marketing site | Simple top nav (5-7 links) | Home, Features, Pricing, Docs, Blog, Login |
| Mobile app | Bottom tab bar (4-5 tabs) | Home, Search, Create, Notifications, Profile |

**Navigation rules:**
- Always label hamburger icons with "Menu" text -- icons alone are ambiguous
- Show breadcrumbs at all viewport sizes, not just desktop
- Build navigation progressively -- it must work without JavaScript
- Current page indicator must remain visible in responsive navigation
- No mega-menus on mobile; no more than 3 levels of nesting

See: [references/navigation-forms.md](references/navigation-forms.md)

### 3. Form Patterns

**Core concept:** Forms are the highest-friction UI pattern. Every unnecessary field, confusing label, or validation delay reduces completion rates.

**Why it works:** Research shows most forms can remove 20-60% of their fields without impacting data quality. Perceived complexity reduces completion rates more than actual complexity.

**Key insights:**

#### Layout
- **Labels above fields** -- always. Closest visual proximity.
- **One column** for forms -- multi-column increases completion time by 15-25%
- **Group related fields** with visible boundaries and tighter spacing within groups
- **Auto-focus the first field** to reduce interaction cost
- **Size fields proportionally** to expected input (postcode = short, address = long)

#### Input Optimisation
- Match keyboard to input type: `type="email"`, `type="tel"`, `type="number"`, `type="date"`
- Use input masking for formatted data (phone, dates, credit cards)
- Enable browser autocomplete / autofill (30% faster completion per Google research)
- Show/hide password toggle instead of "confirm password" field
- Avoid dropdowns on mobile -- prefer radio buttons, segmented controls, or steppers

#### Validation
- Validate inline **after the user leaves the field** (on blur), not while typing
- Show errors **next to the field**, not only in a top summary
- Plain language: "Email must include @" not "Error: invalid format"
- Never rely on colour alone for error indication -- add icons and text
- Preserve user input when errors occur -- never clear fields on error
- Show all errors at once, not one at a time

#### Friction Reduction
- Remove every non-essential field
- Explain why sensitive data is needed ("We need your phone for delivery updates")
- Mark only optional fields (if most are required); use "Optional" text, not asterisks
- Persist form data across accidental page reloads

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Signup | Minimal fields (email + password) | Defer profile completion to after signup |
| Checkout | Auto-fill + address API + card scanning | Google Places autocomplete, camera card capture |
| Contact | Name + email + message (3 fields) | No phone, no company, no dropdown for "topic" |
| Settings | Section-by-section with inline save | Each section has its own "Save" button |

See: [references/navigation-forms.md](references/navigation-forms.md)

### 4. Button Patterns

**Core concept:** Buttons must look clickable, communicate their action, and follow a clear visual hierarchy.

**Key insights:**

#### Visual Hierarchy

| Level | Style | Examples |
|-------|-------|---------|
| **Primary** | Filled, high contrast, strongest visual weight | "Create Account", "Submit Order", "Get Started" |
| **Secondary** | Outlined or ghost, lower visual weight | "Cancel", "Back", "Learn More" |
| **Tertiary** | Text-only, minimal visual weight | "Skip", "Maybe Later", "Dismiss" |
| **Destructive** | Distinct colour (typically red), requires confirmation | "Delete Account", "Remove Item" |

**Rule:** Never give "Cancel" the same visual weight as "Submit". The primary action must dominate.

#### Sizing and Touch Targets
- Minimum: **44x44 CSS pixels** (10mm physical)
- Primary action: largest button in context
- Breathing room between adjacent buttons (minimum 8px, recommended 16px)
- Full-width on mobile for primary actions

#### Labeling
- **Action verbs** describing the outcome: "Create Account", "Send Message", "Download PDF"
- Must answer: "What happens when I click this?"
- Avoid: "OK", "Submit", "Yes/No", "Click Here"

#### Required States
- **Default** -- resting appearance
- **Hover** -- cursor feedback (desktop)
- **Active/Pressed** -- click confirmation
- **Focused** -- keyboard navigation indicator (never remove without replacement)
- **Disabled** -- muted with explanation (prefer enabled + validate on submit)
- **Loading** -- spinner or progress during async operations

### 5. Card Patterns

**Core concept:** Cards group heterogeneous content into discrete, scannable, often interactive units.

**Key insights:**
- One primary action per card; secondary actions in overflow menu
- Entire card clickable for the primary action (not just a "Read more" link)
- Consistent dimensions within a grid (same height per row minimum)
- Internal hierarchy: Image > Title > Description > Meta
- Maximum 3-4 pieces of information per card

### 6. Modal & Dialog Patterns

**Core concept:** Modals interrupt flow and demand immediate attention. Use only when interruption is justified.

**When to use:** Destructive action confirmation, short decision-required forms, critical alerts.

**When NOT to use:** Informational content, long forms, marketing/upsells, errors (use inline).

**Rules:**
- Always provide visible close button (X) AND Escape key
- Dim/blur the background (figure-ground separation)
- Focus trap: tab cycling stays within the modal
- Return focus to trigger element on close
- Never stack modals
- Mobile: consider full-screen or bottom sheet instead of centred modal

### 7. Loading State Patterns

**Core concept:** Every async operation needs appropriate feedback based on its duration.

| Duration | Pattern | Example |
|----------|---------|---------|
| < 100ms | No indicator | Direct manipulation (toggle, click) |
| 100-400ms | Subtle indicator | Button state change, micro-animation |
| 400ms-2s | Spinner or skeleton | Content loading, navigation |
| 2-10s | Progress bar + percentage | File upload, data processing |
| > 10s | Progress + status messages | "Generating report... Analysing data..." |

**Skeleton screens:**
- Mirror the layout of the content being loaded
- Subtle shimmer/pulse animation
- Replace with real content progressively (no flash)
- Better than spinners for content-heavy pages

### 8. Notification Patterns

| Type | Persistence | Position | Use case |
|------|-------------|----------|----------|
| **Toast** | Auto-dismiss (3-5s) | Top-right or bottom | Success confirmations, non-critical info |
| **Banner** | Persistent until dismissed | Top of page/section | System messages, warnings |
| **Inline** | Persistent | Next to source element | Validation errors, field-level feedback |
| **Modal** | Requires user action | Centre overlay | Destructive action confirmation |

**Rules:**
- Success notifications auto-dismiss; errors persist until acknowledged
- Errors always colour-independent (icon + text, not just red colour)
- Stack multiple notifications vertically, don't overlap
- Include an action when recovery is possible ("Undo", "Retry")

## Pattern Decision Reference

When choosing between competing patterns, use this table:

| Decision | Choose A | Choose B | Why |
|----------|----------|----------|-----|
| Hamburger vs visible nav | Visible when space allows | Hamburger on mobile only | Hidden nav reduces discoverability by 50%+ |
| Dropdown vs radio buttons (mobile) | Radio / segmented control | Dropdown only for 10+ options | Dropdowns need 2 taps and hide options |
| Placeholder vs label | Always visible labels | Never placeholder-only | Placeholders disappear (recognition > recall) |
| Modal vs inline | Inline when possible | Modal only for interruption | Modals interrupt flow; require focus management |
| Carousel vs static | Static content | Carousel only for media galleries | < 1% interaction past first slide |
| Infinite scroll vs pagination | Pagination for goal-oriented tasks | Infinite scroll for browsing/feeds | Pagination preserves position and back button |
| Icon-only vs icon + label | Icon + label | Icon-only for universal icons (X, search, home) | Most icons are ambiguous without text |
| Confirm password vs toggle | Show/hide toggle | Never confirm password | Single field + toggle reduces errors |
| Disabled button vs enabled | Enabled + validate on submit | Disabled only with visible explanation | Disabled buttons don't explain what's wrong |
| Skeleton vs spinner | Skeleton for content loading | Spinner for actions (submit, search) | Skeletons reduce perceived wait time |
| Bottom sheet vs modal (mobile) | Bottom sheet for selections/actions | Modal for critical confirmations | Bottom sheets are thumb-friendly and dismissible |
| Tabs vs accordion | Tabs when sections are equal priority | Accordion for progressive disclosure | Tabs show all labels; accordions save space |

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Form labels as placeholders | Labels disappear on focus | Always use visible labels above inputs |
| Multi-column forms | 15-25% slower completion | Use single-column layout |
| Validate while user is still typing | Premature errors frustrate and distract | Validate on blur (when user leaves field) |
| Icon-only navigation without labels | Users can't predict meaning | Add text labels to all navigation icons |
| Equal-weight Cancel and Submit buttons | Users click the wrong one | Primary action gets strong visual weight; secondary gets weak |
| Carousel for important content | < 1% see past first slide | Use static layout or prioritise content |
| Modal for non-critical information | Unnecessary interruption | Use inline content, banners, or tooltips |
| No loading feedback for actions > 400ms | Users think the system is broken | Add spinners, skeletons, or optimistic UI |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Does every page answer "Where am I?" | Missing current location indicator | Add active nav state, breadcrumbs, or page title |
| Do forms use labels above fields (not placeholders)? | Recognition violation | Add persistent labels |
| Is there exactly one primary CTA per view? | Competing actions | Demote secondary actions to outlined/text style |
| Do all async actions show feedback within 400ms? | Doherty violation | Add loading states appropriate to duration |
| Are dropdown menus avoided on mobile? | Hick's Law + friction | Replace with radio buttons or segmented controls |
| Can users dismiss modals with X, Escape, and backdrop click? | Control violation | Add all three dismissal methods |

## Reference Files

- [references/scanning-patterns.md](references/scanning-patterns.md) -- F-pattern, Z-pattern, visual weight, and content placement strategies
- [references/navigation-forms.md](references/navigation-forms.md) -- Navigation patterns, form design rules, and validation strategies
- [references/tables-search-loading.md](references/tables-search-loading.md) -- Table design, search patterns, loading states, and notification patterns

## Further Reading

- Smashing Magazine: [Responsive Navigation Patterns](https://www.smashingmagazine.com/2017/04/overview-responsive-navigation-patterns/)
- Smashing Magazine: [Mobile Form Design](https://www.smashingmagazine.com/2018/08/best-practices-for-mobile-form-design/)
- Smashing Magazine: [Button Design](https://www.smashingmagazine.com/2016/11/a-quick-guide-for-designing-better-buttons/)
- Nielsen Norman Group: [F-Shaped Reading Pattern](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)
