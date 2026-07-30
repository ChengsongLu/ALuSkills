---
name: maintain-task-checkpoints
description: Assess whether long-running or multi-stage coding work needs recoverable persistent state, obtain user confirmation before implicitly creating it, and persist, update, restore, hand off, or safely clean up confirmed checkpoints. Use when the user explicitly requests checkpoints or persistent task state, when work must be handed between agents, or when a complex task has high recovery cost due to multiple modules, migrations, state transitions, external side effects, likely interruption, or context compaction. Do not create checkpoint files for short, low-risk, single-pass work.
---

# Maintain Task Checkpoints

Maintain a compact recovery index for complex coding work. Treat checkpoints as temporary evidence subordinate to user instructions, repository rules, current source, Git state, tests, and formal design documents.

## Decide whether to persist state

Create a checkpoint when explicitly requested or when losing current context would make safe recovery materially difficult. Consider:

- multiple independently completed stages;
- changes across several modules;
- important design decisions, migrations, state machines, concurrency, or side effects;
- long operations likely to be interrupted;
- agent-to-agent handoff;
- known context compaction.

Do not activate merely because many files are present.

Treat this decision as a read-only preflight. An explicit request for a
checkpoint, persistent task state, or handoff artifact authorizes activation.
Otherwise:

1. Assess actual recovery cost and the risk of lost or repeated work.
2. Recommend whether to activate checkpoints using task-specific reasons.
3. State the proposed directory, files, and categories of information to
   persist.
4. Explicitly ask the user to confirm activation.
5. Do not create or update checkpoint files before confirmation. If the user
   declines, continue the underlying task without checkpoints when safe and
   report the resulting recovery limitation.

Once activated, do not repeat confirmation for routine updates within the
confirmed task identity, scope, location, and artifact set. Reassess and obtain
confirmation before changing task identity, moving the checkpoint, materially
expanding persisted scope, or adding optional artifacts that were not included
in the confirmed recommendation.

## Choose the output location

Use a user- or repository-specified location when one is explicit. Otherwise store each task under the project root:

```text
.maintain-task-checkpoints/
└── YYYYMMDD-HHMMSS-short-name/
    ├── STATE.md
    ├── CHECKPOINTS.md
    └── artifacts/          # create only when necessary
```

Use a short, descriptive task name that does not invent unconfirmed domain terminology. Keep every task isolated.

Before writing, verify that the directory is permitted and writable. If it conflicts with project rules, obtain agreement on an alternative; do not silently write elsewhere. Do not modify ignore rules or stage checkpoint artifacts unless the user explicitly requests it.

## Create the initial state

After development scope is confirmed and before implementation begins, create `STATE.md` with:

- task ID, status, last update, absolute repository path, branch, and starting commit;
- goal, scope, and non-goals;
- confirmed decisions;
- important assumptions with evidence sources;
- completed, current, and next work;
- changed files and their purposes;
- passed, failed, and unperformed validation;
- blockers, open decisions, and residual risks;
- side effects that must not be repeated during recovery.

Use only `in_progress`, `blocked`, or `completed` as task status. Never record planned or unverified work as completed.

Initialize `CHECKPOINTS.md` as an append-only stage history. Do not split every operation into a separate file or duplicate information recoverable from source, Git, or formal documents.

## Update at meaningful boundaries

Update `STATE.md` after finishing the current atomic operation when:

- confirmed scope or plan changes;
- an independently meaningful stage completes;
- an important decision is made;
- a long, risky, or interruptible operation is about to begin;
- validation status changes;
- a blocker or user decision is needed;
- the current work period is about to end or context is likely to compact.

When a stage completes, also append a checkpoint containing:

- completion time and stage name;
- work completed;
- decisions established or changed;
- files changed;
- validation result;
- remaining work and next step.

Record reasons and conclusions, not a command transcript. If checkpoint writing fails, continue safe in-scope implementation when possible, but report the missing recovery evidence.

## Protect information

Never store:

- secrets, tokens, credentials, or `.env` contents;
- personal or sensitive data;
- unredacted full logs, requests, responses, or command output;
- large source excerpts, test output, conversation history, or formal documents.

Move durable architecture, interface, business, security, or operational conclusions into the project's formal documentation. A checkpoint must not become the only copy of a long-lived decision.

## Restore safely

Look for a matching checkpoint after interruption, handoff, incomplete-context continuation, or unexplained related working-tree changes.

Resolve truth in this order:

1. latest explicit user instruction;
2. applicable repository rules and current formal specifications;
3. current source, Git state and diff, and actual validation;
4. checkpoint files;
5. historical conversation or summaries.

After reading a checkpoint:

- verify repository path, branch, task ID, timestamp, and diff;
- recheck current files and validation before continuing;
- correct stale state when higher-priority evidence disagrees;
- avoid repeating migrations, messages, deployments, task creation, file operations, or other side effects;
- do not merge multiple plausible checkpoints without reliable evidence; ask the user when identity remains ambiguous.

## Complete, hand off, and clean up

At completion:

1. Mark `STATE.md` as `completed`.
2. Record final changes, validation, unverified items, and residual risks.
3. Append a final checkpoint.
4. Confirm that durable conclusions exist in source, tests, specs, or maintained documentation.

Before handoff, make current work, next work, blockers, and non-repeatable side effects accurate and prominent. Require the receiver to revalidate the checkpoint against higher-priority evidence.

Preserve the completed checkpoint by default. Delete it only when the current user request already authorizes checkpoint cleanup or after obtaining explicit user confirmation, and only after confirming it contains no needed deliverable or untransferred durable conclusion. Remove only the confirmed task directory, report what was removed, and never remove another task's checkpoint; preserve and report ambiguous ownership.
