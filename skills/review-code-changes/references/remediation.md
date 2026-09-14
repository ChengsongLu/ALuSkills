# Remediating Review Findings

Read this reference only after the user explicitly authorizes fixing findings from a code review.

For a recorded review, use its existing
`.review-code-changes/YYYY_MM_DD_scope_NNN/` directory. Write remediation
progress and final evidence to `remediation.md`, link it from `review.md`, and
update finding statuses only when their actual implementation and validation
state changes. Do not create a separate review directory for the remediation
itself.

For a conversation review, remediate directly from the findings reported in the
conversation. Keep progress and evidence in the conversation unless the user
requests a durable report or agrees to one because a concrete handoff need arises.
Risk determines validation depth, not whether artifacts are required. Continue
inspection and authorized remediation without waiting for a format decision.

## Confirm the remediation scope

1. Read the original review conclusion and baseline from the recorded artifacts
   or conversation.
2. Identify exactly which findings the user authorized.
3. Treat the confirmed set as the required closure boundary.
4. Do not silently include other findings or treat excluded findings as resolved, ignored, or deferred.
5. When the fix introduces unresolved product or technical decisions, investigate repository evidence and ask the user directly. If the requested remediation would expand into a new design effort or the repository requires a separate formal specification, stop before implementation, explain the required next activity in generic terms, and return control to the user.

## Revalidate each finding

Use current code rather than old line numbers or assumptions.

- Reproduce or statically confirm the trigger, root cause, and affected paths.
- Record when a finding no longer exists, was inaccurate, or was already resolved; do not change code merely to match the old report.
- Define the expected change, affected paths, acceptance criteria, and validation.
- Separate validation of the original defect from validation of risks introduced by the fix.
- Capture applicable invariants and forbidden outcomes for state, persistence, concurrency, security, and side effects.

## Review the fix design before implementation

Before editing, define the smallest root-cause fix and challenge it as an
attacker, a failing dependency, and a concurrent caller would. Inspect the
proposed change for applicable risks involving:

- trust boundaries, authorization, validation, canonicalization, injection,
  escaping, serialization, and sensitive-data exposure;
- privilege or access expansion, insecure defaults, fail-open behavior, and
  bypasses of existing security controls;
- partial failure, rollback, retries, duplicate execution, races, stale state,
  exception ordering, and repeated external side effects;
- compatibility changes that could cause callers to skip validation or fall
  back to unsafe behavior.

Prefer a narrow change that preserves existing invariants and security controls.
Define negative tests or equivalent static evidence for credible abuse and
failure cases, not only an expected success case. Revise the design before
implementation when it creates a plausible new vulnerability. If no safe design
can be established within the authorized scope, stop and obtain the missing
decision or scope authorization instead of applying a speculative fix.

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

After all fixes and their initial validation, discard the pre-fix conclusion and
perform a fresh review from the final combined diff and current affected code.
Perform both of these distinct checks:

- **Remediation-diff review:** Inspect only the new fix for regressions, state-precedence errors, exception-order changes, repeated side effects, security problems, unrelated edits, and documentation drift.
- **Original-change impact check:** Reuse valid prior review evidence. Revisit original capabilities when the fix changes their assumptions, shared invariants, or relevant baseline; expand further only when that evidence warrants it.

Apply the contract-and-structure and adversarial perspectives from the main
review workflow during this fresh review. Trace changed trust boundaries and
direct callers or callees far enough to detect vulnerabilities or regressions
that are not visible in the remediation hunk alone.

Treat every credible issue found during re-review as an active finding. Resolve
issues introduced by the remediation, rerun the affected validation, and review
the updated diff and affected paths. Reuse unaffected review evidence. Do not close while a remediation-caused
correctness, reliability, security, compatibility, or side-effect problem
remains. Report unrelated or out-of-scope findings without silently modifying
them.

Do not replace either review with passing tests. When a test fails, distinguish implementation defects, stale tests, environmental limits, and unrelated known failures. Do not weaken valid assertions or make production code conform to an incorrect test merely to get a pass.

Do not mark a finding resolved while required validation that is executable in the current environment remains incomplete. A finding may be resolved with explicit residual risk when only additional platform, production, or manual verification remains.

## Close and deliver

For a recorded review, write `remediation.md`. For each authorized finding,
report:

- actual result and changed area;
- original-defect evidence;
- fix-risk validation;
- final re-review results and any resulting fix-and-review iterations;
- incomplete or unverified work;
- residual risk and the condition required to continue.

List excluded original findings separately and leave their status unchanged. Report new out-of-scope findings separately.

For conversation remediation, report the same evidence directly in the final
response without creating review artifacts.

If the findings belong to a persistent inspection report, update only that report using its status vocabulary and include actual code locations and validation evidence. Never mark unimplemented or unvalidated work as resolved.

In the final response, summarize the closure state and link to `review.md` and
`remediation.md` only when they exist.
