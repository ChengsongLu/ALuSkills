# Workflows

## Contents

- Common preparation
- Initialize
- Navigate and retrieve
- Plan and implement a change
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
11. Write orientation, architecture foundations, and core runtime flows first.
12. Populate chapters in resumable batches. Track workflow status, explanatory
    coverage, and evidence status independently.
13. Build `index.md` with:
    - separate "understand the system" and "change the system" entry points;
    - a recommended first reading path and book map;
    - task, concept, source-area, state-machine, and contract navigation where
      applicable;
    - visible incomplete, stale, conflicted, and `needs-review` coverage.
14. Check that primary task paths identify conditional reading and source or
    test evidence.
15. Integrate concise maintenance guidance into the applicable repository Agent
    instruction file using `repository-rules.md`.
16. Generate `handbook.html`.
17. Run deterministic validation.
18. Perform a semantic review of coverage, evidence, terminology, links, and
    contradictions.

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
   2. prerequisite concepts and invariants;
   3. relevant flows and state machines;
   4. responsible modules;
   5. interfaces, state, or operations;
   6. cited source and tests.
5. Explain why each next item is relevant and what decision determines whether
   deeper reading is necessary.
6. Verify behavior in source when the answer affects a code change or when a
   chapter is `draft` or `needs-review`.

## Plan and implement a change

Use the full workflow below for changes likely to affect documented design,
responsibilities, flows, state, contracts, side effects, relationships, or
durable source evidence.

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

### Before changing code

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
7. Read the affected chapters before implementing.

### After changing code

1. Inspect the actual Git diff, including staged and unstaged changes.
2. Recalculate impact from what changed, not only what was planned.
3. For every candidate chapter, determine whether the change affected:
   - design or terminology;
   - responsibilities or boundaries;
   - runtime order or control flow;
   - state, data, failure, retry, cancellation, or recovery behavior;
   - interfaces, configuration, persistence, or side effects;
   - chapter relationships or source references.
4. Update only affected statements and mappings.
5. When only internal implementation changed, record that the chapter was
   inspected and avoid a meaningless prose diff.
6. Update coverage or evidence state when the change exposes missing depth,
   invalid evidence, or a new design surface.
7. Update the coverage inventory when responsibilities, flows, state machines,
   contracts, or operational surfaces appear, move, split, merge, or disappear.
8. Preserve protected and uncertain content. Add `needs-review` when required.
9. Regenerate `handbook.html` only when handbook Markdown, YAML, or managed
   assets changed.
10. Run deterministic validation after handbook source changes or when the user
    or repository instructions explicitly require it.
11. Report updated, inspected-but-unchanged, and unresolved chapters.

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
6. Check the human reading path and Agent task routes independently.
7. Re-read protected content only to detect conflicts; never rewrite it.
8. Update current-state documentation and remove stale current-state content
   according to the evolution workflow.
9. Regenerate `handbook.html`.
10. Run deterministic validation followed by semantic review.

## Evolve or remove content

Keep the handbook about the current system.

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
