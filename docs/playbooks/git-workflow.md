# Git Workflow

## Branching Policy

- Do all feature and bugfix work on a new branch.
- Prefer a **git worktree** per ticket (see `.cursor/skills/git-worktrees/SKILL.md`)
  so the primary checkout stays usable for other work.
- To pick the next **unblocked** Linear issue (by priority and due date) and
  open a worktree: in **Cursor**, run **`/linear-next`** (repo command under
  `.cursor/commands/linear-next.md`). It uses **Linear MCP** plus shell for
  `git worktree` / `make setup`.
- Branch must be linked to a Linear issue.
- Recommended branch format: `<LINEAR-ID>-<short-description>`.
- Feature branches may be rebased and force-pushed with `--force-with-lease`.
- Never rewrite `master` history.

Examples:

- `ENG-123-metadata-template-reuse`
- `ENG-210-fix-spss-label-parsing`

## Required Sequence Per Ticket

1. Confirm Linear issue has spec, design, and validation doc links.
2. Create feature docs at `docs/features/<TICKET>/spec.md`, `design.md`, and `validation.md`.
3. Create branch from current `master` tip (often via `git worktree add` or
   Cursor **`/linear-next`**).
4. Implement and commit freely on the ticket branch.
5. Rebase on latest `master` before final review.
6. Push and open PR linked to Linear issue.
7. Merge using squash merge (default).
8. Delete feature branch after merge.
9. Do not merge or update `master` without explicit user permission.
10. Complete PR readiness gate in `docs/playbooks/pr-readiness.md` before requesting review.

## Merge Strategy

- Default merge mode: **squash merge**.
- Disable regular merge commits and rebase merges on GitHub repository settings.
- One merged PR should represent one Linear ticket outcome.
- Keep implementation detail in PR conversation and linked docs, not master history noise.

## Stacked PR Policy

- Prefer single PR per ticket by default.
- Allow stacked PRs only when each layer is independently reviewable and testable.
- Limit stack depth to 2-3 open PRs.
- Each stacked PR still requires ticket linkage and full artifact/reconciliation checks.

## Additional Rules To Formalize Early

- Keep PRs small enough for focused review; split oversized work into ticketed slices.
- Require CI green before merge (`pnpm check`, `make lint`, `make test`).
- Require PR template completion and governance checklist.
- Require feature-docs check to pass (hooks + CI).
- Use `--force-with-lease` only on your own feature branch.
- Avoid long-lived branches; rebase frequently during active work.

## As-Built Reconciliation Rule

- If implementation deviates from original spec/design:
  - update spec/design docs in-place for coherence,
  - append a change addendum entry at the bottom with what changed and why,
  - reflect final status in validation doc.
