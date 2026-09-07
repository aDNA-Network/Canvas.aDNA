"""__producer__ — TODO(clone): one-line description. A canvas producer on canvas_std (Operation Palette).

TODO(clone): rename this package dir (`src/__producer__/`) to your producer's package name.
"""

from __future__ import annotations


def _ensure_canvas_core() -> None:
    """Guarded self-bootstrap for the unpackaged ``canvas_core`` engine shelf. KEEP THIS.

    ``canvas_core`` is a bare directory-package under ``what/production/`` (no pyproject), so it is
    importable only with that directory on ``sys.path``. Under pytest the pyproject ``pythonpath``
    covers it; under the console script (or a direct ``python -m``) this does. Deleting it makes
    ``layout.py``'s ``canvas_core.layout_fit`` import fail outside the test runner only — the worst
    kind of breakage to discover.
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
