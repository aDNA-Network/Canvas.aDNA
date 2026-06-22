"""LOC-heavy substrate smoke for `canvas_core/core.py` (1034 LOC).

Authored under M-R5-01a S2 Phase 4 (`campaign_canvasforge_review`) to
provide minimum-viable test coverage for the largest-LOC canvas_core
module not covered by inherited Phase 1 migrations. Goal: prevent silent
breakage on Phase 7 cleanup-mission file moves; not full unit coverage.

Exercises the `CanvasBuilder` public surface — node creation, edge
creation, group containment, build/save round-trip, validation,
constant invariants. Pure substrate — no canvas_presentation /
canvas_comic imports.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import json
import tempfile
from pathlib import Path

from canvas_core.core import CanvasBuilder


class TestCanvasBuilderInstantiation:
    """Smoke: CanvasBuilder can be constructed and exposes class invariants."""

    def test_default_construction(self):
        cb = CanvasBuilder()
        assert cb.name == "untitled"
        assert cb.version == "1.0.0"
        assert cb.nodes == []
        assert cb.edges == []

    def test_named_construction(self):
        cb = CanvasBuilder(name="test_canvas", version="2.0.0")
        assert cb.name == "test_canvas"
        assert cb.version == "2.0.0"

    def test_valid_constants(self):
        # VALID_* frozensets are non-empty and immutable
        assert len(CanvasBuilder.VALID_NODE_TYPES) >= 4
        assert "text" in CanvasBuilder.VALID_NODE_TYPES
        assert "file" in CanvasBuilder.VALID_NODE_TYPES
        assert "group" in CanvasBuilder.VALID_NODE_TYPES
        assert "link" in CanvasBuilder.VALID_NODE_TYPES
        assert len(CanvasBuilder.VALID_COLORS) == 7  # 0..6

    def test_generate_id_format(self):
        i = CanvasBuilder.generate_id()
        assert isinstance(i, str)
        assert len(i) == 16  # 8 bytes -> 16 hex chars
        # all hex chars
        int(i, 16)


class TestNodeCreation:
    """Smoke: node-creation methods register and return node dicts."""

    def test_add_text_node(self):
        cb = CanvasBuilder()
        node = cb.add_text_node(id="n1", text="Hello", x=0, y=0)
        assert node["type"] == "text"
        assert node["id"] == "n1"
        assert node["text"] == "Hello"
        assert "n1" in cb.node_ids
        assert cb.get_node("n1") is node

    def test_add_file_node(self):
        cb = CanvasBuilder()
        node = cb.add_file_node(id="f1", file="path/to/doc.md", x=0, y=0)
        assert node["type"] == "file"
        assert node["file"] == "path/to/doc.md"

    def test_add_group(self):
        cb = CanvasBuilder()
        cb.add_group(id="g1", x=0, y=0, width=400, height=400, label="Group A")
        assert "g1" in cb.node_ids
        node = cb.get_node("g1")
        assert node["type"] == "group"
        assert node["label"] == "Group A"


class TestEdgeCreation:
    """Smoke: edge creation registers edges with valid endpoints."""

    def test_add_edge(self):
        cb = CanvasBuilder()
        cb.add_text_node(id="a", text="A", x=0, y=0)
        cb.add_text_node(id="b", text="B", x=400, y=0)
        edge = cb.add_edge(id="e1", from_node="a", to_node="b")
        assert edge["fromNode"] == "a"
        assert edge["toNode"] == "b"
        assert len(cb.edges) == 1


class TestBuildAndSaveRoundTrip:
    """Smoke: build() returns a valid canvas dict; save() round-trips through JSON."""

    def test_build_returns_dict(self):
        cb = CanvasBuilder(name="round_trip")
        cb.add_text_node(id="n1", text="Hello", x=0, y=0)
        canvas = cb.build()
        assert isinstance(canvas, dict)
        assert "nodes" in canvas
        assert "edges" in canvas
        assert len(canvas["nodes"]) == 1

    def test_save_round_trip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "smoke.canvas"
            cb = CanvasBuilder(name="smoke_save")
            cb.add_text_node(id="n1", text="Hello", x=0, y=0)
            cb.add_text_node(id="n2", text="World", x=400, y=0)
            cb.add_edge(id="e1", from_node="n1", to_node="n2")
            saved = cb.save(out)
            assert saved.exists()

            data = json.loads(saved.read_text())
            assert "nodes" in data
            assert "edges" in data
            assert len(data["nodes"]) == 2
            assert len(data["edges"]) == 1


class TestValidate:
    """Smoke: validate() returns a list (errors or empty)."""

    def test_clean_canvas_validates(self):
        cb = CanvasBuilder()
        cb.add_text_node(id="n1", text="Hello", x=0, y=0)
        errors = cb.validate()
        assert isinstance(errors, list)
        # A well-formed single-node canvas has no errors
        assert errors == []

    def test_dangling_edge_detected(self):
        cb = CanvasBuilder()
        cb.add_text_node(id="n1", text="Hello", x=0, y=0)
        cb.add_edge(id="e1", from_node="n1", to_node="nonexistent")
        errors = cb.validate()
        assert isinstance(errors, list)
        # Validate produces at least one error reference; specific text not asserted (smoke).
        assert len(errors) >= 1
