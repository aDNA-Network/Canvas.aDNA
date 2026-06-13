---
type: artifact
artifact_type: fork_baseline
title: "P1 Fork Baseline — what v2.0.0 inherits, the _reserved extension map, the pinned upstream"
campaign_id: campaign_canvas_genesis_planning
mission_id: mission_p1_source_inventory
phase: 1
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
status: accepted
tags: [artifact, fork_baseline, canvas, standard, genesis, p1]
---

# P1 Deliverable 2 — Fork Baseline

> **Phase P1 / Operation Cartography.** Defines the baseline the **aDNA Canvas Standard v2.0.0** forks from:
> the pinned upstream version, the verbatim invariants + vocabularies inherited from Advanced Canvas v5.6.6 +
> Canvas Standard v1.0.0, the additive **`_reserved`** extension map for aDNA-native semantics, and the
> Obsidian-degradation contract (C4). Companion: [[p1_source_inventory]] (the labeled catalog).
> **Planning only** — no schema is implemented here; P2 mints the normative spec from this baseline.

---

## §1 — Upstream baseline pin  ⟵ **operator decision at the P1 gate**

**Finding (resolved at source).** The v1.0.0 corpus cites its upstream **verbatim**:
- `AC/context_advanced_canvas_standard.md:103` → "Advanced Canvas plugin **v5.6.6** documentation"
- `AC/context_advanced_canvas_schema.md:60` → "Advanced Canvas (**v5.6.6**) adds visual properties…"
- **No JSON Canvas spec version is cited anywhere** — the base `.canvas` format is referenced generically.
- Current upstream (verified 2026-06-12): Advanced Canvas **~v6.2.1** (96 releases; recently updated).

So the brief's "v5.6.6 — confirm" is **confirmed as the provenance-accurate derivation point**: v1.0.0 was
demonstrably built against v5.6.6, not a guess. The fork-baseline decision is therefore *which* version v2.0.0
pins, given upstream has moved a full major line ahead.

| Option | Pin | Cost / benefit | 
|--------|-----|----------------|
| **PIN-A (recommended)** | **Advanced Canvas v5.6.6** (as-derived) + **JSON Canvas 1.0** as the stable format floor | Zero re-derivation risk — every inherited invariant in §2/§3 is already verified against v5.6.6. Record a **drift-delta** to ~v6.2.1 as a P2/execution review item (scan the v5.6.6→v6.2.1 changelog for additive features — e.g. new node/edge styles — worth absorbing into `_reserved`, *additively*, not as a baseline reset). |
| PIN-B | Re-baseline to current ~v6.2.1 now | Forks from latest, but every v1.0.0 invariant must be re-verified against a major-version-newer plugin; the entire v1.0.0 corpus's citations go stale; upstream is actively churning (updated days ago). Higher risk for no P1 benefit. |

**Recommendation: PIN-A.** Pin **Advanced Canvas v5.6.6** + **JSON Canvas 1.0**; carry the **v5.6.6 → ~v6.2.1
drift-delta** as a tracked P2/execution evaluation item. *(JSON Canvas 1.0 is the stable open base format; it is
not version-cited in the corpus — flag to confirm the `.canvas` floor at P2.)*

> **✅ RATIFIED — operator confirmed PIN-A at the P1 exit gate, 2026-06-12.** Baseline locked: **Advanced Canvas
> v5.6.6** + **JSON Canvas 1.0**; the v5.6.6 → ~v6.2.1 drift-delta is a tracked P2/execution review item
> (absorb additively via `_reserved`, never as a baseline reset). The `.canvas` floor (JSON Canvas 1.0) is to be
> confirmed at P2 (fork-baseline §6).

---

## §2 — Inherited invariants (verbatim, KEEP)

The seven load-bearing rules v2.0.0 carries **unchanged** from v1.0.0 (source: `AC/…standard.md`, `…schema.md`,
`…roundtrip.md`). These are the contract a valid aDNA canvas must satisfy.

