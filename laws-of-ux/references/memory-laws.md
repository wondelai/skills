# Memory Laws -- Miller's Law, Serial Position, Zeigarnik Effect

How human memory limitations and biases affect interface design.

## Miller's Law Deep Dive

### What Miller Actually Said

George Miller's 1956 paper is often misquoted as "the magic number 7." What he actually demonstrated:

- Short-term memory can hold approximately **7 +/- 2 chunks** of information
- The key word is **chunks** -- grouped, meaningful units, not individual items
- Chunking is the strategy: group items into meaningful patterns to increase effective capacity
- Modern research suggests the actual limit may be closer to **4 +/- 1** for novel information

### Chunking Strategies for UI

| Content type | Without chunking | With chunking |
|-------------|------------------|---------------|
| Phone number | 5551234567 | (555) 123-4567 |
| Credit card | 4242424242424242 | 4242 4242 4242 4242 |
| IBAN | DE89370400440532013000 | DE89 3704 0044 0532 0130 00 |
| Serial number | A8B2C4D6E9F1 | A8B2-C4D6-E9F1 |
| Long content | 15 paragraphs in sequence | 5 sections with 3 paragraphs each |
| Navigation | 20 flat links | 4 categories with 5 links each |
| Settings | 30 toggles | 6 groups with 5 settings each |

### Input Masking Implements Miller's Law

Automatically format user input into chunks:

```
Input: 4242424242424242
Display: 4242 4242 4242 4242

Input: 15551234567
Display: +1 (555) 123-4567

Input: 12252025
Display: 12/25/2025
```

**Implementation rules:**
- Apply formatting as the user types (not just on blur)
- Never reject input because of formatting -- strip formatting before validation
- Show the formatted version in the field
- Allow paste of unformatted values

### Dashboard Design and Miller's Law

Dashboards are the most common Miller's Law violation:

**Problem:** 20+ metrics visible simultaneously, each competing for attention.
**Solution:** Group into panels of 3-5 related metrics.

```
┌─ Revenue ─────────┐  ┌─ Users ───────────┐  ┌─ Performance ─────┐
│ Total: $142K       │  │ Active: 12,450     │  │ Uptime: 99.97%    │
│ Growth: +12%       │  │ New: 1,230         │  │ Avg Response: 82ms│
│ MRR: $48K          │  │ Churn: 2.1%        │  │ Error Rate: 0.3%  │
└────────────────────┘  └────────────────────┘  └────────────────────┘
```

Each panel is one "chunk" -- the brain processes 3 panels (within capacity) instead of 9 individual metrics.

---

## Serial Position Effect

### The Pattern

Users remember:
- **First items** (primacy effect) -- they get the most rehearsal
- **Last items** (recency effect) -- they're still in short-term memory
- **Middle items** -- most likely to be forgotten

### Design Implications

| Context | First position | Last position | Middle |
|---------|---------------|---------------|--------|
| Navigation | Most important link | Second most important | Less critical links |
| Lists | Key item or recommended option | CTA or summary | Supporting details |
| Onboarding | Most impactful feature | Clear next step | Additional features |
| Pricing | Free/entry plan | Enterprise/contact | Standard plans |
| Tab bars | Home/primary screen | Profile/account | Secondary screens |

### Practical Application

- **Tab bar:** Home (first) and Profile (last) are most used; middle tabs get less engagement
- **Feature lists:** Lead with the strongest feature; end with the CTA. Middle features are skimmed.
- **Error messages:** Start with what went wrong; end with how to fix it. Middle context is often skipped.

---

## Zeigarnik Effect

### The Pattern

People remember **uncompleted tasks** better than completed ones. Interrupted activities create cognitive tension that persists until resolution.

### Design Applications

| Pattern | How it leverages Zeigarnik | Example |
|---------|---------------------------|---------|
| **Progress bars** | Incomplete fill creates tension to complete | "Profile 70% complete" |
| **Saved drafts** | Unfinished work stays salient in memory | "You have an unfinished post" |
| **Streak indicators** | Breaking a streak creates tension | "15-day streak -- don't break it!" |
| **Abandoned cart emails** | Reminding of unfinished purchase | "You left items in your cart" |
| **Checklists** | Unchecked items demand completion | "3 of 5 setup steps completed" |
| **Cliffhangers** | Incomplete content motivates return | "Next episode in 5..." |

### Ethical Considerations

The Zeigarnik Effect is powerful for engagement but easily abused:

**Ethical uses:**
- Helping users complete tasks they started and want to finish (onboarding, checkout)
- Saving progress so users can return without starting over
- Showing progress toward a goal the user set themselves

**Unethical uses:**
- Artificial incompleteness to manufacture engagement ("Profile incomplete" when it's perfectly functional)
- Pressure through streaks that penalise breaks
- Guilt-inducing notifications about "unfinished" tasks the user abandoned intentionally
- Fake urgency ("Your cart is expiring!")

**Rule:** Use Zeigarnik to help users accomplish **their** goals, not to manufacture anxiety that serves **your** metrics.

---

## Recognition vs Recall

### The Principle

Recognition (identifying among options) is easier than recall (retrieving from memory). Interfaces should minimise recall demands.

### Design Checklist

| Recall (avoid) | Recognition (prefer) |
|----------------|---------------------|
| "Enter the product code" | Dropdown/search with product names and images |
| "Type your previous search" | Recent searches shown on focus |
| "Remember your settings from last time" | Settings visible and pre-filled |
| Blank text field for category | Tags, pills, or checkboxes to select |
| "Which page were you on?" | Breadcrumbs showing current path |
| "Enter the file path" | File browser with visual thumbnails |

### Search Design for Recognition

Search should show recognition cues, not demand recall:

1. **Autocomplete:** Suggest matches as the user types
2. **Recent searches:** Show on focus (before typing)
3. **Search results:** Include images, descriptions, and context -- not just titles
4. **Filters as recognition:** Faceted search with visible categories
5. **"Did you mean...":** Correct spelling without demanding the user recall the exact term
