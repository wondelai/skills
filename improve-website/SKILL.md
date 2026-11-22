---
name: improve-website
description: 'Guided journey from a live website that underperforms to a prioritized, evidence-backed backlog of conversion, usability, message, and speed fixes - each shipped as a testable experiment. Orchestrates eight skills phase by phase - cro-methodology, ux-heuristics, refactoring-ui, web-typography, storybrand-messaging, high-perf-browser, made-to-stick, design-everyday-things - asking the user questions at every decision point and recording results in the project docs/ folder (WEBSITE.md, DESIGN.md, IMPROVE-WEBSITE-PLAN.md) so the journey resumes across sessions. Use when the user wants to fix a landing page that isn''t converting, diagnose why visitors leave, audit for clarity and usability, or says ''the homepage feels off but a redesign didn''t help''. No site yet, create-website; converts but needs traffic, grow-website; if the friction is in a product app, not the marketing site, improve-app; if one specific flow leaks, conversion-optimization. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Improve a Website

An interactive, resumable journey that turns a live-but-underperforming website into a ranked backlog of
defensible fixes. Across eight phases it diagnoses why visitors don't convert, then fixes usability,
hierarchy, typography, message, speed, memory, and errors — asking you at each decision point and
recording results in `docs/`. Each change is tied to a reason; the big ones ship as tests.

## Core Principle

**Diagnose, fix, prove: evidence from real visitors decides what changes, and every fix ships as a
testable hypothesis.** Order is deliberate — research first, then usability, look, message, speed,
memory, and error-tolerance, because each phase's output feeds the next.

This skill sequences the phases, asks the decision questions, and records what you decide. The
constituent skills carry the method — invoke them rather than improvising their frameworks.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | cro-methodology | Why don't visitors convert, and which fix moves the most money? | Extends docs/METRICS.md, docs/WEBSITE.md, docs/EXPERIMENTS.md — GATE |
| 2 | ux-heuristics | Where do visitors stumble before they weigh the offer? | Extends docs/DESIGN.md, docs/EXPERIMENTS.md |
| 3 | refactoring-ui | Does the page look as clear as it reads? | Extends docs/DESIGN.md, docs/EXPERIMENTS.md |
| 4 | web-typography | Can visitors comfortably read the copy? | Extends docs/DESIGN.md, docs/EXPERIMENTS.md |
| 5 | storybrand-messaging | Does a stranger grasp the offer in five seconds? | Extends docs/POSITIONING.md, docs/EXPERIMENTS.md |
| 6 | high-perf-browser | Does the page arrive before patience runs out? | Extends docs/METRICS.md, docs/WEBSITE.md, docs/EXPERIMENTS.md |
| 7 | made-to-stick | Is the idea memorable enough to survive to the decision? | Extends docs/POSITIONING.md, docs/EXPERIMENTS.md |
| 8 | design-everyday-things | Do the visitors who act ever get stuck? | Extends docs/DESIGN.md, docs/EXPERIMENTS.md |

## Operating Rules

