# The 37signals Approach to UX, UI, and Copy

## Table of Contents

- [Design Philosophy](#design-philosophy)
- [UX Principles](#ux-principles)
- [UI Design Approach](#ui-design-approach)
- [Copywriting as Product Design](#copywriting-as-product-design)
- [The Basecamp Design Process](#the-basecamp-design-process)
- [Interface Patterns](#interface-patterns)
- [Writing the Interface](#writing-the-interface)
- [Anti-Patterns](#anti-patterns)

## Design Philosophy

The 37signals design philosophy rests on a single conviction: design is not decoration. Design is how it works. Every pixel, every word, every interaction is a product decision. The goal is not to make software that looks beautiful in a screenshot — it is to make software that feels obvious in use.

This means design starts with the problem, not the screen. Before asking "What should this look like?", ask "What is the user trying to do, and what is the fastest path to doing it?" The answer shapes everything: the layout, the copy, the interactions, and — critically — what is not on the screen.

**The three design principles:**

1. **Clarity over cleverness.** A clever interface that confuses users is a failed interface. A boring interface that gets the job done is a successful one.
2. **Reduction over addition.** When a screen is not working, the first instinct should be to remove elements, not add them. Most design problems are caused by too much, not too little.
3. **Convention over innovation.** Use standard patterns (links look like links, buttons look like buttons, forms work like forms) unless there is a compelling reason not to. Innovation for its own sake is a cost, not a benefit.

## UX Principles

### Start with the Core Job

Every screen in the product should serve a clear purpose connected to the user's core job. If you cannot articulate what the user is trying to accomplish on a screen, the screen should not exist.

**The one-screen test:** Can you describe what the user does on this screen in one sentence? If you need two sentences, the screen is doing too much. Split it or simplify it.

**Examples:**
- "The user sees all their projects and opens one." (Projects list — clear purpose)
- "The user writes a message to their team." (Message composer — clear purpose)
- "The user sees their dashboard with activity feed, upcoming deadlines, team status, notifications, and quick actions." (Dashboard — doing too much; simplify)

### Reduce to the Essence

For every element on the screen, ask: "If I remove this, does the user fail at their task?" If the answer is no, remove it. Start with the minimum viable screen and add only what is proven necessary.

**The removal checklist:**

| Element | Keep If | Remove If |
|---------|---------|-----------|
| Navigation item | User needs it at least weekly | It serves < 10% of users or is accessible from another path |
| Form field | Data is required to complete the task | Data is "nice to have" or can be inferred |
| Confirmation dialog | Action is destructive and irreversible | Action is easily undone |
| Tooltip or help text | The UI element is genuinely confusing | Better solution: rename the element so it is self-explanatory |
| Loading indicator | Operation takes > 1 second | Operation is instant |
| Success notification | User needs confirmation to proceed | The result of the action is already visible on screen |

### Design for the Happy Path First

Design the screen for the most common scenario first. Get that working perfectly. Then handle edge cases, empty states, and error states. Most users will experience the happy path most of the time — invest your design energy proportionally.

**Priority order for design attention:**
1. The happy path (80% of user time)
2. Empty states (first-time experience)
3. Error states (things that go wrong)
4. Edge cases (unusual but valid scenarios)
5. Power user features (requested by few, used by fewer)

### Make Navigation Obvious

Users should always know where they are, how they got there, and how to get back. This sounds basic because it is — and yet most software fails at it. The 37signals approach: use clear breadcrumbs, descriptive page titles, and consistent navigation patterns. Never make the user guess where they are.

## UI Design Approach

### Build in the Browser

The 37signals approach to UI design is to build in the browser from day one. This means HTML and CSS, not Figma or Sketch. The browser is the final medium — designing in an intermediate tool and then translating is waste.

**Why browser-first design works:**

- **Real interactions.** You can click, scroll, and type. You discover interaction problems immediately.
- **Real constraints.** Browser rendering, responsive behavior, and performance are immediate. No surprises at implementation time.
- **Real content.** Using real data instead of lorem ipsum reveals length issues, truncation needs, and content hierarchy problems.
- **No handoff.** The "design" and the "implementation" are the same artifact. Nothing is lost in translation.

**What this does not mean:** It does not mean the designer must write production-quality code. It means the designer works in HTML/CSS (possibly with a programmer pairing) to create the real interface. The code may be rough — it gets refined during the cycle.

### Visual Hierarchy Through Weight, Not Decoration

The 37signals UI style relies on content hierarchy achieved through font weight, size, color contrast, and whitespace — not through borders, backgrounds, shadows, or decorative elements.

**Hierarchy tools (in order of preference):**

1. **Font size.** Bigger = more important. Simple and universal.
2. **Font weight.** Bold = emphasis. Use sparingly — if everything is bold, nothing is.
3. **Color contrast.** High contrast (black text) = primary. Low contrast (gray text) = secondary. One accent color for interactive elements.
4. **Whitespace.** Generous spacing groups related elements and separates unrelated ones. Whitespace is not empty space — it is a design element.
5. **Position.** Top-left is where the eye goes first (in LTR languages). Put the most important thing there.

**What to avoid:**

- Excessive borders and dividers — use whitespace to separate instead
- Background colors on every section — reserve background color for meaningful distinction
- Shadow on every card — use shadow sparingly to create meaningful depth
- Icon overuse — icons without labels are ambiguous; use text labels

### Responsive as Reduction

When designing for smaller screens, the 37signals approach is not "rearrange everything to fit" but "remove what is not essential at this size." A mobile interface is not a shrunk desktop interface — it is a simpler interface that serves the most common mobile use cases.

**Mobile reduction principles:**

- Show only the primary action, not all available actions
- Use full-screen flows instead of modals or sidebars
- Reduce navigation to essential items only
- Prioritize reading and quick actions over complex editing
- Accept that some features are desktop-only — that is okay

### Use Standard Components

Do not invent custom UI components when standard ones exist. A standard dropdown, a standard checkbox, a standard text input — users already know how these work. Custom components carry a learning cost.

**When custom components are justified:**
- The standard component genuinely cannot serve the use case (rare)
- The custom component is dramatically simpler than the standard alternative
- The custom component is used repeatedly throughout the product (worth the investment)

**When custom components are not justified:**
- "It looks cooler" — users do not care about cool; they care about familiar
- "It matches our brand" — brand is expressed through content and tone, not through reinventing checkboxes
- "The designer wanted it" — design serves users, not designers' portfolios

## Copywriting as Product Design

At 37signals, interface copy is not an afterthought — it is a core design element. The words on the screen shape user expectations, guide behavior, and build (or erode) trust. Copy is written by the people who design and build the product, not by a separate copywriting team.

### The Copy Rules

**1. Use the fewest words possible.** Every word on the screen competes for the user's attention. Remove words that do not earn their place.

| Wordy | Concise |
|-------|---------|
| "Click the button below to save your changes" | "Save" (button label) |
| "Are you sure you want to delete this item? This action cannot be undone." | "Delete this? It can't be undone." |
| "You have successfully completed the setup process." | "You're all set." |
| "In order to proceed, please enter your email address in the field below." | "Email" (field label) |

**2. Use the simplest words possible.** Write at a 6th-grade reading level. Not because users are unsophisticated, but because simple words are processed faster by everyone, including experts.

| Complex | Simple |
|---------|--------|
| "Utilize" | "Use" |
| "Terminate" | "End" |
| "Configure" | "Set up" |
| "Authenticate" | "Sign in" |
| "Facilitate" | "Help" |
| "Leverage" | "Use" |

**3. Be specific, not abstract.** Tell the user exactly what will happen, not what category of thing will happen.

| Abstract | Specific |
|----------|---------|
| "Manage your account" | "Change your name, email, or password" |
| "Enhanced collaboration features" | "Invite your team and share files" |
| "Optimize your workflow" | "Send automatic reminders when tasks are due" |

**4. Write how you talk.** Read your copy aloud. If it sounds robotic or stilted, rewrite it. Interface copy should sound like a helpful colleague, not a legal document.

**5. Be honest about what is happening.** If something will take time, say so. If there are limitations, disclose them. If something went wrong, explain what happened. Never use vague language to hide bad news.

### Error Messages as Conversations

Error messages are the most neglected and most important copy in any application. A user encountering an error is frustrated — the error message is your chance to help them or abandon them.

**The error message formula:**

1. **What happened** (in plain language)
2. **Why it happened** (if the user can understand the cause)
3. **What to do next** (specific action the user can take)

**Examples:**

| Bad | Good |
|-----|------|
| "Error 422: Unprocessable Entity" | "That email address is already in use. Try signing in instead?" |
| "An unexpected error occurred" | "Something went wrong on our end. Try again in a few minutes." |
| "Invalid input" | "Names can only contain letters and spaces." |
| "Request failed" | "We couldn't reach the server. Check your connection and try again." |

### Empty States as Onboarding

An empty state (a screen with no content yet) is not an error — it is an opportunity. It is the user's first encounter with a feature, and it should teach them what to do next.

**Good empty state pattern:**

1. A brief explanation of what this area is for (one sentence)
2. A clear call to action (one button or link)
3. Optionally, a short example of what the area looks like when populated

**Example:**
- Bad empty state: "No items found."
- Good empty state: "This is where your team's messages live. Post the first one?" [New Message button]

## The Basecamp Design Process

The design process at 37signals integrates design thinking into every phase of the Shape Up cycle.

**During shaping (before the cycle):**

- The shaper uses breadboards to map the core interaction flow
- Fat marker sketches establish the general layout approach
- Copy is drafted for key screens — labels, button text, primary messages
- No pixel-level design work happens yet

**During building (the cycle):**

- **Days 1-3:** The designer builds the core screen in HTML/CSS with real (or realistic) copy. The programmer connects it to data. The interface is ugly but functional.
- **Days 4-10:** Design and code evolve together. The designer refines layout, typography, and spacing while the programmer implements functionality. They work on the same scopes.
- **Weeks 3-5:** The interface takes its final shape. Copy is refined. Edge cases are designed as they are discovered. Scope decisions happen in real time.
- **Week 6:** Polish. The team reviews every screen for consistency, clarity, and quality. Final copy review. Final visual review.

**Design decisions are made in context:** The designer does not design all screens up front and hand them off. They design each scope as it is built, making decisions with the full context of real data, real interactions, and real constraints.

## Interface Patterns

### Progressive Disclosure

Show the minimum necessary information first. Reveal more detail on demand. This keeps screens clean while still providing depth for users who need it.

**Examples:**
- Show a list of tasks. Click a task to see its details, comments, and history.
- Show a project summary. Expand sections to see individual metrics.
- Show the primary form fields. Link to "Advanced options" for rarely-used settings.

### Confirmation Through Visibility

Instead of showing a success toast or modal ("Item saved!"), make the result of the action visible in the interface itself. The user sees the item appear in the list, the status change, the content update. The interface is its own confirmation.

**When explicit confirmation is needed:**
- Destructive actions (delete, cancel, remove)
- Actions with delayed effects (email sent, payment processed)
- Actions where the result is not immediately visible on the current screen

### One Primary Action per Screen

Every screen should have one primary action — the thing the user is most likely to do. Make it visually prominent. Secondary actions can exist but should be visually subordinate.

**How to implement:**
- One button with the primary style (colored, prominent)
- Secondary actions as text links or muted buttons
- Destructive actions in a separate area or behind a menu

## Anti-Patterns

These are common UI/UX patterns that violate the 37signals approach:

| Anti-Pattern | Why It Fails | 37signals Alternative |
|-------------|-------------|---------------------|
| Dashboard with 12 widgets | Overwhelms; users ignore most of it | Show one thing well; link to details |
| Wizard with 7 steps | Too much friction for setup | Ask the minimum; infer the rest |
| Modal upon modal | Creates navigation confusion | Use full pages for complex interactions |
| Tooltip on every element | Signals that the UI is not self-explanatory | Rename elements to be clear without help |
| "Are you sure?" for everything | Creates modal fatigue; users click through without reading | Only confirm destructive, irreversible actions |
| Custom scrollbars | Breaks platform conventions; accessibility risk | Use native scrollbars |
| Infinite configuration page | Pushes decisions to users who do not want to make them | Pick defaults; reduce options |
| Feature comparison table on pricing | Overwhelms with complexity; induces analysis paralysis | Simple plan descriptions focusing on the job each plan serves |
| Auto-playing animations | Distracts from content; accessibility concern | Static by default; animate only on interaction |
| Notification badges on everything | Creates anxiety; trains users to ignore notifications | Notify only for things that require action |
