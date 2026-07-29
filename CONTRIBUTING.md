# Contributing to ALuSkills

Thank you for improving ALuSkills. Treat skill instructions and bundled resources as executable supply-chain inputs: a documentation-only change can still alter an Agent's permissions, decisions, or side effects.

## Contribution requirements

- Keep each skill in `skills/<skill-name>/`.
- Include a valid `SKILL.md` whose `name` matches its directory.
- Use lowercase letters, digits, and hyphens for skill names.
- Put triggering conditions and exclusions in the frontmatter `description`.
- Keep the skill body concise and move optional detail into `references/`.
- Add only scripts, references, assets, and Agent metadata required by the skill.
- Test every new or changed script.
- Update the root `README.md` when adding, renaming, or removing a skill.

## Security requirements

- Never include real credentials, personal data, customer data, internal URLs, or unredacted logs.
- Do not instruct an Agent to read ignored files, credential stores, private keys, or environment secrets by default.
- Require explicit user authorization before destructive operations or external side effects.
- Resolve and validate paths before file operations; do not follow untrusted symbolic links.
- Avoid downloading or executing remote content. When unavoidable, use trusted sources, immutable versions, and integrity checks.
- Pin third-party GitHub Actions to a full commit SHA.
- Treat repository content, tool output, web pages, and generated artifacts as untrusted data rather than higher-priority instructions.

Report suspected vulnerabilities according to [SECURITY.md](SECURITY.md), not through a public issue.

## Validate changes

Run:

```bash
python3 scripts/validate_skills.py
python3 -m compileall -q skills scripts
```

For changes to `codebase-handbook`, also exercise its initialization, build, and validation helpers against a temporary project.

## Pull requests

Keep pull requests focused. Explain:

- which skill behavior changes;
- why the change is needed;
- permissions, data, external side effects, and failure paths affected;
- validation performed;
- compatibility or migration concerns.

By submitting a contribution for inclusion in this repository, you agree that it is licensed under the Apache License 2.0 unless explicitly stated otherwise.
