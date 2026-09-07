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

from canvas_core import layout_fit as lf
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


class TestProfiles:
    """`--profile` (Halftone H6, from H4 finding #4).

    A comic page is a composed reading surface: panels bleed flush to the page
    edge, a page carries no heading, a splash fills its page. The three
    knowledge-canvas *aesthetic* traps fire on every conformant comic page —
    a gate that always fails is not a gate. The `comic` profile drops exactly
    those three and nothing else.
    """

    AESTHETIC = {"CV-GROUP-PADDING-01", "CV-HIERARCHY-01", "CV-NODE-DENSITY-01"}
    CORRECTNESS = {
        "CV-TEXT-BOUNDS-01", "CV-LEAD-COST-01", "CV-EDGE-LABEL-01",
        "CV-FILE-PROPS-01", "CV-IMAGE-ASPECT-RATIO-01", "CV-COHERENCE-01",
        "CV-PENDING-01", "CV-GROUP-LABEL-01",
    }

    def _flush_page(self, tmp_path):
        """A page group whose panel bleeds flush to every edge — legal comic."""
        return _write_canvas(
            tmp_path / "page.canvas",
            [
                {"id": "pg", "type": "group", "label": "Page 1",
                 "x": 0, "y": 0, "width": 663, "height": 1025},
                {"id": "pg_p0", "type": "text", "text": "Panel one.",
                 "x": 0, "y": 0, "width": 663, "height": 1025},
            ],
        )

    def test_default_profile_is_unchanged(self, tmp_path):
        """knowledge-canvas is the default and is byte-identical to pre-H6."""
        from canvas_core.traps.cli import DEFAULT_PROFILE, _profile_skips
        assert DEFAULT_PROFILE == "knowledge-canvas"
        assert _profile_skips() == _profile_skips("knowledge-canvas")
        assert "CV-DIMENSION-VISIBILITY-01" in _profile_skips()

    def test_comic_profile_drops_only_the_aesthetic_traps(self):
        from canvas_core.traps.cli import _profile_skips
        dropped = _profile_skips("comic") - _profile_skips("knowledge-canvas")
        assert dropped == self.AESTHETIC

    def test_correctness_traps_survive_every_profile(self):
        """The load-bearing guarantee: no profile ever drops a real check."""
        from canvas_core.traps.cli import PROFILES, _profile_skips
        for profile in PROFILES:
            assert not (self.CORRECTNESS & _profile_skips(profile)), profile

    def test_flush_comic_page_fails_default_passes_comic(self, tmp_path):
        p = self._flush_page(tmp_path)
        default_findings, _ = check_canvas(p)
        assert {f.trap_id for f in default_findings} & self.AESTHETIC
        comic_findings, _ = check_canvas(p, profile="comic")
        assert comic_findings == []
        assert main([p, "--profile", "comic"]) == 0

    def test_all_traps_flag_is_an_alias_for_profile_all(self, tmp_path):
        from canvas_core.traps.cli import _resolve_profile, _profile_skips
        assert _resolve_profile(None, True) == "all"
        assert _resolve_profile(None, False) == "knowledge-canvas"
        # An explicit --profile wins over the deprecated flag.
        assert _resolve_profile("comic", True) == "comic"
        assert _profile_skips("all") == set()

    def test_comic_profile_admits_comic_specific_scope(self):
        """CV-COMIC-STYLE-01 is scaffolded; the profile must not pre-skip it."""
        from canvas_core.traps.cli import _profile_skips
        assert "CV-COMIC-STYLE-01" not in _profile_skips("comic")
        assert "CV-COMIC-STYLE-01" in _profile_skips("knowledge-canvas")

    def test_unknown_profile_is_rejected(self, tmp_path):
        # Was "deck" until Blueprint P2c made it a real profile.
        p = _write_canvas(tmp_path / "c.canvas",
                          [_text_node("t1", "Fine.", 300, 120)])
        try:
            check_canvas(p, profile="poster")
        except ValueError as exc:
            assert "unknown profile" in str(exc)
        else:
            raise AssertionError("expected ValueError for an unknown profile")

    # --- deck profile (Blueprint P2c, 2026-09-07) ---------------------------

    def test_deck_profile_drops_the_same_aesthetics_as_comic(self):
        from canvas_core.traps.cli import _profile_skips
        assert self.AESTHETIC <= _profile_skips("deck")

    def test_deck_profile_admits_what_the_default_suppresses(self):
        """The deck profile is a RE-AIM, not a relaxation.

        It drops 3 inapplicable aesthetics **and admits 2 checks the default
        hides from a deck** — its own ``deck-specific`` traps and the
        presentation-metadata trap, both of which a deck genuinely has. On the
        shipped example that surfaced a HIGH the default profile could not see
        (F-P2-10).
        """
        from canvas_core.traps.cli import _profile_skips
        assert "CV-AUDIENCE-01" not in _profile_skips("deck")
        assert "CV-AUDIENCE-01" in _profile_skips("knowledge-canvas")
        assert "CV-DIMENSION-VISIBILITY-01" not in _profile_skips("deck")
        assert "CV-DIMENSION-VISIBILITY-01" in _profile_skips("knowledge-canvas")

    def test_deck_profile_excludes_comic_traps(self):
        from canvas_core.traps.cli import _profile_skips
        assert "CV-COMIC-STYLE-01" in _profile_skips("deck")

    def test_full_slide_fails_default_passes_deck(self, tmp_path):
        """A 16:9 slide filled edge-to-edge is a slide, not a defect."""
        p = _write_canvas(
            tmp_path / "slide.canvas",
            [
                {"id": "s0", "type": "group", "label": "Slide 1",
                 "x": 0, "y": 0, "width": 1280, "height": 720},
                {"id": "s0_body", "type": "text", "text": "Body copy.",
                 "x": 0, "y": 0, "width": 1280, "height": 720},
            ],
        )
        default_findings, _ = check_canvas(p)
        assert {f.trap_id for f in default_findings} & self.AESTHETIC
        deck_findings, _ = check_canvas(p, profile="deck")
        assert not ({f.trap_id for f in deck_findings} & self.AESTHETIC)

    # --- advisory (ungraduated) traps: report, do not gate (P2c) -------------

    def test_advisory_set_is_narrow(self):
        """Only traps that have FIRED and never been accepted — not every ungraduated one.

        The broad reading ("not graduated and nothing accepted") captures 13 of the 14 live traps,
        including CV-TEXT-BOUNDS-01, and would silence the gate entirely (F-P2-13). Guard the
        narrow predicate so nobody widens it back by accident.
        """
        from canvas_core.traps.cli import _advisory_trap_ids
        advisory = _advisory_trap_ids()
        assert "CV-AUDIENCE-01" in advisory       # fired=2, accepted=0
        assert "CV-TEXT-BOUNDS-01" not in advisory  # fired=0 -> no record, not "useless"
        assert "CV-FILE-PROPS-01" not in advisory
        assert "CV-PENDING-01" not in advisory      # graduated
        assert len(advisory) < len(self.CORRECTNESS)

    def test_advisory_finding_does_not_set_exit_code(self, tmp_path, capsys):
        """A HIGH from an advisory trap prints, is tagged, and still exits 0."""
        # Three slide groups with wildly uneven word counts -> CV-AUDIENCE-01 (advisory, HIGH).
        nodes = []
        for i, words in enumerate((2, 60, 3)):
            x = i * 700
            nodes.append({"id": f"s{i}", "type": "group", "label": f"Slide {i}",
                          "x": x, "y": 0, "width": 600, "height": 900})
            text = " ".join(["word"] * words)
            nodes.append({"id": f"s{i}_t", "type": "text", "text": text,
                          "x": x + 40, "y": 40,
                          "width": 500, "height": lf.fit_text_height(text, 500, min_height=200)})
        p = _write_canvas(tmp_path / "uneven.canvas", nodes)
        findings, _ = check_canvas(p, profile="deck")
        assert any(f.trap_id == "CV-AUDIENCE-01" and f.severity == "high" for f in findings)
        assert main([p, "--profile", "deck"]) == 0
        out = capsys.readouterr().out
        assert "(advisory)" in out and "does not gate" in out

    def test_advisory_flag_is_reported_in_json(self, tmp_path, capsys):
        p = self._flush_page(tmp_path)
        main([p, "--profile", "all", "--json"])
        findings = json.loads(capsys.readouterr().out)["findings"]
        assert findings and all("advisory" in f for f in findings)

    def test_a_gating_trap_still_fails(self, tmp_path):
        """The rule must not have silenced the gate — a real HIGH still exits 1."""
        p = _write_canvas(tmp_path / "missing.canvas", [
            {"id": "f1", "type": "file", "file": "nope/does_not_exist.png",
             "x": 0, "y": 0, "width": 100, "height": 100},
        ])
        findings, _ = check_canvas(p, vault_root=str(tmp_path))
        assert any(f.trap_id == "CV-FILE-PROPS-01" for f in findings)
        assert main([p, "--vault-root", str(tmp_path)]) == 1

    def test_profile_is_reported_in_json(self, tmp_path, capsys):
        p = self._flush_page(tmp_path)
        main([p, "--profile", "comic", "--json"])
        assert json.loads(capsys.readouterr().out)["profile"] == "comic"
