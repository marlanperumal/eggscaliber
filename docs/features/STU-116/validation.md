# STU-116 Validation

## Metadata

- Linear issue: [STU-116 — STU-114: Design slice](https://linear.app/stunted-chicken-labs/issue/STU-116/stu-114-design-slice)
- Feature branch: `STU-116-stu-114-design-slice`
- Related spec: `docs/features/STU-116/spec.md`
- Related design: `docs/features/STU-116/design.md`

## Purpose

Confirm the **design slice** is complete enough for STU-122 to implement without
reopening STU-117 architecture decisions. This is a **documentation and review**
gate, not automated product QA.

## Review checklist

### Alignment with domain

- [ ] Every documented UI state maps to `MetadataLifecycleState` (`draft`,
  `preview`, `published`).
- [ ] Documented transitions match `InMemoryMetadataWorkflowService` rules:
  preview only after passing gate; publish only from preview; discard preview
  only from preview; published terminal.
- [ ] Gate failure path never describes a `preview` UI state when the domain
  remains `draft`.

### Coverage

- [ ] Connect → draft → preview → publish happy path is described end-to-end.
- [ ] Gate failure, discard preview, and missing/unauthorized revision flows
  have explicit UX guidance.
- [ ] Wide-table / many-column editing has an agreed IA pattern (scroll,
  freeze, bulk actions).
- [ ] Tenant-facing copy does not leak cross-tenant signals on access errors.

### Handoff quality

- [ ] Open questions for STU-122 are listed in `design.md` (autosave, async
  preview, body mapping).
- [ ] Links from Linear STU-116 to this spec and `design.md` are present.
- [ ] **Figma**: `design.md` links the exploration file; reviewer has opened the
  page and confirmed **Option A vs B** (or recorded a decision in Linear).
- [ ] **Flowchart**: Mermaid process flow in `design.md` matches the agreed
  trusted-boundary story (server-side gates).

## Roles

| Role              | Responsibility                                      |
| ----------------- | --------------------------------------------------- |
| Owner (assignee)  | Drives updates; resolves open questions or logs them for STU-122 |
| Reviewer          | Confirms checklist; may be same person in early stage |
| Build (STU-122)   | Acknowledges handoff; flags mismatches early        |

## Exit criteria

- All required checklist items above are **checked** or **waived in writing**
  in a Linear comment on STU-116 with rationale.
- STU-116 may move to **Done** after merge; STU-122 should not start conflicting
  UX without an addendum here.

## Addendum

| Date       | Change                    | Reason              |
| ---------- | ------------------------- | ------------------- |
| 2026-04-06 | Initial validation doc    | Replace stub        |
