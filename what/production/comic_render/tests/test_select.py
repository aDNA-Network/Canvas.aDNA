"""Select — Schema-A records only, F-36 relative paths, idempotency."""

from __future__ import annotations

import json

import pytest
from canvas_core.rlhf import SelectionRecord, validate_selection_record

from comic_render.dispatch import run_generate, run_refine
from comic_render.select import run_select
from conftest import PANEL_COUNT


def _dispatched(planned):
    manifest, mpath, canvas_path = planned
    run_generate(manifest, mpath)
    return manifest, mpath, canvas_path


def test_select_writes_valid_schema_a_records(planned):
    manifest, mpath, _ = _dispatched(planned)
    summary = run_select(manifest, mpath)
    assert len(summary["selected"]) == PANEL_COUNT
    base = mpath.parent
    for panel in manifest.panels:
        sel = panel.results["selection"]
        record_path = base / sel["record_path"]
        assert record_path.exists() and record_path.name.startswith("sel_")
        record = SelectionRecord.from_dict(json.loads(record_path.read_text()))
        assert validate_selection_record(record) == []  # Schema-A clean, F-36 included
        assert record.register == manifest.register
        assert len(record.variants) == 3
        assert record.variants[0].cost_usd == 0.0 and record.variants[0].seed == panel.seed
        assert not record.variants[0].image_path.startswith("/")  # F-36 vault-relative
        assert sel["selected"] == panel.results["variants"][0]  # pick_index 0
    # audit log appended beside the records
    month_dirs = list((base / "runs/science_stanley_mini/selections").iterdir())
    assert any((d / "audit.log").exists() for d in month_dirs if d.is_dir())


def test_no_schema_b_sidecars_anywhere(planned):
    manifest, mpath, _ = _dispatched(planned)
    run_select(manifest, mpath)
    # ImagenWiring's Schema-B sidecar is {item_id}.selection.json — the bridge must never emit it
    assert not list(mpath.parent.rglob("*.selection.json"))


def test_select_is_idempotent(planned):
    manifest, mpath, _ = _dispatched(planned)
    first = run_select(manifest, mpath)
    again = run_select(manifest, mpath)
    assert again["selected"] == [] and len(again["skipped"]) == PANEL_COUNT
    assert again["records"] == []
    # records from the first run still referenced
    assert manifest.panels[0].results["selection"]["selection_record"] in first["records"]


def test_select_over_refined_outputs(chain_planned):
    manifest, mpath, _ = chain_planned
    run_generate(manifest, mpath)
    run_refine(manifest, mpath)
    run_select(manifest, mpath)
    for panel in manifest.panels:
        assert "refined" in panel.results["selection"]["selected"]


def test_pick_index_bounds(planned):
    manifest, mpath, _ = _dispatched(planned)
    with pytest.raises(ValueError, match="pick_index"):
        run_select(manifest, mpath, pick_index=7)


def test_select_before_dispatch_errors(planned):
    manifest, mpath, _ = planned
    with pytest.raises(RuntimeError, match="no outputs"):
        run_select(manifest, mpath)
