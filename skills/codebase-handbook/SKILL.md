---
name: codebase-handbook
description: Create, navigate, synchronize, validate, render, and evolve a repository's natural-language technical handbook in .codebase-handbook. Use when a user asks to initialize or consult a codebase handbook, or when a repository already contains .codebase-handbook and a task involves understanding, planning, modifying, refactoring, reviewing, or explaining code that may affect design, responsibilities, runtime behavior, contracts, source references, or the generated handbook.html reading view. Do not initialize a handbook during an ordinary coding task unless the user explicitly asks.
---

# Codebase Handbook

Build and maintain a navigable technical book about a repository's design and
runtime behavior. Explain stable concepts, responsibilities, flows, state,
failure behavior, and relationships. Cite source files and symbols as evidence
without turning the handbook into file-by-file or function-by-function
documentation.

Treat the output as a book, not a collection of summaries. Maintain one
canonical set of chapters with a human reading plane and an Agent task-navigation
plane.

## Start Here

1. Locate the project root.
2. Check whether `<project-root>/.codebase-handbook/` exists.
3. If it exists, read these files in order before acting:
   1. `config.yaml`
   2. `preferences.md`
   3. `manifest.yaml`
   4. `index.md`
4. Apply requirements in this precedence order:
   1. The user's current explicit instructions
   2. `.codebase-handbook/preferences.md`
   3. `.codebase-handbook/config.yaml`
   4. This skill's defaults
5. Choose the matching workflow below.

Never infer that a missing handbook should be created. Initialize only when the
user explicitly requests it.

## Choose a Workflow

- **Initialize**: Read [workflows.md](references/workflows.md), then
  [handbook-spec.md](references/handbook-spec.md),
  [book-model.md](references/book-model.md),
  [evidence-and-writing.md](references/evidence-and-writing.md), and
  [repository-rules.md](references/repository-rules.md).
- **Navigate or answer a codebase question**: Read
  [workflows.md](references/workflows.md) and follow the navigation workflow.
- **Plan or implement a code change in a repository with a handbook**: Read
  [workflows.md](references/workflows.md) and follow both the pre-change and
  post-change workflows.
- **Validate or audit**: Read [workflows.md](references/workflows.md) and
  [handbook-spec.md](references/handbook-spec.md), then
  [book-model.md](references/book-model.md).
- **Build the HTML reading view**: Read
  [html-view.md](references/html-view.md).
- **Split, merge, rename, deprecate, or remove a module or chapter**: Read
  [workflows.md](references/workflows.md) and follow the evolution workflow.
- **Edit repository-level Agent instructions**: Always read
  [repository-rules.md](references/repository-rules.md) first.

## Non-Negotiable Rules

### Preserve the repository

- Treat Git-tracked files as the default analysis boundary.
- Respect `.gitignore`. Exclude dependencies, build products, caches,
  binaries, and generated files by default.
- Explain why ignored content is needed and request permission before reading
  it. Never modify `.gitignore` automatically.
- Do not prescribe whether `.codebase-handbook/` is tracked or ignored. Do not
  inspect or alter its Git tracking policy unless the user asks.
- Preserve unrelated working-tree changes and concurrent edits.

### Preserve existing content

- Treat all existing handbook prose as intentional regardless of who or what
  authored it.
- Make evidence-driven, local edits. Never regenerate a whole existing chapter
  merely because a template changed.
- Do not edit `preferences.md`.
- Do not automatically edit a `Maintainer notes` section or content enclosed
  by `codebase-handbook:preserve` markers.
- Preserve uncertain content and mark it `needs-review`; do not silently
  delete it.
- Merge structured files without dropping unknown fields.

### Describe the right level

- Document design, responsibilities, boundaries, runtime flows, state and data
  changes, failure paths, side effects, concurrency, and recovery when relevant.
- Decompose by mental model, lifecycle, state ownership, failure model, and
  developer change task. Do not compress distinct subsystems merely because
  they collaborate.
- Do not create exhaustive file, class, function, endpoint, or test catalogs.
- Cite repository-relative paths plus stable symbols. Do not use fixed line
  numbers as durable references.
- Separate verified behavior, documented intent, inference, and unresolved
  conflict.
- Omit inapplicable chapter sections rather than filling them with speculation.

### Keep the handbook usable

- Make `index.md` a task and concept navigator, not only a table of contents.
- Organize the human reading path as parts and ordered chapters.
- Record machine-readable coverage inventory, chapter, source, relationship,
  status, depth, evidence, and update-trigger mappings in `manifest.yaml`.
- Link related chapters in both directions when the relationship is symmetric.
- Use Mermaid only when it materially clarifies a relationship or sequence;
  keep the prose independently understandable.
- Describe only the current system by default. Let Git retain history.

## Deterministic Helpers

Initialize the empty handbook structure:

```bash
python3 <skill-dir>/scripts/initialize_handbook.py --project-root <project-root>
```

This helper refuses to overwrite an existing handbook and creates an initial
`handbook.html`. After it succeeds, perform the semantic discovery and writing
steps from `references/workflows.md`.

Regenerate the self-contained HTML reading view:

```bash
python3 <skill-dir>/scripts/build_handbook.py --project-root <project-root>
```

Validate structure, links, manifest paths, and source references:

```bash
python3 <skill-dir>/scripts/validate_handbook.py --project-root <project-root>
```

Validation also checks that `handbook.html` exists and matches its Markdown and
YAML inputs. Script success proves only deterministic integrity. It does not
prove that prose still matches repository behavior.

## Completion Contract

For an initialization, do not claim completion until every in-scope design
surface is represented in the coverage inventory, every primary reading path is
usable, and chapters reach the required depth and evidence state. For an
update, report:

- chapters updated;
- chapters inspected but unchanged, with the reason;
- unresolved or `needs-review` items;
- HTML reading view regenerated and current;
- deterministic validation performed;
- semantic areas not verified and why.
