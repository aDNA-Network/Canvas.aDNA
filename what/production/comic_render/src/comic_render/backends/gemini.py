"""The ``gemini`` generate backend — Halftone H3, the first real pixels.

Dispatch client only. Everything here is an HTTP call through the shared Google layer; no model, no
sampler, no weights ever enter this vault ("Canvas dispatches, it does not diffuse").

**This is now a thin binding, not an implementation.** Model IDs, prices, aspect menus and
credential lane order live in **``Home.aDNA/what/code/googleai/``** — one place for the whole fleet.
What lives *here* is only what is manifest-shaped: the ``ImageClient`` conformance
``comic_render.dispatch`` expects, the ``SUPPORTED_ASPECTS`` class attribute ``extract.plan`` reads
without constructing a client, and ``cost_per_image`` for the budget cap.

**Why it changed the day after it was written.** The first version carried its own model map, its own
price table and its own credential read — ``os.environ["GEMINI_API_KEY"]``. That is Home credential
**C05**, which Home's own inventory documents as depleted and *deliberately out of the render chain*.
The result was a ``429``, a phase reported to the operator as blocked on billing, and a funded Vertex
service account (**C63**) sitting unused on the same machine the whole time. It was the third
instance of that same bug in the fleet. The fix is not a better credential read here — it is not
having a credential read here at all.
"""

from __future__ import annotations

from typing import Any

from canvas_core.image_generation import ImagePrompt

from comic_render.aspect import DEFAULT_SUPPORTED
from comic_render.backends._googleai import GoogleAIUnavailable, require_googleai

# The shared layer is resolved at import when present, and its ABSENCE IS NOT FATAL: the whole
# offline pipeline is provable against `fake`, and `backends/__init__` imports this module, so a
# hard failure here would make a node without Home.aDNA unable to run even the offline suite.
# Missing it costs you the gemini backend, nothing else — and constructing one says so.
try:
    _ga = require_googleai()
except GoogleAIUnavailable:  # pragma: no cover - exercised on nodes without Home.aDNA
    _ga = None

#: Read by ``backends.supported_aspects_for`` WITHOUT constructing this class, so planning a gemini
#: chain never touches a credential. Sourced from the shared registry — which sources it from the
#: service's own validation error — falling back to this package's conservative menu when the shared
#: layer is absent. The fallback is deliberately the EXISTING constant, never a second copy of the
#: real menu: two hand-maintained copies is the failure this whole change removes.
SUPPORTED_ASPECT_RATIOS: tuple[str, ...] = (
    tuple(_ga.models.GEMINI_IMAGE_ASPECTS) if _ga is not None else DEFAULT_SUPPORTED
)

DEFAULT_MODEL = "image.pro"      # the operator's 2026-08-04 ruling: "Gemini pro-image class"
DEFAULT_IMAGE_SIZE = "2K"

#: Tier vocabulary ``ImagenWiring`` already speaks -> shared-registry capability aliases. Kept so
#: existing callers passing model="pro"/"ultra" keep working; "ultra" maps to the pro tier because
#: the model it used to mean (imagen-4.0-ultra) retires 2026-08-17.
TIER_ALIASES: dict[str, str] = {
    "pro": "image.pro", "ultra": "image.pro",
    "flash": "image.flash", "standard": "image.flash",
    "lite": "image.lite", "fast": "image.lite",
    "economy": "image.economy",
}


class GeminiCredentialError(RuntimeError):
    """No usable Google credential. Raised from the shared resolver; names variables, never values."""


class GeminiImageClient:
    """``ImageClient``-conformant generate backend, bound to the shared Google layer."""

    model_name = "gemini-3-pro-image"
    SUPPORTED_ASPECTS = SUPPORTED_ASPECT_RATIOS

    def __init__(
        self,
        api_key: str | None = None,   # accepted for back-compat; lane resolution is the shared layer's
        *,
        model: str = DEFAULT_MODEL,
        image_size: str = DEFAULT_IMAGE_SIZE,
        client: Any | None = None,
    ) -> None:
        if client is None and _ga is None:
            raise GeminiCredentialError(
                "the gemini backend needs the shared Google model layer "
                "(Home.aDNA/what/code/googleai). Offline runs use --chain 'generate:fake'."
            )
        try:
            self._client = client or _ga.GoogleAIClient()
        except Exception as exc:
            if _ga is not None and isinstance(exc, _ga.CredentialError):
                raise GeminiCredentialError(str(exc)) from exc
            raise
        self.model = model
        self.image_size = image_size
        self.model_name = self._client.resolve(model).id
        self.cost_per_image = self._client.cost_of(model, image_size)
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

        Errors are returned, not raised: ``dispatch`` runs a whole issue, and one refused panel must
        not abandon the twenty-six that would have succeeded.
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
    return _ga.projected_spend(TIER_ALIASES.get(model, model), images, image_size)
