"""Round-trip: the sync hash is stable across rebuilds (and a cyclic case validates, if the domain can cycle). TEMPLATE.

TODO(clone): remove the module-level skip once the producer + fixtures exist.
"""

from __future__ import annotations

import pytest

pytest.skip("scaffold template — clone, implement, remove this skip", allow_module_level=True)

from canvas_std import compute_sync_hash  # noqa: E402

from __producer__.consume import build  # noqa: E402


def test_sync_hash_is_stable(diagram_input):
    # TODO(clone): provide a domain input fixture; assert two independent builds hash identically.
    assert compute_sync_hash(build(diagram_input)) == compute_sync_hash(build(diagram_input))
