---
name: high-perf-browser
description: 'Optimize web performance through network protocols, resource loading, and browser rendering internals. Use when the user mentions "my site is slow", "Core Web Vitals", "HTTP/2 or HTTP/3", "resource hints", "network latency", "render blocking", "TCP/TLS optimization", "service worker", "Cache-Control or caching strategy", or "critical rendering path". Also trigger when diagnosing slow page loads, optimizing time to first byte, choosing between WebSocket and SSE, or reducing bundle sizes. For UI visual performance, see refactoring-ui. For font loading, see web-typography.'
license: MIT
metadata:
  author: wondelai
  version: "1.4.1"
---

# High Performance Browser Networking Framework

A systematic approach to web performance grounded in how browsers, protocols, and networks actually work. Apply these principles when building frontend applications, setting performance budgets, configuring servers, or diagnosing slow page loads.

## Core Principle

**Latency, not bandwidth, is the bottleneck.** Most web performance problems stem from too many round trips, not too little throughput. A 5x bandwidth increase yields diminishing returns; a 5x latency reduction transforms the user experience.

**The foundation:** Every request passes through DNS resolution, TCP handshake, TLS negotiation, and HTTP exchange before a single byte of content arrives — each step adding round-trip latency. High-performance applications minimize round trips, parallelize requests, and eliminate unnecessary network hops. Understanding the protocol stack is the prerequisite for meaningful optimization.

## Scoring

**Goal: 10/10.** Score by how many of the eight Quick Diagnostic rows pass, weighted toward the field metrics: **9-10** = all eight pass (the four field-metric rows in the green plus content-hashing, HTTP/2+, minimized render-blocking, and compression); **5-6** = the four field-metric rows pass but one or more transport/caching/compression rows fail; **<=3** = any field-metric row is in the red. Always report the score, which diagnostic rows failed, and the specific fix for each.

## The High Performance Browser Networking Framework

Six domains for building fast, resilient web applications:

### 1. Network Fundamentals

**Core concept:** Every HTTP request pays a latency tax — DNS lookup, TCP three-way handshake, TLS negotiation — before any application data flows. Reducing or eliminating these round trips is the single highest-leverage optimization.

**Why it works:** Light travels at a finite speed: a New York–London packet takes ~28ms one way regardless of bandwidth. These physics-level constraints cannot be solved with bigger pipes — only with fewer trips.

**Key insights:**
- TCP three-way handshake adds one full RTT before data transfer begins
- TCP slow start limits initial throughput to ~14KB (10 segments) in the first round trip — keep critical resources under this threshold
- Upgrade to TLS 1.3: it halves the handshake round trips of TLS 1.2 and enables 0-RTT resumption for returning visitors
- Head-of-line blocking in TCP means one lost packet stalls all streams on that connection
- Bandwidth-delay product caps in-flight data; high-latency links underutilize bandwidth

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Connection warmup** | Pre-establish connections to critical origins | `<link rel="preconnect" href="https://cdn.example.com">` |
| **DNS prefetch** | Resolve third-party domains early (saves 20-120ms) | `<link rel="dns-prefetch" href="https://analytics.example.com">` |
| **TLS optimization** | TLS 1.3 + session resumption | `ssl_protocols TLSv1.3;` with session tickets |
| **Connection reuse** | Keep-alive avoids repeated handshakes | `Connection: keep-alive` (default in HTTP/1.1+) |

See [references/network-fundamentals.md](references/network-fundamentals.md) when tuning servers or diagnosing handshake latency — the full TLS 1.2-vs-1.3 RTT derivation, slow-start doubling table, initcwnd/BDP math, OCSP-stapling Nginx config, and the DNS cache hierarchy.

### 2. HTTP Protocol Evolution

**Core concept:** HTTP evolved from a simple request-response protocol into a multiplexed, binary system. Choosing the right protocol version and configuring it properly eliminates entire categories of performance problems.

**Why it works:** HTTP/1.1 forces workarounds (domain sharding, sprites, concatenation) because it cannot multiplex. HTTP/2 multiplexes but inherits TCP head-of-line blocking; HTTP/3 (QUIC over UDP) eliminates it. Each generation removes a bottleneck — and makes the previous generation's workarounds counterproductive.

**Key insights:**
- HTTP/1.1 allows one outstanding request per TCP connection; browsers open 6 per host as a workaround
- HTTP/2 multiplexes unlimited streams over one connection — domain sharding becomes counterproductive
- HPACK header compression in HTTP/2 cuts repetitive header overhead by 85-95%
- HTTP/3 (QUIC) eliminates TCP head-of-line blocking and enables 0-RTT resumption and connection migration
- Prefer `103 Early Hints` over HTTP/2 Server Push (which over-pushes and is widely deprecated)
- Connection coalescing lets one HTTP/2 connection serve multiple hostnames sharing a certificate

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **HTTP/2 migration** | Remove HTTP/1.1 workarounds | Undo domain sharding, sprites, file concatenation |
| **103 Early Hints** | Send preload hints before the full response | `103` with `Link: </style.css>; rel=preload` |
| **QUIC/HTTP/3** | Advertise HTTP/3 on CDN or origin | `Alt-Svc: h3=":443"` header |
| **Stream prioritization** | Signal resource importance | CSS and fonts highest priority; images lower |

