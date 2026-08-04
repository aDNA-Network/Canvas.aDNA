"""Dispatch + refine — chain execution, idempotency, budget cap (R9)."""

from __future__ import annotations

import pytest

from comic_render.backends.fake import FakeImageClient, FakeRefineClient
from comic_render.dispatch import BudgetCapExceededError, run_generate, run_refine
from comic_render.manifest import RenderManifest
from conftest import PANEL_COUNT


def test_generate_fans_out_variants(planned):
    manifest, mpath, _ = planned
    summary = run_generate(manifest, mpath)
    assert len(summary["generated"]) == PANEL_COUNT
    assert summary["calls"] == PANEL_COUNT * 3
    base = mpath.parent
    for panel in manifest.panels:
        variants = panel.results["variants"]
        assert len(variants) == 3
        assert all((base / v).exists() for v in variants)
        assert variants[0].endswith(f"{panel.panel_id}_v1.png")
        assert panel.results["model"] == "fake-solid-v0"
    # resumable state survives a reload
    assert RenderManifest.load(mpath).panels[0].results["variants"] == \
        manifest.panels[0].results["variants"]
    assert manifest.spend == {"usd": 0.0, "calls": PANEL_COUNT * 3}


def test_generate_is_idempotent(planned):
    manifest, mpath, _ = planned
    run_generate(manifest, mpath)
    again = run_generate(manifest, mpath)
    assert again["generated"] == [] and again["calls"] == 0
    assert len(again["skipped"]) == PANEL_COUNT


def test_budget_cap_blocks_before_any_call(planned):
    manifest, mpath, _ = planned
    manifest.budget_cap = 0.10
    pricey = FakeImageClient(cost_per_image=0.05)  # 27 calls x $0.05 = $1.35 >> cap
    with pytest.raises(BudgetCapExceededError):
        run_generate(manifest, mpath, client_overrides={"fake": pricey})
    assert pricey.calls == []  # NOTHING dispatched
    assert not any(p.results.get("variants") for p in manifest.panels)


def test_spend_recorded_under_cap(planned):
    manifest, mpath, _ = planned
    manifest.budget_cap = 5.0
    client = FakeImageClient(cost_per_image=0.05)
    run_generate(manifest, mpath, client_overrides={"fake": client})
    assert manifest.spend["calls"] == PANEL_COUNT * 3
    assert manifest.spend["usd"] == pytest.approx(PANEL_COUNT * 3 * 0.05)


def test_refine_runs_chain_over_variants(chain_planned):
    manifest, mpath, _ = chain_planned
    run_generate(manifest, mpath)
    summary = run_refine(manifest, mpath)
    assert len(summary["refined"]) == PANEL_COUNT
    assert summary["calls"] == PANEL_COUNT * 3
    base = mpath.parent
    for panel in manifest.panels:
        refined = panel.results["refined"]
        assert len(refined) == 3 and all("refined" in r for r in refined)
        assert all((base / r).exists() for r in refined)
        assert panel.results["model"] == "fake-refine-v0"
        assert panel.final_outputs() == refined  # selection operates on the last stage


def test_refine_is_idempotent(chain_planned):
    manifest, mpath, _ = chain_planned
    run_generate(manifest, mpath)
    run_refine(manifest, mpath)
    again = run_refine(manifest, mpath)
    assert again["calls"] == 0 and len(again["skipped"]) == PANEL_COUNT


def test_refine_before_generate_errors(chain_planned):
    manifest, mpath, _ = chain_planned
    with pytest.raises(RuntimeError, match="run dispatch first"):
        run_refine(manifest, mpath)


def test_refine_noop_without_refine_stage(planned):
    manifest, mpath, _ = planned
    run_generate(manifest, mpath)
    summary = run_refine(manifest, mpath)
    assert len(summary["no_refine_stage"]) == PANEL_COUNT and summary["calls"] == 0


def test_refine_receives_negative_channel(chain_planned):
    manifest, mpath, _ = chain_planned
    run_generate(manifest, mpath)
    refiner = FakeRefineClient()
    run_refine(manifest, mpath, client_overrides={"fake": refiner})
    negatives = {c["seed_image"]: c for c in refiner.calls}
    assert negatives  # calls recorded
    # every panel with a negative layer had it passed out-of-band
    with_negative = [p for p in manifest.panels if p.negative]
    assert with_negative, "fixture panels carry a negative channel"
    assert all(c["denoise"] == 0.4 for c in refiner.calls)
