---
type: consumer_pattern_doc
doc_id: videoforge_consumer_pattern_v0.1
schema_version: "0.1.0"
contract_for: VideoForge.aDNA (Iris)
contract_against: visual_dna v0.2 (with v0.2.2 amendments §5.7 + §5.8 + §5.9)
status: published_runtime_pending
authored_at: "2026-05-25"
authored_by: agent_stanley
authored_in: "CanvasForge.aDNA campaign_canvasforge_v1_2 mission_m_v1_2_f_visual_dna_pilot S5"
re_merge_rationale: "lattice-labs/who/coordination/coord_2026_04_16_forge_split.md"
tags: [consumer_pattern, videoforge, visual_dna, v0_1, character_consistent_frames, identity_preservation, smoke_test_spec, defer_with_spec, hermes, iris, canvasforge, pilot_s5]
---

# VideoForge `visual_dna` Consumer Pattern — v0.1

> Load-bearing deliverable of CanvasForge.aDNA Visual-DNA Pilot Sub-Campaign **M-V1-2-F-VDP-01 Session 5**. Specifies the contract between CanvasForge visual-DNA producers and VideoForge as a character-consistent-video consumer. Published 2026-05-25 in defer-with-spec posture — VideoForge runtime not yet live for character work (Phase 4 active); contract awaits Phase 5 implementation.

## §1 Purpose + scope

Establish the consumer pattern by which VideoForge (persona Iris) reads a visual-DNA character bundle and composes a multi-frame video clip with **character identity preserved across all frames**. Eliminates the per-clip "character bible" overhead — the visual-DNA bundle IS the character bible.

### What this doc is

- The **consumer-side contract** for VideoForge against the v0.2 visual-DNA schema (`spec_v0.2.md`), with the v0.2.2 amendments §5.7 (hex hygiene), §5.8 (framing-lock directive), and §5.9 (label hygiene) applied to per-frame video generation.
- A **defer-with-spec deliverable** — VideoForge's character-consistent rendering is not yet implemented (Phase 4 agent-council scaffolding active; consumer integration is Phase 5 work). This doc is the contract VideoForge implements at Phase 5.
- A **smoke-test spec** — §5 defines a concrete first-target (3-second SS-character head-turn clip) for VideoForge to render against the contract as the Phase 5 integration milestone success criterion.

### What this doc is NOT

