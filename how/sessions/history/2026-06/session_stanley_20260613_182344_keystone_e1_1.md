---
type: session
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [session, campaign, canvas, keystone, execution, e1_1, validate]
session_id: session_stanley_20260613_182344_keystone_e1_1
user: stanley
started: 2026-06-13T18:23:44-0700
status: completed
intent: "Operation Keystone E1.1 — implement validate(doc, level) for Core (C-*) and Extended (E-*) in canvas_std/validate.py against the golden fixtures. aDNA-Native (A-*) stays NotImplemented until E1.4; strip stays E1.5. Update the smoke test; verify the core/extended validate-xfails flip to PASS and the negative fixture rejects."
machine: stanley-local
tier: 1
heartbeat: 2026-06-13T18:27:25-0700
files_modified:
  - STATE.md
  - how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md
  - what/code/canvas_std/src/canvas_std/validate.py
  - what/code/canvas_std/tests/test_smoke.py
  - what/code/canvas_std/CHANGELOG.md
files_created:
  - how/campaigns/campaign_canvas_genesis/missions/mission_e1_1_validate.md
completed: 2026-06-13T18:27:25-0700
---

## Activity Log

- 18:23 — Operator: start E1.1. Implementing Core/Extended validation.
- 18:27 — `validate()` Core+Extended implemented + verified against the golden fixtures. E1.1 done; E1.2 next.

## SITREP

**Completed**:
- **Keystone E1.1** — `validate(doc, level)` implements Core (C-1..C-5) + Extended (E-1..E-4) in `canvas_std/validate.py` against the KEEP floor; monotone (aDNA-Native ⊃ Extended ⊃ Core). C-4 requires an explicit `toEnd`. aDNA-Native delegates A-* to `reserved.py` (NotImplementedError until E1.4); `strip` stays E1.5.
- Updated `test_smoke.py`. **Verified** (direct run): core/extended fixtures clean, negative rejects on C-4, aDNA-Native valid@Extended + raises@aDNA-Native, broken doc surfaces C-2/C-3/C-4. The core/extended/negative `validate` xfails in `test_fixtures.py` now PASS.

**In progress**: none — E1.1 closed.

**Next up**: **Keystone E1.2** — `to_canvas`/`from_canvas`/`compute_sync_hash` in `roundtrip.py`.

**Blockers**: none. (`pytest` absent in system Python — `make install` to run the suite.)

**Files touched**: see frontmatter.

## Next Session Prompt

Canvas.aDNA / Mondrian — **Operation Keystone (the v2.0.0 build) is ACTIVE; E0 (bootstrap) done; Phase E1 underway — E1.1 (`validate` Core/Extended) ✅ (2026-06-13).** `what/code/canvas_std/src/canvas_std/validate.py` now implements `validate(doc, level)` for Core (C-1..C-5) + Extended (E-1..E-4) against the KEEP floor (`schema.py`); aDNA-Native delegates the A-* (`_reserved`) checks to `reserved.py` which raises `NotImplementedError` until E1.4; `strip()` raises until E1.5. The golden fixtures (`tests/fixtures/`) validate as expected; the core/extended/negative `validate` xfails in `tests/test_fixtures.py` now PASS, the `adna_native` validate-xfail + all `strip`/degradation xfails remain (flip at E1.4/E1.5). **Run the suite with `cd what/code/canvas_std && make install && make test`** (system Python 3.14 lacks pytest; E1.1 was verified via a direct `PYTHONPATH=src python3` run). **Next mission: E1.2** — implement the round-trip converters in `src/canvas_std/roundtrip.py`: `to_canvas` (=`build`, forward source→view, deterministic), `from_canvas` (=`read_back`, advisory view→source draft), `compute_sync_hash` (16-hex SHA-256 over sorted node ids + sorted `from→to` edge pairs) per `spec_roundtrip_protocol_v2` §3–§4 (and the P1 finding that `to_canvas`/`from_canvas` alias the legacy `build`/`read_back`). Charter `mission_e1_2_roundtrip.md`; once it lands, remove `to_canvas`/`from_canvas`/`compute_sync_hash` from the smoke test's NotImplemented-stub list. Then E1.3 (`diff`/`merge`), E1.4 (`_reserved` validators → flips the `adna_native` validate-xfail), E1.5 (`strip` + D-1..D-3 → flips the degradation xfails). Building is in scope; Keystone phase gates are human gates — **E3** (CanvasForge migration; parity vs Wilhelm 8.80 / Issue 01 8.43) + **E6** (cutover) are load-bearing — do not start E3 without the operator. Side-tracks: Δ2 LIP (`what/decisions/lip_draft_canvas_as_primitive`); III/SiteForge upstream notes; III pin at E5.1.
