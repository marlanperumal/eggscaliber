---
name: git-worktrees
description: >-
  Best practices for git worktrees in this monorepo: where to create them,
  dependency install (uv, pnpm), env and secrets, port conflicts, Cursor
  workspace, and safe cleanup. Use when starting parallel feature branches,
  isolating a ticket from the main checkout, or tearing down a worktree.
---

# Git worktrees (Eggscaliber)

## When to use

- **Parallel tickets** without stashing or constant `git checkout`.
- **Clean isolation** so the main clone stays on `master` (or another branch)
  while feature work happens in a dedicated directory.
- **Agent or human** implementing a Linear-linked branch per
  `.cursor/skills/feature-workflow/SKILL.md`.

**Default:** create a **linked worktree** under **`.worktrees/<branch-slug>/`**
at the repository root (same machine, same object database as your primary
clone).

## Location and gitignore

1. Prefer **`.worktrees/`** at the repo root (already listed in `.gitignore`).
2. Before creating a **new** ignore pattern elsewhere, verify it is ignored:

   ```bash
   git check-ignore -q .worktrees && echo "ok"
   ```

3. Do **not** commit worktree paths or put worktrees inside tracked directories
   without ignoring them.

If you use a different root (e.g. global path under `~`), keep it **outside**
the repo so nothing under that tree can be mistaken for the main worktree.

## Create a worktree for a feature branch

Run from your **primary** clone's **repository root** so the relative path
`.worktrees/...` is created next to the root `Makefile` / `package.json`, not
under some nested folder.

```bash
git fetch origin
```

**New branch** (typical for a ticket):

```bash
git worktree add .worktrees/<TICKET>-short-name -b <TICKET>-short-name origin/<base>
```

Replace **`<base>`** with your default branch name (often `master`). Use the same
branch naming as the feature workflow (e.g. `STU-117-architecture-slice`).
Confirm with `gh repo view --json defaultBranchRef` if unsure.

**Existing branch** (branch already exists locally):

```bash
git worktree add .worktrees/<TICKET>-short-name <TICKET>-short-name
```

Then work **only** from that directory for that ticket:

```bash
cd .worktrees/<TICKET>-short-name
```

## Install and link packages (monorepo)

All commands below assume **current working directory is the worktree root**
(the directory that contains `Makefile`, `package.json`, `apps/`, etc.).

```bash
make setup
```

This matches root-run expectations in `AGENTS.md`: **`uv sync --project apps/api`**
and **`pnpm install`**.

- **Python:** `uv sync --project apps/api` creates a **local** virtualenv under
  `apps/api/.venv` (gitignored). Each worktree has its **own** environment—do not
  assume sharing with the primary clone unless you intentionally override uv’s
  environment location (not recommended for isolation).
- **Node:** `pnpm` installs **workspace** `node_modules` under this checkout
  (root + packages). Each worktree has its **own** `node_modules` trees.

After setup, run **`make check`** (or the same commands as the feature workflow)
from **this** worktree root.

## Environment variables and secrets

- **`.env` and `.env.*` are gitignored** (see root `.gitignore`). Never commit
  them.
- **Per worktree:** copy or create a `.env` in the **worktree root** (or paths
  your apps load from) so each checkout has explicit configuration.
- **Symlink to primary clone’s `.env`:** acceptable for **one-machine** dev if
  you want a single secrets file; you then **share** secrets and edits across
  worktrees—avoid if branches need different values (e.g. different API URLs).
- **Docker Compose:** if multiple worktrees run **`docker compose`** against the
  same project name and ports, they **collide**. Options: run compose from only
  one checkout at a time, set distinct **`COMPOSE_PROJECT_NAME`** (and/or **ports**)
  per worktree via env (e.g. in a worktree-local `.env`), or stop stacks before
  switching.

Document any branch-specific env in the ticket or `docs/features/<TICKET>/`
artifacts, not in git-tracked secret files.

## Ports and parallel dev servers

Running **`make dev`**, **`make api`**, or **`pnpm --filter @eggscaliber/web dev`**
from **two** worktrees at once will usually **conflict** on the same host ports
(e.g. API `8000`, Vite default). For parallel runs, override ports via env vars
supported by your stack (set in that worktree’s environment or `.env`), or run
only one stack at a time.

## Cursor / IDE workspace

- Open the **worktree folder** as the workspace root when doing focused
  implementation so search, terminals, and file paths align with **`git status`**
  for that branch.
- If the agent should continue from the worktree, use **move workspace to the
  worktree root** (see Cursor app-control MCP `move_agent_to_root`) after the
  worktree exists.

## Cleanup

When the branch is merged or the worktree is no longer needed:

1. Stop dev servers and **docker** stacks started from this worktree.
2. From your **primary** clone: **`cd`** to the **repository root** if you are
   not already there. If your shell is **inside** the worktree you are removing,
   move out first—Git refuses to remove the worktree that is your current working
   directory.

   ```bash
   # From primary clone root (not inside .worktrees/<branch-slug>)
   git worktree remove .worktrees/<branch-slug>
   ```

   Paths are relative to the repository root. Use an absolute path only when you
   are not at the root and need an explicit location.

   If Git refuses because of uncommitted changes, either commit/stash or, only
   if you accept losing untracked state, use **`--force`** (destructive).

3. Prune stale metadata:

   ```bash
   git worktree prune
   ```

4. Delete the local branch when appropriate (after merge). With **squash** merges
   (per `AGENTS.md`), `git branch -d` often reports “not fully merged” because the
   tip commit is not on `master`; use **`git branch -D <branch-name>`** to drop the
   local branch anyway, or delete the branch via **`gh pr merge`** when your flow
   uses **`--delete-branch`**.

   ```bash
   git branch -d <branch-name>   # ok when branch is merged as a merge commit
   # git branch -D <branch-name> # after squash merge to default branch, if -d refuses
   ```

5. **Do not** manually `rm -rf` the worktree directory before
   **`git worktree remove`** unless you know the worktree is already detached;
   prefer **`git worktree remove`** to keep Git’s bookkeeping consistent.

## Quick reference

| Concern | Guidance |
|--------|----------|
| Location | `.worktrees/<branch-slug>/` at repo root |
| Ignore | `.worktrees/` in `.gitignore`; verify with `git check-ignore` |
| Deps | `make setup` from worktree root |
| Verify | `make check` from same root |
| Env | Per-worktree `.env` or symlink; never commit |
| Ports / Docker | One active stack or distinct ports/project names |
| Done | `git worktree remove` → `git worktree prune` → optional `git branch -d` / `-D` if squash-merged |

## Related

- Feature delivery steps: `.cursor/skills/feature-workflow/SKILL.md`
- General worktree patterns (directory choice, safety): superpowers
  **using-git-worktrees** skill in your global plugin cache, if available.
