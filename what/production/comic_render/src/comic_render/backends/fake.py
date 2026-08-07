"""The ``fake`` backend — deterministic solid-PNG stubs; the offline default everywhere in tests.

Whole-pipeline provability with zero network and zero render engines: generate writes a valid
solid-color PNG whose color is a hash of the prompt text (+ output path, so variants differ), at
the pixel size a real 2K cloud client would return for the requested aspect ratio. Refine writes a
new PNG whose color is a hash of the **seed image's bytes** + denoise — proving the chain actually
flowed data from stage to stage. Pure ``struct``/``zlib`` PNGs (``png_meta``) — no PIL anywhere.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from canvas_core.image_generation import ImagePrompt

from comic_render.png_meta import read_png_size, write_solid_png

_SIZE_BY_NAME = {"1K": 1024, "2K": 2048, "4K": 4096}


def _long_edge(image_size: str) -> int:
    if image_size in _SIZE_BY_NAME:
        return _SIZE_BY_NAME[image_size]
    try:
        return max(64, int(image_size))
    except (TypeError, ValueError):
        return 2048


def dims_for(aspect_ratio: str, image_size: str = "2K") -> tuple[int, int]:
    """Pixel dims a cloud client would return: long edge = image_size, shaped by aspect ratio."""
    long = _long_edge(image_size)
    try:
        w_part, h_part = aspect_ratio.split(":")
        w_r, h_r = float(w_part), float(h_part)
        if w_r <= 0 or h_r <= 0:
            raise ValueError
    except (ValueError, AttributeError):
        w_r = h_r = 1.0
    if w_r >= h_r:
        return long, max(1, round(long * h_r / w_r))
    return max(1, round(long * w_r / h_r)), long


def _color_from(*parts: bytes) -> tuple[int, int, int]:
    digest = hashlib.sha256(b"\x00".join(parts)).digest()
    return digest[0], digest[1], digest[2]


class FakeImageClient:
    """``ImageClient``-conformant deterministic stub (generate stage).

    ``cost_per_image`` exists so budget-cap enforcement is testable structurally; the real fake
    spend is 0.0.
    """

    model_name = "fake-solid-v0"

    def __init__(self, cost_per_image: float = 0.0) -> None:
        self.cost_per_image = cost_per_image
        self.calls: list[dict[str, Any]] = []  # audit trail for tests

    def generate_image(
        self,
        prompt: ImagePrompt | str,
        output_path: str | None = None,
        style: str = "photo",
        aspect_ratio: str = "1:1",
        image_size: str = "2K",
        model: str = "ultra",
    ) -> dict[str, Any]:
        # ImagenWiring forwards prompt TEXT (str) by documented contract — accept it silently
        # rather than routing through the deprecation shim meant for external callers.
        prompt_obj = ImagePrompt(text=prompt) if isinstance(prompt, str) else prompt
        if not output_path:
            return {"success": False, "error": "fake backend requires an explicit output_path"}
        width, height = dims_for(aspect_ratio, image_size)
        # Salt with the variant FILENAME (not the absolute path): variants differ from each other,
        # but the same canvas produces byte-identical images wherever the run directory lives.
        color = _color_from(prompt_obj.text.encode("utf-8"), Path(output_path).name.encode("utf-8"))
        write_solid_png(output_path, width, height, color)
        self.calls.append({"output_path": output_path, "aspect_ratio": aspect_ratio, "model": model})
        return {"success": True, "image_path": output_path, "adapter": "fake", "cost_usd": self.cost_per_image}


class FakeRefineClient:
    """``RefineClient``-conformant deterministic stub (refine stage).

    Output color is derived from the seed image's BYTES — a refine result can only be reproduced
    by feeding it the same generate output, which is exactly the chain property H2 must prove.
    Dimensions are preserved from the seed image (read via pure-Python IHDR parse).
    """

    model_name = "fake-refine-v0"

    def __init__(self, cost_per_image: float = 0.0) -> None:
        self.cost_per_image = cost_per_image
        self.calls: list[dict[str, Any]] = []

    def refine_image(
        self,
        seed_image: str,
        prompt: str,
        output_path: str,
        negative: str | None = None,
        denoise: float = 0.4,
        workflow: str | None = None,
        lora: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        seed_path = Path(seed_image)
        if not seed_path.exists():
            return {"success": False, "error": f"seed image missing: {seed_image}"}
        width, height = read_png_size(seed_path)
        color = _color_from(
            seed_path.read_bytes(),
            f"{denoise:.3f}".encode("ascii"),
            (negative or "").encode("utf-8"),
        )
        write_solid_png(output_path, width, height, color)
        # ``lora`` is recorded, not honored: the fake has no model to condition. Recording it is
        # what lets the chain tests assert dispatch threaded the pair-gated entry through.
        self.calls.append({"seed_image": seed_image, "output_path": output_path,
                           "denoise": denoise, "lora": lora})
        return {"success": True, "image_path": output_path, "adapter": "fake_refine", "cost_usd": self.cost_per_image}
