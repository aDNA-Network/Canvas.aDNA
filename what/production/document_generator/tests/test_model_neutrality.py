"""E4.2 guardrail: the producer-side domain model stays substrate-neutral — it must not import ``canvas_std``.

The contracts live in ``model.py`` as pure domain data; the canvas-specific emission lives only in ``consume.py`` /
``blocks.py`` (ADR-004 two-shelf firewall). This AST guard fails loudly if a future edit leaks the substrate in.
"""

from __future__ import annotations

import ast
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1] / "src" / "document_generator" / "model.py"


def test_model_has_no_canvas_std_import():
    tree = ast.parse(MODEL.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all("canvas_std" not in a.name for a in node.names), "model.py must not import canvas_std"
        elif isinstance(node, ast.ImportFrom):
            assert not (node.module and "canvas_std" in node.module), "model.py must not import from canvas_std"
