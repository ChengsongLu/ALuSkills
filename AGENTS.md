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

## Use a pull-request workflow

Unless the user explicitly requests local-only work, deliver repository changes
through a short-lived branch and pull request:

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
5. Create focused commits with messages that explain the behavior or intent,
   not just the files changed.
6. Push the temporary branch and open a pull request against the default branch.
7. In the pull request, summarize:
   - what changed and why;
   - affected Skill behavior, permissions, data, or side effects;
   - validation performed;
   - compatibility, migration, or residual risks.
8. Wait for required CI checks and an independent review. An Agent must not
   approve its own pull request.
9. Address review findings with additional commits, rerun affected validation,
   and wait for the updated checks and review result.
10. Merge only after all required checks pass, blocking findings are resolved,
    and the required approval is present. Use a merge method allowed by the
    repository rather than rewriting shared history.
11. Confirm that the pull request was merged, then delete the remote temporary
    branch. Return to the default branch, update it with a fast-forward-only
    pull, and delete the local temporary branch.

Do not merge a draft pull request or a pull request with pending or failed
required checks. Do not delete a branch before confirming that its pull request
was merged.

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

When the user requests only one step of a larger workflow, such as creating a
commit, stop after that authorized step and explicitly name the next step. For
example: "The commit is ready on `docs/example`; next, I can push the branch
and open a pull request." Never describe repository delivery as complete while
required push, review, checks, merge, or cleanup steps remain.

If no further action is needed, say so explicitly. If work is blocked, state
the blocker and the exact decision or external action needed to continue.

## Validate changes

Run the smallest relevant checks while iterating. Before opening or updating a
pull request, run the repository-level validation:

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
