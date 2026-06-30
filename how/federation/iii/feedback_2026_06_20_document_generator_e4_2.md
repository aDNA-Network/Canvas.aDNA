---
type: feedback
created: 2026-06-20
updated: 2026-06-20
last_edited_by: agent_stanley
review_of: [what/production/document_generator/examples/canvas_standard_whitepaper.canvas, what/production/document_generator/examples/grant_proposal.canvas]
reviewer: "Canvas.aDNA iii/ wrapper (III.aDNA v0.5.0) — 5-lens persona panel"
scope: structural
verdict: "0 High / 0 Med — SHIP; CANVAS-L-002 resolved-by-reflow (residual tracked); 1 Low; 1 new spec-gap erratum candidate"
mission: mission_e4_2_lf_contracts
tags: [iii, review, feedback, canvas, keystone, e4_2, document-generator, contracts, reflow, structural]
---

# Wired Canvas Review — document_generator E4.2 (LF visual/format contracts + reflow)

The third **real** III review through the active Canvas `iii/` wrapper (III v0.5.0), over the E4.2 build: the genre
**format/visual contracts** (F1–F7 / V1–V8 / X1–X14) now ride the `.canvas` as declarative `_reserved` metadata, the
**`region` component class** is exercised for the first time, and **reflow/auto-pagination** closes the bulk of
`CANVAS-L-002`. Same discipline as the E4.1 review ([[feedback_2026_06_19_document_generator]]).

**Scope = STRUCTURAL.** No render loop exists yet (`canvas_presentation` lands at **PT P5**); pixel-level VR1 checks
(font/contrast, page-break/orphan-widow *pixels*, the 24-criterion scoring) stay **PT-P5-gated and out of scope** —
*deferred*, not *passed* (§Deferred). The review covers the object-level lenses over the two `.canvas` artifacts.

## DISPATCH

- **Engine:** III `skill_iii_review` (federation) via `iii/CLAUDE.md` `federation_ref` → III.aDNA v0.5.0 (`0f06aa6`, oracle lattice 1.2.6).
- **Packs:** inspect/introspect/learning-store + `context_iii_canvas_visual` (CV-* traps) + the **Canvas-owned VR1–VR5 contract** (standard-bearer inversion).
- **Panel:** 5 lenses (`iii/what/context/canvas_reviewers.yaml`) — domain architect · quant/rigor · skeptical executive · information designer · accuracy auditor (≥1 rigor + 1 accuracy lens, always).
- **Targets:** `canvas_standard_whitepaper.canvas` (genre whitepaper; reflowed 2→**5** pages / 32 nodes / 23 edges) + `grant_proposal.canvas` (genre grant; **1 model page → 4 canvas pages** / 27 nodes / 19 edges).

## INSPECT — findings

**Structural metadata present (precondition — PASS):** both artifacts validate `adna_native` (`[OK]`) and degrade
D-1/D-2/D-3. The new contract surface is well-formed: `semantic_bindings.{genre,format,visual}` carry the declared
F/V/X fields; figure nodes carry the per-asset visual `qualities` (V2–V8 — TikZ/CanvasForge/scorecard, and the
captured-override on Figure 2); exactly one `canonical` surface (`doc_root`) with **derived surfaces backed by real
`region`-class nodes** (A-5 holds); the **`region` class is exercised** (derived-surface markers + `rgn_subclass`),
each `degrades_to: group`. Reflow is sound: every emitted page's measured content ≤ `CONTENT_H` (912) — no silent
overflow — and a non-overflowing, no-genre document is **byte-identical to E4.1** (regression-locked by the golden).

| ID | Lens / trap | Location | Severity | Finding |
|----|-------------|----------|----------|---------|
| F-E42-001 | information designer | reflow planner (`layout.paginate`) | **Low** | Reflow is **section-atomic**: a single section taller than a whole page (rare in practice) still overflows its own page — flagged `qualities.layout_note: "oversized_overflow"` (traced, not silent). Intra-section pagination (split a section mid-block, widow/orphan) is deliberately **not** attempted here — it is a PT-P5 render concern. This is the **narrow residual** of `CANVAS-L-002`, not a reopen. |
| F-E42-002 | accuracy auditor + info designer | citation `link` nodes (both examples) | **Low** | `CANVAS-L-001` (citation label → bare URL) **recurs** — E4.2 records visual/format intent but does not add a Standard-side link-label carry, so authored `sources[].label`s still render label-less. Unchanged disposition (errata; producer- or Standard-side fix). Frequency holds at 2 (same producer family; not a new independent surface). |

**Not firing (checked, clean):** CV-CONFIDENCE-01 (every emitted F/V/X field traces to a real `spec_format_contract`
F# / `spec_visual_contract` V#/X# slot — no invented contract fields) · CV-COHERENCE-01 (containment holds; region
markers sit in a metadata gutter, never overlapping the page column) · CV-HIERARCHY-01 · CV-TEMPLATE-01 · the
substrate-neutrality invariant (AST-guarded: `model.py` imports no `canvas_std`).

## CANVAS-L-002 — disposition (the headline)

