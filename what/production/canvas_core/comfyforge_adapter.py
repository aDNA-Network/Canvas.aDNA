"""ComfyForge Tier 1 adapter — direct HTTP API client for ComfyUI on Anduril.

Implements the ImageClient Protocol for ComfyUI running on the Anduril
RTX 3090 (Nebula mesh, 10.42.0.8:8188). Tier 1 is a style-transfer
experimental path, NOT an alternative production backend (ADR 003).

API pattern per coord note § Tier 1 contract:
    POST /prompt          — submit workflow JSON → {"prompt_id": "<UUID>"}
    GET  /history/{id}    — poll for completion → download image
    GET  /system_stats    — health check (circuit-breaker probe)
    POST /upload/image    — stage a seed image for img2img (refine; H4)

Circuit-breaker escalation:
    Anduril (primary) → Mac MPS (fallback) → Imagen (v1.0 safety net)

**Refine (img2img), added at Halftone H4** — the hybrid backend the operator locked is a *chain*:
a cloud backend generates, ComfyUI refines. ``refine_image`` is that second stage, conforming to
``comic_render.backends.base.RefineClient``. It lives here, not in the bridge, by the bridge's own
boundary rule: "Canvas dispatches, it does not diffuse" — the H4 seam is an HTTP adapter in
``canvas_core``; the bridge module is a thin manifest-shaped binding.

Migrated: N/A (new in M-3-05)
"""

from __future__ import annotations

import hashlib
import json
import logging
import mimetypes
import shutil
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
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
# Refine (img2img) defaults — H4
# ---------------------------------------------------------------------------

# Denoise strength for the refine stage. <1.0 is what makes it img2img rather than txt2img:
# the seed image survives, the style is unified over it.
DEFAULT_REFINE_DENOISE = 0.4

# The negative channel travels as its own CLIPTextEncode node — NEVER concatenated into the
# positive prompt (H1 split the channel precisely so chain backends could honor it, roadmap R6).
DEFAULT_REFINE_NEGATIVE = "blurry, low quality, distorted, watermark, text"

# Upscale model for the optional refine upscale stage. Named in the comic_panel_refine ask.
# Corrected 2026-08-07 from a guessed "RealESRGAN_x2.pth" to the weight actually installed on L1 —
# a name the mocks happily accepted and no real server would have.
DEFAULT_UPSCALE_MODEL = "RealESRGAN_x4plus.pth"


