"""Bootstrap for the shared Google model layer (``Home.aDNA/what/code/googleai/``).

``Home.aDNA`` is **local-by-default** (workspace Standing Rule 4) and unpackaged, so it is reached by
path rather than by install — the same pattern ``canvas_core/rlhf/review_collect.py`` uses for
``canvas_context``. A node without Home.aDNA must fail with a message that says so, not with a bare
``ModuleNotFoundError`` that leaves the reader wondering why rendering stopped working.

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

    Counting ``parents[n]`` is how this got the wrong directory the first time — and it would break
    again the moment the package moved a level. Searching is immune to both.
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
                f"Do NOT work around this by re-inlining model IDs or an API key here — that "
                f"duplication is exactly what put a retired model and a dead credential in this "
                f"backend in the first place."
            )
        # APPEND, never insert(0). Home's shelf holds ~45 loose modules with generic names
        # (`api_helpers`, `frame_diff`, `window_helpers`); putting it at the front of sys.path would
        # let it shadow anything else in the process for every later import.
        sys.path.append(str(root))
    import googleai

    return googleai
