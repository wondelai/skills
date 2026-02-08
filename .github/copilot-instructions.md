# Agent Skills Repository Instructions

This repository contains agent skills for Claude Code and agentskills.io-compatible agents.

## Key Requirements

When working with skills in this repository:

- All SKILL.md files must have valid YAML frontmatter with `name`, `description`, `license`, and `metadata` fields.
- The `name` field must be lowercase with hyphens only, max 64 characters, and match the parent directory name exactly.
- The `description` field must be max 1024 characters and include specific trigger phrases for skill discovery.
- Always bump the `metadata.version` when modifying any skill content (MINOR for features, PATCH for fixes).
- Use semantic versioning (x.y.z) for all version numbers.

## Directory Structure

Each skill follows this structure: `{skill-name}/SKILL.md` with optional `references/*.md` for supporting content.

## Compliance

All skills must comply with the OpenAgentSkills specification: https://agentskills.io/specification

## Style

- Write concise, actionable instructions for AI agents.
- Include practical examples and trigger phrases.
- Keep main SKILL.md under 500 lines; move detailed content to reference files.
- Use MIT license for all skills (author: wondelai).

## Marketplace

When adding new skills, update both `README.md` and `.claude-plugin/marketplace.json` to include the skill in an appropriate plugin collection.
