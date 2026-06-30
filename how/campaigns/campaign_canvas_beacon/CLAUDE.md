# CLAUDE.md — Campaign: Operation Beacon (`campaign_canvas_beacon`)

## Campaign Identity

| Field | Value |
|-------|-------|
| Campaign | `campaign_canvas_beacon` |
| Owner | stanley |
| Status | 🟢 **active** (chartered 2026-06-30 from the Lodestar P2 gate; scope Tier 0–3 locked) |
| Current Phase | **B1 — Tier 0 quick wins** (R0.1–R0.4). → B2 docs sprint → B3 publishing hardening → B4 governance unblock. HOLD at every gate. |
| Persona | Mondrian (Canvas.aDNA) |
| Predecessor | `campaign_canvas_lodestar` (Operation Lodestar — review-and-recommend; closed at P2 2026-06-30) |

## Quick Start

1. Read this file (auto-loaded in the campaign dir).
2. Read `campaign_canvas_beacon.md` — the master/charter (goal, decisions-locked, phases B1–B4, R-items, firewall handling, out-of-scope).
3. Read the **source of truth**: Lodestar's `../campaign_canvas_lodestar/missions/artifacts/lodestar_{gap_register,positioning_assessment,recommendations}.md` (R-IDs map there).
4. Check `STATE.md` for the open phase; run that phase's mission (create a session in `how/sessions/active/`).
5. **HOLD at every phase gate** (SO-1). Per-mission AAR (SO-5). Commit/push operator-gated (Git-Ops §3).

## Key Files

| File | Purpose |
|------|---------|
| `campaign_canvas_beacon.md` | Master/charter — phases B1–B4, R-items, decisions-locked, firewall handling, open items, out-of-scope |
| `missions/mission_beacon_tier0_quickwins.md` | Phase B1 mission (Tier 0; R0.1–R0.4) |
| `missions/artifacts/` | Per-mission deliverables / notes land here |
| `../campaign_canvas_lodestar/missions/artifacts/` | **Source of truth** — Lodestar's gap register · positioning assessment · recommendations |

## Standing Orders

- **This is a build, on a green base.** B1–B4 ship docs/spec/governance; the engineering is already done. Lift &
  repackage internal prose where it exists; don't re-derive.
- **`canvas_std` is touchable but firewalled-by-discipline.** Docs/metadata/additive-packaging only by default
  (README, schema `$id` note, CHANGELOG, an additive cert-kit runner). **Core `src/canvas_std/*.py` logic stays
  untouched** except the *gated* R3.3 A-5 ratification. **Re-run `pytest -q` after every `canvas_std` touch →
  expect `105 passed / 10 skipped`.** `git diff --stat -- src/canvas_std/*.py` empty except the gated touch.
- **Cross-vault writes are coord memos, never silent.** The D3 registrar arrangement (B4/R3.2) is staged as a
  `who/coordination/` memo to `aDNA.aDNA` (Rosetta); hold for ack before treating numbering final (Rule 10 / Git-Ops §6).
- **2.1.0 is a reconciliation, not a naive cut.** The Standard already ships v2.2.0 — resolve the slot in B4 before any release framing.
- **Phase gates are human gates.** SITREP + HOLD; never auto-advance; archive never delete (SO-6).

## Context Loading

| Subtopic | When |
|----------|------|
| Lodestar `lodestar_recommendations.md` (the tier menu) + `lodestar_gap_register.md` (the evidence) | Always — the plan + the gap IDs |
| `lodestar_positioning_assessment.md` | B2/B4 — the RLHF-surface story (R1.3 explainer) + the D2 deferral wording |
| `MANIFEST.md` · `what/code/canvas_std/README.md` · `what/production/{_scaffold,deck_generator}/README.md` · `how/skills/skill_canvas_producer_build.md` | B1/B2 — doc source material |
| `what/specs/spec_adna_canvas_standard.md` · `what/code/canvas_std/CHANGELOG.md` · `tests/fixtures/manifest.json` | B1/B3 — spec + publishing targets |
| `what/decisions/adr_003_standard_governance.md` · `what/decisions/lip_queue_disposition.md` · `Archive.aDNA/lattice-labs/how/governance/lips/` | B4 — governance home + LIP migration |

## Delegation Notes

Chartered 2026-06-30 immediately after closing Operation Lodestar at its P2 gate (same session,
`…_164238_beacon_charter_tier0`). The operator's four P2 answers (scope Tier 0–3 · new-campaign vehicle ·
D3 global+aDNA.aDNA registrar · commit+push review) are the ratification; the build plan is approved
(`~/.claude/plans/please-read-the-claude-md-snazzy-shore.md`). Keep phases **sequential + gated**: create
each B-phase mission only when its phase opens — never pre-spawn past a HOLD.
