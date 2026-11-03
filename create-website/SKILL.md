---
name: create-website
description: 'Guided journey from a blank page to a live, high-converting website, built message-first, then design, then conversion. Orchestrates ten skills phase by phase - one-page-marketing, storybrand-messaging, made-to-stick, top-design, web-typography, refactoring-ui, ux-heuristics, cro-methodology, scorecard-marketing, steve-jobs-design-review - asking the user questions at every decision point and recording results in the project docs/ folder (POSITIONING.md, WEBSITE.md, CREATE-WEBSITE-PLAN.md) so the journey resumes across sessions. Use when the user wants to build a new website or landing page from scratch, turn a validated idea into a page that converts, or says ''build me a landing page for my SaaS''. Site already exists: use improve-website site-wide, conversion-optimization for one flow, or grow-website for traffic; building a software product, not a marketing site: create-app; no positioning yet: create-business first, or the positioning phase here. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Create a Website

A blank page becomes a live, high-converting website through ten phases run in one dependency-respecting order: message, then design, then conversion, then a brutal review. This journey is interactive — the agent asks before every decision and never designs before the message is settled — and resumable, because every decision and artifact lives in the project's `docs/` folder. You drive the phases; the constituent skills carry the method.

## Core Principle

**Message before design, design before conversion — in that order; looks-fine is the floor, not the goal.** A visitor decides in five seconds whether to stay, and that decision rides on whether they instantly understand what you do and why it matters to *them* — so clarity comes first and design serves it. This skill sequences the phases, asks the questions, and records the decisions; the constituent skills carry the frameworks. Invoke them rather than improvising their method.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | one-page-marketing | Who is this for, and what is the site's one job? | Creates docs/MARKETING.md; extends docs/CUSTOMER.md |
| 2 | storybrand-messaging | What do we say, with the customer as hero? | Creates docs/POSITIONING.md, docs/WEBSITE.md |
| 3 | made-to-stick | How do we make the message memorable? | Extends docs/POSITIONING.md, docs/WEBSITE.md |
| 4 | top-design | What makes this page unforgettable to look at? | Creates docs/DESIGN.md |
| 5 | web-typography | Is the type readable as well as dramatic? | Extends docs/DESIGN.md |
| 6 | refactoring-ui | Is the design consistent and systematic? | Extends docs/DESIGN.md |
| 7 | ux-heuristics | Can anyone use it without thinking? | Extends docs/DESIGN.md |
| 8 | cro-methodology | Why don't visitors convert, and what answers them? | Extends docs/WEBSITE.md, docs/EXPERIMENTS.md |
| 9 | scorecard-marketing | How do we capture the not-ready-to-buy majority? | Extends docs/WEBSITE.md, docs/MARKETING.md |
| 10 | steve-jobs-design-review | Is it insanely great, or not done? | Extends docs/WEBSITE.md — GATE |

## Operating Rules

