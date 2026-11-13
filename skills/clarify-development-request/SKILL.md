---
name: clarify-development-request
description: Clarify development goals, scope, behavior, and acceptance through progressive discussion. Use when users want to think through an idea before coding, clarify requirements, confirm items step by step, ask one question at a time, or create or revise a development brief; also use when unresolved choices materially affect development outcomes. Skip routine implementation choices, execution requests with settled requirements and no requested discussion, and code-review-only work.
---

# Clarify Development Request

Build shared, actionable requirements from repository evidence and progressive
conversation. Help users form an initial idea as well as resolve ambiguity in an
existing request. The outcome is agreed behavior, scope, and acceptance; a
`brief.md` is optional.

## Choose the entry and respect its boundary

- **Requested discussion:** Enter when the user asks to explore a development
  idea, clarify requirements, confirm items, or discuss behavior before coding.
  Honor this request even if the existing code suggests a complete answer.
  Present established understanding briefly for correction instead of inventing
  questions or skipping the requested discussion. A request to create or revise
  a brief also enters this workflow; use settled decisions without reopening
  them and ask only about material gaps.
- **Clarification during execution:** When authorized work exposes a choice
  that would materially change behavior, contracts, scope, or acceptance,
  investigate the relevant facts and ask about the remaining decision directly.
  Pause only dependent work and continue unaffected authorized work. If facts
  and the user's request already settle the choice, continue without adding a
  clarification ceremony or artifact.

An explicit discussion or review checkpoint takes precedence over the automatic
exit for clear execution requests. Respect "discuss first, implement after my
confirmation" across turns; a reply to one question is not authorization to
implement. Where the user already authorized clarification followed by
implementation, do not add a new approval gate.

Private naming, file placement, refactoring mechanics, test organization, and
other reversible local choices do not justify clarification unless they affect
an observable contract. Permission to ask a necessary question is not a separate
step.

## Establish the current understanding

Read only the repository instructions, code, tests, documentation, or analogous
implementations needed to distinguish known facts from product decisions. For
an initial idea without an existing project, start with the intended outcome;
do not require repository evidence that does not exist.

Treat current behavior as evidence, not automatic authority for future behavior.
Surface relevant conflicts between code, documentation, and the user's intent.
Do not ask users to look up facts available in the repository; ask them to decide
product tradeoffs that those facts cannot settle.

Keep track of goals and success criteria, scope and non-goals, confirmed
constraints, established facts, assumptions, and unresolved decisions. Reuse
prior answers. For an oversized request, propose independently deliverable
concerns and establish which to clarify first without silently dropping scope.

## Discuss one decision, then update the understanding

In requested discussion, default to one main decision per turn. A few simple,
independent questions may be grouped when easier to answer; honor an explicit
one-question-at-a-time request. During execution, ask only what is needed to
resolve the material uncertainty, without turning it into an extended interview.

For each decision:

1. Identify the question that most affects what can be decided next. Start with
   goals, users, and success criteria when those are unclear, then establish
   scope, behavior, and acceptance as needed.
2. Explain what the answer changes. When useful, offer a recommendation and
   its evidence or a concrete example, without treating it as the user's choice.
   If the user delegates the choice, decide within that authority and explain it.
3. Incorporate the answer into the shared understanding. Revisit dependent
   conclusions when an answer changes an earlier assumption; preserve settled
   decisions that are unaffected.
4. Ask the next relevant question, or close when the agreed scope is resolved.
   At meaningful transitions, briefly summarize what is settled and what remains;
   do not repeat the full inventory after every answer.

Use applicable dimensions to discover missing decisions, not as a questionnaire:
interaction and domain semantics; data and side effects; failure and recovery;
authorization and privacy; compatibility; and acceptance. Follow newly exposed
issues when they change the outcome, and skip irrelevant or settled dimensions.

Discuss risks at the level the user needs to decide: for example, whether a
retry may duplicate an action, what survives a failure, or who may see data.
Record required outcomes and forbidden outcomes where they affect behavior,
scope, or acceptance. Do not require a transaction, concurrency, or security
checklist merely because the feature stores data or has side effects. Leave
internal mechanisms for subsequent design unless choosing one is necessary to
resolve the requirement or establish feasibility.

Compare approaches only when the choice affects the requirement under
discussion. Explain the consequential tradeoffs without manufacturing alternatives
or adding a separate detailed-design phase.

## Close at the agreed scope

Clarification is complete when decisions needed for the authorized next step
are resolved within the agreed scope. Distinguish confirmed decisions, unverified
assumptions, unresolved questions, and explicitly excluded or deferred work.
Acceptance should make different interpretations observable, using concrete
examples when helpful; avoid imposing a fixed template on a small decision.

If the user cannot decide yet, report the open choice and exactly which work it
blocks. A partial summary is useful but must not be labeled implementation-ready
for the blocked behavior. An agreed scope reduction or deferral can allow other
work to proceed; do not silently convert an unanswered question into a decision.

Deliver a concise account of the agreed outcome and any remaining blockers,
whether or not a file was created. Self-review it against evidence and the
conversation for consistency, completeness within scope, and testable acceptance.
Correct wording directly; return semantic gaps to the discussion.

Do not require repeated confirmation of decisions already made. Honor any
explicit final checkpoint; otherwise return to the originally authorized task.
If the user asked only for discussion or a brief, deliver it without starting
implementation. Do not invoke or prescribe another Skill. If requirements
change later, reopen only affected decisions.

## Record a brief when authorized

Resolve a small set of decisions in conversation without creating files. An
explicit request to create a brief authorizes the file; a request to revise one
authorizes updates within that scope. Otherwise propose a brief only when a
durable record would materially help, and obtain agreement before writing it.
Declining a file does not block work once the decisions are resolved.

A brief records the goal and success criteria, scope and non-goals, confirmed
behavior and constraints, acceptance examples or criteria, unresolved decisions,
and next step. Omit inapplicable sections. Include technical directions,
tradeoffs, or risk boundaries only when already established and relevant to the
requirements; do not perform extra design to fill headings.

Keep confirmed decisions separate from assumptions and open questions. Judge
clarity by whether the text permits conflicting interpretations of observable
behavior, scope, or acceptance, not by banning particular words. Explicit
deferral is valid when its scope and consequence are clear. Apply the same self-review used for conversational
outcomes before delivering or updating the file.

Use the user- or repository-specified location, including an existing brief being
revised. For a new brief without a specified location, use:

```text
.clarify-development-request/
└── YYYY_MM_DD_short-name_NNN/
    └── brief.md
```

Derive `short-name` from confirmed scope. Start `NNN` at `000` and use the next
unused sequence for the same date and name. Maintain that one file as decisions
change; do not create parallel notes. Do not modify ignore rules or stage the
artifact unless explicitly asked.

When updating a brief, check affected content and dependent conclusions, fixing
in-scope gaps and repetition while preserving confirmed decisions and project
conventions. Revisit the whole brief for an overall revision; do not reformat
historical briefs solely because these instructions changed. Link the file in
the final response whenever one was written or updated.
