# Handbook Specification

## Contents

- Directory contract
- Configuration contract
- Preferences contract
- Manifest contract
- Book and coverage contract
- Chapter contract
- Status model
- Protected content

## Directory contract

Create the handbook only at the project root:

```text
.codebase-handbook/
├── config.yaml
├── preferences.md
├── manifest.yaml
├── index.md
├── handbook.html
└── <part-or-topic-groups>/
```

Create only directories that the book needs. Directory names may follow book
parts or stable topic groups. Do not require one directory per chapter type.
Keep every handbook file under `.codebase-handbook/`.

## Configuration contract

Treat `config.yaml` as user-maintained machine-readable policy. Preserve unknown
keys and do not change a configured value merely to match a new default.

The default schema is:

```yaml
schema_version: 2
language: auto
scan:
  tracked_files_only: true
  respect_gitignore: true
  exclude_generated: true
source_references:
  durable_line_numbers: false
html:
  title: auto
  show_source_evidence: true
```

Resolve `language: auto` from the repository's primary existing documentation
language. Ask the user when there is no reliable primary language.

## Preferences contract

Treat `preferences.md` as project-specific natural-language user requirements.
Read it before every create, navigate, update, validation, and audit operation.
Never rewrite, normalize, or automatically append to it.

Preferences may specify:

- priority concepts, modules, or flows;
- desired depth or excluded detail;
- project terminology;
- preferred diagrams or reading paths;
- content that must not be recorded;
- additional validation or maintenance expectations.

Current explicit user instructions override this file. This file overrides
`config.yaml` defaults and the skill defaults.

Do not prescribe whether the project tracks or ignores `.codebase-handbook/`.
That repository policy belongs to the user.

## Manifest contract

Treat `manifest.yaml` as the machine-readable knowledge index and synchronization
ledger. Preserve unknown fields during updates.

Recommended schema:

```yaml
schema_version: 2
handbook_status: planned
parts:
  - id: architecture
    title: Architecture foundations
    purpose: Establish boundaries, layers, topology, and durable invariants.
    order: 20
chapters:
  - id: authentication
    path: modules/authentication.md
    summary: Owns session authentication and token refresh, but not user authorization policy.
    kind: module
    part: architecture
    order: 30
    status: verified
    coverage: complete
    evidence_status: verified
    read_when:
      - Changing authentication behavior
    concepts:
      - session authentication
      - token refresh
    sources:
      - src/auth/service.py
      - src/auth/store.py
    source_symbols:
      - src/auth/service.py::AuthService
    related:
      - user-authentication-flow
    update_triggers:
      - src/auth/**
      - config/auth.*
coverage_inventory:
  - area: src/auth/**
    kind: source-area
    disposition: covered
    chapters:
      - authentication
unresolved: []
```

Requirements:

- Keep `id` stable across file moves and title edits.
- Keep part IDs stable and use `order` for presentation.
- Store paths relative to `.codebase-handbook/` in `path`.
- Store source paths and glob patterns relative to the project root.
- Use `related` chapter IDs, not titles.
- Keep `sources` to direct evidence. Use `update_triggers` for broader impact
  candidates.
- Use `summary` as a compact routing statement: name the chapter's purpose,
  central mechanism, or most important boundary in one sentence. Do not copy a
  source walkthrough or the full chapter opening into it.
- Use `concepts` for stable project terms that help an Agent and HTML search
  resolve the chapter. Do not turn it into a symbol or keyword dump.
- Use `read_when` for developer tasks and decisions, not as another topic list.
- Do not treat an update-trigger match as proof that prose must change.
- Record unresolved conflicts or coverage gaps in `unresolved`.
- Preserve schema v1 manifests during ordinary updates. Upgrade structure only
  when the user requests it or a book-wide audit requires it.
- Populate or refine `summary` and `concepts` when creating a chapter, changing
  its responsibility, or performing a confirmed structural audit. Do not create
  unrelated metadata churn during a local synchronization.

