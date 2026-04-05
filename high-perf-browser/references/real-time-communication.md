# Real-Time Communication

When data must flow continuously between client and server, the standard HTTP request-response model introduces unnecessary overhead. Real-time communication protocols -- WebSocket, Server-Sent Events (SSE), and WebRTC -- each solve different use cases with different trade-offs.


## Table of Contents
1. [Choosing the Right Approach](#choosing-the-right-approach)
2. [WebSocket Protocol](#websocket-protocol)
3. [Server-Sent Events (SSE)](#server-sent-events-sse)
4. [Long Polling](#long-polling)
5. [WebRTC Basics](#webrtc-basics)
6. [Connection Management Best Practices](#connection-management-best-practices)
7. [Scaling Real-Time Systems](#scaling-real-time-systems)

---

## Choosing the Right Approach

| Requirement | Best transport | Why |
|------------|---------------|-----|
| Bidirectional, low-latency messaging | WebSocket | Full-duplex, minimal per-message overhead |
| Server-to-client push (unidirectional) | SSE | Simpler API, auto-reconnect, works over HTTP |
| Periodic data updates | HTTP polling or `stale-while-revalidate` | Simplest; no persistent connection needed |
| Peer-to-peer audio/video/data | WebRTC | Direct peer connection, media-optimized |
| Fallback for restricted networks | Long polling | Works everywhere HTTP works |

**Default to the simplest option that meets requirements.** SSE handles many "real-time" use cases without WebSocket's complexity. HTTP polling with `stale-while-revalidate` is sufficient when updates happen every few seconds or minutes.

## WebSocket Protocol

WebSocket provides a persistent, full-duplex communication channel over a single TCP connection. After an HTTP upgrade handshake, client and server exchange frames with minimal overhead (~2-6 bytes per frame).

### Connection lifecycle

```
1. Client sends HTTP upgrade request
2. Server responds with 101 Switching Protocols
3. Connection upgraded to WebSocket (persistent, full-duplex)
4. Client and server exchange frames freely
5. Either side sends a close frame to terminate
```

### Opening handshake

The WebSocket connection begins as an HTTP request:

```
GET /ws HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

Server response:
```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

After this handshake, the connection is no longer HTTP -- it is a raw TCP connection with WebSocket framing.

### Client implementation

```javascript
class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.reconnectDelay = 1000;
    this.maxReconnectDelay = 30000;
    this.messageQueue = [];
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('Connected');
      this.reconnectDelay = 1000;  // Reset backoff
      this.flushQueue();
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };

    this.ws.onclose = (event) => {
      if (!event.wasClean) {
        this.scheduleReconnect();
      }
    };

    this.ws.onerror = () => {
      // onerror is always followed by onclose
    };
  }

  send(data) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      this.messageQueue.push(data);
    }
  }

  flushQueue() {
    while (this.messageQueue.length > 0) {
      this.send(this.messageQueue.shift());
    }
  }

  scheduleReconnect() {
    setTimeout(() => this.connect(), this.reconnectDelay);
    this.reconnectDelay = Math.min(
      this.reconnectDelay * 2,
      this.maxReconnectDelay
    );
  }

  handleMessage(data) {
    // Application-specific message handling
  }
}
```

### Frame types

| Frame type | Opcode | Purpose |
|-----------|--------|---------|
| Text | 0x1 | UTF-8 text data |
| Binary | 0x2 | Binary data (images, protobuf, etc.) |
| Ping | 0x9 | Heartbeat request |
| Pong | 0xA | Heartbeat response |
| Close | 0x8 | Connection termination |

### Heartbeats and connection monitoring

Mobile networks and load balancers silently drop idle connections. Heartbeats detect dead connections:

```javascript
// Client-side heartbeat
class HeartbeatWebSocket extends WebSocketClient {
  constructor(url, heartbeatInterval = 30000) {
    super(url);
    this.heartbeatInterval = heartbeatInterval;
    this.heartbeatTimer = null;
    this.pongReceived = true;
  }

  connect() {
    super.connect();

    this.ws.onopen = () => {
      this.startHeartbeat();
    };
  }

  startHeartbeat() {
    this.heartbeatTimer = setInterval(() => {
      if (!this.pongReceived) {
        // Server did not respond to last ping
        this.ws.close();
        return;
      }
      this.pongReceived = false;
      this.ws.send(JSON.stringify({ type: 'ping' }));
    }, this.heartbeatInterval);
  }

  handleMessage(data) {
    if (data.type === 'pong') {
      this.pongReceived = true;
      return;
    }
    // Handle other messages
  }
}
```

**Server-side heartbeat timing:**
- 30 seconds is a common interval for most use cases
- Mobile apps may use longer intervals (60-90s) to save battery
- Trading and gaming may use shorter intervals (5-10s) for faster dead connection detection

### WebSocket and HTTP/2

An important caveat: **WebSocket connections bypass HTTP/2 multiplexing.** Each WebSocket connection is a separate TCP connection, not a stream on an existing HTTP/2 connection. For applications that open many WebSocket connections to the same origin, this can create connection overhead.

RFC 8441 defines WebSocket over HTTP/2, but browser support is limited.

### Binary vs. text frames

For high-throughput applications, binary frames with a compact serialization format (Protocol Buffers, MessagePack, CBOR) significantly reduce message size:

```javascript
// Text (JSON) - 84 bytes
ws.send(JSON.stringify({ type: 'position', x: 123.456, y: 789.012, t: 1679000000 }));

// Binary (Protocol Buffers) - ~20 bytes
const buffer = Position.encode({ x: 123.456, y: 789.012, t: 1679000000 }).finish();
ws.send(buffer);
```

## Server-Sent Events (SSE)

SSE provides a simple, HTTP-based protocol for server-to-client push. The server holds an HTTP connection open and streams events to the client.

### Key advantages over WebSocket

- **Simpler:** Works over standard HTTP; no upgrade handshake
- **Auto-reconnect:** The `EventSource` API reconnects automatically with configurable retry delay
- **Event IDs:** Built-in support for resuming from the last received event
- **Works through HTTP proxies:** Standard HTTP, so no proxy configuration needed
- **HTTP/2 compatible:** SSE connections are HTTP/2 streams (multiplexed with other requests)

### When SSE is sufficient

SSE handles the majority of "real-time" web use cases:
- Live notifications
- Real-time dashboards and monitoring
- Stock tickers and live scores
- Chat (with a separate HTTP POST for sending messages)
- Streaming AI responses (like ChatGPT)
- Build/deployment status updates

### Server implementation

The server sends a response with `Content-Type: text/event-stream`:

```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

data: {"message": "Hello"}

event: notification
data: {"type": "alert", "text": "New message"}

id: 42
event: update
data: {"price": 142.50}

retry: 5000

```

Event format:
- `data:` -- the event payload (can span multiple lines)
- `event:` -- event type (defaults to "message")
- `id:` -- event ID (sent as `Last-Event-ID` on reconnect)
- `retry:` -- reconnection delay in milliseconds

### Client implementation

```javascript
const eventSource = new EventSource('/api/stream');

// Default "message" events
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Message:', data);
};

// Named events
eventSource.addEventListener('notification', (event) => {
  const data = JSON.parse(event.data);
  showNotification(data);
});

// Connection management
eventSource.onerror = (event) => {
  if (eventSource.readyState === EventSource.CLOSED) {
    console.log('Connection closed by server');
  } else {
    console.log('Connection error, will auto-reconnect');
  }
};

// Close when done
eventSource.close();
```

### Resuming after disconnection

When the connection drops, the browser sends the last received event ID:

```
GET /api/stream HTTP/1.1
Last-Event-ID: 42
```

The server can use this to resume from where the client left off, preventing data loss during brief disconnections.

### SSE with authentication

`EventSource` does not support custom headers. Workarounds:

```javascript
// Option 1: Token in URL (less secure, logged in server access logs)
const eventSource = new EventSource('/api/stream?token=abc123');

// Option 2: Cookie-based authentication (preferred)
// Set an HttpOnly cookie first; EventSource sends cookies automatically

// Option 3: Use fetch() with ReadableStream for custom headers
async function streamWithHeaders(url, headers) {
  const response = await fetch(url, { headers });
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const text = decoder.decode(value);
    // Parse SSE format manually
    processSSEText(text);
  }
}
```

## Long Polling

Long polling is the fallback when WebSocket and SSE are unavailable (restrictive firewalls, legacy infrastructure).

### How it works

1. Client sends an HTTP request
2. Server holds the request open until it has new data (or a timeout occurs)
3. Server sends the response
4. Client immediately sends a new request
5. Repeat

```javascript
async function longPoll(url, lastEventId = null) {
  while (true) {
    try {
      const params = lastEventId ? `?since=${lastEventId}` : '';
      const response = await fetch(`${url}${params}`, {
        signal: AbortSignal.timeout(60000),  // 60s timeout
      });

      if (response.ok) {
        const data = await response.json();
        lastEventId = data.id;
        handleUpdate(data);
      }
    } catch (error) {
      if (error.name === 'TimeoutError') {
        // Normal timeout, reconnect immediately
        continue;
      }
      // Network error, back off
      await new Promise(r => setTimeout(r, 5000));
    }
  }
}
```

### Long polling trade-offs

| Aspect | Long polling | WebSocket | SSE |
|--------|-------------|-----------|-----|
| Latency | Higher (new request each time) | Lowest | Low |
| Server resources | High (many open connections) | Medium | Medium |
| Complexity | Low | Medium | Low |
| Firewall compatibility | Highest | Lower | High |
| Bidirectional | Yes (via separate requests) | Yes (native) | No (one-way) |

## WebRTC Basics

WebRTC enables peer-to-peer communication for audio, video, and arbitrary data between browsers without a relay server.

### Architecture

```
Browser A ←→ Signaling Server ←→ Browser B
     ↕                                ↕
     └────── Direct P2P Connection ──┘
```

1. **Signaling:** Peers exchange session descriptions (SDP) and ICE candidates through a signaling server (WebSocket, HTTP, or any mechanism)
2. **ICE:** Interactive Connectivity Establishment discovers the best network path (direct, STUN, or TURN relay)
3. **DTLS/SRTP:** Encrypted media and data channels over UDP

### Data channels

For non-media real-time data (gaming, file transfer, screen sharing metadata), WebRTC data channels provide:
- Ordered or unordered delivery
- Reliable or unreliable (lossy) transport
- Low latency (UDP-based)
- Direct peer-to-peer (no server relay for media)

```javascript
const peerConnection = new RTCPeerConnection({
  iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
});

const dataChannel = peerConnection.createDataChannel('game', {
  ordered: false,        // Unordered for lower latency
  maxRetransmits: 0,     // Unreliable (no retransmission)
});

dataChannel.onopen = () => {
  dataChannel.send(JSON.stringify({ type: 'move', x: 10, y: 20 }));
};
```

### When to use WebRTC

- Video/audio calls
- Screen sharing
- Peer-to-peer file transfer
- Low-latency gaming (data channels)
- IoT device streaming

**Do not use WebRTC for:** Standard server-to-client push (use SSE or WebSocket), REST API alternatives, or scenarios where a server relay is needed anyway.

## Connection Management Best Practices

### Exponential backoff with jitter

When reconnecting after a failure, exponential backoff prevents thundering herd problems:

```javascript
function getReconnectDelay(attempt, baseDelay = 1000, maxDelay = 30000) {
  const exponentialDelay = baseDelay * Math.pow(2, attempt);
  const cappedDelay = Math.min(exponentialDelay, maxDelay);
  // Add random jitter (0-100% of delay) to prevent synchronized reconnects
  const jitter = cappedDelay * Math.random();
  return cappedDelay + jitter;
}
```

Without jitter, if a server restarts and 10,000 clients all reconnect simultaneously with the same backoff timing, the server faces a thundering herd of reconnection attempts.

### Message queuing during disconnection

Queue outbound messages when disconnected and flush when reconnected:

```javascript
class ResilientConnection {
  constructor() {
    this.queue = [];
    this.connected = false;
  }

  send(message) {
    if (this.connected) {
      this.transport.send(message);
    } else {
      this.queue.push(message);
      if (this.queue.length > 1000) {
        this.queue.shift();  // Prevent unbounded growth
      }
    }
  }

  onReconnect() {
    this.connected = true;
    while (this.queue.length > 0) {
      this.transport.send(this.queue.shift());
    }
  }
}
```

### Connection lifecycle on mobile

Mobile connections face unique challenges:
- **Network switches:** WiFi to cellular transitions drop TCP connections
- **Background tabs:** Browsers throttle or suspend timers and connections in background tabs
- **Battery optimization:** OS may terminate background network activity

Strategies:
- Detect visibility changes with `document.visibilitychange` and reconnect when returning to foreground
- Use shorter heartbeat intervals on mobile to detect dead connections faster
- Implement message ID tracking so the server can resume from the last acknowledged message

```javascript
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    // Tab became visible -- check connection health
    if (!isConnectionAlive()) {
      reconnect();
    }
  }
});
```

## Scaling Real-Time Systems

### Horizontal scaling with pub/sub

WebSocket connections are stateful -- a client connects to a specific server instance. To scale horizontally, use a pub/sub broker:

```
Client A → Server 1 ←→ Redis Pub/Sub ←→ Server 2 → Client B
Client C → Server 1 ←→     or NATS     ←→ Server 3 → Client D
```

When Client A sends a message, Server 1 publishes it to Redis. All servers subscribed to that channel receive it and forward to their connected clients.

### Connection limits

Each WebSocket connection consumes:
- A file descriptor on the server
- Memory for the connection state
- CPU for message processing

Practical limits:
- A single Node.js process can handle ~50,000-100,000 concurrent WebSocket connections (depending on message rate)
- Use connection limits and load balancing to distribute connections
- Consider connection pooling for services that broadcast to many clients

### Load balancing considerations

- **Sticky sessions:** Required for WebSocket and long polling (the same client must reach the same server)
- **Connection draining:** When scaling down, drain connections gracefully before terminating a server instance
- **Health checks:** Exclude servers with too many connections or high latency from the load balancer pool

The choice of real-time transport should be driven by requirements, not technology preferences. SSE handles most server-push use cases with far less complexity than WebSocket. WebSocket is essential for bidirectional, low-latency communication. WebRTC is specialized for peer-to-peer media. Long polling is the universal fallback.
