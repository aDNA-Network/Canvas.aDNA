"""Backend protocols — reuse ``canvas_core``'s ``ImageClient``; extend (never break) with refine.

``ImageClient`` is the existing substrate protocol (``canvas_core/image_generation.py``) — the
bridge invents NO new generate abstraction. The **refine** stage needs an init-image input the
generate protocol doesn't carry, so ``RefineClient`` is an additive sibling Protocol (roadmap §1:
"extend via an optional RefineClient protocol — don't break ImageClient"). Structured prompt
layers (esp. the separate ``negative`` channel) travel out-of-band from the manifest — the
generate protocol forwards text only.
"""

from __future__ import annotations

from typing import Any, Protocol

from canvas_core.image_generation import ImageClient, ImagePrompt  # noqa: F401 (re-export)


class RefineClient(Protocol):
    """Minimal interface for an img2img refine step (chain stage 2).

    Return contract mirrors ``ImageClient.generate_image``: ``{"success": bool, "image_path": str}``
    or ``{"success": False, "error": str}``. The production form binds to Vulcan's
    ``comic_panel_refine`` ComfyUI workflow at H4 (img2img + positive/negative + denoise +
    LoRA slot + upscale); H2 proves the chain with the fake.

    ``lora`` (H4, optional) is the panel's ``characters[]`` entry carrying the pair-gated
    ``{trigger_word, lora_ref}`` — the LoRA slot the roadmap reserves for "LoRA re-enters via the
    refine chain when trained" (R3). Backends that cannot condition on a LoRA ignore it.
    """

    def refine_image(
        self,
        seed_image: str,
        prompt: str,
        output_path: str,
        negative: str | None = None,
        denoise: float = 0.4,
        workflow: str | None = None,
        lora: dict[str, Any] | None = None,
    ) -> dict[str, Any]: ...
