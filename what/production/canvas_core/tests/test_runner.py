"""Tests for canvas_core.traps.runner.run_all_traps (M-V1-2-E-01 S2 D3 fold-in).

Covers the **trap_kwargs passthrough added in S2: ``run_all_traps`` accepts
arbitrary keyword arguments and forwards each one to the per-trap ``check()``
only if the trap's signature declares it (``inspect.signature`` filter).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.runner import run_all_traps

PIL_AVAILABLE = True
try:
    from PIL import Image  # noqa: F401
except Exception:
    PIL_AVAILABLE = False


def _canvas(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "edges": []}


def _group_node(id: str, x: float, y: float, w: float, h: float, label: str = "") -> dict:
    return {"id": id, "type": "group", "label": label,
            "x": x, "y": y, "width": w, "height": h}


def _image_node(id: str, x: float, y: float, w: float, h: float, file: str = "img.png") -> dict:
    return {"id": id, "type": "file", "file": file,
            "x": x, "y": y, "width": w, "height": h}


def _write_image(path: Path, w: int, h: int) -> None:
    from PIL import Image
    img = Image.new("RGB", (w, h), color=(128, 128, 128))
    img.save(path, format="PNG")


@pytest.mark.skipif(not PIL_AVAILABLE, reason="PIL required for asset_root threading test")
def test_run_all_traps_threads_asset_root_to_aspect_ratio_trap(tmp_path):
    """asset_root reaches CV-IMAGE-ASPECT-RATIO-01 via **trap_kwargs.

    Source 100x100 (1:1) rendered 125x100 (1.25) → aspect drift 0.25 → high
    severity per ASPECT_DRIFT_HIGH=0.15 threshold. The trap can only see the
    source dimensions if ``asset_root`` is threaded through the runner.
    """
    img_path = tmp_path / "a.png"
    _write_image(img_path, 100, 100)
    canvas = _canvas([
        _group_node("g1", 0, 0, 1000, 1000),
        _image_node("i1", 100, 100, 125, 100, file="a.png"),
    ])

    findings = run_all_traps(canvas, asset_root=tmp_path)

    aspect_drifts = [
        f for f in findings
        if f.trap_id == "CV-IMAGE-ASPECT-RATIO-01" and f.condition == "aspect_drift"
    ]
    assert len(aspect_drifts) == 1
    assert aspect_drifts[0].severity == "high"


def test_run_all_traps_filters_unknown_kwargs():
    """Unknown kwargs are silently dropped by the per-trap inspect.signature filter."""
    canvas = _canvas([
        _group_node("g1", 0, 0, 1000, 1000),
    ])

    findings = run_all_traps(
        canvas,
        foo_bar_unknown_kwarg_xyz="ignored",
        another_made_up_kwarg=42,
    )

    runner_errors = [f for f in findings if f.condition == "runner_error"]
    assert runner_errors == []
