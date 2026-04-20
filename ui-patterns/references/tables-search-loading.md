# Tables, Search, Loading & Notifications -- Deep Dive

Patterns for data display, search interfaces, async feedback, and user notifications.

## Table Patterns

### Design Rules

| Rule | Why | Implementation |
|------|-----|----------------|
| Right-align numbers | Easier decimal/digit comparison | `text-align: right` on numeric columns |
| Left-align text | Natural reading direction (LTR) | Default alignment |
| Sticky headers | Column labels stay visible during scroll | `position: sticky; top: 0` |
| Row distinction | Scanability in dense data | Zebra striping OR subtle bottom borders (not both) |
| Sortable columns | User-driven data organisation | Click column header; show sort direction icon |
| Row hover | Help track the eye across wide tables | Subtle background change on `:hover` |

### Responsive Table Strategies

| Strategy | How it works | Best for |
|----------|-------------|----------|
| **Horizontal scroll** | Table scrolls horizontally in a container | Complex data tables with many columns |
| **Priority columns** | Show critical columns; hide others behind "expand" | Tables with clear primary/secondary columns |
| **Stacked cards** | Each row becomes a card on mobile | < 20 rows, heterogeneous content |
| **Collapsed rows** | Show summary; expand for full row | Large datasets with detail-on-demand |

**Rules:**
- Always indicate horizontal scroll (shadow, fade, or partial column visible)
- Never make the table wider than the viewport without scroll indication
- Maintain column header association when stacking (label: value format)
- Keep the primary action column (checkboxes, actions) visible during scroll

### Data Table Interactions

| Feature | When to include | How |
|---------|----------------|-----|
| **Sort** | Any tabular data | Click column header; toggle asc/desc; show arrow |
| **Filter** | > 20 rows | Filter controls above table; show active filter count |
| **Search** | > 50 rows | Search input above table; highlight matching text |
| **Pagination** | > 25-50 rows | Below table; show total count; adjustable page size |
| **Select / bulk actions** | Admin interfaces | Checkboxes on rows; floating action bar on selection |
| **Inline edit** | Frequently updated data | Click cell to edit; save on blur or explicit action |
| **Export** | Analytics, reporting | Button above table; CSV/Excel format options |

---

## Search Patterns

### Core Search UI

```
┌──────────────────────────────────┐
│  🔍  Search products...         │
├──────────────────────────────────┤
│  Recent searches                 │
│  • blue running shoes           │
│  • wireless headphones          │
├──────────────────────────────────┤
│  Suggested                      │
│  • bluetooth speaker            │
│  • bluetooth headphones         │
└──────────────────────────────────┘
```

### Search Design Rules

| Rule | Why | Implementation |
|------|-----|----------------|
| Prominent placement | Users expect to find search easily | Top of page, centred or right-aligned |
| Magnifying glass icon | Universal search signifier | Icon inside or beside input |
| Autocomplete / suggestions | Recognition over recall | Debounced suggestions (200-300ms after typing stops) |
| Preserve query | Users need to modify searches | Keep search text in input after results load |
| Result count | Orientation and expectation setting | "Showing 12 of 156 results" |
| No-results state | Prevent dead ends | Show suggestions, categories, or contact support |
| Recent searches | Recognition over recall | Show on focus before typing begins |

### Search Result Design

| Element | Purpose | Rules |
|---------|---------|-------|
| Title | Primary match identifier | Bold, clickable, highlight matching terms |
| Snippet | Context for the match | 1-2 lines, highlight matching terms in context |
| URL / path | Location context | Muted, truncated, shows hierarchy |
| Metadata | Secondary info | Date, author, category -- muted styling |
| Image | Visual recognition | Thumbnail if available |
| Action | Direct interaction | "Add to cart", "Open", "Preview" |

### Null State Design

When search returns no results:

1. **Acknowledge** the search: "No results for 'xyzzy'"
2. **Check spelling**: "Did you mean 'xyz'?"
3. **Suggest alternatives**: "Try these popular searches..."
4. **Offer help**: "Browse categories" or "Contact support"
5. **Never show an empty page** with no guidance

---

## Loading State Patterns

### The Loading Decision Tree

```
Duration known?
├── Yes → Determinate progress bar (percentage, steps)
└── No
    ├── Duration < 400ms → No indicator needed
    ├── Duration 400ms-2s → Indeterminate spinner or skeleton
    └── Duration > 2s → Spinner + status text ("Loading messages...")
```

