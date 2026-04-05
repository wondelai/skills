# Core Web Vitals Optimization

Core Web Vitals are Google's standardized performance metrics that measure real user experience. They directly impact search ranking and correlate strongly with user engagement, conversion rates, and bounce rates.


## Table of Contents
1. [The Three Core Web Vitals](#the-three-core-web-vitals)
2. [LCP: Largest Contentful Paint](#lcp-largest-contentful-paint)
3. [INP: Interaction to Next Paint](#inp-interaction-to-next-paint)
4. [CLS: Cumulative Layout Shift](#cls-cumulative-layout-shift)
5. [Measuring Core Web Vitals](#measuring-core-web-vitals)
6. [Performance Budgets](#performance-budgets)
7. [Debugging Workflow](#debugging-workflow)
8. [Quick Reference: Optimization Impact](#quick-reference-optimization-impact)

---

## The Three Core Web Vitals

| Metric | Measures | Good | Needs Improvement | Poor |
|--------|----------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | Loading performance | < 2.5s | 2.5s - 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | Interactivity | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | Visual stability | < 0.1 | 0.1 - 0.25 | > 0.25 |

### Supporting metrics

| Metric | Measures | Target |
|--------|----------|--------|
| **TTFB** (Time to First Byte) | Server responsiveness | < 800ms |
| **FCP** (First Contentful Paint) | Initial render speed | < 1.8s |
| **TBT** (Total Blocking Time) | Main thread availability (lab proxy for INP) | < 200ms |

## LCP: Largest Contentful Paint

LCP measures when the largest visible content element finishes rendering. This is what users perceive as "the page has loaded."

### What counts as the LCP element

- `<img>` elements (including those inside `<picture>`)
- `<video>` poster images
- Elements with `background-image` via CSS
- Block-level text elements (`<h1>`, `<p>`, etc.)

The LCP element changes as the page loads. The final LCP element is the one that is largest when rendering stabilizes.

### Common LCP problems

**Slow server response (high TTFB):** The browser cannot render anything until it receives the first byte of HTML.

Fixes:
- Add a CDN to reduce network latency
- Implement server-side caching (Redis, Varnish)
- Use streaming server-side rendering to send the HTML `<head>` immediately
- Optimize database queries and backend processing
- Use `103 Early Hints` to let the browser start fetching critical resources before the full response

**Late-discovered LCP resource:** The browser discovers the LCP image late in the rendering process (e.g., a CSS background image or a `<img>` tag deep in the HTML).

Fixes:
```html
<!-- Preload the LCP image -->
<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">

<!-- Or use fetchpriority directly -->
<img src="/hero.webp" fetchpriority="high" alt="Hero" width="1200" height="600">
```

**Render-blocking resources:** CSS and synchronous JavaScript delay rendering.

Fixes:
- Inline critical CSS in `<head>`
- Defer non-critical CSS loading
- Use `defer` or `async` on scripts
- Remove unused CSS (audit with Coverage panel)

**Slow resource load time:** The LCP image itself is too large or served from a slow origin.

Fixes:
- Compress images (AVIF, WebP)
- Serve responsive images with `srcset`
- Use a CDN for image delivery
- Set appropriate cache headers

**Client-side rendering:** SPAs that render content in JavaScript after the initial HTML load have inherently slow LCP.

Fixes:
- Use server-side rendering (SSR) or static site generation (SSG)
- Stream HTML with `Transfer-Encoding: chunked`
- Pre-render the above-fold content on the server

### LCP optimization checklist

- [ ] TTFB under 800ms
- [ ] LCP resource discoverable in HTML source (not CSS or JS)
- [ ] LCP resource preloaded with `fetchpriority="high"`
- [ ] No render-blocking resources before LCP
- [ ] LCP image optimized (format, compression, responsive)
- [ ] LCP image served from CDN
- [ ] Critical CSS inlined; non-critical CSS deferred

## INP: Interaction to Next Paint

INP measures the delay between a user interaction (click, tap, keypress) and the next visual update. It replaced FID (First Input Delay) as a Core Web Vital in March 2024.

**Why INP matters more than FID:** FID only measured the delay of the first interaction. INP measures all interactions throughout the page lifecycle and reports the worst (at the 98th percentile). A page can have a good FID but terrible INP if JavaScript blocks the main thread during later interactions.

### What causes poor INP

**Long tasks on the main thread:** Any JavaScript task that runs for more than 50ms blocks the browser from processing user input.

**Excessive event handler work:** Click handlers that perform heavy computation, DOM manipulation, or synchronous operations delay the visual response.

**Layout thrashing:** Reading layout properties (like `offsetHeight`) and then writing to the DOM in a loop forces the browser to recalculate layout repeatedly.

### INP optimization strategies

**Break up long tasks:**

```javascript
// BAD: One long task blocking the main thread
function processAllItems(items) {
  items.forEach(item => heavyOperation(item));
}

// GOOD: Yield to the main thread between chunks
async function processAllItems(items) {
  for (const item of items) {
    heavyOperation(item);
    // Yield to let the browser handle pending interactions
    await scheduler.yield();
  }
}
```

If `scheduler.yield()` is not available, use a polyfill pattern:

```javascript
function yieldToMain() {
  return new Promise(resolve => setTimeout(resolve, 0));
}

async function processAllItems(items) {
  for (let i = 0; i < items.length; i++) {
    heavyOperation(items[i]);
    if (i % 10 === 0) await yieldToMain();
  }
}
```

**Defer non-urgent work:**

```javascript
// Use requestIdleCallback for work that does not need to happen immediately
requestIdleCallback(() => {
  analytics.track('page_view');
  prefetchNextPage();
});
```

**Minimize event handler work:**

```javascript
// BAD: Heavy computation in click handler
button.addEventListener('click', () => {
  const result = expensiveCalculation();  // 200ms
  updateDOM(result);                       // 50ms
});

// GOOD: Show immediate feedback, defer heavy work
button.addEventListener('click', () => {
  showLoadingState();                      // 5ms - immediate feedback
  requestAnimationFrame(() => {
    const result = expensiveCalculation();
    updateDOM(result);
    hideLoadingState();
  });
});
```

**Avoid layout thrashing:**

```javascript
// BAD: Read-write-read-write forces repeated layout
elements.forEach(el => {
  const height = el.offsetHeight;        // Read (forces layout)
  el.style.height = height * 2 + 'px';  // Write (invalidates layout)
});

// GOOD: Batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight);  // All reads
elements.forEach((el, i) => {
  el.style.height = heights[i] * 2 + 'px';            // All writes
});
```

**Reduce JavaScript payload:**
- Code-split: load only what the current page needs
- Tree-shake: remove unused exports
- Lazy-load non-critical modules
- Defer third-party scripts (analytics, widgets)

### INP optimization checklist

- [ ] No JavaScript tasks longer than 50ms on the main thread
- [ ] Event handlers provide immediate visual feedback
- [ ] Non-urgent work deferred with `requestIdleCallback` or `scheduler.yield()`
- [ ] No layout thrashing (batched reads and writes)
- [ ] JavaScript code-split and lazy-loaded
- [ ] Third-party scripts loaded async or deferred

## CLS: Cumulative Layout Shift

CLS measures how much visible content shifts unexpectedly during the page lifecycle. Layout shifts destroy user trust -- users click the wrong button, lose their reading position, or experience visual chaos.

### What causes layout shifts

**Images without dimensions:** When an image loads, it pushes surrounding content down if no space was reserved.

**Dynamic content injection:** Ads, banners, cookie notices, and lazy-loaded content that inserts above existing content.

**Web fonts causing text reflow:** When a web font loads and replaces a fallback font with different metrics, text reflows and shifts surrounding elements.

**Dynamic content resizing:** Accordions, tab panels, or carousels that change height.

### CLS prevention strategies

**Always set image dimensions:**

```html
<!-- Explicit dimensions reserve space -->
<img src="photo.jpg" width="800" height="600" alt="Photo">

<!-- CSS aspect-ratio works too -->
<style>
  .hero-img { aspect-ratio: 16 / 9; width: 100%; }
</style>
```

**Reserve space for dynamic content:**

```css
/* Reserve space for an ad slot */
.ad-slot {
  min-height: 250px;
  background: #f0f0f0;
}

/* Reserve space for a cookie banner */
.cookie-banner-placeholder {
  min-height: 80px;
}
```

**Use `font-display: optional` for strict CLS prevention:**

```css
@font-face {
  font-family: 'Custom Font';
  src: url('font.woff2') format('woff2');
  font-display: optional;  /* Uses font only if already cached */
}
```

Alternatively, use `font-display: swap` with font metric overrides to match fallback metrics:

```css
@font-face {
  font-family: 'Custom Font';
  src: url('font.woff2') format('woff2');
  font-display: swap;
  size-adjust: 105%;
  ascent-override: 95%;
  descent-override: 22%;
  line-gap-override: 0%;
}
```

**Insert dynamic content below the viewport or with explicit reservations:**

```javascript
// BAD: Inserting a banner at the top pushes everything down
document.body.prepend(bannerElement);

// GOOD: Use CSS transforms that don't trigger layout
// Or insert in a reserved slot with min-height already set
document.querySelector('.banner-slot').appendChild(bannerElement);
```

**Use CSS `contain` for independent layout regions:**

```css
.widget {
  contain: layout;  /* Layout changes inside don't affect outside */
}
```

### CLS optimization checklist

- [ ] All images and videos have explicit width and height attributes
- [ ] Ad slots and dynamic content areas have reserved minimum heights
- [ ] Web fonts use `font-display: swap` or `optional` with metric overrides
- [ ] No content inserted above existing visible content
- [ ] CSS animations use `transform` and `opacity` only (composited properties)
- [ ] Embeds (iframes, widgets) have explicit dimensions

## Measuring Core Web Vitals

### Lab tools (synthetic testing)

| Tool | Metrics | Use case |
|------|---------|----------|
| **Lighthouse** (Chrome DevTools) | LCP, TBT, CLS | Development, auditing |
| **WebPageTest** | All vitals + filmstrip | Detailed analysis |
| **PageSpeed Insights** | Lab + field data | Quick overview |

### Field tools (real user monitoring)

| Tool | Data source | Use case |
|------|------------|----------|
| **Chrome User Experience Report (CrUX)** | Chrome users | Public dataset, search ranking data |
| **Google Search Console** | CrUX data per URL/group | SEO impact monitoring |
| **web-vitals library** | Your users | Custom RUM implementation |

### Implementing RUM with the web-vitals library

```javascript
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,  // 'good', 'needs-improvement', 'poor'
    id: metric.id,
    navigationType: metric.navigationType,
  });
  // Use sendBeacon for reliable delivery
  navigator.sendBeacon('/analytics', body);
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

### Lab vs. field data

| Aspect | Lab (synthetic) | Field (RUM) |
|--------|----------------|-------------|
| **Environment** | Controlled (specific device, network) | Real user conditions |
| **INP measurement** | Uses TBT as proxy | True INP from real interactions |
| **CLS measurement** | Page load only | Full page lifecycle |
| **Reproducibility** | High | Low (varies by user) |
| **Use for** | Debugging, development | Monitoring, search ranking |

**Always prioritize field data** for understanding real performance. Lab data is useful for debugging but does not capture the diversity of real-world conditions.

## Performance Budgets

Performance budgets set thresholds that prevent regressions:

```javascript
// Example budget in a CI/CD pipeline
const budgets = {
  lcp: 2500,      // ms
  inp: 200,       // ms (use TBT in lab)
  cls: 0.1,       // score
  ttfb: 800,      // ms
  totalJS: 300,   // KB (compressed)
  totalCSS: 50,   // KB (compressed)
  totalImages: 500, // KB
  totalFonts: 200,  // KB
};
```

### Enforcing budgets

**Lighthouse CI:** Run Lighthouse in CI and fail builds that exceed budgets:

```json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["error", { "maxNumericValue": 200 }]
      }
    }
  }
}
```

**Bundle size monitoring:** Tools like `bundlesize`, `size-limit`, or Webpack's `performance.maxAssetSize` can catch JavaScript bloat before it ships.

## Debugging Workflow

When Core Web Vitals are poor, follow this systematic approach:

### 1. Identify the problem metric
Check CrUX data in Search Console or PageSpeed Insights.

### 2. Reproduce in lab
Use Lighthouse or WebPageTest with throttled conditions matching your users.

### 3. Diagnose root cause

**For poor LCP:**
- Check TTFB (server issue?)
- Check resource waterfall (late-discovered LCP resource?)
- Check render-blocking resources (too much blocking CSS/JS?)
- Check resource size (unoptimized images?)

**For poor INP:**
- Record a Performance trace in DevTools
- Identify long tasks (red flags in the flame chart)
- Find the interaction that triggered the long task
- Determine which script/function caused the blocking

**For poor CLS:**
- Use the Layout Shift Regions overlay in DevTools (Rendering panel)
- Check for images without dimensions
- Look for late-injected content (ads, banners)
- Test font loading behavior

### 4. Fix and verify
Implement the fix, measure in lab, deploy, and verify with field data (allow 28 days for CrUX data to reflect changes).

## Quick Reference: Optimization Impact

| Optimization | LCP | INP | CLS | Effort |
|-------------|-----|-----|-----|--------|
| Add CDN | High | -- | -- | Low |
| Preload LCP resource | High | -- | -- | Low |
| Inline critical CSS | High | -- | -- | Medium |
| Code-split JavaScript | Medium | High | -- | Medium |
| Set image dimensions | -- | -- | High | Low |
| Use `font-display: swap` | -- | -- | Medium | Low |
| Defer third-party scripts | Medium | High | Medium | Low |
| Implement streaming SSR | High | Medium | -- | High |
| Break up long tasks | -- | High | -- | Medium |
| Reserve ad slot space | -- | -- | High | Low |

Optimizing Core Web Vitals is not a one-time task -- it requires continuous monitoring and a performance-aware development culture that treats metrics regressions as bugs.
