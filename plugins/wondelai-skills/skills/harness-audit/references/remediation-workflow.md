# Harness Remediation Workflow & Verified Tool Patterns

Use this reference when turning an audit report into concrete, verified repository changes — whether moving a bare Level 0 repository to Level 2 or clearing the Level 3 review ceiling to reach Level 4–5.

---

## 1. Non-Negotiable Safety Rules During Remediation

Apply these six rules on every harness upgrade, whether executed interactively or from a generated `HARNESS-FIX-PROMPT.md`:

1. **Read before merging — never clobber existing team rules.** If `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, `.codex/config.toml`, or `.github/workflows/*` already exist, read the entire file first. Preserve project-specific invariants, custom deny rules, and domain warnings while removing duplication and filler.
2. **Stay strictly inside the repository.** Never modify `~/.claude`, `~/.codex`, `~/.cursor`, `~/.gitconfig`, machine-wide caches, or live cloud/production environments (production databases, worker secrets, remote deploys, live webhooks).
3. **Never write an unverified command.** Before putting any install, lint, typecheck, test, or build command into `AGENTS.md`, a hook, or CI, execute it in the repository and observe its exit code. If a command fails on `main`, report the broken baseline rather than silently documenting a broken stop condition.
4. **Never soften the oracle to get green.** Do not add `.skip()`, `.only()`, `@ts-ignore`, `@ts-nocheck`, `eslint-disable`, or constant tautologies (`expect(true).toBe(true)`) to pass `verification.test-quality-scan` or CI.
5. **Respect context budgets.** Keep root `AGENTS.md` under 150 lines (ideally 50–120 lines). Move file-type or directory-specific guidance into path-scoped rules or local `README.md` pointers.
6. **Do not copy rotting MCP server catalogs.** Point developers to the official MCP Registry (`https://registry.modelcontextprotocol.io/`) and official vendor docs. Always interpolate secrets via `${VAR}` / `${env:VAR}` and verify every configured package exists before committing.

---

## 2. Remediation Sequence: Clear Caps Before Polishing

Fix findings in strict leverage order rather than alphabetically:

### Phase A — Clear Critical Security & Config Caps (Unlocks Level 2 → 3)
1. **Rotate and purge hardcoded credentials** flagged by `harness.secret-hygiene` or `harness.mcp-hygiene`. Update `.gitignore` (`.env`, `.env.local`, `*.pem`, `*.key`, plus `.dev.vars` for Cloudflare Workers) and add `.env.example` with empty or obviously synthetic placeholders.
2. **Fix broken tool configs** flagged by `harness.permissions-policy` and `harness.hooks`:
   - Remove retired Codex `approval_policy = "untrusted"` → replace with `approval_policy = "on-request"`.
   - Remove `bypassPermissions` or `--dangerously-skip-permissions` from repo-level settings.
   - Add `stop_hook_active` loop guard to any Claude Code `Stop` hook.
   - Remove archived/non-existent npm MCP servers (`@modelcontextprotocol/server-postgres`, `-sqlite`, `-mysql`, `-slack`, `-git`, `-jira`, `-puppeteer`, `-github`), move `.claude/mcp.json` to root `.mcp.json`, replace deprecated `/sse` with `type: "http"`, and add `type: "stdio"` to `.cursor/mcp.json` stdio entries.

### Phase B — Establish Canonical Intent & Fast Verify Loop (Unlocks Level 1 → 3)
1. **Consolidate instructions into one `AGENTS.md`** (≤ 150 lines) containing:
   - One-paragraph stack summary and repository shape.
   - Exact verified commands (`install`, `typecheck`, `lint`, `test`, `build`).
   - Non-obvious runtime invariants (things that pass typecheck but fail at runtime).
   - Shared/production resource boundaries ("never run remote deploy or prod DB migrations locally").
   - Short "Read before you touch" pointer table for high-risk subdirectories.
2. **Add a 1-line `CLAUDE.md`** containing bare `@AGENTS.md` (no backticks, no code fence).
3. **Wire unified verify scripts and CI on `pull_request`:** Ensure the exact commands in `AGENTS.md` run inside `.github/workflows/ci.yml` (or `.gitlab-ci.yml`) from a committed lockfile and pinned runtime version (`.node-version`, `.python-version`, `rust-toolchain.toml`, or `mise.toml`).
4. **Move noisy directory rules out of root `AGENTS.md`** into `.claude/rules/*.md` (with `paths:` YAML frontmatter) and `.cursor/rules/*.mdc` (with `globs:` comma-separated frontmatter).

### Phase C — Protect the Oracle & Move to Evidence Review (Unlocks Level 3 → 4)
1. **Clean up test anti-patterns:** Remove every `.only()`, delete empty test stubs, replace tautological assertions with behavioral assertions against hand-computed expected values, and pay down `@ts-ignore` / `eslint-disable` clusters.
2. **Add `.github/CODEOWNERS`** protecting `tests/`, `.github/`, `AGENTS.md`, `CLAUDE.md`, `.claude/`, `.codex/`, `.cursor/`, and lint/type config files — and note for the repository admin to turn on **Require review from Code Owners** in GitHub branch protection / rulesets (a `CODEOWNERS` file alone only requests review).
3. **Add `.github/pull_request_template.md`** requiring a verification evidence table (exact commands + exit codes), a checklist confirming no tests/oracles were weakened, explicit flags for high/critical risk paths (auth, money, schema migrations, secrets, CI/tests), and rollback notes.
4. **Add an advisory PR review layer** (`.cursor/BUGBOT.md`, `.coderabbit.yaml`, or `anthropics/claude-code-action` / `openai/codex-action`) alongside deterministic CI gates — deterministic checks decide mergeability; review agents advise.

### Phase D — Parallel Isolation & Bounded Factory Loops (Unlocks Level 4 → 5)
1. **Enable collision-free worktrees:** Add a worktree script (`bin/wt` or `scripts/worktree.sh`) plus `.worktreeinclude` for untracked local config, and parameterize dev/test server ports via `.env.example` / `.wt-env` so parallel checkouts never fight over one port or database.
2. **Gate deploys and automate low-risk loops:** Separate `verify` and `deploy` jobs in CI (`needs: [verify]`), deny local deploy commands in `.claude/settings.json`, and configure Renovate or Dependabot as the first Level 4–5 loop candidate (small blast radius, minutes-to-surface in CI, revertible in one commit).
3. **Version agent topology and fitness functions:** Commit specialized read-only reviewer or verifier specs under `.claude/agents/`, track recurring loops in `loops.yaml`, and codify architectural budgets (bundle size, dependency boundaries, Lighthouse/SEO, coverage/mutation gates).

---

## 3. Verified Cross-Tool Configuration Snippets

Every key, path, and behavior below has been verified against current Claude Code, OpenAI Codex, and Cursor behavior so remediation never introduces hallucinated config keys.

### Single-Source Instructions (`AGENTS.md` + `CLAUDE.md`)

`CLAUDE.md` (1 line — bare `@AGENTS.md`, never wrapped in backticks):

```markdown
@AGENTS.md
```

Path-scoped Claude Code rule (`.claude/rules/testing.md` — `paths:` ensures it loads only when reading/editing matching files):

```markdown
---
paths:
  - "**/*.test.*"
  - "**/*.spec.*"
  - "tests/**"
