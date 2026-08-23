---
type: composition_rules
sibling_spec: visual_dna v0.2 (spec_v0.2.md)
status: reference_copy_superseded_by_visualdna_v1_0
superseded_by: ~/aDNA/VisualDNA.aDNA/what/artifacts/visual_dna_schema/composition_rules.md
superseded_at: 2026-05-28 (VisualDNA.aDNA P1 schema_lock mission close per Stanley sign-off via ExitPlanMode please-read-the-claude-md-jazzy-summit)
authored_at: "2026-05-24"
authored_in: "CanvasForge.aDNA M-V1-2-F-VDP-01 S1"
re_merge_rationale: "lattice-labs/who/coordination/coord_2026_04_16_forge_split.md"
tags: [composition, visual_dna, mix_patterns, conflict_resolution, agent_facing, pilot_deliverable, reference_copy, superseded, historical_anchor]
---

> **REFERENCE-COPY NOTICE (2026-05-28)** — This file is a historical reference-copy.
> The canonical composition rules document is now `~/aDNA/VisualDNA.aDNA/what/artifacts/visual_dna_schema/composition_rules.md`
> at framework version v1.0.0 (GA tagged at P1 schema_lock close 2026-05-28).
> v0.2.1 §5.7 hex hygiene + v0.2.2 §5.8 framing-lock + v0.2.2 §5.9 label hygiene amendments
> are promoted to first-class §6 / §7 / §8 sections in the v1.0 canonical document.
> Consumer wrappers re-pin from `~0.1 → ~1.0` at framework P5 close (4 vaults: CanvasForge / ScienceStanley / ComfyForge / VideoForge).
> See `~/aDNA/VisualDNA.aDNA/who/coordination/coord_2026_05_28_p1_schema_lock_closed.md` for migration coord.

# Visual-DNA Composition Rules — v0.2

> Agent-facing guidance for **mixing 2+ visual-DNA bundles** to compose novel scenes. Sibling deliverable to `spec_v0.2.md` (the schema contract). This document is the *behavior* contract.

## §0 Purpose

The schema (`spec_v0.2.md`) defines what a single visual-DNA bundle looks like. This document defines how an agent should **combine** bundles to produce a coherent scene. Without composition rules, two valid bundles can be combined in incoherent ways (palette wars, framing conflicts, invariant violations).

The rules are deliberately simple. The complexity lives in the bundles; this is the merge protocol.

---

## §1 Pattern 1 — character + location → scene

The most common composition. Inhabit a location with a character.

### Inputs
- One **character_dna** bundle (provides identity + portrait/cinematic prompt + invariants + charm_signal)
- One **location_dna** bundle (provides environmental prompt + cinematic palette + lighting directive + atmosphere_signal)

### Merge protocol
1. **Pick a composition template from the LOCATION** — prefer `composition_templates.contextual` (the with-character variant). If absent, fall back to `wide_establishing` with character DNA injected.
2. **Pick the character's `text_prompt.cinematic_subset`** (if absent, use portrait_subset adapted for cinematic — see §5 conflict resolution).
3. **Concatenate the location's `text_prompt.cinematic_subset` after the character's** with a clear `[ENVIRONMENT]` separator marker.
4. **Override the character's `palette_anchors.portrait_mode.background`** with the location's `palette_anchors.cinematic_mode` directives (location wins for environmental palette).
5. **Preserve the character's `palette_anchors.portrait_mode` for skin/hair/costume** (character wins for body palette).
6. **Concatenate invariants**: union the character's required invariants + the location's required invariants. Both must hold.
7. **Carry forward `charm_signal` from the character** AND `atmosphere_signal` from the location (both apply; orthogonal axes).
8. **Use the LOCATION's reference_image_set.contextual[*]** as primary reference; fall back to the location's establishing + the character's portraits if no contextual reference exists.

### Worked example — Stanley at lab whiteboard

