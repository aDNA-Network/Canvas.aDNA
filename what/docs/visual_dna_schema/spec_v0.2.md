---
type: spec
spec_id: visual_dna_v0.2
status: reference_copy_superseded_by_visualdna_v1_0
superseded_by: ~/aDNA/VisualDNA.aDNA/what/artifacts/visual_dna_schema/spec_v1.0.md
superseded_at: 2026-05-28 (VisualDNA.aDNA P1 schema_lock mission close per Stanley sign-off via ExitPlanMode please-read-the-claude-md-jazzy-summit)
schema_version: "0.2.0"
predecessor: "visual_dna v0.1 (implicit; pre-landed in ScienceStanley.aDNA SS character bundle 2026-05-23)"
authored_at: "2026-05-24"
authored_by: agent_stanley
authored_in: "CanvasForge.aDNA campaign_canvasforge_v1_2 mission_m_v1_2_f_visual_dna_pilot S1"
federation_target: "VisualDNA.aDNA (v1.0 GA canonical as of 2026-05-28)"
empirical_anchor: "ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml"
re_merge_rationale: "lattice-labs/who/coordination/coord_2026_04_16_forge_split.md"
tags: [spec, visual_dna, schema, v0_2, pilot_deliverable, framework_seed, hermes, canvasforge, pillar_f, character_dna, location_dna, object_dna, consumer_compat, lora_refs, composition_rules, reference_copy, superseded, historical_anchor]
---

> **REFERENCE-COPY NOTICE (2026-05-28)** — This file is a historical reference-copy.
> The canonical schema spec is now `~/aDNA/VisualDNA.aDNA/what/artifacts/visual_dna_schema/spec_v1.0.md`
> at framework version v1.0.0 (GA tagged at P1 schema_lock close 2026-05-28).
> v0.2 + v0.2.1 + v0.2.2 amendments are absorbed into v1.0; this file remains for historical reference.
> Consumer wrappers re-pin from `~0.1 → ~1.0` at framework P5 close (4 vaults: CanvasForge / ScienceStanley / ComfyForge / VideoForge).
> See `~/aDNA/VisualDNA.aDNA/who/coordination/coord_2026_05_28_p1_schema_lock_closed.md` for migration coord.

# `visual_dna` Schema — v0.2

> Primary deliverable of CanvasForge.aDNA Visual-DNA Pilot Sub-Campaign **M-V1-2-F-VDP-01 Session 1**. Defines the YAML contract that lets any entity (character / location / object) in any vault carry a portable visual-DNA bundle consumable by all 5 target systems (Gemini · ComfyForge · VideoForge · social content · metaverse).

## §1 Purpose + scope

Establish a **portable, consumer-agnostic, federation-aware** schema for capturing the visual identity of an entity (character, location, object). Each entity carries one YAML bundle. Agents in any vault consume the bundle to generate canon-consistent imagery without re-discovering canon each time.

### What this spec is

- The **schema contract** between visual-DNA *producers* (a vault that owns the entity) and visual-DNA *consumers* (Gemini, ComfyForge LoRAs, VideoForge, social content automation, metaverse rendering).
- A **pattern proof** for the future `VisualDNA.aDNA` Framework.aDNA (stub bootstrapped 2026-05-23; Pygmalion persona). This spec is the seed; the full framework lands post-pilot at S6 AAR.
- **Empirically grounded** in the pre-landed ScienceStanley character bundle (`stanley.yaml`) — the schema must validate against that bundle without lossy projection. See §4.

### What this spec is NOT

