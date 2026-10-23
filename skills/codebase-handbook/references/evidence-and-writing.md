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
no stable symbol exists. Cite a small set of direct evidence, usually at the
end; place a citation near a claim when needed to distinguish uncertainty.

## Write for understanding and change

Open with the chapter's purpose and central mechanism. Explain the mental
model, main flow, ownership and important boundaries, material failure or
recovery consequences, and change implications as applicable. These are reader
questions, not mandatory headings. Omit irrelevant sections.

Use prose for causality and consequences, tables for exact repeated mappings,
and diagrams only when they clarify relationships that prose makes hard to
follow. Keep prose understandable without diagram rendering. Avoid exhaustive
file, endpoint, symbol, exception, and test catalogs.

Keep detail proportional to its value: include a constant, helper, or failure
case only when it affects understanding or safe modification. Explain a
relationship's reason and important ownership or failure implications rather
than listing import chains. Do not turn every relationship into a checklist.

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
5. Keep source evidence at the end. Do not append successive implementation
   updates after it or preserve a chronology of patches.

Do not rewrite unaffected chapters or sacrifice a real invariant merely to
reduce length. When duplication spans chapters beyond the authorized scope,
report the structural opportunity instead of silently broadening the edit.