- Not a rendering-engine spec (VideoForge owns the backend selection — Veo / Wan / other image-conditioned-video runtime; this doc is backend-agnostic by construction).
- Not a comprehensive video-production pattern (audio / score / voice-over / multi-shot editing are VideoForge-side; this doc is character-visual-identity-preservation across frames).
- Not an exhaustive multi-entity composition spec (S5 scope is single-character cameo; multi-character + location-backdrop video composition deferred to S6+; see §5 deferred items).
- Not a VideoForge mission-planning document (VideoForge's Iris agent owns Phase 5 mission topology; this doc is consumer-side contract input).

### Scope of this v0.1 release

- 1 entity type: character (location-backdrop video composition deferred to S6+ Pattern 1 video adaptation).
- 1 cameo class: single-character N-frame clip (3 seconds at 24-30 fps = 72-90 frames).
- 1 animation directive locked as canonical smoke-test target: **head-turn** (Stanley left → center → right; emphasizes facial-feature invariant hold under rotation).
- Backend-agnostic: contract works for any image-conditioned-video runtime VideoForge elects.

---

## §2 Data model — visual-DNA fields consumed by VideoForge

VideoForge reads the following fields from a visual-DNA character bundle (using `stanley.yaml` as the canonical example). Cross-reference: `spec_v0.2.md §5` consumer-compat matrix row for VideoForge.

### §2.1 Required fields

| Field path | Type | Role in video composition |
|---|---|---|
| `text_prompt.portrait_subset` | string (~1500 chars) | Primary character-DNA prompt; baseline for every frame. The compressed variant carries identity-bearing tokens (skin tone, hair, costume, charm tells) without environmental clutter — appropriate for cameo cuts where the character is the subject. **NOT** the full `text_prompt.full_prompt_path` content (~5000 chars; carries environmental + cinematic detail that biases the model away from frame-to-frame consistency). |
| `reference_image_set.portraits[*].path` | list of file paths | Frame-conditioning anchors. The 5 canonical portrait images (anchor + 4 variants) supply the model with concrete identity references the per-frame generator conditions on. Critical for maintaining identity across N frames — text-only generation drifts; reference-image-conditioned generation stays close to the anchor. |
| `composition_templates.<name>` | nested dict | Per-frame framing directive. For cameo clips, `portrait_icon` (1:1 tight crop) or `portrait_closeup` (head + shoulders) are the canonical choices; `wide_cinematic_establishing` (16:9) is environmental and applies to S6+ scene-backdrop video composition, not S5 cameo scope. |
| `invariants.required[*]` | list of `{id, pattern, anti_pattern, provenance}` | Pre-flight prompt validation + per-frame gate. Pre-flight: each invariant's `pattern` (e.g., for Stanley: `purple turtleneck`, `auburn hair`, `STANLEY badge`) must be present in the assembled per-frame prompt. Per-frame gate: sample N frames; verify each invariant's visual signature holds across the sequence (charm_signal tells visible; anti_tells absent). |
| `charm_signal.tells[*]` + `charm_signal.anti_tells[*]` | list of strings | Per-frame VQA criteria. `tells` (e.g., "warm half-smile", "soft-focus eye crinkles") inform expected character expression behavior across frames; `anti_tells` (e.g., "cold expression", "smug smirk") are excluded behaviors. Frame gate scores frames against tells/anti-tells inclusion/exclusion. |

### §2.2 Optional fields

| Field path | Type | Role when present |
|---|---|---|
| `lora_refs[*]` | list of `{path, model_family, trigger_word, recommended_weight, training_data_manifest, version, status}` | Optional SDXL LoRA augmentation. If VideoForge's chosen backend supports SDXL LoRA loading (e.g., Wan + ComfyUI workflow extension), the bundle's LoRA refs become consumable for tighter character fidelity. Per `lora_refs[*]`: load `.safetensors` at `path`, inject `trigger_word` into the per-frame prompt prefix, weight at `recommended_weight` (typically 0.6). If backend does NOT support LoRA, this block is informational and VideoForge falls back to text + reference-image conditioning. |
| `palette_anchors.portrait_mode.*` | nested dict | Optional palette pinning for backends that accept palette declarations. If the backend supports color-grading directives, the bundle's `portrait_mode` palette (skin / hair / costume hex values) can pin per-frame color consistency. Most image-conditioned-video runtimes do NOT take palette directives directly; the palette implicitly carries via reference_image_set. |

### §2.3 NOT consumed by VideoForge at S5 cameo scope

- `text_prompt.cinematic_subset` — environmental + scene context; for S6+ scene-backdrop video composition (Pattern 1 video adaptation), not S5 cameo.
- `text_prompt.full_prompt_path` (full ~5000 char) — too dense; biases per-frame generation toward portrait-not-frame consistency.
- `reference_image_set.scenes[*]` — environmental compositions; appropriate for location-DNA backdrop work, not character cameo.
- `reference_image_set.discarded[*]` — vars rejected during canon election (e.g., Stanley vars 5-6 comic-panel + whiteboard per Stanley's `discarded` block); these are NEGATIVE references and MUST NOT condition any frame.
- `consumer_compat.videoforge` — VideoForge's own status field; produced by CanvasForge (the consumer-side wrapper updates this); not consumed by VideoForge runtime.
- `federation_ref` — framework-level metadata; not consumed by runtime.

---

## §3 Frame composition + identity preservation protocol

VideoForge's per-frame generator runs once per frame (or once per keyframe in a keyframe-interpolation pipeline). Identity preservation across N frames depends on three disciplines, all carried from the visual-DNA bundle into every per-frame prompt assembly.

### §3.1 Baseline + reference anchor pattern

For each frame in the sequence:

1. **Baseline prompt** = `text_prompt.portrait_subset` (compressed character-DNA carrier, ~1500 chars). Constant across all frames in a cameo.
2. **Reference-image conditioning** = `reference_image_set.portraits[*].path` (5 canonical anchors). Some image-conditioned-video runtimes accept a single primary reference + N auxiliary references; this contract recommends the canonical `anchor` (entry where `canonical: true`) as primary + the 4 variants as auxiliary references.
3. **Per-frame composition directive** = `composition_templates.portrait_icon` (cameo standard). Constant across all frames in a cameo of fixed framing; varies per keyframe in a framing-shift cameo (rare; S5 cameo scope is fixed-framing).
4. **Per-frame animation token** = the per-frame variation from the animation directive (§4.2 below). E.g., for head-turn: frame 0 = "facing camera"; frame 36 = "looking forward"; frame 72 = "head turned to camera-right looking off-frame". The animation token is appended to the baseline + composition directive.

The composed per-frame prompt structure mirrors `composition_rules.md §6.2`:

```
[UNION INVARIANT HEADER]            <- character display name (e.g., "Science Stanley") appears ONLY here
[ANIMATION DIRECTIVE]                <- e.g., "Frame N of N: <animation token>"
[CHARACTER]                          <- portrait_subset from text_prompt
[FRAMING]                            <- composition_templates.portrait_icon directive
[PALETTE]                            <- palette_anchors.portrait_mode hex block (declarative, not content)
[INVARIANTS]                         <- invariants.required[*].patterns (role descriptors, NOT identity tokens)
[CHARM]                              <- charm_signal.tells (expected expression behavior)
Avoid: <anti_tells> + <discarded variant traits> + in-frame text/labels + portrait framing drift
```

### §3.2 Framing-lock discipline (cross-frame extension of composition_rules.md §5.8)

The v0.2.2 §5.8 amendment addressed static-image framing drift (wide compositions rendering as portraits despite explicit wide directives). For video, the equivalent drift is **cross-frame framing instability** — frame 0 renders portrait-tight, frame 36 renders wider, frame 72 renders portrait-tight-again. This violates cameo coherence.

**Cross-frame framing-lock discipline**:

1. The composition directive (e.g., `portrait_icon` for cameo) is declared ONCE at the per-frame prompt's `[FRAMING]` block and held constant across all frames in a sequence.
2. The per-frame `[FRAMING]` block SHOULD include the explicit subject-area-ratio directive from §5.8: "Subject area: ~80% (head + shoulders fill frame); subject centered". For wide-cameo variants, the appropriate `portrait_closeup` template directive applies the analog ratio.
3. The `Avoid:` block of every per-frame prompt SHOULD append: "Avoid: framing drift across frames, subject-area-ratio inconsistency, sudden zoom-in / zoom-out".
4. **Per-frame gate validation**: sample frames 0%, 33%, 66%, 100% of the timeline; verify subject occupies ~same frame proportion in each (visual estimation acceptable; precise pixel measurement at follow-up validation session).

### §3.3 Label hygiene cross-frame (extension of composition_rules.md §5.9)

§5.9 addressed static-image identity-token leakage (e.g., "STANLEY" rendered as whiteboard text in multi-entity scenes). For video, the equivalent risk is **per-frame label rendering** — each frame independently risks rendering the character's display name as in-frame text if not disciplined.

**Cross-frame label hygiene discipline**:

1. Character display name (e.g., "Science Stanley") appears ONLY in the per-frame prompt's `[UNION INVARIANT HEADER]` block.
2. Descriptive `[CHARACTER]` + `[INVARIANTS]` + `[CHARM]` blocks use role-descriptor language only (e.g., "the man with auburn hair", "warm half-smile" — sourced from `charm_signal.tells`).
3. The `Avoid:` block of every per-frame prompt SHOULD include: "Avoid: in-frame text, name banners, name badges (unless canon — see invariants.has_in_frame_name_badge)".
4. **Canon-badge invariants honored per-character**: if the character bundle's `invariants` declares an in-frame name badge (Stanley's `STANLEY` badge per stanley.yaml § text_prompt.portrait_subset), the per-frame prompt explicitly authorizes that badge in the `[INVARIANTS]` block. Characters not declaring a canon badge inherit the §5.9 default-disallow.

### §3.4 Charm-signal continuity

The character's `charm_signal.tells[*]` (e.g., for Stanley: warm half-smile, soft-focus eye crinkles, slight forward lean of curiosity) should be **present in spirit across the sequence**, not slavishly identical per-frame. For a head-turn animation, the smile may visibly fade at the extreme rotation frame (frame 72; head turned away) and return at the center frame — this is expected and consistent with naturalistic motion. The frame gate (§5.3) scores frames against tells inclusion, not identical persistence; small smile drift is acceptable, smug-smirk anti-tell appearance is NOT acceptable.

### §3.5 Anti-tell exclusion + discarded-variant exclusion

The `Avoid:` block of every per-frame prompt MUST include:

- All entries from `charm_signal.anti_tells[*]` (e.g., "cold expression", "smug smirk", "intense glare").
- Identity-bearing traits from `reference_image_set.discarded[*]` (e.g., for Stanley: "comic-panel rendering", "whiteboard background scene" — vars 5-6 discarded 2026-05-23 per Stanley feedback).

This exclusion is the key defense against frame drift toward the discarded canon.

---

## §4 Input / output contract

### §4.1 Input schema (CanvasForge → VideoForge)

VideoForge's consumer integration receives the following input shape (proposed; final shape elected by VideoForge agent at Phase 5):

```yaml
videoforge_visual_dna_cameo_request:
  character_dna_bundle_path: str         # absolute path to character visual-DNA bundle (e.g., ~/aDNA/ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml)
  composition_template_name: str         # which template to apply (portrait_icon | portrait_closeup | other)
  frame_count: int                       # total frames in sequence (72 for 3-sec at 24fps; 90 for 3-sec at 30fps)
  frame_rate_fps: int                    # 24 or 30 typically
  animation_directive:                   # enum + per-frame variation source
    directive_id: str                    # e.g., "head_turn_left_to_right" | "smile_progression" | "engage_disengage_gaze"
    keyframes:                           # list of {frame_index, animation_token}
      - { frame_index: 0, animation_token: "facing camera, head straight" }
      - { frame_index: 36, animation_token: "head turning, eyes following camera-right" }
      - { frame_index: 72, animation_token: "head turned to camera-right, looking off-frame" }
    interpolation: str                   # "keyframe_interpolation" | "per_frame_generation"
  lora_refs_consumed:                    # which lora_refs entries (by version) to load; empty list = no LoRA augmentation
    - { version: "0.1", weight: 0.6 }    # references lora_refs entries by version
  output_format: str                     # "mp4" | "png_sequence" | "mp4_with_png_sequence_sidecar"
  output_path: str                       # where the result lands
  validation:
    per_frame_gate_enabled: bool         # true = run iii_aggregate scoring on sampled frames
    invariant_preflight: bool            # true = string-match invariants.required[*].patterns in assembled prompts before render
```

### §4.2 Output schema (VideoForge → CanvasForge)

```yaml
videoforge_visual_dna_cameo_result:
  request_echo:                          # input echo for provenance
    character_dna_bundle_path: str
    composition_template_name: str
    frame_count: int
    animation_directive_id: str
  rendered_outputs:
    primary_output_path: str             # MP4 (or PNG sequence dir if png_sequence)
    sidecar_outputs:                     # optional supplementary outputs
      png_sequence_dir: str | null
      metadata_json: str                 # path to per-frame validation results
  metadata_summary:
    backend_used: str                    # which backend rendered (Veo | Wan | other)
    lora_refs_loaded: list               # which LoRA refs were actually used (may differ from request if backend incompatible)
    total_render_time_sec: int
    estimated_cost_usd: float
  validation_results:
    invariant_preflight_status: "pass" | "fail" | "skipped"
    preflight_failures: list             # if any invariant missing from assembled prompts
    per_frame_gate_results:              # list of per-sampled-frame results
      - { frame_index: 0, iii_aggregate: float, invariants_held: list, anti_tells_observed: list }
      - { frame_index: 24, iii_aggregate: float, invariants_held: list, anti_tells_observed: list }
      - { frame_index: 48, iii_aggregate: float, invariants_held: list, anti_tells_observed: list }
      - { frame_index: 71, iii_aggregate: float, invariants_held: list, anti_tells_observed: list }
    overall_pass: bool                   # true if all per-frame gates pass thresholds (see §5)
```

### §4.3 Cross-vault path-resolution requirement

The input schema's `character_dna_bundle_path` and `lora_refs[*].path` resolve cross-vault — the character bundle lives at `ScienceStanley.aDNA/what/visual_dna/...` while VideoForge's runtime lives at `VideoForge.aDNA/videoforge/...`. VideoForge's runtime requires cross-vault read access for both the character bundle YAML AND the reference image files it points at (the bundle's `reference_image_set.portraits[*].path` entries are vault-relative; the runtime resolves them via the vault root path passed at session init).