1. **Resume first.** Before anything else, read `docs/IMPROVE-WEBSITE-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/IMPROVE-WEBSITE-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Load the phase's skill and use it: each phase's Invoke line names the skill by slug — use that skill to run the phase. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Diagnose before redesigning.** No visual or copy change ships before the Phase 1 diagnosis produces evidence for it, and every change lands in EXPERIMENTS.md with a pre-committed metric. A fix with no Phase 1 finding behind it goes back to Phase 1; a bold change with no test attached stays in the backlog until it has one.

## Intake

Ask these before creating the tracker:

1. **What page or flow are we improving, and what is the ONE action it should drive?** (Scopes every
   phase; gates Phase 1 — a page with three CTAs has no goal.)
2. **What is the conversion problem in your words, and what evidence do you have** — analytics,
   bounce rate, drop-off? (Feeds the Phase 1 funnel diagnosis.)
3. **Do you have real visitor input** — exit surveys, reviews, support tickets, recordings — or can
   you get it? (Phase 1's counter-objections must use the customer's own words.)
4. **Roughly how much traffic per week?** (Decides whether A/B tests can reach significance; low
   traffic leans on the qualitative and heuristic phases.)
5. **Which complaint do you hear most** — "looks unprofessional," "nobody understands what we do,"
   "it's slow," "the text is hard to read"? (Routes which fix phase to front-load, per the guide FAQ.)
6. **Do you have existing positioning or brand docs (POSITIONING.md)?** (Phase 5 and 7 build on them.)
7. **Can you share real assets** — URLs, live copy, CSS, analytics screenshots? (The skills are only
   as good as the evidence you feed them.)

Live assets: if the user gives a URL and
[Firecrawl](https://docs.firecrawl.dev/mcp-server?utm_source=wondelai-skills&utm_medium=integration)
is available (MCP, or `firecrawl scrape <url> --format markdown,branding --full-page-screenshot --json`),
pull the rendered copy, a full-page screenshot, and the fonts, colors, and type sizes yourself, then
confirm them with the user. If it is not available or the result is incomplete, ask the user to paste
them. Analytics always comes from the user.

Skip heuristics: skip Phase 4 if body text already meets 16px / ~66ch / 1.5-1.7 line height; skip Phase 6
if Core Web Vitals are already green (but triage a fast LCP fix first if the page barely renders); skip
Phase 5 or 7 if messaging is already validated and clear. Never skip Phase 1 — it aims every other phase.

Then create `docs/IMPROVE-WEBSITE-PLAN.md` from the template and confirm the plan. Done when
`docs/IMPROVE-WEBSITE-PLAN.md` exists with every phase statused and the user has confirmed the plan.

## Phases

### Phase 1 — Diagnose why visitors don't convert (cro-methodology) — GATE

**Purpose:** Find where and why the page loses visitors before any pixel changes. Phases 2-8 may only
fix problems traceable to a Phase 1 finding.

**Brief (fallback):** Don't guess — discover. Map the funnel for blocked arteries (underperforming
high-traffic stages) and missing links (stages that don't exist). Name the ONE action each page drives.
Build the O/CO table for the Big 5 (Trust, Price, Fit, Timing, Effort) in the customer's words, each counter at friction. Rank by ICE.

**Invoke:** Use the `cro-methodology` skill with the target page/flow, the ONE action, and real visitor input. Ask
for a funnel map, an O/CO table, missing persuasion assets, and an ICE-ranked hypothesis list.

**Decide with the user:** (1) Confirm the ONE action per page; cut competing CTAs. (2) Attack the
highest-money blocked artery or a missing link first? (3) Low traffic: accept qualitative + heuristic evidence.

**Artifact:** Extend docs/METRICS.md `## Funnel` and `## Stage & One Metric That Matters`; docs/WEBSITE.md
`## Conversion Elements` and `## Audit Findings` (issue | severity 0-4 | fix | status); docs/EXPERIMENTS.md
`## Experiment Backlog` (ICE-ranked). Update the tracker.

**Done when:** the funnel is mapped, the ONE action set per page, every researched objection has a
counter, the backlog is ICE-ranked, and Phase 1 shows done — only then are Phases 2-8 unlocked.

### Phase 2 — Remove the usability friction (ux-heuristics)

**Purpose:** Find where visitors stumble — the friction that makes them quit before they weigh the offer.

**Brief (fallback):** Don't make me think. Users scan, satisfice, and muddle through. Run a heuristic
evaluation against Nielsen's 10 heuristics; rate each issue 0-4 by frequency, impact, and persistence
so catastrophes outrank cosmetics. Apply the Trunk Test to interior pages (what site, page, options,
where am I, where's search?). Cut half the words, then half again; kill mystery-meat icon navigation.

**Invoke:** Use the `ux-heuristics` skill with the page/flow and the Phase 1 findings. Ask for a severity-rated
evaluation, a Trunk Test result per key page, and rewritten error and label copy.

**Decide with the user:** Which severity-4 and -3 issues get fixed now versus backlogged? Confirm fixes
run by severity, not by ease.

**Artifact:** Extend docs/DESIGN.md `## UX Audit Findings` (issue | heuristic | severity 0-4 | fix |
status); append each fix to docs/EXPERIMENTS.md `## Experiment Backlog` with ICE. Update the tracker.

**Done when:** every issue carries a 0-4 severity, the Trunk Test passes on each key page or is logged,
and severity-4 issues have an owner.

### Phase 3 — Fix the visual hierarchy (refactoring-ui)

**Purpose:** Make the page look as clear as it reads — one obvious focal point, not everything competing.

**Brief (fallback):** Great UI is systems, not talent. Design in grayscale first: establish hierarchy
with size, weight, and contrast before any color — combine levers, don't multiply (all three only for
the hero element). Enforce a spacing scale (4/8/16/24/32/48/64) where gaps between groups exceed gaps
within them. Constrain text to 45-75 chars. Add color last: 5-9 shades per hue, grays tinted, not #000.

