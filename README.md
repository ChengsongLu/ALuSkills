# ALuSkills

**English** | [简体中文](README.zh-CN.md)

Help coding agents do more than generate code—help them reliably complete the critical engineering work involved in software development.

ALuSkills is a collection of Agent Skills designed for real-world codebases. Together, they cover the complete workflow from an incoming requirement to design, implementation, code review, long-running task recovery, and knowledge capture:

```text
Ambiguous request → Development brief → Technical specification → Implementation and review → Task recovery → Codebase handbook
```

They emphasize:

- **Working from repository evidence**: read the relevant code, tests, and documentation before reaching conclusions;
- **Producing inspectable artifacts**: persist requirements, designs, review results, and task state instead of leaving them only in a conversation;
- **Covering difficult paths**: account for failures, recovery, concurrency, compatibility, security, and external side effects;
- **Triggering only when needed**: keep simple tasks simple and avoid imposing extra process on low-risk changes.

These Skills follow the [Agent Skills specification](https://agentskills.io/specification) and can be installed in Codex, Claude Code, Cursor, and other compatible agents through the [`skills`](https://github.com/vercel-labs/skills) CLI.

## 1. Installation

Installation uses the [`skills`](https://github.com/vercel-labs/skills) CLI and requires Node.js and `npx` on your machine.

### 1.1 List available Skills

The following command only lists the Skills; it does not install them:

```bash
npx skills add ChengsongLu/ALuSkills --list
```

Confirm that the source is `ChengsongLu/ALuSkills` and that 5 skills are listed.

### 1.2 Install all Skills globally

Interactive mode is recommended for the first installation:

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global
```

During installation, focus on these steps:

1. **Select agents**

   Use `↑` and `↓` to move, `Space` to select, and `Enter` to confirm.

   - Codex and Cursor are included in `Universal (.agents/skills)` and do not need to be selected separately;
   - For Claude Code, additionally select `Claude Code` under `Additional agents`;
   - Do not select agents you do not use, to avoid creating unrelated directories or links.

2. **Review the installation summary**

   You should see 5 skills installed in `~/.agents/skills/`. Entries such as `copy → Codex ...` mean those agents can read the universal copy and are expected.

   If you need Claude Code, also confirm that the summary includes `Claude Code`. If it does not, select `No` and run the installation again.

3. **Confirm installation**

   At `Proceed with installation?`, select `Yes` and press `Enter`.

Restart your agent or start a new session after installation.

### 1.3 Specify agents directly

Skip the interactive prompts and install for Codex:

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global --agent codex --yes
```

Install for Claude Code:

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global --agent claude-code --yes
```

Install for Cursor:

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global --agent cursor --yes
```

Install for all three:

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global \
  --agent codex --agent claude-code --agent cursor --yes
```

### 1.4 Installation locations

| Agent | Project directory | Global directory |
| --- | --- | --- |
| Codex | `.agents/skills/` | `~/.codex/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |

The CLI may place a shared copy in `~/.agents/skills/` for agents to read directly or link to. Treat the paths shown in `Installation Summary` as authoritative.

### 1.5 Update

Update the globally installed ALuSkills:

```bash
npx skills update --global \
  clarify-development-request \
  write-technical-spec \
  review-code-changes \
  maintain-task-checkpoints \
  codebase-handbook
```

This command updates only the 5 listed skills. To update all globally installed skills from every source, use:

```bash
npx skills update --global
```

Restart your agent or start a new session after updating so that the new Skill content and trigger rules take effect.

### 1.6 Verify

```bash
npx skills list --global
```

The output should include the 5 skills from this repository.

## 2. Skills

| Skill | Problem it solves | Key artifacts |
| --- | --- | --- |
| [`clarify-development-request`](skills/clarify-development-request/) | Determines and confirms whether structured clarification is needed, then produces an implementation-ready brief | `brief.md` |
| [`write-technical-spec`](skills/write-technical-spec/) | Determines whether a task needs a technical specification and, after confirmation, turns it into a repository-aligned design | Optional `flow.md`, `design.md`, and `implement.md` |
| [`review-code-changes`](skills/review-code-changes/) | Reviews changes and safely remediates explicitly authorized findings with a final re-review | Optional `review.md`, `coverage.md`, and `remediation.md` |
| [`maintain-task-checkpoints`](skills/maintain-task-checkpoints/) | Determines and confirms whether recovery state should be persisted so complex tasks can continue safely | `STATE.md` and `CHECKPOINTS.md` |
| [`codebase-handbook`](skills/codebase-handbook/) | After confirming scope and structure, captures codebase behavior in an isolated technical book | Markdown chapters, `manifest.yaml`, and `handbook.html` |

### 2.1 clarify-development-request

Before non-trivial development begins, this Skill investigates relevant code, tests, and documentation, then asks only the questions that would genuinely change product behavior, contracts, scope, or acceptance outcomes. It first makes a lightweight decision without writing files. Mechanical edits, clearly low-risk tasks, and work involving only local implementation choices exit immediately without creating `brief.md`. When implicitly triggered and material decisions remain unresolved, it explains the evidence and impact, recommends whether to enter structured clarification, and waits for confirmation before writing files. Explicit requests to clarify requirements, confirm a request item by item, ask one question at a time, first get the requirements clear, collaboratively define feature behavior or boundaries, or create a brief authorize entry without redundant confirmation. Once the brief is complete, the Skill performs a self-review, waits for user approval, reports clarification complete, and stops without invoking or requiring another Skill.

Use it to:

- Turn a one-line request into an implementation-ready brief;
- Clarify a feature one decision at a time when the user asks for item-by-item confirmation;
- Define goals, scope, non-goals, and acceptance criteria;
- Clarify state, failure semantics, compatibility, security, and side-effect boundaries;
- Resolve open decisions that would affect downstream work while remaining independent of other Skills.

It is not intended for ordinary consultation, diagnosis-only or review-only work, mechanical edits, or clearly specified low-risk tasks.

**Simple usage example**

> **User:** Add an order-export feature.
>
> **Agent:** I inspected the existing order query and permission logic. The repository does not determine the export format or maximum record count; these choices affect the API, performance limits, and acceptance criteria. I recommend entering structured clarification with `clarify-development-request`, which will create a `brief.md` after we resolve the open decisions. Would you like to proceed?
>
> **User:** Yes.
>
> **Agent:** Which format should the first release support: CSV, XLSX, or both? I recommend CSV only because it supports streaming and keeps the initial scope smaller.
>
> **User:** CSV only.
>
> **Agent:** Should the export contain the user's current filtered results or all orders they can access? This choice changes both the request contract and acceptance tests.
>
> **User:** Export the current filtered results, with a limit of 10,000 records.
>
> **Agent:** Understood. I will record CSV-only export, reuse of the current filters and permissions, and the 10,000-record limit in `brief.md`, together with failure behavior and testable acceptance criteria. I will self-review the brief and ask you to confirm it before design or implementation begins.

The Agent does not ask questions that repository evidence can answer. If the repository and the request already determine the required behavior, it continues normally without starting the clarification workflow.
After the user confirms `brief.md`, the Skill stops and waits for the user to choose the next action. It does not automatically enter specification, planning, or implementation and has no dependency on another Skill.

**Key artifact**

```text
.clarify-development-request/
└── 2026_07_29_export-orders_000/
    └── brief.md
```

Example `brief.md`:

```markdown
# Export orders

## Goal and success criteria
- Users can export the currently filtered results rather than all orders.
- Export requests containing up to 10,000 records finish within 30 seconds.

## Scope
- Support CSV; XLSX is out of scope for this change.
- Reuse the existing order-query permissions and filters.

## Failure behavior
- Do not produce an incomplete file when export fails, and return a retryable message to the user.

## Acceptance
- Cover empty results, insufficient permissions, over-limit requests, and generation failures.
```

Install:

```bash
npx skills add ChengsongLu/ALuSkills --skill clarify-development-request --global
```

### 2.2 write-technical-spec

This Skill first distinguishes creation, update, and review modes. In creation mode, it uses current repository evidence and task complexity to confirm whether to enter the technical-specification workflow, then confirms whether a separate `flow.md` is needed. Update mode repeats the relevant gate only when a change materially expands scope or changes the document set. Review mode performs a read-only implementation-readiness review of an existing specification without modifying documentation or code. The Skill independently reviews requirement completeness, cross-document consistency, repository feasibility, state and failure boundaries, and test verifiability. It does not depend on another Skill. It ends with an explicit gate result of `READY`, `READY WITH NON-BLOCKING FINDINGS`, or `BLOCKED`, and coding does not begin until blocking findings are resolved.

Use it to:

- Write technical proposals or design documents;
- Draw happy-path and failure-handling flows with Mermaid;
- Plan module, interface, data, state, and compatibility changes;
- Define phased implementation and validation strategies;
- Review whether an existing design is complete and consistent with the repository.

**Key artifacts**

```text
.write-technical-spec/
└── 2026_07_29_export_orders_000/
    ├── flow.md       # Optional: flows and important branches
    ├── design.md     # Design boundaries, contracts, and decisions
    └── implement.md  # Phased changes and validation plan
```

Example `design.md`:

```markdown
## Design

- `OrderExportService` receives authorized query conditions and does not reimplement permission checks.
- The query uses a read-only pagination cursor, writes batches to a temporary file, and publishes it atomically only after success.
- If any batch fails, delete the temporary file and do not return a partial export.

## Compatibility

- The existing order-query API remains unchanged.
- The new export endpoint reuses the current filter-parameter format.
```

Install:

```bash
npx skills add ChengsongLu/ALuSkills --skill write-technical-spec --global
```

### 2.3 review-code-changes

This Skill performs evidence-driven reviews of working-tree diffs, staged changes, specific commits, branch comparisons, or pull requests. After freezing a read-only baseline, it recommends either a lightweight or persistent review based on actual risk. A normal code-review request authorizes only read-only inspection; if the user has not explicitly requested a formal or persistent report, the Skill must ask for confirmation before creating `.review-code-changes/`, `review.md`, or `coverage.md`. Both modes inspect correctness, reliability, security, compatibility, tests, and documentation risks from the perspective of contracts and adversarial failures.

Use it to:

- Review current uncommitted changes;
- Review a specific commit or branch diff;
- Inspect state, concurrency, persistence, retry, cancellation, and failure-recovery paths;
- Produce findings with evidence, impact levels, and remediation direction;
- Fix confirmed findings after the user explicitly authorizes changes;
- Challenge each proposed fix for new vulnerabilities and regressions before implementation;
- Re-review the final remediation diff and affected paths, repeating the fix-and-review cycle until no credible remediation-caused issue remains.

By default, it reviews only and does not modify implementation files. During
authorized remediation, passing tests do not replace the required final
re-review.

**Key artifacts**

```text
.review-code-changes/
└── 2026_07_29_working-tree_000/
    ├── review.md       # Confirmed findings and overall conclusion
    ├── coverage.md     # Coverage record for large or high-risk reviews
    └── remediation.md  # Authorized fixes, validation, and final re-review evidence
```

Example `review.md`:

```markdown
## [P1] Do not expose an export file before publication is complete

`export_orders.py:84` saves the download URL to the database before the final batch has been written.
A concurrent download can read an incomplete CSV, and after a process crash the URL can permanently point to a partial file.

Write to a temporary path first, close and validate the file, move it atomically, and update the download state at the same commit boundary.
```

Install:

```bash
npx skills add ChengsongLu/ALuSkills --skill review-code-changes --global
```

### 2.4 maintain-task-checkpoints

This Skill maintains compact recovery state for long-running, multi-stage, or expensive-to-recover development tasks. When triggered implicitly, it first evaluates the actual recovery cost, explains the recommendation, directory, files, and recorded content, and waits for confirmation before creating a checkpoint. When the user explicitly requests checkpoints or handoff artifacts, it does not ask for redundant confirmation. Once activated, it can continue updating within the confirmed task identity, scope, location, and artifact set; expanding the persisted scope requires confirmation again.

Use it for:

- Complex development spanning multiple modules and phases;
- Tasks involving migrations, state machines, concurrency, or external side effects;
- Work that must be handed off between agents;
- Tasks where interruption could cause dangerous operations to be repeated;
- Any task for which the user explicitly requests saved checkpoints.

Short, low-risk tasks that can be completed in one pass should not create checkpoints.

**Key artifacts**

```text
.maintain-task-checkpoints/
└── 20260729-143000-export-orders/
    ├── STATE.md        # Current recoverable state
    └── CHECKPOINTS.md  # Append-only phase history
```

Example `STATE.md`:

```markdown
## Current state

- Status: in_progress
- Completed: export query and streaming CSV writer
- Current: implementing atomic publication of the temporary file
- Next: add failure-injection tests and validate performance with 10,000 records

## Validation

- Passed: 18/18 unit tests
- Pending: temporary-file cleanup test after process interruption

## Do not repeat

- The test database migration has already run; do not create the same index again.
```

Install:

```bash
npx skills add ChengsongLu/ALuSkills --skill maintain-task-checkpoints --global
```

### 2.5 codebase-handbook

This Skill creates and maintains a `.codebase-handbook/` technical handbook inside a repository. Rather than presenting a file-by-file API inventory, it works as a technical book that explains stable concepts, module responsibilities, runtime flows, state transitions, failure behavior, system relationships, and the corresponding source evidence. Complete coverage, evidence, and update-trigger relationships live in `manifest.yaml`. Chapter prose prioritizes core conclusions, mental models, important flows, and boundaries, followed by editorial compression that prevents evidence analysis from reading like a source-code traversal log. All writes are confined to `.codebase-handbook/`; source code, configuration, tests, ordinary documentation, and agent instruction files such as `AGENTS.md` are read-only evidence and are never modified by the Skill. Initialization authorizes only an empty skeleton and read-only discovery. After evidence produces a recommended scope, chapter structure, and writing batches, the Skill waits for confirmation. It also requires confirmation before an implicit synchronization expands scope or before chapters are split, merged, renamed, or deleted.

Use it to:

- Initialize a technical handbook for a codebase;
- Navigate and understand an existing handbook;
- Synchronize architecture and behavior documentation before or after code changes;
- Validate handbook structure, references, and coverage;
- Generate a visualization-friendly, self-contained HTML reading view;
- Split, merge, or otherwise evolve handbook chapters.

**Key artifacts**

```text
.codebase-handbook/
├── index.md
├── manifest.yaml
├── architecture/
│   └── system-overview.md
├── flows/
│   └── order-export.md
└── handbook.html
```

Example chapter:

```markdown
# Order export flow

Read this chapter when changing order queries, permission checks, file storage, or download state.

Order export separates long-running file generation from the request lifecycle. The database task record owns export state, while the published file in storage is the downloadable result. File publication is an indivisible commit boundary.

## Runtime behavior

1. The API layer validates user permissions and normalizes filters.
2. Export Service reads orders page by page and writes a temporary CSV.
3. After the file is fully closed, it is published atomically and the task is marked ready.

## Key boundaries

- Download clients must not observe temporary files.
- File publication creates an external side effect; recovery must not blindly rerun the export after publication.

## Failure and recovery

- Failure before publication: delete the temporary file and mark the task failed.
- State update failure after publication: the recovery task scans storage results and reconciles database state.

## Source evidence
- `src/orders/export_service.py::OrderExportService`
- `src/jobs/export_orders.py::run_export`
```

`handbook.html` is generated from the Markdown chapters and `manifest.yaml`. It is a self-contained page that can be opened directly without a local server. Designed for human readers, it emphasizes chapter purpose, capability summaries, key concepts, and narrative flows, while placing source evidence, update triggers, and validation state in expandable maintenance sections. It retains a book-style table of contents, full-text search, chapter map, breadcrumbs, in-page table of contents, previous/next and related-topic navigation, light and dark themes, and a responsive layout. Agents use `manifest.yaml` and `index.md` first to locate relevant chapters, source files, stable symbols, and change-trigger relationships, then read source code as needed for verification instead of parsing the generated HTML.

**`handbook.html` preview**

![The reading view generated for codebase-handbook's handbook.html, with a table of contents, search, status indicators, and volume-based chapter navigation](docs/images/codebase-handbook-html-preview.png)

On desktop, the table of contents and full-text search stay fixed on the left, while the reading area shows handbook status, coverage, evidence state, and a volume-based chapter map. The same self-contained file also supports light and dark themes and narrow-screen reading.

This Skill does not initialize a handbook merely because an ordinary coding task is underway; initialization requires an explicit user request.

Install:

```bash
npx skills add ChengsongLu/ALuSkills --skill codebase-handbook --global
```

## 3. Repository structure

Each Skill is an independent directory containing at least one `SKILL.md` with YAML frontmatter:

```text
skills/
├── clarify-development-request/
├── codebase-handbook/
├── maintain-task-checkpoints/
├── review-code-changes/
└── write-technical-spec/
```

Every Skill contains `agents/openai.yaml`; some also contain `scripts/`, `references/`, or `assets/`. During installation, these dependencies are copied or linked to the target agent's Skills directory together with the corresponding `SKILL.md`.

## 4. License

This project is licensed under the [Apache License 2.0](LICENSE).

Copyright 2026 Chengsong Lu.