def _node_sort_key(node_id: str) -> tuple[int, int | str]:
    """ComfyUI node ids are numeric strings — order them numerically, not lexically ("10" < "6")."""
    return (0, int(node_id)) if node_id.isdigit() else (1, node_id)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class ComfyForgeConfig:
    """Configuration for the Tier 1 ComfyForge adapter."""

    endpoint: str = "http://10.42.0.8:8188"
    timeout_s: int = 30                  # per-HTTP-request timeout (submit · upload · download)
    # Wall-clock budget for a generation to finish, polled via /history. MUST NOT be timeout_s:
    # sampling takes minutes where an HTTP round-trip takes milliseconds (see _poll_history).
    generation_timeout_s: int = 600
    failover_ms: int = 2000
    poll_interval_s: float = 2.0
    style_config_path: str | None = None
    checkpoint: str = "sd_xl_base_1.0.safetensors"
    sampler: str = "euler"
    scheduler: str = "normal"
    steps: int = 20
    cfg_scale: float = 7.0
    # Directory of named ComfyUI workflow templates (e.g. ComfyUI.aDNA's what/workflows/). When a
    # refine call names a workflow that resolves here, the template is patched; otherwise the
    # built-in img2img graph is used. Read-only consumption of the owning vault (Rule 10).
    workflow_dir: str | None = None


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
    # RefineClient conformance (img2img — Halftone H4)
    # ------------------------------------------------------------------

    def refine_image(
        self,
        seed_image: str,
        prompt: str,
        output_path: str | None = None,
        negative: str | None = None,
        denoise: float = DEFAULT_REFINE_DENOISE,
        workflow: str | None = None,
        lora: dict[str, Any] | None = None,
        upscale: bool = False,
        seed: int | None = None,
    ) -> dict[str, Any]:
        """Refine an existing image via ComfyUI img2img.

        The second stage of the hybrid render chain: ``seed_image`` (a cloud-generated panel)
        is uploaded, encoded to latent, and re-sampled at ``denoise`` < 1.0 so the composition
        survives while style unifies. Conforms to ``RefineClient``; the extra ``lora`` /
        ``upscale`` / ``seed`` arguments are a superset the bridge binding may pass through.

        ``lora`` (optional): ``{"name": str, "strength_model": float, "strength_clip": float}``.
        ``workflow`` (optional): a named template resolved under ``config.workflow_dir`` — e.g.
        Vulcan's ``comic_panel_refine``. When it does not resolve, the built-in graph is used and
        the return records which was taken, so a missing upstream workflow degrades rather than
        fails.

        Returns ``{"success": True, "image_path": str, ...}`` or
        ``{"success": False, "error": str}`` — the same shape as ``generate_image``.
        """
        seed_path = Path(seed_image)
        if not seed_path.exists():
            return {
                "success": False,
                "error": f"seed_image not found: {seed_image}",
                "adapter": "comfyforge_tier1",
            }

        if not self.health_check():
            return {
                "success": False,
                "error": "comfyui_unreachable",
                "adapter": "comfyforge_tier1",
                "endpoint": self.config.endpoint,
            }

        try:
            uploaded = self._upload_image(seed_path)
            template, source = self._resolve_refine_workflow(workflow)
            if template is not None:
                graph = self._patch_workflow_template(
                    template,
                    prompt=self._apply_style(prompt, "photo"),
                    negative=negative or DEFAULT_REFINE_NEGATIVE,
                    seed_filename=uploaded,
                    denoise=denoise,
                    seed=seed if seed is not None else self._refine_seed(prompt, seed_path),
                )
            else:
                graph = self._build_img2img_workflow(
                    prompt=prompt,
                    negative=negative,
                    seed_filename=uploaded,
                    denoise=denoise,
                    seed=seed if seed is not None else self._refine_seed(prompt, seed_path),
                    lora=lora,
                    upscale=upscale,
                    filename_prefix=f"canvas_refine_{Path(output_path).stem}"
                    if output_path else "canvas_refine",
                )
            prompt_id = self._submit_workflow(graph)
            history = self._poll_history(prompt_id)
            image_path = self._download_image(history, prompt_id, output_path)
            return {
                "success": True,
                "image_path": image_path,
                "adapter": "comfyforge_tier1",
                "prompt_id": prompt_id,
                "stage": "refine",
                "denoise": denoise,
                "workflow_source": source,
            }
        except Exception as e:
            logger.error("ComfyForge refine failed: %s", e)
            return {
                "success": False,
                "error": str(e),
                "adapter": "comfyforge_tier1",
                "stage": "refine",
            }

    @staticmethod
    def _refine_seed(prompt: str, seed_path: Path) -> int:
        """Deterministic refine seed from (prompt, seed-image name).

        Unlike ``_build_workflow``'s wall-clock seed, refine is part of a reproducible bridge run:
        the same panel variant refined twice must ask for the same sampling.
        """
        digest = hashlib.sha256(f"{prompt}:{seed_path.name}".encode()).digest()
        return int.from_bytes(digest[:4], "big")

    def _resolve_refine_workflow(
        self, workflow: str | None
    ) -> tuple[dict[str, Any] | None, str]:
        """Resolve a named workflow template → (graph, source-label).

        ``(None, "builtin")`` when no name was given or the name does not resolve — the built-in
        img2img graph then applies. A named-but-missing workflow is a degradation, not an error:
        the upstream workflow (Vulcan's ``comic_panel_refine``) may not exist yet.
        """
        if not workflow:
            return None, "builtin"
        if not self.config.workflow_dir:
            logger.info("workflow %r requested but no workflow_dir configured — built-in graph",
                        workflow)
            return None, "builtin"
        candidate = Path(self.config.workflow_dir).expanduser() / f"{workflow}.json"
        if not candidate.exists():
            logger.info("workflow %r not found at %s — built-in graph", workflow, candidate)
            return None, "builtin"
        return json.loads(candidate.read_text()), f"template:{workflow}"

    def _patch_workflow_template(
        self,
        template: dict[str, Any],
        *,
        prompt: str,
        negative: str,
        seed_filename: str,
        denoise: float,
        seed: int,
    ) -> dict[str, Any]:
        """Patch a named workflow template's inputs by node class.

        Convention (the contract asked of Vulcan): the FIRST ``CLIPTextEncode`` is positive, the
        second negative; ``LoadImage`` takes the uploaded seed; ``KSampler`` takes denoise + seed.
        Everything else in the template — checkpoint, LoRA stack, upscale — is the workflow
        author's business and is left untouched.
        """
        graph = json.loads(json.dumps(template))  # never mutate the caller's template
        text_nodes = [
            k for k in sorted(graph, key=_node_sort_key)
            if graph[k].get("class_type") == "CLIPTextEncode"
        ]
        if text_nodes:
            graph[text_nodes[0]].setdefault("inputs", {})["text"] = prompt
        if len(text_nodes) > 1:
            graph[text_nodes[1]].setdefault("inputs", {})["text"] = negative
        for node in graph.values():
            class_type = node.get("class_type")
            if class_type == "LoadImage":
                node.setdefault("inputs", {})["image"] = seed_filename
            elif class_type == "KSampler":
                inputs = node.setdefault("inputs", {})
                inputs["denoise"] = denoise
                inputs["seed"] = seed
        return graph

    def _build_img2img_workflow(
        self,
        prompt: str,
        negative: str | None,
        seed_filename: str,
        denoise: float,
        seed: int,
        lora: dict[str, Any] | None = None,
        upscale: bool = False,
        filename_prefix: str = "canvas_refine",
    ) -> dict[str, Any]:
        """Build the built-in SDXL img2img graph (the fallback when no template resolves).

        Shape mirrors ``_build_workflow`` — checkpoint → (optional LoRA) → CLIP encodes →
        KSampler → VAE decode → (optional upscale) → save — with ``LoadImage``/``VAEEncode``
        supplying the latent instead of ``EmptyLatentImage``, and ``denoise`` < 1.0.
        """
        styled_prompt = self._apply_style(prompt, "photo")
        negative_text = negative or DEFAULT_REFINE_NEGATIVE

        model_source: list[Any] = ["4", 0]
        clip_source: list[Any] = ["4", 1]

        workflow: dict[str, Any] = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "seed": seed,
                    "steps": self.config.steps,
                    "cfg": self.config.cfg_scale,
                    "sampler_name": self.config.sampler,
                    "scheduler": self.config.scheduler,
                    "denoise": denoise,
                    "model": model_source,
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["11", 0],
                },
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {"ckpt_name": self.config.checkpoint},
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": styled_prompt, "clip": clip_source},
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": negative_text, "clip": clip_source},
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
            },
            "10": {
                "class_type": "LoadImage",
                "inputs": {"image": seed_filename, "upload": "image"},
            },
            "11": {
                "class_type": "VAEEncode",
                "inputs": {"pixels": ["10", 0], "vae": ["4", 2]},
            },
        }

        if lora and lora.get("name"):
            workflow["14"] = {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": lora["name"],
                    "strength_model": float(lora.get("strength_model", 1.0)),
                    "strength_clip": float(lora.get("strength_clip", 1.0)),
                    "model": ["4", 0],
                    "clip": ["4", 1],
                },
            }
            workflow["3"]["inputs"]["model"] = ["14", 0]
            workflow["6"]["inputs"]["clip"] = ["14", 1]
            workflow["7"]["inputs"]["clip"] = ["14", 1]

        save_source: list[Any] = ["8", 0]
        if upscale:
            workflow["12"] = {
                "class_type": "UpscaleModelLoader",
                "inputs": {"model_name": DEFAULT_UPSCALE_MODEL},
            }
            workflow["13"] = {
                "class_type": "ImageUpscaleWithModel",
                "inputs": {"upscale_model": ["12", 0], "image": ["8", 0]},
            }
            save_source = ["13", 0]

        # Per-output prefix, not a constant: ComfyUI caches by graph identity, so two refines that
        # differ only in destination path would be byte-identical graphs — the server returns
        # `execution_cached` with EMPTY outputs and the download finds nothing. (The deterministic
        # refine seed makes that collision the common case, not the rare one.) Varying the prefix
        # also makes server-side outputs traceable back to the panel variant that asked for them.
        workflow["9"] = {
            "class_type": "SaveImage",
            "inputs": {"images": save_source, "filename_prefix": filename_prefix},
        }
        return workflow

    def _upload_image(self, path: Path) -> str:
        """``POST /upload/image`` (multipart) → the server-side filename a LoadImage references.

        Hand-rolled multipart: the adapter is stdlib-only by design (no ``requests`` dependency
        on the production shelf).
        """
        boundary = f"----adnaCanvas{uuid.uuid4().hex}"
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        parts: list[bytes] = []
        for name, value in (("type", "input"), ("overwrite", "true")):
            parts.append(
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n"
                f"{value}\r\n".encode()
            )
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; "
            f"filename=\"{path.name}\"\r\nContent-Type: {content_type}\r\n\r\n".encode()
        )
        parts.append(path.read_bytes())
        parts.append(f"\r\n--{boundary}--\r\n".encode())
        body = b"".join(parts)

        req = urllib.request.Request(
            f"{self.config.endpoint}/upload/image",
            data=body,
            method="POST",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        with urllib.request.urlopen(req, timeout=self.config.timeout_s) as resp:
            data = json.loads(resp.read())
        name = data.get("name")
        if not name:
            raise RuntimeError(f"No filename in /upload/image response: {data}")
        subfolder = data.get("subfolder") or ""
        return f"{subfolder}/{name}" if subfolder else name

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
        """Poll /history/{prompt_id} until generation completes or times out.

        The deadline is ``generation_timeout_s`` — a **wall-clock sampling budget**, not the
        per-request HTTP timeout. Conflating the two silently caps every real generation at 30s:
        an SDXL img2img at 20 steps takes ~35s of sampling alone on MPS, so the adapter abandoned
        jobs the server went on to finish successfully. (Found 2026-08-07 by the H4 live smoke
        against a real ComfyUI; mocked polls return instantly and can never surface it.)
        """
        url = f"{self.config.endpoint}/history/{prompt_id}"
        budget = self.config.generation_timeout_s
        deadline = time.monotonic() + budget

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
            f"ComfyUI generation timed out after {budget}s (prompt_id={prompt_id})"
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
                f"No images in ComfyUI history for prompt_id={prompt_id} — if the run reported "
                "success with every node 'execution_cached', an identical graph was already "
                "executed and the server emitted no new outputs (vary the SaveImage "
                "filename_prefix or the seed)"
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
