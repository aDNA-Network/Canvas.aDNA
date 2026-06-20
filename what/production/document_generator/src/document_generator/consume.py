"""The document generator: ``Document`` -> a v2.0.0-conformant, aDNA-Native multi-page ``.canvas``.

Each page is a **group** node nested in a ``doc_root`` group (the single canonical surface). Pipeline:
  1. assemble the ``canvas_std`` **source contract** — doc_root group + per-page group + interior nodes (from
     ``blocks.build_page``); a ``sequence`` chain across pages, ``reading_order`` within each page, and ``adjacency``
     from each section's prose to its citations;
  2. ``canvas_std.to_canvas`` (sets ``toEnd`` + ``_reserved.sync``);
  3. set ``isStartNode`` on page 0 + a subtle heading color (Extended; ``to_canvas`` carries only text/file/url/label);
  4. **enrich ``_reserved`` to aDNA-Native** — component_types (doc/page panels + interior classes incl image/table/
     code) / semantic_bindings (``profile: long_document``) / panel_link (a region per page + the document
     ``words`` extent, **exactly one canonical surface**, sequence + reading_order + adjacency edges) / context_object.

``canvas_std`` is the only substrate dependency and is never mutated (substrate-neutrality / C8).
"""

from __future__ import annotations

from typing import Any

from canvas_std import to_canvas

from document_generator import blocks, layout
from document_generator.model import Document

ADNA_VERSION = "2.0.0"
DOC_ID = "doc_root"
HEADING_COLOR = "5"  # a valid color slot; degrades cleanly (proven Core/Extended-valid by the degradation tests)


def build_document(document: Document) -> dict[str, Any]:
    """Map a ``Document`` to a v2.0.0 aDNA-Native multi-page ``.canvas`` document (a plain dict)."""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    component_types: dict[str, dict[str, Any]] = {}
    panel_link_edges: dict[str, dict[str, str]] = {}
    regions: dict[str, dict[str, Any]] = {}
    heading_ids: list[str] = []

    n_pages = len(document.pages)
    doc_box = layout.doc_box(n_pages)
    nodes.append({"id": DOC_ID, "type": "group", "label": document.title, **doc_box.as_node()})
    component_types[DOC_ID] = {"class": "panel", "semantic_type": "document", "degrades_to": "group"}
    # The document-level region carries the LF length_window as a `words` extent (the page regions carry `pages`).
    regions[DOC_ID] = {"flow": "vertical", "pagination": "paged",
                       "extent": {"unit": "words", "max": document.word_count()}, "surface": "print_page"}

    page_ids: list[str] = []
    for p, page in enumerate(document.pages):
        pid = f"page{p}"
        pbox = layout.page_box(p)
        nodes.append({"id": pid, "type": "group", "label": f"Page {p + 1}", **pbox.as_node()})
        component_types[pid] = {"class": "panel", "semantic_type": "page", "degrades_to": "group"}
        regions[pid] = {"flow": "vertical", "pagination": "paged",
                        "extent": {"unit": "pages", "max": 1}, "surface": "print_page"}
        page_ids.append(pid)

        build = blocks.build_page(page, pid, pbox)
        nodes.extend(build.nodes)
        component_types.update(build.component_types)
        heading_ids.extend(build.headings)
        for k in range(len(build.reading) - 1):
            eid = f"{pid}_ro_{k}"
            edges.append({"id": eid, "fromNode": build.reading[k], "toNode": build.reading[k + 1],
                          "fromSide": "bottom", "toSide": "top"})
            panel_link_edges[eid] = {"kind": "reading_order"}
        for n, (a, b) in enumerate(build.adjacency):
            eid = f"{pid}_adj_{n}"
            edges.append({"id": eid, "fromNode": a, "toNode": b, "fromSide": "right", "toSide": "left"})
            panel_link_edges[eid] = {"kind": "adjacency"}

    for i in range(len(page_ids) - 1):
        eid = f"seq_{i}"
        edges.append({"id": eid, "fromNode": page_ids[i], "toNode": page_ids[i + 1],
                      "fromSide": "bottom", "toSide": "top"})
        panel_link_edges[eid] = {"kind": "sequence"}

    source = {"name": document.id, "version": document.version, "nodes": nodes, "edges": edges}
    doc = to_canvas(source)

    # isStartNode + heading color: Advanced Canvas (Extended) fields to_canvas doesn't carry — set them post-hoc (KEEP).
    by_id = {n["id"]: n for n in doc["nodes"]}
    by_id[page_ids[0]]["isStartNode"] = True
    for hid in heading_ids:
        by_id[hid]["color"] = HEADING_COLOR

    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    reserved["adna_version"] = ADNA_VERSION
    reserved["conformance_level"] = "adna_native"
    reserved["component_types"] = component_types
    reserved["semantic_bindings"] = {"profile": "long_document"}
    reserved["panel_link"] = {
        "edges": panel_link_edges,
        "regions": regions,
        "surfaces": [{"id": DOC_ID, "role": "canonical"}],
    }
    reserved["context_object"] = {"id": document.id, "version": document.version, "refs": list(document.refs)}
    return doc
