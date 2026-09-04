"""Diagrammatic-context authority passthrough (Blueprint P2, b2.1).

The `authority` key declares which of the three authority models a context canvas obeys
(`dual_channel` / `generator` / `view` — the axis the P1 draft pattern proposes and `adr_011` rules
for the `view` row). It is **optional**: a spec that does not declare it produces exactly the output
it produced before this feature existed, which is the property the first test pins.

⚠ The load-bearing caveat, restated where it will actually be read: `canvas_std` does NOT know this
key (F-B1-2). `validate(doc, ADNA_NATIVE)` passes whether `authority` is absent, correct, or
misspelled — so the enum check tested here is producer-side and is currently the *only* enforcement
that exists anywhere. `test_misspelled_authority_is_rejected_here_because_the_validator_cannot`
exists to keep that true; if LIP-0010 Option B is ever ratified, it becomes redundant rather than
wrong.
"""

from __future__ import annotations

import dataclasses

import pytest
from canvas_std import ConformanceLevel, validate

from diagram_generator.consume import build_diagram
from diagram_generator.model import AUTHORITY_MODELS, DiagramInput


def _reserved(doc: dict) -> dict:
    return doc["metadata"]["frontmatter"]["_reserved"]


def test_undeclared_authority_changes_nothing(diagram: DiagramInput):
    """The backward-compatibility pin: no `authority` in, no `authority` out, everything else equal."""
    doc = build_diagram(diagram)
    assert "authority" not in _reserved(doc)
    assert _reserved(doc)["context_object"]["refs"] == list(diagram.refs)


@pytest.mark.parametrize("model", sorted(AUTHORITY_MODELS))
def test_each_authority_model_round_trips_and_still_validates(diagram: DiagramInput, model: str):
    doc = build_diagram(dataclasses.replace(diagram, authority=model))
    assert _reserved(doc)["authority"] == model
    # Additive: the key does not disturb aDNA-Native conformance.
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_misspelled_authority_is_rejected_here_because_the_validator_cannot(diagram: DiagramInput):
    """F-B1-2's mitigation. `veiw` is the exact typo recorded as passing `canvas-std validate`."""
    with pytest.raises(ValueError, match="unknown authority"):
        dataclasses.replace(diagram, authority="veiw")


def test_prose_channel_appends_a_wikilink_ref(diagram: DiagramInput):
    doc = build_diagram(
        dataclasses.replace(
            diagram,
            authority="dual_channel",
            prose="what/context/context_canvas_surface_legs.md",
        )
    )
    refs = _reserved(doc)["context_object"]["refs"]
    assert refs[-1] == "[[context_canvas_surface_legs]]"
    assert refs[:-1] == list(diagram.refs)  # existing refs preserved, not replaced
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_prose_without_dual_channel_is_a_spec_error(diagram: DiagramInput):
    """A prose pair IS what dual_channel means; declaring one under another model asserts a sync
    obligation the declared authority does not carry."""
    with pytest.raises(ValueError, match="requires authority: dual_channel"):
        dataclasses.replace(diagram, authority="generator", prose="what/docs/anything.md")
    with pytest.raises(ValueError, match="requires authority: dual_channel"):
        dataclasses.replace(diagram, prose="what/docs/anything.md")


def test_authority_survives_the_yaml_surface(tmp_path):
    """The field has to arrive through `from_dict`, not only through the dataclass."""
    d = DiagramInput.from_dict(
        {
            "title": "t",
            "id": "urn:adna:canvas:diagram:t",
            "diagram_type": "flowchart",
            "authority": "dual_channel",
            "prose": "what/docs/x.md",
            "nodes": [{"id": "a"}, {"id": "b"}],
            "edges": [{"from": "a", "to": "b"}],
        }
    )
    assert d.authority == "dual_channel"
    assert _reserved(build_diagram(d))["authority"] == "dual_channel"
