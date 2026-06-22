"""Degradation: stripping _reserved yields a valid baseline (Obsidian) canvas; no out-of-enum baseline leaks. TEMPLATE.

TODO(clone): remove the module-level skip once the producer + fixtures exist.
"""

from __future__ import annotations

import pytest

pytest.skip("scaffold template — clone, implement, remove this skip", allow_module_level=True)

from canvas_std import ConformanceLevel, degradation_report, strip, validate  # noqa: E402


def test_degradation_report_all_pass(doc):
    assert degradation_report(doc) == {"D-1": True, "D-2": True, "D-3": True}


def test_strip_is_core_and_extended_valid(doc):
    bare = strip(doc)
    assert validate(bare, ConformanceLevel.CORE) == []
    assert validate(bare, ConformanceLevel.EXTENDED) == []


def test_strip_removes_reserved(doc):
    bare = strip(doc)
    assert "_reserved" not in bare.get("metadata", {}).get("frontmatter", {})


def test_no_out_of_enum_shape(doc):
    # If your domain carries rich shapes, they ride _reserved.qualities.shape — NEVER a baseline styleAttributes.shape
    # (VALID_SHAPES is small; an out-of-enum baseline shape fails E-2/D-2). Delete if not applicable.
    for n in doc["nodes"]:
        assert "shape" not in n.get("styleAttributes", {}), f"node {n['id']} leaked a styleAttributes.shape"
