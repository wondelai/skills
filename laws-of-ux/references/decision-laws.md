# Decision Laws -- Hick's Law & Jakob's Law

How users make choices and what they expect from interfaces.

## Hick's Law Deep Dive

### The Formula

```
RT = a + b × log₂(n + 1)
```

Where:
- **RT** = Reaction Time
- **n** = Number of choices
- **a, b** = Constants

The logarithmic relationship means going from 2 to 4 options has more impact than going from 20 to 22. The first few additional options cost the most cognitive effort.

### Choice Reduction Strategies

| Strategy | How it works | Example |
|----------|-------------|---------|
| **Progressive disclosure** | Show only what's needed now; reveal more on demand | "Advanced settings" expandable section |
| **Categorisation** | Group options into meaningful categories | Settings → Account / Notifications / Privacy |
| **Recommended option** | Highlight one choice to short-circuit decision-making | "Most popular" plan badge |
| **Smart defaults** | Pre-select the most common option | Country pre-selected based on IP |
| **Recent/frequent** | Surface previously chosen options | "Recent searches" dropdown |
| **Search + filter** | Let users narrow large sets themselves | Product filters: price, size, colour |

### Navigation Limits

| Level | Maximum items | Strategy beyond limit |
|-------|--------------|----------------------|
| Top-level nav | 5-7 | Merge, categorise, or use mega-menu with clear sections |
| Dropdown menu | 7-10 | Add search within dropdown; categorise with headers |
| Tab bar (mobile) | 5 | "More" tab for additional items |
| Action menu | 5-7 | Group into sections with dividers |
| Toolbar | 5-7 visible | Overflow menu (...) for additional actions |

### Choice Architecture

The way choices are presented influences decisions:

1. **Default bias:** Users tend to accept pre-selected options. Use ethical defaults.
2. **Order effect:** First and last options are chosen more often (Serial Position Effect).
3. **Decoy effect:** An inferior option can make a target option look better (pricing tiers).
4. **Anchoring:** The first number seen influences subsequent judgments (original price shown with discount).

**Ethical boundary:** Choice architecture must serve the user's interest. Manipulative defaults (pre-checked newsletter signup, harder-to-find unsubscribe) are dark patterns.

### Progressive Disclosure Patterns

| Pattern | Implementation | Use case |
|---------|---------------|----------|
| Accordion | Click to expand one section at a time | FAQ, settings categories |
| "Show more" | Button reveals additional items | Product features, search results |
| Tabs | Switch between content panels | Dashboard views, profile sections |
| Wizard / Stepper | One step at a time in sequence | Onboarding, checkout, complex forms |
| Tooltip / Popover | Hover or click for details | Feature explanations, data tooltips |
| Detail panel | Select item to show details in adjacent panel | Email clients, admin dashboards |

---

## Jakob's Law Deep Dive

### Universal Web Conventions (2024+)

| Element | Expected position | Expected behaviour |
|---------|------------------|-------------------|
| Logo | Top-left | Links to homepage |
| Primary navigation | Top horizontal bar or left sidebar | Visible on desktop; hamburger on mobile |
| Search | Top-right or top-centre | Magnifying glass icon; expands on click/tap |
| Login / Account | Top-right | Avatar or "Sign in" text |
| Shopping cart | Top-right (e-commerce) | Icon with item count badge |
| Footer | Bottom | Contact, legal, sitemap links |
| "Back" | Top-left (mobile) or browser back | Returns to previous page |
| Breadcrumbs | Below top nav, above content | Clickable path: Home > Category > Page |

### Platform-Specific Conventions

| Platform | Convention | Breaking it causes |
|----------|-----------|-------------------|
| **iOS** | Back button top-left; tab bar bottom | Navigation confusion |
| **Android** | System back gesture; FAB bottom-right | Broken navigation flow |
| **Desktop web** | Right-click context menu; Ctrl/Cmd shortcuts | Frustration for power users |
| **Desktop apps** | Menu bar top; File/Edit/View order | Disorientation |

### When to Break Convention

Breaking convention is expensive. Only do it when:

1. **The new pattern is clearly better** AND you can teach it quickly
2. **The convention doesn't exist** for your use case (novel interaction type)
3. **Platform guidelines** explicitly recommend a different approach

**How to break convention safely:**
- Provide onboarding / tooltip for the new pattern
- Offer the conventional alternative as a fallback (e.g., drag-to-reorder + manual sort button)
- Test with real users -- what seems intuitive to you may confuse them

### Mental Model Alignment

Users arrive with mental models from prior experience:

| User expects | Because of | If you break it |
|-------------|-----------|-----------------|
| "Delete" is reversible (trash/undo) | Desktop OS, Gmail | Data loss, anger, support tickets |
| Swiping left in a list reveals actions | iOS Mail, messaging apps | Nothing happens, confusion |
| Clicking a logo goes home | Every website ever | Users get lost |
| Red means error/danger | Traffic lights, fire, blood | Misinterpretation of status |
| Search returns relevant results | Google | Frustration, abandonment |

**Rule:** When your mental model differs from the user's, the user's model wins. Adapt the interface, not the user.