---

## §5 Smoke test spec + validation plan

### §5.1 Canonical smoke-test target — Stanley head-turn cameo

Locked at S5 plan-mode (operator AskUserQuestion 2026-05-25): the canonical smoke-test target for VideoForge Phase 5 integration is a **3-second Stanley head-turn cameo** (left → center → right).

| Parameter | Value | Rationale |
|---|---|---|
| Character | Science Stanley (`stanley.yaml`) | Canonical anchor; 11 invariants well-validated by VDP-01 S2 + S3; iii_aggregate baselines established. |
| Duration | 3 seconds | Mission charter S5 baseline; long enough to validate cross-frame identity hold, short enough to constrain test cost + iteration time. |
| Frame rate | 24 fps (preferred) or 30 fps (acceptable) | Standard cinema (24) or web video (30); both acceptable; VideoForge elects per backend default. |
| Total frames | 72 (24 fps) or 90 (30 fps) | Derives from duration × fps. |
| Composition template | `portrait_icon` (1:1 close cameo) | Cameo standard; tight head-and-shoulders crop maximizes per-frame identity-signal density (face fills frame; clearer invariant gate). |
| Animation directive | `head_turn_left_to_right` | Keyframes: frame 0 = "facing camera, head straight"; frame ⌊N/2⌋ = "head turning, eyes following camera-right"; frame N-1 = "head turned to camera-right, looking off-frame". Emphasizes facial-feature invariant hold under rotation — the most rigorous identity-preservation test class. |
| Interpolation | Per-backend default | Backend election; some image-conditioned-video runtimes interpolate from keyframes (recommended for cost), others generate per-frame (recommended for quality). |
| LoRA augmentation | OPTIONAL | If VideoForge backend supports SDXL LoRA loading, consume `stanley.yaml § lora_refs[*]` at weight 0.6 (per S4 ComfyForge pre-flight recommendation); otherwise text + reference-image conditioning only. |
| Output | MP4 + per-frame PNG sequence sidecar + metadata JSON | MP4 = primary delivery; PNG sequence + metadata = validation surface. |

