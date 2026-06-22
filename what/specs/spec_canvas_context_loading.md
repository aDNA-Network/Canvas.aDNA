---
type: spec
spec_id: spec_canvas_context_loading
title: "aDNA Canvas context-loading & traversal protocol — loading a canvas as a context graph (Salon leg 2)"
standard_version: "2.0.2"
status: ratified
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
phase: P1
campaign_id: campaign_canvas_salon
resolves: "leg-2 loading/traversal protocol (the 'how' companion to spec_context_object D7)"
supersedes:
superseded_by:
tags: [spec, canvas, context-object, loading, traversal, leg2, salon, surface, rfc2119]
---

# aDNA Canvas Context-Loading & Traversal Protocol (Salon leg 2)

> **Status: RATIFIED 2026-06-22 (operator, P1→P2 gate of Operation Salon, `campaign_canvas_salon`).** Companion to
> [[spec_context_object|spec_context_object.md]] (D7, ratified): that spec defines the context-object *metadata*
> (`_reserved.context_object`) and declares that a canvas **SHOULD** be loadable/traversable *without rendering*; this
> spec supplies the **protocol** it left unspecified — *how* an agent does the loading and traversal. RFC 2119 keywords
> (MUST / SHOULD / MAY). Bounded by [[adr_006_canvas_surface_boundary|ADR-006]]: this is a **contract + a reference
> loader**, never a rendering engine, a transport, or a cross-surface router.

## 1. Purpose & relationship

1.1. An aDNA canvas has a dual nature ([[spec_context_object]] §1): **render-AS-output** (a 2D artifact) and
**read-AS-context** (a structured object an agent loads to understand a domain). `spec_context_object.md` governs the
*identity* of the read-AS-context face — the stable `id`, `version`, `refs`, `summary` carried in
`_reserved.context_object`. It states (§2.3) that a canvas referenced as context **SHOULD** be loadable by summary/refs
without rendering. It does **not** define the loading/traversal procedure. **This spec is that procedure.**

1.2. This spec is **substrate-neutral** and **implementation-agnostic**: it defines an abstract *context-graph model*,
a normative *load pipeline*, a *reference-resolution contract*, and a *traversal read-contract*. It names a single
conformant **reference implementation** (the `canvas_context` sibling, §10) but does not require that one — any loader
that satisfies §9 is conformant.

1.3. It does not re-open the canvas-as-primitive question (Δ2 / LIP-0009); a canvas remains a *view of the `lattice`
primitive* (aDNA Decision 9), and all metadata rides in `_reserved` — no core-primitive change.

## 2. Scope

**In scope.** Loading a `.canvas` document (any conformance level) into an in-memory **context graph**; overlaying the
`_reserved` semantic layers; classifying and exposing outbound references; an advisory staleness check against the
authoritative source; a read-only traversal API; and graceful degradation for canvases that carry no `_reserved`.

**Out of scope.**
- **Rendering & media I/O** — no rasterization, image generation, video/frame decoding, or layout-to-pixels. File and
  media components are represented by reference, not loaded content (substrate-neutrality test, C8).
- **Federation network transport** — this spec defines the resolver *interface* (§5); the actual cross-vault fetch is
  the resolver's / federation layer's job, not the loader's (`adr_006` §1–§2).
- **Cross-surface routing** — *when* to surface context on a canvas vs an ISS gate vs a Terminal prompt vs a web page is
  the future `aDNA.aDNA` **OIP** layer's decision-tree (`adr_006` §3). A loader MUST NOT encode routing logic.
- **Mutation** — loading is **read-only**; authoring/round-trip writes are governed by
  [[spec_roundtrip_protocol_v2|spec_roundtrip_protocol_v2.md]], not here.

## 3. The context-graph model (abstract)

A conformant loader produces a **`ContextGraph`** — a navigable, read-only structure. The following are conceptual
record shapes (a reference implementation realizes them in its host language):

