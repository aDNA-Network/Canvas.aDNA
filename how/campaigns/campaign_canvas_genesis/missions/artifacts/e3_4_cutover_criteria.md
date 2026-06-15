---
type: artifact
artifact_class: cutover_criteria
created: 2026-06-14
updated: 2026-06-14
last_edited_by: agent_stanley
mission: mission_e3_4_cutover
campaign: campaign_canvas_genesis
verdict: MET
tags: [artifact, cutover, criteria, gate, keystone, e3, canvasforge]
---

# E3.4 — Cutover criteria: **ALL MET** ✅

**Operation Keystone, Phase E3 (CanvasForge migration), mission E3.4 (cutover), objective 1.**

The cutover is the **one-way step** of E3 — it supersedes CanvasForge's embedded Canvas Standard v1.0.0 framing in
favor of consuming v2.0.0 from Canvas.aDNA. Per the campaign `§Cutover & Rollback`, cutover proceeds **only** when
all of the following are met. They are.

## Criteria checklist

| # | Criterion | Target | Status | Evidence |
|---|-----------|--------|--------|----------|
| 1 | **Parity gate GREEN** | E3.3 no-regression vs Wilhelm 8.80 / Issue 01 8.43 | ✅ | `artifacts/e3_3_parity_verdict.md` — shim output-neutral; A/B normalized-canvas SHA identical shim-ON vs shim-OFF (`aa675665…`); 0 federated-floor rejects (deck 56 / comic 11) |
| 2 | **Conformance suite green** | CanvasForge suite passes under the shim | ✅ | `pytest` **900 passed / 3 skipped / 11 subtests** (this session, shim-ON) |
| 3 | **`iii/` review ≥ baseline** | VR1–VR5 ≥ Wilhelm 8.80 / Issue 01 8.43 | ✅ | by construction — E3.3 proved output is structurally identical, so any VR re-score is unchanged. `iii/` pin v0.4.0 / canonical jsonl md5 `5adb0dfa…` unchanged. *(A live re-review is optional; it would measure only model noise — the same rationale that selected E3.3 Approach A.)* |
| 4 | **Locked baseline SHA unchanged** | `3ce4d341…` (Critical Rule 2) | ✅ | verified pre + post this session |
| 5 | **Rollback rehearsed** | revert restores pre-migration path, no consumer breakage | ✅ | `artifacts/e3_4_rollback_rehearsal.md` — net-zero revert/restore; embedded path 900/3; tree clean; baseline unchanged |
| 6 | **Operator gate** | cutover is operator-approved (consequential / one-way) | ✅ | operator authorized **full cutover** 2026-06-14 (plan approval) |

## Decision

**CUT OVER.** All six criteria are met. Proceed to objective 3 (supersede the embedded v1.0.0 framing — banner;
archive-never-delete) and objective 4 (schedule the `canvas_core` shim retirement in the Home.aDNA ledger).

## Notes

- **Reversibility preserved.** Cutover supersedes by **banner**, not deletion (SO-6 archive-never-delete), and the
  `canvas_core`→`canvas_std` shim stays live through the E-D2 grace window (expiry 2027-06-13). The cutover is
  "committed" but not irrecoverable: the rollback runbook in `e3_4_rollback_rehearsal.md` restores the embedded path.
- **Final cross-system cutover + shim retirement** are deferred to **E6.2** (all consumers green), scheduled in the
  Home.aDNA shim ledger (objective 4).
