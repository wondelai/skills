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

// Agent Skills spec limits. Exceeding one fails the build instead of publishing
// an index that clients reject.
const NAME_PATTERN = /^[a-z0-9-]{1,64}$/;
const MAX_DESCRIPTION = 1024;

/**
 * Parse one single-line YAML scalar, or throw. This is deliberately a subset of
 * YAML: anything it cannot read exactly (a block scalar, an unclosed or folded
 * quote, a double-quoted escape other than \", a trailing comment) is an error
 * rather than a silently truncated value, because the output is published to
 * third parties without review.
 */
function scalar(raw, fail) {
  const value = raw.trim();
  if (value.startsWith("'")) {
    const quoted = value.match(/^'((?:[^']|'')*)'$/);
    if (!quoted) fail('has an unclosed or folded single-quoted value');
    return quoted[1].replaceAll("''", "'");
  }
  if (value.startsWith('"')) {
    const quoted = value.match(/^"((?:[^"\\]|\\")*)"$/);
    if (!quoted) fail('has an unclosed, folded or escaped double-quoted value (only \\" is supported)');
    return quoted[1].replaceAll('\\"', '"');
  }
  if (/^[|>]/.test(value)) fail('is a block scalar (only single-line values are supported)');
  if (/\s#/.test(value)) fail('has a trailing comment or an unquoted " #"; quote the value');
  return value;
}

/** One single-line frontmatter field, or a thrown error naming the file. */
function field(frontmatter, key, path) {
  const fail = (why) => {
    throw new Error(`${path}: frontmatter "${key}" ${why}.`);
  };
  const lines = frontmatter.split(/\r?\n/);
  const index = lines.findIndex((line) => line.startsWith(`${key}:`));
  if (index < 0) fail('is missing');
  // An indented next line is a continuation of a plain or quoted multi-line value.
  if (/^[ \t]+\S/.test(lines[index + 1] ?? '')) fail('continues onto the next line (only single-line values are supported)');
  const value = scalar(lines[index].slice(key.length + 1), fail);
  if (!value) fail('is empty');
  return value;
}

// `ls-tree` lines are "<mode> <type> <object>\t<path>". Only regular files
// (100644/100755) count: a symlinked SKILL.md would be indexed with the digest of
// its link-target string, not the content an agent receives.
const paths = git('ls-tree', '-r', sha)
  .toString()
  .split('\n')
  .map((line) => line.match(/^(\d+) blob [0-9a-f]+\t(.+)$/))
  .filter((match) => match && (match[1] === '100644' || match[1] === '100755'))
  .map((match) => match[2])
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
  if (!NAME_PATTERN.test(name)) throw new Error(`${path}: name "${name}" must match ${NAME_PATTERN}.`);
  if (description.length > MAX_DESCRIPTION) {
    throw new Error(`${path}: description is ${description.length} characters; the limit is ${MAX_DESCRIPTION}.`);
  }
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