```
ContextGraph:
  id:                <stable urn/slug | null>      # from context_object.id; null ⇒ pure output artifact
  version:           <semver | null>               # from context_object.version
  summary:           <string | null>               # from context_object.summary
  conformance:       { declared, reached, stale }   # declared/reached level; stale flag (§7)
  panels:            [ Panel ]                      # group/region nodes, layout-bearing
  components:        [ Component ]                  # all nodes as typed components
  relations:         [ Relation ]                   # all edges as typed relations
  refs:              [ Ref ]                        # outbound context references
  anchors:           { <label>: <node_id> }         # from _reserved.panel_link.anchors
  surfaces:          [ Surface ]                    # from _reserved.panel_link.surfaces

Component:                                          # one per nodes[] entry
  id:                <node id>
  node_type:         text | file | group | link     # baseline JSON Canvas type
  class:             <component class | null>        # from _reserved.component_types[id].class (14 classes)
  semantic_type:     <profile string | null>        # e.g. heading, figure, quote, footnote
  qualities:         { … }                           # class-specific (substrate, language, ref, …)
  payload:           { text? | file? | url? | label? }   # baseline content, by reference for media
  degrades_to:       text | file | group | link      # baseline fallback
  geometry:          { x, y, width, height }         # advisory; layout, not semantics

Panel:                                              # Component with class ∈ {panel, group, region}
  id:                <group/region node id>
  flow:              none | vertical | horizontal | columns   # _reserved.panel_link.regions[id].flow
  pagination:        none | paged | continuous
  extent:            { unit, max } | null            # words | pages | slides
  surface:           <free-form string | null>       # print_page | slide | web | letter | …
  children:          [ <node_id> ]                   # nodes geometrically/semantically contained

Relation:                                           # one per edges[] entry
  id:                <edge id>
  from:              <node id>
  to:                <node id>
  directed:          <bool>                          # from toEnd/fromEnd
  kind:              sequence | reading_order | adjacency | dependency | null   # _reserved.panel_link.edges[id].kind
  label:             <string | null>

Ref:                                                # one per context_object.refs entry (+ inline refs)
  form:              wikilink | federation_ref
  target:            <raw ref string>                # "[[path]]"  |  "lattice://instance/lattice[/node]"
  resolved:          <handle | unresolved>           # set only by a resolver (§5)

Surface:  { id: <group_id>, role: canonical | derived, surface: <string> }
```

3.1. The **baseline layer** (`panels`/`components`/`relations` from `nodes`/`edges`) MUST be derivable from a canvas
with `_reserved` stripped — i.e. from any valid JSON Canvas / Advanced Canvas file. The `_reserved` overlay is
**purely additive** semantic enrichment (§4 L3).

## 4. The load pipeline (normative)

A conformant loader executes these steps in order. Each step's MUST/SHOULD/MAY is binding.

**L1 — Parse & validate.** Parse the `.canvas` JSON. Determine the declared level from
`_reserved.conformance_level` (`core` | `extended` | `adna_native`); if absent, infer the structural level. Run the
Standard validator (`validate_suite(doc, declared_level)`). The loader **MUST** refuse to produce a `ContextGraph`
from a document that fails **Core** validation (malformed topology — missing required node/edge fields, duplicate ids,
dangling edge endpoints). It **SHOULD** surface Extended / aDNA-Native failures as warnings and **MAY** still load in a
degraded mode. Record `conformance.declared` and `conformance.reached`.

**L2 — Build the baseline graph.** Map each `nodes[]` entry to a `Component` stub (id, `node_type`, `payload` from
`text`/`file`/`url`/`label`, advisory `geometry`); each `group` node is also a `Panel` candidate. Map each `edges[]`
entry to a `Relation` stub (id, `from`/`to`, `directed` from `toEnd`/`fromEnd`, `label`). This layer **MUST** succeed on
a stripped (baseline) canvas.

**L3 — Overlay the `_reserved` semantic layer.** When `_reserved` is present, merge **additively**:
`component_types[node_id]` → `Component.{class, semantic_type, qualities, degrades_to}`;
`panel_link.regions[group_id]` → `Panel.{flow, pagination, extent, surface, responsive}`;
`panel_link.edges[edge_id].kind` → `Relation.kind`; `panel_link.anchors` → `ContextGraph.anchors`;
`panel_link.surfaces[]` → `ContextGraph.surfaces`. A node/edge **without** a `_reserved` entry **MUST** retain its L2
baseline stub (no silent drop). The loader **MUST NOT** require `_reserved` for any step.

