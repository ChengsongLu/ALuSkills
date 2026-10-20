---
name: develop-with-tdd
description: Implement regression fixes, logic whose correctness cannot be judged by reading, and external contract changes with focused TDD, or use when TDD is explicitly requested. Skip routine CRUD, wiring, documentation, and other low-risk changes.
---

# Develop With TDD

Protect the behavior that most needs evidence with short red-green cycles. TDD
is an implementation technique here, not a ritual for every changed line and
not a separate artifact workflow.

## Select the scope

1. Read applicable repository instructions, the relevant requirement, current
   implementation, existing tests, and direct callers before editing.
2. Use TDD when the user explicitly requests it, or for:
   - regression defects;
   - logic whose correctness cannot be confirmed by reading it, such as state
     machines, concurrency, retry or recovery paths, and complex business rules;
   - changes to public interfaces or other externally consumed contracts.
3. Implement routine CRUD, wiring, configuration, documentation, formatting,
   and mechanical changes directly, then add focused tests where the risk
   warrants them. When one task mixes both kinds of work, apply TDD only to the
   critical behavior.
4. If meaningful TDD would require a new test harness or a broad testability
   refactor, explain the benefit, the cost, and a narrower validation
   alternative, then obtain confirmation before expanding the work.

Do not create planning or report files because this Skill applies, and do not
expand the user's requested scope.

## Write tests that matter

- Map each test to a confirmed requirement, acceptance criterion, historical
  defect, or concrete risk. Do not invent product behavior to make a test
  possible; ask when a remaining ambiguity would change visible behavior,
  contracts, state, or security.
- Test through the boundary closest to the real caller that is still cheap and
  deterministic: a public function, module entry point, API, event, persisted
  result, or user-visible outcome.
- Do not test private methods merely because they are easy to call, and do not
  expose internals or add abstractions, forwarding layers, or dependency
  injection solely to create a test hook.
- Mock only uncontrollable, slow, expensive, or externally side-effecting
  dependencies. Assert observable outcomes rather than chains of internal calls.
- Control time, randomness, ordering, and shared state so tests stay
  deterministic and independent.
- For persistent or side-effecting behavior, cover the most relevant failure
  boundary around the core commit point in addition to the main path: failure
  before commit, auxiliary failure after commit, or duplicate execution. A
  completed core side effect must not be repeated because later logging,
  cleanup, or synchronization fails.

## Run red-green cycles

1. **Red:** Write the tests for one behavior; its success and failure
   boundaries may be written together. Run the narrowest command and confirm
   each new test fails because the behavior is absent or the defect
   remains—not because of a bad assertion, fixture, mock, environment, or
   unrelated pre-existing failure. If a test unexpectedly passes, determine
   whether the behavior already exists or the test observes the wrong thing
   before changing production code.
2. **Green:** Make the smallest implementation change that passes those tests
   without breaking confirmed contracts or adjacent behavior. Rerun them.
3. **Refactor when useful:** If the green change introduced duplication or
   unclear responsibility, clean it up under the passing tests and rerun them.
   Skip this step when the diff is already minimal.
4. Move to the next behavior. Do not write tests for many unrelated behaviors
   before starting implementation.

For a defect, reproduce it through a stable external boundary before fixing it.
When an existing test conflicts with confirmed behavior, determine whether the
test or the implementation is stale; do not bend a correct contract or keep a
wrong implementation merely to make the suite green.

Do not describe work as TDD if the red run was not actually observed failing
for the intended reason. When the environment prevents a red or green run,
continue only as far as repository constraints allow and report the missing
evidence.

## Validate and report

1. Run the directly affected tests, then the smallest adjacent, integration, or
   contract checks the impact requires.
2. Review the final diff: remove tests that only pin private implementation
   details or duplicate other evidence, and check for an omitted high-risk
   failure boundary.
3. Follow repository-specific validation and delivery requirements.
4. Report, briefly per behavior, the red and green evidence actually observed,
   the final validation run, anything not run, and residual risk. Do not claim
   that passing tests prove untested states cannot fail.
