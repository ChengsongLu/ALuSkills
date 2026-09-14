---
name: write-technical-spec
description: Assess material design risks, or create, update, and review technical specifications. Use for interacting contracts, state, migration, or recovery concerns; skip clear localized low-risk changes.
---

# Write Technical Spec

Assess, create, update, or review a technical specification using current repository evidence. Keep creation, revision, and read-only review distinct; make the workflow self-contained and do not delegate any part of it to another Skill.

## Select the operating mode

Read enough repository and specification context to select one mode before taking action:

- **Assess or create:** Use the entry assessment below for explicit requests or development work whose request or repository evidence reveals material design risk. Assessment alone does not authorize specification artifacts. Explicit authoring requests authorize the requested artifacts; confirm only implicitly proposed artifacts or material scope expansion.
- **Update:** Locate the existing specification by scope and evidence, confirm it is the same design effort, and edit only within the user's authorized scope. Ask again only for a material scope expansion or unresolved design decision.
- **Review:** Inspect an existing specification for implementation readiness. Treat a review request as read-only unless the user explicitly asks for remediation; do not edit specifications, source, tests, repository metadata, or persistent review artifacts.

Do not send review requests through the creation gates. If the target specification or requested review baseline cannot be identified safely, ask the user for the missing location or scope.

Resolve missing inputs within this Skill. Investigate repository facts first. When a remaining choice would change semantics, contracts, scope, data, state, security, visible behavior, compatibility, or acceptance criteria, explain the unresolved decision and its impact, then ask the user directly. Do not continue past the affected gate until it is resolved. Leave reversible local implementation choices to the plan when they cannot affect observable behavior or acceptance.

## Assess whether to enter the specification workflow

Apply this read-only assessment before implementing the affected behavior when
the request or repository investigation reveals the risks below. Do not wait
for the user to mention a specification. Reassess if later investigation exposes
material design risk that was not apparent initially; do not repeat an already
resolved gate unless its scope or risk materially changes.

1. Read enough repository instructions, documentation conventions, current implementation, relevant tests, existing specifications, and analogous modules to assess the affected behavior.
2. Assess actual complexity and risk rather than using file count or request length as a proxy. Consider:
   - changes to public contracts, user-visible behavior, data, state, or schemas;
   - coordination across modules, services, processes, or external systems;
   - concurrency, security, privacy, migration, compatibility, deployment, or rollback concerns;
   - multiple meaningful branches, failure modes, recovery paths, or side effects;
   - unresolved tradeoffs that implementation should not decide implicitly.
3. Recommend entering the specification workflow when several of these concerns interact, when the change has material risk, or when repository rules require a spec. Recommend skipping it for localized, low-risk work whose behavior and validation are already clear.
4. If implicit assessment finds localized low-risk work with clear behavior and validation, stop this workflow and continue the requested task without an entry-confirmation question or artifacts. For an explicit assessment or specification request, report the recommendation even when it is to skip.
5. When implicitly recommending a specification, explain the task-specific reason and proposed document set in one confirmation question before writing. Continue unaffected authorized work. If the user declines, return to the requested task and resolve any remaining behavior decision directly.

An explicit request to create a specification authorizes its requested scope and
artifacts. Honor requested flow documents without asking again. For an unspecified
document set, choose the smallest useful set under the authoring guidance; explain
that choice without a separate approval gate. Confirm only a material scope
expansion, an unresolved design decision, or a user-required review checkpoint.

## Read only the selected workflow

- For assessment alone, stop after the assessment above; load no authoring guide.
- For creation or updates, read [authoring.md](references/authoring.md).
- For a standalone readiness review, read [readiness-review.md](references/readiness-review.md).
  Keep it read-only. Authoring also uses this review once the requested set is complete.
