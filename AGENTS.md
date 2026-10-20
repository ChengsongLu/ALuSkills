# Repository Instructions

These instructions apply to the entire repository. User instructions take
precedence when they explicitly request a different delivery workflow.

## Preserve the working tree

- Read the current branch, status, repository instructions, and relevant files
  before making changes.
- Treat existing staged, modified, and untracked files as user-owned unless the
  current task clearly created them.
- Do not discard, rewrite, stage, or commit unrelated changes, and never use
  destructive Git commands to clean the working tree.

## Choose the delivery path

Changes to Skill behavior—any `SKILL.md`, `references/`, `scripts/`, `assets/`,
or `agents/` file—go through a short-lived branch and a user-managed pull
request. Documentation-only and tooling changes outside `skills/` (README,
contributing or security docs, CI, validation scripts) may be committed
directly to the default branch once the user approves the commit.

For the pull-request path:

1. Start from the latest default branch and create a focused branch named
   `<type>/<short-description>`, where `type` is `feat`, `fix`, `docs`,
   `refactor`, or `chore`.
2. Make only the changes required for the task, review the complete diff, and
   run the validation below.
3. Before any commit, show what is ready, the validation results, and the
   proposed message, and ask the user to choose **commit only** or **commit
   and push the current branch**. An earlier request to make changes is not
   approval to commit or push.
4. Commit with messages that explain behavior or intent. After commit only, ask
   whether to push. Pushing never authorizes creating, updating, approving, or
   merging a pull request.
5. Give the user a ready-to-paste pull-request title and body covering what
   changed and why, affected Skill behavior, permissions, data, or side
   effects, validation performed, and compatibility or residual risks.
6. Address review findings the user reports, rerun affected validation, and
   obtain approval again before each additional commit.
7. After the user confirms the merge, fetch and verify that the default branch
   contains the delivered changes (compare trees to account for squash
   merges). Only then delete the remote and local temporary branches and
   fast-forward the default branch.

Never create a commit without explicit user approval. Do not merge a draft pull
request or one with pending or failed required checks, and do not delete a
branch before the user confirms its merge.

## Close every handoff

End each task by stating the outcome and affected files, the current branch and
commit or pull-request state, the validation that passed, failed, or was not
run, and the single next action—who takes it and whether you are waiting on the
user. Never describe delivery as complete while a required push, review, merge,
or cleanup step remains; if nothing remains, say so.

## Validate changes

Run the smallest relevant checks while iterating. Before asking the user to
approve a commit, run:

```bash
git diff --check
python3 scripts/validate_skills.py
python3 -m compileall -q skills scripts
```

For changes to `codebase-handbook`, also exercise its initialization, build, and
validation helpers against a temporary project. Report any check that could not
be run and why; never describe unrun or failing validation as successful.

## Keep commits focused

- Do not mix unrelated cleanup or refactoring into the task.
- Do not commit temporary review outputs, task checkpoints, credentials,
  private data, generated caches, or local environment files.
- Update both READMEs when adding, removing, or renaming a Skill, or when public
  installation and usage behavior changes.

## Keep every Skill independent and portable

- Each Skill must remain self-contained and useful when installed by itself. Its
  behavior must not depend on another Skill being installed, available, or
  invoked before or after it.
- Do not make one Skill invoke, require, recommend, route to, or name another
  Skill in its `SKILL.md`, references, scripts, assets, or Agent metadata.
- Resolve overlap through precise trigger conditions and explicit scope
  boundaries, not cross-Skill orchestration. A Skill investigates the repository
  facts and resolves the decisions its own workflow needs.
- When work falls outside a Skill's scope, stop the affected workflow, explain
  the missing decision or next activity in generic terms, and return control to
  the user without prescribing another Skill.
- Collection-level documentation may describe how the Skills cover adjacent
  development stages, but no individual Skill may assume that context at
  runtime.
