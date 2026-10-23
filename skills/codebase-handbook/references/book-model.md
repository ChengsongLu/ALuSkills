# Book Model

## One body, two reading paths

Markdown chapters explain the system; HTML presents those same chapters to
humans. `index.md` and `manifest.yaml` route tasks and concepts to chapters and
source evidence. Neither is a second explanatory body.

Start discovery with purpose and boundaries, major responsibilities, entry
points, important flows, state ownership, external contracts, and relevant
operation or failure concerns. Existing documentation is a discovery aid;
verify material claims against implementation, configuration, and tests.
Do not inventory every file or helper.

## Organize around reader questions

Begin with orientation and architecture, then the mechanisms readers need to
understand or change. Use parts only when grouping improves a substantial book.
Chapter IDs stay stable across title and path changes.

A chapter may explain a subsystem, flow, state machine, interface, operational
concern, or change task. Split when independent reading and maintenance become
clearer: distinct ownership, lifecycle, failure behavior, or change tasks are
signals, not mandatory chapter boundaries. Merge overlapping explanations when
one coherent chapter can preserve the important distinctions. Neither chapter
count nor length alone determines quality.

Do not create empty categories, separate chapters for every discovered concept,
or operational guides that duplicate maintained repository documentation.
Link to authoritative detail and explain only the relevant architectural context.

## Keep routing small

Each chapter needs an ID, path, short summary, status, and direct evidence.
Add concepts, reading conditions, relationships, stable symbols, and broader
update triggers only when they improve retrieval. Sources already identify
impact candidates; do not repeat them in triggers without a broader need.

`index.md` needs an initial reading path and the important task or concept
entry points. Link to chapters for constraints and detailed guidance instead
of repeating their invariants and evidence lists in a large routing table.
HTML generates the full book map from the manifest, so the index need not
manually duplicate that map.

## Coverage without a permanent analysis ledger

During discovery or an audit, check that major responsibilities, important
flows, state owners, contracts, and operational boundaries are addressed or
explicitly out of scope. Record material gaps in `unresolved`.

Use `coverage_inventory` only when a compact map materially helps prevent
omissions in a large repository. Entries map responsibility areas to chapters
or explain exclusions. Do not preserve every discovered relationship, candidate
source, helper, or discarded hypothesis. Existing inventories may be retained
and updated locally; reducing their scope is deliberate structural work.

Use chapter `status` for planned, draft, verified, or needs-review work. Existing
`coverage` and `evidence_status` fields remain supported, but new handbooks need
not maintain three parallel classifications. An evidence check and topic
completeness are different: report significant unchecked areas explicitly.

Initialization is complete when the agreed scope has usable reading paths,
major mechanisms are explained with evidence, significant gaps are visible,
and deterministic validation plus semantic review have been performed. A
partial scope is acceptable when explicitly agreed; do not present it as
whole-repository coverage.
