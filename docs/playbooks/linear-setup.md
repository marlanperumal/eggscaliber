# Linear Setup Checklist

## Projects

- Pilot Core
- Metadata Editor
- Grounded AI
- Experimentation

## Workflow States

- Discovery
- Spec Ready
- Design Ready
- Build
- Verify
- Pilot
- Done

## Recommended Fields

- Stage Gate
- Risk Level
- Outcome Metric
- Feature Flag
- User-Test Status
- Spec Doc Path
- Design Doc Path
- Validation Doc Path
- Feature Branch

## Views

- Executive Roadmap (Now/Next/Later)
- This Week Delivery
- Blocked And Risks
- User Feedback Queue

## Ticket Policy

- Every feature or bug ticket must include linked spec, design, and validation docs.
- Every implementation ticket must include a ticket-linked feature branch name.
- Ticket cannot move to `Done` unless as-built reconciliation is complete.

## Roadmap epics vs actionable work

- **Roadmap epics** use a **`[Roadmap Epic]`** title prefix and track multi-slice
  outcomes; they are **not** default targets for an implementation worktree.
- **Actionable** issues are slices, bugs, chores, or other tickets with a single
  clear delivery branch (often child issues under an epic).
- Automated pickup (`.cursor/commands/linear-next.md`) **skips** `[Roadmap Epic]`
  titles so the next issue is always implementation-sized.
