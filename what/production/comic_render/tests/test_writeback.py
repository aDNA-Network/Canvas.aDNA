"""Write-back — NEW file, input immutable, topology + sync block byte-identical."""

from __future__ import annotations

import json

import pytest
from canvas_std import compute_sync_hash
from canvas_std.reserved import ANCHOR_REF_KEYS

from comic_render.dispatch import run_generate
from comic_render.extract import reserved_block
from comic_render.select import run_select
from comic_render.writeback import WritebackInvariantError, run_writeback
from conftest import PANEL_COUNT, SPLASH_ID


@pytest.fixture()
def selected(planned):
    manifest, mpath, canvas_path = planned
    run_generate(manifest, mpath)
    run_select(manifest, mpath)
    return manifest, mpath, canvas_path


def test_writeback_produces_new_file_input_untouched(selected):
    manifest, mpath, canvas_path = selected
    before = canvas_path.read_bytes()
    out, summary = run_writeback(manifest, mpath)
    assert out.name == "mini_issue.rendered.canvas" and out.exists()
    assert canvas_path.read_bytes() == before  # input immutable
    assert len(summary["rendered"]) == PANEL_COUNT


def test_topology_and_sync_block_identical(selected):
    manifest, mpath, canvas_path = selected
    out, _ = run_writeback(manifest, mpath)
    source = json.loads(canvas_path.read_text())
    rendered = json.loads(out.read_text())
    assert compute_sync_hash(rendered) == compute_sync_hash(source) == manifest.source_sync_hash
    assert reserved_block(rendered)["sync"] == reserved_block(source)["sync"]
    assert len(rendered["nodes"]) == len(source["nodes"])
    assert len(rendered["edges"]) == len(source["edges"])
    assert [e["id"] for e in rendered["edges"]] == [e["id"] for e in source["edges"]]


def test_panels_flip_to_file_nodes(selected):
    manifest, mpath, _ = selected
    out, _ = run_writeback(manifest, mpath)
    rendered = json.loads(out.read_text())
    nodes = {n["id"]: n for n in rendered["nodes"]}
    ct = reserved_block(rendered)["component_types"]
    for panel in manifest.panels:
        node = nodes[panel.panel_id]
        assert node["type"] == "file"
        assert "text" not in node
        assert not node["file"].startswith("/")  # vault-relative
        assert node["file"].endswith(".png")
        assert ct[panel.panel_id]["degrades_to"] == "file"
        q = ct[panel.panel_id]["qualities"]
        assert q["status"] == "rendered"
        prov = q["render_provenance"]
        assert prov["seed"] == panel.seed
        assert prov["model"] == "fake-solid-v0"
        assert prov["selection_record"].startswith("sel_")
        assert len(prov["prompt_hash"]) == 16
        assert prov["backend_chain"] == [{"stage": "generate", "backend": "fake"}]
        assert q["image_prompt"] == panel.prompt_text  # original qualities preserved
        assert not set(q) & set(ANCHOR_REF_KEYS)


def test_writeback_idempotent_and_force(selected):
    manifest, mpath, _ = selected
    out, _ = run_writeback(manifest, mpath)
    first_bytes = out.read_bytes()
    _, again = run_writeback(manifest, mpath)
    assert again.get("unchanged") == out.name  # skip: already written
    assert out.read_bytes() == first_bytes
    _, forced = run_writeback(manifest, mpath, force=True)
    assert forced.get("written") == out.name  # rewritten (timestamps may differ)


def test_writeback_without_selection_errors(planned):
    manifest, mpath, _ = planned
    run_generate(manifest, mpath)  # dispatched but never selected
    with pytest.raises(WritebackInvariantError, match="without selections"):
        run_writeback(manifest, mpath)


def test_skip_status_panels_left_alone(selected):
    manifest, mpath, _ = selected
    manifest.panel(SPLASH_ID).status = "skip"
    out, summary = run_writeback(manifest, mpath, force=True)
    assert SPLASH_ID in summary["skipped_policy"]
    rendered = json.loads(out.read_text())
    node = {n["id"]: n for n in rendered["nodes"]}[SPLASH_ID]
    assert node["type"] == "text"  # untouched


def test_missing_selected_image_errors(selected):
    manifest, mpath, _ = selected
    victim = manifest.panels[0]
    (mpath.parent / victim.results["selection"]["selected"]).unlink()
    with pytest.raises(WritebackInvariantError, match="selected image missing"):
        run_writeback(manifest, mpath, force=True)
