"""Visual inspection pipeline for canvas presentations.

Orchestrates the full visual inspection loop:
  1. Render canvas JSON → HTML slides (via html_renderer)
  2. Screenshot HTML slides via Playwright MCP or local HTTP server
  3. Score screenshots via visual review criteria (VR1-VR5)
  4. Generate comparison reports for iterative improvement

This module provides the orchestration layer. The actual Playwright
calls and LLM-based visual analysis happen at the agent level (the
agent calls MCP tools). This module prepares inputs and processes outputs.

Migrated from lattice-protocol/extensions/canvas/canvas_visual_inspector.py
(M-1-03). Per ADR 001 § Borderline Files: substrate, but deck-wired through
Wave 1; pluggable-renderer decouple deferred to post-Wave-1 sprint. Imports
of html_renderer and visual_review are now intra-package (both in canvas_core).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from typing import Any

from .html_renderer import (
    render_presentation,
)
from .visual_review import (
    CanvasVisualScore,
    VisualCriterionScore,
    VisualReviewReport,
    generate_review_prompt,
    parse_visual_review_response,
)

# ---------------------------------------------------------------------------
# Screenshot Orchestration
# ---------------------------------------------------------------------------


@dataclass
class ScreenshotResult:
    """Result of screenshotting a single slide."""

    slide_index: int
    slide_title: str
    slide_type: str
    html_path: Path
    screenshot_path: Path | None = None
    error: str | None = None


@dataclass
class ScreenshotBatch:
    """Results of screenshotting an entire presentation."""

    title: str
    output_dir: Path
    slides: list[ScreenshotResult] = field(default_factory=list)

    @property
    def success_count(self) -> int:
        return sum(1 for s in self.slides if s.screenshot_path is not None)

    @property
    def screenshot_paths(self) -> list[Path]:
        return [s.screenshot_path for s in self.slides if s.screenshot_path]


def prepare_screenshots(
    canvas_path: str | Path,
    output_dir: str | Path,
    *,
    theme_name: str | None = None,
) -> ScreenshotBatch:
    """Render HTML slides and prepare for Playwright screenshots.

    This function renders all slides as HTML and returns a ScreenshotBatch
    with html_path set for each slide. The agent then uses Playwright MCP
    to take screenshots of each HTML file.

    Args:
        canvas_path: Path to .canvas file.
        output_dir: Directory for HTML and screenshots.
        theme_name: Optional theme override.

    Returns:
        ScreenshotBatch ready for the agent to screenshot.
    """
    canvas_path = Path(canvas_path)
    output_dir = Path(output_dir)

    html_dir = output_dir / "html"
    screenshots_dir = output_dir / "screenshots"
    html_dir.mkdir(parents=True, exist_ok=True)
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    rendered = render_presentation(
        canvas_path,
        html_dir,
        theme_name=theme_name,
    )

    batch = ScreenshotBatch(
        title=rendered.title,
        output_dir=output_dir,
    )

    for slide in rendered.slides:
        html_path = html_dir / slide.filename
        screenshot_name = slide.filename.replace(".html", ".png")

        batch.slides.append(
            ScreenshotResult(
                slide_index=slide.index,
                slide_title=slide.title,
                slide_type=slide.slide_type,
                html_path=html_path,
                screenshot_path=screenshots_dir / screenshot_name,
            )
        )

    return batch


def serve_slides(html_dir: str | Path, port: int = 8765) -> HTTPServer:
    """Start a local HTTP server for Playwright to access HTML slides.

    Returns the HTTPServer instance. Call server.shutdown() when done.

    Args:
        html_dir: Directory containing HTML slide files.
        port: Port to serve on.

    Returns:
        Running HTTPServer instance (in a daemon thread).
    """
    html_dir = Path(html_dir).resolve()

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(html_dir), **kwargs)

        def log_message(self, format: str, *args: Any) -> None:
            pass  # Suppress logging

    server = HTTPServer(("127.0.0.1", port), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def slide_urls(batch: ScreenshotBatch, port: int = 8765) -> list[dict[str, Any]]:
    """Generate Playwright-compatible URLs for each slide.

    Returns a list of dicts with: index, title, type, url, screenshot_path.
    """
    results: list[dict[str, Any]] = []
    for slide in batch.slides:
        filename = slide.html_path.name
        results.append(
            {
                "index": slide.slide_index,
                "title": slide.slide_title,
                "type": slide.slide_type,
                "url": f"http://127.0.0.1:{port}/{filename}",
                "screenshot_path": str(slide.screenshot_path),
            }
        )
    return results


# ---------------------------------------------------------------------------
# Visual Analysis Integration
# ---------------------------------------------------------------------------


def visual_inspect(
    canvas_path: str | Path,
    output_dir: str | Path,
    *,
    theme_name: str | None = None,
) -> dict[str, Any]:
    """Prepare a full visual inspection package for agent execution.

    This returns everything the agent needs to:
    1. Serve the HTML slides
    2. Screenshot each slide via Playwright
    3. Read each screenshot and score VR1-VR5
    4. Write the review report

    Args:
        canvas_path: Path to .canvas file.
        output_dir: Directory for all outputs.
        theme_name: Optional theme override.

    Returns:
        Dict with batch info, slide URLs, review prompts, and output paths.
    """
    batch = prepare_screenshots(
        canvas_path,
        output_dir,
        theme_name=theme_name,
    )

    # Generate review prompts for each slide
    prompts: list[dict[str, str]] = []
    for slide in batch.slides:
        prompt = generate_review_prompt(slide.slide_title, slide.slide_type)
        prompts.append(
            {
                "slide_index": str(slide.slide_index),
                "slide_title": slide.slide_title,
                "slide_type": slide.slide_type,
                "prompt": prompt,
            }
        )

    report_path = Path(output_dir) / f"{batch.title}_visual_review.md"
    json_path = Path(output_dir) / f"{batch.title}_visual_review.json"

    return {
        "title": batch.title,
        "slide_count": len(batch.slides),
        "html_dir": str(batch.output_dir / "html"),
        "screenshots_dir": str(batch.output_dir / "screenshots"),
        "slides": [
            {
                "index": s.slide_index,
                "title": s.slide_title,
                "type": s.slide_type,
                "html_path": str(s.html_path),
                "screenshot_path": str(s.screenshot_path),
            }
            for s in batch.slides
        ],
        "prompts": prompts,
        "report_path": str(report_path),
        "json_path": str(json_path),
    }


def build_review_report(
    title: str,
    slide_scores: list[dict[str, Any]],
    screenshot_dir: str | Path | None = None,
) -> VisualReviewReport:
    """Build a VisualReviewReport from agent-collected scores.

    The agent scores each slide (via multimodal Read or Gemini describe_image)
    and passes the results here for aggregation.

    Args:
        title: Presentation title.
        slide_scores: List of dicts, each with:
            - slide_index: int
            - slide_title: str
            - slide_type: str
            - scores: dict of VR1-VR5 with score and notes
            - screenshot_path: optional path
        screenshot_dir: Optional path to screenshots for report linking.

    Returns:
        VisualReviewReport with all slides scored.
    """
    report = VisualReviewReport(
        title=title,
        review_method="playwright_visual",
    )

    for entry in slide_scores:
        # Try parsing as LLM JSON response
        scores = entry.get("scores", {})
        if isinstance(scores, str):
            slide_score = parse_visual_review_response(
                scores,
                entry.get("slide_index", 0),
                entry.get("slide_title", ""),
                entry.get("slide_type", "content"),
            )
        else:
            slide_score = CanvasVisualScore(
                node_index=entry.get("slide_index", 0),
                node_label=entry.get("slide_title", ""),
                node_type=entry.get("slide_type", "content"),
                screenshot_path=entry.get("screenshot_path"),
            )
            for cid, info in scores.items():
                if cid.startswith("VR"):
                    slide_score.criteria.append(
                        VisualCriterionScore(
                            id=cid,
                            name=info.get("name", cid),
                            score=max(0.0, min(10.0, float(info.get("score", 5.0)))),
                            weight=_criterion_weight(cid),
                            notes=info.get("notes", ""),
                        )
                    )

        report.node_scores.append(slide_score)

    return report


def save_review_report(
    report: VisualReviewReport,
    output_dir: str | Path,
    title: str | None = None,
) -> tuple[Path, Path]:
    """Save review report as markdown and JSON.

    Returns (markdown_path, json_path).
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    name = title or report.title
    safe_name = name.replace(" ", "_").lower()

    md_path = output_dir / f"{safe_name}_visual_review.md"
    json_path = output_dir / f"{safe_name}_visual_review.json"

    md_path.write_text(report.to_markdown(), encoding="utf-8")
    json_path.write_text(
        json.dumps(report.to_dict(), indent=2),
        encoding="utf-8",
    )

    return md_path, json_path


