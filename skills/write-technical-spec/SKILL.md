---
name: write-technical-spec
description: Assess, create, update, or review repository-grounded technical specifications, including a read-only preimplementation review of requirements, cross-document consistency, feasibility, state and failure boundaries, and test verifiability. Use when the user asks whether a spec is needed, requests a technical spec, design, flow, implementation plan, design review, implementation-readiness review, or wants confirmed requirements turned into flow.md, design.md, implement.md, or phased implementation documents. Do not invoke merely because an ordinary coding task has a short plan.
---

# Write Technical Spec

Assess, create, update, or review a technical specification using current repository evidence. Keep creation, revision, and read-only review distinct; make the workflow self-contained and do not delegate any part of it to another Skill.

## Select the operating mode

Read enough repository and specification context to select one mode before taking action:

- **Create:** Assess whether the task needs a specification, then use the entry and document-set gates below.
- **Update:** Locate the existing specification by scope and evidence, confirm it is the same design effort, and edit only within the user's authorized scope. Reapply the gates only for a material scope or document-set change.
- **Review:** Inspect an existing specification for implementation readiness. Treat a review request as read-only unless the user explicitly asks for remediation; do not edit specifications, source, tests, repository metadata, or persistent review artifacts.

Do not send review requests through the creation gates. If the target specification or requested review baseline cannot be identified safely, ask the user for the missing location or scope.

Resolve missing inputs within this Skill. Investigate repository facts first. When a remaining choice would change semantics, contracts, scope, data, state, security, visible behavior, compatibility, or acceptance criteria, explain the unresolved decision and its impact, then ask the user directly. Do not continue past the affected gate until it is resolved. Leave reversible local implementation choices to the plan when they cannot affect observable behavior or acceptance.

## Assess whether to enter the specification workflow

1. Read repository instructions, documentation conventions, current implementation, relevant tests, existing specifications, and analogous modules.
2. Assess actual complexity and risk rather than using file count or request length as a proxy. Consider:
   - changes to public contracts, user-visible behavior, data, state, or schemas;
   - coordination across modules, services, processes, or external systems;
   - concurrency, security, privacy, migration, compatibility, deployment, or rollback concerns;
   - multiple meaningful branches, failure modes, recovery paths, or side effects;
   - unresolved tradeoffs that implementation should not decide implicitly.
3. Recommend entering the specification workflow when several of these concerns interact, when the change has material risk, or when repository rules require a spec. Recommend skipping it for localized, low-risk work whose behavior and validation are already clear.
4. Present the recommendation, its task-specific reasons, and the expected artifact set at a high level. Explicitly ask the user to confirm whether to enter the specification workflow.
5. Do not create a specification directory or write specification artifacts before the user confirms this gate. If the user confirms skipping the workflow, stop this skill and hand off to the requested next activity.

Treat an earlier request for a specification as intent to assess and propose the workflow, not as confirmation of the evidence-based recommendation. A user may explicitly waive the gate or direct a mandatory repository workflow; otherwise obtain confirmation after presenting the recommendation.

## Confirm whether the specification needs a flow document

Perform this gate only after the user confirms entering the specification workflow.

1. Recommend including `flow.md` when the user or repository requires it, or when a diagram and flow-focused review would materially clarify multiple actors, boundaries, asynchronous transitions, branches, failure, degradation, compensation, or recovery paths.
2. Recommend omitting `flow.md` when the change is predominantly a localized structural or contract design with a short linear path that `design.md` can explain clearly.
3. Explain the recommendation using the task's actual flow complexity and name the proposed document set.
4. Explicitly ask the user to confirm whether to include `flow.md`.
5. Do not create or write any specification artifacts until the user confirms this second gate.

Honor an explicit user waiver or an already confirmed repository-mandated document set. Do not infer confirmation merely because the user initially requested a flow document; present the repository-grounded recommendation first.

## Establish conventions and inputs

1. Use a user- or repository-specified output location when one is explicit.
2. Otherwise place specifications under the project-root `.write-technical-spec/`, using a short lowercase underscore-separated feature name.
3. Confirm that goals, scope, contracts, behavior, and acceptance criteria are sufficiently resolved. Handle unresolved decisions using the self-contained rule above.

