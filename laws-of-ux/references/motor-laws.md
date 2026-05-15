# Motor Laws -- Fitts's Law & Doherty Threshold

Physical interaction and response time: how size, distance, and speed affect usability.

## Fitts's Law Deep Dive

### The Formula

```
MT = a + b × log₂(2D/W)
```

Where:
- **MT** = Movement Time
- **D** = Distance to target
- **W** = Width (size) of target
- **a, b** = Device-dependent constants

The practical implication: **doubling the target size** reduces movement time more than **halving the distance**.

### Touch Target Sizing Guide

| Element | Minimum size | Recommended | Notes |
|---------|-------------|-------------|-------|
| Primary button | 44x44px | 48x48px | Full-width on mobile for maximum Fitts advantage |
| Secondary button | 36x36px | 44x44px | Smaller acceptable if not primary action |
| Icon button | 44x44px | 48x48px | Tap target larger than visual icon (padding) |
| Navigation link | 44px height | 48px height | Full-width hit area, not just text |
| List item (tappable) | 44px height | 56-72px | Taller for comfortable repeated tapping |
| Checkbox / Radio | 44x44px | 44x44px | Tap target includes label, not just the box |
| Close button (X) | 44x44px | 44x44px | Never smaller, even if visually minimal |

### Thumb Zone (Mobile)

On mobile, the thumb has natural reach zones:

```
┌─────────────────────┐
│  Hard    Easy   Hard │  ← Top: hardest to reach
│                      │
│  Easy    Easy   Easy │  ← Middle: comfortable
│                      │
│  Easy    Easy   Easy │  ← Bottom: natural resting zone
└─────────────────────┘
```

**Rules:**
- Primary actions belong in the bottom third (natural thumb zone)
- Destructive actions in the top corners (harder to reach accidentally)
- Navigation tabs at the bottom for easy switching
- FABs (floating action buttons) in the bottom-right for right-handed users

### Edge and Corner Targets

Screen edges are "infinitely deep" -- the cursor can't overshoot them. This makes edge and corner targets extremely fast to acquire.

**Use this for:**
- Menu bars pinned to screen edges (macOS menu bar)
- Scroll bars at viewport edges
- Side panels / drawers anchored to viewport edges
- Desktop: corners are the fastest targets (infinite in two dimensions)

**Don't break this:**
- Never add padding/margin between a clickable element and the screen edge
- Sub-pixel gaps between the element and the edge negate the advantage

### Spacing Between Targets

Adjacent interactive elements need sufficient gap to prevent mis-taps:

| Context | Minimum gap | Recommended |
|---------|-------------|-------------|
| Buttons side-by-side | 8px | 16px |
| List items (tappable) | 4px | 8px |
| Icon buttons | 8px | 12px |
| Toolbar items | 4px | 8px |

---

## Doherty Threshold Deep Dive

### Response Time Categories

| Duration | User perception | Required feedback |
|----------|----------------|-------------------|
| 0-100ms | Instantaneous | None -- feels like direct manipulation |
| 100-400ms | Slight delay | Subtle: button state change, micro-animation |
| 400ms-1s | Noticeable wait | Spinner or skeleton screen |
| 1-2s | Definite wait | Spinner with context ("Loading messages...") |
| 2-5s | Uncomfortable | Progress bar (determinate if possible) |
| 5-10s | Frustrating | Progress bar + percentage + status messages |
| 10s+ | Unacceptable for foreground | Background processing + notification on completion |

### Optimistic UI Pattern

Show the result immediately. Sync in the background. Roll back only if the server rejects.

**When to use:**
- Actions with > 95% success rate (likes, follows, toggles, saves)
- Actions where the user expects instant feedback
- Non-destructive actions that can be retried

**When NOT to use:**
- Payment processing (must wait for confirmation)
- Destructive actions (deletion must confirm)
- Actions with complex validation (form submissions with server-side rules)

### Skeleton Screen Pattern

Replace loading spinners with grey placeholder blocks matching the content layout:

**Rules:**
1. Mirror the exact layout of the content being loaded
2. Use subtle shimmer/pulse animation to indicate activity
3. Replace with real content progressively (don't flash blank → skeleton → content)
4. Better than spinners for content-heavy pages (reduces perceived load time by 20-30%)

### Animation as Perceived Speed

Transitions and animations can mask loading time:

- 300-500ms ease-in-out transitions feel natural
- Staggered content appearance (items appearing 50ms apart) feels faster than all-at-once
- Skeleton → content morphing feels smoother than instant replacement
- Progress bars that start fast and slow near the end feel faster than linear progress
