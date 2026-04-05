---
name: high-perf-browser
description: 'Optimize web performance through network protocols, resource loading, and browser rendering internals. Use when the user mentions "page load speed", "Core Web Vitals", "HTTP/2", "resource hints", "network latency", "render blocking", "TCP optimization", "service worker", or "critical rendering path". Also trigger when diagnosing slow page loads, optimizing time to first byte, choosing between WebSocket and SSE, or reducing bundle sizes. Covers TCP/TLS optimization, caching strategies, WebSocket/SSE, and protocol selection. For UI visual performance, see refactoring-ui. For font loading, see web-typography.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# High Performance Browser Networking Framework

A systematic approach to web performance optimization grounded in how browsers, protocols, and networks actually work. Apply these principles when building frontend applications, reviewing performance budgets, configuring servers, or diagnosing slow page loads.

## Core Principle

**Latency, not bandwidth, is the bottleneck.** Most web performance problems stem from too many round trips, not too little throughput. A 5x bandwidth increase yields diminishing returns; a 5x latency reduction transforms the user experience.

**The foundation:** Every network request passes through DNS resolution, TCP handshake, TLS negotiation, and HTTP exchange before a single byte of content arrives. Each step adds round-trip latency. High-performance applications minimize round trips, parallelize requests, and eliminate unnecessary network hops. Understanding the protocol stack is not optional -- it is the prerequisite for meaningful optimization.

## Scoring

**Goal: 10/10.** When reviewing or building web applications, rate performance 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## The High Performance Browser Networking Framework

Six domains for building fast, resilient web applications:

### 1. Network Fundamentals

**Core concept:** Every HTTP request pays a latency tax: DNS lookup, TCP three-way handshake, and TLS negotiation -- all before any application data flows. Reducing or eliminating these round trips is the single highest-leverage optimization.

**Why it works:** Light travels at a finite speed. A packet from New York to London takes ~28ms one way regardless of bandwidth. TCP slow start means new connections begin transmitting slowly. TLS adds 1-2 more round trips. These physics-level constraints cannot be solved with bigger pipes -- only with fewer trips.

**Key insights:**
- TCP three-way handshake adds one full RTT before data transfer begins
- TCP slow start limits initial throughput to ~14KB (10 segments) in the first round trip -- keep critical resources under this threshold
- TLS 1.2 adds 2 RTTs; TLS 1.3 reduces this to 1 RTT (0-RTT with session resumption)
- Head-of-line blocking in TCP means one lost packet stalls all streams on that connection
- Bandwidth-delay product determines in-flight data capacity; high-latency links underutilize bandwidth
- DNS resolution can add 20-120ms; pre-resolve with `dns-prefetch`

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Connection warmup** | Pre-establish connections to critical origins | `<link rel="preconnect" href="https://cdn.example.com">` |
| **DNS prefetch** | Resolve third-party domains early | `<link rel="dns-prefetch" href="https://analytics.example.com">` |
| **TLS optimization** | Enable TLS 1.3 and session resumption | Server config: `ssl_protocols TLSv1.3;` with session tickets |
| **Initial payload** | Keep critical HTML under 14KB compressed | Inline critical CSS, defer non-essential scripts |
| **Connection reuse** | Keep-alive connections to avoid repeated handshakes | `Connection: keep-alive` (default in HTTP/1.1+) |

See: [references/network-fundamentals.md](references/network-fundamentals.md) for TCP congestion control, bandwidth-delay product, and TLS handshake details.

### 2. HTTP Protocol Evolution

**Core concept:** HTTP has evolved from a simple request-response protocol to a multiplexed, binary, server-push-capable system. Choosing the right protocol version and configuring it properly eliminates entire categories of performance problems.

**Why it works:** HTTP/1.1 forces browsers into workarounds like domain sharding and sprite sheets because it cannot multiplex requests. HTTP/2 solves multiplexing but inherits TCP head-of-line blocking. HTTP/3 (QUIC) moves to UDP, eliminating head-of-line blocking and enabling connection migration. Each generation removes a bottleneck.

