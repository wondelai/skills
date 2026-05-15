# Common Region & Uniform Connectedness -- Deep Dive

Container-based and connection-based grouping -- the explicit tools for when spacing and similarity aren't enough.

## Common Region in Practice

### When to Use Containers

Containers (cards, panels, fieldsets, coloured backgrounds) explicitly group elements. Use them when:

1. **Proximity alone is ambiguous** -- elements from different groups are too close to separate spatially
2. **Mixed content types** -- grouped elements don't share visual similarity (image + text + button)
3. **Interaction boundaries** -- the user needs to know "this is one clickable unit" (cards)
4. **Section identity** -- the group needs a visible identity (settings panels, feature blocks)

### Container Patterns

| Pattern | Structure | Use case |
|---------|-----------|----------|
| **Card** | Border or shadow + padding | Discrete content units (products, articles, users) |
| **Panel** | Background colour + padding | Settings groups, sidebar sections |
| **Fieldset** | Border + legend/label | Form field groups |
| **Well / Inset** | Recessed background | Code blocks, quoted content, secondary info |
| **Stripe** | Full-width background colour | Page sections (hero, features, testimonials) |
| **Chip / Tag** | Tight border + small padding | Labels, categories, filters |

### Card Design Rules

Cards are the most common Common Region pattern. Rules:

1. **One primary action per card.** The card itself should be the clickable target for the primary action. Secondary actions go in a menu or footer.
2. **Consistent dimensions** within a grid. Same height per row minimum; same width preferred.
3. **Internal hierarchy:** Image > Title > Description > Meta. Apply Proximity within the card.
4. **Maximum 3-4 pieces of information.** Beyond that, the card loses scanability.
5. **Don't overload.** If a card needs tabs or scrolling, it's not a card -- it's a page.

### Container Nesting Rules

Avoid deep nesting. Maximum 2 levels: page → card, or page → panel → card.

```
❌ Bad: Page → Section → Panel → Card → Nested Card
✅ Good: Page → Section → Card
✅ Good: Page → Panel → Card (2 levels max)
```

**Why:** Each nesting level adds visual complexity (borders, shadows, backgrounds stacking). Beyond 2 levels, the interface becomes noisy and the grouping hierarchy is lost.

### Container vs Spacing

**Use spacing (Proximity) when:**
- The grouping is within a single context (fields in a form, items in a list)
- Adding a container would create unnecessary visual noise
- The layout is simple and spacing alone communicates structure

**Use containers (Common Region) when:**
- Multiple content types need to appear as one unit (card with image + text + button)
- The group needs to be interactive as a whole (clickable card)
- You need to override proximity-based grouping
- The group has a distinct identity or purpose within the page

---

## Uniform Connectedness in Practice

### The Strongest Grouping Principle

Uniform connectedness -- visual connections between elements -- is the strongest Gestalt grouping principle. It overrides proximity, similarity, and common region.

Use it for relationships that must be unambiguous.

### Connection Patterns

| Pattern | Implementation | Use case |
|---------|---------------|----------|
| **Step connector** | Horizontal or vertical line between numbered circles | Multi-step processes, wizards, checkout flows |
| **Tree connector** | Lines with branches | File trees, org charts, nested navigation |
| **Flow connector** | Arrows between boxes | Process diagrams, data flow, architecture |
| **Timeline connector** | Vertical line with branching events | Activity feeds, history, changelog |
| **Label connector** | Line from label to element | Annotations, tooltips, diagram callouts |

### Step Indicator Design

The most common Uniform Connectedness pattern in UI:

```
( 1 )----( 2 )----( 3 )----( 4 )
 Cart    Shipping  Payment  Confirm
```

**Rules:**
1. Completed steps: filled circle, checkmark, or solid colour
2. Current step: highlighted, larger, or animated
3. Future steps: outlined, muted, or greyed
4. Connecting line: solid for completed transitions, dashed for pending
5. Labels below or beside each step -- never rely on numbers alone
6. Clickable completed steps allow backward navigation

### Timeline / Activity Feed Design

Vertical Uniform Connectedness:

```
 ● Event 1 -- 2 hours ago
 |   Description...
 |
 ● Event 2 -- 5 hours ago
 |   Description...
 |
 ○ Event 3 -- Yesterday
    Description...
```

**Rules:**
1. Continuous line connects all events
2. Most recent at top (reverse chronological)
3. Filled circles for significant events, empty for minor
4. Date/time stamps visible for each event
5. Line breaks or gaps signal time jumps

### Conditional Form Connections

Show relationships between form fields using visual connectors:

```
[  Country  ▼ ]
       |
       ├── If "US": [  State  ▼ ] [  ZIP Code  ]
       └── If "UK": [  County   ] [  Postcode   ]
```

Use indentation + connecting lines to show that sub-fields depend on the parent selection. This is clearer than dynamically showing/hiding fields without visual context.

### When NOT to Use Connections

- **Between all elements in a list** -- proximity is sufficient
- **Between unrelated content** -- connections imply relationships; don't create false ones
- **In dense layouts** -- too many lines create visual chaos; use proximity and similarity instead
- **For decoration** -- lines must communicate meaning; decorative lines add noise
