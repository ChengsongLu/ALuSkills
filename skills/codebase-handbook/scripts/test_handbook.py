"""Regression checks for handbook parsing, boundaries, and generated output."""
from pathlib import Path
from html.parser import HTMLParser
import subprocess
import sys
import tempfile
import unittest

from build_handbook import build_handbook, parse_manifest_data
from handbook_data import load_yaml

SCRIPTS = Path(__file__).resolve().parent


class BookCards(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "button" and "book-card" in attrs.get("class", "").split():
            self.targets.append(attrs["data-target"])


class HandbookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        self.run_helper("initialize_handbook.py")
        self.book = self.root / ".codebase-handbook"
        (self.root / "source.py").write_text("def sample(): pass\n")
        (self.book / "chapter.md").write_text("# Sample\n\n## Details\n\nContent.\n")
        self.manifest = """schema_version: 2
handbook_status: verified
chapters:
  - id: sample
    path: chapter.md
    summary: "C# behavior"
    status: verified
    sources: [source.py]
    source_symbols: ["source.py::sample"]
unresolved: []
"""
        (self.book / "manifest.yaml").write_text(self.manifest)
        (self.book / "index.md").write_text("# Index\n\nStatus: verified\n\n[Details](chapter.md#details)\n")

    def run_helper(self, script, expected=0):
        result = subprocess.run([sys.executable, str(SCRIPTS / script),
                                 "--project-root", str(self.root)],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_empty_shell(self):
        (self.book / "manifest.yaml").write_text("schema_version: 2\nhandbook_status: planned\nchapters: []\n")
        (self.book / "index.md").write_text("# Index\n\nStatus: planned\n")
        self.run_helper("build_handbook.py")
        self.run_helper("validate_handbook.py")

    def test_roundtrip_compact_and_legacy(self):
        self.run_helper("build_handbook.py")
        self.run_helper("validate_handbook.py")
        for version in (1, 2):
            text = self.manifest.replace("schema_version: 2", f"schema_version: {version}")
            text = text.replace("    status: verified", "    status: verified\n    coverage: complete\n    evidence_status: verified")
            (self.book / "manifest.yaml").write_text(text)
            self.run_helper("build_handbook.py")
            self.run_helper("validate_handbook.py")
        self.run_helper("initialize_handbook.py", expected=2)

    def test_optional_parts_preserve_book_map_and_order(self):
        (self.book / "second.md").write_text("# Second\n")
        text = self.manifest.replace("    status: verified", "    status: verified\n    order: 20")
        text = text.replace("unresolved: []", """  - id: second
    path: second.md
    status: verified
    order: 10
    sources: [source.py]
unresolved: []""")
        for parts in ("", "parts:\n  - id: core\n    title: Core\n"):
            with self.subTest(parts=bool(parts)):
                manifest = parts + text
                if parts:
                    manifest = manifest.replace("    path: second.md", "    path: second.md\n    part: core")
                (self.book / "manifest.yaml").write_text(manifest)
                self.run_helper("build_handbook.py")
                self.run_helper("validate_handbook.py")
                cards = BookCards()
                cards.feed((self.book / "handbook.html").read_text())
                self.assertEqual(cards.targets, ["second", "sample"])

    def test_yaml_supported_forms_and_rejections(self):
        chapter = parse_manifest_data(self.manifest)[1][0]
        self.assertEqual(chapter.summary, "C# behavior")
        self.assertEqual(chapter.sources, ["source.py"])
        folded = self.manifest.replace('"C# behavior"', ">-\n      First line\n      second line")
        self.assertEqual(parse_manifest_data(folded)[1][0].summary, "First line second line")
        for text in ("chapters: []\nchapters: []", "[1, 2]", "x: !!python/object:foo {}"):
            with self.assertRaises(ValueError):
                load_yaml(text)
        for text in ("chapters: wrong", "chapters: [{}]",
                     self.manifest.replace("sources: [source.py]", "sources: source.py")):
            with self.assertRaises(ValueError):
                parse_manifest_data(text)

    def test_extension_metadata_cannot_override_internal_fields(self):
        text = self.manifest.replace("    path: chapter.md", """    path: chapter.md
    chapter_id: extension-value
    title: [custom, metadata]
    markdown: {custom: metadata}""")
        (self.book / "manifest.yaml").write_text(text)
        self.run_helper("build_handbook.py")
        self.run_helper("validate_handbook.py")
        chapter = parse_manifest_data(text)[1][0]
        self.assertEqual(chapter.chapter_id, "sample")
        self.assertEqual((self.book / "manifest.yaml").read_text(), text)

    def test_config_and_html_escaping(self):
        config = (self.book / "config.yaml").read_text().replace("title: auto", 'title: "Custom # title"').replace("show_source_evidence: true", "show_source_evidence: false")
        (self.book / "config.yaml").write_text(config)
        (self.book / "chapter.md").write_text('# Sample\n\n<script>alert("x")</script>\n')
        html = build_handbook(self.root).read_text()
        self.assertIn("<title>Custom # title</title>", html)
        self.assertNotIn("source.py::sample", html)
        self.assertNotIn('<script>alert("x")</script>', html)
        self.assertIn("<title>Override</title>", build_handbook(self.root, "Override").read_text())

    def test_paths_cannot_embed_external_files(self):
        outside = self.root.parent / "outside.md"
        outside.write_text("# Private\n\nSENTINEL\n")
        (self.book / "escape.md").symlink_to(outside)
        original_output = (self.book / "handbook.html").read_bytes()
        for target in ("../../outside.md", str(outside), "escape.md"):
            (self.book / "manifest.yaml").write_text(self.manifest.replace("path: chapter.md", f"path: {target}"))
            with self.assertRaises(ValueError):
                build_handbook(self.root)
            self.run_helper("validate_handbook.py", expected=2)
            self.assertEqual((self.book / "handbook.html").read_bytes(), original_output)
        (self.book / "manifest.yaml").write_text(self.manifest)
        (self.book / "config.yaml").unlink()
        (self.book / "config.yaml").symlink_to(outside)
        with self.assertRaises(ValueError):
            build_handbook(self.root)

    def test_handbook_directory_symlink_rejected(self):
        actual = self.root.parent / "actual-book"
        self.book.rename(actual)
        self.book.symlink_to(actual, target_is_directory=True)
        with self.assertRaises(ValueError):
            build_handbook(self.root)
        self.run_helper("initialize_handbook.py", expected=2)
        self.run_helper("validate_handbook.py", expected=2)

    def test_anchor_and_freshness_checks(self):
        self.run_helper("build_handbook.py")
        (self.book / "chapter.md").write_text("# Sample\n\n## Details\n\n[bad](#missing)\n")
        result = self.run_helper("validate_handbook.py", expected=1)
        self.assertIn("stale", result.stderr)
        self.assertIn("broken chapter anchor", result.stderr)
        (self.book / "chapter.md").write_text("# Sample\n\n## Details\n\n```md\n[example](missing.md)\n```\n")
        self.run_helper("build_handbook.py")
        self.run_helper("validate_handbook.py")


if __name__ == "__main__":
    unittest.main()
