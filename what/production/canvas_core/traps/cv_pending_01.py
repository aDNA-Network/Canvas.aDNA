"""CV-PENDING-01 — Unresolved placeholders shipped as done.

Graduated trap (3/3 cycles, 100% acceptance). Detects PendingImage and
PendingPanel markers that were never resolved before delivery.

Scans text nodes for placeholder patterns and file nodes for missing images.
"""

from __future__ import annotations

import re
from typing import Any

from . import TrapFinding

# Patterns that indicate unresolved placeholders
PENDING_PATTERNS = [
    re.compile(r"pending[_\s]?image", re.IGNORECASE),
    re.compile(r"pending[_\s]?panel", re.IGNORECASE),
    re.compile(r"\[placeholder\]", re.IGNORECASE),
    re.compile(r"\[pending\]", re.IGNORECASE),
    re.compile(r"TODO:\s*add\s*image", re.IGNORECASE),
    re.compile(r"TODO:\s*generate", re.IGNORECASE),
]


def check(
    canvas_data: dict[str, Any],
    *,
    r11_node_ids: set[str] | None = None,
) -> list[TrapFinding]:
    """Check for unresolved placeholders in canvas data.

    Args:
        canvas_data: Parsed canvas JSON (must have 'nodes' key).
        r11_node_ids: Optional set of node IDs under R11 gating.
            Accepted for uniform contract with other implemented traps
            (so ``run_all_traps()`` can pass kwarg through without per-trap
            introspection); ignored in body since placeholder detection
            is voice-register-agnostic.

    Returns:
        List of TrapFinding for each node containing placeholder markers.
    """
    findings: list[TrapFinding] = []
    nodes = canvas_data.get("nodes", [])

    for node in nodes:
        node_id = node.get("id", "unknown")
        text = node.get("text", "")
        node_type = node.get("type", "")

        # Check text content for pending patterns
        for pattern in PENDING_PATTERNS:
            if pattern.search(text):
                findings.append(TrapFinding(
                    trap_id="CV-PENDING-01",
                    condition="unresolved_placeholder",
                    node_ids=[node_id],
                    severity="critical",
                    message=f"Node {node_id} contains unresolved placeholder: "
                            f"matched '{pattern.pattern}' in text content",
                ))
                break  # One finding per node is enough

        # Check file nodes with empty or placeholder paths
        if node_type == "file":
            file_path = node.get("file", "")
            if not file_path or "placeholder" in file_path.lower() or "pending" in file_path.lower():
                findings.append(TrapFinding(
                    trap_id="CV-PENDING-01",
                    condition="unresolved_file_reference",
                    node_ids=[node_id],
                    severity="critical",
                    message=f"File node {node_id} has unresolved file reference: '{file_path}'",
                ))

    return findings
