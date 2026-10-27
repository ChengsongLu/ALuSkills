# Bundled diagram renderer

- Package: `@mermaid-js/tiny` 12.2.0 (MIT; see `mermaid.LICENSE`).
- Source: https://registry.npmjs.org/@mermaid-js/tiny/-/tiny-12.2.0.tgz
- File: unmodified `package/dist/mermaid.tiny.js`.
- SHA-256: `ea0cdf04eb31907eb20d956a34fe300095365c876887b54ffa29f1f847f56d00`.
- Upstream: https://github.com/mermaid-js/mermaid

The standalone Tiny bundle avoids runtime imports and network access. Its
embedded third-party license notices are retained. It excludes mindmaps,
architecture diagrams, KaTeX, and optional plugins. Mermaid 12 targets ES2024;
use a modern browser (Safari 17.4+ or current Chromium/Firefox). Older browsers
retain source fallback. The renderer adds approximately 3.75 MB to HTML files
containing Mermaid, because the script is embedded as a base64 data URL.

To upgrade, obtain a pinned package from the upstream npm registry, replace
the bundle and license, update this notice and the builder integrity hash,
and run the helper regression suite plus offline browser checks for common
diagrams, invalid syntax, hostile content, theme changes, zoom, and navigation.
Rebuild existing HTML after upgrading; the handbook input hash does not track
renderer changes. Package fetching is a maintainer operation, never part of
handbook initialization, building, or reading.
