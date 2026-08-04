"""comic_render — the Halftone render bridge (H2+).

``issue.canvas`` → render manifest → dispatched variants → selection → ``issue.rendered.canvas``
(a NEW file; the input is immutable) → composited print pages.

Boundary (campaign standing order): **"Canvas dispatches, it does not diffuse."** This package MAY
import HTTP dispatch clients; it MUST NEVER import a render engine (torch/diffusers/local
pipelines); PIL is reached only through ``canvas_core.print``. Enforced by ``tests/test_boundary.py``
(the inverted mirror of comic_generator's guard). It also never imports ``comic_generator`` — the
producer hands off file-shaped via ``.canvas``.

``issue.rendered.canvas`` is a **derived artifact** (operator ruling 2026-08-03, roadmap open
decision #5): the YAML source + producer stay authoritative; re-renders are cheap.
"""

from __future__ import annotations

__version__ = "0.1.0"

MANIFEST_SCHEMA_VERSION = "0.1"


def _ensure_canvas_core() -> None:
    """Guarded self-bootstrap for the unpackaged ``canvas_core`` (traps/cli.py precedent).

    ``canvas_core`` is a bare directory-package on the production shelf (no pyproject) — importable
    only with ``what/production/`` on ``sys.path``. Under pytest the pyproject ``pythonpath``
    covers it; under the ``comic-render`` console script (or a direct ``python -m``) this inserts
    the shelf root, resolved from this file's real location (editable installs preserve it).
    """
    import importlib.util
    import sys
    from pathlib import Path

    if importlib.util.find_spec("canvas_core") is not None:
        return
    shelf = Path(__file__).resolve().parents[3]  # src/comic_render → src → comic_render → production
    if (shelf / "canvas_core" / "__init__.py").exists() and str(shelf) not in sys.path:
        sys.path.insert(0, str(shelf))


_ensure_canvas_core()
