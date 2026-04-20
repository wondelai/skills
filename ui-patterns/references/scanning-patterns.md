# Scanning Patterns -- Deep Dive

How users visually process web pages and how to design for their scanning behaviour.

Source: Nielsen Norman Group eye-tracking research, Interaction Design Foundation.

## The F-Pattern

### When It Occurs

The F-pattern emerges under three conditions:
1. Text lacks web formatting (no bolding, bullets, subheadings)
2. Users prioritise efficiency (scanning, not reading)
3. Users lack strong motivation to read every word

It is the **default** scanning pattern -- the fallback when no visual hierarchy guides the eye. Good design prevents F-pattern scanning by providing clear entry points.

### Eye-Tracking Findings

Research shows:
- First lines receive significantly more fixations than subsequent lines
- Initial words on the left of each line get more attention than words further right
- The pattern holds on both desktop and mobile
- In RTL languages (Arabic, Hebrew), the pattern mirrors to a flipped F
- Users skip large chunks of content based on how text flows in a column

### Eight Techniques to Combat F-Pattern Scanning

1. **Place the most important points in the first two paragraphs** -- these get the most attention
2. **Use visually prominent headings and subheadings** -- they act as scanning anchors
3. **Start headings with information-carrying words** -- users may see only the first 2-3 words
4. **Visually group related content** with borders, backgrounds, or proximity
5. **Bold critical words and phrases** within body text
6. **Use distinct link styling** with information-bearing words (never "click here")
7. **Use bullets and numbered lists** for sequences and feature lists
8. **Remove unnecessary content** -- every word competes with every other word

### Content Placement Rules

| Position | Attention level | Best for |
|----------|----------------|----------|
| Top-left | Highest | Brand, primary heading, most critical info |
| Top horizontal band | High | Headlines, navigation, key message |
| Left edge (vertical) | Medium-high | Headings, bullet starts, labels |
| Right side | Lower | Secondary info, sidebar, ads |
| Below the fold | Low (unless scrolling is encouraged) | Supporting content, details |

---

## The Z-Pattern

### When to Use

The Z-pattern applies to pages with minimal text and a clear visual flow:
- Landing pages and hero sections
- Splash screens and app store listings
- Print ads and poster layouts
- Marketing emails (above the fold)

### The Four Zones

```
Zone 1 (top-left) ──────→ Zone 2 (top-right)
         ↘
              ↘
                   ↘
Zone 3 (bottom-left) ───→ Zone 4 (bottom-right)
```

| Zone | Content to place | Example |
|------|-----------------|---------|
| Zone 1 | Logo, brand mark | Company logo |
| Zone 2 | CTA or key action | "Sign Up Free" button |
| Zone 3 | Key message, value prop | "Build faster with AI" headline |
| Zone 4 | Primary CTA (conversion) | "Start Your Free Trial" button |

### Repeated Z-Patterns

Long landing pages use **zig-zag layouts** -- alternating image-left/text-right and text-left/image-right sections:

```
[Image]  [Text + CTA]
[Text + CTA]  [Image]
[Image]  [Text + CTA]
```

Each row follows a mini Z-pattern, creating a natural reading flow down the page.

---

## Visual Weight

### What Creates Visual Weight

Visual weight determines which elements attract the eye first. From strongest to weakest:

| Factor | How it works | High weight | Low weight |
|--------|-------------|-------------|------------|
| **Size** | Larger = heavier | 48px heading | 14px body text |
| **Contrast** | More contrast = heavier | Dark text on white | Light grey on white |
| **Colour saturation** | Vivid = heavier | Bright red CTA | Muted grey link |
| **Whitespace** | More surrounding space = heavier | Isolated hero heading | Dense paragraph |
| **Density / complexity** | More detail = heavier | Photo or illustration | Solid colour block |
| **Position** | Top and left = heavier (LTR) | Top-left content | Bottom-right content |
| **Imagery** | Faces > objects > text | Portrait photo | Icon |

### The Three-Level Hierarchy

Every page needs exactly three distinct visual weight levels:

| Level | Role | Visual treatment |
|-------|------|-----------------|
| **Dominant** | Single entry point -- what users see first | Largest, highest contrast, most whitespace |
| **Sub-dominant** | Secondary focal points | Medium size, accent colour, moderate contrast |
| **Subordinate** | Supporting content | Body text, muted colours, standard sizing |

**Critical rule:** Create distinct levels, not a continuum. If users can't tell which level an element belongs to, the hierarchy is too subtle.

### Visual Weight and Content Priority

Map visual weight to content importance:

1. Determine content priority: What must users see first? Second? Third?
2. Assign visual weight: Highest priority gets most weight (dominant level)
3. Create clear separation: Each level must be noticeably different from the others
4. Test by squinting: If you blur the page, can you still identify the three levels?

### Visual Direction

Visual direction guides the eye from one element to the next:

| Technique | How it creates direction | Example |
|-----------|------------------------|---------|
| Lines and arrows | Explicit directional cue | Step connectors, flow diagrams |
| Pointing imagery | People looking / pointing toward content | Person looking at CTA |
| Size gradient | Eye moves from large to small | Hero heading → subheading → body |
| Colour gradient | Eye follows colour intensity | Saturated header → muted body |
| Alignment | Eye follows alignment axis | Left-aligned elements guide downward |
| Whitespace channel | Eye follows the open path | Gutters between columns guide vertical flow |
