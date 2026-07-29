# Evidence and Writing

## Contents

- Evidence classes
- Conflict handling
- Writing style
- Source references
- Relationship writing
- What not to document

## Evidence classes

Use these categories:

- **Verified current behavior**: supported by current source, configuration,
  migrations, or executable tests.
- **Documented intent**: stated by maintained documentation, comments, or
  specifications and consistent with current behavior.
- **Inference**: a reasoned interpretation not directly established by a source.
- **Conflict**: current behavior and documented intent disagree.
- **Unknown**: evidence is missing, inaccessible, or ambiguous.

Do not present inference as fact. Put material conflicts and unknowns in the
chapter and `manifest.yaml.unresolved`.

Tests are evidence, not automatic truth. When tests and implementation disagree,
determine whether the test, fixture, mock, or implementation is stale before
describing the behavior.

## Conflict handling

1. State what current executable evidence shows.
2. State what documented intent claims.
3. Cite both.
4. Explain the practical consequence.
5. Mark the affected chapter `needs-review`.
6. Ask for a decision when resolving the conflict would change project meaning.

Do not edit source or existing project documentation merely to make the
handbook internally consistent.

## Writing style

- Write for developers who need to understand, maintain, or change the system.
- Lead with purpose and mental model, then runtime behavior and evidence.
- Prefer natural technical prose over symbol inventories.
- Explain why a relationship exists, not only that two files import each other.
- Explain durable invariants, ownership, commit points, and change consequences
  when they are more important than individual implementation steps.
- Use consistent project terminology.
- Keep detail proportional to design significance and change risk.
- Describe important failure and recovery behavior even when the happy path is
  simple.
- Let overview chapters stay concise, but follow them with dedicated chapters
  for materially distinct lifecycles, state owners, failure models, and common
  change tasks.
- Avoid copying long source excerpts.

## Source references

Use repository-relative paths and stable symbols:

```text
src/jobs/worker.py — Worker.run()
config/runtime.yaml — jobs.retry_limit
tests/jobs/test_retry.py — test_retry_stops_after_limit()
```

Use file-only references when no stable symbol exists. Avoid durable line
numbers, absolute local paths, editor URLs, and references to ignored build
artifacts.

## Relationship writing

For every material relationship, explain:

- direction;
- reason;
- exchanged data or control;
- ownership of state;
- failure propagation;
- whether the dependency is synchronous, asynchronous, persistent, or
  operational.

Use a diagram only when it reduces the effort required to understand several
relationships or a multi-stage sequence. Keep the prose sufficient without the
diagram.

## What not to document

Do not create:

- exhaustive file, class, or function catalogs;
- restatements of obvious syntax;
- transient implementation details with no design or maintenance value;
- generated code or vendored dependency explanations;
- historical behavior presented as current;
- guessed business meaning;
- duplicated API reference material when a maintained authoritative source
  already exists.
