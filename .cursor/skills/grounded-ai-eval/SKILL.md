---
name: grounded-ai-eval
description: Evaluate NL analytics outputs for grounding and correctness against available datasets. Use when validating AI query planning and response generation.
---

# Grounded AI Evaluation

## Goals

- Ensure no ungrounded claims.
- Validate query plan quality and execution fidelity.
- Verify provenance in final outputs.

## Evaluation Flow

1. Run prompt against known fixtures.
2. Inspect generated query plan.
3. Verify executed operations and result set.
4. Confirm response cites dataset/source context.
5. Record pass/fail with failure categories.

## Failure Categories

- Missing-data hallucination.
- Wrong dataset or wrong period.
- Incorrect transformation semantics.
- Missing provenance.
