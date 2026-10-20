---
name: clarify-development-request
description: Resolve material requirement decisions that repository evidence cannot answer. Use for ambiguous development behavior or explicit clarification requests; skip routine implementation choices and review-only work.
---

# Clarify Development Request

Resolve ambiguous development requirements from repository facts and
decision-changing questions. Keep resolved decisions in the conversation or an
authorized brief, and pause only the work that depends on unresolved material
choices.

## Gate the workflow

Treat the initial classification as a read-only preflight. Run it when the
request or later investigation exposes a potentially material unresolved
requirement, before implementing the affected behavior; the user need not ask
for clarification by name.

1. Read only enough repository instructions, code, tests, documentation, and
   analogous implementations to separate missing facts from missing product
   decisions.
2. Enter this workflow only when the user explicitly requested clarification,
   item-by-item confirmation, or collaborative definition of behavior before
   design or implementation; or when a remaining decision would change product
   behavior, contracts, scope, or acceptance criteria.
3. Private naming, file placement, refactoring mechanics, test organization,
   and other reversible local choices are implementation decisions unless they
   affect an observable contract.
4. If the request and repository evidence already determine behavior, scope,
   and acceptance, exit immediately: create no files, ask for no confirmation,
   and continue the requested work.

Ask the unresolved decision directly; permission to ask is not a separate gate.
Continue unaffected authorized work while awaiting the answer.

## Decide whether to write a brief

Resolve a small set of decisions in the conversation without creating files.
An explicit request for a brief authorizes `brief.md`. Otherwise propose one
only when durable decisions would materially help, and confirm before writing
it; declining does not block work once decisions are resolved.

When authorized, use a user- or repository-specified location, or by default:

```text
.clarify-development-request/
└── YYYY_MM_DD_short-name_NNN/
    └── brief.md
```

Derive `short-name` from confirmed scope. Start `NNN` at `000` and use the next
unused sequence for the same date and name. Update that one file as decisions
change; do not create parallel notes. Do not modify ignore rules or stage the
artifact unless the user explicitly asks.

## Establish the boundary and inventory

- Reuse established evidence; read more only to resolve a material uncertainty.
- Split an oversized request into independently deliverable concerns and agree
  on which to clarify first.
- Treat repository facts as evidence, not as substitutes for product decisions.
  Surface conflicts between current code and historical design.
- Track, without repeatedly displaying: goals and success criteria, scope and
  non-goals, confirmed constraints, established repository facts, decisions
  still affecting behavior or contracts, and local details that can wait.
- Never ask the user for information the repository can answer.

## Resolve material decisions

Ask dependent questions one at a time; batch a few independent questions when
that is easier to answer. Honor an explicit one-question-at-a-time request.
Explain what each answer changes, and offer a recommendation with evidence when
useful without deciding product semantics on the user's behalf.

Work through applicable unresolved dimensions in dependency order: goal and
success criteria; scope and non-goals; names and domain semantics; interaction
or interface contracts; data, state transitions, persistence, and side effects;
failure, concurrency, idempotency, recovery, authorization, and sensitive data;
compatibility with callers, data, deployment, and configuration; validation and
delivery criteria. Skip dimensions already confirmed or irrelevant, follow newly
exposed branches before moving on, and revisit dependent conclusions when the
user revises an earlier answer.

For stateful, persistent, concurrent, security-sensitive, or side-effecting
work, state the invariants and forbidden outcomes: the source of truth, the
commit point after which auxiliary failures must not reverse the outcome,
terminal-state convergence, retry and duplicate-execution behavior,
data-exposure boundaries, and side effects that must never repeat. Infer an
invariant from code only when the evidence is conclusive; ask when it is a
business tradeoff.

## Select a direction

Once the request is clear, present two or three approaches only when a real
design choice exists, compare benefits, costs, and risks, and recommend one from
repository evidence. Do not manufacture alternatives. Describe the direction at
the level of module boundaries, data flow, visible behavior, error handling, and
validation, not file-by-file steps.

## Deliver

When a brief is authorized, write a concise `brief.md` with: goal and success
criteria; scope and non-goals; confirmed decisions; selected approach and
tradeoffs; invariants and forbidden outcomes (or `Not applicable`); risk,
security, and compatibility boundaries; acceptance and validation criteria;
open decisions (or `None`); and the next step (or `Awaiting user direction`).
Do not leave decision-changing language such as "could", "prefer", "later", or
"A or B" in confirmed content.

Before delivering it, self-review against repository evidence and every
conversation decision for completeness, consistency, and testable acceptance.
Fix wording and evidence gaps directly; ask the user only about issues that
change semantics, scope, contracts, state, security, compatibility, or
acceptance.

Clarification is complete when material decisions are resolved and any brief
records them accurately. Do not require repeated confirmation of decisions
already made. Return to the originally authorized task; if the user asked only
for clarification, deliver the result without starting implementation. Do not
invoke or prescribe another Skill. If requirements change later, reopen only
the affected decisions.

Link `brief.md` in the final response when one was written. When the gate
exits, continue the underlying task without mentioning a clarification
artifact.
