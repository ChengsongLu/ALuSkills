---
name: maintain-task-checkpoints
description: Create and maintain task recovery checkpoints when the user explicitly asks for persistent task state or a cross-session handoff, or verify an existing checkpoint when resuming interrupted work. Do not create checkpoints on your own initiative.
---

# Maintain Task Checkpoints

Maintain a compact recovery index for coding work that the user wants to
persist or hand off. Checkpoints are temporary evidence, subordinate to user
instructions, repository rules, current source, Git state, tests, and formal
design documents.

## Select the entry path

- **Create or maintain:** Only when the user explicitly asks for a checkpoint,
  persistent task state, or a cross-session or agent-to-agent handoff. That
  request authorizes creation and routine updates within the stated task scope.
  Do not propose or create checkpoints merely because a task is long or
  complex.
- **Resume:** After interruption, handoff, or continuation with incomplete
  context, look for a matching existing checkpoint and follow **Restore
  safely** before repeating work. Discovery and verification are read-only, and
  resuming alone does not authorize creating new checkpoint files.

If no matching checkpoint exists, continue from repository and task evidence,
asking for missing task identity or decisions when needed.

## Choose the output location

Use a user- or repository-specified location when one is explicit. Otherwise:

```text
.maintain-task-checkpoints/
└── YYYYMMDD-HHMMSS-short-name/
    ├── STATE.md
    ├── CHECKPOINTS.md   # optional stage history
    └── artifacts/          # only when necessary
```

Use a short descriptive name without invented domain terms, and keep each task
isolated. Verify the directory is permitted and writable; if it conflicts with
project rules, agree on an alternative rather than writing elsewhere. Do not
modify ignore rules or stage checkpoint artifacts unless the user explicitly
asks. Confirm again before changing task identity, moving the checkpoint, or
materially expanding what is persisted.

## Record state

When maintaining an existing checkpoint, check the active recovery state against
this Skill's current requirements for evidence, compactness, and side effects.
Correct it within the authorized task; preserve useful history and user-defined
locations. Do not rewrite completed checkpoints or change their layout merely
because defaults changed. Read-only recovery reports relevant gaps without edits.

Create `STATE.md` before the next affected operation, recording verified
progress only:

- task ID, status (`in_progress`, `blocked`, or `completed`), last update,
  absolute repository path, branch, and starting commit;
- goal, scope, and non-goals;
- confirmed decisions and important assumptions with their evidence;
- completed, current, and next work;
- changed files and their purposes;
- passed, failed, and unperformed validation;
- blockers, open decisions, and residual risks;
- side effects that must not be repeated during recovery.

Use `STATE.md` as the default recovery artifact. Create `CHECKPOINTS.md` only
when requested or when stage history is necessary for the authorized handoff.
Preserve existing history, but do not duplicate current state or what Git and
formal documents already record. Never record unverified work as completed.

Update `STATE.md` at meaningful state or decision changes and before handoff.
Before a non-repeatable side effect, record its intended action and how to
verify the result; afterward record the observed outcome, including uncertainty.
When stage history is maintained, append only material milestones and link to
current state instead of repeating its full contents. Record conclusions, not
command transcripts. If writing fails, continue
safe in-scope work and report the missing recovery evidence.

Never store secrets, tokens, credentials, `.env` contents, personal or
sensitive data, unredacted logs, requests, responses, or large excerpts of
source, output, or conversation. Link durable conclusions to authoritative
records; checkpoint maintenance does not authorize new formal-documentation
work.

## Restore safely

Resolve truth in this order: the latest explicit user instruction; repository
rules and current formal specifications; current source, Git state, diff, and
actual validation; checkpoint files; historical conversation or summaries.

After reading a checkpoint:

- verify repository path, branch, task ID, timestamp, and diff;
- recheck relevant files and validation evidence, rerunning checks only when
  changes or missing evidence make earlier results unreliable;
- report stale checkpoint state when higher-priority evidence disagrees;
  correct the files only when checkpoint maintenance is authorized;
- distinguish attempted, completed, failed, and unknown side effects; verify
  external results before retrying. Do not repeat confirmed completed effects.
  Retry a confirmed incomplete operation only when still authorized and safe;
  an unknown outcome requires reconciliation, not an assumption of failure;
- do not merge multiple plausible checkpoints without reliable evidence; ask
  the user when identity remains ambiguous.

## Complete and hand off

When maintaining authorized checkpoint files, at completion mark `STATE.md`
as `completed`, record final changes,
validation, unverified items, and residual risks. Append a final checkpoint
only if stage history is maintained.
Report any durable conclusion that exists only in the checkpoint.

Before handoff, make current work, next work, blockers, and non-repeatable side
effects accurate and prominent, and require the receiver to revalidate against
higher-priority evidence.

Preserve completed checkpoints by default. Delete one only when the user has
authorized cleanup and it holds no needed deliverable or untransferred
conclusion; remove only that task's directory, report what was removed, and
never remove another task's checkpoint.
