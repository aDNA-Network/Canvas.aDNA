---
type: decision
artifact_type: lip_draft
title: "LIP DRAFT — canvas as a first-class aDNA primitive? (Δ2)"
status: draft
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
phase: P2
target_process: "lattice-labs/how/governance/lips/lip_0001_lip_process.md"
tags: [lip, draft, canvas, primitive, governance, delta2, genesis]
---

# LIP DRAFT — Canvas as a first-class aDNA primitive? (Δ2)

> **DRAFT — NOT SUBMITTED, NOT RATIFIED.** Staged in Canvas.aDNA as the Δ2 proposal vehicle. It is a draft for
> the **lattice-labs LIP process** (`lip_0001_lip_process.md`); it does **not** number itself, and **no change to
> the aDNA core primitive set occurs unless and until a real LIP ratifies it.** Operation Cartography does not
> touch the core primitive set (out of scope).

## Summary

Propose evaluating whether an **aDNA canvas** should be elevated from a *view of the `lattice` primitive* (aDNA
Decision 9) to a **fourth first-class deployable primitive** alongside {module, dataset, lattice}.

## Motivation (Δ2)

Canvas.aDNA's v2.0.0 gives a canvas semantics a bare lattice lacks: a component model (D4), panel/link flow &
pagination (D5), multi-surface output, and context-object metadata (D7). The question (raised as delta Δ2 at the
P0 gate) is whether that richer semantic load justifies primitive status, or whether it rides additively in
`_reserved` over a lattice view (the current model).

## Options

- **(P) Elevate to primitive.** Canvas becomes `{namespace}_canvas` (or a core 4th type). Pros: first-class
  registry/federation identity; clearer than "a lattice rendered visually." Cons: touches the core deployable set
  + SDK + registry; ripples across every vault; high blast radius.
- **(V) Keep as view (status quo, recommended default).** Canvas stays a serialization of `lattice`; all v2.0.0
  semantics live in `_reserved`. Pros: zero core change; the C4 degradation + `_reserved` model already carry the
  semantics; reversible. Cons: "canvas" has no standalone primitive identity in the registry.

## Backward compatibility / blast radius

Option P modifies the **aDNA core standard** (primitive set, SDK type vocabulary, registry) — owned by
`aDNA.aDNA` / `lattice-labs`, not Canvas.aDNA. It therefore **requires a ratified LIP**; Canvas.aDNA cannot make
it unilaterally. Option V is fully backward-compatible (no core change).

## Recommendation

**Default to V (view) for v2.0.0**; carry P as an open LIP for the ecosystem to evaluate after the Standard ships
and real consumer evidence accumulates (does any consumer need canvas as a standalone primitive that a
lattice-view can't serve?). Revisit at P4/P5 or when a consumer use-case forces it.

## Submission note

To advance Option P: submit this draft through `lip_0001_lip_process.md` (proposal → review → ratify), cross-ref
[[spec_context_object]] §3. Until ratified, [[spec_context_object]] treats a canvas as a view and keeps all
extensions in `_reserved`.

## Related
- [[spec_context_object]] (D7) · [[adr_003_standard_governance]] §2 · [[adr_000_canvas_identity]] (Δ2 raised) ·
  `aDNA.aDNA` core primitive set · `lattice-labs/how/governance/lips/lip_0001_lip_process.md`.
