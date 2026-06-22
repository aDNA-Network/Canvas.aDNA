"""Model-neutrality: ``model.py`` imports NO ``canvas_std`` (the substrate-free layer). Load-bearing."""

from __future__ import annotations

import ast
import pathlib


def test_model_imports_no_canvas_std():
    src = pathlib.Path(__file__).resolve().parents[1] / "src" / "letter_generator" / "model.py"
    tree = ast.parse(src.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [getattr(node, "module", None) or ""] + [a.name for a in getattr(node, "names", [])]
            assert not any("canvas_std" in (n or "") for n in names), "model.py must not import canvas_std"
