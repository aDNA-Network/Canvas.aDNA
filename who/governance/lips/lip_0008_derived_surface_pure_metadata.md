---
type: lip
lip_number: "LIP-0008"
title: "Derived Surfaces as Pure Metadata (Canvas panel_link A-5 relaxation)"
author: "Stanley Bishop (Mondrian-drafted; Canvas.aDNA standard-bearer)"
status: final
created: 2026-06-20
updated: 2026-07-02
requires: []
replaces: []
last_edited_by: agent_mondrian
review_opened: 2026-06-20
review_earliest_close: 2026-06-27
migrated_from: "Archive.aDNA/lattice-labs/how/governance/lips/lip_0008_derived_surface_pure_metadata.md"
migrated_on: 2026-07-02
lands_in_version: "2.3.0"
tags: [lip, governance, canvas, canvas_standard, panel_link, surface, conformance, standard, b4]
banner: "who/assets/banners/banner_governance.jpg"
icon: layers
---

# LIP-0008: Derived Surfaces as Pure Metadata (Canvas panel_link A-5 relaxation)

> **Migrated live into the Canvas.aDNA governance home** at Operation Beacon Phase B4 (2026-07-02) from the archived
> lattice-labs registry (reader-only). The ≥7-day review window opened 2026-06-20 and lapsed (earliest close
> 2026-06-27) with no objection; the FA (operator) ratified the direction, so status advanced **Review → Accepted**.
> The A-5 relaxation then **landed in Canvas Standard v2.3.0** (Operation Beacon B4.2, 2026-07-02 — the gated
> `canvas_std` touch + version cut; suite 115/10, certification 11/11), so status is now **Final**
> (Review → Accepted → Implemented → Final).

## Abstract

This proposal relaxes conformance check **A-5** of the **aDNA Canvas Standard** so that a `role: derived` entry in
`_reserved.panel_link.surfaces` **MAY** omit its `id` (and its backing node), carrying pure metadata, while the single
**canonical** surface keeps its node-resolution guarantee. It removes a synthetic-node wart: today a *derived* output
surface (e.g. `html`, `funder_portal`) has no content region, so producers must mint a zero-content `region`-class
marker node purely to pass A-5. The change is **MINOR** and **backward-compatible (relaxing)** — every currently-valid
canvas stays valid — and targets the **aDNA Canvas Standard v2.3.0** (see §6 reconciliation note). The Standard is owned
by **Canvas.aDNA** (persona Mondrian); this gap was surfaced building the in-vault `document_generator` consumer at
Operation Keystone E4.2 (the first use of `region`-class derived-surface markers). The decision vehicle is staged at
`Canvas.aDNA/what/decisions/lip_draft_derived_surface_metadata.md`.

## Motivation

The `spec_panel_link_semantics` model lets a `panel_link` declare multiple output *surfaces*, exactly one of which is
**canonical** — the round-trip authority (§5.2). Other surfaces are **derived**: regenerated outputs (HTML, a funder
portal, a print target), never hand-authored, never the source of truth. A derived surface therefore has nothing to
point at on the canvas. Yet conformance **A-5** asserts blanketly that *every* `surfaces[].id` must resolve to a real
node, so the producer is forced to fabricate an empty `region`-class marker node (`surface_<name>`, `role:
derived_surface`) solely to satisfy the check.

