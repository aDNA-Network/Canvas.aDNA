"""Model-neutrality: ``model.py`` imports NO ``canvas_std`` (the substrate-free layer).  TEMPLATE.

This AST-guard is load-bearing — keep it. TODO(clone): rename the ``__producer__`` path segment + remove the skip.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

pytest.skip("scaffold template — clone, rename the path segment, remove this skip", allow_module_level=True)


def test_model_imports_no_canvas_std():
    src = pathlib.Path(__file__).resolve().parents[1] / "src" / "__producer__" / "model.py"
    tree = ast.parse(src.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [getattr(node, "module", None) or ""] + [a.name for a in getattr(node, "names", [])]
            assert not any("canvas_std" in (n or "") for n in names), "model.py must not import canvas_std"
