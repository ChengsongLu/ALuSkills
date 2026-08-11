#!/usr/bin/env python3
"""Build a self-contained book-style HTML view from handbook sources."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote


HANDBOOK_DIR = ".codebase-handbook"
OUTPUT_NAME = "handbook.html"
HASH_INPUTS = ("config.yaml", "preferences.md", "manifest.yaml", "index.md")


@dataclass
class Part:
    part_id: str
    title: str = ""
    purpose: str = ""
    order: int = 0


@dataclass
class DisplayChapter:
    chapter_id: str
    path: str
    summary: str = ""
    part: str = ""
    order: int = 0
    kind: str = "chapter"
    status: str = "planned"
    coverage: str = "outline"
    evidence_status: str = "partial"
    related: list[str] = field(default_factory=list)
    concepts: list[str] = field(default_factory=list)
    read_when: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    source_symbols: list[str] = field(default_factory=list)
    update_triggers: list[str] = field(default_factory=list)
    title: str = ""
    markdown: str = ""


@dataclass
class RenderedMarkdown:
    body: str
    headings: list[tuple[int, str, str]]


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def integer(value: str, default: int = 0) -> int:
    try:
        return int(scalar(value))
    except ValueError:
        return default


def first_heading(markdown: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", markdown)
    return match.group(1).strip() if match else fallback


def humanize(value: str) -> str:
    return re.sub(r"[-_]+", " ", value).strip().title()


def top_scalar(text: str, key: str, default: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^\s#]+)", text)
    return scalar(match.group(1)) if match else default


def parse_manifest_data(text: str) -> tuple[list[Part], list[DisplayChapter]]:
    """Parse the supported manifest subset without adding a YAML dependency."""
    parts: list[Part] = []
    chapters: list[DisplayChapter] = []
    section = ""
    current_part: Part | None = None
    current_chapter: DisplayChapter | None = None
    list_key: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line:
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if indent == 0:
            match = re.match(r"([a-zA-Z_][\w-]*):", stripped)
            section = match.group(1) if match else ""
            current_part = None
            current_chapter = None
            list_key = None
            continue

        item_id = re.match(r"-\s+id:\s*(.+)$", stripped)
        if indent == 2 and item_id and section == "parts":
            current_part = Part(part_id=scalar(item_id.group(1)))
            parts.append(current_part)
            current_chapter = None
            list_key = None
            continue
        if indent == 2 and item_id and section == "chapters":
            current_chapter = DisplayChapter(
                chapter_id=scalar(item_id.group(1)), path=""
            )
            chapters.append(current_chapter)
            current_part = None
            list_key = None
            continue

        field_match = re.match(r"([a-zA-Z_][\w-]*):\s*(.*)$", stripped)
        if indent == 4 and field_match:
            key, value = field_match.groups()
            list_key = key if not value else None
            if current_part is not None:
                if key == "title":
                    current_part.title = scalar(value)
                elif key == "purpose":
                    current_part.purpose = scalar(value)
                elif key == "order":
                    current_part.order = integer(value)
            elif current_chapter is not None:
                if key == "path":
                    current_chapter.path = scalar(value)
                elif key == "summary":
                    current_chapter.summary = scalar(value)
                elif key == "part":
                    current_chapter.part = scalar(value)
                elif key == "order":
                    current_chapter.order = integer(value)
                elif key == "kind":
                    current_chapter.kind = scalar(value)
                elif key == "status":
                    current_chapter.status = scalar(value)
                elif key == "coverage":
                    current_chapter.coverage = scalar(value)
                elif key == "evidence_status":
                    current_chapter.evidence_status = scalar(value)
            continue

        list_item = re.match(r"-\s+(.+)$", stripped)
        if (
            current_chapter is not None
            and indent >= 6
            and list_item
            and list_key
        ):
            value = scalar(list_item.group(1))
            target = getattr(current_chapter, list_key, None)
            if isinstance(target, list):
                target.append(value)

    return parts, chapters


def load_book(handbook: Path) -> tuple[list[Part], list[DisplayChapter]]:
    manifest_path = handbook / "manifest.yaml"
    index_path = handbook / "index.md"
    if not manifest_path.is_file() or not index_path.is_file():
        raise ValueError("manifest.yaml and index.md are required")

    manifest_text = manifest_path.read_text(encoding="utf-8")
    parts, registered = parse_manifest_data(manifest_text)
    index_markdown = index_path.read_text(encoding="utf-8")
    chapters = [
        DisplayChapter(
            chapter_id="index",
            path="index.md",
            part="",
            order=-1,
            kind="overview",
            status=top_scalar(manifest_text, "handbook_status", "planned"),
            coverage="complete",
            evidence_status="verified",
            title=first_heading(index_markdown, "Codebase Handbook"),
            markdown=index_markdown,
        )
    ]

    seen = {"index"}
    for chapter in registered:
        if not chapter.chapter_id:
            raise ValueError("manifest chapter id cannot be empty")
        if chapter.chapter_id in seen:
            raise ValueError(f"duplicate chapter id: {chapter.chapter_id}")
        seen.add(chapter.chapter_id)
        if not chapter.path:
            raise ValueError(f"chapter {chapter.chapter_id} is missing path")

        chapter_path = handbook / chapter.path
        if chapter_path.is_file():
            chapter.markdown = chapter_path.read_text(encoding="utf-8")
            chapter.title = first_heading(
                chapter.markdown, humanize(chapter.chapter_id)
            )
        elif chapter.status == "planned":
            chapter.title = humanize(chapter.chapter_id)
            chapter.markdown = (
                f"# {chapter.title}\n\n"
                "This chapter is planned and has not been written yet."
            )
        else:
            raise ValueError(
                f"chapter {chapter.chapter_id} path does not exist: {chapter.path}"
            )
        chapters.append(chapter)

    if parts:
        part_order = {part.part_id: part.order for part in parts}
        chapters[1:] = sorted(
            chapters[1:],
            key=lambda item: (
                part_order.get(item.part, 10_000),
                item.order,
                item.title.casefold(),
            ),
        )
    return sorted(parts, key=lambda item: (item.order, item.title.casefold())), chapters


def load_chapters(handbook: Path) -> list[DisplayChapter]:
    """Backward-compatible helper used by validation."""
    return load_book(handbook)[1]


def compute_source_hash(
    handbook: Path, chapters: list[DisplayChapter] | None = None
) -> str:
    chapters = chapters or load_chapters(handbook)
    paths = {handbook / name for name in HASH_INPUTS}
    for chapter in chapters:
        path = handbook / chapter.path
        if path.is_file():
            paths.add(path)
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.as_posix()):
        if not path.is_file():
            raise ValueError(f"missing HTML input: {path.name}")
        relative = path.relative_to(handbook).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def normalize_handbook_target(current_path: str, target: str) -> str:
    decoded = unquote(target.split("#", 1)[0])
    current_parent = PurePosixPath(current_path).parent
    combined = current_parent / decoded
    parts: list[str] = []
    for part in combined.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return PurePosixPath(*parts).as_posix()


def slugify(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^\w\u0080-\uffff]+", "-", value, flags=re.UNICODE)
    return value.strip("-").lower() or "section"


def render_inline(
    raw: str, current_path: str, path_to_id: dict[str, str]
) -> str:
    placeholders: list[str] = []

    def hold(fragment: str) -> str:
        token = f"\x00{len(placeholders)}\x00"
        placeholders.append(fragment)
        return token

    def code_replace(match: re.Match[str]) -> str:
        return hold(f"<code>{html.escape(match.group(1))}</code>")

    def link_replace(match: re.Match[str]) -> str:
        label = html.escape(match.group(1))
        target = match.group(2).strip()
        if target.startswith(("http://", "https://", "mailto:")):
            href = html.escape(target, quote=True)
            return hold(
                f'<a href="{href}" target="_blank" rel="noreferrer">{label}</a>'
            )
        fragment = unquote(target.split("#", 1)[1]) if "#" in target else ""
        if target.startswith("#"):
            href = f"#{quote(path_to_id.get(current_path, 'index'))}/{quote(slugify(fragment))}"
            return hold(f'<a href="{href}">{label}</a>')
        normalized = normalize_handbook_target(current_path, target)
        chapter_id = path_to_id.get(normalized)
        if chapter_id:
            suffix = f"/{quote(slugify(fragment))}" if fragment else ""
            return hold(
                f'<a href="#{quote(chapter_id)}{suffix}">{label}</a>'
            )
        return hold(
            f'<span class="unresolved-link" title="{html.escape(target, quote=True)}">'
            f"{label}</span>"
        )

    protected = re.sub(r"`([^`\n]+)`", code_replace, raw)
    protected = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_replace, protected)
    escaped = html.escape(protected)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", escaped)
    for index, fragment in enumerate(placeholders):
        escaped = escaped.replace(f"\x00{index}\x00", fragment)
    return escaped


def strip_first_h1(markdown: str) -> str:
    return re.sub(r"\A(?:\ufeff)?#\s+.+?\r?\n(?:\r?\n)?", "", markdown, count=1)


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_markdown(
    markdown: str, current_path: str, path_to_id: dict[str, str]
) -> RenderedMarkdown:
    lines = strip_first_h1(markdown).splitlines()
    output: list[str] = []
    headings: list[tuple[int, str, str]] = []
    heading_ids: dict[str, int] = {}
    paragraph: list[str] = []
    list_kind: str | None = None
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(item.strip() for item in paragraph)
            output.append(f"<p>{render_inline(text, current_path, path_to_id)}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_kind
        if list_kind:
            output.append(f"</{list_kind}>")
            list_kind = None

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            close_list()
            language = stripped[3:].strip().lower()
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            code = html.escape("\n".join(code_lines))
            caption = (
                "<figcaption>Diagram source</figcaption>"
                if language == "mermaid"
                else ""
            )
            class_name = (
                f' class="language-{html.escape(language, quote=True)}"'
                if language
                else ""
            )
            output.append(
                f'<figure class="code-block">{caption}<pre><code{class_name}>'
                f"{code}</code></pre></figure>"
            )
            index += 1
            continue
        if not stripped:
            flush_paragraph()
            close_list()
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = max(2, min(len(heading.group(1)), 6))
            plain_title = re.sub(r"[*_`]", "", heading.group(2)).strip()
            base = slugify(plain_title)
            heading_ids[base] = heading_ids.get(base, 0) + 1
            anchor = base if heading_ids[base] == 1 else f"{base}-{heading_ids[base]}"
            headings.append((level, plain_title, anchor))
            output.append(
                f'<h{level} id="{html.escape(anchor, quote=True)}">'
                f"{render_inline(heading.group(2), current_path, path_to_id)}"
                f'<a class="heading-anchor" href="#{quote(path_to_id.get(current_path, "index"))}/{quote(anchor)}" '
                f'aria-label="Link to this section">#</a></h{level}>'
            )
            index += 1
            continue
        if "|" in line and index + 1 < len(lines) and is_table_separator(lines[index + 1]):
            flush_paragraph()
            close_list()
            headers = table_cells(line)
            output.append('<div class="table-wrap"><table><thead><tr>')
            output.extend(
                f"<th>{render_inline(cell, current_path, path_to_id)}</th>"
                for cell in headers
            )
            output.append("</tr></thead><tbody>")
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                output.append("<tr>")
                output.extend(
                    f"<td>{render_inline(cell, current_path, path_to_id)}</td>"
                    for cell in table_cells(lines[index])
                )
                output.append("</tr>")
                index += 1
            output.append("</tbody></table></div>")
            continue
        item = re.match(r"^[-*+]\s+(.+)$", stripped)
        ordered = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if item or ordered:
            flush_paragraph()
            desired = "ul" if item else "ol"
            if list_kind != desired:
                close_list()
                output.append(f"<{desired}>")
                list_kind = desired
            output.append(
                f"<li>{render_inline((item or ordered).group(1), current_path, path_to_id)}</li>"
            )
            index += 1
            continue
        if stripped.startswith(">"):
            flush_paragraph()
            close_list()
            output.append(
                f"<blockquote>{render_inline(stripped[1:].strip(), current_path, path_to_id)}</blockquote>"
            )
            index += 1
            continue
        paragraph.append(line)
        index += 1

    flush_paragraph()
    close_list()
    return RenderedMarkdown("\n".join(output), headings)


def searchable_text(markdown: str) -> str:
    text = re.sub(r"```.*?```", " ", markdown, flags=re.DOTALL)
    text = re.sub(r"[#>*_`\[\]()|:-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def safe_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def render_page(
    root: Path,
    handbook: Path,
    parts: list[Part],
    chapters: list[DisplayChapter],
    source_hash: str,
    title: str,
) -> str:
    path_to_id = {chapter.path: chapter.chapter_id for chapter in chapters}
    chapter_by_id = {chapter.chapter_id: chapter for chapter in chapters}
    part_by_id = {part.part_id: part for part in parts}
    rendered = {
        chapter.chapter_id: render_markdown(
            chapter.markdown, chapter.path, path_to_id
        )
        for chapter in chapters
    }

    nav_groups: list[str] = [
        '<button class="nav-item nav-home" data-target="index"><span>Overview</span></button>'
    ]
    grouped: dict[str, list[DisplayChapter]] = {}
    for chapter in chapters[1:]:
        grouped.setdefault(chapter.part, []).append(chapter)
    ordered_group_ids = [part.part_id for part in parts]
    ordered_group_ids.extend(key for key in grouped if key not in ordered_group_ids)
    for group_id in ordered_group_ids:
        items = grouped.get(group_id, [])
        if not items:
            continue
        part = part_by_id.get(group_id)
        group_title = part.title if part else humanize(group_id or "Chapters")
        nav_groups.append(
            f'<section class="nav-group"><h2>{html.escape(group_title)}</h2>'
            + "".join(
                f'<button class="nav-item" data-target="{html.escape(ch.chapter_id, quote=True)}">'
                f"<span>{html.escape(ch.title)}</span>"
                f'<small class="status status-{html.escape(ch.status, quote=True)}">'
                f"{html.escape(ch.status)}</small></button>"
                for ch in items
            )
            + "</section>"
        )

    book_map = "".join(
        '<section class="book-part">'
        f"<h3>{html.escape(part.title or humanize(part.part_id))}</h3>"
        + (f"<p>{html.escape(part.purpose)}</p>" if part.purpose else "")
        + '<div class="book-part-links">'
        + "".join(
            f'<button class="book-card{" has-summary" if ch.summary else ""}" '
            f'data-target="{html.escape(ch.chapter_id, quote=True)}">'
            '<span class="book-card-heading">'
            f"<strong>{html.escape(ch.title)}</strong><small>{html.escape(ch.kind)}</small></span>"
            + (
                f'<span class="book-card-summary">{html.escape(ch.summary)}</span>'
                if ch.summary
                else ""
            )
            + "</button>"
            for ch in grouped.get(part.part_id, [])
        )
        + "</div></section>"
        for part in parts
        if grouped.get(part.part_id)
    )

    articles: list[str] = []
    for position, chapter in enumerate(chapters):
        result = rendered[chapter.chapter_id]
        part = part_by_id.get(chapter.part)
        breadcrumb = (
            f"<span>{html.escape(part.title)}</span><span>›</span>"
            if part
            else ""
        )
        toc = "".join(
            f'<a class="toc-level-{level}" href="#{quote(chapter.chapter_id)}/{quote(anchor)}">'
            f"{html.escape(heading)}</a>"
            for level, heading, anchor in result.headings
            if level <= 3
        )
        overview_sections: list[str] = []
        if chapter.read_when:
            overview_sections.append(
                '<section><h2>Use this chapter when</h2><ul>'
                + "".join(f"<li>{html.escape(item)}</li>" for item in chapter.read_when)
                + "</ul></section>"
            )
        if chapter.concepts:
            overview_sections.append(
                '<section><h2>Key concepts</h2><div class="concept-list">'
                + "".join(
                    f"<span>{html.escape(item)}</span>" for item in chapter.concepts
                )
                + "</div></section>"
            )
        overview = (
            '<aside class="chapter-overview" aria-label="Chapter guide">'
            + "".join(overview_sections)
            + "</aside>"
            if overview_sections
            else ""
        )
        maintenance_sections: list[str] = []
        direct_evidence = chapter.sources + chapter.source_symbols
        if direct_evidence:
            maintenance_sections.append(
                '<section><h2>Direct source evidence</h2><ul class="path-list">'
                + "".join(
                    f"<li><code>{html.escape(item)}</code></li>"
                    for item in direct_evidence
                )
                + "</ul></section>"
            )
        if chapter.update_triggers:
            maintenance_sections.append(
                '<section><h2>Update triggers</h2><ul class="path-list">'
                + "".join(
                    f"<li><code>{html.escape(item)}</code></li>"
                    for item in chapter.update_triggers
                )
                + "</ul></section>"
            )
        if chapter.chapter_id != "index":
            maintenance_sections.append(
                '<section><h2>Handbook state</h2><dl class="state-grid">'
                f"<div><dt>Status</dt><dd>{html.escape(chapter.status)}</dd></div>"
                f"<div><dt>Coverage</dt><dd>{html.escape(chapter.coverage)}</dd></div>"
                f"<div><dt>Evidence</dt><dd>{html.escape(chapter.evidence_status)}</dd></div>"
                "</dl></section>"
            )
        maintenance_count = len(direct_evidence) + len(chapter.update_triggers)
        maintenance = (
            '<details class="maintenance"><summary><span>Sources and maintenance</span>'
            f"<small>{maintenance_count} indexed paths</small></summary>"
            '<div class="maintenance-grid">'
            + "".join(maintenance_sections)
            + "</div></details>"
            if maintenance_sections
            else ""
        )
        related = [
            chapter_by_id[item]
            for item in chapter.related
            if item in chapter_by_id and item != "index"
        ]
        related_html = (
            '<footer class="related"><h2>Related chapters</h2><div>'
            + "".join(
                f'<button data-target="{html.escape(item.chapter_id, quote=True)}">'
                f"{html.escape(item.title)}</button>"
                for item in related
            )
            + "</div></footer>"
            if related
            else ""
        )
        previous_chapter = chapters[position - 1] if position > 0 else None
        next_chapter = chapters[position + 1] if position + 1 < len(chapters) else None
        pager = '<nav class="pager" aria-label="Chapter navigation">'
        if previous_chapter:
            pager += (
                f'<button data-target="{html.escape(previous_chapter.chapter_id, quote=True)}">'
                f"<small>Previous</small><span>{html.escape(previous_chapter.title)}</span></button>"
            )
        else:
            pager += "<span></span>"
        if next_chapter:
            pager += (
                f'<button class="next" data-target="{html.escape(next_chapter.chapter_id, quote=True)}">'
                f"<small>Next</small><span>{html.escape(next_chapter.title)}</span></button>"
            )
        pager += "</nav>"
        map_panel = (
            '<section class="book-map"><div class="section-heading">'
            "<div><p class=\"kicker\">Book map</p><h2>Explore by part</h2></div>"
            "<p>Use the book to understand the system, or search for a change task.</p>"
            f"</div>{book_map}</section>"
            if chapter.chapter_id == "index" and book_map
            else ""
        )
        articles.append(
            f'<article class="chapter{" active" if position == 0 else ""}" '
            f'data-chapter="{html.escape(chapter.chapter_id, quote=True)}">'
            f'<div class="breadcrumbs"><button data-target="index">Handbook</button><span>›</span>'
            f"{breadcrumb}<strong>{html.escape(chapter.title)}</strong></div>"
            '<header class="chapter-header"><div>'
            f'<span class="eyebrow">{html.escape(chapter.kind)}</span>'
            f"<h1>{html.escape(chapter.title)}</h1>"
            + (
                f'<p class="chapter-summary">{html.escape(chapter.summary)}</p>'
                if chapter.summary
                else ""
            )
            + "</div></header>"
            f"{overview}{map_panel}"
            '<div class="reading-layout">'
            f'<div class="prose">{result.body}</div>'
            + (
                f'<aside class="on-page"><strong>On this page</strong>{toc}</aside>'
                if toc
                else ""
            )
            + f"</div>{maintenance}{related_html}{pager}</article>"
        )

    search_data = [
        {
            "id": chapter.chapter_id,
            "title": chapter.title,
            "part": part_by_id.get(chapter.part).title
            if chapter.part in part_by_id
            else "",
            "text": " ".join(
                item
                for item in [
                    chapter.summary,
                    " ".join(chapter.concepts),
                    " ".join(chapter.read_when),
                    " ".join(chapter.sources),
                    " ".join(chapter.source_symbols),
                    " ".join(chapter.update_triggers),
                    searchable_text(chapter.markdown),
                ]
                if item
            ),
        }
        for chapter in chapters
    ]
    config_text = (handbook / "config.yaml").read_text(encoding="utf-8")
    configured_language = top_scalar(config_text, "language", "auto")
    page_language = configured_language if configured_language != "auto" else "und"

    return f"""<!doctype html>
