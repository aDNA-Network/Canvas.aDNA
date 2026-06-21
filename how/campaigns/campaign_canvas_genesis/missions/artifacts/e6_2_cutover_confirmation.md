---
type: artifact
artifact_class: cutover_confirmation
created: 2026-06-20
updated: 2026-06-20
last_edited_by: agent_stanley
mission: mission_e6_2_cutover_shim_schedule
campaign: campaign_canvas_genesis
verdict: MET (floor/Standard) — federation-integration layer deferred to PT P5
tags: [artifact, cutover, confirmation, shim, retirement, keystone, e6]
---

# E6.2 — Final cutover confirmation + shim-retirement schedule

**Operation Keystone, Phase E6, mission E6.2.** Campaign-level confirmation of the cutover (the E3.4 floor cutover
already happened; this is the final cross-system confirmation + the shim-retirement schedule) per the campaign
`§Cutover & Rollback`.

## 1. Cutover criteria (campaign-level)

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | **Parity GREEN** | ✅ | E6.1 (`e6_1_parity_report.md`): `canvas_std` frozen since E0.2; four suites green (46/8 · 10 · 16 · 37); deck/comic 0 floor rejects; the lone SHA delta is a relocation-induced absolute image path, not a regression. |
| 2 | **Canvas-generation conformance green under the shim** | ✅ floor | KEEP floor re-run 2026-06-20: `canvas_core/tests` **736 passed / 3 skipped** + `canvas_comic/tests` **99 passed (+11 subtests)** = **835/3 green**. The shim emits its expected `DeprecationWarning`; **no `canvas_std`/`canvas_core` API breakage** (zero Import/Attribute/Type errors). |
| 2b | **Federation-integration tests** (`test_federation_validation.py`) | ⚠ **deferred → PT P5** | 25 failed / 30 errors / 10 passed — **all** `FileNotFoundError` on relocated consumer-wrapper lattices (`ScienceStanley.aDNA` presentationforge/graphicnovelforge, `ContextCommons.aDNA` presentationforge). Root cause: pt09 archived CanvasForge to `Archive.aDNA/`, breaking sibling-vault path resolution (tests resolve consumer paths relative to CanvasForge's own location). **This is the E5.2 / PT-P5 wrapper-refederation layer**, not a floor/Standard regression. See §3. |
| 3 | **`iii/` review ≥ baseline** | ✅ | E5.1 + E4.1 + E4.2 structural reviews all **0 High / 0 Med**; III pin v0.5.0 (`0f06aa6`); VR carries by construction (parity is structural). Pixel/VR1 explicitly PT-P5-gated (not scored as passing). |
| 4 | **Locked baseline SHA unchanged** | ✅ | `baseline_vr_scores.json` = `3ce4d341…` verified intact (CanvasForge Critical Rule 2). |
| 5 | **Rollback intact** | ✅ | `e3_4_rollback_rehearsal.md` runbook still valid: `core.py` frozen at `1a51801` (shim markers = 2, working-tree clean; the 4 commits since are banners/coordination/archive, not `core.py`); revert target `1a51801~1` exists; baseline intact. Net-zero, not time-pressured (grace window to 2027-06-13). |
| 6 | **Operator gate** | ✅ | E5→E6 crossing authorized this session ("Advance to E6"). Final campaign-close (`status: completed`) takes a second, explicit operator nod. |

**Decision:** the cutover is **CONFIRMED for what Keystone owns** — the Standard (`canvas_std`), the migrated floor
(`canvas_core` consuming `canvas_std` under the shim), and the three in-vault consumers — all green and
parity-proven. The **external-consumer federation wiring** (criterion 2b) is **explicitly deferred to PT P5 / E5.2**
(it is the wrapper-refederation work), red only because the pt09 relocation moved CanvasForge out from beside its
consumer vaults.

## 2. Shim-retirement schedule

- **Shim:** `canvas_core` re-exports the floor (10 `VALID_*` enums + `TYPE_MAPPING`/`EDGE_TYPE_MAPPING`) from
  `canvas_std.schema` behind a `DeprecationWarning` (`canvasforge.canvas_core.__init__`).
- **Grace window (E-D2):** 12 months → **retire on/after 2027-06-13** (decided E3.2; registered Home.aDNA §C).
- **Retire-condition (Standing Rule 9):** window-lapse **AND** verified ref-sweep-zero (no live `canvas_core`-floor
  importer outside `_archive/`/session history) **AND** owner-ack (Mondrian + Hestia).
- **Coupling:** the shim **folds into the pt09 merge** (Home §C #29) and the PT-P5 `canvas_core` relocation — when
  `canvas_core` moves to `Canvas.aDNA/what/production/canvas_core/` (ADR-004), the shim's re-export and its
  retirement are re-homed with it. Retirement is therefore **executed during/after PT P5**, never inside Keystone.
- **Action:** confirmation memo to Hestia (Home.aDNA owns the shim ledger) —
  `who/coordination/coord_2026_06_20_mondrian_to_hestia_shim_retirement_schedule.md`. No direct edit to the
  `Home.aDNA` tree (cross-vault hygiene); Hestia records/updates §C.

## 3. Federation-integration finding → PT P5 handoff

The 55 red `test_federation_validation.py` cases are the concrete manifestation of "**E5.2 federation rollout is
PT-P5-coupled**." pt09 physically relocated CanvasForge under `Archive.aDNA/`, so its federation tests — which
resolve consumer-wrapper lattice paths *relative to CanvasForge's location* — now look under
`…/Archive.aDNA/ScienceStanley.aDNA/…` (wrong) instead of `…/ScienceStanley.aDNA/…`. PT P5 (the ~8 consumer-wrapper
refederations) repoints these. Until then they are **expected-red**, tracked here and in the E6.3 handoff register.
**Not a `canvas_std` defect, not a floor regression** (the floor is 835/3 green; only the relative-path resolution
in the archived integration tests broke).

## Conclusion

Cutover criteria **MET at the Standard/floor level**; the cross-system cutover is confirmed for the Keystone
deliverable. The federation-integration layer is honestly recorded as **PT-P5-deferred** (criterion 2b), not
green-washed. Shim retirement is **scheduled** (2027-06-13, SR-9 retire-condition), executed at/after PT P5. Clears
E6.2 → E6.3 (campaign AAR + handoff), pending the operator's campaign-close disposition.
