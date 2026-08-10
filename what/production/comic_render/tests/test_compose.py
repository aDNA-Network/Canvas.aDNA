"""Compose — the R5 geometry shim golden (±1 px) + page export via PrintExporter."""

from __future__ import annotations

import json

import pytest
from canvas_core.print import BLEED_PX_H, BLEED_PX_W, BLEED_WIDTH, PrintExporter

from comic_render.compose import build_shim, run_compose
from comic_render.dispatch import run_generate
from comic_render.extract import load_canvas
from comic_render.manifest import rendered_canvas_path_for
from comic_render.select import run_select
from comic_render.vault import resolve_vault_root
from comic_render.writeback import run_writeback
from conftest import PAGE_COUNT, SPLASH_ID


@pytest.fixture()
def written(planned):
    manifest, mpath, canvas_path = planned
    run_generate(manifest, mpath)
    run_select(manifest, mpath)
    run_writeback(manifest, mpath)
    return manifest, mpath, canvas_path


def _specs_by_page(manifest, mpath):
    rendered = rendered_canvas_path_for(mpath.parent / manifest.source_canvas)
    doc = load_canvas(rendered)
    shim = build_shim(doc, manifest, vault_root=resolve_vault_root(rendered))
    exporter = PrintExporter(shim, mpath.parent / "unused", issue_name=manifest.comic_id)
    return {s.page_number: s for s in exporter.build_page_specs()}


def test_placement_golden(written):
    """The R5 remap: canvas-absolute 663x1025 pages → 687.5x1050 bleed print canvas, ±1 px."""
    manifest, mpath, _ = written
    specs = _specs_by_page(manifest, mpath)
    assert set(specs) == set(range(1, PAGE_COUNT + 1))

    # Page 1: the full-page splash promotes to a true full-bleed placement.
    (splash,) = specs[1].panel_placements
    assert splash.panel_id == SPLASH_ID and splash.is_bleed
    assert (splash.x, splash.y, splash.width, splash.height) == (0, 0, BLEED_PX_W, BLEED_PX_H)

    # Page 2: three standard panels. Expected px = ((node − page) + 12.5 units) × 3.
    # p0: node (856,189) 638x326 on page (831,176) → (37.5, 25.5) u → (112.5, 76.5) px.
    by_id = {p.panel_id: p for p in specs[2].panel_placements}
    p0 = by_id["spread0_page1_p0"]
    assert abs(p0.x - 112) <= 1 and abs(p0.y - 76) <= 1
    assert abs(p0.width - 1914) <= 1 and abs(p0.height - 978) <= 1
    p1 = by_id["spread0_page1_p1"]  # node (856,525) 314x326 → (37.5, 361.5) u
    assert abs(p1.x - 112) <= 1 and abs(p1.y - 1084) <= 1
    assert abs(p1.width - 942) <= 1 and abs(p1.height - 978) <= 1
    p2 = by_id["spread0_page1_p2"]  # node (1180,525) → (361.5, 361.5) u
    assert abs(p2.x - 1084) <= 1 and abs(p2.y - 1084) <= 1

    # No standard placement may escape the bleed canvas.
    for spec in specs.values():
        for pl in spec.panel_placements:
            assert 0 <= pl.x and pl.x + pl.width <= BLEED_PX_W + 1
            assert 0 <= pl.y and pl.y + pl.height <= BLEED_PX_H + 1


def test_compose_exports_all_pages(written):
    manifest, mpath, _ = written
    result = run_compose(manifest, mpath)
    pages = result["pages"]
    assert len(pages) == PAGE_COUNT
    for page in pages:
        assert page["width"] == BLEED_PX_W and page["height"] == BLEED_PX_H
        assert page["filename"] == f"science_stanley_mini_{page['page_number']:02d}.jpg"
    files = sorted(f.name for f in (mpath.parent / "runs/science_stanley_mini/pages").glob("*.jpg"))
    assert len(files) == PAGE_COUNT