### Skeleton Screen Design

Skeleton screens are grey placeholder blocks that mirror the layout of the content being loaded.

**Rules:**
1. **Match the layout exactly** -- skeleton should be indistinguishable from content at a glance
2. **Use subtle animation** -- shimmer (left-to-right gradient) or pulse (opacity animation)
3. **Replace progressively** -- content appears section by section, not all at once
4. **Don't flash** -- if content loads in < 300ms, don't show skeleton (show nothing instead)

**Skeleton block styling:**
- Background: neutral grey (`#e0e0e0` or equivalent)
- Border radius: match the content it represents (rounded for avatars, straight for text)
- Height: match the content height (don't collapse or expand when real content loads)
- Animation: 1.5-2s cycle, ease-in-out

### Progress Bar Design

| Type | When to use | Implementation |
|------|-------------|----------------|
| **Determinate** | Known total (file upload, multi-step) | Show percentage + progress fill |
| **Indeterminate** | Unknown duration | Animated bar moving back and forth |
| **Stepped** | Multi-step process | "Step 2 of 4" with segmented bar |
| **Circular** | Compact spaces | Circular progress ring (e.g., upload thumbnail) |

**Progress bar rules:**
- Start with initial progress (5-10%) -- a bar at 0% feels stuck
- Non-linear perceived speed: faster at the start, slower near the end feels right
- Include percentage text for long operations
- Status messages for operations > 5s ("Processing payment...", "Generating report...")
- Allow cancellation for operations > 2s

### Optimistic UI

Show the result immediately. Sync in the background. Roll back only on failure.

**Pattern:**

```
User clicks "Like" →
  1. Immediately: heart fills, count increments
  2. Background: API call to save
  3a. Success: no visible change (already shown)
  3b. Failure: heart unfills, count decrements, show toast error
```

**Candidates for optimistic UI:**
- Likes, follows, bookmarks (high success rate, low stakes)
- Message sending (show in chat immediately)
- Settings toggles (apply immediately)
- Adding to cart (show badge immediately)

**Not candidates:**
- Payment processing
- Account deletion
- Publishing content (moderation required)
- File uploads (need actual transfer)

---

## Notification Patterns

### Notification Types

#### Toast Notifications

```
┌──────────────────────────────┐
│ ✓ Message sent successfully  │  ← Auto-dismiss: 3-5 seconds
│                    [Undo]    │  ← Optional action
└──────────────────────────────┘
```

**Rules:**
- Auto-dismiss after 3-5 seconds for success messages
- Position: top-right (desktop) or top-centre (mobile)
- Stack vertically if multiple appear
- Include undo action for reversible operations
- Never use for errors (errors must persist)

#### Banner Notifications

```
┌──────────────────────────────────────────┐
│ ⚠ Your subscription expires in 3 days.   │
│                           [Renew] [✕]    │
└──────────────────────────────────────────┘
```

**Rules:**
- Persistent until user dismisses or takes action
- Full-width, top of page or section
- Include clear action button and dismiss (X)
- Colour-coded: info (blue), warning (yellow), error (red), success (green)
- Maximum 2 banners visible simultaneously

#### Inline Feedback

```
┌─────────────────────────────┐
│  Email address              │
│  ┌────────────────────────┐ │
│  │ not-valid               │ │
│  └────────────────────────┘ │
│  ⚠ Email must include @     │  ← Inline, next to source
└─────────────────────────────┘
```

**Rules:**
- Appears directly below or beside the source element
- Persistent until the issue is resolved
- Icon + text (never colour alone)
- Field border colour changes as reinforcement

### Notification Stacking

When multiple notifications appear simultaneously:

1. Stack vertically with 8px gap
2. Newest on top (or bottom, but be consistent)
3. Maximum 3 visible at once; queue additional
4. Each independently dismissible
5. "Dismiss all" option when > 2 visible

### Empty States

Empty states are a type of notification -- they tell users "there's nothing here yet":

**Required elements:**
1. Clear explanation of what would appear here
2. Visual (illustration or icon) to prevent the page from feeling broken
3. Action to resolve the empty state ("Create your first project")
4. Optional: link to help/documentation

```
┌──────────────────────────────────────┐
│                                      │
│          📂 No projects yet          │
│                                      │
│   Create your first project to       │
│   get started.                       │
│                                      │
│        [ Create Project ]            │
│                                      │
└──────────────────────────────────────┘
```
