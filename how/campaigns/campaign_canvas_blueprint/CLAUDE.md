# CLAUDE.md — Campaign: Operation Blueprint (`campaign_canvas_blueprint`)

## Campaign Identity

| Field | Value |
|---|---|
| Campaign | `campaign_canvas_blueprint` |
| Owner | stanley |
| Status | 🟢 **active** (chartered 2026-08-22; plan approval = the charter gate) |
| Current Phase | **P0 ✅ · P1 ✅ · P2 ✅ (all complete-with-open-item) · ▶ P2c ✅ (2026-09-07)** — the producer re-gate (`mission_b2c_producer_regate`), added 2026-09-07 as a **dated scope amendment** with plan approval as its gate. **Shipped:** one shared `canvas_core/layout_fit.py` (producers and traps now measure with the same function), a `deck` trap profile, an advisory-trap gating rule, 3 generated example assets, and **13 authored surfaces gating clean per domain profile**. It discharged `mission_b2`'s follow-up (a), which its own AAR sequenced **ahead of** the deferred P2b conversion memos: *offering conversions while our own shelf fails the gate repeats the credibility problem the dogfood just fixed.* ▶ **P2b ✅ (2026-09-07)** — the conversion offers, and the mission that found the defect class was ours. Census **re-derived, both figures wrong**: Operations **10** not 5 (the *gitignored projection* is what fails, not the tracked source, which is 5/5 clean); ScienceStanley **33** not 29 in **three classes**, **9 of them Canvas's own output** from the producer we archived at Halftone. **40 of 41 errors across both vaults are one class** — C-4 missing explicit `toEnd`, the **F-HR-1** Obsidian-re-save signature we diagnosed in our own vault 2026-08-23 and filed as internal housekeeping. Shipped **`canvas_core/conform.py`** (+13 tests): `normalize_edges` clears 40/41 with zero judgement calls; `unresolved_edges` **reports and never repairs** the one real defect (a C-3 dangling edge live in a shipped teaching package, found in 40ms). Memos **#10/#11 delivered**, both vaults read-only and quiescent-probed at act time. ⛔ **The `_reserved` tier of both offers is HELD** — no `authority` value fits a hand-authored canvas, and `canvas_std` accepts a wrong one silently (F-P2b-5). ▶ **NEXT GATE: P3** — HOLD. **b1.5 (finalize the pattern with Rosetta) is still OPEN** — the phase does not advance on their silence; the authority-axis evidence is **held as an artifact, deliberately not dispatched as a fourth unanswered memo**. P3–P5 behind it (P4's build half may run parallel with operator ack; its live chain additionally spend-gated). |
| Persona | Mondrian (Canvas.aDNA) |
| Predecessor | `campaign_canvas_halftone` (comic system; completed 2026-08-22) |

## Quick Start

1. Read this file, then `campaign_canvas_blueprint.md` (master: goal · locked decisions · phases · risks).
2. Read the two charter artifacts: `artifacts/draft_pattern_diagrammatic_context.md` + `what/specs/spec_comfyui_canvas_emission.md`.
3. Check `STATE.md` for the open phase; create the phase's mission at its gate (never pre-spawn past a HOLD).
4. **HOLD at every phase gate** (SO-1). Per-mission AAR (SO-5). Commit/push operator-gated. **P4's live chain is additionally SPEND-gated.**

## Standing Orders (campaign-local)

- **`what/code/canvas_std/` is untouched unless a ratified LIP says otherwise** — verify `git diff --stat -- what/code/canvas_std/` empty at every gate. Default posture: 2.3.0 already suffices for diagrammatic context (Emacs is the existence proof).
- **Offer, never write.** Doctrine goes to Rosetta as a staged draft; conversions go to Operations/SS as offers with worked examples. Zero writes into other vaults (Rule 10).
- **Every shipped canvas** passes `canvas-std validate --level adna_native` + the agent-confirmed render (Amendment 1), and obeys `context_canvas_topology_graphs.md` v1.1 (angle-aware crossings; placement over routing).
- **Verify "unanswered" at source** before treating any 2026-08-04 memo as refused — the fleet's memo delivery was itself broken (Estafette).
- **Carried from Halftone**: H4 live chain (spend-gated) · HR second consumer (= the P4 board) · `ImagenWiring` panel-path deprecation · `comic_book_design/` ruling (P5).

## Key Files

| File | Purpose |
|---|---|
| `campaign_canvas_blueprint.md` | Master/charter |
| `artifacts/draft_pattern_diagrammatic_context.md` | The P1 doctrine draft (staged → Rosetta, memo #9) |
| `../../..​/what/specs/spec_comfyui_canvas_emission.md` | The P4 seam contract (memo #14 → Vulcan; feeds ComfyUI's restart charter) |
| `../campaign_canvas_halftone/missions/artifacts/halftone_campaign_aar_rollup.md` | Predecessor AAR — the five findings that outlive Halftone |