### §5.2 Pre-flight validation

Before any frames render, the runtime validates:

1. **Bundle parse**: `stanley.yaml` parses as valid v0.2 YAML.
2. **Required-block presence**: 11 required-block headers per spec §3 (`id`, `display_name`, `entity_type`, `text_prompt`, `reference_image_set`, `palette_anchors`, `composition_templates`, `invariants`, `charm_signal`, `consumer_compat`, `federation_ref`).
3. **Per-frame prompt invariant string-match**: each of the 11 required invariants' `pattern` field (e.g., `auburn hair`, `purple turtleneck`, `STANLEY badge`) appears in the assembled per-frame prompt. If ANY invariant missing → pre-flight fail; render aborts.
4. **Reference image existence**: all paths in `reference_image_set.portraits[*].path` resolve to existing readable files.
5. **LoRA path existence** (if `lora_refs_consumed` non-empty): each `lora_refs[*].path` resolves to existing `.safetensors` file.

### §5.3 Per-frame gate validation (cross-frame iii_aggregate thresholds)

After render, sample 4 frames across the timeline (0%, 33%, 66%, 100% of frame count) and run iii_aggregate scoring per frame. The per-frame gate uses the following thresholds:

| Sampled frame | Frame position | iii_aggregate threshold | Rationale |
|---|---|---|---|
| Anchor frame | 0% (frame 0) | ≥ 85 | First frame is the "anchor-most"; closest to reference images; should score near static-image variants (var_1 = 89; anchor = 90+). |
| Early-mid frame | 33% (frame ~24 of 72) | ≥ 80 | Acceptable interpolation drift; mid-rotation frames have less reference-image proximity. |
| Late-mid frame | 66% (frame ~48 of 72) | ≥ 80 | Same threshold as 33%; symmetric across the rotation. |
| Exit frame | 100% (frame N-1) | ≥ 82 | Final frame should re-stabilize per character canon; slightly tighter than mid-rotation but looser than anchor. |

