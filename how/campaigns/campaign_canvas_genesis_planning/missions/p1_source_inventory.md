---
type: artifact
artifact_type: source_inventory
title: "P1 Source Inventory — aDNA Canvas Standard fork sources, classified"
campaign_id: campaign_canvas_genesis_planning
mission_id: mission_p1_source_inventory
phase: 1
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
status: review
tags: [artifact, inventory, canvas, standard, genesis, p1]
---

# P1 Deliverable 1 — Source Inventory (classified)

> **Phase P1 / Operation Cartography.** A labeled catalog of every artifact the **aDNA Canvas Standard
> v2.0.0** forks from. Each source is tagged **KEEP / EXTEND / SUPERSEDE / DEFER-TO-PRODUCER**. This is a
> *planning* artifact — nothing is migrated or modified; it tells P2 what to build the normative spec from.
> Companion: [[p1_fork_baseline]] (verbatim invariants/constants + inheritance + `_reserved` map + version pin).

## Classification rubric

| Label | Meaning | Lands in |
|-------|---------|----------|
| **KEEP** | A v1.0.0 invariant/rule/enum carried into v2.0.0 **unchanged** (the round-trippable Obsidian-baseline contract). | Canvas.aDNA Standard (verbatim) |
| **EXTEND** | Generalized **additively** in v2.0.0 across all 2D outputs (papers/decks/comics/sites/letters), via the namespaced `_reserved` block. | Canvas.aDNA Standard (generalized) |
| **SUPERSEDE** | Replaced by a clean **standalone successor** (chiefly: the *embedded-in-CanvasForge* standard framing → a normative spec Canvas.aDNA owns). | Canvas.aDNA Standard (rewrite) |
| **DEFER-TO-PRODUCER** | Application-specific design/rendering/pipeline logic — stays in CanvasForge / ComfyForge / LF-successor (substrate-neutrality test C8). | Producer vault (unchanged) |

**Method.** Built via 4 parallel read-and-classify passes over the source corpus; verbatim constants and
invariants transcribed (see companion). Path shorthands: **AC** = `CanvasForge.aDNA/what/context/advanced_canvas/`
· **CC** = `CanvasForge.aDNA/what/code/canvas_core/` · **LFS** = `Archive.aDNA/LiteratureForge.aDNA/what/specs/`.

---

## §A — Canvas Standard v1.0.0 corpus (`AC/`, 7 artifacts)

| # | Artifact | Path | ~lines | Label | Rationale | Target in v2.0.0 |
|---|----------|------|-------:|-------|-----------|------------------|
| A1 | `context_advanced_canvas_schema.md` | AC | 204 | **KEEP** | The JSON node/edge/metadata schema + `_reserved` carrier — the round-trippable Obsidian/Advanced-Canvas baseline contract. | The v2.0.0 **schema floor**; aDNA extensions added additively in `_reserved`. |
| A2 | `context_advanced_canvas_roundtrip.md` | AC | 102 | **KEEP** | Round-Trip Protocol v1.0 (authority matrix, sync-hash, 3-way merge, advisory Canvas→YAML) — core interop invariant. | The v2.0.0 **round-trip contract** (generalize "`.lattice.yaml`" → "authoritative source"; rule stands). |
| A3 | `context_advanced_canvas_standard.md` | AC | 104 | **SUPERSEDE** | *Is* the v1.0.0 standard, but framed as embedded-in-CanvasForge context and hard-bound to lattice node types (module/dataset/reasoning/process). | Replaced by a **standalone normative spec** owned by Canvas.aDNA; its invariants re-stated cleanly. |
| A4 | `advanced_canvas.md` | AC | 47 | **DEFER-TO-PRODUCER** | Obsidian/Dataview folder-note tied to CanvasForge's directory + banners; no normative content. | Stays in CanvasForge. |
| A5 | `context_advanced_canvas_validation_results.md` | AC | 183 | **DEFER-TO-PRODUCER** | CanvasForge-specific M8 empirical run (builder/test counts) — evidence, not a rule. | Stays in CanvasForge; **informs** (≠ is) the P3 conformance-suite spec. |
| A6 | `context_advanced_canvas_tooling_gaps.md` | AC | 90 | **DEFER-TO-PRODUCER** | Tracks CanvasForge tool state (G1–G12 mission tickets) — implementation backlog. | Stays in CanvasForge; Canvas.aDNA owns gap *contracts* (sync-hash, `_reserved`), not the tickets. |
| A7 | `graft_manifest.yaml` | AC | 300 | **DEFER-TO-PRODUCER** | One-way `lattice-labs → CanvasForge` migration audit ledger (sha256 provenance); no normative/federation content. | Stays in CanvasForge; Canvas.aDNA authors its **own** fork-baseline manifest. |

