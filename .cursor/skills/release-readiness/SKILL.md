---
name: release-readiness
description: Verify feature readiness for pilot rollout with checklist and rollback validation. Use before releasing feature slices.
---

# Release Readiness

## Required Evidence

- CI and tests pass.
- Manual QA checklist completed.
- Feature flag strategy documented.
- Monitoring and alerts are in place.
- Rollback procedure has been validated.

## Decision

Return one of:

- Ready
- Ready with conditions
- Not ready

Include the smallest next action to reach ready.
