"""Tests for canvas_core.traps.cv_file_props_01 (Halftone HV O1)."""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_file_props_01 import check


def _file_node(id: str, rel: str, w: float = 400, h: float = 300) -> dict:
    return {"id": id, "type": "file", "file": rel,
            "x": 0, "y": 0, "width": w, "height": h}


def _canvas(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "edges": []}


def _vault(tmp_path, props_hidden: bool | None = None):
    (tmp_path / ".obsidian").mkdir()
    if props_hidden is not None:
        (tmp_path / ".obsidian" / "app.json").write_text(
            json.dumps({"propertiesInDocument": "hidden" if props_hidden else "visible"})
        )
    return tmp_path


class TestVaultRootRequired:
    def test_skips_without_vault_root(self):
        canvas = _canvas([_file_node("f1", "missing.md")])
        assert check(canvas) == []


class TestFileResolution:
    def test_missing_target_fires_high(self, tmp_path):
        root = _vault(tmp_path)
        canvas = _canvas([_file_node("f1", "nope/missing.md")])
        findings = check(canvas, vault_root=root)
        missing = [f for f in findings if f.condition == "file_missing"]
        assert len(missing) == 1
        assert missing[0].severity == "high"

    def test_resolving_target_clean(self, tmp_path):
        root = _vault(tmp_path, props_hidden=True)
        (root / "note.md").write_text("# Hi\n\nBody.\n")
        canvas = _canvas([_file_node("f1", "note.md")])
        conditions = {f.condition for f in check(canvas, vault_root=root)}
        assert "file_missing" not in conditions


class TestPropertiesExposed:
    def test_frontmatter_without_hidden_fires(self, tmp_path):
        root = _vault(tmp_path)  # no app.json setting
        (root / "note.md").write_text("---\ntype: note\n---\n\n# Hi\n\nBody.\n")
        canvas = _canvas([_file_node("f1", "note.md")])
        findings = [f for f in check(canvas, vault_root=root)
                    if f.condition == "properties_exposed"]
        assert len(findings) == 1
        assert findings[0].severity == "high"
        assert "f1" in findings[0].node_ids

    def test_frontmatter_with_hidden_clean(self, tmp_path):
        root = _vault(tmp_path, props_hidden=True)
        (root / "note.md").write_text("---\ntype: note\n---\n\n# Hi\n\nBody.\n")
        canvas = _canvas([_file_node("f1", "note.md")])
        findings = [f for f in check(canvas, vault_root=root)
                    if f.condition == "properties_exposed"]
        assert findings == []


class TestTitleClips:
    def test_long_h1_in_short_card_fires(self, tmp_path):
        root = _vault(tmp_path, props_hidden=True)
        (root / "long.md").write_text(
            "# A Very Long Title That Wraps Multiple Times In A Narrow Card "
            "And Then Some More Words\n\nBody.\n"
        )
        canvas = _canvas([_file_node("f1", "long.md", w=260, h=60)])
        findings = [f for f in check(canvas, vault_root=root)
                    if f.condition == "title_clips"]
        assert len(findings) == 1
        assert findings[0].severity == "high"
        assert "Set height >=" in findings[0].message

    def test_generous_card_clean(self, tmp_path):
        root = _vault(tmp_path, props_hidden=True)
        (root / "note.md").write_text("# Short\n\nBody.\n")
        canvas = _canvas([_file_node("f1", "note.md", w=400, h=400)])
        clips = [f for f in check(canvas, vault_root=root)
                 if f.condition in ("title_clips", "content_hidden")]
        assert clips == []


class TestBinaryTargets:
    """Halftone H2 regression: image file nodes (the render bridge's write-back output) must get
    the existence check ONLY — embed/Properties semantics are markdown-target behavior, and the
    utf-8 read crashed on the PNG signature before this guard."""

    _PNG = (b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)  # signature + junk — enough to poison utf-8

    def test_png_target_no_crash_no_embed_findings(self, tmp_path):
        root = _vault(tmp_path)  # properties NOT hidden — must still not fire for a PNG
        (root / "panel.png").write_bytes(self._PNG)
        canvas = _canvas([_file_node("p1", "panel.png", w=260, h=60)])
        findings = check(canvas, vault_root=root)
        assert findings == []  # exists + binary → clean

    def test_png_target_missing_still_fires(self, tmp_path):
        root = _vault(tmp_path)
        canvas = _canvas([_file_node("p1", "runs/panel.png")])
        conditions = {f.condition for f in check(canvas, vault_root=root)}
        assert conditions == {"file_missing"}

    def test_mixed_targets_markdown_still_checked(self, tmp_path):
        root = _vault(tmp_path)  # properties visible
        (root / "panel.png").write_bytes(self._PNG)
        (root / "note.md").write_text("---\ntype: note\n---\n\n# Hi\n\nBody.\n")
        canvas = _canvas([_file_node("p1", "panel.png"), _file_node("f1", "note.md")])
        exposed = [f for f in check(canvas, vault_root=root)
                   if f.condition == "properties_exposed"]
        assert len(exposed) == 1
        assert exposed[0].node_ids == ["f1"]  # the PNG node is not implicated