**Key insights:**
- HTTP/1.1 allows only one outstanding request per TCP connection; browsers open 6 connections per host as a workaround
- HTTP/2 multiplexes unlimited streams over a single TCP connection, making domain sharding counterproductive
- HPACK header compression in HTTP/2 reduces repetitive header overhead by 85-95%
- HTTP/3 runs over QUIC (UDP), eliminating TCP head-of-line blocking and enabling 0-RTT connection resumption
- Server Push (HTTP/2) sends resources before the browser requests them -- use sparingly and prefer `103 Early Hints` instead
- Connection coalescing in HTTP/2 lets one connection serve multiple hostnames sharing a certificate

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **HTTP/2 migration** | Remove HTTP/1.1 workarounds | Undo domain sharding, remove sprite sheets, stop concatenating files |
| **Stream prioritization** | Signal resource importance to the server | CSS and fonts at highest priority; images at lower priority |
| **103 Early Hints** | Send preload hints before the full response | Server sends `103` with `Link: </style.css>; rel=preload` |
| **QUIC/HTTP/3** | Enable HTTP/3 on CDN or origin | Add `Alt-Svc: h3=":443"` header to advertise HTTP/3 support |
| **Header optimization** | Minimize custom headers to reduce overhead | Audit cookies and custom headers; remove unnecessary ones |

See: [references/http-protocols.md](references/http-protocols.md) for protocol comparison, migration strategies, and server push vs. Early Hints.

### 3. Resource Loading and Critical Rendering Path

**Core concept:** The browser must build the DOM, CSSOM, and render tree before painting pixels. Any resource that blocks this pipeline delays first paint. Optimizing the critical rendering path means identifying and eliminating these bottlenecks.

**Why it works:** CSS is render-blocking: the browser will not paint until all CSS is parsed. JavaScript is parser-blocking by default: `<script>` halts DOM construction until the script downloads and executes. Fonts can block text rendering for up to 3 seconds. Each blocking resource adds latency directly to time-to-first-paint.

**Key insights:**
- Critical rendering path: HTML bytes -> DOM -> CSSOM -> Render Tree -> Layout -> Paint -> Composite
- CSS blocks rendering; JavaScript blocks parsing -- these have different optimization strategies
- `async` downloads scripts in parallel and executes immediately; `defer` downloads in parallel but executes after DOM parsing
- `<link rel="preload">` fetches critical resources at high priority without blocking rendering
- `<link rel="prefetch">` fetches resources for likely next navigations at low priority
- Inline critical CSS (above-the-fold styles) and defer the rest to eliminate the render-blocking CSS request
- Fonts: use `font-display: swap` to avoid invisible text during font loading

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Critical CSS** | Inline above-the-fold styles in `<head>` | `<style>/* critical styles */</style>` + async load full CSS |
| **Script loading** | Use `defer` for most scripts; `async` for independent scripts | `<script src="app.js" defer></script>` |
| **Resource hints** | Preload critical fonts, hero images, above-fold assets | `<link rel="preload" href="font.woff2" as="font" crossorigin>` |
| **Image optimization** | Lazy-load below-fold images; use modern formats | `<img loading="lazy" src="photo.avif" srcset="...">` |
| **Font loading** | Prevent invisible text with font-display | `@font-face { font-display: swap; }` |

See: [references/resource-loading.md](references/resource-loading.md) for async/defer behavior, resource hint strategies, and image optimization.

### 4. Caching Strategies

**Core concept:** The fastest network request is one that never happens. A layered caching strategy -- browser memory, disk cache, service worker, CDN, and origin -- dramatically reduces load times for repeat visitors and subsequent navigations.

**Why it works:** Cache-Control headers tell the browser and intermediaries exactly how long a response remains valid. Content-hashed URLs enable aggressive immutable caching. Service workers provide a programmable cache layer that works offline. Each cache hit eliminates a full network round trip.

**Key insights:**
- `Cache-Control: max-age=31536000, immutable` for content-hashed static assets (JS, CSS, images)
- `Cache-Control: no-cache` still caches but revalidates every time -- use for HTML documents
- `ETag` and `Last-Modified` enable conditional requests (`304 Not Modified`) that save bandwidth
- `stale-while-revalidate` serves cached content immediately while fetching a fresh copy in the background
- Service workers intercept fetch requests and can serve from cache, fall back to network, or implement custom strategies
- CDN caching moves content closer to users, reducing RTT; configure `Vary` headers correctly to avoid cache pollution

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Static assets** | Long-lived immutable cache with hash busting | `style.a1b2c3.css` with `Cache-Control: max-age=31536000, immutable` |
| **HTML documents** | Revalidate on every request | `Cache-Control: no-cache` with `ETag` for conditional requests |
| **API responses** | Short TTL with stale-while-revalidate | `Cache-Control: max-age=60, stale-while-revalidate=3600` |
| **Offline support** | Service worker cache-first strategy | Cache static shell; network-first for dynamic content |
| **CDN config** | Cache at edge with proper Vary headers | `Vary: Accept-Encoding, Accept` to prevent serving wrong format |

