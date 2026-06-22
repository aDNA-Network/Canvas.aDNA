"""Tests for canvas_core.traps.cv_coherence_01 (M-R3-01a)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_coherence_01 import check
from canvas_core.traps import TrapFinding


def _canvas(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "edges": []}


def _group(id: str, x: float, y: float, w: float = 1000, h: float = 800,
           color: str | None = None) -> dict:
    g = {"id": id, "type": "group", "x": x, "y": y, "width": w, "height": h}
    if color is not None:
        g["color"] = color
    return g


def _text(id: str, x: float, y: float, text: str = "x",
          cssclasses: str | None = None) -> dict:
    n = {"id": id, "type": "text", "text": text,
         "x": x, "y": y, "width": 200, "height": 100}
    if cssclasses is not None:
        n["styleAttributes"] = {"cssclasses": cssclasses}
    return n


# ---------------------------------------------------------------------------
# (a) palette_drift
# ---------------------------------------------------------------------------


class TestPaletteDrift:
    def test_singleton_color_fires(self):
        """A group with a unique color (no peer) triggers palette_drift."""
        canvas = _canvas([
            _group("g1", 0, 0, color="2"),
            _group("g2", 1500, 0, color="2"),
            _group("g3", 3000, 0, color="5"),  # singleton
        ])
        findings = check(canvas)
        drifts = [f for f in findings if f.condition == "palette_drift"]
        assert len(drifts) == 1
        assert drifts[0].node_ids == ["g3"]
        assert drifts[0].severity == "medium"
        assert "5" in drifts[0].message

    def test_uniform_palette_no_fire(self):
        """All groups using the same color — no drift."""
        canvas = _canvas([
            _group("g1", 0, 0, color="2"),
            _group("g2", 1500, 0, color="2"),
            _group("g3", 3000, 0, color="2"),
        ])
        findings = check(canvas)
        drifts = [f for f in findings if f.condition == "palette_drift"]
        assert len(drifts) == 0

    def test_no_color_no_fire(self):
        """Groups without color attribute don't fire palette_drift."""
        canvas = _canvas([
            _group("g1", 0, 0),
            _group("g2", 1500, 0),
        ])
        findings = check(canvas)
        drifts = [f for f in findings if f.condition == "palette_drift"]
        assert len(drifts) == 0


# ---------------------------------------------------------------------------
# (b) style_drift
# ---------------------------------------------------------------------------


class TestStyleDrift:
    def test_singleton_cssclass_fires(self):
        """A cssclass present in only one group's children triggers style_drift."""
        canvas = _canvas([
            _group("g1", 0, 0),
            _text("t1", 10, 10, cssclasses="hero"),
            _group("g2", 1500, 0),
            _text("t2", 1510, 10, cssclasses="hero"),
            _group("g3", 3000, 0),
            _text("t3", 3010, 10, cssclasses="critical"),  # singleton
        ])
        findings = check(canvas)
        drifts = [f for f in findings if f.condition == "style_drift"]
        assert len(drifts) == 1
        assert drifts[0].node_ids == ["g3"]
        assert "critical" in drifts[0].message

    def test_uniform_cssclasses_no_fire(self):
        """All groups share the same cssclass — no drift."""
        canvas = _canvas([
            _group("g1", 0, 0),
            _text("t1", 10, 10, cssclasses="hero"),
            _group("g2", 1500, 0),
            _text("t2", 1510, 10, cssclasses="hero"),
        ])
        findings = check(canvas)
        drifts = [f for f in findings if f.condition == "style_drift"]
        assert len(drifts) == 0

    def test_multi_token_singleton(self):
        """Multi-token cssclasses where one token is singleton."""
        canvas = _canvas([
            _group("g1", 0, 0),
            _text("t1", 10, 10, cssclasses="hero shared"),
            _group("g2", 1500, 0),
            _text("t2", 1510, 10, cssclasses="shared unique-token"),  # unique-token singleton
        ])
        findings = check(canvas)
        drifts = [f for f in findings if f.condition == "style_drift"]
        # Both 'hero' (g1 only) and 'unique-token' (g2 only) are singletons
        assert len(drifts) == 2
        assert {d.node_ids[0] for d in drifts} == {"g1", "g2"}


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_no_groups_no_fire(self):
        """Canvas with zero groups — early return."""
        canvas = _canvas([_text("t1", 0, 0, cssclasses="hero")])
        findings = check(canvas)
        assert len(findings) == 0

    def test_single_group_no_fire(self):
        """One group has no peers to drift from."""
        canvas = _canvas([
            _group("g1", 0, 0, color="5"),
            _text("t1", 10, 10, cssclasses="hero"),
        ])
        findings = check(canvas)
        # Both palette_drift and style_drift require >=2 groups
        assert len(findings) == 0

    def test_empty_styleattributes_no_fire(self):
        """Children with no styleAttributes contribute no tokens."""
        canvas = _canvas([
            _group("g1", 0, 0, color="2"),
            _text("t1", 10, 10),  # no cssclasses
            _group("g2", 1500, 0, color="2"),
            _text("t2", 1510, 10),
        ])
        findings = check(canvas)
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# R11 escalation
# ---------------------------------------------------------------------------


class TestR11Escalation:
    def test_palette_drift_escalated(self):
        """palette_drift on R11 group bumps severity medium -> high."""
        canvas = _canvas([
            _group("g1", 0, 0, color="2"),
            _group("g2", 1500, 0, color="2"),
            _group("g3", 3000, 0, color="5"),  # singleton
        ])
        findings = check(canvas, r11_node_ids={"g3"})
        drifts = [f for f in findings if f.condition == "palette_drift"]
        assert len(drifts) == 1
        assert drifts[0].severity == "high"

    def test_no_escalation_without_r11(self):
        """Non-R11 nodes keep default severity."""
        canvas = _canvas([
            _group("g1", 0, 0, color="2"),
            _group("g2", 1500, 0, color="2"),
            _group("g3", 3000, 0, color="5"),  # singleton
        ])
        findings = check(canvas, r11_node_ids={"other"})
        drifts = [f for f in findings if f.condition == "palette_drift"]
        assert len(drifts) == 1
        assert drifts[0].severity == "medium"


# ---------------------------------------------------------------------------
# Wilhelm baseline sanity-fire (mission Exit Gate criterion 5)
# ---------------------------------------------------------------------------


class TestWilhelmBaseline:
    def test_wilhelm_fires_at_least_one(self):
        """Wilhelm parity baseline must produce at least one CV-COHERENCE-01 finding.

        Wilhelm canvas has color=5 (singleton), color=3 (×2), color=2 (×3),
        plus 9 groups with no color — palette_drift should fire on the
        singleton 'Rare AI Archive' group.
        """
        import json
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "..",
            "what", "artifacts", "parity_deck", "wilhelm_parity.canvas"
        )
        path = os.path.normpath(path)
        if not os.path.isfile(path):
            import pytest
            pytest.skip(f"Wilhelm baseline missing: {path}")

        with open(path) as f:
            canvas_data = json.load(f)

        findings = check(canvas_data)
        assert len(findings) >= 1, (
            f"Expected >=1 CV-COHERENCE-01 finding on Wilhelm baseline, got {len(findings)}"
        )
