# Authoring a Technical Specification

## Establish conventions and inputs

1. Use a user- or repository-specified output location when one is explicit.
2. Otherwise place specifications under the project-root `.write-technical-spec/`, using a short lowercase underscore-separated feature name.
3. Confirm that goals, scope, contracts, behavior, and acceptance criteria are sufficiently resolved. Investigate missing facts directly and ask only about unresolved material decisions.

Use the following default document set, respecting a narrower explicit request. Include `flow.md` only when requested or when multiple actors, asynchronous transitions, or failure and recovery paths benefit from a separate flow explanation:

```text
.write-technical-spec/
└── YYYY_MM_DD_feature_NNN/
    ├── flow.md          # optional
    ├── design.md
    └── implement.md
```

When updating an existing specification, locate candidates by feature scope, read their current documents, and reuse one only after confirming that it represents the same design effort. Confirm material scope expansion; do not repeat authorization for an ordinary continuation. Do not reuse a directory merely because its slug matches.

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

Continue to design when the flow follows resolved requirements. Ask only about unresolved material decisions or an explicitly requested review checkpoint.

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

Keep implementation detail out of `design.md`. Move file-by-file steps, algorithms, lock or temporary-file mechanics, recovery scans, release commands, test matrices, fixtures, mocks, and individual assertions into `implement.md`.

For high-risk behavior, state the principle and non-negotiable constraint in `design.md`; put the executable sequence and risk-relevant cases in `implement.md`.

## Review the design

Before writing the implementation plan:

1. Compare the design with repository rules, current code, module documentation, related specs, and the confirmed request.
2. Check module boundaries, state transitions, persistence, migrations, concurrency, idempotency, side effects, failure and recovery behavior, operations, security, privacy, compatibility, and testability.
3. Remove or relocate detail that belongs in the implementation plan.
4. Search for decision-changing uncertainty such as “could,” “recommended,” “default,” “prefer,” “decide during implementation,” “A or B,” or unresolved questions.
5. Directly fix wording and evidence omissions that do not change behavior.
6. Ask the user to decide any issue that changes semantics, contracts, scope, data, state, security, visible behavior, or acceptance.
7. Record a concise review note in the document.

Begin `implement.md` when material design decisions are resolved; do not ask again about decisions already authorized.

## Write the implementation plan

Use `implement.md` to describe execution:

- ordered phases and dependencies;
- files or modules to add or change and why;
- detailed algorithms and state transitions;
- persistence, locking, atomicity, compensation, recovery, and deployment mechanics;
- interface, schema, configuration, migration, and compatibility changes;
- testing strategy, test locations, fixtures, mocks, assertions, failure injection, and coverage matrix;
- validation commands and manual checks;
- documentation updates and final delivery checks.

When the work needs multiple independently executable phases, use:

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
implementation readiness. Report the verdict and link the documents together.
A request to author a specification does not itself authorize coding. If coding
was also authorized, return to it after blocking design issues are resolved;
otherwise deliver the specification and stop.
