# Navigation & Form Patterns -- Deep Dive

Detailed guidance for the two highest-impact component categories.

## Navigation Deep Dive

### The Three Questions Framework

Every navigation system must answer:

| Question | Implementation | Common failure |
|----------|---------------|----------------|
| **"Where am I?"** | Active nav state, breadcrumbs, page title | Responsive nav hides current page indicator |
| **"Where can I go?"** | Visible menu items, category structure | Too many items or hidden behind hamburger |
| **"Where have I been?"** | Visited link state, breadcrumbs, history | No visited state; breadcrumbs missing |

### Mobile Navigation Patterns

#### Bottom Tab Bar (3-5 Primary Destinations)

```
┌────────────────────────────────┐
│                                │
│         Page Content           │
│                                │
├──────┬──────┬──────┬──────┬────┤
│ Home │Search│ Add  │ Inbox│ Me │
│  🏠  │  🔍  │  ➕  │  📥  │ 👤 │
└──────┴──────┴──────┴──────┴────┘
```

**Rules:**
- Maximum 5 tabs; use "More" for additional destinations
- Icon + label always (never icon-only)
- Active tab visually distinct (colour, weight, fill)
- Centre tab can be elevated for primary action (FAB style)
- Tab labels: 1-2 words maximum

#### Hamburger Menu (Complex Navigation)

**When to use:** Mobile viewport with > 5 navigation items or multi-level hierarchy.

**Rules:**
- Label with "Menu" text alongside the hamburger icon
- Full-screen or drawer overlay (not tiny dropdown)
- Show current page indicator within the expanded menu
- Allow closing via X button, swipe, and backdrop tap
- Animate open/close (slide or fade, 200-300ms)

#### Pull-to-Refresh

- Use only for content feeds (timeline, inbox, news)
- Show clear indicator (spinner + "Pull to refresh" text)
- Provide loading feedback during refresh
- Don't use for non-feed content (settings, profiles, forms)

### Desktop Navigation Patterns

#### Sidebar Navigation (Apps / Dashboards)

```
┌──────────┬────────────────────┐
│ Logo     │ Top Bar / Search   │
├──────────┤                    │
│ Dashboard│                    │
│ Projects │   Main Content     │
│ Team     │                    │
│ Settings │                    │
│          │                    │
│ ──────── │                    │
│ Help     │                    │
│ Logout   │                    │
└──────────┴────────────────────┘
```

**Rules:**
- Collapsible to icons-only for more content space
- Active item clearly highlighted (background colour, left border)
- Group items with dividers or section headers
- Sticky/pinned items at bottom (help, logout, settings)
- Width: 200-280px expanded, 56-72px collapsed

#### Breadcrumbs

```
Home > Products > Electronics > Headphones
```

**Rules:**
- All items except the current page are clickable links
- Separator: ">" or "/" (consistent throughout the site)
- Current page in bold or non-linked text
- Don't use for flat site structures (no hierarchy = no breadcrumbs)
- Show on all viewport sizes, not just desktop
- Truncate middle items on mobile: Home > ... > Headphones

---

## Form Design Deep Dive

### Label Placement Evidence

| Position | Completion time | Error rate | Best for |
|----------|----------------|------------|----------|
| **Above field** | Fastest | Lowest | All forms (default choice) |
| Left-aligned | Slower (eye movement) | Higher | Dense admin forms |
| Right-aligned | Medium | Medium | Compact horizontal layouts |
| Inside (placeholder) | Varies | Highest | Never (disappears on focus) |

**Verdict:** Labels above fields is the only universally recommended pattern.

### Input Field Patterns

#### Text Input

```html
<label for="email">Email address</label>
<input type="email" id="email" autocomplete="email"
    placeholder="you@example.com" inputmode="email">
```

- `type` controls validation
- `inputmode` controls mobile keyboard
- `autocomplete` enables browser autofill
- `placeholder` shows format hint (but is NOT a label)

#### Common Input Types and Keyboards

| Data | HTML type | inputmode | Keyboard shown |
|------|-----------|-----------|----------------|
| Email | `email` | `email` | @ symbol visible |
| Phone | `tel` | `tel` | Numeric with + |
| Number | `text` | `numeric` | Number pad |
| URL | `url` | `url` | .com shortcut |
| Search | `search` | `search` | Search/Go button |
| Password | `password` | -- | Default with show/hide toggle |
| Currency | `text` | `decimal` | Numbers + decimal |

**Note:** Use `type="text"` with `inputmode="numeric"` for numbers you don't want browser up/down arrows on (credit cards, PINs).

### Validation Patterns

#### Timing

| When | How | Use for |
|------|-----|---------|
| On blur (leaving field) | Show error below field | Most fields (default) |
| On change (after first error) | Clear error when corrected | Recovery from initial error |
| On submit | Show all errors | Final validation pass |
| Real-time (while typing) | Only for format feedback | Character count, password strength |

#### Error Message Formula

**What happened** + **How to fix it**

| Bad | Good |
|-----|------|
| "Invalid input" | "Email address must include @" |
| "Error in field 3" | "Phone number must be 10 digits" |
| "Required" | "Please enter your first name" |
| "Password too weak" | "Password must include a number and a special character" |

#### Error Display

```
┌─────────────────────────────┐
│  Email address              │
│  ┌────────────────────────┐ │
│  │ not-an-email           │ │
│  └────────────────────────┘ │
│  ⚠ Email must include @     │
└─────────────────────────────┘
```

**Rules:**
- Error message directly below the field (not in a distant summary)
- Icon + coloured text (never colour alone)
- Field border colour changes (reinforcement, not sole indicator)
- Error message visible without scrolling
- Don't clear the user's input on error

### Mobile Form Optimisations

1. **Full-width inputs** -- easier to tap, more typing space
2. **Large touch targets** -- 44px minimum field height
3. **Sticky submit button** -- fixed at bottom on long forms
4. **Section-by-section** -- break long forms into collapsible or stepped sections
5. **Address autocomplete** -- Google Places API or similar
6. **Camera card scanning** -- credit card capture for payment forms
7. **Biometric auth** -- fingerprint / face for login instead of password
