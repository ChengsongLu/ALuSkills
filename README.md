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
| [`write-technical-spec`](skills/write-technical-spec/) | Creating, updating, or reviewing a repository-grounded design | Optional `flow.md`, `design.md`, and `implement.md` |
| [`develop-with-tdd`](skills/develop-with-tdd/) | Implementing selected high-risk behavior with focused TDD | Source code and tests |
| [`review-code-changes`](skills/review-code-changes/) | Reviewing a diff and safely remediating authorized findings | Optional `review.md`, `coverage.md`, and `remediation.md` |
| [`maintain-task-checkpoints`](skills/maintain-task-checkpoints/) | Preserving recoverable state for long or interruption-prone work | `STATE.md` and `CHECKPOINTS.md` |
| [`codebase-handbook`](skills/codebase-handbook/) | Building and maintaining an evidence-linked technical handbook | Markdown chapters, `manifest.yaml`, and `handbook.html` |

### clarify-development-request

Use this Skill when a development request contains unresolved decisions that
would change behavior, contracts, scope, or acceptance criteria. It inspects the
repository first, asks one decision-changing question at a time, and produces a
confirmed `brief.md`. It skips ordinary consultation, mechanical edits, and
well-specified low-risk work.

### write-technical-spec

Use this Skill to create, update, or review a technical specification. It checks
requirements against the repository, defines relevant flows, boundaries,
contracts, failure behavior, and validation, and produces `design.md`,
`implement.md`, and an optional `flow.md`. Review mode is read-only.

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
likely to be interrupted, or explicitly needs a handoff. It records current
state and completed checkpoints without storing credentials or replacing Git.
Implicit activation requires confirmation before writing files.

### codebase-handbook

Use this Skill to initialize, consult, synchronize, validate, or render a
repository's technical handbook. It explains stable architecture, runtime
behavior, state, failures, and relationships with source evidence. Every write
stays under `.codebase-handbook/`; source code and ordinary repository files
remain read-only evidence.

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
