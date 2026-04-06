# Engineering Patterns

## Purpose

Define consistent design and code patterns so contributors and agents know where
code belongs and how to implement changes clearly.

## Pattern Entry Template

Use this template for each pattern:

- Pattern ID:
- Context:
- Rule:
- Rationale:
- Example (good):
- Example (avoid):
- Enforcement:
- Allowed exceptions:

## Core Pattern Set (v0)

### PAT-001 Layered Boundaries

- Context: Backend services and orchestration.
- Rule: Keep adapters, domain logic, and API transport concerns separated.
- Enforcement: Import boundaries in review and architecture checks.

### PAT-002 Metadata-First Contracts

- Context: Ingestion, query planning, rendering.
- Rule: All transformations and queries depend on versioned metadata contracts.
- Enforcement: Contract tests and publish validation gates.

### PAT-003 Small Vertical Slices

- Context: Feature delivery.
- Rule: Implement minimal end-to-end slices behind flags before expanding scope.
- Enforcement: Stage-gate review and PR checklist.
- Note: Pair with PAT-006 so slices drive abstractions, not the reverse.

### PAT-004 Deterministic Analytics Tests

- Context: Crosstab/trend and AI grounding workflows.
- Rule: Use fixtures with deterministic expected outputs for core analytics paths.
- Enforcement: CI integration tests.

### PAT-005 Explicit Error Semantics

- Context: API and connector logic.
- Rule: Use typed error categories and actionable error messages.
- Enforcement: Unit tests and review checklist.

### PAT-006 Early Invariants, Deferred Platform

- Context: Greenfield or pre-pilot code where product shape is still uncertain.
- Rule: Commit early to **non-negotiable invariants** (tenant isolation, metadata
  versioning such as draft or preview or publish, no silent destructive
  overwrite). Treat everything else as **provisional**: prefer concrete code
  paths in vertical slices over new protocols, registries, or repository layers
  until a **second caller** or **second integration** needs the seam.
- Rationale: Thin invariant boundaries prevent unsafe experiments; heavy
  indirection before real workloads hides the wrong abstractions and slows
  iteration.
- Example (good): One ingestion source wired end-to-end; shared types only for
  tenant id and lifecycle state; extract a Protocol after the second connector
  repeats the same surface.
- Example (avoid): Adding ports and adapters for every concern up front with
  a single implementation each; large generic metadata schemas before real
  datasets exercise them.
- Enforcement: PR review asks “does this abstraction have two uses or one
  proven vertical slice behind it?” Deferrals recorded in ticket or addendum
  when intentionally shipping a stub for a known next slice.
- Allowed exceptions: Spikes and time-boxed branches (document discard or
  merge outcome in the ticket); regulated or contractual interfaces frozen by
  policy.

## Change Management

- Update this file when introducing or replacing a pattern.
- Reference updated pattern IDs in PR descriptions.
- Record deviations in `docs/engineering/exceptions.md`.