That is a small but real defect against the Strategic Heart principle of **substrate parsimony** ("specify contracts,
not engines" — the Standard should not compel producers to emit meaningless nodes). Synthetic zero-content nodes
inflate the baseline graph and exist only to pass validation. The honest model is: the canonical surface resolves; a
derived surface is metadata describing a regenerated output, not a node on the canvas.

## Specification

### §1 — Current behavior (A-5)

`spec_conformance_suite` **A-5** requires every `_reserved.panel_link.surfaces[].id` to resolve to a node in the
canvas. The reference implementation enforces this across **all** surface entries in
`canvas_std/reserved.py::validate_panel_link` (the surfaces loop).

### §2 — Proposed relaxation

A surface entry is `{surface, role, id?}`. The rule becomes:

- The **canonical** surface is unchanged: there MUST be exactly one, and its `id` MUST resolve.
- A `role: derived` surface's `id` is **OPTIONAL**. When omitted, **no backing node is required** — the entry is pure
  metadata (`{surface, role: derived, …}`).
- A `role: derived` surface that *does* carry an `id` still MUST resolve (so existing canvases remain valid).

### §3 — Conformance change (A-5 restatement)

A-5 changes from "every surface `id` resolves" to: **"the canonical surface resolves; a `role: derived` surface MAY
omit `id`, and if present `id` MUST resolve."**

### §4 — Spec-text change

`spec_panel_link_semantics §5.2` is amended to state that derived surfaces are pure metadata and require no backing
node; the canonical surface remains the single resolved round-trip authority.

### §5 — Reference-impl landing sites (on Final)

- `canvas_std/reserved.py::validate_panel_link` surfaces loop — relax per §2 (locate the current A-5 surface check).
- Producers (e.g. `document_generator/consume.py`) **may** then stop minting the synthetic `region`-class marker.

### §6 — Versioning

**MINOR** → aDNA Canvas Standard **v2.3.0** (additive / relaxing / conformance-optional).

> **Reconciliation note (2026-07-02, migration).** This LIP originally targeted **v2.1.0**. Between filing (2026-06-20)
> and ratification, the Standard shipped **v2.2.0** at Operation Armature (the interaction runtime), so the v2.1.0 slot
> was never cut. The relaxation therefore lands as **v2.3.0** atop the 2.2.0 line; the reserved 2.1.0 slot is recorded
> as **superseded**. See `what/decisions/lip_queue_disposition.md` and `canvas_std/CHANGELOG.md`.

## Rationale

Two options were carried in full in the decision vehicle:

- **(i) Keep/bless the backing node.** Treat the `region`-class `role: derived_surface` marker as the canonical
  representation, optionally tightening the check to *require* it. Non-breaking, uniform on-canvas anchors — but keeps
  the synthetic-node wart and forces producers to keep minting markers.
- **(ii) Relax A-5 — derived surfaces as pure metadata (chosen).** Matches §5.2 ("derived = regenerated, never
  hand-authored"), drops the synthetic node, and preserves the only resolution guarantee that matters for round-trip
  (the canonical surface). Cost: surfaces become non-uniform (some node-backed, some not), so a tool that assumes
  `surfaces[].id` always resolves must special-case `role: derived` — acceptable, because the canonical-surface
  guarantee is explicit and unchanged.

The operator (FA) **direction-approved option (ii) on 2026-06-20**. Because (ii) changes what A-5 asserts and what
downstream tooling may assume, it is a genuine conformance call and rides this formal LIP rather than a patch.

## Backwards Compatibility

Relaxing and additive. Every currently-valid canvas (which provides ids for all surfaces) stays valid; only the
requirement loosens, so producers MAY stop minting markers going forward. No existing canvas is invalidated. The change
is `panel_link`-scoped (C4-safe).

## Reference Implementation

- Surfaced by: `Canvas.aDNA/what/production/document_generator/src/document_generator/consume.py` (the synthetic
  `region`-class marker, minted to satisfy A-5).
- Conformance check: `Canvas.aDNA/what/code/canvas_std/src/canvas_std/reserved.py::validate_panel_link`.
- Decision vehicle: `Canvas.aDNA/what/decisions/lip_draft_derived_surface_metadata.md` +
  `Canvas.aDNA/what/decisions/lip_queue_disposition.md` (row B4).

The §2/§5 changes land when this LIP reaches **Final** (Beacon B4.2).

## Security Considerations

None material. This is a conformance-optional relaxation of a structural validation check. A pure-metadata derived
surface carries no executable content and introduces no external reference beyond what the canonical surface already
declares; it cannot widen any trust, auth, or secret-handling surface.

## Decision Log

| Date | Decision | Authority |
|------|----------|-----------|
| 2026-06-20 | Direction approved — option (ii), derived surfaces as pure metadata (MINOR A-5 relaxation). Filed as LIP-0008 (Draft) pending the ≥7-day review. | Operator (FA), at the Canvas post-Keystone LIP-queue closeout |
| 2026-06-20 | **Review opened** (status Draft→Review) — formal LIP-0001 review period (minimum 7 days); earliest close **2026-06-27**. | Steward: Protocol / FA (operator, Phase 0) |
| 2026-07-02 | **Migrated live** into the Canvas.aDNA governance home (`who/governance/lips/`) from the archived lattice-labs registry (Operation Beacon B4.1). Archive original left reader-only. | Mondrian (Canvas.aDNA) |
| 2026-07-02 | **Review window lapsed** (closed 2026-06-27, no objection); FA ratifies direction → status **Review → Accepted**. Reconciled landing version **v2.1.0 → v2.3.0** (2.1.0 superseded by the Armature 2.2.0 jump). Implementation + **Final** to land in B4.2. | Operator (FA), Phase 0 |
| 2026-07-02 | **Implemented → Final.** The A-5 relaxation landed in the `canvas_std` validator (`reserved.py::validate_panel_link` surfaces loop) + fixture/regression tests (suite **115/10**, certification **11/11**) and the Standard was cut to **v2.3.0** (Operation Beacon B4.2). Status **Accepted → Implemented → Final**. | Operator (FA), Phase 0 |

## Copyright

This LIP is placed in the public domain via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
