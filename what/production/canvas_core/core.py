"""CanvasBuilder — Obsidian Advanced Canvas generation library.

Generates valid Obsidian .canvas JSON with Advanced Canvas v5.6.6 support.
Closes P0 gaps G1-G5 from the Round-Trip Protocol v1.0:
  G1: Position preservation on regeneration
  G2: _reserved metadata block (metadata.frontmatter._reserved)
  G3: Sync hash computation (topology-based SHA-256)
  G4: Node shape injection (7 Advanced Canvas shapes via styleAttributes)
  G5: Edge path styles (4 line styles, 8 arrow types, 3 pathfinding methods)

Also provides:
  - Layout engines (DAG, grid, radial, presentation)
  - Round-trip operations (read_back, diff, merge, validate)
  - Selection board for RLHF variant comparison
  - Semantic node/edge creation per Canvas Standard v1.0.0

Part of campaign_advanced_canvas Phase 1 (M2).
"""

from __future__ import annotations

import hashlib
import json
import math
import secrets
import warnings
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

# --- aDNA Canvas Standard floor: federated to canvas_std (Operation Keystone E3.2) ----------------
# DEPRECATED 2026-06-13 — the Standard floor (the VALID_* value enums + TYPE_MAPPING +
# EDGE_TYPE_MAPPING) is now sourced from `canvas_std`, the reference implementation owned by
# Canvas.aDNA (federation_ref: Canvas.aDNA v2.0.0 — see CanvasForge.aDNA/canvas/CLAUDE.md). The
# constants are re-exported below as CanvasBuilder class attributes for the E-D2 grace window
# (expires 2027-06-13); relying on CanvasForge's embedded copy is deprecated and retired at cutover
# (E3.4). Mirrors the lattice-protocol/extensions/canvas/__init__.py extraction-shim precedent.
# Requires `adna-canvas-std` importable (editable install:
# `pip install -e ~/aDNA/Canvas.aDNA/what/code/canvas_std`). Rollback = revert this commit.
from canvas_std import schema as _canvas_std_schema  # DEPRECATED_STUB Canvas.aDNA

warnings.warn(
    "The aDNA Canvas Standard floor embedded in canvasforge.canvas_core (VALID_* enums, "
    "TYPE_MAPPING, EDGE_TYPE_MAPPING) is deprecated; canvas_std.schema is the single source of "
    "truth (federation_ref: Canvas.aDNA v2.0.0). canvas_core re-exports it through the E-D2 grace "
    "window (expires 2027-06-13).",
    DeprecationWarning,
    stacklevel=2,
)


