---
type: manifest
created: 2026-06-06
updated: 2026-06-21
last_edited_by: agent_stanley
persona: Mondrian (locked — P0 2026-06-06)
category: Platform.aDNA (standard-bearer — Δ1 Option P, locked P0 2026-06-06)
tags: [manifest, governance, canvas, standard, platform]
---

# Canvas.aDNA — Project Manifest

## Project Identity

**Canvas.aDNA** (display: **Canvas**) is a **Platform.aDNA** project (standard-bearer) that **owns the aDNA Canvas Standard** — an agentic-context-native fork of the Obsidian **Advanced Canvas** / **JSON Canvas** standard, maintained by aDNA Labs — **and ships its runnable reference tooling** (validators · round-trip converters · conformance harness; code-as-WHAT-object at `what/code/canvas_std/`, built in the execution campaign). Category locked at P0 (Δ1, Option P).

The thesis: a *canvas* — a possibly-linked set of panels carrying positioned **text · typography · image · video · shape · embed · link** components — is a near-universal **output primitive**. Papers, blog posts, sites, letters, pitch decks, comics, PDFs, and Google Docs are all assemblies of the same component classes with specified position and qualities. By forking and evolving Advanced Canvas into an agentic-context-**native**, agentic-context-**developed** standard, canvas becomes simultaneously:

- **(a) a core context object** in the agentic context graph (read AS context, render AS output),
- **(b) a primary human↔AI / human↔human interaction surface**, and
- **(c) the shared substrate** for a broad range of two-dimensional outputs produced with the same class of tools, context, and learning — modular per component class.

Canvas.aDNA is the **standard-bearer**. **CanvasForge** (Hermes — spatial substrate; decks/comics) and **LiteratureForge** (Thoth — document forge) are **producers** that consume the Standard.

## Status

**✅ OPERATION KEYSTONE COMPLETE (2026-06-20) — the aDNA Canvas Standard v2.0.0 shipped as running infrastructure.** Operation Cartography (planning) closed 2026-06-13; the operator activated **Operation Keystone** (the build), now closed `status: completed`. **E0–E2** shipped the `canvas_std` **reference implementation** (validators · round-trip · conformance harness · v2.0.0 **JSON Schema** · `canvas-std` CLI; `pytest` 46/8, `ruff` clean). **E3** = the parity-gated **CanvasForge migration** onto `canvas_std` (full cutover 2026-06-14 via the `canvas/` wrapper + the `canvas_core→canvas_std` shim). **E4** stood up **three in-vault consumers** on `canvas_std` alone — `brief_consumer` 10/10 · `deck_generator` 16/16 · `document_generator` 37/37 (long-form LF-successor; the two-shelf firewall held, `canvas_std` git-diff 0). **E5.1** wired the `iii/` quality wrapper (III v0.5.0; 0 High/0 Med). **E6** validated cross-system parity (GREEN), confirmed the cutover, scheduled the shim retirement (2027-06-13), and closed the campaign (operator disposition: complete-with-PT-P5-tail). **LIP queue CLOSED 2026-06-20** — B1+B3+B2 shipped in **Standard v2.0.1** (errata patch on the v2.0.0 line; B2 = ride-on-text); B4 (pure-metadata) → v2.1.0 via a lattice-labs LIP. **Open tail → PT P5** (`canvas_core` relocation per ADR-004 + federation rollout E5.2 + v2.0.x registration). Ratified: `adr_000` · `adr_004` · `adr_005`. See `STATE.md` + `how/campaigns/campaign_canvas_genesis/` §Completion Summary + `missions/artifacts/e6_3_handoff_register.md`.

**✅ OPERATION ATELIER COMPLETE (2026-06-21) — both pt09-absorbed production layers built on `canvas_std`.** `campaign_canvas_production` (`status: completed`) stood up the remaining two producers: **`diagram_generator`** (36/36; all 5 diagram types — flowchart/sequence/class/state/gantt — aDNA-Native; native graph + a derived Mermaid `code` node) and **`comic_generator`** (87/87; multi-page/spread; `image`-class panels carrying the 6-layer prompt as `_reserved` metadata — **no rendering**, ComfyUI keeps pixels). With brief/deck/document, **all 5 in-vault producers** are conformant (final sweep **266 passed**; `ruff` clean; `canvas_std` firewall git-diff 0). The canvas-producer pattern is graduated to `what/context/context_canvas_producer_pattern.md`; 2 spec-gap errata (AT-1 graph extent unit · AT-2 free-form `surface`) → the LIP queue; structural `iii/` review `iii/feedback_2026_06_21_atelier_producers.md` (0 High / 0 Med). See `STATE.md` + `how/campaigns/campaign_canvas_production/` §Completion Summary.

## Architecture (aDNA triad)

```
Canvas.aDNA/
├── what/   # Knowledge — the Standard spec, component model, decisions (ADRs), context corpus
├── how/    # Operations — Operation Keystone campaign, missions, sessions, templates, skills
└── who/    # People — governance, coordination (naming/persona notes)
```

Base ontology: 14 entity types (WHO 3 · WHAT 4 · HOW 7) — see CLAUDE.md § Domain Knowledge. Domain extensions (e.g. a `what/specs/` standard-spec leg) are added through the genesis campaign.

## Relationships

| Relationship | Vault | Note |
|---|---|---|
| `forks` | Obsidian Advanced Canvas / JSON Canvas | upstream baseline (pin at P1; brief cites Advanced Canvas v5.6.6 — confirm) |
| `extracts-standard-from` (proposed, D2) | `CanvasForge.aDNA` (Hermes) | Canvas Standard v1.0.0 currently embedded in `canvas_core`; producer post-extraction |
| `unifies-seam-with` (D3) | `LiteratureForge.aDNA` (Thoth) | document-as-canvas; reconcile with Amendment-02 Document-DNA engine (complements) |
| `federates-with` | `III.aDNA` (Argus) | quality loops via an `iii/` wrapper — specify contracts, don't re-implement engines |
| `composes-with` | `VisualDNA.aDNA` (Pygmalion) · `ComfyForge.aDNA` | `brand_style_pack_ref` styling; raster engine |
| `conforms-to` | `SiteForge.aDNA` forge pattern (`sf_forge_pattern_spec.md`) | consumer-integration contract (federation_ref + graft + version_policy) |
| `proposes-amendment-to` (D7, Δ2) | `aDNA.aDNA` core standard | canvas-as-primitive vs canvas-as-view — via a LIP |

## Entry Points

| Audience | Start Here | Then |
|----------|-----------|------|
| **Agents** | `CLAUDE.md` (auto-loaded) | `STATE.md` (Resume Here) → `how/campaigns/campaign_canvas_genesis/` (Operation Keystone) |
| **Humans** | this `MANIFEST.md` | `what/decisions/adr_000_canvas_identity.md` → `STATE.md` |

## Naming note

`Canvas.aDNA` uses CamelCase (override of `skill_project_fork` snake_case validator, ADR-009 §3 exception — same grandfathered class as every sibling `*.aDNA` vault). Recorded in `who/coordination/coord_2026_06_06_naming_persona_exceptions.md`.
