#!/usr/bin/env node
/**
 * Builds .well-known/agent-skills/index.json — the Agent Skills discovery index
 * (https://schemas.agentskills.io/discovery/0.2.0/schema.json) — for one commit.
 *
 *   node scripts/build-agent-skills-index.mjs [<sha>] [--out <file>] [--repo <dir>]
 *
 * <sha> defaults to $AGENT_SKILLS_INDEX_SHA, then HEAD. Every top-level
 * `<dir>/SKILL.md` tracked at that commit becomes one entry. The bytes are read
 * from the commit (`git show <sha>:<path>`), never the working tree, so each
 * digest describes exactly what raw.githubusercontent.com serves at the pinned
 * URL. Output is sorted by name and written deterministically: the same input
 * produces a byte-identical file.
 *
 * Fails loudly on a missing or unparseable `name` or `description`, or a `name`
 * that differs from its directory. No dependencies; plain Node.
 */

import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO = 'wondelai/skills';
const SCHEMA = 'https://schemas.agentskills.io/discovery/0.2.0/schema.json';

/** Removes `--flag value` from args and returns the value, if present. */
function takeOption(args, flag) {
  const index = args.indexOf(flag);
  return index >= 0 ? args.splice(index, 2)[1] : undefined;
}

const args = process.argv.slice(2);
const repoRoot = resolve(takeOption(args, '--repo') ?? resolve(dirname(fileURLToPath(import.meta.url)), '..'));
const out = resolve(repoRoot, takeOption(args, '--out') ?? '.well-known/agent-skills/index.json');
const ref = args[0] ?? process.env.AGENT_SKILLS_INDEX_SHA ?? 'HEAD';

const git = (...gitArgs) => execFileSync('git', ['-C', repoRoot, ...gitArgs], { maxBuffer: 64 * 1024 * 1024 });
const sha = git('rev-parse', '--verify', `${ref}^{commit}`).toString().trim();

/** Unquote a YAML scalar — descriptions are single-quoted, plain, or double-quoted. */
function unquote(value) {
  const trimmed = value.trim();
  if (trimmed.startsWith("'") && trimmed.endsWith("'")) return trimmed.slice(1, -1).replaceAll("''", "'");
  if (trimmed.startsWith('"') && trimmed.endsWith('"')) return trimmed.slice(1, -1).replaceAll('\\"', '"');
  return trimmed;
}

/** One single-line frontmatter field, or a thrown error naming the file. */
function field(frontmatter, key, path) {
  const line = frontmatter.match(new RegExp(`^${key}:[ \\t]*(.*)$`, 'm'));
  const value = line ? unquote(line[1]) : '';
  if (!value || /^[|>][+-]?$/.test(value)) {
    throw new Error(`${path}: frontmatter "${key}" is missing, empty or multi-line (only single-line values are supported).`);
  }
  return value;
}

const paths = git('ls-tree', '-r', '--name-only', sha)
  .toString()
  .split('\n')
  .filter((path) => /^[^/]+\/SKILL\.md$/.test(path));

if (paths.length === 0) throw new Error(`No top-level <dir>/SKILL.md files at ${sha}.`);

const skills = paths.map((path) => {
  const dir = path.split('/')[0];
  const bytes = git('show', `${sha}:${path}`);
  const frontmatter = bytes.toString('utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!frontmatter) throw new Error(`${path}: no YAML frontmatter.`);
  const name = field(frontmatter[1], 'name', path);
  const description = field(frontmatter[1], 'description', path);
  if (name !== dir) throw new Error(`${path}: frontmatter name "${name}" differs from directory "${dir}".`);
  return {
    name,
    type: 'skill-md',
    description,
    url: `https://raw.githubusercontent.com/${REPO}/${sha}/${path}`,
    digest: `sha256:${createHash('sha256').update(bytes).digest('hex')}`,
  };
});

skills.sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0));

mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, `${JSON.stringify({ $schema: SCHEMA, skills }, null, 2)}\n`);
console.log(`${out} — ${skills.length} skills at ${sha.slice(0, 7)}`);