**L4 — Resolve context identity.** Read `_reserved.context_object` → `ContextGraph.{id, version, summary, refs}`. If
`context_object` is **absent**, the canvas is a **pure output artifact**: the graph still loads (panels / components /
relations intact) but `id`/`version`/`summary` are `null` and `refs` is empty (§8). The loader **MUST NOT** fabricate
an identity.

**L5 — Classify & expose references.** For each entry in `context_object.refs` (and any inline references discovered in
component payloads — e.g. `[[wikilinks]]` inside `text`), build a `Ref` with `form` classified as **wikilink**
(`[[…]]`, in-vault) or **federation_ref** (`lattice://…` or a `federation_ref` block, cross-vault). The loader **MUST**
expose every `Ref`; it **MUST NOT** itself perform cross-vault transport. Resolution is delegated to a caller-supplied
resolver (§5); with no resolver, every `Ref.resolved` is `unresolved` (lazy).

**L6 — Detect staleness (advisory).** If `_reserved.sync.sync_hash` is present, the loader **SHOULD** recompute the
topology hash with the Standard's sync-hash function (`compute_sync_hash`, per [[spec_roundtrip_protocol_v2]]) and
compare. On mismatch, set `conformance.stale = true`. Staleness is **advisory**: a stale canvas **MUST** still load and
the loader **MUST** surface the flag; it **MUST NOT** block on it.

**L7 — No rendering.** Throughout, the loader **MUST NOT** invoke any render pipeline, rasterizer, image generator, or
media decoder. `file`-type nodes and `image` / `video` components are carried by their **reference** (path / URI) plus
metadata (`semantic_type`, `qualities`) — never by decoded pixel/frame data. Loading is a pure structural-and-semantic
read.

## 5. Reference resolution (the resolver interface)

5.1. The loader defines and calls an abstract **`Resolver`** contract; it does not implement transport itself:

```
Resolver.resolve(ref: Ref) -> handle | unresolved
  wikilink       → a local handle (vault-relative path to a loadable canvas/doc)
  federation_ref → a federation handle/descriptor (NOT transported content)
```

