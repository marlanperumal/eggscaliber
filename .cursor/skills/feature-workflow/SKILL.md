---
name: feature-workflow
description: >-
  End-to-end feature delivery for ticket-linked branches: Linear updates, local
  verification, push, PR creation, timed waits for Gemini PR review bot, threaded
  replies and resolves, @gemini review re-review loop until clean or capped.
  Use when implementing a Linear issue, opening/updating a PR, or driving
  automated PR review to completion.
---

# Feature Workflow (Linear + GitHub + Gemini Review)

## Goal

Execute a repeatable path from ticket pickup through merge-ready PR, without
guessing which checks or API calls apply. Use **explicit waits** so the Gemini
review bot can run before you fetch feedback.

## Preconditions

- Repository root: run `uv` / `pnpm` / `git` / `gh` from Eggscaliber root per
  `AGENTS.md`.
- **Feature branches use a git worktree** (isolated directory), not a branch
  switch in the primary clone. Follow **`.cursor/skills/git-worktrees/SKILL.md`**
  for creating the worktree, `make setup`, env/ports, and cleanup.
- **Default base branch is `master`** (not `main`) unless the repo default was
  renamed—confirm with `gh repo view --json defaultBranchRef`.
- **Linear**: read MCP tool schemas under
  `~/.cursor/projects/<workspace>/mcps/plugin-linear-linear/tools/*.json`
  before calling Linear tools; use real newlines in markdown bodies, not
  `\n` escapes.
- **GitHub CLI**: `gh auth status` must succeed for `gh pr`, `gh api`, comments.

## Phase A — Pick up the ticket

1. **Linear**: set issue **In Progress** (`save_issue` with `state` + `id`).
2. **Branch (in a worktree)**: from your primary clone, add a linked worktree
   and branch from latest default branch (see **`git-worktrees`** skill for
   paths, setup, and env):

   ```bash
   git fetch origin
   git worktree add .worktrees/<TICKET>-short-name -b <TICKET>-short-name origin/master
   cd .worktrees/<TICKET>-short-name
   make setup
   ```

   Use the ticket prefix from Linear (e.g. `STU-117-architecture-slice`).
   Confirm the default base branch name if it is not `master`
   (`gh repo view --json defaultBranchRef`). If the branch already exists
   locally, use `git worktree add .worktrees/<TICKET>-short-name <TICKET>-short-name`
   instead.

   Run **all** subsequent git commits, `make check`, and `git push` from the
   **worktree** directory unless you explicitly document another arrangement.
3. **Artifacts**: ensure `docs/features/<TICKET>/spec.md`, `design.md`,
   `validation.md` exist before push (see `scripts/check_feature_docs.sh`).
4. Implement, test, update docs in-place with addenda when intent changes.

## Phase B — Verify and push (no drive-by scope)

Run from repo root **in this order** unless a playbook overrides:

```bash
make check
```

If hooks are required before push (per project): `make hooks-run-push` or
`uvx pre-commit run --all-files --hook-stage pre-push`.

Then:

```bash
git status
git add <paths>
git commit -m "<type>(<TICKET>): <short description>"
git push -u origin <branch>
```

Use `required_permissions: ["all"]` (or non-sandbox) when pre-push hooks need
full OS access (common `PermissionError` from `pre_commit` otherwise).

## Phase C — Open the PR

```bash
gh pr create --base master --head <branch> \
  --title "feat(<TICKET>): …" \
  --body "$(cat <<'EOF'
## Linear
- [<TICKET>](<url>)

## Summary
…

## Artifacts
- docs/features/<TICKET>/spec.md
…
EOF
)"
```

Adjust `--base` if `master` is wrong. Capture the PR **number** from output.

**Linear**: comment on the issue with PR link; optionally set state **In
Review** when the PR is open.

## Phase D — First bot pass (mandatory wait)

1. **Wait 5 minutes** before querying review feedback (bot latency):
   - Shell: `sleep 300` with `block_until_ms` ≥ 310000, **or**
   - `Await` with `block_until_ms: 300000`.
