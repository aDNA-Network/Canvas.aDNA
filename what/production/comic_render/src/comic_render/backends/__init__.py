"""Render-chain backends — dispatch clients only, never engines.

Registry maps backend names to (generate-client factory, refine-client factory). H2 shipped
``fake`` (the offline default everywhere in tests); H4 landed ``comfy`` **refine** (the Vulcan
seam); H3 landed ``gemini`` **generate** — the first backend here that spends money.

``comfy`` stays absent from the GENERATE registry on purpose: in this chain ComfyUI is the
*refine* engine and the cloud backend is the production substrate (inherited ADR-003). Asking for
``generate:comfy`` is a design error worth surfacing, not a configuration to silently honor.
"""

from __future__ import annotations

from typing import Any

from comic_render.aspect import DEFAULT_SUPPORTED
from comic_render.backends.base import ImageClient, RefineClient
from comic_render.backends.comfy import ComfyRefineClient
from comic_render.backends.fake import FakeImageClient, FakeRefineClient
from comic_render.backends.gemini import GeminiImageClient


def _generate_only_elsewhere(backend: str, reason: str):
    def _raise(**_: Any):
        raise NotImplementedError(f"backend {backend!r} is not a generate backend — {reason}")
    return _raise


GENERATE_BACKENDS: dict[str, Any] = {
    "fake": FakeImageClient,
    "gemini": GeminiImageClient,
    "comfy": _generate_only_elsewhere(
        "comfy",
        "ComfyUI is the refine stage of the chain (ADR-003: the cloud backend is the production "
        "substrate). Use 'refine:comfy'.",
    ),
}

REFINE_BACKENDS: dict[str, Any] = {
    "fake": FakeRefineClient,
    "comfy": ComfyRefineClient,
}


def supported_aspects_for(backend: str | None) -> tuple[str, ...]:
    """The aspect menu a generate backend accepts — read WITHOUT constructing the client.

    Plan runs before any credential is needed and must stay that way, so this reads the class
    attribute off the registry entry. Backends that declare nothing (and the not-yet placeholders,
    which are plain functions) fall back to the conservative default.
    """
    entry = GENERATE_BACKENDS.get(backend or "")
    declared = getattr(entry, "SUPPORTED_ASPECTS", None)
    return tuple(declared) if declared else DEFAULT_SUPPORTED


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
