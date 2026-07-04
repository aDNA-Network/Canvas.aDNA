---
campaign_id: campaign_canvas_beacon
type: campaign
title: "Operation Beacon — Canvas Standard publish-hardening & governance unblock"
owner: stanley
status: completed
estimated_sessions: "4-7"
phase_count: 4
mission_count: 4
priority: high
predecessor: campaign_canvas_lodestar
created: 2026-06-30
updated: 2026-07-02
last_edited_by: agent_mondrian
status_history: "active (2026-06-30 — chartered from the Lodestar P2 gate; scope=Tier 0–3 · D3=global+aDNA.aDNA registrar · D2=no-LIP-0009-reopen) → completed (2026-07-02 — all four phases shipped: B1 quick-wins · B2 docs · B3 publishing/cert-kit · B4 governance-unblock + LIP-0008 A-5 relaxation cut into Standard v2.3.0)"
tags: [campaign, canvas, beacon, publishing, documentation, governance, standard, lip, conformance, rlhf]
---

# Campaign: Operation Beacon — Canvas Standard publish-hardening & governance unblock

> The **build** that **Operation Lodestar** (review-and-recommend, closed at its P2 gate 2026-06-30)
> recommended and the operator gated. Lodestar reviewed; Beacon builds. R-IDs below map to Lodestar's
> deliverables (`../campaign_canvas_lodestar/missions/artifacts/lodestar_{gap_register,positioning_assessment,recommendations}.md`).

## ✅ Completion Summary (2026-07-02)

**Operation Beacon is COMPLETE.** All four human-gated phases shipped on a green base; the aDNA Canvas Standard is now navigable, citable, self-certifying, and its governance is unblocked.

| Phase | Shipped |
|-------|---------|
| **B1 · Tier 0** | Wrong-repo/dead-link fixes · `canvas_std/README` version-currency · spec title/H1 · schema `$id` pin-note. |
| **B2 · Tier 1** | Root **`README.md`** · **MANIFEST** refresh · **producer quickstart** · **Standard explainer** (RLHF-surface story) · `VISION.md` replaced (B6). |
| **B3 · Tier 2** | **Citable spec** (Abstract · CC-BY-4.0 · stable identifier · resolvable refs) · standard-scope **version-history** · **certification kit** · specs index. |
| **B4 · Tier 3** | **LIP governance home** stood up (`who/governance/lips/`) + LIP-0008/0009 migrated live · dead `lattice-labs` refs re-pointed (`adr_003` Amendment) · Rosetta registrar memo staged · **LIP-0008 A-5 relaxation implemented + cut into Canvas Standard v2.3.0** (LIP-0008 → Final; LIP-0009 → Final/Option V). |

**End state:** aDNA Canvas Standard **v2.3.0**; `canvas_std` **115 passed / 10 skipped**, certification **11/11**; firewall clean (B4.2 = one reviewable `reserved.py` touch; `validate.py`/`schema.py` untouched). Commits: B1 `2299be0` · B2 `3d69261`/`465fbc2` · B3 `c79ac58` · B4.1 governance `b344968` · B4.2 v2.3.0 + close (this session).

**Open tail (non-blocking):** the **D3 registrar handshake** — a cross-vault coord memo to `aDNA.aDNA` (Rosetta) is staged and **pending ack** (`#needs-human`); until then Canvas LIP numbering is provisional-final under the inherited global numbers. **Named second wave:** Tier 4 spec-it (prompting primitive · RLHF seam). **Deferred/hold-open:** C-iv canvas-as-primitive (D2, `idea_oip_v1x_interface_reanchor`); producer marker-node cleanup (now optional).

