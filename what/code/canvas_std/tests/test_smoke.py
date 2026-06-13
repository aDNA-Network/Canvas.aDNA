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


def test_keep_floor_not_loaded_yet():
    # E0.1: the KEEP floor is declared but empty; E0.2 populates it.
    assert schema.is_floor_loaded() is False


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
