"""The letter generator: ``Letter`` -> a v2.0.0-conformant, aDNA-Native one-page-letter ``.canvas``.

Single-surface, native-primary mapping (mirrors ``diagram_generator``). The whole letter is ONE ``group`` node =
``letter_root`` = the single canonical surface; each block (letterhead, date, recipient, salutation, each body
paragraph, closing, signature) is an interior baseline ``text`` node in reading order; consecutive blocks are chained
with ``reading_order`` panel-link edges (vertical bottom->top). The block's rich role rides in
``_reserved.component_types[*].semantic_type`` (free-form; never an enum) with ``class: "text"`` and
``degrades_to: "text"``.

Pipeline (the canonical four steps):
  1. assemble the ``canvas_std`` **source contract** ``{name, version, nodes, edges}`` — interior nodes are baseline
     ``text`` (no ``semantic_type`` on the source node, so ``to_canvas``'s ``lattice`` profile injects no color/shape);
  2. ``doc = to_canvas(source)`` (sets explicit edge ``toEnd`` + ``_reserved.sync``);
  3. **enrich ``_reserved`` to aDNA-Native** — component_types (panel + per-block text components) / semantic_bindings
     (the bare ``document`` profile) / panel_link (one ``letter_root`` region, one canonical surface, reading_order
     edge kinds) / context_object.

``canvas_std`` is the only substrate dependency and is never mutated (C8 — the two-shelf firewall).
"""

from __future__ import annotations

from typing import Any

from canvas_std import to_canvas

from letter_generator import layout
from letter_generator.model import Letter

ADNA_VERSION = "2.0.0"
ROOT_ID = "letter_root"
PROFILE = "document"          # producer-side profile name (bare; NEVER registered in canvas_std.schema)
SURFACE = "print_page"        # open, producer-defined surface vocabulary (AT-2)
READING_ORDER = "reading_order"


def _blocks(letter: Letter) -> list[tuple[str, str, str]]:
    """Return the ordered blocks as ``(node_id, semantic_type, text)`` in reading order.

    Multi-line blocks (sender / recipient / signature) are joined with newlines; each body paragraph is its own node
    (``body0``, ``body1``, ...). Empty blocks are dropped so the letter only carries what the author supplied.
    """
    out: list[tuple[str, str, str]] = []
    if letter.sender:
        out.append(("letterhead", "letterhead", "\n".join(letter.sender)))
    if letter.date:
        out.append(("date", "date", letter.date))
    if letter.recipient:
        out.append(("recipient", "recipient", "\n".join(letter.recipient)))
    if letter.salutation:
        out.append(("salutation", "salutation", letter.salutation))
    for i, para in enumerate(letter.body):
        out.append((f"body{i}", "body", para))
    if letter.closing:
        out.append(("closing", "closing", letter.closing))
    if letter.signature:
        out.append(("signature", "signature", "\n".join(letter.signature)))
    return out


def build_letter(letter: Letter) -> dict[str, Any]:
    """Map a ``Letter`` to a v2.0.0 aDNA-Native one-page-letter ``.canvas`` document (a plain dict)."""
    blocks = _blocks(letter)
    line_counts = [text.count("\n") + 1 for _, _, text in blocks]
    boxes, root_box = layout.stack(line_counts)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    component_types: dict[str, dict[str, Any]] = {}
    panel_link_edges: dict[str, dict[str, str]] = {}

    # 1) The single canonical surface: a group enclosing the whole letter.
    nodes.append({"id": ROOT_ID, "type": "group", "label": letter.title, **root_box.as_node()})
    component_types[ROOT_ID] = {"class": "panel", "semantic_type": PROFILE, "degrades_to": "group"}

    # Interior baseline text nodes — one per block, in reading order.
    for (nid, semantic_type, text), box in zip(blocks, boxes):
        nodes.append({"id": nid, "type": "text", "text": text, **box.as_node()})
        component_types[nid] = {
            "class": "text",            # a valid COMPONENT_CLASSES entry
            "semantic_type": semantic_type,  # free-form role (letterhead/date/.../signature) — not enum-checked
            "degrades_to": "text",
        }

    # Chain consecutive blocks with reading_order edges (linear; reading_order is NOT acyclicity-checked).
    for i in range(len(blocks) - 1):
        eid = f"flow{i}"
        edges.append({
            "id": eid,
            "fromNode": blocks[i][0],
            "toNode": blocks[i + 1][0],
            "fromSide": "bottom",
            "toSide": "top",
        })
        panel_link_edges[eid] = {"kind": READING_ORDER}

    # 2) To the substrate.
    source = {"name": letter.id, "version": letter.version, "nodes": nodes, "edges": edges}
    doc = to_canvas(source)

    # 3) Enrich _reserved -> aDNA-Native.
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    reserved["adna_version"] = ADNA_VERSION
    reserved["conformance_level"] = "adna_native"
    reserved["component_types"] = component_types
    reserved["semantic_bindings"] = {"profile": PROFILE}
    reserved["panel_link"] = {
        "edges": panel_link_edges,
        "regions": {
            ROOT_ID: {
                "flow": "vertical",
                "pagination": "paged",
                "extent": {"unit": "pages", "max": 1},
                "surface": SURFACE,
            }
        },
        "surfaces": [{"id": ROOT_ID, "role": "canonical"}],
    }
    reserved["context_object"] = {"id": letter.id, "version": letter.version, "refs": list(letter.refs)}
    return doc
