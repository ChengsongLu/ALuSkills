# Repository Instructions

These instructions apply to the entire repository. The repository owner may explicitly request a different delivery workflow.

## Preserve the working tree

- Read the current branch, status, repository instructions, and relevant files
  before making changes.
- Treat existing staged, modified, and untracked files as user-owned unless the
  current task clearly created them.
- Do not discard, rewrite, stage, or commit unrelated changes, and never use
  destructive Git commands to clean the working tree.

## Choose the delivery path

Contributors other than the repository owner must work on a separate branch
(in a fork if needed) and submit a pull request targeting main. If the
requester’s role is unclear, use the pull-request workflow.

For the repository owner, work directly on main by default. Use a separate
branch or pull request only when requested or required by remote rules.

1. Before starting new work, check the working tree and bring main up to date
   by fast-forward when safe. Preserve any unrelated work in progress.
2. Review the scoped diff, run the validation below, and show the changes,
   validation results, and proposed commit message.
3. After the owner confirms the reviewed changes are ready, commit only those
   changes on main and push main to origin. One confirmation covers both steps.
4. Verify the remote tip after pushing. If the push is rejected, preserve the
   local commit and report the reason. Never force-push main.

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
