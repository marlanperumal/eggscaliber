# Linear next

Pick the **highest-priority**, **soonest-due** **unblocked** issue in the
**Eggscaliber** Linear project, move it to **In Progress**, and **start** it per
`.cursor/skills/feature-workflow/SKILL.md` and `.cursor/skills/git-worktrees/SKILL.md`.

## Before any Linear MCP calls

Read the tool schemas under
`~/.cursor/projects/<workspace>/mcps/plugin-linear-linear/tools/*.json` (or the
workspace `mcps/plugin-linear-linear/tools/` folder). Use **real newlines** in
markdown bodies passed to tools, not `\n` escape sequences.

## 1) Load candidates

- Call **`list_issues`** with `project: "Eggscaliber"`, `limit: 250` (paginate
  with `cursor` if needed).
- Keep issues whose **status/state** is **not** terminal (exclude **Done**,
  **Completed**, **Canceled**, and equivalents).
- If the response has no `priority` or `dueDate`, fetch details with
  **`get_issue`** as needed.

## 2) Sort order (pick logic)

Sort the remaining issues by:

1. **Priority** (more urgent first). Treat **missing / none / 0** as **lowest**
   priority (sort **last**). If Linear uses numeric priority, **lower number =
   higher urgency** (e.g. 1 before 2).
2. **Due date** ascending (**sooner first**; issues **without** a due date
   **after** those with one).
3. **Stable tie-break:** issue identifier (e.g. `STU-123`).

## 3) Unblocked check

Walk the sorted list from the top. For each issue, call **`get_issue`** with
`includeRelations: true`.

The issue is **blocked** and must be **skipped** if any **incomplete** issue is
still blocking it. Use the tool’s relation fields (`blockedBy`, `blocks`, etc.)
as returned:

- If **`blockedBy`** (or equivalent) lists blocker issues, treat the candidate as
  blocked **unless every** blocker is in a **terminal** state (Done / Completed /
  Canceled).
- If blocker **state** is missing on the relation edge, **`get_issue`** each
  blocker id until you can decide.

The **first** issue that is **not** blocked is the **winner**. If none qualify,
say so and stop.

## 4) Linear: start the ticket

- Call **`save_issue`** with the winner’s `id` / identifier and set **`state`**
  to **In Progress** (or the team’s equivalent started state name).

## 5) Git: worktree + setup (do not thrash the user’s current branch)

Run shell commands from a **terminal** with **`required_permissions` / non-sandbox**
if `git` or hooks need it.

1. Resolve the **main repo root** with `git rev-parse --show-toplevel` (the
   workspace may already be a worktree; that path is still the correct root for
   `git worktree add`).
2. Confirm default branch: `gh repo view --json defaultBranchRef` (fallback
   `master`).
3. **Branch name:** match repo convention `<TICKET>-short-slug` (e.g. from
   Linear `gitBranchName` or slugify the title). Max length reasonable for git.
4. If `.worktrees/<branch>` already exists or the branch is already checked out
   elsewhere, **stop** and report—do not overwrite.
5. `git fetch origin`
6. `git worktree add .worktrees/<branch> -b <branch> origin/<defaultBranch>`
7. `cd` to that worktree and run **`make setup`**.

Optional: if **Cursor app-control** MCP **`move_agent_to_root`** is available
and the user wants to continue in the new worktree, move the agent workspace to
the **absolute path** of `.worktrees/<branch>` **after** the worktree exists.

## 6) Feature docs gate

Before the user will pass **`scripts/check_feature_docs.sh`** on push, ensure
`docs/features/<TICKET>/spec.md`, `design.md`, and `validation.md` exist. If
they are missing, **create minimal stubs** that link the Linear issue and state
what must be filled (do not invent product requirements).

## 7) Report back

Reply with: winning **issue id**, **title**, **URL**, **worktree path**,
**branch name**, and the **exact commands** you ran (or would run) so the user
can verify.
