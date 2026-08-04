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
