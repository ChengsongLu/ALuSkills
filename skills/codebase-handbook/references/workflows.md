# Workflows

## Navigate

Choose the shortest useful entry path:

| Task context | Entry point |
| --- | --- |
| Known file, symbol, or changed code | Match manifest sources, symbols, and applicable update triggers |
| Behavior or concept question | Use index task routes or manifest summaries and concepts |
| Broad orientation | Follow the index's initial reading path within the requested scope |

Search or extract matching manifest records; do not load the whole manifest
or every chapter by default. Read the relevant chapter sections with enough
surrounding context to retain their conditions. Follow `related` and other
conditional links only when they affect the question, state, or contract.

If routing is missing, ambiguous, or stale, search the current repository and
use its evidence to refine the candidates. No handbook match does not prove
that a capability or dependency is absent. Do not force a match to an
unrelated chapter. Report material routing gaps without repairing them during
read-only navigation.

Verify current behavior-sensitive claims against source, regardless of chapter
status. Stop expanding once the requested explanation, relevant boundaries,
and supporting evidence are sufficient. Report unresolved uncertainty rather
than treating missing evidence as certainty. Do not synchronize or rebuild
during read-only navigation.

## Initialize

Only an explicit request authorizes initialization.

1. Resolve the project root, repository rules, current Git state, language, and
   requested scope. Run the initializer and read preferences.
2. Discover major responsibilities, boundaries, flows, state, and contracts
   from tracked evidence. Exclude generated and irrelevant material.
3. Choose a small coherent chapter plan using the book model. Explain scope
   and exclusions; ask only about material unresolved decisions.
4. Write orientation and core mechanisms first, then supporting chapters.
   Mark unfinished topics honestly and work in resumable batches.
5. Build compact task navigation and evidence mappings. Check for significant
   omissions without cataloging the whole implementation.
6. Apply the writing guide, build HTML, validate, and review whether the agreed
   scope is understandable and supported by evidence.

## Assess or synchronize a code change

Source changes are separately authorized work; this workflow writes only the
handbook. Before implementation, match affected responsibilities, source paths,
contracts, and any update triggers to candidate chapters. Expand through related
state or flows only when the change can affect them.

Establish the change range from the request and repository state before
deciding that synchronization is unnecessary:

| Requested scope | Evidence to inspect |
| --- | --- |
| Working-tree changes | Staged and unstaged diffs plus relevant untracked files |
| A commit or commit range | The specified commits' changes, including additions, renames, and deletions |
| Branch or pull-request changes | The agreed base and target revisions; use their merge base when assessing changes introduced by the branch |
| Current handbook audit | Current source against the documented scope; no historical diff is required |

Include working-tree changes alongside committed changes only when they belong
to the task. A clean working tree does not imply that committed changes need
no synchronization. Do not assume the last commit or default branch is the
baseline; resolve it from the request and available repository evidence. If
materially ambiguous, ask about the range while continuing independent current
source checks. Without version-control history, use an available before/after
snapshot or report the limits of a current-state comparison.

After implementation, inspect the actual changes in that range. Determine
whether documented behavior, boundaries, evidence, or relationships changed.
A source-path match is a reason to inspect, not a reason to rewrite. Verify
the resulting explanation against the target source state and identify the
range or state used in the handoff.

If nothing durable changed, report no synchronization need; do not rebuild or
validate solely because related code changed. If invocation is implicit and no
repository rule or explicit request authorizes updates, report the concrete
impact and ask before writing. Existing update authorization covers ordinary
scoped edits; confirm material scope expansion or unresolved design decisions.

Update the affected explanation and mappings using the writing guide. Preserve
protected content and unknown fields. Do not add a new change-log paragraph
for every patch. Rebuild and validate when handbook inputs change, and verify
changed claims against current evidence. Report material unresolved items.

## Audit

An audit request is read-only unless updates are also authorized. Compare the
current major responsibilities and important flows with the book's scope,
chapters, and any coverage inventory. Look for missing explanations, stale
claims, duplication, poor routing, and unnecessary metadata. Inspect the
primary reading paths as well as the underlying evidence.
Check the existing artifact against the current Skill's book model, writing,
format, and validation requirements, including conventions inherited from
earlier versions. Treat compatible older metadata as supported, not as a
mandatory migration. Report any relevant requirements not yet satisfied.

Distinguish structural validation from semantic review. Running validation does
not authorize regeneration or repairs. During an authorized maintenance audit,
make evidence-driven edits, then rebuild and validate. Preserve unaffected
content and report any areas not checked.

## Restructure or remove

An explicit rename, split, merge, or removal request authorizes that operation.
Confirm only ambiguous targets, removal of still-valid information, or a
material scope expansion. Preserve protected content and unique valid facts.

Keep stable chapter IDs for unchanged concepts. For splits or merges, migrate
content and update incoming links, manifest routes, and related chapters before
removing obsolete files. Keep current behavior in the book and let Git retain
history; create archives only when requested. Rebuild and validate afterward.

## Resume

Re-read current instructions and preferences, inspect Git state and handbook
files, and verify what changed since the interruption. Status labels are hints,
not proof. Resume from the first incomplete dependency and reuse evidence
whose baseline has not changed.
