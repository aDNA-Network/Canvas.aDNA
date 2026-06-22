"""Components: every component class is in the taxonomy; every degrades_to is a baseline type."""

from __future__ import annotations

from canvas_std.reserved import BASELINE_TYPES, COMPONENT_CLASSES


def test_classes_and_degrades_to_valid(doc):
    cts = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    for cid, c in cts.items():
        assert c["class"] in COMPONENT_CLASSES, f"{cid}: class {c.get('class')!r} not in taxonomy"
        assert c["degrades_to"] in BASELINE_TYPES, f"{cid}: degrades_to {c.get('degrades_to')!r} not baseline"


def test_image_class_is_used_for_image_panels(doc):
    cts = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    image_components = [c for c in cts.values() if c["class"] == "image"]
    assert image_components, "the thread fixture has an image panel -> expected an image-class component"
    for c in image_components:
        assert c["degrades_to"] == "text"
        assert c["qualities"]["image_prompt"]  # the prompt rides as metadata
