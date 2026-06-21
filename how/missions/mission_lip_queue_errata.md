---
plan_id: mission_lip_queue_errata
type: plan
title: "LIP queue — 4 spec-gap errata (B1 implement · B3 clarify · B2/B4 draft)"
owner: stanley
status: completed
mission_class: implementation
created: 2026-06-20
updated: 2026-06-20
last_edited_by: agent_stanley
tags: [plan, mission, standard, lip, errata, post-keystone]
---

# LIP Queue — 4 Spec-Gap Errata

## Goal

Work the LIP queue handed off at Operation Keystone close (`campaign_canvas_genesis/missions/artifacts/e6_3_handoff_register.md` §B). The 4 errata are not uniform, so each gets the right treatment: **implement** B1 (the §6-mandated orphan-anchor + `naming_convention` validator that `canvas_std` lacks), **clarify** B3 (pagination-construct ambiguity) in-spec, and **draft + gate** B2 (quote/footnote class) and B4 (derived-surface-as-metadata) as operator-decision LIPs. Package B1+B3 as a proposed **v2.0.1** errata release (ADR-003 §1: both PATCH-class); commit locally and HOLD the push.

This is a **standalone mission** (Operation Keystone is closed). Taking the B2/B4 LIPs to **Final** requires the LIP review period (≥7 days, calendar-gated per `lip_0001_lip_process`) — **out of this mission's scope**; this mission produces the Draft artifacts + the decision gate.

## Tasks

### 1. Queue disposition note
- **Status**: planned
- **Description**: `what/decisions/lip_queue_disposition.md` — classify B1–B4 (severity, C4 non-breaking, version impact, recommended path, B2/B4 options). Single source the STATE/handoff updates point to.
- **Files**: `what/decisions/lip_queue_disposition.md`
- **Depends on**: none

### 2. B1 — orphan-anchor + naming_convention validator
- **Status**: planned
- **Description**: Pin the anchor model from the E4.2 consumer emission; sharpen `spec_panel_link_semantics` §5.3/§6 to define it normatively (Standard owns the *declaration* layer; the orphan-*traversal* engine stays producer-side, C8); implement `validate_anchors` in `canvas_std/reserved.py` (regression-safe — flags only declared refs + well-formedness); add a valid anchored fixture + an orphan-violation fixture + manifest entries; suite green + no consumer regression.
- **Files**: `spec_panel_link_semantics.md`, `canvas_std/src/canvas_std/reserved.py`, `canvas_std/tests/fixtures/*`, `canvas_std/tests/fixtures/manifest.json`
- **Depends on**: 1

### 3. B3 — pagination-construct clarification (errata)
- **Status**: planned
- **Description**: Add normative clarifying text to `spec_panel_link_semantics` §4/§5.1: a page/slide is a `panel` carrying `region` pagination props; pagination is declared on the region; inter-page order is a `sequence` chain over section-panels. Cross-check `document_generator/consume.py`.
- **Files**: `spec_panel_link_semantics.md`
- **Depends on**: none

### 4. B2 + B4 — gated LIP drafts (NOT applied)
- **Status**: planned
- **Description**: `lip_draft_text_quote_footnote_class.md` (B2: add classes vs formalize ride-on-text — recommend ride-on-text) + `lip_draft_derived_surface_metadata.md` (B4: require backing node vs relax A-5 — present both, operator decides). Canonical LIP template; status Draft.
- **Files**: `what/decisions/lip_draft_text_quote_footnote_class.md`, `what/decisions/lip_draft_derived_surface_metadata.md`
- **Depends on**: 1

### 5. Release prep + record (then HOLD)
- **Status**: planned
- **Description**: `canvas_std/CHANGELOG.md`; bump v2.0.1 (7 spec frontmatters + `__init__.py` STANDARD_VERSION + federation example); update STATE.md + handoff register §B; commit locally; HOLD push.
- **Files**: `canvas_std/CHANGELOG.md`, `canvas_std/src/canvas_std/__init__.py`, `what/specs/spec_*.md`, `STATE.md`, handoff register
- **Depends on**: 2, 3, 4

## Notes

- **Two-shelf firewall:** this mission deliberately, and for the first time since E3, touches `canvas_std` + the Standard specs. The break is **governed** (errata via ADR-003 §2 maintainer discretion) and **documented** here + in the disposition note.
- **Regression gate (hard):** the new validator ships inside `canvas_std`, which the 3 in-vault consumers import. `document_generator` (37) · `deck_generator` (16) · `brief_consumer` (10) suites + the 4 example `.canvas` outputs MUST stay green. Anchor model designed so existing canvases (which declare conventions but no explicit anchor-refs) pass vacuously.
- **Gated to operator:** B2/B4 design calls · the v2.0.1 version bump · the push · the LIP review period.

## Completion Summary

Delivered the executable LIP-queue scope; operator-gated items handed to STATE.

### Deliverables
- **B1 implemented** — `canvas_std/reserved.py::validate_anchors` (orphan-anchor + `naming_convention` +
  `orphan_detector` well-formedness + reference resolution), wired into `validate_reserved`. Spec sharpened:
  `spec_panel_link_semantics §5.3/§6`. Fixtures `adna_anchored.canvas` (valid) + `adna_orphan_anchor.canvas`
  (negative) + `test_anchors.py` (12). **Suite 70 passed / 10 skipped, `ruff` clean.**
- **B3 clarified** — `spec_panel_link_semantics §4/§5.1` (page = `panel` carrying `region`; pagination
  region-declared; `sequence` unit = section-panel).
- **B2 + B4 drafted + gated** — `lip_draft_text_quote_footnote_class.md`, `lip_draft_derived_surface_metadata.md`.
- **Governance** — `lip_queue_disposition.md`; handoff register §B annotated; CHANGELOG + STATE updated.
- **Regression proof** — `document_generator` 37 / `deck_generator` 16 / `brief_consumer` 10 green; 4 example canvases [OK].

### Descoped (operator-gated, by design)
- B2/B4 design decisions; the v2.0.1 release-cut; the ≥7-day LIP review to Final; the push. All tracked in `STATE.md`.

### Key Findings
- The §6 "no orphaned anchors" gap was partly a spec under-specification (the anchor model was undefined). Fixing
  it = sharpen the spec to define the declarative anchor layer + implement to match — the Standard owns the
  *declaration*, the orphan-*traversal* engine stays producer-side (C8). This made the validator regression-safe by
  construction (existing canvases declare conventions but no explicit refs → vacuously clean).

## AAR

- **Worked**: pinning the anchor model from the live consumer emission (`model.py`/`consume.py`) before coding —
  the validator was regression-safe on the first run (all 4 example canvases + 3 consumer suites green).
- **Didn't**: the v2.0.1 version bump turned out to have an 11-file / 13-site blast radius (incl. 4 test assertions
  + schema identity), too governed to apply unilaterally — held it as a release-cut gate instead.
- **Finding**: 2 of the 4 "errata" (B2/B4) are genuine design forks, not mechanical fixes — right to gate, not assume.
- **Change**: for Standard-version releases, treat the version-marker bump as a discrete operator release-cut step,
  separate from the substantive errata work (captured the one-shot edit-list so the cut is trivial).
- **Follow-up**: operator gates in `STATE.md` §Next Steps — B2/B4 decisions, cut v2.0.1?, push.
