# GitHub Repository Settings

This playbook defines baseline repository enforcement for Eggscaliber.

## Merge Options

- Allow squash merge: enabled.
- Allow merge commit: disabled.
- Allow rebase merge: disabled.
- Delete branch on merge: enabled.

## Branch Protection (`master`)

- Require pull request before merging: enabled.
- Required approving reviews: 0 (pilot default).
- Dismiss stale approvals on new commits: enabled.
- Require status checks: enabled.
- Required status check contexts:
  - `checks`
- Require branches to be up to date before merging: enabled.
- Require linear history: enabled.
- Allow force pushes: disabled.
- Allow deletions: disabled.

## Policy Notes

- This setup optimizes for pilot speed while preventing direct pushes to `master`.
- Increase required approvals to 1+ when team review load increases.
