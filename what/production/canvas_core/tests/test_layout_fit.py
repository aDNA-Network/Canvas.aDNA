"""Tests for canvas_core.layout_fit — the shared producer/trap measurement.

The point of this module is *agreement*, not accuracy in isolation. So most of
these tests assert the round trip: size a node (or a container, or a label)
through ``layout_fit``, run the corresponding trap over the result, and require
**zero findings**. A test that only checked the helper's arithmetic would pass
while producer and trap continued to disagree — which is exactly the state
these helpers exist to end (F-P2-6, Blueprint P2c).
"""

from __future__ import annotations

import pytest

from canvas_core import layout_fit as lf
from canvas_core.traps import cv_group_label_01, cv_group_padding_01, cv_hierarchy_01
from canvas_core.traps import cv_lead_cost_01, cv_text_bounds_01

# --- helpers ---------------------------------------------------------------

TEXTS = [
    "Short.",
    "**Findings**\nA paragraph of prose that runs on for a while and will "
    "certainly need to wrap at any sane node width, twice over.",
    "#### Title\nBody line one.\nBody line two.\n\nAnd a third paragraph that "
    "is long enough to wrap several times at 400px of width.",
    "- one\n- two\n- three\n- four\n- five\n- six\n- seven\n- eight",
    "\n".join(f"Line {i} of a deliberately tall block of content." for i in range(20)),
]

WIDTHS = [320, 400, 620, 816, 1180]


def _text_node(nid: str, text: str, x: int, y: int, w: int, h: int) -> dict:
    return {"id": nid, "type": "text", "text": text, "x": x, "y": y,
            "width": w, "height": h}


def _group(nid: str, label: str, x: int, y: int, w: int, h: int) -> dict:
    return {"id": nid, "type": "group", "label": label, "x": x, "y": y,
            "width": w, "height": h}


# --- fit_text_height =======================================================


@pytest.mark.parametrize("text", TEXTS)
@pytest.mark.parametrize("width", WIDTHS)
def test_fit_text_height_clears_the_bounds_trap(text, width):
    """A node sized here draws zero CV-TEXT-BOUNDS-01 findings. The contract."""
    h = lf.fit_text_height(text, width)
    canvas = {"nodes": [_text_node("n1", text, 0, 0, width, h)], "edges": []}
    findings = [f for f in cv_text_bounds_01.check(canvas)
                if f.condition == "overflow"]
    assert findings == []


@pytest.mark.parametrize("text", TEXTS)
def test_one_px_short_does_overflow(text):
    """The height is tight, not merely generous — the trap fires just below it."""
    width = 400
    h = lf.fit_text_height(text, width)
    canvas = {"nodes": [_text_node("n1", text, 0, 0, width, max(1, h - 40))],
              "edges": []}
    findings = [f for f in cv_text_bounds_01.check(canvas)
                if f.condition == "overflow"]
    assert findings, "a node 40px under the fitted height should overflow"


def test_fit_text_height_honours_min_height():
    assert lf.fit_text_height("hi", 400, min_height=200) == 200


def test_fit_text_height_is_integer_and_deterministic():
    a = lf.fit_text_height(TEXTS[1], 620)
    b = lf.fit_text_height(TEXTS[1], 620)
    assert a == b and isinstance(a, int)


def test_fit_text_height_degenerate_width():
    assert lf.fit_text_height("anything", 0) == 0


def test_fits_agrees_with_fit_text_height():
    for text in TEXTS:
        h = lf.fit_text_height(text, 620)
        assert lf.fits(text, 620, h)


# --- leads and headings ====================================================


def test_heading_uses_h4():
    assert lf.heading("Executive summary") == "#### Executive summary"


def test_heading_clears_both_traps_together():
    """The whole reason #### exists here: h1/h2/h3 trip lead-cost, bold trips
    hierarchy, #####/###### pass only by not being headings (F-P2-3)."""
    text = lf.heading("Overview") + "\nBody copy under the title."
    width = 620
    node = _text_node("t", text, 10, 10, width, lf.fit_text_height(text, width))
    canvas = {"nodes": [_group("g", "Overview", 0, 0, width + 100, 900), node],
              "edges": []}
    assert cv_lead_cost_01.check(canvas) == []
    assert [f for f in cv_hierarchy_01.check(canvas)
            if f.condition == "title_slot_missing"] == []


@pytest.mark.parametrize("bad_lead", ["# T", "## T", "### T"])
def test_the_leads_we_rejected_do_trip_lead_cost(bad_lead):
    text = f"{bad_lead}\nBody."
    node = _text_node("t", text, 10, 10, 620, lf.fit_text_height(text, 620))
    canvas = {"nodes": [_group("g", "G", 0, 0, 720, 900), node], "edges": []}
    assert cv_lead_cost_01.check(canvas), f"{bad_lead!r} should cost too much"


