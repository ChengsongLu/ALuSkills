#!/usr/bin/env python3
"""Create a non-destructive .codebase-handbook skeleton."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from build_handbook import build_handbook


HANDBOOK_DIR = ".codebase-handbook"


def resolve_project_root(value: str | None) -> Path:
    candidate = Path(value).expanduser().resolve() if value else Path.cwd().resolve()
    if not candidate.is_dir():
        raise ValueError(f"Project root is not a directory: {candidate}")
    return candidate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an empty .codebase-handbook without overwriting files."
    )
    parser.add_argument(
        "--project-root",
        help="Project root. Defaults to the current directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = resolve_project_root(args.project_root)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    target = root / HANDBOOK_DIR
    if target.exists():
        print(f"error: refusing to overwrite existing {target}", file=sys.stderr)
        return 2

    template = Path(__file__).resolve().parent.parent / "assets" / "handbook-template"
    if not template.is_dir():
        print(f"error: handbook template is missing: {template}", file=sys.stderr)
        return 2

    shutil.copytree(template, target)
    build_handbook(root)
    print(f"created {target}")
    print("next: read preferences.md, inventory the project, and populate manifest.yaml")
    print("next: integrate concise maintenance guidance into applicable Agent rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
