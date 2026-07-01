#!/usr/bin/env bash
#
# sync-ide-skills.sh — Sync skill symlinks to IDE compatibility directories.
#
# Discovers all skill directories (those containing SKILL.md) at the repo root
# and creates symlinks in each IDE's skills directory:
#   .claude/skills/  .cursor/skills/  .windsurf/skills/  .pi/skills/
#
# Run this after adding or removing a skill.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

IDE_DIRS=(.claude/skills .cursor/skills .windsurf/skills .pi/skills .agents/skills)

# Discover skills: top-level directories containing SKILL.md
skills=()
for dir in */; do
  dir="${dir%/}"
  [[ -f "$dir/SKILL.md" ]] && skills+=("$dir")
done

if [[ ${#skills[@]} -eq 0 ]]; then
  echo "Error: No skill directories found (expected dirs with SKILL.md at repo root)"
  exit 1
fi

echo "Found ${#skills[@]} skills: ${skills[*]}"
echo ""

errors=0

for ide_dir in "${IDE_DIRS[@]}"; do
  # Clean existing symlinks
  rm -rf "$ide_dir"
  mkdir -p "$ide_dir"

  for skill in "${skills[@]}"; do
    ln -s "../../$skill" "$ide_dir/$skill"
  done

  # Verify symlinks resolve
  broken=$(find "$ide_dir" -maxdepth 1 -type l ! -exec test -e {} \; -print 2>/dev/null || true)
  if [[ -n "$broken" ]]; then
    echo "ERROR: Broken symlinks in $ide_dir:"
    echo "$broken"
    errors=$((errors + 1))
  else
    echo "OK  $ide_dir/ — ${#skills[@]} symlinks"
  fi
done

echo ""
if [[ $errors -gt 0 ]]; then
  echo "FAILED: $errors directory(ies) have broken symlinks"
  exit 1
else
  echo "All ${#skills[@]} skills synced to ${#IDE_DIRS[@]} IDE directories."
fi

# Regenerate the Codex plugin marketplace too (skill set may have changed).
if [[ -x "$REPO_ROOT/scripts/generate-codex-plugins.sh" ]]; then
  echo ""
  "$REPO_ROOT/scripts/generate-codex-plugins.sh"
fi