See: [references/caching-strategies.md](references/caching-strategies.md) for cache hierarchy, service worker patterns, and CDN configuration.

### 5. Core Web Vitals Optimization

**Core concept:** Core Web Vitals -- LCP, INP, and CLS -- are Google's user-centric performance metrics that directly impact search ranking and user experience. Each metric targets a different phase: loading (LCP), interactivity (INP), and visual stability (CLS).

**Why it works:** These metrics measure what users actually experience, not what servers report. A page can have a fast TTFB but terrible LCP if the hero image loads late. A page can load quickly but feel sluggish if main-thread JavaScript blocks input handling (poor INP). Optimizing for these metrics means optimizing for real user perception.

**Key insights:**
- LCP (Largest Contentful Paint): target < 2.5s -- optimize the largest visible element (hero image, heading block, or video poster)
- INP (Interaction to Next Paint): target < 200ms -- keep main thread free; break long tasks; use `requestIdleCallback` for non-urgent work
- CLS (Cumulative Layout Shift): target < 0.1 -- reserve space for dynamic content; set explicit dimensions on images and embeds
- TTFB (Time to First Byte): target < 800ms -- optimize server response time, use CDN, enable compression
- FCP (First Contentful Paint): target < 1.8s -- eliminate render-blocking resources, inline critical CSS
- Measure with Real User Monitoring (RUM) in production, not just synthetic tests in lab conditions

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **LCP optimization** | Preload LCP element; set `fetchpriority="high"` | `<img src="hero.webp" fetchpriority="high">` |
| **INP optimization** | Break long tasks; yield to main thread | `scheduler.yield()` or `setTimeout` to chunk work |
| **CLS prevention** | Reserve space for async content | `<img width="800" height="600">` or CSS `aspect-ratio` |
| **TTFB reduction** | CDN, server-side caching, streaming SSR | Edge rendering with `Transfer-Encoding: chunked` |
| **Performance budget** | Set thresholds and block deploys that exceed them | LCP < 2.5s, INP < 200ms, CLS < 0.1 in CI pipeline |

See: [references/core-web-vitals.md](references/core-web-vitals.md) for measurement tools, debugging workflows, and optimization checklists.

### 6. Real-Time Communication

**Core concept:** When data must flow continuously between client and server, choosing the right transport -- WebSocket, SSE, or long polling -- determines latency, resource usage, and scalability.

**Why it works:** HTTP's request-response model creates overhead for real-time data. WebSocket establishes a persistent full-duplex connection with minimal framing overhead (~2 bytes per frame). Server-Sent Events (SSE) provide a simpler server-to-client push over standard HTTP. The right choice depends on whether communication is unidirectional or bidirectional, how frequently data flows, and infrastructure constraints.

**Key insights:**
- WebSocket: full-duplex, minimal framing overhead, ideal for chat, gaming, and collaborative editing
- SSE: server-to-client only, auto-reconnects, works through HTTP proxies, simpler to implement than WebSocket
- Long polling: fallback when WebSocket/SSE are unavailable; high overhead from repeated HTTP requests
- WebSocket connections bypass HTTP/2 multiplexing -- each WebSocket is a separate TCP connection
- Implement heartbeat/ping frames to detect dead connections; mobile networks silently drop idle connections
- Connection management: exponential backoff on reconnection; queue messages during disconnection

**Code applications:**

| Context | Pattern | Example |
|---------|---------|---------|
| **Chat / collaboration** | WebSocket with heartbeat and reconnection | `new WebSocket('wss://...')` with ping every 30s |
| **Live feeds / notifications** | SSE for server-to-client streaming | `new EventSource('/api/updates')` with auto-reconnect |
| **Legacy fallback** | Long polling when WebSocket is blocked | `fetch('/poll')` in a loop with timeout |
| **Connection resilience** | Exponential backoff on reconnection | Delay: 1s, 2s, 4s, 8s... capped at 30s |
| **Scaling** | Use a pub/sub broker behind WebSocket servers | Redis Pub/Sub or NATS for horizontal scaling |

