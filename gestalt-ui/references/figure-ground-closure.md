# Figure-Ground & Closure -- Deep Dive

How users distinguish foreground from background, and how the brain completes incomplete visual information.

## Figure-Ground in Practice

### Establishing Clear Figure-Ground

The figure is what the user should focus on. The ground is everything else. Ambiguous figure-ground forces the brain to oscillate, causing confusion and cognitive load.

**Techniques for stable figure-ground:**

| Technique | How it works | Example |
|-----------|-------------|---------|
| **Contrast** | Higher contrast = figure | Dark text on light background; bright CTA on muted section |
| **Size** | Smaller overlapping element = figure | A modal (small) over a page (large) |
| **Elevation / Shadow** | Elevated elements = figure | Cards with shadow on flat background |
| **Blur / Dim** | Blurred elements = ground | Dimmed backdrop behind a modal dialog |
| **Saturation** | More saturated = figure | Colourful CTA on desaturated hero image |
| **Convexity** | Convex shapes = figure | Rounded buttons and badges on flat surfaces |

### Elevation Hierarchy

Use shadow depth to create consistent figure-ground layers:

```
Level 0  -- Flat surface (page background, ground)
Level 1  -- Subtle lift (cards, input fields)
           box-shadow: 0 1px 3px rgba(0,0,0,0.12)
Level 2  -- Moderate elevation (dropdowns, popovers)
           box-shadow: 0 4px 6px rgba(0,0,0,0.1)
Level 3  -- High elevation (modals, dialogs)
           box-shadow: 0 10px 25px rgba(0,0,0,0.15)
Level 4  -- Maximum elevation (notifications, tooltips)
           box-shadow: 0 15px 35px rgba(0,0,0,0.2)
```

**Rules:**
- Higher elevation = closer to the user = more attention
- Never place a lower-elevation element on top of a higher one
- Consistent shadow direction (typically top-left light source)
- Dark mode: use lighter surfaces instead of shadows for elevation

### Figure-Ground for Modals

Modals are the most explicit figure-ground pattern in UI:

1. **Scrim:** Dark semi-transparent overlay (ground) behind the modal (figure)
2. **Blur:** Optional -- blurring the background further separates layers
3. **Focus trap:** Keyboard focus locked within the modal reinforces it as figure
4. **Dismiss:** Clicking the scrim closes the modal -- returning to the background as figure

**Common mistakes:**
- Scrim too transparent -- ground competes with figure
- No scrim at all -- modal floats ambiguously over active content
- Multiple modals stacked -- figure-ground becomes figure-figure-ground (confusing)

### Figure-Ground for Navigation

Sidebar navigation uses figure-ground:
- Sidebar (darker background) = ground/context
- Main content (lighter, more spacious) = figure/focus
- Active nav item: inverted figure-ground within the sidebar (highlighted item = figure within the sidebar ground)

---

## Closure in Practice

### How Closure Works in UI

The brain completes patterns when given enough visual information. This means you can communicate "more content exists" without showing it explicitly.

### Carousel / Horizontal Scroll Patterns

**The peek pattern:** Show 10-20% of the next item at the edge of the viewport.

```
[  Card 1  ][  Card 2  ][  Card 3  ][ Ca...
                                     ^
                           Partial card = "scroll for more"
```

**Rules:**
- Show enough of the next item to be recognisable (not just a sliver)
- Don't show a partial item if there's nothing to scroll to (false closure)
- Combine with scroll indicators (dots, arrows) for reinforcement
- Fade-out gradients can substitute for partial items

### Progress and Completion

Closure drives progress indicators:

- **Progress bars:** Incomplete fill implies a complete target. The brain sees "how much is left" automatically.
- **Step indicators:** Completed steps (filled circles) vs incomplete (empty circles). The brain wants to fill them all.
- **Checklists:** Unchecked items create tension (Zeigarnik Effect + Closure) that motivates completion.
- **Circular progress:** Incomplete ring strongly implies the complete circle.

### Truncation Patterns

Text and content truncation relies on Closure:

| Pattern | Signal | User inference |
|---------|--------|----------------|
| `"This is a long title that..."` | Ellipsis | "There's more text -- I can expand" |
| `"Showing 5 of 23 results"` | Count | "I can load more" |
| Gradient fade at bottom of a container | Visual fade | "Content continues below" |
| `"Read more"` link | Explicit | "There's more content -- click to see" |

**Rules:**
- Always provide a way to see the full content (expand, navigate, tooltip)
- Never truncate critical information (prices, error messages, CTAs)
- Ellipsis should appear at word boundaries, not mid-word
- "Show more" is better than silent truncation for important content

### False Closure (Anti-pattern)

False closure occurs when visual cues suggest more content exists, but it doesn't:

- A partial card at the carousel edge, but scrolling reveals nothing
- A "Load more" button that loads zero results
- A progress bar that jumps from 90% to stuck at 99%
- An empty space at the bottom of a list that looks like it should scroll

**Fix:** Only use closure cues when they're truthful. If there's no more content, don't show partial elements.
