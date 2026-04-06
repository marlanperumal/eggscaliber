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

### PAT-004 Deterministic Analytics Tests

- Context: Crosstab/trend and AI grounding workflows.
- Rule: Use fixtures with deterministic expected outputs for core analytics paths.
- Enforcement: CI integration tests.

### PAT-005 Explicit Error Semantics

- Context: API and connector logic.
- Rule: Use typed error categories and actionable error messages.
- Enforcement: Unit tests and review checklist.

## Change Management

- Update this file when introducing or replacing a pattern.
- Reference updated pattern IDs in PR descriptions.
- Record deviations in `docs/engineering/exceptions.md`.