Use the following default document set:

```text
.write-technical-spec/
└── YYYY_MM_DD_feature_NNN/
    ├── flow.md          # optional
    ├── design.md
    └── implement.md
```

When updating an existing specification, locate candidates by feature scope, read their current documents, and reuse one only after confirming that it represents the same design effort. Apply the entry and flow gates to material scope or document-set changes; do not repeat them for a straightforward continuation whose workflow and document set the user already confirmed. Do not reuse a directory merely because its slug matches.

For every independent new specification, start `NNN` at `000` and select the next unused sequence for the same date and feature. Never overwrite or silently merge an existing specification. Do not modify ignore rules or stage specification artifacts unless the user explicitly requests it.

## Write the flow document

Skip this section when the confirmed document set omits `flow.md`.

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

After completing each document or implementation phase, perform a self-review before presenting it for confirmation. Before moving from one document or phase to the next, or from the specification to coding:

- review the current document together with other relevant files in the same spec;
- confirm that important conversation decisions have been persisted;
- check for conflicts with current source and project rules;
- check completeness at the document's intended abstraction level;
- check internal consistency, actionable detail, evidence support, and agreement with previously confirmed documents;
- correct non-behavioral issues directly;
- obtain user confirmation for decision-changing corrections;
- retain a short record of the review dimensions and conclusion.

Report the self-review conclusion and link the completed document when asking the user to confirm the stage. Do not start the next document, phase, or coding until the self-review is complete, blocking issues are resolved, and the user confirms the current stage.

After the implementation plan is complete, run the whole-spec preimplementation review below. Do not start coding until its blocking issues are resolved, its repository baseline is still current, and the user confirms the implementation-ready specification.

## Run the whole-spec preimplementation review

Use this review both as the final gate for a specification created or updated by this Skill and as the complete workflow for a standalone review request.

### Freeze the review baseline

Inventory before judging the specification:

- every in-scope specification document, including `flow.md`, `design.md`, `implement.md`, and phase documents;
- the confirmed request and any requirement, brief, decision, or acceptance source referenced by the specification;
- applicable repository instructions, documentation, source, configuration, tests, analogous modules, and earlier specifications;
- the current branch or revision and any relevant working-tree changes.

State material omissions or baseline ambiguity. In standalone review mode, remain read-only and report them instead of creating or correcting artifacts.

### Check implementation readiness

Review the complete document set against the frozen baseline:

1. **Requirement completeness:** Trace goals, scope, non-goals, constraints, dependencies, user decisions, and acceptance criteria into design decisions, implementation steps, and validation. Flag requirements with no implementation or verification path and plan steps with no requirement basis.
2. **Cross-document consistency:** Compare terminology, actors, boundaries, interfaces, schemas, state transitions, ordering, side effects, compatibility promises, file inventories, and phase dependencies. Treat later documents that silently contradict confirmed earlier decisions as blocking.
3. **Repository feasibility:** Resolve named files, symbols, interfaces, dependencies, commands, and test locations against the current repository. Check that sequencing, migration, deployment, rollback, compatibility, permissions, and operational assumptions are executable. Do not allow implementation to decide unresolved product or architectural behavior implicitly.
4. **State and failure boundaries:** Identify the source of truth, initial and terminal states, valid and invalid transitions, commit points, partial failures, retries, duplicate execution, idempotency, compensation, recovery, cancellation, and side-effect invariants wherever applicable. Require an explicit disposition for each meaningful failure branch.
5. **Test verifiability:** Trace every acceptance criterion, invariant, state transition, compatibility promise, and meaningful failure branch to a test or explicit manual check. Require the test level or location, setup or fixtures, action, assertions, failure injection or mocks when needed, validation command, and expected result. Flag behavior that cannot be observed deterministically.

Recheck repository evidence immediately before issuing the verdict when the specification or relevant repository state changed during review.

### Report findings and verdict

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

In each authoring stage response, link to the current document. In the final response, summarize the confirmed specification or reviewed baseline, report the implementation-readiness verdict, and link to the specification directory or index document when one exists.
