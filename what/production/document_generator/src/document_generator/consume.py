"""The document generator: ``Document`` -> a v2.0.0-conformant, aDNA-Native multi-page ``.canvas``.

Each canvas page is a **group** node nested in a ``doc_root`` group (the single canonical surface). Pipeline:
  1. **reflow** the model pages into emitted canvas pages (``layout.paginate`` — section-level auto-pagination; E4.2);
  2. assemble the ``canvas_std`` **source contract** — doc_root group + per-page group + interior nodes (from
     ``blocks.build_page``); a ``sequence`` chain across the *emitted* pages, ``reading_order`` within each page, and
     ``adjacency`` from each section's prose to its citations;
  3. emit the genre **format/visual contracts** (F1–F7 / V1–V8 / X1–X14) as declarative ``_reserved`` metadata —
     ``semantic_bindings.{genre,format,visual}``, ``brand_style_pack_ref``, derived ``panel_link.surfaces`` (each
     backed by a ``region``-class marker node) and the ``surface_subclass`` ``region`` (first use of the class). All
     **additive**: an empty genre emits nothing new, so the output is byte-identical to E4.1;
  4. ``canvas_std.to_canvas`` (sets ``toEnd`` + ``_reserved.sync``), then ``isStartNode`` + heading color, then
     enrich ``_reserved`` to aDNA-Native.

``canvas_std`` is the only substrate dependency and is never mutated (substrate-neutrality / ADR-004 two-shelf firewall).
E4.2 records visual/format **intent** declaratively; it renders no pixels (typography/palette/figure-placement/VR1 are
PT-P5). Any field with no Standard slot is recorded as open ``qualities``/binding data — never as a schema edit.
"""

from __future__ import annotations

from typing import Any

from canvas_std import to_canvas

from document_generator import blocks, layout
from document_generator.model import Document, OrphanDetector, StyleLock

ADNA_VERSION = "2.0.0"
DOC_ID = "doc_root"
HEADING_COLOR = "5"  # a valid color slot; degrades cleanly (proven Core/Extended-valid by the degradation tests)


def _format_binding(fc) -> dict[str, Any]:
    """The set format-contract fields (F1–F7) as a declarative ``semantic_bindings.format`` block."""
    d: dict[str, Any] = {}
    lw = fc.length_window
    if lw.is_set():
        d["length_window"] = {"min": lw.min, "max": lw.max, "unit": lw.unit}                       # F1
    if fc.sections:
        d["sections"] = [{"name": s.name, "required": s.required, "order_locked": s.order_locked}   # F2
                         for s in fc.sections]
    if fc.output_surfaces:
        d["output_surfaces"] = [                                                                    # F3
            {"surface": s.surface, "role": s.role, **({"aspect_ratio": s.aspect_ratio} if s.aspect_ratio else {})}
            for s in fc.output_surfaces
        ]
    ac = fc.asset_conventions
    if ac.is_set():
        d["asset_conventions"] = {k: v for k, v in                                                  # F4
                                  {"table_form": ac.table_form, "equation_form": ac.equation_form,
                                   "figure_placement": ac.figure_placement}.items() if v}
    if fc.round_trip_surface:
        d["round_trip_surface"] = fc.round_trip_surface                                             # F5
    ftr = fc.format_template_ref
    if ftr.is_set():
        d["format_template_ref"] = {k: v for k, v in                                                # F6
                                    {"owner": ftr.owner, "template_id": ftr.template_id,
                                     "resolver": ftr.resolver}.items() if v}
    nc = fc.naming_convention
    if nc.is_set():
        d["naming_convention"] = {k: v for k, v in                                                  # F7
                                  {"label_form": nc.label_form, "migration_rule": nc.migration_rule}.items() if v}
    return d


def _visual_binding(vc) -> dict[str, Any]:
    """The set cross-asset visual fields (X1–X14, minus X3 brand) + a default-asset (V1–V8) summary."""
    d: dict[str, Any] = {}
    cr = vc.cross
    if cr.engine_map:
        d["engine_map"] = dict(cr.engine_map)                                                       # X1
    if cr.orphan_detector != OrphanDetector():
        d["orphan_detector"] = {"mode": cr.orphan_detector.mode, "threshold": cr.orphan_detector.threshold}  # X2
    if cr.color_signal_vocabulary:
        d["color_signal_vocabulary"] = dict(cr.color_signal_vocabulary)                             # X4 (names, not RGB)
    if cr.style_lock != StyleLock():
        d["style_lock"] = {k: v for k, v in
                           {"kind": cr.style_lock.kind, "provider": cr.style_lock.provider}.items() if v}  # X5
    if cr.performance_budget:
        d["performance_budget"] = dict(cr.performance_budget)                                       # X7
    if cr.naming_convention.is_set():
        d["naming_convention"] = {k: v for k, v in
                                  {"label_form": cr.naming_convention.label_form,
                                   "migration_rule": cr.naming_convention.migration_rule}.items() if v}  # X8
    if cr.overlay_extends_base:
        d["overlay_extends_base"] = True                                                            # X9
    if cr.visual_voices:
        d["visual_voices"] = list(cr.visual_voices)                                                 # X10
    if cr.substrate_inheritance != "own":
        d["substrate_inheritance"] = cr.substrate_inheritance                                       # X11
    if cr.surface_subclass:
        d["surface_subclass"] = cr.surface_subclass                                                 # X12
    if cr.form_fill_exemption:
        d["form_fill_exemption"] = True                                                             # X13
    if cr.export_round_trip:
        d["export_round_trip"] = dict(cr.export_round_trip)                                         # X14
    da_d = blocks._asset_quals(vc.default_asset)                                                     # V2–V8 summary
    if vc.default_asset.substrate != "canvas":
        da_d["substrate"] = vc.default_asset.substrate                                              # V1
    if vc.default_asset.caption_form != "descriptive":
        da_d["caption_form"] = vc.default_asset.caption_form                                        # V6
    if da_d:
        d["default_asset"] = da_d
    return d


