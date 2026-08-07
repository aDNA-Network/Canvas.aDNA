---
type: session
session_id: session_stanley_20260807_h4_live_verify_and_gate_items
user: stanley
persona: Mondrian
tier: 1
campaign: campaign_canvas_halftone
mission: mission_h4_vulcan_seam
created: 2026-08-07
updated: 2026-08-07
status: completed
last_edited_by: agent_mondrian
tags: [session, halftone, h4, comfyui, live_verification, agent_confirmed_render, gate_items]
---

# Session: H4 live verification on L1 + working the four gate items

## Intent

Execute the approved recommendation set. **Item 0 first** (the one I proposed and the operator
approved): verify H4 against a *real* ComfyUI on this node — `~/ComfyUI` is a live install with the
exact checkpoint the built-in graph defaults to, so the whole refine seam is testable today with no
Anduril, no Gemini, no spend. Then items 4 → 1 → 2 → 3.

## Scope

- Item 0 — live-verify the four refine paths; fix whatever the live run exposes; regression
- Item 4 — surface the HR review pass; collect + close HR 3/3 if the operator does it
- Item 1 — edit the Vulcan memo with verified facts + the smaller ask; send on GO
- Item 2 — wrapper follow-up #2 recommendation (rides the memo)
- Item 3 — push the batch on GO

## Files touched

- `what/production/canvas_core/comfyforge_adapter.py` — L1 `generation_timeout_s` split from
  `timeout_s` · L2 per-output `filename_prefix` + cache-naming error · L3 upscale-model correction
- `what/production/canvas_core/tests/test_comfyforge_adapter.py` — +5 `TestLiveRunRegressions`
- `what/production/comic_render/README.md` — the flat-seed operational note
- `how/campaigns/campaign_canvas_halftone/missions/mission_h4_vulcan_seam.md` — live-verification section
- `how/campaigns/campaign_canvas_halftone/campaign_canvas_halftone.md` — `executor_tier_default: fable`
- `who/coordination/coord_2026_08_06_mondrian_to_vulcan_comic_panel_refine_ask.md` — rewritten + `sent`
- `who/coordination/coord_2026_08_06_berthier_to_canvas_executor_tier_default.md` — inbound, `actioned`
- `STATE.md` · this session file

**Outside this vault (files-only, zero commits — Rule 10):**
`ComfyUI.aDNA/who/coordination/coord_2026_08_06_mondrian_to_vulcan_comic_panel_refine_ask.md`

## SITREP

**Completed** — all five items.

- **Item 0** (the one I proposed): H4 live-verified on L1 against a real ComfyUI. Three defects found
  that mocks structurally cannot catch — an **inherited** 30s generation ceiling, a result-cache
  collision my own deterministic seed made common, and a guessed upscale-model name. Four paths then
  green *and looked at*, including Vulcan's real `workflow_img2img.json`.
- **Item 1** — Vulcan memo delivered, rewritten around verified facts; decision #2 ruled (don't bundle).
- **Item 2** — the "leave the LoRA runner archived" recommendation rides that memo; his call now.
- **Item 3** — parity push executed.
- **Inbound** — Berthier's `executor_tier_default: fable` applied after auditing their slate read.

**In progress** — nothing.

**Next up** — **H3** (Luke's cloud lane): one live
`--chain "generate:gemini,refine:comfy@0.4/comic_panel_refine"` run closes H3 *and* H4's deferred live
gemini→comfy proof. Then **H6** (authoring contract · print E2E · RLHF seam doc · the comic-domain
visual-check profile question · close).

**Blockers** — none. Awaiting Vulcan's reply (nothing depends on it) and, standing, the D3 registrar ack.

**Still open, unchanged** — **the HR review pass**: all six sidecar verdicts in
`what/artifacts/review_surface_pilot/sidecars/` remain `null`. It is the last HR gate item and the only
thing keeping the collector unexercised on real human verdicts.

**Judgement worth recording** — the first live render passed every automated assertion on a picture of
nothing. Byte counts, dimensions and differs-from-seed are not evidence that an image is *right*; only
looking is. That is the second time in four sessions the agent-confirmed-render doctrine caught what both
rails missed.

## Next Session Prompt

> Open `Canvas.aDNA` as Mondrian; read `STATE.md` → `how/campaigns/campaign_canvas_halftone/`. Halftone has
> **H3** (held for Luke's cloud lane — spend params pre-ruled: Gemini pro-image class · 3 variants/panel ·
> $5 cap · `GEMINI_API_KEY` via the Home broker · geometry-derived aspect to implement in `extract.py`) and
> **H6** (authoring contract · print E2E · RLHF seam doc · `canvas_comic` disposition · AAR/close) left.
> **H4 is done AND live-verified** (2026-08-07) — `refine:comfy` works against a real ComfyUI, so one live
> `generate:gemini,refine:comfy@0.4/comic_panel_refine` run closes H3 and H4's remainder together. Read
> `missions/mission_h4_vulcan_seam.md` §Live verification (three defects mocks can't catch) and §Findings
> #4 (visual-check is not yet a meaningful gate for comic pages — H6 decides: comic-domain profile or
> declared exemption) before touching the bridge. To re-run anything live: start `~/ComfyUI` and set
> `COMIC_RENDER_COMFY_ENDPOINT`; `COMIC_RENDER_COMFY_WORKFLOW_DIR=~/aDNA/ComfyUI.aDNA/what/workflows/base`
> reaches Vulcan's real workflows. Possibly pending: Vulcan's reply on `comic_panel_refine` + the endpoint
> question + wrapper follow-up #2; and **the HR review pass** — check whether
> `what/artifacts/review_surface_pilot/sidecars/*.md` still carry `verdict: null`; if the operator has
> filled them, run `review_collect --approver stanley` and close HR gate 3/3. **HOLD at every phase gate**
> (SO-1); firewall `what/code/canvas_std/` stays diff-0; pushes operator-gated.
