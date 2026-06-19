---
type: decision
adr_id: "004"
title: "Production code layout — canvas_core relocates to what/production/ (PT P5 relocation contract)"
status: proposed
created: 2026-06-19
updated: 2026-06-19
last_edited_by: agent_stanley
signed_by: "(pending operator ratification — proposed by Mondrian 2026-06-19)"
supersedes:
superseded_by:
resolves: "pt09 E4 code-layout reshape + Hestia substrate-path memo 2026-06-18 (Hearthstone P3 unblock)"
phase: "PT P5 (pt09 follow-up)"
tags: [adr, canvas, production, canvas_core, canvas_std, pt09, pt_p5, relocation, hearthstone, federation]
---

# ADR-004: Production Code Layout — `canvas_core` → `what/production/` (PT P5 relocation contract)

> Note: this is **Canvas.aDNA ADR-004**, distinct from `Home.aDNA`'s own `adr_004_consumer_wrapper_placement`
> (ADRs are per-vault namespaced). The exemplar bundle's bare "ADR-004" reference means Home's, not this one.

## Status

**Proposed** — 2026-06-19 (Mondrian). **Awaiting operator ratification** (Canvas ADRs carry an operator signature at
the gate; Mondrian proposes, Stanley ratifies — `signed_by` filled on countersign).

**This is a binding decision that pre-commits the PT P5 target — it is NOT authorization to move code now.** The
physical relocation executes at **PT P5** under Operation Keystone; **the E3→E4 phase gate stays HELD** (this ADR
does not open E4). It answers Hestia's substrate-path memo ([[../../../Home.aDNA/who/coordination/coord_2026_06_18_hestia_to_mondrian_canvas_substrate_path|coord 2026-06-18]])
and resolves the pt09-mandated "Mondrian reconciles the E4 code layout" reshape. Reply with the actionable values:
[[../../who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply|coord 2026-06-19 reply]].

## Context

**pt09** (Production Tidy, 2026-06-17) merged CanvasForge into Canvas (Hermes → Mondrian), reversing the E3.4
federated-producer split: Canvas.aDNA now owns the Standard **and** the production layers (deck · comic · diagram).
pt09 was a **governance** merge — the code (`canvas_core`/`canvas_comic`/`canvas_presentation`) stays in the archived
source (`Archive.aDNA/CanvasForge.aDNA/what/code/`) and **relocates into Canvas at PT P5** (see
[[../production/README|what/production/README]]).

Operation **Hearthstone** (aDNA.aDNA / Rosetta) is gated on the relocation target: the public node-exemplar bundle's
topology generator (`Home.aDNA/.../build_topology_canvas.py`) imports `canvas_core` (`CanvasBuilder` + `spatial`).
Hestia kept it functional via the `CanvasForge.aDNA` archive shim ("path TBD — Mondrian") and asked three questions:
**(1)** canonical path, **(2)** import name, **(3)** successor env-var. This ADR answers all three, plus a hard
dependency-resolution rule the three questions did not surface.

**Package shape (verified):** `canvas_core/__init__.py` eagerly loads the whole engine — `html_renderer`,
`image_generation`, `comfyforge_adapter`, `pdf_export`, `gdoc_export`, `visual_review`, `scoring`, `mermaid`,
`critique/`, `rlhf/`, `traps/` — ~80 files; the substrate (`core.CanvasBuilder`, `spatial`, `geometry`) is ~6 of them.
Per [[adr_001_canvasforge_relationship]] the *normative* core was already extracted into `canvas_std` at E0.2/E3.2;
what remains is, by that ADR's own words, "a **pure producer** that retains only producer-side convenience." `core.py`
now hard-imports `from canvas_std import schema` (the E3.2 constants shim), so **`canvas_core` depends on
`canvas_std`.** `canvas_comic`/`canvas_presentation` import `canvas_core` by bare name.

## Decision

**1 — Path: `Canvas.aDNA/what/production/canvas_core/`.** The three producer packages (`canvas_core`,
`canvas_comic`, `canvas_presentation`) relocate **together** to `what/production/`. This keeps the two-shelf split
clean: `what/code/` = the Standard's lean, zero-dependency reference library (`canvas_std`); `what/production/` = the
absorbed CanvasForge engine. It implements ADR-001's "CanvasForge becomes a pure producer" by *siting* the producer.

**2 — Import name: keep `canvas_core`.** A location-only move (the contextscope / rareharness / latticeprotocol
precedent — relocations grandfather package names). `from canvas_core.core import CanvasBuilder` and
`from canvas_core import spatial` survive unchanged across all consumers.

**3 — Env-var: `CANVAS_CORE_HOME`**, default → `…/Canvas.aDNA/what/production`. It names the package it locates and is
layout-agnostic. **Keep `CANVASFORGE_CODE` as a deprecated alias** (read `CANVAS_CORE_HOME or CANVASFORGE_CODE`;
`DeprecationWarning` when only the legacy is set). The alias is a **new shim** with its own Home §C row, co-terminous
with the constants-shim window (2027-06-13) — not a note on §C #29.

**4 — Dependency-resolution rule (the rule the three questions missed):** the env-var locator places only
`canvas_core` on `sys.path`; `canvas_core` hard-imports `canvas_std`. So **`canvas_std` must be separately importable**
on the node or `import canvas_core` raises `ImportError` and any try/except degrades — a *silent* non-render on fresh
nodes. Contract: `canvas_core` declares a hard dependency on **`adna-canvas-std`**. **Preferred:** install
`adna-canvas-std` (published, zero-dep) at bootstrap. **Fresh-node fallback:** add `what/code/canvas_std/src` as a
second `sys.path` entry (works because canvas_std is zero-dep). The locator stays single-purpose (locate `canvas_core`).

