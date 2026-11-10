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
5. **Test verifiability:** Connect acceptance criteria and high-risk invariants to focused tests or explicit manual checks. Specify setup, assertions, and failure injection only where needed to establish observability or a critical boundary. Reuse existing test infrastructure; do not require a Cartesian test matrix or duplicate the same evidence for every transition.
6. **Complexity and proportionality:** Apply the check below to the proposed design as a whole. A coherent, internally consistent design can still solve more than the requested problem or impose unnecessary operational cost.

## Check complexity and proportionality

Use the applicable questions below within the final review after each authoring
or update task, and during standalone review. Scale depth to material changes;
do not create an exhaustive inventory of trivial fields or require a new report.

Check that the specification includes the default implementation simplicity
constraint from the authoring guide, equivalent wording, or the user's explicit
alternative. Presence of that sentence does not replace reviewing the actual
design against the questions below.

- **Basis for added mechanisms:** For material new state, layers, abstractions,
  configuration, coordination, checks, retries, recovery paths, and migration
  steps, identify the requirement, external contract, existing failure, or
  concrete reachable failure path they address. Distinguish confirmed scope,
  repository constraints, and author-proposed behavior. Hypothetical future
  reuse or a generic appeal to safety is not sufficient justification.
- **Existing behavior and ownership:** Check the actual semantics and call paths
  of existing storage, lifecycle, authorization, execution, and recovery before
  duplicating them. Similar names do not establish equivalence. Prefer one owner
  for each fact and transition; explain a real gap when adding another record
  or state machine. Reuse is not mandatory when its coupling or adaptation costs
  exceed a smaller independent solution.
- **Proportionate safeguards:** Identify the trigger, consequence, and actual
  boundary protected by a safeguard. Consider the likelihood and impact supported
  by evidence, without inventing numerical risk estimates. Compare the benefit
  with added branches, state, user interruptions, false rejections, and recovery
  work. Accept bounded low-impact risk when appropriate; remove unnecessary
  protection instead of replacing it with a more elaborate mechanism. Preserve
  demonstrated authorization, data-integrity, and high-impact side-effect
  boundaries.
- **Scope and behavior expansion:** Look for new defaults, modes, approval steps,
  configuration knobs, compatibility paths, dynamic reconfiguration, rollout
  prerequisites, or changes to existing users and unattended work that were not
  required by the request. Do not present an author's conservative preference as
  a confirmed requirement. Resolve consequential choices explicitly, while
  deciding ordinary implementation details without extra permission requests.
- **Smallest complete alternative:** Compare a concrete simpler design when one
  is apparent: fewer independent states, existing lifecycle transitions, a
  narrower abstraction, fewer coordination points, or deletion of an unnecessary
  branch. Count implementation, testing, operation, migration, and user costs,
  not just lines of code. Preserve the requested behavior and all necessary call
  paths; silently dropping an entry point or recovery guarantee is not a
  simplification. Do not invent alternatives merely to fill a comparison table.

For a material finding, name the mechanism and location, its evidence or missing
basis, the consequence, and the specific simplification and tradeoff. When applying
a correction, update affected flows, contracts, plans, and validation criteria
together so removed complexity does not survive elsewhere.

Stop when material findings are resolved or clearly reported. Do not force a
reduction when the existing design is already the simplest complete solution,
add tests merely to justify unnecessary branches, or repeat the whole review
without a relevant change. Summarize the concrete simplifications made or why
remaining complexity is necessary; avoid an unsupported “simplicity checked”
claim. Optional refinements alone do not block readiness.

During authorized authoring or updates, apply local simplifications that preserve
confirmed design decisions, behavior, and scope. Ask only when a proposal changes
those decisions, contracts, acceptance criteria, or scope. Continue unaffected
work while awaiting the answer. Optional simplification alone is not an
implementation blocker. Standalone review remains read-only unless remediation
is explicitly authorized.

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