```yaml
# Inputs:
character: ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml
location:  ScienceStanley.aDNA/what/visual_dna/locations/lab_interior.yaml

# Composition output (assembled prompt; conceptual):
[CHARACTER]
<stanley.text_prompt.cinematic_subset OR portrait_subset rewritten cinematic>
Science Stanley: early-30s; spiky warm-brown hair (auburn highlights #c97c5c);
round blue-framed glasses; white lab coat; purple turtleneck (#9d7cd8);
STANLEY name badge at chest; standing at lab whiteboard; gesturing toward
a diagram; engaged-not-performing energy.

[ENVIRONMENT]
<lab_interior.text_prompt.cinematic_subset>
Inhabited night-lit lab/office; dark wood furniture with lived-in lab clutter;
warm-amber desk surface (foreground) with anchor objects (mug with steam,
notebook, framed photo); cool blue monitor glow modeling midground; glass-walled
clean lab visible through deep window behind (background atmosphere; soft DOF
blur). Warm-cool dual lighting palette for depth.

[PALETTE]
Skin/hair/costume: from character.palette_anchors.portrait_mode
Environment + lighting: from location.palette_anchors.cinematic_mode

[FRAMING]
Apply location.composition_templates.contextual (16:9; character + whiteboard share focal hierarchy)

[INVARIANTS] (union)
- round_glasses ✓ (character)
- spiky_brown_hair_auburn ✓ (character)
- white_lab_coat ✓ (character)
- purple_turtleneck ✓ (character)
- STANLEY_name_badge ✓ (character)
- warm_cool_dual_lighting ✓ (location)
- lived_in_clutter ✓ (location)
- dark_wood_furniture ✓ (location)
```

---

## §2 Pattern 2 — character + character → two-shot

Two characters in one frame; identity-preservation for both.

### Inputs
- Two **character_dna** bundles (each provides identity + invariants + charm_signal)

### Merge protocol
1. **Both characters MUST have a compatible `composition_template`** — typically both have `portrait_icon` or both have `comic_panel`. If templates conflict, fall back to a generic `wide_two_shot` (16:9, both characters visible, neither cropped).
2. **Concatenate both characters' portrait_subset prompts** with a clear `[CHARACTER A]` / `[CHARACTER B]` separator.
3. **Background**: explicit decision required — either neutral (`#76428a` or other), inherited from a third location_dna (becomes a 3-DNA composition; see §4), or scene-implied via prompt (e.g., "at a coffee shop table").
4. **Palette anchors**: keep each character's portrait_mode palette intact; if invariants conflict (e.g., both characters declare different turtleneck color), each character keeps their own.
5. **Concatenate invariants**: union both characters' required invariants. Both must hold. If two characters have *contradictory* invariants on the same body-coordinate (rare — e.g., both declare a different name-badge text), the prompt explicitly lists both — the renderer assigns each correctly via spatial cue.
6. **Charm signals**: both carry; the scene reads correctly when both are present.
7. **Spatial cue**: include an explicit positional directive — "Character A on left; Character B on right; both facing 3/4 toward camera; eye contact between them" — to disambiguate identity assignment.

### Worked example — Stanley + (hypothetical) Carly two-shot

```yaml
[CHARACTER A — Stanley on LEFT]
<stanley.text_prompt.portrait_subset; framed at 3/4-turn-right>

[CHARACTER B — (hypothetical) Carly on RIGHT]
<carly.text_prompt.portrait_subset; framed at 3/4-turn-left>

[BACKGROUND]
Neutral solid purple (#76428a) per Stanley's portrait_mode default;
both characters' costume colors hold against this background.

[FRAMING]
Wide two-shot 16:9; both head-and-shoulders visible; eye contact between them;
gentle smiles; engaged conversation energy.

[INVARIANTS] (union)
- (Stanley's 11 invariants) ✓
- (Carly's invariants) ✓
- Spatial: Stanley on LEFT; Carly on RIGHT
```

---

## §3 Pattern 3 — character + object → activity shot

A character interacting with a canonical object.

### Inputs
- One **character_dna** bundle
- One **object_dna** bundle

