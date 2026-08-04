"""Tests for canvas_core.traps.cli — `canvas-visual-check` (Halftone HV O3).

Includes the two named acceptance fixtures from the HV mission:
  - a 320x110 text node with a `##` lead MUST FAIL (the Oration shape);
  - the reworked pattern (`**bold**` lead, 340x200) MUST PASS.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cli import check_canvas, main


ORATION_FAIL_TEXT = (
    "## The Authentic Voice\n"
    "Speak from lived experience; the audience forgives everything except "
    "pretending. Three beats: arrival, turn, gift."
)
REWORKED_PASS_TEXT = (
    "**The Authentic Voice**\n"
    "Speak from lived experience; the audience forgives everything except "
    "pretending."
)


def _write_canvas(path, nodes, edges=None):
    path.write_text(json.dumps({"nodes": nodes, "edges": edges or []}))
    return str(path)


def _text_node(id, text, w, h):
    return {"id": id, "type": "text", "text": text,
            "x": 0, "y": 0, "width": w, "height": h}


class TestAcceptanceFixtures:
    def test_oration_shape_fails(self, tmp_path, capsys):
        """320x110 + `##` lead: overflow (CV-TEXT-BOUNDS) fires; exit 1."""
        p = _write_canvas(tmp_path / "broken.canvas",
                          [_text_node("t1", ORATION_FAIL_TEXT, 320, 110)])
        findings, _ = check_canvas(p)
        trap_ids = {f.trap_id for f in findings}
        assert "CV-TEXT-BOUNDS-01" in trap_ids  # calibrated overflow
        assert "CV-LEAD-COST-01" in trap_ids    # the avoidable cause
        # --strict: medium findings (overflow, lead-cost) fail the run.
        assert main([p, "--strict"]) == 1
        out = capsys.readouterr().out
        assert "Set height >=" in out

    def test_reworked_shape_passes(self, tmp_path, capsys):
        """**bold** lead + 340x200 (the M-R5 rework pattern): exit 0."""
        p = _write_canvas(tmp_path / "fixed.canvas",
                          [_text_node("t1", REWORKED_PASS_TEXT, 340, 200)])
        assert main([p, "--strict"]) == 0
        out = capsys.readouterr().out
        assert "[OK]" in out
        assert "looking at the rendered canvas" in out


class TestCliBehavior:
    def test_json_output_shape(self, tmp_path, capsys):
        p = _write_canvas(tmp_path / "c.canvas",
                          [_text_node("t1", "Short.", 300, 120)])
        rc = main([p, "--json"])
        report = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert report["canvas"] == p
        assert report["ok"] is True
        assert isinstance(report["findings"], list)
        # 13 implemented/graduated traps (9 pre-HV + 4 HV) minus the 2
        # presentation-workflow traps the default profile skips.
        assert report["traps_run"] >= 11

    def test_unreadable_input_exits_2(self, tmp_path):
        bad = tmp_path / "bad.canvas"
        bad.write_text("{not json")
        assert main([str(bad)]) == 2

    def test_default_exit_ignores_medium(self, tmp_path):
        """Without --strict, medium-only findings keep exit 0."""
        p = _write_canvas(tmp_path / "warnish.canvas",
                          [_text_node("t1", "## Lead\nOne line.", 600, 300)])
        assert main([p]) == 0
        assert main([p, "--strict"]) == 1

    def test_vault_root_autodetect_wires_file_traps(self, tmp_path):
        (tmp_path / ".obsidian").mkdir()
        p = _write_canvas(
            tmp_path / "c.canvas",
            [{"id": "f1", "type": "file", "file": "missing.md",
              "x": 0, "y": 0, "width": 300, "height": 200}],
        )
        findings, root = check_canvas(p)
        assert root == str(tmp_path)
        assert any(f.condition == "file_missing" for f in findings)

    def test_multiple_files_worst_exit_wins(self, tmp_path, capsys):
        good = _write_canvas(tmp_path / "good.canvas",
                             [_text_node("t1", "Fine.", 300, 120)])
        bad = _write_canvas(tmp_path / "bad.canvas",
                            [_text_node("t2", ORATION_FAIL_TEXT, 320, 110)])
        assert main([good, bad, "--strict"]) == 1
