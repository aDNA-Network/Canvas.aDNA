---
type: decision
adr_id: "008"
title: "Comic render doctrine — adoption + re-anchor of the CanvasForge image-generation decisions (provider strategy · dual-prompt · prompt-construction) for Operation Halftone"
status: ratified
created: 2026-07-09
updated: 2026-07-09
last_edited_by: agent_mondrian
signed_by: Stanley (operator) — Halftone plan approval 2026-07-09 (decisions locked 2026-07-07)
ported_from: |
  Archive.aDNA/CanvasForge.aDNA/what/decisions/adr_003_image_generation_provider_strategy.md (accepted 2026-04-21) +
  adr_005_dual_prompt_protocol.md (accepted 2026-05-03; §D5 amendment 2026-05-26) +
  adr_008_prompt_construction_contract.md (ratified 2026-05-26). Archive originals reader-only (SO-6) — the full
  historical record, incl. mission machinery this adoption deliberately does not carry.
supersedes:
superseded_by:
phase: halftone-h1
tags: [adr, canvas, comic, render, image-generation, gemini, imagen, comfyui, dual-prompt, prompt-construction, rlhf, halftone, ported]
---

# ADR-008: Comic Render Doctrine (adopted CanvasForge decisions, re-anchored)

## Status

**Ratified** — 2026-07-09, by the operator's approval of the Operation Halftone plan (backend decision locked
2026-07-07). This ADR **adopts into live Canvas.aDNA governance** the operative decisions of three CanvasForge-era
ADRs that were stranded in the archive when CanvasForge merged into Canvas (pt09) — re-anchored onto the code as it
exists today (`what/production/comic_generator/` + `canvas_core/`), with the stale mission machinery explicitly
retired. One consolidated adoption rather than three verbatim ports: the archive originals remain the full
historical record; this document is what the Halftone render bridge (H2–H4) cites.

## Adopted decisions (operative)

### §1 — Provider strategy: cloud generates, ComfyUI refines *(from CF ADR-003, upgraded by the 2026-07-07 hybrid decision)*

- **Gemini/Imagen is the production GENERATE default** for comic panel rendering (CF ADR-003 §D1, substrate-wide).
- **ComfyUI is the style-transfer / REFINE engine** (CF ADR-003 §D2) — **upgraded by the operator (2026-07-07)**
  from a post-hoc training exercise to a **first-class pipeline stage**: the render manifest's `render_chain` may
  chain `generate` (cloud) → `refine` (ComfyUI img2img seeded by the generate output; LoRA-when-trained; upscale).
  Interop is a chain, not a backend switch.
- **Substrate-neutral request shape** (CF ADR-003 §D3): backends plug in behind the `ImageClient` protocol
  (`what/production/canvas_core/image_generation.py`); provider enums stay adapter-internal. The Halftone bridge
  extends with an optional `RefineClient` (init-image input) rather than breaking `ImageClient`.
- **Corpus accumulation is a first-class side-effect** (CF ADR-003 §D4): every render run captures selection
  records — **Schema-A `SelectionRecord`s only** (`canvas_core/rlhf/selection.py`), preserving the transfer/RLHF
  corpus regardless of the §4 seam disposition.

### §2 — Dual-prompt contract *(from CF ADR-005)*

- A panel's image directive is up to **three segments**: **PART 1** text (the 6-layer assembly) · **PART 2** spatial
  layout (Mermaid `comic_panel_layout` grammar: TOP/MID/BOT regions, depth/framing, relations) · **PART 3**
  compositional intent (optional free-text anchor; the V2 wrapper; CF ADR-005 §D5).
