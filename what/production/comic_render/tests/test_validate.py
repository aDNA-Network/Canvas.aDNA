"""Stage-6 gate — conformance + degradation + file existence + sync hash + DPI warnings."""

from __future__ import annotations

import json

import pytest

from comic_render.dispatch import run_generate
from comic_render.select import run_select
from comic_render.validate import BridgeValidationError, run_validate
from comic_render.writeback import run_writeback
from conftest import PANEL_COUNT, SPLASH_ID


@pytest.fixture()
def written(planned):
    manifest, mpath, _canvas_path = planned
    run_generate(manifest, mpath)
    run_select(manifest, mpath)
    out, _ = run_writeback(manifest, mpath)
    return manifest, mpath, out


def test_green_path(written):
    manifest, mpath, _ = written
    report = run_validate(manifest, mpath)
    assert report["ok"] is True
    assert report["level_reached"] == "adna_native"
    assert report["degradation"] == {"D-1": True, "D-2": True, "D-3": True}
    assert report["files_checked"] == PANEL_COUNT


def test_splash_dpi_warning_surfaces(written):
    """R7: a 2K source on a full-page target is ~199.8 DPI — warned, never silent, never fatal."""
    manifest, mpath, _ = written
    report = run_validate(manifest, mpath)
    assert any(SPLASH_ID in w and "effective DPI" in w for w in report["warnings"])


def test_missing_rendered_canvas_errors(planned):
    manifest, mpath, _ = planned
    with pytest.raises(BridgeValidationError, match="write-back first"):
        run_validate(manifest, mpath)


def test_missing_file_target_fails_gate(written):
    manifest, mpath, out = written
    rendered = json.loads(out.read_text())
    file_nodes = [n for n in rendered["nodes"] if n.get("type") == "file"]
    victim = mpath.parent / file_nodes[0]["file"]
    victim.unlink()
    with pytest.raises(BridgeValidationError, match="missing target"):
        run_validate(manifest, mpath)


def test_topology_tamper_fails_gate(written):
    manifest, mpath, out = written
    rendered = json.loads(out.read_text())
    rendered["nodes"].append({"id": "intruder", "type": "text", "text": "x",
                              "x": 0, "y": 0, "width": 10, "height": 10})
    out.write_text(json.dumps(rendered))
    with pytest.raises(BridgeValidationError, match="sync_hash|conformance"):
        run_validate(manifest, mpath)


def test_broken_reserved_fails_conformance(written):
    manifest, mpath, out = written
    rendered = json.loads(out.read_text())
    ct = rendered["metadata"]["frontmatter"]["_reserved"]["component_types"]
    ct[SPLASH_ID]["degrades_to"] = "hologram"  # not a baseline type → A-3 failure
    out.write_text(json.dumps(rendered))
    with pytest.raises(BridgeValidationError, match="conformance"):
        run_validate(manifest, mpath)
