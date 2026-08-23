# CLAUDE.md — Campaign: Operation Blueprint (`campaign_canvas_blueprint`)

## Campaign Identity

| Field | Value |
|---|---|
| Campaign | `campaign_canvas_blueprint` |
| Owner | stanley |
| Status | 🟢 **active** (chartered 2026-08-22; plan approval = the charter gate) |
| Current Phase | **P0 ✅ (charter + the two charter artifacts + memos #9/#14). ▶ NEXT GATE: P1 (doctrine)** — HOLD for the operator. P2–P5 sequential behind it (P4's build half may run parallel after P1 with operator ack; its live chain additionally spend-gated). |
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
- **Every shipped canvas** passes `canvas-std validate --level adna-native` + the agent-confirmed render (Amendment 1), and obeys `context_canvas_topology_graphs.md` v1.1 (angle-aware crossings; placement over routing).
- **Verify "unanswered" at source** before treating any 2026-08-04 memo as refused — the fleet's memo delivery was itself broken (Estafette).
- **Carried from Halftone**: H4 live chain (spend-gated) · HR second consumer (= the P4 board) · `ImagenWiring` panel-path deprecation · `comic_book_design/` ruling (P5).

## Key Files

| File | Purpose |
|---|---|
| `campaign_canvas_blueprint.md` | Master/charter |
| `artifacts/draft_pattern_diagrammatic_context.md` | The P1 doctrine draft (staged → Rosetta, memo #9) |
| `../../..​/what/specs/spec_comfyui_canvas_emission.md` | The P4 seam contract (memo #14 → Vulcan; feeds ComfyUI's restart charter) |
| `../campaign_canvas_halftone/missions/artifacts/halftone_campaign_aar_rollup.md` | Predecessor AAR — the five findings that outlive Halftone |
