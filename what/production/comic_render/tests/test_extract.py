"""Plan/extract — topology reading, staleness guard, contract errors."""

from __future__ import annotations

import json

import pytest
from canvas_std import compute_sync_hash

from comic_render.extract import StaleManifestError, check_freshness, parse_chain, plan
from comic_render.manifest import RenderManifest
from conftest import PAGE_COUNT, PANEL_COUNT, SPLASH_ID


def test_plan_extracts_all_panels(planned):
    manifest, _, canvas_path = planned
    assert len(manifest.panels) == PANEL_COUNT
    assert manifest.comic_id == "science_stanley_mini"
    assert manifest.source_canvas == canvas_path.name
    doc = json.loads(canvas_path.read_text())
    assert manifest.source_sync_hash == compute_sync_hash(doc)


def test_page_numbers_follow_sequence_chain(planned):
    manifest, _, _ = planned
    pages = {p.page_number for p in manifest.panels}
    assert pages == set(range(1, PAGE_COUNT + 1))
    splash = manifest.panel(SPLASH_ID)
    assert splash.page_number == 1 and splash.reading_index == 0
    # page 2 carries three panels in reading order p0 -> p1 -> p2
    page2 = sorted(
        (p for p in manifest.panels if p.page_number == 2), key=lambda p: p.reading_index
    )
    assert [p.panel_id for p in page2] == [
        "spread0_page1_p0", "spread0_page1_p1", "spread0_page1_p2",
    ]


def test_prompt_layers_negative_channel_survives(planned):
    manifest, _, _ = planned
    splash = manifest.panel(SPLASH_ID)
    assert splash.prompt_text  # producer contract: non-empty image_prompt
    assert splash.prompt_layers and "negative" in splash.prompt_layers
    assert splash.negative == splash.prompt_layers["negative"]


def test_target_px_from_geometry(planned):
    manifest, _, _ = planned
    splash = manifest.panel(SPLASH_ID)  # 663x1025 canvas units @300dpi
    assert splash.target_px == {"w": 1989, "h": 3075}


def test_seeds_are_deterministic_per_panel(planned):
    manifest, _, canvas_path = planned
    again, _ = plan(canvas_path, force=True)
    assert {p.panel_id: p.seed for p in manifest.panels} == {
        p.panel_id: p.seed for p in again.panels
    }
    assert len({p.seed for p in manifest.panels}) == PANEL_COUNT  # all distinct


def test_replan_keeps_fresh_manifest_state(planned):
    manifest, mpath, canvas_path = planned
    manifest.panels[0].results["variants"] = ["marker.png"]
    manifest.save(mpath)
    kept, _ = plan(canvas_path)  # unchanged canvas → resumable state preserved
    assert kept.panels[0].results.get("variants") == ["marker.png"]
    rebuilt, _ = plan(canvas_path, force=True)
    assert rebuilt.panels[0].results == {}


def test_topology_change_triggers_replan_and_staleness_error(planned):
    manifest, _, canvas_path = planned
    doc = json.loads(canvas_path.read_text())
    doc["nodes"].append({"id": "intruder", "type": "text", "text": "x",
                         "x": 0, "y": 0, "width": 10, "height": 10})
    canvas_path.write_text(json.dumps(doc))
    with pytest.raises(StaleManifestError):
        check_freshness(manifest, doc)
    replanned, _ = plan(canvas_path)  # stale → rebuilt against the new topology
    assert replanned.source_sync_hash == compute_sync_hash(doc)
    assert replanned.source_sync_hash != manifest.source_sync_hash


def test_missing_image_prompt_fails_fast(canvas_path):
    doc = json.loads(canvas_path.read_text())
    ct = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    ct[SPLASH_ID]["qualities"]["image_prompt"] = ""
    canvas_path.write_text(json.dumps(doc))
    with pytest.raises(ValueError, match="image_prompt"):
        plan(canvas_path)


def test_parse_chain_forms():
    stages = parse_chain("generate:fake,refine:comfy@0.35")
    assert [(s.stage, s.backend, s.denoise) for s in stages] == [
        ("generate", "fake", None), ("refine", "comfy", 0.35),
    ]
    with pytest.raises(ValueError):
        parse_chain("generate")  # no backend
    with pytest.raises(ValueError):
        parse_chain("")


def test_custom_plan_options_recorded(canvas_path):
    manifest, _ = plan(canvas_path, chain="generate:fake,refine:fake@0.4",
                       variant_count=2, budget_cap=9.99, register="reg_x")
    assert manifest.budget_cap == 9.99 and manifest.register == "reg_x"
    assert all(p.variant_count == 2 for p in manifest.panels)
    assert [s["stage"] for s in manifest.backend_policy["default_chain"]] == ["generate", "refine"]
    assert all(len(p.render_chain) == 2 for p in manifest.panels)


def test_loaded_manifest_equals_planned(planned):
    manifest, mpath, _ = planned
    assert RenderManifest.load(mpath).to_dict() == manifest.to_dict()


def test_plan_lifts_qualities_characters_into_panelspec(canvas_path):
    """H5 seam: the producer's `qualities.characters` asset channel rides into `PanelSpec.characters`."""
    doc = json.loads(canvas_path.read_text())
    ct = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    assets = [{"name": "stanley", "reference_images": ["ScienceStanley.aDNA/refs/anchor.png"]}]
    ct[SPLASH_ID]["qualities"]["characters"] = assets
    canvas_path.write_text(json.dumps(doc))
    manifest, _ = plan(canvas_path)
    assert manifest.panel(SPLASH_ID).characters == assets
    assert all(p.characters == [] for p in manifest.panels if p.panel_id != SPLASH_ID)
