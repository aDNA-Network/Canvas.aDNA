"""Components: every component class is in the taxonomy; every degrades_to is a baseline type."""

from __future__ import annotations

from canvas_std.reserved import BASELINE_TYPES, COMPONENT_CLASSES


def test_classes_and_degrades_to_valid(doc):
    cts = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    for cid, c in cts.items():
        assert c["class"] in COMPONENT_CLASSES, f"{cid}: class {c.get('class')!r} not in taxonomy"
        assert c["degrades_to"] in BASELINE_TYPES, f"{cid}: degrades_to {c.get('degrades_to')!r} not baseline"
