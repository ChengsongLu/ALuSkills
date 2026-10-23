---
name: commit-changes
description: Stage and commit repository changes with a reviewed, informative commit message when the user asks to commit. Do not use to decide whether work should be committed, or for push, merge, or pull-request management.
---

# Commit Changes

Turn the user's authorized changes into a focused commit whose message explains
what changed and why. Commit only when the user asks; an earlier request to make
changes is not approval to commit.

## Determine the scope

1. Read applicable repository instructions; they override the defaults below
   for message language, format, trailers, and delivery workflow.
2. Inspect the branch, staged, unstaged, and untracked changes, and the diff
   statistics.
3. When the user asks to commit everything, include all uncommitted changes in
   the current repository without asking file by file.
4. Otherwise stage and commit only the authorized content. Do not carry along
   unrelated or user-excluded changes that are already staged; when they would
   be included, ask how to handle them before committing.
5. Ask about scope only when changes are mixed or their ownership is unclear.
   When the scope is already clear, do not ask about excluding files again.
6. Flag files that look like credentials, local environment configuration,
   caches, or build output before staging them.

## Write the message

- Use the language the user or repository instructions specify; otherwise match
  the language of recent commits in the repository.
- Do not add `Co-Authored-By` or tool-attribution trailers unless the user or
  repository requires them.
- A single, local change whose title fully describes it may use a title only.
  Multiple topics, cross-module behavior, deployment, or external contract
  changes require a title, a blank line, and a body.
- Never summarize a batch with a vague title such as "improve", "update", or
  "fix" alone.
- The title states the core outcome. The body groups the main changes by
  feature, module, or topic and states their purpose or behavioral result,
  covering everything important in the actual commit. Do not list files one by
  one, narrate implementation steps, or pad to a fixed number of points.
- State compatibility impact, upgrade steps, or known limitations when they
  exist.
- Record only validation that was actually run, with its result. Adding a test
  is not the same as the test passing.

## Confirm and commit

1. Follow the user's authorization and repository approval requirements. By
   default show the complete proposed message and covered files before committing.
   Wait for confirmation unless the user already approved them or explicitly
   authorized committing without another message review. Do not repeat an
   already satisfied approval gate.
2. Preserve the approved title, body, and line breaks exactly; when message
   drafting was delegated, commit the message prepared within that authorization.
3. Report the commit hash, title, and any remaining uncommitted changes.

Do not push unless the user explicitly asks. Never force-push a shared branch.
Do not skip hooks unless the user explicitly asks; when a hook changes files or
fails, report it and resolve it before retrying.