def compare_reviews(
    before: VisualReviewReport,
    after: VisualReviewReport,
) -> dict[str, Any]:
    """Compare two visual review reports (before/after improvement).

    Returns a summary of score changes per slide and per criterion.
    """
    before_scores: dict[int, CanvasVisualScore] = {s.node_index: s for s in before.node_scores}
    after_scores: dict[int, CanvasVisualScore] = {s.node_index: s for s in after.node_scores}

    slide_deltas: list[dict[str, Any]] = []
    for idx in sorted(set(before_scores) | set(after_scores)):
        b = before_scores.get(idx)
        a = after_scores.get(idx)

        delta: dict[str, Any] = {
            "slide_index": idx,
            "title": (a or b).node_label if (a or b) else f"Slide {idx}",
        }

        if b and a:
            delta["before"] = round(b.weighted_score, 2)
            delta["after"] = round(a.weighted_score, 2)
            delta["change"] = round(a.weighted_score - b.weighted_score, 2)

            # Per-criterion deltas
            b_crit = {c.id: c.score for c in b.criteria}
            a_crit = {c.id: c.score for c in a.criteria}
            criterion_deltas: dict[str, float] = {}
            for cid in set(b_crit) | set(a_crit):
                bs = b_crit.get(cid, 0)
                as_ = a_crit.get(cid, 0)
                criterion_deltas[cid] = round(as_ - bs, 2)
            delta["criteria"] = criterion_deltas
        elif a:
            delta["before"] = None
            delta["after"] = round(a.weighted_score, 2)
            delta["change"] = None
        else:
            delta["before"] = round(b.weighted_score, 2) if b else None
            delta["after"] = None
            delta["change"] = None

        slide_deltas.append(delta)

    return {
        "before_aggregate": round(before.aggregate_score, 2),
        "after_aggregate": round(after.aggregate_score, 2),
        "aggregate_change": round(after.aggregate_score - before.aggregate_score, 2),
        "before_passes": before.passes,
        "after_passes": after.passes,
        "slides": slide_deltas,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_CRITERION_WEIGHTS: dict[str, float] = {
    "VR1": 0.25,
    "VR2": 0.25,
    "VR3": 0.20,
    "VR4": 0.15,
    "VR5": 0.15,
}


def _criterion_weight(cid: str) -> float:
    """Look up criterion weight by ID."""
    return _CRITERION_WEIGHTS.get(cid, 0.20)


# ---------------------------------------------------------------------------
# Automated VR Scoring (via Gemini describe_image MCP)
# ---------------------------------------------------------------------------


def automated_vr_score(
    screenshot_path: str | Path,
    slide_title: str = "",
    slide_type: str = "content",
) -> dict[str, Any]:
    """Prepare an automated VR scoring request for a single slide.

    Returns a dict with the screenshot path and VR prompt, ready for the
    agent to pass to Gemini's describe_image MCP tool.

    Args:
        screenshot_path: Path to screenshot PNG.
        slide_title: Title of the slide.
        slide_type: Type of the slide.

    Returns:
        Dict with: screenshot_path, prompt, slide_title, slide_type.
    """
    prompt = generate_review_prompt(slide_title, slide_type)
    return {
        "screenshot_path": str(screenshot_path),
        "prompt": prompt,
        "slide_title": slide_title,
        "slide_type": slide_type,
    }


def batch_score(
    batch: ScreenshotBatch,
) -> list[dict[str, Any]]:
    """Prepare automated VR scoring requests for an entire batch.

    Returns a list of scoring request dicts, one per slide with a
    screenshot. The agent iterates these and calls describe_image
    for each, then passes results to build_review_report().

    Args:
        batch: ScreenshotBatch with screenshot paths set.

    Returns:
        List of scoring request dicts.
    """
    requests: list[dict[str, Any]] = []
    for slide in batch.slides:
        if slide.screenshot_path and slide.screenshot_path.exists():
            req = automated_vr_score(
                slide.screenshot_path,
                slide_title=slide.slide_title,
                slide_type=slide.slide_type,
            )
            req["slide_index"] = slide.slide_index
            requests.append(req)
    return requests


def build_automated_report(
    title: str,
    scored_responses: list[dict[str, Any]],
) -> VisualReviewReport:
    """Build a review report from automated (Gemini) scoring responses.

    Each entry in scored_responses should have:
        - slide_index: int
        - slide_title: str
        - slide_type: str
        - response: str (JSON from Gemini describe_image)
        - screenshot_path: optional str

    Args:
        title: Presentation title.
        scored_responses: List of response dicts from automated scoring.

    Returns:
        VisualReviewReport with review_method="gemini_automated".
    """
    report = VisualReviewReport(
        title=title,
        review_method="gemini_automated",
    )

    for entry in scored_responses:
        response = entry.get("response", "")
        slide_score = parse_visual_review_response(
            response,
            entry.get("slide_index", 0),
            entry.get("slide_title", ""),
            entry.get("slide_type", "content"),
        )
        slide_score.screenshot_path = entry.get("screenshot_path")
        report.node_scores.append(slide_score)

    return report


def multi_theme_render(
    canvas_path: str | Path,
    output_dir: str | Path,
    theme_names: list[str] | None = None,
) -> dict[str, ScreenshotBatch]:
    """Render a presentation in multiple themes for cross-theme comparison.

    Args:
        canvas_path: Path to .canvas file.
        output_dir: Base output directory.
        theme_names: List of theme names. Defaults to all 7 themes.

    Returns:
        Dict mapping theme_name → ScreenshotBatch.
    """
    from .html_renderer import THEMES

    if theme_names is None:
        theme_names = list(THEMES.keys())

    output_dir = Path(output_dir)
    results: dict[str, ScreenshotBatch] = {}

    for name in theme_names:
        theme_dir = output_dir / name
        batch = prepare_screenshots(
            canvas_path,
            theme_dir,
            theme_name=name,
        )
        results[name] = batch

    return results
