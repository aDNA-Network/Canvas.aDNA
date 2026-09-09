"""Image probing shared by the review-surface builders.

``review_canvas.py`` has carried a private PNG header reader since Halftone HR. The
variant-selection board needs the same three operations, and P2c's rule is that a measurement two
surfaces share is extracted once rather than reimplemented per surface — the alternative is how
five producers ended up with five different ``est_text_height`` guesses.

Deliberately **PIL-free**: this reads the PNG IHDR chunk directly, so the review path keeps working
on a shelf where Pillow is only a ``canvas_core.print`` dependency. :func:`node_size` delegates the
geometry to :func:`canvas_core.layout_fit.fit_exact_aspect_box`, which is where a sizing decision
belongs.
"""

from __future__ import annotations

import struct
from math import gcd
from pathlib import Path

from canvas_core.layout_fit import fit_exact_aspect_box

_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path: str | Path) -> tuple[int, int]:
    """``(width, height)`` from a PNG's IHDR chunk. Raises ``ValueError`` if it is not a PNG."""
    image = Path(path)
    with image.open("rb") as handle:
        header = handle.read(26)
    if len(header) < 26 or header[:8] != _PNG_MAGIC or header[12:16] != b"IHDR":
        raise ValueError(f"{image}: not a PNG (cannot size the review node)")
    width, height = struct.unpack(">II", header[16:24])
    return int(width), int(height)


def reduced_aspect(width: int, height: int) -> tuple[int, int]:
    """The image's aspect in lowest terms — what ``CV-IMAGE-ASPECT-RATIO-01`` compares against."""
    divisor = gcd(int(width), int(height)) or 1
    return int(width) // divisor, int(height) // divisor


def aspect_label(width: int, height: int) -> str:
    """``"3:2"``-style label for a node's ``qualities.aspect_ratio``."""
    ratio_w, ratio_h = reduced_aspect(width, height)
    return f"{ratio_w}:{ratio_h}"


def node_size(width: int, height: int, max_width: float, max_height: float) -> tuple[int, int]:
    """Largest integer node box inside the fit box at the image's exact aspect."""
    return fit_exact_aspect_box(width, height, max_width, max_height)
