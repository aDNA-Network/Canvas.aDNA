---
type: decision
artifact_type: lip_draft
title: "LIP DRAFT — derived surfaces: region-backed node vs pure metadata (B4)"
status: submitted
lip_number: "LIP-0008"
filed_as: "lattice-labs/how/governance/lips/lip_0008_derived_surface_pure_metadata.md"
created: 2026-06-20
updated: 2026-06-20
last_edited_by: agent_stanley
phase: post-keystone
target_process: "lattice-labs/how/governance/lips/lip_0001_lip_process.md"
tags: [lip, draft, canvas, panel-link, surface, conformance, errata, b4]
---

# LIP DRAFT — derived surfaces: region-backed node vs pure metadata (B4)

> **✅ FILED as LIP-0008 + REVIEW OPENED 2026-06-20** — submitted to
> `lattice-labs/how/governance/lips/lip_0008_derived_surface_pure_metadata.md`, registered (`lip_registry.md`), and
> **Review opened** (status `draft`→`review`; LIP-0001 formal ≥7-day period, **earliest close 2026-06-27**). On
> **Final** the A-5 relaxation lands in Canvas Standard **v2.1.0** at the §5 sites below. This draft is retained as the
> Canvas-side decision record.
>
> **DIRECTION APPROVED 2026-06-20 (operator) — option (ii) pure metadata; NOT YET RATIFIED.** Staged in Canvas.aDNA
> as the B4 decision vehicle (LIP queue, `lip_queue_disposition.md`). Because (ii) **relaxes A-5** it is a **MINOR**
> change that **MUST** ride a real lattice-labs LIP (`lip_0001_lip_process.md`, ≥7-day review) before any code/spec
> change — so **no change to `spec_conformance_suite` (A-5), `spec_panel_link_semantics §5.2`, or `canvas_std`
> occurs this session**; it lands in **v2.1.0** when the LIP reaches Final. See **Disposition** below.

## Disposition — DIRECTION LOCKED 2026-06-20 (operator); pending LIP → v2.1.0

**Operator chose option (ii) — relax A-5, derived surfaces as pure metadata** (drop the synthetic `region`-class
backing node). This is a **MINOR** conformance relaxation, so — unlike B2 — it is **not** applied as a PATCH this
session; it rides the formal LIP process:

1. **Submit** this draft to `lattice-labs/how/governance/lips/` (number it; cross-vault, operator-owned) and start
   the **≥7-day review** (calendar gate, `lip_0001_lip_process.md`).
2. **On Final → land in v2.1.0** at the confirmed sites: `canvas_std/reserved.py::validate_panel_link` surfaces
   loop (`reserved.py:161–168`) changes from "every surface `id` resolves" to "the canonical surface resolves; a
   `role: derived` surface MAY omit `id`"; amend conformance **A-5** (`spec_conformance_suite.md`) +
   `spec_panel_link_semantics §5.2`; producers (`document_generator/consume.py`) may then stop minting the marker.

Backwards-compatible (relaxing): every currently-valid canvas stays valid. Option (i) (keep/bless the backing node)
**not taken**. The draft body below is retained as the decision record.

## Summary

Conformance check **A-5** requires every `_reserved.panel_link.surfaces[].id` to resolve to a real node. A
**derived** surface (`html`, `funder_portal`) has no content, so `document_generator/consume.py` mints a
**synthetic `region`-class marker node** (`surface_<name>`, `qualities.role: derived_surface`) purely to satisfy
A-5. Decide whether to keep requiring that backing node or to allow derived surfaces to be pure metadata.

## Motivation

Discovered building `document_generator` E4.2 (the first use of `region`-class derived-surface markers). The
canonical surface is the round-trip authority (§5.2); derived surfaces are regenerated, never hand-authored. A
derived surface therefore has nothing to point at — yet A-5's blanket "every surface id resolves" forces the
producer to fabricate an empty marker node solely to pass validation. That is a small but real wart: synthetic
nodes with no content inflate the baseline graph and exist only to satisfy a check.

## Options

- **(i) Keep the backing node (status quo + document the pattern).** Bless the `region`-class
  `role: derived_surface` marker as the canonical representation of a derived surface; optionally teach
  `validate_panel_link` to *require* that a `surfaces[role=derived]` entry's `id` resolves to a `region`-class
  node carrying `qualities.role: derived_surface`. **PATCH/MINOR** (clarification, or a tightened check). Pros:
  every surface has a uniform on-canvas anchor; visualizers can show derived surfaces as nodes. Cons: keeps the
  synthetic-node wart; producers must keep minting markers.

- **(ii) Relax A-5 — allow derived surfaces as pure metadata *(lean)*.** Amend A-5 + §5.2 so a `role: derived`
  surface MAY omit `id` (and the backing node), carrying only `{surface, role: derived, …}` metadata; A-5's
  id-resolution requirement applies to the **canonical** surface only (which already must be exactly one and must
  resolve). **MINOR** (v2.1.0) — additive/relaxing, conformance-optional. Pros: removes the synthetic node;
  honors §5.2 (derived = regenerated, not a source node); the canonical surface remains the single resolved
  round-trip authority, so a metadata-only derived surface is harmless. Cons: surfaces become non-uniform (some
  node-backed, some not); any tool assuming `surfaces[].id` always resolves must special-case `role: derived`.

## Recommendation

**Lean (ii)** — a metadata-only derived surface matches §5.2's "derived surfaces are regenerated, never
hand-authored" and drops a synthetic-node wart, while the canonical surface keeps the resolution guarantee that
matters for round-trip. But this is a genuine conformance call (it changes what A-5 asserts and what downstream
tooling may assume), so it is **explicitly the operator's decision** — both options are carried here in full.

> Implementation note (either option): the B1 work added `validate_anchors`; if **(i)** is chosen, the
> `derived_surface` role check is a natural extension there or in `validate_panel_link`. If **(ii)** is chosen,
> `validate_panel_link`'s surface loop changes from "every surface id resolves" to "the canonical surface
> resolves; a `role: derived` surface with an `id` still resolves, but `id` becomes optional."

## Backwards compatibility

Both C4-safe (`panel_link`-scoped). (i) is non-breaking (current canvases already mint the node). (ii) is
relaxing — every currently-valid canvas (which provides ids for all surfaces) stays valid; only the requirement
loosens, so producers MAY stop minting markers going forward. No existing canvas is invalidated by either.

## Reference / related

- `spec_conformance_suite.md` (A-5) · `spec_panel_link_semantics.md §5.2` (multi-surface; canonical authority) ·
  `document_generator/src/document_generator/consume.py::_emit_contract` (the synthetic marker, lines ~126–135) ·
  `lip_queue_disposition.md` (B4 row) · `canvas_std/reserved.py::validate_panel_link` (surface-id resolution).
