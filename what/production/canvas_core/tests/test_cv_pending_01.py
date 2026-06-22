"""Tests for canvas_core.traps.cv_pending_01 — graduated trap (3/3 cycles, 100% acceptance).

Authored at M-V1-04 S2 (D1 static check fold; gap fill — graduated trap previously had no
unit test coverage). Mirrors test_cv_text_bounds_01.py shape (M-1-07 + 27 unit tests).

Detection conditions per scaffold spec (`context_iii_canvas_visual.md` Trap CV-PENDING-01):
  (a) text content matches PENDING_PATTERNS (regex: pending_image / pending_panel / [placeholder] / [pending] / TODO: add image / TODO: generate)
  (b) file-node with empty path or path containing 'placeholder'/'pending' substring
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_pending_01 import check
from canvas_core.traps import TrapFinding


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _canvas(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "edges": []}


def _text_node(node_id: str, text: str) -> dict:
    return {"id": node_id, "type": "text", "text": text}


def _file_node(node_id: str, file_path: str) -> dict:
    return {"id": node_id, "type": "file", "file": file_path}


# ---------------------------------------------------------------------------
# (a) Text content placeholder detection
# ---------------------------------------------------------------------------


class TestPlaceholderTextPatterns:
    def test_pending_image_marker_fires(self):
        canvas = _canvas([_text_node("n1", "PendingImage: hero-shot-stanley")])
        findings = check(canvas)
        assert len(findings) == 1
        assert findings[0].trap_id == "CV-PENDING-01"
        assert findings[0].condition == "unresolved_placeholder"
        assert findings[0].severity == "critical"
        assert "n1" in findings[0].node_ids

    def test_pending_panel_marker_fires(self):
        canvas = _canvas([_text_node("n1", "pending_panel for page 3")])
        findings = check(canvas)
        assert len(findings) == 1
        assert findings[0].condition == "unresolved_placeholder"

    def test_placeholder_bracket_marker_fires(self):
        canvas = _canvas([_text_node("n1", "Architecture diagram [placeholder]")])
        findings = check(canvas)
        assert len(findings) == 1

    def test_pending_bracket_marker_fires(self):
        canvas = _canvas([_text_node("n1", "Hero image [pending]")])
        findings = check(canvas)
        assert len(findings) == 1

    def test_todo_add_image_fires(self):
        canvas = _canvas([_text_node("n1", "TODO: add image of Stanley with monitor")])
        findings = check(canvas)
        assert len(findings) == 1

    def test_todo_generate_fires(self):
        canvas = _canvas([_text_node("n1", "TODO: generate panel 4 with R3 character lock")])
        findings = check(canvas)
        assert len(findings) == 1

    def test_case_insensitive_match(self):
        canvas = _canvas([_text_node("n1", "PENDING IMAGE here")])
        findings = check(canvas)
        assert len(findings) == 1

    def test_one_finding_per_node(self):
        """Multiple matching patterns in one node → single finding (break after first match)."""
        canvas = _canvas([_text_node("n1", "[placeholder] PendingImage TODO: add image")])
        findings = check(canvas)
        assert len(findings) == 1


# ---------------------------------------------------------------------------
# (b) File-node empty-path / placeholder-path detection
# ---------------------------------------------------------------------------


class TestFileNodeUnresolved:
    def test_empty_file_path_fires(self):
        canvas = _canvas([_file_node("n1", "")])
        findings = check(canvas)
        assert len(findings) == 1
        assert findings[0].condition == "unresolved_file_reference"
        assert findings[0].severity == "critical"

    def test_placeholder_in_file_path_fires(self):
        canvas = _canvas([_file_node("n1", "assets/placeholder_hero.png")])
        findings = check(canvas)
        assert len(findings) == 1
        assert findings[0].condition == "unresolved_file_reference"

    def test_pending_in_file_path_fires(self):
        canvas = _canvas([_file_node("n1", "assets/pending_panel_4.png")])
        findings = check(canvas)
        assert len(findings) == 1

    def test_resolved_file_path_no_fire(self):
        canvas = _canvas([_file_node("n1", "assets/wilhelm_hero_final.png")])
        findings = check(canvas)
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# Negative cases (clean canvases)
# ---------------------------------------------------------------------------


class TestCleanCanvas:
    def test_clean_text_no_fire(self):
        canvas = _canvas([_text_node("n1", "Wilhelm Foundation rare-disease diagnostic stack")])
        findings = check(canvas)
        assert len(findings) == 0

    def test_empty_canvas_no_fire(self):
        canvas = _canvas([])
        findings = check(canvas)
        assert len(findings) == 0

    def test_no_nodes_field_no_fire(self):
        """Canvas dict without 'nodes' key returns [] (defensive default)."""
        findings = check({"edges": []})
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# Structural / API contract
# ---------------------------------------------------------------------------


class TestApiContract:
    def test_returns_list_of_trap_finding(self):
        canvas = _canvas([_text_node("n1", "PendingImage")])
        findings = check(canvas)
        assert isinstance(findings, list)
        assert all(isinstance(f, TrapFinding) for f in findings)

    def test_severity_critical_for_all_pending_findings(self):
        canvas = _canvas([
            _text_node("n1", "PendingImage"),
            _file_node("n2", ""),
        ])
        findings = check(canvas)
        assert len(findings) == 2
        assert all(f.severity == "critical" for f in findings)

    def test_finding_node_ids_singleton(self):
        canvas = _canvas([_text_node("n1", "PendingImage")])
        findings = check(canvas)
        assert findings[0].node_ids == ["n1"]


# ---------------------------------------------------------------------------
# Mixed canvas (multiple findings)
# ---------------------------------------------------------------------------


class TestMixedCanvas:
    def test_two_node_two_findings(self):
        canvas = _canvas([
            _text_node("n1", "PendingImage hero"),
            _file_node("n2", "assets/placeholder.png"),
            _text_node("n3", "Wilhelm Foundation real content"),
        ])
        findings = check(canvas)
        assert len(findings) == 2
        node_ids = {f.node_ids[0] for f in findings}
        assert node_ids == {"n1", "n2"}
