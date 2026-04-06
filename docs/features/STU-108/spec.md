# STU-108 Spec

## Metadata

- Linear Issue: STU-108
- Feature Branch: feature/stu-108-finalize-tooling-and-workflow-governance-scaffold-in-repo
- Related Design Doc: `docs/features/STU-108/design.md`
- Related Validation Doc: `docs/features/STU-108/validation.md`

## Summary

Bootstrap Eggscaliber with root-runnable tooling and explicit workflow governance so
feature delivery is traceable, testable, and aligned to Linear-linked execution.

## Problem Statement

The project started without a stable engineering operating system. Without documented
governance, templates, and enforcement, delivery can drift from requirements and produce
inconsistent quality and visibility.

## User Value

- Faster and safer delivery cadence for pilot work.
- Clear traceability from roadmap issue to code and verification artifacts.
- Reduced review overhead through consistent guardrails.

## Scope

### In Scope

- Root-level commands for development and verification (`uv`, `pnpm`, `docker`).
- CI and local hook quality gates.
- PR templates and checklists.
- Agent operating charter, playbooks, rules, and skill scaffolding.
- Git/branching policy and GitHub repository protections.

### Out Of Scope

- Product feature implementation beyond health-check skeletons.
- Full frontend app scaffolding and production deployment workflows.

## Constraints

- Keep master protected and PR-driven.
- Maintain compatibility with local-first development.
- Keep process lightweight enough for pilot speed.

## Data Contracts

No runtime product data contract changes. This is process/tooling foundation work.

## API/Interface Changes

- Added API health endpoint scaffolding (`apps/api/main.py`) for smoke verification.
- Added root command interfaces via `Makefile` and `package.json` scripts.

## Acceptance Criteria

- Root quality commands run successfully from repository root.
- Pre-commit and pre-push hooks are installed and runnable.
- CI validates equivalent checks before merge.
- PR workflow enforces spec/design/validation artifacts and reconciliation.
- Branching policy is documented and protected in GitHub settings.

## Rollout Plan

- Apply settings and docs on STU-108 branch.
- Validate locally and in CI.
- Merge via squash once checks pass and review is complete.

## Observability Plan

- Use CI check status as primary observability for pre-merge quality compliance.
- Use PR template/governance checklist completion as process observability.

## Test Strategy

- `make check`
- `make hooks-run-push`
- `docker compose config`
- GitHub Actions checks job pass

## Risks And Mitigations

- Risk: process overhead may slow pilot iteration.
  - Mitigation: keep approvals lightweight while enforcing key guardrails.
- Risk: doc compliance is done manually.
  - Mitigation: add branch/ticket-linked docs guard script in hooks + CI.

## Change Addendum

- Date: 2026-04-06
- Change: Added automated requirement for per-ticket feature docs path convention.
- Reason: Ensure spec/design/validation artifacts are always created, not only templated.
- Impact: Branches without required docs now fail pre-push/CI checks.
