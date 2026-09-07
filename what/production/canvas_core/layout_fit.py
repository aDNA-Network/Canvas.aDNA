"""Layout fitting — the one measurement producers and traps share.

Every in-vault producer used to carry its own ``est_text_height(text, wrap=…,
line_h=…, pad=…)``: a character-count guess with per-producer constants
(``deck`` wrapped at 60 chars and charged 30px a line, ``document`` at 88 and
24, and so on). The visual traps measure something else entirely — the
Obsidian-CSS-calibrated model in :mod:`canvas_core.text_metrics`, where a
node's content box is ``display:flex`` so paragraph margins **do not collapse**
and a ``##`` lead costs 98.9px before a single body character renders.

Producer and trap therefore never agreed, and the disagreement was invisible
until someone ran the gate: **99 findings across 7 shipped example files, 89 of
them (90%) from four classes**, all of which reduce to "the producer sized the
node with a different model than the trap measures it with" (F-P2-6, Blueprint
P2c).

This module is the fix, and it is deliberately thin. It does not implement a
measurement — it *delegates* to the very functions the traps call, so a
producer that sizes through here passes by construction rather than by luck:

===========================  =========================================  ==========================
Helper                       Delegates to                               Closes
===========================  =========================================  ==========================
:func:`fit_text_height`      ``text_metrics.obsidian_required_node_height``  CV-TEXT-BOUNDS-01/overflow
:func:`fit_lead` /           ``text_metrics.classify_lead_block``       CV-LEAD-COST-01/heading_lead
:func:`heading`                                                         + CV-HIERARCHY-01/title_slot_missing
:func:`fit_group_size`       the CV-GROUP-PADDING-01 fill ratio         CV-GROUP-PADDING-01/aggregate_fill
:func:`fit_group_label`      ``traps.cv_group_label_01.label_budget``   CV-GROUP-LABEL-01/label_truncates
===========================  =========================================  ==========================

**Why ``####`` and not ``**bold**``.** Two shipped traps constrain the same
property from opposite sides: ``CV-HIERARCHY-01`` *requires* a markdown heading
marker in a group's top 40%, and ``CV-LEAD-COST-01`` *forbids* ``h1/h2/h3``
leads. Measured across every lead form (F-P2-3): ``h1/h2/h3`` pass hierarchy and
trip lead-cost; ``**bold**`` does the reverse; ``#####``/``######`` pass both
only by classifying as ``plain`` — a green check for the wrong reason; **``####``
alone passes both honestly**, at 42.6px against bold's 40.0px. 2.6px is not
worth a sibling-trap failure, and this module encodes that choice once so no
producer has to rediscover it.

**A producer MAY import this.** ``adr_004`` sites ``canvas_core`` as the shared
engine shelf under ``what/production/``, not a sibling producer; ``comic_render/
compose.py`` has imported from it since Halftone. The interim constants
``diagram_generator/layout.py`` mirrored out of ``text_metrics`` — and flagged
as a mirror in its own comment — are retired in favour of these calls.

New in Blueprint P2c (2026-09-07). Substrate-neutral: no ``canvas_std`` import,
no application imports, integer output (producer geometry must stay a pure,
reproducible function of its input — the round-trip sync hash depends on it).
"""

from __future__ import annotations

import math
import os
import re

from canvas_core.text_metrics import (
    OBSIDIAN_SAFE_FILL,
    classify_lead_block,
    measure_obsidian_extent,
    obsidian_required_node_height,
)
from canvas_core.traps.cv_group_label_01 import label_budget
from canvas_core.traps.cv_group_padding_01 import (
    AGGREGATE_FILL_MEDIUM,
    PADDING_MIN_PX,
)

__all__ = [
    "GROUP_FILL_TARGET",
    "LEAD_MARKER",
    "MIN_EDGE_PAD",
    "fit_group_label",
    "fit_group_size",
    "fit_image_box",
    "fit_image_height",
    "fit_lead",
    "fit_text_height",
    "fits",
    "heading",
    "is_titled",
    "label_fits",
    "lead_kind",
]

# CV-GROUP-PADDING-01 fires above 0.90 fill on either axis. Aim below it with
# headroom: a fixed pad cannot satisfy a ratio (F-P2-4), so containers scale.
GROUP_FILL_TARGET = 0.88
assert GROUP_FILL_TARGET < AGGREGATE_FILL_MEDIUM  # the target must clear the trap

# The trap's per-node edge-distance floor (its `edge_violation` sub-condition),
# separate from the aggregate fill ratio. A container must satisfy both.
MIN_EDGE_PAD = int(PADDING_MIN_PX)

# The only lead form that clears CV-LEAD-COST-01 and CV-HIERARCHY-01 together.
LEAD_MARKER = "#### "

