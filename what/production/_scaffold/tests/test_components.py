"""Components: every component class' ``degrades_to`` is a baseline type.  TEMPLATE.

TODO(clone): remove the module-level skip once the producer + fixtures exist.
"""

from __future__ import annotations

import pytest

pytest.skip("scaffold template — clone, implement, remove this skip", allow_module_level=True)

BASELINE_TYPES = {"text", "file", "group", "link"}


def test_degrades_to_in_baseline(doc):
    cts = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    for cid, c in cts.items():
        assert c["degrades_to"] in BASELINE_TYPES, f"{cid}: degrades_to '{c.get('degrades_to')}' not baseline"
