# Resource Loading and Critical Rendering Path

The browser converts raw bytes into rendered pixels through a precise pipeline. Understanding this pipeline reveals exactly which resources block rendering and how to eliminate or defer them.


## Table of Contents
1. [The Critical Rendering Path](#the-critical-rendering-path)
2. [Render-Blocking Resources](#render-blocking-resources)
3. [Async and Defer](#async-and-defer)
4. [Resource Hints](#resource-hints)
5. [Font Loading Strategies](#font-loading-strategies)
6. [Image Optimization](#image-optimization)
7. [Resource Loading Priority](#resource-loading-priority)
8. [Practical Loading Strategy](#practical-loading-strategy)

---

## The Critical Rendering Path

Every page load follows this sequence:

```
HTML bytes → Parse → DOM
                      ↓
CSS bytes  → Parse → CSSOM
                      ↓
              Render Tree (DOM + CSSOM)
                      ↓
                    Layout (geometry calculation)
                      ↓
                    Paint (pixel rendering)
                      ↓
                    Composite (layer assembly)
```

**The key insight:** The browser cannot paint anything until both the DOM and CSSOM are complete. CSS is **render-blocking**. JavaScript is **parser-blocking**. Every blocking resource directly adds to time-to-first-paint.

### DOM Construction

The browser receives HTML bytes, decodes them into characters, tokenizes them into tags, and builds the DOM tree. This is incremental -- the parser processes HTML as it arrives, building the tree progressively.

**When parsing stops:**
- A `<script>` tag without `async` or `defer` halts DOM construction. The browser must download the script, execute it (because it might call `document.write()`), and then resume parsing.
- The parser does not stop for CSS files, but rendering is blocked until CSS is parsed.

### CSSOM Construction

CSS files are fetched and parsed into the CSSOM (CSS Object Model). Unlike DOM construction:
- CSSOM is not incremental -- the browser waits for all CSS before computing styles
- CSS is render-blocking but not parser-blocking (DOM construction continues)
- A `<script>` after a `<link rel="stylesheet">` is blocked until the CSS loads (because the script might query computed styles)

### Render Tree

The render tree combines the DOM and CSSOM, containing only visible elements with their computed styles. Elements with `display: none` are excluded. The render tree triggers:

1. **Layout (reflow):** Calculates the exact position and size of each element
2. **Paint:** Fills in pixels -- text, colors, borders, shadows, images
3. **Composite:** Assembles painted layers into the final image (GPU-accelerated for transformed/animated elements)

## Render-Blocking Resources

### CSS is render-blocking

The browser will not render any content until all CSS in the `<head>` is loaded and parsed. This means:

```html
<!-- This CSS file blocks ALL rendering until loaded -->
<link rel="stylesheet" href="styles.css">
```

**Optimization strategies:**

**Inline critical CSS:** Extract the styles needed for above-the-fold content and embed them directly in the HTML:

```html
<head>
  <style>
    /* Critical styles for above-the-fold content */
    body { font-family: system-ui; margin: 0; }
    .hero { padding: 2rem; background: #f8f9fa; }
    .nav { display: flex; gap: 1rem; }
  </style>
  <!-- Load full stylesheet asynchronously -->
  <link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>
</head>
```

**Media queries for conditional CSS:** Stylesheets with media queries that do not match the current context are downloaded but do not block rendering:

```html
<!-- Blocks rendering (matches all screens) -->
<link rel="stylesheet" href="styles.css">

<!-- Does NOT block rendering on screen (only for print) -->
<link rel="stylesheet" href="print.css" media="print">

<!-- Does NOT block rendering below 768px -->
<link rel="stylesheet" href="desktop.css" media="(min-width: 768px)">
```

**Remove unused CSS:** Audit CSS with Chrome DevTools Coverage panel. Typical sites ship 60-90% unused CSS.

### JavaScript is parser-blocking

A `<script>` tag without attributes halts DOM parsing:

```html
<p>This paragraph is parsed</p>
<script src="app.js"></script>
<!-- DOM parsing stops until app.js downloads AND executes -->
<p>This paragraph waits</p>
```

## Async and Defer

The `async` and `defer` attributes change how scripts interact with the parser:

### `defer`

```html
<script src="app.js" defer></script>
```

- Downloads in parallel with DOM parsing (non-blocking)
- Executes **after** DOM parsing is complete, before `DOMContentLoaded`
- Multiple deferred scripts execute in document order
- **Best for:** Most application scripts that depend on the DOM

### `async`

```html
<script src="analytics.js" async></script>
```

- Downloads in parallel with DOM parsing (non-blocking)
- Executes **immediately** when download completes (may interrupt parsing)
- No guaranteed execution order between multiple async scripts
- **Best for:** Independent scripts that do not depend on DOM or other scripts (analytics, ads)

### Comparison

| Attribute | Download | Execution | Order guaranteed | Blocks parsing |
|-----------|----------|-----------|-----------------|----------------|
| None | Sequential | Immediately | Yes | Yes |
| `async` | Parallel | When ready | No | Briefly (during execution) |
| `defer` | Parallel | After DOM parsed | Yes | No |

### Module scripts

```html
<script type="module" src="app.mjs"></script>
```

Module scripts are deferred by default. Adding `async` to a module script makes it execute as soon as its dependency graph is resolved.

## Resource Hints

Resource hints allow developers to inform the browser about resources it will need, enabling earlier loading.

### `dns-prefetch`

Resolves the DNS for a domain before any request is made:

```html
<link rel="dns-prefetch" href="https://cdn.example.com">
```

- Cheapest hint -- only does DNS resolution
- Use for third-party domains (analytics, fonts, CDNs)
- Saves 20-120ms per domain

### `preconnect`

Resolves DNS, establishes TCP connection, and negotiates TLS:

```html
<link rel="preconnect" href="https://cdn.example.com">
```

- More expensive than `dns-prefetch` (holds a connection open)
- Use for origins you will definitely request from within seconds
- Limit to 2-4 critical origins to avoid wasting connections
- Always include `crossorigin` for CORS-enabled resources:

```html
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

### `preload`

Fetches a specific resource at high priority without blocking rendering:

```html
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/hero.webp" as="image">
<link rel="preload" href="/critical.css" as="style">
```

- **The `as` attribute is required** -- it sets the correct priority and CORS mode
- Fetches immediately at high priority
- Does not apply the resource (does not render CSS, execute JS, etc.)
- Use for critical resources discovered late in the HTML (fonts referenced in CSS, images in CSS backgrounds)
- **Warning:** Preloading too many resources dilutes the benefit -- limit to truly critical resources (LCP image, critical fonts)

### `prefetch`

Fetches a resource at low priority for a likely future navigation:

```html
<link rel="prefetch" href="/next-page.html">
<link rel="prefetch" href="/next-page-data.json">
```

- Downloaded at lowest priority during idle time
- Stored in the HTTP cache for future use
- Use for resources needed on the next likely page (next step in a flow, frequently visited page)
- Does not work if the user has Data Saver enabled

### `prerender` / Speculation Rules

Modern browsers support the Speculation Rules API for prerendering entire pages:

```html
<script type="speculationrules">
{
  "prerender": [
    { "urls": ["/likely-next-page"] }
  ]
}
</script>
```

- Renders the entire page in a hidden tab
- Near-instant navigation when the user clicks
- Expensive in terms of memory and bandwidth -- use only for high-confidence predictions

## Font Loading Strategies

Web fonts create unique performance challenges because the browser may hide text while fonts load (Flash of Invisible Text, or FOIT) or show a jarring swap (Flash of Unstyled Text, or FOUT).

### `font-display` values

```css
@font-face {
  font-family: 'Custom Font';
  src: url('font.woff2') format('woff2');
  font-display: swap;  /* Show fallback immediately, swap when ready */
}
```

| Value | Behavior | Best for |
|-------|----------|----------|
| `auto` | Browser default (usually FOIT for 3s) | Not recommended |
| `block` | Invisible text for up to 3s, then swap | Icon fonts only |
| `swap` | Show fallback immediately, swap when loaded | Body text, most use cases |
| `fallback` | Brief invisible period (100ms), then fallback, then swap | Balanced approach |
| `optional` | Brief invisible period, uses font only if cached | Performance-critical; accepts FOUT |

### Preloading fonts

Fonts referenced in CSS are discovered late -- the browser must load HTML, then CSS, then discover the font URL. Preloading jumps the queue:

```html
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
```

The `crossorigin` attribute is required even for same-origin fonts because the font specification requires CORS.

### Font subsetting

Subset fonts to include only the characters needed:
- Latin-only sites can drop CJK, Cyrillic, and other ranges
- Use `unicode-range` in `@font-face` to load character ranges on demand

```css
@font-face {
  font-family: 'Custom Font';
  src: url('font-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF;  /* Basic Latin */
}
```

## Image Optimization

Images typically account for 50-70% of total page weight.

### Lazy loading

```html
<!-- Browser-native lazy loading -->
<img src="photo.jpg" loading="lazy" alt="Description">

<!-- Do NOT lazy-load above-fold images (LCP candidates) -->
<img src="hero.jpg" loading="eager" fetchpriority="high" alt="Hero">
```

### Responsive images

Serve appropriately sized images for each viewport:

```html
<img
  srcset="photo-400.webp 400w,
          photo-800.webp 800w,
          photo-1200.webp 1200w"
  sizes="(max-width: 600px) 400px,
         (max-width: 1000px) 800px,
         1200px"
  src="photo-800.webp"
  alt="Description"
>
```

### Modern formats

| Format | Compression | Browser support | Best for |
|--------|-------------|-----------------|----------|
| **AVIF** | Best (50% smaller than JPEG) | Chrome, Firefox, Safari 16+ | Photos, complex images |
| **WebP** | Good (25-35% smaller than JPEG) | All modern browsers | General purpose |
| **JPEG** | Baseline | Universal | Fallback |
| **PNG** | Lossless | Universal | Transparency, screenshots |
| **SVG** | Vector (tiny for icons) | Universal | Icons, logos, illustrations |

Use the `<picture>` element for format negotiation:

```html
<picture>
  <source srcset="photo.avif" type="image/avif">
  <source srcset="photo.webp" type="image/webp">
  <img src="photo.jpg" alt="Description">
</picture>
```

### Explicit dimensions

Always set width and height (or use CSS `aspect-ratio`) to prevent layout shift:

```html
<img src="photo.jpg" width="800" height="600" alt="Description">
```

```css
img {
  aspect-ratio: 4 / 3;
  width: 100%;
  height: auto;
}
```

## Resource Loading Priority

Modern browsers assign priorities based on resource type and position. The `fetchpriority` attribute gives developers explicit control:

```html
<!-- High priority for LCP image -->
<img src="hero.webp" fetchpriority="high" alt="Hero">

<!-- Low priority for below-fold image -->
<img src="footer-bg.webp" fetchpriority="low" loading="lazy" alt="">

<!-- High priority for critical script -->
<script src="critical.js" fetchpriority="high"></script>
```

### Default browser priorities

| Resource | Default priority |
|----------|-----------------|
| HTML document | Highest |
| CSS in `<head>` | Highest |
| Preloaded resources | High |
| Scripts in `<head>` | High |
| Images in viewport | High |
| Scripts at end of body | Medium |
| Images out of viewport | Low |
| Prefetched resources | Lowest |

## Practical Loading Strategy

A complete resource loading strategy for a typical page:

```html
<head>
  <!-- 1. DNS prefetch for third-party origins -->
  <link rel="dns-prefetch" href="https://analytics.example.com">

  <!-- 2. Preconnect to critical origins -->
  <link rel="preconnect" href="https://cdn.example.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- 3. Preload critical resources discovered late -->
  <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/hero.avif" as="image">

  <!-- 4. Inline critical CSS -->
  <style>/* above-fold styles */</style>

  <!-- 5. Async load full stylesheet -->
  <link rel="preload" href="/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">

  <!-- 6. Deferred application scripts -->
  <script src="/app.js" defer></script>

  <!-- 7. Async independent scripts -->
  <script src="/analytics.js" async></script>
</head>
<body>
  <!-- 8. LCP element with high priority -->
  <img src="/hero.avif" fetchpriority="high" alt="Hero" width="1200" height="600">

  <!-- 9. Below-fold images lazy loaded -->
  <img src="/feature.webp" loading="lazy" alt="Feature" width="800" height="400">

  <!-- 10. Prefetch next page for likely navigation -->
  <link rel="prefetch" href="/next-page.html">
</body>
```

This ordering ensures critical resources load first, nothing blocks rendering unnecessarily, and resources for future navigations are prepared during idle time.
