"""R11 Patient's Voice gate — substrate enforcement module.

Per ADR 000 § Voice Register Governance and ADR 002 § R11 Gating:
- Wrappers declare *where* R11 may appear via lattice-level `r11_gated_nodes`
- Substrate enforces human approval before gated node output proceeds downstream
- Wrappers tighten (add nodes to gate list) but never loosen (remove nodes)

This module provides the enforcement mechanism. Full HITL integration
(Obsidian review surface, reviewer-notes schema) lands in Phase 4 M-4-04.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class R11GateResult:
    """Result of an R11 gate check."""

    node_id: str
    gated: bool
    approved: bool = False
    approver: str | None = None
    reason: str | None = None


@dataclass
class R11GateConfig:
    """R11 gate configuration extracted from lattice metadata.

    Populated from the lattice-level `r11_gated_nodes` list plus any
    wrapper-declared fine-grained gate specifications (e.g.,
    `r11_gated_slide_types`, `r11_gated_pages`).
    """

    gated_nodes: list[str] = field(default_factory=list)
    fine_grain: dict[str, Any] = field(default_factory=dict)


def load_r11_config(lattice_metadata: dict[str, Any]) -> R11GateConfig:
    """Extract R11 gate configuration from lattice YAML metadata.

    Args:
        lattice_metadata: The parsed `lattice:` block from a YAML file.

    Returns:
        R11GateConfig with gated node IDs and any fine-grain specs.
    """
    gated_nodes = lattice_metadata.get("r11_gated_nodes", [])
    fine_grain: dict[str, Any] = {}

    # Wrapper-declared fine-grained gates: any `r11_gated_<custom>` key flows
    # through, except `r11_gated_nodes` which is reserved for the canonical
    # gate at check_r11_gate(). Generalized from a hardcoded slide/page/panel
    # whitelist so future applications (topology, sequence, matrix, etc.) can
    # declare their own register namespaces without a substrate edit.
    for key, value in lattice_metadata.items():
        if key.startswith("r11_gated_") and key != "r11_gated_nodes":
            fine_grain[key] = value

    return R11GateConfig(gated_nodes=list(gated_nodes), fine_grain=fine_grain)


def check_r11_gate(
    node_id: str,
    config: R11GateConfig,
    approvals: dict[str, R11GateResult] | None = None,
) -> R11GateResult:
    """Check whether a node requires R11 human approval.

    Args:
        node_id: The lattice node ID being evaluated.
        config: R11 gate configuration from the lattice.
        approvals: Previously recorded approvals (keyed by node_id).

    Returns:
        R11GateResult indicating whether the node is gated and its
        approval status.
    """
    if node_id not in config.gated_nodes:
        return R11GateResult(node_id=node_id, gated=False, approved=True)

    # Check for prior approval
    if approvals and node_id in approvals:
        prior = approvals[node_id]
        if prior.approved:
            return prior

    # Gated and not yet approved — requires human intervention
    return R11GateResult(
        node_id=node_id,
        gated=True,
        approved=False,
        reason="R11 Patient's Voice gate: human approval required before output proceeds",
    )


def merge_wrapper_gates(
    canonical: R11GateConfig,
    wrapper: R11GateConfig,
) -> R11GateConfig:
    """Merge wrapper R11 gates into canonical config.

    Per ADR 002 § Override Pattern rule 5: wrappers tighten (add nodes)
    but never loosen (remove nodes).

    Args:
        canonical: R11 config from the canonical forge lattice.
        wrapper: R11 config from the consumer wrapper lattice.

    Returns:
        Merged config with the union of gated nodes.
    """
    merged_nodes = list(set(canonical.gated_nodes) | set(wrapper.gated_nodes))
    merged_fine_grain = {**canonical.fine_grain, **wrapper.fine_grain}
    return R11GateConfig(gated_nodes=merged_nodes, fine_grain=merged_fine_grain)
