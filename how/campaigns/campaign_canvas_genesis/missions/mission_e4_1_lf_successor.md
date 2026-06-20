---
plan_id: mission_e4_1_lf_successor
type: plan
title: "E4.1 — Stand up the LF-successor (in-vault, pt09-reshaped)"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 4
campaign_mission_number: 1
mission_class: build
created: 2026-06-19
updated: 2026-06-19
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, e4, lf-successor, in-vault, document-generator, building]
---

> **STATUS: ✅ DONE 2026-06-19.** `document_generator` built + green (**18/18**, `ruff` clean) on `canvas_std`;
> structural `iii/` review **0 High / 0 Med**; first use of the `code` component. **No gate advanced** (E5→E6 stays the
> human gate). See Completion Summary / AAR.

# Mission: E4.1 — Stand up the LF-successor (in-vault)

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] · **Phase**: 4

## Goal

Stand up the LiteratureForge-successor **document-production layer in-vault** (per pt09 + the LiteratureForge
wind-down) consuming the Standard's component_model + panel_link + round-trip. Concretely: a third net-new consumer,
**`document_generator`**, that turns a structured long-form document spec into a v2.0.0 aDNA-Native, **multi-page**
`.canvas` — proving the Standard's long-form **document** profile end-to-end on `canvas_std` alone, exactly as
`brief_consumer` (E4.3, single-page) and `deck_generator` (E4.4, deck) did for their profiles.

## D3 governed touch — RESOLVED by [[adr_005_lf_successor_in_vault|ADR-005]] (ratified 2026-06-19)

In-vault at `what/production/`, federating against `canvas_std` only (zero `canvas_core`/PT-P5 coupling); the
genre/writing pipeline (trap-packs, reviewer voices, reward rubrics) **stays producer-side** and is simply *absent*
in E4.1. Substrate-neutrality held by the ADR-004 two-shelf firewall. LF quarry for E4.2:
`Archive.aDNA/LiteratureForge.aDNA/what/specs/` (visual/format contracts + Thoth doctrine + 39 corpus).

## Objectives

- **E4.1-O1 — Package scaffold.** `what/production/document_generator/` cloning the consumer template: `pyproject.toml`
  (hatchling; deps `adna-canvas-std` + `pyyaml>=6`; console script `document-generator`; ruff line-length 100),
  `src/document_generator/`, `tests/`, `examples/`.
- **E4.1-O2 — Substrate-free model** (`model.py`): `Document → Page → Section → Block`/`Source` frozen dataclasses +
  `from_dict` + `load_document`. No `canvas_std` import (substrate neutrality).
- **E4.1-O3 — Deterministic multi-page geometry** (`layout.py`): US-Letter pages stacked vertically (a document reads
  top-to-bottom, unlike the deck row); integer, reproducible coordinates.
- **E4.1-O4 — Block builders** (`blocks.py`): map heading→`typography_run`, body/list→`text`, figure→`image`
  (→`file`/`link`) + caption→`caption`, table→`table`, **code→`code` (first consumer to exercise it)**,
  blockquote→`text`(quote) + attribution, citation→`link`. Emit `reading_order` flow + `adjacency` (body→citations).
- **E4.1-O5 — Assemble + enrich** (`consume.py`): source contract = `doc_root` (single canonical surface) enclosing
  per-page `page{p}` panels enclosing interior content → `to_canvas` → `isStartNode` on page 0 → enrich `_reserved`
  to aDNA-Native: `profile="long_document"`; per-page regions `flow=vertical, pagination=paged, extent{unit:pages,max:1}`;
  `doc_root` region carries the document `extent{unit:words}` (LF `length_window`); `sequence` chain across pages.
- **E4.1-O6 — CLI** (`__main__.py`): `document-generator build <in.yaml|.json> <out.canvas>`.
- **E4.1-O7 — Worked example** (`examples/canvas_standard_whitepaper.yaml`): a self-referential whitepaper ABOUT the
  Standard — ≥3 sections across **2 pages**, **1 vault figure + 1 http figure** (both degrade targets), 1 table,
  1 code block, ≥1 blockquote, several citations.
