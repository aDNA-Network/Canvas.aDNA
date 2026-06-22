"""Golden-ratio and compositional geometry helpers.

Pure-math functions with zero canvas/slide/panel assumptions. Consumed by
deck layout (SlideLayout), comic panel composition, and any future canvas
application needing proportional subdivision.

Extracted from lattice-protocol/extensions/canvas/canvas_layout.py lines 14-75
(M-1-02) per ADR 001 § canvas_layout.py Geometry Extraction. The deck-bound
residue (SlideLayout, LayoutStrategy, NodePlacement) migrates to
canvas_presentation/layout.py in Wave 2 (M-2a).

M-1-06: resolve_viewport() added for aspect-ratio-respecting render paths.
"""

from __future__ import annotations

import logging
from typing import Any

_log = logging.getLogger(__name__)

PHI = 1.618033988749895

# 16:9 fallback when a canvas group declares no dimensions.
# Explicit constant — not silently baked into render paths.
_DEFAULT_VIEWPORT = (1920, 1080)


def resolve_viewport(canvas_group: dict[str, Any]) -> tuple[int, int]:
    """Extract viewport dimensions from a canvas group's declared size.

    Returns (width, height) from the group's ``width`` and ``height`` keys.
    Falls back to 16:9 1920x1080 with a logged warning if dimensions are
    missing or zero. The fallback is explicit — applications that need a
    specific aspect (comic vertical, diagram square) must declare dimensions
    on their canvas groups.

    Args:
        canvas_group: A canvas group node dict (must have ``id``).

    Returns:
        (width, height) in canvas units.
    """
    w = canvas_group.get("width", 0)
    h = canvas_group.get("height", 0)
    if w > 0 and h > 0:
        return (int(w), int(h))
    gid = canvas_group.get("id", "<unknown>")
    _log.warning(
        "Canvas group %s declares no dimensions (width=%s, height=%s); "
        "falling back to %dx%d",
        gid, w, h, *_DEFAULT_VIEWPORT,
    )
    return _DEFAULT_VIEWPORT


def golden_split(total: float, *, major_first: bool = True) -> tuple[float, float]:
    """Split ``total`` into two segments at the golden ratio.

    Args:
        total: Length to split.
        major_first: If True, first segment is the larger one.

    Returns:
        (major, minor) or (minor, major) depending on ``major_first``.
    """
    major = total / PHI
    minor = total - major
    if major_first:
        return major, minor
    return minor, major


def golden_rect(width: float, height: float) -> tuple[float, float, float, float]:
    """Subdivide a rectangle via golden ratio on the width axis.

    Returns (x1, w1, x2, w2) for left and right sub-rects.
    """
    w1, w2 = golden_split(width)
    return 0.0, w1, w1, w2


def thirds_points(total: float) -> tuple[float, float]:
    """Return the two rule-of-thirds positions along ``total``."""
    return total / 3, total * 2 / 3


def fibonacci_spacing(count: int, total: float) -> list[float]:
    """Distribute ``count`` items across ``total`` using Fibonacci-weighted spacing.

    Returns a list of center positions.
    """
    if count <= 0:
        return []
    if count == 1:
        return [total / 2]

    # Generate fibonacci weights
    fibs = [1, 1]
    while len(fibs) < count + 1:
        fibs.append(fibs[-1] + fibs[-2])
    weights = fibs[1 : count + 1]
    total_weight = sum(weights)

    # Compute cumulative positions
    positions: list[float] = []
    cumulative = 0.0
    for w in weights:
        segment = total * w / total_weight
        positions.append(cumulative + segment / 2)
        cumulative += segment
    return positions
