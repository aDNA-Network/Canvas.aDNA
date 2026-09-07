"""Bootstrap for the shared OpenAI model layer (``Home.aDNA/what/code/openaiapi/``).

Sibling of ``_googleai.py`` — read that docstring for the why (path-reached because
Home.aDNA is local-by-default and unpackaged; loud actionable failure on nodes without it;
``OPENAIAPI_PATH`` override so a future promotion to its own graph is a config change).
"""

from __future__ import annotations

import os
import sys
from importlib.util import find_spec
from pathlib import Path
from typing import Any

PATH_ENV = "OPENAIAPI_PATH"
_SHELF = Path("Home.aDNA") / "what" / "code"


class OpenAIAPIUnavailable(ImportError):
    """The shared OpenAI model layer is not reachable from this node."""


def _search_upward() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / _SHELF
        if (candidate / "openaiapi" / "__init__.py").exists():
            return candidate
    return None


def openaiapi_shelf() -> Path | None:
    override = os.environ.get(PATH_ENV)
    if override:
        return Path(override)
    return _search_upward()


def require_openaiapi() -> Any:
    """Import and return the ``openaiapi`` package, or raise something actionable."""
    if find_spec("openaiapi") is None:
        root = openaiapi_shelf()
        if root is None or not (root / "openaiapi" / "__init__.py").exists():
            raise OpenAIAPIUnavailable(
                f"the shared OpenAI model layer was not found "
                f"(searched upward for {_SHELF}/openaiapi; {PATH_ENV}="
                f"{os.environ.get(PATH_ENV) or 'unset'}).\n"
                f"It is owned by Home.aDNA (local-by-default, Standing Rule 4).\n"
                f"Fix by placing Home.aDNA in the workspace, or by setting {PATH_ENV} to the "
                f"directory CONTAINING the openaiapi package.\n"
                f"Do NOT work around this by re-inlining model IDs or an API key here — that "
                f"duplication is the three-times-shipped bug the shared layers exist to end."
            )
        # APPEND, never insert(0) — see _googleai.py for why.
        sys.path.append(str(root))
    import openaiapi

    return openaiapi
