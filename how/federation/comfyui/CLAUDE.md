---
type: federation_wrapper
wrapper_for: ComfyUI.aDNA
created: 2026-08-03
updated: 2026-08-03
last_edited_by: agent_vulcan
mission_origin: ComfyUI seam true-up 2026-08-03 (operator-authorized cross-vault fix; Vulcan-authored, recording memo in who/coordination/) — restores the ex-CanvasForge consumer seam absorbed at the Canvas merge
status: active
tags: [federation, comfyui, consumer_wrapper, canvas, image_generation, lora_training, vdp]
---

# Canvas `comfyui/` — ComfyUI.aDNA Consumer Wrapper

Federation wrapper for **ComfyUI.aDNA** (persona Vulcan; Platform.aDNA · `software_deployment_graph`, consumed via the forge pattern per ADR-039). Canvas.aDNA absorbed CanvasForge's production line (deck · comic · diagram at `what/production/`), and with it the **ComfyUI consumer seam** that CanvasForge held (`comfyforge/` wrapper, old-graph pin `e9b4303`) — but no wrapper carried over at the merge. This wrapper restores that seam against the **re-genesis graph**.

Consumed capabilities (the carried CanvasForge asks):
- **VDP-01/02 render support** — local-inference image generation for visual-DNA production (txt2img · img2img style transfer) feeding comic/deck pipelines
- **LoRA training dispatch** — character-consistency LoRAs for visual-DNA bundles (dispatch-gated: Anduril stack verify at ComfyUI M03 B-leg; L1 does not train — MPS)
- **III generation-trap pack** — review of generated variants before production placement

Wrapper is lightweight: `federation_ref` + local extensions. ComfyUI canonical content (workflows, traps, registry) is **never** copied here — only referenced. Canonical consumption spec: `~/aDNA/Astro.aDNA/what/artifacts/sf_forge_pattern_spec.md`.

## federation_ref

```yaml
federation_ref:
  source_vault: ComfyUI.aDNA
  source_path: ~/aDNA/ComfyUI.aDNA
  version: "0.2.0"                      # re-genesis graph (old-graph 0.1.0 seam: CanvasForge comfyforge/ @ e9b4303, archived)
  version_policy: tracking              # advance pinned_at_commit when Canvas needs new capabilities
  pinned_at_commit: "a8a4356"           # ComfyUI.aDNA HEAD 2026-08-03 (category Platform·SDG applied; M03 gate open)
  pinned_at: 2026-08-03
  # Adjusted 2026-08-06 (Halftone H4 — Vulcan follow-up #1) to ACTUAL Canvas consumption. Canvas
  # consumes ComfyUI as the chain's REFINE stage only; generation is the cloud backend's (ADR-003).
  skills_used:
    - how/skills/skill_iii_visual_triage.md        # generation-trap audit of variants
  skills_referenced:                               # read for context; not a Canvas-side runtime path
    - how/skills/skill_generation_session.md       # text/img → workflow → generation → III review
    - how/skills/skill_lora_training.md            # LoRA TRAINING is Vulcan's + Anduril-gated; Canvas only LOADS a trained LoRA
  workflows_used:
    - what/workflows/base/workflow_img2img.json    # the refine stage's structural reference
    - what/workflows/base/workflow_upscale.json    # roadmap R7 (full-bleed DPI headroom)
    - what/workflows/production/workflow_comic_panel_refine.json
                                                   # ✅ AUTHORED upstream 2026-08-22 (Vulcan's answer memo, collected at source):
                                                   # img2img + inert LoraLoader (strength 0.0 until a TRAINED weight) + RealESRGAN
                                                   # x4plus leg + explicit VAELoader; node convention 3/4/5/7 kept — patch-by-class
                                                   # works unchanged; shape-parity verified against our fixture; denoise 0.4 default.
  workflows_requested: []                          # comic_panel_refine ask (2026-08-06) SATISFIED 2026-08-22
  contexts_used:
    - what/context/iii/comfyforge_generation_traps.yaml   # 9 generation traps — upstream filename (ComfyUI.aDNA-owned)
  adrs_inherited:
    - what/decisions/adr_004_comfyui_as_generation_framework.md
    - what/decisions/adr_005_dual_hardware_dispatch.md
    - what/decisions/adr_006_sdxl_flux_base_models.md
    - what/decisions/adr_007_kohya_lora_training.md
  server_endpoints:
    l1_local: http://localhost:8188      # PRIMARY — Vulcan's 2026-08-22 ruling: L1-first confirmed
    rd_node: pending campaign_rd_forge M-RD1       # opportunistic fast endpoint = adna_rd_l1 <forge-overlay-addr>, NOT Anduril;
                                                   # endpoint string arrives by memo when their deploy lands (office-LAN/mesh reach only)
    # anduril <parked-box-addr>:8188: DROPPED 2026-08-22 — dead Nebula path on a parked box (3090 absent
    # from device tree, recovery unscheduled per operator S167). canvas_core default now l1_local.
    # ⛔ Overlay addresses are held mesh-only, NOT in this public repo (Forgejo.aDNA publication
    # boundary 2026-08-20; ADR-016 D2.4 — a boundary declared by the graph that owns the fact binds
    # every graph that quotes it). Literals live at ComfyUI.aDNA's wrapper + the node's Home.aDNA
    # inventory; resolve them there, never by re-inlining here. Ruling: adr_012.
    override_env: COMIC_RENDER_COMFY_ENDPOINT      # H4: the bridge resolves this, else l1_local
  secrets_dependency: none               # local inference; no API keys
  local_extensions: []
```

## Predecessor-seam provenance (quarry pointers)

- CanvasForge `comfyforge/` wrapper (old seam, archived): `~/aDNA/Archive.aDNA/CanvasForge.aDNA/comfyforge/CLAUDE.md`
- LoRA dispatch runner (quarry copy; live rehoming TBD — candidate `what/production/` tooling): `~/aDNA/Archive.aDNA/CanvasForge.aDNA/how/campaigns/campaign_canvasforge_v1_2/runners/lora_training_dispatch_runner.py`
- VDP-01 S4 AAR (LoRA pre-flight precedent): `~/aDNA/Archive.aDNA/CanvasForge.aDNA/how/campaigns/campaign_canvasforge_v1_2/missions/mission_m_v1_2_f_visual_dna_pilot.aar.md`
- Sibling consumer wrappers: WebForge `~/aDNA/WebForge.aDNA/how/federation/comfyui/CLAUDE.md` (the exemplar) · ZenZachary `~/aDNA/ZenZachary.aDNA/how/federation/comfyui/CLAUDE.md`