**Overall pass criterion**: all 4 sampled frames meet threshold AND no `charm_signal.anti_tells[*]` observed in any sampled frame AND no `reference_image_set.discarded[*]` traits observed in any sampled frame.

### §5.4 Cross-frame invariant union check

In addition to per-frame iii_aggregate, the gate runs a cross-frame invariant union check:

- For each invariant in `stanley.yaml § invariants.required[*]`, verify the invariant's visual signature is present in ≥ 3 of 4 sampled frames (≥75% frame coverage).
- Invariants permitted partial-coverage in cameo (motion-occluded body features may dip below threshold during extreme rotation; e.g., `STANLEY badge` may not be visible at frame 100 when head is turned away).
- Charm signals: ≥ 2 of 4 frames must show at least one `charm_signal.tells[*]` (warm expression visible in at least half the cameo).

### §5.5 Deferred items (out of S5 cameo scope)

- **Multi-character video composition** — Pattern 2 (character + character) + Pattern 4 (character + character + location) deferred to S6+ pilot AAR sweep or post-pilot mission. The composition_rules.md cross-frame discipline (§3.2 + §3.3) extends cleanly; the smoke-test class becomes "Stanley + Charlie two-shot conversation" rather than single-character cameo.
- **Location-backdrop video composition** — Pattern 1 (character + location) video adaptation deferred to S6+. The lab_interior location bundle is ready (VDP-01 S3 closed; iii_aggregate 86-93 across references); video adaptation requires VideoForge to consume location-DNA `palette_anchors.cinematic_mode` + `composition_templates.wide_cinematic_establishing` + `atmosphere_signal` on top of character DNA. This is the natural Phase 5.5 / S6 follow-up scope.
- **Audio + score + voice-over** — out-of-pilot. The Visual-DNA pilot is visual identity preservation; audio surfaces are VideoForge-side concerns not part of the visual-DNA bundle contract.
- **Multi-shot editing** — cuts + transitions + montage are VideoForge's own editor agent concern (per `adr_002_agent_council_topology.md` Editor agent); single-cameo smoke test sits before any multi-shot work.
- **Backend selection rationale** — Veo vs Wan vs other image-conditioned-video runtimes is Iris's election at Phase 5 mission planning; this contract is backend-agnostic.