def test_bold_lead_trips_hierarchy_not_lead_cost():
    """The other half of the contradiction — and why the fix hint had to change."""
    text = "**Title**\nBody."
    node = _text_node("t", text, 10, 10, 620, lf.fit_text_height(text, 620))
    canvas = {"nodes": [_group("g", "G", 0, 0, 720, 900), node], "edges": []}
    assert cv_lead_cost_01.check(canvas) == []
    assert [f for f in cv_hierarchy_01.check(canvas)
            if f.condition == "title_slot_missing"]


@pytest.mark.parametrize("src,want", [
    ("## Findings\nbody", "#### Findings\nbody"),
    ("# One", "#### One"),
    ("###### Deep\nbody", "#### Deep\nbody"),
    ("#### Already\nbody", "#### Already\nbody"),
    ("**Bold**\nbody", "**Bold**\nbody"),
    ("plain body", "plain body"),
    ("", ""),
])
def test_fit_lead(src, want):
    assert lf.fit_lead(src) == want


def test_fit_lead_never_invents_a_heading():
    assert not lf.is_titled(lf.fit_lead("just prose"))


def test_is_titled_follows_the_hierarchy_trap():
    assert lf.is_titled("##### Five") is True   # a heading to hierarchy...
    assert lf.lead_kind("##### Five") == "plain"  # ...but 'plain' to the cost model
    assert lf.is_titled("**Bold**") is False


# --- groups ================================================================


@pytest.mark.parametrize("bbox", [(400, 300), (1440, 600), (3000, 2200), (120, 80)])
def test_fit_group_size_clears_the_padding_trap(bbox):
    """Both sub-conditions: aggregate fill AND per-node edge distance."""
    bb_w, bb_h = bbox
    pad = 80
    gw, gh = lf.fit_group_size(bb_w, bb_h, pad)
    child = _text_node("c", "x", pad, pad, bb_w, bb_h)
    canvas = {"nodes": [_group("g", "G", 0, 0, gw, gh), child], "edges": []}
    assert cv_group_padding_01.check(canvas) == []


def test_fit_group_size_scales_with_content():
    """A fixed pad cannot satisfy a ratio (F-P2-4) — the container must grow."""
    small_w, _ = lf.fit_group_size(400, 300, 80)
    big_w, _ = lf.fit_group_size(4000, 300, 80)
    assert small_w - 400 <= big_w - 4000, "padding must widen as content widens"


def test_fit_group_size_raises_a_thin_pad_to_the_edge_floor():
    gw, gh = lf.fit_group_size(200, 200, pad=4)
    assert (gw - 200) / 2 >= lf.MIN_EDGE_PAD
    assert (gh - 200) / 2 >= lf.MIN_EDGE_PAD


def test_fit_group_size_is_integer():
    gw, gh = lf.fit_group_size(333.3, 777.7, 80)
    assert isinstance(gw, int) and isinstance(gh, int)


@pytest.mark.parametrize("label", [
    "Adaptive aDNA Harness for the Undiagnosed — R01 Proposal",
    "aDNA Canvas Standard v2.0.0 — One-Page Brief",
    "ALL CAPS SECTION LABEL",
    "Short",
])
def test_fit_group_label_min_width_clears_the_label_trap(label):
    _, min_w = lf.fit_group_label(label, width=100)
    canvas = {"nodes": [_group("g", label, 0, 0, min_w, 400)], "edges": []}
    assert cv_group_label_01.check(canvas) == []


def test_fit_group_label_min_width_is_tight():
    label = "Adaptive aDNA Harness for the Undiagnosed — R01 Proposal"
    _, min_w = lf.fit_group_label(label, width=100)
    canvas = {"nodes": [_group("g", label, 0, 0, min_w - 30, 400)], "edges": []}
    assert cv_group_label_01.check(canvas), "just under min_width should truncate"


def test_all_caps_labels_need_more_room():
    _, mixed = lf.fit_group_label("Section overview here", 0)
    _, caps = lf.fit_group_label("SECTION OVERVIEW HERE", 0)
    assert caps > mixed


def test_label_fits_agrees_with_the_trap():
    label = "A moderately long group label for testing"
    _, min_w = lf.fit_group_label(label, 0)
    assert lf.label_fits(label, min_w)
    assert not lf.label_fits(label, min_w - 40)


def test_empty_label_is_vacuously_fine():
    assert lf.fit_group_label("", 500) == ("", 0)
    assert lf.label_fits("", 10)
