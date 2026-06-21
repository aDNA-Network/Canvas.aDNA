---
type: artifact
artifact_class: handoff_register
created: 2026-06-20
updated: 2026-06-20
last_edited_by: agent_stanley
mission: mission_e6_3_campaign_aar
campaign: campaign_canvas_genesis
tags: [artifact, handoff, register, pt-p5, lip-queue, graduation, keystone, e6]
---

# E6.3 — Keystone handoff register + context-graduation report

The single place every open item from Operation Keystone is handed off. Keystone shipped the Standard + reference
impl + floor migration + three in-vault consumers, all green. The remaining work is **follow-on, not core** — it
lands in PT P5 (federation/relocation), the LIP queue (Standard errata), or an optional separate track.

## A. PT P5 handoff (production-relocation + federation rollout — E5.2)

| # | Item | Detail | Source |
|---|------|--------|--------|
| A1 | **`canvas_core` relocation** | move `canvas_core` → `Canvas.aDNA/what/production/canvas_core/` (import unchanged; env `CANVAS_CORE_HOME`); `canvas_std` separately importable | ADR-004 |
| A2 | **~8 consumer-wrapper refederations** (E5.2) | repoint the producer/consumer `canvas/` wrappers (ComfyUI/Astro + SS/CC presentationforge/graphicnovelforge…) at the relocated `canvas_core` + Canvas v2.0.0 | campaign E5.2 |
| A3 | **Federation-integration tests red** | `CanvasForge test_federation_validation.py` = 25f/30e, **all** `FileNotFoundError` on consumer-wrapper lattices under a wrong `Archive.aDNA/` prefix (pt09 relocation broke sibling-vault path resolution). Repointing A2 turns these green. **Not a floor/Standard regression** (floor 835/3 green). | E6.2 (`e6_2_cutover_confirmation.md` §3) |
| A4 | **v2.0.0 registry registration** | deferred E2.3 → "E5 rollout"; coupled to E5.2. Register the Standard + conformance suite once wrappers refederate. | campaign E2.3/Verification Strategy |
| A5 | **Parity re-baseline** | re-capture `deck_norm_sha256` at the relocated resident path; note the deck builder's **absolute image-path embedding** as a portability nit (machine/location-specific). | E6.1 §5 |
| A6 | **FU1 — `canvas/`-routing Standing Order** | route `what/production/` standard-consumption through `canvas/` (mirror `iii/`) at the P5 refederation | ADR-004 checklist |
| A7 | **FU2 — round-trip-function dedup** | validate/diff/merge/round-trip → `canvas_std` once `canvas_core` is co-located; gated by `e3_3_parity_check.py` | ADR-004 checklist |
| A8 | **`CANVAS-L-002` residual** | intra-section pagination (a single section taller than a page; `oversized_overflow`) — widow/orphan/mid-block split | E4.2 |
| A9 | **Shim retirement execution** | `canvas_core→canvas_std` shim retires on/after **2027-06-13** (E-D2); SR-9 retire-condition; ref-sweep is downstream of A2. Ledger: Home.aDNA §C (memo `coord_2026_06_20_mondrian_to_hestia_shim_retirement_schedule`). | E6.2 |

## B. LIP queue — Standard spec-gap errata (`adr_003`, governed process)

| # | Erratum candidate | Severity | Source |
|---|-------------------|----------|--------|
| B1 | **Orphan-anchor + `naming_convention` validator absent** — `spec_panel_link_semantics §5.3/§6` mandates the check; `canvas_std/reserved.py::validate_panel_link` lacks it | Medium | E4.1 |
| B2 | **No dedicated `quote`/`blockquote` or `footnote` component class** — long-form rides on `text` + `semantic_type` | Low | E4.1 |
| B3 | **`sequence`-unit / pagination-construct ambiguity** — which construct owns pagination, `region` or page-`panel`? (sharpened once E4.2 exercised `region`) | Medium | E4.1→E4.2 |
| B4 | **Derived-surface backing node** — a derived `panel_link.surface` has no content region; producer must mint a synthetic `region` marker to satisfy A-5. Allow surface-as-pure-metadata? | Low→Med | E4.2 |

> These are **additive/non-breaking** (new class / new validator / a metadata question) → handle as v2.0.x **minor**
> via the `adr_003` LIP process; they do **not** block a valid v2.0.0.

