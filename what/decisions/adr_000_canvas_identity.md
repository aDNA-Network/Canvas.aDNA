---
type: decision
adr_id: "000"
title: "Project Identity — Canvas.aDNA, the aDNA Canvas Standard"
status: ratified
created: 2026-06-06
updated: 2026-06-12
last_edited_by: agent_stanley
signed_by: Stanley (operator) — P0 gate 2026-06-06
annotations: "P1 resolution 2026-06-12 — §4 baseline pinned (PIN-A: Advanced Canvas v5.6.6 + JSON Canvas 1.0)"
supersedes:
superseded_by:
tags: [adr, identity, canvas, standard, framework, genesis]
---

# ADR-000: Project Identity — Canvas.aDNA

## Status

**Ratified** — 2026-06-06 (Stanley, operator), at the **P0 gate** (Operation Cartography). Operator locks:
**persona = Mondrian**; **category = Platform.aDNA (standard-bearer), Option P** (Δ1 resolved — Canvas.aDNA
ships the runnable reference tooling, vault+code split); **scope boundary confirmed** as §3 (plus the
reference implementation). P0 closed; P1 may open on operator go.

## Context

CanvasForge (Hermes) embeds a "Canvas Standard v1.0.0" inside its `canvas_core` substrate (decks/comics);
LiteratureForge (Thoth) routes visuals out to that substrate via `spec_visual_contract.md`. The operator's
thesis (architect brief, 2026-06-06): a *canvas* — possibly-linked panels of positioned text/typography/
image/video/shape/embed/link components — is a near-universal **output primitive** spanning papers, posts,
sites, letters, decks, comics, PDFs, Google Docs. Forking Obsidian **Advanced Canvas** / **JSON Canvas** into
an agentic-context-native, agentic-context-developed standard makes canvas (a) a core context object, (b) a
human↔AI / human↔human interaction surface, and (c) the shared substrate for 2D outputs. **Canvas.aDNA** owns
that Standard; CanvasForge + LiteratureForge become **producers** that consume it.

Repo verification (2026-06-06) confirms the substrate already exports PDF (`pdf_export.py`, ADR-010) and
Google Docs (`gdoc_export.py`, ADR-011); the v1.0.0 standard + Round-Trip Protocol are real; a LIP process
exists; the lattice-protocol→canvasforge extraction-shim is a working precedent. Two **deltas** sharpen this
ADR (below).

## Decision

### 1. Category: Platform.aDNA (standard-bearer) — **Δ1 resolved, Option P**

**Locked (operator, P0):** Canvas.aDNA is a **Platform.aDNA** that governs the aDNA Canvas Standard **and ships
its runnable reference tooling** — validators, round-trip converters, and the conformance harness. This is the
**Option P** resolution of Δ1: because the Standard ships runnable code, the pure-Framework definition
(`spec_framework_ecosystem.md`: "produce no primary artifact and deploy no runtime") does not apply.

- **Vault+code split.** The reference implementation has a **code-as-WHAT-object** home at `what/code/canvas_std/`
  (single-repo, per the VideoForge Amendment-1 precedent). It is **declared now, built later** in the execution
  campaign (C3 — no runtime built this campaign).
- **"Standard-bearer" framing.** Canvas.aDNA is a Platform whose deployable system *is* the Standard + its
  reference tooling (not a partner-institution service). Whether this warrants a distinct `Standard.aDNA`
  sub-category is a minor open question for P4/LIP; it does not block P0.
- **Cascade to D2.** Option P **tilts D2 toward extraction** (the standard machinery — schema, validators,
  round-trip — lives here; CanvasForge becomes a producer consuming it). D2 itself is resolved at P2.

### 2. Persona: Mondrian — **locked**

**Locked (operator, P0): Mondrian** — Piet Mondrian reduced composition to a disciplined grid of lines and
primary fields in pursuit of a *universal* visual language from the fewest elements. The vault does the same
for agentic media: it reduces any 2D output to a rigorous grammar of typed components on a canvas. Distinct
from all existing Lattice personas (Berthier, Hermes, Iris, Argus, Ariadne, Pygmalion, Thoth, …).
*(Alternatives Seshat / Mercator considered and set aside.)*

### 3. Mission scope

Canvas.aDNA provides a forked, federable, agentic-context-native canvas standard for any 2D output, with:
a normative spec; a modular component model (per component class); panel/link semantics for non-DAG outputs
(flow/pagination/reading-order); a round-trip contract to baseline Obsidian; a conformance-suite spec; a
consumer federation contract; and LIP-style versioning/governance.

**Owns** (confirmed P0): schema · component model · round-trip contract · conformance-suite spec ·
federation contract · versioning/governance · **the reference implementation** (validators · round-trip
converters · conformance harness) at `what/code/canvas_std/` (Option P).
**Does NOT own** (substrate-neutrality test, C8): producer pipelines · rendering runtimes · image generation
— these stay in CanvasForge / ComfyForge / LiteratureForge / SiteForge.

### 4. Upstream baseline & compatibility contract (C4)

The aDNA Canvas Standard is a **fork of Advanced Canvas (Obsidian) / JSON Canvas**. Pin the upstream baseline
at P1 (brief cites Advanced Canvas **v5.6.6** — confirm current). **✅ P1 resolution (2026-06-12):** baseline
pinned — **Advanced Canvas v5.6.6** (confirmed cited verbatim in the v1.0.0 corpus) **+ JSON Canvas 1.0**;
**PIN-A** ratified at the P1 exit gate (drift-delta to ~v6.2.1 tracked for P2/execution; see
`how/campaigns/campaign_canvas_genesis_planning/missions/p1_fork_baseline.md` §1). **Compatibility contract:** aDNA-native
extensions live additively in the namespaced **`_reserved`** block so a vanilla Obsidian reader ignores them
without error; a valid aDNA canvas **degrades to a valid Obsidian canvas**. Preserve v1.0.0 invariants
(YAML/`.lattice.yaml` authoritative + `.canvas` view; required `_lattice_meta` group; `_reserved` extension
carrier; semantic type→color/shape; explicit `toEnd:"arrow"`) unless a later ADR supersedes (C5).

### 5. Version line

Propose **aDNA Canvas Standard v2.0.0** — a clean successor to the embedded v1.0.0. The major bump (new
component model + panel/link semantics + context-object model) is justified in a dedicated ADR at P2 (D6).
Consumer `version_policy` default: **minor** (review on minor bump).

## Consequences

### Positive
- A single standard-bearer for every 2D output; producers stop re-deriving canvas semantics.
- Canvas becomes a first-class context object + interaction surface (serves the OIP/interface thesis).
- Clean federation story via the SiteForge forge pattern; quality via an `iii/` wrapper (no engine rebuild).

### Negative
- Δ1 forces a real category/runtime split decision (where the reference implementation lives).
- Extraction from CanvasForge (D2) is a multi-phase, parity-gated migration (execution campaign, not now).
- Δ2 (canvas-as-primitive) touches the aDNA core standard → requires a LIP, not a unilateral change.

### Neutral
- Inherited template ADRs (`adr_001/002/003`) are generic scaffold; the Canvas ADR namespace begins here at
  `adr_000`; D2–D7 mint as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then).

## Related
- `decision_register_genesis.md` (D1–D7) · `how/campaigns/campaign_canvas_genesis_planning/` ·
  `aDNA.aDNA/what/specs/spec_framework_ecosystem.md` · `SiteForge.aDNA/what/artifacts/sf_forge_pattern_spec.md` ·
  `CanvasForge.aDNA/what/context/advanced_canvas/` · `lattice-labs/how/governance/lips/lip_0001_lip_process.md`.
