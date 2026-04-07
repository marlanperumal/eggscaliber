# STU-116 Spec

## Metadata

- Linear issue: [STU-116 — STU-114: Design slice](https://linear.app/stunted-chicken-labs/issue/STU-116/stu-114-design-slice)
- Feature branch: `STU-116-stu-114-design-slice`
- Parent epic: STU-114 (Metadata Ingestion and Editor MVP)
- Architecture dependency: [STU-117](../STU-117/spec.md) (`MetadataLifecycleState`, workflow rules)
- Related design doc: `docs/features/STU-116/design.md` (includes Mermaid process
  flowchart and [Figma wireframes](https://www.figma.com/design/Qoi4vgPKWqM7yJv5FCWAiL/STU-116-Metadata-editor-UX))
- Related validation doc: `docs/features/STU-116/validation.md`
- Downstream build: STU-122 (ingest + editor implementation)

## Summary

Define the **product-facing** experience for bringing sources into the tenant,
editing metadata under **draft → preview → publish**, and surfacing **preview
gate** outcomes before anything becomes published truth—without prescribing
final visual design tokens or component libraries.

## Problem statement

Pilots need a legible path from “connect or upload a source” through “edit many
fields safely” to “see what will publish and why it might be blocked.” Without
an agreed flow and state model mapped to UI, build work (STU-122) risks opaque
errors, skipped preview discipline, or UX that fights the domain invariants in
`apps.api.metadata_domain`.

## Users and scenarios

- **Data owner / analyst**: connects CSV, SPSS, or Postgres-backed data, reviews
  inferred or imported metadata, fixes labels and levels in bulk, requests
  preview, publishes when satisfied.
- **Reviewer / admin** (may be same person in early pilots): confirms preview
  output and gate results before publish.
- **Support / operator** (secondary): reads clear, structured failure reasons
  (gate messages, workflow errors) without cross-tenant leakage.

## Scope

### In scope

- End-to-end **journey map**: source selection → ingestion descriptor surfaced →
  draft editing → preview request → gate outcome → publish or discard preview.
- **UI state machine** aligned to `draft`, `preview`, `published` and legal
  transitions (`submit_for_preview` requires passing `PreviewGateReport`;
  `publish` from `preview` only; `discard_preview` from `preview` to `draft`;
  `published` terminal).
- **Empty, loading, invalid, and recovery** patterns for the editor (including
  wide tables / many columns at the information-architecture level).
- **Grounding surfaces**: what the pilot sees when a change is incompatible,
  risky, or blocked by gates—mapped to `PreviewGateReport.messages` and
  `MetadataWorkflowError.details` as conceptual copy/structure targets (not API
  shapes).
- **Tenant safety UX**: user-visible messaging when a revision cannot be found
  or accessed; must not reveal existence of resources in other tenants (same
  ambiguity as `MetadataNotFoundError`).

### Out of scope

- Implementation of React (or other) components, routes, or feature flags
  (STU-122).
- Pixel-perfect visual specs; exact design-system tokens (Figma may follow).
- Performance targets (STU-121) except noting where perceived latency affects
  the draft → preview loop.

## Constraints

- UX must respect **no publish from draft** and **no preview without passing
  gate** as enforced by the reference workflow (see STU-117 design).
- **Preview gate integrity (production):** any HTTP/API entrypoint must **run or
  verify** preview gates **server-side** and pass a trustworthy
  `PreviewGateReport` into the workflow port. Untrusted clients must not be
  able to advance the lifecycle by forging `passed: true`. The domain method
  signature that accepts a report is for **in-process** orchestration and tests
  (STU-117), not an instruction to trust browser-supplied gate results.
- **Orchestration encapsulation (STU-122):** production services should expose a
  **single trusted path** (façade or `PreviewGateRunner`-style port) that runs
  gates and then calls `submit_for_preview` with the resulting report—avoid
  scattering “build a `PreviewGateReport` in the handler” across routes. Keeping
  **gate execution** separate from the **workflow mutation** port is deliberate
  for STU-117 tests and alternative validators; **security** comes from never
  letting untrusted layers inject reports, not from merging concerns inside the
  domain package in this slice.
- **Published** revisions are terminal in the product narrative: no “edit in
  place”; changes fork through a new draft revision (wording for pilots).
- Field-level body remains **opaque** at the domain layer; UI copy may describe
  “metadata fields” generically until richer schema ships.

## Success signals (from Linear)

- STU-122 can implement against linked artifacts without unresolved **major UX
  unknowns** that would force architecture changes.
- Build has **traceable links** from the issue to this spec and `design.md`.

## Acceptance criteria

- `spec.md`, `design.md`, and `validation.md` describe a coherent flow that
  matches STU-117 lifecycle rules.
- Design doc enumerates **primary screens or areas**, **states**, and **key
  transitions** with edge cases (failed gate, discard preview, not found).
- Validation doc defines how design completeness is reviewed before STU-122
  build starts.

## Rollout

- Land on `STU-116-stu-114-design-slice`; merge when validation checklist passes.
- STU-122 references updated Figma or diagrams when available.

## Addendum

| Date       | Change                                      | Reason                          |
| ---------- | ------------------------------------------- | ------------------------------- |
| 2026-04-06 | Initial spec replacing stub after STU-117   | Unblock design/build handoff    |
| 2026-04-06 | Gate integrity constraint for production API | PR security review              |
| 2026-04-06 | Link Figma + process flowchart in design doc   | Design completeness           |
| 2026-04-07 | Orchestration encapsulation for gate reports   | PR review (Gemini)            |