- **Per-application spatial adapters; substrate carries only the data contract.** The live comic adapter is
  `comic_generator/panel_layout.py` (ported from the quarry's `mermaid_layout.py`); `ImagePrompt` is the data type.
  A future producer (diagram, sequence) ships its own adapter; nothing central changes.
- *Retired with this adoption:* the lattice `config.strategy:` enum + the v1.1 lattice-orchestrator enforcement
  layer (CF ADR-005 §D2/§D4) — never built; the Atelier producers replaced lattice-level pre-flight with
  data-driven inputs + `context_object.refs`. If a lattice orchestrator ever revives, it re-opens here.

### §3 — Prompt-construction contract *(from CF ADR-008)*

- **The 6-layer assembly is the canonical prompt-construction pattern** (CF ADR-008 §D1 Option C), now living in
  `comic_generator/prompt.py` as pure, data-driven functions (Atelier scope D5): 1 style · 2 characters · 3 scene ·
  4 camera/composition · 5 lighting · 6 negative. Standalone runners MAY compose their own shape; substrate tuning
  applies only to the 6-layer path.
- **The four RLHF back-flow surfaces** (CF ADR-008 §D2 + addenda) all carry into the live producer:
  **B1** register-keyed hint dicts (`rlhf_hints.py` + the `rlhf_character_hints`/`rlhf_camera_nuances` kwargs —
  threaded end-to-end through `build_comic` at Halftone H1) · **B2** character-registry content override (the
  `character_bible`/`character_registry` path; VisualDNA composes here at H5) · the **panel-type nuance**
  sub-dimension (`PANEL_TYPE_TEMPLATES["nuances"]` + `Panel.compositional_nuance`) · the **wrapper-level intent**
  (`ImagePrompt.compositional_intent` → PART 3).
- **Pick-frequency is the RLHF methodology** (CF ADR-008 §D6): selection-pick-frequency over `pick_reason` text;
  per-axis VR gradients stay deferred. Pattern derivation strips the hash suffix (register-equivalence classes,
  CF ADR-008 §D7 / CF ADR-007 §3).
- *Retired with this adoption:* the `ContextPack` 5-file pre-flight gate (dropped at Atelier A2 — instance data is
  threaded as arguments; declarative provenance rides `context_object.refs`); `register_compliance_score` stays
  ratified-as-deferred.

## New bindings (Halftone, 2026-07-09)

- **"Canvas dispatches, it does not diffuse."** The render bridge (`what/production/comic_render/`, H2+) may import
  HTTP dispatch clients; it MUST NOT import a diffusion/render engine (AST-guarded). Pixels, models, and workflows
  are ComfyUI.aDNA's (Vulcan's); the cross-vault ask rides a coord memo (H4), never a silent write.
- **`qualities.prompt_layers` is the per-channel prompt contract** (landed H1): the structured
  `{style, characters, scene, camera, lighting, negative}` breakdown beside the assembled `image_prompt` — the
  **`negative` channel** feeds backends with a distinct negative input (ComfyUI CLIP encode) without unpicking the
  assembled text; the negative suffix is instance data (`ComicInput.negative_suffix`), unblocking photorealistic
  registers. Contract detail: `what/docs/comic_prompt_contract.md`.
- **Write-back never mutates**: rendering produces a NEW `.canvas` (topology unchanged ⇒ sync_hash byte-identical);
  the YAML source + producer remain authoritative; rendered canvases are derived artifacts.

## Provenance & supersession map

| Quarry decision | Disposition here |
|---|---|
| CF ADR-003 §D1 Gemini substrate-default · §D2 ComfyForge style-transfer · §D3 neutral request · §D4 corpus accumulation | **Adopted** (§1; §D2 upgraded to the first-class refine stage) |
| CF ADR-003 budget classes / cost ceilings | Adopted in spirit → the manifest `budget_cap` + H3 spend gate |
| CF ADR-005 §D1 lattice `inputs:` + §D2 orchestrator + §D4 `config.strategy` | **Retired** (never-built enforcement layer; replaced by data-driven inputs) |
| CF ADR-005 §D3 per-app spatial adapters + §D5 PART-3 intent | **Adopted** (§2) |
| CF ADR-008 §D1 six-layer canonical (Option C) · §D2 four back-flow surfaces · §D6 pick-frequency · §D7 strip-hash | **Adopted** (§3) |
| CF ADR-008 ContextPack pre-flight · register_compliance_score | **Retired / stays deferred** |
| CF ADR-004/006/007 (visual-QA HITL · visual-style RLHF loop · bridge schema) | **Referenced, not adopted here** — the RLHF-seam doc (H6, Lodestar R4.2) is their disposition vehicle |

## Consequences

- The Halftone bridge has a single live authority cite for backend order, the dual-prompt shape, and the prompt
  channels — no spelunking in the archive.
- ComfyUI's role is finally unambiguous: refine engine in the chain, owner of pixels/workflows, non-blocking.
- The retired machinery (lattice orchestrator, ContextPack gate) is explicitly closed, not silently forgotten.

## Related

`what/docs/comic_prompt_contract.md` (the handable prompt contract) · `how/campaigns/campaign_canvas_halftone/`
(charter + gap register + roadmap) · `adr_004_production_code_layout.md` (two-shelf firewall) ·
`Archive.aDNA/CanvasForge.aDNA/what/decisions/adr_00{3,5,8}*.md` (full originals, reader-only).
