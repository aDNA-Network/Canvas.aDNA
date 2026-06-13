---
type: artifact
artifact_type: harmonization_plan
title: "P5 Harmonization Plan — ecosystem impact of aDNA Canvas Standard v2.0.0"
campaign_id: campaign_canvas_genesis_planning
mission_id: mission_p5_harmonization
phase: 5
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
status: review
tags: [artifact, harmonization, canvas, standard, genesis, p5]
---

# P5 — Ecosystem Harmonization Plan

> **Phase P5 / Operation Cartography (final).** The file-by-file impact of adopting **aDNA Canvas Standard v2.0.0**
> across the ecosystem, the v1.0.0→v2.0.0 deprecation-shim strategy, and upstream/LIP notes. All impact is
> **executed by Operation Keystone** (`campaign_canvas_genesis`), gated and reversible — **nothing here changes
> another vault now** (C3). This plan is the map Keystone follows.

## 1. Impact matrix (by vault)

Disposition legend: **KEEP** (unchanged) · **REFERENCE** (becomes a `federation_ref`, not a copy) · **SUPERSEDE**
(replaced by the v2.0.0 spec) · **EXTRACT** (moves into `canvas_std`) · **MIGRATE** (rewired onto v2.0.0) ·
**NEW** (added) · **NO-OP** (verified unaffected). "Keystone" = the owning execution phase.

