---
name: write-technical-spec
description: Create and review repository-grounded technical specifications for a feature, module, behavior change, or implementation plan. Use when the user asks for a technical spec, design document, flow document, implementation plan, design review, or to turn confirmed requirements into flow.md, design.md, implement.md, or phased implementation documents. Do not invoke merely because an ordinary coding task has a short plan.
---

# Write Technical Spec

Turn confirmed requirements and repository evidence into a staged technical specification that keeps process flow, design decisions, and implementation details at the correct level.

## Establish conventions and inputs

1. Read repository instructions, documentation conventions, current implementation, relevant tests, existing specifications, and analogous modules.
2. Use a user- or repository-specified output location when one is explicit.
3. Otherwise place specifications under the project-root `.write-technical-spec/`, using a short lowercase underscore-separated feature name.
4. Confirm that goals, scope, contracts, behavior, and acceptance criteria are sufficiently resolved. Invoke `$clarify-development-request` if a remaining choice would change the design.
5. Include a separate flow document when the user requests it, the project
   convention requires it, or multiple meaningful branches, boundaries, or
   failure paths make it materially useful. Otherwise omit it without asking;
   do not block a straightforward specification on an optional artifact.

Use the following default document set:

```text
.write-technical-spec/
└── YYYY_MM_DD_feature_NNN/
    ├── flow.md          # optional
    ├── design.md
    └── implement.md
```

When the user explicitly asks to continue or update an existing specification, locate candidates by feature scope, read their current documents, and reuse one only after confirming that it represents the same design effort. Do not reuse a directory merely because its slug matches.

For every independent new specification, start `NNN` at `000` and select the next unused sequence for the same date and feature. Never overwrite or silently merge an existing specification. Do not modify ignore rules or stage specification artifacts unless the user explicitly requests it.

## Write the flow document

Skip this section when the flow-document gate above omits `flow.md`.

Use `flow.md` to explain the core processing flow, not detailed design.

- Start with a concise background, scope, and covered boundaries.
- Put a Mermaid-based core-flow overview near the beginning.
- Split important subflows into focused diagrams.
- Show primary data flow, triggers, branches, boundaries, failure, degradation, and recovery paths when applicable.
- Keep node labels short; move detailed meaning into notes, rules, or a small table after the diagram.
- Move tradeoffs, schemas, interfaces, algorithms, tests, and operational details to the appropriate later document.

Obtain user confirmation before treating the flow as the basis for design.

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

For high-risk behavior, state the principle and non-negotiable constraint in `design.md`; put the executable sequence and exhaustive cases in `implement.md`.

## Review the design

Before writing the implementation plan:

1. Compare the design with repository rules, current code, module documentation, related specs, and the confirmed request.
2. Check module boundaries, state transitions, persistence, migrations, concurrency, idempotency, side effects, failure and recovery behavior, operations, security, privacy, compatibility, and testability.
3. Remove or relocate detail that belongs in the implementation plan.
4. Search for decision-changing uncertainty such as “could,” “recommended,” “default,” “prefer,” “decide during implementation,” “A or B,” or unresolved questions.
5. Directly fix wording and evidence omissions that do not change behavior.
6. Ask the user to decide any issue that changes semantics, contracts, scope, data, state, security, visible behavior, or acceptance.
7. Record a concise review note in the document.

Do not begin `implement.md` until the user confirms the design and no implementation-changing design decision remains.

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

## Review every stage

Before moving from one document or phase to the next:

- review the current document together with other relevant files in the same spec;
- confirm that important conversation decisions have been persisted;
- check for conflicts with current source and project rules;
- check completeness at the document's intended abstraction level;
- correct non-behavioral issues directly;
- obtain user confirmation for decision-changing corrections;
- retain a short record of the review dimensions and conclusion.

Before coding, ensure the plan is supported by current repository evidence, the documents agree, the user has confirmed the plan, and no design choice has been delegated implicitly to implementation.

Use Markdown and the repository's established language. Include a table of contents for substantial documents. Do not provide effort or time estimates unless the user explicitly requests them.

In each stage response, link to the current document. In the final response, summarize the confirmed specification and link to its directory or index document.