See [references/http-protocols.md](references/http-protocols.md) when picking or migrating a protocol version — side-by-side HTTP/1.1-vs-2-vs-3 comparison, the step-by-step de-sharding migration, and why Server Push lost to 103 Early Hints.

### 3. Resource Loading and Critical Rendering Path

**Core concept:** The browser must build the DOM, CSSOM, and render tree before painting pixels: HTML → DOM → CSSOM → Render Tree → Layout → Paint → Composite. Any resource that blocks this pipeline delays first paint.

**Why it works:** CSS is render-blocking (no paint until CSSOM is ready) while JavaScript is parser-blocking (`<script>` halts DOM construction until it downloads and executes) — so each needs a different optimization strategy. Every blocking resource adds latency directly to time-to-first-paint.

**Key insights:**
- `async` downloads in parallel and executes immediately (use for independent scripts); `defer` downloads in parallel but executes after DOM parsing (use for most scripts)
- `<link rel="preload">` fetches critical resources at high priority now; `rel="prefetch"` fetches likely next-navigation resources at low priority
- Inline above-the-fold CSS and async-load the rest to eliminate the render-blocking CSS request
- Fonts can block text rendering for up to 3s — use `font-display: swap`

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Critical CSS** | Inline above-the-fold styles in `<head>` | `<style>/* critical */</style>` + async full CSS |
| **Script loading** | `defer` by default; `async` for independents | `<script src="app.js" defer></script>` |
| **Resource hints** | Preload critical fonts, hero images | `<link rel="preload" href="font.woff2" as="font" crossorigin>` |
| **Image optimization** | Lazy-load below-fold; modern formats | `<img loading="lazy" src="photo.avif" srcset="...">` |

See [references/resource-loading.md](references/resource-loading.md) when shaving first paint — the exact async/defer/module execution order, the full resource-hint decision tree, and the image/font (`font-display`, `srcset`, AVIF) playbook.

### 4. Caching Strategies

**Core concept:** The fastest network request is one that never happens. Layer caches — browser memory, disk, service worker, CDN, origin — to eliminate round trips for repeat visitors.

**Why it works:** Cache-Control headers tell the browser and intermediaries exactly how long a response stays valid; content-hashed URLs make aggressive immutable caching safe. Each cache hit eliminates a full network round trip.

**Key insights:**
- `Cache-Control: no-cache` still caches but revalidates every time; `no-store` never caches — don't confuse them
- `ETag` / `Last-Modified` enable conditional requests (`304 Not Modified`) that skip the body transfer
- Service workers provide a programmable cache layer that works offline (cache-first shell, network-first dynamic content)
- Misconfigured `Vary` headers cause CDN cache pollution — serve the wrong encoding or format to the wrong client

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Static assets** | Immutable cache + hash busting | `style.a1b2c3.css` with `Cache-Control: max-age=31536000, immutable` |
| **HTML documents** | Revalidate on every request | `Cache-Control: no-cache` with `ETag` |
| **API responses** | Short TTL + background refresh | `Cache-Control: max-age=60, stale-while-revalidate=3600` |
| **CDN config** | Cache at edge with correct Vary | `Vary: Accept-Encoding, Accept` |

See [references/caching-strategies.md](references/caching-strategies.md) when designing a cache policy — the full browser/SW/CDN/origin hierarchy, copy-paste service-worker cache-first vs network-first recipes, and the `Vary` pitfalls that pollute a CDN.

### 5. Core Web Vitals Optimization

**Core concept:** Core Web Vitals — LCP, INP, CLS — are Google's user-centric metrics covering loading, interactivity, and visual stability. They impact search ranking and reflect real user experience.

**Why it works:** A fast TTFB means nothing if the hero image still loads late (LCP) or main-thread JavaScript blocks interactions (INP) — so server-side timing can look green while users wait. Optimize the perceived milestones, not the byte-delivery clock.

**Key insights** (numeric pass/fail thresholds live in the Quick Diagnostic):
- LCP — optimize the largest visible element (hero image, heading block, video poster)
- INP — keep the main thread free; break long tasks so every interaction (not only the first) stays responsive
- CLS — reserve space for dynamic content before it loads
- TTFB and FCP (< 1.8s) are upstream gates: they bound every downstream milestone, so fix them first
- Measure with Real User Monitoring (RUM) in production — lab/synthetic tests miss real-device and network variance

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **LCP** | Preload LCP element; raise its priority | `<img src="hero.webp" fetchpriority="high">` |
| **INP** | Break long tasks; yield to main thread | `scheduler.yield()` or `setTimeout` chunking |
| **CLS** | Reserve space for async content | `<img width="800" height="600">` or CSS `aspect-ratio` |
| **Performance budget** | Fail CI when a vital regresses past its Quick Diagnostic threshold | Lighthouse CI assertions on LCP/INP/CLS |