## Book and coverage contract

Use `parts` to define the human reading hierarchy. Every non-index chapter in a
schema v2 handbook must belong to a part unless it is deliberately presented as
an appendix-level ungrouped chapter.

Use `coverage_inventory` as the discovery and completeness ledger. Inventory
source responsibility areas, important flows, persisted state machines,
external contract groups, and operational surfaces. Map each entry to one or
more chapters, or mark it excluded with a reason.

Do not derive completeness from chapter count, file count, word count, or
`status: verified`. Apply the decomposition and completion rules in
[book-model.md](book-model.md).

## Chapter contract

Begin with a short statement explaining when a developer should read the
chapter, then state its core conclusion. Organize the rest in the smallest set
of sections that establishes the mental model and supports safe change. Use
this default progression when applicable:

1. Core conclusion
2. Mental model
3. Runtime behavior
4. Key boundaries
5. Failure and recovery
6. Change guidance
7. Source evidence

This is an optional structure, not a fill-in template. Omit inapplicable
sections, rename them to match the project, and add a section only when the
chapter's dominant purpose requires it. Integrate responsibilities,
prerequisites, participants, state changes, external interfaces, side effects,
relationships, and unresolved questions into the section where they best
support understanding. Do not create empty or repetitive sections merely to
enumerate the contract.

For `flow` chapters, emphasize phases, participants, control and data movement,
commit points, failure branches, and observability.

For `state-machine` chapters, emphasize state ownership, transitions,
preconditions, invariants, idempotency, cancellation, retry, and recovery.

For `module` chapters, emphasize responsibilities, non-responsibilities,
collaborators, owned state, extension points, and change impact.

For `guide` chapters, begin from a developer task and explain the reading,
decision, implementation, and validation path without duplicating source.

Prefer stable design language over code-shaped prose. Depth means complete
design and runtime understanding, not exhaustive symbol documentation.
Apply the editorial compression pass in
[evidence-and-writing.md](evidence-and-writing.md) after drafting or materially
updating a chapter.

Use source references like:

```text
src/auth/service.py — AuthService.refresh_session()
```

Avoid durable line-number references. An ephemeral analysis response may add
line numbers for convenience.

## Status model

- `planned`: scope identified; prose may not exist.
- `draft`: prose exists but evidence or relationships remain incomplete.
- `verified`: an Agent checked the chapter against current source evidence.
- `needs-review`: a conflict, uncertainty, protected statement, or unavailable
  dependency prevents verification.

Track explanatory coverage independently:

- `outline`: orientation or summary only;
- `substantial`: primary design, runtime, state, and change questions are
  answered, but secondary paths or evidence remain;
- `complete`: all applicable chapter-contract questions are answered at the
  repository's required depth.

Track evidence independently:

- `partial`: only some material claims were checked;
- `verified`: current evidence supports the material claims;
- `stale`: relevant source changed after verification;
- `conflicted`: current evidence disagrees or is ambiguous.

Show incomplete, stale, conflicted, and `needs-review` coverage in `index.md`.
Do not present a partial handbook as complete.

## HTML output

Treat `handbook.html` as generated output. Never edit it by hand. Regenerate it
after changing `config.yaml`, `preferences.md`, `manifest.yaml`, `index.md`, or
any registered chapter. Treat it as the human reading projection; Agents should
use `manifest.yaml`, `index.md`, chapters, and cited repository evidence rather
than scraping generated HTML. See [html-view.md](html-view.md).

## Protected content

Treat all existing prose as intentional. Additionally, never automatically edit:

```markdown
## Maintainer notes
```

or:

```markdown
<!-- codebase-handbook:preserve:start -->
Protected content
<!-- codebase-handbook:preserve:end -->
```

When protected content conflicts with current behavior, preserve it and record
the conflict in `manifest.yaml` as `needs-review`.