**Invoke:** Use the `refactoring-ui` skill with the page, the Phase 2 findings, and the CSS framework. Ask for a
grayscale hierarchy pass, spacing-scale corrections, a systematic palette, and exact class/CSS changes.

**Decide with the user:** Fix within the current design system or introduce new tokens? Confirm color
work waits until the grayscale layout reads.

**Artifact:** Extend docs/DESIGN.md `## Tokens` (spacing scale · palette shades · shadows) and `## Components`
(component | decision | status); append fixes to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** the layout reads in grayscale, the spacing scale is applied, one primary CTA dominates,
and the token decisions are recorded.

### Phase 4 — Make the words readable (web-typography)

**Purpose:** Fix the measurements that decide whether visitors can comfortably read the copy.

**Brief (fallback):** Size, line length, and line height matter more than the typeface. Fix three: body
≥16px (18px for reading-heavy pages); line length 45-75 chars (~66 sweet spot) via ch or max-width; line
height 1.5-1.7 body, 1.1-1.25 headings. Build a modular scale; load fonts with swap, preload one, subset, <200KB.

**Invoke:** Use the `web-typography` skill with the reading-heavy templates and the DESIGN.md type decisions. Ask for
corrected CSS with a fluid clamp() scale and a font-loading plan.

**Decide with the user:** Keep the current typefaces or repair the pairing? Confirm the font-loading
budget (<200KB) that Phase 6 will verify.

**Artifact:** Extend docs/DESIGN.md `## Typography` (typefaces · scale · measure · line height · loading
strategy); append fixes to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** body size, measure, and line height meet targets on the key templates, the scale is
defined, and the loading strategy is recorded.

### Phase 5 — Sharpen the message (storybrand-messaging)

**Purpose:** Make a stranger understand what you do and why it matters in five seconds.

**Brief (fallback):** The customer is the hero; your brand is the guide (Yoda, not Luke). Run SB7: a
Character wanting one thing, a Problem at three levels (external / internal / philosophical — most brands
miss the internal), a Guide with empathy and authority, a Plan of 3-4 safe steps, one Direct plus one
Transitional CTA, and Failure/Success stakes. Write the "We help [X] who struggle with [Y] to [Z]" one-liner.

**Invoke:** Use the `storybrand-messaging` skill with the current copy, POSITIONING.md if it exists, and the internal
problems from the Phase 1 objections. Ask for above-the-fold rewrites, a BrandScript, and one-liners.

**Decide with the user:** Which one-liner passes the repeat-after-one-hearing test? Confirm the internal
problem the copy must name.

**Artifact:** Extend docs/POSITIONING.md `## Brand Script (StoryBrand)`, `## One-Liner`, and `## Key Messages`
(surface | message | status); append copy tests to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** the one-liner is chosen, above-the-fold copy names the internal problem with one Direct
and one Transitional CTA, and the messages are logged by surface.

### Phase 6 — Make the page fast (high-perf-browser)

**Purpose:** Ensure a slow load doesn't waste the clarity work — the page must arrive before patience runs out.

**Brief (fallback):** Latency, not bandwidth, is the bottleneck — cut round trips. Target Core Web Vitals:
LCP <2.5s, INP <200ms, CLS <0.1, TTFB <800ms. Preload the LCP hero element; reserve space (width/height or
aspect-ratio) to stop CLS; defer non-critical JS; inline critical CSS; cache immutable; on HTTP/2 undo sharding.

**Invoke:** Use the `high-perf-browser` skill with the page URL and a performance trace or Lighthouse run if
available. Ask for the LCP element, layout-shift sources, blocking resources, and a prioritized fix list.

**Decide with the user:** If the page barely renders, triage a fast LCP fix before the rest? Which fixes
ship now versus need a test?

**Artifact:** Extend docs/METRICS.md `## Baselines & Targets` (CWV metric | baseline | target | miss response)
and docs/WEBSITE.md `## Audit Findings`; append fixes to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** CWV baselines and targets are recorded, every fix has an owner, and any HTTP/1.1
workaround still active on HTTP/2 is flagged.

### Phase 7 — Make the core idea stick (made-to-stick)

**Purpose:** Make the offer memorable enough to survive the gap between the visit and the decision.

