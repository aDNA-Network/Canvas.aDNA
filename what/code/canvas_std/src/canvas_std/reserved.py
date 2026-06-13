"""Validators for the additive ``_reserved`` block (the aDNA-Native layer).

E0.1: signatures frozen; bodies raise NotImplementedError (E1.4).
Spec: spec_component_model (D4), spec_panel_link_semantics (D5), spec_context_object (D7),
spec_adna_canvas_standard §7.
"""

from __future__ import annotations

from typing import Any

# The reserved-key namespace (spec_adna_canvas_standard §7.2). E1.4 validates each against its sub-spec.
RESERVED_KEYS: tuple[str, ...] = (
    "adna_version",
    "conformance_level",
    "sync",
    "component_types",
    "semantic_bindings",
    "panel_link",
    "brand_style_pack_ref",
    "context_object",
)


def validate_reserved(reserved: dict[str, Any]) -> list[str]:
    """Validate a ``_reserved`` block; returns errors ([] == valid). Implemented at E1.4."""
    raise NotImplementedError("validate_reserved(): implemented at Keystone E1.4")


def validate_component_types(block: dict[str, Any], node_ids: set[str]) -> list[str]:
    """spec_component_model §7 — class in taxonomy, ids resolve, profile tokens in the §6 enums. E1.4."""
    raise NotImplementedError("validate_component_types(): implemented at Keystone E1.4")


def validate_panel_link(block: dict[str, Any], ids: set[str]) -> list[str]:
    """spec_panel_link_semantics §6 — sequence acyclic, exactly one canonical surface, no orphans. E1.4."""
    raise NotImplementedError("validate_panel_link(): implemented at Keystone E1.4")