See: [references/real-time-communication.md](references/real-time-communication.md) for WebSocket lifecycle, SSE patterns, and scaling strategies.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Adding bandwidth to fix slow pages | Latency, not bandwidth, is the bottleneck for most web traffic | Reduce round trips: preconnect, cache, CDN |
| Loading all JS upfront | Parser-blocking scripts delay first paint and interactivity | Code-split; use `defer`; lazy-load non-critical modules |
| No resource hints | Browser discovers critical resources too late in the parse | Add `preconnect`, `preload` for above-fold critical resources |
| Cache-Control missing or `no-store` everywhere | Every visit re-downloads all resources from origin | Set proper `max-age` for static assets; use content hashing |
| Ignoring CLS | Layout shifts destroy user trust and hurt search ranking | Set explicit dimensions on all images, embeds, and ads |
| Using WebSocket for everything | Unnecessary complexity when SSE or HTTP polling suffices | Match transport to data flow pattern; SSE for server push |
| Domain sharding on HTTP/2 | Defeats multiplexing; creates extra TCP connections | Consolidate to one origin; let HTTP/2 multiplex |
| No compression | HTML, CSS, JS transfer at full size, wasting bandwidth | Enable Brotli (preferred) or Gzip on server and CDN |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Is TTFB under 800ms? | Server or network too slow | Add CDN, enable server caching, check backend |
| Is LCP under 2.5s? | Largest element loads too late | Preload LCP resource; set `fetchpriority="high"` |
| Is INP under 200ms? | Main thread blocked during interactions | Break long tasks; defer non-critical JS |
| Is CLS under 0.1? | Elements shift after initial render | Set explicit dimensions; reserve space for dynamic content |
| Are static assets cached with content hashes? | Repeat visitors re-download everything | Add hash to filenames; set `Cache-Control: immutable` |
| Is HTTP/2 or HTTP/3 enabled? | Missing multiplexing and header compression | Enable HTTP/2 on server; add HTTP/3 via CDN |
| Are render-blocking resources minimized? | CSS and sync JS delay first paint | Inline critical CSS; `defer` scripts; remove unused CSS |
| Is compression enabled (Brotli/Gzip)? | Transferring uncompressed text resources | Enable Brotli on server/CDN; fall back to Gzip |

## Reference Files

- [network-fundamentals.md](references/network-fundamentals.md): TCP handshake, congestion control, TLS optimization, DNS resolution, head-of-line blocking
- [http-protocols.md](references/http-protocols.md): HTTP/1.1 workarounds, HTTP/2 multiplexing, HTTP/3 and QUIC, migration strategies
- [resource-loading.md](references/resource-loading.md): Critical rendering path, async/defer, resource hints, image and font optimization
- [caching-strategies.md](references/caching-strategies.md): Cache-Control headers, service workers, CDN configuration, cache invalidation
- [core-web-vitals.md](references/core-web-vitals.md): LCP, INP, CLS optimization, measurement tools, performance budgets
- [real-time-communication.md](references/real-time-communication.md): WebSocket, SSE, long polling, connection management, scaling

## Further Reading

This skill is based on Ilya Grigorik's comprehensive guide to browser networking and web performance:

- [*"High Performance Browser Networking"*](https://www.amazon.com/High-Performance-Browser-Networking-performance/dp/1449344763?tag=wondelai00-20) by Ilya Grigorik (the complete reference for networking protocols, browser internals, and performance optimization)
- [hpbn.co](https://hpbn.co/) -- Free online edition maintained by the author

## About the Author

**Ilya Grigorik** is a web performance engineer, author, and developer advocate who spent over a decade at Google working on Chrome, web platform performance, and HTTP standards. He was a co-chair of the W3C Web Performance Working Group and contributed to the development of HTTP/2 and related web standards. His book *High Performance Browser Networking* (O'Reilly, 2013) is widely regarded as the definitive reference for understanding how browsers interact with the network -- from TCP and TLS fundamentals through HTTP protocol evolution to real-time communication patterns. Grigorik's approach emphasizes that meaningful optimization requires understanding the underlying protocols, not just applying surface-level tricks, and that latency is the fundamental constraint shaping web performance.
