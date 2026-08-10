"""Geometry-derived aspect ratios — the 2026-08-04 operator ruling (H2 finding #1).

**The problem this exists for.** A panel carries *two* statements about its own shape: the
``qualities.aspect_ratio`` the author declared, and the width/height the author actually drew. On
the mini-issue they disagree, badly and silently. The splash declares ``3:4`` (0.750) and is drawn
663x1025 (**0.647**); the wide establishing panels declare ``16:9`` (1.778) and are drawn 638x326
(**1.957**). Rendering to the declared ratio and compositing into the drawn box is what produced
the ~10-14% cover-crop that ``CV-IMAGE-ASPECT-RATIO-01`` caught on the H2 render.

**The ruling.** Geometry wins. Plan computes each panel's true ratio from node geometry and snaps
it to the nearest ratio the *generate backend actually supports*; the manifest records the declared
value (untouched), the effective value, and the residual error.

**What this does NOT do — read before trusting it.** Snapping *reduces* drift; it cannot remove it.
Image backends expose a small discrete menu of ratios (Imagen: 1:1, 3:4, 4:3, 9:16, 16:9) and panel
geometry is continuous. The splash's nearest supported ratio is ``9:16`` (0.5625) against a true
0.647 — still ~14% off, and still cropped at compose time. The deliverable here is that the
residual is **chosen, bounded and recorded** instead of accidental and invisible. The trap remains
the instrument that measures what is left.

Errors are measured in **log space** (``|ln(true / candidate)|``) because aspect ratios are scale
quantities: 2.0-vs-1.0 and 1.0-vs-0.5 are the same amount of wrong, and a linear difference says
otherwise.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

# Conservative menu used when a backend declares none of its own. These five are the intersection
# offered by the mainstream cloud image APIs; a backend that supports more should say so via its
# own ``SUPPORTED_ASPECTS`` rather than widening this.
DEFAULT_SUPPORTED: tuple[str, ...] = ("1:1", "3:4", "4:3", "9:16", "16:9")

# Above this residual, plan() calls the panel out by name instead of snapping quietly. ~0.08 in
# log space is ~8% linear, which is roughly where crop on a printed panel stops being deniable —
# a figure's head leaves the frame. On the mini-issue this reports the splash (0.140) and the two
# wide establishing panels (0.096, whose DECLARED label is correct and whose drawn box is not) and
# stays quiet for the six near-square panels (0.038). Tune it by what a reader would notice, not
# by what makes the output short.
SNAP_WARN_THRESHOLD = 0.08


def parse_ratio(spec: str | None) -> float | None:
    """``"16:9"`` -> 1.777…  Returns None for anything unparseable (never raises on author input)."""
    if not spec or ":" not in spec:
        return None
    w_part, _, h_part = spec.partition(":")
    try:
        w, h = float(w_part), float(h_part)
    except ValueError:
        return None
    if w <= 0 or h <= 0:
        return None
    return w / h


def ratio_error(a: float, b: float) -> float:
    """Scale-symmetric distance between two ratios: ``|ln(a/b)|``."""
    return abs(math.log(a / b))


def snap(true_ratio: float, supported: Sequence[str] = DEFAULT_SUPPORTED) -> tuple[str, float]:
    """Nearest supported ratio to ``true_ratio`` -> ``(spec, residual_error)``.

    Ties break toward the earlier entry in ``supported``, which is why the menus are written
    most-common-first: an exactly-ambiguous panel lands on the more conventional shape.
    """
    if not supported:
        raise ValueError("cannot snap against an empty supported-ratio list")
    best_spec, best_err = None, math.inf
    for spec in supported:
        candidate = parse_ratio(spec)
        if candidate is None:
            continue
        err = ratio_error(true_ratio, candidate)
        if err < best_err:
            best_spec, best_err = spec, err
    if best_spec is None:
        raise ValueError(f"no parseable ratio in supported list {list(supported)!r}")
    return best_spec, best_err


def effective_for(
    width: float,
    height: float,
    declared: str,
    supported: Sequence[str] = DEFAULT_SUPPORTED,
) -> tuple[str, float]:
    """Panel geometry + declared ratio -> ``(effective_spec, residual_error)``.

    Degenerate geometry (a zero or negative dimension — a malformed node, not a real panel) falls
    back to the declared ratio with zero error. There is nothing to derive from a box with no area,
    and inventing a ratio there would be worse than honoring what the author wrote.
    """
    if width <= 0 or height <= 0:
        return declared, 0.0
    return snap(width / height, supported)


def drift_report(
    declared: str, effective: str, error: float, threshold: float = SNAP_WARN_THRESHOLD
) -> str | None:
    """A one-line note when a panel's drawn shape disagrees with what it declared.

    Returns None when the snap agreed with the declaration or the residual is small — the common
    case must stay quiet, or the loud case stops being noticeable.
    """
    if declared == effective and error < threshold:
        return None
    if declared != effective:
        return f"declared {declared} -> requesting {effective} (geometry); residual {error:.3f}"
    return f"{declared} kept, but geometry is {error:.3f} off the nearest supported ratio"
