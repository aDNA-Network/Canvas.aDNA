"""Pure-geometry spatial analysis for Obsidian canvas nodes.

Provides overlap detection, alignment scoring, containment checks,
spacing analysis, and structural summaries for canvas quality review.
All functions operate on generic canvas node dicts — zero application
assumptions.

Migrated from lattice-protocol/extensions/canvas/canvas_spatial.py
(M-1-02, full direct copy). Pure substrate.
"""

from __future__ import annotations

import math
from typing import Any  # noqa: F401 (used in return annotations)

# ---------------------------------------------------------------------------
# Bounding box
# ---------------------------------------------------------------------------


def bounding_box(node: dict) -> tuple[float, float, float, float]:
    """Return (x1, y1, x2, y2) bounding box for a node.

    ``x1, y1`` is the top-left corner; ``x2, y2`` is the bottom-right corner.
    """
    x = node.get("x", 0.0)
    y = node.get("y", 0.0)
    w = node.get("width", 0.0)
    h = node.get("height", 0.0)
    return (x, y, x + w, y + h)


# ---------------------------------------------------------------------------
# Overlap detection
# ---------------------------------------------------------------------------


def overlaps(a: dict, b: dict, tolerance: float = 5.0) -> bool:
    """Return True if nodes ``a`` and ``b`` overlap (minus tolerance margin)."""
    ax1, ay1, ax2, ay2 = bounding_box(a)
    bx1, by1, bx2, by2 = bounding_box(b)
    # Shrink each box by tolerance before checking
    ax1 += tolerance
    ay1 += tolerance
    ax2 -= tolerance
    ay2 -= tolerance
    bx1 += tolerance
    by1 += tolerance
    bx2 -= tolerance
    by2 -= tolerance
    # No overlap if separated on any axis
    if ax2 <= bx1 or bx2 <= ax1:
        return False
    if ay2 <= by1 or by2 <= ay1:
        return False
    return True


def detect_overlaps(
    nodes: list[dict],
    tolerance: float = 5.0,
) -> list[tuple[str, str]]:
    """Return list of ``(id_a, id_b)`` pairs for overlapping nodes."""
    pairs: list[tuple[str, str]] = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if overlaps(nodes[i], nodes[j], tolerance):
                pairs.append((nodes[i]["id"], nodes[j]["id"]))
    return pairs


# ---------------------------------------------------------------------------
# Alignment scoring
# ---------------------------------------------------------------------------


def alignment_score(nodes: list[dict]) -> float:
    """Score how well nodes align on a grid (0.0 = chaotic, 1.0 = perfect).

    Measures the fraction of node pairs that share either an x or y coordinate.
    Groups are excluded from alignment scoring.
    """
    content = [n for n in nodes if n.get("type") != "group"]
    if len(content) < 2:
        return 1.0

    x_values = [n.get("x", 0.0) for n in content]
    y_values = [n.get("y", 0.0) for n in content]

    # Count how many nodes share x or y positions (within 1px tolerance)
    aligned_pairs = 0
    total_pairs = 0
    for i in range(len(content)):
        for j in range(i + 1, len(content)):
            total_pairs += 1
            if abs(x_values[i] - x_values[j]) < 1.0:
                aligned_pairs += 1
            elif abs(y_values[i] - y_values[j]) < 1.0:
                aligned_pairs += 1

    return aligned_pairs / total_pairs if total_pairs > 0 else 1.0


# ---------------------------------------------------------------------------
# Containment
# ---------------------------------------------------------------------------


def containment_check(
    parent: dict,
    children: list[dict],
) -> list[str]:
    """Return IDs of children that are outside the parent's bounding box."""
    px1, py1, px2, py2 = bounding_box(parent)
    outside: list[str] = []
    for child in children:
        cx1, cy1, cx2, cy2 = bounding_box(child)
        if cx1 < px1 or cy1 < py1 or cx2 > px2 or cy2 > py2:
            outside.append(child["id"])
    return outside


# ---------------------------------------------------------------------------
# Spacing analysis
# ---------------------------------------------------------------------------