---

## §6 Re-merge rationale

The VideoForge consumer pattern is load-bearing for the canvas-as-message substrate (Hermes core) — every cameo clip is a canvas being carried from intent (character cameo for narrative beat) to delivery (rendered MP4) via VideoForge as the moving-image courier. The visual-DNA bundle is the structured message; VideoForge is the courier that preserves the message's integrity (character identity) across the multi-frame journey. The 2026-04-16 canvas-substrate re-merge (`lattice-labs/who/coordination/coord_2026_04_16_forge_split.md`) established that canvas is the substrate, not just a static-image side product — and video is canvas-in-motion, the natural extension of canvas-as-message across time.

The pilot's 5-consumer matrix (Gemini · ComfyForge · VideoForge · social content · metaverse) validates that the canvas-message-substrate scales across all visual production surfaces. VideoForge is the temporal extension; this consumer pattern doc is the contract that formalizes the substrate's reach into moving-image work without absorbing VideoForge's runtime into the substrate itself.

---

## References

### Within CanvasForge.aDNA

- Visual-DNA schema spec v0.2: `~/aDNA/Canvas.aDNA/what/docs/visual_dna_schema/spec_v0.2.md` (§5 consumer-compat matrix row for VideoForge; §6 versioning + federation_ref protocol)
- Composition rules: `~/aDNA/Canvas.aDNA/what/docs/visual_dna_schema/composition_rules.md` (§5.8 framing-lock + §5.9 label hygiene — cross-frame discipline source)
- VideoForge consumer wrapper: `~/aDNA/CanvasForge.aDNA/videoforge/CLAUDE.md` (federation_ref + local_extensions; entry pointer for VideoForge agent)
- Sibling consumer wrapper (S4 precedent): `~/aDNA/CanvasForge.aDNA/comfyforge/CLAUDE.md` (ComfyForge LoRA training; populates the `lora_refs[*]` block this VideoForge contract optionally consumes)
- Pilot mission: `~/aDNA/CanvasForge.aDNA/how/campaigns/campaign_canvasforge_v1_2/missions/mission_m_v1_2_f_visual_dna_pilot.md` (S5 deliverable lineage)