> **Note (no EXTEND in §A):** no §A file is *already* generalized beyond lattice pipelines + decks. EXTEND work
> is net-new in P2, performed **on** the KEEP invariants (A1/A2) and the SUPERSEDE target (A3) — not a relabel.

---

## §B — Reference-implementation source (`CC/`, 3 artifacts)

> Option P (D1, ratified P0) makes Canvas.aDNA the owner of a reference impl at `what/code/canvas_std/`
> (declared, **built later** — C3). ★ marks natural **extraction targets** into that future home.

| # | Artifact | Path | ~lines | Label | Rationale | Target |
|---|----------|------|-------:|-------|-----------|--------|
| B1 | Constants block (`VALID_*` ×10, `TYPE_MAPPING`, `EDGE_TYPE_MAPPING`) | CC/`core.py` | ~85 | **KEEP** + **EXTEND** ★ | The 10 `VALID_*` enums *are* the baseline-fidelity vocabulary (a valid aDNA canvas must degrade to these) → KEEP. The two semantic maps cover only lattice types today → **EXTEND** into a cross-output component taxonomy under `_reserved`. | ★ `canvas_std/` schema core. (Verbatim values in companion.) |
| B2 | `CanvasBuilder` class | CC/`core.py` | ~1000 | **EXTEND** ★ (split) | Normative core — `build`/`read_back`/`diff`/`merge`/`validate`/`compute_sync_hash`/`preserve_positions` + `add_semantic_node/edge` + node/edge model + `_lattice_meta` injector — is exactly the validator·round-trip·conformance trio Canvas.aDNA owns. `layout_*`, `selection_board`, `save`, accessors are app convenience. | ★ `canvas_std/` for the normative slice; **CanvasForge** keeps layout/selection/I-O behind a thin builder facade. |
| B3 | `pdf_export.py` (ADR-010) · `gdoc_export.py` (ADR-011) | CC | 144 · 693 | **DEFER-TO-PRODUCER** | App-specific runtimes (PIL/CMYK PDF carrier; Google Docs/Drive API + Imagen carriage). Canvas.aDNA "does NOT own rendering runtimes." `gdoc`'s `DocElement` taxonomy is **noted as input** to the EXTEND component taxonomy. | **CanvasForge** (engines stay); Canvas.aDNA may write a normative **export-carrier contract** they conform to. |

**Naming caveat for P2:** there is no literal `to_canvas`/`from_canvas` — `build()`(+`save()`) and `read_back()`
fill those roles. Alias them explicitly at extraction so the conformance vocabulary matches the API.

---

## §C — Design context corpus (`AC/`, 15 artifacts)

> Default here is **DEFER-TO-PRODUCER** (design taste / coordinate math / `PresentationBuilder` proposals).
> **⚑** marks schema/typed-vocabulary hiding in a "design" doc — those are Standard-ownership candidates (EXTEND).