1. **Resume first.** Before anything else, read `docs/CREATE-WEBSITE-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/CREATE-WEBSITE-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Load the phase's skill and use it: each phase's Invoke line names the skill by slug — use that skill to run the phase. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Every scarcity claim, testimonial, and guarantee on the site must be true.** When a persuasion tactic needs inventing evidence, replace it with a tactic that uses evidence you have.

## Intake

Ask these before creating the tracker:

1. What is the product or service, and who is it for? (Gates Phase 1's niche and avatar, and every word of the message.)
2. Do `docs/POSITIONING.md` or `docs/CUSTOMER.md` already exist from a create-business run? (If yes, lighten Phases 1-2 and reuse them; if positioning is thin, add the obviously-awesome optional phase.)
3. What is the single primary conversion goal — start a trial, book a demo, purchase, or take a quiz? (Gates every CTA decision in Phases 1, 8, 9.)
4. Full multi-page site or a single landing page? (Gates sitemap scope and whether Phases 8-9 apply.)
5. What is the tech stack and where does the code live? (So design and copy land in real files, not a hand-off doc.)
6. What proof assets exist today — testimonials, results, logos, guarantees? (Gates the Phase 8 persuasion audit and Rule 8.)
7. How much does craft matter — competing on design, or a functional site? (Gates whether Phases 4-5 run fully or lightly.)

Skip heuristics: skip Phase 1 when a prior run already fixed the niche, avatar, and USP; run Phases 4-5 lightly for an internal or throwaway page where craft does not sell (never skip refactoring-ui); skip Phase 9 when one direct CTA suffices and there is no nurture motion; skip Phase 3 only under a brutal timeline — and warn that clear-but-forgettable copy evaporates. Then create the tracker from the template and confirm the plan.

Done when `docs/CREATE-WEBSITE-PLAN.md` exists with every phase statused and the user has confirmed the plan.

## Phases

### Phase 1 — Frame the strategy and pick one niche (one-page-marketing)

**Purpose:** Decide who the site is for, the USP, and the single primary conversion goal before any page exists.

**Brief (fallback):** PVP Index — score candidate niches on Personal fulfillment, Value to the market, and Profitability, then pick *one*. "Speak to everyone, speak to no one." Write a USP that passes the swap test: if a competitor's name fits your tagline, it is too generic. Map the Before and During squares to concrete pages, each with one job.

**Invoke:** Use the `one-page-marketing` skill with the product and target from intake. Ask for (a) PVP scores for 2-3 niches, (b) a one-paragraph avatar, (c) a swap-test USP, (d) the Before/During squares mapped to homepage, landing, and lead-capture pages.

**Decide with the user:** Which niche to dominate (recommend the highest PVP score)? What is the single primary conversion goal — trial, demo, purchase, or quiz lead?

**Artifact:** Create docs/MARKETING.md with `## Target Market & Avatar` (niche, avatar, USP, primary goal) and `## Before / During / After Grid`. Extend docs/CUSTOMER.md with `## Segments & Best-Fit Customer`. Update the tracker.

**Done when:** MARKETING.md names one niche, a swap-test USP, and one primary goal; CUSTOMER.md records the best-fit segment; the user confirmed the niche and goal.

### Phase 2 — Write the message with StoryBrand (storybrand-messaging)

**Purpose:** Write the words the visitor judges in five seconds — customer as hero, you as guide.

**Brief (fallback):** SB7 — a Character who wants something, a Problem (external/internal/philosophical), a Guide with empathy and authority, a Plan, a call to Action, the stakes of Failure, a vivid Success. Name the internal problem (how it *feels*), not just the external one. One-liner: "We help [character] who struggle with [problem] to [solution] so they can [result]."

**Invoke:** Use the `storybrand-messaging` skill with the avatar and USP from MARKETING.md. Ask for a full BrandScript, homepage copy following the StoryBrand wireframe (header, stakes, value, guide, plan, CTA), and five one-liner variations ranked by repeatability.

**Decide with the user:** Which one-liner is most repeatable after a single hearing? Confirm the customer, not the brand, is the hero — no opening "We…".

**Artifact:** Create docs/POSITIONING.md with `## Brand Script (StoryBrand)`, `## One-Liner`, `## Key Messages`. Create docs/WEBSITE.md with `## Sitemap` and `## Page Briefs` (wireframe-derived copy blocks). Update the tracker.

**Done when:** POSITIONING.md holds a complete BrandScript and a locked one-liner; WEBSITE.md has a sitemap and a homepage page brief; the user approved the one-liner.

### Phase 3 — Make the message stick (made-to-stick)

**Purpose:** Turn clear copy into memorable copy that survives the closed tab and gets repeated.

**Brief (fallback):** SUCCESs — Simple, Unexpected, Concrete, Credible, Emotional, Story. Fight the Curse of Knowledge. Highest leverage is Concrete: replace every abstraction with a picture ("report generation from 4 hours to 10 minutes"). Add one unexpected hook, one Sinatra-test proof, and one named-customer story.

**Invoke:** Use the `made-to-stick` skill with the copy in WEBSITE.md `## Page Briefs` and the messages in POSITIONING.md. Ask for a SUCCESs score, concrete rewrites of every abstract benefit, one unexpected hero hook, and a short customer story.

**Decide with the user:** Approve the sticky rewrites and pick the hero hook. Which numbers and claims are true and citable (this feeds Rule 8)?

