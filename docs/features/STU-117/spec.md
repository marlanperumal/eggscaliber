# STU-117 Spec

## Metadata

- Linear Issue: STU-117
- Feature Branch: `STU-117-architecture-slice`
- Parent Epic: STU-114 (Metadata Ingestion and Editor MVP)
- Related Design Doc: `docs/features/STU-117/design.md`
- Related Validation Doc: `docs/features/STU-117/validation.md`

## Summary

Establish explicit boundaries between stable dataset definitions, per-period dataset
instances, ingestion adapters, and the metadata `draft -> preview -> publish`
workflow so later build slices can plug in persistence and HTTP without revisiting
core contracts.

## Problem Statement

Without typed models and service interfaces, ingestion and editor work risks
silent coupling, weak tenant isolation, and ad hoc state transitions that violate
metadata versioning rules.

## User Value

- Safer parallel work across ingestion, editor UI, and validation slices.
- Clear extension points for storage and connectors.
- Enforceable tenant scoping at the domain layer.

## Scope

### In Scope

- Pydantic models for `DatasetDefinition`, `DatasetInstance`, `MetadataRevision`,
  lifecycle state, ingestion source descriptor, and preview gate report.
- `typing.Protocol` contracts for ingestion adapters, definition/instance
  repositories, and the metadata workflow service.
- Reference `InMemoryMetadataWorkflowService` implementing allowed transitions
  with logging hooks for critical transitions.
- Unit tests for happy path, gate failure, tenant mismatch, and terminal
  `published` state.

### Out Of Scope

- REST/GraphQL routes and feature flags (deferred to STU-122 and related slices).
- Real database or object-store persistence.
- Full schema for field-level metadata (opaque `body` on revisions for now).

## Constraints

- Tenant id must be checked on every workflow operation touching a revision.
- `DatasetDefinition` identity must remain stable across `DatasetInstance`
  periods (enforced by modeling separation; migration policy when types change
  is out of band for this slice).
- No cross-tenant reads or writes in reference service or adapter contracts.

## Data Contracts

- `MetadataLifecycleState`: `draft | preview | published`.
- `IngestionSourceKind`: `csv | spss | postgres`.
- `PreviewGateReport`: boolean `passed` plus optional blocking messages.
- `MetadataRevision`: tenant-scoped, instance-bound, carries opaque `body` map
  (deep-copied on draft create so nested structures are snapshotted).
- `MetadataWorkflowError`: optional `details` tuple (e.g. preview gate
  messages) for structured handling without parsing `str(exc)`.
- Workflow lookup by `revision_id`: unknown id or wrong `tenant_id` both raise
  `MetadataNotFoundError` with the same message shape.

## API/Interface Changes

- No new public HTTP endpoints.
- Python import surface: `apps.api.metadata_domain`.

## Acceptance Criteria

- Domain package exists with models, protocols, and in-memory workflow
  implementation as specified.
- Illegal transitions raise `MetadataWorkflowError` (with `details` when
  preview gates fail). Wrong-tenant or unknown revision access raises
  `MetadataNotFoundError`.
- Automated tests cover at least one happy path and multiple negative paths.
- Spec, design, and validation docs exist under `docs/features/STU-117/`.

## Rollout Plan

- Land on `STU-117-architecture-slice`; merge via squash after review.
- Downstream slices implement adapters and persistence behind the protocols.

## Observability Plan

- `logging` events on create, preview, publish, and discard with structured
  `extra` fields: `revision_id`, `tenant_id`, `instance_id`, `state` on create.

## Test Strategy

- `pytest apps/api/tests/test_metadata_workflow.py`
- Full API suite: `make test` from repository root.

## Addendum

| Date       | Change                         | Reason                          |
| ---------- | ------------------------------ | ------------------------------- |
| 2026-04-06 | Initial architecture slice   | STU-117 scope baseline          |
| 2026-04-06 | PR review hardening (deep copy, gate `details`, unified not-found) | PR #2 |
| 2026-04-06 | `MetadataRevision.dataset_instance_id` renamed to `instance_id` (Gemini) | PR #2 |
| 2026-04-06 | Workflow returns deep-isolated revisions; `get_revision` on protocol | PR #2 |
| 2026-04-06 | Removed unused `TenantIsolationError`; ID fields `min_length=1` on models | PR #2 |
| 2026-04-06 | `InMemoryMetadataWorkflowService` uses `threading.Lock` for atomic transitions | PR #2 |