See [references/core-web-vitals.md](references/core-web-vitals.md) when a metric is in the red — per-metric debugging workflows (what to inspect for a bad LCP/INP/CLS), the lab-vs-RUM tooling map, and per-vital optimization checklists.

### 6. Real-Time Communication

**Core concept:** When data must flow continuously, the transport choice — WebSocket, SSE, or long polling — determines latency, resource usage, and scalability.

**Why it works:** HTTP's request-response model adds overhead to every real-time update. WebSocket offers full-duplex with ~2-byte framing; SSE offers simpler server-to-client push over plain HTTP. Match the transport to the data flow direction and frequency instead of defaulting to the most powerful option.

**Key insights:**
- WebSocket: bidirectional (chat, gaming, collaborative editing); SSE: server-to-client only, auto-reconnects, proxy-friendly, simpler
- Long polling is a fallback only — high overhead from repeated HTTP requests
- Each WebSocket is a separate TCP connection that bypasses HTTP/2 multiplexing
- Send heartbeat/ping frames — mobile networks silently drop idle connections
- Reconnect with exponential backoff and queue messages while disconnected

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Chat / collaboration** | WebSocket + heartbeat + reconnection | `new WebSocket('wss://...')` with ping every 30s |
| **Live feeds / notifications** | SSE for server-to-client streaming | `new EventSource('/api/updates')` |
| **Connection resilience** | Exponential backoff on reconnect | 1s, 2s, 4s, 8s... capped at 30s |
| **Scaling** | Pub/sub broker behind WebSocket servers | Redis Pub/Sub or NATS |

See [references/real-time-communication.md](references/real-time-communication.md) when building a live feature — the WebSocket connect/heartbeat/reconnect lifecycle, the SSE `EventSource` pattern, and how to scale fan-out behind a pub/sub broker.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Adding bandwidth to fix slow pages | Latency is the bottleneck, not throughput | Reduce round trips: preconnect, cache, CDN |
| Loading all JS upfront | Parser-blocking scripts delay paint and interactivity | Code-split; `defer`; lazy-load non-critical modules |
| No resource hints | Browser discovers critical resources too late | `preconnect` + `preload` for above-fold criticals |
| Missing Cache-Control / `no-store` everywhere | Every visit re-downloads everything | Proper `max-age` + content hashing |
| Ignoring CLS | Layout shifts destroy trust and ranking | Explicit dimensions on images, embeds, ads |
| WebSocket for everything | Needless complexity when SSE/polling suffices | Match transport to data flow; SSE for server push |
| Domain sharding on HTTP/2 | Defeats multiplexing; extra TCP connections | Consolidate origins; let HTTP/2 multiplex |
| No compression | Text resources transfer at full size | Enable Brotli (preferred) or Gzip on server/CDN |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Is TTFB under 800ms? | Server or network too slow | CDN, server caching, check backend |
| Is LCP under 2.5s? | Largest element loads too late | Preload LCP resource; `fetchpriority="high"` |
| Is INP under 200ms? | Main thread blocked | Break long tasks; defer non-critical JS |
| Is CLS under 0.1? | Elements shift after render | Explicit dimensions; reserve space |
| Are static assets content-hashed and cached? | Repeat visitors re-download | Hashed filenames + `Cache-Control: immutable` |
| Is HTTP/2 or HTTP/3 enabled? | No multiplexing or header compression | Enable HTTP/2 on server; HTTP/3 via CDN |
| Are render-blocking resources minimized? | CSS and sync JS delay first paint | Inline critical CSS; `defer` scripts; prune unused CSS |
| Is compression enabled (Brotli/Gzip)? | Uncompressed text transfers | Enable Brotli on server/CDN; Gzip fallback |

## Further Reading

Based on Ilya Grigorik's comprehensive guide to browser networking and web performance:

- [*"High Performance Browser Networking"*](https://www.amazon.com/High-Performance-Browser-Networking-performance/dp/1449344763?tag=wondelai00-20) by Ilya Grigorik (the complete reference for networking protocols, browser internals, and performance optimization)
- [hpbn.co](https://hpbn.co/) -- Free online edition maintained by the author

## About the Author

**Ilya Grigorik** is a web performance engineer who spent over a decade at Google working on Chrome, web platform performance, and HTTP standards, and co-chaired the W3C Web Performance Working Group. His book *High Performance Browser Networking* (O'Reilly, 2013) is widely regarded as the definitive reference on how browsers interact with the network.