- **E4.1-O8 — Tests + verify** (`tests/`): conformance · round-trip · degradation · components (target 14–18).
- **E4.1-O9 — Quality** : `iii_quality_contract.md` (clone deck's) + a structural `iii/` review of the example
  (5-lens, structural-only; pixel/VR1 deferred PT-P5) → 0 High / 0 Med; file spec-gap erratum candidates.

## Acceptance criteria (the green bar)

1. `validate(doc, ConformanceLevel.ADNA_NATIVE) == []`; `validate_suite(...,ADNA_NATIVE)` → `ok`, `meets_declared`,
   `level_reached == ADNA_NATIVE`.
2. Exactly one `role="canonical"` surface (`doc_root`); one `panel_link.region` per page; `sequence` chain length
   `== n_pages-1`; `isStartNode` on page 0.
3. Round-trip: `compute_sync_hash(doc)` matches `_reserved.sync`; `diff(to_canvas(from_canvas(doc)),doc)["topology_changed"] is False`; all ids recovered.
4. Degradation: `degradation_report == {D-1,D-2,D-3: True}`; `strip(doc)` Core- **and** Extended-valid; `_reserved`
   removed; `isStartNode` survives strip.
5. Components: every `class ∈ COMPONENT_CLASSES`, every `degrades_to ∈ BASELINE_TYPES`; explicit **`code→text`**,
   figure→`file`+`link`, caption/table assertions.
6. Example builds + conforms; `document-generator build …` CLI cross-checks the Python API.
7. `ruff check .` clean; **no regression** in `canvas_std` (46/8) · `brief_consumer` (10) · `deck_generator` (16).
8. Structural `iii/` review → 0 High / 0 Med (pixel/VR1 deferred PT-P5); erratum candidates logged.

## Notes

- Reuses the E4.3 source-contract + `_reserved`-enrichment pattern and the E4.4 multi-region (panel + region + sequence)
  pattern (page ≙ slide). Genre pipeline stays producer-side.
- **Profile string `long_document`** is distinct from `brief_consumer`'s `document` (single-page) — keeps the two
  consumers' semantics clean; profile strings are producer-set/unvalidated (canvas_std `_validate_semantic_bindings`).

## Completion Summary (2026-06-19)

Built **`document_generator`** at `what/production/document_generator/` — the in-vault, long-form, genre-bound
LF-successor — cloning the `deck_generator` template (panel/region/`sequence`) and the `brief_consumer`
`_reserved`-enrichment pattern. A document spec (`Document → Page → Section → Block`/`Source`) maps to a v2.0.0
aDNA-Native **multi-page** `.canvas`: a `doc_root` canonical surface enclosing per-page `panel{page}` regions
(`pagination: paged`, `extent.unit: pages`) plus a document `words` extent; a `sequence` chain across pages,
`reading_order` within, and `adjacency` from prose to citations; `isStartNode` on page 0. Profile `long_document`
(distinct from the brief's single-page `document`). Files: `pyproject.toml`, `src/document_generator/`
(`__init__/model/layout/blocks/consume/__main__`), `examples/canvas_standard_whitepaper.yaml` (+ generated `.canvas`),
`README.md`, `iii_quality_contract.md`, `tests/` (conftest + conformance/roundtrip/degradation/components).

**Acceptance — all 8 criteria met:** `validate(…, ADNA_NATIVE) == []` + `validate_suite` ok; one canonical surface +
one region per page + `sequence` length `n_pages-1` + `isStartNode`; round-trip sync-hash + topology stable; D-1..D-3 +
strip Core/Extended-valid + isStartNode survives; components valid incl. **`code → text` (first consumer to exercise
`code`)** + figure→file/link; example builds + CLI `canvas-std validate` → `adna_native [OK]`; `ruff` clean; **no
regression** (`canvas_std` 46/8 · `brief_consumer` 10 · `deck_generator` 16); structural `iii/` review **0 High / 0 Med**
(`iii/feedback_2026_06_19_document_generator.md`). Tests: **18/18**.

**Spec-gap erratum candidates surfaced (→ LIP queue, `adr_003`; not fixed):** (1) orphan-anchor + `naming_convention`
validator absent — `spec_panel_link_semantics §5.3/§6` mandates it, `canvas_std/reserved.py::validate_panel_link` lacks
it (headline); (2) no dedicated `quote`/`blockquote` or `footnote` component class; (3) `sequence`-unit ambiguity for
paginated multi-section docs (§5.1 section-panels vs the page-centric chain used here; `region` class left unexercised).

## AAR (5-line)

- **Worked:** the deck template (panel/region/`sequence`) generalized cleanly to multi-page long-form; the `code`
  component class (never exercised) worked first try; the brief + deck patterns composed with no surprises; green on the
  first full test run.
- **Didn't:** nothing blocked. The deterministic single-pass layout can overflow a fixed page box for content-heavy
  pages (no reflow) — a known producer limitation (`CANVAS-L-002`), deliberately deferred.
- **Finding:** building the first **§5 long-form** consumer surfaced 3 Standard/impl gaps (chiefly the missing
  orphan-anchor validator) — the intended "consumer reveals a spec gap → v2.0.x erratum" mechanism working as designed.
- **Change:** introduced `profile: long_document` (vs the brief's `document`) to keep single-page/long-form semantics
  clean; modeled sections as content runs inside page panels (page-centric `sequence`) rather than section-panels.
- **Follow-up:** E4.2 (LF visual/format-contract migration + per-genre config + reflow/auto-pagination); 3 erratum
  candidates → LIP queue; `region` class still unexercised; pixel/VR1 review at PT P5.
