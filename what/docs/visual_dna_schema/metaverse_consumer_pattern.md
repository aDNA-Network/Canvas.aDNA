---
type: consumer_pattern_doc
doc_id: metaverse_consumer_pattern_v0.1
schema_version: "0.1.0"
contract_for: ScienceStanley metaverse (and future per-vault metaverse consumers; runtime TBD per metaverse-side campaign)
contract_against: visual_dna v0.2 (with v0.2.1 §5.7 + v0.2.2 §5.8 + §5.9 amendments)
status: published_runtime_pending
authored_at: "2026-05-25"
authored_by: agent_stanley
authored_in: "CanvasForge.aDNA campaign_canvasforge_v1_2 mission_m_v1_2_f_visual_dna_pilot S6"
re_merge_rationale: "lattice-labs/who/coordination/coord_2026_04_16_forge_split.md"
tags: [consumer_pattern, metaverse, visual_dna, v0_1, character_derivatives, location_derivatives, three_d_avatar, pixel_art_tile, defer_with_spec, hermes, canvasforge, pilot_s6]
---

# Metaverse `visual_dna` Consumer Pattern — v0.1

> Load-bearing deliverable of CanvasForge.aDNA Visual-DNA Pilot Sub-Campaign **M-V1-2-F-VDP-01 Session 6** — the pilot-closing session. Specifies the contract between CanvasForge visual-DNA producers and any metaverse-side runtime that needs canon-consistent 3D / avatar / pixel-art derivatives of canonical entities. Published 2026-05-25 in **defer-with-spec** posture — the ScienceStanley metaverse runtime is not yet implemented; full integration is the scope of a future metaverse-side campaign. This doc is the contract that runtime will implement when it lands.

## §1 Purpose + scope

Establish the consumer pattern by which a metaverse-side runtime reads a visual-DNA character or location bundle and produces **derivative assets** — 3D avatar meshes, pixel-art tile sprites, voxel chunks, 2D billboard variants, walkable-space scene references — that all stay **canon-consistent** with the canonical text+image bundle. Eliminates the per-derivative "redo the character bible" overhead: the visual-DNA bundle IS the cross-modality bible.

### What this doc is

- The **consumer-side contract** for metaverse runtimes against the v0.2 visual-DNA schema (`spec_v0.2.md`), with the v0.2.1 §5.7 hex hygiene + v0.2.2 §5.8 framing-lock + §5.9 label hygiene amendments applied where they have cross-modality analogs.
- A **defer-with-spec deliverable** — the SS metaverse runtime is TBD; this doc is the contract it implements when it lands. Pattern is also adoptable by any future per-vault metaverse (CC, WGA, RareHarness avatar UIs, etc.).
- A **multi-derivative spec** — covers 5 derivative classes: (a) 3D avatar mesh; (b) pixel-art tile sprite; (c) voxel chunk; (d) 2D billboard variant; (e) walkable-space scene reference. Each derivative class consumes a different subset of bundle fields (§2).
- A **sibling of the videoforge_consumer_pattern.md** — both formalize the substrate's reach beyond static-image work without absorbing the consumer runtime into the substrate itself.

### What this doc is NOT

