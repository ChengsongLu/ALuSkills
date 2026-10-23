# Handbook Specification

## Files and policy

Keep all files under the project-root `.codebase-handbook/`:

```text
config.yaml
preferences.md
manifest.yaml
index.md
handbook.html
<topic-groups>/<chapter>.md
```

Create only needed topic directories. Chapters must use paths inside this
folder; absolute paths, parent traversal, and escaping symbolic links are
rejected. The handbook directory itself must not be a symbolic link.

Read `preferences.md` as user-maintained project requirements; never edit it.
Preserve configured policy and unknown YAML fields. Helpers use safe YAML
loading and reject duplicate mapping keys or invalid known field types.
Supported schema versions are 1 and 2; retain an existing version during
ordinary updates. New handbooks use version 2.

```yaml
schema_version: 2
language: auto
scan:
  tracked_files_only: true
  respect_gitignore: true
  exclude_generated: true
source_references:
  durable_line_numbers: false
html:
  title: auto
  show_source_evidence: true
```

The scan and source-reference settings guide the Agent's analysis; the helpers
do not scan the repository to enforce them. Resolve automatic prose language
from maintained repository documentation or the user's request; ask only when
no reliable preference exists. Set an explicit language tag when known.

HTML title precedence is CLI `--title`, configured title, then project folder
name. `show_source_evidence: false` omits generated evidence and trigger panels
and their search metadata; it does not redact authored chapter content and is
not a privacy filter.

## Compact manifest

```yaml
schema_version: 2
handbook_status: draft
chapters:
  - id: authentication
    path: modules/authentication.md
    summary: Explains session authentication and token refresh boundaries.
    status: verified
    sources:
      - src/auth/service.py
      - tests/auth/test_sessions.py
unresolved: []
```

Use stable IDs, handbook-relative chapter paths, and project-relative source
paths. Direct sources should be sufficient to locate evidence. Symbol entries
use `path::Symbol`; source symbol existence still requires manual inspection.

Optional chapter fields:

- `kind`: dominant purpose, such as module, flow, state-machine, or guide;
- `part`, `order`: reading organization;
- `read_when`, `concepts`: useful task and terminology routes;
- `source_symbols`: selected stable evidence locations;
- `related`: related chapter IDs;
- `update_triggers`: broader source globs not adequately covered by sources;
- `coverage`, `evidence_status`: existing or specifically useful depth and
  evidence classifications, not mandatory parallel bookkeeping.

Optional `parts` entries use `id`, `title`, `purpose`, and `order`. Ungrouped
chapters are allowed. Optional `coverage_inventory` entries use `area`, `kind`,
`disposition` (`covered` or `excluded`), chapter IDs in `chapters`, and a `reason`
for exclusions. Keep these maps at responsibility level, not file level.

## Status and compatibility

`status` and `handbook_status` use `planned`, `draft`, `verified`, or
`needs-review`. Planned chapters may not yet have prose. Verified means the
material claims were checked at the time; it does not prove present freshness
or exhaustive coverage. Keep important gaps in `unresolved` and visible in the
index. A verified handbook cannot contain unfinished chapters.

When present, `coverage` uses `outline`, `substantial`, or `complete`;
`evidence_status` uses `partial`, `verified`, `stale`, or `conflicted`.
A verified chapter cannot simultaneously declare unverified evidence. Preserve
these fields in existing books; do not force migration or add them to every
new chapter. A short overview is not inherently incomplete.

## Chapters and protection

Use the [writing guide](evidence-and-writing.md) for chapter content and local
compression. `index.md` provides a first reading path, important task routes,
and visible status or gaps. Avoid manually duplicating the generated book map.

Never automatically edit a `Maintainer notes` section or content between:

```markdown
<!-- codebase-handbook:preserve:start -->
Protected content
<!-- codebase-handbook:preserve:end -->
```

When protected content conflicts with evidence, preserve it and flag the
chapter for review. Otherwise update authorized affected explanations in place.

## HTML and validation

Generate `handbook.html`; do not edit it manually. Build after changing
configuration, preferences, manifest, index, or registered chapters. See
[html-view.md](html-view.md).

Validation covers known structure, source paths, chapter links and anchors,
and the HTML input hash. It does not prove semantic accuracy, symbol existence,
external-document anchor validity, or that the HTML output was not tampered
with. Rebuild using the current helper when its renderer changes.
