# HTML Reading View

## Contract

Generate one self-contained page at `.codebase-handbook/handbook.html`. Keep
Markdown and YAML as the editable source of truth. Never manually edit the
generated HTML.

The page must:

- work when opened directly without a local server;
- embed its content, styling, and interaction code;
- escape raw handbook HTML rather than executing it;
- expose the part and chapter hierarchy as a book contents tree;
- provide full-text search with chapter context and result snippets;
- provide breadcrumbs, an on-page contents list, heading deep links,
  previous/next navigation, related-topic navigation, and light/dark themes;
- foreground a concise chapter summary, read-when guidance, key concepts, and
  the authored explanation when those fields are available;
- render chapter summaries in the generated book map so readers can choose a
  chapter by purpose rather than title alone;
- include manifest summaries, concepts, tasks, source paths, symbols, and
  update triggers in full-text search when evidence display is enabled;
- keep workflow status, coverage depth, evidence status, source evidence, and
  update triggers in a collapsible maintenance section;
- preserve browser back and forward navigation;
- provide keyboard focus states, a skip link, an associated search label, and
  reduced-motion behavior;
- include only `index.md` and chapters registered in `manifest.yaml`;
- exclude `preferences.md`, configuration, and unresolved internal metadata
  from displayed prose;
- record a deterministic hash of all display and requirement inputs.

Embed the bundled Mermaid Tiny renderer only when Mermaid blocks are present.
Render diagrams offline with strict security, without external fonts, images,
plugins, or a CDN. Block diagram configuration frontmatter and init directives
so authored content cannot override viewer settings. Keep the original source
in an expandable section; show it with a local error message when rendering
fails or the syntax is unsupported. A failed diagram must not break navigation
or other diagrams. Without JavaScript, diagram source remains visible.

Provide keyboard-accessible fit, actual-size, and zoom controls and a focusable
scroll area for wide diagrams. Re-render for theme changes; render chapters
when opened so hidden content does not produce incorrect layout. Wide tables
scroll within the reading column, with visible headers and top-aligned cells.
Keep normal prose readable on narrow screens without page-level overflow.

The bundled version, license, integrity hash, and update procedure live in
`assets/vendor/NOTICE.md`. Tiny supports the common technical diagram types;
mindmaps, architecture diagrams, KaTeX, and optional plugins are excluded.
Unsupported diagrams retain their source and a visible fallback message.

The landing chapter should present the authored `index.md` plus a generated
book map. Do not use a single dense relationship graph as the primary
navigation for a large handbook.

Treat this page as the human reading projection. Do not require an Agent to
parse it for task routing or code evidence; `manifest.yaml`, `index.md`, chapter
Markdown, and the repository remain the Agent-facing sources.

Keep the design content-first. Do not hide the authored mental model, main
runtime flow, boundaries, or failure consequences behind interaction. Use
progressive disclosure only for verification and maintenance metadata that is
important but secondary during normal reading.

## Build

Run:

```bash
python3 <skill-dir>/scripts/build_handbook.py --project-root <project-root>
```

Use `--title` for an explicit per-build title override; otherwise use
`html.title` from config or derive the title from the project directory name.
Install `scripts/requirements.txt` before running helpers.
`html.show_source_evidence: false` hides generated evidence and trigger panels
and their search metadata, not citations authored in Markdown.

Regenerate after changing:

- `config.yaml`;
- `preferences.md`;
- `manifest.yaml`;
- `index.md`;
- any chapter registered in `manifest.yaml`.

## Validation

The builder hashes the relative path and content of every input above and embeds
the result in a meta tag. `validate_handbook.py` recalculates the hash and fails
when the page is missing or stale.

Do not use this hash as semantic validation. It checks the recorded input hash, not output integrity or the current
renderer version. Rebuild after upgrading the helper.

Perform static accessibility checks after builder changes. When browser tooling
is available, also verify desktop and narrow layouts, keyboard navigation,
search, deep links, history navigation, and theme switching.

## Git policy

Do not prescribe whether `handbook.html` or any other handbook file is tracked,
untracked, or ignored. This is a repository policy chosen by the user.
