# ALuSkills

**English** | [简体中文](README.zh-CN.md)

ALuSkills is a collection of Agent Skills for reliable software development in
real codebases:

```text
Requirement → Specification → TDD implementation → Review → Recovery → Handbook
```

The Skills work from repository evidence, focus on difficult behavior and
failure paths, and avoid adding process to simple tasks. Each Skill is
self-contained, independently installable, and does not rely on another Skill.

## Skills

| Skill | Use it for | Output |
| --- | --- | --- |
| [`clarify-development-request`](skills/clarify-development-request/) | Resolving material requirement decisions before implementation | `brief.md` |
| [`write-technical-spec`](skills/write-technical-spec/) | Assessing spec needs and creating, updating, or reviewing a repository-grounded design | Optional `flow.md`, `design.md`, and `implement.md` |
| [`develop-with-tdd`](skills/develop-with-tdd/) | Implementing selected high-risk behavior with focused TDD | Source code and tests |
| [`review-code-changes`](skills/review-code-changes/) | Reviewing a diff and safely remediating authorized findings | Optional `review.md`, `coverage.md`, and `remediation.md` |
| [`maintain-task-checkpoints`](skills/maintain-task-checkpoints/) | Assessing persistence needs and recovering interrupted work from checkpoints | `STATE.md` and `CHECKPOINTS.md` |
| [`codebase-handbook`](skills/codebase-handbook/) | Navigating codebases through existing handbooks and maintaining them | Markdown chapters, `manifest.yaml`, and `handbook.html` |

### clarify-development-request

Use this Skill when a development request contains unresolved decisions that
would change behavior, contracts, scope, or acceptance criteria, even when the
user has not requested clarification. It inspects repository facts first and
confirms implicit entry before asking structured questions and writing
`brief.md`. Explicit clarification requests authorize entry. It skips ordinary
consultation, mechanical edits, and well-specified low-risk work.

### write-technical-spec

Use this Skill to assess spec needs when a development request or repository
investigation reveals interacting changes or material design risk, even without
a spec request. Implicit assessment is read-only; localized low-risk work
continues without an entry question or artifacts. Recommended entry requires
confirmation before writing. Explicit creation, updates, and read-only reviews
remain supported. Authoring defines flows, boundaries, contracts, failure
behavior, and validation in `design.md`, `implement.md`, and optional `flow.md`.

### develop-with-tdd

Use this Skill when the user explicitly requests TDD or when a regression,
complex rule, state transition, concurrency behavior, security boundary,
external contract, or side effect needs focused protection. It maps each test
to confirmed behavior, selects a stable test seam, and runs small
red-green-refactor cycles. It creates no separate workflow artifact and does
not impose TDD on low-risk changes.

### review-code-changes

Use this Skill to review a working-tree diff, commit, branch comparison, or pull
request. It checks correctness, reliability, security, compatibility, testing,
and documentation. Reviews remain read-only unless remediation is explicitly
authorized; completed remediation is validated and reviewed again.

### maintain-task-checkpoints

Use this Skill when a task is long-running, multi-stage, expensive to recover,
likely to be interrupted, or explicitly needs a handoff. Also use it to resume
interrupted work or continue with incomplete context by locating and verifying
a matching checkpoint against current instructions, source, and Git. Recovery
does not require the remaining task to be complex or authorize new files.
Creating persistent state implicitly requires confirmation; routine updates
stay within the previously confirmed scope. Checkpoints never store credentials
or replace Git.

### codebase-handbook

Use this Skill to initialize, consult, synchronize, validate, or render a
repository's technical handbook. When a handbook exists, also use it for
codebase questions about architecture, responsibilities, flows, contracts, and
implementation locations without requiring the user to mention the handbook.
Navigation is read-only and verifies relevant stale evidence against source;
it does not authorize handbook writes or initialize a missing handbook.
Changes affecting documented behavior or cited symbols trigger an impact
assessment. Every handbook write stays under `.codebase-handbook/`; source code
and ordinary repository files remain read-only evidence for this Skill.

## Install and update

Installation requires Node.js and `npx`.

List available Skills:

```bash
npx skills add ChengsongLu/ALuSkills --list
```

Install all Skills globally:

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global
```

Install one Skill for a specific agent:

```bash
npx skills add ChengsongLu/ALuSkills \
  --skill develop-with-tdd --global --agent codex --yes
```

Replace the Skill name and agent with the ones you need. Common agent values
include `codex`, `claude-code`, and `cursor`.

Update the ALuSkills installed globally:

```bash
npx skills update --global \
  clarify-development-request \
  write-technical-spec \
  develop-with-tdd \
  review-code-changes \
  maintain-task-checkpoints \
  codebase-handbook
```

Verify the installation:

```bash
npx skills list --global
```

Restart the agent or open a new session after installation or update.

## Repository structure

```text
skills/
├── clarify-development-request/
├── codebase-handbook/
├── develop-with-tdd/
├── maintain-task-checkpoints/
├── review-code-changes/
└── write-technical-spec/
```

Every Skill contains `SKILL.md` and `agents/openai.yaml`. A Skill includes
`references/`, `scripts/`, or `assets/` only when its workflow needs them.

## License

[Apache License 2.0](LICENSE) © 2026 Chengsong Lu