### Merge protocol
1. **Object inherits the character's framing** — pick a composition_template from the CHARACTER (typically `portrait_closeup` or `wide_cinematic_establishing`).
2. **Object's prompt is appended as a foreground/midground hint** — "holding <object>" or "<object> on table in foreground" depending on activity.
3. **Object inherits the character's host palette** — if shot is portrait_mode, the object uses character's portrait_mode palette as backdrop; if shot is cinematic_mode (with a location_dna in the mix — see §4), object inherits cinematic_mode.
4. **Concatenate invariants**: character + object invariants both required.
5. **Activity cue**: include an explicit verb — "holding", "using", "examining", "placing on desk" — to anchor the interaction.
6. **Object's contextual reference_image_set** is preferred over isolated (the contextual version already shows the object in canonical use).

### Worked example — Stanley holding coffee mug

```yaml
[CHARACTER]
<stanley.text_prompt.portrait_subset; head-and-shoulders + hand visible>

[OBJECT — held]
Ceramic mug; cream-white body (#ad9580) with hand-drawn pixel-art bear illustration
on side facing viewer; steaming hot liquid visible at top; Stanley is holding
the mug in his left hand at chest height, mug visible to viewer.

[BACKGROUND]
Solid medium-purple #76428a (Stanley's portrait_mode default).

[FRAMING]
Apply stanley.composition_templates.portrait_closeup (1:1; tighter head + upper-shoulders +
visible hand).

[INVARIANTS] (union)
- (Stanley's 11 invariants) ✓
- ceramic_mug_with_bear_illustration ✓ (object)
- cream_white_body ✓ (object)
- steam_visible ✓ (object)
- Activity: holding at chest height; mug face visible to viewer
```

---

## §4 Pattern 4 — character + character + location → group scene

Multiple characters in a shared environment. Combine §1 + §2 protocols.

### Merge protocol
1. **Start with the LOCATION** (use Pattern 1 protocol to inhabit the location).
2. **Add second character** as in Pattern 2, with the LOCATION providing the background instead of a neutral fill.
3. **Spatial cues for each character** are mandatory at 3+ DNAs (the renderer needs explicit positional anchors).
4. **Invariants** union all three bundles; both characters' invariants AND the location's invariants must hold.
5. **Reference image priority**: location.contextual > location.establishing + each character's portraits.

### Worked example — Stanley + Carly at lab whiteboard

Pattern 1 (Stanley + lab_interior) → adds Pattern 2 (Carly as second character):

```yaml
[CHARACTER A — Stanley at whiteboard LEFT]
<stanley.text_prompt.cinematic_subset; gesturing toward diagram on whiteboard>

[CHARACTER B — Carly seated MID-RIGHT]
<carly.text_prompt.portrait_subset rewritten cinematic; seated at desk;
 looking up at whiteboard, engaged>

[ENVIRONMENT]
<lab_interior.text_prompt.cinematic_subset>

[FRAMING]
Apply lab_interior.composition_templates.contextual extended (16:9; 2 characters share
focal hierarchy with whiteboard; Stanley LEFT-foreground; Carly MID-RIGHT seated).

[PALETTE]
Skin/hair/costume: each character's own portrait_mode (preserved per §2.4)
Environment + lighting: lab_interior.cinematic_mode

[INVARIANTS] (union of all three)
(All Stanley invariants + all Carly invariants + all lab_interior invariants)
```

---

## §5 Conflict resolution

When 2+ DNAs declare conflicting fields, the following hierarchy applies (top wins):

### §5.1 Palette anchors

1. **Character body palette wins** — each character keeps their own skin/hair/costume palette. Two characters with different turtleneck colors both render correctly.
2. **Location wins for environment** — desk_wood, lighting_directive, room_blacks, monitor_glow all come from location_dna.
3. **Object inherits host** — object palette anchors only override if object is the *subject* of a detail_isolated shot; in contextual shots, object inherits the surrounding palette.

### §5.2 Composition templates

1. **Most specific wins** — `contextual` (with character) beats `wide_establishing` (without) when both are available.
2. **Location wins for multi-DNA scenes** — when 1+ characters are placed in a location, the location's composition templates govern.
3. **Character wins for character-centric shots** — Pattern 3 (character + object) defers to the character's framing because the object is a prop.

### §5.3 Invariants

