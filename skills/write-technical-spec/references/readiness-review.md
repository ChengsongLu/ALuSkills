# Specification Readiness Review

Use this review once the requested specification is complete, or for a standalone review request. Recheck only affected dimensions after a correction; reuse evidence whose baseline is unchanged.

## Freeze the review baseline

Inventory before judging the specification:

- every in-scope specification document, including `flow.md`, `design.md`, `implement.md`, and phase documents;
- the confirmed request and any requirement, brief, decision, or acceptance source referenced by the specification;
- applicable repository instructions, documentation, source, configuration, tests, analogous modules, and earlier specifications;
- the current branch or revision and any relevant working-tree changes.

State material omissions or baseline ambiguity. In standalone review mode, remain read-only and report them instead of creating or correcting artifacts.

## Check implementation readiness

Review the requested document set against the frozen baseline. For a deliberately
limited deliverable (for example, only a flow), evaluate its requested abstraction
level and report what remains necessary for implementation; do not create extra
documents or treat an agreed omission as a defect merely to fill the default set.

Review these applicable dimensions:

1. **Requirement completeness:** Trace goals, scope, non-goals, constraints, dependencies, user decisions, and acceptance criteria into design decisions, implementation steps, and validation. Flag requirements with no implementation or verification path and plan steps with no requirement basis.
2. **Cross-document consistency:** Compare terminology, actors, boundaries, interfaces, schemas, state transitions, ordering, side effects, compatibility promises, file inventories, and phase dependencies. Treat later documents that silently contradict confirmed earlier decisions as blocking.
3. **Repository feasibility:** Resolve named files, symbols, interfaces, dependencies, commands, and test locations against the current repository. Check that sequencing, migration, deployment, rollback, compatibility, permissions, and operational assumptions are executable. Do not allow implementation to decide unresolved product or architectural behavior implicitly.
4. **State and failure boundaries:** Identify the source of truth, initial and terminal states, valid and invalid transitions, commit points, partial failures, retries, duplicate execution, idempotency, compensation, recovery, cancellation, and side-effect invariants wherever applicable. Require an explicit disposition for each meaningful failure branch.
5. **Test verifiability:** Trace every acceptance criterion, invariant, state transition, compatibility promise, and meaningful failure branch to a test or explicit manual check. Require the test level or location, setup or fixtures, action, assertions, failure injection or mocks when needed, validation command, and expected result. Flag behavior that cannot be observed deterministically.
6. **Overall design simplicity:** Check whether the design can be simplified to improve stability and reduce complexity while preserving confirmed requirements and necessary safeguards. Look for unnecessary layers, duplicated state or sources of truth, avoidable coordination, and redundant failure or recovery paths. For each concrete opportunity, explain the current design, proposed simplification, affected documents and exact changes, expected stability benefit, and tradeoffs. Do not recommend simplification merely to reduce document length or remove necessary safety mechanisms. If no justified simplification exists, say so explicitly.

For simplifications found during authoring or updates, present the proposed update
points to the user and obtain explicit confirmation before applying them, even
when they preserve observable behavior. Existing authorization to write or update
the specification does not approve these newly proposed simplifications. Continue
unaffected review work while awaiting confirmation. Apply only confirmed changes,
synchronize affected documents, and recheck affected review dimensions. If the
user declines, retain the existing design and report any remaining findings on
their merits; an optional simplification alone is not an implementation blocker.
In standalone review mode, report proposals without editing; confirmation must
also authorize remediation before any changes are made.

Recheck repository evidence immediately before issuing the verdict when the specification or relevant repository state changed during review.

## Report findings and verdict

Lead with findings ordered by severity. For each finding, provide the exact specification location, supporting repository evidence, implementation impact, and the decision or remediation required:

- **P1 — Blocking:** The specification would permit materially incorrect, unsafe, incompatible, or indeterminate implementation. Resolve it before coding.
- **P2 — Material:** A significant implementation, failure-handling, or verification gap exists, but it does not make the core direction unsafe or indeterminate.
- **P3 — Minor:** A localized clarity, organization, or non-blocking evidence issue exists.

Finish with exactly one implementation-readiness verdict:

- **READY:** No implementation-blocking or material findings remain.
- **READY WITH NON-BLOCKING FINDINGS:** Only explicitly identified non-blocking findings remain.
- **BLOCKED:** At least one P1 finding or unresolved decision remains.

Do not use user confirmation alone to override a `BLOCKED` verdict. Resolve the underlying issue or record an explicit change to the requirement, contract, or accepted risk, then repeat affected review dimensions. If no findings exist, say so explicitly and still summarize the reviewed baseline and residual testing or operational risks.

Use Markdown and the repository's established language. Include a table of contents for substantial documents. Do not provide effort or time estimates unless the user explicitly requests them.

In the final response, summarize the specification or reviewed baseline, report the implementation-readiness verdict, and link to the specification directory or index document when one exists.
