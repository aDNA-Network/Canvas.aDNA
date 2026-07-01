---
type: manifest
created: 2026-06-06
updated: 2026-06-30
last_edited_by: agent_mondrian
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

Canvas.aDNA is the **standard-bearer** *and* production owner. Since Production Tidy **pt09** (2026-06-17), **CanvasForge merged into Canvas** (Hermes → Mondrian) and **LiteratureForge was wound down** (Thoth, 2026-06-08) — the canvas **producers** now live **in-vault** at `what/production/` (7 conformant: `brief` · `deck` · `document` · `diagram` · `comic` · `letter` · `post`). Image generation stays in **ComfyUI**; web in **Astro**.

> **Repo visibility** (Git.aDNA P6 Wave 2, 2026-06-22): this vault's repo `github.com/aDNA-Network/Canvas.aDNA` (branch `master`) is now **GitHub-public**, class **P-released**, under Git.aDNA governance — visibility-flipped private→public via the agnostic `gitops_set_visibility` verb (ADR-013 host-role inversion; released-FOSS → GitHub-public). Fresh full-history `gitleaks` scan (62 commits) clean. Visibility-only — `origin` unchanged, no `rollback` remote, no Home §C shim. Git-ops declaration: `how/federation/git/CLAUDE.md`; doctrine: `CLAUDE.md` → `## Git-Ops`.

## Status

**✅ OPERATION KEYSTONE COMPLETE (2026-06-20) — the aDNA Canvas Standard v2.0.0 shipped as running infrastructure.** Operation Cartography (planning) closed 2026-06-13; the operator activated **Operation Keystone** (the build), now closed `status: completed`. **E0–E2** shipped the `canvas_std` **reference implementation** (validators · round-trip · conformance harness · v2.0.0 **JSON Schema** · `canvas-std` CLI; `pytest` 46/8, `ruff` clean). **E3** = the parity-gated **CanvasForge migration** onto `canvas_std` (full cutover 2026-06-14 via the `canvas/` wrapper + the `canvas_core→canvas_std` shim). **E4** stood up **three in-vault consumers** on `canvas_std` alone — `brief_consumer` 10/10 · `deck_generator` 16/16 · `document_generator` 37/37 (long-form LF-successor; the two-shelf firewall held, `canvas_std` git-diff 0). **E5.1** wired the `iii/` quality wrapper (III v0.5.0; 0 High/0 Med). **E6** validated cross-system parity (GREEN), confirmed the cutover, scheduled the shim retirement (2027-06-13), and closed the campaign (operator disposition: complete-with-PT-P5-tail). **LIP queue CLOSED 2026-06-20** — B1+B3+B2 shipped in **Standard v2.0.1** (errata patch on the v2.0.0 line; B2 = ride-on-text); B4 (pure-metadata) → v2.1.0 via a lattice-labs LIP. **Open tail → PT P5** (`canvas_core` relocation per ADR-004 + federation rollout E5.2 + v2.0.x registration). Ratified: `adr_000` · `adr_004` · `adr_005`. See `STATE.md` + `how/campaigns/campaign_canvas_genesis/` §Completion Summary + `missions/artifacts/e6_3_handoff_register.md`.

**✅ OPERATION ATELIER COMPLETE (2026-06-21) — both pt09-absorbed production layers built on `canvas_std`.** `campaign_canvas_production` (`status: completed`) stood up the remaining two producers: **`diagram_generator`** (36/36; all 5 diagram types — flowchart/sequence/class/state/gantt — aDNA-Native; native graph + a derived Mermaid `code` node) and **`comic_generator`** (87/87; multi-page/spread; `image`-class panels carrying the 6-layer prompt as `_reserved` metadata — **no rendering**, ComfyUI keeps pixels). With brief/deck/document, **all 5 in-vault producers** are conformant (final sweep **266 passed**; `ruff` clean; `canvas_std` firewall git-diff 0). The canvas-producer pattern is graduated to `what/context/context_canvas_producer_pattern.md`; 2 spec-gap errata (AT-1 graph extent unit · AT-2 free-form `surface`) → the LIP queue; structural `iii/` review `iii/feedback_2026_06_21_atelier_producers.md` (0 High / 0 Med). **Post-Atelier (2026-06-21): AT-1/AT-2 RESOLVED as editorial clarifications → aDNA Canvas Standard v2.0.2** (`extent` optional for non-paginated regions · `surface` an open vocabulary; no validator-behavior change; errata queue B1–B4 + AT-1/AT-2 fully drained). See `STATE.md` + `how/campaigns/campaign_canvas_production/` §Completion Summary + `what/decisions/lip_queue_disposition.md` §Closeout — AT-1/AT-2.

**✅ OPERATIONS PALETTE · SALON · ARMATURE COMPLETE (2026-06-22/23) — the output family completed and the three-leg thesis made runtime-real.** **Palette** completed the output family (`letter_generator` 17 · `post_generator` 20) and graduated the producer factory (`skill_canvas_producer_build` + `_scaffold`) → **7 in-vault producers** conformant. **Salon** proved *canvas-as-surface*: leg 2 (the `canvas_context` loader — load and traverse a canvas *as context* without rendering) + leg 3 (the interface-surface spec). **Armature** built the leg-3 **interaction runtime** and cut **Standard v2.2.0** (the first `canvas_std` firewall touch since Keystone, under `adr_007`) — all three legs now runtime-enabled. Full regression green (`canvas_std` **105/10** · `canvas_context` **58** · 7 producers **223**).

**▶ CURRENT — Operation Beacon (chartered 2026-06-30):** Canvas Standard **publish-hardening & governance unblock** — Tier 0–3 (docs · citable spec · conformance certification kit · a Canvas-local LIP home → v2.1.0 reconciliation); the gated follow-on to the **Operation Lodestar** review. See `STATE.md` + `how/campaigns/campaign_canvas_beacon/`.

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
| `absorbed` (pt09, 2026-06-17) | **CanvasForge → merged into Canvas** (Hermes → Mondrian) | deck/comic/diagram production now **in-vault** at `what/production/`; Canvas owns Standard *and* production |
| `superseded` (2026-06-08) | **LiteratureForge → wound down** (Thoth) | document-as-canvas now carried by the in-vault `document_generator` |
| `federates-with` | `III.aDNA` (Argus) | quality loops via an `iii/` wrapper — specify contracts, don't re-implement engines |
| `composes-with` | `VisualDNA.aDNA` (Pygmalion) · `ComfyUI.aDNA` | `brand_style_pack_ref` styling; raster engine (image generation) |
| `conforms-to` | `Astro.aDNA` forge pattern (`sf_forge_pattern_spec.md`) | consumer-integration contract (federation_ref + graft + version_policy) |
| `proposes-amendment-to` (D7, Δ2) | `aDNA.aDNA` core standard | canvas-as-primitive vs canvas-as-view — via a LIP |

## Entry Points

| Audience | Start Here | Then |
|----------|-----------|------|
| **Agents** | `CLAUDE.md` (auto-loaded) | `STATE.md` (Resume Here) → the current campaign in `how/campaigns/` |
| **Humans** | [`README.md`](README.md) → the [Standard explainer](what/docs/canvas_standard_explainer.md) | `what/decisions/adr_000_canvas_identity.md` → this `MANIFEST.md` → `STATE.md` |

## Naming note

`Canvas.aDNA` uses CamelCase (override of `skill_project_fork` snake_case validator, ADR-009 §3 exception — same grandfathered class as every sibling `*.aDNA` vault). Recorded in `who/coordination/coord_2026_06_06_naming_persona_exceptions.md`.
