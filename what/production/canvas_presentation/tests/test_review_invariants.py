"""Tests for PresentationBuilder.review() ↔ structural-state invariants.

Mission: campaign_canvas_visual_command / mission_cvc_m03 (D3) (upstream).

Bug being prevented (D1, fixed in canvas_scoring.py upstream → canvas_presentation/scoring.py
canonical PresentationScoringMixin):
    Before M03, ``PresentationBuilder.review()`` was called from user-facing
    code BEFORE any of ``_apply_structural_fixes()`` had run. The function
    reported orphan slides + missing startNode + a low score, even though
    ``save()`` would produce a structurally-correct canvas with edges and a
    startNode. The pre-fix state was not a real defect — it was transient
    pre-finalization state.

The M03 fix invokes ``_apply_structural_fixes()`` at the top of ``review()``.
The fix is idempotent (the underlying primitives skip already-set startNode,
skip existing nav edges, and set dimensions to constants), so repeated
``review()`` calls do not double-apply.

Migrated from `lattice-protocol/extensions/canvas/tests/test_canvas_presentation_review.py`
under M-R5-01a (campaign_canvasforge_review).
"""

from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import unittest

from canvas_presentation.presentation import PresentationBuilder


def _build_minimal_deck() -> PresentationBuilder:
    """Three-slide happy-path deck — title + content + content."""
    pb = PresentationBuilder(
        name="test_review_invariants",
        version="1.0.0",
        presentation_type="executive",
        theme="scientific",
        density_profile="balanced",
        audience="meeting",
    )
    pb.add_title_slide("Quarterly Review", subtitle="Q1 2026 Highlights")
    pb.add_content_slide(
        "Pipeline Status",
        "### Three Initiatives Shipped\n\n"
        "- Initiative A landed on schedule with all KPIs green\n"
        "- Initiative B partially shipped, full launch slated for Q2\n"
        "- Initiative C exceeded baseline projections by 12%",
    )
    pb.add_content_slide(
        "Looking Forward",
        "### Next Quarter Focus\n\n"
        "- Double down on Initiative C's growth signal\n"
        "- Resource Initiative B's Q2 completion\n"
        "- Open hiring for two senior engineering roles",
    )
    return pb


class TestReviewAppliesStructuralFixes(unittest.TestCase):
    """The M03 invariant: ``review()`` reflects post-finalization state."""

    def test_review_sets_start_node_on_first_call(self) -> None:
        pb = _build_minimal_deck()
        # Sanity: pre-review state is unfinalized
        self.assertIsNone(pb._cb._start_node)

        pb.review()

        self.assertIsNotNone(
            pb._cb._start_node,
            "review() must call _apply_structural_fixes(), which sets _start_node",
        )
        first_slide_id = pb._slides[0]["id"]
        self.assertEqual(pb._cb._start_node, first_slide_id)
        first_node = pb._cb.get_node(first_slide_id)
        self.assertTrue(first_node.get("isStartNode"))

    def test_review_creates_navigation_edges(self) -> None:
        pb = _build_minimal_deck()
        slide_ids = {s["id"] for s in pb._slides}
        # Pre-review: no group-to-group edges
        pre_edges = [
            e for e in pb._cb.edges
            if e["fromNode"] in slide_ids and e["toNode"] in slide_ids
        ]
        self.assertEqual(pre_edges, [])

        pb.review()

        post_edges = [
            e for e in pb._cb.edges
            if e["fromNode"] in slide_ids and e["toNode"] in slide_ids
        ]
        # 3 slides → 2 sequential nav edges
        self.assertEqual(
            len(post_edges), len(pb._slides) - 1,
            "review() must produce exactly len(slides) - 1 sequential nav edges",
        )

    def test_review_reports_no_false_structural_failures(self) -> None:
        pb = _build_minimal_deck()

        report = pb.review()

        for issue in report.issues:
            self.assertNotIn(
                "Orphaned slides", issue,
                "review() must not report orphan slides on a valid happy-path deck",
            )
            self.assertNotIn(
                "No startNode set", issue,
                "review() must not report missing startNode after structural fixes",
            )

    def test_structural_category_scores_post_fix_state(self) -> None:
        pb = _build_minimal_deck()

        report = pb.review()

        structural = report.categories["structural"]
        s2 = next(c for c in structural.criteria if c.id == "S2")
        s4 = next(c for c in structural.criteria if c.id == "S4")
        self.assertEqual(s2.score, 1.0, f"S2 Navigation should be 1.0 post-fix, got {s2.score}")
        self.assertEqual(s4.score, 1.0, f"S4 Start Node should be 1.0 post-fix, got {s4.score}")

    def test_review_is_idempotent(self) -> None:
        """Repeated review() calls must produce the same scores and not duplicate edges."""
        pb = _build_minimal_deck()

        r1 = pb.review()
        edges_after_first = list(pb._cb.edges)
        r2 = pb.review()
        edges_after_second = list(pb._cb.edges)

        self.assertEqual(
            len(edges_after_first), len(edges_after_second),
            "review() must not add duplicate edges on repeated calls",
        )
        self.assertEqual(
            r1.score, r2.score,
            "Identical decks should produce identical review scores across calls",
        )

    def test_review_preserves_first_review_history_consistency(self) -> None:
        """The very first review() must already reflect post-fix state in history."""
        pb = _build_minimal_deck()

        report = pb.review()

        self.assertEqual(len(pb._review_history), 1)
        self.assertEqual(pb._review_history[0].score, report.score)
        struct = pb._review_history[0].categories["structural"]
        s2 = next(c for c in struct.criteria if c.id == "S2")
        self.assertEqual(s2.score, 1.0)


class TestReviewDoesNotChangeContent(unittest.TestCase):
    """review() may apply structural fixes but must not mutate slide content."""

    def test_slide_count_unchanged(self) -> None:
        pb = _build_minimal_deck()
        n_before = len(pb._slides)
        pb.review()
        self.assertEqual(len(pb._slides), n_before)

    def test_slide_titles_unchanged(self) -> None:
        pb = _build_minimal_deck()
        titles_before = [s["title"] for s in pb._slides]
        pb.review()
        titles_after = [s["title"] for s in pb._slides]
        self.assertEqual(titles_before, titles_after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