1. **Union by default** — all invariants from all DNAs must hold.
2. **Contradictory invariants on the same body-coordinate** — both are listed in the prompt with explicit spatial assignment (rare; only fires for character + character with same-feature contradictions).
3. **Anti-pattern collision** — if Character A's `patterns` includes a phrase that Character B's `anti_patterns` excludes, the renderer is given both characters with spatial cues so the constraint applies per-character (e.g., "Character A has spiky hair; Character B has smooth hair" — the prompt names both).

### §5.4 Charm + atmosphere signals

- **Orthogonal — never conflict.** Charm is character-bound; atmosphere is location-bound; both carry simultaneously without merge logic.
- Multi-character: both characters' charm_signals carry; tells are union'd.

### §5.5 LoRA refs

1. **Character LoRAs apply when character is present** — load all `lora_refs` from each character DNA at the consumer-recommended weights.
2. **Multiple character LoRAs** — load each at its `recommended_weight`; if combined weight > ~1.5, scale proportionally (per ComfyForge guidance, not this spec).
3. **Location / object LoRAs typically absent** — placeholder mode dominant.

### §5.6 Conflict-resolution audit trail

When composition produces a conflict that required hierarchy fall-back, the agent SHOULD log the conflict in the composition output's `provenance` field for the rendered image — e.g., "Conflict: Stanley.background (#76428a) overridden by lab_interior.cinematic_mode.room_blacks (#29272a) per Pattern 1 protocol §1.4."

### §5.7 Hex color code hygiene in prompts — AMENDMENT 2026-05-24 (v0.2.1, additive)

**Empirical finding** (M-V1-2-F-VDP-01 S3 III pass, 2026-05-24): when Imagen 4 Ultra receives a prompt that inlines literal hex color strings (e.g., `purple turtleneck (#9d7cd8)`) inside descriptive `[CHARACTER]`, `[ENVIRONMENT]`, or `[INVARIANTS]` blocks, the model may render those hex character sequences as in-frame text on badges, whiteboards, signs, and other text surfaces. Observed at S3 on the integration scene whiteboard (`9d7c08`, `1f1414`, `7422950`) and on the IMPROVE #2 portrait variant's STANLEY badge (`1F1414`).

**Disposition**:

1. Hex color values SHOULD only appear in a dedicated `[PALETTE]` section of the assembled prompt where the consumer renderer reads them as palette declarations, not as content for rendering.
2. Hex color values MUST NOT be inlined into `[CHARACTER]`, `[ENVIRONMENT]`, or `[INVARIANTS]` prose where the consumer may interpret them as text content for in-frame text surfaces.
3. Color references inside descriptive blocks SHOULD use descriptive names (e.g., "purple turtleneck", "auburn-warm hair") rather than hex codes; the `[PALETTE]` block carries the hex anchor for any consumer that needs the exact value.
4. The `[PALETTE]` section format remains as in §6.2 — hex values are grouped, role-keyed, and rendered as palette declarations rather than as character traits.

**Runner-side implication**: image-gen runners that assemble prompts from `text_prompt.cinematic_subset` or `text_prompt.portrait_subset` should either:
- Pre-strip inline hex tokens from descriptive blocks before injection, OR
- Author the `cinematic_subset` / `portrait_subset` field values without inline hex tokens in the first place (preferred — keeps the visual_dna bundle itself clean).

**Severity**: MEDIUM (cosmetic; canon-invariants unaffected; thumbnail-readability impacted).

**Carry-forward**: pilot S4+ runners apply this discipline. The character bundle `stanley.yaml` and location bundle `lab_interior.yaml` may benefit from a v0.2.x bundle revision that strips inline hex from `text_prompt` blocks (deferred to pilot AAR sweep at S6). **CLOSED 2026-05-24 at M-V1-2-F-VDP-02 S2**: stanley.yaml + lab_interior.yaml hex hygiene fix landed (6 + 1 hex-to-name substitutions); descriptive blocks now reference palette_anchors by name.

### §5.8 Framing-lock directive in prompts — AMENDMENT 2026-05-24 (v0.2.2, additive)