**Artifact:** Extend docs/POSITIONING.md `## Key Messages` (sticky versions) and docs/WEBSITE.md `## Page Briefs` (concrete copy). Update the tracker.

**Done when:** every abstract benefit is a concrete outcome with a real, true number, one unexpected hook and one customer story exist, and the copy is signed off.

### Phase 4 — Design the signature moment (top-design)

**Purpose:** Make the page look agency-built, not template-built — starting from the one screenshot-worthy moment.

**Brief (fallback):** Every pixel intentional. Start with the signature moment (usually the hero), not the header: dramatic scale (min 10:1 display-to-body), an asymmetric composition, a choreographed load with ~80ms staggered word reveals. Custom cubic-beziers (expo-out `0.16,1,0.3,1`), animate only `transform`/`opacity`, warm off-blacks (`#0a0a0a`) not pure black. Custom cursor only if the user opts in.

**Invoke:** Use the `top-design` skill with POSITIONING.md and the WEBSITE.md page briefs. Ask for the signature hero design, a custom color system (no AI purple-to-blue gradient), and a scored audit across typography, composition, motion, color, and details.

**Decide with the user:** What is the signature moment worth screenshotting? Approve the color system. Custom cursor — yes, or native (recommend native unless craft is the product)?

**Artifact:** Create docs/DESIGN.md with `## Design Direction` (signature moment, personality, references). Update the tracker.

**Done when:** DESIGN.md names the signature moment and color system, the top-design audit scores are recorded, and the user approved the direction.

### Phase 5 — Choose and tune the type (web-typography)

**Purpose:** Make the type readable as well as dramatic — the discipline behind the drama.

**Brief (fallback):** Clear-goblet principle — type serves content. "Type for a moment" (headlines) versus "type to live with" (body). Three measures beat typeface choice: 16-18px body, 45-75ch measure (66 optimal, `max-width: 65ch`), line height 1.5-1.7 body / 1.1-1.25 headings. One to two families. Under 200KB payload, WOFF2, variable fonts, `clamp()` fluid scale, preload + `font-display: swap`.

**Invoke:** Use the `web-typography` skill with DESIGN.md `## Design Direction`. Ask for a display+body pairing, full CSS (clamp scale, per-context line heights, 65ch measure), and a font-loading plan under 200KB with zero layout shift.

**Decide with the user:** Approve the pairing; confirm the performance budget (recommend a single variable font to cut the file count).

**Artifact:** Extend docs/DESIGN.md `## Typography` (typefaces, scale, measure, line height, loading strategy). Update the tracker.

**Done when:** DESIGN.md `## Typography` specifies the pairing, scale, measures, and a sub-200KB loading strategy, and the user approved the pairing.

### Phase 6 — Make it systematic (refactoring-ui)

**Purpose:** Add the consistency that keeps the wow from collapsing on the second and third sections.

**Brief (fallback):** Design in grayscale first, add color last. Systems over talent: constrained scales for spacing (4, 8, 16, 24, 32, 48, 64), type, color, and shadow. Hierarchy from combining levers (large OR bold OR dark), saving all three for one element. Space between groups exceeds space within. Near-black (`#111827`) not pure `#000`, tinted grays. Two-layer shadows mapped to elevation. Run the blur test.

**Invoke:** Use the `refactoring-ui` skill with DESIGN.md. Ask for a grayscale hierarchy audit, a constrained token set (spacing, a 9-shade palette with tinted grays, a type scale, a shadow scale), and refactored button/form/card components with one primary action per section.

**Decide with the user:** Approve the token scales; confirm the primary/secondary/tertiary button hierarchy.

**Artifact:** Extend docs/DESIGN.md `## Tokens` (spacing, palette, shadows) and `## Components` (per-component decisions). Update the tracker.

**Done when:** DESIGN.md defines the token scales and component decisions, buttons show one clear primary per section, and the user approved the tokens.

### Phase 7 — Make it effortless to use (ux-heuristics)

**Purpose:** Remove the friction of making a visitor think.