| # | Artifact (`AC/context_advanced_canvas_…`) | ~lines | Label | Rationale | Target |
|---|---|-------:|-------|-----------|--------|
| C1 | `…visual_vocabulary.md` | 98 | **EXTEND** ⚑ | Typed node-type→`shape` enum + color-slot codes + edge `pathStyle`/`arrow`/`border` enums — the component model's shape/edge vocabulary in all but name. | Canvas.aDNA component model (generalize type→shape; strip Lattice-specific color semantics). |
| C2 | `…css_classes.md` | 111 | **EXTEND** ⚑ | The `cssclasses` → `data-css-classes` DOM-attribute **binding contract** (how a class token serializes into node `styleAttributes`). | Canvas.aDNA (extract the binding; defer the class list + palette). |
| C3 | `…design_system.md` | 215 | **EXTEND** ⚑ (split) | `styleAttributes.latticeRole` → `data-lattice-role` **role-attribute namespace + serialization** is a component-model extension point. Palette/spacing/theme-profiles are taste. | Canvas.aDNA (role-attr schema) + CanvasForge (palette/themes). |
| C4 | `…presentation_mode.md` | 113 | **EXTEND** ⚑ (partial) | `isStartNode` flag + group/portal slide-graph wiring is normative panel/link traversal semantics. Only the px sizing table is taste. | Canvas.aDNA (panel/link semantics) + CanvasForge (sizing). |
| C5 | `…agentic_composition.md` | 193 | **DEFER-TO-PRODUCER** | CanvasBuilder node-strategy decision tree + spacing constants — generation guidance. | CanvasForge |
| C6 | `…composition_patterns.md` | 198 | **DEFER-TO-PRODUCER** | Deck color-banding / weight sequencing / interior-layout catalog — producer composition. | CanvasForge |
| C7 | `…slide_layout_principles.md` | 190 | **DEFER-TO-PRODUCER** | PB/CB coordinate math + layout constants (incl. a logged coordinate bug) — engine-specific. | CanvasForge |
| C8 | `…diagram_patterns.md` | 347 | **DEFER-TO-PRODUCER** | Architecture/flowchart/sequence/Mermaid→canvas recipes + PB method proposals — rendering. | CanvasForge |
| C9 | `…typography_system.md` | 177 | **DEFER-TO-PRODUCER** | Modular type-scale theory, font pairing, measure/leading — design taste; `--cl-*` vars are producer CSS. | CanvasForge |
| C10 | `…color_accessibility.md` | 212 | **DEFER-TO-PRODUCER** | WCAG/CVD audit of the Tokyo Night palette — palette-specific accessibility taste. | CanvasForge |
| C11 | `…design_modern_patterns.md` | 217 | **DEFER-TO-PRODUCER** | Stripe/Linear/Vercel/Apple style DNA + SaaS templates + density norms — brand taste. | CanvasForge |
| C12 | `…design_tufte.md` | 163 | **DEFER-TO-PRODUCER** | Tufte principles mapped to PB `review()` checks — quality heuristics. | CanvasForge |
| C13 | `…data_visualization.md` | 224 | **DEFER-TO-PRODUCER** | Chart selection + Tufte/Cairo/Schwabish + PB chart enhancements — viz taste + pipeline. | CanvasForge |
| C14 | `…scientific_communication.md` | 168 | **DEFER-TO-PRODUCER** | Assertion-evidence, figure/citation conventions, PB slide-type proposals — domain comms taste. | CanvasForge |
| C15 | `…visual_elements.md` | 151 | **DEFER-TO-PRODUCER** | Image taxonomy + Imagen prompt engineering + cost table — image-gen. | CanvasForge → ComfyForge |

> **⚑ Convergence note:** C1–C4 plus the round-trip/`_reserved` contract already assumed by C14 and C4
> converge on the same conclusion — the typed component vocabulary, css-class & role-attribute bindings,
> and panel/link traversal semantics belong to the **Standard**, while the producers consume them. These four
> are the P2 component-model (D4) and panel/link-semantics (D5) seed material.

---

## §D — LiteratureForge specs (`LFS/`, 3 artifacts) — D3 fork sources

| # | Spec | Path | ~lines | Label | Rationale | Target |
|---|------|------|-------:|-------|-----------|--------|
| D1 | `spec_visual_contract.md` (V1–V8 + X1–X14) | LFS | 209 | **EXTEND** | The **substrate axis** (`canvas \| raster`) is a typed visual-component routing model; `style_lock`/`brand_style_pack_ref`, per-surface geometry (`aspect_ratio_table`/`surface_subclass`/`substrate_inheritance`), `orphan_detector`/`naming_convention` (label/ref link-existence), and `export_round_trip` are component-schema/link-semantics. §3 engine routing + `scorecard`/`visual_voices` review DEFER. | Canvas.aDNA **visual-component contract**; routing/review → CanvasForge/ComfyForge/III. |
| D2 | `spec_format_contract.md` (F1–F7) | LFS | 150 | **EXTEND** | Structural kernel: **`sections` (ordered, order-locked)** = long-form reading-order/flow; `round_trip_surface` **already cross-refs the Canvas Round-Trip Protocol**; `output_surfaces` (canonical/derived) = multi-surface model; `length_window` = pagination/extent. Template-resolver + per-genre instances (NeurIPS/NIH/SF424) DEFER. | Canvas.aDNA **panel/link flow + pagination + round-trip + multi-surface** (D5); template/genre logic → LF-successor. |
| D3 | `spec_genre_submodule.md` (5-part bundle) | LFS | 159 | **DEFER-TO-PRODUCER** | Dominantly a writing-composition method (trap-pack / reviewer-voices / reward-rubric + 5-step generate→review lifecycle + voice-fidelity). Only the seam-header + overlay-as-parent-diff primitive is a minor EXTEND. | **LF-successor producer**; seam-header/overlay primitive optionally → Standard. |