5.2. In-vault **wikilink** resolution **SHOULD** be supported by a default path resolver (vault-relative lookup).
Cross-vault **federation_ref** resolution **MAY** be deferred; when performed, the resolver returns a *handle /
descriptor*, and the loader **MUST NOT** cross the vault boundary to fetch content (that is the federation layer's role,
and ultimately is gated by the boundary in `adr_006`). A resolved handle MAY itself be loaded by recursively applying
this protocol, enabling bounded multi-canvas context traversal under caller control (depth/cycle limits are the
caller's responsibility; the loader **MUST** be cycle-safe — re-encountering a loaded `id` returns the existing node).

## 6. Traversal primitives (the read contract)

A conformant loader exposes at least the following **read-only** primitives (names illustrative; semantics binding). All
**MUST** be free of side effects on the source document.

| Primitive | Returns |
|-----------|---------|
| `identity()` | `{ id, version }` |
| `summary()` | the agent-facing summary, or `null` |
| `conformance()` | `{ declared, reached, stale }` |
| `panels()` / `children(panel_id)` | layout-bearing panels; a panel's contained nodes |
| `components()` / `component(id)` | all typed components; one by id |
| `relations()` / `neighbors(node_id, kind?)` | all typed relations; adjacent node ids, optionally filtered by `kind` |
| `reading_order(panel_id?)` | an ordered node-id walk following `kind ∈ {reading_order, sequence}` from the start node (`isStartNode`) / canonical surface |
| `refs()` / `resolve(ref, resolver)` | outbound `Ref`s; a resolved handle via §5 |
| `anchors()` / `surfaces()` | label→node-id map; canonical/derived surfaces |

6.1. `reading_order()` gives an agent the **document order** of a non-DAG output (a deck's slides, a paper's sections)
without rendering — the core leg-2 capability. It **MUST** be derived from `panel_link` reading-order/sequence edges
(per [[spec_panel_link_semantics]]), falling back to geometry only when those are absent.

## 7. Authority & staleness

7.1. Per aDNA Decision 9 and [[spec_roundtrip_protocol_v2]], the authoritative source of a canvas is its
`.lattice.yaml`; the `.canvas` is the **view**. A loader reads the **view**. The `conformance.stale` flag (§4 L6)
signals the view may trail its source; a caller that needs source-of-truth values consults the authoritative file via
the round-trip protocol. This spec does not perform that reconciliation — it only surfaces the flag.

## 8. Degradation (canvases without `_reserved`)

8.1. A canvas with no `_reserved` block (a pure JSON Canvas / Advanced Canvas file, or an aDNA output artifact not
registered as context) **MUST** still load: L2 yields the baseline `panels`/`components`/`relations`; L3 is a no-op;
L4 yields a null identity; L5 still classifies any inline wikilinks. The loader returns a valid `ContextGraph` with
`id = null`. This mirrors the Standard's degradation contract (`strip` / `degradation_report`): aDNA-native enrichment
is additive, and its absence is valid, not an error.

## 9. Conformance

A **conformant context loader**:

- **MUST** validate before loading and refuse a Core-invalid document (§4 L1);
- **MUST** load **without rendering** or media decoding (§4 L7);
- **MUST** be **read-only** — no mutation of the source (§6);
- **MUST** treat `_reserved` as additive and handle its absence (§3.1, §8);
- **MUST** expose every outbound `Ref` and delegate cross-vault transport to a resolver (§4 L5, §5);
- **MUST** be cycle-safe across recursive resolution (§5.2);
- **MUST** expose the §6 traversal primitives;
- **SHOULD** detect staleness via the Standard sync-hash (§4 L6);
- **SHOULD** resolve in-vault wikilinks with a default resolver (§5.2);
- **MAY** defer federation resolution (§5.2).

9.1. **Conformance fixtures.** The conformance set reuses the `canvas_std` golden fixtures
(`tests/fixtures/adna_native.canvas`, `core_minimal.canvas`, `extended_styled.canvas` — covering aDNA-native, baseline,
and no-`_reserved` paths) plus at least one **real producer** output
(`what/production/document_generator/examples/*.canvas`) loaded as a context graph without rendering. A loader passes
when it yields the expected `ContextGraph` shape, the correct `reading_order()`, and the documented degradation on the
no-`_reserved` fixture. (The executable suite lands with the reference implementation at P2.)

## 10. Reference implementation (forward-pointer, D6)

10.1. Per the ratified decision **D6** (Operation Salon P0, `adr_006`-bounded), the reference loader is built at
**Salon P2** as a **new sibling package** `what/code/canvas_context/` that imports `canvas_std` **read-only** — using its
public API (`validate_suite`, `validate`, `strip`, `degradation_report`, `compute_sync_hash`) and reserved-layer enums
(`COMPONENT_CLASSES`, `PL_EDGE_KINDS`, `ANCHOR_REF_KEYS`, …). The `canvas_std` **firewall stays intact** (frozen since
Keystone; `git -C what/code/canvas_std diff --stat` empty at every gate). This spec is impl-agnostic; the sibling is one
conformant realization and **may be folded into `canvas_std` later** at a deliberate Standard release if the loader
graduates to core reference tooling.

## 11. Boundary (ADR-006)

11.1. This spec defines a **contract** and authorizes a **reference loader** — not a product runtime, a transport, or a
router. Federation transport belongs to the federation layer; cross-surface routing (Canvas vs ISS vs Terminal vs web)
belongs to the future `aDNA.aDNA` **OIP** layer; web rendering belongs to Astro; gate runtimes belong to ISS
([[adr_006_canvas_surface_boundary|ADR-006]] §2–§3). A loader that stays within §2's "out of scope" list keeps Canvas on
its side of the fence.

## 12. Related

- [[spec_context_object]] (D7 — the context-object metadata + the "loadable without rendering" SHOULD this spec implements)
- [[spec_adna_canvas_standard]] (§7 `_reserved`; the JSON node/edge shape + conformance levels + degradation contract)
- [[spec_component_model]] (the 14-class component taxonomy overlaid in L3)
- [[spec_panel_link_semantics]] (reading-order / flow / region / sequence — the basis of `reading_order()`)
- [[spec_roundtrip_protocol_v2]] (authority matrix + `compute_sync_hash` for the staleness check)
- [[spec_federation_contract]] (`federation_ref` form + cross-vault reference declaration)
- [[adr_006_canvas_surface_boundary]] (the binding boundary) · [[adr_000_canvas_identity]] (the three-leg thesis)
- `how/campaigns/campaign_canvas_salon/campaign_canvas_salon.md` (P1 → P2: this spec → the `canvas_context` loader + pilot)
