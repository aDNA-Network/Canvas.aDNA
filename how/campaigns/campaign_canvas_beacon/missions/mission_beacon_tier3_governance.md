---
type: mission
mission_id: mission_beacon_tier3_governance
campaign_id: campaign_canvas_beacon
phase: B4
status: completed
owner: stanley
persona: Mondrian
created: 2026-07-02
updated: 2026-07-02
last_edited_by: agent_mondrian
tags: [mission, beacon, tier3, governance, lip, canvas_std, v2.3.0, firewall]
---

# Mission: Operation Beacon — Phase B4 / Tier-3 governance unblock + LIP-0008 → v2.3.0

## Intent

Unblock the one genuinely-blocked Lodestar item: the LIP-governance home died when `lattice-labs` was archived
(2026-06-27), leaving `adr_003 §2` on a dead path and LIP-0008 unable to advance. Stand up a Canvas-local LIP home,
migrate the two Canvas-stewarded LIPs live, re-point the dead refs, stage the aDNA.aDNA registrar handshake, and
**reconcile LIP-0008** — which the B4 investigation proved is **not** implemented in v2.2.0, so (operator chose FULL)
implement the A-5 relaxation and cut Canvas Standard **v2.3.0**.

Two objective groups with a firewall gate between: **B4.1** pure governance (zero `src/*.py` touch), then **B4.2** the
single reviewable `canvas_std` touch + version cut. Governance and code commit **separately**.

## Objectives

| # | Grp | Objective | Status |
|---|-----|-----------|--------|
| **O1** | B4.1 | Stand up `who/governance/lips/` — fork CC0 `lip_0001` + `lip_template`; migrate live `lip_0008`/`lip_0009`; author Canvas-scoped `lip_registry` + dir `AGENTS.md` | ✅ done |
| **O2** | B4.1 | Re-point dead governance refs — `adr_003 §2`/Context/Related (dated Amendment, not silent edit) + `adr_000`; annotate `lip_queue_disposition` + the two `lip_draft_*` (migration banners, history preserved) | ✅ done |
| **O3** | B4.1 | LIP-0009 → **Final** (Option V; no re-open, D2); LIP-0008 → **Accepted** (review lapsed 2026-06-27, FA-ratified) | ✅ done |
| **O4** | B4.1 | Stage the aDNA.aDNA (Rosetta) registrar coord memo (cross-vault, gated; never a silent write) | ✅ done |
| **G1** | gate | **SITREP + HOLD** — governance changeset committed discretely (`b344968`); operator chose "proceed to B4.2, push both at close" | ✅ done |
| **O5** | B4.2 | Implement A-5 relaxation in `reserved.py` (`role: derived` surfaces MAY omit `id`; surfaces-only scope guard) + positive fixture + 3 regression tests; harness **115/10** + `certify.py` **11/11** | ✅ done |
| **O6** | B4.2 | Cut Canvas Standard **v2.3.0** (STANDARD_VERSION + all mirror sites; CHANGELOG `[2.3.0]` + 2.1.0 superseded; A-5 spec text §5.2/§6 + conformance suite); LIP-0008 → Implemented → **Final** | ✅ done |
| **O7** | B4.2 | Code/version touch as its own separate commit; push at close; Beacon close (AARs + campaign completed + STATE reconcile) | ✅ done |

## Notes
- **Firewall (ADR-004 two-shelf).** B4.1 touched **zero** `canvas_std/src/*.py`. B4.2 is the sole gated logic touch —
  `reserved.py` `validate_panel_link` surfaces loop only; `validate.py`/`schema.py` node-id logic **unchanged**; harness
  re-run mandatory; committed apart from the governance docs.
- **Version reconciliation.** LIP-0008 targeted v2.1.0; the Standard shipped v2.2.0 (Armature) first, so 2.1.0 is
  **superseded** — the relaxation lands as **v2.3.0** (MINOR; relaxing/backward-compatible).
- **Cross-vault dependency.** D3 registrar (aDNA.aDNA) is a staged coord memo, **pending Rosetta ack**; Canvas numbering
  is provisional-final under inherited global numbers until then.
- **Lifecycle correctness.** LIP-0001 requires *Implemented* before *Final*; hence LIP-0008 is Accepted in B4.1 and only
  Final in B4.2 (once the code lands). LIP-0009 (Option V = status quo) has a vacuous implementation → Final in B4.1.

## AAR

- **Worked:** the two-mission firewall split held cleanly — B4.1 pure governance (`canvas_std/src` git-diff 0), B4.2 the single gated `reserved.py` touch. The A-5 relaxation was a 9-line surgical change (skip id-resolution only for `role: derived` with no `id`); the harness went 105→**115/10** (+3 regression tests + the golden fixture) with zero prior-test regression, and `certify.py` reached **11/11**. The v2.3.0 cut mirrored the v2.0.1/2.0.2 site-list exactly (STANDARD_VERSION · schema title/x-standard-version [$id kept] · conformance.py ×3 · test_smoke ×2 · test_conformance ×1 · 9 spec frontmatters · federation example · core-spec title/H1/table · specs README).
- **Didn't:** didn't renumber the LIPs (D3 keeps global 0008/0009 under an aDNA.aDNA registrar — a cross-vault dependency held open, pending Rosetta ack); didn't touch producers (they still mint synthetic marker nodes — now *optional*/valid, a future cleanup); didn't retro-insert 2.1.0 (recorded **superseded**).
- **Finding:** the B4 investigation was right — the A-5 relaxation was genuinely **un-implemented** in v2.2.0, so advancing LIP-0008 to Final *required* real, gated code (not a paper flip). The scope guard (only `role: derived` exempt; canonical + id-bearing derived still resolve) is locked by 3 regression tests, so a future accidental over-relaxation fails CI.
- **Change:** reserved 2.1.0 → **superseded**; the relaxation shipped as **v2.3.0** (MINOR, backward-compatible). LIP-0008 → **Final** (landed v2.3.0); LIP-0009 → **Final** (Option V, no re-open). `adr_003 §2` re-pointed to the Canvas-local LIP home via a dated Amendment.
- **Follow-up:** Rosetta registrar ack (**#needs-human**, non-blocking); producers MAY drop synthetic marker nodes (future producer work); Tier 4 spec-it (prompting primitive · RLHF seam) remains the named second wave; on ack, flip `adr_003` Amendment 1 + `lip_registry` from "pending" to ratified.
