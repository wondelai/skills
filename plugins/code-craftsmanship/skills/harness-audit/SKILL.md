---
name: harness-audit
description: 'Audit and harden a repository''s AI coding agent harness across the 6 Software Factory Stations (Intent, Harness, Loop, Graph, Verification, Release) and place it on the Autonomy Ladder (Level 0–5). Use when you need to: (1) audit a repo''s readiness for Claude Code, Codex, or Cursor using `@wondelai/harness-audit` or manual inspection, (2) diagnose why agents drift, loop, break tests, or stall in PR review, (3) fix duplicated AGENTS.md/CLAUDE.md, broken MCP configs, retired Codex settings, unguarded Stop hooks, or weak test oracles, (4) generate a verified remediation plan or scaffold starter harness files safely, or (5) climb from Level 2 paired prompting to Level 3–4 spec-driven verified loops.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Harness Audit

Audit, score, and harden the repository machinery around your coding agents — instructions, permissions, hooks, MCP configs, verification loops, worktree isolation, test oracles, and release gates — so Claude Code, OpenAI Codex, and Cursor produce reliable, verifiable changes instead of plausible-looking regressions.

## Core Principle

**Autonomy is earned by verification, never granted by prompt optimism.** A repository's maturity on the Autonomy Ladder (Level 0 to Level 5) is capped by its weakest safety gate: polished `AGENTS.md` files cannot compensate for missing CI, hardcoded secrets, broken MCP servers, or tests an agent can silently weaken to go green. Every audit starts with deterministic facts on disk — ideally by running `npx @wondelai/harness-audit` — pairs them with a qualitative inspection of instruction signal-to-noise and test strength, and closes every fix with a command-and-output verification ledger.

Two framing rules govern every audit and remediation:

- **One level per loop, capped by risk class.** Maturity belongs to a repeatable class of change (dependency bumps, bug fixes, feature work), while risk class (`low`, `medium`, `high`, `critical`) caps individual changes. Auth, payments, schema migrations, secrets, tests, and CI remain human-read even in a Level 4–5 repository.
- **Verify every claim against the live repo.** Never invent build commands, flags, or MCP package names from memory. Run every verification command and check every config key before committing it to `AGENTS.md` or CI.

## Scoring

**Goal: 10/10.** `score = number of Quick Diagnostic rows passed` (10 rows, 1 point each).

- **9–10:** Production-grade harness (typically Autonomy Level 4–5, subject to zero blocking caps) — maintain through periodic audits and incident feedback loops.
- **7–8:** Solid Level 3 foundation — focus on oracle protection (`CODEOWNERS`), evidence-oriented PR templates, and eliminating review bottlenecks.
- **5–6:** Level 2 paired ceiling — consolidate instructions, harden permissions/hooks/MCP hygiene, and establish a single fast verification loop before scaling agent autonomy.
- **≤4:** Level 0–1 ad-hoc state — establish canonical `AGENTS.md`, deterministic local `typecheck` + `lint` + `test`, and PR-triggered CI before delegating multi-file tasks.

**Hard gating caps (blocking regardless of raw score):** hardcoded credentials or retired/bypassed permission policies cap a repo at **Level 2**; missing CI or tautological/broken tests cap it at **Level 3**; unprotected test/CI oracles cap it at **Level 4**.

## Framework

### 1. Run the Deterministic Baseline First

**Core concept:** Before offering opinions, establish an objective, file-backed baseline across all six Software Factory Stations (`Intent`, `Harness`, `Loop`, `Graph`, `Verification`, `Release`).

**Why it works:** LLMs naturally flatter a codebase or fixate on whichever file was opened last. A deterministic scan measures every station uniformly, flags silent tool traps (such as backticked `` `@AGENTS.md` `` or retired Codex `approval_policy = "untrusted"`), and applies gating caps honestly.

