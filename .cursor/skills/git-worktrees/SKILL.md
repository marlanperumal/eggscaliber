---
name: git-worktrees
description: >-
  Git worktrees for this monorepo: .worktrees layout, make setup (uv/pnpm),
  env and ports, Cursor workspace, cleanup. Use for parallel ticket branches
  or after **`/linear-next`** in Cursor.
---

# Git worktrees (Eggscaliber)

## When to use

- Parallel tickets without constant `git checkout`.
- **`/linear-next`** in Cursor creates a worktree when you run that command.
- Otherwise follow **Phase A** in `.cursor/skills/feature-workflow/SKILL.md`.

**Layout:** `.worktrees/<branch-slug>/` at the repo root (ignored in `.gitignore`).

## Create

From the **primary** clone:

```bash
git fetch origin
git worktree add .worktrees/<TICKET>-short-name -b <TICKET>-short-name origin/master
cd .worktrees/<TICKET>-short-name
make setup
```

Confirm the default base branch with `gh repo view --json defaultBranchRef` if it
is not `master`.

## Env, ports, Docker

- `.env` / `.env.*` are gitignored; use a **per-worktree** `.env` or a symlink to
  your main clone if you accept shared secrets.
- Multiple worktrees running **the same ports** or **docker compose** project
  will conflict—use different ports or one active stack at a time.

## Python / Node

- `make setup` runs `uv sync --project apps/api` and `pnpm install`; virtualenv
  lives under `apps/api/.venv` in **this** checkout.

## Cleanup

```bash
git worktree remove /path/to/repo/.worktrees/<branch-slug>
git worktree prune
```

## Related

- **Pick next ticket:** **`/linear-next`** (`.cursor/commands/linear-next.md`).
- **Delivery:** `.cursor/skills/feature-workflow/SKILL.md`.
