---
type: artifact
artifact_class: rollback_rehearsal
created: 2026-06-14
updated: 2026-06-14
last_edited_by: agent_stanley
mission: mission_e3_4_cutover
campaign: campaign_canvas_genesis
result: PASS
tags: [artifact, rollback, rehearsal, cutover, keystone, e3, canvasforge]
---

# E3.4 — Rollback rehearsal: **PASS** ✅

**Operation Keystone, Phase E3, mission E3.4 (cutover), objective 2.**

Demonstrates that the CanvasForge migration to `canvas_std` is cleanly **reversible**: reverting the E3.2 shim
commit restores the pre-migration embedded path with no consumer breakage, and restoring HEAD returns the shim —
**net-zero to the working tree**. This is the safety net that makes the cutover (objective 3) safe to commit.

## Setup

- **CanvasForge HEAD** = `1a51801` (the E3.2 constants-only shim; 0 commits since) — so the rollback target is a
  single-file revert: `what/code/canvas_core/core.py` at `1a51801~1`.
- **Test env**: gitignored `.venv` at `CanvasForge.aDNA/what/code/` (`adna-canvas-std` editable).
- **Suite**: `pytest canvas_core/tests/ canvas_comic/tests/ tests/test_federation_validation.py`.
- **Baseline guard**: `canvas_core/tests/fixtures/baseline_vr_scores.json` SHA `3ce4d341…` (CanvasForge Critical Rule 2).

## Procedure & results

| Step | Action | Result |
|------|--------|--------|
| 0 | Pre-state (shim ON / HEAD): record baseline SHA + run suite | baseline `3ce4d341…`; **900 passed / 3 skipped / 11 subtests** (1.47s); `core.py` line 41 = `from canvas_std import schema … # DEPRECATED_STUB` |
| 1 | Roll back the shim: `git checkout 1a51801~1 -- what/code/canvas_core/core.py` | shim markers = **0** (gone); embedded floor present (`VALID_SHAPES = frozenset(…)`) |
| 2 | Suite on the **embedded** (rolled-back) path | **900 passed / 3 skipped / 11 subtests** (1.33s) — self-contained, **no `canvas_std` import**, no consumer breakage |
| 3 | Restore HEAD: `git checkout HEAD -- what/code/canvas_core/core.py` (unconditional) | shim markers = **2** (back); `git status` for `core.py` = **empty (clean)** |
| 4 | Post-state baseline SHA | `3ce4d341…` **UNCHANGED** |

## Findings

- **Reversible & clean.** Reverting `1a51801` restores a fully-green, self-contained pre-migration state; restoring
  HEAD returns the shim. The tree is byte-identical before and after (net-zero) — the rehearsal leaves no trace.
- **No consumer breakage.** The embedded path passes 900/3 with no `canvas_std` dependency. The shim's forward
  promise (the *old* import path `from canvas_core import …` keeps working post-migration) is already proven by the
  shim-ON suite at HEAD (step 0, 900/3). Both directions hold.
- **Floor parity confirmed operationally.** Both the shim path and the embedded path give an identical 900/3 — the
  embedded constants are verbatim-identical to `canvas_std.schema` (consistent with the E3.3 structural-identity proof).

## Rollback runbook (for E6.2 / contingency)

```bash
CF=~/aDNA/CanvasForge.aDNA
git -C $CF checkout 1a51801~1 -- what/code/canvas_core/core.py   # restore embedded floor
# (or `git -C $CF revert 1a51801` for a committed rollback)
# verify: cd $CF/what/code && .venv/bin/python -m pytest canvas_core/tests/ canvas_comic/tests/ tests/test_federation_validation.py -q
```
The shim re-export keeps the old `canvas_core` import path working through the E-D2 grace window (expiry 2027-06-13),
so a rollback is never time-pressured during that window.