**Empirical finding** (M-V1-2-F-VDP-01 S3 + M-V1-2-F-VDP-02 S1 III passes, 2026-05-24): when Imagen 4 Ultra receives a prompt that mixes a character `[CHARACTER]` block (typically dense, multi-clause, identity-specifying) with an environmental framing directive (e.g., "wide cinematic 16:9 patrol through lab"), the model may prioritize the character block's portrait-style attention budget over the framing directive and render a portrait-style image despite the explicit wide framing instruction. Observed first at VDP-01 S3 wide_establishing.png (F-VDP-01.S3.B) and recurrent at VDP-02 S1 var_2_lab_guardian_patrol.png (F-VDP-02.S1.A; iii_aggregate 78.0 — invariants present but framing portrait-not-wide). The recurrence across two missions is the trigger for amendment to schema rather than per-runner workaround.

**Disposition**:

1. Wide-environmental compositions SHOULD lead with an explicit **framing-directive prefix sentence** declared at the top of the assembled prompt (not buried mid-block), e.g., "Wide cinematic 16:9 environmental shot — character occupies <40% of frame area; environment dominates ≥60%."
2. The `[CHARACTER]` block in wide compositions SHOULD use a **compressed character description** (~300 chars carrying only invariant-bearing identity tokens) rather than the full `portrait_subset` (~1500 chars) — the longer the character block, the stronger the portrait pull.
3. The composition's intended **subject-area-ratio** SHOULD be explicit and measurable: "Subject area: ≤40%; Environment area: ≥60%; subject NOT centered, occupies left- or right-third per rule-of-thirds composition" (or equivalent measurable directive).
4. Wide composition prompts SHOULD append negative framing tokens to the consumer `Avoid` list: "Avoid: portrait framing, head-and-shoulders composition, character filling frame, centered close-up."

**Runner-side implication**: image-gen runners that assemble Pattern 1 (character + location) or wide cinematic Pattern 4 (group + location) prompts should:
- Prefix the assembled prompt with the framing-directive sentence BEFORE the `[CHARACTER]` block, AND
- Substitute a compressed character subset (~300 chars; may be authored as `text_prompt.compressed_character_subset` in a future v0.2.x bundle revision) for the full `portrait_subset` when assembling wide compositions, AND
- Append the negative framing tokens to the consumer's `Avoid` list.

**Severity**: MEDIUM (output may still pass invariant gate but fails composition intent; consumer's planned use case for the wide image is unmet; iii_aggregate scoring catches this as "framing not as directed").

**Carry-forward**: pilot S4+ runners assemble Pattern 1 / Pattern 4 prompts with framing-directive prefix + compressed character block. A formal `text_prompt.compressed_character_subset` field may be elected for v0.2.x bundles to make the compression structural rather than per-runner. Closes F-VDP-01.S3.B + F-VDP-02.S1.A as a class.

### §5.9 Label hygiene in prompts — AMENDMENT 2026-05-24 (v0.2.2, additive)

**Empirical finding** (M-V1-2-F-VDP-02 S1 III pass, 2026-05-24): when Imagen 4 Ultra receives a prompt with character-identity tokens (e.g., `Science Stanley`, `Charlie the Quantum`) appearing in descriptive prose alongside in-frame surfaces (whiteboards, monitor screens, name badges, signs, paper notes), the model may render those identity tokens as literal in-frame text. Observed at VDP-02 S1 Pattern 2 integration scene `stanley_and_charlie_lab_check_in.png` where "STANLEY" appeared rendered on the whiteboard background twice as content text (F-VDP-02.S1.C). Same class of failure as §5.7 hex hygiene — prompt tokens rendered as surface text.

**Disposition**:

1. Character / location / object IDENTITY tokens (display names; e.g., "Science Stanley", "Charlie the Quantum", "Stanley's lab") SHOULD appear ONLY in the union-invariant header block of the assembled prompt — NOT in descriptive `[CHARACTER]`, `[ENVIRONMENT]`, or `[INVARIANTS]` prose blocks where they may be interpreted as content for in-frame text surfaces.
2. Identity tokens MAY appear in the prompt's `Avoid` list (e.g., `Avoid: in-frame text or labels, name banners`) — that is a directive about what the model should NOT render, not content to BE rendered.
3. When composing multi-entity scenes (Pattern 2 character+character or Pattern 4 group+location), the assembled prompt SHOULD reference each entity by short ROLE descriptor (e.g., "the man with auburn hair", "the cream-coated dog") in descriptive prose blocks; the FULL display name lives in the union-invariant header only.
4. NAME BADGES are a canon-opt-in special case: if a character's bundle declares an in-frame name badge as a canon invariant (Stanley's `STANLEY` name badge per stanley.yaml § text_prompt.portrait_subset), the badge text IS authorized in-frame content for that character only. Characters not declaring a canon-badge are subject to §5.9. v0.2.x bundle revisions may codify this as `invariants.has_in_frame_name_badge: bool` per character.