- Not a rendering engine (consumers handle rendering)
- Not an asset store (reference image binaries live where they live; the schema points at them)
- Not a LoRA training pipeline (ComfyForge owns training; this schema captures the *reference* to a trained LoRA)
- Not opinionated about prompt-construction beyond the `text_prompt` field (CanvasForge substrate's 6-layer assembly + ADR-005 dual-prompt protocol handle production prompt construction; the bundle supplies the *content*)

### Scope of this v0.2 release

- 3 entity types: character · location · object
- 5 consumer integrations: gemini · comfyforge · videoforge · social_content · metaverse
- 4 NEW v0.2 fields over the implicit v0.1: `lora_refs`, `consumer_compat`, `entity_type`, `status`
- Schema validates against the SS character bundle (pre-landed 2026-05-23) and against the location_dna + object_dna templates (S3 + future-session deliverables)

---

## §2 Pattern overview

**Visual-DNA-per-entity** treats the visual identity of an entity as first-class data, on par with the canvas substrate's existing typed primitives. Three claims:

1. **Identity is portable.** Once an entity's visual DNA is captured, *any* canvas application in *any* vault can render it consistently — without re-discovering canon, re-prompt-engineering, or relying on author memory.
2. **Identity composes.** Two or more visual DNAs combine to produce novel scenes (character + location → environmental shot; character + character → two-shot; character + object → activity shot). See `composition_rules.md`.
3. **Identity federates.** The same bundle is consumed by Gemini text-to-image, ComfyForge LoRA-augmented gen, VideoForge frame composition, social content automation, and metaverse 3D/avatar/pixel-art derivative pipelines. One bundle, N consumers.

The pilot's slogan: **"Any context graph becomes its own cartoon show by adding a visual descriptive layer to its objects."**

### Why now

The CanvasForge v1.2 Pillar F substrate (style-search loop + 100-cycle persona optimization + canonical anchor + III multi-voice review) produced the SS character canonical anchor on 2026-05-23. That anchor was the proof-of-concept: a single text_prompt + reference_image_set + palette_anchors + composition_templates + invariants + charm_signal can capture an entity's identity precisely enough that re-renders feel canonically consistent. This spec promotes that proof to a reusable pattern.

---

## §3 v0.2 schema

The schema is a single root key `visual_dna:` containing the following fields.

### §3.1 Top-level fields

```yaml
visual_dna:
  id: <string>                  # REQUIRED. Unique within vault. e.g., "ss_character_stanley"
  display_name: <string>        # REQUIRED. Human-readable. e.g., "Science Stanley (Stanley Bishop)"
  entity_type: <enum>           # REQUIRED v0.2. One of: character | location | object
  version: <semver>             # REQUIRED. Bundle version. e.g., "0.1.0"
  status: <enum>                # REQUIRED v0.2. One of:
                                #   draft | active_canonical_anchor | deprecated | archived
  established_at: <date>        # REQUIRED. Date the bundle reached active status. ISO 8601 date.
  source_pilot: <string>        # OPTIONAL. Pilot/mission that produced the bundle. Free-form.
```

### §3.2 `text_prompt` block

The canonical generation prompt. May be inline OR pointed at via a separate file.

```yaml
  text_prompt:
    description: <string>       # OPTIONAL. Author note: how to use this prompt.
    full_prompt_path: <path>    # OPTIONAL. Path to the full prompt file (relative to bundle root).
    full_prompt_inline: <text>  # OPTIONAL. Alternative to full_prompt_path; inline full prompt.
    portrait_subset: <text>     # OPTIONAL but RECOMMENDED for characters.
                                # Portrait-mode-only extract; 1500-2500 chars target band per
                                # Compactness Critic; production should prefer this over full_prompt
                                # when generating portrait variants.
    cinematic_subset: <text>    # OPTIONAL. Cinematic-mode-only extract for locations + scenes.
    notes: <text>               # OPTIONAL. Author guidance (e.g., "extract portrait subset for icons").
```

At minimum, one of `full_prompt_path` / `full_prompt_inline` / `portrait_subset` MUST be present.

### §3.3 `reference_image_set` block

Curated reference images grouped by purpose. Each image declares provenance + III score + canonical flag.

```yaml
  reference_image_set:
    portraits:                  # OPTIONAL. List of portrait-mode references (typically 1:1 or 4:5).
      - path: <relative-path>
        label: <string>
        provenance: <string>    # How it was generated. e.g., "v3 optimization run iter 50 variant_1; MD5 ..."
        method: <string>        # OPTIONAL alternative to provenance. e.g., "Imagen 4 Ultra text-to-image; 1:1"
        stanley_election: <string>      # OPTIONAL. Operator-pick provenance.
        iii_aggregate: <float>          # OPTIONAL. III aggregate VR score (0-100).
        canonical: <bool>               # OPTIONAL. True iff this is the canonical anchor.
    scenes:                     # OPTIONAL. List of scene/environmental references (wide/cinematic).
      - { path, label, method, iii_aggregate, ... }
    expressions:                # OPTIONAL. List of expression-variant references for characters.
      - { path, label, method, iii_aggregate, ... }
    establishing:               # OPTIONAL (locations only). List of wide-establishing-shot references.
      - { ... }
    detail:                     # OPTIONAL (locations, objects). List of detail-shot references.
      - { ... }
    discarded:                  # OPTIONAL but RECOMMENDED. Block documenting rejected references.
      reason: <string>          # Why these were rejected.
      items:                    # List of paths with brief rejection rationale.
        - <path-or-description>
```

Categories under reference_image_set are open-set: characters typically have {portraits, scenes, expressions}; locations have {establishing, detail}; objects have {detail, contextual} — but producers may add additional categories as the entity warrants.

### §3.4 `palette_anchors` block

Hex colors keyed by rendering mode. Multiple modes supported.

```yaml
  palette_anchors:
    portrait_mode:              # OPTIONAL. Hex map for portrait renders.
      background: "#76428a"
      skin_highlight: "#fee1bf"
      hair_highlight: "#c97c5c"
      # ... arbitrary author-defined keys (no schema constraint on key names)
    cinematic_mode:             # OPTIONAL. Hex map for cinematic / environmental renders.
      desk_wood_dominant: "#614133"
      # ...
      lighting_directive: <string>   # OPTIONAL prose. e.g., "warm-amber desk-lamp + cool blue monitor glow"
    # ... additional modes (e.g., comic_panel_mode, social_card_mode) — author-defined keys.
```

Key names within a mode are author-defined (no schema enum lock); consumers walk the map and substitute into prompt-construction templates.

### §3.5 `composition_templates` block

Named compositional templates with aspect + framing guidance.

```yaml
  composition_templates:
    <template_name>:            # e.g., portrait_icon, wide_cinematic_establishing
      aspect: <string>          # e.g., "1:1", "16:9", "4:3"
      framing: <string>         # Prose framing directive.
      background: <string>      # OPTIONAL.
      lighting: <string>        # OPTIONAL.
      use_cases: [<string>, ...] # OPTIONAL. List of canonical use cases.
```

Template names are author-defined; producers add templates as the entity warrants. Recommended templates for each entity_type:

- **character**: portrait_icon, portrait_closeup, wide_cinematic_establishing, plus optional comic_panel
- **location**: wide_establishing, detail_shot, contextual (character-inhabited)
- **object**: detail_isolated, contextual (in-use by character)

### §3.6 `invariants` block

String-match + visual-canon checks that gate canon-fidelity.

```yaml
  invariants:
    method: <string>            # e.g., "string-match on prompt + visual-canon check"
    required:
      - name: <string>          # Identifier for this invariant. e.g., "round_glasses"
        patterns: [<string>, ...]   # Strings that MUST appear in the prompt.
        anti_patterns: [<string>, ...]  # OPTIONAL. Strings that MUST NOT appear.
        provenance: <string>    # OPTIONAL. Where this invariant came from.
                                # e.g., "canon-locked R1" or "Stanley-Likeness Aligner v3"
```

Invariants are author-curated; the production gate runner enforces presence/absence at prompt-construction time and (optionally) at rendered-image VQA time.

### §3.7 `charm_signal` block (character only; OPTIONAL for other types)

The non-visual quality that makes the entity feel like itself.

```yaml
  charm_signal:
    description: <text>
    tells: [<string>, ...]      # Qualities that ARE the charm.
    anti_tells: [<string>, ...] # Qualities that BREAK the charm.
```

Used by VR-axis voices (notably Charm Calibrator persona) when scoring rendered output for character bundles. For non-character entities, omit or repurpose (e.g., a location's "atmosphere_signal").

### §3.8 `lora_refs` block (NEW v0.2)

Pointers to trained LoRAs (ComfyForge or other LoRA-producing pipelines) for this entity.

```yaml
  lora_refs:
    # OPTION A: empty placeholder (populated at a later session)
    placeholder: "pilot_S4_will_populate"
    # OPTION B: list of trained LoRAs
    - path: "ComfyForge.aDNA/what/loras/ss_character_v0.1.safetensors"
      model_family: <enum>      # e.g., "sdxl", "sd15", "flux"
      trigger_word: <string>    # Token that activates the LoRA. e.g., "scistanley"
      recommended_weight: <float>  # Recommended LoRA strength. e.g., 0.6
      training_data_manifest: <path>  # Path to the training-data manifest file.
      trained_at: <timestamp>
      version: <semver>
      notes: <string>           # OPTIONAL.
```

Either form is valid. Producers commit a `placeholder` block when no LoRA exists yet (e.g., between pilot S1 schema design and pilot S4 ComfyForge integration); consumers detect placeholder and fall back to text-only generation.

### §3.9 `consumer_compat` block (NEW v0.2)

Per-consumer compatibility + validation status. One entry per supported consumer.

```yaml
  consumer_compat:
    gemini:
      runtime: <string>         # e.g., "CanvasForge.aDNA canonical via latlab.mcp.image.server.GeminiImageClient"
      models: [<string>, ...]   # Models this consumer uses.
      validation: <enum>        # PENDING | VALIDATED | NOT_APPLICABLE
      validated_at: <date>      # OPTIONAL.
      notes: <string>           # OPTIONAL.
    comfyforge:
      runtime: <string>
      training_datasets: [<string>, ...]
      validation: <enum>
    videoforge:
      runtime: <string>
      consumer_pattern: <string>
      validation: <enum>
    social_content:
      runtime: <string>
      consumer_pattern: <string>
      validation: <enum>
    metaverse:
      runtime: <string>
      consumer_pattern: <string>
      validation: <enum>
```

Each consumer block is OPTIONAL but RECOMMENDED — entries with `validation: NOT_APPLICABLE` allow producers to declare scope explicitly (e.g., a location-DNA bundle marks `comfyforge: NOT_APPLICABLE` if no location LoRA pipeline exists).

### §3.10 `federation_ref` + `re_merge_rationale`

```yaml
  federation_ref:
    framework: <string>         # e.g., "VisualDNA.aDNA"
    version: <semver-range>     # e.g., "~0.1"
    pilot_source: <string>      # OPTIONAL. Originating mission / campaign.

  re_merge_rationale: <path>    # REQUIRED per CR7+SO7.
                                # e.g., "lattice-labs/who/coordination/coord_2026_04_16_forge_split.md"
```

Per CR7+SO7 the re-merge rationale citation is mandatory on every visual_dna bundle.

---

## §4 Worked examples

### §4.1 Character example — Science Stanley (condensed from pre-landed bundle)

This is the **empirical anchor** for the v0.2 schema. The full bundle at `ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml` validates against this spec.

```yaml
visual_dna:
  id: ss_character_stanley
  display_name: "Science Stanley (Stanley Bishop)"
  entity_type: character
  version: "0.1.0"
  status: active_canonical_anchor
  established_at: "2026-05-23"
  source_pilot: "CanvasForge.aDNA M-V1-2-F-01 + M-V1-2-F-VDP-01"

  text_prompt:
    full_prompt_path: "prompt.md"
    portrait_subset: |
      16-bit pixel art (SNES-era); Studio Ghibli warmth; soft cel-shading with
      gradient transitions on skin and ambient light; deliberate pixel-grid;
      dark line-work outlines (#1f1414). Science Stanley: early-30s; oval-narrow
      face with defined jawline; clean-shaven; strong brow with open forehead;
      spiky warm-brown hair (auburn highlights #c97c5c, shadow #742950); bright
      warm-blue eyes with engaged direct gaze; slight asymmetric smile; round
      blue-framed glasses; white lab coat; purple turtleneck (#9d7cd8); STANLEY
      name badge at chest; head-and-shoulders bust; 3/4 turn; eyes meet viewer;
      solid medium-purple background (#76428a).

  reference_image_set:
    portraits:
      - path: "references/anchor_iconic_portrait.png"
        label: "Canonical anchor (iconic head-and-shoulders portrait)"
        provenance: "v3 optimization run iter 50 variant_1; MD5 17de16b72150e2cdddf64a55c1b0c08d"
        iii_aggregate: 91.0
        canonical: true
      - { path: "references/var_1_portrait_closeup.png", iii_aggregate: 88.0, ... }
    scenes:
      - { path: "references/var_2_wide_cinematic.png", iii_aggregate: 88.0, ... }
    expressions:
      - { path: "references/var_3_expression_warm_laughing.png", iii_aggregate: 88.0, ... }
      - { path: "references/var_4_expression_focused.png", iii_aggregate: 87.0, ... }
    discarded:
      reason: "Per Stanley feedback 2026-05-23 22:00 via canonical_anchor ISS: diverged substantially from canonical style"
      items:
        - "anchor_var_5_comic_panel_ready.png — divergent"
        - "anchor_var_6_at_whiteboard_explaining.png — divergent"

  palette_anchors:
    portrait_mode:
      background: "#76428a"
      skin_highlight: "#fee1bf"
      hair_highlight: "#c97c5c"
      turtleneck: "#9d7cd8"
    cinematic_mode:
      desk_wood_dominant: "#614133"
      monitor_glow_cool: "#495556"
      lighting_directive: "warm-amber desk-lamp + cool-blue monitor glow"

  composition_templates:
    portrait_icon:
      aspect: "1:1"
      framing: "head-and-shoulders bust; 3/4 turn; eyes meet viewer; gentle slight smile"
      background: "solid medium-purple #76428a; no clutter"
      use_cases: ["avatar", "icon", "badge", "social profile"]
    wide_cinematic_establishing:
      aspect: "16:9"
      framing: "wide environmental; character at desk; foreground anchor objects"
      lighting: "warm desk-lamp + cool monitor glow + dim ambient room shadow"
      use_cases: ["hero illustration", "deck cover", "blog header"]

  invariants:
    method: "string-match on prompt + visual-canon check"
    required:
      - name: "round_glasses"
        patterns: ["round glasses", "round circular blue", "blue-framed glasses"]
        anti_patterns: ["square glasses", "rectangular frames"]
        provenance: "canon-locked R1"
      - name: "spiky_brown_hair_auburn"
        patterns: ["spiky brown hair", "auburn highlights"]
        anti_patterns: ["smooth hair", "long flowing hair", "blond hair"]
        provenance: "canon-locked R1"
      - name: "warm_blue_eyes_engaged_gaze"
        patterns: ["bright warm-blue eyes", "engaged direct gaze"]
        provenance: "Stanley-Likeness Aligner v3"
      # ... full 11 invariants in the source bundle

  charm_signal:
    description: "Stanley's warm-mentor charm; engaged-not-performing"
    tells: ["warm presenter energy", "approachable confidence", "slight playful spark in eyes"]
    anti_tells: ["aloof / cold", "stoic-authority", "theater-smile"]

  lora_refs:
    placeholder: "pilot_S4_will_populate"

  consumer_compat:
    gemini:
      runtime: "CanvasForge.aDNA canonical via latlab.mcp.image.server.GeminiImageClient"
      models: ["imagen-4-ultra", "gemini-2.5-flash-image"]
      validation: VALIDATED
      validated_at: "2026-05-23"
    comfyforge:
      runtime: "ComfyForge.aDNA local SDXL with LoRA"
      training_datasets: ["dataset_ss_pixel_v1", "dataset_ss_ghibli_v1"]
      validation: PENDING
    videoforge: { runtime: "VideoForge.aDNA (Iris)", validation: PENDING }
    social_content: { runtime: "Python stub (pilot S6)", validation: PENDING }
    metaverse: { runtime: "ScienceStanley metaverse (TBD)", validation: PENDING }

  federation_ref:
    framework: "VisualDNA.aDNA"
    version: "~0.1"
    pilot_source: "CanvasForge.aDNA M-V1-2-F-VDP-01"

  re_merge_rationale: "lattice-labs/who/coordination/coord_2026_04_16_forge_split.md"
```

**Schema-validation status: VALID.** The pre-landed `stanley.yaml` matches every required v0.2 field, plus the optional `discarded` sub-block of `reference_image_set` (recommended pattern; SS bundle is the source of this convention). The two NEW v0.2 fields are present: `lora_refs` populated as a placeholder (will be replaced at pilot S4 ComfyForge integration), and `consumer_compat` populated with full 5-consumer entries (Gemini validated; rest PENDING per pilot session sequence). Outbound coord memo to ScienceStanley.aDNA at `who/coordination/coord_2026_05_24_visual_dna_schema_validation.md` confirms validation outcome.

### §4.2 Location example — SS lab interior (sketch; S3 deliverable)

The location_dna pattern. Source material: cinematic-mode prompt fragments from the SS character canonical anchor + `palette_anchors.cinematic_mode` block + Var 2 (wide cinematic 16:9) reference image.

```yaml
visual_dna:
  id: ss_location_lab_interior
  display_name: "Science Stanley's Lab Interior"
  entity_type: location
  version: "0.1.0"
  status: draft               # populated at pilot S3
  established_at: "<S3-close-date>"
  source_pilot: "CanvasForge.aDNA M-V1-2-F-VDP-01 S3"

  text_prompt:
    cinematic_subset: |
      Inhabited night-lit lab/office; dark wood furniture with lived-in lab clutter;
      warm-amber desk surface (foreground) with anchor objects (mug with steam,
      notebook, framed photo); cool blue monitor glow modeling midground;
      glass-walled clean lab visible through deep window behind (background
      atmosphere; soft DOF blur; faint dust motes in lamp beam). Warm-cool dual
      lighting palette for depth.

  reference_image_set:
    establishing:
      - path: "references/wide_establishing.png"
        label: "Wide 16:9 establishing shot of lab interior"
        method: "Imagen 4 Ultra text-to-image (S3)"
    detail:
      - path: "references/desk_corner.png"
      - path: "references/whiteboard_corner.png"
      - path: "references/window_corner.png"

  palette_anchors:
    cinematic_mode:
      desk_wood_dominant: "#614133"
      desk_wood_shadow: "#452c25"
      cream_cloth_paper: "#ad9580"
      monitor_glow_cool: "#495556"
      room_blacks: "#29272a"
      lighting_directive: "warm-amber desk-lamp + cool-blue monitor glow + warm-cool dual lighting for depth"

  composition_templates:
    wide_establishing:
      aspect: "16:9"
      framing: "wide environmental; no character present; foreground/midground/background depth"
      use_cases: ["scene establisher", "deck-section header"]
    contextual:
      aspect: "16:9"
      framing: "wide environmental WITH character DNA injected; character at desk or whiteboard"
      use_cases: ["scene with character", "Stanley-at-work shots"]

  invariants:
    method: "string-match + visual-canon check"
    required:
      - name: "warm_cool_dual_lighting"
        patterns: ["warm-amber desk-lamp", "cool-blue monitor glow", "warm-cool dual lighting"]
      - name: "lived_in_clutter"
        patterns: ["lived-in lab clutter", "anchor objects", "sticky notes", "annotated monitors"]
      - name: "dark_wood_furniture"
        patterns: ["dark wood furniture", "warm-amber desk"]

  # charm_signal repurposed as atmosphere_signal for locations
  # (locations don't "charm" but they do carry an atmosphere)

  lora_refs:
    # No location LoRA in pilot scope — text-only consumer integration
    placeholder: "no_location_lora_in_pilot_scope"

  consumer_compat:
    gemini: { validation: PENDING, notes: "primary consumer; validated at S3" }
    comfyforge: { validation: NOT_APPLICABLE, notes: "no location LoRA pipeline in pilot scope" }
    videoforge: { validation: PENDING, notes: "S5 may use this as scene backdrop" }
    social_content: { validation: PENDING, notes: "background composite in S6 sample posts" }
    metaverse: { validation: PENDING, notes: "S6 documentation pass; 3D-derivative deferred" }

  federation_ref: { framework: "VisualDNA.aDNA", version: "~0.1", pilot_source: "CanvasForge.aDNA M-V1-2-F-VDP-01 S3" }
  re_merge_rationale: "lattice-labs/who/coordination/coord_2026_04_16_forge_split.md"
```

### §4.3 Object example — Stanley's coffee mug (sketch; pattern-only)

Object DNA is the *simplest* of the three; small reference set; tight prompt; no charm_signal.

```yaml
visual_dna:
  id: ss_object_coffee_mug
  display_name: "Science Stanley's coffee mug"
  entity_type: object
  version: "0.1.0"
  status: draft
  established_at: "<future-session>"
  source_pilot: "CanvasForge.aDNA M-V1-2-F-VDP-01 (post-S3 pattern reference)"

  text_prompt:
    full_prompt_inline: |
      Ceramic mug; cream-white body (#ad9580) with hand-drawn pixel-art bear
      illustration on side facing viewer; steaming hot liquid visible at top;
      sits on warm-amber wood desk; consistent in 16-bit pixel art style; soft
      cel-shading; dark line-work outline (#1f1414).

  reference_image_set:
    detail:
      - path: "references/mug_isolated.png"
        label: "Isolated detail shot on neutral background"
    contextual:
      - path: "references/mug_on_desk.png"
        label: "On Stanley's desk (in lab cinematic context)"

  palette_anchors:
    portrait_mode:
      ceramic: "#ad9580"
      illustration: "#1f1414"
      steam: "#f5f0e8"
    # No cinematic_mode — objects inherit cinematic palette from the location they appear in.

  composition_templates:
    detail_isolated:
      aspect: "1:1"
      framing: "centered; isolated on neutral background; close-up of illustration side"
      use_cases: ["asset library", "merchandise mockup"]
    contextual:
      aspect: "varies (inherits from host scene)"
      framing: "embedded in scene; typically foreground anchor in cinematic_mode"
      use_cases: ["foreground anchor in wide_cinematic", "character-using-object shots"]

  invariants:
    method: "string-match + visual check"
    required:
      - name: "ceramic_mug_with_bear_illustration"
        patterns: ["ceramic mug", "bear illustration", "hand-drawn pixel-art bear"]
      - name: "cream_white_body"
        patterns: ["cream-white body", "#ad9580"]
        anti_patterns: ["black mug", "red mug", "logo-printed"]
      - name: "steam_visible"
        patterns: ["steaming hot liquid", "steam visible at top"]

  # charm_signal: omitted (objects don't carry charm; they carry character via their host)

  lora_refs:
    placeholder: "objects_typically_dont_need_loras"

  consumer_compat:
    gemini: { validation: PENDING }
    comfyforge: { validation: NOT_APPLICABLE }
    videoforge: { validation: NOT_APPLICABLE, notes: "objects appear via host scene composition" }
    social_content: { validation: PENDING, notes: "potential merchandise asset" }
    metaverse: { validation: PENDING, notes: "3D-asset derivative possible" }

  federation_ref: { framework: "VisualDNA.aDNA", version: "~0.1" }
  re_merge_rationale: "lattice-labs/who/coordination/coord_2026_04_16_forge_split.md"
```

---

## §5 Consumer-compat matrix

How each of the 5 target consumers reads a visual_dna bundle.

| Consumer | Reads from bundle | Substitution / use | Validation evidence |
|---|---|---|---|
| **Gemini** (CanvasForge canonical) | `text_prompt.portrait_subset` or `text_prompt.full_prompt_inline` + `palette_anchors.<mode>` (substituted into prompt) + `composition_templates.<name>` (substituted as framing block) + `invariants.required[*].patterns` (string-match pre-flight) | Imagen 4 Ultra (text-to-image) + Gemini 2.5 Flash Image (image-edit on reference_image_set entries) | SS character bundle 2026-05-23: anchor + 4 variations VALIDATED |
| **ComfyForge** (SDXL + LoRA) | `lora_refs[*].path` (load LoRA at `recommended_weight`) + `lora_refs[*].trigger_word` (inject into prompt) + `reference_image_set.portraits[*].path` (augment training_data_manifest) | Local SDXL with LoRA-augmented gen; reference images feed into training_data_manifest extension | Pilot S4 PENDING |
| **VideoForge** (Iris) | `text_prompt.portrait_subset` (character-DNA prompt) + `reference_image_set.portraits[*].path` (frame-conditioning + identity-preservation across frames) + `composition_templates.<name>` (per-frame composition) + `lora_refs[*]` (if SDXL backend supports) | Frame composition preserving character identity across N frames; cameo clip generation | Pilot S5 PENDING |
| **Social content** (automation) | `text_prompt.portrait_subset` + `reference_image_set.expressions[*]` (sample random expression for variety) + `composition_templates.portrait_icon` | Topic + visual_dna → SS-character-in-context image via Imagen Ultra (optional LoRA via ComfyForge wrapper) | Pilot S6 PENDING |
| **Metaverse** (3D / avatar / pixel-art derivatives) | `palette_anchors.portrait_mode` (avatar tinting) + `text_prompt.portrait_subset` (initial 3D-mesh prompt) + `reference_image_set.portraits[*]` (PBR-texture reference) + `invariants.required[*].patterns` (canon enforcement on derivatives) | 3D-mesh / avatar / pixel-art-derivative pipelines all read the same bundle | Pilot S6 DOCUMENTED (full integration deferred) |

### Recommended consumer-compat block per entity_type

| entity_type | gemini | comfyforge | videoforge | social_content | metaverse |
|---|---|---|---|---|---|
| character | PRIMARY | LoRA-PAIR | character-consistent frames | PRIMARY consumer | full 5-DNA suite |
| location | PRIMARY | NOT_APPLICABLE typically | scene-backdrop | background composite | 3D scene derivative |
| object | PRIMARY | NOT_APPLICABLE typically | NOT_APPLICABLE | merchandise asset | 3D-asset derivative |

---

## §6 Versioning + federation_ref protocol

### Schema versioning

- This spec is **`visual_dna v0.2`** — schema_version `0.2.0`.
- Producers declare `version:` at the **bundle** level (not the schema level); two bundles can have version `0.1.0` while both validating against schema `v0.2`.
- Schema-version-vs-bundle-version: a bundle's `federation_ref.version: "~0.1"` is a pin against the **framework version** (VisualDNA.aDNA framework v0.1 = this v0.2 schema as the stub publishes it). When the framework lands as v1.0, all bundles re-pin to `"~1.0"` and an additive migration may apply.

### v0.2 changes from v0.1

NEW required fields:
- `entity_type` (was implicit; now declared)
- `status` (was implicit; now declared)

NEW optional-but-recommended blocks:
- `lora_refs` (was absent; defaults to placeholder)
- `consumer_compat` (was absent; defaults to gemini-only)
- `discarded` sub-block inside `reference_image_set` (was ad-hoc in SS bundle; now formalized)

NO breaking changes from v0.1 — all SS-bundle v0.1-shaped data validates against v0.2 unchanged.

### federation_ref protocol

Every bundle MUST declare `federation_ref.framework: VisualDNA.aDNA`. During the pilot, `version: "~0.1"` is the placeholder. After pilot S6 AAR populates the `VisualDNA.aDNA` stub mission, the framework version may bump to v1.0 with a fresh activation pass.

---

## §7 Re-merge rationale (CR7+SO7 citation)

Per CR7+SO7 in `CanvasForge.aDNA/CLAUDE.md`, every visual_dna bundle and this schema spec cite the 2026-04-16 split-reversal recorded at:

**`lattice-labs/who/coordination/coord_2026_04_16_forge_split.md`**

The visual-DNA pattern is load-bearing for CanvasForge's canvas-as-message substrate (Hermes core) — every canvas application (deck slide, comic panel, social post, metaverse avatar) becomes a carried message about a canonical entity. The 2026-04-16 split-reversal established that canvas is the substrate (not deck-only or comic-only); visual-DNA generalizes the same principle to entity-identity: one bundle, many applications.

---

## §8 Schema-validation note

The pre-landed Science Stanley character bundle at `ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml` validates against this spec. Validation outcome:

- **PASS** — every required v0.2 field is present (`id`, `display_name`, `entity_type`, `version`, `status`, `established_at`).
- **PASS** — `text_prompt`, `reference_image_set`, `palette_anchors`, `composition_templates`, `invariants`, `charm_signal` all conform.
- **PASS (placeholder mode)** — `lora_refs` declared as `placeholder: "pilot_S4_will_populate"` (acceptable per §3.8 OPTION A).
- **PASS** — `consumer_compat` declared with all 5 consumer entries; Gemini VALIDATED, rest PENDING per pilot sequence.
- **PASS** — `federation_ref` + `re_merge_rationale` both present.

Outbound coord memo at `ScienceStanley.aDNA/who/coordination/coord_2026_05_24_visual_dna_schema_validation.md` documents the validation outcome and notes which fields will be populated at later sessions (S4 lora_refs; S2 may inline consumer_compat refinements; S3 may add a comic_panel_mode palette block per discarded vars 5+6 future re-validation).

---

## §9 What comes next (pilot session sequence)

| Session | Goal | Schema impact |
|---|---|---|
| **S1 (THIS)** | Schema spec authored | v0.2 ratified |
| S2 | SS character bundle validated + extended | possibly add NEW v0.2 fields if gap surfaces; otherwise no change |
| S3 | Location DNA (lab interior) authored + integration test | location_dna template proven against schema |
| S4 | ComfyForge LoRA integration | `lora_refs` block populated in SS bundle |
| S5 | VideoForge consumer pattern | `consumer_compat.videoforge.validation: VALIDATED` |
| S6 | Social content + metaverse + AAR | `consumer_compat.social_content + metaverse.validation: VALIDATED` + framework recommendations populated in VisualDNA.aDNA stub mission |

If schema gaps surface at S2-S6, a v0.2.x amendment is filed (additive); a breaking change (would require v0.3.0) is treated as a charter event requiring Stanley sign-off.

---

## Amendment 2026-05-24 (v0.2.1 — additive only)

**Source**: M-V1-2-F-VDP-01 S3 III pass — first end-to-end exercise of `composition_rules.md` Pattern 1 (character + location → scene) surfaced a prompt-construction gap.

**Amendment scope** (additive only per S3 plan §H and S3 charter `do NOT bump to v0.3`):
- `composition_rules.md` gains **§5.7 Hex color code hygiene in prompts** documenting the observed hex-leakage failure mode and the prompt-construction discipline that prevents it.
- No change to schema field set, schema semantics, or any required/optional designation.
- No change to consumer_compat enum or federation_ref protocol.

**Where to read it**: see `composition_rules.md § §5.7`.

**Why additive, not breaking**: existing bundles + runners continue to function; the amendment is a *discipline* layered on top of the existing prompt-assembly structure. Bundles authored before 2026-05-24 that inline hex codes into descriptive `text_prompt` blocks remain schema-valid; the §5.7 hygiene rule applies forward-going, and a future bundle-revision pass may strip inline hex from `text_prompt` blocks at the operator's discretion (deferred to pilot AAR sweep at S6).

**Carry-forward status (2026-05-24 close M-V1-2-F-VDP-02 S2)**: bundle-revision pass landed for stanley.yaml + lab_interior.yaml; descriptive blocks now reference palette_anchors by name (6 + 1 = 7 hex-to-name substitutions). Future-bundle authoring discipline is in effect.

---

## Amendment 2026-05-24-v2 (v0.2.2 — additive only)

**Source**: M-V1-2-F-VDP-02 S1 III pass + recurrence-detection across VDP-01 S3 → VDP-02 S1 — two new prompt-construction failure modes surfaced (framing-lock recurrence + label hygiene) requiring schema-level discipline rather than per-runner workaround.

**Amendment scope** (additive only per S2 charter `do NOT bump to v0.3`):
- `composition_rules.md` gains **§5.8 Framing-lock directive in prompts** documenting the observed wide-cinematic-rendered-as-portrait failure mode (F-VDP-01.S3.B + F-VDP-02.S1.A) and the prompt-prefix + compressed-character-subset discipline that prevents it.
- `composition_rules.md` gains **§5.9 Label hygiene in prompts** documenting the observed identity-token-rendered-as-in-frame-text failure mode (F-VDP-02.S1.C) and the role-descriptor + union-invariant-header-only discipline that prevents it.
- No change to schema field set, schema semantics, or any required/optional designation.
- No change to consumer_compat enum or federation_ref protocol.
- Flagged for potential v0.2.x bundle structural revisions (NOT mandatory at v0.2.2): `text_prompt.compressed_character_subset` (~300 char) field and `invariants.has_in_frame_name_badge: bool` field — both opt-in; existing bundles remain schema-valid without them.

**Where to read it**: see `composition_rules.md § §5.8` and `composition_rules.md § §5.9`.

**Why additive, not breaking**: existing bundles + runners continue to function; the amendments are *discipline* layered on top of the existing prompt-assembly structure. Bundles authored before 2026-05-24-v2 that lack compressed_character_subset or has_in_frame_name_badge remain schema-valid; the §5.8 / §5.9 hygiene rules apply forward-going at the runner-assembly layer, and a future bundle-revision pass may add the optional structural fields at the operator's discretion (deferred to pilot AAR sweep at S6).

**Why v0.2.2 not v0.2.1 successor numbering**: v0.2.1 amendment block (above) remains as historical anchor for §5.7 hex hygiene; v0.2.2 layers §5.8 + §5.9 over the v0.2.1 baseline. The cumulative schema is "v0.2 (canonical) + v0.2.1 §5.7 + v0.2.2 §5.8 + §5.9". A breaking change (would require v0.3.0) is treated as a charter event requiring Stanley sign-off.

---

## References

- **Mission charter**: `../../how/campaigns/campaign_canvasforge_v1_2/missions/mission_m_v1_2_f_visual_dna_pilot.md`
- **Empirical anchor**: `~/aDNA/ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml`
- **Anchor prompt audit**: `~/aDNA/ScienceStanley.aDNA/what/visual_dna/characters/stanley/prompt.md`
- **III pass on anchor + variations**: `~/aDNA/ScienceStanley.aDNA/what/visual_dna/characters/stanley/iii_pass.md`
- **VisualDNA.aDNA stub vault**: `~/aDNA/VisualDNA.aDNA/`
- **CanvasForge persona + standing orders**: `~/aDNA/CanvasForge.aDNA/CLAUDE.md`
- **Re-merge rationale (CR7+SO7)**: `~/aDNA/lattice-labs/who/coordination/coord_2026_04_16_forge_split.md`
- **Pillar F mission (parent)**: `../../how/campaigns/campaign_canvasforge_v1_2/missions/mission_m_v1_2_f_prompt_tuning_context_system.md`
- **Composition rules (sibling deliverable)**: `composition_rules.md`
- **Template YAMLs (sibling deliverables)**: `schema/character_dna.yaml`, `schema/location_dna.yaml`, `schema/object_dna.yaml`
