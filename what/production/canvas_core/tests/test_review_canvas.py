"""Halftone HR — review-surface builder tests (`canvas_core.rlhf.review_canvas`).

The shared tmp-vault fixture (conftest: manifest + real minimal PNGs + hidden-properties app.json) exercises:
adna_native self-gate, the interaction overlay shape, exact-aspect integer geometry, the partially-failed-
manifest reality (missing `output_path` → pattern-derived; missing file → excluded), the verdict-preserving
overwrite refusal, and a clean geometry-trap run.
"""

from __future__ import annotations

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cli import check_canvas
from canvas_std import ConformanceLevel, validate_interaction, validate_suite
from conftest import build_review as _build


def test_build_validates_adna_native_and_derives_missing_paths(vault):
    root, paths = _build(vault)
    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    assert report.level_reached is ConformanceLevel.ADNA_NATIVE, report.failed
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    assert validate_interaction(reserved, doc) == []
    # var_1 (explicit path) + var_2 (pattern-derived) included; var_9 (file absent) excluded.
    assert set(paths.sidecars) == {"var_1", "var_2"}
    files = {n["file"] for n in doc["nodes"] if n.get("type") == "file"}
    assert any("anchor_var_2_wide.png" in f for f in files)


def test_overlay_shape_and_state(vault):
    _, paths = _build(vault)
    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    block = doc["metadata"]["frontmatter"]["_reserved"]["interaction"]
    assert block["interaction_version"] == "1.0"
    affs = block["affordances"]
    assert len(affs) == 8 * 2  # 8 controls × 2 variants
    node_ids = {n["id"] for n in doc["nodes"]}
    for aid, entry in affs.items():
        assert entry["anchor"] in node_ids and entry["anchor"].endswith("_sidecar")
        if entry["kind"] == "choice":
            assert entry["options"]
        else:
            assert "options" not in entry or entry["options"] is None
    assert sorted(block["state"]["open"]) == ["var_1.verdict", "var_2.verdict"]
    assert block["responses"] == []


def test_geometry_ints_and_exact_aspect(vault):
    _, paths = _build(vault)
    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in doc["nodes"]}
    for n in doc["nodes"]:
        for key in ("x", "y", "width", "height"):
            assert isinstance(n[key], int), f"{n['id']}.{key} is not int"
    img1, img2 = nodes["var_1_image"], nodes["var_2_image"]
    assert img1["width"] * 1 == img1["height"] * 1          # 1:1 exact
    assert img2["width"] * 6 == img2["height"] * 11         # 11:6 exact
    header = next(n for n in doc["nodes"] if n["id"] == "header")
    assert header["text"].startswith("**")                  # CV-LEAD-COST-01: no '#' lead


def test_traps_clean_on_the_pilot(vault):
    root, paths = _build(vault)
    findings, resolved = check_canvas(str(paths.canvas), vault_root=str(root))
    bad = [f for f in findings if getattr(f, "severity", "") in ("high", "critical")]
    assert bad == [], [f"{f.trap_id}: {f.message}" for f in bad]


def test_refuses_to_overwrite_verdict_bearing_sidecar(vault):
    root, paths = _build(vault)
    sp = paths.sidecars["var_1"]
    text = sp.read_text(encoding="utf-8")
    sp.write_text(text.replace("verdict: null", "verdict: approve", 1), encoding="utf-8")
    with pytest.raises(FileExistsError, match="operator signal"):
        _build(vault)
    _build(vault, force=True)  # explicit force overwrites
    assert "verdict: null" in sp.read_text(encoding="utf-8")
