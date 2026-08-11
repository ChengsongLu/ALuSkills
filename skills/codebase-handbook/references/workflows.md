# Workflows

## Contents

- Common preparation
- Initialize
- Navigate and retrieve
- Assess handbook impact around a code change
- Incrementally validate
- Fully audit
- Evolve or remove content
- Resume interrupted work

## Common preparation

1. Resolve the project root.
2. Inspect Git status and preserve unrelated changes.
3. If `.codebase-handbook/` exists, read `config.yaml`, `preferences.md`,
   `manifest.yaml`, and `index.md` in that order.
4. Resolve the active language and scope.
5. Use Git-tracked files as the default source inventory.
6. Treat source code, configuration, migrations, and tests as evidence of
   current behavior.
7. Treat README files, maintained module documents, comments, and historical
   specifications as evidence of intent that requires verification.
8. Record conflicts instead of silently choosing a convenient account.

## Initialize

Initialize only after an explicit request.

1. Confirm the project root.
2. Run `scripts/initialize_handbook.py`.
3. Read `preferences.md` before discovery.
4. Inventory tracked source, configuration, migrations, tests, entry points,
   existing documentation, and build or runtime metadata.
5. Exclude vendor code, generated files, caches, binaries, and build products.
6. Establish concepts, module boundaries, runtime flows, interfaces, state,
   external dependencies, and operational concerns.
7. Build `coverage_inventory` before planning chapters. Include source
   responsibility areas, important flows, persisted state machines, external
   contract groups, and operational surfaces.
8. Define the book's parts and primary human reading paths.
9. Decompose chapters using lifecycle, state ownership, failure model, and
   developer change-task boundaries. Do not collapse distinct topics only to
   keep the chapter count small.
10. Complete the chapter inventory and relationships before deep writing.
11. Present the evidence-based initialization plan: scope and exclusions,
    coverage inventory, parts, chapters, reading paths, relationships, and
    proposed writing batches. Explain the recommendation and explicitly ask the
    user to confirm it.
12. Treat the explicit initialization request as authorization for the empty
    skeleton and read-only discovery, not as confirmation of the discovered
    book structure. Keep the proposed inventory and structure in memory; do not
    begin deep writing until the user confirms the plan.
13. Write orientation, architecture foundations, and core runtime flows first.
14. Analyze evidence completely, then draft chapters as explanations rather
    than preserving source-discovery or call order. Populate chapters in
    resumable batches and track workflow status, explanatory coverage, and
    evidence status independently.
15. Run the editorial compression pass from `evidence-and-writing.md` on each
    completed batch. Consolidate repeated facts, replace repeated exact mappings
    with tables, move analysis-only detail out of prose, and preserve manifest
    coverage and evidence mappings.
16. Build `index.md` with:
    - separate "understand the system" and "change the system" entry points;
    - a recommended first reading path and book map;
    - task, concept, source-area, state-machine, and contract navigation where
      applicable;
    - visible incomplete, stale, conflicted, and `needs-review` coverage.
17. Check that primary task paths identify conditional reading and source or
    test evidence.
18. Generate `handbook.html`.
19. Run deterministic validation.
20. Perform a semantic review of coverage, evidence, terminology, links,
    contradictions, and expression quality.

Do not claim initialization is complete until every in-scope topic is covered
at the required status.

## Navigate and retrieve

Use the handbook as a decision index, not as a substitute for source inspection.

1. Classify the task by project concept, module, runtime flow, interface,
   operational concern, or combination.
2. Start with `index.md`.
3. Use `manifest.yaml` to resolve candidate chapters and source evidence.
4. Produce or follow a reading plan in this order:
   1. task index or system reading path;
   2. manifest `summary`, `concepts`, and `read_when` for candidate selection;
   3. prerequisite concepts and invariants;
   4. relevant flows and state machines;
   5. responsible modules;
   6. interfaces, state, or operations;
   7. manifest `sources`, `source_symbols`, and cited tests.
5. Explain why each next item is relevant and what decision determines whether
   deeper reading is necessary.
6. Verify behavior in source when the answer affects a code change or when a
   chapter is `draft` or `needs-review`.
7. Do not parse `handbook.html` for Agent routing when the Markdown and manifest
   sources are available. HTML is a human reading projection, not a separate
   evidence source.

## Assess handbook impact around a code change

Use the full workflow below for changes likely to affect documented design,
responsibilities, flows, state, contracts, side effects, relationships, or
durable source evidence.

Treat the source change as separately authorized work outside this skill. Read
repository content to assess impact, but write only handbook files under
`.codebase-handbook/`.

When repository instructions require handbook consultation for a small,
localized change, use a lightweight impact check:

1. Read `index.md` and only the `manifest.yaml` entries matched by the intended
   paths or symbols.
2. Inspect a chapter only when its `sources` or `update_triggers` match, or when
   the diff reveals a documented behavior change.
3. Expand to the full workflow only when evidence shows a material handbook
   impact or an unresolved boundary.
4. If the final diff changes no durable handbook subject or cited symbol, make
   no handbook edit and do not rebuild or validate `handbook.html`. Report that
   the lightweight check found no synchronization need.