_HEADING_RE = re.compile(r"^(\s*)(#{1,6})\s+")


# ---------------------------------------------------------------------------
# Text height
# ---------------------------------------------------------------------------


def fit_text_height(text: str, width: float, *, min_height: int = 0) -> int:
    """Node height (px) at which *text* fits inside *width* under the trap.

    Delegates to :func:`canvas_core.text_metrics.obsidian_required_node_height`
    — literally the number ``CV-TEXT-BOUNDS-01`` prints in its own fix hint
    ("Set height >= N"), which already rounds up to 10 and divides by
    ``OBSIDIAN_SAFE_FILL`` so only 90% of a node's declared height is counted
    as usable.

    Replaces the per-producer ``est_text_height`` character-count guesses. Those
    were not merely less accurate; they measured a *different model* than the
    gate, which is why every one of them drifted in the same direction.

    Args:
        text: Markdown content of the node.
        width: The node's declared width in px.
        min_height: Floor, for producers with a minimum node size.

    Returns:
        Integer height in px, ``>= min_height``.
    """
    if width <= 0:
        return int(min_height)
    return max(int(min_height), int(obsidian_required_node_height(text, float(width))))


def fits(text: str, width: float, height: float) -> bool:
    """Whether *text* fits a ``width x height`` node — ``CV-TEXT-BOUNDS-01``'s own predicate."""
    if width <= 0 or height <= 0:
        return True
    return measure_obsidian_extent(text, float(width)) <= OBSIDIAN_SAFE_FILL * float(height)


# ---------------------------------------------------------------------------
# Leads and headings
# ---------------------------------------------------------------------------


def heading(title: str) -> str:
    """Render *title* as the canonical canvas heading (``#### <title>``).

    Use for a node that is *meant* to be a group's title. Positioned in the
    upper 40% of its group, it satisfies ``CV-HIERARCHY-01``'s title slot; as an
    ``h4`` it costs 42.6px rather than an ``h2``'s 98.9px.
    """
    return f"{LEAD_MARKER}{title.strip()}"


def fit_lead(text: str) -> str:
    """Normalize an existing markdown heading lead to ``####``; leave the rest alone.

    ``## Findings`` becomes ``#### Findings``. Body text, bold leads and
    already-``h4`` text are returned unchanged — this demotes a heading's *cost*,
    it never invents a heading where the author wrote none.
    """
    if not text:
        return text
    first, sep, rest = text.partition("\n")
    m = _HEADING_RE.match(first)
    if m is None or m.group(2) == "####":
        return text
    return m.group(1) + LEAD_MARKER + first[m.end():] + sep + rest


def is_titled(text: str) -> bool:
    """Whether *text* leads with a real markdown heading (``CV-HIERARCHY-01``'s signal).

    Note ``#####``/``######`` classify as ``plain`` in the cost model but *are*
    heading markers to the hierarchy trap — the asymmetry that let a canvas pass
    both traps for the wrong reason (F-P2-3). This follows the hierarchy trap.
    """
    return _HEADING_RE.match(text.lstrip().split("\n", 1)[0]) is not None


def lead_kind(text: str) -> str:
    """The lead classification the cost model assigns (``h1``..``h4``/``bold``/``plain``)."""
    return classify_lead_block(text)


# ---------------------------------------------------------------------------
# Groups
# ---------------------------------------------------------------------------


def fit_group_size(
    bbox_w: float,
    bbox_h: float,
    pad: float,
    *,
    fill_target: float = GROUP_FILL_TARGET,
) -> tuple[int, int]:
    """Container size holding a ``bbox_w x bbox_h`` child bounding box.

    Satisfies **both** ``CV-GROUP-PADDING-01`` sub-conditions:

    * ``aggregate_fill`` — the children fill at most *fill_target* of the
      container on either axis, so the ratio holds however large the content
      grows. A fixed pad cannot do this: the fill degrades as content widens,
      which is why the trap fired at 90.36% on a diagram — *barely*, so it read
      as a one-off rather than the scaling defect it was (F-P2-4).
    * ``edge_violation`` — at least :data:`MIN_EDGE_PAD` px between any child
      edge and the container edge.

    Args:
        bbox_w: Width of the children's bounding box.
        bbox_h: Height of the children's bounding box.
        pad: The producer's nominal inset (raised to ``MIN_EDGE_PAD`` if lower).
        fill_target: Fill ratio to aim for; must be below the trap's 0.90.

    Returns:
        ``(width, height)`` as integers.
    """
    pad = max(float(pad), float(MIN_EDGE_PAD))
    w = max(bbox_w + 2 * pad, bbox_w / fill_target + 1) if bbox_w > 0 else 2 * pad
    h = max(bbox_h + 2 * pad, bbox_h / fill_target + 1) if bbox_h > 0 else 2 * pad
    return int(math.ceil(w)), int(math.ceil(h))


