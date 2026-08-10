"""The ``gemini`` generate backend — Halftone H3, the first real pixels.

Dispatch client only. Everything here is an HTTP call through Google's GenAI SDK; no model, no
sampler, no weights ever enter this vault ("Canvas dispatches, it does not diffuse").

**Lineage.** Adapted from ``adna_lab.mcp.image.server.GeminiImageClient`` (Jupyter.aDNA — the
credential handling, the tier map and the result contract are that client's shape, credited here
the way Kennedy's ``canvas_fit_check.py`` was at HV). **It is not a copy, and the difference is
load-bearing:** the precedent calls ``client.models.generate_images`` against ``imagen-4.0-*``.
Verified live on 2026-08-09, the Imagen 4 family is **deprecated with a shutdown date of
2026-08-17** — eight days after this was written. Building H3 on it would have shipped a backend
with a fortnight to live. This client targets the **Gemini native image** models instead, which
are reached through ``generate_content`` with ``response_modalities=['Image']`` — a different call,
a different config object, and a different response shape.

**Everything below was verified against the live API, not against documentation.** The aspect menu
came from the service itself: sending a deliberately invalid ratio returns a 400 that enumerates
the valid ones, which costs nothing and cannot go stale the way a hand-copied list does.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from canvas_core.image_generation import ImagePrompt

API_KEY_ENV = "GEMINI_API_KEY"
MODEL_ENV = "COMIC_RENDER_GEMINI_MODEL"

# Tier -> model id. Keyed by the tier vocabulary ``ImagenWiring`` already speaks (its DEFAULT_MODEL
# is "pro", which is also the operator's 2026-08-04 ruling: "Gemini pro-image class").
# "ultra" is retained as an alias for "pro" so pre-H3 callers using the old Imagen tier vocabulary
# resolve to something live rather than to a model that no longer exists.
MODELS: dict[str, str] = {
    "pro": "gemini-3-pro-image",
    "ultra": "gemini-3-pro-image",
    "flash": "gemini-3.1-flash-image",
    "lite": "gemini-3.1-flash-lite-image",
    "economy": "gemini-2.5-flash-image",
}
DEFAULT_TIER = "pro"

# USD per output image, by (tier, image_size). Verified against ai.google.dev/gemini-api/docs/pricing
# on 2026-08-09. These drive the manifest budget cap, so a stale number here means a real overspend:
# re-verify before any run that matters, and treat the cap as the actual guard rather than this map.
PRICING: dict[tuple[str, str], float] = {
    ("pro", "1K"): 0.134, ("pro", "2K"): 0.134, ("pro", "4K"): 0.24,
    ("flash", "1K"): 0.067, ("flash", "2K"): 0.101, ("flash", "4K"): 0.151,
    ("lite", "1K"): 0.0336, ("lite", "2K"): 0.0336, ("lite", "4K"): 0.0336,
    ("economy", "1K"): 0.039, ("economy", "2K"): 0.039, ("economy", "4K"): 0.039,
}
PRICING_VERIFIED_ON = "2026-08-09"

# Straight from the service's own 400 on an invalid value (2026-08-09). Ordered most-conventional
# first because ``aspect.snap`` breaks ties toward the earlier entry.
SUPPORTED_ASPECT_RATIOS: tuple[str, ...] = (
    "1:1", "3:4", "4:3", "2:3", "3:2", "9:16", "16:9",
    "4:5", "5:4", "21:9", "1:4", "4:1", "1:8", "8:1",
)

VALID_IMAGE_SIZES: tuple[str, ...] = ("1K", "2K", "4K")
DEFAULT_IMAGE_SIZE = "2K"


class GeminiCredentialError(RuntimeError):
    """``GEMINI_API_KEY`` is absent. Names the variable; never echoes a value."""


class GeminiImageClient:
    """``ImageClient``-conformant generate backend over the Gemini native image models."""

    model_name = "gemini-3-pro-image"

    # Read by ``backends.supported_aspects_for`` WITHOUT constructing this class, so that planning
    # a gemini chain never touches a credential.
    SUPPORTED_ASPECTS = SUPPORTED_ASPECT_RATIOS

    def __init__(
        self,
        api_key: str | None = None,
        *,
        tier: str = DEFAULT_TIER,
        image_size: str = DEFAULT_IMAGE_SIZE,
        client: Any | None = None,
    ) -> None:
        # Credential by NAME from the environment (Home.aDNA broker discipline): the value is read
        # here, held on the SDK client, and never logged, never written to the manifest, and never
        # placed in an exception message.
        self._api_key = api_key or os.environ.get(API_KEY_ENV, "")
        if not self._api_key and client is None:
            raise GeminiCredentialError(
                f"{API_KEY_ENV} is not set — the gemini backend needs it. Provision it through the "
                "Home.aDNA credential broker; do not inline a key."
            )
        if image_size not in VALID_IMAGE_SIZES:
            raise ValueError(f"image_size must be one of {VALID_IMAGE_SIZES}, got {image_size!r}")
        self.tier = tier if tier in MODELS else DEFAULT_TIER
        self.image_size = image_size
        self.model_name = os.environ.get(MODEL_ENV) or MODELS[self.tier]
        self.cost_per_image = PRICING.get((self.tier, image_size), PRICING[("pro", "2K")])
        self._client = client
        self.calls: list[dict[str, Any]] = []  # audit trail, mirroring the fake + comfy clients

    def _get_client(self) -> Any:
        """Lazy SDK client — import inside the method so the offline suite never needs the SDK."""
        if self._client is None:
            try:
                from google import genai
            except ImportError as exc:  # pragma: no cover - environment-dependent
                raise ImportError(
                    "google-genai is required for the gemini backend: "
                    "pip install 'comic-render[cloud]'"
                ) from exc
            self._client = genai.Client(api_key=self._api_key)
        return self._client

    def generate_image(
        self,
        prompt: ImagePrompt | str,
        output_path: str | None = None,
        style: str = "photo",
        aspect_ratio: str = "1:1",
        image_size: str = "2K",
        model: str = DEFAULT_TIER,
    ) -> dict[str, Any]:
        """Generate one image. Returns the ``ImageClient`` result contract.

        Errors are returned, not raised: ``dispatch`` runs a whole issue, and one refused panel
        must not abandon the twenty-six that would have succeeded.
        """
        from google.genai import types

        prompt_obj = ImagePrompt(text=prompt) if isinstance(prompt, str) else prompt
        if not output_path:
            return {"success": False, "error": "gemini backend requires an explicit output_path"}

        if aspect_ratio not in SUPPORTED_ASPECT_RATIOS:
            # Refuse rather than silently substituting: plan already snapped to this menu, so an
            # unsupported value here means the manifest and the backend disagree — a bug worth
            # surfacing, not smoothing over.
            return {
                "success": False,
                "error": f"aspect_ratio {aspect_ratio!r} is not supported by {self.model_name} "
                         f"(supported: {', '.join(SUPPORTED_ASPECT_RATIOS)})",
            }

        size = image_size if image_size in VALID_IMAGE_SIZES else self.image_size
        model_id = os.environ.get(MODEL_ENV) or MODELS.get(model, MODELS[self.tier])
        text = prompt_obj.text
        if style and style != "photo":
            text = f"{style} style: {text}"

        try:
            response = self._get_client().models.generate_content(
                model=model_id,
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["Image"],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                        image_size=size,
                    ),
                ),
            )
            data = _first_image_bytes(response)
            if data is None:
                # A response with no image part is the safety-filter / refusal shape. It is a
                # success at the HTTP layer and a failure at the only layer that matters.
                return {
                    "success": False,
                    "error": f"no image in response from {model_id} "
                             f"(refusal or safety filter; finish_reason={_finish_reason(response)})",
                }

            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            self.calls.append({
                "output_path": output_path, "aspect_ratio": aspect_ratio,
                "image_size": size, "model": model_id,
            })
            return {
                "success": True,
                "image_path": output_path,
                "adapter": "gemini",
                "model": model_id,
                "aspect_ratio": aspect_ratio,
                "image_size": size,
                "size_bytes": len(data),
                "cost_usd": self.cost_per_image,
            }
        except Exception as exc:  # noqa: BLE001 - the whole point is that one panel cannot abort a run
            return {"success": False, "error": f"{type(exc).__name__}: {exc}"}


def _first_image_bytes(response: Any) -> bytes | None:
    """The image bytes from a ``generate_content`` response, or None if it carries no image.

    Gemini interleaves modalities: an image response may also contain text parts, and the image
    may not be first. Walking every part is the difference between working and intermittently
    working.
    """
    for candidate in getattr(response, "candidates", None) or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", None) or []:
            inline = getattr(part, "inline_data", None)
            if inline is not None and getattr(inline, "data", None):
                return inline.data
    return None


def _finish_reason(response: Any) -> str:
    for candidate in getattr(response, "candidates", None) or []:
        reason = getattr(candidate, "finish_reason", None)
        if reason:
            return str(reason)
    return "unknown"


def projected_spend(images: int, tier: str = DEFAULT_TIER, image_size: str = DEFAULT_IMAGE_SIZE)\
        -> float:
    """What a run of ``images`` calls will cost — for reporting a number BEFORE spending it."""
    return round(images * PRICING.get((tier, image_size), PRICING[("pro", "2K")]), 4)
