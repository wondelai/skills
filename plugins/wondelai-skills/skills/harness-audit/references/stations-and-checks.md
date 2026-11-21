# Six Factory Stations, 30 Checks & Autonomy Ladder Scoring

This reference documents the complete inspection rubric behind `@wondelai/harness-audit` and the `harness-audit` skill. Use it when running an audit manually (without shell access to `npx`), when interpreting a specific check ID in a JSON/HTML report, or when explaining why a repository's Autonomy Level was capped.

---

## 1. The Three Axes and Why Stations Matter

Most team debates about "AI maturity" stall because people mix three different units:

1. **Maturity (Autonomy Ladder, Level 0–5)** — *Who reads what before a change merges?* Measured **per loop** (a repeatable class of change such as dependency bumps, bug fixes, or feature work in a service), never averaged into a vanity number like "Level 3.4".
2. **Risk Class (`low`, `medium`, `high`, `critical`)** — *How costly is a wrong answer on this specific diff?* Risk class caps what any loop may do. Authentication, money movement, schema migrations, secrets, tests, and CI workflows stay human-read even when a repository supports Level 4 or Level 5 loops elsewhere.
3. **Capability (Six Factory Stations)** — *What concrete machinery exists in the repository to steer, constrain, verify, and ship agent work?* This is what `harness-audit` measures deterministically on disk.

| # | Station | Weight | Decision It Owns | Symptom When Missing |
| --- | --- | --- | --- | --- |
| 1 | **Intent** (`intent`) | 20% | What the agent knows before it starts | Plausible code solving the wrong problem or violating local conventions |
| 2 | **Harness** (`harness`) | 18% | What the agent may run, read, and reach | Constant approval friction, broken MCP startups, or leaked secrets / prod touches |
| 3 | **Loop** (`loop`) | 18% | How fast the agent verifies and when it stops | Runs that finish by declaring victory without proof, or burn retries on env drift |
| 4 | **Graph** (`graph`) | 10% | How multiple agents run without colliding | Parallel runs overwriting files, fighting over port 3000, or corrupting local DBs |
| 5 | **Verification** (`verification`) | 20% | What counts as proof the agent cannot fake | Green builds built on `.skip()`, `@ts-ignore`, or tests the agent softened |
| 6 | **Release** (`release`) | 14% | How verified work leaves the repository safely | Review queues choking on diffs nobody can explain a week after merge |

---

## 2. Complete Catalog of the 30 Deterministic Checks

Each check evaluates observable files on disk and assigns one of four statuses:

- `pass` (100% of check weight) — artifact present and free of known failure modes.
- `warn` (50% of check weight) — partially present or carrying non-critical friction.
- `fail` (0% of check weight) — missing critical foundation or active defect found.
- `info` (excluded from station denominator) — neutral observation when a check does not apply to the repository's shape (for example, zero MCP files or a pure CLI library without browser E2E).

### Station 1 — Intent (`intent`, 20% of overall score)