def fit_group_label(label: str, width: float) -> tuple[str, int]:
    """Check a group label against its width; report the width it needs.

    Obsidian group labels never wrap — they hard-ellipsise, and because the
    label scales with ``--zoom-multiplier`` **fewer** characters fit the further
    back you stand, which is exactly the view used to survey a large canvas.

    Delegates the budget to :func:`canvas_core.traps.cv_group_label_01.label_budget`
    so producer and trap cannot disagree.

    Args:
        label: The group label.
        width: The group's current width in px.

    Returns:
        ``(label, min_width)`` — *label* unchanged, and the minimum width at
        which it does not truncate. ``min_width <= width`` means it already
        fits. Callers widen a frame group, or shorten an interior one.
    """
    if not label:
        return label, 0
    # Same divisors as ``label_budget``: ALL-CAPS glyphs run ~15% wider.
    divisor = 25.0 if label == label.upper() else 22.0
    return label, int(math.ceil(len(label) * divisor))


def label_fits(label: str, width: float) -> bool:
    """Whether *label* renders in full at *width* (the trap's own predicate)."""
    if not label or width <= 0:
        return True
    return len(label) <= label_budget(float(width), label)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------


def fit_image_height(
    image: str,
    width: float,
    *,
    max_height: float | None = None,
    search_from: str | None = None,
) -> int | None:
    """Node height that preserves *image*'s intrinsic aspect at *width*.

    ``CV-IMAGE-ASPECT-RATIO-01`` compares a file node's declared box against the asset's real
    dimensions and flags drift above 5% (HIGH above 15%, CRITICAL above 30%). A producer with a
    fixed ``FIG_H`` cannot satisfy it for arbitrary assets — and worse, the same asset used at two
    different box widths cannot be authored to fit both, so the fix has to be on the producer side.

    Discovered at P2c only *after* the three missing example PNGs were generated: with the files
    absent, this trap had nothing to resolve and stayed silent. Restoring an asset therefore turned
    a ``file_missing`` finding into an ``aspect_drift`` one — **the second defect was always there,
    masked by the first.** A check that cannot run is not a check that passes.

    Returns ``None`` when the asset cannot be resolved or read (remote URL, missing file, no
    Pillow), which the caller should read as "keep your default" — never as "fits".

    Args:
        image: The node's ``file`` value, as it will be written (vault-relative).
        width: The node's declared width.
        max_height: Optional clamp; the width is *not* reduced to compensate, since the caller owns
            its column. A clamped result may still drift, so callers with a hard height budget
            should verify rather than assume.
        search_from: Directory to begin resolution from (defaults to the process cwd). Resolution
            walks up looking for a directory containing ``.obsidian`` — the same vault-root
            discovery ``canvas-visual-check`` uses — so producers need no vault configuration.
    """
    if width <= 0 or image.startswith(("http://", "https://", "data:")):
        return None
    try:
        from PIL import Image
    except ImportError:
        return None

    start = os.path.abspath(search_from or os.getcwd())
    roots: list[str] = []
    current = start
    while True:
        roots.append(current)
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent

    for root in roots:
        candidate = os.path.join(root, image)
        if not os.path.isfile(candidate):
            continue
        try:
            with Image.open(candidate) as im:
                src_w, src_h = im.size
        except Exception:
            return None
        if src_w <= 0 or src_h <= 0:
            return None
        height = float(width) * src_h / src_w
        if max_height is not None:
            height = min(height, float(max_height))
        return max(1, int(round(height)))
    return None


def fit_image_box(
    image: str,
    max_width: float,
    max_height: float,
    *,
    search_from: str | None = None,
) -> tuple[int, int] | None:
    """Largest box inside ``max_width x max_height`` that preserves *image*'s aspect.

    The companion :func:`fit_image_height` clamps height and lets width stand, which **still
    drifts** whenever the clamp binds — exactly what happened on the deck's image slide, where the
    asset wanted 560px of height in the 436px a 16:9 slide had left after its heading and caption
    (28.4% drift, HIGH). Fitting *both* axes is the only answer when the caller's height is fixed;
    the caller then centres the narrower result in its column.

    Returns ``None`` on the same terms as :func:`fit_image_height` — unresolvable means "keep your
    default", never "fits".
    """
    if max_width <= 0 or max_height <= 0:
        return None
    natural_h = fit_image_height(image, max_width, search_from=search_from)
    if natural_h is None:
        return None
    if natural_h <= max_height:
        return int(max_width), natural_h
    # Height binds: scale the width down by the same ratio rather than squashing the asset.
    scale = float(max_height) / float(natural_h)
    return max(1, int(round(max_width * scale))), int(max_height)
