"""Manifest v0.1 — round-trip, seeds, chain shape, output precedence."""

from __future__ import annotations

import pytest

from comic_render.manifest import (
    MANIFEST_SCHEMA_VERSION,
    PanelSpec,
    RenderManifest,
    RenderStage,
    default_seed,
    manifest_path_for,
    prompt_hash,
    rendered_canvas_path_for,
)


def _panel(**over) -> PanelSpec:
    base = {
        "panel_id": "p1", "page_number": 1, "reading_index": 0, "status": "prompt_only",
        "prompt_text": "a panel", "aspect_ratio": "1:1", "target_px": {"w": 100, "h": 100},
        "seed": 1, "variant_count": 3, "output_dir": "runs/x",
    }
    base.update(over)
    return PanelSpec(**base)


def test_roundtrip_preserves_everything(tmp_path):
    m = RenderManifest(
        comic_id="x", source_canvas="x.canvas", source_sync_hash="ab" * 8,
        backend_policy={"default_chain": [{"stage": "generate", "backend": "fake"}],
                        "allow_fallback": False},
        budget_cap=1.5, register="test_reg",
        panels=[_panel(prompt_layers={"style": "s", "negative": "n"},
                       render_chain=[RenderStage("generate", "fake"),
                                     RenderStage("refine", "fake", denoise=0.4)])],
    )
    path = m.save(tmp_path / "m.json")
    loaded = RenderManifest.load(path)
    assert loaded.schema_version == MANIFEST_SCHEMA_VERSION
    assert loaded.budget_cap == 1.5 and loaded.register == "test_reg"
    p = loaded.panel("p1")
    assert p.negative == "n"
    assert [s.stage for s in p.render_chain] == ["generate", "refine"]
    assert p.render_chain[1].denoise == 0.4


def test_schema_version_mismatch_refused(tmp_path):
    m = RenderManifest(comic_id="x", source_canvas="x.canvas", source_sync_hash="ab" * 8,
                       backend_policy={})
    path = m.save(tmp_path / "m.json")
    text = path.read_text().replace(MANIFEST_SCHEMA_VERSION, "9.9")
    path.write_text(text)
    with pytest.raises(ValueError, match="schema_version"):
        RenderManifest.load(path)


def test_default_seed_deterministic_and_distinct():
    assert default_seed("comic", "p1") == default_seed("comic", "p1")
    assert default_seed("comic", "p1") != default_seed("comic", "p2")
    assert default_seed("comic", "p1") != default_seed("other", "p1")
    assert default_seed("comic", "p1") >= 0


def test_prompt_hash_is_16_hex():
    h = prompt_hash("some prompt")
    assert len(h) == 16 and int(h, 16) >= 0


def test_invalid_chain_stage_rejected():
    with pytest.raises(ValueError, match="stage"):
        RenderStage(stage="diffuse", backend="fake")


def test_final_outputs_prefers_refined():
    p = _panel()
    p.results = {"variants": ["a.png"], "refined": ["b.png"]}
    assert p.final_outputs() == ["b.png"]
    p.results = {"variants": ["a.png"]}
    assert p.final_outputs() == ["a.png"]
    p.results = {}
    assert p.final_outputs() == []


def test_dispatchable_excludes_rendered_and_skip():
    m = RenderManifest(
        comic_id="x", source_canvas="x.canvas", source_sync_hash="ab" * 8, backend_policy={},
        panels=[_panel(panel_id="a"), _panel(panel_id="b", status="rendered"),
                _panel(panel_id="c", status="skip")],
    )
    assert [p.panel_id for p in m.dispatchable()] == ["a"]


def test_sidecar_path_conventions(tmp_path):
    c = tmp_path / "issue.canvas"
    assert manifest_path_for(c).name == "issue.render_manifest.json"
    assert rendered_canvas_path_for(c).name == "issue.rendered.canvas"
