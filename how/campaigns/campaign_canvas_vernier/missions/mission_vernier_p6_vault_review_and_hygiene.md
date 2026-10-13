---
plan_id: mission_vernier_p6_vault_review_and_hygiene
type: plan
title: "Vault review and hygiene — compaction, the undefined finding, the stale pins, and the inbox turned into a gate"
owner: stanley
status: in_progress   # 2026-10-13: obj 1–6 run ahead of P2 by operator ruling (phase-order amendment); obj 7 + three opus items remain
campaign_id: campaign_canvas_vernier
campaign_phase: "P6"
campaign_mission_number: 5
mission_class: verification
executor_tier: sonnet
token_budget_estimated: "~150k (sonnet sweep) + ~60k (opus rulings)"
created: 2026-10-12
updated: 2026-10-13
last_edited_by: agent_mondrian
tags: [plan, campaign, vernier, hygiene]
---

# Mission: Vault review and hygiene — compaction, the undefined finding, the stale pins, and the inbox turned into a gate

**Campaign**: [[how/campaigns/campaign_canvas_vernier/campaign_canvas_vernier|campaign_canvas_vernier]]
**Phase**: P6 · **Mission**: 5 of 6 (chartered at the 2026-10-12 scope amendment)
**Depends on**: the signed verdicts at `how/gates/vernier_p1_exit_20261012` (P2) unless stated otherwise per objective.

## Goal

Discharge the governance-surface findings of the 2026-10-12 review (F-V-1, F-V-4, F-V-5) and the carried residue. Mechanical items run on sonnet; the three judgment items (F-DT-10 disposition, `data_bearing` ruling text, Seven Lamps review) on opus.

## Exit Gate

STATE.md top block ≤ 3K words with every struck banner relocated verbatim to `how/state_archive_20261012.md` (SO-7); F-DT-10 defined from the 09-15 session evidence or struck with the reason on the line; `canvas_context` derives its Standard version from `canvas_std` (no literal); `lip_draft_*` → `superseded` with pointers; `lip_queue_disposition` → `completed`; D3 registrar ping memo'd to Rosetta; **gate #11 `inbox_receipt`** in `gate_manifest.py` (untracked inbox file older than 7 days = ⛔; verified by derivation with a planted file); **`--check-doors`** compares every `.html` receiver URL to the sidecar (F-V-5); F-S078-04 fixed (`TB` accepted as alias of `TD`, test added) in `diagram_generator`; Seven Lamps proposal reviewed with a written disposition; ImagenWiring fleet consumer sweep run and pasted; `skill_l1_upgrade` RFC1918 upstream memo; ADR-012 `data_bearing` ruling text for City's register (Canvas is control-plane: `data_bearing: false`, with the `what/artifacts/` gitignored shelf named as the exception); doors archived per Home ADR-017 once ruled.

## Objectives

### 1. STATE compaction (sonnet) — archive file beside it, nothing deleted
### 2. F-DT-10 (opus) — define or strike, reason on the line
### 3. Pins + LIP statuses (sonnet)
### 4. Gate #11 `inbox_receipt` + `--check-doors` (sonnet; exit codes verified by derivation, F-GM precedent)
### 5. F-S078-04 `TB`→`TD` alias + test (sonnet; production code, not firewalled)
### 6. Seven Lamps review · ImagenWiring sweep · RFC1918 upstream · `data_bearing` ruling · D3 ping (opus)
### 7. Door hygiene per Home ADR-017 after verdicts land

## Campaign Context

- Review + triage this mission answers to: `artifacts/review_20261012_vault_state_and_inbox_triage.md`.
- Standing rules: phase gates are human gates · firewall touches named file-by-file before the signature · every figure re-derived before it is written · state the population on the face of the number.

## Notes

### Progress — 2026-10-13 (`session_stanley_20261013_vernier_receipt_door_refresh_p6`, opus)

| Obj | Item | State | Evidence |
|---|---|---|---|
| 1 | STATE compaction | ✅ | `431fbc3`: 433 → 131 lines, reconstruction byte-equal to HEAD; archive `how/state_archive_20261012.md` §A–§F; top block 933 words after the update |
| 2 | F-DT-10 | ✅ **defined** | `40e4fa5`: the label attached to Datum P4b D13b/D13c ("coverage by coincidence"), from the 09-15 session's own evidence |
| 3 | pins + LIP statuses | ✅ | `826ec1f` + `4d02745` (`canvas_context` STANDARD_VERSION derived, 0.3.2) · `806cd25` (two drafts → `superseded`; `text_quote_footnote` stays `resolved`, since it was never a LIP; queue → `completed`) |
| 4 | gate #11 + `--check-doors` | ✅ | `dcd7984`: both exits verified both ways with planted probes; one self-caught reporter slip |
| 5 | F-S078-04 | ✅ | `d7f14f4`: `TB`→`TD` alias, +1 test (52 + 1 failed against HEAD, then 53) |
| 6a | Seven Lamps | ✅ disposition | `e6b342a` → `artifacts/p6_seven_lamps_disposition.md`; the reply goes in the P4 wave |
| 6b | ImagenWiring sweep | ✅ | `4c2d77a`: 0 external call sites across 114 live root dirs |
| 6c | `data_bearing` ruling text | ⏸ **operator classification** | Home's register projects the key from **our own MANIFEST frontmatter** (`inventory_vaults.yaml` row_schema 2.2), so City reads Canvas as `unruled` → sealed because we never stated it. The value (`false` vs `split`) is an owner classification. Put to the operator at the sitting close |
| 6d | RFC1918 upstream memo · D3 registrar ping | ⏸ **batched** | one Rosetta memo with #20, after the `adr_011` verdict (#20's payload is ADR-011's erratum, and three separate Rosetta memos would repeat the F-V-1 load on their side) |
| 7 | door archival per Home ADR-017 | ⏸ waits for verdicts | — |

**Carried, observed not fixed:** `canvas_context/pyproject.toml` declares `0.2.0` against `__version__` `0.3.2`, a second drifted copy.
Left alone because the editable install's metadata would disagree with its dist-info until a reinstall.

## Completion Summary

*Fill out when setting `status: completed`.*

## AAR

*Mandatory before `status: completed` — Worked / Didn't / Finding / Change / Follow-up.*
