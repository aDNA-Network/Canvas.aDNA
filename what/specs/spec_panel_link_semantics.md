---
type: spec
spec_id: spec_panel_link_semantics
title: "aDNA Canvas panel/link semantics (D5) — flow, pagination, reading-order for non-DAG outputs"
standard_version: "2.2.0"
status: ratified
created: 2026-06-12
updated: 2026-06-23
last_edited_by: agent_stanley
phase: P2
resolves: D5
tags: [spec, canvas, panel-link, flow, pagination, genesis, p2, d5]
---

# aDNA Canvas Panel/Link Semantics (D5)

> **Status: RATIFIED 2026-06-12 (operator, P2 gate).** Specifies how non-DAG 2D outputs (papers, letters, decks,
> comics, sites) express reading-order, flow, pagination, and regions **without breaking lattice-graph
> semantics**. Additive in `_reserved.panel_link`. RFC 2119 keywords.
>
> **Errata 2026-06-20 (LIP queue B1/B3; ships in v2.0.1, cut 2026-06-20).** §5.3/§6 **sharpened** to
> define the anchor model normatively (the previously under-specified "orphan check"); §4/§5.1 **clarified** to
> resolve the pagination-construct ambiguity (a page is a `panel` carrying a `region`; pagination is
> region-declared; the `sequence` unit is the section-panel). These are clarifications/errata — they make explicit
> what §6 already mandated, changing no rule. The reference validator now enforces the anchor layer
> (`canvas_std::validate_anchors`). `standard_version` advanced to 2.0.1 at the operator's release-cut 2026-06-20
> (`what/decisions/lip_queue_disposition.md`).
>
> **Errata 2026-06-21 (Atelier AT-1/AT-2; ships in v2.0.2, cut 2026-06-21).** §4 **clarified** that `extent` is
> **optional** — it expresses pagination/length (`words|pages|slides`), so a non-paginated single-surface region
> (`pagination: none` — e.g. a diagram/graph) legitimately omits it (AT-1) — and that the `surface` subclass label
> (§4, and `surfaces[].surface` §5.2) is an **open, free-form vocabulary** (producer-defined; the listed tokens are
> non-normative examples), not a closed enum (AT-2); §6 restates both. No rule changes — this makes explicit what the
> validator already does (`extent` validated only when present; the `surface` label never enum-checked). Surfaced while
> building `diagram_generator` + `comic_generator` (Operation Atelier). `standard_version` advanced to 2.0.2 at the
> operator's release-cut 2026-06-21 (`what/decisions/lip_queue_disposition.md` §Atelier addendum).

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
    extent:      { unit: words|pages|slides, max: <n> }   # OPTIONAL — from LF length_window (pagination/length)
    responsive:  none | <breakpoint-profile>              # sites; producer-resolved
    surface:     print_page | slide | web | letter | …    # surface subclass (LF); OPEN vocabulary (examples)
