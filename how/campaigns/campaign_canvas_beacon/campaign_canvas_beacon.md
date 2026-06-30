---
campaign_id: campaign_canvas_beacon
type: campaign
title: "Operation Beacon — Canvas Standard publish-hardening & governance unblock"
owner: stanley
status: active
estimated_sessions: "4-7"
phase_count: 4
mission_count: 1
priority: high
predecessor: campaign_canvas_lodestar
created: 2026-06-30
updated: 2026-06-30
last_edited_by: agent_mondrian
status_history: "active (2026-06-30 — chartered from the Lodestar P2 gate; operator ratified scope=Tier 0–3 full publish-hardening · vehicle=new campaign · D3=global+aDNA.aDNA registrar · D2=accept no-LIP-0009-reopen via the approved plan; Phase B1 Tier-0 executing in session …_164238)"
tags: [campaign, canvas, beacon, publishing, documentation, governance, standard, lip, conformance, rlhf]
---

# Campaign: Operation Beacon — Canvas Standard publish-hardening & governance unblock

> The **build** that **Operation Lodestar** (review-and-recommend, closed at its P2 gate 2026-06-30)
> recommended and the operator gated. Lodestar reviewed; Beacon builds. R-IDs below map to Lodestar's
> deliverables (`../campaign_canvas_lodestar/missions/artifacts/lodestar_{gap_register,positioning_assessment,recommendations}.md`).

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

## Missions

- → `missions/mission_beacon_tier0_quickwins.md` (Phase B1 — created at charter; executing).
- B2/B3/B4 missions are created when their phase opens (after the prior phase's operator gate). Never pre-spawn past a HOLD.

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