### Before an authorized code change

1. Inspect the task and handbook navigation.
2. Identify directly responsible modules and flows.
3. Resolve relevant coverage-inventory entries and change-task routes.
4. Expand through upstream, downstream, shared state, interfaces, state
   machines, invariants, and side effects.
5. Match likely source changes against `sources` and `update_triggers`.
6. Produce an impact checklist with:
   - chapters that must be inspected;
   - conditional chapters and the condition;
   - relevant source evidence;
   - unresolved scope questions.
7. Read the affected chapters before the separately authorized implementation
   begins.

### After an authorized code change

1. Inspect the actual Git diff, including staged and unstaged changes.
2. Recalculate impact from what changed, not only what was planned.
3. For every candidate chapter, determine whether the change affected:
   - design or terminology;
   - responsibilities or boundaries;
   - runtime order or control flow;
   - state, data, failure, retry, cancellation, or recovery behavior;
   - interfaces, configuration, persistence, or side effects;
   - chapter relationships or source references.
4. When invocation was implicit, present the actual impact, recommend the
   chapters and mappings to update, and explicitly ask the user to confirm
   before writing. Treat an explicit handbook-update request or a repository
   rule that mandates synchronization as authorization for ordinary scoped
   updates, but obtain confirmation when actual impact materially expands that
   scope.
5. Update only affected statements and mappings within the confirmed scope.
6. When only internal implementation changed, record that the chapter was
   inspected and avoid a meaningless prose diff.
7. Update coverage or evidence state when the change exposes missing depth,
   invalid evidence, or a new design surface.
8. Update the coverage inventory when responsibilities, flows, state machines,
   contracts, or operational surfaces appear, move, split, merge, or disappear.
9. Preserve protected and uncertain content. Add `needs-review` when required.
10. Apply the editorial compression pass to materially changed prose without
    broadening the confirmed scope or rewriting unaffected sections.
11. Regenerate `handbook.html` only when handbook Markdown, YAML, or managed
    assets changed.
12. Run deterministic validation after handbook source changes or when the user
    or repository instructions explicitly require it.
13. Report updated, inspected-but-unchanged, and unresolved chapters.

## Incrementally validate

Run after a related code or handbook change.

1. Validate required files, Schema versions, Markdown links, manifest chapter
   paths, source paths, and the `handbook.html` source hash.
2. Inspect all chapters matched by changed sources or update triggers.
3. Confirm related links and manifest relationships still agree.
4. Verify changed prose against source, tests, configuration, and migrations.
5. State explicitly that script validation does not prove semantic accuracy.

## Fully audit

Run after initialization, a major structural change, a long maintenance gap, or
an explicit request.

1. Rebuild the tracked-file inventory.
2. Compare current modules, flows, state machines, interfaces, and operational
   surfaces with `coverage_inventory`.
3. Find uncovered, orphaned, duplicated, over-broad, under-explained, or
   obsolete topics.
4. Reapply chapter decomposition rules; split summary chapters that combine
   distinct lifecycles, owners, failure models, or change tasks.
5. Check all chapter workflow statuses, coverage levels, evidence statuses,
   terminology, source evidence, relationships, and unresolved items.
6. Apply the editorial compression pass across chapter boundaries: identify
   source-traversal prose, duplicated explanations, over-expanded ordinary
   failures, and evidence references that interrupt the reading path. Preserve
   complete manifest coverage while making only evidence-driven local edits.
7. Check the human reading path and Agent task routes independently.
8. Re-read protected content only to detect conflicts; never rewrite it.
9. Update current-state documentation and remove stale current-state content
   according to the evolution workflow.
10. Regenerate `handbook.html`.
11. Run deterministic validation followed by semantic review.

## Evolve or remove content

Keep the handbook about the current system.

Before writing, present the repository evidence, recommended structural action,
affected chapter IDs and relationships, content migration or preservation plan,
and expected navigation impact. Explicitly ask the user to confirm the
evidence-based plan; an earlier request to evolve the handbook is intent to
assess, not confirmation of the resulting structure. Do not rename, split,
merge, deprecate, remove, or archive content before confirmation unless the
user explicitly waives this gate.

Within the confirmed plan:

1. For a rename, keep the chapter ID stable when the underlying concept remains
   the same.
2. For a split, create new stable IDs, migrate relevant prose, update inbound
   and outbound relationships, then remove the obsolete chapter.
3. For a merge, preserve unique valid information, choose one stable surviving
   ID when possible, and update all references.
4. For a deletion, verify that the concept no longer exists, migrate any still
   valid design rationale, update inbound links, and remove obsolete prose.
5. Let Git preserve history. Create explicit archives only when the user asks,
   and label them as non-current.

## Resume interrupted work

1. Re-read current user instructions and handbook preferences.
2. Inspect Git status and current handbook files.
3. Treat `manifest.yaml` statuses as hints, not proof.
4. Recheck repository changes since the interrupted work began.
5. Revalidate any chapter that may have become stale.
6. Continue from the earliest incomplete dependency rather than blindly
   continuing the last textual step.
