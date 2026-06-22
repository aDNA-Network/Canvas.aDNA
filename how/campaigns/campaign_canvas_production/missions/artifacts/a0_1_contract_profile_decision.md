---
type: decision_record
created: 2026-06-21
updated: 2026-06-21
status: ratified
last_edited_by: agent_stanley
campaign_id: campaign_canvas_production
mission: mission_a0_1_contract_profile_triage
tags: [canvas, production, atelier, decision, a0, contract, profile]
---

# A0.1 Decision Record — production-contract + profile triage

**Purpose:** resolve the six governance/contract questions that gate the diagram and comic builds, **before any
code**. Each decision carries a doctrine-aligned **recommended default** and rationale. The operator ratifies (accept /
edit) at the **A0→A1 gate**; ratification **activates** Operation Atelier and authorizes the A1 diagram build.

> **Spec landscape (confirmed):** there is **no dedicated `spec_diagram_*` or `spec_comic_*`** file in `what/specs/`.
> Diagram and comic appear only as *references* inside the ratified specs — the `comic` profile is named in
> `spec_federation_contract §6.1` (`profiles_used: [lattice, deck, comic]`), comics are named for `adjacency` edges in
> `spec_panel_link_semantics §3`, and diagrams ride the `shape` component class in `spec_component_model §2`. **No new
> Standard spec is required** — both producers operate entirely within ratified specs + the `_reserved` extension
> namespace. (See D2.)

---

## D1 — Per-producer quality contract (`iii_quality_contract.md`)?

**Recommended: YES for both — light for diagram, full for comic.** Modeled on `deck_generator/iii_quality_contract.md`
(a *contract*, not an engine: the generator emits the `component_types`/`panel_link`/`context_object.refs` an `iii/`
review needs; III scores; the producer does not score itself; pixel/visual scoring stays PT-P5-gated).

- **Diagram (light):** lenses = *correctness* (graph faithfully represents the asserted relations — no phantom/missing
  edges), *legibility* (layout reads naturally, labels fit), *render fidelity* (the derived Mermaid `code` node matches
  the native graph), plus the mandatory *rigor* + *accuracy* lenses for any quantitative diagram (gantt durations,
  class cardinalities).
- **Comic (full):** lenses = *visual-narrative coherence*, *character consistency*, *composition/panel hierarchy*,
  plus mandatory *rigor* + *accuracy* (verify-or-omit on story facts; GRAPH-GAP for unsupported beats). The legacy
  `ComicReport.review()` rubric (page-count band, panel-type variety, coverage, color-script continuity) becomes the
  contract's measurable dimensions — **not** shipped code.

*Rationale:* parity with the deck precedent; pre-stages the A3.1 structural `iii/` review; keeps the "generator does
not score itself" doctrine (C6/C8).

---

## D2 — Are the `diagram` / `comic` `semantic_bindings` profiles producer-side (no Standard LIP)?

**Recommended: PRODUCER-SIDE, no LIP.** Each producer declares a bare `{"profile": "diagram"}` / `{"profile": "comic"}`
in `_reserved.semantic_bindings`, mirroring `deck_generator`'s `{"profile": "deck"}`. The A-4 validator only checks
*inline binding tokens* against the enums; a bare named profile passes. `spec_component_model §4.3` permits new domains
to register additional profiles producer-side; `spec_federation_contract §6.1` already names `comic`.

- **Do NOT** register `diagram`/`comic` as **built-in** profiles in `canvas_std.schema.SEMANTIC_PROFILES` — that would
  edit the immutable substrate and **would** require a LIP. Keep them producer-side.
- Any optional color/shape *defaults* a profile implies must stay within the `spec_adna_canvas_standard §6` enums
  (`VALID_COLORS` / `VALID_SHAPES`).

*Rationale:* zero Standard touch → zero LIP → no calendar-gate dependency; consistent with deck.

---

## D3 — Diagram shape-enum policy

**Recommended: SAFE PATH — Mermaid shapes ride `_reserved.qualities.shape`; the producer does NOT set baseline
`styleAttributes.shape`.** `VALID_SHAPES = {None, pill, diamond, parallelogram, circle, predefined-process, document,
database}` does **not** include Mermaid's `rect`/`round`/`stadium`. Setting an out-of-enum baseline `styleAttributes.shape`
would fail conformance **E-2** and break degradation **D-2**.

- Baseline node `type: "text"` (carrying the node `label`), `degrades_to: "text"`; the full Mermaid shape vocab lives
  in `_reserved.component_types[node].qualities.shape` (forward-compatible; validator preserves unknown qualities).
