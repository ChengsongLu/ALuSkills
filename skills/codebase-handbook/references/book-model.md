# Book Model and Coverage Design

## Contents

- Two coordinated reading planes
- Required discovery model
- Book hierarchy
- Chapter types
- Decomposition rules
- Coverage inventory
- Agent indexes
- Completion standard

## Two coordinated reading planes

Build one canonical body of chapters and expose it through two reading planes.
Do not create duplicate prose for Agents and humans.

### Human book plane

Organize the handbook as a coherent technical book. Let a reader move from
orientation, through architecture and runtime behavior, into subsystem design,
interfaces, and operation. Use parts, prerequisites, chapter order, and
cross-references to preserve narrative continuity. Render this plane through
the authored Markdown and `handbook.html`. In the HTML view, foreground the
functional summary and main reading path; keep verification and synchronization
metadata available without making it compete with the explanation.

### Agent navigation plane

Let an Agent begin with a task, concept, source area, state machine, or external
contract and resolve:

1. what to read first;
2. which related chapters are conditional;
3. which source and tests provide evidence;
4. which invariants and boundaries must remain true;
5. which chapters must be inspected after a change.

Store these routes in `index.md` and machine-readable manifest fields. Link them
to the same chapters used by the human book. Route from manifest chapter
summaries, concepts, `read_when`, relationships, sources, stable symbols, and
update triggers before opening broad prose. Inspect the cited source and tests
when answering a code-change question; generated HTML is not an Agent evidence
source.

The two planes share knowledge but do not require identical presentation.
Manifest metadata is a compact route to the canonical chapter and repository
evidence, while HTML is a human-oriented projection of that chapter. Do not
create a second body of explanatory prose for either plane.

## Required discovery model

Before writing chapters, build a knowledge map covering:

- system purpose and external boundaries;
- architectural layers and dependency direction;
- top-level source and runtime modules;
- entry points, startup, shutdown, and composition;
- important end-to-end request and background flows;
- persisted or long-lived state machines;
- ownership of data and facts;
- extension mechanisms;
- external interfaces and side effects;
- configuration, security, observability, testing, and operation.

Use existing documentation as a discovery aid, not as proof of current
behavior. Verify it against source, configuration, migrations, and tests.

Do not mark discovery complete merely because every visible top-level directory
has been named. Group files by design responsibility and split a directory when
it contains materially different responsibilities.

## Book hierarchy

Use `parts` for narrative organization and `chapters` for stable addressable
topics. A typical large repository may use:

1. Orientation and reading guide
2. Architecture foundations
3. Runtime and request lifecycles
4. Subsystem design
5. State, data, and contracts
6. Extension and development
7. Testing, operation, and deployment
8. Appendices and indexes

Adapt names and count to the repository. Do not force empty parts.

Keep `chapter.id` stable across title or path changes. Use `chapter.part` and
`chapter.order` to control reading order without encoding order in the ID.

## Chapter types

Choose a type by the question the chapter answers:

- `orientation`: how to approach the system or book;
- `concept`: vocabulary and mental models;
- `architecture`: boundaries, layers, topology, or dependency direction;
- `module`: a subsystem's purpose, responsibilities, and collaboration;
- `flow`: a multi-stage runtime sequence across participants;
- `state-machine`: states, transitions, ownership, idempotency, and recovery;
- `interface`: an external or cross-module contract;
- `decision`: a durable design choice and its constraints;
- `guide`: a safe change or extension path;
- `operation`: development, testing, deployment, or incident behavior;
- `index`: task, source, contract, state, or glossary navigation.

A chapter can reference another type but should have one dominant purpose.

## Decomposition rules

Split a topic when any of these are true:

- it has a distinct state owner or lifecycle;
- it has a separate failure, retry, cancellation, or recovery model;
- it can change independently behind a stable boundary;
- developers commonly search for it as a separate task;
- combining it would hide a cross-module contract or side effect;
- the chapter would need several unrelated runtime paths;
- the source evidence and update triggers cover unrelated domains.

Merge topics only when they share the same mental model, lifecycle, ownership,
and likely change path.

Do not use chapter length alone as the decision. A short chapter may represent
an important invariant; a long chapter may still be cohesive.

## Coverage inventory

Coverage completeness and chapter readability are independent concerns.
`manifest.yaml` must retain the full map of in-scope design surfaces, chapter
relationships, evidence, and update triggers. Chapter prose should progressively
disclose that knowledge and include only the explanation needed to establish
the correct mental model, runtime behavior, boundaries, failure consequences,
and change impact. Complete coverage does not require every discovered helper,
exception, or source relationship to appear in prose.

Record the discovered design surface in `manifest.yaml.coverage_inventory`
before deep writing. Each entry should use:

```yaml
coverage_inventory:
  - area: app/auth/**
    kind: source-area
    disposition: covered
    chapters:
      - authentication
  - area: generated/**
    kind: source-area
    disposition: excluded
    reason: Generated artifacts are not design evidence.
```

Inventory at least:

- top-level source responsibility areas;
- important end-to-end flows;
- persisted state machines;
- external interface groups;
- operational surfaces.

Use `disposition: covered` or `excluded`. Require a reason for exclusions. A
covered entry may map to several chapters. An inventory entry is a discovery
claim, not proof that the prose is deep enough.

Conversely, concise prose is not proof of shallow coverage. Judge it by whether
the reader can answer how the mechanism runs, who owns its state, what happens
on material failure, and what a change can affect, while the manifest preserves
the complete discovery and synchronization model.

During audit, compare the current repository to this inventory and find new,
orphaned, over-broad, duplicated, or obsolete entries.

## Agent indexes

Make `index.md` answer both "understand" and "change" questions. Include:

- a short system reading path;
- a book map by part;
- task-based change paths;
- concept and terminology entry points;
- source-area routes;
- state-machine and contract routes when applicable;
- visible coverage health and unresolved gaps.

For every important change task, provide:

1. first chapter;
2. conditional chapters and the condition;
3. invariants or contracts to preserve;
4. source and test evidence;
5. post-change inspection targets.

Keep the index concise. Move detailed change procedures to `guide` chapters.
Keep chapter-level routing metadata concise enough that an Agent can select
evidence without reading every candidate chapter.

## Completion standard

Treat the three dimensions independently:

- `status`: writing workflow (`planned`, `draft`, `verified`, `needs-review`);
- `coverage`: explanatory depth (`outline`, `substantial`, `complete`);
- `evidence_status`: current support (`partial`, `verified`, `stale`,
  `conflicted`).

`verified` means evidence was checked. It does not mean the topic is complete.

Do not call the whole handbook complete until:

- every in-scope coverage inventory entry is covered or explicitly excluded;
- important flows and persisted state machines have dedicated treatment;
- every chapter required for the primary reading paths has substantial or
  complete coverage;
- complete chapters have verified evidence;
- navigation supports both human reading and Agent change tasks;
- material unresolved items are visible;
- the HTML view is current;
- deterministic validation and semantic audit both pass.