---

# Testing Invariants

- Pin observable behavior against hand-computed expected values; delete tautological tests on sight.
- Never commit `.only()` or weaken assertions to satisfy a failing run.
- Keep unit tests deterministic and isolated from shared network or database state.
```

Path-scoped Cursor rule (`.cursor/rules/testing.mdc` — must end in `.mdc`, `globs` is one comma-separated string):

```markdown
---
description: Testing discipline and oracle protection for automated suites
globs: "**/*.test.*,**/*.spec.*,tests/**"
alwaysApply: false
---

# Testing Invariants

- Pin observable behavior against hand-computed expected values; never write tautologies.
- Never commit `.only()` or weaken assertions to satisfy a failing run.
```

### Hardened `.claude/settings.json` (Allow/Deny + Safe Guarded Stop Hook)

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run typecheck)",
      "Bash(npm run lint)",
      "Bash(npm test)",
      "Bash(npm run build)",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Bash(git log *)"
    ],
    "deny": [
      "Bash(npm run deploy)",
      "Bash(npm run deploy:*)",
      "Bash(wrangler deploy*)",
      "Bash(npm publish*)"
    ]
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "sh -c 'INPUT=$(cat); echo \"$INPUT\" | grep -q \"\\\"stop_hook_active\\\":true\" && exit 0; git diff --quiet && exit 0; npm test 2>&1 | tail -n 60 >&2; exit ${PIPESTATUS:-$?}'",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

Why the Stop hook is written this way:
- **Checks `stop_hook_active` first:** Prevents infinite blocking loops when the suite stays red after a retry.
- **Skips when working tree is clean:** A Stop hook fires after every turn, including a Q&A response that edited no files.
- **Sends bounded stderr on failure:** Returning exit code 2 (or wrapping failure into exit 2) shows the tail of the failure output directly to the model so it can fix the root cause instead of guessing. Always test the exact shell snippet on your target shell (POSIX `sh` / `bash`) before committing.

### Valid `.codex/config.toml`

```toml
# Valid values: "on-request", "never" (isolated CI only), or a [granular] table.
# NEVER use "untrusted" — retired in Codex 0.149.0 and rejected at startup.
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