| # | Invariant | Verbatim anchor |
|---|-----------|-----------------|
| I1 | **YAML is authoritative; canvas is the view layer.** `.lattice.yaml` is the semantic source of truth (Decision 9); `.canvas` is a derived view — never edit a canvas expecting auto-propagation. | `standard.md:27` |
| I2 | **`_lattice_meta` group is required.** Every canvas includes a group node `id:"_lattice_meta"` encoding source name + version; it stores the YAML-topology **sync hash**. | `standard.md:35`, `roundtrip.md:31` |
| I3 | **`_reserved` metadata block present.** A `_reserved` block lives under `metadata.frontmatter._reserved` (a preserved, no-validation custom store) — `{}` in v1.0; the additive extension carrier going forward. | `standard.md:43`, `schema.md:104-119` |
| I4 | **Explicit `toEnd:"arrow"` on directed edges.** Obsidian defaults to no arrow; every directed edge sets `toEnd:"arrow"` as a top-level edge property (not in `styleAttributes`). | `standard.md:97`, `schema.md:94` |
| I5 | **Semantic type → color/shape convention.** Node visual styling is *derived from* semantic type (a convention, not free styling). Reserved colors: red `"1"`=warn/error, orange `"2"`=note, yellow `"3"`=highlight; `"4""5""6"` for node types. | `standard.md:42,86-91` |
| I6 | **Edge-style convention.** Solid = data flow; `long-dashed` = control/federation; `dotted` = optional. | `standard.md:33` |
| I7 | **Round-Trip authority + sync-hash.** YAML→Canvas is primary/automated; Canvas→YAML is **advisory only** (draft requiring human review). Sync-hash in `_lattice_meta` detects staleness; topology round-trips, but `config`/`data_mapping`/`port`/`execution`/`fair`/`federation` are **lossy by design**. | `roundtrip.md:27,31,44-55,93` |

---

## §3 — Inherited vocabularies (verbatim, KEEP) + the JSON shape

Source: `CC/core.py` (`CanvasBuilder` class attributes) + `AC/…schema.md`. These enums are the baseline-fidelity
vocabulary — a valid aDNA canvas must use these tokens (KEEP). The two **semantic maps** are KEEP-as-floor but
**EXTEND** in v2.0.0 (they cover only lattice/pipeline types today).

**Node/edge JSON floor (JSON Canvas + Advanced Canvas v5.6.6):**
- **Node** — required: `id`, `type` ∈ `{text, file, group, link}`, `x`, `y`, `width`, `height`; optional `color`.
  Advanced-Canvas extensions in `styleAttributes` (`shape`, `border`, `textAlign`) + top-level `isStartNode`,
  `collapsed`, `portal`, `dynamicHeight`. Default rectangle = absence of a `shape`.
- **Edge** — required: `id`, `fromNode`, `fromSide` ∈ `{top,bottom,left,right}`, `toNode`, `toSide`; optional
  `label`, `color`; **mandated** top-level `toEnd:"arrow"`. `styleAttributes`: `path`, `arrow`, `pathfindingMethod`.

**Validation enums (`VALID_*`, 10 families — KEEP):**

| Enum | Members |
|------|---------|
| `VALID_NODE_TYPES` | `text, file, group, link` |
| `VALID_SHAPES` | `None, pill, diamond, parallelogram, circle, predefined-process, document, database` |
| `VALID_BORDERS` | `None, dashed, dotted, invisible` |
| `VALID_TEXT_ALIGN` | `None, center, right` *(left = implicit default)* |
| `VALID_COLORS` | `"0","1","2","3","4","5","6"` *(+ `#`-hex accepted by `validate()`)* |
| `VALID_PATH_STYLES` | `None, dotted, short-dashed, long-dashed` |
| `VALID_ARROWS` | `None, triangle-outline, thin-triangle, halved-triangle, diamond, diamond-outline, circle, circle-outline` |
| `VALID_PATHFINDING` | `None, square, a-star` |
| `VALID_SIDES` | `top, bottom, left, right` |
| `VALID_ENDS` | `none, arrow` |

**`TYPE_MAPPING` (KEEP-as-floor → EXTEND; lattice types only today):**

| key | color | shape | node_type |
|-----|-------|-------|-----------|
| `module` | `"4"` | `predefined-process` | `file` |
| `dataset` | `"5"` | `database` | `file` |
| `reasoning` | `"6"` | `diamond` | `text` |
| `process` | `None` | `None` | `text` |
| `input` | `"4"` | `parallelogram` | `text` |
| `output` | `"5"` | `parallelogram` | `text` |
| `start` | `None` | `pill` | `text` |
| `end` | `None` | `pill` | `text` |

**`EDGE_TYPE_MAPPING` (KEEP-as-floor → EXTEND):**

| key | path_style | arrow | from_end | to_end |
|-----|-----------|-------|----------|--------|
| `data` | `None` | `None` | `None` | `arrow` |
| `control` | `long-dashed` | `None` | `None` | `arrow` |
| `optional` | `dotted` | `triangle-outline` | `None` | `arrow` |
| `bidirectional` | `None` | `None` | `arrow` | `arrow` |
| `weak` | `short-dashed` | `circle-outline` | `None` | `arrow` |

