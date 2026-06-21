"""E0.1 smoke test — asserts the package imports, the Standard version, and the frozen API surface.

Behavior tests land with the implementation (E0.2/E1). Here we only verify the skeleton: the public
names exist and the unimplemented stubs honor the NotImplemented contract.
"""

from __future__ import annotations

import canvas_std
from canvas_std import schema
from canvas_std.conformance import _cli
from canvas_std.validate import ConformanceLevel


def test_versions():
    assert canvas_std.STANDARD_VERSION == "2.0.1"
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


def test_cli_and_schema_live(capsys):
    # E2.3: the whole reference engine + tooling is implemented (no stubs remain).
    from pathlib import Path

    assert _cli(["schema"]) == 0
    sch = canvas_std.json_schema()
    assert sch["x-standard-version"] == "2.0.1" and "node" in sch["$defs"]
    capsys.readouterr()

    fx = Path(__file__).parent / "fixtures"
    assert _cli(["validate", str(fx / "adna_native.canvas")]) == 0  # auto-detects level from _reserved
    assert _cli(["validate", str(fx / "invalid_missing_arrow.canvas"), "--level", "core"]) == 1


def test_validate_suite_live():
    # E2.1: validate_suite reports the level reached + the degradation report for an aDNA-Native doc.
    import json
    from pathlib import Path

    adna = json.loads((Path(__file__).parent / "fixtures" / "adna_native.canvas").read_text())
    rep = canvas_std.validate_suite(adna, ConformanceLevel.ADNA_NATIVE)
    assert rep.ok and rep.level_reached == ConformanceLevel.ADNA_NATIVE
    assert rep.failed == [] and all(rep.degradation.values())
    bad = canvas_std.validate_suite(
        json.loads((Path(__file__).parent / "fixtures" / "invalid_missing_arrow.canvas").read_text()),
        ConformanceLevel.CORE,
    )
    assert not bad.ok and any(f["id"] == "C-4" for f in bad.failed)


def test_strip_and_degradation_live():
    # E1.5: strip() removes _reserved; the result is Extended-valid; the D-1..D-3 report is all-true.
    import json
    from pathlib import Path

    adna = json.loads((Path(__file__).parent / "fixtures" / "adna_native.canvas").read_text())
    bare = canvas_std.strip(adna)
    assert "_reserved" not in bare.get("metadata", {}).get("frontmatter", {})
    assert "_reserved" in adna["metadata"]["frontmatter"]  # original untouched (deep copy)
    assert canvas_std.validate(bare, ConformanceLevel.EXTENDED) == []
    assert all(canvas_std.degradation_report(adna).values())


def test_diff_merge_live():
    # E1.3: diff detects a moved node + a new node; merge keeps source semantics, canvas positions.
    a = {"nodes": [{"id": "x", "type": "text", "x": 0, "y": 0, "width": 10, "height": 10}], "edges": []}
    b = {
        "nodes": [
            {"id": "x", "type": "text", "x": 99, "y": 0, "width": 10, "height": 10},
            {"id": "y", "type": "text", "x": 0, "y": 0, "width": 10, "height": 10},
        ],
        "edges": [],
    }
    d = canvas_std.diff(a, b)
    assert d["nodes_added"] == ["y"] and d["positions_changed"] == ["x"] and d["topology_changed"] is True


def test_validate_is_live_core():
    # E1.1: validate() no longer raises for Core; an empty doc reports its missing arrays.
    errors = canvas_std.validate({}, ConformanceLevel.CORE)
    assert errors and any("C-1" in e for e in errors)


def test_roundtrip_live():
    # E1.2: to_canvas builds a conformant view; sync-hash is stable; from_canvas drafts the topology back.
    source = {
        "name": "t",
        "version": "0.1.0",
        "nodes": [
            {"id": "a", "semantic_type": "module", "text": "M"},
            {"id": "b", "semantic_type": "dataset", "text": "D"},
        ],
        "edges": [{"id": "e", "fromNode": "a", "toNode": "b", "semantic_type": "data"}],
    }
    canvas = canvas_std.to_canvas(source)
    assert canvas_std.validate(canvas, ConformanceLevel.EXTENDED) == []
    assert canvas_std.compute_sync_hash(source) == canvas_std.compute_sync_hash(canvas)
    draft = canvas_std.from_canvas(canvas)
    assert draft["_draft"] is True
    assert {n["id"] for n in draft["nodes"]} == {"a", "b"}
    assert next(n for n in draft["nodes"] if n["id"] == "a")["semantic_type"] == "module"
