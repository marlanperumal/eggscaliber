# PR Readiness Gate

Run this before requesting review or asking others to spend time on feedback.

## Required Commands

- `make verify`
- `gh pr checks <PR_NUMBER>` (ensure latest run is passing or clearly explain pending items)

## Self-Review Checklist

- Confirm branch is ticket-linked.
- Confirm ticket docs exist:
  - `docs/features/<TICKET>/spec.md`
  - `docs/features/<TICKET>/design.md`
  - `docs/features/<TICKET>/validation.md`
- Confirm PR template fields are complete and accurate.
- Confirm this change set has no unhandled knock-on consequences (docs, config, tests,
  duplicated/contradictory logic, or stale guidance).
- Confirm comments from previous review round are either:
  - addressed in code, or
  - explicitly deferred with rationale and backlog ticket.

## Internal Reviewer Agent Gate

- Run a dedicated reviewer pass before push using the project reviewer workflow.
- Reviewer output must explicitly include:
  - critical issues found (or explicit no-critical-issues statement),
  - required fixes,
  - optional improvements.
- Apply required fixes before push, or document a defer decision with rationale and backlog link.

## Stop Condition

If any item above fails, do not request review yet.
