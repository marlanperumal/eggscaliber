# Stage Gates

## Gate 0: Roadmap Ready

- Problem and outcome are clear.
- Success metric is defined.
- Owner and dependencies are assigned.
- Kill criteria are documented.

## Gate 1: Spec Ready

- Acceptance criteria are testable.
- Data contracts are explicit.
- Rollout strategy and non-goals are included.
- Spec doc exists in repo and is linked from the Linear issue.

## Gate 2: Design Ready

- Figma and code prototype are aligned.
- Empty/loading/error/success states are defined.
- Major edge cases are documented.
- Design doc exists in repo and is linked from the Linear issue.

## Gate 3: Build Ready

- Work is sliced into vertical increments.
- Feature flag and migration plans are defined.
- Handoff input contract is complete.
- Feature branch is created from a Linear ticket and named with ticket prefix.

## Gate 4: Verification Ready

- Automated tests pass.
- Manual script execution is documented.
- Telemetry checks pass for key paths.
- Validation doc exists in repo and is linked from the Linear issue.
- As-built reconciliation is complete (docs align with implementation).

## Gate 5: Release Ready

- Staged rollout plan approved.
- Rollback steps tested.
- Stakeholder/pilot communication prepared.
- If specs/design changed during implementation, addendum sections describe what changed and why.

## Gate 6: Post-Release Review

- Metrics reviewed against targets.
- Incidents and learnings documented.
- Follow-up backlog captured.

