---
name: develop-with-tdd
description: Implement repository changes with selective, risk-driven test-driven development by mapping tests to confirmed behavior, choosing stable seams and appropriate test levels, and completing focused red-green-refactor cycles. Use when the user explicitly requests TDD or when implementing a regression fix, complex business rule, state transition, concurrency behavior, security boundary, external contract, or side effect where TDD materially reduces risk. Do not invoke for review-only work, test-only requests, documentation, simple configuration, mechanical edits, or other low-risk changes.
---

# Develop With TDD

Implement the behavior that needs protection through focused red-green-refactor
cycles. Apply TDD where its evidence is valuable; do not turn it into a ritual
for every changed line.

## Select the TDD scope

1. Read applicable repository instructions, requirements or specifications,
   current implementation, relevant tests, and direct callers before editing.
2. Use TDD when the user explicitly requests it. Otherwise use it only for
   behavior whose complexity or failure risk justifies the cycle, especially:
   - regression defects and complex business rules;
   - state transitions, concurrency, retries, or recovery;
   - persistence, external side effects, or security boundaries;
   - public interfaces and other externally consumed contracts.
3. Exclude documentation, comments, formatting, simple configuration,
   mechanical changes, and low-risk connection code unless they participate in
   a behavior that the selected test must exercise.
4. When one task mixes high- and low-risk work, apply TDD only to the critical
   behavior and use proportionate validation for the rest.

Treat TDD as an implementation technique, not a separate artifact workflow. Do
not create planning or TDD-report files merely because this Skill applies. Keep
the workflow self-contained: resolve its repository investigation and
decision-making directly, do not invoke or recommend external workflows, and
do not expand the user's requested scope.

If meaningful TDD would require a new test harness, a broad testability
refactor, or substantially higher delivery cost, explain the concrete benefit,
cost, and a narrower validation alternative, then obtain confirmation before
expanding the work.

## Confirm behavior and risk

Before writing a test, identify:

- the confirmed behavior or defect the test will protect;
- the observable result and stable boundary through which it can be verified;
- the realistic failure that the test prevents;
- the smallest useful success, boundary, or failure case.

Map every new test to a confirmed requirement, acceptance criterion, historical
defect, or concrete risk. Do not invent product behavior to make a test
possible. Investigate repository evidence first; when a remaining ambiguity
would change visible behavior, contracts, state, security, compatibility, or
acceptance, ask the user and pause the affected cycle.

Tests are implementation evidence, not a substitute for reviewing unmodeled
failure orderings, state combinations, side effects, or recovery paths.

## Choose the seam and test level

A useful test seam is a boundary that a real caller uses and a test can observe
or control reliably: a public interface, module entry point, API, event,
persistent result, task terminal state, or user-visible outcome.

- Prefer the seam closest to the real caller that can verify the behavior with
  acceptable cost and determinism.
- Use unit tests for isolated rules, integration tests for module cooperation,
  contract or API tests for external interfaces, and end-to-end tests only when
  a critical path cannot be protected more cheaply.
- Do not begin from a private method merely because it is easy to call. Test an
  internal algorithm directly only when it is itself a meaningful, complex
  rule.
- Do not expose private interfaces or introduce abstractions, compatibility
  layers, forwarding modules, or dependency injection solely to create a test
  hook.
- Use mocks or stubs only for dependencies that are uncontrollable, slow,
  expensive, or externally side-effecting. Prefer observable outcomes over a
  network of assertions about internal calls.
- Control time, randomness, execution order, and shared external state so that
  tests remain deterministic and independent.

For work crossing modules or layers, first select a minimal vertical slice from
the real entry point to the core result. Keep the slice small in data and
features without choosing temporary core boundaries, data models, or contracts
that the next increment must replace. Use it to validate module relationships
and the important seams before filling in secondary capabilities.

## Run focused red-green-refactor cycles

Complete one behavior or closely related risk boundary at a time:

1. **Red:** Add the smallest test that expresses the selected behavior. Run the
   narrowest command that exercises it and verify that it fails because the
   behavior is absent or the defect remains—not because of a bad assertion,
   fixture, mock, environment, syntax error, or unrelated pre-existing failure.
   If it unexpectedly passes, determine whether the behavior already exists or
   the test observes the wrong thing before changing production code.
2. **Green:** Make the smallest implementation change that satisfies the test
   without violating confirmed contracts, data boundaries, failure semantics,
   or adjacent behavior. Run the focused test again and verify that it passes.
3. **Refactor:** Remove relevant duplication and improve names or responsibility
   boundaries under the passing test. Do not add speculative abstractions or
   broaden the feature. Rerun the focused test after refactoring.
4. **Expand:** Select the next highest-value behavior or failure boundary and
   repeat. Avoid writing a large batch of unvalidated tests before starting the
   implementation.

Do not describe work as a completed TDD cycle if the red test was not actually
run and observed failing for the intended reason. When the environment prevents
either the red or green run, continue only as far as the user and repository
constraints allow, and report the missing evidence precisely.

## Protect state and side effects

For stateful, concurrent, asynchronous, persistent, or side-effecting behavior,
identify the core commit point and test the most relevant failure boundary in
addition to the main regression or success path. Depending on the risk, cover:

- failure before the core commit;
- auxiliary work failing after the core commit;
- cancellation, retry, duplicate delivery, or repeated execution;
- legal terminal-state convergence and prevention of duplicate side effects;
- restart or recovery from an intermediate state.

An already completed core side effect must not be repeated merely because
logging, metrics, cleanup, projection, or state synchronization fails later.
When concurrency or recovery cannot be automated reliably, record the manual
validation performed and the residual risk.

## Handle defects and legacy behavior

- For a defect, prefer a regression test through a stable external boundary.
  Verify that it reproduces the defect before applying the minimal fix.
- When legacy behavior is unclear, use a characterization test only when it
  provides needed protection. Label it conceptually as observed current
  behavior; do not treat history as proof of the correct requirement.
- When an existing test conflicts with confirmed behavior, inspect the source,
  assertion, fixture, and mocks to determine what is stale. Do not preserve an
  incorrect implementation or rewrite a correct contract merely to make the
  suite green.

## Validate and deliver

After the focused cycles:

1. Run the directly affected tests, then the smallest relevant adjacent,
   integration, or contract checks required by the impact.
2. Review the final diff and confirm that each new test protects behavior or a
   concrete risk rather than private implementation details.
3. Check for omitted high-risk failure boundaries and remove redundant tests
   that add maintenance cost without meaningful evidence.
4. Follow repository-specific validation and delivery requirements.
5. Report the behavior protected through TDD, the red and green evidence
   actually observed, the final validation run, anything not run, and residual
   risk. Do not claim that passing tests prove untested states cannot fail.
