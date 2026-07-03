---
type: lip
lip_number: "LIP-0009"
title: "Canvas as a First-Class aDNA Primitive (evaluation)"
author: "Stanley Bishop (Mondrian-drafted; Canvas.aDNA standard-bearer)"
status: final
created: 2026-06-20
updated: 2026-07-02
requires: []
replaces: []
last_edited_by: agent_mondrian
review_opened: 2026-06-20
review_earliest_close: 2026-06-27
resolution: "Option V — canvas stays a view (aDNA Decision 9); elevation to a 4th primitive deferred, no re-open (D2)"
migrated_from: "Archive.aDNA/lattice-labs/how/governance/lips/lip_0009_canvas_as_primitive.md"
migrated_on: 2026-07-02
tags: [lip, governance, canvas, canvas_standard, primitive, aDNA_core, delta2]
banner: "who/assets/banners/banner_governance.jpg"
icon: box
---

# LIP-0009: Canvas as a First-Class aDNA Primitive (evaluation)

> **Migrated live into the Canvas.aDNA governance home** at Operation Beacon Phase B4 (2026-07-02) from the archived
> lattice-labs registry (reader-only), and **declared Final on the recommended Option V** (keep canvas as a view). This
> is an *evaluation* LIP: its "implementation" is the status quo (no core change), so the review — opened 2026-06-20,
> lapsed 2026-06-27 with the recommendation unchanged — completes at **Final**. Elevation (Option P) is **not
> re-opened** (D2); the re-evaluation trigger (§3) is preserved and tracked via
> `Canvas.aDNA/how/backlog/idea_oip_v1x_interface_reanchor`.

## Abstract

This proposal evaluates whether an **aDNA canvas** should be elevated from a *view of the `lattice` primitive*
(aDNA Decision 9) to a **fourth first-class deployable primitive** alongside `{module, dataset, lattice}`. It records
the question raised as delta **Δ2** at the Canvas.aDNA P0 gate (`adr_000_canvas_identity`). The **recommendation is
Option V (keep canvas as a view; status quo)** — all aDNA Canvas Standard v2.0.0 semantics already ride additively in
the namespaced `_reserved` block over a lattice view, with zero change to the aDNA core. This LIP therefore
**formalizes a deliberate deferral**: it changes nothing in the core primitive set now, and keeps Option P (elevate to
primitive) open in governance for evidence-driven re-evaluation. The core primitive set is owned by
**aDNA.aDNA / lattice-labs**, not Canvas.aDNA, which is precisely why the question is filed here.

## Motivation

The aDNA Canvas Standard v2.0.0 gives a canvas semantics a bare `lattice` lacks: a component model (Canvas Decision
D4), panel/link flow and pagination (D5), multi-surface output, and context-object metadata (D7). Δ2, raised at the
Canvas.aDNA P0 gate, asks whether that richer semantic load justifies **primitive status** — a standalone
registry/federation identity — or whether it is correctly expressed as additive metadata in `_reserved` over a lattice
view (the model the Standard ships).

Leaving Δ2 as an informal Canvas-side note is unsatisfying: the question touches the aDNA **core** (the deployable
primitive set, the SDK type vocabulary, the registry), which Canvas.aDNA cannot change unilaterally. Recording it as a
LIP puts the consideration — and its current recommendation — where the core's governance lives, and advances the
Strategic Heart principle of **legibility** (the standing decision and its re-open trigger are explicit, not implicit).

## Specification

### §1 — Options

- **(P) Elevate to primitive.** Canvas becomes a core 4th deployable type (`{namespace}_canvas` or equivalent). Pros:
  first-class registry/federation identity; clearer than "a lattice rendered visually." Cons: modifies the core
  deployable set + SDK type vocabulary + registry; ripples across every vault; high blast radius.
- **(V) Keep as view (status quo — recommended).** Canvas stays a serialization of `lattice`; all v2.0.0 semantics
  live in `_reserved`. Pros: zero core change; the C4 degradation + `_reserved` model already carry the semantics;
  fully reversible. Cons: "canvas" has no standalone primitive identity in the registry.

### §2 — Current decision

**Default to V.** No consumer has yet required a standalone canvas primitive that a lattice-view cannot serve; the
existing `_reserved` + C4-degradation model carries every shipped canvas semantic with no core blast radius.

### §3 — Re-evaluation trigger

Re-open **P** when a concrete consumer use-case forces it — i.e. a consumer needs canvas as a standalone primitive
identity that a lattice-view demonstrably cannot serve. The reopening LIP carries that evidence. (Tracked via
`Canvas.aDNA/how/backlog/idea_oip_v1x_interface_reanchor`.)

### §4 — Ownership boundary

Option P modifies the **aDNA core standard** (primitive set, SDK type vocabulary, registry), owned by
`aDNA.aDNA` / `lattice-labs` — **not** Canvas.aDNA. It therefore requires a ratified LIP; Canvas.aDNA cannot enact it
unilaterally. Option V requires no core change.

## Rationale

V is recommended because the `_reserved` + C4-degradation model already carries canvas semantics with zero core blast
radius and full reversibility, while P's first-class registry/federation identity is **not yet justified by any
consumer use-case**. Filing this LIP (rather than leaving Δ2 informal) records the deferral in the core's governance
and keeps P available for an evidence-driven reopening — the disciplined way to hold an open architectural question
without prematurely paying its cost.

## Backwards Compatibility

- **V (recommended):** no change — canvas remains a `lattice` view and all extensions stay in `_reserved`; fully
  backward-compatible.
- **P (if later ratified):** a core change to the primitive set / SDK / registry, with cross-vault ripple. It is
  deferred precisely to avoid that blast radius until a use-case justifies it.

## Reference Implementation

None proposed (V = status quo). The decision vehicle is staged at
`Canvas.aDNA/what/decisions/lip_draft_canvas_as_primitive.md`; cross-reference `spec_context_object §3`, which treats a
canvas as a view and keeps all v2.0.0 extensions in `_reserved` until and unless a LIP ratifies P.

## Security Considerations

None for V (no change). P's implications — a standalone registry/federation identity for canvas objects — would be
assessed in the reopening LIP if and when consumer evidence reopens it.

## Decision Log

| Date | Decision | Authority |
|------|----------|-----------|
| 2026-06-12 | Δ2 raised at the Canvas.aDNA P0 gate (`adr_000_canvas_identity`); staged as a Canvas-side LIP vehicle. | Canvas.aDNA (Mondrian) |
| 2026-06-20 | Filed as LIP-0009 (Draft) at the Canvas post-Keystone tail; current recommendation **Option V** (defer P pending consumer evidence). | Operator (FA) |
| 2026-06-20 | **Review opened** (status Draft→Review) — formal LIP-0001 review period (minimum 7 days); earliest close **2026-06-27**. | Steward: Protocol / FA (operator, Phase 0) |
| 2026-07-02 | **Migrated live** into the Canvas.aDNA governance home (Operation Beacon B4.1); archive original left reader-only. Review window lapsed 2026-06-27 with the recommendation unchanged → **declared Final on Option V** (keep as view; elevation deferred, **no re-open** — D2). Re-eval trigger (§3) preserved. | Operator (FA), Phase 0 |

## Copyright

This LIP is placed in the public domain via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