**Key insights:**
- Run `npx @wondelai/harness-audit --format json` (or `--format terminal`) when shell execution is available; it runs 30 deterministic checks locally with zero runtime dependencies and zero telemetry.
- When running in a restricted or read-only environment without `npx`, execute the exact same 6-station inspection manually using file reads and grep.
- Always separate **repo artifacts** (observable on disk) from **org & workflow practices** (PR review queues, spec-first discipline, revert tracking — captured via `--interview` or 3–5 targeted questions).

**Tool commands:**

| Goal | Command |
| --- | --- |
| Quick terminal scorecard | `npx @wondelai/harness-audit` |
| Machine-readable JSON for agent processing | `npx @wondelai/harness-audit --format json` |
| Standalone shareable HTML report (Schematic style) | `npx @wondelai/harness-audit --format html --out harness-audit.html` |
| Tailored remediation prompt | `npx @wondelai/harness-audit --prompt --out HARNESS-FIX-PROMPT.md` |
| CI quality gate (exits 1 below threshold) | `npx @wondelai/harness-audit --ci --min-score 70 --format json` |
| Safe starter scaffolding (preview first) | `npx @wondelai/harness-audit init --dry-run --tools claude-code,cursor,codex` |

See [references/stations-and-checks.md](references/stations-and-checks.md) when executing the audit manually or interpreting any of the 30 check IDs — contains the complete check catalog, station weights, gating cap rules, and tool-specific failure signatures across Claude Code, Codex, and Cursor.

### 2. Station 1 — Intent: Single Source, Tight Budget, Scoped Rules

**Core concept:** One concise canonical brief (`AGENTS.md`, target ≤ 150 lines) owns project-wide commands and invariants; tool adapters stay paper-thin; directory-specific rules load only when matching paths are touched.

**Why it works:** Verbose instruction files padded with generic advice ("write clean code", "follow best practices") measurably lower agent task success and raise token cost by over 20%. Parallel `AGENTS.md` and `CLAUDE.md` files drift the first time anyone updates a command in only one file.

**Key insights:**
- Codex, Cursor, and GitHub Copilot read root `AGENTS.md` directly. Claude Code loads it via a 1-line `CLAUDE.md` containing a bare `@AGENTS.md` line — never wrap `@AGENTS.md` in backticks or a code fence, or Claude Code treats it as inert text.
- Codex silently truncates project docs past `project_doc_max_bytes` (32 KiB default); keep root `AGENTS.md` crisp and push domain rules down into `.claude/rules/*.md` (with `paths:` YAML frontmatter) and `.cursor/rules/*.mdc` (with `globs:` comma-separated string; plain `.md` files in `.cursor/rules/` are ignored).
- Extract repeatable workflows into skills (`.claude/skills/` or `.agents/skills/`) and commit real standards/spec artifacts (`TESTING.md`, `CODING_STANDARDS.md`, ADRs, PR/issue templates).

### 3. Station 2 — Harness: Permissions, Hooks, MCP & Secret Hygiene

**Core concept:** Move critical boundaries from polite prompt requests into versioned tool configuration, deterministic hooks, clean MCP declarations, and secret ignore/scanning rules.

**Key insights:**
- **Permissions:** Commit `.claude/settings.json` with explicit `permissions.allow` for read-only and verify commands and `permissions.deny` for deploy/production scripts. In `.codex/config.toml`, use `approval_policy = "on-request"` and `sandbox_mode = "workspace-write"` — flag `approval_policy = "untrusted"` as a critical startup error (retired in Codex 0.149.0) and never commit `bypassPermissions`.
- **Hooks:** Wire fast formatting/linting/targeted verification via `.claude/settings.json` hooks, `.cursor/hooks.json`, or `lefthook`/`.husky`. Every Claude Code `Stop` hook MUST inspect `stop_hook_active` from stdin JSON and exit 0 when true so a red suite stops cleanly instead of looping.
- **MCP hygiene:** Claude Code reads root `.mcp.json`, never `.claude/mcp.json`. Flag archived or non-existent npm servers (`@modelcontextprotocol/server-postgres`, `-sqlite`, `-mysql`, `-slack`, `-git`, `-jira`, `-puppeteer`, `-github`), deprecated `/sse` endpoints (migrate to Streamable HTTP `type: "http"`), missing `type: "stdio"` in `.cursor/mcp.json`, and hardcoded `Authorization: Bearer` tokens or API keys (always use `${VAR}` / `${env:VAR}`).
- **Secret hygiene:** Verify `.gitignore` covers `.env`, `.env.local`, `*.pem`, `*.key` (and `.dev.vars` for Cloudflare Workers), commit `.env.example`, scan tracked config/scripts for leaked credentials, and run `gitleaks` or `trufflehog` in CI.