### Campaign AAR
- **Worked:** the tier structure front-loaded credibility-per-hour (Tier 0/1 = high-visibility, low-risk) and isolated the one genuinely-blocked + code-touching item (B4) to the end, behind its own gate. ~80% of the doc layer was repackaged internal prose, not new writing. Every `canvas_std` touch stayed reviewable; the harness never regressed (105 → 115).
- **Didn't:** Tier 4 (spec-it) stayed out (named second wave); the D3 registrar remains a pending cross-vault ack (correctly held, not forced).
- **Finding:** the B4 investigation earned its keep — the A-5 relaxation was *not* already in v2.2.0, so "advance LIP-0008 to Final" was a real gated code cut (v2.3.0), not a paper flip; the reserved 2.1.0 slot reconciled cleanly as *superseded*.
- **Change:** the repo went from invisible-but-strong to a published Standard — root README + explainer + citable spec (CC-BY-4.0) + cert kit + a live LIP governance home; Standard v2.2.0 → **v2.3.0**.
- **Follow-up:** Rosetta registrar ack; Tier 4 second wave when scheduled; producers may drop synthetic marker nodes.

## Goal

Turn a **technically-strong-but-externally-invisible** Canvas Standard into a **navigable, citable, governed
published Standard** — and build the evidence base a future canvas-as-primitive claim would need. Concretely:
ship the documentation layer (README · explainer · producer quickstart), make the spec externally citable
(abstract · license · version-history · conformance kit), and **unblock the LIP-governance home** (dead since
`lattice-labs` archived 2026-06-27) so v2.1.0 can land. **Articulation, not engineering** — most prose exists
internally and is repackaged; the build is mostly doc/metadata + a small governance unblock on a green base.

## Context (from Lodestar)

Six campaigns (Cartography → Keystone → Atelier → Palette → Salon → Armature) built the three-leg canvas
thesis to a runtime-enabled state — **386 tests green** (canvas_std 105/10 · canvas_context 58 · 7 producers
223), full C/E/A/I/D conformance, 9 ratified specs. Lodestar found the build solid but **invisible + under-
articulated**: no root README, no Canvas explainer/quickstart; spec text unlicensed + version-stale; the LIP
home dead (blocking v2.1.0); and the most differentiated asset — a *working, operational* **Canvas-as-RLHF
surface** (13 live records) — buried in a producer and undersold as an "audit trail."

## Decisions locked (operator, at the Lodestar P2 gate, 2026-06-30)

| Decision | Choice |
|----------|--------|
| **Scope** | Tier 0 + 1 + 2 + 3 (full publish-hardening). **Tier 4 spec-it = named second wave (OUT).** |
| **Vehicle** | This campaign — `campaign_canvas_beacon` — phases B1–B4. |
| **D3 numbering** | Global LIP sequence + **`aDNA.aDNA` as number registrar**; Canvas holds content + ratification. |
| **D2 LIP-0009** | Accept "no re-open" (keep Option V); record the deferral in the new home at Tier 3. |
| **B6 VISION** | Unresolved sub-decision — confirm replace-vs-add at Phase B2 (recommend: replace the generic `VISION.md`). |

## Phases (human-gated; never auto-advance — SO-1)

| Phase | Tier | What | Gate |
|-------|------|------|------|
| **B1** | Tier 0 | **Quick wins** — R0.1 fix wrong-repo/dead links · R0.2 refresh `canvas_std/README` · R0.3 fix spec title/H1 + stale producer names · R0.4 schema `$id` pin-note. | SITREP + HOLD |
| **B2** | Tier 1 | **Documentation sprint** — R1.1 root README · R1.4 MANIFEST refresh · R1.2 producer quickstart · R1.3 Standard explainer · (B6 VISION sub-gate). | SITREP + HOLD |
| **B3** | Tier 2 | **Publishing hardening** — R2.1 citable spec (abstract/license/refs/ID) · R2.2 standard-scope version-history (+back-fill `[2.0.2]`) · R2.3 conformance cert kit · R2.4 external index. | SITREP + HOLD |
| **B4** | Tier 3 | **Governance unblock → v2.1.0 reconciliation** — R3.1 stand up `who/governance/lips/` (fork CC0 `lip_0001`; migrate live `lip_0008`/`lip_0009`; re-point `adr_003 §2`) · R3.2 cross-vault coord memo to `aDNA.aDNA` (D3 registrar) · R3.3 reconcile the 2.1.0 slot + advance LIP-0008 → Final + record LIP-0009 Option-V. | SITREP + HOLD |

## Firewall handling (`canvas_std` touches)

