---
type: artifact
artifact_id: halftone_campaign_aar_rollup
campaign_id: campaign_canvas_halftone
created: 2026-08-22
updated: 2026-08-22
last_edited_by: agent_mondrian
status: active
tags: [artifact, halftone, aar, rollup, campaign_close]
---

# Operation Halftone — campaign AAR rollup (2026-08-22)

Chartered 2026-07-09 · amended 2026-08-03 (+HV/+HR/+HF) · completed 2026-08-22.
10 phases, 9 missions, ~14 sessions. Proof milestone achieved: **the first rendered comic pages in
the fleet's history** — 27 panels / $3.618 / 4 print-ready pages / eye-gate PASSED.

## The five findings that should outlive the campaign

1. **"Has this line ever run?" beats every assertion suite.** The campaign's defining defect family
   was code that was written, looked correct, and had never executed: `export_spread` unreachable
   (spreads silently squashed 2:1) · `RLHF_SIGNAL_TYPE_REJECT` declared and never emitted · the H4
   `_poll_history` 30s HTTP timeout doubling as the generation deadline · `build_comic_parity.py`
   broken since PT-P5. None was wrong logic; all were unreachable/unemitted paths every test passed
   around. (H6 O5, H3 O5, H4, R5.)

2. **Look at the pixels.** Three phases in a row, visual confirmation caught what assertions could
   not: H2's aspect drift, H4's picture-of-nothing, H6's spread split passing every assertion on two
   flat green rectangles. The doctrine "no canvas ships without an agent-confirmed render" earned
   graduation into the producer skill and federation contract (Amendment 1).

3. **Verify blockers before reporting them up.** The 2026-08-09 "blocked on billing" call was a
   misdiagnosis — a depleted credential read while the funded Vertex lane sat unused on the same
   machine. It cost three days and produced a false STATE. The correction (read Home's credential
   inventory before believing any quota/auth failure) is now standing doctrine and drove Operation
   Rosetta Stone's shared `googleai` layer fleet-wide.

4. **Records drift unless re-measured at the moment of use.** STATE.md was "actively false in six
   places" at the 2026-08-12 wind-down; adr_009's importer census said 1 where measurement said 4
   (F-H6RE-1); the federation-validation module validated wrappers its owners had retired
   (F-H6RE-2); the dev-lane annex's own pointer called a ratified artifact "draft". The pattern:
   a task list is not a record of state — re-measure before acting on any census.

5. **Calibrate against human-judged corpora, not invented thresholds.** CV-COMIC-STYLE-01's
   threshold brackets between the eye-gate-passed corpus's measured max (0.987) and a synthetic
   gross break (1.482). The eye-gate also proved art-consistency held with **no LoRA** — R3's
   risk pricing was conservative, which re-sequences the successor's ComfyUI work (refine-stage
   LoRA is an enhancement, not a blocker).

## Per-mission AAR index

| Mission | Status | AAR |
|---|---|---|
| h1 producer hardening | completed | in-mission (SO-5) |
| hv visual fidelity | completed | in-mission |
| h2 render bridge | completed | in-mission |
| h5 visualdna compose | completed | in-mission |
| hr review surface | built; gate 3/3 = standing operator item | in-mission |
| hf federation hygiene | completed | in-mission |
| h4 vulcan seam | completed (live chain carried) | in-mission |
| h3 first light | completed | in-mission + wind-down AARs (2026-08-12) |
| h6 close | completed (offline 2026-08-09 + re-open 2026-08-22) | two AARs in-mission |

## Carried forward (successor: Operation Blueprint)

H4 live `generate:gemini,refine:comfy` chain (spend-gated; needs ComfyUI standing) · RLHF pilot
second consumer = the ComfyUI variant-selection board · legacy panel-side `ImagenWiring`
deprecation candidates · `comic_book_design/` resurrect-or-archive ruling (SS notified).
**Standing operator items:** HR gate 3/3 review pass · adr_010 §7.7 signature · push GO batch.
