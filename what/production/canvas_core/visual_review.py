"""Visual inspection pipeline for presentation quality assessment.

Provides a framework for screenshot-based visual review of rendered
canvas presentations. Uses Playwright for screenshots and an LLM
(via Gemini MCP) for visual quality scoring.

This is a soft gate — informational scoring, not blocking. The
programmatic review system remains the primary quality gate.

Part of campaign_presentation_excellence M16 (Visual Quality Engine).
"""

from __future__ import annotations

import json
import statistics
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Visual Quality Rubric — 5 Criteria, 0-10 each
# ---------------------------------------------------------------------------

VISUAL_CRITERIA = [
    {
        "id": "VR1",
        "name": "Text Readability",
        "description": (
            "Font size appropriate for projection/reading. No text cramping "
            "or overflow. Line length comfortable (45-75 chars). Adequate "
            "contrast between text and background."
        ),
        "weight": 0.25,
    },
    {
        "id": "VR2",
        "name": "Visual Hierarchy",
        "description": (
            "Headings clearly prominent above body text. Clear information "
            "flow direction (top→bottom or left→right). Eye naturally drawn "
            "to the most important element first."
        ),
        "weight": 0.25,
    },
    {
        "id": "VR3",
        "name": "Whitespace Quality",
        "description": (
            "Breathing room around content elements. Margins feel generous "
            "but not wasteful. Consistent spacing rhythm. No cramped areas "
            "or awkward gaps."
        ),
        "weight": 0.20,
    },
    {
        "id": "VR4",
        "name": "Color Harmony",
        "description": (
            "Colors work together cohesively. Accent colors draw attention "
            "without clashing. Background doesn't compete with content. "
            "Sufficient contrast for accessibility."
        ),
        "weight": 0.15,
    },
    {
        "id": "VR5",
        "name": "Professional Appearance",
        "description": (
            "Overall polish and enterprise-appropriate styling. Consistent "
            "element sizing. Alignment feels intentional. Would not look "
            "out of place in a boardroom presentation."
        ),
        "weight": 0.15,
    },
]


@dataclass
class VisualCriterionScore:
    """Score for a single visual quality criterion."""

    id: str
    name: str
    score: float  # 0-10
    weight: float
    notes: str = ""


@dataclass
class CanvasVisualScore:
    """Visual quality scores for a single canvas node (slide, panel, etc.).

    Renamed from `SlideVisualScore` at v1.1 H4 M-V1-06 S1 per ADR-001 § Wave 1
    Substrate-Neutrality Ratchet (substrate names should be application-agnostic).
    Field-name neutrality (`slide_index`/`slide_title`/`slide_type` →
    `node_index`/`node_label`/`node_type`) plus the matching
    `slide_scores → node_scores` rename on `VisualReviewReport`,
    topology-aware `_estimate_hierarchy()`, and application-pluggable
    `generate_review_prompt()` landed at M-V1-06 S2.
    """

    node_index: int
    node_label: str
    node_type: str
    criteria: list[VisualCriterionScore] = field(default_factory=list)
    screenshot_path: str | None = None

    @property
    def weighted_score(self) -> float:
        """Weighted average of all criteria."""
        if not self.criteria:
            return 0.0
        total_weight = sum(c.weight for c in self.criteria)
        if total_weight <= 0:
            return 0.0
        return sum(c.score * c.weight for c in self.criteria) / total_weight

    @property
    def min_criterion(self) -> float:
        """Lowest criterion score."""
        if not self.criteria:
            return 0.0
        return min(c.score for c in self.criteria)


# Legacy alias — preserves backward compatibility for parity-script kwarg
# constructors and visual_inspector attribute access while M-V1-06 S2 cascades
# the field renames + topology-aware refactor through all consumers.
SlideVisualScore = CanvasVisualScore


