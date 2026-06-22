"""Deterministic layout — the producer-side graph geometry for a diagram.

Nodes are placed on a layered grid: a *rank* per node (longest-path depth from a root over the edge DAG; cyclic
back-edges are ignored for ranking only), laid out as rows (``TD``/``BT``) or columns (``LR``/``RL``) per the
diagram's ``direction``. The whole diagram is enclosed by the ``diagram_root`` group; the derived ``mermaid_src`` code
node is parked off to the right of the graph. All coordinates are **integers** and a pure function of the input
(reproducible). Geometry is not scored here — it only needs to be deterministic and roughly non-overlapping.
"""

from __future__ import annotations

from dataclasses import dataclass

from diagram_generator.model import DiagramInput

# Cell + node geometry, integer points.
NODE_W = 220
NODE_H = 100
GAP_X = 120  # horizontal spacing between cell origins
GAP_Y = 140  # vertical spacing between cell origins
PAD = 80  # padding inside the diagram_root group, around the graph
LABEL_BAND = 56  # room under the group label
SRC_W = 480  # width of the parked mermaid_src code node
SRC_GAP = 120  # gap between the graph and the parked code node


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


def layout(d: DiagramInput) -> tuple[dict[str, Box], Box, Box]:
    """Return (per-node boxes keyed by id, the diagram_root group box, the mermaid_src code-node box)."""
    rank = _ranks(d)
    horizontal = d.direction in ("LR", "RL")

    # Group nodes by rank, preserving declaration order within a rank (determinism).
    by_rank: dict[int, list[str]] = {}
    for n in d.nodes:
        by_rank.setdefault(rank[n.id], []).append(n.id)

    boxes: dict[str, Box] = {}
    max_lane = max((len(v) for v in by_rank.values()), default=1)
    n_ranks = (max(by_rank) + 1) if by_rank else 1

    for r in sorted(by_rank):
        lane_ids = by_rank[r]
        for lane, nid in enumerate(lane_ids):
            if horizontal:
                # rank advances along x (columns); lane spreads down y.
                x = PAD + r * (NODE_W + GAP_X)
                y = PAD + LABEL_BAND + lane * (NODE_H + GAP_Y)
            else:
                # rank advances down y (rows); lane spreads across x.
                x = PAD + lane * (NODE_W + GAP_X)
                y = PAD + LABEL_BAND + r * (NODE_H + GAP_Y)
            boxes[nid] = Box(x, y, NODE_W, NODE_H)

    if horizontal:
        graph_w = n_ranks * NODE_W + (n_ranks - 1) * GAP_X
        graph_h = max_lane * NODE_H + (max_lane - 1) * GAP_Y
    else:
        graph_w = max_lane * NODE_W + (max_lane - 1) * GAP_X
        graph_h = n_ranks * NODE_H + (n_ranks - 1) * GAP_Y

    # Park the mermaid_src code node to the right of the graph, vertically centered-ish.
    src_x = PAD + graph_w + SRC_GAP
    src_y = PAD + LABEL_BAND
    src_h = max(NODE_H, graph_h)
    src_box = Box(src_x, src_y, SRC_W, src_h)

    group_w = src_x + SRC_W + PAD
    group_h = PAD * 2 + LABEL_BAND + max(graph_h, src_h)
    group_box = Box(0, 0, group_w, group_h)
    return boxes, group_box, src_box
