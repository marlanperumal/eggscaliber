---
name: pre-push-reviewer
description: Run a strict internal review pass before pushing commits. Use when a branch has local changes or new commits and is about to be pushed or opened for review.
---

# Pre-Push Reviewer

## Goal

Catch preventable review feedback before pushing.

## Required Workflow

1. Inspect staged and unstaged diffs plus recent commits.
2. Review against project standards (`AGENTS.md`, playbooks, templates, rules).
3. Identify:
   - critical issues (must-fix before push),
   - important issues (should-fix before push),
   - optional improvements.
4. Verify knock-on consequences:
   - docs and templates updated where behavior/policy changed,
   - config and CI consistency maintained,
   - tests/hooks/check commands still align and are non-redundant.
5. Run required verification commands before push.

## Output Format

- Critical findings:
- Important findings:
- Optional improvements:
- Verification results:
- Push decision: Ready | Blocked

If blocked, include exact fixes required before push.
