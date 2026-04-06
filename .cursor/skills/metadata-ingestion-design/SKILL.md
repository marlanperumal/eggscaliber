---
name: metadata-ingestion-design
description: Design metadata and ingestion changes with compatibility and draft publish safeguards. Use when implementing dataset onboarding or metadata edits.
---

# Metadata Ingestion Design

## Objectives

- Keep raw source intact.
- Maintain stable field identities across instances.
- Support draft -> preview -> publish workflows.

## Checklist

- Identify impacted metadata entities.
- Define compatibility rules for changed fields.
- Define migration behavior and rollback path.
- Add validation checks for levels and multis decoders.
- Define preview artifacts for UI and query behavior.

## Output

- Proposed metadata changes.
- Validation and migration plan.
- Risks and mitigation notes.