### 4. Station 3 — Loop & Station 4 — Graph: Fast Proof and Parallel Isolation

**Core concept:** Give agents a single fast, reproducible local verification loop (Station 3) and collision-free checkout/port/state isolation when running multiple agents in parallel (Station 4).

**Key insights:**
- Every Level 3–4 loop needs a machine-checkable stop condition: strict static types (`strict: true` in `tsconfig.json`, `pyright`/`mypy`, or native Go/Rust), fast deterministic formatter/linter (`oxlint`, `Biome`, `dprint`, `Ruff`, `golangci-lint`), committed lockfile, pinned runtime version (`.node-version`, `.python-version`, `rust-toolchain.toml`), and exact verify commands mirrored identically in `AGENTS.md` and CI.
- Parallel agents in one working tree overwrite each other's edits and collide on port 3000 or a shared local database. Provide a git worktree helper (plus `.worktreeinclude` for untracked local config), parameterized port env vars, and ephemeral local state (Miniflare, SQLite, Testcontainers, `os.tmpdir()`).
- Document module boundaries (`ARCHITECTURE.md` or a "Read before you touch" table in `AGENTS.md`) and separate planner/builder/reviewer roles under `.claude/agents/` or a `loops.yaml` register before running unattended tasks.

### 5. Station 5 — Verification & Station 6 — Release: Oracles You Can Trust

**Core concept:** Deterministic checks decide whether a change is safe; AI code reviewers advise; the agent must never be able to quietly edit its own grading rubric.

**Why it works:** An agent optimizing for "exit code 0" will occasionally skip a failing test, loosen a type check with `@ts-ignore`, or assert `expect(true).toBe(true)`. Without oracle protection and PR evidence bundles, throughput rises while stability collapses.

**Key insights:**
- **Test quality scan:** Reject `.only()`, empty test bodies, constant-to-constant tautologies (`expect(true).toBe(true)`), mock-echo assertions, and `@ts-ignore` / `eslint-disable` sprawl. Pin observable behavior against hand-computed expected values.
- **Protect the oracle:** Add `.github/CODEOWNERS` covering `tests/`, `.github/`, `AGENTS.md`, and lint/type configs, enable required Code Owner review on protected branches, and fail automated factory branches that modify protected oracle paths.
- **Evidence-driven release:** Run lint, typecheck, and tests on `pull_request` in CI, gate deploy jobs behind verification (`needs: [verify]`), require an evidence checklist in `.github/pull_request_template.md` (commands run, outputs, escalation paths touched, rollback notes), automate patch/minor dependency bumps (Renovate/Dependabot), and wire runtime observability (Sentry, OpenTelemetry, structured logging, healthchecks).

### 6. Execute the Audit & Safe Remediation Protocol

**Core concept:** Audit read-only first, fix blockers in cap-clearing order (secrets & broken configs → CI & verify loop → single-source intent → oracle protection → parallel isolation), and never clobber existing team conventions.

