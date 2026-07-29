---
name: clarify-development-request
description: Clarify goals, scope, behavior, contracts, state, side effects, risks, compatibility, and acceptance criteria before non-trivial software development. Use when the user explicitly asks to refine or prepare a development request, or when unresolved product or technical choices would materially change an implementation. Do not invoke for ordinary consultation, diagnosis, review-only work, mechanical edits, or a well-specified low-risk change.
---

# Clarify Development Request

Convert an ambiguous development request into a confirmed, implementation-ready brief. Investigate repository facts first, ask only decision-changing questions, and do not implement while material choices remain unresolved.

## Place the output

Use a user- or repository-specified location when one is explicit. Otherwise persist each clarification under the project root:

```text
.clarify-development-request/
└── YYYY_MM_DD_short-name_NNN/
    └── brief.md
```

Derive `short-name` from confirmed scope, not from an unverified initial guess. Start `NNN` at `000` and select the next unused sequence for the same date and short name. Keep every clarification run isolated.

Create `brief.md` once the request has entered this workflow and enough scope is known to name it safely. Update that file as decisions change; do not create parallel notes that can drift. Do not modify ignore rules or stage the artifact unless the user explicitly requests it.

## Establish the boundary

1. Read applicable repository instructions, current documentation, relevant code, tests, existing specs, and analogous implementations.
2. Classify the request as consultation, diagnosis, review, mechanical change, or non-trivial development.
3. Skip this workflow when repository evidence and the user request already determine behavior, scope, and acceptance criteria.
4. Split an oversized request into independently deliverable concerns. Explain the split and obtain agreement on the concern to clarify first.
5. Treat repository facts as evidence, not as substitutes for product decisions. Surface conflicts between current code and historical design.

## Build the decision inventory

Record without repeatedly displaying:

- goals and observable success criteria;
- scope and explicit non-goals;
- confirmed user constraints and preferences;
- facts established from the repository;
- decisions that still affect behavior, architecture, contracts, state, security, compatibility, or acceptance;
- local implementation details that can safely wait for planning or coding.

Do not ask the user for information that can be determined from the repository.

## Resolve material decisions

Ask one focused question at a time. Explain what the answer changes. Give a recommendation and its evidence when useful, but do not use a recommendation to decide product semantics on the user's behalf.

Check only applicable dimensions, in this order:

1. goal and success criteria;
2. scope and non-goals;
3. names and domain semantics;
4. user interaction or interface contracts;
5. data sources, state transitions, persistence, termination, and side effects;
6. failure semantics, concurrency, idempotency, recovery, authorization, and sensitive-data boundaries;
7. compatibility with callers, data, deployment, platforms, and configuration;
8. validation and delivery criteria.

Follow a newly exposed decision branch before moving on. Skip dimensions that are already confirmed or irrelevant. If the user revises an earlier decision, update the inventory and revisit dependent conclusions.

## Capture invariants

For stateful, persistent, concurrent, security-sensitive, or side-effecting work, state the invariants and forbidden outcomes. Cover applicable concerns such as:

- the authoritative source of truth;
- the commit point after which the outcome must not be reversed by auxiliary failures;
- required terminal-state convergence;
- retry and duplicate-execution behavior;
- permissions and data-exposure boundaries;
- side effects that must never be repeated.

Infer an invariant from code or existing design only when the evidence is conclusive. Ask the user when it represents a business tradeoff.

## Select a direction

After the request is sufficiently clear:

1. Present two or three viable approaches only when a real design choice exists.
2. Compare benefits, costs, risks, and applicability.
3. Recommend an approach using current repository evidence.
4. Avoid manufacturing alternatives when one approach is plainly appropriate.
5. Describe the selected direction at the level of module boundaries, data flow, visible behavior, error handling, and validation—not file-by-file implementation.
6. Confirm independent design decisions separately rather than hiding them in one blanket approval.

## Deliver the development brief

Write a concise, deterministic `brief.md` containing:

- **Goal and success criteria**
- **Scope and non-goals**
- **Confirmed decisions**
- **Selected approach and tradeoffs**
- **Invariants and forbidden outcomes**; write `Not applicable` when appropriate
- **Risk, security, and compatibility boundaries**
- **Acceptance and validation criteria**
- **Open decisions**; write `None` only when none remain
- **Next step and its scope**

Do not leave decision-changing language such as “could,” “prefer,” “by default,” “later,” or “A or B” in the confirmed brief. Explicitly defer only local implementation choices that cannot change contracts, behavior, or acceptance.

Consider clarification complete only when no material decision remains, the user confirms the brief, and the next phase is identified. If the next phase is a technical specification, invoke `$write-technical-spec` and provide the confirmed `brief.md` as its source rather than relying on conversation history.

If requirements change later, reopen only the affected decisions and update any dependent brief or specification before continuing implementation.

In the final response, summarize the outcome and link to `brief.md`.
