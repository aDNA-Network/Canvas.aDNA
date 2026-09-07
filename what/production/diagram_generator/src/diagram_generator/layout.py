"""Deterministic layout — the producer-side graph geometry for a diagram.

Nodes are placed on a layered grid: a *rank* per node (longest-path depth from a root over the edge DAG; cyclic
back-edges are ignored for ranking only), laid out as rows (``TD``/``BT``) or columns (``LR``/``RL``) per the
diagram's ``direction``. The whole diagram is enclosed by the ``diagram_root`` group; the derived ``mermaid_src`` code
node is parked off to the right of the graph. All coordinates are **integers** and a pure function of the input
(reproducible). Geometry is not scored here — it only needs to be deterministic and roughly non-overlapping.
"""

from __future__ import annotations

from dataclasses import dataclass

from canvas_core.layout_fit import fit_group_size, fit_text_height, heading

from diagram_generator.model import DiagramInput

# Cell + node geometry, integer points.
NODE_W = 220
NODE_H = 100
GAP_X = 120  # horizontal spacing between cell origins
GAP_Y = 140  # vertical spacing between cell origins
PAD = 80  # padding inside the diagram_root group, around the graph
LABEL_BAND = 56  # minimum room under the group label
TITLE_GAP = 40  # clearance between the title node and rank 0 (overlap tolerance is 5px)
SRC_W = 480  # width of the parked mermaid_src code node
SRC_GAP = 120  # gap between the graph and the parked code node
TITLE_H = 60  # minimum height of the `#### <title>` heading node (CV-HIERARCHY-01 title slot)

# --- Visual-gate fitting (delegated, not mirrored) -----------------------------------------------
# ⛩ RETROFITTED 2026-09-07 (Blueprint P2c). P2 left four constants here — SRC_LINE_H=44,
# SRC_WRAP_COLS=46, SAFE_FILL=0.9, H4_LEAD_COST=42.6 — derived by rounding up two live trap readings
# and flagged in this very comment as an INTERIM: "a mirror of a measurement rather than the
# measurement". They are gone. Height now comes from `canvas_core.layout_fit.fit_text_height`, which
# delegates to the same `text_metrics.obsidian_required_node_height` CV-TEXT-BOUNDS-01 prints in its
# own fix hint, and container sizing from `fit_group_size`, which carries the ratio-scaling rule this
# module discovered (F-P2-4: a threshold expressed as a ratio needs a fix expressed as a ratio).
#
# The producer-wide census found this producer's four repaired classes accounted for 89 of the other
# producers' 99 findings — five hand-repairs would have produced five slightly different answers.
# One measurement, shared by producer and trap, is the whole point.


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int

    def as_node(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.w, "height": self.h}


def _ranks(d: DiagramInput) -> dict[str, int]:
    """Longest-path rank per node from the roots (nodes with no incoming edge). Cyclic back-edges are skipped for
    ranking; every node still gets a rank (a node only reachable through a cycle defaults to 0). Deterministic."""
    ids = [n.id for n in d.nodes]
    adj: dict[str, list[str]] = {nid: [] for nid in ids}
    indeg: dict[str, int] = {nid: 0 for nid in ids}
    for e in d.edges:
        adj[e.from_id].append(e.to_id)
        indeg[e.to_id] += 1

    rank: dict[str, int] = {nid: 0 for nid in ids}
    # Kahn-style longest-path over the acyclic portion; process roots first, in declaration order.
    indeg_work = dict(indeg)
    queue = [nid for nid in ids if indeg_work[nid] == 0]
    seen: set[str] = set()
    while queue:
        u = queue.pop(0)
        if u in seen:
            continue
        seen.add(u)
        for v in adj[u]:
            if rank[v] < rank[u] + 1:
                rank[v] = rank[u] + 1
            indeg_work[v] -= 1
            if indeg_work[v] == 0:
                queue.append(v)
    return rank