**Brief (fallback):** Beat the Curse of Knowledge. Score key messages on SUCCESs (Simple, Unexpected,
Concrete, Credible, Emotional, Stories). Concrete: replace abstraction with sensory specifics ("order
in 30 minutes, still hot"; "save 16 hours a month"). Simple: the Commander's Intent — the one thing
visitors must remember. Make statistics human-scale (Sinatra Test); prefer specific over round figures.

**Invoke:** Use the `made-to-stick` skill with the headline, value prop, and key features plus the Phase 5 one-liner.
Ask for a SUCCESs score per message with concrete rewrites, the Commander's Intent, and a human-scale stat.

**Decide with the user:** What is the single Commander's Intent message? Which abstractions become which
concrete specifics?

**Artifact:** Extend docs/POSITIONING.md `## Key Messages` with SUCCESs scores and concrete rewrites; append
copy tests to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** each key message has a SUCCESs score and a concrete rewrite, the Commander's Intent is
named, and the key statistic is human-scale.

### Phase 8 — Design out the errors (design-everyday-things)

**Purpose:** Protect the visitors who decided to act — make the wrong action impossible, not just warned against.

**Brief (fallback):** There is no human error, only bad design. Bridge two gulfs: Execution ("how do I
do this?") with clear signifiers (pressable buttons, editable fields) and constraints (date picker over
free text, Submit disabled until valid); Evaluation ("what happened?") with feedback within 0.1s. Fix
slips with undo and separated destructive actions; error messages say what went wrong and how to fix, no blame.

**Invoke:** Use the `design-everyday-things` skill with the conversion-critical flows (signup, checkout, account
setup). Ask for weak signifiers, where constraints make errors impossible, feedback gaps, and message rewrites.

**Decide with the user:** Where should a constraint replace an error message? Where should undo replace
an are-you-sure confirmation?

**Artifact:** Extend docs/DESIGN.md `## UX Audit Findings` (issue | heuristic = Norman gulf | severity 0-4 |
fix | status); append fixes to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** each conversion flow has signifier/constraint/feedback fixes logged, error messages meet
the checklist, and destructive actions offer undo.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| influence-psychology | objection points need ethical persuasion assets (social proof, authority, real scarcity) | Extends docs/WEBSITE.md `## Conversion Elements` |
| microinteractions | interactions feel dead or unresponsive | Extends docs/DESIGN.md `## Microinteraction Inventory` |
| top-design | the redesign warrants a signature moment, not just fixes | Extends docs/DESIGN.md `## Design Direction` |
| steve-jobs-design-review | before relaunch, for a brutal end-to-end verdict | Extends docs/WEBSITE.md `## Audit Findings` |

Optional phases follow the same operating rules — load and use each listed skill exactly as a core phase would; insert where the Add-when condition first becomes true.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Redesigning before researching — a prettier page on the same unaddressed objections converts identically. | Run Phase 1 (cro-methodology) first; no visual or copy change ships without a Phase 1 finding behind it. |
| Testing meek tweaks (button colors, font nudges) too small to ever reach significance. | Use ICE scoring to pick bold changes; ask "could this 10x results?" before you test it (cro-methodology). |
| Adding color before the grayscale layout works. | Grayscale first, color last; if the page fails desaturated, no palette saves it (refactoring-ui). |
| Optimizing speed in a vacuum, ahead of the clarity work. | Sequence speed after clarity (Phase 6); exception — triage a fast LCP fix if the page barely renders (high-perf-browser). |
| Treating "user error" as the user's fault and adding more warnings. | Prevent errors with constraints and forgive them with undo, not dialogs (design-everyday-things). |
| Confusing clarity with stickiness — a clear message can be instantly forgotten. | Run both Phase 5 and Phase 7; StoryBrand makes you understood, Made to Stick makes you remembered. |

## Completing the Journey

Exit checklist:

- [ ] Every phase in `docs/IMPROVE-WEBSITE-PLAN.md` is `done` or `skipped: reason`.
- [ ] WEBSITE.md, DESIGN.md, POSITIONING.md, and METRICS.md carry every fix as a table row with owner and priority.
- [ ] Each high-ICE change is a designed A/B test in EXPERIMENTS.md `## Experiment Cards` with a pre-committed metric.
- [ ] The ONE action per key page is unambiguous and competing CTAs are removed.

Close the loop by re-invoking `cro-methodology` to design the bold tests for the high-ICE backlog: size
the sample up front, run one full business cycle, require 95% confidence, never peek early — then promote
them from `## Experiment Backlog` to `## Experiment Cards`, and close the tracker with Next Actions carried into the artifacts.

Forward routing: when the site converts and needs more qualified traffic, continue with the `grow-website` skill.
When the friction lives in the product, not the marketing site, continue with the `improve-app` skill.