**5 — federation_ref `source_module`:** the canonical post-P5 value is **`what/production/canvas_core`** (the exemplar
template currently records the anticipatory `what/code/canvas_core`; `source_vault: Canvas.aDNA` is already correct).

**Considered and rejected:**
- **`what/code/canvas_core/` (sibling to `canvas_std`).** *Rejected:* a "library cohesion" argument that blurs the
  Standard-vs-engine line — `canvas_core` is a heavy engine (image-gen, html render, review, comfyui adapters), not a
  lean library — and contradicts the pt09 plan. The Standard-vs-producer boundary is *already* drawn at `canvas_std`;
  redrawing it inside the producer is the anti-pattern.
- **Fold `canvas_core` into `canvas_std`.** *Rejected:* pollutes the zero-dependency Standard reference impl with the
  full producer engine; breaks the "specify contracts, not engines / the Standard stays lean" doctrine (CLAUDE.md).
- **Split (substrate → `what/code`, producers → `what/production`).** *Rejected on a hard fact:* `canvas_core/__init__`
  is monolithic and `canvas_comic`/`canvas_presentation` do bare `from canvas_core import …`; peeling `spatial`/
  `geometry` into a separate top-level package manufactures a third shim for zero benefit.
- **Rename the package.** *Rejected:* breaks ~5–8 live consumers + the public exemplar for no benefit; precedent is to
  grandfather names on relocation.
- **Keep `CANVASFORGE_CODE` as the canonical env-var.** *Rejected:* bakes the archived CanvasForge brand into every new
  node bootstrap. (Retained only as a deprecated alias.)

## Consequences

### Positive
- Hearthstone P3 unblocked with a *correct* substrate path; the silent-non-render trap is closed in writing (§Decision 4).
- Clean two-shelf layout: `what/code/` (the Standard) vs `what/production/` (the engine) — legible and doctrine-aligned.
- Import name preserved → P5 is a path move, not an API break; ~8 consumers + the exemplar need no import edits.

### Negative
- `what/production/` graduates from a README-only governance marker to a real 3-package code home (executes at P5).
- A new env-var deprecation window (`CANVASFORGE_CODE` alias) to track and retire (Home §C).

### Neutral
- The `canvasforge.canvas_core` namespace (LP's 26 deprecation stubs, grace to 2027-05-04) is a separate top-level
  package on a separate clock — unaffected by where bare `canvas_core` lands.

## P5 Execution Checklist (binds the relocation; not executed by this ADR)

**Invariant — co-location:** `canvas_core`, `canvas_comic`, `canvas_presentation` move **together** to
`what/production/` (bare cross-imports require a shared `sys.path` root). Do not land `canvas_core` and strand the siblings.

**Scheduled follow-ups (folded here from the E3.4 parked list, now OBE-reframed post-pt09):**
- **FU2 — round-trip-function dedup** (`validate`/`diff`/`merge`/round-trip → `canvas_std`). E3.2 repointed only the
  *constants*; the functions are still self-contained in `canvas_core` (`core.py` `validate` L699 / `diff` L598 /
  `merge` L661). **Do this at relocation, once `canvas_core` and `canvas_std` are co-located in Canvas** — not in the
  archive (editing about-to-move code). *Acceptance:* `e3_3_parity_check.py` GREEN, CanvasForge suite 900/3, locked
  baseline `3ce4d341` unchanged.
- **FU1 — canvas/-routing Standing Order**, reframed as **Canvas production governance**: route `what/production/`
  standard-consumption through the `canvas/` wrapper (mirroring the `iii/` Standing Order), folded into the P5
  refederation. Not a marginal edit to the archived "do-not-resume" CanvasForge `CLAUDE.md`.

**Verify-at-execution items:**
- `canvas_core/paths.py` `find_vault_root()` will resolve to `Canvas.aDNA` post-move (was CanvasForge-relative) — verify
  no producer code hard-coded a CanvasForge-relative path.
- `e3_3_parity_check.py` (Canvas's own mission artifact) is itself a bare-`canvas_core` consumer — give it the same
  locator/install treatment so Canvas's regression harness survives the move.
- ~8 consumer wrappers / ~11 wrappers refederate `source_vault: CanvasForge.aDNA → Canvas.aDNA` + `source_module →
  what/production/canvas_core` (PT P5 wrapper-refederation).
- **Notify Hestia (Home.aDNA) at relocation** — she re-verifies the staged exemplar resolver + drops the interim
  `CanvasForge.aDNA`-archive branch (her staged fallthrough auto-flips, but she wants a re-verify); per the 2026-06-19
  ack (`Home.aDNA/who/coordination/coord_2026_06_19_hestia_to_mondrian_substrate_staged_ack.md`).

## Related
- [[adr_001_canvasforge_relationship]] (D2 — "CanvasForge becomes a pure producer"; this ADR sites that producer) ·
  [[adr_000_canvas_identity]] §1 (Option P — Canvas ships the reference tooling) · [[adr_003_standard_governance]] (D6).
- [[../production/README|what/production/README]] (pt09 P5 relocation table) · [[../../STATE|STATE]] (E3→E4 HELD).
- [[../../who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply|reply to Hestia 2026-06-19]] ·
  `Home.aDNA/who/coordination/coord_2026_06_18_hestia_to_mondrian_canvas_substrate_path.md` (the memo) · Home §C shim
  ledger (env-var alias row — Hestia-owned).
- `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_core/core.py` (`from canvas_std import schema` — the §Decision-4 dep) ·
  `…/missions/artifacts/e3_3_parity_check.py` (the FU2 gate).