**Protocol:**
1. **Run the scan** (`npx @wondelai/harness-audit --format json` or manual 6-station inspection) plus a qualitative read of `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, and 2–3 real test files.
2. **Present the scored audit** in the fixed format below, highlighting active level caps before individual warnings.
3. **Remediate safely** (only after user confirmation or when explicitly asked to fix):
   - Read every existing instruction/config file end to end and merge surgically — never blindly overwrite.
   - Never touch `~/.claude`, `~/.codex`, `~/.cursor`, `~/.gitconfig`, or live production resources.
   - Verify every new or modified command by executing it in the repo.
4. **Close with the verification ledger:** Re-run `npx @wondelai/harness-audit` and the repo's own verify commands, then print a `Claim | Command | Exit Code & Output` table.

ALWAYS output standalone audits in this format:

```markdown
# Harness Audit: [repo-name]
**Overall Score:** XX/100   **Autonomy Level:** Level X ([Short Name])   **Quick Diagnostic:** N/10
**Uncapped Level:** Level Y (caps: [none | list triggered cap IDs])
**Detected Stack:** [languages, frameworks, package manager, layout]

## Station Scores
| # | Station | Score | Pass / Warn / Fail | Top Blocker |
| --- | --- | --- | --- | --- |

## Blocking & High-Priority Findings
| # | Check ID | Status | Evidence (file / line / metric) | Concrete Fix |
| --- | --- | --- | --- | --- |

## Qualitative Notes (Instructions, Tests, Architecture)
- [2–4 concrete observations from reading the actual files]

