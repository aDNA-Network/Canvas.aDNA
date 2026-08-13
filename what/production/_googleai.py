"""Bootstrap for the shared Google model layer (``Home.aDNA/what/code/googleai/``).

This is the standalone-script counterpart to
``comic_render/src/comic_render/backends/_googleai.py``. That one is imported as part of a package;
the loose scripts under ``what/production/`` (``demos/``, and the parity builder under
``what/artifacts/``) already put this directory on ``sys.path`` to reach ``canvas_core``, so they get
this module for free with ``from _googleai import require_googleai``. **One copy for all of them** —
three parallel copies of a fifteen-line bootstrap is a smaller version of the disease this whole
migration exists to cure.

``Home.aDNA`` is **local-by-default** (workspace Standing Rule 4) and unpackaged, so it is reached by
path rather than by install. A node without Home.aDNA must fail with a message that says so, not with
a bare ``ModuleNotFoundError`` that leaves the reader wondering why image generation stopped working.

``GOOGLEAI_PATH`` overrides the location, so if the package is later promoted to its own
``GoogleAI.aDNA`` graph this stays a configuration change rather than an edit here.
"""

from __future__ import annotations

import os
import sys
from importlib.util import find_spec
from pathlib import Path
from typing import Any

PATH_ENV = "GOOGLEAI_PATH"
_SHELF = Path("Home.aDNA") / "what" / "code"


class GoogleAIUnavailable(ImportError):
    """The shared Google model layer is not reachable from this node."""


def _search_upward() -> Path | None:
    """Walk up from this file looking for a workspace that contains the shelf.

    Counting ``parents[n]`` is how the sibling copy got the wrong directory the first time — and it
    would break again the moment the file moved a level. Searching is immune to both. (The parity
    builder proved the point independently: its hardcoded ``parents[2] / "code"`` silently stopped
    resolving when the code moved to ``what/production/`` at PT P5, and nobody noticed for two months.)
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / _SHELF
        if (candidate / "googleai" / "__init__.py").exists():
            return candidate
    return None


def googleai_shelf() -> Path | None:
    """Where the package lives: ``GOOGLEAI_PATH`` if set, else discovered by walking up."""
    override = os.environ.get(PATH_ENV)
    if override:
        return Path(override)
    return _search_upward()


def require_googleai() -> Any:
    """Import and return the ``googleai`` package, or raise something actionable."""
    if find_spec("googleai") is None:
        root = googleai_shelf()
        if root is None or not (root / "googleai" / "__init__.py").exists():
            raise GoogleAIUnavailable(
                f"the shared Google model layer was not found "
                f"(searched upward for {_SHELF}/googleai; {PATH_ENV}="
                f"{os.environ.get(PATH_ENV) or 'unset'}).\n"
                f"It is owned by Home.aDNA (local-by-default, Standing Rule 4), so a node without "
                f"Home.aDNA does not have it.\n"
                f"Fix by placing Home.aDNA in the workspace, or by setting {PATH_ENV} to the "
                f"directory CONTAINING the googleai package.\n"
                f"Do NOT work around this by re-inlining a model ID or an API key here — that "
                f"duplication is exactly what left three scripts in this vault pinned to a model "
                f"family that shuts down 2026-08-17."
            )
        # APPEND, never insert(0). Home's shelf holds ~45 loose modules with generic names
        # (`api_helpers`, `frame_diff`, `window_helpers`); putting it at the front of sys.path would
        # let it shadow anything else in the process for every later import.
        sys.path.append(str(root))
    import googleai

    return googleai
