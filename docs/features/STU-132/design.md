# STU-132 Design

## Metadata

- Linear Issue: STU-132
- Spec: `docs/features/STU-132/spec.md`

## Approach

- **Single skill** (`.cursor/skills/git-worktrees/SKILL.md`) holds Eggscaliber
  worktree guidance; **feature-workflow** links it instead of duplicating long
  sections.
- **Layout:** `.worktrees/<branch-slug>/` at repo root, ignored via `.gitignore`.
- **Setup:** `make setup` from worktree root (same as `AGENTS.md`).
- **Env:** Document per-worktree `.env` vs symlink tradeoffs and port/docker
  collision risks without prescribing a single team-wide env layout.

## Rule updates

- **feature-delivery-workflow** and **branching-and-ticket-linkage** get one
  short paragraph each pointing to the skill so always-on rules stay in sync.

## Risks / mitigations

- **Stash confusion:** Human workflows may forget which directory is active;
  mitigated by opening the worktree as the IDE root and naming branches with
  ticket IDs.
