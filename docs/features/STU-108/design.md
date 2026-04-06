# STU-108 Design

## Metadata

- Linear Issue: STU-108
- Feature Branch: feature/stu-108-finalize-tooling-and-workflow-governance-scaffold-in-repo
- Related Spec Doc: `docs/features/STU-108/spec.md`
- Related Validation Doc: `docs/features/STU-108/validation.md`
- Figma Link(s): N/A (tooling/governance feature)

## Design Summary

Establish a layered delivery control plane:

1. Root command orchestration (`Makefile`, `package.json`, Docker compose).
2. Quality gates (hooks + CI).
3. Workflow policy artifacts (AGENTS, playbooks, templates).
4. Ticket-linked branch and docs conventions.

## UX States

- Empty: N/A
- Loading: N/A
- Error: N/A
- Success: N/A

## Interaction Flows

### Developer Flow

1. Create Linear ticket and linked branch.
2. Create docs under `docs/features/<TICKET>/`.
3. Implement changes.
4. Run `make verify`.
5. Open PR and complete governance checklist.

### Reviewer Flow

1. Review PR diff and linked docs.
2. Validate reconciliation notes.
3. Approve and squash merge.

## Component/Module Boundaries

- `Makefile` + `package.json`: command UX and orchestration.
- `.pre-commit-config.yaml`: local quality gates.
- `.github/workflows/ci.yml`: pre-merge enforcement.
- `docs/playbooks/*`: process policy.
- `.cursor/rules/*`: agent behavior enforcement.
- `scripts/check_feature_docs.sh`: docs-compliance automation.

## Edge Cases

- Branch name missing ticket identifier -> docs check fails with guidance.
- Ticket directory exists but missing one of three required docs -> check fails.
- Default branch builds (master/main) bypass ticket-doc requirement.

## Accessibility And Usability Notes

N/A (non-UI feature).

## Technical Design Notes

- Use branch-name ticket extraction with regex `([A-Za-z]+-[0-9]+)`.
- Normalize ticket ID to uppercase for canonical doc folder naming.
- Check for exact files:
  - `docs/features/<TICKET>/spec.md`
  - `docs/features/<TICKET>/design.md`
  - `docs/features/<TICKET>/validation.md`
- Run check in:
  - pre-push hook stage
  - CI job (with explicit branch/ref env)

## Change Addendum

- Date: 2026-04-06
- Change: Added explicit automation layer for feature-doc completeness.
- Reason: convert policy from manual checklist to enforceable quality gate.
- Impact: PRs can no longer pass without feature-specific docs in the expected location.
