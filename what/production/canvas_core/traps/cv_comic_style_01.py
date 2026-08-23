"""CV-COMIC-STYLE-01 — Comic style-lock drift (character/palette/rendering inconsistency).

Implemented + calibrated at the Halftone H6 re-open (2026-08-22) against the H3
first-light corpus (``what/artifacts/h3_first_light/``, 27 panels, eye-gate
PASSED 2026-08-13) — the corpus the scaffold was deliberately waiting for
(``canvas_authoring_guidance.md``: "it needs H3's real renders").

Mechanism (v0, deliberately simple and explainable):
    Each panel image is reduced to a normalized 4x4x4 RGB histogram (64 bins) on
    a 64x64 thumbnail. The run's *style centroid* is the mean histogram across
    all panels; each panel's drift score is the chi-square distance to that
    centroid. A panel drifts when its score exceeds ``DRIFT_THRESHOLD``.

Calibration provenance:
    The 27 H3 panels — a corpus a human eye-gate judged style-consistent —
    define the "consistent" distribution. Their max intra-run chi-square
    distance to leave-one-out centroid measured 0.987 (mean 0.408, min 0.190) on 2026-08-22
    (calibration record: campaign_canvas_halftone/missions/artifacts/
    cv_comic_style_01_calibration.md). The threshold is set at 1.20 —
    ~1.2x the observed consistent max, and below the 1.482 a synthetic
    grayscale break of an H3 panel scores — so the trap stays silent on a
    corpus of H3's measured diversity and fires on gross palette/rendering
    breaks (a grayscale panel in a color run, a photoreal panel in a
    flat-color run). Threshold tightening is expected as more eye-gated
    corpora accumulate (cycles_fired discipline).

Scope guards:
    - Needs ``asset_root`` (same kwarg CV-IMAGE-ASPECT-RATIO-01 uses) to
      resolve file nodes; returns [] without it.
    - Needs >= MIN_PANELS resolvable raster images; drift against a centroid
      of one or two panels is statistically meaningless.
    - Pixel comparison only — it cannot judge character *identity* drift
      (that stays with the human eye-gate / R3).
"""

from __future__ import annotations

import os
from typing import Any

from . import TrapFinding

try:  # Pillow is a canvas_core production dependency (print/compose already use it)
    from PIL import Image
except ImportError:  # pragma: no cover - environment guard
    Image = None  # type: ignore[assignment]

RASTER_EXTS = (".png", ".jpg", ".jpeg", ".webp")
THUMB_SIZE = 64
BINS_PER_CHANNEL = 4
MIN_PANELS = 3
# Calibrated on the H3 first-light corpus (27 panels, eye-gate PASSED):
# max leave-one-out chi-square distance to centroid = 0.987, mean = 0.408.
DRIFT_THRESHOLD = 1.20


def _histogram_signature(path: str) -> list[float] | None:
    """Normalized 4x4x4 RGB histogram of a 64x64 thumbnail, or None if unreadable."""
    if Image is None:
        return None
    try:
        with Image.open(path) as im:
            im = im.convert("RGB").resize((THUMB_SIZE, THUMB_SIZE))
            pixels = list(im.getdata())
    except OSError:
        return None
    bins = [0.0] * (BINS_PER_CHANNEL ** 3)
    shift = 256 // BINS_PER_CHANNEL
    for r, g, b in pixels:
        idx = (r // shift) * BINS_PER_CHANNEL * BINS_PER_CHANNEL + (g // shift) * BINS_PER_CHANNEL + (b // shift)
        bins[idx] += 1.0
    total = float(len(pixels))
    return [v / total for v in bins]


def _chi_square(h1: list[float], h2: list[float]) -> float:
    """Symmetric chi-square distance between two normalized histograms."""
    acc = 0.0
    for a, b in zip(h1, h2):
        denom = a + b
        if denom > 0.0:
            diff = a - b
            acc += (diff * diff) / denom
    return acc


def check(
    canvas_data: dict[str, Any],
    *,
    r11_node_ids: set[str] | None = None,
    asset_root: str | os.PathLike | None = None,
) -> list[TrapFinding]:
    """Run CV-COMIC-STYLE-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating (severity +1
            conceptually; this trap's default is already ``high``).
        asset_root: Directory for resolving file-node image paths. **Required**
            — the trap returns ``[]`` (skips) when absent.

    Returns:
        List of :class:`TrapFinding`, one per drifting panel (may be empty).
    """
    if asset_root is None or Image is None:
        return []
    root = os.fspath(asset_root)

    panels: list[tuple[str, list[float]]] = []  # (node_id, signature)
    for node in canvas_data.get("nodes", []):
        if node.get("type") != "file":
            continue
        file_ref = node.get("file", "")
        if not file_ref or not file_ref.lower().endswith(RASTER_EXTS):
            continue
        path = file_ref if os.path.isabs(file_ref) else os.path.join(root, file_ref)
        sig = _histogram_signature(path)
        if sig is not None:
            panels.append((node.get("id", "unknown"), sig))

    if len(panels) < MIN_PANELS:
        return []

    n = len(panels)
    dims = len(panels[0][1])
    totals = [sum(sig[i] for _, sig in panels) for i in range(dims)]

    findings: list[TrapFinding] = []
    for node_id, sig in panels:
        # Leave-one-out centroid: a drifting panel must not dilute the very
        # baseline it is judged against (at small n a gross outlier would
        # otherwise pull the centroid toward itself and dampen its own score).
        centroid = [(totals[i] - sig[i]) / (n - 1) for i in range(dims)]
        score = _chi_square(sig, centroid)
        if score > DRIFT_THRESHOLD:
            findings.append(TrapFinding(
                trap_id="CV-COMIC-STYLE-01",
                condition="style_lock_drift",
                node_ids=[node_id],
                severity="high",
                message=(
                    f"Panel {node_id} drifts from the run's style centroid "
                    f"(chi-square {score:.3f} > threshold {DRIFT_THRESHOLD}; "
                    f"H3-calibrated consistent max 0.987). Palette/rendering "
                    f"inconsistency — re-render or justify."
                ),
            ))
    return findings
