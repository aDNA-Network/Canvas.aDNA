"""Diagram types: one fixture per type — each builds, validates aDNA-Native, and has the right edge kinds.

Also exercises the ported Mermaid generators (the derived ``code`` node): every type produces a recognized,
balanced Mermaid source, and the source mentions every node (render-fidelity twin of the native graph).
"""

from __future__ import annotations

import pytest
from canvas_std import ConformanceLevel, validate

from diagram_generator import mermaid
from diagram_generator.consume import build_diagram

# expected panel_link edge kind per diagram type (gantt = sequence; everything else = dependency)
_EXPECTED_KIND = {
    "flowchart": "dependency",
    "sequence": "dependency",
    "class_diagram": "dependency",
    "state_diagram": "dependency",
    "gantt": "sequence",
}

_MERMAID_HEADER = {
    "flowchart": "flowchart",
    "sequence": "sequenceDiagram",
    "class_diagram": "classDiagram",
    "state_diagram": "stateDiagram-v2",
    "gantt": "gantt",
}


@pytest.mark.parametrize("dtype", sorted(_EXPECTED_KIND))
def test_each_type_validates_adna_native(dtype, all_types):
    doc = build_diagram(all_types[dtype])
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == [], dtype


@pytest.mark.parametrize("dtype", sorted(_EXPECTED_KIND))
def test_each_type_edge_kind(dtype, all_types):
    doc = build_diagram(all_types[dtype])
    pl = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]
    kinds = {m["kind"] for m in pl["edges"].values()}
    assert kinds == {_EXPECTED_KIND[dtype]}, (dtype, kinds)


@pytest.mark.parametrize("dtype", sorted(_MERMAID_HEADER))
def test_each_type_mermaid_source(dtype, all_types):
    d = all_types[dtype]
    src = mermaid.mermaid_for(d)
    assert src.startswith(_MERMAID_HEADER[dtype]), (dtype, src.split(chr(10))[0])
    assert mermaid.validate(src) == [], (dtype, mermaid.validate(src))
    # the derived source references every native node (render-fidelity: no dropped node)
    for n in d.nodes:
        assert n.id in src, f"{dtype}: node {n.id} missing from Mermaid source"


def test_class_diagram_folds_members_and_relation_glyph(class_diagram):
    src = mermaid.mermaid_for(class_diagram)
    assert "class Animal {" in src
    assert "+name: str" in src  # a member attribute
    assert "Dog --|> Animal" in src  # inherits -> --|> glyph


def test_gantt_durations_present(gantt):
    src = mermaid.mermaid_for(gantt)
    assert "gantt" in src and "dateFormat" in src
    assert "design : 2d" in src and "build : 3d" in src  # durations carried (rigor/quantitative)
