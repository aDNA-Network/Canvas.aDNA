"""deck_generator — a reference deck consumer of the aDNA Canvas Standard v2.0.0 (Operation Keystone E4.4).

Producer code on the ``what/production/`` shelf: it *consumes* the Standard's reference tooling (``canvas_std``, the
installed ``adna-canvas-std``) and never modifies it. ``build_deck`` is the public entry point. Sibling to the E4.3
``brief_consumer`` (the single-page precedent); this one is multi-slide (slides = group nodes).
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

from deck_generator.consume import build_deck  # noqa: E402
from deck_generator.model import DeckInput, Slide, load_deck  # noqa: E402

__version__ = "0.1.0"
STANDARD_VERSION = "2.0.0"

__all__ = ["build_deck", "load_deck", "DeckInput", "Slide", "__version__", "STANDARD_VERSION"]
