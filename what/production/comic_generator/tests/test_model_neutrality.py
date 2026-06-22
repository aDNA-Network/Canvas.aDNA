"""A2 guardrail: the producer-side content layer stays substrate-neutral — it must not import ``canvas_std``.

The ported content modules (``model`` / ``style`` / ``prompt`` / ``panel_layout`` / ``rlhf_hints``) are pure domain
logic; the canvas-specific emission lives only in ``layout`` / ``panels`` / ``consume`` (ADR-004 two-shelf firewall).
This AST guard fails loudly if a future edit leaks the substrate into the content layer. It also asserts the IMAGE
boundary: no content module imports ComfyUI or any image-render library.
"""

from __future__ import annotations

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "comic_generator"

# The substrate-free content layer (must not see canvas_std).
CONTENT_MODULES = ["model.py", "style.py", "prompt.py", "panel_layout.py", "rlhf_hints.py"]

# No module anywhere in the package may import an image-render engine (image-boundary hard rule).
IMAGE_RENDER_FORBIDDEN = ("comfy", "comfyui", "PIL", "cv2", "torch", "diffusers", "imageio")


def _imports(path: Path) -> list[str]:
    names: list[str] = []
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.append(node.module)
    return names


def test_content_layer_has_no_canvas_std_import():
    for mod in CONTENT_MODULES:
        for name in _imports(SRC / mod):
            assert "canvas_std" not in name, f"{mod} must not import canvas_std (leaked: {name})"


def test_no_module_imports_an_image_render_engine():
    """The producer emits PROMPTS only — no pixel generation anywhere in the package."""
    for path in SRC.glob("*.py"):
        for name in _imports(path):
            top = name.split(".")[0]
            assert top not in IMAGE_RENDER_FORBIDDEN, f"{path.name} imports image-render lib {name!r}"