### Within ScienceStanley.aDNA (consumer bundle examples)

- Stanley character bundle (S5 primary target): `~/aDNA/ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml`
- Lab interior location bundle (S6+ target): `~/aDNA/ScienceStanley.aDNA/what/visual_dna/locations/lab_interior/lab_interior.yaml`
- Charlie character bundle (future S5-equivalent target post-VDP-02): `~/aDNA/ScienceStanley.aDNA/what/visual_dna/characters/charlie/charlie.yaml`

### Within VideoForge.aDNA (consumer-side integration surfaces)

- VideoForge governance: `~/aDNA/VideoForge.aDNA/CLAUDE.md` (persona Iris)
- VideoForge ADR 002 (agent council topology): `~/aDNA/VideoForge.aDNA/what/decisions/adr_002_agent_council_topology.md` (storyboarder + critic + curator are primary inbound surfaces for this contract)
- VideoForge ADR 003 (cross-graph entry contract): `~/aDNA/VideoForge.aDNA/what/decisions/adr_003_cross_graph_entry_contract.md` (the canonical entry contract; this consumer pattern doc is one such inbound)
- VideoForge ADR 005 (context learning + RLHF): `~/aDNA/VideoForge.aDNA/what/decisions/adr_005_context_learning_rlhf.md` (iii_aggregate scoring surface for the per-frame gate)
- VideoForge ADR 008 (operator-retarget + dogfood + testbed reframe): `~/aDNA/VideoForge.aDNA/what/decisions/adr_008_operator_retarget_dogfood_testbed.md` (the M_4_00 reframe; visual-DNA integration aligns with the dogfood pivot)
- VideoForge code (current Imagen wrapper; future integration target): `~/aDNA/VideoForge.aDNA/videoforge/lvf/graphics/image_gen.py`
- VideoForge code (storyboarder agent IO; primary inbound surface): `~/aDNA/VideoForge.aDNA/videoforge/lvf/schemas/agent_storyboarder_io.py`
- Inbound coord memo (2026-05-23 from VDP-01 S1): `~/aDNA/VideoForge.aDNA/who/coordination/coord_2026_05_23_visualdna_video_consumer.md`
- Outbound coord memo (S5 close; pattern publication notice + second nudge): `~/aDNA/VideoForge.aDNA/who/coordination/coord_2026_05_25_vdp_s5_consumer_pattern_publication.md`

### Cross-vault framework partner

- VisualDNA.aDNA stub: `~/aDNA/VisualDNA.aDNA/CLAUDE.md` (persona Pygmalion; activates post-pilot S6 AAR; will host the canonical VideoForge-consumer wrapper template absorbed from this v0.1 doc)

### Re-merge rationale (load-bearing per CR7+SO7)

- `~/aDNA/lattice-labs/who/coordination/coord_2026_04_16_forge_split.md` — the 2026-04-16 CanvasForge re-merge that established the canvas-substrate this pattern federates with.
