---
plan_id: mission_e4_2_lf_contracts
type: plan
title: "E4.2 — Migrate LF visual/format contracts (in-vault) + reflow"
owner: stanley
status: completed
completed: 2026-06-20
campaign_id: campaign_canvas_genesis
campaign_phase: 4
campaign_mission_number: 2
mission_class: integration
created: 2026-06-19
updated: 2026-06-20
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, e4, lf-successor, contracts, reflow, in-progress, unblocked]
---

> **STATUS: ✅ completed (2026-06-20, operator go — full envelope incl. reflow).** D3 touch ratified
> ([[adr_005_lf_successor_in_vault|ADR-005]] 2026-06-19); unblocked. Built mid-E5; **no gate advanced (E5→E6 still held).**
> Green: `document_generator` **37/37** (18 + 19 new), `ruff` clean; both examples `adna_native [OK]` + D-1/D-2/D-3; no
> regression (`canvas_std` 46/8 · `brief_consumer` 10 · `deck_generator` 16); `canvas_std` untouched (firewall git-diff 0).

# Mission: E4.2 — Migrate LF visual/format contracts (in-vault) + reflow

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] · **Phase**: 4

## Goal

Migrate the LiteratureForge visual/format contracts (`spec_format_contract` F1–F7 + `spec_visual_contract` V1–V8
per-asset / X1–X14 cross-asset, scavenged from `Archive.aDNA/LiteratureForge.aDNA/what/specs/`) into the **in-vault**
LF-successor `document_generator` as **producer-side declarative metadata**, add **per-genre profiles**, take the
**first use of the `region` component class**, and add the **reflow/auto-pagination** engine that closes
`CANVAS-L-002`. The schema-level contracts were already absorbed into `canvas_std` (component_model + panel_link) at
P1/E2; this mission wires the producer side only — `canvas_std` is **untouched** (ADR-004 two-shelf firewall).

## Dependencies

- **Blocked by**: E4.1 stand-up only ([[mission_e4_1_lf_successor]], done). D3 touch resolved
  ([[adr_005_lf_successor_in_vault|ADR-005]], ratified 2026-06-19). Zero PT-P5 dependency.

## Objectives

1. **O1 — Contract model (`model.py`).** Add frozen, substrate-neutral dataclasses for the format contract (F1–F7),
   the per-asset visual contract (V1–V8) and the cross-asset visual contract (X1–X14), plus a `GenreProfile` and a
   `GENRE_PROFILES` registry (whitepaper + grant fully worked from `spec_format_contract §3/§5` + `spec_visual_contract
   §6`; research/blog/exec stubbed). Attach `Document.genre`, `Block.asset`, `Section.section_kind`; extend `from_dict`
   to read optional `genre:`/`format:`/`visual:`/`asset:` keys. **No `canvas_std` import** (guard-tested).
2. **O2 — Reflow (`layout.py`).** Move shared geometry constants here; add `CONTENT_H`, deterministic content-unit
   height fns (shared by measure + emit), `PageFragment`/`SectionFragment`, and `paginate()` — **section-level**
   greedy packing that distributes a model page's sections across as many canvas pages as needed (a section taller
   than a page gets its own page + an `oversized_overflow` diagnostic; intra-section widow/orphan is the documented
   residual). Integer-deterministic; a non-overflowing document is byte-identical to E4.1.
3. **O3 — Emission + edges (`blocks.py`, `consume.py`).** Fragment-aware `build_page`; merge resolved `AssetVisual`
   into figure/caption `qualities` (V1–V8); `_emit_contract_metadata` mapping F/V/X → `_reserved`
   (`semantic_bindings.{genre,format,visual}`, `brand_style_pack_ref`, `panel_link.surfaces` with derived-surface
   backing nodes, `panel_link.regions`); first use of the `region` class (derived-surface markers + `rgn_subclass`);
   `sequence` over the **emitted** page list; conditional emission (no genre ⇒ E4.1-identical output).
4. **O4 — Examples + tests.** Extend the whitepaper example (genre: whitepaper + figure `asset:` overrides) +
   regenerate; add a reflow-forcing `grant_proposal.yaml` + golden. New tests (`test_contracts`, `test_region_class`,
   `test_reflow`, `test_model_neutrality`) + a frozen no-contract golden; coherent updates to the existing suite.

