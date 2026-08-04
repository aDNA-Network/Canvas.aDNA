"""End-to-end offline — the H2 exit criteria in one test module.

Full pipeline (incl. the hybrid generate→refine chain) with zero network: fake-rendered
mini-issue pages composite; the rendered canvas revalidates aDNA-Native; sync_hash unchanged;
the input canvas byte-identical; the whole run reproducible in a different directory.
"""

from __future__ import annotations

import json

from canvas_std import compute_sync_hash

from comic_render.compose import run_compose
from comic_render.dispatch import run_generate, run_refine
from comic_render.extract import plan
from comic_render.select import run_select
from comic_render.validate import run_validate
from comic_render.writeback import run_writeback
from conftest import FIXTURE, PAGE_COUNT, PANEL_COUNT


def _full_run(canvas_path, chain="generate:fake,refine:fake@0.4"):
    manifest, mpath = plan(canvas_path, chain=chain)
    run_generate(manifest, mpath)
    run_refine(manifest, mpath)
    run_select(manifest, mpath)
    out, _ = run_writeback(manifest, mpath)
    report = run_validate(manifest, mpath)
    composed = run_compose(manifest, mpath)
    return manifest, mpath, out, report, composed


def test_hybrid_chain_end_to_end(canvas_path):
    input_bytes = canvas_path.read_bytes()
    manifest, mpath, rendered_path, report, composed = _full_run(canvas_path)

    # Exit: composited pages exist.
    assert len(composed["pages"]) == PAGE_COUNT
    for page in composed["pages"]:
        assert (mpath.parent / "runs/science_stanley_mini/pages" / page["filename"]).exists()

    # Exit: rendered canvas revalidates; sync_hash unchanged.
    assert report["ok"] and report["level_reached"] == "adna_native"
    rendered = json.loads(rendered_path.read_text())
    assert compute_sync_hash(rendered) == manifest.source_sync_hash

    # The chain was real: every file node points at a REFINED output.
    file_nodes = [n for n in rendered["nodes"] if n.get("type") == "file"]
    assert len(file_nodes) == PANEL_COUNT
    assert all("refined" in n["file"] for n in file_nodes)

    # Input immutable through the whole pipeline.
    assert canvas_path.read_bytes() == input_bytes


def test_run_is_reproducible_across_directories(tmp_path):
    """Same canvas, two independent working dirs → byte-identical images + identical topology."""
    import shutil

    runs = []
    for name in ("alpha", "beta"):
        workdir = tmp_path / name
        workdir.mkdir()
        canvas = workdir / "mini_issue.canvas"
        shutil.copy(FIXTURE, canvas)
        manifest, mpath, rendered_path, _, _ = _full_run(canvas)
        variant_bytes = {
            v: (mpath.parent / v).read_bytes()
            for p in manifest.panels
            for v in (*p.results["variants"], *p.results["refined"])
        }
        doc = json.loads(rendered_path.read_text())
        file_map = {n["id"]: n["file"] for n in doc["nodes"] if n.get("type") == "file"}
        runs.append((variant_bytes, file_map, compute_sync_hash(doc)))

    assert runs[0][0] == runs[1][0]  # every variant + refined image byte-identical
    assert runs[0][1] == runs[1][1]  # same vault-relative file wiring
    assert runs[0][2] == runs[1][2]  # same topology hash
