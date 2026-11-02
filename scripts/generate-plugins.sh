#!/usr/bin/env bash
#
# generate-plugins.sh — mirror the Claude plugin marketplace into the OpenAI
# Codex plugin standard AND the Agent Plugins standard (agent-plugins.org),
# so Codex users and any Agent Plugins-conforming client get the same
# collections.
#
# SINGLE SOURCE OF TRUTH: .claude-plugin/marketplace.json (collections, skill
# membership, versions, metadata). This script regenerates, from it:
#
#   plugins/<collection>/.codex-plugin/plugin.json   # Codex plugin manifest
#   plugins/<collection>/plugin.json                 # Agent Plugins v1.0.0 manifest
#   plugins/<collection>/skills/<skill>              # real COPIES of repo-root skills
#   plugins/wondelai-skills/                         # all-in-one Agent Plugin (every skill;
#                                                    #   no .codex-plugin/, not in the Codex marketplace)
#   .agents/plugins/marketplace.json                 # Codex marketplace (collections only)
#
# Skills are copied, not symlinked: the Agent Plugins spec requires every
# package path to resolve inside the plugin root, so out-of-root symlinks
# would be skipped by conforming clients. Re-run this script after editing
# any skill so the copies don't go stale.
#
# Codex resolves a marketplace entry's source.path relative to the REPO ROOT
# (not the .agents/plugins/ dir), so plugin dirs live at repo-root plugins/ —
# matching real-world multi-harness marketplaces. See:
#   https://developers.openai.com/codex/plugins/build
#   https://agent-plugins.org/
#
# Fully generated and idempotent: safe to re-run. Invoked by
# scripts/sync-ide-skills.sh (skill set or content changed) and
# scripts/sync-marketplace-versions.sh (version changed) so the generated
# plugins always track the Claude side.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

SRC=".claude-plugin/marketplace.json"
PLUGINS_DIR="plugins"
MP_DIR=".agents/plugins"
MP="$MP_DIR/marketplace.json"
AP_SCHEMA="https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
BUNDLE_NAME="wondelai-skills"

[[ -f "$SRC" ]] || { echo "Error: $SRC not found (run from the skills repo root)" >&2; exit 1; }
command -v jq >/dev/null || { echo "Error: jq is required" >&2; exit 1; }

# The all-in-one bundle shares the plugins/ namespace with the collections.
jq -e --arg b "$BUNDLE_NAME" '[.plugins[].name] | index($b) == null' "$SRC" >/dev/null \
  || { echo "Error: a collection is named '$BUNDLE_NAME' — clashes with the bundle dir" >&2; exit 1; }

# This script fully owns these generated paths (the bundle lives under plugins/ too).
rm -rf "$PLUGINS_DIR" "$MP_DIR"
mkdir -p "$PLUGINS_DIR" "$MP_DIR"

# 1) Codex marketplace manifest — one entry per Claude collection (bundle excluded).
jq '{
  name: .name,
  interface: { displayName: "Wondel.ai Skills" },
  plugins: [ .plugins[] | {
    name: .name,
    source: { source: "local", path: ("./plugins/" + .name) },
    policy: { installation: "AVAILABLE", authentication: "ON_USE" },
    category: (.category // "Coding")
  } ]
}' "$SRC" > "$MP"

# 2) One dual-format plugin dir per collection:
#    Codex manifest + Agent Plugins manifest + skill copies.
count="$(jq '.plugins | length' "$SRC")"
total_copies=0
for i in $(seq 0 $((count - 1))); do
  name="$(jq -r ".plugins[$i].name" "$SRC")"
  pdir="$PLUGINS_DIR/$name"
  mkdir -p "$pdir/.codex-plugin" "$pdir/skills"

  # Reuse the collection's Claude metadata; point skills at the bundled dir.
  jq ".plugins[$i]
      | {name, version, description, license, keywords, repository, homepage}
      + {skills: \"./skills/\"}
      | with_entries(select(.value != null))" "$SRC" > "$pdir/.codex-plugin/plugin.json"

  # Agent Plugins v1.0.0 manifest — skills are discovered under skills/, so the
  # schema (additionalProperties: false) allows no skills/category/source keys.
  jq --argjson i "$i" --arg s "$AP_SCHEMA" '.plugins[$i]
      | { "$schema": $s, name, version, description, author,
          homepage, repository, license, keywords }
      | with_entries(select(.value != null))' "$SRC" > "$pdir/plugin.json"

  # Copy each member skill from its repo-root dir (spec: no out-of-root symlinks).
  while IFS= read -r sk; do
    sk="${sk#./}"; sk="${sk%/}"   # no trailing slash: BSD cp -R src/ copies contents, not the dir
    if [[ ! -f "$sk/SKILL.md" ]]; then
      echo "  warn: skill '$sk' (collection $name) has no SKILL.md — skipping" >&2
      continue
    fi
    cp -R "$sk" "$pdir/skills/$sk"
    total_copies=$((total_copies + 1))
  done < <(jq -r ".plugins[$i].skills[]" "$SRC")
done

# 3) All-in-one Agent Plugin: every unique skill across all collections.
bdir="$PLUGINS_DIR/$BUNDLE_NAME"
mkdir -p "$bdir/skills"

jq --arg s "$AP_SCHEMA" --arg n "$BUNDLE_NAME" '
  { "$schema": $s,
    name: $n,
    version: .metadata.version,
    description: .description,
    author: (.owner + {url: "https://wondel.ai"}),
    homepage: "https://github.com/wondelai/skills",
    repository: "https://github.com/wondelai/skills",
    license: "MIT" }
  | with_entries(select(.value != null))' "$SRC" > "$bdir/plugin.json"

bundle_copies=0
while IFS= read -r sk; do
  sk="${sk#./}"; sk="${sk%/}"
  if [[ ! -f "$sk/SKILL.md" ]]; then
    echo "  warn: skill '$sk' (bundle $BUNDLE_NAME) has no SKILL.md — skipping" >&2
    continue
  fi
  cp -R "$sk" "$bdir/skills/$sk"
  bundle_copies=$((bundle_copies + 1))
done < <(jq -r '[.plugins[].skills[]] | unique | .[]' "$SRC")

# Copies must ship clean — strip Finder droppings picked up from source dirs.
find "$PLUGINS_DIR" -name '.DS_Store' -type f -delete

# 4) Validate: well-formed JSON, zero symlinks anywhere in the generated tree,
#    and every bundled skill has a regular-file SKILL.md.
jq -e . "$MP" >/dev/null || { echo "Error: generated $MP is invalid JSON" >&2; exit 1; }
for pj in "$PLUGINS_DIR"/*/.codex-plugin/plugin.json "$PLUGINS_DIR"/*/plugin.json; do
  jq -e . "$pj" >/dev/null || { echo "Error: invalid JSON: $pj" >&2; exit 1; }
done
links="$(find "$PLUGINS_DIR" -type l -print 2>/dev/null || true)"
[[ -z "$links" ]] || { echo "Error: symlinks in generated tree (Agent Plugins spec requires real files):" >&2; echo "$links" >&2; exit 1; }
for sd in "$PLUGINS_DIR"/*/skills/*/; do
  [[ -f "${sd}SKILL.md" ]] || { echo "Error: missing SKILL.md in $sd" >&2; exit 1; }
done

echo "Generated $count dual-format plugins ($total_copies skill copies) + $BUNDLE_NAME bundle ($bundle_copies skills) + $MP"