- *(Optional richer-degradation enhancement, deferred unless the operator wants it: for the two Mermaid shapes that
  ARE legal — `diamond`, `circle` — also set baseline `styleAttributes.shape` for a nicer stripped view. Default: do
  not, to keep E-2/D-2 trivially green.)*

*Rationale:* guarantees Extended-level conformance + clean degradation; mirrors how `deck_generator` carries image
substrate in `qualities` rather than baseline fields.

---

## D4 — Diagram-type scope for v1

**Recommended: ALL FIVE** (`flowchart`, `sequence`, `class_diagram`, `state_diagram`, `gantt`), built incrementally —
**flowchart + sequence as the first end-to-end vertical slice (A1.1)**, the remaining three in A1.2. The ported
`mermaid.py` already covers all five; the per-type canvas builders use a `_BUILDERS` dict (the `deck_generator/slides.py`
pattern), so adding types is incremental.

- *Edge-kind discipline (A-5):* flowchart/state edges → `dependency`/`reading_order` (may legitimately cycle);
  `sequence` reserved for gantt/strictly-linear order (must be acyclic).
- *Minimal alternative (if a single-session A1 is wanted):* ship flowchart + sequence only, defer class/state/gantt to
  a follow-on. The architecture supports it.

*Rationale:* a complete diagram layer is the goal; the vertical-slice-first sequence de-risks the pipeline before
breadth.

---

## D5 — Comic scope: data-driven engine vs baked Science-Stanley story

**Recommended: DATA-DRIVEN ENGINE; the legacy 32-page SS issue → `examples/` only.** The legacy `canvas_comic` engine
hard-codes one project (STANLEY/AGENT_STANLEY/HELIX characters, a 15-spread color-script, dual-protagonist story-state,
GHIBLI/PIXEL styles). The producer should keep the **mechanism** (lookups over characters/color-script/story-state) but
take those tables from the **input spec**, with the SS issue ported as the worked example — exactly how
`document_generator` ships generic genre *mechanism* + worked genre *instances* (whitepaper/grant).

Bundled sub-decisions (same default):
- **Drop** the legacy `ContextPack` file-existence gate (it required five vault files); carry the same five inputs
  (storyboard / character-bible / color-theory / prompt-engineering / voice) as **declarative** `context_object.refs`.
- **RLHF hints:** port the mechanism **dormant** (store-path optional, defaults to empty) so the prompt-assembly tests
  pass; ships inert. *(Alternative: omit entirely, ~90 LOC saved.)*
- **Issue dimensions:** page/spread counts are a **function of the input** (build a 4-page mini or a 48-page issue);
  32/16 survive only as the example's values and the quality-contract's "standard issue" band.
- **Spread layer:** model **both** — spread groups carry color/mood `region`s (matching the spread-keyed color-script),
  page groups are the sequenced reading unit. Fully additive + validator-clean. *(Minimal alternative: pages-only,
  color-script on the page region.)*

*Rationale:* substrate-neutrality is Mondrian's core operating principle — a "standard" producer must not bake one
brand's story; the SS issue proves the engine as an example.

---

## D6 — Codename / slug

**Recommended: Operation Atelier / `campaign_canvas_production`.** *Atelier* = a production studio (the production
layers Canvas owns); complements "Keystone" (which built the structural reference impl) and fits the Mondrian persona.
Cosmetic; rename freely.

---

## Ratification

| # | Decision | Default | Operator disposition |
|---|----------|---------|----------------------|
| D1 | Quality contracts | Yes — light diagram / full comic | ✅ Accepted (default) 2026-06-21 |
| D2 | Profiles producer-side | Yes, no LIP | ✅ Accepted (default) 2026-06-21 |
| D3 | Diagram shape-enum | qualities.shape; no baseline shape | ✅ Accepted (default) 2026-06-21 |
| D4 | Diagram-type scope | All 5; flowchart+sequence first | ✅ Accepted (default) 2026-06-21 |
| D5 | Comic scope | Data-driven; SS issue as example | ✅ Accepted (default) 2026-06-21 |
| D6 | Codename | Operation Atelier | ✅ Accepted (default) 2026-06-21 |

On ratification: set this record `status: ratified`, update the campaign Decision Points, complete mission A0.1 (+AAR),
set the campaign `status: active`, and open Phase A1 (author the A1.1 mission from the approved plan's diagram design).

> **✅ RATIFIED 2026-06-21** — the operator accepted all 6 defaults at the A0→A1 gate
> (`session_stanley_20260621_194755_a1_diagram_build`). Campaign activated (`status: active`); Phase A1 opened;
> the `diagram_generator` build is authorized.