<html lang="{html.escape(page_language, quote=True)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="codebase-handbook-source-sha256" content="{source_hash}">
<title>{html.escape(title)}</title>
<style>
:root {{ color-scheme: light dark; --bg:#f6f7f9; --panel:#fff; --panel-2:#f0f3f6; --text:#17202a; --muted:#667085; --line:#dfe4ea; --accent:#176b87; --accent-soft:#dff2f5; --code:#edf1f5; --shadow:0 16px 44px rgba(24,39,75,.08); }}
[data-theme="dark"] {{ --bg:#0d1218; --panel:#151c24; --panel-2:#101820; --text:#e8edf2; --muted:#9ba8b5; --line:#293543; --accent:#73d2de; --accent-soft:#17343c; --code:#101820; --shadow:0 16px 44px rgba(0,0,0,.24); }}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:16px/1.72 "IBM Plex Sans",Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
button,input {{ font:inherit; }}
button {{ color:inherit; }}
a {{ color:var(--accent); }}
:focus-visible {{ outline:3px solid var(--accent); outline-offset:3px; }}
.skip-link {{ position:fixed; left:16px; top:-80px; z-index:100; background:var(--accent); color:#fff; padding:10px 14px; border-radius:8px; }}
.skip-link:focus {{ top:16px; }}
.layout {{ min-height:100vh; display:grid; grid-template-columns:330px minmax(0,1fr); }}
.sidebar {{ position:sticky; top:0; height:100vh; padding:22px 18px; border-right:1px solid var(--line); background:color-mix(in srgb,var(--panel) 96%,transparent); overflow:auto; }}
.brand {{ display:flex; justify-content:space-between; gap:12px; margin-bottom:18px; }}
.brand h1 {{ margin:0; font-size:19px; line-height:1.25; }}
.brand p {{ margin:5px 0 0; color:var(--muted); font-size:12px; }}
.theme-toggle {{ border:1px solid var(--line); background:var(--panel); border-radius:9px; padding:7px 10px; cursor:pointer; }}
.search-wrap {{ position:relative; margin-bottom:18px; }}
.search-label {{ display:block; font-size:12px; font-weight:700; margin-bottom:6px; color:var(--muted); }}
.search {{ width:100%; padding:10px 12px; border:1px solid var(--line); border-radius:9px; background:var(--bg); color:var(--text); }}
.search-results {{ display:none; position:absolute; z-index:20; top:72px; left:0; right:0; max-height:55vh; overflow:auto; background:var(--panel); border:1px solid var(--line); border-radius:11px; box-shadow:var(--shadow); padding:6px; }}
.search-results.open {{ display:block; }}
.search-result {{ width:100%; text-align:left; border:0; border-radius:8px; background:transparent; padding:10px; cursor:pointer; }}
.search-result:hover {{ background:var(--accent-soft); }}
.search-result strong,.search-result small {{ display:block; }}
.search-result small {{ color:var(--muted); margin-top:3px; line-height:1.4; }}
mark {{ background:#ffe08a; color:#1d2939; border-radius:2px; }}
.nav-home {{ margin-bottom:10px; }}
.nav-group {{ margin:16px 0; }}
.nav-group h2 {{ margin:0 10px 6px; color:var(--muted); font-size:11px; text-transform:uppercase; letter-spacing:.09em; }}
.nav-item {{ width:100%; min-height:44px; display:flex; justify-content:space-between; gap:8px; align-items:center; text-align:left; border:0; border-radius:8px; padding:8px 10px; background:transparent; cursor:pointer; }}
.nav-item:hover,.nav-item.active {{ background:var(--accent-soft); color:var(--accent); }}
.status {{ border:1px solid var(--line); border-radius:99px; padding:1px 6px; color:var(--muted); font-size:10px; }}
.main {{ min-width:0; padding:34px clamp(22px,5vw,76px) 80px; }}
.chapter {{ display:none; max-width:1180px; margin:0 auto; }}
.chapter.active {{ display:block; }}
.breadcrumbs {{ display:flex; flex-wrap:wrap; gap:7px; align-items:center; color:var(--muted); font-size:13px; margin-bottom:22px; }}
.breadcrumbs button {{ border:0; background:transparent; padding:0; cursor:pointer; color:var(--accent); }}
.chapter-header {{ margin-bottom:24px; }}
.chapter-header h1 {{ max-width:880px; margin:5px 0 10px; font-size:clamp(34px,5vw,58px); line-height:1.08; letter-spacing:-.035em; }}
.chapter-summary {{ max-width:72ch; margin:16px 0 0; color:var(--muted); font-size:clamp(17px,2vw,20px); line-height:1.58; }}
.eyebrow,.kicker {{ color:var(--accent); font-size:12px; font-weight:750; text-transform:uppercase; letter-spacing:.12em; }}
.chapter-overview {{ max-width:1000px; display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px; margin:0 0 24px; }}
.chapter-overview section {{ border:1px solid var(--line); border-radius:12px; background:var(--panel); padding:18px 20px; box-shadow:var(--shadow); }}
.chapter-overview h2 {{ margin:0 0 8px; font-size:14px; }}
.chapter-overview ul {{ margin:0; padding-left:20px; }}
.concept-list {{ display:flex; flex-wrap:wrap; gap:7px; }}
.concept-list span {{ border:1px solid var(--line); border-radius:99px; background:var(--panel-2); padding:4px 9px; font-size:13px; }}
.reading-layout {{ display:grid; grid-template-columns:minmax(0,760px) 220px; gap:28px; align-items:start; }}
.prose,.book-map,.related {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; box-shadow:var(--shadow); padding:clamp(24px,4vw,44px); }}
.prose {{ max-width:76ch; }}
.prose h2,.prose h3,.prose h4 {{ line-height:1.3; scroll-margin-top:24px; }}
.prose h2 {{ margin-top:2.2em; }}
.prose h2:first-child {{ margin-top:0; }}
.heading-anchor {{ opacity:0; margin-left:8px; font-size:.7em; text-decoration:none; }}
.prose h2:hover .heading-anchor,.prose h3:hover .heading-anchor,.heading-anchor:focus {{ opacity:1; }}
.prose code,.maintenance code {{ background:var(--code); border-radius:5px; padding:2px 5px; overflow-wrap:anywhere; }}
.code-block {{ margin:1.5em 0; }}
.code-block figcaption {{ color:var(--muted); font-size:12px; }}
.prose pre {{ overflow:auto; background:var(--code); border:1px solid var(--line); border-radius:10px; padding:16px; }}
.prose pre code {{ padding:0; }}
.prose blockquote {{ margin:1.5em 0; padding:10px 18px; border-left:4px solid var(--accent); background:var(--accent-soft); }}
.table-wrap {{ overflow:auto; }}
table {{ border-collapse:collapse; width:100%; }}
th,td {{ padding:9px 12px; border:1px solid var(--line); text-align:left; }}
.unresolved-link {{ text-decoration:underline dotted; color:var(--muted); }}
.on-page {{ position:sticky; top:24px; display:grid; gap:5px; padding:14px 0 14px 18px; border-left:1px solid var(--line); font-size:13px; }}
.on-page strong {{ margin-bottom:4px; }}
.on-page a {{ text-decoration:none; color:var(--muted); }}
.on-page a:hover {{ color:var(--accent); }}
.toc-level-3 {{ padding-left:12px; }}
.book-map {{ margin-bottom:24px; }}
.section-heading {{ display:flex; justify-content:space-between; gap:24px; align-items:end; margin-bottom:24px; }}
.section-heading h2,.section-heading p {{ margin:0; }}
.section-heading>p {{ max-width:420px; color:var(--muted); }}
.book-part {{ padding:20px 0; border-top:1px solid var(--line); }}
.book-part h3,.book-part p {{ margin:0 0 7px; }}
.book-part p {{ color:var(--muted); }}
.book-part-links {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:10px; }}
.book-card {{ min-height:52px; display:grid; align-content:start; text-align:left; gap:7px; border:1px solid var(--line); border-radius:10px; background:var(--panel-2); padding:13px 14px; cursor:pointer; }}
.book-card.has-summary {{ min-height:88px; }}
.book-card:hover {{ border-color:var(--accent); background:var(--accent-soft); }}
.book-card-heading {{ display:flex; justify-content:space-between; gap:10px; align-items:start; }}
.book-card-heading small,.book-card-summary {{ color:var(--muted); }}
.book-card-heading small {{ flex:none; }}
.book-card-summary {{ line-height:1.45; font-size:13px; }}
.maintenance {{ margin-top:24px; border:1px solid var(--line); border-radius:14px; background:var(--panel); box-shadow:var(--shadow); }}
.maintenance>summary {{ min-height:52px; display:flex; justify-content:space-between; gap:16px; align-items:center; padding:13px 18px; cursor:pointer; font-weight:700; }}
.maintenance>summary small {{ color:var(--muted); font-weight:500; }}
.maintenance[open]>summary {{ border-bottom:1px solid var(--line); }}
.maintenance-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:24px; padding:20px; }}
.maintenance-grid h2 {{ margin:0 0 10px; font-size:15px; }}
.path-list {{ margin:0; padding-left:20px; }}
.path-list li+li {{ margin-top:6px; }}
.state-grid {{ display:grid; gap:8px; margin:0; }}
.state-grid div {{ display:flex; justify-content:space-between; gap:16px; border-bottom:1px solid var(--line); padding-bottom:7px; }}
.state-grid dt {{ color:var(--muted); }}
.state-grid dd {{ margin:0; font-weight:700; }}
.related {{ margin-top:24px; }}
.related h2 {{ margin-top:0; font-size:18px; }}
.related button,.pager button {{ min-height:44px; border:1px solid var(--line); border-radius:9px; background:var(--panel-2); padding:8px 11px; cursor:pointer; }}
.pager {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:24px; }}
.pager button {{ display:grid; text-align:left; }}
.pager button.next {{ text-align:right; }}
.pager small {{ color:var(--muted); }}
.build-meta {{ margin:18px 8px; color:var(--muted); font-size:10px; overflow-wrap:anywhere; }}
@media (max-width:950px) {{ .reading-layout {{ grid-template-columns:1fr; }} .on-page {{ position:relative; top:auto; grid-column:1; grid-row:1; border-left:0; border-bottom:1px solid var(--line); padding:10px 0 16px; }} }}
@media (max-width:760px) {{ .layout {{ grid-template-columns:1fr; }} .sidebar {{ position:relative; height:auto; border-right:0; border-bottom:1px solid var(--line); }} .nav-groups {{ max-height:330px; overflow:auto; }} .main {{ padding:26px 15px 60px; }} .section-heading {{ display:block; }} .chapter-overview,.maintenance-grid {{ grid-template-columns:1fr; }} .maintenance>summary {{ align-items:flex-start; flex-direction:column; gap:2px; }} }}
@media (prefers-reduced-motion:reduce) {{ html {{ scroll-behavior:auto; }} }}
</style>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
<div class="layout">
  <aside class="sidebar">
    <div class="brand"><div><h1>{html.escape(title)}</h1><p>{html.escape(root.name)}</p></div><button class="theme-toggle" id="theme-toggle" aria-label="Toggle color theme">◐</button></div>
    <div class="search-wrap">
      <label class="search-label" for="search">Search the handbook <span aria-hidden="true">⌘K</span></label>
      <input class="search" id="search" type="search" placeholder="Concept, flow, module, change task…" autocomplete="off" aria-controls="search-results" aria-expanded="false">
      <div class="search-results" id="search-results" role="listbox"></div>
    </div>
    <nav class="nav-groups" aria-label="Book contents">{"".join(nav_groups)}</nav>
    <p class="build-meta">Source hash: {source_hash}</p>
  </aside>
  <main class="main" id="main-content" tabindex="-1">{"".join(articles)}</main>
</div>
<script>
const searchData={safe_json(search_data)};
const chapters=[...document.querySelectorAll('.chapter')];
const navItems=[...document.querySelectorAll('.nav-item')];
const search=document.getElementById('search');
const results=document.getElementById('search-results');
function routeParts() {{
  const raw=decodeURIComponent(location.hash.slice(1));
  const [chapter,...section]=raw.split('/');
  return [chapter||'index',section.join('/')];
}}
function showChapter(id,section='',push=false) {{
  const target=document.querySelector(`[data-chapter="${{CSS.escape(id)}}"]`)||document.querySelector('[data-chapter="index"]');
  id=target.dataset.chapter;
  chapters.forEach(item=>item.classList.toggle('active',item===target));
  navItems.forEach(item=>{{const active=item.dataset.target===id; item.classList.toggle('active',active); if(active)item.setAttribute('aria-current','page');else item.removeAttribute('aria-current');}});
  const nextHash=`#${{encodeURIComponent(id)}}${{section?'/'+encodeURIComponent(section):''}}`;
  if(push&&location.hash!==nextHash) history.pushState(null,'',nextHash);
  requestAnimationFrame(()=>{{
    const heading=section?target.querySelector(`#${{CSS.escape(section)}}`):null;
    if(heading) heading.scrollIntoView({{block:'start'}});
    else window.scrollTo({{top:0,behavior:'smooth'}});
  }});
}}
document.addEventListener('click',event=>{{
  const trigger=event.target.closest('[data-target]');
  if(trigger){{event.preventDefault(); showChapter(trigger.dataset.target,'',true);}}
  if(!event.target.closest('.search-wrap')) closeResults();
}});
window.addEventListener('popstate',()=>{{const [c,s]=routeParts();showChapter(c,s,false);}});
window.addEventListener('hashchange',()=>{{const [c,s]=routeParts();showChapter(c,s,false);}});
function escapeHtml(value) {{const node=document.createElement('span');node.textContent=value;return node.innerHTML;}}
function escapeAttr(value) {{return escapeHtml(value).replaceAll('"','&quot;').replaceAll("'","&#39;");}}
function marked(value,query) {{
  const safe=escapeHtml(value),at=value.toLocaleLowerCase().indexOf(query);
  if(at<0)return safe;
  return escapeHtml(value.slice(0,at))+'<mark>'+escapeHtml(value.slice(at,at+query.length))+'</mark>'+escapeHtml(value.slice(at+query.length));
}}
function snippet(text,query) {{
  const at=text.toLocaleLowerCase().indexOf(query),start=Math.max(0,at-70),end=Math.min(text.length,at+query.length+110);
  return (start?'…':'')+marked(text.slice(start,end),query)+(end<text.length?'…':'');
}}
function closeResults() {{results.classList.remove('open');search.setAttribute('aria-expanded','false');}}
search.addEventListener('input',()=>{{
  const query=search.value.trim().toLocaleLowerCase();
  if(!query){{closeResults();results.innerHTML='';return;}}
  const matches=searchData.filter(item=>(item.title+' '+item.part+' '+item.text).toLocaleLowerCase().includes(query)).slice(0,20);
  results.innerHTML=matches.length?matches.map(item=>`<button class="search-result" role="option" data-target="${{escapeAttr(item.id)}}"><strong>${{marked(item.title,query)}}</strong><small>${{escapeHtml(item.part)}}${{item.part?' · ':''}}${{snippet(item.text,query)}}</small></button>`).join(''):'<p class="search-result"><strong>No results</strong><small>Try a module name, runtime concept, state, or change task.</small></p>';
  results.classList.add('open');search.setAttribute('aria-expanded','true');
}});
document.addEventListener('keydown',event=>{{
  if((event.metaKey||event.ctrlKey)&&event.key.toLocaleLowerCase()==='k'){{event.preventDefault();search.focus();}}
  if(event.key==='Escape'){{closeResults();search.blur();}}
}});
const themeKey='codebase-handbook-theme';let stored=null;
try{{stored=localStorage.getItem(themeKey);}}catch(_){{}}
if(stored)document.documentElement.dataset.theme=stored;
document.getElementById('theme-toggle').addEventListener('click',()=>{{const next=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=next;try{{localStorage.setItem(themeKey,next);}}catch(_){{}}}});
const [initialChapter,initialSection]=routeParts();showChapter(initialChapter,initialSection,false);
</script>
</body>
</html>
"""


def build_handbook(root: Path, title: str | None = None) -> Path:
    root = root.expanduser().resolve()
    handbook = root / HANDBOOK_DIR
    if not handbook.is_dir():
        raise ValueError(f"handbook does not exist: {handbook}")
    parts, chapters = load_book(handbook)
    source_hash = compute_source_hash(handbook, chapters)
    display_title = title or f"{root.name} Codebase Handbook"
    page = render_page(root, handbook, parts, chapters, source_hash, display_title)
    output = handbook / OUTPUT_NAME
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".handbook.", suffix=".html", dir=handbook
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(page)
        os.replace(temporary_name, output)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a self-contained .codebase-handbook/handbook.html."
    )
    parser.add_argument("--project-root", help="Project root. Defaults to cwd.")
    parser.add_argument("--title", help="Optional display title.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = (
        Path(args.project_root).expanduser().resolve()
        if args.project_root
        else Path.cwd().resolve()
    )
    try:
        output = build_handbook(root, args.title)
    except ValueError as error:
        print(f"error: {error}")
        return 2
    print(f"built {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
