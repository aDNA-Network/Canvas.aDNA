---
type: artifact
artifact_id: cv_comic_style_01_calibration
campaign_id: campaign_canvas_halftone
phase: H6-reopen
created: 2026-08-22
updated: 2026-08-22
last_edited_by: agent_mondrian
status: active
tags: [artifact, halftone, h6, visual_check, trap, calibration, cv_comic_style_01]
---

# CV-COMIC-STYLE-01 calibration record (2026-08-22)

The trap the H6 offline pass left "deliberately still scaffolded" ("it compares rendered pixels
across panels, so it cannot be calibrated against the fake backend's solid PNGs — it needs H3's
real renders") is now **implemented and calibrated**: `canvas_core/traps/cv_comic_style_01.py`,
registry `status: implemented`.

## Mechanism (v0)

Per-panel signature = normalized 4×4×4 RGB histogram (64 bins) of a 64×64 thumbnail. Run style
centroid = mean signature. Drift score = symmetric chi-square distance to centroid. Fires above
`DRIFT_THRESHOLD`. Needs `asset_root` + ≥3 resolvable raster panels; pixel-statistics only —
character *identity* drift stays with the human eye-gate (R3).

## Calibration corpus and measurement

| | |
|---|---|
| Corpus | `what/artifacts/h3_first_light/spread*_v*.png` — **27 panels**, eye-gate **PASSED** 2026-08-13 |
| Consistent distribution | max **0.987** (`spread1_page1_p0_v1.png`) · mean **0.408** · min **0.190** (leave-one-out centroid) |
| Synthetic gross break | grayscale conversion of an H3 panel vs the run centroid: **1.482** |
| **Threshold chosen** | **1.20** — ~1.2× consistent max; below the grayscale-break score |

Interpretation: an eye-gate-passed corpus defines "consistent"; the threshold admits H3's full
measured diversity (including its most chromatically distinct panel at 0.987) and fires on a
gross palette/rendering break. Sensitivity is deliberately coarse at v0 — the trap's job is to
catch the *unmissable* break a tired reviewer might still miss, not to out-judge the eye-gate.
Tighten as more eye-gated corpora accumulate (`cycles_fired` discipline governs graduation).

## Tests

`canvas_core/tests/test_cv_comic_style_01.py` — 6 tests: asset_root guard · MIN_PANELS guard ·
consistent-run silence · gross-break firing (cold solid blue in a warm run) · non-raster/missing
ignored · threshold-vs-calibration constants guard.
