---
type: spec
spec_id: spec_panel_link_semantics
title: "aDNA Canvas panel/link semantics (D5) — flow, pagination, reading-order for non-DAG outputs"
standard_version: "2.0.0"
status: proposed
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
phase: P2
resolves: D5
tags: [spec, canvas, panel-link, flow, pagination, genesis, p2, d5]
---

# aDNA Canvas Panel/Link Semantics (D5)

> **Status: PROPOSED — HELD at the P2 exit gate.** Specifies how non-DAG 2D outputs (papers, letters, decks,
> comics, sites) express reading-order, flow, pagination, and regions **without breaking lattice-graph
> semantics**. Additive in `_reserved.panel_link`. RFC 2119 keywords.

## 1. Scope & the non-breaking guarantee

The v1.0.0 canvas is a **DAG of typed nodes/edges** (data/control/optional flow). Documents and decks need a
*different* relation: a **reading path** (this slide after that one; this section before that; this column wraps
to the next page). These are expressed as **additive typed edges + region properties in `_reserved.panel_link`**.
A stripper that removes `_reserved` **MUST** leave the baseline graph intact — panel/link semantics never alter
`fromNode`/`toNode`/`toEnd` or node geometry ([[spec_adna_canvas_standard]] §11). Lattice DAG semantics and
reading-path semantics coexist as two layers over the same nodes.

## 2. A "panel"

A **panel** is a `group`/`region` component ([[spec_component_model]] §2) that bounds a set of components and
carries flow/region properties. "Possibly-linked panels" — the canvas thesis — are panels joined by §3 reading
edges. A deck slide, a comic page, a printed page, and a responsive site section are all panels.

## 3. Reading-path edge kinds (additive)

`_reserved.panel_link.edges` declares typed reading relations, keyed by baseline edge `id` (the edge also exists
in the baseline graph so it degrades to a plain arrow):

| kind | meaning |
|------|---------|
| `sequence` | strict next/previous order (slides, pages) |
| `reading_order` | soft reading order within a panel (top-to-bottom, column flow) |
| `adjacency` | spatial neighbor without order (gutter-adjacent comic panels) |
| `dependency` | preserves the lattice data/control DAG (passthrough; not a reading relation) |

A `sequence` chain **MUST** be acyclic and **SHOULD** originate at the node flagged `isStartNode: true`
(Advanced Canvas, from §C4 presentation-mode). Tools rendering a linear output **MUST** follow `sequence`, then
`reading_order`, ignoring `dependency` for pagination.

## 4. Region & pagination properties

`_reserved.panel_link.regions` keys a panel `id` →
```
regions:
  <group_id>:
    flow:        none | vertical | horizontal | columns
    pagination:  none | paged | continuous
    extent:      { unit: words|pages|slides, max: <n> }   # from LF length_window
    responsive:  none | <breakpoint-profile>              # sites; producer-resolved
    surface:     print_page | slide | web | letter | …    # surface subclass (LF)
```
`pagination: paged` + `extent` define page breaks for print/PDF; `flow: columns` defines wrap. These inform
producer layout; the Standard fixes the **declaration**, not the layout engine (C8).

## 5. Document flow (absorbed from LF format-contract, D2-inventory)

5.1. A long-form document is a panel with `flow: vertical|columns` whose child components form an **ordered,
order-locked section list** — the LF format-spec's `sections` ([[p1_source_inventory]] §D2). Order-lock is
expressed as a `sequence` chain over section-panels.

5.2. **Multi-surface.** `_reserved.panel_link.surfaces` declares `output_surfaces` with exactly one `canonical`
and zero-or-more `derived` (LF F3). The canonical surface is the round-trip authority
(`spec_roundtrip_protocol_v2.md`); derived surfaces are regenerated, never hand-authored as source.

5.3. **Naming/anchor links.** `caption` components and cross-references use a `naming_convention` + an
**orphan check** (every referenced anchor exists) — link-existence semantics the Standard owns (LF X8/F7 + the
visual contract's `orphan_detector`).

## 6. Conformance

Panel/link semantics are an **aDNA-Native** feature. A validator **MUST** check: every `panel_link.edges` /
`regions` / `surfaces` key references an existing baseline `id`; `sequence` chains are acyclic; exactly one
`canonical` surface; `extent.unit`/`flow`/`pagination` ∈ their enums; no orphaned anchors. Absent
`_reserved.panel_link` → a plain canvas/lattice (no reading path), still valid Core/Extended.

## 7. Related
- [[spec_adna_canvas_standard]] (§11 degradation) · [[spec_component_model]] (region/panel components) ·
  `spec_roundtrip_protocol_v2.md` (canonical surface authority) · [[adr_002_literatureforge_seam]] (document-AS-canvas) ·
  [[p1_source_inventory]] §C4/§D1/§D2 (slide-graph + LF format/visual contracts).
