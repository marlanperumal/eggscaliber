# STU-132 Spec

## Metadata

- Linear Issue: [STU-132](https://linear.app/stunted-chicken-labs/issue/STU-132/document-git-worktrees-in-feature-workflow-and-add-git-worktrees-skill)
- Feature Branch: `STU-132-git-worktrees-workflow`
- Related Design Doc: `docs/features/STU-132/design.md`
- Related Validation Doc: `docs/features/STU-132/validation.md`

## Summary

Make **git worktrees** the default way to implement ticket-linked branches, and
document Eggscaliber-specific setup, environment, and cleanup in a repo skill.

## Problem Statement

The feature workflow described branch creation via checkout in the primary
clone, which conflicts with parallel work and leaves no single place for worktree
conventions (deps, `.env`, ports, removal).

## User Value

- Primary checkout can stay on in-progress work while a ticket ships from an
  isolated directory.
- Agents and developers share one playbook for `uv`/`pnpm`, env files, and
  `git worktree remove`.

## Scope

### In Scope

- `.cursor/skills/git-worktrees/SKILL.md` (new).
- Updates to `.cursor/skills/feature-workflow/SKILL.md`,
  `.cursor/rules/feature-delivery-workflow.mdc`,
  `.cursor/rules/branching-and-ticket-linkage.mdc`.
- `.gitignore` entry for `.worktrees/`.

### Out Of Scope

- CI changes, Docker Compose multi-worktree automation, or Cursor product changes.

## Acceptance Criteria

- Feature workflow preconditions and Phase A describe worktree + `make setup`.
- Rules reference the git-worktrees skill.
- `.worktrees/` is ignored by git.
