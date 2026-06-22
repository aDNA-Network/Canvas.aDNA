"""ComfyForge Tier 1 adapter — direct HTTP API client for ComfyUI on Anduril.

Implements the ImageClient Protocol for ComfyUI running on the Anduril
RTX 3090 (Nebula mesh, 10.42.0.8:8188). Tier 1 is a style-transfer
experimental path, NOT an alternative production backend (ADR 003).

API pattern per coord note § Tier 1 contract:
    POST /prompt          — submit workflow JSON → {"prompt_id": "<UUID>"}
    GET  /history/{id}    — poll for completion → download image
    GET  /system_stats    — health check (circuit-breaker probe)

Circuit-breaker escalation:
    Anduril (primary) → Mac MPS (fallback) → Imagen (v1.0 safety net)

Migrated: N/A (new in M-3-05)
"""

from __future__ import annotations

import json
import logging
import shutil
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from canvas_core.image_generation import ImagePrompt, _coerce_prompt

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Aspect ratio → ComfyUI pixel dimensions
# ---------------------------------------------------------------------------

ASPECT_RATIO_MAP: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "16:9": (1344, 768),
    "9:16": (768, 1344),
    "4:3": (1152, 896),
    "3:4": (896, 1152),
    "3:2": (1216, 832),
    "2:3": (832, 1216),
}

DEFAULT_DIMENSIONS = (1024, 1024)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class ComfyForgeConfig:
    """Configuration for the Tier 1 ComfyForge adapter."""

    endpoint: str = "http://10.42.0.8:8188"
    timeout_s: int = 30
    failover_ms: int = 2000
    poll_interval_s: float = 2.0
    style_config_path: str | None = None
    checkpoint: str = "sd_xl_base_1.0.safetensors"
    sampler: str = "euler"
    scheduler: str = "normal"
    steps: int = 20
    cfg_scale: float = 7.0


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------

