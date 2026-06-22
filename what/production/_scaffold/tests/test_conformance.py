"""Conformance: validates at aDNA-Native; exactly one canonical surface; component_types resolve.  TEMPLATE.

TODO(clone): remove the module-level skip once the producer + fixtures exist.
"""

from __future__ import annotations

import pytest

pytest.skip("scaffold template — clone, implement, remove this skip", allow_module_level=True)

from canvas_std import ConformanceLevel, validate, validate_suite  # noqa: E402


def test_validates_adna_native(doc):
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_suite_meets_declared(doc):
    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    assert report.failed == []
    assert report.meets_declared is True
    assert report.ok is True


def test_one_canonical_surface_resolves(doc):
    pl = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]
    canonical = [s for s in pl["surfaces"] if s.get("role") == "canonical"]
    assert len(canonical) == 1  # the A-5 load-bearing constraint
    assert canonical[0]["id"] in {n["id"] for n in doc["nodes"]}


def test_component_types_resolve(doc):
    node_ids = {n["id"] for n in doc["nodes"]}
    assert set(doc["metadata"]["frontmatter"]["_reserved"]["component_types"]).issubset(node_ids)