- Not a 3D-modeling tool spec (Blender / Maya / Unity workflows are metaverse-side concerns; this doc is what they read from the bundle, not how they render).
- Not a comprehensive metaverse-world spec (movement / physics / interaction / multiplayer-sync are metaverse-side; this doc is asset-derivation contract only).
- Not a real-time-rendering spec (per-frame budget / GPU-side optimization / LOD selection are metaverse-side; this doc is asset-source contract).
- Not a per-vault metaverse mission-planning document (each consuming vault's metaverse campaign owns its own runtime topology; this doc is the consumer-side input contract).

### Scope of this v0.1 release

- 2 entity types: character + location (object derivatives deferred; the lab_interior pattern carries cleanly to interactive walkable-space scene references for free).
- 5 derivative classes (above).
- Visual-fidelity envelope: 16-bit pixel art (SNES-era) as the canonical source; 3D + voxel derivatives explicitly inherit the pixel-art discipline (chunky low-poly aesthetic preferred over photorealistic-uprez to stay canon-consistent).
- Backend-agnostic: contract works for any metaverse runtime the consuming vault elects.

---

## §2 Data model — visual-DNA fields consumed per derivative class

A metaverse runtime reads the following fields from a visual-DNA character or location bundle. Cross-reference: `spec_v0.2.md §5` consumer-compat matrix row for metaverse + `context_bio_digital_cozy_metaverse_style.md` (SS canonical metaverse style anchor v1.0) + `style_search_ss_metaverse_application_charter.md` (complementary environment-archetype scaffold).

### §2.1 Required fields (all derivative classes)

| Field path | Type | Role across derivatives |
|---|---|---|
| `id` + `display_name` + `entity_type` | string | Identity binding for asset registry; metaverse runtime indexes assets by `id`; displays `display_name` in UI / overlays; routes by `entity_type` (character pipelines vs location pipelines). |
| `palette_anchors.portrait_mode` (characters) OR `palette_anchors.cinematic_mode` (locations) | nested hex dict | Color-canon ground truth for ALL derivatives. 3D mesh material assignments / pixel-art sprite palettes / voxel block colors / billboard texture tints / scene reference color-grading — every derivative MUST inherit these hex anchors. Palette drift across derivatives breaks cross-modality canon. |
| `invariants.required[*]` | list of `{name, patterns, anti_patterns, [provenance]}` | Per-derivative validation contract. Each derivative MUST be inspectable against the invariant list; if a derivative omits a required invariant (e.g., 3D mesh missing the round blue-framed glasses), the asset is non-canon and fails the derivative gate. |
| `reference_image_set.portraits[*].path` (characters) OR `reference_image_set.establishing[*].path` (locations) | list of file paths | Source-of-truth canonical images for ANY 2D derivative (sprite atlas / billboard / icon). 3D + voxel pipelines use these as reference for proportions + silhouette + palette extraction. The `canonical: true` entry is the primary reference. |
| `composition_templates.*` (where present) | nested dict | Aspect-ratio + framing source for 2D derivatives. The `portrait_icon` template (1:1 character) is the canonical avatar-thumbnail derivative; `wide_cinematic_establishing` (16:9 location) is the canonical hero-scene billboard. |

### §2.2 Required fields (character bundles only)

| Field path | Type | Role across derivatives |
|---|---|---|
| `charm_signal.tells[*]` + `charm_signal.anti_tells[*]` | list of strings | Animation / pose / expression-state validation. 3D rigging poses + sprite emotion sets + billboard alt-textures all gated against tells-must-show / anti-tells-must-be-absent. The metaverse runtime emits expression states that score against the same tells lattice the static-image pilot uses. |
| `text_prompt.portrait_subset` | string (~1500 chars) | Source-of-truth character-DNA prompt; informs ANY derivative pipeline that uses text-conditioned generation (e.g., LoRA-augmented 2D billboard regeneration; voxel-block-from-text experiments). The compressed variant carries identity-bearing tokens without environmental clutter — appropriate for asset-derivation pipelines that need character DNA without scene context. |

### §2.3 Required fields (location bundles only)

| Field path | Type | Role across derivatives |
|---|---|---|
| `atmosphere_signal.tells[*]` + `atmosphere_signal.anti_tells[*]` | list of strings | Walkable-space ambience validation. The lab interior's "inhabited working space; mentor's lab; late-night studious calm" tells inform the metaverse runtime's ambient lighting + audio + interaction prompts. Anti-tells (sterile clean-room; corporate office; dystopian neon) are excluded as scene-mode states. |
| `text_prompt.cinematic_subset` | string | Source-of-truth location-DNA prompt; informs scene-reference regeneration + walkable-space dressing + environment archetype selection. Pairs with `context_bio_digital_cozy_metaverse_style.md` § dual-resolution rule (high-fidelity 32-bit for physical world; 16-bit chunky sprites for AI agents). |

### §2.4 Optional fields

| Field path | Type | Role when present |
|---|---|---|
| `lora_refs[*]` | list of `{path, model_family, trigger_word, recommended_weight, ...}` | Optional 2D billboard regeneration via SDXL LoRA. If the metaverse runtime supports SDXL LoRA loading for asset regeneration (e.g., re-rendering a billboard sprite from a new angle), the bundle's LoRA refs become consumable for tighter character fidelity. If backend does NOT support LoRA, derivative regeneration falls back to text + reference-image conditioning. |
| `palette_anchors.cinematic_mode` (on character bundles) | nested dict | Optional palette pinning for character-in-scene derivatives (3D character standing in a metaverse scene; the cinematic_mode palette pins the environmental lighting tint applied to the character's material). |
| `reference_image_set.scenes[*]` + `reference_image_set.expressions[*]` | list of paths | Optional auxiliary references for expression / pose / scene-context derivatives. Sprite-sheet atlases drawing emotion states from `expressions[*]`; walkable-space environmental references drawing scene dressing from `scenes[*]`. |

### §2.5 NOT consumed by metaverse derivatives

- `reference_image_set.discarded[*]` — vars rejected during canon election (e.g., Stanley vars 5-6 comic-panel + whiteboard per Stanley's `discarded` block); these are NEGATIVE references and MUST NOT condition any derivative.
- `consumer_compat.metaverse` — metaverse's own status field; produced by CanvasForge (the consumer-side wrapper updates this); not consumed by metaverse runtime.
- `federation_ref` — framework-level metadata; not consumed by runtime.

---

## §3 Composition rules — multi-DNA derivatives (Pattern 1 lift)

Metaverse runtimes routinely compose 2+ DNAs (character placed in location for a walkable scene; multiple characters in a multiplayer scene). The composition rules from `composition_rules.md` Pattern 1 (character + location → scene) lift cleanly to derivative pipelines.

### §3.1 Character-in-walkable-space derivative

For a character placed in a metaverse walkable-space scene:

1. **Character DNA** — `character.yaml` provides 3D mesh + palette + invariants + charm_signal pose constraints.
2. **Location DNA** — `location.yaml` provides walkable-space geometry reference + atmosphere_signal ambient state + cinematic_mode palette pinning for environmental lighting.
3. **Composition rules** — Pattern 1 (character + location → scene) §5.4 charm × atmosphere orthogonality holds: the character's charm_signal (Stanley's warm-presenter energy) carries independently of the location's atmosphere_signal (lab interior's late-night studious calm); the metaverse runtime composes both into the scene-state without conflict.
4. **Union invariant check** — every invariant from both bundles (Stanley's 11 + lab interior's 6 = 17 union invariants for a Stanley-at-lab-interior walkable scene) must be inspectable; missing invariants on either side fail the composition gate.
5. **Palette discipline** — per `composition_rules.md §5.1` location wins for environmental palette; character retains portrait_mode palette for the character mesh material assignments.

### §3.2 Multi-character derivative (deferred to S6+ pattern-evolution)

Pattern 2 (character + character) extension to walkable-space + multiplayer-sync deferred; pilot scope is Pattern 1 only. The composition_rules.md §5 disciplines extend cleanly when the pattern is exercised — pilot VDP-02 S1 validated Pattern 2 in static-image scope (Stanley + Charlie at 91.7% union-invariant).

---

## §4 I/O contract

### §4.1 Input schema (CanvasForge → metaverse runtime)

The metaverse runtime's derivative pipelines receive the following input shape (proposed; final shape elected by the metaverse-side runtime at its activation campaign):

```yaml
metaverse_visual_dna_derivative_request:
  entity_dna_bundle_path: str            # absolute path to character OR location visual_dna YAML
  derivative_class: enum                 # "3d_avatar_mesh" | "pixel_art_tile" | "voxel_chunk" | "2d_billboard" | "walkable_space_scene_ref"
  target_runtime_format: enum            # "gltf" | "fbx" | "unity_prefab" | "godot_scene" | "tiled_tmx" | "png_atlas" | "raw_voxel_grid"
  composition_dnas:                      # optional secondary DNAs for compositional derivatives
    - { path: str, role: "primary" | "scene_backdrop" | "co_character" }
  expression_state:                      # for character 3D / billboard derivatives
    state_id: str                        # e.g., "warm_laughing" | "focused" | "presenter_default"
    derived_from_reference: str          # e.g., "var_3_expression_warm_laughing.png"
  invariant_inspection_required: bool    # true = post-derivation gate runs invariants.required[*] check
  derivative_output_path: str            # where the asset lands
  source_of_truth_validation:            # required cross-check at derivation time
    palette_anchor_check: bool           # true = derivative palette pinned to bundle palette_anchors
    canonical_reference_required: bool   # true = derivative references the canonical: true entry
    discarded_exclusion_check: bool      # true = derivative does NOT inherit from discarded[*] entries
```

### §4.2 Output schema (metaverse runtime → CanvasForge / consuming vault)

```yaml
metaverse_visual_dna_derivative_result:
  request_echo:                          # input echo for provenance
    entity_dna_bundle_path: str
    derivative_class: str
    target_runtime_format: str
  rendered_outputs:
    primary_output_path: str             # the derivative asset (gltf / fbx / png_atlas / etc.)
    sidecar_outputs:                     # optional supplementary outputs
      preview_image_path: str | null     # 2D render of the derivative (for human-inspection at gate)
      metadata_json_path: str            # path to derivation provenance + validation results
  metadata_summary:
    derivation_tool_used: str            # which backend ran (Blender plugin / Unity importer / etc.)
    lora_refs_loaded: list               # which LoRA refs were used (if any; may differ if backend incompatible)
    derivation_time_sec: int
    estimated_cost: float                # if cloud-derivation; 0 for local
  validation_results:
    invariant_inspection_status: "pass" | "fail" | "skipped"
    inspection_failures: list            # if any invariant missing from the derivative
    palette_anchor_check_status: "pass" | "fail" | "skipped"
    palette_drift_observed: list         # if any hex drift detected from bundle palette_anchors
    canonical_reference_used: str | null # which canonical entry was used as source-of-truth
    discarded_exclusion_status: "pass" | "fail" | "skipped"
    overall_pass: bool
```

### §4.3 Cross-vault path resolution

The input schema's `entity_dna_bundle_path` + `lora_refs[*].path` + `reference_image_set.*[*].path` all resolve cross-vault — the character bundle lives at `ScienceStanley.aDNA/what/visual_dna/...` while the metaverse runtime may live in a separate metaverse-side vault. The runtime requires cross-vault read access for the bundle YAML AND the reference image files it points at.

### §4.4 Asset-registry feedback loop

After derivation, the consuming vault's metaverse runtime SHOULD emit an asset-registry record back to the bundle's `consumer_compat.metaverse` block, updating `validation` from `PILOT_S6_DOCUMENTED → DERIVATIVE_REGISTERED_<derivative_class>` and populating `asset_registry_path` with the metaverse-side asset entry. This is the lockstep-flip discipline mirrored from VideoForge consumer pattern §C — the bundle's consumer-side status surface tracks the runtime's derivation state.

---

## §5 Deferred items + dependencies on metaverse-side campaign

### §5.1 Out of pilot S6 cameo / pattern-publication scope

- **3D mesh authoring + rigging pipelines** — Blender / Maya / Unity workflows that produce the actual .gltf / .fbx / .unity-prefab files. These are metaverse-side concerns; this doc is the input contract only.
- **Voxel-chunk derivation algorithms** — the actual reverse-pixel-art-to-voxel conversion is a metaverse-side concern; this doc specifies what the bundle MUST provide as input.
- **Runtime asset-registry implementation** — the metaverse-side database / KV-store / file-system layout that holds derivative assets is metaverse-side.
- **Multiplayer character sync** — out of pilot; pattern doesn't constrain how avatars synchronize across clients.
- **Walkable-space physics / interaction** — out of pilot; pattern doesn't constrain locomotion or trigger zones.
- **Dual-resolution rule implementation** — per `context_bio_digital_cozy_metaverse_style.md` § dual-resolution: high-fidelity 32-bit for physical world / humans + 16-bit chunky sprites for AI agents. This doc documents the rule; metaverse runtime implements it.
- **Environment-archetype hookup** — `style_search_ss_metaverse_application_charter.md` defines 3 environment archetypes (lab_interior, digital_network_space, global_federation); each archetype's location-DNA bundle would consume this pattern when fleshed out.

### §5.2 Dependencies on future metaverse-side campaign

This pattern is a defer-with-spec deliverable; the **ScienceStanley metaverse-side campaign** owns the runtime implementation. Recommended pre-conditions for that campaign to consume this contract:

1. ScienceStanley metaverse runtime selection (Unity / Godot / Three.js / custom).
2. Asset-registry topology (per-entity-per-derivative-class registry shape).
3. Cross-vault read access pattern (filesystem mount / git-submodule / API-fetch).
4. Lockstep status-flip protocol (how `consumer_compat.metaverse.validation` updates flow back to the bundle).
5. III-style derivative-gate scoring (analog of the per-frame iii_aggregate scoring in the VideoForge pattern §5.3).

When that campaign opens, this v0.1 pattern doc is its consumer-contract input; the runtime implements against it; lockstep-flip the bundle status surfaces; pilot consumer_compat matrix entry flips from `PILOT_S6_DOCUMENTED → DERIVATIVE_REGISTERED_<class>` as derivatives land.

> **§5.2 note — 2D-consumer reading (Mondrian, 2026-08-22).** The ScienceStanley metaverse-side
> campaign has opened (`campaign_ss_metaverse_brand`) and ruled its world **2D narrative** (SS Sitting A,
> ruling A1-a, 2026-08-06) — the literal-3D/voxel/walkable reading is excluded by ruling on their side.
> For a 2D consumer, the preconditions above read: **1 (runtime selection) — void**, there is no runtime;
> **2 (asset registry) and 3 (cross-vault read) — satisfied by re-read** (their image ledger/census +
> plain filesystem reads); **4 (lockstep flip) and 5 (III derivative gates) — intact as written**. The
> 3D derivative classes remain valid for any future consumer whose metaverse *is* 3D; nothing here is
> deprecated. SS's disposition of record: `ScienceStanley.aDNA/what/context/narrative/context_narrative_metaverse_world.md` §3.

---

## §6 Re-merge rationale

The metaverse consumer pattern is the canvas-as-message substrate's **cross-modality** extension — the third orthogonal axis of substrate reach (after the temporal axis VideoForge formalized at S5 + the algorithmic axis ComfyForge LoRA formalized at S4). Every metaverse-derivative asset is a canvas being carried from intent (canonical character or location bundle) to delivery (3D / voxel / pixel-art / walkable-space derivative) via the metaverse runtime as the cross-modality courier. The visual-DNA bundle is the structured message; each derivative class is a courier specialization that preserves the message's integrity (character identity, palette discipline, atmosphere ambient state) across the cross-modality journey.

The 2026-04-16 canvas-substrate re-merge (`lattice-labs/who/coordination/coord_2026_04_16_forge_split.md`) established that canvas is the substrate, not just a static-image side product — and the metaverse derivative-pipeline class is the natural cross-modality extension of canvas-as-message into interactive 3D + voxel + walkable-space surfaces. The pilot's 5-consumer matrix (Gemini · ComfyForge · VideoForge · social_content · **metaverse**) validates that the canvas-message-substrate scales across all visual production surfaces. The metaverse is the cross-modality extension; this pattern doc formalizes the substrate's reach into derivative-asset work without absorbing any metaverse runtime into the substrate itself.

---

## References

### Within CanvasForge.aDNA

- Visual-DNA schema spec v0.2: `~/aDNA/Canvas.aDNA/what/docs/visual_dna_schema/spec_v0.2.md` (§5 consumer-compat matrix row for metaverse; §6 versioning + federation_ref protocol)
- Composition rules: `~/aDNA/Canvas.aDNA/what/docs/visual_dna_schema/composition_rules.md` (§5 multi-DNA composition; Pattern 1 character + location source for §3.1)
- Sibling consumer pattern (S5 precedent + shape template): `~/aDNA/Canvas.aDNA/what/docs/visual_dna_schema/videoforge_consumer_pattern.md` (v0.1; established the pattern-publication + defer-with-spec contract shape this doc mirrors)
- Sibling consumer wrapper (S4 precedent): `~/aDNA/CanvasForge.aDNA/comfyforge/CLAUDE.md` (LoRA-as-visual-DNA-component contract; lora_refs producer side)
- Sibling consumer wrapper (S5 precedent): `~/aDNA/CanvasForge.aDNA/videoforge/CLAUDE.md` (federation_ref + local_extensions + 3-artifact lockstep flip discipline mirrored at §4.4 above)
- Pilot mission: `~/aDNA/CanvasForge.aDNA/how/campaigns/campaign_canvasforge_v1_2/missions/mission_m_v1_2_f_visual_dna_pilot.md` (S6 deliverable lineage)
- Pilot AAR: `~/aDNA/CanvasForge.aDNA/how/campaigns/campaign_canvasforge_v1_2/missions/mission_m_v1_2_f_visual_dna_pilot.aar.md` (closes the pilot; this pattern doc cited per CR7+SO7)
- Complementary metaverse scaffold (style externalization for RLHF environment archetypes): `~/aDNA/CanvasForge.aDNA/how/missions/artifacts/style_search_ss_metaverse_application_charter.md` (3 environment archetypes; complementary not duplicative)

### Within ScienceStanley.aDNA (consumer bundle examples + style canonical)

- Stanley character bundle (S6 primary character target): `~/aDNA/ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml`
- Lab interior location bundle (S6 location-derivative target): `~/aDNA/ScienceStanley.aDNA/what/visual_dna/locations/lab_interior/lab_interior.yaml`
- Charlie character bundle (future multi-character derivative target post-VDP-02): `~/aDNA/ScienceStanley.aDNA/what/visual_dna/characters/charlie/charlie.yaml`
- **SS metaverse style anchor (canonical v1.0)**: `~/aDNA/ScienceStanley.aDNA/what/context/visual/context_bio_digital_cozy_metaverse_style.md` (cozy bio-digital retro-futurism; 32-bit pixel art + Studio Ghibli + scientific clutter; dual-resolution rule; cyber-chiaroscuro lighting bible) — this style anchor is the canon for any ScienceStanley metaverse derivative; per-vault metaverse consumers will declare their own equivalents

### Cross-vault framework partner

- VisualDNA.aDNA stub: `~/aDNA/VisualDNA.aDNA/CLAUDE.md` (persona Pygmalion; activates post-pilot S6 AAR; will host the canonical metaverse-consumer wrapper template absorbed from this v0.1 doc)

### Re-merge rationale (load-bearing per CR7+SO7)

- `~/aDNA/lattice-labs/who/coordination/coord_2026_04_16_forge_split.md` — the 2026-04-16 CanvasForge re-merge that established the canvas-substrate this pattern federates with.
