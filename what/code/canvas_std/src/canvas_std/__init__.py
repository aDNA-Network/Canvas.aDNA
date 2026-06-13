"""adna-canvas-std — reference implementation of the aDNA Canvas Standard.

Standard-bearer tooling (Option P): validators, round-trip converters, conformance harness.
E0.1 skeleton — the public API surface is frozen here; behavior is filled by E0.2 (KEEP floor)
and E1 (implementation). See the normative specs in Canvas.aDNA/what/specs/.
"""

from __future__ import annotations

__version__ = "0.1.0"  # package version
STANDARD_VERSION = "2.0.0"  # the aDNA Canvas Standard version this package implements (distinct, per P2)
UPSTREAM_BASELINE = "Advanced Canvas v5.6.6 + JSON Canvas 1.0"  # PIN-A (p1_fork_baseline §1)

from canvas_std.conformance import ConformanceReport, validate_suite
from canvas_std.roundtrip import compute_sync_hash, diff, from_canvas, merge, to_canvas
from canvas_std.validate import ConformanceLevel, ValidationError, strip, validate

__all__ = [
    "__version__",
    "STANDARD_VERSION",
    "UPSTREAM_BASELINE",
    "ConformanceLevel",
    "ValidationError",
    "validate",
    "strip",
    "to_canvas",
    "from_canvas",
    "compute_sync_hash",
    "diff",
    "merge",
    "validate_suite",
    "ConformanceReport",
]
