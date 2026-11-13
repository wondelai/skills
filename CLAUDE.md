# CLAUDE.md

## Repository Purpose

This is a collection of 65 agent skills for Claude, Claude Code, Claude Cowork, Codex, Cursor, OpenClaw, Hermes Agent and other agentskills.io-compatible agents. Skills provide specialized domain knowledge and frameworks for specific use cases (UX design, marketing, product strategy, sales, operations, positioning, virality, code quality, systems architecture, etc.). Fourteen of them are **metaskills** — guided journeys that orchestrate the other skills step by step toward a goal.

## Repository Structure

The Codex plugin standard (`plugins/` + `.agents/plugins/marketplace.json`) and the [Agent Plugins](https://agent-plugins.org/) standard (root `plugin.json` in each `plugins/*` dir, plus the `plugins/wondelai-skills` all-in-one bundle) are **generated from `.claude-plugin/marketplace.json`** by `scripts/generate-plugins.sh` — same 10 collections, same skill membership, versions tracked automatically. The plugin trees contain **copies** of the skills, not symlinks (the Agent Plugins spec requires all paths to resolve inside the plugin root), so after editing any skill's `SKILL.md` or `references/`, re-run `scripts/sync-ide-skills.sh` to refresh them. Never hand-edit the generated trees.

## Skill File Format

Each skill has a `SKILL.md` with this structure:

```markdown
---
name: skill-name
description: 'Framework description based on Author''s "Book Title". Use when you need to: (1) first use case, (2) second use case, (3) third use case.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Skill Title

Intro paragraph about the framework.

## Core Principle

**Bold opening statement.** Foundation paragraph.

## Scoring

**Goal: 10/10.** Score with a reproducible rule tied to the Quick Diagnostic that spans the full 0-10 — e.g. `score = round(rows passed / N × 10)` — then spell out the 9-10 / 7-8 / 5-6 / <=3 bands. (Don't write "1 point per row" when there are fewer than 10 rows: the top band becomes unreachable.)

## Framework Sections

### 1. First Section

**Core concept:** ...
**Why it works:** ... (only when it states a real mechanism — cut if it just restates the Core concept)
**Key insights:** (bullet list of non-obvious points only)
**Product applications:** (table: Context | Application | Example)
**Copy patterns:** (bullet list with quoted examples)
**Ethical boundary:** ... (only when a concrete, behavior-changing constraint — omit platitudes the model already follows)
See [references/file.md](references/file.md) when <situation> — <what it adds>   (inline when-to-read pointer, at the point of need; no trailing roster)

## Common Mistakes
(Table: Mistake | Why It Fails | Fix)

## Quick Diagnostic
(Table: Question | If No | Action)

## Further Reading
(Amazon links with ?tag=wondelai00-20)

## About the Author
(Author bio)
```

Skills adapted from a non-book source (a public style guide or standard, e.g. `technical-documentation`) replace `## About the Author` with `## About the Source` — the same 2-3 sentences plus the source's license and an attribution line; everything else in the template is unchanged.

### Metaskill Format (the 14 guided journeys)

The 14 metaskills (create/improve/grow × business/website/app, improve-code-quality, remove-technical-debt, design-code-architecture, conversion-optimization, architecture-optimization) are **orchestrators, not book skills** — do not force-fit the book template above (no Scoring, Further Reading, or About the Author). Their SKILL.md sections, in order: intro → `## Core Principle` (the journey's sequencing law) → `## Journey Map` (Phase | Skill | Question it answers | Artifact) → `## Operating Rules` (rules 1–7 word-identical across all 14; rule 8 is the journey-specific guardrail) → `## Intake` → `## Phases` (each phase has six fields: Purpose, Brief (fallback), Invoke, Decide with the user, Artifact, Done when) → `## Optional Phases` → `## Common Mistakes` → `## Completing the Journey`. Descriptions follow a 5-sentence formula whose 4th sentence routes to sibling metaskills (negative triggers) — keep the routing mutually consistent when editing. Metaskills write UPPERCASE artifacts into the *user's project* `docs/` folder; the canonical skeletons and section headings live in [docs/ARTIFACT-REGISTRY.md](docs/ARTIFACT-REGISTRY.md) — artifact headings quoted in phases must match it, and each metaskill's `references/artifact-templates.md` copies the skeletons it creates. The two optimization metaskills (conversion-optimization, architecture-optimization) additionally ship `references/methods.md` — the full per-phase method — so they run standalone when no constituent skill is installed.

## Adding New Skills

1. Create a new folder: `{skill-name}/`
2. Create `SKILL.md` with YAML frontmatter (`name`, `description`) and skill instructions
3. Add `references/` folder with supporting `.md` files (each 1500-3000 words)
4. Add the skill to `README.md`:
   - Add to "Via skills.sh" installation list
   - Add row to "Available Skills" table
   - Add "Skill Details" section (description, About the author, Use when, Example prompts)
   - Add to "Copyright & Disclaimer" section
5. Add the skill's path to `.claude-plugin/marketplace.json` under the appropriate plugin collection (add the `./skill-name` entry only — do **not** hand-pick a version; see Versioning Policy)
6. Run `scripts/sync-ide-skills.sh` — regenerates the IDE mirrors (`.claude/.cursor/.windsurf/.pi/.agents`) **and** the plugin trees (`plugins/` + `.agents/plugins/` — Codex and Agent Plugins formats, including the `wondelai-skills` bundle). These are generated; never hand-edit them.

## Versioning Policy

**Auto-increment rule:** When modifying a skill's `SKILL.md` or its `references/` files, always bump the version in the frontmatter:
- Content addition/enhancement → bump MINOR (e.g., `1.0.0` → `1.1.0`)
- Small fix/typo → bump PATCH (e.g., `1.1.0` → `1.1.1`)

Then re-run `scripts/sync-ide-skills.sh` — the `plugins/` trees embed copies of every skill and go stale otherwise.

### Marketplace versions (automated)

The versions in `.claude-plugin/marketplace.json` (top-level `metadata.version` and every `plugins[].version`) are **not** hand-edited. They are auto-synced to the latest GitHub release by `.github/workflows/sync-marketplace-version.yml`, which runs `scripts/sync-marketplace-versions.sh` on each published release (which in turn regenerates the `plugins/` and `.agents/plugins/` trees via `scripts/generate-plugins.sh`) and commits the result to `main`. To ship: bump the affected skills' `SKILL.md` versions, merge, then publish a `vX.Y.Z` GitHub release — the workflow sets all marketplace versions to `X.Y.Z`. To sync without a release, run `scripts/sync-marketplace-versions.sh X.Y.Z` locally.

## Testing

**Tautological tests considered harmful.** A test that restates the implementation instead of pinning behavior proves nothing: it passes for any code that compiles, fails only when the implementation is edited, and turns every refactor into a test rewrite. Typical shapes — asserting a mock returns what the test told it to return, re-deriving the expected value with the same expression the code under test uses, `expect(CONSTANT).toBe(CONSTANT)`, or snapshotting output nobody read before approving it.

Write tests against observable behavior and hand-computed expected values instead. Delete tautological tests on sight rather than fixing them — they carry no coverage to preserve. This applies to any test written in this repo and to the test examples inside the code-quality skills (`clean-code`, `working-with-legacy-code`, `refactoring-patterns`); a characterization test that pins an *observed* value is not tautological, but one that pins whatever the code recomputes at assert time is.

## Commit Policy

Commit directly to main.
