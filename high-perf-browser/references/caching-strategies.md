# Caching Strategies

The fastest network request is one that never happens. A well-designed caching strategy eliminates redundant data transfer, reduces server load, and dramatically improves load times for repeat visitors and subsequent navigations.


## Table of Contents
1. [The Cache Hierarchy](#the-cache-hierarchy)
2. [HTTP Cache-Control Headers](#http-cache-control-headers)
3. [Conditional Requests and Revalidation](#conditional-requests-and-revalidation)
4. [Content Hashing for Cache Busting](#content-hashing-for-cache-busting)
5. [Service Workers for Cache Control](#service-workers-for-cache-control)
6. [CDN Configuration](#cdn-configuration)
7. [Stale-While-Revalidate](#stale-while-revalidate)
8. [Caching Strategy by Resource Type](#caching-strategy-by-resource-type)
9. [Common Caching Mistakes](#common-caching-mistakes)

---

## The Cache Hierarchy

Browsers check caches in a specific order before making a network request:

```
1. Memory cache (in-process, lost on tab close)
2. Service worker cache (programmable, persistent)
3. Disk cache (HTTP cache, persistent)
4. CDN / edge cache (network, shared across users)
5. Origin server (final fallback)
```

Each layer closer to the user is faster. Memory cache is near-instant. Disk cache avoids the network entirely. CDN cache reduces RTT by serving from a nearby edge location. The goal is to satisfy as many requests as possible from the closest cache layer.

## HTTP Cache-Control Headers

The `Cache-Control` header is the primary mechanism for controlling browser and CDN caching behavior.

### Essential directives

| Directive | Meaning | Use case |
|-----------|---------|----------|
| `max-age=N` | Cache for N seconds without revalidation | Static assets with known freshness |
| `no-cache` | Cache but always revalidate before use | HTML documents, API responses |
| `no-store` | Do not cache at all | Sensitive data (banking, health) |
| `immutable` | Never revalidate (even on reload) | Content-hashed static assets |
| `public` | Can be cached by shared caches (CDN) | Public content |
| `private` | Only browser can cache, not CDN | User-specific content |
| `stale-while-revalidate=N` | Serve stale for N seconds while fetching fresh | Near-real-time content |
| `stale-if-error=N` | Serve stale if origin returns an error | Fault tolerance |

### Common caching patterns

**Static assets with content hashing (optimal):**
```
Cache-Control: max-age=31536000, immutable
```
Files like `app.a1b2c3.js` can be cached forever because the URL changes when content changes. `immutable` tells the browser to skip revalidation even when the user hits refresh.

**HTML documents:**
```
Cache-Control: no-cache
```
The browser caches the document but revalidates on every request. Combined with `ETag`, this enables `304 Not Modified` responses that transfer only headers, not the full document.

**API responses with near-real-time needs:**
```
Cache-Control: max-age=0, stale-while-revalidate=60
```
Always revalidate, but if the origin is slow, serve the cached response and update in the background.

**Sensitive content:**
```
Cache-Control: no-store
```
Never cache. Use for authentication tokens, financial data, personal health information.

**Shared public content:**
```
Cache-Control: public, max-age=3600, stale-while-revalidate=86400
```
CDN can cache for 1 hour; serve stale for up to 24 hours while refreshing.

## Conditional Requests and Revalidation

When a cached resource expires (or uses `no-cache`), the browser sends a conditional request to check if the resource has changed.

### ETag (Entity Tag)

The server generates a unique identifier (hash) for the response content:

```
HTTP/1.1 200 OK
ETag: "abc123def456"
Cache-Control: no-cache
```

On revalidation, the browser sends:
```
GET /page.html HTTP/1.1
If-None-Match: "abc123def456"
```

If the content has not changed, the server responds:
```
HTTP/1.1 304 Not Modified
```

No body is transferred -- only headers. This saves bandwidth while ensuring freshness.

### Last-Modified

A simpler mechanism using timestamps:

```
HTTP/1.1 200 OK
Last-Modified: Wed, 21 Oct 2025 07:28:00 GMT
```

Revalidation:
```
GET /page.html HTTP/1.1
If-Modified-Since: Wed, 21 Oct 2025 07:28:00 GMT
```

**ETag vs. Last-Modified:** ETag is more precise (content-based), while Last-Modified has second-level granularity. Servers should support both; browsers prefer ETag when both are present.

## Content Hashing for Cache Busting

The most effective caching pattern combines long-lived cache headers with content-hashed filenames:

```
styles.css → styles.a1b2c3.css
app.js     → app.d4e5f6.js
logo.png   → logo.g7h8i9.png
```

**How it works:**
1. Build tools generate a hash of each file's contents
2. The hash is embedded in the filename
3. HTML references the hashed filename
4. The server sets `Cache-Control: max-age=31536000, immutable`
5. When the file changes, a new hash produces a new URL
6. The browser treats it as a completely new resource

**Implementation with common build tools:**

Webpack:
```javascript
output: {
  filename: '[name].[contenthash].js',
  chunkFilename: '[name].[contenthash].js',
}
```

Vite:
```javascript
build: {
  rollupOptions: {
    output: {
      entryFileNames: 'assets/[name].[hash].js',
      chunkFileNames: 'assets/[name].[hash].js',
      assetFileNames: 'assets/[name].[hash].[ext]',
    }
  }
}
```

**The HTML document itself cannot be hashed** (users navigate to `/index.html`, not `/index.a1b2c3.html`). This is why HTML uses `no-cache` while all referenced assets use content hashing.

## Service Workers for Cache Control

Service workers provide a programmable cache layer between the browser and the network. They intercept every fetch request and can implement sophisticated caching strategies.

### Cache-first (offline-first)

Serve from cache if available; fall back to network:

```javascript
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(cached => cached || fetch(event.request))
  );
});
```

**Best for:** Static assets (CSS, JS, images, fonts) that rarely change.

### Network-first

Try the network; fall back to cache if offline:

```javascript
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        const clone = response.clone();
        caches.open('dynamic').then(cache => cache.put(event.request, clone));
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
```

**Best for:** HTML documents and API responses where freshness matters.

### Stale-while-revalidate

Serve from cache immediately; update cache in the background:

```javascript
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      const fetchPromise = fetch(event.request).then(response => {
        const clone = response.clone();
        caches.open('dynamic').then(cache => cache.put(event.request, clone));
        return response;
      });
      return cached || fetchPromise;
    })
  );
});
```

**Best for:** Content that updates periodically but where instant display is preferred (news feeds, social timelines).

### Precaching the app shell

During service worker installation, cache the core application shell:

```javascript
const CACHE_NAME = 'app-shell-v1';
const SHELL_URLS = [
  '/',
  '/styles.css',
  '/app.js',
  '/offline.html',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(SHELL_URLS))
  );
});
```

### Cache versioning and cleanup

Old caches must be cleaned up to prevent storage bloat:

```javascript
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    )
  );
});
```

## CDN Configuration

CDNs cache content at edge locations close to users, reducing RTT for cached responses.

### CDN caching headers

The `Cache-Control` header controls both browser and CDN caching. Use `s-maxage` to set a different TTL for shared caches (CDNs) vs. browsers:

```
Cache-Control: public, max-age=60, s-maxage=3600
```

This tells browsers to cache for 60 seconds but CDNs to cache for 1 hour.

### Vary header

The `Vary` header tells caches which request headers affect the response:

```
Vary: Accept-Encoding
```

Without `Vary: Accept-Encoding`, a CDN might serve a Brotli-compressed response to a client that only supports Gzip.

Common `Vary` values:
- `Accept-Encoding` -- different compression (Brotli, Gzip, identity)
- `Accept` -- different content types (HTML vs. JSON, AVIF vs. WebP)
- `Accept-Language` -- different language versions

**Warning:** `Vary: *` or `Vary: Cookie` effectively disables CDN caching because every request differs.

### Cache purging

When content changes, CDN caches must be invalidated:

- **Purge by URL:** Invalidate a specific resource
- **Purge by tag:** Tag resources with categories; purge all resources with a tag
- **Purge by prefix:** Invalidate all resources under a path
- **Soft purge:** Mark as stale; serve stale while fetching fresh (similar to `stale-while-revalidate`)

Content-hashed URLs largely eliminate the need for cache purging of static assets. Focus purging on HTML and API responses.

## Stale-While-Revalidate

The `stale-while-revalidate` directive is one of the most powerful caching tools:

```
Cache-Control: max-age=60, stale-while-revalidate=3600
```

Behavior:
1. **0-60 seconds:** Serve from cache without revalidation (fresh)
2. **60-3660 seconds:** Serve from cache immediately (stale) AND fetch a fresh copy in the background
3. **After 3660 seconds:** Cache is completely stale; must wait for network

This pattern gives users instant responses while keeping content reasonably fresh. It is ideal for:
- API endpoints that update periodically
- Configuration data
- Product listings
- Any content where a few minutes of staleness is acceptable

## Caching Strategy by Resource Type

| Resource | Cache-Control | Hash | Revalidation |
|----------|--------------|------|-------------|
| HTML | `no-cache` | No | ETag + 304 |
| CSS (bundled) | `max-age=31536000, immutable` | Yes | None needed |
| JavaScript (bundled) | `max-age=31536000, immutable` | Yes | None needed |
| Images (static) | `max-age=31536000, immutable` | Yes | None needed |
| Fonts | `max-age=31536000, immutable` | Yes | None needed |
| API responses | `max-age=0, stale-while-revalidate=60` | No | ETag + 304 |
| User-specific data | `private, no-cache` | No | ETag + 304 |
| Sensitive data | `no-store` | No | N/A |

## Common Caching Mistakes

| Mistake | Consequence | Fix |
|---------|------------|-----|
| No `Cache-Control` on static assets | Browser uses heuristic caching (unpredictable) | Explicitly set `max-age` and `immutable` |
| `no-store` on everything | Every visit fetches all resources from origin | Use `no-cache` for HTML; long cache + hash for assets |
| Missing `Vary: Accept-Encoding` | CDN serves wrong compression format | Add `Vary: Accept-Encoding` to compressed responses |
| Cache busting with query strings | Some CDNs ignore query strings; proxies may not cache | Use filename hashing instead of `?v=123` |
| No ETag on HTML | Conditional requests impossible; full document re-downloaded | Configure server to generate ETags |
| `max-age=0` without `stale-while-revalidate` | Every request blocks on revalidation | Add `stale-while-revalidate` for better perceived performance |
| Service worker caching everything | Cache grows unbounded; stale content persists | Implement cache limits and versioned cleanup |

A comprehensive caching strategy is often the single highest-impact performance optimization -- it reduces server load, saves bandwidth, and makes repeat visits feel instant.
