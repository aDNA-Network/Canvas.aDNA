"""The ``comfy`` refine backend — the Vulcan seam (Halftone H4).

Thin binding, by design. All ComfyUI mechanics (multipart upload, img2img graph, submit/poll/
download) live in ``canvas_core.comfyforge_adapter`` — the bridge's own boundary rule says the H4
seam is an HTTP adapter in the substrate ("Canvas dispatches, it does not diffuse"). What lives
*here* is everything manifest-shaped: endpoint policy, the separate negative channel, the named
workflow, and turning a panel's ``characters[]`` LoRA entry into a conditioned refine call.

Endpoint policy is the bridge's, not the substrate's: ``canvas_core``'s adapter keeps its
documented Anduril-mesh default for its existing callers, while the bridge resolves
``COMIC_RENDER_COMFY_ENDPOINT`` and otherwise uses the L1-local endpoint the federation wrapper
declares (``how/federation/comfyui/CLAUDE.md`` → ``server_endpoints.l1_local``).

``cost_per_image`` is 0.0: local inference is free, which is what keeps the manifest ``budget_cap``
a meaningful guard on the *cloud* generate stage rather than a number diluted by refine calls.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from canvas_core.comfyforge_adapter import (
    DEFAULT_REFINE_DENOISE,
    ComfyForgeConfig,
    ComfyForgeTier1Adapter,
)

# The wrapper's declared l1_local endpoint — "Canvas render support runs L1-local".
DEFAULT_ENDPOINT = "http://localhost:8188"
ENDPOINT_ENV = "COMIC_RENDER_COMFY_ENDPOINT"
WORKFLOW_DIR_ENV = "COMIC_RENDER_COMFY_WORKFLOW_DIR"


def resolve_endpoint() -> str:
    """``COMIC_RENDER_COMFY_ENDPOINT`` → else the wrapper-declared L1-local endpoint."""
    return os.environ.get(ENDPOINT_ENV) or DEFAULT_ENDPOINT


def resolve_workflow_dir() -> str | None:
    """``COMIC_RENDER_COMFY_WORKFLOW_DIR`` → the dir holding named workflow templates.

    Unset is the normal state today: no template resolves, the adapter's built-in img2img graph
    applies, and a named workflow degrades instead of failing. Point it at ComfyUI.aDNA's
    ``what/workflows/base/`` (read-only consumption, Rule 10) once ``comic_panel_refine`` lands.
    """
    return os.environ.get(WORKFLOW_DIR_ENV) or None


def lora_name_for(lora_ref: str) -> str:
    """A manifest ``lora_ref`` (a path) → the bare filename ComfyUI's LoraLoader expects."""
    return Path(lora_ref).name


def apply_trigger_word(prompt: str, trigger_word: str | None) -> str:
    """Prepend a LoRA trigger token unless it is already present.

    The prompt contract (§1a) deliberately leaves the trigger out of the assembled prompt text —
    it is dispatch-side conditioning, meaningful only to whoever loads the LoRA. The pair-gate
    guarantees a trigger only ever arrives alongside a TRAINED/VALIDATED ``lora_ref``, so
    injecting it here can never emit an inert token.
    """
    if not trigger_word:
        return prompt
    if trigger_word.lower() in prompt.lower():
        return prompt
    return f"{trigger_word}, {prompt}"


class ComfyRefineClient:
    """``RefineClient``-conformant binding to the ComfyUI HTTP adapter."""

    model_name = "comfyui-img2img"

    def __init__(
        self,
        endpoint: str | None = None,
        adapter: ComfyForgeTier1Adapter | None = None,
        *,
        workflow_dir: str | None = None,
        upscale: bool = False,
        cost_per_image: float = 0.0,
    ) -> None:
        self.cost_per_image = cost_per_image
        self.upscale = upscale
        self.adapter = adapter or ComfyForgeTier1Adapter(
            ComfyForgeConfig(
                endpoint=endpoint or resolve_endpoint(),
                workflow_dir=workflow_dir if workflow_dir is not None else resolve_workflow_dir(),
            )
        )
        self.calls: list[dict[str, Any]] = []  # audit trail, mirroring the fake clients

    @property
    def endpoint(self) -> str:
        return self.adapter.config.endpoint

    def health_check(self) -> bool:
        """Reachability probe — used by the live-path smoke to skip when no node is up."""
        return self.adapter.health_check()

    def refine_image(
        self,
        seed_image: str,
        prompt: str,
        output_path: str,
        negative: str | None = None,
        denoise: float = DEFAULT_REFINE_DENOISE,
        workflow: str | None = None,
        lora: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Refine one variant. Returns the ``RefineClient`` result contract unchanged."""
        conditioned = prompt
        lora_spec: dict[str, Any] | None = None
        if lora and lora.get("lora_ref"):
            lora_spec = {
                "name": lora_name_for(lora["lora_ref"]),
                "strength_model": float(lora.get("strength_model", 1.0)),
                "strength_clip": float(lora.get("strength_clip", 1.0)),
            }
            conditioned = apply_trigger_word(prompt, lora.get("trigger_word"))

        result = self.adapter.refine_image(
            seed_image=seed_image,
            prompt=conditioned,
            output_path=output_path,
            negative=negative,
            denoise=denoise,
            workflow=workflow,
            lora=lora_spec,
            upscale=self.upscale,
        )
        self.calls.append({
            "seed_image": seed_image,
            "output_path": output_path,
            "denoise": denoise,
            "workflow": workflow,
            "lora": lora_spec,
            "success": result.get("success"),
        })
        return result