Lodestar was read-only (`canvas_std` git-diff 0). **Beacon deliberately + reviewably touches the
`what/code/canvas_std/` tree** — but **docs/metadata/additive-packaging only** by default: `README.md` (R0.2),
the schema `$id` note (R0.4), `CHANGELOG.md` (R2.2), an additive cert-kit runner (R2.3). **Core
validator/converter logic (`src/canvas_std/*.py`) stays untouched** — the sole exception is the *gated* R3.3
A-5 ratification (its own small reviewable touch under ratified LIP-0008, the Armature precedent). **After
every `canvas_std` touch, re-run `pytest -q` and confirm `105 passed / 10 skipped` stays green.**

## Open items to resolve in-flight
- **2.1.0 slot reconciliation** (B4/R3.3) — the Standard already ships v2.2.0, so the LIP-0008 A-5 relaxation
  can't be retro-inserted as 2.1.0. Investigate whether it's already implemented in the v2.2.0 validator →
  fold-into-2.2.0 (record slot as reserved/superseded) **or** ship as a gated patch/minor (2.2.1/2.3.0).
- **B6 VISION** replace-vs-add (B2 sub-gate).
- **D3 registrar handshake** — cross-vault dependency; hold for `aDNA.aDNA` (Rosetta) ack before treating numbering final.

## Out of scope (named second wave + deferred)
- **Tier 4 spec-it** (C-i prompting primitive · C-ii RLHF seam) — planned **second wave** after Beacon (additive/firewall-safe).
- **C-iii pattern-memorialization** (defer) · **C-iv canvas-as-primitive / LIP-0009 re-open** (hold-open; trigger = a real registry/federation consumer; tracked via `idea_oip_v1x_interface_reanchor`).
- Lower-priority docs **B5** (Canvas↔Lattice integration) · **B8** (repo-map) · **B9** (glossary) — candidate adds, not gated tiers.
- **A8** legacy federation suite (PT-P5, Hestia-owned) · **Hearthlight Tier-B** rollout (Hestia-owned).

## Missions (all completed)

- → `missions/mission_beacon_tier0_quickwins.md` (Phase B1 — quick wins). ✅
- → `missions/mission_beacon_tier1_docs.md` (Phase B2 — documentation sprint). ✅
- → `missions/mission_beacon_tier2_publishing.md` (Phase B3 — publishing hardening). ✅
- → `missions/mission_beacon_tier3_governance.md` (Phase B4 — governance unblock + v2.3.0 A-5 relaxation). ✅

## Reuse, not rebuild
- Lodestar's three deliverables = the source of truth (gap IDs, positioning calls, the tier menu).
- `what/production/{_scaffold,deck_generator}/README.md` + `how/skills/skill_canvas_producer_build.md` → the producer quickstart (near-pure assembly).
- `MANIFEST.md:15-23` (thesis) + `canvas_std/README` (quickstart) → the root README.
- The archived CC0 `lip_0001_lip_process.md` → forkable process doc for the new LIP home.
- The `canvas-std` conformance harness + `tests/fixtures/` (10 golden + manifest) → the cert kit + green re-verification.

## Next-session prompt
> Open `how/campaigns/campaign_canvas_beacon/` (read its `CLAUDE.md` + this master). Operation Beacon is the
> gated build following Operation Lodestar — scope **Tier 0–3**, decisions locked (D3=global+aDNA.aDNA
> registrar · D2=accept no-reopen). Check `STATE.md` for the current phase. Execute the open phase's mission,
> re-running `pytest -q` in `what/code/canvas_std/` after any touch there (expect 105/10). **HOLD at every
> B-phase gate** (SO-1) — SITREP + operator approval before advancing; per-mission AAR (SO-5); commit/push
> operator-gated (Git-Ops §3). Lodestar's `missions/artifacts/` deliverables are the source of truth.

## Provenance
Chartered 2026-06-30 from the Operation Lodestar P2 gate (closed same day). The operator answered a 4-question
gate (scope / vehicle / D3 numbering / review-commit) and approved the build plan
(`~/.claude/plans/please-read-the-claude-md-snazzy-shore.md`). Predecessor campaign:
`campaign_canvas_lodestar` (review-and-recommend). Session: `…_164238_beacon_charter_tier0`.