class CanvasBuilder:
    """Build Obsidian canvas JSON with Advanced Canvas v5.6.6 support.

    Usage::

        cb = CanvasBuilder("my_lattice", "1.0.0")
        cb.add_text_node("n1", "Hello", x=0, y=0)
        cb.add_file_node("n2", "path/to/file.md", x=400, y=0)
        cb.add_edge("e1", "n1", "n2")
        cb.save("output.canvas")
    """

    # --- aDNA Canvas Standard floor — re-exported from canvas_std (SSOT; see module header) --------
    # Repointed at Operation Keystone E3.2 (2026-06-13); verbatim-identical to the E0.2 KEEP-floor
    # port, so canvas_std.schema is authoritative without behavioral change. Producer engines read
    # these via ``self.`` and are unchanged.  # DEPRECATED_STUB Canvas.aDNA
    VALID_SHAPES = _canvas_std_schema.VALID_SHAPES
    VALID_BORDERS = _canvas_std_schema.VALID_BORDERS
    VALID_TEXT_ALIGN = _canvas_std_schema.VALID_TEXT_ALIGN
    VALID_COLORS = _canvas_std_schema.VALID_COLORS
    VALID_PATH_STYLES = _canvas_std_schema.VALID_PATH_STYLES
    VALID_ARROWS = _canvas_std_schema.VALID_ARROWS
    VALID_PATHFINDING = _canvas_std_schema.VALID_PATHFINDING
    VALID_SIDES = _canvas_std_schema.VALID_SIDES
    VALID_NODE_TYPES = _canvas_std_schema.VALID_NODE_TYPES
    VALID_ENDS = _canvas_std_schema.VALID_ENDS

    # Semantic type -> visual mapping (built-in "lattice" profile, KEEP floor)
    TYPE_MAPPING: dict[str, dict[str, Any]] = _canvas_std_schema.TYPE_MAPPING

    # Semantic edge type -> visual mapping (built-in "lattice" profile, KEEP floor)
    EDGE_TYPE_MAPPING: dict[str, dict[str, Any]] = _canvas_std_schema.EDGE_TYPE_MAPPING

    # Default sizing (pixels)
    DEFAULT_NODE_WIDTH = 350
    DEFAULT_NODE_HEIGHT = 200
    DEFAULT_FILE_HEIGHT = 300
    DEFAULT_GROUP_WIDTH = 400
    DEFAULT_GROUP_HEIGHT = 400
    PRESENTATION_SLIDE_WIDTH = 1200
    PRESENTATION_SLIDE_HEIGHT = 1100
    PRESENTATION_SPACING = 1600

    def __init__(self, name: str = "untitled", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self._nodes: list[dict] = []
        self._edges: list[dict] = []
        self._node_index: dict[str, dict] = {}
        self._reserved: dict[str, Any] = {}
        self._start_node: str | None = None

    # --- ID Generation ---

    @staticmethod
    def generate_id() -> str:
        """Generate a 16-character hex ID (Obsidian convention)."""
        return secrets.token_hex(8)

    # --- Node Creation ---

    def add_text_node(
        self,
        id: str,
        text: str,
        x: float = 0,
        y: float = 0,
        width: float | None = None,
        height: float | None = None,
        color: str | None = None,
        shape: str | None = None,
        border: str | None = None,
        text_align: str | None = None,
        **kwargs: Any,
    ) -> dict:
        """Add a text node containing markdown content."""
        node = self._build_node(
            id=id,
            node_type="text",
            x=x,
            y=y,
            width=width or self.DEFAULT_NODE_WIDTH,
            height=height or self.DEFAULT_NODE_HEIGHT,
            color=color,
            shape=shape,
            border=border,
            text_align=text_align,
            **kwargs,
        )
        node["text"] = text
        self._register_node(node)
        return node

    def add_file_node(
        self,
        id: str,
        file: str,
        x: float = 0,
        y: float = 0,
        width: float | None = None,
        height: float | None = None,
        color: str | None = None,
        shape: str | None = None,
        border: str | None = None,
        **kwargs: Any,
    ) -> dict:
        """Add a file node embedding a vault file."""
        node = self._build_node(
            id=id,
            node_type="file",
            x=x,
            y=y,
            width=width or self.DEFAULT_NODE_WIDTH,
            height=height or self.DEFAULT_FILE_HEIGHT,
            color=color,
            shape=shape,
            border=border,
            **kwargs,
        )
        node["file"] = file
        self._register_node(node)
        return node

    def add_link_node(
        self,
        id: str,
        url: str,
        x: float = 0,
        y: float = 0,
        width: float | None = None,
        height: float | None = None,
        color: str | None = None,
        **kwargs: Any,
    ) -> dict:
        """Add a link node embedding an external URL."""
        node = self._build_node(
            id=id,
            node_type="link",
            x=x,
            y=y,
            width=width or self.DEFAULT_NODE_WIDTH,
            height=height or self.DEFAULT_NODE_HEIGHT,
            color=color,
            **kwargs,
        )
        node["url"] = url
        self._register_node(node)
        return node

    def add_group(
        self,
        id: str,
        label: str = "",
        x: float = 0,
        y: float = 0,
        width: float | None = None,
        height: float | None = None,
        color: str | None = None,
        background: str | None = None,
        background_style: str | None = None,
        is_start_node: bool = False,
        collapsed: bool = False,
        **kwargs: Any,
    ) -> dict:
        """Add a group node that visually contains other nodes."""
        node = self._build_node(
            id=id,
            node_type="group",
            x=x,
            y=y,
            width=width or self.DEFAULT_GROUP_WIDTH,
            height=height or self.DEFAULT_GROUP_HEIGHT,
            color=color,
            **kwargs,
        )
        if label:
            node["label"] = label
        if background:
            node["background"] = background
        if background_style:
            node["backgroundStyle"] = background_style
        if is_start_node:
            node["isStartNode"] = True
            self._start_node = id
        if collapsed:
            node["collapsed"] = True
        self._register_node(node)
        return node

    def add_semantic_node(
        self,
        id: str,
        semantic_type: str,
        content: str,
        file_path: str | None = None,
        x: float = 0,
        y: float = 0,
        width: float | None = None,
        height: float | None = None,
        **kwargs: Any,
    ) -> dict:
        """Add a node using Canvas Standard v1.0.0 semantic type mapping.

        Args:
            semantic_type: One of module, dataset, reasoning, process,
                          input, output, start, end.
            content: Text content (used for text nodes or as fallback).
            file_path: Vault file path (used when semantic type maps to file node).
        """
        mapping = self.TYPE_MAPPING.get(semantic_type)
        if not mapping:
            raise ValueError(
                f"Unknown semantic type: {semantic_type!r}. Valid: {sorted(self.TYPE_MAPPING)}"
            )

        if mapping["node_type"] == "file" and file_path:
            return self.add_file_node(
                id=id,
                file=file_path,
                x=x,
                y=y,
                width=width,
                height=height,
                color=mapping["color"],
                shape=mapping["shape"],
                **kwargs,
            )
        return self.add_text_node(
            id=id,
            text=content,
            x=x,
            y=y,
            width=width,
            height=height,
            color=mapping["color"],
            shape=mapping["shape"],
            **kwargs,
        )

    # --- Edge Creation ---

    def add_edge(
        self,
        id: str,
        from_node: str,
        to_node: str,
        from_side: str = "right",
        to_side: str = "left",
        from_end: str | None = None,
        to_end: str = "arrow",
        label: str | None = None,
        color: str | None = None,
        path_style: str | None = None,
        arrow: str | None = None,
        pathfinding: str | None = None,
        **kwargs: Any,
    ) -> dict:
        """Add an edge connecting two nodes.

        Args:
            from_end: "none" or "arrow" (default: omitted = none).
            to_end: "none" or "arrow" (default: "arrow" per Canvas Standard).
            path_style: Line style — "dotted", "short-dashed", "long-dashed".
            arrow: Arrow head — "triangle-outline", "thin-triangle", etc.
            pathfinding: Routing — "square", "a-star" (default bezier).
        """
        edge: dict[str, Any] = {
            "id": id,
            "fromNode": from_node,
            "toNode": to_node,
            "fromSide": from_side,
            "toSide": to_side,
            "toEnd": to_end,
        }
        if from_end:
            edge["fromEnd"] = from_end
        if label:
            edge["label"] = label
        if color:
            edge["color"] = color

        # G5: Edge styleAttributes
        style_attrs: dict[str, str] = {}
        if path_style:
            style_attrs["path"] = path_style
        if arrow:
            style_attrs["arrow"] = arrow
        if pathfinding:
            style_attrs["pathfindingMethod"] = pathfinding
        if style_attrs:
            edge["styleAttributes"] = style_attrs

        self._edges.append(edge)
        return edge

    def add_semantic_edge(
        self,
        id: str,
        from_node: str,
        to_node: str,
        edge_type: str = "data",
        label: str | None = None,
        **kwargs: Any,
    ) -> dict:
        """Add an edge using Canvas Standard v1.0.0 semantic edge types.

        Args:
            edge_type: One of data, control, optional, bidirectional, weak.
        """
        style = self.EDGE_TYPE_MAPPING.get(edge_type)
        if not style:
            raise ValueError(
                f"Unknown edge type: {edge_type!r}. Valid: {sorted(self.EDGE_TYPE_MAPPING)}"
            )
        return self.add_edge(
            id=id,
            from_node=from_node,
            to_node=to_node,
            label=label,
            path_style=style.get("path_style"),
            arrow=style.get("arrow"),
            from_end=style.get("from_end"),
            to_end=style.get("to_end", "arrow"),
            **kwargs,
        )

    # --- Metadata Group (Canvas Standard v1.0.0) ---

    def add_lattice_meta_group(self, x: float = -200, y: float = -100) -> dict:
        """Add the required _lattice_meta group with lattice name/version."""
        return self.add_group(
            id="_lattice_meta",
            label=f"{self.name} v{self.version}",
            x=x,
            y=y,
            width=200,
            height=50,
        )

    # --- Layout Engines ---

    def layout_dag(
        self,
        direction: str = "lr",
        h_spacing: float = 400,
        v_spacing: float = 200,
    ) -> None:
        """Apply DAG layout using topological sort.

        Args:
            direction: "lr" (left-to-right) or "tb" (top-to-bottom).
            h_spacing: Spacing along primary axis.
            v_spacing: Spacing along secondary axis.
        """
        content_nodes = [n for n in self._nodes if n["type"] != "group"]
        if not content_nodes:
            return

        # Build adjacency
        node_ids = {n["id"] for n in content_nodes}
        children: dict[str, list[str]] = defaultdict(list)
        in_degree: dict[str, int] = dict.fromkeys(node_ids, 0)

        for edge in self._edges:
            f, t = edge["fromNode"], edge["toNode"]
            if f in node_ids and t in node_ids:
                children[f].append(t)
                in_degree[t] = in_degree.get(t, 0) + 1

        # Kahn's algorithm with level assignment
        queue = sorted(nid for nid, deg in in_degree.items() if deg == 0)
        levels: dict[str, int] = {}
        while queue:
            next_queue: list[str] = []
            for nid in queue:
                # Level = max predecessor level + 1
                pred_lvls = [
                    levels[e["fromNode"]]
                    for e in self._edges
                    if e["toNode"] == nid and e["fromNode"] in levels
                ]
                levels[nid] = (max(pred_lvls) + 1) if pred_lvls else 0
                for child in children[nid]:
                    in_degree[child] -= 1
                    if in_degree[child] == 0:
                        next_queue.append(child)
            queue = sorted(next_queue)

        # Handle any remaining nodes (cycles or disconnected)
        for nid in node_ids:
            if nid not in levels:
                levels[nid] = max(levels.values(), default=0) + 1

        # Assign positions
        level_counts: dict[int, int] = defaultdict(int)
        for node in content_nodes:
            level = levels.get(node["id"], 0)
            rank = level_counts[level]
            level_counts[level] += 1

            if direction == "lr":
                node["x"] = level * h_spacing
                node["y"] = rank * v_spacing
            else:
                node["x"] = rank * h_spacing
                node["y"] = level * v_spacing

    def layout_grid(
        self,
        columns: int = 3,
        h_spacing: float = 400,
        v_spacing: float = 350,
    ) -> None:
        """Apply grid layout to non-group nodes."""
        content_nodes = [n for n in self._nodes if n["type"] != "group"]
        for i, node in enumerate(content_nodes):
            node["x"] = (i % columns) * h_spacing
            node["y"] = (i // columns) * v_spacing

    def layout_radial(
        self,
        center_node: str | None = None,
        radius: float = 400,
    ) -> None:
        """Apply radial/hub-spoke layout around a center node."""
        content_nodes = [n for n in self._nodes if n["type"] != "group"]
        if not content_nodes:
            return

        if center_node and center_node in self._node_index:
            center = self._node_index[center_node]
            others = [n for n in content_nodes if n["id"] != center_node]
        else:
            center = content_nodes[0]
            others = content_nodes[1:]

        center["x"] = 0
        center["y"] = 0

        if others:
            angle_step = 2 * math.pi / len(others)
            for i, node in enumerate(others):
                angle = i * angle_step - math.pi / 2  # Start from top
                node["x"] = round(radius * math.cos(angle))
                node["y"] = round(radius * math.sin(angle))

    def layout_presentation(
        self,
        slide_width: float | None = None,
        slide_height: float | None = None,
        spacing: float | None = None,
    ) -> None:
        """Layout group nodes as presentation slides left-to-right."""
        sw = slide_width or self.PRESENTATION_SLIDE_WIDTH
        sh = slide_height or self.PRESENTATION_SLIDE_HEIGHT
        sp = spacing or self.PRESENTATION_SPACING

        groups = [n for n in self._nodes if n["type"] == "group"]
        for i, group in enumerate(groups):
            group["x"] = i * sp
            group["y"] = 0
            group["width"] = sw
            group["height"] = sh

    # --- Build & Save ---

    def build(self) -> dict:
        """Build the complete canvas JSON dict.

        Includes metadata block with _reserved data (G2) and sync hash (G3).
        """
        canvas: dict[str, Any] = {
            "nodes": deepcopy(self._nodes),
            "edges": deepcopy(self._edges),
        }

        # G2 + G3: metadata block
        sync_hash = self.compute_sync_hash()
        reserved = {
            **self._reserved,
            "sync_hash": sync_hash,
            "builder": "CanvasBuilder",
            "builder_version": "1.0.0",
            "lattice_name": self.name,
            "lattice_version": self.version,
        }

        metadata: dict[str, Any] = {
            "frontmatter": {"_reserved": reserved},
            "version": "1.0-1.0",  # Advanced Canvas plugin spec version
        }
        if self._start_node:
            metadata["startNode"] = self._start_node

        canvas["metadata"] = metadata
        return canvas

    def save(self, path: str | Path) -> Path:
        """Save canvas JSON to a .canvas file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        canvas = self.build()
        path.write_text(json.dumps(canvas, indent=2) + "\n")
        return path

    # --- Round-Trip Operations ---

    @classmethod
    def read_back(cls, path: str | Path) -> CanvasBuilder:
        """Load an existing .canvas file into a CanvasBuilder instance.

        Restores nodes, edges, metadata, and _reserved state.
        """
        path = Path(path)
        data = json.loads(path.read_text())

        builder = cls()
        builder._nodes = data.get("nodes", [])
        builder._edges = data.get("edges", [])

        # Rebuild index
        for node in builder._nodes:
            builder._node_index[node["id"]] = node

        # Extract metadata
        metadata = data.get("metadata", {})
        frontmatter = metadata.get("frontmatter", {})
        reserved = frontmatter.get("_reserved", {})

        builder.name = reserved.get("lattice_name", "untitled")
        builder.version = reserved.get("lattice_version", "1.0.0")
        builder._start_node = metadata.get("startNode")

        # Preserve user-added _reserved keys
        internal_keys = {
            "sync_hash",
            "builder",
            "builder_version",
            "lattice_name",
            "lattice_version",
        }
        builder._reserved = {k: v for k, v in reserved.items() if k not in internal_keys}

        return builder

    def diff(self, other: CanvasBuilder) -> dict:
        """Compare this builder against another, returning structured differences.

        Returns:
            dict with keys: nodes_added, nodes_removed, nodes_modified,
            edges_added, edges_removed, edges_modified, positions_changed,
            topology_changed (bool).
        """
        self_ids = {n["id"] for n in self._nodes}
        other_ids = {n["id"] for n in other._nodes}
        self_eids = {e["id"] for e in self._edges}
        other_eids = {e["id"] for e in other._edges}

        result: dict[str, Any] = {
            "nodes_added": [n for n in other._nodes if n["id"] not in self_ids],
            "nodes_removed": [n for n in self._nodes if n["id"] not in other_ids],
            "nodes_modified": [],
            "edges_added": [e for e in other._edges if e["id"] not in self_eids],
            "edges_removed": [e for e in self._edges if e["id"] not in other_eids],
            "edges_modified": [],
            "positions_changed": [],
        }

        # Check modified nodes
        for nid in self_ids & other_ids:
            s = self._node_index[nid]
            o = other._node_index[nid]

            if s.get("x") != o.get("x") or s.get("y") != o.get("y"):
                result["positions_changed"].append(
                    {
                        "id": nid,
                        "from": {"x": s.get("x"), "y": s.get("y")},
                        "to": {"x": o.get("x"), "y": o.get("y")},
                    }
                )

            s_content = {k: v for k, v in s.items() if k not in ("x", "y")}
            o_content = {k: v for k, v in o.items() if k not in ("x", "y")}
            if s_content != o_content:
                result["nodes_modified"].append({"id": nid, "from": s, "to": o})

        # Check modified edges
        self_edge_idx = {e["id"]: e for e in self._edges}
        other_edge_idx = {e["id"]: e for e in other._edges}
        for eid in self_eids & other_eids:
            if self_edge_idx[eid] != other_edge_idx[eid]:
                result["edges_modified"].append(
                    {
                        "id": eid,
                        "from": self_edge_idx[eid],
                        "to": other_edge_idx[eid],
                    }
                )

        result["topology_changed"] = bool(
            result["nodes_added"]
            or result["nodes_removed"]
            or result["edges_added"]
            or result["edges_removed"]
        )
        return result

    def merge(self, other: CanvasBuilder, strategy: str = "yaml_wins") -> CanvasBuilder:
        """Merge another builder into this one with conflict resolution.

        Strategies:
          - yaml_wins: Semantic content from self (YAML-regenerated),
            positions from other (canvas-edited). Default per Round-Trip Protocol.
          - canvas_wins: All content from other (canvas state).
        """
        result = CanvasBuilder(self.name, self.version)

        if strategy == "yaml_wins":
            result._nodes = deepcopy(self._nodes)
            result._edges = deepcopy(self._edges)
            result._node_index = {n["id"]: n for n in result._nodes}
            result._reserved = {**self._reserved, **other._reserved}
            result._start_node = self._start_node or other._start_node

            # Apply canvas positions (canvas authority for layout)
            for o_node in other._nodes:
                r_node = result._node_index.get(o_node["id"])
                if r_node:
                    r_node["x"] = o_node["x"]
                    r_node["y"] = o_node["y"]
                    if "width" in o_node:
                        r_node["width"] = o_node["width"]
                    if "height" in o_node:
                        r_node["height"] = o_node["height"]
        elif strategy == "canvas_wins":
            result._nodes = deepcopy(other._nodes)
            result._edges = deepcopy(other._edges)
            result._node_index = {n["id"]: n for n in result._nodes}
            result._reserved = {**self._reserved, **other._reserved}
            result._start_node = other._start_node or self._start_node
        else:
            raise ValueError(f"Unknown merge strategy: {strategy!r}")

        return result

    def validate(self) -> list[str]:
        """Validate canvas against Canvas Standard v1.0.0.

        Returns a list of validation error strings (empty = valid).
        """
        errors: list[str] = []
        node_ids: set[str] = set()

        for node in self._nodes:
            nid = node.get("id")
            if not nid:
                errors.append("Node missing 'id'")
                continue
            if nid in node_ids:
                errors.append(f"Duplicate node ID: {nid}")
            node_ids.add(nid)

            ntype = node.get("type")
            if not ntype:
                errors.append(f"Node {nid} missing 'type'")
            elif ntype not in self.VALID_NODE_TYPES:
                errors.append(f"Node {nid} invalid type: {ntype}")

            if "x" not in node or "y" not in node:
                errors.append(f"Node {nid} missing position (x, y)")
            if "width" not in node or "height" not in node:
                errors.append(f"Node {nid} missing dimensions (width, height)")

            # Type-specific content checks
            if ntype == "text" and "text" not in node:
                errors.append(f"Text node {nid} missing 'text'")
            if ntype == "file" and "file" not in node:
                errors.append(f"File node {nid} missing 'file'")
            if ntype == "link" and "url" not in node:
                errors.append(f"Link node {nid} missing 'url'")

            # Color validation
            color = node.get("color")
            if color is not None and color not in self.VALID_COLORS:
                if not (isinstance(color, str) and color.startswith("#")):
                    errors.append(f"Node {nid} invalid color: {color}")

            # G4: styleAttributes validation
            style = node.get("styleAttributes", {})
            shape = style.get("shape")
            if shape is not None and shape not in self.VALID_SHAPES:
                errors.append(f"Node {nid} invalid shape: {shape}")
            border = style.get("border")
            if border is not None and border not in self.VALID_BORDERS:
                errors.append(f"Node {nid} invalid border: {border}")
            ta = style.get("textAlign")
            if ta is not None and ta not in self.VALID_TEXT_ALIGN:
                errors.append(f"Node {nid} invalid textAlign: {ta}")

        # Edge validation
        edge_ids: set[str] = set()
        for edge in self._edges:
            eid = edge.get("id")
            if not eid:
                errors.append("Edge missing 'id'")
                continue
            if eid in edge_ids:
                errors.append(f"Duplicate edge ID: {eid}")
            edge_ids.add(eid)

            if edge.get("fromNode") not in node_ids:
                errors.append(f"Edge {eid} references unknown fromNode: {edge.get('fromNode')}")
            if edge.get("toNode") not in node_ids:
                errors.append(f"Edge {eid} references unknown toNode: {edge.get('toNode')}")

            for side_key in ("fromSide", "toSide"):
                val = edge.get(side_key)
                if val and val not in self.VALID_SIDES:
                    errors.append(f"Edge {eid} invalid {side_key}: {val}")

            # Canvas Standard: toEnd="arrow" required
            if edge.get("toEnd") != "arrow":
                errors.append(f"Edge {eid} missing toEnd='arrow' (Canvas Standard requirement)")

            # G5: edge styleAttributes validation
            style = edge.get("styleAttributes", {})
            ps = style.get("path")
            if ps is not None and ps not in self.VALID_PATH_STYLES:
                errors.append(f"Edge {eid} invalid path style: {ps}")
            ar = style.get("arrow")
            if ar is not None and ar not in self.VALID_ARROWS:
                errors.append(f"Edge {eid} invalid arrow: {ar}")
            pf = style.get("pathfindingMethod")
            if pf is not None and pf not in self.VALID_PATHFINDING:
                errors.append(f"Edge {eid} invalid pathfinding: {pf}")

        return errors

    def compute_sync_hash(self) -> str:
        """Compute topology-based sync hash (G3).

        Hash covers sorted node IDs and sorted edge connections.
        Used to detect YAML<->canvas divergence.
        """
        topology = {
            "nodes": sorted(n["id"] for n in self._nodes),
            "edges": sorted(f"{e['fromNode']}->{e['toNode']}" for e in self._edges),
        }
        raw = json.dumps(topology, sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()[:16]

    # --- Position Preservation (G1) ---

    def preserve_positions(self, reference: CanvasBuilder) -> int:
        """Copy positions from a reference builder for matching node IDs.

        Implements G1: nodes that exist in both self and reference get
        their x/y/width/height from reference. New nodes keep their
        current positions (from layout or explicit placement).

        Returns the number of nodes whose positions were preserved.
        """
        count = 0
        for node in self._nodes:
            ref = reference._node_index.get(node["id"])
            if ref:
                node["x"] = ref["x"]
                node["y"] = ref["y"]
                if "width" in ref:
                    node["width"] = ref["width"]
                if "height" in ref:
                    node["height"] = ref["height"]
                count += 1
        return count

    # --- Selection Board (RLHF) ---

    def selection_board(
        self,
        variants: list[dict],
        labels: list[str] | None = None,
        title: str = "Variant Selection",
        columns: int = 2,
        h_spacing: float = 500,
        v_spacing: float = 400,
    ) -> CanvasBuilder:
        """Create a comparison canvas for RLHF variant selection.

        Args:
            variants: List of dicts. Each must have at least ``id`` plus
                     either ``text`` or ``file``. Optional: color, shape,
                     width, height.
            labels: Display labels (defaults to "Variant 1", "Variant 2", ...).
            title: Title text for the board header.
            columns: Grid columns for layout.

        Returns:
            A new CanvasBuilder containing the selection board.
        """
        board = CanvasBuilder(f"{self.name}_selection", self.version)

        # Title node
        title_id = board.generate_id()
        board.add_text_node(
            id=title_id,
            text=f"# {title}\n\nSelect preferred variant.",
            x=0,
            y=-150,
            width=columns * h_spacing,
            height=100,
            text_align="center",
        )

        if not labels:
            labels = [f"Variant {i + 1}" for i in range(len(variants))]

        for i, (variant, label) in enumerate(zip(variants, labels, strict=False)):
            col = i % columns
            row = i // columns
            x = col * h_spacing
            y = row * v_spacing

            # Label group
            board.add_group(
                id=board.generate_id(),
                label=label,
                x=x - 25,
                y=y - 25,
                width=h_spacing - 50,
                height=v_spacing - 50,
            )

            # Content node
            vid = variant.get("id", board.generate_id())
            w = variant.get("width", 400)
            h = variant.get("height", 300)
            c = variant.get("color")
            s = variant.get("shape")

            if "file" in variant:
                board.add_file_node(
                    id=vid,
                    file=variant["file"],
                    x=x,
                    y=y,
                    width=w,
                    height=h,
                    color=c,
                    shape=s,
                )
            else:
                board.add_text_node(
                    id=vid,
                    text=variant.get("text", ""),
                    x=x,
                    y=y,
                    width=w,
                    height=h,
                    color=c,
                    shape=s,
                )

        return board

    # --- Accessors ---

    @property
    def nodes(self) -> list[dict]:
        """Read-only access to node list."""
        return list(self._nodes)

    @property
    def edges(self) -> list[dict]:
        """Read-only access to edge list."""
        return list(self._edges)

    @property
    def node_ids(self) -> set[str]:
        """Set of all node IDs."""
        return set(self._node_index)

    def get_node(self, id: str) -> dict | None:
        """Get a node by ID, or None."""
        return self._node_index.get(id)

    # --- Private Helpers ---

    def _build_node(
        self,
        id: str,
        node_type: str,
        x: float,
        y: float,
        width: float,
        height: float,
        color: str | None = None,
        shape: str | None = None,
        border: str | None = None,
        text_align: str | None = None,
        **kwargs: Any,
    ) -> dict:
        """Build a base node dict with optional styleAttributes (G4)."""
        node: dict[str, Any] = {
            "id": id,
            "type": node_type,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
        }
        if color:
            node["color"] = color

        # G4: Build styleAttributes block
        style_attrs: dict[str, str] = {}
        if shape:
            style_attrs["shape"] = shape
        if border:
            style_attrs["border"] = border
        if text_align:
            style_attrs["textAlign"] = text_align

        # Allow explicit styleAttributes from kwargs
        extra_styles = kwargs.pop("styleAttributes", None)
        if extra_styles:
            style_attrs.update(extra_styles)

        if style_attrs:
            node["styleAttributes"] = style_attrs

        # Pass through remaining kwargs
        for k, v in kwargs.items():
            if v is not None:
                node[k] = v

        return node

    def _register_node(self, node: dict) -> None:
        """Register a node in internal lists and index."""
        self._nodes.append(node)
        self._node_index[node["id"]] = node

    def __repr__(self) -> str:
        return (
            f"CanvasBuilder({self.name!r}, {self.version!r}, "
            f"nodes={len(self._nodes)}, edges={len(self._edges)})"
        )