### Clean MCP Configs (`.mcp.json` for Claude Code, `.cursor/mcp.json` for Cursor)

Root `.mcp.json` (Claude Code — NOT `.claude/mcp.json`):

```json
{
  "mcpServers": {
    "docs": {
      "type": "http",
      "url": "https://your-vendor.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${DOCS_MCP_TOKEN}"
      }
    }
  }
}
```

`.cursor/mcp.json` (Cursor — explicit `type: "stdio"` on stdio servers, `${env:VAR}` for env interpolation):

```json
{
  "mcpServers": {
    "shadcn": {
      "type": "stdio",
      "command": "npx",
      "args": ["shadcn@latest", "mcp"]
    }
  }
}
```

### Oracle Protection (`.github/CODEOWNERS`) & Evidence PR Template

`.github/CODEOWNERS`:

```text
# Protect the verification oracle and agent harness from silent weakening
/tests/                  @your-org/platform-leads
/.github/                @your-org/platform-leads
/AGENTS.md               @your-org/platform-leads
/CLAUDE.md               @your-org/platform-leads
/.claude/                @your-org/platform-leads
/.codex/                 @your-org/platform-leads
/.cursor/                @your-org/platform-leads
/tsconfig.json           @your-org/platform-leads
```

`.github/pull_request_template.md`:

```markdown
## Summary
- What changed and why:

## Verification Evidence
| Check | Command | Exit Code / Result |
| --- | --- | --- |
| Typecheck | `...` | 0 |
| Lint | `...` | 0 |
| Tests | `...` | 0 (N passed) |
| Build | `...` | 0 |

## Risk & Escalation Check
- [ ] No existing tests, lint rules, or type checks were weakened or skipped
- [ ] High/Critical paths touched? (auth, payments, schema migrations, secrets, tests, CI — if yes, request code-owner line-by-line review)
- [ ] Rollback notes (required for stateful/migration changes):
```

---

## 4. Required Verification Ledger Protocol

Every harness remediation ends with proof, never prose assurances. After applying changes:

1. Re-run `npx @wondelai/harness-audit` (or your manual checklist) and record the **Score before → after** and **Autonomy Level before → after**.
2. Run every verification command documented in `AGENTS.md` (`typecheck`, `lint`, `test`, `build`) and confirm exit code `0`.
3. Verify `git status` and `git diff --stat` to ensure no stray secrets, temporary artifacts, or unintended edits remain.
4. Present the final ledger:

```markdown
## Verification Ledger
**Harness Audit:** 54/100 (Level 2) → 86/100 (Level 4)

| Claim / Check Fixed | Command Executed | Exit Code & Observed Output |
| --- | --- | --- |
| `intent.single-source` | `npx @wondelai/harness-audit --format json` | `0 — status: pass (AGENTS.md 88 lines, CLAUDE.md 1 line @AGENTS.md)` |
| `harness.permissions-policy` | `npx @wondelai/harness-audit --format json` | `0 — status: pass (on-request + workspace-write)` |
| Local verification loop | `npm run typecheck && npm run lint && npm test` | `0 — 48 passed, 0 lint errors, 0 type errors` |
```

Any claim without an executed command and observed output in this table is treated as unverified and must be marked `TODO(verify)` rather than declared done.
