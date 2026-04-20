# Proximity & Similarity -- Deep Dive

The two most frequently applied Gestalt principles in UI design. Master these and you solve 80% of layout problems.

## Proximity in Practice

### The Spacing Scale

A consistent spacing scale is the implementation of Proximity. Use a base unit (4px or 8px) and build a scale:

```
4px   -- tight: related inline elements (icon + label)
8px   -- compact: items within a list, input padding
12px  -- snug: related form fields within a group
16px  -- default: between standard list items
24px  -- comfortable: between form groups, content blocks
32px  -- spacious: between major content sections
48px  -- generous: between page-level sections
64px  -- dramatic: hero sections, major visual breaks
```

**The rule:** Space within a group < space between groups. Always. If intra-group and inter-group spacing are equal, the grouping is invisible.

### Proximity Rules for Forms

Forms are where Proximity matters most:

1. **Label-to-field distance:** 4-8px. The label must be unmistakably attached to its field.
2. **Field-to-field distance (within group):** 12-16px. Close enough to be one unit.
3. **Group-to-group distance:** 24-32px. Noticeably larger than field-to-field.
4. **Section-to-section distance:** 32-48px. Clear separation.

**Test:** If you removed all borders and backgrounds, could a user still tell which fields belong together? If yes, your proximity is correct.

### Proximity Rules for Navigation

- Primary nav items: 8-16px between items in the same group
- Group separators: 24-32px or a visible divider
- Utility links (login, cart, search): spatially separated from primary nav
- Mobile: vertical stacking maintains proximity within tap-friendly spacing

### Proximity Rules for Cards

- Internal padding: 16-24px
- Between elements inside a card: 8-12px (title → description → meta)
- Between cards in a grid: 16-24px
- Between card groups/sections: 32-48px

### Common Proximity Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Labels far from their fields | Users associate label with wrong field | Reduce label-to-field gap to 4-8px |
| Equal spacing everywhere | No visual grouping | Use the spacing scale: vary gaps deliberately |
| Huge padding inside small cards | Content floats, feels disconnected | Match padding to content density |
| No gap increase between sections | Page feels like one flat list | Double the gap between logical sections |

---

## Similarity in Practice

### The Similarity Audit

Review your interface for these consistency requirements:

**Links:** All text links must share identical styling.
- Same colour (e.g., blue, brand accent)
- Same text decoration (underline, none on hover, etc.)
- Same hover/focus behaviour
- If some links look different from others, users can't predict clickability

**Buttons:** Buttons of the same importance level must look identical.
- Primary buttons: same fill colour, border radius, padding, font weight
- Secondary buttons: same outline style, same colour but lower visual weight
- Destructive buttons: consistently different (typically red or with warning icon)
- Never mix 3+ button styles at the same hierarchy level

**Icons:** Icon families must be visually uniform.
- Same stroke weight (1px, 1.5px, 2px -- pick one)
- Same dimensions (24x24, 20x20 -- pick one per context)
- Same style (outlined, filled, or duotone -- don't mix within a set)
- Same corner radius and line cap

**Form inputs:** All inputs of the same type must look identical.
- Same border colour, radius, and width
- Same padding, font size, and placeholder colour
- Same focus ring colour and width
- Disabled/readonly states consistent across all inputs

**Status indicators:** Consistent colour-meaning mapping.
- Green = success/active
- Yellow/amber = warning/pending
- Red = error/inactive/destructive
- Blue = informational/neutral
- Never reuse a status colour for a different meaning

### Breaking Similarity Intentionally

Breaking similarity creates a focal point. Use this for:

1. **Primary CTA:** One button that's visually different from all others on the page
2. **Error states:** Red border on the invalid field among normal-bordered fields
3. **Highlighted row:** One table row with a different background
4. **Featured item:** One card with a different border, shadow, or badge

**Rule:** Only one element per context should break similarity. Multiple breaks compete and cancel each other out.

### Similarity + Proximity Combined

The strongest non-connected grouping: elements that are both close together AND look alike.

Example: A dashboard with three metric cards (same size, same style, same spacing) reads as "these metrics belong together" without any labels or borders saying so.

When Similarity and Proximity conflict (elements look alike but are far apart, or look different but are close), resolve by:
1. Adding Common Region (a container) to override both
2. Or adjusting one principle to align with the other
