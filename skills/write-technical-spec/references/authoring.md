# Authoring a Technical Specification

## Establish conventions and inputs

1. Use a user- or repository-specified output location when one is explicit.
2. Otherwise place specifications under the project-root `.write-technical-spec/`, using a short lowercase underscore-separated feature name.
3. Confirm that goals, scope, contracts, behavior, and acceptance criteria are sufficiently resolved. Investigate missing facts directly and ask only about unresolved material decisions.

Default to one `design.md` containing the decisions, a concise implementation
outline, and validation strategy. Add `implement.md` only when independently
executable phases or substantial execution detail justify a separate plan. Add
`flow.md` only when requested or when a separate flow explanation materially
improves understanding. Respect the user's requested document set:

```text
.write-technical-spec/
└── YYYY_MM_DD_feature_NNN/
    ├── flow.md          # optional
    ├── design.md
    └── implement.md     # optional
```

When updating an existing specification, locate candidates by feature scope, read their current documents, and reuse one only after confirming that it represents the same design effort. Confirm material scope expansion; do not repeat authorization for an ordinary continuation. Do not reuse a directory merely because its slug matches.

Check the maintained sections and dependent documents against this Skill's
current authoring and readiness requirements, not only the latest design
change. For an overall revision, check the full requested document set.
Correct in-scope gaps and duplication while preserving confirmed decisions and
repository conventions. Existing useful document splits need not be merged
just because the default is now one file; report broader restructuring needs.

Treat a specification whose implementation is complete as a historical snapshot, not a description of current behavior. Update it only when continuing the same design effort or when the user explicitly asks; do not batch-rewrite completed specifications. Record implemented behavior in the repository's current implementation documentation, and when a specification conflicts with source or tests, treat source and tests as authoritative.

Use repository document conventions. Omit inapplicable sections. Use diagrams
only when they clarify the design.

For every independent new specification, start `NNN` at `000` and select the next unused sequence for the same date and feature. Never overwrite or silently merge an existing specification. Do not modify ignore rules or stage specification artifacts unless the user explicitly requests it.

## Write the flow document

Skip this section when the selected document set omits `flow.md`.

Use `flow.md` to explain the core processing flow, not detailed design.

- Start with a concise background, scope, and covered boundaries.
- Put a Mermaid-based core-flow overview near the beginning.
- Split important subflows into focused diagrams.
- Show primary data flow, triggers, branches, boundaries, failure, degradation, and recovery paths when applicable.
- Keep node labels short; move detailed meaning into notes, rules, or a small table after the diagram.
- Move tradeoffs, schemas, interfaces, algorithms, tests, and operational details to the appropriate later document.

Continue to design only when it is part of the requested document set and the
flow follows resolved requirements. For a flow-only request, review and deliver
that flow without creating additional documents. Ask only about unresolved
material decisions or a requested review checkpoint.

## Write the design document

Use `design.md` to answer what will change, why, where the boundaries lie, and which constraints must hold.

Cover applicable topics:

- background, goals, scope, and non-goals;
- current implementation and affected module boundaries;
- core flow, domain model, data, and state changes;
- public interfaces, configuration, and user-visible behavior;
- persistence, migration, deployment, and compatibility;
- security, privacy, concurrency, idempotency, recovery, and side-effect invariants;
- key decisions and tradeoffs;
- major risks and high-level validation strategy.

Keep enough implementation detail to establish feasibility and important
constraints. Avoid speculative file inventories and test scaffolding. If a
separate plan is justified, move detailed execution steps there and link to it
instead of repeating design decisions.

For high-risk behavior, state the invariant and the sequence that enforces it.
Describe validation for the important failure boundaries at the lowest useful
level; separate files are not a prerequisite for rigor.

## Review the design

Before delivery or writing a separate implementation plan:

1. Compare the design with repository rules, current code, module documentation, related specs, and the confirmed request.
2. Check module boundaries, state transitions, persistence, migrations, concurrency, idempotency, side effects, failure and recovery behavior, operations, security, privacy, compatibility, and testability.
3. Remove duplication and detail that does not help implementation.
4. Search for decision-changing uncertainty such as “could,” “recommended,” “default,” “prefer,” “decide during implementation,” “A or B,” or unresolved questions.
5. Directly fix wording and evidence omissions that do not change behavior.
6. Ask the user to decide any issue that changes semantics, contracts, scope, data, state, security, visible behavior, or acceptance.
7. Report material unresolved findings; do not add a review log to every document.

If a separate plan is needed, begin it when material design decisions are
resolved; do not ask again about decisions already authorized.

## Write the implementation plan

When a separate plan is justified, use `implement.md` to describe relevant execution details:

- ordered phases and dependencies;
- files or modules to add or change and why;
- detailed algorithms and state transitions;
- persistence, locking, atomicity, compensation, recovery, and deployment mechanics;
- interface, schema, configuration, migration, and compatibility changes;
- acceptance checks and key failure cases, with concrete setup or failure
  injection only where needed to show the behavior can be tested;
- validation commands and manual checks;
- documentation updates and final delivery checks.

Split a large plan into phase documents only when independently maintained
phases benefit from separate files; otherwise keep phases in one document:

```text
implement.md
implement_phase_1.md
implement_phase_2.md
...
```

Keep `implement.md` as an index with phase links, the overall validation strategy, and the complete file-change inventory. Put phase-specific steps and verification in the corresponding phase document.

## Review and deliver the requested document set

Self-review each document against the resolved requirements and relevant repository
evidence, correcting ordinary omissions directly. Reuse verified evidence across
documents; revisit it when changes invalidate it. Pause only the work dependent on
an unresolved material decision, or at a review checkpoint the user requested.
Do not require approval after every document or implementation phase.

When the requested set is complete, apply
[readiness-review.md](readiness-review.md) to check cross-document consistency and
implementation readiness, including one overall design simplification check.
Apply ordinary in-scope simplification directly. Ask before changing confirmed
design decisions, contracts, or scope. Report the verdict and remaining decisions;
link separate documents when they exist.
A request to author a specification does not itself authorize coding. If coding
was also authorized, return to it after blocking design issues are resolved;
otherwise deliver the specification and stop.
