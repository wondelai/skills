#!/usr/bin/env bash
#
# sync-marketplace-versions.sh — align .claude-plugin/marketplace.json versions
# to a single release version (the source of truth for plugin consumers).
#
# Sets the top-level metadata.version AND every plugins[].version to VERSION,
# so that `/plugin install <collection>@wondelai-skills` users are offered the
# refreshed skills after each release.
#
# Usage:
#   scripts/sync-marketplace-versions.sh [VERSION]
#
#   VERSION  e.g. 1.4.0 or v1.4.0 (the leading "v" is stripped).
#            Defaults to the latest git tag (`git describe --tags --abbrev=0`).
#
# Idempotent: re-running with the same version is a no-op. Run automatically by
# .github/workflows/sync-marketplace-version.yml on each published release.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"
MP=".claude-plugin/marketplace.json"

[[ -f "$MP" ]] || { echo "Error: $MP not found" >&2; exit 1; }

ver="${1:-}"
[[ -z "$ver" ]] && ver="$(git describe --tags --abbrev=0 2>/dev/null || true)"
ver="${ver#v}"

if [[ ! "$ver" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: need a semver version. Pass X.Y.Z, or create a vX.Y.Z tag. Got: '${ver:-<empty>}'" >&2
  exit 1
fi

tmp="$(mktemp)"
jq --arg v "$ver" '
  .metadata.version = $v
  | .plugins = (.plugins | map(.version = $v))
' "$MP" > "$tmp" && mv "$tmp" "$MP"

echo "Synced $MP -> version $ver (metadata.version + $(jq '.plugins | length' "$MP") plugin collections)"

# Propagate the version to the generated Codex plugin marketplace.
if [[ -x "$REPO_ROOT/scripts/generate-codex-plugins.sh" ]]; then
  "$REPO_ROOT/scripts/generate-codex-plugins.sh"
fi
