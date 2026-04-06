# STU-117 Validation

## Metadata

- Linear Issue: STU-117
- Feature Branch: `STU-117-architecture-slice`
- Related Spec Doc: `docs/features/STU-117/spec.md`
- Related Design Doc: `docs/features/STU-117/design.md`

## Validation Scope

Confirm metadata domain contracts, workflow transitions, and tenant isolation
behavior match the spec and design.

## Automated Verification

- Unit: `apps/api/tests/test_metadata_workflow.py` (happy path, gate failure
  with `details`, illegal publish, wrong-tenant as not-found, unknown revision,
  terminal published, nested body deep copy).
- Static: `ruff check apps/api`, `mypy apps/api` via `make check`.

## Manual Verification

- Scenario 1: from repo root, run `make check` after sync.
- Scenario 2: skim `apps/api/metadata_domain/` and confirm alignment with
  `docs/features/STU-117/design.md` diagram and tables.

## Observability Verification

- Logging: workflow methods emit INFO logs with `revision_id`, `tenant_id`,
  `state` in `extra` (verify in tests or local run with logging configured).

## As-Built Reconciliation

- Implementation matches spec and design: Yes
- If no, docs updated in-place: N/A
- Addendum entries added to changed docs: Yes
- Residual deltas and rationale: HTTP routes and persistence intentionally
  deferred to STU-122 / storage adapters.

## Validation Outcome

- Status: Pass (after `make check` on integration branch)
- Open issues: Wire protocols to real adapters in later tickets.

## Addendum

| Date       | Change              | Reason        |
| ---------- | ------------------- | ------------- |
| 2026-04-06 | Initial validation  | STU-117 close |
| 2026-04-06 | Extended cases for PR #2 review | Review resolution |