**Brief (fallback):** Pages must be self-evident; users scan, satisfice, and muddle through. Trunk Test — dropped onto any page cold, can they answer what site, what page, what sections, and where to go next? Run "get rid of half the words." Plain-language CTAs. Inline validation on blur, mark optional not required fields, 44x44px tap targets, visible system status ("Saving…"/"Saved", skeletons, confirmations).

**Invoke:** Use the `ux-heuristics` skill with WEBSITE.md and DESIGN.md. Ask for a usability audit against Krug's laws and Nielsen's 10 heuristics, each issue rated 0-4, plus rewritten error messages and CTA labels.

**Decide with the user:** Approve the prioritized fix list starting with catastrophic (4) issues; confirm which fixes ship before launch versus later.

**Artifact:** Extend docs/DESIGN.md `## UX Audit Findings` (Issue | Heuristic | Severity | Fix | Status). Update the tracker.

**Done when:** every page passes the Trunk Test, catastrophic issues are fixed, UX Audit Findings are logged with severities, and the user approved the fix order.

### Phase 8 — Engineer the conversion (cro-methodology)

**Purpose:** Turn a clear, usable page into one that answers the real reasons visitors don't convert.

**Brief (fallback):** Don't guess — discover. Build an Objection/Counter table for the Big 5 (Trust, Price, Fit, Timing, Effort); place each counter at the point of friction, never buried in an FAQ; use "CO Only" for objections a visitor won't admit. Proof hierarchy: specific results with context > named testimonials > case studies > bare logos. Proof sandwich; specific numbers ("47,832" not "about 50,000").

**Invoke:** Use the `cro-methodology` skill with WEBSITE.md and the proof assets from intake. Ask for a Big-5 Objection/Counter table with placements, a persuasion-asset audit ranked by the proof hierarchy, a wish list of missing proof, and A/B test hypotheses.

**Decide with the user:** Which counters ship now versus await proof you must acquire? Confirm no counter invents evidence (Rule 8).

**Artifact:** Extend docs/WEBSITE.md `## Conversion Elements` (Objection | Counter | Placement | Status). Extend docs/EXPERIMENTS.md `## Experiment Cards` and `## Experiment Backlog`. Update the tracker.

**Done when:** the Big-5 table has an evidence-backed counter and placement per objection, missing proof is listed as actions, test hypotheses are logged, and no counter relies on invented evidence.

### Phase 9 — Add a lead-generating quiz (scorecard-marketing)

**Purpose:** Capture the ~97% not ready to buy today with a lower-commitment offer.

**Brief (fallback):** Everything is downstream from lead generation; a quiz converts 30-50% versus 3-10% for a static PDF. Four steps: a landing page (concept hook + the 3 Cs — Clarity, Credibility, Connection), a questionnaire that captures the email *before* the questions, a tiered results page, and a segmented follow-up. "Moving toward" hooks beat fear-based ones. Keep it to 8-15 questions for cold traffic.

**Invoke:** Use the `scorecard-marketing` skill with the primary goal and avatar. Ask for a concept hook and landing page, 10-12 scored questions in 3-4 categories, three result tiers with dynamic copy and a CTA each, and a follow-up sequence segmented by tier.

**Decide with the user:** Does the site need a lead-nurture motion? If one direct CTA suffices, skip this phase. Otherwise approve the concept hook.

**Artifact:** Extend docs/WEBSITE.md `## Lead Capture` (quiz funnel design). Extend docs/MARKETING.md `## Nurture Sequences` (tiered follow-up). Update the tracker.

**Done when:** WEBSITE.md `## Lead Capture` specifies a hook, ≤15 questions with email captured first, and tiered results; MARKETING.md holds the segmented follow-up; the hook promises only what the assessment delivers.

### Phase 10 — Hold it to an insanely-great bar (steve-jobs-design-review) — GATE

**Purpose:** Subject the finished site to one brutal, honest review before a single visitor sees it.

**Brief (fallback):** "Start with the customer experience and work backwards." Experience it cold as a stranger. State the One Thing in a single sentence. Count steps-to-value (three, not nine). Walk the slow paths — empty form, error state, failed payment, mobile cold-start. Check the back of the fence — 404, error copy, confirmation email. The verdict is binary: insanely great, or not done. Focusing is saying no.