**D3 decision signal (reported, not decided — resolve at P2):** evidence leans toward *document-AS-canvas*
(absorb/extend) — the format-spec's `round_trip_surface` **already contractually couples to the Canvas
Round-Trip Protocol**, and the visual-spec's substrate axis + label/ref link-checking are canvas-native. But
every spec deliberately draws a clean producer boundary ("specify contracts, not engines"), and the
genre-submodule's `federation_ref` seams show the federated-peer mechanism is already live. Net: the
**schema/flow/round-trip layer wants to live in the Standard; the writing pipeline does not** — compatible with
either D3 Option A (absorb) or Option B (federated peer). The strongest single absorb-signal is the
already-existing round-trip cross-reference.

---

## §E — Inherited template scaffold (archived this mission)

> Generic-aDNA fork scaffold, **not Canvas-canonical**. Per operator decision (2026-06-12), archived to in-vault
> `_inherited_scaffold/` holders (SO-6 archive-never-delete) to free the `adr_001+` namespace for Canvas's real
> ADRs (D2–D7) at P2. History preserved via `git mv`.

| # | Artifact | From → To | Label | Disposition |
|---|----------|-----------|-------|-------------|
| E1 | `adr_001_obsidian_as_knowledge_platform.md` | `what/decisions/` → `what/decisions/_inherited_scaffold/` | **SUPERSEDE** | Archived; generic example. Canvas ADR namespace begins at `adr_000`. |
| E2 | `adr_002_yaml_as_lattice_format.md` | same | **SUPERSEDE** | Archived; generic example. |
| E3 | `adr_003_system_configuration_as_context_topic.md` | same | **SUPERSEDE** | Archived; generic example. |
| E4 | `campaign_adna_workspace_upgrade/` | `how/campaigns/` → `how/campaigns/_inherited_scaffold/` | **SUPERSEDE** | Archived; generic example campaign. |

---

## Roll-up

**Label distribution (28 source artifacts, §A–§D):**

| Label | Count | Artifacts |
|-------|------:|-----------|
| **KEEP** | 3 | A1 schema, A2 round-trip, B1 `VALID_*` enums (the enum half) |
| **EXTEND** | 8 | B1 semantic maps, B2 builder core, C1–C4, D1, D2 |
| **SUPERSEDE** | 1 | A3 embedded standard doc *(+ 4 archived scaffold artifacts, §E)* |
| **DEFER-TO-PRODUCER** | 16 | A4–A7, B3 (×2 exports), C5–C15 |

**What feeds P2 (Standard spec):**
- **Normative floor (KEEP):** the §A1 schema + §A2 round-trip contract + §B1 `VALID_*` enums → the v2.0.0 base
  that degrades to a valid Obsidian canvas.
- **Spec rewrite (SUPERSEDE):** §A3 → a standalone normative `spec_adna_canvas_standard.md`.
- **Component model (D4) + panel/link semantics (D5):** §B1 semantic maps + §C1–C4 ⚑ + §D1/§D2 EXTEND set.
- **D2 (CanvasForge relationship):** §B confirms a clean extraction boundary (normative core ★ vs. producer
  convenience) — tilts toward Option A (extract), consistent with the P0 Option-P cascade.
- **D3 (LF seam):** §D signal — absorb the schema/flow/round-trip, leave the writing pipeline; round-trip
  cross-reference already exists.
- **Reference impl (Option P):** §B ★ extraction targets pre-mapped for the execution campaign.

## Related
- [[p1_fork_baseline]] — verbatim invariants/constants + inheritance + `_reserved` map + version pin.
- [[campaign_canvas_genesis_planning]] · [[mission_p1_source_inventory]] · `what/decisions/adr_000_canvas_identity.md` · `what/decisions/decision_register_genesis.md`.