def src_height_for(mermaid: str) -> int:
    """Height the ``mermaid_src`` node needs so CV-TEXT-BOUNDS-01 passes.

    Measured, not estimated: the consumer wraps the source in a ```mermaid fence, so measure the
    fenced text at ``SRC_W`` through the shared fitter. A too-short node silently truncates the
    source at ~14% shown — the defect this replaces (F-P2-3).
    """
    fenced = f"```mermaid\n{mermaid}\n```"
    return fit_text_height(fenced, SRC_W, min_height=NODE_H)


def title_height_for(title: str, width: int) -> int:
    """Height the `#### <title>` node needs so CV-TEXT-BOUNDS-01 passes.

    Measures the rendered heading — the ``h4`` lead cost and any wrap — through the shared fitter,
    so the number matches what the trap will compute rather than approximating it.
    """
    return fit_text_height(heading(title), width, min_height=TITLE_H)


def layout(d: DiagramInput, mermaid: str = "") -> tuple[dict[str, Box], Box, Box, Box]:
    """Return (per-node boxes, the diagram_root group box, the mermaid_src box, the title box).

    ``mermaid`` is the generated source; when supplied, the code node is sized to actually hold it.
    """
    rank = _ranks(d)
    horizontal = d.direction in ("LR", "RL")

    # Group nodes by rank, preserving declaration order within a rank (determinism).
    by_rank: dict[int, list[str]] = {}
    for n in d.nodes:
        by_rank.setdefault(rank[n.id], []).append(n.id)

    boxes: dict[str, Box] = {}
    max_lane = max((len(v) for v in by_rank.values()), default=1)
    n_ranks = (max(by_rank) + 1) if by_rank else 1

    if horizontal:
        graph_w = n_ranks * NODE_W + (n_ranks - 1) * GAP_X
        graph_h = max_lane * NODE_H + (max_lane - 1) * GAP_Y
    else:
        graph_w = max_lane * NODE_W + (max_lane - 1) * GAP_X
        graph_h = n_ranks * NODE_H + (n_ranks - 1) * GAP_Y

    # The title is measured BEFORE the graph is placed, because the graph must start below it.
    # A fixed LABEL_BAND cannot do this — a title that wraps grows past the band and overlaps
    # rank 0 (CV-TEXT-BOUNDS-01/overlap, HIGH). The band is a floor, not the answer.
    title_w = max(NODE_W, graph_w)
    title_h = title_height_for(d.title, title_w)
    band = max(LABEL_BAND, title_h + TITLE_GAP)

    for r in sorted(by_rank):
        lane_ids = by_rank[r]
        for lane, nid in enumerate(lane_ids):
            if horizontal:
                # rank advances along x (columns); lane spreads down y.
                x = PAD + r * (NODE_W + GAP_X)
                y = PAD + band + lane * (NODE_H + GAP_Y)
            else:
                # rank advances down y (rows); lane spreads across x.
                x = PAD + lane * (NODE_W + GAP_X)
                y = PAD + band + r * (NODE_H + GAP_Y)
            boxes[nid] = Box(x, y, NODE_W, NODE_H)

    # The `# <title>` heading node, occupying the label band at the top-left of the group. It must
    # land in the upper 40% of the group height for CV-HIERARCHY-01's title slot; anchoring it at
    # y=PAD does that for every group taller than ~400px, which every diagram is.
    title_box = Box(PAD, PAD, title_w, title_h)

    # Park the mermaid_src code node to the right of the graph, sized to hold its own text.
    src_x = PAD + graph_w + SRC_GAP
    src_y = PAD + band
    src_h = max(NODE_H, graph_h, src_height_for(mermaid) if mermaid else 0)
    src_box = Box(src_x, src_y, SRC_W, src_h)

    # Children's bounding box, which is what CV-GROUP-PADDING-01 measures against the container.
    bb_w = (src_x + SRC_W) - PAD
    bb_h = (PAD + band + max(graph_h, src_h)) - PAD

    # Scale the container so the fill ratio clears the trap's 90% threshold on BOTH axes. A fixed
    # PAD cannot do this: the ratio degrades as the graph grows, so padding has to grow with it.
    group_w, group_h = fit_group_size(bb_w, bb_h, PAD)
    group_box = Box(0, 0, group_w, group_h)
    return boxes, group_box, src_box, title_box
