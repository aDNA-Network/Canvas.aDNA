"""The inverted AST guard — "Canvas dispatches, it does not diffuse."

Mirror of ``comic_generator/tests/test_model_neutrality.py``, inverted for the bridge: HTTP
dispatch clients MAY be imported; render engines NEVER; PIL only via ``canvas_core.print``; and
``comic_generator`` is never imported (the producer hands off file-shaped). Fails loudly on any
future leak.
"""

from __future__ import annotations

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "comic_render"

# No module in the bridge may import a render engine or touch PIL directly (compose delegates to
# canvas_core.print). "comfy" here means the ComfyUI *local* packages — the H4 seam is an HTTP
# adapter living in canvas_core, never an in-process pipeline.
RENDER_ENGINE_FORBIDDEN = ("torch", "diffusers", "comfy", "comfyui", "cv2", "imageio", "PIL")

# The producer boundary: file-shaped handoff only.
PRODUCER_FORBIDDEN = ("comic_generator",)


def _imports(path: Path) -> list[str]:
    names: list[str] = []
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def _all_modules() -> list[Path]:
    modules = sorted(SRC.rglob("*.py"))
    assert len(modules) >= 12, f"guard must see the whole package, found only {len(modules)}"
    return modules


def test_no_module_imports_a_render_engine():
    for path in _all_modules():
        for name in _imports(path):
            top = name.split(".")[0]
            assert top not in RENDER_ENGINE_FORBIDDEN, (
                f"{path.relative_to(SRC)} imports render/image lib {name!r} — "
                "Canvas dispatches, it does not diffuse (PIL only via canvas_core.print)"
            )


def test_no_module_imports_the_producer():
    for path in _all_modules():
        for name in _imports(path):
            top = name.split(".")[0]
            assert top not in PRODUCER_FORBIDDEN, (
                f"{path.relative_to(SRC)} imports {name!r} — the producer hands off "
                "file-shaped via .canvas, never as an import"
            )


def test_compose_delegates_pil_to_canvas_core():
    """compose.py must reach pixels only through canvas_core.print's exporter."""
    names = _imports(SRC / "compose.py")
    assert any(n.startswith("canvas_core.print") or n == "canvas_core" for n in names)


def test_schema_b_writer_never_imported():
    """Selection records are Schema-A (canvas_core.rlhf) — the Schema-B sidecar writer is off-limits."""
    for path in _all_modules():
        source = path.read_text()
        assert "write_selection_record" not in source.replace(
            "validate_selection_record", ""
        ), f"{path.relative_to(SRC)} references ImagenWiring's Schema-B write_selection_record"