2. **Fetch inline review threads** (preferred—matches “resolve conversation”):

   ```bash
   gh api graphql -f query='
   query {
     repository(owner: "OWNER", name: "REPO") {
       pullRequest(number: PR_NUMBER) {
         reviewThreads(first: 50) {
           nodes {
             id
             isResolved
             comments(first: 5) {
               nodes { fullDatabaseId author { login } body path line }
             }
           }
         }
       }
     }
   }'
   ```

   Use each comment’s **`fullDatabaseId`** (numeric string from GraphQL) as the
   REST **`in_reply_to`** target when posting a reply. GitHub’s GraphQL type is
   **`PullRequestReviewComment`**; it exposes **`line`** and **`fullDatabaseId`**
   (not `databaseId`).

3. **Also** list top-level PR comments if needed:
   `gh pr view PR_NUMBER --json comments,reviews`
4. For each thread: implement fixes, **reply in-thread** (REST):

   ```bash
   gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments \
     -f body='…' \
     -f in_reply_to=FULLDATABASEID
   ```

   Use **`-f`** for `in_reply_to` so `gh` sends a usable value for the numeric
   comment id.

5. **Resolve** threads (GraphQL), using the thread **`id`** from step 2 (e.g.
   `PRRT_…`):

   ```bash
   gh api graphql -f query='
   mutation($threadId: ID!) {
     resolveReviewThread(input: { threadId: $threadId }) {
       thread { isResolved }
     }
   }' -f variables='{"threadId":"PRRT_…"}'
   ```

6. **Push** follow-up commits on the same branch.

## Phase E — Gemini re-review loop

After you have addressed the current round of bot comments (replies + resolves
+ pushed commits):

1. Request a fresh review:

   ```bash
   gh pr comment PR_NUMBER --body "@gemini review"
   ```

2. **Wait 5 minutes** again (`sleep 300` / `Await` 300000ms).
3. Re-run **Phase D** steps 2–6 to fetch new threads, reply, resolve, push.
4. **Repeat** Phase E until:
   - **Exit (success)**: no unresolved `reviewThreads` from the bot **and** no
     new actionable inline feedback in the latest review; **or** the bot
     review state is satisfactory for merge per team bar.
   - **Exit (escalate)**: after **5** full Phase E rounds, stop looping and
     summarize remaining threads for a human.
   - **Exit (blocked)**: CI failing, policy conflict, or ambiguity—document
     and hand off.

If the bot username differs, filter threads by `author.login` (e.g.
`gemini-code-assist`) when deciding what must be cleared.

## Phase F — Close out

1. **Linear**: mark issue **Done** when merged (or per team workflow); keep
   docs reconciliation note in the issue or PR.
2. **Merge**: squash per ticket policy; do not merge `master` without explicit
   permission if policy requires it.
3. **Worktree**: remove the linked worktree when finished (see
   **`git-worktrees`** skill: `git worktree remove`, `git worktree prune`, and
   optional branch deletion).

## Quick command cheat sheet

| Step | Command |
| ---- | ------- |
| New worktree + branch | `git worktree add .worktrees/<b> -b <b> origin/master` then `cd .worktrees/<b>` |
| Worktree setup | `make setup` (from worktree root) |
| Full verify | `make check` |
| Feature docs gate | `bash scripts/check_feature_docs.sh` |
| Push | `git push -u origin <branch>` |
| PR create | `gh pr create --base master --head <branch> …` |
| Wait 5 min | `sleep 300` |
| PR threads | `gh api graphql` (query above) |
| Reply inline | `gh api repos/OWNER/REPO/pulls/<PR>/comments -f body='…' -f in_reply_to=<id>` |
| Resolve thread | `gh api graphql -f query='mutation($i:ID!){resolveReviewThread(input:{threadId:$i}){thread{isResolved}}}' -f variables='{"i":"PRRT_…"}'` |
| Ping Gemini | `gh pr comment <n> --body "@gemini review"` |

## What not to do

- Do not implement a **full** ticket slice only by switching branches in the
  primary clone unless the user explicitly directs that (worktrees are the
  default per **`git-worktrees`** skill).
- Do not merge `master` or change protected defaults without explicit user
  approval (per workspace rules).
- Do not skip the **5-minute waits** when expecting Gemini; polling immediately
  wastes turns and misses comments.
- Do not claim “bot happy” without re-querying threads after the wait.
- Do not exceed **5** Phase E iterations without human escalation.

## Maintenance

- Update **OWNER/REPO** examples if the remote changes; prefer `gh repo view
  --json nameWithOwner` for copy-paste.
- If GitHub replaces review APIs, update Phase D/E GraphQL snippets in this
  skill and record the change in a PR.