def _emit_contract(genre, nodes, component_types, regions, gutter_x) -> list[dict[str, Any]]:
    """Append the contract-derived marker nodes (derived surfaces + the surface_subclass region) to the source,
    register their ``component_types`` + ``regions``, and return the ``panel_link.surfaces`` list.

    A-5 requires every ``surfaces[].id`` to resolve to a real node and exactly one canonical surface: the canonical
    output_surface maps onto ``doc_root``; each derived surface gets a zero-content ``region``-class group marker (the
    `region` class's first use). With an empty genre this adds no nodes and returns the E4.1 default surfaces list.
    """
    fc = genre.format_spec
    vc = genre.visual_spec
    surfaces: list[dict[str, Any]] = [{"id": DOC_ID, "role": "canonical"}]
    gy = layout.DOC_PAD
    for s in fc.output_surfaces:
        if s.role == "canonical":
            surfaces[0]["surface"] = s.surface
            if s.aspect_ratio:
                surfaces[0]["aspect_ratio"] = s.aspect_ratio
        else:
            mid = f"surface_{s.surface}"
            nodes.append({"id": mid, "type": "group", "label": f"surface: {s.surface}",
                          "x": gutter_x, "y": gy, "width": 240, "height": 48})
            component_types[mid] = {"class": "region", "degrades_to": "group",
                                    "qualities": {"role": "derived_surface", "surface": s.surface}}
            regions[mid] = {"flow": "none", "pagination": "none", "surface": s.surface}
            surf: dict[str, Any] = {"id": mid, "role": "derived", "surface": s.surface}
            if s.aspect_ratio:
                surf["aspect_ratio"] = s.aspect_ratio
            surfaces.append(surf)
            gy += 64
    if fc.round_trip_surface:
        surfaces[0]["round_trip"] = fc.round_trip_surface                                            # F5 on the canonical
    if vc.is_set():  # X12 — exercise the `region` class for the surface sub-class
        rid = "rgn_subclass"
        nodes.append({"id": rid, "type": "group", "label": f"subclass: {vc.cross.surface_subclass}",
                      "x": gutter_x, "y": gy, "width": 240, "height": 48})
        component_types[rid] = {"class": "region", "degrades_to": "group",
                                "qualities": {"surface_subclass": vc.cross.surface_subclass}}
        regions[rid] = {"flow": "vertical", "pagination": "paged",
                        "surface": vc.cross.surface_subclass, "subclass": vc.cross.surface_subclass}
    return surfaces


def build_document(document: Document) -> dict[str, Any]:
    """Map a ``Document`` to a v2.0.0 aDNA-Native multi-page ``.canvas`` document (a plain dict)."""
    genre = document.genre
    default_asset = genre.visual_spec.default_asset

    # Reflow: model pages -> emitted canvas pages (section-level pagination; CANVAS-L-002).
    fragments = [pf for page in document.pages for pf in layout.paginate(page)]
    n_pages = len(fragments)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    component_types: dict[str, dict[str, Any]] = {}
    panel_link_edges: dict[str, dict[str, str]] = {}
    regions: dict[str, dict[str, Any]] = {}
    heading_ids: list[str] = []

    doc_box = layout.doc_box(n_pages)
    nodes.append({"id": DOC_ID, "type": "group", "label": document.title, **doc_box.as_node()})
    component_types[DOC_ID] = {"class": "panel", "semantic_type": "document", "degrades_to": "group"}
    # The document-level region carries the actual word count as a `words` extent (the page regions carry `pages`).
    regions[DOC_ID] = {"flow": "vertical", "pagination": "paged",
                       "extent": {"unit": "words", "max": document.word_count()}, "surface": "print_page"}

    page_ids: list[str] = []
    for g, fragment in enumerate(fragments):
        pid = f"page{g}"
        pbox = layout.page_box(g)
        nodes.append({"id": pid, "type": "group", "label": f"Page {g + 1}", **pbox.as_node()})
        component_types[pid] = {"class": "panel", "semantic_type": "page", "degrades_to": "group"}
        regions[pid] = {"flow": "vertical", "pagination": "paged",
                        "extent": {"unit": "pages", "max": 1}, "surface": "print_page"}
        page_ids.append(pid)

        build = blocks.build_page(fragment, pid, pbox, default_asset)
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

    # E4.2 contract metadata (additive; an empty genre is a no-op -> E4.1-identical output).
    surfaces = _emit_contract(genre, nodes, component_types, regions, doc_box.w + 60)
    semantic_bindings: dict[str, Any] = {"profile": "long_document"}
    if genre.name:
        semantic_bindings["genre"] = genre.name
    fb = _format_binding(genre.format_spec) if genre.format_spec.is_set() else {}
    if fb:
        semantic_bindings["format"] = fb
    vb = _visual_binding(genre.visual_spec) if genre.visual_spec.is_set() else {}
    if vb:
        semantic_bindings["visual"] = vb
    brand = genre.visual_spec.cross.brand_style_pack_ref
    brand_ref = ({"vault": brand.vault, "pack_id": brand.pack_id, "version": brand.version}
                 if brand.is_set() else None)

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
    reserved["semantic_bindings"] = semantic_bindings
    if brand_ref:
        reserved["brand_style_pack_ref"] = brand_ref
    reserved["panel_link"] = {
        "edges": panel_link_edges,
        "regions": regions,
        "surfaces": surfaces,
    }
    reserved["context_object"] = {"id": document.id, "version": document.version, "refs": list(document.refs)}
    return doc
