"""diagram_generator — a reference diagram consumer of the aDNA Canvas Standard v2.0.0 (Operation Atelier A1).

Producer code on the ``what/production/`` shelf: it *consumes* the Standard's reference tooling (``canvas_std``, the
installed ``adna-canvas-std``) and never modifies it. ``build_diagram`` is the public entry point. Sibling to the
``deck_generator`` (multi-region/slides precedent); this one maps a typed graph onto a single canonical surface plus a
derived Mermaid ``code`` node. Syntax generators are PORTED from the CanvasForge ``canvas_core.mermaid`` quarry (theme
coupling stripped).

⛩ **Corrected 2026-09-07 (Blueprint P2c):** this docstring read *"nothing here imports ``canvas_core`` or anything
archived"*. The archive half stands; the ``canvas_core`` half was never a rule — ``adr_004`` sites ``canvas_core`` as
the shared **engine shelf** under ``what/production/``, not a sibling producer, and ``comic_render`` has imported from
it since Halftone. This producer now depends on ``canvas_core.layout_fit`` deliberately, so that it and the visual
traps measure with **one** function rather than two independently-guessed models.
"""

from __future__ import annotations


def _ensure_canvas_core() -> None:
    """Guarded self-bootstrap for the unpackaged ``canvas_core`` (``comic_render`` precedent).

    ``canvas_core`` is a bare directory-package on the production shelf (no pyproject) — importable
    only with ``what/production/`` on ``sys.path``. Under pytest the pyproject ``pythonpath``
    covers it; under the console script (or a direct ``python -m``) this inserts the shelf root,
    resolved from this file's real location (editable installs preserve it).
    """
    import importlib.util
    import sys
    from pathlib import Path

    if importlib.util.find_spec("canvas_core") is not None:
        return
    shelf = Path(__file__).resolve().parents[3]  # src/<pkg> → src → <producer> → production
    if (shelf / "canvas_core" / "__init__.py").exists() and str(shelf) not in sys.path:
        sys.path.insert(0, str(shelf))


_ensure_canvas_core()

from canvas_std import STANDARD_VERSION as _CANVAS_STANDARD_VERSION  # noqa: E402

from diagram_generator.consume import build_diagram  # noqa: E402
from diagram_generator.model import DiagramEdge, DiagramInput, DiagramNode, load_diagram  # noqa: E402

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