**Invoke:** Use the `steve-jobs-design-review` skill with the live site or full page set. Ask for a cold first impression, the One Thing, a steps-to-value count, a walk of the failure/empty states and the back of the fence, a binary verdict, and a ranked cut list plus fix list.

**Decide with the user:** Act on the cut list — what to delete to protect the single primary goal? If the verdict is NOT DONE, which fixes are blocking launch?

**Artifact:** Extend docs/WEBSITE.md `## Audit Findings` (Issue | Severity | Fix | Status) with the cut list and fix list. Update the tracker.

**Done when:** the verdict is INSANELY GREAT (not "pretty good"), the cut list is applied, the back of the fence is checked, and blocking fixes are closed — only then does the site launch.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| obviously-awesome | `docs/POSITIONING.md` does not exist yet and the messaging has nothing to stand on | Creates docs/POSITIONING.md |
| influence-psychology | Pricing or signup pages need persuasion-principle audits | Extends docs/WEBSITE.md |
| high-perf-browser | Core Web Vitals or load speed threaten conversions | Extends docs/WEBSITE.md |
| design-everyday-things | Forms or flows confuse users despite clean visuals | Extends docs/DESIGN.md |
| microinteractions | The site needs interaction polish beyond static design | Extends docs/DESIGN.md |

Optional phases follow the same operating rules — load and use each listed skill exactly as a core phase would; insert where the Add-when condition first becomes true.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Designing before you have a message | Run Phase 2 (storybrand) and Phase 3 before Phase 4 (top-design); design serves the words, never the reverse. |
| Making your brand the hero | In storybrand, open with the customer's problem and desired outcome; if the first sentence starts with "We," rewrite it. |
| Stacking competing calls to action | Keep one direct CTA and one transitional; refactoring-ui and the Jobs review both enforce one primary action per section. |
| Confusing clear with sticky | Run the made-to-stick pass — concrete numbers, one unexpected hook, one customer story — so the message survives the closed tab. |
| Testing button colors instead of objections | Build the Objection/Counter table in cro-methodology first; "meek tweaks" rarely move conversion. |
| Polished happy path, broken everywhere else | In the Jobs review, walk the empty state, form error, 404, confirmation email, and mobile cold-start — the back of the fence. |

## Completing the Journey

Exit checklist:
- [ ] POSITIONING.md holds a BrandScript, a repeatable one-liner, and key messages consistent across surfaces
- [ ] WEBSITE.md has a sitemap, page briefs with copy, an Objection/Counter table, and (if in scope) a lead-capture design
- [ ] DESIGN.md defines direction, typography, tokens, components, and a passed UX audit
- [ ] The Steve Jobs review returned INSANELY GREAT — not "pretty good" — and the cut list is applied
- [ ] Every scarcity claim, testimonial, and guarantee on the page is true

Close the tracker: every phase `done` or `skipped: reason`, with any remaining Next Actions carried into the artifacts as checkboxes. Then route forward:

- **Public launch and technical handover (when requested):** if the owner wants the site public and either publishing or the enquiry/booking path is still unfinished, record the unfinished launch work as a Next Actions checkbox before starting it, then finish only that work in the agreed stack. Connect a real form or booking service, or label the fallback as a prototype that does not send. If a real service is connected, send one test enquiry or booking and confirm it reaches the owner before calling the launch done; a prototype or a publish without a form needs no such test. Check the phone layout, title, description and share preview, and follow the publishing host's own setup steps. A host-provided address or an existing domain is fine; a new custom domain is optional and the owner's decision. Record the public URL and unfinished owner actions in the tracker. When the launch work finishes, mark its Next Actions checkbox done.
  For a detailed implementation example, an agent may consult the [full MIT business-website launch workflow published by Add Domain](https://raw.githubusercontent.com/vitaliiphangan-code/add-domain-website-skills/5cfd2313a4b54ea9b22110224c71c5203106b07b/skills/frontend-business-websites/SKILL.md), pinned to an immutable commit. It is optional and does not replace the phases above.
- **Post-launch iteration:** when the site is live and conversion data starts arriving, continue with the `improve-website` skill to turn today's assumptions into tested wins. When the website sells a product that now needs building, continue with the `create-app` skill.
