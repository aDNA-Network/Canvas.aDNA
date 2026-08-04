"""Render-chain backends — dispatch clients only, never engines.

Registry maps backend names to (generate-client factory, refine-client factory). H2 ships ``fake``
(the offline default everywhere in tests); ``gemini`` lands at H3 (SPEND-gated), ``comfy`` at H4
(the Vulcan seam) — until then they raise a clean ``NotImplementedError`` naming their phase.
"""

from __future__ import annotations

from typing import Any

from comic_render.backends.base import ImageClient, RefineClient
from comic_render.backends.fake import FakeImageClient, FakeRefineClient


def _not_yet(backend: str, phase: str):
    def _raise(**_: Any):
        raise NotImplementedError(
            f"backend {backend!r} arrives at Halftone {phase} — H2 is the offline bridge; "
            "use 'fake'"
        )
    return _raise


GENERATE_BACKENDS: dict[str, Any] = {
    "fake": FakeImageClient,
    "gemini": _not_yet("gemini", "H3 (SPEND-gated)"),
    "comfy": _not_yet("comfy", "H4 (Vulcan seam)"),
}

REFINE_BACKENDS: dict[str, Any] = {
    "fake": FakeRefineClient,
    "comfy": _not_yet("comfy", "H4 (Vulcan seam)"),
}


def make_generate_client(backend: str) -> ImageClient:
    try:
        return GENERATE_BACKENDS[backend]()
    except KeyError:
        raise ValueError(f"unknown generate backend {backend!r} (known: {sorted(GENERATE_BACKENDS)})")


def make_refine_client(backend: str) -> RefineClient:
    try:
        return REFINE_BACKENDS[backend]()
    except KeyError:
        raise ValueError(f"unknown refine backend {backend!r} (known: {sorted(REFINE_BACKENDS)})")
