#!/usr/bin/env bash
#
# generate-codex-plugins.sh — mirror the Claude plugin marketplace into the
# OpenAI Codex plugin standard, so Codex users get the same collections.
#
# SINGLE SOURCE OF TRUTH: .claude-plugin/marketplace.json (collections, skill
# membership, versions, metadata). This script regenerates, from it:
#
#   plugins/<collection>/.codex-plugin/plugin.json   # Codex plugin manifest
#   plugins/<collection>/skills/<skill>              # symlinks -> repo-root skills
#   .agents/plugins/marketplace.json                 # Codex marketplace
#
# Codex resolves a marketplace entry's source.path relative to the REPO ROOT
# (not the .agents/plugins/ dir), so plugin dirs live at repo-root plugins/ —
# matching real-world multi-harness marketplaces. See:
#   https://developers.openai.com/codex/plugins/build
#
# Fully generated and idempotent: safe to re-run. Invoked by
# scripts/sync-ide-skills.sh (skill set changed) and
# scripts/sync-marketplace-versions.sh (version changed) so the Codex side
# always tracks the Claude side.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

SRC=".claude-plugin/marketplace.json"
PLUGINS_DIR="plugins"
MP_DIR=".agents/plugins"
MP="$MP_DIR/marketplace.json"

[[ -f "$SRC" ]] || { echo "Error: $SRC not found (run from the skills repo root)" >&2; exit 1; }
command -v jq >/dev/null || { echo "Error: jq is required" >&2; exit 1; }

# This script fully owns these generated paths.
rm -rf "$PLUGINS_DIR" "$MP_DIR"
mkdir -p "$PLUGINS_DIR" "$MP_DIR"

# 1) Codex marketplace manifest — one entry per Claude collection.
jq '{
  name: .name,
  interface: { displayName: "Wondel.ai Skills" },
  plugins: [ .plugins[] | {
    name: .name,
    source: { source: "local", path: ("./plugins/" + .name) },
    policy: { installation: "AVAILABLE", authentication: "ON_FIRST_USE" },
    category: (.category // "Coding")
  } ]
}' "$SRC" > "$MP"

# 2) One Codex plugin per collection: manifest + skill symlinks.
count="$(jq '.plugins | length' "$SRC")"
total_links=0
for i in $(seq 0 $((count - 1))); do
  name="$(jq -r ".plugins[$i].name" "$SRC")"
  pdir="$PLUGINS_DIR/$name"
  mkdir -p "$pdir/.codex-plugin" "$pdir/skills"

  # Reuse the collection's Claude metadata; point skills at the bundled dir.
  jq ".plugins[$i]
      | {name, version, description, license, keywords, repository, homepage}
      + {skills: \"./skills/\"}
      | with_entries(select(.value != null))" "$SRC" > "$pdir/.codex-plugin/plugin.json"

  # Symlink each member skill to its repo-root dir (plugins/<name>/skills/ is 3 deep).
  while IFS= read -r sk; do
    sk="${sk#./}"
    if [[ ! -f "$sk/SKILL.md" ]]; then
      echo "  warn: skill '$sk' (collection $name) has no SKILL.md — skipping" >&2
      continue
    fi
    ln -s "../../../$sk" "$pdir/skills/$sk"
    total_links=$((total_links + 1))
  done < <(jq -r ".plugins[$i].skills[]" "$SRC")
done

# 3) Validate: well-formed JSON + no broken symlinks.
jq -e . "$MP" >/dev/null || { echo "Error: generated $MP is invalid JSON" >&2; exit 1; }
for pj in "$PLUGINS_DIR"/*/.codex-plugin/plugin.json; do
  jq -e . "$pj" >/dev/null || { echo "Error: invalid JSON: $pj" >&2; exit 1; }
done
broken="$(find "$PLUGINS_DIR" -type l ! -exec test -e {} \; -print 2>/dev/null || true)"
[[ -z "$broken" ]] || { echo "Error: broken symlinks:" >&2; echo "$broken" >&2; exit 1; }

echo "Generated $count Codex plugins ($total_links skill links) + $MP"