## Acceptance criteria

- [ ] `document_generator` ~36 tests green (18 existing unchanged + ~18 new); `ruff` clean.
- [ ] CLI `document-generator build grant_proposal.yaml` → `canvas-std validate` → `adna_native [OK]` + D-1/D-2/D-3.
- [ ] Reflow proven: the grant example emits >1 canvas page from one model page; every emitted page's measured
      content ≤ `CONTENT_H` (except a flagged oversized block); a non-overflowing doc is byte-stable vs the golden.
- [ ] First use of the `region` class: ≥1 `component_types[*].class == "region"`, all degrade to `group`.
- [ ] **No regression / firewall held:** `canvas_std` 46/8 · `brief_consumer` 10 · `deck_generator` 16 unchanged;
      `what/code/canvas_std/` has **no diff**; `model.py` imports nothing from `canvas_std`.
- [ ] Structural `iii/` review 0 High / 0 Med; `CANVAS-L-002` dispositioned (resolved-by-reflow + residual); any new
      spec gaps filed as v2.0.x erratum candidates (not Standard edits). **No phase gate advanced.**

## Completion Summary / AAR

**Done (2026-06-20):** all four objectives. **O1** — `model.py` gained the frozen, substrate-neutral contract
dataclasses (FormatContract F1–F7, AssetVisual V1–V8, CrossAssetVisual X1–X14, GenreProfile) + a 5-entry
`GENRE_PROFILES` registry (whitepaper + grant fully worked; research/blog/exec stubbed); `Document.genre`/`Block.asset`/
`Section.section_kind` attached; `from_dict` extended. **O2** — `layout.py` gained `CONTENT_H`, shared content-unit
height fns (measure == emit), and `paginate()` (section-level reflow). **O3** — `blocks.py`/`consume.py` emit the F/V/X
contracts declaratively into `_reserved` (semantic_bindings, brand_style_pack_ref, surfaces, regions), merge per-asset
V-qualities onto figures, and take the **first use of the `region` class** (derived-surface markers + `rgn_subclass`).
**O4** — whitepaper example carries `genre: whitepaper` + a figure asset override; new `grant_proposal.yaml` forces
reflow (1 model page → 4 canvas pages); 19 new tests + a frozen no-contract golden.

**AAR (5-line):**
- **Worked:** the conditional-emission design (no genre ⇒ E4.1-identical output) gave a clean byte-stability guard and
  kept all 18 prior tests green; section-level reflow closed the bulk of `CANVAS-L-002` deterministically.
- **Didn't (first cut):** assumed the existing fixtures *didn't* overflow — they massively do (the CANVAS-L-002
  defect), so "byte-identical for non-overflow" had to move to a dedicated small golden + `n_pages`-emitted fixture.
- **Finding:** declarative-only emission means a derived output surface needs a synthetic backing node to satisfy A-5 →
  **new spec-gap erratum candidate** (surface-without-node); the `region` class is now used (for surface markers), which
  sharpens the prior sequence-unit/pagination-construct erratum.
- **Change:** measurement + emission now share one source of truth (the `layout.*_height` fns) so reflow can't drift
  from layout; geometry constants moved blocks.py → layout.py.
- **Follow-up:** the residual `CANVAS-L-002` (a single section taller than a page) + intra-section widow/orphan → PT P5;
  the 4 spec-gap erratum candidates (3 from E4.1 + 1 new) sit in the LIP queue for `adr_003`.

**Verification:** `document_generator` **37/37**, `ruff` clean; CLI `document-generator build grant_proposal.yaml` →
`canvas-std validate` → `adna_native [OK]` + D-1/D-2/D-3; reflow + region-class + byte-identity asserted; no regression
(`canvas_std` 46/8 · `brief_consumer` 10 · `deck_generator` 16); `what/code/canvas_std/` git-diff **0** (firewall held);
`model.py` AST-guarded against any `canvas_std` import. **No phase gate advanced** — E5→E6 stays the human gate.