**Runner-side implication**: image-gen runners that assemble multi-entity prompts should:
- Render character display names in the union-invariant header block ONLY, AND
- Substitute role descriptors for identity tokens in descriptive prose blocks (the visual_dna bundle's `charm_signal.tells` field is a good source of role-descriptor language), AND
- Verify the consumer's canon-badge invariant declaration before allowing badge-text rendering.

**Severity**: MEDIUM (cosmetic; canon-invariants unaffected; communication intent impacted — Pattern 2 scene shows unintended STANLEY labels where the consumer wanted whiteboard content).

**Carry-forward**: pilot S2+ multi-entity prompts apply this discipline. A v0.2.x bundle revision MAY add an explicit `invariants.has_in_frame_name_badge: bool` field per character to make badge-bearing opt-in structural rather than implicit-by-prompt-content. Stanley's bundle would carry `true` (canon STANLEY badge); Charlie's bundle would carry `false` (no canon badge). Closes F-VDP-02.S1.C.

---

## §6 Worked example — full composition prompt (character + location)

Final demonstration: assembling a production-ready prompt for **"Stanley at lab whiteboard explaining a workflow diagram."**

### §6.1 Inputs
- `character`: `ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml`
- `location`: `ScienceStanley.aDNA/what/visual_dna/locations/lab_interior.yaml` (S3 deliverable; sketch in spec §4.2)

### §6.2 Assembled prompt (production-ready)

```text
16-bit pixel art (SNES-era); Studio Ghibli warmth; soft cel-shading with gradient
transitions on skin and ambient light; deliberate pixel-grid; dark line-work outlines
(#1f1414).

[CHARACTER — Stanley]
Science Stanley: early-30s; oval-narrow face with defined jawline; clean-shaven;
spiky warm-brown hair (auburn highlights #c97c5c, shadow #742950); bright warm-blue
eyes with engaged direct gaze; slight asymmetric smile; round blue-framed glasses;
white lab coat; purple turtleneck (#9d7cd8); STANLEY name badge at chest; standing
at lab whiteboard left of frame; gesturing with right hand toward a pixel-art
workflow diagram on the whiteboard; engaged-not-performing mentor energy with a
slight playful spark in the eyes.

[ENVIRONMENT — lab interior]
Inhabited night-lit lab/office; dark wood furniture with lived-in lab clutter;
whiteboard mid-right with workflow diagram (boxes-and-arrows; pixel-art hand-drawn);
warm-amber desk surface (foreground-right) with anchor objects (mug with steam,
notebook, framed photo); cool blue monitor glow modeling midground; glass-walled
clean lab visible through deep window behind (background atmosphere; soft DOF blur;
faint dust motes in lamp beam). Warm-cool dual lighting palette for depth.

[PALETTE]
Character: skin #fee1bf+#f3d7c3; hair #c97c5c+#742950; coat #fdfaf4-#dbdece;
turtleneck #9d7cd8.
Environment: desk wood #614133+#452c25; monitor glow #495556+#80847c; room
blacks #29272a+#201a1b.

[FRAMING]
16:9 wide environmental; rule-of-thirds: Stanley at left-third, whiteboard at
mid-right, foreground desk anchor objects at right-third; character + whiteboard
share focal hierarchy.

[LIGHTING]
Warm desk-lamp pool spotlighting workspace + cool blue monitor glow on Stanley's
face/hand + dim ambient room shadow + thin window-light bleed from background lab.

[INVARIANTS — all must hold]
round_glasses ✓ · spiky_brown_hair_auburn ✓ · white_lab_coat ✓ · purple_turtleneck ✓ ·
STANLEY_name_badge ✓ · age_early_30s ✓ · aesthetic_handsome_distinguished ✓ ·
hair_spikiness_canonical ✓ · oval_narrow_face_defined_jaw ✓ ·
warm_blue_eyes_engaged_gaze ✓ · warm_sincere_smile_playful_spark ✓ ·
warm_cool_dual_lighting ✓ · lived_in_clutter ✓ · dark_wood_furniture ✓.

[CHARM + ATMOSPHERE]
Charm: warm presenter energy; engaged-not-performing; approachable confidence.
Atmosphere: lived-in scholarly workshop; warm-night-lab quietude.

Avoid: photorealism; 3D rendering; mid-40s aging tells (silver temples; deep lines);
generic stock illustration; illegible whiteboard text; ambiguous silhouette.
```

### §6.3 Reference image selection

Per §1.8, the composition prefers `location.reference_image_set.contextual[*]` (a `Stanley_at_whiteboard` reference if present; otherwise fall back to `location.establishing[*]` + `character.portraits[*]` as separate frame-conditioning inputs to the consumer).

### §6.4 Expected consumer behavior

- **Gemini (Imagen 4 Ultra)**: text-to-image with this assembled prompt; ~1 generation pass.
- **ComfyForge (SDXL + LoRA)**: load `stanley_v0.1.safetensors` at weight 0.6, inject `scistanley` trigger word; reference whiteboard from location's `establishing` as IP-Adapter or ControlNet conditioning.
- **VideoForge**: use this assembled prompt as the per-frame baseline; preserve character identity via portrait references across frames; whiteboard diagram animates over the clip duration.
- **Social content**: select expression from `character.reference_image_set.expressions[*]` per post tone (laughing for celebratory; focused for technical); compose this scene with the selected expression.
- **Metaverse**: 3D-mesh derivative uses character's portrait references for PBR texturing; whiteboard becomes an interactive scene element.

---

## §7 Notes on extensibility

- **More than 4 DNAs**: theoretically supported (chain Pattern 1 + Pattern 2 + Pattern 3 + Pattern 4). Practically, agents should constrain to ≤4 DNAs per scene; beyond that, the prompt becomes brittle and consumer renderers lose identity-preservation fidelity.
- **New entity types** (e.g., creature, vehicle, garment): the schema is open to additions; new entity types compose with characters/locations/objects via the same merge protocol, with entity-type-specific guidance landing in a future composition_rules amendment.
- **Future Pattern 5 — character + character + object** (intimate two-shot with shared activity, e.g., two scientists sharing coffee): combines §2 (two characters) with §3 (shared object); no new merge logic — apply both protocols in sequence.

---

## §8 Re-merge rationale (CR7+SO7 citation)

Per CR7+SO7 in `CanvasForge.aDNA/CLAUDE.md`, this composition-rules document cites:

**`lattice-labs/who/coordination/coord_2026_04_16_forge_split.md`**

The composition protocol is load-bearing for Visual-DNA serving as a *substrate* primitive (not a deck-specific or comic-specific feature). Per the 2026-04-16 split-reversal, CanvasForge is the canvas substrate; Visual-DNA is the entity-identity layer that any canvas application (deck, comic, social card, video, metaverse render) consumes via the same protocol.

---

## References

- **Spec contract**: `spec_v0.2.md` (sibling deliverable)
- **Templates**: `schema/character_dna.yaml`, `schema/location_dna.yaml`, `schema/object_dna.yaml`
- **Empirical anchor**: `~/aDNA/ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml`
- **Mission charter**: `../../how/campaigns/campaign_canvasforge_v1_2/missions/mission_m_v1_2_f_visual_dna_pilot.md`
- **Re-merge rationale**: `~/aDNA/lattice-labs/who/coordination/coord_2026_04_16_forge_split.md`
