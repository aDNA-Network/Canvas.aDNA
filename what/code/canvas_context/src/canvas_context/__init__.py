"""adna-canvas-context — reference context-loader for the aDNA Canvas Standard.

Loads a ``.canvas`` as a navigable :class:`ContextGraph` **without rendering** (Operation Salon leg 2). Reference
realization of ``spec_canvas_context_loading.md`` (ratified 2026-06-22). A read-only consumer of ``canvas_std``'s
public API (D6 firewall — the dependency is one-way: ``canvas_context -> canvas_std``).
"""

from __future__ import annotations

from canvas_context.interaction import (
    AFFORDANCE_KINDS,
    Affordance,
    InteractionSurface,
    Response,
    SurfaceState,
    apply_response,
    is_round_trip_safe,
    load_interaction_surface,
    strip_interaction,
    validate_interaction_block,
)
from canvas_context.loader import CoreValidationError, load_context_graph
from canvas_context.model import (
    UNRESOLVED,
    Component,
    Conformance,
    ContextGraph,
    Panel,
    Ref,
    Relation,
    Surface,
)
from canvas_context.reconcile import (
    Reconciliation,
    governed_apply,
    reconcile,
    write_source_draft,
)
from canvas_context.resolver import (
    DefaultPathResolver,
    FederationDescriptor,
    LocalHandle,
    Resolver,
)

__version__ = "0.3.1"  # package version (0.3.1 — validate_interaction_block now delegates to the canvas_std harness, Armature P2)
SPEC = "spec_canvas_context_loading"  # the leg-2 protocol this realizes (leg-3: spec_interface_surface)
STANDARD_VERSION = "2.2.0"  # the aDNA Canvas Standard version the loaded canvases conform to (cut at Armature P2)

__all__ = [
    "__version__",
    "SPEC",
    "STANDARD_VERSION",
    "load_context_graph",
    "CoreValidationError",
    "ContextGraph",
    "Component",
    "Panel",
    "Relation",
    "Ref",
    "Surface",
    "Conformance",
    "UNRESOLVED",
    "Resolver",
    "DefaultPathResolver",
    "LocalHandle",
    "FederationDescriptor",
    # leg-3 interaction surface (Salon P4 POC) — additive, read-only over the leg-2 ContextGraph
    "load_interaction_surface",
    "InteractionSurface",
    "Affordance",
    "Response",
    "SurfaceState",
    "apply_response",
    "validate_interaction_block",
    "strip_interaction",
    "is_round_trip_safe",
    "AFFORDANCE_KINDS",
    # leg-3 governed write (Armature P1) — advisory-reverse reconciliation over canvas_std.roundtrip
    "reconcile",
    "governed_apply",
    "write_source_draft",
    "Reconciliation",
]
