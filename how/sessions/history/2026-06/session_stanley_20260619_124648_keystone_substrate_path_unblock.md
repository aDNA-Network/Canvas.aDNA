---
type: session
created: 2026-06-19
updated: 2026-06-19
last_edited_by: agent_stanley
tags: [session, keystone, coordination, pt_p5, hearthstone]
session_id: session_stanley_20260619_124648_keystone_substrate_path_unblock
user: stanley
started: 2026-06-19T12:46:48
status: completed
intent: "Answer Hestia's substrate-path memo (coord 2026-06-18) — decide the canonical canvas_core path/import/env-var for the PT P5 relocation — to unblock Operation Hearthstone P3. Record as Canvas ADR-004 (proposed); fold the 2 parked Keystone follow-ups into the P5 contract. Decision-only: no code moves, E3→E4 stays HELD."
tier: 2
files_modified: [STATE.md]
files_created: [what/decisions/adr_004_production_code_layout.md, who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply.md]
cross_vault_writes: ["Home.aDNA/who/coordination/coord_2026_06_19_inbound_from_mondrian_canvas_substrate_path_reply.md (additive courtesy copy only — NO Home ledger edits; left UNCOMMITTED for Hestia)"]
completed: 2026-06-19
---

## Scope Declaration (Tier 2)

- **Writes (Canvas.aDNA):** `what/decisions/adr_004_production_code_layout.md` (new) · `who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply.md` (new) · `STATE.md` (edit) · this session file.
- **Cross-vault write (Home.aDNA):** one additive courtesy memo in `who/coordination/` so Hestia's session finds the reply. **No edits to Home ledgers** (Rule 4 — Mondrian does not write Home's deferred-items / §C; the memo *asks* Hestia to).
- **Out of scope (guardrails):** does NOT open Keystone E4 (E3→E4 human gate HELD); does NOT execute the PT P5 relocation (no code moves); does NOT edit `Archive.aDNA/CanvasForge.aDNA/` (the 2 follow-ups are *scheduled* into adr_004, not executed in-archive); does NOT self-ratify adr_004 (status: proposed → operator countersigns).
- **Conflict scan:** `how/sessions/active/` clean (only `.gitkeep`); `git status` clean, 2 ahead of origin (E3.4 + pt09 batch pending operator push); no competing session.

## Activity Log

- 12:46 — Session started. Startup checklist: `git pull` (already up to date); reviewed STATE (HELD at E3→E4), CLAUDE.md, the inbound Hestia memo + Home deferred-items dependency.
- 12:47 — Plan approved (operator): path = `what/production/canvas_core/`; import = keep `canvas_core`; env-var = `CANVAS_CORE_HOME`; fold both parked follow-ups into adr_004 as P5 items.
- 12:48 — Wrote reply memo to Hestia (the unblock) — 5 actionable values + the `adna-canvas-std` resolution rule + a suggested generator snippet + timing/staging guidance.
- 12:49 — Wrote `adr_004_production_code_layout.md` (status: proposed) — path/import/env-var decision + co-location invariant + P5 execution checklist folding FU1/FU2; `relates: adr_001`.
- 12:50 — Updated STATE.md (pt09 note → adr_004 resolution; follow-ups → contracted P5 items; pushes; next-steps). Cross-filed the courtesy reply into Home (additive; left uncommitted).
- 12:51 — Scope verified: Canvas batch clean (no Archive/CanvasForge edits); Home shows a *pre-existing* uncommitted `topology.canvas` change that is **not mine** — leaving Home un-committed.

## SITREP

**Completed:**
- **Hestia's substrate-path memo (coord 2026-06-18) ANSWERED → Hearthstone P3 unblocked.** Reply filed
  (`who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply.md`) with the 5 values for her
  one-touch repoint: path `what/production/canvas_core/`; import unchanged; env `CANVAS_CORE_HOME` (+`CANVASFORGE_CODE`
  alias); `source_module` → `what/production/canvas_core`; and the **`adna-canvas-std`-must-be-importable** rule that
  closes the silent-non-render trap on fresh nodes.
- **Canvas.aDNA ADR-004** (`what/decisions/adr_004_production_code_layout.md`, **status: proposed**) — the binding PT P5
  relocation contract; resolves the pt09-mandated E4 code-layout reconciliation (no E4 gate opened); folds the 2 parked
  follow-ups (FU1 canvas/-routing as production governance; FU2 round-trip dedup at relocation) into the P5 checklist.
- **STATE.md** updated (E3→E4 HOLD intact; follow-ups now contracted P5 items; pushes batch noted).
- Courtesy cross-file dropped in Home's coordination inbox (additive).

**In progress:** none.

**Next up:**
- **Operator:** ratify ADR-004 (proposed → ratified + `signed_by`).
- **Hestia (Home-local):** repoint the exemplar per the reply; commit her own courtesy memo + her pre-existing
  `topology.canvas`; update Home deferred-items (PT-P5→Hearthstone-P3 answered) + add the §C env-var alias row.
- **Keystone:** still HELD at E3→E4 (human gate). The 2 follow-ups + the physical relocation execute at PT P5.

**Blockers:** none. `#needs-human`: operator ratification of ADR-004 + the E3→E4 gate remain human decisions.

**Files touched:**
- Created: `what/decisions/adr_004_production_code_layout.md` · `who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply.md` · this session file · (Home, uncommitted) `Home.aDNA/who/coordination/coord_2026_06_19_inbound_from_mondrian_canvas_substrate_path_reply.md`.
- Modified: `STATE.md`.
- **Not touched:** anything under `Archive.aDNA/CanvasForge.aDNA/`; Home ledgers; Home `topology.canvas` (pre-existing, not mine).

## Next Session Prompt

Canvas.aDNA (Mondrian) is **HELD at the Keystone E3→E4 human gate**. The 2026-06-19 session answered Hestia's
substrate-path memo and minted **ADR-004 (proposed)** fixing the PT P5 production-code layout: `canvas_core` →
`Canvas.aDNA/what/production/canvas_core/` (import name kept; env-var `CANVAS_CORE_HOME` with `CANVASFORGE_CODE` as a
deprecated alias; `canvas_core` depends on installed `adna-canvas-std`). The two former E3.4 parked follow-ups
(canvas/-routing Standing Order; round-trip-function dedup → `canvas_std`) are now contracted as PT P5 items in
ADR-004's execution checklist, not executed in the archive. **Do not open E4 and do not execute the P5 relocation
without the operator.** Pending: operator ratification of ADR-004; the Canvas batch (adr_004 + reply + STATE + session)
is committed locally and **pending push per the operator batch convention** (joins the E3.4 + pt09 batch — check
`@{u}..HEAD` authorship first). Hestia owns the Home-side repoint + her two local ledger updates per the reply memo.
