---
type: session
session_id: session_stanley_20260809_211323_halftone_h6_offline
user: stanley
persona: Mondrian
tier: 2
campaign: campaign_canvas_halftone
mission: mission_h6_close
created: 2026-08-09
updated: 2026-08-09
status: active
last_edited_by: agent_mondrian
tags: [session, halftone, h6, print, spread, cmyk, dpi, rlhf_seam, dispatch_contract, authoring_contract, visual_check_profile, canvas_comic]
---

# Session: Halftone H6 — the offline pass

## Intent

Open **H6** and execute everything in it that needs neither real pixels nor the campaign close.
Plan approval 2026-08-09 = the H6 gate (HV/H2/H4/H5 precedent). H6 ends this pass **partial** —
Halftone cannot close while H3 is open.

The trigger: three unconsumed Callisto memos were sitting untracked in `who/coordination/`, and the
2026-08-07 one **discharges the Bearly P5 evidence dependency** that HR's dispatch contract and H6's
RLHF seam doc were explicitly parked behind. The parked work is now buildable.

## Operator rulings at plan approval

| Decision | Ruling |
|---|---|
| Lane | **H6-offline pass**; H3 + campaign close stay with Luke's lane |
| Print scope | **Include print E2E** — spread compose · `export_spread` wiring · deterministic CMYK · DPI policy |
| Open decision **#3** (`canvas_comic`) | **Reader-only freeze now**; archive after H3; port `ComicReport` only if the scoring loop revives |
| Open decision **#4** (RLHF routing) | **Both sinks with a named boundary** — Canvas owns capture substrate, III owns signal schema; ISS-vs-III resolves for III on signal |

## Scope declaration (Tier 2 — shared-config edits)

**Writes into (single-writer):**
- `what/specs/spec_rlhf_seam.md` (NEW) · `what/specs/spec_canvas_review_surface.md` (§6 amendment) · `what/specs/AGENTS.md`
- `what/docs/comic_authoring_contract.md` (NEW) · `what/docs/canvas_authoring_guidance.md`
- `what/decisions/` — `canvas_comic` disposition record (NEW)
- `what/production/canvas_core/traps/cli.py` · `canvas_core/print.py` · `canvas_core/tests/{test_visual_check_cli,test_print}.py`
- `what/production/comic_render/src/comic_render/compose.py` · `tests/test_compose.py` · `tests/fixtures/mini_issue.canvas`
- `how/federation/federation_index.md`
- `how/campaigns/campaign_canvas_halftone/` — `missions/mission_h6_close.md` (NEW) · master · CLAUDE.md · `missions/artifacts/halftone_dev_lanes.md`
- `who/coordination/` — three inbound memos filed; one reply memo **staged**
- `STATE.md` · this file

**Conflict scan:** `how/sessions/active/` held only `.gitkeep` at session open (peer-verified by
Callisto at their s031). Origin at parity `feda532`, working tree clean but for the three untracked memos.

## Out of scope (recorded, not silently dropped)

- **H3** — no `backends/gemini.py`, no geometry-aspect implementation, no live dispatch, **no spend**.
  Held for Luke's lane. *Flagged:* `GEMINI_API_KEY` is present on this node (Keychain + env, name only) —
  the phase is held by **ruling**, not blocked by credential.
- **Campaign close / final AAR** — impossible while H3 is open.
- Real-pixel evidence: DPI-on-real-renders · `CV-COMIC-STYLE-01` calibration · the HR pilot's second consumer.
- **The operator's HR review pass** — re-verified this session: all six sidecar verdicts still `null`.
- Any code move for `canvas_comic` (record only, per the ruling).
- D3 Rosetta registrar ack (standing, non-blocking).

## Firewall

`what/code/canvas_std/` — zero touches; `git diff --stat` empty at the gate. AST no-diffusion guard
stays green; PIL reached only via `canvas_core.print`. Cross-vault writes: none (Rule 10).

## Objectives

| # | Objective | Status |
|---|-----------|--------|
| O1 | Intake — consume/file the three Callisto memos; stage the reply | 🔵 |
| O2 | RLHF seam spec (Lodestar R4.2 · G6) | 🔵 |
| O3 | `review_dispatch_contract v0` — stub → real contract | 🔵 |
| O4 | Comic-domain visual-check profile (H4 finding #4) | 🔵 |
| O5 | Print E2E — spread compose · CMYK policy · DPI policy | 🔵 |
| O6 | Comic authoring contract (T3′) | 🔵 |
| O7 | Governance close-out (partial H6) | 🔵 |

## Files touched

*(filled at close)*

## SITREP

*(filled at close)*
