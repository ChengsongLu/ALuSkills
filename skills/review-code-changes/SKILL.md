---
name: review-code-changes
description: Review a working-tree diff, staged changes, commit, branch comparison, or pull-request change set for concrete correctness, reliability, security, compatibility, testing, and documentation risks, and confirm before creating persistent review artifacts that the user did not explicitly request. Use when the user explicitly requests a code review, asks to inspect a diff or commit for findings, or asks to remediate findings from such a review. Do not invoke merely to self-check an ordinary implementation, validate a small edit, or inspect code without a requested change set. Review-only requests must not modify code.
---

# Review Code Changes

Review changed code against its intended contract and adversarial failure conditions. Report actionable findings with evidence and keep implementation files read-only during review-only work.

## Select the mode

- **Lightweight review:** Use for a focused, low-risk change that can be read
  reliably in one pass when the user did not request a persistent artifact.
  Inspect and report in the conversation without creating review files.
- **Recorded review:** Use when the user requests a formal or persistent review,
  when assessing PR or branch readiness, or when the change is large, high risk,
  or needs a durable handoff. Persist the review as described below.
- **Remediation:** Enter only when the user explicitly asks to fix or optimize
  identified findings. Read [references/remediation.md](references/remediation.md)
  completely before modifying code. Adversarially assess the proposed fix before
  implementation, then re-review the final remediation diff and affected paths
  after validation. Do not close remediation while that fresh review identifies
  a credible defect or vulnerability introduced by the fix.

This workflow covers changed code. Do not use it as a project-wide or module-wide codebase inspection process.

Treat initial mode selection as a read-only preflight and finalize it after
freezing the baseline below. Use actual change risk, not file count alone.
Explain the recommendation and the proposed artifacts. An explicit request for
a formal, recorded, or persistent review authorizes recorded mode.
Otherwise, explicitly ask the user to confirm recorded mode before creating
`.review-code-changes/`, `review.md`, or `coverage.md`; a general request to
review code authorizes read-only inspection, not persistent artifacts.

If the user declines recorded mode, continue as a lightweight review with an
in-memory coverage checklist when that remains reliable. If a reliable review
requires durable handoff evidence, report the limitation and ask for direction
instead of silently writing files. Reassess and reconfirm when the review scope
or risk changes enough to alter the recommended mode or artifact set.

## Place the output

Skip this section in lightweight review mode. For a recorded review, use a user-
or repository-specified location when one is explicit. Otherwise create one
isolated review directory under the project root:

```text
.review-code-changes/
└── YYYY_MM_DD_scope_NNN/
    ├── review.md
    ├── coverage.md       # required for large or high-risk reviews
    └── remediation.md    # create only after authorized remediation
```

Use `working-tree`, a short commit or branch slug, or another unambiguous comparison slug for `scope`. Start `NNN` at `000` and select the next unused sequence for the same date and scope. Record the comparison base inside `review.md`; do not rely on the directory name as evidence.

Resolve the prospective output path at this stage, but do not create it yet.
First complete the baseline steps below and freeze the exact review input.
Create the review directory only after the baseline is frozen.

Do not modify ignore rules or stage review artifacts unless the user explicitly requests it.

## Establish the baseline

1. Read applicable repository instructions.
2. Inspect tracked, staged, and untracked status and the overall diff statistics. Capture the exact set of paths that belong to the review before creating any review artifact.
3. Identify the requested comparison base. Do not silently substitute a different base.
4. Read the relevant diff, current specification or requirements, affected module documentation, tests, direct callers, and direct dependencies as needed.
5. Preserve the user's unrelated working-tree changes.
6. Determine whether the change is large or high risk.

For a confirmed recorded review, create the selected review directory after
freezing the baseline. Treat that directory as output-only: exclude it from later
repository-change status, diff, code-coverage, and finding calculations, and
never treat it as code under review. Continue to use `review.md` and
`coverage.md` as workflow evidence during authorized remediation, and continue
to report other user changes normally.

