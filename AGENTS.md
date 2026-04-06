# Eggscaliber Agent Operating Charter

## Mission

Build Eggscaliber as a grounded, metadata-first analytics platform for pilot customers.
Agents execute implementation autonomously while product leadership focuses on roadmap,
specs, design, and user testing.

## Non-Negotiables

- Grounded AI only: no answers based on model prior knowledge when data is unavailable.
- Tenant safety first: all data access must be tenant-scoped.
- Metadata is versioned: draft -> preview -> publish, no destructive overwrite.
- Root-run developer experience: `uv`, `pnpm`, and `docker` run from repository root.
- Every change ships with tests, telemetry updates, and rollback notes.
- Every feature must have version-controlled spec, design, and validation artifacts.
- Every feature branch must map to a Linear issue and must not update `master` without permission.
- Prefer **git worktrees** per ticket. In Cursor, **`/linear-next`** (see
  `.cursor/commands/linear-next.md`) picks the next unblocked Linear issue via
  **MCP** and opens a worktree per the feature-workflow skill.
- Default merge strategy is squash merge to keep `master` history concise per ticket.

## Source Of Truth Split

- Linear: roadmap, priorities, stage status, risks, and user feedback decisions.
- GitHub: code, PRs, CI results, release tags, and changelog.
- Figma: design system, prototype states, and design QA references.
- Repo docs: durable specs, ADRs, playbooks, and pattern standards.
- Cursor: implementation execution workspace and agent orchestration.

## Stage-Gate Workflow

Every feature must pass these gates:

1. Roadmap Ready
2. Spec Ready
3. Design Ready
4. Build Ready
5. Verification Ready
6. Release Ready
7. Post-Release Review

Gate criteria and required artifacts are defined in
`docs/playbooks/stage-gates.md`.

Required feature artifacts (version controlled in repo):

- `docs/features/<TICKET>/spec.md`
- `docs/features/<TICKET>/design.md`
- `docs/features/<TICKET>/validation.md`

Each artifact must be linked from the Linear issue.

## Delivery Loop

For each feature slice:

1. Make it work.
2. Make it right.
3. Make it good.
4. Make it fast.

Do not skip the order unless an explicit exception is recorded.

## Feature Delivery Workflow

For ticket-linked work through **push**, **PR open/update**, **Gemini (or similar)
PR review bots**, and **Linear** status/comments, agents must read and execute
`.cursor/skills/feature-workflow/SKILL.md`. It defines verification commands,
GitHub CLI and GraphQL steps, **mandatory 5-minute waits** before polling bot
feedback, `@gemini review` re-review loops, and escalation when loops cap out.

## Agent Team Topology

- Discovery Cell: clarifies requirements, constraints, and acceptance tests.
- Design Cell: develops UX and technical design options.
- Build Cell: implements feature slices behind flags.
- Quality Cell: performs critical review and adversarial testing.
- Release Cell: handles rollout checks, monitoring, and rollback readiness.

One accountable owner agent is assigned per feature. Parallel subteams are allowed only
for independent workstreams.

## Handoff Contracts

### Input Contract

- Linear issue ID and URL.
- Feature branch name (must be ticket-linked).
- Objective and business outcome.
- In-scope and out-of-scope.
- Constraints and safety requirements.
- Acceptance tests and verification requirements.
- Required artifact updates (docs, dashboards, runbooks, templates).

### Output Contract

- Linear issue ID and branch used.
- Files changed and why.
- Tests run and results.
- Telemetry/logging changes.
- Risks, caveats, and open follow-ups.
- Recommended next action.

## Escalation Policy

Agents must escalate immediately when:

- Requirement ambiguity blocks correct implementation.
- Data safety or tenant isolation is at risk.
- Stage gate fails and cannot be resolved by normal iteration.
- User-visible behavior deviates from approved spec.
- Rollback path is unclear.

Agents may proceed without escalation on low-risk, spec-conformant implementation details.

## PR Quality Bar

Each PR must include:

- Linked Linear issue.
- Linked spec, design, and validation docs in repo.
- Test evidence.
- Pattern compliance statement.
- Observability impact note.
- Rollback note.
- Exception reference (if any).
- As-built reconciliation note (code aligned to docs, or docs updated in-place with addendum).
- Completed PR checklist from `docs/templates/pr-checklist-template.md`.
- Branch rebased on latest `master` before merge unless explicitly waived.
- PR readiness gate completed per `docs/playbooks/pr-readiness.md`.
- Internal reviewer-agent pass completed before push, with required findings addressed.

## Pattern And Testing Governance

- Follow `docs/engineering/patterns.md` and `docs/engineering/testing.md`.
- Record exceptions in `docs/engineering/exceptions.md`.
- For architecture-impacting changes, update
`docs/engineering/architecture-decisions.md`.

## Definition Of Done

A feature is done only when:

- Code is merged and tests pass.
- Spec, design, and validation docs are present, current, and linked in Linear.
- Metrics/logging are in place.
- Feature flag and rollout notes are complete.
- Stage-gate artifacts are complete.
- As-built behavior is reconciled with docs; any divergence is documented in addendum sections.