def spacing_analysis(nodes: list[dict]) -> dict[str, float]:
    """Analyze spacing between consecutive nodes (sorted by position).

    Returns ``{min, max, mean, std_dev}`` of inter-node gaps.
    Groups are excluded.
    """
    content = [n for n in nodes if n.get("type") != "group"]
    if len(content) < 2:
        return {"min": 0.0, "max": 0.0, "mean": 0.0, "std_dev": 0.0}

    # Sort by y then x
    content.sort(key=lambda n: (n.get("y", 0.0), n.get("x", 0.0)))

    gaps: list[float] = []
    for i in range(len(content) - 1):
        _, _, ax2, ay2 = bounding_box(content[i])
        bx1, by1, _, _ = bounding_box(content[i + 1])
        # Use the smaller gap (horizontal or vertical)
        h_gap = bx1 - ax2
        v_gap = by1 - ay2
        # Pick the relevant gap based on orientation
        if abs(content[i].get("y", 0) - content[i + 1].get("y", 0)) < 1.0:
            # Same row — use horizontal gap
            gap = h_gap
        else:
            # Different row — use vertical gap
            gap = v_gap
        gaps.append(gap)

    if not gaps:
        return {"min": 0.0, "max": 0.0, "mean": 0.0, "std_dev": 0.0}

    mean = sum(gaps) / len(gaps)
    variance = sum((g - mean) ** 2 for g in gaps) / len(gaps) if len(gaps) > 1 else 0.0
    return {
        "min": min(gaps),
        "max": max(gaps),
        "mean": round(mean, 2),
        "std_dev": round(math.sqrt(variance), 2),
    }


# ---------------------------------------------------------------------------
# Structural summary
# ---------------------------------------------------------------------------


def structural_summary(canvas: dict) -> dict[str, Any]:
    """Produce a structural summary of a canvas dict.

    Args:
        canvas: A built canvas dict (with ``nodes`` and ``edges`` keys).

    Returns:
        Dict with: ``node_count``, ``edge_count``, ``node_types``,
        ``edge_styles``, ``roles``, ``shapes``, ``colors``,
        ``nesting_depth``, ``file_nodes``, ``link_nodes``,
        ``group_count``, ``has_start_node``.
    """
    nodes = canvas.get("nodes", [])
    edges = canvas.get("edges", [])

    # Node type distribution
    node_types: dict[str, int] = {}
    for n in nodes:
        nt = n.get("type", "unknown")
        node_types[nt] = node_types.get(nt, 0) + 1

    # Edge styles
    edge_styles: set[str] = set()
    for e in edges:
        sa = e.get("styleAttributes", {})
        ps = sa.get("path")
        if ps:
            edge_styles.add(ps)
        else:
            edge_styles.add("solid")
        # Check from/to end for bidirectional
        if e.get("fromEnd") == "arrow" and e.get("toEnd") == "arrow":
            edge_styles.add("bidirectional")

    # Roles
    roles: set[str] = set()
    for n in nodes:
        sa = n.get("styleAttributes", {})
        role = sa.get("latticeRole")
        if role:
            roles.add(role)

    # Shapes
    shapes: set[str] = set()
    for n in nodes:
        sa = n.get("styleAttributes", {})
        shape = sa.get("shape")
        if shape:
            shapes.add(shape)

    # Colors
    colors: set[str] = set()
    for n in nodes:
        c = n.get("color")
        if c:
            colors.add(c)

    # Nesting depth (count how many groups contain other groups)
    groups = [n for n in nodes if n.get("type") == "group"]
    max_depth = _compute_nesting_depth(groups)

    # File and link nodes
    file_nodes = [n for n in nodes if n.get("type") == "file"]
    link_nodes = [n for n in nodes if n.get("type") == "link"]

    # Start node
    metadata = canvas.get("metadata", {})
    has_start_node = "startNode" in metadata

    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "node_types": node_types,
        "edge_styles": sorted(edge_styles),
        "roles": sorted(roles),
        "shapes": sorted(shapes),
        "colors": sorted(colors),
        "nesting_depth": max_depth,
        "file_nodes": len(file_nodes),
        "link_nodes": len(link_nodes),
        "group_count": len(groups),
        "has_start_node": has_start_node,
    }


def _compute_nesting_depth(groups: list[dict]) -> int:
    """Compute maximum nesting depth among groups.

    A group A contains group B if B's bounding box is inside A's.
    """
    if not groups:
        return 0

    # Build containment graph
    contains: dict[str, list[str]] = {g["id"]: [] for g in groups}

    for a in groups:
        ax1, ay1, ax2, ay2 = bounding_box(a)
        for b in groups:
            if a["id"] == b["id"]:
                continue
            bx1, by1, bx2, by2 = bounding_box(b)
            if bx1 >= ax1 and by1 >= ay1 and bx2 <= ax2 and by2 <= ay2:
                contains[a["id"]].append(b["id"])

    # Find max depth via DFS
    def _depth(gid: str, visited: set[str]) -> int:
        if gid in visited:
            return 0
        visited.add(gid)
        children = contains.get(gid, [])
        if not children:
            return 1
        return 1 + max(_depth(c, visited) for c in children)

    return max(_depth(g["id"], set()) for g in groups) if groups else 0