| Check ID | Weight | What It Inspects | Pass / Warn / Fail Criteria |
| --- | --- | --- | --- |
| `intent.instructions-file` | 30 | `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*.mdc`, `.claude/rules/*.md`, `.github/copilot-instructions.md`, `.cursorrules`, `.cursor/rules/*.md` | **Pass** when a supported canonical file exists with no undocumented `.cursorrules` or ignored `.cursor/rules/*.md`. **Warn** if legacy/ignored files coexist. **Fail** if none exist. |
| `intent.single-source` | 20 | Relationship between `AGENTS.md` and `CLAUDE.md` | **Pass** with a single `AGENTS.md`, OR `AGENTS.md` + thin `CLAUDE.md` (≤ 45 lines) containing a bare `@AGENTS.md` line outside backticks and code fences. **Fail** on policy-by-duplication (`CLAUDE.md` > 35 lines without bare `@AGENTS.md`) or backticked `` `@AGENTS.md` `` (which Claude Code silently ignores). **Warn** if only `CLAUDE.md` exists (invisible to Codex/Cursor). |
| `intent.instruction-budget` | 20 | Line count, byte size, and filler phrases in root brief | **Pass** at 5–150 lines, ≤ 32 KiB, and ≤ 1 filler phrase. **Warn** at 151–350 lines or ≥ 2 generic boilerplate hits ("write clean code", "follow best practices", "ensure high quality"). **Fail** at > 350 lines, < 5 lines, or > 32 KiB (Codex's default `project_doc_max_bytes` truncation boundary). |
| `intent.scoped-rules` | 15 | `.claude/rules/*.md` (`paths:` frontmatter), `.cursor/rules/*.mdc` (`globs:`), nested `*/AGENTS.md` | **Pass** when path-scoped rules exist and `.claude/rules/*.md` carry `paths:`. **Warn** in monorepos or ≥ 40-source-file repos with none, or when all `.claude/rules/*.md` omit `paths:` (loading unconditionally on every turn). **Info** in small single repos. |
| `intent.skills-and-specs` | 15 | Project skills (`{.claude,.agents,.cursor}/skills/*/SKILL.md`), PR/issue templates, and spec/standards docs (`TESTING.md`, `CODING_STANDARDS.md`, `DESIGN.md`, `ARCHITECTURE.md`, `docs/adr/`, `docs/specs/`) | **Pass** when ≥ 2 of the 3 categories exist. **Warn** when 1 exists. **Fail** when 0 exist. |

### Station 2 — Harness (`harness`, 18% of overall score)

| Check ID | Weight | What It Inspects | Pass / Warn / Fail Criteria |
| --- | --- | --- | --- |
| `harness.permissions-policy` | 25 | `.claude/settings.json` (`permissions.allow`, `permissions.deny`, `defaultMode`, `sandbox`), `.codex/config.toml` (`approval_policy`, `sandbox_mode`, `default_permissions`), `.cursor/cli.json` | **Critical Fail** if `.codex/config.toml` sets retired `approval_policy = "untrusted"` (removed in Codex 0.149.0 — fails at startup), or if repo config enables `bypassPermissions` / `--dangerously-skip-permissions` / `dangerously-bypass-approvals-and-sandbox`. **Pass** when versioned allow + deny or sandbox/Codex policy exists cleanly. **Warn** if allow-only with no deny/sandbox. **Fail** if no policy exists. |
| `harness.hooks` | 20 | `.claude/settings.json` `hooks`, `.cursor/hooks.json`, `.husky/`, `lefthook.yml`, `.pre-commit-config.yaml`, `.githooks/` | **Fail** if a Claude Code `Stop` hook does not check `stop_hook_active` (inline or in its referenced script), risking an infinite blocking loop on failing suites. **Pass** if valid agent hooks or git hooks exist. **Warn** if neither exists. |
| `harness.mcp-hygiene` | 20 | `.mcp.json`, `.cursor/mcp.json`, `.codex/config.toml` `[mcp_servers.*]`, and misplaced `.claude/mcp.json` | **Info** when no project MCP configs exist (zero false positives). **Critical Fail** if any config references archived/non-existent npm packages (`@modelcontextprotocol/server-postgres`, `-sqlite`, `-mysql`, `-slack`, `-git`, `-jira`, `-puppeteer`, `-github`) or embeds hardcoded `Authorization: Bearer` tokens or plaintext secrets in `env`/`headers`. **Warn** for deprecated `/sse` endpoints (prefer Streamable HTTP `type: "http"`), misplaced `.claude/mcp.json`, or `.cursor/mcp.json` stdio entries missing `type: "stdio"`. **Pass** if clean. |
| `harness.secret-hygiene` | 20 | `.gitignore` patterns, `.env.example`/`.dev.vars.example`, tracked config/script credential scan, CI secret scanner (`gitleaks`, `trufflehog`, `secretlint`) | **Critical Fail** if tracked config/script files contain real-looking API keys, tokens, or private keys (`sk-ant-`, `sk-proj-`, `ghp_`, `github_pat_`, `AKIA...`, `xox...`, `polar_oat_`, `polar_whs_`, `re_...`, `BEGIN PRIVATE KEY`). **Fail** if `.gitignore` omits `.env` (or `.dev.vars` in Cloudflare repos). **Warn** if `.env.local` or `*.pem`/`*.key` are omitted. **Pass** when covered and clean. |
| `harness.sandbox-readiness` | 15 | `.devcontainer/`, `Dockerfile`/`docker-compose*`, `flake.nix`/`shell.nix`, tool sandbox config, production/shared-resource boundary notes in root brief | **Pass** when ≥ 2 signals exist (e.g., container/tool sandbox plus explicit production boundary rules). **Warn** when 1 exists. **Fail** when 0 exist. |

### Station 3 — Loop (`loop`, 18% of overall score)

| Check ID | Weight | What It Inspects | Pass / Warn / Fail Criteria |
| --- | --- | --- | --- |
| `loop.stack-detection` | 10 | Standard manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `Gemfile`, `composer.json`, `*.csproj`) | **Pass** when stack and package manager are deterministically detectable; **Warn** otherwise. |
| `loop.single-command-verify` | 30 | Scripts/targets (`check`, `verify`, `ci`, `test`, `lint`, `typecheck`, `build`) in `package.json`, `Makefile`, `justfile`, and whether `AGENTS.md`/`CLAUDE.md` documents runnable verify commands | **Pass** when a unified `check`/`verify` command (or `test` + `lint`/`typecheck` + `build`) exists and is documented in the root brief. **Warn** if partial or undocumented in the brief. **Fail** if missing. |
| `loop.static-types` | 25 | `tsconfig.json` (`strict: true` or strict `extends`), Python `mypy`/`pyright`/`basedpyright`/`ty`, PHPStan/Psalm, Sorbet/Steep, native Go/Rust/Java/Kotlin/C#/Swift | **Pass** on strict typechecking or statically typed native languages. **Warn** on non-strict `tsconfig.json` or untyped Python/PHP/Ruby. **Fail** on untyped JS without TypeScript. **Info** when no app language is present. |
| `loop.formatter-linter` | 20 | `Biome`, `oxlint`, `dprint`, `ESLint`, `Prettier`, `vite-plus`, `Ruff`, `Black`, `golangci-lint`, `rustfmt`/`clippy`, `RuboCop`, `gofmt`/`go vet` | **Pass** when deterministic formatting/linting is configured. **Fail** when absent. |
| `loop.lockfile-reproducibility` | 15 | Committed lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`, `uv.lock`, `poetry.lock`, `Cargo.lock`, `go.sum`, etc.) AND runtime pin (`.node-version`, `.nvmrc`, `engines.node`, `.python-version`, `rust-toolchain.toml`, `.tool-versions`, `mise.toml`, `go.mod`) | **Pass** when both lockfile and runtime pin exist. **Warn** when only one exists. **Fail** when neither exists. |

### Station 4 — Graph (`graph`, 10% of overall score)

| Check ID | Weight | What It Inspects | Pass / Warn / Fail Criteria |
| --- | --- | --- | --- |
| `graph.worktree-isolation` | 35 | Worktree scripts (`bin/wt`, `scripts/wt*`), `.worktreeinclude`, package scripts, or worktree guidance in root brief | **Pass** with committed worktree tooling/config. **Warn** if only prose-documented. **Fail** if absent. |
| `graph.port-and-state-isolation` | 35 | Configurable `PORT` variables in `.env.example`/`.wt-env` and ephemeral local state (Miniflare, Docker, SQLite, Testcontainers, `tmpdir`) | **Pass** when ports and/or ephemeral state are isolated. **Info** for pure CLI/libraries without dev server ports. **Warn** for web/API apps with hardcoded shared ports/state. |
| `graph.subagent-definitions` | 20 | `.claude/agents/*.md`, `.cursor/agents/*.md`, `.codex/agents/*.md`, `.factory/`, `loops.yaml`, `docs/agents/` | **Pass** when versioned agent/loop specs exist. **Warn** if only agent workflow docs exist. **Info** otherwise (optional below Level 4). |
| `graph.workspace-boundaries` | 10 | `pnpm-workspace.yaml`, `package.json` `workspaces`, `Cargo.toml` `[workspace]`, `turbo.json`, `nx.json`, `go.work`, `ARCHITECTURE.md`, or module boundary table in `AGENTS.md` | **Pass** when explicit boundaries exist. **Fail** in a monorepo without them. **Warn** in a single repo without them. |

### Station 5 — Verification (`verification`, 20% of overall score)

| Check ID | Weight | What It Inspects | Pass / Warn / Fail Criteria |
| --- | --- | --- | --- |
| `verification.unit-tests` | 25 | Test file count vs source file count across JS/TS, Python, Go, Rust, Java, Ruby, PHP, C# conventions | **Pass** at ≥ 3 test files with ≥ 12% ratio (or ≥ 15 test files, or ≥ 2 tests in tiny ≤ 10-file repos). **Warn** if minimal (1–2 files). **Fail** if 0 test files. |
| `verification.e2e-tests` | 15 | Playwright, Cypress, Cloudflare Workers Vitest pool, Supertest/httpx, `e2e/` or `integration/` suites | **Pass** when present. **Warn** on web/API frameworks without any E2E/runtime contract suite. **Info** on pure libraries/CLIs. |
| `verification.oracle-protection` | 20 | `CODEOWNERS` covering `tests/`, `.github/`, or rule files; `.claude/settings.json` edit deny rules on tests/CI; CI protected-path guards | **Pass** when tests or CI paths are explicitly protected. **Warn** if `CODEOWNERS` exists but does not cover tests/CI. **Fail** when unprotected. |
| `verification.test-quality-scan` | 20 | Static scan of up to 150 test files and 250 source files for `.only()`, excessive `.skip()`, empty test blocks, constant-to-constant tautologies (`expect(true).toBe(true)`, `assert True`), and `@ts-ignore`/`@ts-nocheck`/`eslint-disable` sprawl | **Fail** on zero tests, any `.only()`, any constant tautology, ≥ 2 empty test blocks, or ≥ 15 `@ts-ignore`/`@ts-nocheck` directives. **Warn** on ≥ 5 skipped tests, 1 empty test, ≥ 5 `@ts-ignore`, or suppression density > 35%. **Pass** when clean. |
| `verification.automated-pr-review` | 10 | `.cursor/BUGBOT.md`, `.coderabbit.yaml`, `claude-code-action` / `codex-action` review workflows, Danger/reviewdog | **Pass** when configured; **Warn** when absent. |
| `verification.fitness-functions` | 10 | Lighthouse CI, `dependency-cruiser`, `size-limit`, Stryker mutation config, coverage thresholds, SEO/link/budget audit scripts | **Pass** when ≥ 1 automated fitness function exists; **Warn** when none exist. |

### Station 6 — Release (`release`, 14% of overall score)

| Check ID | Weight | What It Inspects | Pass / Warn / Fail Criteria |
| --- | --- | --- | --- |
| `release.ci-pipeline` | 35 | `.github/workflows/*.yml`, `.gitlab-ci.yml`, `.circleci/config.yml`, Azure/Buildkite/Jenkins checking PR trigger + tests + lint/typecheck | **Pass** when CI runs on `pull_request`/`merge_request` with tests AND lint or typecheck. **Warn** when partial (e.g., push-only or missing tests). **Fail** when absent. |
| `release.evidence-pr-template` | 20 | `.github/pull_request_template.md` / `PULL_REQUEST_TEMPLATE/*.md` / GitLab MR templates for checklist + verification/evidence/risk terms | **Pass** with both checklist items and verification/risk prompts. **Warn** if template exists without checklist/evidence cues. **Fail** if missing. |
| `release.dependency-automation` | 15 | `renovate.json`, `.renovaterc*`, `.github/dependabot.yml` | **Pass** when configured; **Warn** when absent. |
| `release.observability-and-safety` | 15 | Sentry, OpenTelemetry, PostHog, Pino/Winston/structlog, Drizzle/Prisma/Alembic `migrations/`, healthcheck endpoints, `CHANGELOG.md` | **Pass** when present. **Warn** on deployed apps without telemetry or migration discipline. **Info** on small libraries/CLIs. |
| `release.deploy-safety` | 15 | Deploy workflows gated with `needs:` / `environment:` / branch condition, and/or `.claude/settings.json` denying local agent deploy/prod commands | **Pass** when deploy workflows are gated or local deploys are denied. **Warn** when an ungated deploy workflow exists. **Info** when no deploy workflow exists. |

---

## 3. Scoring Math and Honest Gating Caps

1. **Per-station score (0–100):** `round((sum(pass weights) + 0.5 * sum(warn weights)) / sum(non-info weights) * 100)`.
2. **Overall score (0–100):** Weighted average of the 6 stations (`0.20*Intent + 0.18*Harness + 0.18*Loop + 0.10*Graph + 0.20*Verification + 0.14*Release`).
3. **Raw Autonomy Level:** `<25 → L0`, `25–44 → L1`, `45–62 → L2`, `63–77 → L3`, `78–89 → L4`, `90–100 → L5`.
4. **Gating Caps (applied after raw level, always reported explicitly):**
   - **Cap to L1:** `intent.instructions-file === fail` AND `loop.single-command-verify === fail`.
   - **Cap to L2 (verification/CI):** `verification.unit-tests === fail` OR `release.ci-pipeline === fail`.
   - **Cap to L2 (harness security/config):** Hardcoded secret found (`harness.secret-hygiene` or `harness.mcp-hygiene`) OR critical permission error (retired Codex `approval_policy = "untrusted"` or `bypassPermissions`).
   - **Cap to L3:** `verification.score < 70` OR `loop.score < 70` OR `release.ci-pipeline !== pass` OR `verification.test-quality-scan === fail`.
   - **Cap to L4:** `verification.oracle-protection !== pass` OR `graph.score < 70` OR `harness.score < 75` OR `verification.score < 85` OR `release.score < 80`.

---

## 4. Qualitative Audit Pass (What Static Checks Cannot See)

After the 30 deterministic checks, inspect three qualitative dimensions that require engineering judgment (this is what `--deep` automates or what you perform directly during a skill-driven audit):

1. **Instruction contradiction & staleness:** Read `AGENTS.md` alongside `package.json`/`Makefile` and CI workflows. Do documented commands still exist and match CI? Are there stale references to removed directories, old package managers, or retired flags?
2. **Real test strength vs mock theater:** Open 2–3 representative test files. Do tests call real business logic and pin hand-computed outputs, or do they mock the module under test and assert that the mock was called with the arguments the test just constructed? Would breaking an `if` condition or off-by-one boundary actually make a test go red?
3. **Architectural legibility:** Can a fresh agent locate the entry points, data layer, auth boundary, and side-effecting boundaries in under three file reads? If critical runtime constraints (like Cloudflare D1 rejecting `Date` bindings or generated files overwritten on build) live only in Slack or tribal memory, record them as missing invariants for `AGENTS.md` or scoped rules.

---

## 5. Org & Workflow Dimensions Invisible on Disk

A clean repository does not guarantee clean delivery if the team process breaks around it. When auditing for a Tech Lead or CTO (or running `--interview --role dev|lead|cto`), evaluate seven organizational dimensions:

1. **Daily adoption consistency:** Shared team harness vs isolated personal prompts.
2. **PR review queue health:** Evidence-bundle review for low/medium risk vs drowning in line-by-line diffs or rubber-stamping.
3. **Spec-first discipline:** Acceptance criteria and stop conditions committed before generation vs one-line prompts.
4. **Paired metrics (throughput + stability):** Tracking AI spend/velocity alongside change failure rate, revert rate, and review wait (guarding against DORA/Faros acceleration whiplash).
5. **Incident-to-harness feedback loop:** Every agent-caused bug adds a regression test, lint rule, or harness constraint.
6. **Senior/Staff ownership:** Senior engineers designing invariants and oracles instead of burning out cleaning up unchecked diffs.
7. **Enforced risk boundaries:** Explicit escalation rules for auth, payments, migrations, secrets, and CI/tests backed by `CODEOWNERS` and branch protection.