**Resolved-by-reflow at section granularity.** E4.2 adds a deterministic measure→page-break planner: the whitepaper
that overflowed its page box by 662px (E4.1) now paginates cleanly across 5 pages; the grant's single content-heavy
model page distributes across 4 pages, each ≤ `CONTENT_H`. The content-heavy-page-overflow that `CANVAS-L-002`
recorded **no longer occurs** for the common case. **Residual (F-E42-001):** a single section taller than a whole page
overflows its own page with an explicit diagnostic; closing that needs intra-section pagination (PT-P5 render loop).
→ `CANVAS-L-002` **accepted / addressed (producer)**; the narrow residual stays tracked under PT P5 (with VR1 pixels).

## Spec-gap erratum candidates (LIP queue — recorded, not fixed; `adr_003` §2)

E4.2 surfaced **one new** candidate and sharpened a prior one:

1. **(NEW) Derived surfaces require a synthetic backing node.** `panel_link.surfaces` models a surface as `{id, role}`
   where the `id` MUST resolve to a node (A-5). A *derived* output surface (html, funder_portal) is not itself a
   content region, so the producer must mint a zero-content `region`-class marker node purely to satisfy A-5. Question
   for the Standard: allow a surface-as-pure-metadata declaration (no backing node), or bless the marker-node pattern
   as the convention? → **v2.0.x erratum candidate (surface model).**
2. **(SHARPENED) `sequence`-unit / pagination-construct ambiguity (was E4.1 erratum #3).** E4.2 now **exercises the
   `region` class** — but for *surface/subclass markers*, while pagination still rides **page-group `panel` nodes** + a
   page-level `sequence` chain (the `region`-for-pagination intent of `spec_panel_link_semantics §5.1` stays
   unexercised). So "which construct owns pagination — `region` or page-`panel`?" is now a concrete, answerable
   question. → carries forward in the LIP queue.

The two other E4.1 candidates (orphan-anchor/`naming_convention` validator absent — headline; no `quote`/`footnote`
class) are **unchanged** in the queue.

## INTROSPECT — calibration

- **Honest gradient:** 0 High / 0 Med is credible — the build is green (37/37) and carefully scoped; the review finds a
  *real* residual (F-E42-001) and a *real* new spec gap, not theatre, and explicitly does **not** mark the PT-P5 pixel
  half as passing.
- **No cross-voice escalation:** no location drew 2+ lenses at Med+ → nothing escalates.
- **Regression honesty:** the byte-identity golden + the firewall git-diff (zero) + the three sibling suites (46/8 ·
  10 · 16) are the evidence that "additive, non-regressing" is true, not asserted.

## IMPROVE — dispositions (human gate)

All findings **Low**; none blocks ship. Package + 37 tests left green and untouched (this is a gate-wiring review, not
a churn pass).

| ID | Disposition |
|----|-------------|
| F-E42-001 | Accepted, tracked — narrow `CANVAS-L-002` residual; intra-section pagination → PT P5. |
| F-E42-002 | Errata — accepted, deferred (= `CANVAS-L-001`, unchanged). |
| Erratum (new) derived-surface backing node | v2.0.x erratum candidate — logged to the LIP queue, not fixed. |
| Erratum (sharpened) pagination construct | Carried in the LIP queue (sequence-unit, now concrete). |

## ACCUMULATE

- **`CANVAS-L-002`** → marked **addressed (resolved-by-reflow, section-level)**; residual `intra_section_pagination`
  noted (PT-P5). Frequency held at 1 (not a recurrence — a resolution).
- **`CANVAS-L-001`** unchanged (frequency 2; not graduated — needs ≥3 + acceptance ≥0.80 + Stanley/Argus gate).
- Canonical III store untouched (read-only from the consumer side; md5 `5adb0dfa38d9224649c3b2cba83852ae` invariant).

## Verdict

**0 High / 0 Med across all structural lenses → SHIP.** E4.2 lands the LF visual/format contracts as declarative
metadata, exercises the `region` class for the first time, and closes the bulk of `CANVAS-L-002` via deterministic
section-level reflow — additive and non-regressing (byte-identity golden; `canvas_std` untouched; siblings green). The
pixel/render half (VR1, intra-section widow/orphan, figure resolution) is correctly deferred to PT P5.

## Deferred to PT P5 (canvas_presentation render loop)

VR1 text-readability (font/contrast pixels) · intra-section pagination (widow/orphan, mid-section page breaks — the
F-E42-001 residual) · the 24-criterion scoring + hard gates · CV-CONTRAST-01 · CV-PENDING-01 (figure resolution) ·
CV-DIMENSION-VISIBILITY-01 pixel viewport.

## Related
- Method: `what/production/document_generator/iii_quality_contract.md` · Panel: `iii/what/context/canvas_reviewers.yaml` ·
  Store: `iii/what/context/canvas_iii_learning_store.jsonl` · Wrapper: `iii/CLAUDE.md` (v0.5.0).
- Prior: [[feedback_2026_06_19_document_generator]] (E4.1) · [[feedback_2026_06_19_canvas_consumers]] (E5.1).
