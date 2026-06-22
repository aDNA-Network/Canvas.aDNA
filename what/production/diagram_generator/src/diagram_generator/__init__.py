"""diagram_generator — a reference diagram consumer of the aDNA Canvas Standard v2.0.0 (Operation Atelier A1).

Producer code on the ``what/production/`` shelf: it *consumes* the Standard's reference tooling (``canvas_std``, the
installed ``adna-canvas-std``) and never modifies it. ``build_diagram`` is the public entry point. Sibling to the
``deck_generator`` (multi-region/slides precedent); this one maps a typed graph onto a single canonical surface plus a
derived Mermaid ``code`` node. Syntax generators are PORTED from the CanvasForge ``canvas_core.mermaid`` quarry (theme
coupling stripped); nothing here imports ``canvas_core`` or anything archived.
"""

from __future__ import annotations

from canvas_std import STANDARD_VERSION as _CANVAS_STANDARD_VERSION

from diagram_generator.consume import build_diagram
from diagram_generator.model import DiagramEdge, DiagramInput, DiagramNode, load_diagram

__version__ = "0.1.0"
# The aDNA Canvas Standard version mirrored from the installed reference tooling (canvas_std).
STANDARD_VERSION = _CANVAS_STANDARD_VERSION

__all__ = [
    "build_diagram",
    "load_diagram",
    "DiagramInput",
    "DiagramNode",
    "DiagramEdge",
    "__version__",
    "STANDARD_VERSION",
]
