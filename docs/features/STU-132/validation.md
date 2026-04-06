# STU-132 Validation

## Metadata

- Linear Issue: STU-132
- Spec: `docs/features/STU-132/spec.md`

## Automated

- `make check` passes on the feature branch after changes land.

## Manual

- [ ] From a clean `origin/master` state, `git worktree add .worktrees/_validate-stu-132 -b _validate-stu-132 origin/master` succeeds.
- [ ] `git check-ignore -q .worktrees` exits 0 (directory ignored).
- [ ] In that test worktree: `make setup` then `make check` succeeds (optional;
      remove test worktree after: `git worktree remove .worktrees/_validate-stu-132`).

## Evidence

- Record PR link and `make check` output in the Linear issue when closing.