## Ordered Remediation Plan
1. [Clear Level caps first, then unlock the next rung]
```

See [references/remediation-workflow.md](references/remediation-workflow.md) when executing fixes or guiding a team up a rung — contains exact safe-merge templates, verified Claude Code / Codex / Cursor configs, `CODEOWNERS` & PR evidence templates, and the full claims-to-output ledger protocol.

## Common Mistakes

| Mistake | Why It Fails | Fix |
| --- | --- | --- |
| Copying project rules into both `AGENTS.md` and `CLAUDE.md` | Rules drift on the first edit; tools silently follow contradictory commands | Keep one `AGENTS.md` (≤ 150 lines) and a thin `CLAUDE.md` with bare `@AGENTS.md` |
| Wrapping `` `@AGENTS.md` `` in backticks in `CLAUDE.md` | Claude Code treats backticked `@` references as plain text and never loads the brief | Put `@AGENTS.md` alone on an unquoted line |
| Leaving retired `approval_policy = "untrusted"` in `.codex/config.toml` | Removed in Codex 0.149.0; Codex fails to start | Replace with `approval_policy = "on-request"` and `sandbox_mode = "workspace-write"` |
| Pasting stale MCP server lists (`server-postgres`, `-sqlite`, `-git`, `/sse`) | Servers fail on startup or don't exist on npm; `/sse` breaks across clients | Use the official MCP Registry (`registry.modelcontextprotocol.io`), Streamable HTTP, and `${VAR}` credentials |
| Writing a Claude `Stop` hook without checking `stop_hook_active` | Failing tests trap the agent in an infinite blocking loop | Read stdin JSON and `exit 0` immediately when `stop_hook_active` is `true` |
| Raising autonomy before protecting tests and CI | Agents weaken assertions or skip tests to hit green exit codes | Add `.github/CODEOWNERS` on `tests/` and `.github/`, scan for `.only()`/tautologies, and require CI on PRs |
| Judging maturity from `AGENTS.md` alone | Beautiful docs with zero CI or leaked secrets produce false Level 4 claims | Enforce honest gating caps and verify every command by running it |

## Quick Diagnostic

| Question | If No | Action |
| --- | --- | --- |
| Does a single canonical root brief (`AGENTS.md`, ≤ 150 lines) exist without duplicated policy in `CLAUDE.md`? | Agents across tools follow stale or conflicting rules and waste context | Consolidate into `AGENTS.md` and reduce `CLAUDE.md` to bare `@AGENTS.md` |
| Are domain-specific rules path-scoped (`.claude/rules/*.md` with `paths:` / `.cursor/rules/*.mdc` with `globs:`)? | Every session pays context overhead for unrelated directories | Split subdirectory invariants into scoped rule files |
| Is there a versioned, valid permission policy (`.claude/settings.json` allow/deny, valid `.codex/config.toml`) with zero bypass defaults? | Agents either prompt endlessly or can invoke destructive/prod commands | Commit explicit allow/deny rules and remove retired or bypass flags |
| Are lifecycle or git hooks configured deterministically (with `stop_hook_active` guarded on any Claude `Stop` hook)? | Critical hygiene rules remain advisory suggestions agents can forget | Wire fast pre-commit or agent hooks and guard `Stop` hooks against loops |
| Are all MCP configs clean (root `.mcp.json`, no archived npm servers, no `/sse`, no hardcoded tokens) and secrets ignored/scanned? | Broken tool startup or credential leaks block safe autonomy | Clean MCP configs, update `.gitignore`, rotate exposed keys, add `gitleaks` |
| Does the repo expose a fast, reproducible verify loop (strict types, linter/formatter, lockfile, runtime pin) matching `AGENTS.md`? | Agents cannot verify their own work reliably before stopping | Add unified `typecheck` + `lint` + `test` + `build` commands and pin lockfile + runtime |
| Can two agents run in parallel without file, port, or local-DB collisions (worktrees + isolated ports/state)? | Multi-agent runs clobber edits and fail on shared ports or DB state | Add worktree tooling/docs, `.env.example` port vars, and ephemeral test state |
| Does a real, non-tautological test suite exist (zero `.only()`, empty tests, `expect(true).toBe(true)`, or `@ts-ignore` sprawl)? | Green test runs provide false confidence and let regressions ship | Delete tautologies, fix `.only()`/skips, pin observable behavior |
| Are tests, CI workflows, and agent rules protected from silent weakening (`CODEOWNERS` / branch rules / CI guard)? | An agent can edit its own oracle to satisfy the stop condition | Add `.github/CODEOWNERS` for `tests/`, `.github/`, and rule files with required review |
| Does PR-triggered CI verify lint, types, and tests, backed by an evidence-oriented PR template and gated deploys? | Unverified code merges on trust and incidents lack rollback clarity | Add PR CI workflow, `.github/pull_request_template.md`, and `needs:`-gated deploy jobs |

## About the Source

This skill adapts the open **AI Developer Toolkit** methodology (6 Software Factory Stations × Autonomy Ladder Levels 0–5) and pairs with the MIT-licensed [`@wondelai/harness-audit`](https://github.com/wondelai/harness-audit) CLI published by Wondel.ai and [developertoolkit.ai](https://developertoolkit.ai/en/ladder/). The Autonomy Ladder's six levels originate from Dan Shapiro's *"The Five Levels: From Spicy Autocomplete to the Dark Factory"* (January 2026); the 6-station architecture, gating caps, and cross-tool verification rules are maintained by Michal Jaskolski / Wondel.ai under the MIT License.

## Further Reading

- [The Autonomy Ladder (Level 0–5)](https://developertoolkit.ai/en/ladder/) and [One Map: Ladder × Lifecycle × Six Stations](https://developertoolkit.ai/en/ladder/one-map/) — Developer Toolkit open canon
- [Agent-Ready Codebase](https://developertoolkit.ai/en/workflows/harness/agent-ready-codebase/) · [Permissions & Sandboxing](https://developertoolkit.ai/en/workflows/harness/permissions-and-sandboxing/) · [Protect the Oracle](https://developertoolkit.ai/en/workflows/test/protect-the-oracle/) · [Evidence Bundle](https://developertoolkit.ai/en/workflows/ship/evidence-bundle/)
- [`@wondelai/harness-audit` CLI](https://github.com/wondelai/harness-audit) — run `npx @wondelai/harness-audit` locally or in CI
- [Dan Shapiro — The Five Levels: From Spicy Autocomplete to the Dark Factory](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/)
- [The AI Engineering Handbook & Role Books (Developer, Tech Lead, CTO)](https://developertoolkit.ai/en/books/)
- [*"Working Effectively with Legacy Code"*](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052?tag=wondelai00-20) by Michael Feathers — characterization tests and seams for building trustworthy test oracles
