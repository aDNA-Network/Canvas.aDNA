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
LABEL_BAND = 56  # minimum room under the group label
TITLE_GAP = 40  # clearance between the title node and rank 0 (overlap tolerance is 5px)
SRC_W = 480  # width of the parked mermaid_src code node
SRC_GAP = 120  # gap between the graph and the parked code node
TITLE_H = 60  # minimum height of the `#### <title>` heading node (CV-HIERARCHY-01 title slot)
H4_LEAD_COST = 42.6  # mirrors canvas_core.text_metrics.OBSIDIAN_LEAD_COST["h4"] — see the note below;
                     # the mirror is interim, not a dependency rule (corrected 2026-09-06)

# --- Visual-gate constants (calibrated against canvas_core/traps, not guessed) -------------------
# CV-TEXT-BOUNDS-01 measures with the Obsidian CSS model and passes when
# `measure_obsidian_extent(text, w) <= OBSIDIAN_SAFE_FILL * height`.
#
# ⛩ CORRECTED 2026-09-06. This block previously justified the constants below with "a producer must
# not depend on a sibling producer". That constraint is NOT this vault's rule and the vault's own
# code contradicts it: `comic_render/compose.py` does `from canvas_core.print import ...`, and
# adr_004 sites `canvas_core` as the shared ENGINE SHELF (what/production/), not a sibling producer.
# So importing `canvas_core.text_metrics` here was legal all along.
#
# The constants therefore stand only as an INTERIM: they are over-estimates derived from two live
# trap readings (666px/18 lines and 1171px/29 lines at w=480) and rounded up, and they pass — but
# they are a mirror of a measurement rather than the measurement. The producer-wide re-gate
# (F-P2-6) should replace them with a shared `canvas_core/layout_fit.py` over the same
# `text_metrics` functions the traps call, so producer and trap share one source of truth.
SRC_LINE_H = 44        # px per rendered line at SRC_W (measured ~37-40; rounded up)
SRC_WRAP_COLS = 46     # chars per line before wrapping at SRC_W (conservative; measured ~52)
SAFE_FILL = 0.9        # trap's OBSIDIAN_SAFE_FILL — usable height is 90% of declared

# CV-GROUP-PADDING-01 fires when the children's bounding box fills >90% of the container on
# either axis. A FIXED pad cannot satisfy a ratio: it fired at 90.36% here purely because the
# graph got wide, and would fire on any diagram past ~1440px. Padding must scale with content.
GROUP_FILL_TARGET = 0.88  # aim below the 0.90 threshold, leaving headroom


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

    Wrap each source line at ``SRC_WRAP_COLS``, cost ``SRC_LINE_H`` per rendered line (plus the two
    code-fence lines the consumer adds), then divide by ``SAFE_FILL`` because the trap only counts
    90% of a node's declared height as usable. Deliberately over-estimates — a too-tall code node is
    invisible to a reader; a too-short one silently truncates the source at ~14% shown, which is the
    defect this replaces.
    """
    rendered = 2  # the ```mermaid fence open + close
    for line in mermaid.splitlines():
        rendered += max(1, -(-len(line) // SRC_WRAP_COLS))  # ceil-div
    return int(rendered * SRC_LINE_H / SAFE_FILL)


def title_height_for(title: str, width: int) -> int:
    """Height the `#### <title>` node needs so CV-TEXT-BOUNDS-01 passes.

    The `h4` lead costs 42.6px before a character renders, and a long title wraps. Charge the lead
    plus a body line per wrapped row, then divide by SAFE_FILL (only 90% of declared height counts).
    """
    cols = max(20, int(width / 10))       # ~10px per char at heading weight (conservative)
    rows = max(1, -(-len(title) // cols))  # ceil-div
    return max(TITLE_H, int((H4_LEAD_COST + rows * SRC_LINE_H) / SAFE_FILL))


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
    group_w = max(bb_w + 2 * PAD, int(bb_w / GROUP_FILL_TARGET) + 1)
    group_h = max(bb_h + 2 * PAD, int(bb_h / GROUP_FILL_TARGET) + 1)
    group_box = Box(0, 0, group_w, group_h)
    return boxes, group_box, src_box, title_box