**Reference-impl surface (Option P extraction map):** normative core to extract into `what/code/canvas_std/` →
`build` (≈`to_canvas`), `read_back` (≈`from_canvas`), `diff`, `merge`, `validate`, `compute_sync_hash`,
`preserve_positions`, `add_semantic_node/edge`, `add_lattice_meta_group`. Stays producer-side in CanvasForge →
`layout_{dag,grid,radial,presentation}`, `selection_board`, `save`, accessors. *(No literal `to_canvas`/
`from_canvas` exists — alias at extraction.)*

---

## §4 — The additive `_reserved` extension map (v2.0.0)

v1.0.0 set `_reserved: {}` and used `metadata.frontmatter._reserved` to carry `sync_hash`/`lattice_name`/
`lattice_version`. v2.0.0 makes `_reserved` the **single namespaced carrier** for every aDNA-native extension,
so a vanilla Obsidian reader ignores the whole block and the canvas still opens. **These are reserved keys —
their schemas are minted at P2 (D4/D5/D6/D7); P1 only fixes the namespace + degradation guarantee.**

```
metadata.frontmatter._reserved:
  adna_version:        "2.0.0"            # Standard version this canvas conforms to
  conformance_level:   core|extended|adna_native   # D6 — set at P2
  sync:                                   # carried from v1.0 (_lattice_meta usage), I2/I7
    sync_hash: <16-hex>
    source_name: <str>
    source_version: <semver>
  component_types:     { … }              # D4 — generalized component taxonomy (text/typography-run/
                                          #       image/video/shape/embed/group-panel/link/table/code/
                                          #       caption/region); supersedes lattice-only TYPE_MAPPING
  semantic_bindings:   { type → semantic_type, color, shape }   # D4 — generalizes TYPE_MAPPING beyond lattice
  panel_link:          { reading_order, flow, pagination, region, sequence }  # D5 — non-DAG output semantics
  brand_style_pack_ref: <federation_ref>  # VisualDNA hook (from LF visual-contract X3); producer-resolved
  context_object:      { id, refs[], version }   # D7 — canvas-as-context metadata (LIP-gated)
```

**Provenance of each reserved key** (traceable to §-rows in [[p1_source_inventory]]): `component_types` /
`semantic_bindings` ← B1 + C1–C3 (EXTEND); `panel_link` ← C4 + D1/D2 (EXTEND); `brand_style_pack_ref` ← D1;
`sync` ← A2/B2 (KEEP); `context_object` ← D7 (Δ2, LIP path). All **additive** — none alters a baseline field.

---

## §5 — Obsidian degradation contract (C4)

The fork stays **round-trippable to baseline Obsidian**. Formally, for any aDNA canvas `K`:

1. **Strip rule.** Removing `metadata.frontmatter._reserved` from `K` yields `K′`, a valid **JSON Canvas 1.0 /
   Advanced Canvas v5.6.6** file — i.e. all aDNA-native semantics live *only* inside `_reserved`.
2. **Ignore rule.** A vanilla Obsidian/Advanced-Canvas reader opens `K` unchanged: it renders nodes/edges from
   the baseline fields and silently ignores `_reserved` (it is a no-validation custom store, I3).
3. **No-baseline-overload rule.** v2.0.0 introduces **no** new top-level node/edge keys and **no** new
   `styleAttributes` tokens outside the inherited `VALID_*` enums; new expressive power is carried in `_reserved`
   or proposed **upstream** (never bolted onto a baseline field).
4. **Conformance hook.** The P3 conformance suite includes a **degradation test**: `validate(strip(K))` must pass
   the baseline schema for every conformance level. *(Contract specified here; the test engine is built later.)*

> This is what "fork, don't drift" means operationally: aDNA-native extensions are **additive and quarantined**;
> a valid aDNA canvas always degrades to a valid Obsidian canvas.

---

## §6 — Open items carried to P2

- **Version pin** (§1) — operator confirms PIN-A (v5.6.6 + JSON Canvas 1.0) at the gate; drift-delta tracked.
- **`_reserved` key schemas** (§4) — `component_types` (D4), `panel_link` (D5), `conformance_level` (D6),
  `context_object` (D7) get normative schemas at P2.
- **`TYPE_MAPPING` generalization** — extend the 8 lattice types to the full cross-output component taxonomy
  without breaking the lattice bindings (KEEP the existing 8 as a registered profile).
- **`to_canvas`/`from_canvas` aliasing** — fix the reference-impl API vocabulary so the conformance suite matches.
- **JSON Canvas floor** — confirm the base format version (assumed 1.0; uncited in the corpus).

## Related
- [[p1_source_inventory]] · [[mission_p1_source_inventory]] · [[campaign_canvas_genesis_planning]]
- `what/decisions/adr_000_canvas_identity.md` (§4 baseline & compatibility contract) · `what/decisions/decision_register_genesis.md` (D4/D5/D6/D7).
