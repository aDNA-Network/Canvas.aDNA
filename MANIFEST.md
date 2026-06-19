---
type: manifest
created: 2026-06-06
updated: 2026-06-19
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

**Execution — Operation Keystone; PHASES E0–E3 ✅, ⛔ HELD at E3→E4 (human gate).** Operation Cartography (planning) closed 2026-06-13; the operator activated **Operation Keystone** (`how/campaigns/campaign_canvas_genesis/`) — the build. **E0–E2** shipped the `canvas_std` **reference implementation** (validators · round-trip · conformance harness · v2.0.0 **JSON Schema** · `canvas-std` CLI; `pytest` 46/8, `ruff` clean). **E3** = the parity-gated **CanvasForge migration** onto `canvas_std` (full cutover 2026-06-14 — CanvasForge single-sources v2.0.0 via the `canvas/` wrapper + the `canvas_core`→`canvas_std` shim). **pt09** (2026-06-17) absorbed CanvasForge **production** (deck·comic·diagram) into this vault — Hermes merged into Mondrian; code relocates at **PT P5**. **ADR-004** (proposed 2026-06-19) fixes that P5 layout (`canvas_core` → `what/production/`). **E4** (LF-successor + net-new consumer) is the next phase and is a human gate. See `STATE.md`.

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
