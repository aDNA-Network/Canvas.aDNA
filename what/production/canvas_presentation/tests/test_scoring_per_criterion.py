"""Per-criterion structural-invariant tests for PresentationScoringMixin.

Mission: campaign_canvasforge_review / M-R5-01a S3 (closes F-2 HIGH).

Authored 2026-05-01. One invariant test per criterion in
``canvas_presentation/scoring.py`` (24 total: S1-S5, C1-C5, D1-D5, T1-T5,
A1-A4) plus one companion VR-baseline integrity test.

Each criterion test builds a deterministic synthetic fixture that exercises
the criterion's hot path, calls ``pb.review()`` (the public scorer entry
point — auto-runs ``_apply_structural_fixes()`` per the M-1-04 G6 contract),
then asserts an invariant property of the criterion's score (range,
boundary, or documented-branch exact value).

The 24-criterion S/C/D/T/A axis is distinct from the 5-VR-dim baseline axis
in ``baseline_vr_scores.json``. Per the M-R5-01a S1 plan: NO axis-mismatched
approx-match. The companion ``TestVRBaselineIntegrity`` test asserts the
locked file's SHA-256 + schema integrity instead.

Critical Rule 2 guardrail: the VR-baseline file is LOCKED at SHA-256
``3ce4d341a727e53434eab16a30b3c9a6e0316ca62c5d6914b984e3ac2939e8b6``. Drift
in the SHA assertion signals a baseline-modification incident, NOT a
test-author mistake — STOP and consult Stanley.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core import CriterionScore, PresentationReport
from canvas_presentation.presentation import PresentationBuilder


LOCKED_BASELINE_SHA256 = (
    "3ce4d341a727e53434eab16a30b3c9a6e0316ca62c5d6914b984e3ac2939e8b6"
)
BASELINE_PATH = (
    Path(__file__).resolve().parents[2] / "canvas_core" / "tests" / "fixtures" / "baseline_vr_scores.json"
)


def _criterion(report: PresentationReport, category: str, cid: str) -> CriterionScore:
    """Locate a single CriterionScore by category + id within a report."""
    for c in report.categories[category].criteria:
        if c.id == cid:
            return c
    raise KeyError(f"criterion {category}/{cid} not in report")


# ----------------------------------------------------------------- S --


class TestStructuralInvariants(unittest.TestCase):
    """S1-S5: structural category invariants."""

    def test_s1_slide_count_in_audience_range_scores_one(self) -> None:
        # Keynote range is 8-20; build 12 slides → in-range branch returns 1.0
        pb = PresentationBuilder(name="t_s1", theme="scientific", audience="keynote")
        pb.add_title_slide("Build the Future", subtitle="Vision 2026")
        for i in range(11):
            pb.add_content_slide(f"Drive Outcome {i+1}", "### Highlight\n\n- One result")
        report = pb.review()
        self.assertEqual(_criterion(report, "structural", "S1").score, 1.0)

    def test_s2_navigation_complete_post_review_scores_one(self) -> None:
        # review() runs _apply_structural_fixes() which connects all slides
        # and sets startNode → orphan_ratio=0 + has_start=True → score=1.0
        pb = PresentationBuilder(name="t_s2", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Q1", subtitle="Quarterly")
        pb.add_content_slide("Build Pipeline", "### Status\n\n- Initiative A landed")
        pb.add_content_slide("Reveal Direction", "### Next\n\n- Initiative B in flight")
        report = pb.review()
        self.assertEqual(_criterion(report, "structural", "S2").score, 1.0)

    def test_s3_section_grouping_six_slide_deck_scores_one(self) -> None:
        # With ≤8 slides and no dividers, S3 takes the auto-pass branch (1.0)
        pb = PresentationBuilder(name="t_s3", theme="scientific", audience="meeting")
        pb.add_title_slide("Build Quarterly", subtitle="Q1")
        for i in range(5):
            pb.add_content_slide(f"Drive Result {i+1}", "### Win\n\n- Outcome shipped")
        report = pb.review()
        self.assertEqual(_criterion(report, "structural", "S3").score, 1.0)

    def test_s4_start_node_first_title_post_review_scores_one(self) -> None:
        # review()._apply_structural_fixes() sets startNode to first slide
        # which is a title → matches the perfect branch (1.0)
        pb = PresentationBuilder(name="t_s4", theme="scientific", audience="meeting")
        pb.add_title_slide("Build Future", subtitle="Vision")
        pb.add_content_slide("Drive Path", "### Plan\n\n- Step one")
        pb.add_content_slide("Reveal Outcome", "### Result\n\n- Win shipped")
        report = pb.review()
        self.assertEqual(_criterion(report, "structural", "S4").score, 1.0)

    def test_s5_three_plus_non_title_types_scores_one(self) -> None:
        # Five slides, four non-title types (content/stats/quote/image)
        # → 3+ types → score=1.0
        pb = PresentationBuilder(name="t_s5", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Variety", subtitle="Mix")
        pb.add_content_slide("Build A", "### A\n\n- Detail")
        pb.add_stats_slide("Reveal Numbers", [("42%", "Growth"), ("3x", "Speed")])
        pb.add_quote_slide("Achieve Voice", quote="Excellence is a habit.", attribution="Aristotle")
        pb.add_image_slide("Show Image", image_path=None, alt_text="placeholder")
        report = pb.review()
        self.assertEqual(_criterion(report, "structural", "S5").score, 1.0)


# ----------------------------------------------------------------- C --


class TestContentInvariants(unittest.TestCase):
    """C1-C5: content category invariants."""

    def test_c1_word_density_under_limit_scores_one(self) -> None:
        # Meeting + balanced → content limit ~100 words; bodies of ~10
        # words each are well under-limit AND well over the 0.1× under-flow
        # floor — so no penalties accumulate → score=1.0.
        pb = PresentationBuilder(name="t_c1", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Q1", subtitle="Quarterly")
        pb.add_content_slide(
            "Build Pipeline",
            "### Highlight\n\n- Initiative A landed on schedule with green KPIs across the board\n"
            "- Initiative B partially shipped",
        )
        pb.add_content_slide(
            "Reveal Forward",
            "### Next\n\n- Initiative C exceeded baseline projections by twelve percent\n"
            "- Open hiring for two senior engineers",
        )
        report = pb.review()
        self.assertEqual(_criterion(report, "content", "C1").score, 1.0)

    def test_c2_titles_with_verbs_score_one(self) -> None:
        # Verb regex matches "build", "drive", "reveal", "deliver" etc.
        # → all per-slide title scores = 1.0 → mean = 1.0.
        pb = PresentationBuilder(name="t_c2", theme="scientific", audience="meeting")
        pb.add_title_slide("Build the Future", subtitle="Vision")
        pb.add_content_slide("Drive Q1 Growth", "### Outcome\n\n- Numbers up")
        pb.add_content_slide("Reveal Findings", "### Result\n\n- Pattern observed")
        report = pb.review()
        self.assertEqual(_criterion(report, "content", "C2").score, 1.0)

    def test_c3_short_flat_bullet_lists_score_one(self) -> None:
        # ≤5 bullets at depth 1 → per-node score 1.0 → mean 1.0.
        pb = PresentationBuilder(name="t_c3", theme="scientific", audience="meeting")
        pb.add_title_slide("Build Three", subtitle="Outline")
        pb.add_content_slide(
            "Drive Three Items",
            "### Items\n\n- First item\n- Second item\n- Third item",
        )
        report = pb.review()
        self.assertEqual(_criterion(report, "content", "C3").score, 1.0)

    def test_c4_visual_ratio_at_audience_target_scores_one(self) -> None:
        # Meeting target = 0.15. Build 5 slides, 1 image → ratio = 0.20 ≥ target → 1.0.
        pb = PresentationBuilder(name="t_c4", theme="scientific", audience="meeting")
        pb.add_title_slide("Build Mix", subtitle="Visual")
        pb.add_content_slide("Drive A", "### A\n\n- One")
        pb.add_content_slide("Drive B", "### B\n\n- Two")
        pb.add_content_slide("Drive C", "### C\n\n- Three")
        pb.add_image_slide("Reveal Image", image_path=None, alt_text="placeholder")
        report = pb.review()
        self.assertEqual(_criterion(report, "content", "C4").score, 1.0)

    def test_c5_no_heading_jumps_scores_one(self) -> None:
        # Bodies with sequential heading levels (h3 → h4) → no jumps → 1.0.
        pb = PresentationBuilder(name="t_c5", theme="scientific", audience="meeting")
        pb.add_title_slide("Build Hierarchy", subtitle="Order")
        pb.add_content_slide(
            "Drive Levels",
            "### Section\n\n#### Subsection\n\n- Detail",
        )
        report = pb.review()
        self.assertEqual(_criterion(report, "content", "C5").score, 1.0)


# ----------------------------------------------------------------- D --


class TestDesignInvariants(unittest.TestCase):
    """D1-D5: design category invariants."""

    def test_d1_whitespace_score_in_unit_range(self) -> None:
        # D1 is layout-heuristic — assert range invariant rather than exact.
        # The contract is bounded [0, 1]; any leak (negative or >1) signals
        # a regression in _score_d1_whitespace's clamping logic.
        pb = PresentationBuilder(name="t_d1", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Whitespace", subtitle="Air")
        pb.add_content_slide("Build Body", "### Air\n\n- One short line\n- Two short line")
        pb.add_content_slide("Reveal Air", "### More\n\n- Brief detail")
        report = pb.review()
        score = _criterion(report, "design", "D1").score
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_d2_no_explicit_colors_scores_one(self) -> None:
        # No slides have group color → colors_used empty → consistency 1.0
        # → nc≤3 branch → score = 1.0.
        pb = PresentationBuilder(name="t_d2", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Color", subtitle="None set")
        pb.add_content_slide("Build A", "### A\n\n- One")
        pb.add_content_slide("Reveal B", "### B\n\n- Two")
        report = pb.review()
        self.assertEqual(_criterion(report, "design", "D2").score, 1.0)

    def test_d3_under_three_slides_scores_one(self) -> None:
        # The early-return branch: <3 slides → score=1.0 unconditionally.
        pb = PresentationBuilder(name="t_d3", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Two", subtitle="Pair")
        pb.add_content_slide("Build A", "### A\n\n- Single bullet")
        report = pb.review()
        self.assertEqual(_criterion(report, "design", "D3").score, 1.0)

    def test_d4_no_mixed_image_text_slides_scores_one(self) -> None:
        # No slide has BOTH image and text → balance_scores=[] → mean
        # branch returns 1.0 default.
        pb = PresentationBuilder(name="t_d4", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Balance", subtitle="Default")
        pb.add_content_slide("Build A", "### A\n\n- Text only")
        pb.add_content_slide("Reveal B", "### B\n\n- Still text only")
        report = pb.review()
        self.assertEqual(_criterion(report, "design", "D4").score, 1.0)

    def test_d5_consistent_heading_per_type_scores_one(self) -> None:
        # All content slides start their first text node with h3 → no
        # heading-level conflict per type → violations=0 → score 1.0.
        pb = PresentationBuilder(name="t_d5", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Typo", subtitle="Consistent")
        pb.add_content_slide("Build Same", "### Header\n\n- Detail one")
        pb.add_content_slide("Reveal Same", "### Header\n\n- Detail two")
        pb.add_content_slide("Achieve Same", "### Header\n\n- Detail three")
        report = pb.review()
        self.assertEqual(_criterion(report, "design", "D5").score, 1.0)


# ----------------------------------------------------------------- T --


class TestStorytellingInvariants(unittest.TestCase):
    """T1-T5: storytelling category invariants."""

    def test_t1_three_phases_present_scores_one(self) -> None:
        # arc=None → heuristic path: title (setup) + comparison (contrast,
        # mid third) + stats (resolution, last third) → 3 phases → 1.0.
        pb = PresentationBuilder(name="t_t1", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Arc", subtitle="Three Phases")
        pb.add_content_slide("Build Setup", "### Phase\n\n- Setup detail")
        pb.add_comparison_slide(
            "Reveal Contrast",
            left_label="Before", left_content="- Slow",
            right_label="After", right_content="- Fast",
        )
        pb.add_content_slide("Drive Mid", "### Mid\n\n- Middle detail")
        pb.add_stats_slide("Achieve Resolution", [("42%", "Improvement")])
        report = pb.review()
        self.assertEqual(_criterion(report, "storytelling", "T1").score, 1.0)

    def test_t2_title_then_engaging_scores_one(self) -> None:
        # First slide title + second slide content (in engaging set) → 1.0.
        pb = PresentationBuilder(name="t_t2", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Open", subtitle="Strong")
        pb.add_content_slide("Build Engagement", "### Hook\n\n- Engaging point")
        pb.add_content_slide("Reveal Body", "### Body\n\n- Detail")
        report = pb.review()
        self.assertEqual(_criterion(report, "storytelling", "T2").score, 1.0)

    def test_t3_two_quote_slides_scores_one(self) -> None:
        # Two quote-typed slides count as STAR moments → ≥2 → score=1.0.
        pb = PresentationBuilder(name="t_t3", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Stars", subtitle="Quotes")
        pb.add_quote_slide("Achieve Voice One", quote="Excellence is a habit.", attribution="A")
        pb.add_content_slide("Build Bridge", "### Bridge\n\n- Connector")
        pb.add_quote_slide("Achieve Voice Two", quote="Quality is never an accident.", attribution="B")
        report = pb.review()
        self.assertEqual(_criterion(report, "storytelling", "T3").score, 1.0)

    def test_t4_average_words_in_audience_range_scores_one(self) -> None:
        # Meeting expects 40-80 words per slide. Build 3 content slides with
        # bodies in that range → avg in range → score=1.0.
        body = (
            "### Outcome\n\n"
            "- We shipped initiative alpha on schedule with measurable impact across the board\n"
            "- We extended runway through the next two quarters by reducing inefficiencies in the pipeline\n"
            "- We grew the team by two senior engineers and one product partner this quarter overall"
        )
        pb = PresentationBuilder(name="t_t4", theme="scientific", audience="meeting")
        pb.add_content_slide("Drive Quarter A", body)
        pb.add_content_slide("Build Quarter B", body)
        pb.add_content_slide("Reveal Quarter C", body)
        report = pb.review()
        self.assertEqual(_criterion(report, "storytelling", "T4").score, 1.0)

    def test_t5_cta_verb_in_last_slide_scores_one(self) -> None:
        # Last slide body contains a CTA verb ("contact") → score=1.0.
        pb = PresentationBuilder(name="t_t5", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Close", subtitle="CTA")
        pb.add_content_slide("Build Body", "### Body\n\n- Detail one")
        pb.add_content_slide(
            "Reveal Action",
            "### Next Step\n\nContact the team to schedule a follow-up.",
        )
        report = pb.review()
        self.assertEqual(_criterion(report, "storytelling", "T5").score, 1.0)


# ----------------------------------------------------------------- A --


class TestAccessibilityInvariants(unittest.TestCase):
    """A1-A4: accessibility category invariants."""

    def test_a1_all_visuals_have_alt_text_scores_one(self) -> None:
        # All visual-typed slides supply alt_text → covered/visual = 1.0.
        # add_diagram_slide requires diagram_file OR mermaid; supply minimal mermaid.
        pb = PresentationBuilder(name="t_a1", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Access", subtitle="Alt Text")
        pb.add_diagram_slide(
            "Build Diagram",
            mermaid="graph LR\n  A --> B",
            alt_text="Topology overview",
        )
        pb.add_image_slide("Reveal Image", image_path=None, alt_text="Hero photo")
        report = pb.review()
        self.assertEqual(_criterion(report, "accessibility", "A1").score, 1.0)

    def test_a2_no_heading_jumps_scores_one(self) -> None:
        # Sequential heading levels h3→h4→h5 → no jumps>1 → score=1.0.
        pb = PresentationBuilder(name="t_a2", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Hierarchy", subtitle="Levels")
        pb.add_content_slide(
            "Build Sequence",
            "### Section\n\n#### Subsection\n\n##### Detail\n\n- Bullet",
        )
        report = pb.review()
        self.assertEqual(_criterion(report, "accessibility", "A2").score, 1.0)

    def test_a3_under_audience_density_ceiling_scores_one(self) -> None:
        # Meeting ceiling = 160 words. Bodies under 160 words each → 0
        # violations → score=1.0.
        pb = PresentationBuilder(name="t_a3", theme="scientific", audience="meeting")
        pb.add_title_slide("Drive Density", subtitle="Bounded")
        pb.add_content_slide("Build Slide", "### Detail\n\n- One short bullet point")
        pb.add_content_slide("Reveal Slide", "### Detail\n\n- Two short bullet point")
        report = pb.review()
        self.assertEqual(_criterion(report, "accessibility", "A3").score, 1.0)

    def test_a4_passing_palette_scores_one(self) -> None:
        # Tokyo Night palette has high-contrast text/bg pairs that pass
        # WCAG AA large-text (≥3:1) for all 4 tested pairs → 1.0.
        # See THEME_PALETTES["tokyo_night"] in canvas_presentation/config_deck.py.
        pb = PresentationBuilder(name="t_a4", theme="tokyo_night", audience="meeting")
        pb.add_title_slide("Drive Contrast", subtitle="WCAG AA")
        pb.add_content_slide("Build Pair", "### Detail\n\n- One")
        report = pb.review()
        self.assertEqual(_criterion(report, "accessibility", "A4").score, 1.0)


# --------------------------------------------------------- VR baseline --


class TestVRBaselineIntegrity(unittest.TestCase):
    """One companion test: VR-baseline file integrity (Critical Rule 2).

    The 24-criterion S/C/D/T/A axis is distinct from the 5-VR-dim baseline
    axis, and the cells grid in baseline_vr_scores.json was synthesized
    from LLM-derived M2 cross-theme scores + interpolation (per the
    file's own ``methodology`` field, lines 2475-2489) — NOT from a
    deterministic scorer. Programmatic per-cell numerical reproduction
    therefore requires either (a) a Gemini API + Playwright run via
    ``score_runner_parity.py`` or (b) cached LLM responses; neither is
    available in CI.

    What IS testable in CI: the locked file's byte-level integrity (SHA-256
    against the locked hash) and its internal schema integrity (cell count,
    cross-references between ``themes``/``slide_types`` lists and the cell
    grid, cell field shape, derived-counter consistency). A mismatch on
    any of these signals a Critical Rule 2 violation: STOP and consult
    Stanley before any further work.
    """

    def test_baseline_file_integrity(self) -> None:
        # 1) Byte-level SHA-256 against the LOCKED hash (Critical Rule 2).
        digest = hashlib.sha256(BASELINE_PATH.read_bytes()).hexdigest()
        self.assertEqual(
            digest, LOCKED_BASELINE_SHA256,
            f"baseline_vr_scores.json SHA-256 drift! Expected {LOCKED_BASELINE_SHA256}, "
            f"got {digest}. This signals a Critical Rule 2 violation. STOP and consult Stanley.",
        )

        # 2) Schema integrity: load and validate structure.
        baseline = json.loads(BASELINE_PATH.read_text())
        themes = baseline["themes"]
        slide_types = baseline["slide_types"]
        cells = baseline["cells"]

        self.assertEqual(len(themes), 7, "expected 7 themes in baseline")
        self.assertEqual(len(slide_types), 15, "expected 15 slide types in baseline")
        self.assertEqual(set(cells.keys()), set(themes), "cells.keys() must match themes list")

        for theme in themes:
            theme_cells = cells[theme]
            self.assertEqual(
                set(theme_cells.keys()), set(slide_types),
                f"cells[{theme!r}] keys must match slide_types list",
            )
            for slide_type in slide_types:
                cell = theme_cells[slide_type]
                for field in ("vr1", "vr2", "vr3", "vr4", "vr5", "weighted", "status"):
                    self.assertIn(
                        field, cell,
                        f"cells[{theme!r}][{slide_type!r}] missing field {field!r}",
                    )

        # 3) vr_weights sum to 1.0 (within float tolerance).
        weights_sum = sum(baseline["vr_weights"].values())
        self.assertAlmostEqual(weights_sum, 1.0, places=9)

        # 4) Derived counters are consistent.
        actual_total = sum(len(theme_cells) for theme_cells in cells.values())
        self.assertEqual(baseline["cells_total"], actual_total)
        actual_passing = sum(
            1
            for theme_cells in cells.values()
            for cell in theme_cells.values()
            if cell["status"] == "PASS"
        )
        self.assertEqual(baseline["cells_passing"], actual_passing)


if __name__ == "__main__":
    unittest.main(verbosity=2)
