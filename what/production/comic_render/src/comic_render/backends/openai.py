"""The ``openai`` generate backend — Operation Polyglot, the second paid cloud lane.

Dispatch client only; a THIN BINDING from day one (the gemini backend earned that shape the
hard way — read its docstring). Model IDs, prices, size menus and credential lane order live
in **``Home.aDNA/what/code/openaiapi/``**. What lives here is only what is manifest-shaped:
``ImageClient`` conformance, the ``SUPPORTED_ASPECTS`` class attribute ``extract.plan``
reads without constructing a client, and ``cost_per_image`` for the budget cap.

⛔ **No credential read here, ever** — that exact bug shipped three times fleet-wide before
the shared layers existed. Doctrine: ADR-008 §1 Amendment 1 (proposed) — ``gemini`` remains
the substrate-wide GENERATE default; ``openai`` is the alternate paid lane, selected
explicitly via ``backend_preference`` / ``--chain 'generate:openai'``.
"""

from __future__ import annotations

from typing import Any

from canvas_core.image_generation import ImagePrompt

from comic_render.backends._openaiapi import OpenAIAPIUnavailable, require_openaiapi

# Absence is not fatal: the offline pipeline is provable against `fake`, and
# `backends/__init__` imports this module. Missing the layer costs you this backend only.
try:
    _oa = require_openaiapi()
except OpenAIAPIUnavailable:  # pragma: no cover - exercised on nodes without Home.aDNA
    _oa = None

#: Read by ``backends.supported_aspects_for`` WITHOUT constructing this class. Sourced from
#: the shared registry; the fallback mirrors the registry's own menu deliberately — the
#: OpenAI size grid (square + 3:2 + 2:3) is a DIFFERENT shape from the package default, and
#: falling back to the wider Gemini-ish menu would let plan approve aspects the API refuses.
SUPPORTED_ASPECT_RATIOS: tuple[str, ...] = (
    tuple(_oa.models.OPENAI_IMAGE_ASPECTS) if _oa is not None else ("1:1", "3:2", "2:3")
)

DEFAULT_MODEL = "image.pro"      # → gpt-image-2 via the shared registry
DEFAULT_IMAGE_SIZE = "1K"        # $0.03/image tier; 2K/4K opt-in per panel spec

#: Same tier vocabulary the gemini backend speaks, so a chain spec can swap backends
#: without re-writing its model words.
TIER_ALIASES: dict[str, str] = {
    "pro": "image.pro", "ultra": "image.pro",
    "economy": "image.economy", "mini": "image.economy",
    "flash": "image.economy", "lite": "image.economy",
}


class OpenAICredentialError(RuntimeError):
    """No usable OpenAI credential. Raised from the shared resolver; names variables, never values."""


class OpenAIImageClient:
    """``ImageClient``-conformant generate backend, bound to the shared OpenAI layer."""

    model_name = "gpt-image-2"
    SUPPORTED_ASPECTS = SUPPORTED_ASPECT_RATIOS

    def __init__(
        self,
        *,
        model: str = DEFAULT_MODEL,
        image_size: str = DEFAULT_IMAGE_SIZE,
        client: Any | None = None,
    ) -> None:
        if client is None and _oa is None:
            raise OpenAICredentialError(
                "the openai backend needs the shared OpenAI model layer "
                "(Home.aDNA/what/code/openaiapi). Offline runs use --chain 'generate:fake'."
            )
        try:
            self._client = client or _oa.OpenAIImagesClient()
        except Exception as exc:
            if _oa is not None and isinstance(exc, _oa.CredentialError):
                raise OpenAICredentialError(str(exc)) from exc
            raise
        self.model = model
        self.image_size = image_size
        self.model_name = self._client.resolve(TIER_ALIASES.get(model, model)).id
        self.cost_per_image = self._client.cost_of(TIER_ALIASES.get(model, model), image_size)
        self.calls: list[dict[str, Any]] = []

    @property
    def lane(self) -> str:
        """Which credential lane is in use — surfaced so a spend report can name it."""
        return str(self._client.lane)

    def generate_image(
        self,
        prompt: ImagePrompt | str,
        output_path: str | None = None,
        style: str = "photo",
        aspect_ratio: str = "1:1",
        image_size: str = DEFAULT_IMAGE_SIZE,
        model: str = DEFAULT_MODEL,
    ) -> dict[str, Any]:
        """Generate one image. Returns the ``ImageClient`` result contract.

        Errors are returned, not raised: one refused panel must not abandon the rest of
        the issue (the dispatch-loop contract every backend here honors).
        """
        text = prompt.text if isinstance(prompt, ImagePrompt) else prompt
        result = self._client.generate_image(
            text, output_path, style=style, aspect_ratio=aspect_ratio,
            image_size=image_size or self.image_size,
            model=TIER_ALIASES.get(model, model),
        )
        if result.get("success"):
            self.calls.append({
                "output_path": output_path, "aspect_ratio": aspect_ratio,
                "image_size": result.get("image_size"), "model": result.get("model"),
            })
        return result


def projected_spend(images: int, model: str = DEFAULT_MODEL,
                    image_size: str = DEFAULT_IMAGE_SIZE) -> float:
    """What a run WILL cost — for reporting a number BEFORE spending it."""
    return _oa.projected_spend(TIER_ALIASES.get(model, model), images, image_size)
