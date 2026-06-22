"""comic_generator — a reference comic consumer of the aDNA Canvas Standard v2.0.0 (Operation Atelier A2).

Producer code on the ``what/production/`` shelf: it *consumes* the Standard's reference tooling (``canvas_std``, the
installed ``adna-canvas-std``) and never modifies it. ``build_comic`` is the public entry point — it maps a comic spec
(ordered pages, each a 2D grid of panels) onto a multi-page ``.canvas`` whose pages are ``group`` nodes carrying a
panel grid. Structurally it mirrors the ``document_generator`` (pages = region-bearing panels; ``sequence`` /
``reading_order`` / ``adjacency`` edges) with a 2D panel interior.

The content layer (``model`` / ``style`` / ``prompt`` / ``panel_layout`` / ``rlhf_hints``) is PORTED from the
CanvasForge ``canvas_comic`` quarry (``CanvasBuilder`` / ``ContextPack`` / ``ImagePrompt`` couplings dropped; the
Science-Stanley instance data lifted out and routed through ``ComicInput`` per scope D5); only the canvas construction
(``layout`` / ``panels`` / ``consume``) is rewritten on ``canvas_std``. Nothing here imports ``canvas_core`` or
anything archived.

Image boundary: this producer emits image PROMPTS as ``_reserved`` metadata only — it NEVER renders pixels, imports
no ComfyUI, and does no image I/O. Already-rendered image *paths* are accepted as optional input.
"""

from __future__ import annotations

from canvas_std import STANDARD_VERSION as _CANVAS_STANDARD_VERSION

from comic_generator.consume import build_comic
from comic_generator.model import ComicInput, Page, Panel, Spread, load_comic

__version__ = "0.1.0"
# The aDNA Canvas Standard version mirrored from the installed reference tooling (canvas_std).
STANDARD_VERSION = _CANVAS_STANDARD_VERSION

__all__ = [
    "build_comic",
    "load_comic",
    "ComicInput",
    "Page",
    "Panel",
    "Spread",
    "__version__",
    "STANDARD_VERSION",
]