```
`pagination: paged` + `extent` define page breaks for print/PDF; `flow: columns` defines wrap. These inform
producer layout; the Standard fixes the **declaration**, not the layout engine (C8).

**`extent` is OPTIONAL (AT-1).** It expresses a **pagination/length** window — its units (`words|pages|slides`)
are length measures — so it applies to paginated or length-bearing regions. A **non-paginated single-surface
region** (`pagination: none` — a diagram/graph, a single graphic) is sized by its content, not paged, and
**legitimately omits `extent`** (there is no length unit for a node-graph; do **not** invent one). When `extent`
is present, its `unit` MUST be in the enum (§6); when absent, the region is simply non-length-bound.

**`surface` is an OPEN vocabulary (AT-2).** The `surface` subclass label is a **free-form, producer-defined
string** naming the output subclass; `print_page | slide | web | letter | …` are **non-normative examples**, not a
closed enum. Producers mint surface tokens for their output kind (e.g. `comic_page`, or a diagram-type name like
`flowchart`). Tools MUST accept unknown `surface` values as valid; the Standard does **not** enum-check this label
(it is application-specific — it belongs to the producer, not the grammar). Interop tools wanting a shared
vocabulary SHOULD treat unrecognized tokens as opaque rather than rejecting them.

**Pagination ownership — a page is a panel that carries a region (no separate "page" construct).** A page,
slide, or printed sheet is a **`panel`** (a `group` component, §2) that **carries these region properties**;
**pagination is declared on the `region`**, never on a free-standing page object (there is none). A producer
emits, per page, one `component_types` entry (`class: panel`, `semantic_type: page|slide`) **and** one
`regions[<page_id>]` entry (`pagination: paged`, `extent`). Ordering across pages is a §3 `sequence` chain — so
the **paginated unit** (a region-bearing page-`panel`) and the **sequenced unit** (the same panel) coincide,
while pagination (region-declared) and reading order (`sequence`/`reading_order`-declared) stay orthogonal layers
over the same panels. The reference producer `document_generator` does exactly this (`consume.py`: each `page{g}`
is a `panel`+`region`, chained by `seq_{i}` `sequence` edges).

## 5. Document flow (absorbed from LF format-contract, D2-inventory)

5.1. A long-form document is a panel with `flow: vertical|columns` whose child components form an **ordered,
order-locked section list** — the LF format-spec's `sections` ([[p1_source_inventory]] §D2). Order-lock is
expressed as a `sequence` chain over section-panels. The **`sequence` unit is the section-panel** (a page-level
`panel`, §4): one `sequence` edge per adjacent page/section pair. A multi-page document and a single page with
multiple sections are the same construct at different granularities — panels chained by `sequence`, each panel a
region (§4) — so "which owns pagination, the region or the page?" has one answer: **the region**, carried by the
page-`panel`.

5.2. **Multi-surface.** `_reserved.panel_link.surfaces` declares `output_surfaces` with exactly one `canonical`
and zero-or-more `derived` (LF F3). The canonical surface is the round-trip authority
(`spec_roundtrip_protocol_v2.md`); derived surfaces are regenerated, never hand-authored as source. Each entry's
`surface` field uses the **same open vocabulary** as the region `surface` subclass (§4, AT-2) — a free-form
producer-defined token, not a closed enum. The validator enforces the `role` set (exactly one `canonical`) and id
resolution, never the `surface` label.

5.3. **Naming/anchor links.** `caption` components and cross-references resolve against **anchors** — a
referenceable target (a baseline node, optionally surfaced under a human label). The Standard owns the
*declarative* anchor layer; the orphan-**traversal** engine (scanning prose for label references) is
producer-side (C8 — the Standard fixes the *declaration*, not the *engine*).

- **`naming_convention`** (LF F7/X8) governs how anchor **labels** are formed:
  `{ label_form: descriptive|legacy, migration_rule: <str> }`. It rides on the contract bindings
  (`_reserved.semantic_bindings.format`/`visual`) or, equivalently, on `_reserved.panel_link`.
- **`orphan_detector`** (LF X2) configures the producer-side orphan pass:
  `{ mode: label_ref|src_cited, threshold: <0..1> }`. The Standard validates this **declaration**; it does not
  run the traversal.
- **Anchors & references.** An optional `_reserved.panel_link.anchors` map keys a **label → a baseline node
  `id`**. A component declares an explicit cross-reference via a `qualities` key in
  { `ref`, `anchor`, `anchor_ref`, `cites`, `for` }, whose value is a node `id` (or a declared anchor label).
  The **orphan check** (§6): every declared anchor and every explicit reference **MUST** resolve — no orphaned
  anchor. A canvas that declares conventions but no explicit references is vacuously orphan-clean.

## 6. Conformance

Panel/link semantics are an **aDNA-Native** feature. A validator **MUST** check: every `panel_link.edges` /
`regions` / `surfaces` key references an existing baseline `id`; `sequence` chains are acyclic; exactly one
`canonical` surface; `flow`/`pagination` ∈ their enums, and `extent.unit` ∈ its enum **when `extent` is present**.
`extent` is **OPTIONAL** (§4, AT-1) — a non-paginated single-surface region (e.g. a diagram) omits it, and its
absence is conformant. The `surface` subclass label (region `surface` and `surfaces[].surface`) is an **open
vocabulary** (§4/§5.2, AT-2) and is **NOT** enum-checked — a validator MUST NOT reject a canvas for an unrecognized
`surface` token.

For the **anchor layer** (§5.3) the validator **MUST** check, wherever each is declared: `naming_convention.label_form
∈ {descriptive, legacy}` and `migration_rule` is a string; `orphan_detector.mode ∈ {label_ref, src_cited}` and
`threshold ∈ [0,1]`; every `_reserved.panel_link.anchors` entry and every explicit component anchor-reference (a
`qualities` key in {`ref`, `anchor`, `anchor_ref`, `cites`, `for`}) resolves to a node `id` or a declared anchor
label — **no orphaned anchors**. The orphan-*traversal* engine (prose label scanning per `orphan_detector.mode`) is
producer-side (C8), not part of this check. Absent `_reserved.panel_link` → a plain canvas/lattice (no reading
path), still valid Core/Extended.

## 7. Related
- [[spec_adna_canvas_standard]] (§11 degradation) · [[spec_component_model]] (region/panel components) ·
  `spec_roundtrip_protocol_v2.md` (canonical surface authority) · [[adr_002_literatureforge_seam]] (document-AS-canvas) ·
  [[p1_source_inventory]] §C4/§D1/§D2 (slide-graph + LF format/visual contracts).
