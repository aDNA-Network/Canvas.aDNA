"""Diagrammatic-context axis passthrough (Blueprint P2 b2.1; SPLIT at Plumbline P1, 2026-09-11).

**Two** keys, answering two questions, which is the point:

- `authority` — *who owns the meaning?* `dual_channel` (the prose) or `view` (an authoritative
  `.lattice.yaml`; the row `adr_011` rules). Both values name an **other** channel, because that
  relationship is what `pattern_diagrammatic_context` is about.
- `production` — *how is the picture made?* `hand_authored` or `generated`.

⛩ `generator` was **removed from the authority axis** by aDNA.aDNA's HAUSSMANN R1 ruling, on Canvas's
own offer as amended by our erratum E2. It never answered the authority question. The proof is this
producer's own output: the two canvases it builds for `context_canvas_surface_legs` and `adr_004` are
`dual_channel` **and** machine-generated at once, and under the single three-value enum they declared
`dual_channel` — so a reader following the table literally received no instruction not to hand-edit
them. ⭐ The "never hand-edit; regenerate" discipline attaches to `production: generated` and to no
authority value at all.

Both keys are **optional**: a spec declaring neither produces exactly the output it produced before
either feature existed, which is the property the first test pins.

⚠ The load-bearing caveat, restated where it will actually be read: `canvas_std` knows NEITHER key
(F-B1-2, re-verified 2026-09-11). `validate(doc, ADNA_NATIVE)` passes whether they are absent,
correct, or misspelled — so the enum checks tested here are producer-side and are, with
`canvas_core.conform`, the *only* enforcement anywhere.
`test_misspelled_authority_is_rejected_here_because_the_validator_cannot` exists to keep that true;
if LIP-0010 is ratified it becomes redundant rather than wrong.
"""

from __future__ import annotations

import dataclasses

import pytest
from canvas_std import ConformanceLevel, validate

from diagram_generator.consume import build_diagram
from diagram_generator.model import AUTHORITY_MODELS, PRODUCTION_MODES, DiagramInput


def _reserved(doc: dict) -> dict:
    return doc["metadata"]["frontmatter"]["_reserved"]


def test_undeclared_axes_change_nothing(diagram: DiagramInput):
    """The backward-compatibility pin: nothing in, nothing out, everything else equal.

    An undeclared axis stays **absent**, not empty. A key written with a placeholder would be a
    false answer that every tool we ship accepts in silence.
    """
    doc = build_diagram(diagram)
    assert "authority" not in _reserved(doc)
    assert "production" not in _reserved(doc)
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
        dataclasses.replace(diagram, authority="view", prose="what/docs/anything.md")
    with pytest.raises(ValueError, match="requires authority: dual_channel"):
        dataclasses.replace(diagram, prose="what/docs/anything.md")


# --- the 2026-09-11 split -------------------------------------------------------------------


def test_generator_is_no_longer_an_authority_and_the_error_says_where_it_went(diagram: DiagramInput):
    """The one change that can break an existing spec, pinned with its migration hint.

    This test previously passed `authority="generator"` as a *valid* value (it was the third cell of
    the old enum). That it now raises is the substance of the ruling.
    """
    with pytest.raises(ValueError, match="production: generated"):
        dataclasses.replace(diagram, authority="generator")


@pytest.mark.parametrize("mode", sorted(PRODUCTION_MODES))
def test_each_production_mode_round_trips_and_still_validates(diagram: DiagramInput, mode: str):
    doc = build_diagram(dataclasses.replace(diagram, production=mode))
    assert _reserved(doc)["production"] == mode
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_misspelled_production_is_rejected_here_too(diagram: DiagramInput):
    """F-B1-2 applies to the new key exactly as it applied to the old one — and for the same reason."""
    with pytest.raises(ValueError, match="unknown production"):
        dataclasses.replace(diagram, production="hand-authored")  # hyphen, not underscore


def test_dual_channel_and_generated_are_both_sayable_at_once(diagram: DiagramInput):
    """E2's defect, now expressible — and this producer is the one that had it.

    Its own two output canvases are prose-owned AND machine-built. The old single enum forced a
    choice between saying so and saying "do not hand-edit me"; it could not say both.
    """
    doc = build_diagram(
        dataclasses.replace(
            diagram,
            authority="dual_channel",
            production="generated",
            prose="what/context/context_canvas_surface_legs.md",
        )
    )
    assert _reserved(doc)["authority"] == "dual_channel"
    assert _reserved(doc)["production"] == "generated"
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_production_survives_the_yaml_surface():
    """Same pin as `authority`: the field has to arrive through `from_dict`, not only the dataclass."""
    d = DiagramInput.from_dict(
        {
            "title": "t",
            "id": "urn:adna:canvas:diagram:t",
            "diagram_type": "flowchart",
            "production": "generated",
            "nodes": [{"id": "a"}, {"id": "b"}],
            "edges": [{"from": "a", "to": "b"}],
        }
    )
    assert d.production == "generated"
    assert _reserved(build_diagram(d))["production"] == "generated"


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
