# Evidence and Writing

## Contents

- Evidence classes
- Conflict handling
- Information hierarchy
- Drafting and editorial compression
- Writing style
- Choosing prose, tables, and diagrams
- Example: context compression
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

## Information hierarchy

Keep coverage completeness and prose density separate:

- Put the complete inventory of design surfaces, chapter mappings, evidence,
  relationships, and update triggers in `manifest.yaml`.
- Put the explanation needed to understand and safely change the mechanism in
  chapter prose.
- Put a small set of stable, direct source references at the end of the chapter.
- Keep analysis artifacts such as call-by-call traces, candidate evidence, and
  discarded hypotheses out of the handbook unless they establish a material
  conflict or unresolved question.

Use this default chapter order, omitting any section that does not help the
chapter's dominant purpose:

1. **Core conclusion**: state the purpose, central mechanism, and most important
   boundary in a short opening.
2. **Mental model**: explain the essential structure with concise prose, a
   compact table, or a diagram when relationships require it.
3. **Runtime behavior**: present the primary path in three to seven meaningful
   phases when a sequential explanation is useful.
4. **Key boundaries**: record fact ownership, read projections, commit points,
   protocol boundaries, invariants, and side effects that constrain changes.
5. **Failure and recovery**: include only failures that alter state, data,
   externally visible side effects, retryability, or recovery.
6. **Change guidance**: identify contracts and related chapters to inspect for
   common modifications, without expanding into a file catalog.
7. **Source evidence**: list a small set of stable sources and symbols that
   directly support the material claims.

The opening should let a reader answer what the mechanism does, how it works at
a high level, and what must not be broken without first reading the evidence
list or implementation details.

## Drafting and editorial compression

Separate writing into two passes:

1. **Evidence analysis**: inspect enough source, configuration, migrations, and
   tests to understand behavior, state, failures, side effects, and conflicts.
   Preserve complete coverage and synchronization metadata in the manifest.
2. **Chapter editing**: synthesize the mental model, primary runtime path,
   boundaries, failure consequences, and change impact. Do not retain discovery
   order as chapter structure.

After a draft or material update, perform an editorial compression pass:

1. Does the first paragraph state the conclusion directly?
2. Does any section follow file, class, function, import, or call order instead
   of explaining a design concept?
3. Is the same fact fully explained in more than one chapter? Keep one canonical
   explanation and link to it elsewhere.
4. Can a paragraph be removed without weakening the mental model, runtime
   behavior, boundaries, failure consequences, or change guidance?
5. Would a compact table replace repeated prose for exact states, levels,
   ownership, or mappings?
6. Does each failure detail affect state, side effects, recovery, or maintenance
   risk? Omit ordinary exception propagation that does not.
7. Do source citations interrupt the explanation? Consolidate them at the end
   unless a citation distinguishes fact, inference, conflict, or uncertainty.
8. Did analysis-only evidence leak into the narrative merely because it was
   collected? Move it to the manifest or omit it from the handbook.

Compression must not remove a material design surface from
`coverage_inventory`, weaken evidence state, hide a conflict, or erase a
boundary needed to change the system safely.

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

## Choosing prose, tables, and diagrams

- Use prose for purpose, causality, ownership, invariants, and consequences.
- Use a table for repeated exact mappings such as modes, states, levels,
  responsibilities, or guarantees.
- Use a numbered flow for a primary path with meaningful state, control, or
  side-effect transitions. Keep it to three to seven phases when that captures
  the mechanism; split or summarize secondary branches instead of padding the
  main path.
- Use Mermaid only when several relationships, branches, or stages are harder
  to understand linearly. Keep accompanying prose independently sufficient.
- Do not diagram a simple import chain or replace a short explanation with a
  decorative visual.

## Example: context compression

A source-traversal draft might list each helper that clears temporary state,
calculates a budget, reads history, builds summaries, and replaces request
content. This records discovery order but does not explain the mechanism.

Lead with the design instead:

> Context compression preserves the durable conversation history and builds a
> smaller read view for the next model request. It keeps the history most useful
> to the current decision, summarizes older material, and can replace the least
> relevant summaries with retrieval references when the budget remains
> exceeded. The active turn stays intact.

If the implementation has several exact policies, summarize their behavioral
difference in a table rather than describing each policy in repetitive prose:

| Policy | Original content | Older history |
| --- | --- | --- |
| Full fidelity | All | Unchanged |
| Balanced | Wider recent window | Summarized |
| Compact | Narrower recent window | Summarized |
| Reference only | Minimum recent context | Replaced by retrieval references |

Then explain selection semantics only when they change the mental model. For
example, distinguish a system that applies policies sequentially from one that
prepares several candidates and selects the first acceptable result. State the
maintenance boundaries separately:

- Durable history remains the fact source; compression changes only a read
  view.
- Structured request and response pairs remain protocol-safe.
- The active turn remains outside historical compression.
- Compression failure does not replay completed external side effects.

Put excerpt lengths, threshold constants, helper order, and full record
classification in prose only when the chapter's task requires those facts.
Otherwise preserve their source mappings and update triggers in the manifest.
At the end of the chapter, cite only the stable policy definition, projection
logic, selection boundary, and contract tests that directly support the claims.

Apply the same rule to module relationships. Explain which component owns the
facts, which creates the read projection, and which chooses the representation.
An import chain between their files is evidence of implementation shape, not a
design explanation.

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