class ComfyForgeTier1Adapter:
    """Tier 1 direct-API adapter for ComfyUI on Anduril.

    Conforms to the ``ImageClient`` Protocol defined in
    ``canvas_core.image_generation``. Translates ``ImageRequest`` fields
    to ComfyUI workflow JSON, POSTs to the endpoint, polls for completion,
    and downloads the result image.

    This adapter is substrate-neutral: it contains no deck-specific or
    comic-specific logic. Any application can use it by passing
    ``backend_preference=["comfyforge_anduril"]`` in an ``ImageRequest``.
    """

    def __init__(self, config: ComfyForgeConfig | None = None) -> None:
        self.config = config or ComfyForgeConfig()
        self._style_config: dict[str, Any] | None = None
        self._healthy: bool | None = None  # None = unknown

    # ------------------------------------------------------------------
    # ImageClient Protocol conformance
    # ------------------------------------------------------------------

    def generate_image(
        self,
        prompt: ImagePrompt | str,
        output_path: str | None = None,
        style: str = "photo",
        aspect_ratio: str = "1:1",
        image_size: str = "2K",
        model: str = "ultra",
    ) -> dict[str, Any]:
        """Generate an image via ComfyUI.

        Returns ``{"success": True, "image_path": str}`` on success,
        ``{"success": False, "error": str}`` on failure.

        M-R2-02: ``prompt`` accepts ``ImagePrompt`` (preferred) or ``str``
        (backcompat with DeprecationWarning, sunset v1.2). The mermaid_layout
        and aspect_ratio fields of ImagePrompt are intentionally not consumed
        here — Tier 1 ComfyForge is a style-transfer engine (ADR 003), so
        only ``.text`` is forwarded to the SDXL workflow.
        """
        prompt_obj = _coerce_prompt(prompt)

        if not self.health_check():
            return {
                "success": False,
                "error": "anduril_unreachable",
                "adapter": "comfyforge_tier1",
            }

        try:
            workflow = self._build_workflow(prompt_obj.text, aspect_ratio, style, model)
            prompt_id = self._submit_workflow(workflow)
            history = self._poll_history(prompt_id)
            image_path = self._download_image(history, prompt_id, output_path)
            return {
                "success": True,
                "image_path": image_path,
                "adapter": "comfyforge_tier1",
                "prompt_id": prompt_id,
            }
        except Exception as e:
            logger.error("ComfyForge Tier 1 generation failed: %s", e)
            return {
                "success": False,
                "error": str(e),
                "adapter": "comfyforge_tier1",
            }

    # ------------------------------------------------------------------
    # Health check (circuit-breaker probe)
    # ------------------------------------------------------------------

    def health_check(self) -> bool:
        """Probe /system_stats to verify Anduril is reachable."""
        url = f"{self.config.endpoint}/system_stats"
        timeout_s = self.config.failover_ms / 1000.0
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                self._healthy = resp.status == 200
        except (urllib.error.URLError, OSError, TimeoutError):
            self._healthy = False
        return self._healthy

    # ------------------------------------------------------------------
    # Workflow construction
    # ------------------------------------------------------------------

    def _build_workflow(
        self,
        prompt: str,
        aspect_ratio: str,
        style: str,
        model: str,
    ) -> dict[str, Any]:
        """Build a ComfyUI workflow JSON from request parameters.

        Produces a minimal SDXL txt2img workflow with checkpoint loader,
        CLIP text encode (positive + negative), KSampler, VAE decode,
        and image save nodes.
        """
        width, height = ASPECT_RATIO_MAP.get(aspect_ratio, DEFAULT_DIMENSIONS)

        # Apply style hints from style config if available
        styled_prompt = self._apply_style(prompt, style)
        negative = "blurry, low quality, distorted, watermark, text"

        workflow = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "seed": int(time.time()) % (2**32),
                    "steps": self.config.steps,
                    "cfg": self.config.cfg_scale,
                    "sampler_name": self.config.sampler,
                    "scheduler": self.config.scheduler,
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0],
                },
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {"ckpt_name": self.config.checkpoint},
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {"width": width, "height": height, "batch_size": 1},
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": styled_prompt, "clip": ["4", 1]},
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": negative, "clip": ["4", 1]},
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {"images": ["8", 0], "filename_prefix": "canvasforge"},
            },
        }
        return workflow

    def _apply_style(self, prompt: str, style: str) -> str:
        """Apply style modifiers from the loaded style config.

        If no style config is loaded or the style key isn't found,
        returns the prompt unmodified.
        """
        config = self._get_style_config()
        if not config:
            return prompt

        from .style_mapping import resolve_style

        style_mods = resolve_style(config, register=style, style_hints="")
        if style_mods.get("positive_suffix"):
            return f"{prompt}, {style_mods['positive_suffix']}"
        return prompt

    def _get_style_config(self) -> dict[str, Any]:
        """Lazy-load style config from configured path."""
        if self._style_config is not None:
            return self._style_config

        if not self.config.style_config_path:
            self._style_config = {}
            return self._style_config

        from .style_mapping import load_style_config

        self._style_config = load_style_config(self.config.style_config_path)
        return self._style_config

    # ------------------------------------------------------------------
    # HTTP operations
    # ------------------------------------------------------------------

    def _submit_workflow(self, workflow: dict[str, Any]) -> str:
        """POST workflow to /prompt and return prompt_id."""
        url = f"{self.config.endpoint}/prompt"
        payload = json.dumps({"prompt": workflow}).encode("utf-8")
        req = urllib.request.Request(
            url, data=payload, method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=self.config.timeout_s) as resp:
            data = json.loads(resp.read())
        prompt_id = data.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"No prompt_id in response: {data}")
        return prompt_id

    def _poll_history(self, prompt_id: str) -> dict[str, Any]:
        """Poll /history/{prompt_id} until generation completes or times out."""
        url = f"{self.config.endpoint}/history/{prompt_id}"
        deadline = time.monotonic() + self.config.timeout_s

        while time.monotonic() < deadline:
            try:
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read())
                if prompt_id in data:
                    return data[prompt_id]
            except (urllib.error.URLError, OSError):
                pass
            time.sleep(self.config.poll_interval_s)

        raise TimeoutError(
            f"ComfyUI generation timed out after {self.config.timeout_s}s "
            f"(prompt_id={prompt_id})"
        )

    def _download_image(
        self,
        history: dict[str, Any],
        prompt_id: str,
        output_path: str | None,
    ) -> str:
        """Extract image data from history response and save to disk."""
        outputs = history.get("outputs", {})

        # Find the SaveImage node output
        image_info = None
        for node_output in outputs.values():
            images = node_output.get("images", [])
            if images:
                image_info = images[0]
                break

        if not image_info:
            raise RuntimeError(
                f"No images in ComfyUI history for prompt_id={prompt_id}"
            )

        filename = image_info.get("filename", f"{prompt_id}.png")
        subfolder = image_info.get("subfolder", "")
        img_type = image_info.get("type", "output")

        # Download from ComfyUI's /view endpoint
        params = urllib.parse.urlencode({
            "filename": filename,
            "subfolder": subfolder,
            "type": img_type,
        })
        view_url = f"{self.config.endpoint}/view?{params}"

        if output_path:
            dest = Path(output_path)
        else:
            dest = Path(tempfile.mkdtemp()) / filename

        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(view_url, method="GET")
        with urllib.request.urlopen(req, timeout=self.config.timeout_s) as resp:
            with open(dest, "wb") as f:
                shutil.copyfileobj(resp, f)

        return str(dest)
