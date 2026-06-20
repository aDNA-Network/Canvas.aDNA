---
type: federation_wrapper
wrapper_for: III.aDNA
created: 2026-06-12
updated: 2026-06-19
last_edited_by: agent_stanley
mission_origin: Canvas.aDNA Operation Cartography — P3 (mission_p3_conformance_federation)
activated_by: Canvas.aDNA Operation Keystone — E5.1 (mission_e5_1_iii_wiring)
status: active
substrate_pin: "III.aDNA v0.5.0"
pinned_at: 2026-06-19
tags: [federation, iii, consumer_wrapper, canvas, active, v0_5_pinned, genesis]
---

# Canvas.aDNA `iii/` — III.aDNA Consumer Wrapper

Federation wrapper for **III.aDNA** (Argus Panoptes) — the Inspect/Introspect/Improve quality framework.
Canvas.aDNA federates against III to review canvas **output quality**, distinct from the **format conformance**
the Standard checks itself ([[spec_conformance_suite]]). The III loop: `DISPATCH → INSPECT {Text/Code/Visual/Data}
→ INTROSPECT → IMPROVE → (human gate) → ACCUMULATE`.

> **ACTIVE — wired at Keystone E5.1 (2026-06-19).** `status: active`; pin **confirmed v0.5.0** against
> `III.aDNA/MANIFEST.md` (Campaign-G G4 production pin `v0.4.1→v0.5.0`; siblings VideoForge/CanvasForge/wga already
> @ v0.5.0). The stale workspace-router note (production pin "v0.4.0") is superseded by III's live state. First real
> review: [[feedback_2026_06_19_canvas_consumers]] (brief_consumer + deck_generator; **structural** — pixel/VR1 PT-P5-gated).

Per **ADR-002** (consumer federation contract) and **ADR-003** (learning-store ownership) at III.aDNA, this
wrapper is lightweight: a `federation_ref` + `local_extensions:`. III canonical content (the review skill,
modules, packs, oracle lattice, canonical corrections store) is **never copied here — only referenced**.

## ⭐ Standard-bearer inversion (the load-bearing point)

Canvas.aDNA **owns the Canvas Standard**; CanvasForge is a producer. So — unlike a normal consumer — Canvas.aDNA
**owns the canvas review _contract_**: the **VR1–VR5 rubric** and the **canvas-visual trap schema** are normative
artifacts of *this* vault, while the III **engines** that run them (`module_iii_inspect_visual`, the oracle
lattice, `skill_iii_review`) stay in III.aDNA. This is the "**specify contracts, not engines**" discipline (C8) in
its cleanest form: producers (CanvasForge, LF-successor) inherit the *contract* from here and the *engine* from
III. The canvas review contract:

| Rule | Weight | Checks (courier-check, not a polish pass) |
|------|-------:|-------------------------------------------|
| **VR1** Text readability | 25% | font size, contrast, line length |
| **VR2** Visual hierarchy | 25% | heading prominence, information flow |
| **VR3** Whitespace quality | 20% | breathing room, spacing rhythm |
| **VR4** Color harmony | 15% | cohesive palette, accent balance |
| **VR5** Professional polish | 15% | alignment, sizing, enterprise-ready |

Canvas-visual **trap schema** (trap ids like `CV-CONTAIN-01`, `CV-HIERARCHY-01`, `CV-TEMPLATE-01`): the *schema*
(trap record shape + the canonical baseline set) is Standard-owned here; modality engines + producer-specific
traps stay in III / the producer. Ownership note: per III ADR-002 §6 the canvas-visual pack is modality-specific
and III core stays modality-agnostic — which is exactly why the contract belongs in the standard-bearer.

## federation_ref

```yaml
federation_ref:
  source_vault: III.aDNA
  source_path: ~/aDNA/III.aDNA
  source_skill: how/skills/skill_iii_review.md
  version: "0.5.0"                 # confirmed vs III.aDNA/MANIFEST.md (Campaign-G G4, 2026-06-19); minor bump 0.4.0→0.5.0 reviewed per ADR-002 §3
  pinned_at_commit: "0f06aa6"      # III v0.5.0 declaration commit (Campaign-G G4; annotated tag deferred to III G6)
  pinned_at: 2026-06-19            # Keystone E5.1 activation
  lattice_version: "1.2.6"         # oracle lattice (Campaign-G G2)
  version_policy: minor
  packs_used:
    - context_iii_inspect_procedures      # universal
    - context_iii_introspect_checks       # universal
    - context_iii_learning_store          # universal
    - context_iii_canvas_visual           # the canvas-visual pack (VR1–VR5 + trap baseline) — Canvas owns the contract
  modules_used:
    - module_iii_dispatch
    - module_iii_inspect_visual           # the engine that runs VR1–VR5 (stays upstream)
    - module_iii_introspect
    - module_iii_improve
    - module_iii_accumulate
  lattice: ~/aDNA/III.aDNA/what/lattices/lattice_iii_verification_oracle.lattice.yaml
  local_extensions:
    - kind: learning_store_local
      path: ~/aDNA/Canvas.aDNA/iii/what/context/canvas_iii_learning_store.jsonl
      rationale: >
        Per III ADR-003 §2 — ACCUMULATE writes target this local store; canonical
        upstream corrections are read-only from the consumer side.
    - kind: review_contract_owned_here
      rationale: >
        VR1–VR5 rubric + canvas-visual trap schema are normative Canvas.aDNA artifacts
        (standard-bearer inversion). III engines render the review; the contract is ours.
      pointer: what/specs/spec_conformance_suite.md §6
    - kind: reviewer_registry
      path: ~/aDNA/Canvas.aDNA/iii/what/context/canvas_reviewers.yaml
      rationale: >
        The 5-lens persona-III inspect panel (domain architect · quantitative/rigor · skeptical
        executive · information designer · accuracy auditor) from deck_generator/iii_quality_contract.md.
        Existing ADR-002 §1a kind (SiteForge reviewer-registry precedent) — additive, no amendment.
```

## Routing notes

1. **ACCUMULATE always writes local** (`iii/what/context/canvas_iii_learning_store.jsonl`); graduation to III
   canonical follows III ADR-003 §3 (frequency ≥ 3 across ≥ 2 sessions, acceptance ≥ 0.80, Stanley + Argus gate).
2. Quality review is **stage 4** of the federation 5-stage gates ([[spec_federation_contract]] §4); format
   conformance is stage 3 ([[spec_conformance_suite]]). Do not conflate them.
3. On a III minor bump, review the changelog and update `version`; a major bump triggers re-validation.
4. **Structural-vs-pixel split (until PT P5).** With no render loop yet (`canvas_presentation` lands at PT P5), a
   canvas review covers the **structural** lenses (information design, accuracy/provenance, through-line, substance)
   over the `.canvas` object; **pixel-level VR1 checks** (font size, contrast, 24-criterion scoring) are
   **PT-P5-gated** and must not be scored as passing before then.

## Cross-References
- [[spec_conformance_suite]] §6 (quality vs format) · [[spec_federation_contract]] §4 (5-stage gates) ·
  `III.aDNA/CLAUDE.md` (Argus) · `CanvasForge.aDNA/iii/CLAUDE.md` (sibling precedent; canvas modality) ·
  `WilhelmAI.aDNA/iii/CLAUDE.md` (minimal-form precedent).
- E5.1 wiring: [[what/context/canvas_reviewers|canvas_reviewers.yaml]] (5-lens panel) ·
  [[feedback_2026_06_19_canvas_consumers|first review]] ·
  `what/production/deck_generator/iii_quality_contract.md` (the method this wraps).
