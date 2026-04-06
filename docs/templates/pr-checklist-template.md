# PR Checklist Template

Use this checklist in every pull request.

## Ticket And Branch

- [ ] Linear issue linked
- [ ] Branch is ticket-linked (`<LINEAR-ID>-<description>`)
- [ ] Scope matches ticket

## Required Artifacts

- [ ] Spec doc linked
- [ ] Design doc linked
- [ ] Validation doc linked

## Verification

- [ ] Automated tests run and results included
- [ ] Manual checks run (or explicitly not required)
- [ ] Logging/metrics impact noted
- [ ] Rollback plan noted

## As-Built Reconciliation

- [ ] Implementation aligns with spec/design
- [ ] If not aligned, docs updated in-place
- [ ] Change addendum entries added with reason
- [ ] Validation doc reflects final as-built status

## Governance

- [ ] Stage gate status updated in Linear
- [ ] Exceptions (if any) logged and referenced
- [ ] No `master` update/merge without explicit user permission
