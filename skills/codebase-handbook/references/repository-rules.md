# Repository Agent Rules

## Purpose

Leave a concise, durable instruction that tells future Coding Agents that the
handbook exists and must be consulted around relevant code changes. Do not copy
the full skill into repository instructions.

## Select the target

1. Discover the Agent instruction files that apply at the project root, such as
   `AGENTS.md`, `CLAUDE.md`, or an explicitly configured equivalent.
2. Determine their actual scope and precedence.
3. Update only the files required for the repository's intended Agent surfaces.
4. Do not duplicate the same rule into every discovered file without a reason.
5. Ask before creating a new instruction file when none exists.

## Preserve the original format

Before editing, read the entire target file and identify:

- language;
- heading hierarchy;
- list and numbering style;
- terminology;
- section ordering;
- spacing and line-ending conventions;
- existing documentation or change-management rules.

Then:

- insert the smallest sufficient rule at the semantically appropriate location;
- match the existing language and formatting;
- merge with equivalent rules instead of adding a duplicate;
- avoid reflowing, formatting, reordering, or rewriting unrelated text;
- inspect the final diff for unrelated changes;
- stop and ask when the new rule conflicts with an existing instruction.

Never replace the file with a fixed template.

## Required meaning

Express these requirements using the repository's style:

1. Before planning or changing existing behavior, read
   `.codebase-handbook/index.md` and follow the relevant reading path.
2. Use `$codebase-handbook` when available to analyze handbook impact.
3. After implementation, inspect the actual Git diff and every affected or
   conditionally affected chapter.
4. Update the handbook only when design, responsibilities, runtime behavior,
   contracts, relationships, or durable source references changed.
5. Regenerate `handbook.html` after handbook source changes.
6. Validate the handbook before completing the task.

Keep the repository rule concise and point to the installed skill for detail.

## Idempotent updates

Prefer an existing unique heading for future discovery. If the target file
already uses managed HTML comments, follow that convention. Do not introduce
HTML markers solely for convenience when they conflict with the file's style.

Record the target file and discoverable section heading in
`manifest.yaml.repository_rules.files`. On later updates, find the section by
meaning as well as title because maintainers may rename it.

Treat all existing content as intentional. Never infer authorship from Git
history, commit author, prose style, or generated-looking text.