@dataclass
class VisualReviewReport:
    """Aggregate visual quality report for a canvas (deck, comic, diagram, ...)."""

    title: str
    node_scores: list[CanvasVisualScore] = field(default_factory=list)
    review_method: str = "manual"  # "manual" | "playwright_gemini" | "screenshot_only"

    @property
    def aggregate_score(self) -> float:
        """Average weighted score across all nodes."""
        if not self.node_scores:
            return 0.0
        return statistics.mean(s.weighted_score for s in self.node_scores)

    @property
    def min_slide_score(self) -> float:
        """Lowest per-node score."""
        if not self.node_scores:
            return 0.0
        return min(s.weighted_score for s in self.node_scores)

    @property
    def passes(self) -> bool:
        """Whether the canvas meets the visual quality threshold (7.5/10)."""
        return self.aggregate_score >= 7.5

    @property
    def weakest_criterion(self) -> str:
        """The criterion with the lowest average score across all nodes."""
        if not self.node_scores or not self.node_scores[0].criteria:
            return "N/A"
        criterion_avgs: dict[str, list[float]] = {}
        for ss in self.node_scores:
            for c in ss.criteria:
                criterion_avgs.setdefault(c.name, []).append(c.score)
        return min(criterion_avgs, key=lambda k: statistics.mean(criterion_avgs[k]))

    def to_markdown(self) -> str:
        """Render as a markdown report.

        Output schema preserved at v1.0 (Slide / slide_index headings) for
        consumer-side backward compatibility with locked baseline JSON files
        and parity-script readers. Substrate field renames at M-V1-06 S2 are
        in-memory only; consumer-facing output schema migration is a separate
        slice.
        """
        lines = [
            f"# Visual Quality Report: {self.title}",
            "",
            f"**Aggregate Score**: {self.aggregate_score:.1f}/10 "
            f"({'PASS' if self.passes else 'NEEDS IMPROVEMENT'})",
            f"**Review Method**: {self.review_method}",
            f"**Weakest Criterion**: {self.weakest_criterion}",
            "",
            "## Per-Slide Scores",
            "",
            "| # | Slide | Type | Score | VR1 | VR2 | VR3 | VR4 | VR5 |",
            "|---|-------|------|-------|-----|-----|-----|-----|-----|",
        ]
        for ss in self.node_scores:
            criterion_scores = {c.id: c.score for c in ss.criteria}

            def _fmt(cid: str, _cs: dict[str, float] = criterion_scores) -> str:
                val = _cs.get(cid)
                return f"{val:.1f}" if val is not None else "-"

            lines.append(
                f"| {ss.node_index} | {ss.node_label[:30]} | {ss.node_type} | "
                f"{ss.weighted_score:.1f} | "
                f"{_fmt('VR1')} | "
                f"{_fmt('VR2')} | "
                f"{_fmt('VR3')} | "
                f"{_fmt('VR4')} | "
                f"{_fmt('VR5')} |"
            )
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for JSON export.

        Output schema preserved at v1.0 (`slides`/`slide_count` top-level keys
        with inner `title` per item) for consumer-side backward compatibility
        with locked baseline JSON and parity-script readers. Substrate field
        renames at M-V1-06 S2 are in-memory only; consumer-facing output
        schema migration is a separate slice.
        """
        return {
            "title": self.title,
            "aggregate_score": round(self.aggregate_score, 2),
            "passes": self.passes,
            "review_method": self.review_method,
            "weakest_criterion": self.weakest_criterion,
            "slide_count": len(self.node_scores),
            "slides": [
                {
                    "index": ss.node_index,
                    "title": ss.node_label,
                    "type": ss.node_type,
                    "weighted_score": round(ss.weighted_score, 2),
                    "criteria": [
                        {
                            "id": c.id,
                            "name": c.name,
                            "score": round(c.score, 2),
                            "notes": c.notes,
                        }
                        for c in ss.criteria
                    ],
                }
                for ss in self.node_scores
            ],
        }


# ---------------------------------------------------------------------------
# Programmatic Visual Estimation
# ---------------------------------------------------------------------------


def estimate_visual_scores(
    slides: list[dict[str, Any]],
    canvas_data: dict[str, Any] | None = None,
    *,
    hierarchy_hints: dict[str, float] | None = None,
) -> VisualReviewReport:
    """Estimate visual quality from canvas structure without rendering.

    This is a heuristic estimator that analyzes node dimensions, spacing,
    and content density to approximate visual quality. It does NOT render
    or screenshot — use the Playwright pipeline for actual visual review.

    Args:
        slides: Canvas-node metadata list (deck slides, comic pages, ...).
        canvas_data: Optional built canvas dict for node analysis.
        hierarchy_hints: Optional mapping of node-type → VR2 score, threaded
            through to `_estimate_hierarchy()`. Applications supply their own
            mapping (e.g., `{"comic_cover": 9.5}`); default deck-canonical
            hints from `DEFAULT_HIERARCHY_HINTS` apply when omitted.

    Returns:
        VisualReviewReport with estimated scores.
    """
    report = VisualReviewReport(
        title="Structural Visual Estimate",
        review_method="structural_estimate",
    )

    nodes: dict[str, dict[str, Any]] = {}
    if canvas_data:
        for node in canvas_data.get("nodes", []):
            nodes[node.get("id", "")] = node

    for i, slide in enumerate(slides):
        slide_score = CanvasVisualScore(
            node_index=i + 1,
            node_label=slide.get("title", f"Slide {i + 1}"),
            node_type=slide.get("type", "content"),
        )

        # Analyze nodes if canvas data available
        node_heights: list[int] = []
        node_widths: list[int] = []
        word_counts: list[int] = []
        total_node_area = 0.0
        slide_area = 0.0

        for nid in slide.get("node_ids", []):
            node = nodes.get(nid, {})
            h = node.get("height", 0)
            w = node.get("width", 0)
            node_heights.append(h)
            node_widths.append(w)
            total_node_area += h * w
            text = node.get("text", "")
            word_counts.append(len(text.split()))

        # Find the slide group
        group = nodes.get(slide.get("id", ""), {})
        sw = group.get("width", 1200)
        sh = group.get("height", 1100)
        slide_area = sw * sh

        # VR1: Text Readability
        vr1_score = _estimate_readability(word_counts, node_heights, node_widths)
        slide_score.criteria.append(
            VisualCriterionScore(
                id="VR1",
                name="Text Readability",
                score=vr1_score,
                weight=0.25,
            )
        )

        # VR2: Visual Hierarchy
        vr2_score = _estimate_hierarchy(slide, node_heights, hierarchy_hints)
        slide_score.criteria.append(
            VisualCriterionScore(
                id="VR2",
                name="Visual Hierarchy",
                score=vr2_score,
                weight=0.25,
            )
        )

        # VR3: Whitespace Quality
        fill_ratio = total_node_area / slide_area if slide_area > 0 else 0.5
        vr3_score = _estimate_whitespace_quality(fill_ratio, slide.get("type", "content"))
        slide_score.criteria.append(
            VisualCriterionScore(
                id="VR3",
                name="Whitespace Quality",
                score=vr3_score,
                weight=0.20,
            )
        )

        # VR4: Color Harmony (structural estimate — limited without rendering)
        vr4_score = 7.0  # Default to reasonable score; needs visual review for accuracy
        slide_score.criteria.append(
            VisualCriterionScore(
                id="VR4",
                name="Color Harmony",
                score=vr4_score,
                weight=0.15,
                notes="Structural estimate — render for accurate assessment",
            )
        )

        # VR5: Professional Appearance
        vr5_score = _estimate_professionalism(
            slide,
            node_heights,
            node_widths,
            fill_ratio,
        )
        slide_score.criteria.append(
            VisualCriterionScore(
                id="VR5",
                name="Professional Appearance",
                score=vr5_score,
                weight=0.15,
            )
        )

        report.node_scores.append(slide_score)

    return report


def _estimate_readability(
    word_counts: list[int],
    node_heights: list[int],
    node_widths: list[int],
) -> float:
    """Estimate text readability from word count vs. available space."""
    if not word_counts:
        return 8.0  # No text = no readability issues

    score = 8.0
    for words, height, width in zip(word_counts, node_heights, node_widths, strict=False):
        if height <= 0 or width <= 0:
            continue

        # Words per 100px of height (at standard width)
        density = (words / height) * 100 if height > 0 else 0

        if density > 40:
            score -= 2.0  # Very cramped
        elif density > 25:
            score -= 1.0  # Somewhat dense

        # Check width — too narrow nodes mean small text or wrapping
        if width < 200 and words > 20:
            score -= 1.0

    return max(0.0, min(10.0, score))


DEFAULT_HIERARCHY_HINTS: dict[str, float] = {
    # Deck-canonical: title and section_divider inherently have hierarchy.
    # Applications register their own hints (comic covers, topology roots, ...)
    # via the `hierarchy_hints` parameter on `estimate_visual_scores()`.
    "title": 9.0,
    "section_divider": 9.0,
}


def _estimate_hierarchy(
    slide: dict[str, Any],
    node_heights: list[int],
    hierarchy_hints: dict[str, float] | None = None,
) -> float:
    """Estimate visual hierarchy from node size differentiation.

    Application-pluggable via `hierarchy_hints` (node-type → hierarchy-score).
    When the canvas node's type matches a registered hint, that score is
    returned directly. Otherwise the function falls back to a ratio-based
    estimate over node heights. Defaults preserve deck-canonical behavior
    (title and section_divider score 9.0).
    """
    hints = hierarchy_hints if hierarchy_hints is not None else DEFAULT_HIERARCHY_HINTS
    ntype = slide.get("type", "content")

    if ntype in hints:
        return hints[ntype]

    if len(node_heights) < 2:
        return 7.0

    # Check if there's meaningful size differentiation
    if max(node_heights) > 0 and min(node_heights) > 0:
        ratio = max(node_heights) / min(node_heights)
        if ratio >= 2.0:
            return 9.0  # Strong differentiation
        if ratio >= 1.3:
            return 7.5  # Moderate differentiation
        return 6.0  # Everything same size — weak hierarchy

    return 7.0


def _estimate_whitespace_quality(
    fill_ratio: float,
    slide_type: str,
) -> float:
    """Score whitespace quality based on fill ratio and type expectations."""
    # Import here to avoid circular dependency
    from .design_tokens import get_slide_tokens

    tokens = get_slide_tokens(slide_type)
    whitespace = 1.0 - fill_ratio

    # Score based on how close to target whitespace
    target = tokens.whitespace_target
    deviation = abs(whitespace - target)

    if deviation <= 0.05:
        return 9.5  # Very close to ideal
    if deviation <= 0.10:
        return 8.0
    if deviation <= 0.15:
        return 7.0
    if deviation <= 0.25:
        return 5.0
    return 3.0  # Way off target


def _estimate_professionalism(
    slide: dict[str, Any],
    node_heights: list[int],
    node_widths: list[int],
    fill_ratio: float,
) -> float:
    """Estimate professional appearance from structural regularity."""
    score = 7.0

    # Consistent node widths suggest intentional design
    if len(node_widths) >= 2:
        width_cv = (
            statistics.stdev(node_widths) / statistics.mean(node_widths)
            if statistics.mean(node_widths) > 0
            else 0
        )
        if width_cv < 0.1:
            score += 1.5  # Very consistent
        elif width_cv < 0.3:
            score += 0.5  # Somewhat consistent
        else:
            score -= 0.5  # Inconsistent sizes

    # Fill ratio in the golden zone
    if 0.35 <= fill_ratio <= 0.65:
        score += 1.0
    elif fill_ratio > 0.80 or fill_ratio < 0.15:
        score -= 1.5

    return max(0.0, min(10.0, score))


# ---------------------------------------------------------------------------
# Screenshot Pipeline Scaffolding
# ---------------------------------------------------------------------------


def generate_review_prompt(
    node_label: str,
    node_type: str,
    *,
    domain_noun: str = "presentation slide",
    item_label: str = "Slide",
) -> str:
    """Generate the prompt for LLM-based visual review of a canvas-node screenshot.

    This prompt is designed for use with Gemini's describe_image MCP tool.
    The caller captures a screenshot and sends it with this prompt.

    Args:
        node_label: Human-readable label for the canvas node being reviewed.
        node_type: Node type (content, title, panel, page, ...).
        domain_noun: Application-specific noun for the artifact under review
            ("presentation slide", "comic panel", "topology diagram", ...).
            Default preserves deck-canonical language.
        item_label: Per-item label rendered before the node label in the
            prompt body ("Slide", "Panel", "Page", "Node", ...).

    Returns:
        Prompt string for visual quality assessment.
    """
    criteria_text = "\n".join(
        f"- **{c['name']}** (weight {c['weight']:.0%}): {c['description']}" for c in VISUAL_CRITERIA
    )

    return f"""Evaluate this {domain_noun} for visual quality.