def test_splash_dpi_warning_propagates(written):
    """R7: the 2K fake source composites at ~195 DPI on the bleed page — warned in the export."""
    manifest, mpath, _ = written
    result = run_compose(manifest, mpath)
    page1 = next(p for p in result["pages"] if p["page_number"] == 1)
    assert any("effective DPI" in w for w in page1["warnings"])


def test_compose_requires_writeback(planned):
    manifest, mpath, _ = planned
    with pytest.raises(FileNotFoundError, match="write-back first"):
        run_compose(manifest, mpath)


def _spread_doc(manifest, mpath):
    """The rendered canvas with the splash widened into a two-page spread."""
    rendered = rendered_canvas_path_for(mpath.parent / manifest.source_canvas)
    doc = json.loads(rendered.read_text())
    node = next(n for n in doc["nodes"] if n["id"] == SPLASH_ID)
    node["width"] = 1400  # wider than 1.5 bleed pages → a two-page spread
    return doc, rendered


def test_spread_panel_composes_at_h6(written):
    """H6 inverts the H2 deferral: a spread builds instead of raising.

    Was ``test_spread_panels_deferred_to_h6`` (asserted NotImplementedError).
    """
    manifest, mpath, _ = written
    doc, rendered = _spread_doc(manifest, mpath)
    shim = build_shim(doc, manifest, vault_root=resolve_vault_root(rendered))

    panel = shim.get_panel(SPLASH_ID)
    assert panel is not None
    # Emitted at the COMBINED bleed width so the placement marks it is_spread.
    assert panel.width == BLEED_WIDTH * 2
    assert panel.bleed is True

    exporter = PrintExporter(shim, mpath.parent / "unused", issue_name=manifest.comic_id)
    placement = next(
        p for s in exporter.build_page_specs() for p in s.panel_placements
        if p.panel_id == SPLASH_ID
    )
    assert placement.is_spread is True
    assert placement.width == BLEED_PX_W * 2
    assert placement.height == BLEED_PX_H


def test_spread_export_splits_into_two_page_halves(written, tmp_path):
    """export_spread is REACHABLE from export_all (it never was before H6).

    The pre-H6 bug this pins: export_all only ever called export_page, so a
    spread exported as two independent pages that each fit the whole spread
    image into one page's width — squashed, silently.
    """
    manifest, mpath, _ = written
    doc, rendered = _spread_doc(manifest, mpath)
    shim = build_shim(doc, manifest, vault_root=resolve_vault_root(rendered))

    exporter = PrintExporter(shim, tmp_path / "pages", issue_name=manifest.comic_id, cmyk=False)
    results = exporter.export_all()

    # Page count is unchanged — a spread is still two printed pages.
    assert len(results) == PAGE_COUNT
    halves = [r for r in results if r.is_spread_half]
    assert len(halves) == 2, "the spread must yield exactly two halves"
    assert [h.page_number for h in halves] == [1, 2]
    for h in halves:
        assert (h.width, h.height) == (BLEED_PX_W, BLEED_PX_H)

    report = (tmp_path / "pages" / "export_report.md").read_text()
    assert "Spread halves" in report and "2" in report


def test_spread_on_last_page_exports_rather_than_dropping(written, tmp_path):
    """A spread with no partner page is a warning, not a lost page."""
    manifest, mpath, _ = written
    rendered = rendered_canvas_path_for(mpath.parent / manifest.source_canvas)
    doc = json.loads(rendered.read_text())
    last_panel_id = manifest.panels[-1].panel_id
    node = next(n for n in doc["nodes"] if n["id"] == last_panel_id)
    node["width"] = 1400
    shim = build_shim(doc, manifest, vault_root=resolve_vault_root(rendered))

    exporter = PrintExporter(shim, tmp_path / "pages", issue_name=manifest.comic_id, cmyk=False)
    results = exporter.export_all()

    assert len(results) == PAGE_COUNT  # nothing dropped
    assert any("no following page" in w for r in results for w in r.warnings)
