# Remediating Review Findings

Read this reference only after the user explicitly authorizes fixing findings from a code review.

For a recorded review, use its existing
`.review-code-changes/YYYY_MM_DD_scope_NNN/` directory. Write remediation
progress and final evidence to `remediation.md`, link it from `review.md`, and
update finding statuses only when their actual implementation and validation
state changes. Do not create a separate review directory for the remediation
itself.

For a lightweight review, remediate directly from the findings reported in the
conversation. Keep progress and evidence in the conversation unless the user
requests a durable report or the remediation expands into large or high-risk
work; in that case, create a recorded-review directory with the original
baseline and findings only after explaining the upgrade, its evidence and
artifacts, and obtaining explicit user confirmation. If the user declines,
continue without persistent artifacts only when the remediation can still be
tracked and validated reliably.

## Confirm the remediation scope

1. Read the original review conclusion and baseline from the recorded artifacts
   or conversation.
2. Identify exactly which findings the user authorized.
3. Treat the confirmed set as the required closure boundary.
4. Do not silently include other findings or treat excluded findings as resolved, ignored, or deferred.
5. Invoke `$clarify-development-request` when the fix introduces unresolved product or technical decisions. After those decisions are confirmed, invoke `$write-technical-spec` when the user requests a specification or the repository's major-change rules require one.

## Revalidate each finding

Use current code rather than old line numbers or assumptions.

- Reproduce or statically confirm the trigger, root cause, and affected paths.
- Record when a finding no longer exists, was inaccurate, or was already resolved; do not change code merely to match the old report.
- Define the expected change, affected paths, acceptance criteria, and validation.
- Separate validation of the original defect from validation of risks introduced by the fix.
- Capture applicable invariants and forbidden outcomes for state, persistence, concurrency, security, and side effects.

## Implement within scope

- Fix the root cause and directly related paths, not only the visible symptom.
- Inspect direct callers, callees, shared state, parallel implementations, compatibility, tests, and documentation.
- Resolve regressions introduced by the remediation before delivery.
- Report unrelated pre-existing problems without modifying them.
- If a directly related issue expands the authorized write scope, explain the dependency and obtain confirmation before expanding.

Read-only investigation may extend beyond the write scope when necessary to understand and verify the fix.

## Validate and re-review

After each independently testable finding:

1. Run validation proportional to its risk and impact.
2. Reproduce the original failure or establish equivalent evidence.
3. Exercise directly related failure, state, concurrency, duplicate-execution, compatibility, and side-effect boundaries.

After all fixes, perform two distinct checks:

- **Remediation-diff review:** Inspect only the new fix for regressions, state-precedence errors, exception-order changes, repeated side effects, security problems, unrelated edits, and documentation drift.
- **Original-change review:** For a large or high-risk original change, revisit all high-risk capabilities and call chains from the original coverage record, not only the known findings. Rebuild the necessary coverage record if it was not retained.

Do not replace either review with passing tests. When a test fails, distinguish implementation defects, stale tests, environmental limits, and unrelated known failures. Do not weaken valid assertions or make production code conform to an incorrect test merely to get a pass.

Do not mark a finding resolved while required validation that is executable in the current environment remains incomplete. A finding may be resolved with explicit residual risk when only additional platform, production, or manual verification remains.

## Close and deliver

For a recorded review, write `remediation.md`. For each authorized finding,
report:

- actual result and changed area;
- original-defect evidence;
- fix-risk validation;
- incomplete or unverified work;
- residual risk and the condition required to continue.

List excluded original findings separately and leave their status unchanged. Report new out-of-scope findings separately.

For lightweight remediation, report the same evidence directly in the final
response without creating review artifacts.

If the findings belong to a persistent inspection report, update only that report using its status vocabulary and include actual code locations and validation evidence. Never mark unimplemented or unvalidated work as resolved.

In the final response, summarize the closure state and link to `review.md` and
`remediation.md` only when they exist.
