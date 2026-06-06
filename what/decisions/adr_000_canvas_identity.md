---
type: decision
adr_id: "000"
title: "Project Identity — Canvas.aDNA, the aDNA Canvas Standard"
status: proposed
created: 2026-06-06
updated: 2026-06-06
last_edited_by: agent_stanley
signed_by: (pending — operator at P0 gate)
supersedes:
superseded_by:
tags: [adr, identity, canvas, standard, framework, genesis]
---

# ADR-000: Project Identity — Canvas.aDNA

## Status

**Proposed** — awaiting operator ratification at the **P0 gate** (Operation Cartography). Persona, category
(incl. Δ1), and scope boundary are operator-locked decisions; this ADR *proposes* and *holds*.

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

### 1. Category: Framework.aDNA *(provisional — Δ1 to resolve at P0)*

Canvas.aDNA is proposed as a **Framework.aDNA** — a vault that defines a standard others federate against
(cf. III.aDNA). Rationale: it defines *how* canvases are specified and consumed; it produces no end-user
artifact and deploys no partner runtime.

> **Δ1 (load-bearing).** `aDNA.aDNA/what/specs/spec_framework_ecosystem.md` is explicit: Frameworks "produce
> no primary artifact and **deploy no runtime**." The Standard will likely need **runnable reference tooling**
> (validators, round-trip converters, conformance harness). That pushes toward Platform. **The operator must
> lock the split:**
> - **Option F (Framework-pure):** Canvas.aDNA owns the *spec* + *conformance-suite spec* + *federation
>   contract*; the runnable reference implementation stays in **CanvasForge `canvas_core`** (or a thin
>   `canvas_std` reference lib it owns), consumed by `federation_ref`. *(recommended default)*
> - **Option P (Platform/hybrid):** Canvas.aDNA ships runnable validators/converters itself → categorize as
>   Platform (or a Standard-bearer sub-category), with a vault+code split.
>
> Resolution feeds D1/D2 (`decision_register_genesis.md`).

### 2. Persona *(operator locks at P0)*

Working persona is **Mondrian** (operator's prior pick) — universal visual language from minimal grid
elements; canvas-as-disciplined-composition. Alternatives carried for the lock:
- **Seshat** — goddess of measurement, records, and laying foundations ("stretching the cord"); the
  measure-and-record counterpart to LiteratureForge's **Thoth**. Strongest standard-bearer/records fit.
- **Mercator** — cartographer/projection; matches the campaign codename "Operation Cartography."

All three are distinct from existing Lattice personas. **`#needs-human`.**

### 3. Mission scope

Canvas.aDNA provides a forked, federable, agentic-context-native canvas standard for any 2D output, with:
a normative spec; a modular component model (per component class); panel/link semantics for non-DAG outputs
(flow/pagination/reading-order); a round-trip contract to baseline Obsidian; a conformance-suite spec; a
consumer federation contract; and LIP-style versioning/governance.

**Owns:** schema · component model · round-trip contract · conformance-suite spec · federation contract ·
versioning/governance.
**Does NOT own** (substrate-neutrality test, C8): producer pipelines · rendering runtimes · image generation
— these stay in CanvasForge / ComfyForge / LiteratureForge / SiteForge.

### 4. Upstream baseline & compatibility contract (C4)

The aDNA Canvas Standard is a **fork of Advanced Canvas (Obsidian) / JSON Canvas**. Pin the upstream baseline
at P1 (brief cites Advanced Canvas **v5.6.6** — confirm current). **Compatibility contract:** aDNA-native
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
