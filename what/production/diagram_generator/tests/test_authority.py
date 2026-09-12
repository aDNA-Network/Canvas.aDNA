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

⛩ **The load-bearing caveat this docstring used to carry has EXPIRED, exactly as it predicted.** It
read: *"`canvas_std` knows NEITHER key (F-B1-2)… the enum checks tested here are producer-side and are,
with `canvas_core.conform`, the only enforcement anywhere… if LIP-0010 is ratified
[`test_misspelled_authority_is_rejected_here_because_the_validator_cannot`] becomes redundant rather
than wrong."*

**LIP-0010 was ratified 2026-09-11 and both keys are now validated by `canvas_std` as A-8 (Standard
v2.4.0).** So:

- The frozensets here are **no longer a second source of truth** — `AUTHORITY_MODELS` / `PRODUCTION_MODES`
  are imported from `canvas_std.reserved`, pinned by
  `test_the_axis_values_are_the_standards_own_sets_not_a_local_copy`.
- The misspelling test is now **redundant rather than wrong**, as forecast, and is kept deliberately:
  it pins that the producer still fails **early**, at `__post_init__`, instead of emitting a canvas for
  the validator to reject later. Its *name* is now a historical artifact — the validator can.
- A-8 is **asymmetric**: `authority` requires `production`; `production` alone is legal. The producer
  enforces the same asymmetry, because the Standard would otherwise reject what it emits.
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
    doc = build_diagram(dataclasses.replace(diagram, authority=model, production="generated"))
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
            production="generated",
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
    """As for `authority`: A-8 validates it since v2.4.0; this pins the earlier producer-side refusal."""
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
            "production": "generated",
            "prose": "what/docs/x.md",
            "nodes": [{"id": "a"}, {"id": "b"}],
            "edges": [{"from": "a", "to": "b"}],
        }
    )
    assert d.authority == "dual_channel"
    assert d.production == "generated"
    assert _reserved(build_diagram(d))["authority"] == "dual_channel"


# --- A-8's asymmetry, enforced at the spec surface (Standard v2.4.0, Gridline P1) ------------------
def test_authority_without_production_is_refused_at_build_time(diagram: DiagramInput):
    """⛩ The Standard rejects this pair as A-8, so the producer must not be able to emit it.

    Caught the day A-8 landed: four call sites in this vault's own tests declared `authority` with no
    `production`, and the new validator turned them red. That is the LIP's promised value arriving —
    the Standard finding under-specification two of our modules had been happy to write.
    """
    with pytest.raises(ValueError, match="requires `production` whenever `authority` is present"):
        dataclasses.replace(diagram, authority="view")


def test_production_without_authority_is_allowed(diagram: DiagramInput):
    """⭐ The converse is legal, and that asymmetry is the corrected form of the rule (F-GL-5).

    A diagram no other channel owns declares only how it is made. A symmetric "two keys or neither"
    would have forced an invented authority value here — the defect `conform.py` names as "passing a
    value to make a number go green".
    """
    doc = build_diagram(dataclasses.replace(diagram, production="hand_authored"))
    assert "authority" not in _reserved(doc)
    assert _reserved(doc)["production"] == "hand_authored"
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_the_axis_values_are_the_standards_own_sets_not_a_local_copy():
    """⛩ De-duplicated 2026-09-11: these were locally-declared frozensets while `canvas_std` knew
    neither key. It knows both now (A-8), so a second copy here could only drift from it."""
    from canvas_std.reserved import AUTHORITY_VALUES, PRODUCTION_VALUES

    assert AUTHORITY_MODELS is AUTHORITY_VALUES
    assert PRODUCTION_MODES is PRODUCTION_VALUES
