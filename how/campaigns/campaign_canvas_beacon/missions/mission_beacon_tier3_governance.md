---
type: mission
mission_id: mission_beacon_tier3_governance
campaign_id: campaign_canvas_beacon
phase: B4
status: in_progress
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
| **G1** | gate | **SITREP + HOLD** — governance changeset committed discretely; operator authorizes push + the B4.2 firewall touch | ⏳ at gate |
| **O5** | B4.2 | Implement A-5 relaxation in `reserved.py` (`role: derived` surfaces MAY omit `id`; surfaces-only scope guard) + positive fixture + regression tests; re-run harness (105/10 → N green) + `certify.py` | ☐ pending |
| **O6** | B4.2 | Cut Canvas Standard **v2.3.0** (STANDARD_VERSION + mirror sites; CHANGELOG `[2.3.0]` + 2.1.0 superseded; A-5 spec text); LIP-0008 → Implemented → Final | ☐ pending |
| **O7** | B4.2 | **SITREP + HOLD** — code/version touch as its own separate commit; operator-gated push; Beacon close (AARs + campaign completed + STATE reconcile) | ☐ pending |

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

_(written at mission close, after B4.2 — SO-5)_
