#!/usr/bin/env python3
"""MVP Deck Demo — M-5-03

First end-to-end canvas artifact produced by CanvasForge.

Charter spec:
  - 5 slides, investor brief format
  - R1 (Research Host) + R7 (Delivery Engineer) voice registers
  - VR ≥ 8.0 aggregate, no slide < 7.5
  - ≤ $0.40 cost, ≤ 40K tokens, ≤ 60s/run

Usage:
    python mvp_deck_demo.py
"""

import json
import sys
import time
from pathlib import Path

# Add canvas packages to path
CODE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_ROOT))

from canvas_presentation import PresentationBuilder
from canvas_core import render_presentation, run_all_traps

# Output paths
ARTIFACT_DIR = CODE_ROOT.parent / "artifacts" / "mvp_deck"
CANVAS_PATH = ARTIFACT_DIR / "investor_brief.canvas"
HTML_DIR = ARTIFACT_DIR / "html"


def build_investor_brief() -> PresentationBuilder:
    """Build a 5-slide investor brief using PresentationBuilder."""
    pb = PresentationBuilder(
        name="canvasforge_investor_brief",
        version="1.0.0",
        presentation_type="pitch",
        audience="pitch",
        theme="lattice_brand",
        arc="problem_solution",
        density_profile="balanced",
    )

    # Slide 1: Title
    pb.add_title_slide(
        title="CanvasForge Delivers AI-Generated Visual Artifacts",
        subtitle="From intent to scored, navigable Obsidian Canvas — automatically",
    )

    # Slide 2: Problem (specific action-verb title)
    pb.add_content_slide(
        title="Manual Canvas Creation Wastes Engineering Hours",
        body=(
            "Teams create visual artifacts manually — slide decks, comic pages, "
            "diagrams — spending hours on layout and formatting instead of content. "
            "Existing tools generate static outputs with no quality feedback loop. "
            "Canvas artifacts lack scoring, review, and iterative improvement."
        ),
    )

    # Slide 3: Solution (specific action-verb title)
    pb.add_content_slide(
        title="CanvasForge Automates Generation With Built-In Quality Scoring",
        body=(
            "CanvasForge treats Obsidian Canvas JSON as a first-class data primitive. "
            "The forge generates scored, navigable canvas artifacts from structured briefs. "
            "A 24-criterion review pipeline scores every artifact before delivery. "
            "Consumer vaults federate via lightweight wrappers — no code duplication."
        ),
    )

    # Slide 4: Evidence (quantitative proof)
    pb.add_stats_slide(
        title="Proven Parity With Production Baselines",
        stats=[
            ("Deck Parity", "VR 8.74 (Wilhelm baseline)"),
            ("Comic Parity", "VR 8.4 (Issue 01 baseline)"),
            ("Substrate Modules", "17 extracted + tested"),
            ("Consumer Wrappers", "3 federated (SS deck, SS comic, CC deck)"),
            ("Test Coverage", "86+ tests, 3-way ratchet green"),
        ],
    )

    # Slide 5: Call to Action (specific ask)
    pb.add_content_slide(
        title="Deploy v1.0 and Begin Brand-Transfer Pipeline",
        body=(
            "Phase 6: Regenerate both parity references through the forge path. "
            "Phase 7: Clean up lattice-labs originals with stub-redirect strategy. "
            "Post-v1.0: Wire ComfyForge style-transfer for ownable brand LoRAs. "
            "The substrate is proven. The courier is ready."
        ),
        role="critical",
    )

    return pb


def run_demo():
    """Execute the full MVP deck demo pipeline."""
    print("=" * 60)
    print("M-5-03: MVP Deck Demo — CanvasForge Investor Brief")
    print("=" * 60)

    start = time.time()

    # 1. Build
    print("\n[1/5] Building presentation...")
    pb = build_investor_brief()
    canvas_json = pb.build()
    slide_count = len(pb.slides)
    print(f"  Built {slide_count} slides")

    # 2. Internal review (24-criterion scoring)
    print("\n[2/5] Running internal review (24 criteria, 5 categories)...")
    report = pb.review()
    print(f"  Score: {report.score:.3f} (Grade: {report.grade})")
    print(f"  Passed: {report.passed}")
    if report.issues:
        print(f"  Issues: {len(report.issues)}")
        for issue in report.issues[:5]:
            print(f"    - {issue}")
    if report.suggestions:
        print(f"  Suggestions: {len(report.suggestions)}")
        for sug in report.suggestions[:3]:
            print(f"    - {sug}")

    # Per-category breakdown
    print("\n  Category breakdown:")
    for cat_name, cat_score in report.categories.items():
        score = cat_score.weighted_score
        passed = cat_score.passed
        total = cat_score.total
        print(f"    {cat_name:15s}: {score:.3f} ({passed}/{total} criteria pass)")

    # 3. Save canvas
    print("\n[3/5] Saving canvas artifact...")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = pb.save(str(CANVAS_PATH))
    file_size = CANVAS_PATH.stat().st_size
    print(f"  Saved: {output_path} ({file_size:,} bytes)")

    # 4. III trap check
    print("\n[4/5] Running III trap check...")
    trap_findings = run_all_traps(canvas_json)
    critical = [f for f in trap_findings if f.severity == "critical"]
    print(f"  Findings: {len(trap_findings)} total, {len(critical)} critical")
    for finding in trap_findings:
        print(f"    [{finding.severity}] {finding.trap_id}: {finding.message[:80]}")

    # 5. Render HTML
    print("\n[5/5] Rendering HTML slides...")
    try:
        HTML_DIR.mkdir(parents=True, exist_ok=True)
        rendered = render_presentation(
            canvas_path=str(CANVAS_PATH),
            output_dir=str(HTML_DIR),
            theme_name="lattice_brand",
        )
        print(f"  Rendered {len(rendered.slides)} slide HTML files to {HTML_DIR}")
    except Exception as e:
        print(f"  HTML render skipped: {e}")

    # Summary
    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print("MVP DECK DEMO RESULTS")
    print("=" * 60)
    print(f"  Slides:          {slide_count} (target: 5)")
    print(f"  Internal score:  {report.score:.3f} / 1.0 (grade: {report.grade})")
    print(f"  Critical traps:  {len(critical)} (target: 0)")
    print(f"  Canvas saved:    {CANVAS_PATH}")
    print(f"  Elapsed:         {elapsed:.1f}s (target: ≤60s)")
    print()

    # Gate check
    gates_passed = True
    if slide_count != 5:
        print(f"  FAIL: Slide count {slide_count} != 5")
        gates_passed = False
    if len(critical) > 0:
        print(f"  FAIL: {len(critical)} critical trap findings")
        gates_passed = False
    if elapsed > 60:
        print(f"  FAIL: Elapsed {elapsed:.1f}s > 60s")
        gates_passed = False

    if gates_passed:
        print("  ALL STRUCTURAL GATES PASSED")
    else:
        print("  SOME GATES FAILED — see above")

    print(f"\n  Note: VR1-VR5 visual scoring (Gemini vision on screenshots)")
    print(f"  requires separate invocation of the visual review pipeline.")

    return report


if __name__ == "__main__":
    run_demo()