**{item_label}**: "{node_label}" (type: {node_type})

Score each criterion from 0-10:

{criteria_text}

Respond in this exact JSON format:
{{
  "VR1": {{"score": <0-10>, "notes": "<brief observation>"}},
  "VR2": {{"score": <0-10>, "notes": "<brief observation>"}},
  "VR3": {{"score": <0-10>, "notes": "<brief observation>"}},
  "VR4": {{"score": <0-10>, "notes": "<brief observation>"}},
  "VR5": {{"score": <0-10>, "notes": "<brief observation>"}}
}}

Be specific about what works and what doesn't. Score honestly —
a generic AI-generated {domain_noun} should score 5-6, not 8-9."""


def parse_visual_review_response(
    response: str,
    node_index: int,
    node_label: str,
    node_type: str,
) -> CanvasVisualScore:
    """Parse an LLM visual review response into a CanvasVisualScore.

    Args:
        response: JSON string from the LLM review.
        node_index: 1-based canvas-node index.
        node_label: Human-readable label for the canvas node.
        node_type: Node type (content, title, panel, page, ...).

    Returns:
        CanvasVisualScore with parsed criteria scores.
    """
    slide_score = CanvasVisualScore(
        node_index=node_index,
        node_label=node_label,
        node_type=node_type,
    )

    try:
        # Extract JSON from response (may be wrapped in markdown code blocks)
        json_match = response
        if "```" in response:
            import re

            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response, re.DOTALL)
            if match:
                json_match = match.group(1)

        data = json.loads(json_match)

        criteria_map = {c["id"]: c for c in VISUAL_CRITERIA}
        for cid, info in data.items():
            if cid in criteria_map:
                crit = criteria_map[cid]
                score_val = float(info.get("score", 5.0))
                notes = info.get("notes", "")
                slide_score.criteria.append(
                    VisualCriterionScore(
                        id=cid,
                        name=crit["name"],
                        score=max(0.0, min(10.0, score_val)),
                        weight=crit["weight"],
                        notes=notes,
                    )
                )
    except (json.JSONDecodeError, ValueError, KeyError, AttributeError):
        # Fallback: use structural estimate scores
        for crit in VISUAL_CRITERIA:
            slide_score.criteria.append(
                VisualCriterionScore(
                    id=crit["id"],
                    name=crit["name"],
                    score=5.0,
                    weight=crit["weight"],
                    notes="Failed to parse LLM response — using default score",
                )
            )

    return slide_score
