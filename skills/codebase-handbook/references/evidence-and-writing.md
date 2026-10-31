# Evidence and Writing

## Evidence

Distinguish verified current behavior, documented intent, inference, and
unknown or conflicting evidence. Source, configuration, migrations, and tests
support behavior; comments and specifications may describe intent. Tests can
also be stale. Investigate disagreements instead of automatically favoring
whichever account is convenient.

For a material conflict, explain the behavior, intent, evidence, and practical
consequence; mark the chapter `needs-review` and record the unresolved question.
Ask only when resolving it requires a product or design decision. Do not edit
source or ordinary project documents to make the handbook consistent.

Use repository-relative paths and stable symbols, for example
`src/jobs/worker.py — Worker.run()`. File-only references are sufficient when
no stable symbol exists. Keep grouped paths and roles in the manifest. Cite evidence near a claim
when needed to distinguish uncertainty.

## Write for understanding and change

Open with the chapter's purpose and central mechanism. Explain the mental
model, main flow, ownership and important boundaries, material failure or
recovery consequences, and change implications as applicable. These are reader
questions, not mandatory headings. Omit irrelevant sections.

Within a chapter, use descriptive headings for independently useful questions
so readers can retrieve and update one mechanism without loading unrelated
detail. Separate distinct flows, ownership rules, or failure conditions rather
than accumulating them in a long generic section. Keep conditions beside the
claims they qualify; short coherent chapters need no extra subdivisions.

Explain the key logic with as little text as clarity allows. Prefer visual
structure for flows and comparisons; use prose for the necessary reasons and
boundaries. Choose the form by the reader's question:

| Question | Preferred form |
| --- | --- |
| What is this for? | One or two opening sentences |
| How does execution or state progress? | A small flowchart, sequence diagram, or text arrows; label branches, commit points, and end conditions |
| What differs across scenarios or components? | A short comparison table with concrete conditions and outcomes |
| Where are files, and who owns them? | An annotated text tree or ownership diagram |
| What is a single rule or limitation? | One direct sentence |

Give the main flow before secondary cases. Split dense diagrams by reader
question rather than drawing one whole-system graph. Name entities and arrows;
use meaningful labels and a brief diagram purpose or Mermaid `accTitle` and
`accDescr` where helpful. Keep labels readable and tables scannable, without
putting paragraphs into cells. Do not require a fixed number of diagrams,
sections, or words.

Do not repeat a diagram or table row by row in prose. Keep the explanation
usable from Markdown text, including diagram source; HTML is a reading
projection, not a second body. Preserve permissions, version and concurrency
ownership, commit points, idempotency, cancellation, and recovery conditions
where material. Never turn a conditional guarantee into an unconditional one
to shorten it. Express these constraints in explicit diagram labels, table
text, or nearby sentences; color, position, and arrow styling alone must not
carry essential meaning. Avoid exhaustive file, endpoint, symbol, exception, and test
catalogs; link to maintained detail only after checking it exists.

Use standard Mermaid flowcharts, sequence, state, class, or entity relationship
diagrams, or plain text for simple flows. The offline viewer uses Mermaid Tiny;
mindmaps, architecture diagrams, KaTeX, and optional layout/icon plugins are
not included. Do not use diagram configuration frontmatter, init directives,
external images, or click actions. Check syntax and, when a browser is available,
rendering, label legibility, and agreement with the surrounding explanation.

Keep detail proportional to its value: include a constant, helper, or failure
case only when it affects understanding or safe modification. Explain a
relationship's reason and important ownership or failure implications rather
than listing import chains. Do not turn every relationship into a checklist.

## Semantic review before completion

Review each module chapter against its declared scope and current evidence.
The authored explanation should let a reader answer the applicable questions:

- What responsibility does the module own, and what invokes or consumes it?
- What conditions choose the main path and materially different branches?
- What state or data does it read, retain, replace, or publish, and who owns it?
- Where does work commit or terminate, and what survives failure or cancellation?
- What may be retried, resumed, or recalled, under which permissions and limits?

Use these questions to identify missing explanations, not as mandatory headings.
A chapter summary and a large source index alone do not explain a module's
design. Follow the relevant implementation and test behavior far enough to
support its branches and boundaries; filenames, symbol lists, and docstrings
alone are insufficient evidence. File roles should explain how each confirmed
participant contributes to the feature.

When initializing or substantially restructuring a book, complete a
representative module with meaningful state or branching first. Check its
coverage against the questions above and any user-provided depth reference,
then apply that standard across the remaining modules. This is a working
calibration step, not an extra approval gate or a substitute for reviewing the
other chapters. For example, context compression needs its trigger, retained
content, commit conditions, failure behavior, and recall boundaries explained;
the exact sections and details depend on the implementation.

Keep unfinished modules in draft and expose material gaps in the index and
manifest. Set verified only after evidence and semantic review are complete.
Report structural checks and tests actually executed separately from this review.

## Draft and maintain

Inspect enough evidence to support the important claims, then synthesize the
explanation independently of source traversal order. Preserve useful evidence
routes; discard analysis-only notes instead of relocating them into metadata.

For each affected section:

1. Update its existing explanation before adding a new paragraph.
2. Consolidate repetition locally or link to the canonical chapter elsewhere.
3. Remove superseded statements once the replacement is verified; preserve
   uncertain and explicitly protected content.
4. Retain details only if they improve the mental model, boundaries, failure
   understanding, or change guidance.
5. Keep the file index in the manifest and avoid a chronology of patches.

Do not rewrite unaffected chapters or sacrifice a real invariant merely to
reduce length. When duplication spans chapters beyond the authorized scope,
report the structural opportunity instead of silently broadening the edit.
