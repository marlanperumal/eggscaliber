# Testing Standards

## Purpose

Define minimum test expectations for each feature slice.

## Required Test Layers

- Unit tests for new domain logic.
- Integration tests for adapter boundaries and key workflows.
- Contract tests for metadata schema and API interfaces.
- Manual exploratory checks for ingestion editor and grounding behavior.

## Feature Checklist

- Happy path covered.
- At least one negative case covered.
- Error handling behavior verified.
- Feature flag on/off behavior verified when applicable.
- Logging and metric events verified for critical flows.

## Data And Fixture Rules

- Prefer deterministic fixtures over ad-hoc data.
- Keep fixtures representative but minimal.
- Version fixture updates with code changes.

## AI Grounding Verification

- Validate query plan generation against expected structure.
- Validate response citations/provenance for dataset-backed outputs.
- Fail tests on ungrounded claims or missing provenance metadata.

## Manual QA Artifacts

For each significant feature, add:

- Manual test script in `docs/playbooks/manual-qa/`.
- Observed result summary in the PR.
- Follow-up issue for any deferred defects.