For a lightweight review, keep the exact comparison base and reviewed paths in
memory. Upgrade to a recorded review before producing artifacts only when the
inspection reveals cross-module or high-risk behavior, cannot be completed
reliably in one focused pass, or the user asks for a durable report. Apply the
recorded-mode recommendation and confirmation gate before that upgrade.

Treat a change as large or high risk when it crosses modules or changes persistence, migrations, state transitions, concurrency, background work, security, compatibility, or external side effects, or when it cannot be read reliably in one focused pass.

## Record high-risk coverage

For a large or high-risk review, maintain `coverage.md` in the current review directory. If the output directory cannot be written, keep an in-memory checklist and report that limitation rather than writing elsewhere.

Organize coverage by capability, call chain, or state machine—not by file count. For each area, inspect or mark with a reason:

- entry point and contract;
- source of truth and state transitions;
- persistence and external side effects;
- success path;
- failure, cancellation, retry, recovery, and restart paths;
- relevant tests and documentation.

Mark areas as checked, not applicable, or limited. Do not claim complete coverage while a high-risk area remains unchecked.

## Perform two review passes

### Pass 1: Contract and structure

Check that the implementation solves the stated problem and remains consistent with:

- requirements and current specifications;
- module boundaries and ownership;
- interfaces and externally visible responses;
- state machines and persistence ownership;
- migrations and backward compatibility;
- documentation and operational expectations.

### Pass 2: Adversarial behavior

Discard the assumption that the happy path succeeds. Check applicable cases:

- failure of each important await, commit, file write, or external call;
- partial effects before a later failure;
- auxiliary logging, metrics, cleanup, projection, or synchronization failing after the core commit;
- stale snapshots or request data overwriting newer runtime state;
- cancellation before the first event, after partial output, and near natural completion;
- retries, recovery, concurrent execution, and at-least-once delivery duplicating persistence or side effects;
- service restart while work is in an intermediate state;
- sensitive information escaping through responses, logs, files, or diagnostics.

Small low-risk changes may combine both perspectives in one pass, but must not omit applicable adversarial checks.

## Evaluate tests

Treat passing tests as evidence, not as proof of review completeness.

- Verify that assertions express the real contract.
- Check whether fixtures and mocks preserve important failure behavior.
- For state, concurrency, persistence, or side effects, look for failure injection, state combinations, duplicate execution, and recovery coverage.
- Use static analysis to assess uncovered paths.
- Record missing evidence as a validation gap or residual risk rather than inventing a confirmed defect.

## Classify findings

Assign impact independently from recommended action.

Impact:

- **Critical:** data loss, security exposure, production outage, repeated dangerous side effects, or core-flow breakage.
- **High:** important functional error, compatibility regression, inconsistent state, migration risk, or common reproducible failure.
- **Medium:** localized, boundary, or recoverable problem.
- **Low:** maintainability, documentation, coverage, or minor experience problem.

Action:

- **Must fix:** concrete evidence and a realistic path to incorrect behavior, state or data inconsistency, security exposure, compatibility regression, material user impact, or a critical evidence gap that prevents a safe change.
- **Should fix:** a real but limited issue with reliable mitigation, or mainly maintainability or minor experience impact.
- **May ignore:** a highly constrained and very unlikely case with no material business, data, security, or user impact.

Do not report theoretical speculation, style preference, or a concern without a plausible trigger as a finding.

## Deliver the review

For a lightweight review, report findings first in the final response with tight
file and line references, followed by meaningful validation gaps and residual
risks. Do not create `review.md` merely to record that no finding was found.

For a recorded review, write `review.md`. List findings first, grouped by `Must
fix`, `Should fix`, and `May ignore`, then ordered by impact. For every finding
include:

- identifier and concise title;
- file and tight line range;
- impact and action;
- code evidence;
- trigger and consequence;
- focused remediation direction.

After findings, summarize:

- validation performed and not performed;
- testing, manual-validation, or evidence gaps;
- covered capabilities or call chains for a large review;
- limited areas and residual risks;
- confidence based on evidence boundaries.

When no finding meets the evidence bar, say so plainly and still report meaningful gaps and residual risks. Do not imply that no defect can exist.

In the final response, summarize the highest-priority findings and link to
`review.md` and `coverage.md` only when those artifacts were created.
