"""Degradation: stripping _reserved yields a valid baseline (Obsidian) canvas; isStartNode survives; panels degrade."""

from __future__ import annotations

from canvas_std import ConformanceLevel, degradation_report, strip, validate

from comic_generator.consume import build_comic


def test_degradation_report_all_pass(doc):
    assert degradation_report(doc) == {"D-1": True, "D-2": True, "D-3": True}


def test_strip_is_core_and_extended_valid(doc):
    bare = strip(doc)
    assert validate(bare, ConformanceLevel.CORE) == []
    assert validate(bare, ConformanceLevel.EXTENDED) == []


def test_strip_removes_reserved(doc):
    bare = strip(doc)
    assert "_reserved" not in bare.get("metadata", {}).get("frontmatter", {})


def test_isStartNode_survives_strip_on_first_page(doc):
    """`isStartNode` is a baseline Advanced-Canvas field — it must survive the _reserved strip on page 0."""
    bare = strip(doc)
    start = [n for n in bare["nodes"] if n.get("isStartNode") is True]
    assert len(start) == 1


def test_panels_degrade_to_file_or_text(doc):
    """Every `image` panel degrades to a baseline `file` (rendered) or `text` (prompt-only) node."""
    by_id = {n["id"]: n for n in doc["nodes"]}
    comps = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    image_panels = {nid: e for nid, e in comps.items() if e["class"] == "image"}
    assert image_panels, "expected at least one image panel"
    for nid, e in image_panels.items():
        assert e["degrades_to"] in ("file", "text")
        assert by_id[nid]["type"] == e["degrades_to"]  # the baseline node matches its degrades_to


def test_no_out_of_enum_style_on_baseline_nodes(doc):
    """The image prompt / spatial layout / aspect ride ONLY in _reserved.qualities — no baseline overload."""
    for n in doc["nodes"]:
        assert "shape" not in n.get("styleAttributes", {}), f"node {n['id']} leaked a styleAttributes.shape"
        # the rich panel payload must not appear as baseline node fields
        assert "image_prompt" not in n
        assert "aspect_ratio" not in n


def test_degradation_holds_for_minimal_comic():
    """A minimal comic with no instance overlays still degrades cleanly (mechanism-defaults path)."""
    doc = build_comic(
        _mini()
    )
    assert degradation_report(doc) == {"D-1": True, "D-2": True, "D-3": True}
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def _mini():
    from comic_generator.model import ComicInput, Page, Panel

    return ComicInput(
        title="Mini",
        id="urn:adna:canvas:comic:mini",
        version="0.1.0",
        pages=(
            Page(number=1, layout_type="splash", panels=(Panel(panel_type="splash", scene="A scene."),)),
            Page(number=2, layout_type="grid", panels=(
                Panel(panel_type="action", scene="Another.", row=0, col=0),
                Panel(panel_type="dialogue", scene="More.", row=0, col=1),
            )),
        ),
    )
