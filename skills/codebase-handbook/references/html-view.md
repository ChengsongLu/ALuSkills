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
  update triggers in full-text search;
- keep workflow status, coverage depth, evidence status, source evidence, and
  update triggers in a collapsible maintenance section;
- preserve browser back and forward navigation;
- provide keyboard focus states, a skip link, an associated search label, and
  reduced-motion behavior;
- include only `index.md` and chapters registered in `manifest.yaml`;
- exclude `preferences.md`, configuration, and unresolved internal metadata
  from displayed prose;
- record a deterministic hash of all display and requirement inputs.

Mermaid code blocks remain safely visible as diagram source unless a future
self-contained renderer is bundled. Do not require a CDN or network access.

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

Use `--title` only when the user or `preferences.md` specifies a display title.
Otherwise derive the title from the project directory name.

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

Do not use this hash as semantic validation. It proves only that the HTML view
was built from the current handbook inputs.

Perform static accessibility checks after builder changes. When browser tooling
is available, also verify desktop and narrow layouts, keyboard navigation,
search, deep links, history navigation, and theme switching.

## Git policy

Do not prescribe whether `handbook.html` or any other handbook file is tracked,
untracked, or ignored. This is a repository policy chosen by the user.
