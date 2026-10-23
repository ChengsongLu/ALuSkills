#!/usr/bin/env python3
"""Validate deterministic integrity and book-model structure."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

from build_handbook import (
    compute_source_hash,
    load_chapters,
    parse_manifest_data,
    scalar,
    top_scalar,
    render_markdown,
    slugify,
)


from handbook_data import load_yaml, records, typed_fields, confined_path, handbook_directory


REQUIRED_FILES = ("config.yaml", "preferences.md", "manifest.yaml", "index.md")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SUPPORTED_SCHEMAS = {"1", "2"}
STATUSES = {"planned", "draft", "verified", "needs-review"}
COVERAGE_LEVELS = {"outline", "substantial", "complete"}
EVIDENCE_STATUSES = {"partial", "verified", "stale", "conflicted"}


@dataclass
class CoverageEntry:
    area: str
    kind: str = ""
    disposition: str = ""
    chapters: list[str] = field(default_factory=list)
    reason: str = ""


def parse_coverage_inventory(text: str) -> list[CoverageEntry]:
    return [CoverageEntry(**typed_fields(item, CoverageEntry))
            for item in records(load_yaml(text), "coverage_inventory")]


def resolve_project_root(value: str | None) -> Path:
    candidate = Path(value).expanduser().resolve() if value else Path.cwd().resolve()
    if not candidate.is_dir():
        raise ValueError(f"Project root is not a directory: {candidate}")
    return candidate


def is_external_link(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "data:"))


def check_markdown_links(handbook: Path, errors: list[str]) -> None:
    # Only authored handbook files; ignore code examples when finding links.
    chapters = load_chapters(handbook)
    targets = {chapter.path: chapter.chapter_id for chapter in chapters}
    anchors = {
        confined_path(handbook, chapter.path): {
            heading[2] for heading in render_markdown(
                chapter.markdown, chapter.path, targets).headings
        } for chapter in chapters
    }
    for chapter in chapters:
        markdown = confined_path(handbook, chapter.path)
        text = re.sub(r"(?ms)^```[^\n]*\n.*?^```[^\n]*$", "", chapter.markdown)
        text = re.sub(r"`[^`\n]*`", "", text)
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().strip("<>")
            if not target or is_external_link(target):
                continue
            path_part, _, fragment = target.partition("#")
            resolved = ((markdown.parent / unquote(path_part)).resolve()
                        if path_part else markdown)
            if not resolved.exists():
                errors.append(f"broken Markdown link in {chapter.path}: {raw_target}")
            elif fragment and resolved in anchors and slugify(unquote(fragment)) not in anchors[resolved]:
                errors.append(f"broken chapter anchor in {chapter.path}: {raw_target}")


def schema_version(path: Path, errors: list[str]) -> str:
    text = path.read_text(encoding="utf-8")
    version = top_scalar(text, "schema_version", "")
    if version not in SUPPORTED_SCHEMAS:
        errors.append(f"{path.name} uses unsupported schema_version {version}")
    return version


def source_matches(root: Path, source: str) -> bool:
    if "::" in source:
        source = source.split("::", 1)[0]
    if any(character in source for character in "*?["):
        return any(root.glob(source))
    return (root / source).exists()


def check_manifest(
    root: Path,
    handbook: Path,
    version: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    manifest_path = handbook / "manifest.yaml"
    text = manifest_path.read_text(encoding="utf-8")
    parts, chapters = parse_manifest_data(text)
    inventory = parse_coverage_inventory(text)
    part_ids: set[str] = set()
    chapter_ids: set[str] = set()

    for part in parts:
        if not part.part_id:
            errors.append("manifest contains a part without an id")
        elif part.part_id in part_ids:
            errors.append(f"duplicate part id: {part.part_id}")
        part_ids.add(part.part_id)
        if version == "2" and not part.title:
            errors.append(f"part {part.part_id} is missing title")

    for chapter in chapters:
        if not chapter.chapter_id:
            errors.append("manifest contains a chapter without an id")
            continue
        if chapter.chapter_id in chapter_ids:
            errors.append(f"duplicate chapter id: {chapter.chapter_id}")
        chapter_ids.add(chapter.chapter_id)
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", chapter.chapter_id):
            errors.append(
                f"chapter id must use lowercase letters, digits, and hyphens: "
                f"{chapter.chapter_id}"
            )
        if chapter.status not in STATUSES:
            errors.append(
                f"chapter {chapter.chapter_id} has invalid status: {chapter.status}"
            )
        if version == "2":
            if chapter.coverage and chapter.coverage not in COVERAGE_LEVELS:
                errors.append(
                    f"chapter {chapter.chapter_id} has invalid coverage: "
                    f"{chapter.coverage}"
                )
            if chapter.evidence_status and chapter.evidence_status not in EVIDENCE_STATUSES:
                errors.append(
                    f"chapter {chapter.chapter_id} has invalid evidence_status: "
                    f"{chapter.evidence_status}"
                )
            if chapter.part and chapter.part not in part_ids:
                errors.append(
                    f"chapter {chapter.chapter_id} references unknown part: "
                    f"{chapter.part or '(empty)'}"
                )
            if chapter.status != "planned" and not chapter.sources:
                warnings.append(
                    f"chapter {chapter.chapter_id} has no direct source evidence"
                )
            if chapter.status == "verified" and chapter.evidence_status not in {"", "verified"}:
                errors.append(
                    f"verified chapter {chapter.chapter_id} must have "
                    "evidence_status: verified"
                )
        if not chapter.path:
            errors.append(f"chapter {chapter.chapter_id} is missing path")
        else:
            chapter_path = confined_path(handbook, chapter.path)
            if not chapter_path.exists():
                message = (
                    f"chapter {chapter.chapter_id} path does not exist: {chapter.path}"
                )
                if chapter.status == "planned":
                    warnings.append(message)
                else:
                    errors.append(message)
        for source in chapter.sources:
            if not source_matches(root, source):
                message = (
                    f"chapter {chapter.chapter_id} source does not exist: {source}"
                )
                if chapter.status in {"planned", "draft"}:
                    warnings.append(message)
                else:
                    errors.append(message)

    for chapter in chapters:
        for related in chapter.related:
            if related not in chapter_ids:
                errors.append(
                    f"chapter {chapter.chapter_id} relates to unknown chapter: {related}"
                )

    seen_areas: set[str] = set()
    for entry in inventory:
        if not entry.area:
            errors.append("coverage inventory contains an empty area")
            continue
        if entry.area in seen_areas:
            errors.append(f"duplicate coverage area: {entry.area}")
        seen_areas.add(entry.area)
        if entry.disposition not in {"covered", "excluded"}:
            errors.append(
                f"coverage area {entry.area} has invalid disposition: "
                f"{entry.disposition or '(empty)'}"
            )
        if entry.disposition == "covered":
            if not entry.chapters:
                errors.append(
                    f"covered area {entry.area} does not map to any chapter"
                )
            for chapter_id in entry.chapters:
                if chapter_id not in chapter_ids:
                    errors.append(
                        f"coverage area {entry.area} references unknown chapter: "
                        f"{chapter_id}"
                    )
        if entry.disposition == "excluded" and not entry.reason:
            errors.append(f"excluded area {entry.area} is missing a reason")

    handbook_status = top_scalar(text, "handbook_status", "planned")
    if handbook_status not in STATUSES:
        errors.append(f"invalid handbook_status: {handbook_status}")
    if version == "2" and handbook_status == "verified":
        for chapter in chapters:
            if chapter.status != "verified":
                errors.append(
                    f"verified handbook contains non-verified chapter: "
                    f"{chapter.chapter_id}"
                )
            if chapter.coverage == "outline":
                errors.append(
                    f"verified handbook contains outline-only chapter: "
                    f"{chapter.chapter_id}"
                )


def check_index_consistency(
    handbook: Path, manifest_text: str, errors: list[str], warnings: list[str]
) -> None:
    index_text = (handbook / "index.md").read_text(encoding="utf-8")
    match = re.search(
        r"(?mi)^(?:status|状态)\s*[:：]\s*([^\s#]+)", index_text
    )
    if not match:
        warnings.append("index.md does not expose the handbook status")
        return
    index_status = scalar(match.group(1))
    manifest_status = top_scalar(manifest_text, "handbook_status", "planned")
    if index_status != manifest_status:
        errors.append(
            f"index.md status ({index_status}) does not match "
            f"manifest handbook_status ({manifest_status})"
        )


def check_html(handbook: Path, errors: list[str]) -> None:
    html_path = confined_path(handbook, "handbook.html")
    if not html_path.is_file():
        errors.append("missing generated HTML reading view: handbook.html")
        return
    html_text = html_path.read_text(encoding="utf-8")
    match = re.search(
        r'<meta name="codebase-handbook-source-sha256" content="([0-9a-f]{64})">',
        html_text,
    )
    if not match:
        errors.append("handbook.html is missing its source hash")
        return
    try:
        chapters = load_chapters(handbook)
        expected = compute_source_hash(handbook, chapters)
    except ValueError as error:
        errors.append(f"cannot calculate handbook.html source hash: {error}")
        return
    if match.group(1) != expected:
        errors.append("handbook.html is stale; regenerate it with build_handbook.py")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate handbook structure, book model, and references. "
            "This does not validate semantic accuracy."
        )
    )
    parser.add_argument("--project-root", help="Project root. Defaults to cwd.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = resolve_project_root(args.project_root)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    handbook = handbook_directory(root)
    if not handbook.is_dir():
        print(f"error: handbook does not exist: {handbook}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    for required in REQUIRED_FILES:
        if not confined_path(handbook, required).is_file():
            errors.append(f"missing required file: {required}")

    if not errors:
        config_version = schema_version(handbook / "config.yaml", errors)
        manifest_version = schema_version(handbook / "manifest.yaml", errors)
        if config_version and manifest_version and config_version != manifest_version:
            warnings.append(
                "config.yaml and manifest.yaml use different schema versions"
            )
        check_markdown_links(handbook, errors)
        check_manifest(
            root, handbook, manifest_version, errors, warnings
        )
        manifest_text = (handbook / "manifest.yaml").read_text(encoding="utf-8")
        check_index_consistency(handbook, manifest_text, errors, warnings)
        check_html(handbook, errors)

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        print(
            f"validation failed: {len(errors)} error(s), {len(warnings)} warning(s)",
            file=sys.stderr,
        )
        return 1
    print(f"validation passed with {len(warnings)} warning(s)")
    print("source symbols, external-file anchors, semantic accuracy, and coverage require manual review")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