### CanvasForge.aDNA (Hermes) — the primary migration
| Artifact | Disposition | Keystone |
|----------|-------------|----------|
| `what/code/canvas_core/core.py` — `CanvasBuilder` normative core (`build`/`read_back`/`diff`/`merge`/`validate`/`compute_sync_hash`/`preserve_positions` + semantic mappers + `VALID_*`) | **EXTRACT** → `Canvas.aDNA/what/code/canvas_std/` | E0.2, E1, E3.2 |
| `canvas_core/` `layout_*`, `selection_board`, `save`, accessors | **KEEP** (producer convenience) | — |
| `canvas_core/pdf_export.py`, `gdoc_export.py` | **KEEP** (producer export engines; conform to the export-carrier contract) | — |
| `what/context/advanced_canvas/context_advanced_canvas_standard.md` (embedded v1.0.0) | **SUPERSEDE** by `spec_adna_canvas_standard` | E3.4 |
| `…/context_advanced_canvas_schema.md`, `…_roundtrip.md` | **REFERENCE** (now the v2.0.0 spec floor; cite, don't re-derive) | E3.2 |
| `…/advanced_canvas/` design docs (typography/color/composition/…) | **KEEP** (producer design taste) | — |
| `iii/` wrapper (10-trap canvas-visual bridge + 5-voice review) | **KEEP**; the VR1–VR5 + trap **schema** ownership clarifies to Canvas.aDNA (engines stay) | E5.1 |
| **`canvas/` federation wrapper** | **NEW** (`federation_ref` to Canvas.aDNA v2.0.0) | E3.1 |

### Archive.aDNA/LiteratureForge.aDNA (Thoth, wound down)
| Artifact | Disposition | Keystone |
|----------|-------------|----------|
| `what/specs/spec_visual_contract.md` (V1–V8/X1–X14) | **MIGRATE** — contract absorbed into `spec_component_model` (visual-component contract); engine routing → producer | E4.2 |
| `what/specs/spec_format_contract.md` (F1–F7) | **MIGRATE** — `sections`/`output_surfaces`/`round_trip_surface` absorbed into `spec_panel_link_semantics` + round-trip v2 | E4.2 |
| `what/specs/spec_genre_submodule.md` (5-part) | **KEEP** in the LF-successor producer (writing pipeline; D3 = federated) | E4.1 |
| Archived vault itself | **KEEP** archived (quarry); the **LF-successor** is a NEW federated producer | E4.1 |

### SiteForge.aDNA (the forge pattern parent)
| Artifact | Disposition | Keystone |
|----------|-------------|----------|
| `what/artifacts/sf_forge_pattern_spec.md` | **KEEP** (Canvas's `spec_federation_contract` conforms to it) | — |
| SiteForge as a canvas consumer (if/when it emits canvases) | **NEW** `canvas/` wrapper (optional) | E5.2 |

### VisualDNA.aDNA (Pygmalion)
| Artifact | Disposition | Keystone |
|----------|-------------|----------|
| Brand-pack bundles (`brand_style_pack_ref` target) | **KEEP**; `spec_component_model` §6 references them via `federation_ref` (producer-resolved) | E4/E5 |
| `consumer_compat` block | **NEW** (optional) note for canvas component bindings | E5.2 |

### III.aDNA (Argus)
| Artifact | Disposition | Keystone |
|----------|-------------|----------|
| `context_iii_canvas_visual` pack (VR1–VR5 + trap baseline) | **REFERENCE** — the *contract* is Canvas.aDNA-owned (standard-bearer inversion); III keeps the **engine** (`module_iii_inspect_visual`, oracle lattice, review skill) | E5.1 |
| Possible III ADR note acknowledging Canvas.aDNA owns the canvas review contract | **NEW** (upstream proposal; §3) | E5.1 |

### SS / CC consumer wrappers (ScienceStanley, ContextCommons)
| Artifact | Disposition | Keystone |
|----------|-------------|----------|
| `siteforge/` / forge wrappers that consume CanvasForge **output** | **NO-OP** — they consume CanvasForge artifacts, not `canvas_core` internals; the extraction is transparent to them | E6 (verify) |

## 2. Deprecation-shim strategy (v1.0.0 → v2.0.0)

- **Mechanism:** after EXTRACT (E3.2), `canvasforge.canvas_core` re-exports from `canvas_std` — mirroring the
  working `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` precedent. Both import
  paths resolve during the grace window.
- **Grace window:** default **12 months** (matching the lattice-protocol shim's 2027-05-04 horizon); registered
  in the `Home.aDNA` shim ledger at extraction (Standing Rule 9, shim-window discipline).
- **Cutover:** only on a green parity gate (Wilhelm 8.80 / Issue 01 8.43) + conformance-suite green + `iii/`
  review ≥ baseline + operator gate (Keystone E3.3/E3.4, E6.2).
- **Rollback:** revert the wrapper repoint; the shim keeps the old path live → zero consumer breakage.
- **Version policy:** consumers pin `version_policy: minor` (review on minor, re-validate on major). v1.0.0 is a
  retired internal line; v2.0.0 is the published successor.

## 3. Upstream-contribution / LIP notes

- **Δ2 canvas-as-primitive LIP** ([[lip_draft_canvas_as_primitive]]) — submit to the `lattice-labs` LIP process
  if/when consumer evidence warrants; keep-as-view is the v2.0.0 default (no core change).
- **III ownership note** — propose an III ADR/learning-store note recording that the canvas review *contract*
  (VR1–VR5 + trap schema) is owned by Canvas.aDNA (the standard-bearer), III owns the engines. Clean precedent
  for "framework owns engine, standard-bearer owns contract."
- **`version_policy: tracking`** — surfaced (federation contract §3) as a pre-1.0 wild value not in the canonical
  sf_forge spec; propose canonicalizing it (or formally restricting to `minor`/`locked`) to SiteForge.
- **JSON Canvas floor** — confirm the base format version (assumed 1.0; uncited in the v1.0.0 corpus) at E0.

## 4. Router-row finalize

The workspace router row (`~/aDNA/CLAUDE.md`) was finalized this phase to the settled identity: *Platform.aDNA
(Mondrian) — standard-bearer owning the aDNA Canvas Standard **v2.0.0** + its `canvas_std` reference tooling;
CanvasForge + LF-successor are producers.* Per Standing Rule 7 the row carries routing identity only; campaign
state stays in `STATE.md`. *(Note: the root router was also touched externally on 2026-06-12; the Canvas row
finalize is independent of that change.)*

## 5. Related
- [[campaign_canvas_genesis_planning]] (Operation Cartography) · [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone — executes this map) · [[p1_source_inventory]] · [[p1_fork_baseline]] · the v2.0.0 spec set + `adr_001/002/003`.
