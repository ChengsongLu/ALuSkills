#!/usr/bin/env python3
"""Validate the repository's Agent Skill structure without external dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELD_PATTERN = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:[ \t]+(.*))?$")
ALLOWED_FIELDS = {"name", "description"}


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return {}, [f"{path}: cannot read UTF-8 text: {exc}"]

    if not lines or lines[0] != "---":
        return {}, [f"{path}: missing opening YAML frontmatter delimiter"]

    try:
        closing_index = lines.index("---", 1)
    except ValueError:
        return {}, [f"{path}: missing closing YAML frontmatter delimiter"]

    if closing_index == 1:
        errors.append(f"{path}: frontmatter is empty")

    fields: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:closing_index], start=2):
        match = FIELD_PATTERN.fullmatch(line)
        if not match:
            errors.append(
                f"{path}:{line_number}: unsupported or malformed frontmatter line"
            )
            continue

        key, raw_value = match.groups()
        value = (raw_value or "").strip()
        if key in fields:
            errors.append(f"{path}:{line_number}: duplicate frontmatter field {key!r}")
        fields[key] = value

    if not any(line.strip() for line in lines[closing_index + 1 :]):
        errors.append(f"{path}: skill body is empty")

    return fields, errors


def validate_skill(skill_dir: Path) -> list[str]:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_dir}: missing SKILL.md"]

    fields, errors = parse_frontmatter(skill_file)
    unknown_fields = sorted(set(fields) - ALLOWED_FIELDS)
    if unknown_fields:
        errors.append(
            f"{skill_file}: unsupported frontmatter fields: "
            + ", ".join(unknown_fields)
        )

    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        errors.append(f"{skill_file}: missing non-empty name")
    elif len(name) > 64:
        errors.append(f"{skill_file}: name exceeds 64 characters")
    elif not NAME_PATTERN.fullmatch(name):
        errors.append(f"{skill_file}: name must use lowercase kebab-case")
    elif name != skill_dir.name:
        errors.append(
            f"{skill_file}: name {name!r} does not match directory {skill_dir.name!r}"
        )

    if not description:
        errors.append(f"{skill_file}: missing non-empty description")
    elif len(description) > 1024:
        errors.append(f"{skill_file}: description exceeds 1024 characters")

    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"error: missing skills directory: {SKILLS_DIR}", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        print("error: no skill directories found", file=sys.stderr)
        return 1

    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
