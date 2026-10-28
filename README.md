# ALuSkills

**English** | [简体中文](README.zh-CN.md)

Agent Skills for software development: evaluating proposals, clarifying
requirements, designing changes, testing, reviewing, and maintaining codebases.
Each Skill works independently and uses evidence with effort proportionate to
the task. Choose the ones you need; no fixed sequence is required.

## Skills

Follow a Skill link for details. The table describes declared usage conditions;
actual selection depends on the host agent. None is an always-on rule for every
task. Requests can be made in natural language; no Skill name is required.
Existing authorization remains valid within its scope.

| Skill | Use it for | Output | Activation and confirmation |
| --- | --- | --- | --- |
| [`reason-from-evidence`](skills/reason-from-evidence/SKILL.md) | Evaluating proposals without reflexive agreement or opposition | Judgment and supporting reasons | Context: proposal discussions or challenges to a conclusion; no entry confirmation |
| [`codebase-handbook`](skills/codebase-handbook/SKILL.md) | Navigating codebases and maintaining technical handbooks | Markdown handbook and HTML reading view | Context: consult an existing handbook or assess change impact; initialization requires a request, other writes require authorization |
| [`clarify-development-request`](skills/clarify-development-request/SKILL.md) | Resolving material requirement ambiguities | Decisions; optional `brief.md` | Context: material ambiguity prompts questions directly; a brief requires a request or agreement |
| [`write-technical-spec`](skills/write-technical-spec/SKILL.md) | Assessing design risk; writing, updating, and reviewing specs | `design.md` and supporting documents as needed | Context: assess material design risks; confirm proposed documents unless already requested |
| [`maintain-task-checkpoints`](skills/maintain-task-checkpoints/SKILL.md) | Preserving task state that is costly to reconstruct and resuming work | `STATE.md` | Context: assess recovery needs and confirm justified proposals; explicit requests authorize creation, then maintain within scope; check existing records on resume |
| [`develop-with-tdd`](skills/develop-with-tdd/SKILL.md) | Using focused TDD for regressions, complex logic, and contract changes | Code and tests | Context: regressions, complex logic, or contract changes; also on request; confirm substantial scope expansion |
| [`review-code-changes`](skills/review-code-changes/SKILL.md) | Reviewing diffs and fixing authorized findings | Review findings; authorized fixes | Request: review a diff; fixes require explicit authorization, persistent reports require a request or agreement |
| [`commit-changes`](skills/commit-changes/SKILL.md) | Committing authorized changes with informative messages | Git commit | Request: commit changes; follow repository approval rules and honor existing approval |
| [`write-weekly-report`](skills/write-weekly-report/SKILL.md) | Summarizing a week's Git commits | Weekly report | Request: write a weekly report or summarize a week of commits |

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
  reason-from-evidence \
  codebase-handbook \
  clarify-development-request \
  write-technical-spec \
  maintain-task-checkpoints \
  develop-with-tdd \
  review-code-changes \
  commit-changes \
  write-weekly-report
```

Verify the installation:

```bash
npx skills list --global
```

Restart the agent or open a new session after installation or update.

## Additional requirements

The `codebase-handbook` Python helpers require Python 3.9+ and PyYAML. Replace
`/path/to/codebase-handbook` with the installed Skill directory:

```bash
python3 -m pip install -r /path/to/codebase-handbook/scripts/requirements.txt
```

Run the helpers with the same Python environment.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for structure and validation requirements,
and [SECURITY.md](SECURITY.md) for reporting vulnerabilities.

## License

[Apache License 2.0](LICENSE) © 2026 Chengsong Lu
