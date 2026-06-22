"""adna-canvas-context — reference context-loader for the aDNA Canvas Standard.

Loads a ``.canvas`` as a navigable :class:`ContextGraph` **without rendering** (Operation Salon leg 2). Reference
realization of ``spec_canvas_context_loading.md`` (ratified 2026-06-22). A read-only consumer of ``canvas_std``'s
public API (D6 firewall — the dependency is one-way: ``canvas_context -> canvas_std``).
"""

from __future__ import annotations

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
from canvas_context.resolver import (
    DefaultPathResolver,
    FederationDescriptor,
    LocalHandle,
    Resolver,
)

__version__ = "0.1.0"  # package version
SPEC = "spec_canvas_context_loading"  # the protocol this realizes
STANDARD_VERSION = "2.0.2"  # the aDNA Canvas Standard version the loaded canvases conform to

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
]
