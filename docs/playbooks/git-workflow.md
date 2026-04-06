# Git Workflow

## Branching Policy

- Do all feature and bugfix work on a new branch.
- Branch must be linked to a Linear issue.
- Recommended branch format: `<LINEAR-ID>-<short-description>`.

Examples:

- `ENG-123-metadata-template-reuse`
- `ENG-210-fix-spss-label-parsing`

## Required Sequence Per Ticket

1. Confirm Linear issue has spec, design, and validation doc links.
2. Create branch from current `master` tip.
3. Implement and commit freely on the ticket branch.
4. Push and open PR linked to Linear issue.
5. Complete as-built reconciliation before final review.
6. Do not merge or update `master` without explicit user permission.

## As-Built Reconciliation Rule

- If implementation deviates from original spec/design:
  - update spec/design docs in-place for coherence,
  - append a change addendum entry at the bottom with what changed and why,
  - reflect final status in validation doc.