> **Disposition 2026-06-20 (`mission_lip_queue_errata`, `what/decisions/lip_queue_disposition.md`):**
> **B1 ✅ DONE** — `canvas_std::validate_anchors` implemented + `spec_panel_link_semantics §5.3/§6` sharpened (anchor
> model); suite 70/10, `ruff` clean, no consumer regression. **PATCH.**
> **B3 ✅ DONE** — clarified in-spec (§4/§5.1: a page is a `panel` carrying a `region`; pagination region-declared;
> `sequence` unit = section-panel). **PATCH.**
> **B2 ◻ DRAFTED + GATED** — `lip_draft_text_quote_footnote_class.md` (add classes vs ride-on-text; recommend
> ride-on-text). **B4 ◻ DRAFTED + GATED** — `lip_draft_derived_surface_metadata.md` (backing node vs pure metadata;
> recommend metadata). Both await an operator decision; to **Final** needs the ≥7-day LIP review.
> **Release:** B1+B3 packaged as **v2.0.1**, content done at `STANDARD_VERSION=2.0.0`, **release-cut HELD for operator**.

> **Closeout 2026-06-20 (`session_stanley_20260620_200612_lip_queue_closeout`):** **B2 → (ii) ride-on-text APPLIED**
> (PATCH → v2.0.1; `spec_component_model §4.4` + `canvas_std.reserved.LONGFORM_SEMANTIC_TYPES` + the
> `adna_longform_quote` fixture/test; draft resolved). **B4 → (ii) pure metadata, DIRECTION LOCKED** — a MINOR A-5
> relaxation, so it rides a lattice-labs LIP (≥7-day review) → **v2.1.0** (no code this session). **v2.0.1 CUT**
> (B1 + B3 + B2; `STANDARD_VERSION` 2.0.0 → 2.0.1). Remaining LIP-queue tail = the B4 LIP submission only.

## C. Separate / optional tracks

- **E5.3 — Δ2 canvas-as-primitive LIP** (`lip_draft_canvas_as_primitive`): optional, cross-vault (touches the aDNA
  core primitive set; lattice-labs LIP process). Draft staged; submission operator-discretionary.
- **Low review errata** (E5.1): `CANVAS-L-001` citation-label-dropped (freq 2; not yet graduated to III canonical —
  needs ≥3 / ≥2 sessions / Stanley+Argus gate) + the 3 Low provenance/order findings → a generator pass.

## D. Context-graduation report (`skill_context_graduation`)

**Scan** of Keystone deliverables (missions · artifacts · decisions · specs) against the graduation criteria:

| Source | Candidate topic | Reuse | Existing coverage | Disposition |
|--------|-----------------|-------|-------------------|-------------|
| `spec_federation_contract` · `spec_conformance_suite` · `spec_component_model` · `spec_panel_link_semantics` | the Standard's contracts | high | **full** (already first-class specs in `what/specs/`) | **no-op** — already durable + indexed |
| `adr_000/004/005` | identity · two-shelf firewall · in-vault-LF | high | **full** (ADRs) | **no-op** — durable |
| `e3_3`/`e6_1` parity proofs + the relocation gotcha | **migration parity methodology** (deterministic structural proof; absolute-path/relocation pitfalls; KEEP-floor-vs-federation split) | high (any future producer migration) | **none** | **candidate → recommend a `what/context/` guide** (deferred follow-up; ~1–2K tokens) |
| `iii/CLAUDE.md` routing-note 4 | structural-vs-pixel review split | medium | partial (lives in the wrapper) | keep in wrapper; cross-ref only |

**Finding:** Keystone filed its durable knowledge **as it went** (specs + ADRs + the `iii/` wrapper), so graduation
at close is largely **confirmatory** — most output is already durable and indexed (the "not redundant" criterion
discards it for *new* graduation). The one genuine net-new candidate is the **migration parity methodology** (the
deterministic-structural-proof technique + the relocation pitfalls surfaced at E6.1/E6.2). Recommended as a single
optional context guide; **not produced here** to keep the close proportionate — flagged as a post-campaign
follow-up for operator discretion.

## Summary

Nothing in this register is a Keystone blocker. PT P5 owns relocation + federation (A); the LIP process owns Standard
errata (B); the optional tracks (C) are operator-discretionary; graduation (D) is confirmatory with one optional
guide recommended. Keystone's core deliverable is complete and green.
