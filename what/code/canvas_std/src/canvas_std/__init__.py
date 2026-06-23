"""adna-canvas-std — reference implementation of the aDNA Canvas Standard.

Standard-bearer tooling (Option P): validators, round-trip converters, conformance harness.
The reference engine is implemented across Operation Keystone E1.1–E1.5; the conformance harness
+ CLI are E2. See the normative specs in Canvas.aDNA/what/specs/.
"""

from __future__ import annotations

from canvas_std.conformance import ConformanceReport, json_schema, validate_suite
from canvas_std.reserved import validate_interaction
from canvas_std.roundtrip import (
    compute_sync_hash,
    diff,
    from_canvas,
    merge,
    preserve_positions,
    to_canvas,
)
from canvas_std.validate import (
    ConformanceLevel,
    ValidationError,
    degradation_report,
    strip,
    validate,
)

__version__ = "0.1.0"  # package version
STANDARD_VERSION = "2.2.0"  # the aDNA Canvas Standard version this package implements (interaction_version 1.0 cut here, Armature P2 / adr_007)
UPSTREAM_BASELINE = "Advanced Canvas v5.6.6 + JSON Canvas 1.0"  # PIN-A (p1_fork_baseline §1)

__all__ = [
    "__version__",
    "STANDARD_VERSION",
    "UPSTREAM_BASELINE",
    "ConformanceLevel",
    "ValidationError",
    "validate",
    "validate_interaction",
    "strip",
    "degradation_report",
    "to_canvas",
    "from_canvas",
    "compute_sync_hash",
    "diff",
    "merge",
    "preserve_positions",
    "validate_suite",
    "ConformanceReport",
    "json_schema",
]
