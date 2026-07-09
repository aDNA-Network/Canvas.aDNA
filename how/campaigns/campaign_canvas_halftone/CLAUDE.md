# CLAUDE.md — Campaign: Operation Halftone (`campaign_canvas_halftone`)

## Campaign Identity

| Field | Value |
|-------|-------|
| Campaign | `campaign_canvas_halftone` |
| Owner | stanley |
| Status | 🟢 **active** (chartered 2026-07-09 from the operator-approved comic-system review) |
| Current Phase | **H0+H1 COMPLETE; HOLDING at H1→H2.** Charter + review artifacts ✅ · producer hardening ✅ (prompt_layers · validations · RLHF E2E · suite 87→100; producers 236; firewall clean) · governance rail 1 ✅ (adr_008 adoption + prompt contract). **Next: H2 — `comic_render` bridge, offline.** HOLD (SO-1). |
| Persona | Mondrian (Canvas.aDNA) |
| Predecessor | `campaign_canvas_beacon` (publish-hardening; completed 2026-07-02) |

## Quick Start

1. Read this file (auto-loaded in the campaign dir).
2. Read `campaign_canvas_halftone.md` — the master/charter (goal, locked decisions, phases H0–H6, firewall discipline).
3. Read the **source of truth**: `missions/artifacts/halftone_gap_register.md` (G1–G6 evidence) + `halftone_roadmap.md` (tier detail + bridge architecture).
4. Check `STATE.md` for the open phase; run that phase's mission (create a session in `how/sessions/active/`).
5. **HOLD at every phase gate** (SO-1). Per-mission AAR (SO-5). Commit/push operator-gated (Git-Ops §3). **H3 render dispatch is additionally SPEND-gated.**

## Key Files

| File | Purpose |
|------|---------|
| `campaign_canvas_halftone.md` | Master/charter — phases H0–H6, locked decisions, firewall, missions index |
| `missions/artifacts/halftone_gap_register.md` | The review's G1–G6 gap register with file:line evidence |
| `missions/artifacts/halftone_roadmap.md` | Tier detail: bridge architecture, manifest contract, backend interop, risks |
| `missions/mission_h1_producer_hardening.md` | H0+H1 mission (charter · prompt_layers · validation · ADR port · prompt contract) |

## Standing Orders (campaign-local)

- **"Canvas dispatches, it does not diffuse."** The render bridge (`what/production/comic_render/`, H2+) may import HTTP
  dispatch clients; it must NEVER import a diffusion/render engine (torch/diffusers/local pipelines) — AST-guarded. Pixels,
  models, and workflows belong to ComfyUI.aDNA (Vulcan).
- **`what/code/canvas_std/` is untouched this entire campaign.** Verify `git diff --stat -- what/code/canvas_std/` is empty
  at every gate. Comic work lives in `what/production/` + docs/decisions.
- **Reuse the existing substrate**: `canvas_core/image_generation.py` (`ImageClient` protocol — do NOT invent a new backend
  abstraction) · `comfyforge_adapter.py` (working ComfyUI HTTP client) · `print.py` (PrintExporter) · `rlhf/` (Schema-A
  SelectionRecords only).
- **Write-back never mutates**: rendering produces `issue.rendered.canvas` (a NEW file); the input canvas is immutable;
  topology never changes (sync_hash stays byte-identical); stage-5 revalidation is a hard gate.
- **Hybrid backend is a chain, not a switch**: manifest `render_chain` = ordered stages (generate → optional refine);
  Gemini output seeds ComfyUI img2img. Cloud path primary; nothing blocks on Vulcan's ack.
- **Cross-vault = coord memos or read-only** (Rule 10): ComfyUI (H4 memo, pending_ack) · VisualDNA/SS (read-only bundles;
  H6 contract announcement). Never write into another vault.
- **Phase gates are human gates** (SO-1); H3 adds a **spend gate** (model tier · variants/panel · budget cap · credential
  via the Home.aDNA broker — tokens never transit the conversation).

## Context Loading

| Subtopic | When |
|----------|------|
| `halftone_gap_register.md` + `halftone_roadmap.md` | Always — gap IDs + architecture |
| `what/production/comic_generator/` (README · model.py · panels.py · prompt.py · style.py) | H1/H2 — the producer being hardened + the qualities the bridge extracts |
| `what/production/canvas_core/{image_generation,comfyforge_adapter,print}.py` | H2–H4 — the reused substrate |
| `what/docs/comic_prompt_contract.md` (after H1) | H2+ — the prompt contract the manifest + Vulcan memo bind to |
| `ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml` | H5 — the empirical VisualDNA anchor |
| `Archive.aDNA/CanvasForge.aDNA/what/decisions/` (read-only quarry) | H1 — ADR port sources |

## Delegation Notes

Chartered 2026-07-09 after a three-track read-only review (code · governance · workflow) + a design pass. The
operator's three answers (full program · hybrid interoperating backend · T3 contract-only) are the ratification;
the build plan is approved. Keep phases **sequential + gated** (H5 may run parallel after H2 with operator ack);
create each phase's mission only when its phase opens — never pre-spawn past a HOLD.
