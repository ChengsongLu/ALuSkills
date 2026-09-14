---
name: clarify-development-request
description: Resolve material requirement decisions that repository evidence cannot answer. Use for ambiguous development behavior or explicit clarification requests; skip routine implementation choices and review-only work.
---

# Clarify Development Request

Resolve ambiguous development requirements from repository facts and decision-changing questions. Keep resolved decisions in the conversation or an authorized brief, and pause only implementation that depends on unresolved material choices.

## Gate the workflow before writing

Treat initial classification as a read-only preflight, not as entry into the
clarification workflow.

Use this preflight when the request or later repository investigation exposes a
potentially material unresolved requirement, before implementing the affected
behavior. The user need not ask for clarification by name.

1. Read only enough repository instructions, code, tests, documentation, and
   analogous implementations to distinguish missing facts from missing product
   decisions.
2. Classify the request as consultation, diagnosis, review, mechanical change,
   well-specified low-risk development, or non-trivial development with a
   material unresolved decision.
3. Enter this workflow only when the user explicitly requested clarification,
   item-by-item confirmation, one-question-at-a-time discovery, or collaborative
   definition of feature behavior or boundaries before design or implementation;
   or when a remaining decision would change product behavior, contracts, scope,
   or acceptance criteria.
4. Treat naming inside a private implementation, file placement, refactoring
   mechanics, test organization, and other reversible local choices as
   implementation decisions unless they affect an observable contract.
5. If repository evidence and the request already determine the behavior,
   scope, and acceptance criteria, stop this workflow immediately. Do not create
   a directory or `brief.md`, do not ask for confirmation, and continue the
   user's requested work normally.

Ask the unresolved decision directly; permission to ask a question is not a
separate gate. Continue unaffected authorized work while awaiting the answer.
Resolve a small set of decisions in the conversation without creating files.
An explicit request for a brief authorizes `brief.md`. Otherwise propose a brief
only when durable decisions would materially help, and confirm that artifact
before writing it. Declining a brief does not block work once the underlying
decisions are resolved. Clarification alone does not authorize a persistent file.

## Place the output

When a brief is authorized, use a user- or repository-specified location, or the following default:

```text
.clarify-development-request/
└── YYYY_MM_DD_short-name_NNN/
    └── brief.md
```

Derive `short-name` from confirmed scope, not from an unverified initial guess. Start `NNN` at `000` and select the next unused sequence for the same date and short name. Keep every clarification run isolated.

Create `brief.md` only after the preflight gate confirms that the request belongs
in this workflow, the user has authorized the artifact, and enough scope is known to
name it safely. Update that file as decisions change; do not create parallel
notes that can drift. Do not modify ignore rules or stage the artifact unless
the user explicitly requests it.

## Establish the boundary

1. Reuse established repository evidence; read additional sources only to resolve a material uncertainty.
2. Split an oversized request into independently deliverable concerns. Explain the split and obtain agreement on the concern to clarify first.
3. Treat repository facts as evidence, not as substitutes for product decisions. Surface conflicts between current code and historical design.

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

Ask dependent questions one at a time; batch a few independent questions when easier to answer. Honor an explicit request for one question at a time. Explain what each answer changes. Give a recommendation and its evidence when useful, but do not use a recommendation to decide product semantics on the user's behalf.

Check applicable unresolved dimensions; use dependencies to choose the order:

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
6. Make each material design choice explicit; independent choices may be presented together.

## Deliver the development brief

When authorized, write a concise, deterministic `brief.md` containing:

- **Goal and success criteria**
- **Scope and non-goals**
- **Confirmed decisions**
- **Selected approach and tradeoffs**
- **Invariants and forbidden outcomes**; write `Not applicable` when appropriate
- **Risk, security, and compatibility boundaries**
- **Acceptance and validation criteria**
- **Open decisions**; write `None` only when none remain
- **Next step and its scope**; write `Awaiting user direction` when the user has
  not chosen one

Do not leave decision-changing language such as “could,” “prefer,” “by default,” “later,” or “A or B” in the confirmed brief. Explicitly defer only local implementation choices that cannot change contracts, behavior, or acceptance.

Before delivering an authorized brief:

1. Self-review it against repository evidence and every conversation decision.
2. Check completeness, internal consistency, acceptance testability, and the
   absence of unresolved decision-changing language.
3. Fix wording, organization, and evidence omissions that do not change
   behavior.
4. Ask the user to resolve any issue that changes semantics, scope, contracts,
   state, security, compatibility, or acceptance.
5. Report the self-review conclusion and link `brief.md`. Ask only about material
   decisions still unresolved or a review checkpoint explicitly requested by the user.

Clarification is complete when material decisions are resolved and any authorized
brief records them accurately. Do not require repeated confirmation of decisions
already made. Return to the original authorized task; if the user requested only
clarification, deliver the result without starting implementation. Ask for a next
step only when the user has not already specified one. Do not invoke or prescribe
another Skill.

If requirements change later, reopen only the affected decisions and update any
authorized brief before dependent work continues.

When this workflow produced a brief, summarize the outcome and link to
`brief.md` in the final response. When the preflight gate exits, continue the
underlying task without mentioning a nonexistent clarification artifact.
