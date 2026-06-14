"""E0.1 smoke test — asserts the package imports, the Standard version, and the frozen API surface.

Behavior tests land with the implementation (E0.2/E1). Here we only verify the skeleton: the public
names exist and the unimplemented stubs honor the NotImplemented contract.
"""

from __future__ import annotations

import pytest

import canvas_std
from canvas_std import schema
from canvas_std.validate import ConformanceLevel


def test_versions():
    assert canvas_std.STANDARD_VERSION == "2.0.0"
    assert canvas_std.__version__ == "0.1.0"
    assert "v5.6.6" in canvas_std.UPSTREAM_BASELINE


def test_public_api_surface_exists():
    for name in (
        "validate",
        "strip",
        "to_canvas",
        "from_canvas",
        "compute_sync_hash",
        "diff",
        "merge",
        "validate_suite",
    ):
        assert callable(getattr(canvas_std, name)), name


def test_conformance_levels():
    assert {lvl.value for lvl in ConformanceLevel} == {"core", "extended", "adna_native"}


def test_keep_floor_loaded():
    # E0.2: the verbatim KEEP floor is populated.
    assert schema.is_floor_loaded() is True
    assert schema.VALID_NODE_TYPES == frozenset({"text", "file", "group", "link"})
    assert schema.VALID_COLORS == frozenset({"0", "1", "2", "3", "4", "5", "6"})
    assert None in schema.VALID_SHAPES and "database" in schema.VALID_SHAPES
    assert schema.VALID_ENDS == frozenset({"none", "arrow"})
    assert schema.NODE_REQUIRED_FIELDS == ("id", "type", "x", "y", "width", "height")
    assert schema.EDGE_REQUIRED_FIELDS == ("id", "fromNode", "fromSide", "toNode", "toSide")


def test_lattice_profile_verbatim():
    assert len(schema.TYPE_MAPPING) == 8 and len(schema.EDGE_TYPE_MAPPING) == 5
    assert schema.TYPE_MAPPING["module"] == {"color": "4", "shape": "predefined-process", "node_type": "file"}
    assert schema.TYPE_MAPPING["reasoning"] == {"color": "6", "shape": "diamond", "node_type": "text"}
    assert schema.EDGE_TYPE_MAPPING["optional"] == {
        "path_style": "dotted",
        "arrow": "triangle-outline",
        "from_end": None,
        "to_end": "arrow",
    }
    # every directed edge profile ends in an arrow (toEnd:"arrow" invariant)
    assert all(e["to_end"] == "arrow" for e in schema.EDGE_TYPE_MAPPING.values())
    # all profile tokens stay within the §6 enums (so Extended-degradation holds)
    for entry in schema.TYPE_MAPPING.values():
        assert entry["shape"] in schema.VALID_SHAPES
        assert entry["color"] is None or entry["color"] in schema.VALID_COLORS
        assert entry["node_type"] in schema.VALID_NODE_TYPES


@pytest.mark.parametrize(
    "call",
    [
        lambda: canvas_std.validate({}, ConformanceLevel.CORE),
        lambda: canvas_std.strip({}),
        lambda: canvas_std.to_canvas({}),
        lambda: canvas_std.from_canvas({}),
        lambda: canvas_std.compute_sync_hash({}),
    ],
)
def test_stubs_raise_not_implemented(call):
    with pytest.raises(NotImplementedError):
        call()
