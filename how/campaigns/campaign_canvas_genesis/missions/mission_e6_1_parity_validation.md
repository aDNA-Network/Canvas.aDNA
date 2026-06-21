---
plan_id: mission_e6_1_parity_validation
type: plan
title: "E6.1 — Cross-system parity validation (all consumers green)"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 6
campaign_mission_number: 1
mission_class: validation
created: 2026-06-20
updated: 2026-06-20
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, e6, parity, validation, cutover]
---

> **STATUS: completed 2026-06-20** (session `session_stanley_20260620_170330_keystone_e6_validation_cutover`).
> First mission of Phase E6 — opened by the **operator-authorized E5→E6 gate crossing** (AskUserQuestion: "Advance
> to E6"). Report: `missions/artifacts/e6_1_parity_report.md`. Verdict **GREEN**.

# Mission: E6.1 — Cross-system parity validation

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]]
**Phase**: 6 — Validation & cutover · **Mission**: E6.1 (first of the phase, the gating step)

## Goal

Confirm at campaign level that the shipped deliverable — `canvas_std` v2.0.0 — does not regress any consumer
(original CanvasForge + the three net-new in-vault consumers) before the cutover ceremony (E6.2). Read-only
validation: re-run every suite, every example's CLI conformance, the E3.3 parity proof, and the firewall invariant.

## Exit Gate
- Four suites green at recorded counts: `canvas_std` 46/8 · `brief_consumer` 10 · `deck_generator` 16 ·
  `document_generator` 37; all `ruff` clean.
- All four consumer examples build → `canvas-std validate` → `adna_native [OK]` + D-1/D-2/D-3.
- Cross-system parity (CanvasForge leg): deck floor-rejects 0 · comic floor-rejects 0 · structural equivalence to
  the locked reference; any SHA delta root-caused.
- Firewall: `canvas_std` git-diff 0; floor frozen since E0.2.
- Report artifact written. **HARD CHECKPOINT honored** — proceed to E6.2 only on GREEN.

## Objectives

### 1. Run the four suites + lint
- **Status**: completed · **Result**: 46/8 · 10 · 16 · 37; all `ruff` clean. No regression.

### 2. CLI conformance on every example
- **Status**: completed · **Result**: brief / deck / whitepaper / grant all `adna_native [OK]`, D-1/D-2/D-3 True
  (built to scratch paths; committed goldens untouched).

### 3. Cross-system parity proof (reuse `e3_3_parity_check.py`)
- **Status**: completed · **Result**: deck 56/20, 0 rejects; comic 11, 0 rejects; baseline `3ce4d341` untouched.
  `deck_norm_sha256` drifted `aa675665…`→`0d741640…`; **root-caused to a relocation-induced absolute image path**
  (pt09 archive move → `.resolve()` now yields `…/Archive.aDNA/…`). 55/56 node bodies byte-identical; fingerprint
  identical → **no structural regression**. Detail: `e6_1_parity_report.md` §3.

### 4. Firewall + freeze evidence
- **Status**: completed · **Result**: `canvas_std` tracked diff 0 vs HEAD; `schema.py` last touched at E0.2
  (`e2b1a5d`); no untracked. Two-shelf firewall intact.

### 5. Resolve the README staleness flag
- **Status**: completed · **Description**: `what/code/canvas_std/README.md` header still read "E0.1 skeleton / not
  yet functional" while the package is E2-complete (46/8; CHANGELOG confirms "no stubs remain"). Fixed **doc-only**
  (no schema/API change — firewall preserved). · **Files**: `what/code/canvas_std/README.md`

## Notes
- **Rigor over rubber-stamp:** the lone SHA delta was chased through five hypotheses (dates, in-process, hash-seed,
  git-frozen inputs, committed-ref diff) before the absolute-path root cause was isolated — the gate is credible
  precisely because the anomaly was explained, not assumed benign.
- **PT-P5 handoff:** re-baseline the parity capture at the relocated resident path; note the deck builder's absolute
  image-path embedding as a portability nit (KEEP-reference, not `canvas_std`).

## Completion Summary

Completed 2026-06-20. Verdict **GREEN** — `canvas_std` validated across the full consumer set with no regression;
the cross-system SHA delta is a fully-explained relocation artifact in the archived KEEP reference. Clears the
parity input to the E6.2 cutover-criteria checklist.

## AAR
- **Worked**: Reusing `e3_3_parity_check.py` verbatim gave a deterministic, API-free cross-system check; the
  committed-reference diff pinpointed the exact differing node in one step.
- **Didn't**: The E3.3 capture was never bit-reproducible across the pt09 relocation — a known limitation of
  absolute-path embedding, not caught at E3.3 because the move hadn't happened yet.
- **Finding**: All git-tracked build inputs were frozen yet output drifted → the cause was a *non-git*
  environmental input (a resolved absolute path), which only a content diff (not a git diff) could surface.
- **Change**: E6.1 now records both the suite/conformance matrix **and** a structural-equivalence proof against the
  *locked committed reference* (stronger than a prior-capture SHA match, which is path-fragile).
- **Follow-up**: PT-P5 re-baseline + the absolute-path portability nit (handoff register, E6.3).
