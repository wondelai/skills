# Microinteraction Case Studies

Detailed design breakdowns of common UI patterns, analyzed through the four-part microinteraction structure: Trigger, Rules, Feedback, and Loops & Modes. Each case study documents the interaction from first use through edge cases, providing a practical blueprint for implementation.

## Table of Contents
1. [Case Study 1: Form Submission](#case-study-1-form-submission)
2. [Case Study 2: Toggle / Switch](#case-study-2-toggle-switch)
3. [Case Study 3: Pull-to-Refresh](#case-study-3-pull-to-refresh)
4. [Case Study 4: Loading States](#case-study-4-loading-states)
5. [Case Study 5: Notifications (Toast / Snackbar)](#case-study-5-notifications-toast-snackbar)
6. [Cross-Cutting Patterns](#cross-cutting-patterns)

---

## Case Study 1: Form Submission

A form submission microinteraction covers the moment from when the user taps "Submit" to when they receive confirmation of success or details of failure. It is one of the highest-stakes microinteractions because users have invested time and data.

### The Four Parts

**Trigger:**
- Manual trigger: "Submit" button (primary action, full-width or prominent)
- Keyboard trigger: Enter key in last field (convention, not always expected)
- System trigger: Auto-save draft after 30 seconds of inactivity (background)

**Rules:**
1. On trigger, validate all required fields client-side before sending to server
2. If validation fails, prevent submission and highlight first invalid field
3. If validation passes, disable submit button and show loading state
4. Send data to server
5. On server success (200), show success feedback and redirect or reset form
6. On server error (4xx/5xx), show error message and preserve all input
7. On network timeout (>15 seconds), show retry option with preserved input

**Feedback:**

| State | Visual | Copy | Duration |
|-------|--------|------|----------|
| **Idle** | Blue "Submit" button, normal state | "Submit" or "Create Account" | Persistent |
| **Validating** | Button briefly disabled | "Checking..." | 0-500ms |
| **Validation error** | Red border on invalid fields, scroll to first error | "Please enter a valid email" inline | Until corrected |
| **Submitting** | Button shows spinner, text changes | "Submitting..." | Server response time |
| **Success** | Green checkmark replaces spinner | "Done! Redirecting..." | 1-2 seconds |
| **Server error** | Red banner at top, button re-enabled | "Something went wrong. Please try again." | Until dismissed |
| **Network error** | Yellow banner, retry button | "Connection lost. Your data is saved locally." | Until retry succeeds |

**Loops & Modes:**
- Auto-save loop: draft saved to local storage every 30 seconds (open loop)
- Long loop: after 3+ submissions, hide optional tooltips and field hints
- No modes (single-purpose interaction)

### Edge Cases

| Edge Case | Handling |
|-----------|---------|
| User double-clicks submit | Disable button on first click; debounce server request |
| User navigates away mid-submission | Show "Unsaved changes" dialog; save draft to local storage |
| Session expires during submission | Queue submission; re-authenticate and retry |
| Very long form (20+ fields) | Show progress indicator; validate sections independently |
| Paste of formatted text | Strip formatting; accept plain text only |
| Autofill conflict | Accept autofill values; re-validate on submit |

### Implementation Notes

| Platform | Key Detail |
|----------|-----------|
| **Web** | Use `<form>` native validation as baseline; enhance with JS. Preserve form data in `sessionStorage`. |
| **iOS** | Use `UITextFieldDelegate` for per-field validation. Keyboard "Return" key should move to next field, not submit. |
| **Android** | `TextInputLayout` with `setError()` for inline validation. Handle back button to save draft. |

---

## Case Study 2: Toggle / Switch

A toggle is a binary microinteraction: on or off. Despite its apparent simplicity, a well-designed toggle requires careful attention to state communication, animation timing, and accessibility.

### The Four Parts

**Trigger:**
- Manual trigger: tap/click anywhere on the toggle (track or thumb)
- Keyboard trigger: Space bar when toggle is focused
- Drag trigger: drag thumb from one position to the other
- System trigger: external state change (admin disables feature remotely)

**Rules:**
1. On trigger, immediately start transition animation
2. If action requires server confirmation, send request in background
3. Toggling on may trigger additional UI (reveal settings, enable features)
4. Toggling off may trigger confirmation dialog for destructive changes
5. If server rejects the change, revert toggle to previous state with error message
6. Rapid toggling (clicking multiple times fast) should debounce: only the final state is sent

**Feedback:**

| State | Thumb Position | Track Color | Label (if used) | Haptic |
|-------|---------------|-------------|-----------------|--------|
| **Off** | Left | Gray (#E5E7EB) | "Off" | None |
| **Transitioning on** | Sliding right | Transitioning to green | -- | None |
| **On** | Right | Green (#22C55E) | "On" | Light tap |
| **Transitioning off** | Sliding left | Transitioning to gray | -- | None |
| **Disabled** | Current position | Faded (40% opacity) | "Unavailable" | None |
| **Loading** | Current position | Faded with inline spinner | "Updating..." | None |
| **Error** | Reverted position | Flash red briefly, return to normal | "Failed to update" | Error pattern |

**Loops & Modes:**
- No traditional loop (single action)
- Long loop: if toggle controls a feature with settings, first 3 toggles might show a tooltip explaining the feature
- No modes

### Animation Specification

| Property | Value | Easing |
|----------|-------|--------|
| Thumb position (left to right) | 150-200ms | ease-in-out |
| Track color transition | 150-200ms | ease-in-out (synchronized with thumb) |
| Thumb shadow on drag | 100ms to enlarge shadow | ease-out |
| Revert on error | 200ms | ease-out with red flash |

### Accessibility

| Requirement | Implementation |
|-------------|---------------|
| **ARIA role** | `role="switch"` with `aria-checked="true/false"` |
| **Focus indicator** | 2px blue outline around entire toggle on Tab focus |
| **Keyboard** | Space bar toggles; no Enter (per switch role spec) |
| **Screen reader** | "Wi-Fi, switch, on" -- announces label, role, and state |
| **Reduced motion** | Skip animation; instant state change |
| **Touch target** | Minimum 44x44pt including padding around toggle |

### Edge Cases

| Edge Case | Handling |
|-----------|---------|
| Toggle + settings reveal | Settings panel slides open below toggle; accordion animation 200ms |
| Toggle with destructive off | Confirmation dialog: "Disabling will delete all data. Are you sure?" |
| Toggle server failure | Revert toggle; show inline error for 3 seconds |
| Rapid toggling | Debounce 500ms; only send final state to server |
| Toggle with dependent toggles | Child toggles disable when parent turns off |

---

## Case Study 3: Pull-to-Refresh

Pull-to-refresh is a gesture-triggered microinteraction invented by Loren Brichter for Tweetie (acquired by Twitter). It transforms a natural gesture (pulling down on a list) into a data refresh. It is one of the most widely adopted microinteraction patterns in mobile design.

### The Four Parts

**Trigger:**
- Manual trigger: pull down on a scrollable list past a threshold (~60pt)
- The trigger is invisible -- no button exists; the gesture is the trigger
- System fallback: auto-refresh on app foreground after X minutes (system trigger)

**Rules:**
1. User must be scrolled to the top of the list for pull to activate
2. Pulling down below threshold shows visual hint but does not trigger refresh
3. Pulling past threshold (typically 60-80pt) "locks" the refresh
4. Releasing after passing threshold triggers the refresh request
5. Releasing before threshold snaps back with no refresh
6. While refreshing, spinner remains visible at top; list is still scrollable
7. On data received, new content animates into list; spinner dismisses
8. On failure, spinner dismisses; error message appears briefly
9. Minimum spinner display: 500ms (prevents flash for fast connections)

**Feedback:**

| Pull Distance | Visual Feedback | Haptic Feedback |
|--------------|----------------|-----------------|
| **0-20pt** | Slight rubber-band stretch | None |
| **20-60pt** | Spinner icon appears, partially rotated proportional to pull | None |
| **60pt (threshold)** | Spinner completes rotation; visual snap indicating activation | Light tap (selection feedback) |
| **60pt+ (past threshold)** | Spinner remains complete; pull distance continues with resistance | None |
| **Release (past threshold)** | Spinner animates (spinning); list adjusts to accommodate | None |
| **Data received** | Spinner stops; new items slide in from top; spinner area collapses | None |
| **Error** | Spinner stops; brief error text ("Could not refresh"); area collapses | Error pattern |

**Loops & Modes:**
- Auto-refresh loop: if user has not pulled-to-refresh in 5+ minutes and returns to app, auto-refresh fires (system trigger)
- Long loop: for first 3 uses on a new device, show a subtle "Pull down to refresh" hint text
- Rate limiting rule: ignore pull-to-refresh if last refresh was < 5 seconds ago
- No modes

### Discoverability Strategy

Pull-to-refresh has zero visible affordance -- it relies entirely on platform convention. For apps where users might not know the gesture:

| Strategy | Implementation | When to Remove |
|----------|---------------|----------------|
| **Hint text** | "Pull down to refresh" text above list, visible at scroll top | After 3 successful pull-to-refresh actions |
| **Auto-refresh on first load** | Show the refresh animation automatically on first visit | After first visit only |
| **Visible refresh button** | Small refresh icon in header as fallback | Never (always keep as alternative) |

### Platform-Specific Implementations

| Platform | Key Detail |
|----------|-----------|
| **iOS** | `UIRefreshControl` -- native component. Spinner is an `ActivityIndicator`. Threshold is system-defined. |
| **Android** | `SwipeRefreshLayout` -- Material Design. Uses circular progress that fills as user pulls. |
| **Web** | Custom implementation required. Must handle touch events; prevent native browser pull-to-refresh interference. Use `overscroll-behavior: contain` on scroll container. |

---

## Case Study 4: Loading States

Loading is not a single microinteraction but a family of patterns for communicating "the system is working." The design challenge is keeping users informed and engaged during a period they cannot control.

### Loading Pattern Selection

| Scenario | Best Pattern | Why |
|----------|-------------|-----|
| **< 300ms** | No indicator (instant feel) | Any indicator would flash distractingly |
| **300ms - 1s** | Inline spinner | Acknowledges loading without drama |
| **1s - 5s** | Skeleton screen | Shows layout immediately; reduces perceived wait |
| **5s - 30s** | Determinate progress bar | Users need to see actual progress |
| **30s+** | Progress bar + background option | Users should be able to do other things |
| **Unknown duration** | Indeterminate spinner + status text | Transparency: "Processing..." then "Almost done..." |

### Skeleton Screen Design

**Trigger:** System trigger -- content request initiated.

**Rules:**
1. Show skeleton immediately on navigation (within 100ms)
2. Skeleton shapes must match the final layout precisely
3. Use subtle pulse animation on skeleton shapes (opacity 0.3 to 0.6, 1.5s loop)
4. Load content progressively: text first, then images
5. Crossfade from skeleton to real content (200ms)
6. Never show skeleton for content already in cache

**Skeleton Visual Specification:**

| Content Type | Skeleton Shape | Color | Animation |
|-------------|---------------|-------|-----------|
| **Text line** | Rounded rectangle, 60-80% width | Gray-200 (#E5E7EB) | Pulse 0.3-0.6 opacity |
| **Heading** | Rounded rectangle, 40-50% width, taller | Gray-200 | Pulse 0.3-0.6 opacity |
| **Avatar** | Circle, matching avatar size | Gray-200 | Pulse 0.3-0.6 opacity |
| **Image** | Rounded rectangle, matching aspect ratio | Gray-200 | Pulse 0.3-0.6 opacity |
| **Button** | Rounded rectangle, matching button size | Gray-200 | Pulse 0.3-0.6 opacity |

### Progress Bar Design

**Trigger:** System trigger -- long operation begins.

**Rules:**
1. Appear within 200ms of operation start
2. Progress must be real (based on actual progress, not fake animation)
3. Never go backward (if real progress reverses, pause at current point)
4. Final 5% should be server confirmation, not client processing
5. On completion, bar fills to 100%, brief pause, then success state

**Feedback:**

| Progress State | Visual | Text |
|---------------|--------|------|
| **0%** | Empty bar with subtle background | "Starting upload..." |
| **1-99%** | Bar fills proportionally; color stays blue | "Uploading... 47%" |
| **99%** | Bar nearly full; slight pause | "Finalizing..." |
| **100%** | Bar fills completely; transitions to green | "Complete!" |
| **Error at any point** | Bar turns red; stops at current position | "Upload failed at 47%. Retry?" |
| **Cancelled** | Bar fades out; reset | "Upload cancelled." |

### Loading State Accessibility

| Requirement | Implementation |
|-------------|---------------|
| Screen reader | `aria-live="polite"` region announces "Loading content" and "Content loaded" |
| Progress bar | `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax` |
| Reduced motion | Replace pulse animation with static gray; replace spinner with "Loading..." text |
| Timeout | If loading exceeds 30 seconds, announce "Still loading. You can continue waiting or try again." |

---

## Case Study 5: Notifications (Toast / Snackbar)

Notifications are transient microinteractions that communicate system events without requiring full user attention. They appear, convey a message, and disappear -- but the design details determine whether they are helpful or infuriating.

### The Four Parts

**Trigger:**
- System trigger: action completes (save, send, delete)
- System trigger: external event occurs (new message, status change)
- System trigger: error detected (network loss, permission denied)
- Manual trigger: user action with reversible outcome (delete triggers "Undo" toast)

**Rules:**
1. Appear in a consistent position (bottom-center for mobile, bottom-left or top-right for desktop)
2. Stack if multiple appear simultaneously (limit to 3 visible; queue additional)
3. Auto-dismiss after 5-8 seconds for informational; persist for errors until acknowledged
4. Slide in with animation (300ms); slide out on dismiss (200ms)
5. Must not cover critical UI elements (primary actions, navigation)
6. If toast contains an action ("Undo"), the action must be available for the entire display duration
7. Dismissable via swipe (mobile) or close button (desktop)

**Feedback:**

| Notification Type | Background Color | Icon | Auto-Dismiss | Action |
|------------------|-----------------|------|-------------|--------|
| **Success** | Green or dark gray | Checkmark | 5 seconds | None or "View" |
| **Info** | Blue or dark gray | Info circle | 5 seconds | Optional link |
| **Warning** | Yellow/amber | Warning triangle | 8 seconds | "Fix" or "Dismiss" |
| **Error** | Red | X circle | No (persist) | "Retry" and "Dismiss" |
| **Undo** | Dark gray | Undo arrow | 8 seconds | "Undo" (primary) |

**Loops & Modes:**
- Stacking loop: if user triggers 5 actions rapidly, queue toasts; show max 3 at once
- Long loop: if same notification appears 3+ times in a session, batch: "3 items saved"
- Consolidation: "3 files uploaded" instead of three separate "File uploaded" toasts
- No modes

### Toast Layout Specification

```
┌────────────────────────────────────────────────┐
│  [Icon]  Message text here          [Action] [X]│
│          Secondary text (optional)              │
└────────────────────────────────────────────────┘
```

| Element | Specification |
|---------|--------------|
| Width | Min 288px, max 568px (desktop); full-width minus margins (mobile) |
| Height | Min 48px, max 112px (2 lines + action) |
| Padding | 16px horizontal, 12px vertical |
| Border radius | 8px |
| Shadow | Medium elevation (shadow-md) |
| Position | Bottom-center (mobile), bottom-left or top-right (desktop), 16px from edge |
| Z-index | Above all content, below modals and dialogs |

### Animation Specification

| Transition | Duration | Easing | Direction |
|-----------|----------|--------|-----------|
| Enter | 300ms | ease-out (deceleration) | Slide up from below (mobile) or slide in from right (desktop) |
| Exit (auto-dismiss) | 200ms | ease-in (acceleration) | Slide down or fade out |
| Exit (swipe dismiss) | 150ms | ease-out | Follow swipe direction |
| Stack push | 200ms | ease-in-out | Existing toasts shift up to accommodate new one |

### Accessibility

| Requirement | Implementation |
|-------------|---------------|
| Screen reader | `role="status"` with `aria-live="polite"` (info/success); `role="alert"` with `aria-live="assertive"` (error) |
| Focus management | Do not steal focus from user's current position; action button reachable via Tab |
| Keyboard | Esc key dismisses; Tab reaches action buttons |
| Timeout | For error toasts, no auto-dismiss; for info toasts, pause timer on hover/focus |
| Reduced motion | Replace slide animation with fade (200ms) |

### Edge Cases

| Edge Case | Handling |
|-----------|---------|
| 10 toasts triggered at once | Queue: show 3; dismiss oldest first; show queued |
| Toast covers primary action | Reposition toast above the action; or provide alternative placement |
| User clicks Undo at last second | Accept undo if within the timeout window, even if fade-out started |
| Toast during full-screen mode | Overlay on top of full-screen content with higher z-index |
| Long text content | Truncate at 2 lines with "..." and "Show more" link |
| Network loss while showing "Undo" | Queue undo action locally; execute when connection returns |

---

## Cross-Cutting Patterns

### Patterns That Apply Across All Case Studies

| Pattern | Application | Example |
|---------|-------------|---------|
| **Debouncing** | Prevent rapid duplicate triggers | Double-click submit, rapid toggle, pull-to-refresh spam |
| **Optimistic UI** | Show result before server confirms | Toggle, like, delete with undo |
| **Progressive disclosure** | Show simple first, details on demand | Error summary first, full details expandable |
| **Graceful degradation** | Work without JavaScript, animation, or haptics | Form submits via native HTML; toggle works without animation |
| **Accessibility baseline** | All patterns must work for all users | ARIA roles, keyboard operation, reduced motion, screen reader |
| **State persistence** | Preserve user work across interruptions | Form drafts, scroll position, toggle state |
