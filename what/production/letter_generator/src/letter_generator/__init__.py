"""letter_generator — a reference one-page-letter consumer of the aDNA Canvas Standard v2.0.0.

Producer code on the ``what/production/`` shelf: it *consumes* the Standard's reference tooling (``canvas_std``, the
installed ``adna-canvas-std``) and never modifies it (C8 — the two-shelf firewall). ``build_letter`` is the public
entry point. A letter maps onto a **single canonical surface** — one ``letter_root`` ``group`` enclosing a vertical
stack of interior baseline ``text`` nodes (letterhead, date, recipient, salutation, body paragraphs, closing,
signature), chained in reading order. Closest sibling: ``diagram_generator`` (single-surface, smallest/cleanest).
"""

from __future__ import annotations

from canvas_std import STANDARD_VERSION as _CANVAS_STANDARD_VERSION

from letter_generator.consume import build_letter
from letter_generator.model import Letter, load_letter

__version__ = "0.1.0"
# The aDNA Canvas Standard version mirrored from the installed reference tooling (canvas_std).
STANDARD_VERSION = _CANVAS_STANDARD_VERSION

__all__ = [
    "build_letter",
    "load_letter",
    "Letter",
    "__version__",
    "STANDARD_VERSION",
]
