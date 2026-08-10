# Repository Instructions

These instructions apply to the entire repository. User instructions take
precedence when they explicitly request a different delivery workflow.

## Preserve the working tree

- Read the current branch, status, repository instructions, and relevant files
  before making changes.
- Treat existing staged, modified, and untracked files as user-owned unless the
  current task clearly created them.
- Do not discard, rewrite, stage, or commit unrelated changes.
- Never use destructive Git commands to clean the working tree.

## Use a user-managed pull-request workflow

Unless the user explicitly requests local-only work, deliver repository changes
through a short-lived branch and a pull request managed by the user:

1. Start from the latest default branch with a clean understanding of any
   existing local changes.
2. Create a focused branch before editing. Use
   `<type>/<short-description>`, where `type` is one of:
   - `feat` for a new Skill or capability;
   - `fix` for a defect correction;
   - `docs` for documentation-only changes;
   - `refactor` for behavior-preserving restructuring;
   - `chore` for maintenance, tooling, or repository configuration.
3. Make only the changes required for the task.
4. Review the complete diff and run the relevant validation.
5. Before creating any commit, show the user what is ready, report the
   validation results, propose the commit message, and offer two explicit
   authorization choices when remote delivery is applicable: **commit only**
   or **commit and push the current branch**. Wait for the user's choice. Do
   not treat an earlier request to make changes as approval to commit or push.
6. After the user approves, create focused commits with messages that explain
   the behavior or intent, not just the files changed. If the user chose commit
   only, stop after the commit and explicitly ask whether to push it. If the
   user chose commit and push, push the current branch immediately after the
   commit succeeds and report both outcomes.
7. Do not push the temporary branch or create, update, approve, or merge a pull
   request unless the user explicitly authorizes that action. Selecting commit
   and push counts only as authorization to push the resulting commit to the
   current branch; it does not authorize pull-request actions. By default, the
   user is responsible for creating, reviewing, and merging the pull request in
   the repository.
8. Provide the user with a ready-to-paste pull-request title and body that
   summarize:
   - what changed and why;
   - affected Skill behavior, permissions, data, or side effects;
   - validation performed;
   - compatibility, migration, or residual risks.
9. Tell the user to return and explicitly confirm after the merge succeeds,
   then stop. Do not continue with post-merge work or clean up branches before
   that confirmation.
10. If the user reports review findings before merging, address them and rerun
    affected validation, then obtain explicit user approval again before
    creating each additional commit. Offer the same commit-only or
    commit-and-push choice for every additional commit.
11. After the user confirms the merge, fetch the remote state and verify that
    the default branch contains the delivered changes. Account for squash
    merges by comparing the resulting file tree or diff instead of relying only
    on commit ancestry.
12. Only after verification succeeds, delete the remote temporary branch,
    return to the default branch, update it with a fast-forward-only pull, and
    delete the local temporary branch. Report the final clean state and say
    explicitly that no further action is needed.

Never create a commit without explicit user approval. Do not merge a draft pull
request or a pull request with pending or failed required checks. Do not delete
a branch before the user confirms that its pull request was merged.

## Close every handoff

At the end of each task, tell the user both what is complete and what should
happen next. Do not make the user infer the remaining workflow from Git state
or repository policy.

The final response must include:

- the outcome and the files or behavior affected;
- the current branch and, when applicable, the commit, pull request, or merge
  state;
- the validation that passed, failed, or was not run;
- the single next recommended action, who must take it, and whether the Agent
  is waiting for user approval or input.

When changes are ready to commit, stop and ask the user to choose between
approving the proposed commit only or approving the commit and immediate push
of the current branch. After a commit-only authorization, proactively ask
whether to push. After a commit-and-push authorization, report the push and
name pull-request creation as the next step. Never describe repository delivery
as complete while required push, review, checks, merge, or cleanup steps remain.

When a pull request is ready for the user, state whether the branch is already
pushed. If it is not, ask the user to push it first. Then tell the user to create
and merge the pull request in the repository, return and confirm that the merge
succeeded, after which the Agent will verify `main`, synchronize it, and clean
up the temporary branches. Do not replace this with a vague request to send
back the pull request link unless inspecting that link is genuinely required.

If no further action is needed, say so explicitly. If work is blocked, state
the blocker and the exact decision or external action needed to continue.

## Validate changes

Run the smallest relevant checks while iterating. Before asking the user to
approve a commit, run the repository-level validation:

```bash
git diff --check
python3 scripts/validate_skills.py
python3 -m compileall -q skills scripts
```

For changes to `codebase-handbook`, also exercise its initialization, build, and
validation helpers against a temporary project.

Record any check that could not be run and explain why. Never describe unrun or
failing validation as successful.

## Keep commits and pull requests focused

- Do not mix unrelated cleanup or refactoring into the task.
- Do not commit temporary review outputs, task checkpoints, credentials,
  private data, generated caches, or local environment files.
- Update `README.md` when adding, removing, or renaming a Skill, or when public
  installation and usage behavior changes.
- Treat changes to `SKILL.md`, references, scripts, assets, and Agent metadata
  as behavior changes that require the same care as source-code changes.
