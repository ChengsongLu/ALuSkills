---
name: review-code-changes
description: Review a requested code diff for logic, correctness, and related risks, or remediate its findings when authorized. Skip routine implementation self-checks and whole-codebase audits.
---

# Review Code Changes

Review changed code against its intended contract and adversarial failure
conditions. Report actionable findings with evidence and keep implementation
files read-only during review-only work.

## Select the mode

- **Conversation review (default):** Report findings in the conversation; keep
  any coverage checklist in memory.
- **Recorded review:** Only when the user requests a persistent report, or
  agrees to one because durable handoff evidence is needed. Risk alone does not
  require files, and choosing a format never pauses code inspection.
- **Remediation:** Only when the user explicitly asks to fix identified
  findings. Read [references/remediation.md](references/remediation.md)
  completely before modifying code, adversarially assess the proposed fix
  first, and re-review the final remediation diff and affected paths after
  validation. Do not close remediation while that review finds a credible
  defect introduced by the fix.

This workflow covers logic, correctness, and related reliability, security,
compatibility, test, and documentation risks in changed code. A PR or branch is
only a source for the comparison diff; do not turn this into PR approval,
CI-status, merge-readiness, or repository-wide inspection work.

## Establish the baseline

1. Read applicable repository instructions.
2. Inspect tracked, staged, and untracked status and diff statistics, and fix
   the exact set of paths under review.
3. Use the requested comparison base; never silently substitute another.
4. Read the relevant diff, current requirements or specifications, affected
   module documentation, tests, direct callers, and direct dependencies.
5. Preserve unrelated working-tree changes.
6. Decide whether the change is large or high risk from changed contracts,
   state, persistence, concurrency, security, and external effects—not from the
   number of modules touched. Increase depth when evidence reveals risk;
   depth never changes the output mode.

For a recorded review, create the output only after the baseline is fixed. Use
a user- or repository-specified location, or by default:

```text
.review-code-changes/
└── YYYY_MM_DD_scope_NNN/
    ├── review.md
    ├── coverage.md       # large or high-risk reviews only
    └── remediation.md    # only after authorized remediation
```

Use `working-tree`, a short commit or branch slug, or another unambiguous slug
for `scope`; start `NNN` at `000` and take the next unused sequence. Record the
comparison base inside `review.md`. Exclude the review directory from all later
status, diff, and finding calculations. If it cannot be written, keep the
checklist in memory and report the limitation. Do not modify ignore rules or
stage review artifacts unless the user explicitly asks.

## Track high-risk coverage

For a large or high-risk review, keep a coverage checklist organized by
capability, call chain, or state machine. For each area, mark checked, not
applicable, or limited: entry point and contract; source of truth and state
transitions; persistence and external side effects; success path; failure,
cancellation, retry, recovery, and restart paths; relevant tests and
documentation. Do not claim complete coverage while a high-risk area remains
unchecked.

## Review in two passes

**Contract and structure:** Confirm the change solves the stated problem and
stays consistent with requirements and specifications, module ownership,
interfaces and visible responses, state machines and persistence ownership,
migrations and compatibility, and documentation and operations.

**Adversarial behavior:** Drop the assumption that the happy path succeeds and
check applicable cases: failure of each important await, commit, write, or
external call; partial effects before a later failure; auxiliary logging,
metrics, cleanup, or synchronization failing after the core commit; stale
snapshots overwriting newer state; cancellation before the first event, after
partial output, and near completion; retries, recovery, concurrency, and
at-least-once delivery duplicating effects; restart in an intermediate state;
sensitive data escaping through responses, logs, files, or diagnostics.

Small low-risk changes may combine both passes but must not omit applicable
adversarial checks.

Treat passing tests as evidence, not proof. Check that assertions express the
real contract, that fixtures and mocks preserve important failure behavior,
and, for state or side effects, whether failure injection, duplicate execution,
and recovery are covered. Record missing evidence as a validation gap or
residual risk rather than inventing a defect.

## Classify findings

Impact:

- **Critical:** data loss, security exposure, outage, repeated dangerous side
  effects, or core-flow breakage.
- **High:** important functional error, compatibility regression, inconsistent
  state, migration risk, or common reproducible failure.
- **Medium:** localized, boundary, or recoverable problem.
- **Low:** maintainability, documentation, coverage, or minor experience issue.

Action:

- **Must fix:** concrete evidence and a realistic path to incorrect behavior,
  inconsistent data, security exposure, compatibility regression, material user
  impact, or a critical evidence gap that prevents a safe change.
- **Should fix:** a real but limited issue with reliable mitigation, or mainly
  maintainability or minor experience impact.
- **May ignore:** a highly constrained, very unlikely case with no material
  business, data, security, or user impact.

Do not report speculation, style preference, or a concern without a plausible
trigger as a finding.

## Deliver

List findings first, grouped by action and ordered by impact. For each give an
identifier and title, file and tight line range, impact and action, code
evidence, trigger and consequence, and a focused remediation direction. Then
summarize validation performed and not performed, evidence gaps, covered call
chains for a large review, limited areas, residual risks, and confidence.

In conversation mode, deliver this in the final response. In recorded mode,
write it to `review.md` and summarize the highest-priority findings in the
final response with links to the artifacts actually created. Do not create
`review.md` merely to record that nothing was found. When no finding meets the
evidence bar, say so plainly, still report meaningful gaps, and do not imply
that no defect can exist.
