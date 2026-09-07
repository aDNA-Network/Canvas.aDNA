"""Producer-owned integer geometry (``canvas_std`` is geometry-agnostic).

TODO(clone): compute node ``x/y/width/height`` boxes for your domain. Keep it **deterministic** (no randomness, no
wall-clock) so the round-trip sync hash is stable across rebuilds. Single-surface producers can often inline trivial
geometry in ``consume.py`` and delete this module; multi-page producers benefit from a dedicated layout pass.

⛔ **Do NOT write your own ``est_text_height(text, wrap=…, line_h=…)``.** Every producer in this vault did, each with
different constants, and every one of them disagreed with what the visual traps actually measure — 99 findings across
7 shipped example files, 89 of them (90%) from four classes, all reducing to *"the producer sized the node with a
different model than the trap measures it with"* (Blueprint P2c, F-P2-6). Size through
:mod:`canvas_core.layout_fit` and you pass the gate by construction:

======================================  =============================================================
``canvas_core.layout_fit``              use it for
======================================  =============================================================
``fit_text_height(text, width)``        every text node's height (CV-TEXT-BOUNDS-01)
``heading(title)`` / ``fit_lead(text)`` any titling text — emits ``#### ``, the ONLY lead that clears
                                        CV-LEAD-COST-01 and CV-HIERARCHY-01 together
``fit_group_size(bb_w, bb_h, pad)``     any container (CV-GROUP-PADDING-01, both sub-conditions)
``fit_group_label(label, width)``       the minimum width a group label needs (CV-GROUP-LABEL-01)
``fit_image_box(img, max_w, max_h)``    figure boxes, aspect-preserving (CV-IMAGE-ASPECT-RATIO-01)
======================================  =============================================================

Importing ``canvas_core`` is legal and expected: ``adr_004`` sites it as the shared **engine shelf** under
``what/production/``, not a sibling producer. Two things your clone needs for that import to resolve — both already in
this scaffold, do not delete them:

  * ``pyproject.toml``: ``pythonpath = ["src", ".."]`` and the ``env = ["pillow>=10"]`` extra;
  * ``__init__.py``: the ``_ensure_canvas_core()`` bootstrap, for the console-script path.
"""

from __future__ import annotations

from dataclasses import dataclass

from canvas_core.layout_fit import fit_group_label, fit_group_size, fit_text_height, heading

# TODO(clone): your domain's constants. Anything named ``*_H`` should be a FLOOR that measurement can
# grow past — never a fixed answer. A fixed height is how a `##` heading costing 98.9px shipped in a
# 48px box; a fixed pad is how a container's fill ratio degraded silently as content grew (F-P2-4).
CONTENT_W = 620          # the width interior text nodes are emitted at
PAD = 48                 # nominal container inset (layout_fit raises it to the trap's 24px floor)
GAP = 20                 # vertical gap between blocks
TITLE_BAND = 56          # room under the group label, above the first block
BLOCK_MIN_H = 60         # floor for a one-line block


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int

    def as_node(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.w, "height": self.h}


def title_text(title: str) -> str:
    """The surface's title node — ``#### <title>``.

    Emit one, positioned in the upper 40% of its group: that is what satisfies
    ``CV-HIERARCHY-01``'s title slot. A group *label* is not a substitute — labels never wrap, they
    hard-ellipsise, and they get shorter the further you zoom out.
    """
    return heading(title)


def block_height(text: str, *, width: int = CONTENT_W, min_h: int = BLOCK_MIN_H) -> int:
    """Height a text node needs — the number ``CV-TEXT-BOUNDS-01`` prints in its own fix hint."""
    return fit_text_height(text, width, min_height=min_h)


def stack(texts: list[str], title: str = "") -> tuple[list[Box], Box, Box | None]:
    """Worked example: a vertical column inside one conformant container.

    Returns ``(per-block boxes in order, the container box, the title box or None)``. Delete or
    reshape for your domain — but keep the three moves it demonstrates, because each closes a trap
    class that has actually shipped broken in this vault:

      1. measure every block (never estimate);
      2. emit a ``####`` title node inside the group, not just a label;
      3. size the container from its content *ratio*, and widen it for its label.
    """
    boxes: list[Box] = []
    y = PAD + TITLE_BAND
    top = y

    title_box: Box | None = None
    if title:
        title_box = Box(PAD, y, CONTENT_W, block_height(title_text(title)))
        y += title_box.h + GAP

    for text in texts:
        h = block_height(text)
        boxes.append(Box(PAD, y, CONTENT_W, h))
        y += h + GAP

    content_h = (y - GAP) - top if (boxes or title_box) else 0
    w, ratio_h = fit_group_size(CONTENT_W, content_h, PAD)
    # A fill ceiling and an asymmetric top offset are different constraints — satisfy both.
    h = max(top + content_h + PAD, ratio_h)
    if title:
        _, min_w = fit_group_label(title, w)
        w = max(w, min_w)
    return boxes, Box(0, 0, w, h), title_box
