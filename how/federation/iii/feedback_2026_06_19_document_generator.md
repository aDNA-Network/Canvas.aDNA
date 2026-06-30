---
type: feedback
created: 2026-06-19
updated: 2026-06-19
last_edited_by: agent_stanley
review_of: [what/production/document_generator/examples/canvas_standard_whitepaper.canvas]
reviewer: "Canvas.aDNA iii/ wrapper (III.aDNA v0.5.0) — 5-lens persona panel"
scope: structural
verdict: "0 High / 0 Med — SHIP; 2 Low + 1 GRAPH-GAP + 3 spec-gap errata candidates"
mission: mission_e4_1_lf_successor
tags: [iii, review, feedback, canvas, keystone, e4_1, document-generator, structural]
---

# Wired Canvas Review — document_generator (Keystone E4.1, the LF-successor)

The second **real** III review through the active Canvas `iii/` wrapper (III v0.5.0), exercising the method in
`what/production/document_generator/iii_quality_contract.md` against the new long-form consumer's worked example. Same
discipline as the E5.1 review ([[feedback_2026_06_19_canvas_consumers]]).

**Scope = STRUCTURAL.** No render loop exists yet (`canvas_presentation` lands at **PT P5**), so pixel-level VR1 checks
(font/contrast, page-break/orphan-widow pixels, the 24-criterion scoring) are **PT-P5-gated and out of scope** —
*deferred*, not *passed* (§Deferred). The review covers the object-level lenses over the `.canvas` artifact.

## DISPATCH

- **Engine:** III `skill_iii_review` (federation, not copy) via `iii/CLAUDE.md` `federation_ref` → III.aDNA v0.5.0
  (commit `0f06aa6`, oracle lattice 1.2.6).
- **Packs:** `context_iii_inspect_procedures` + `context_iii_introspect_checks` + `context_iii_learning_store` +
  `context_iii_canvas_visual` (the CV-* traps) + the **Canvas-owned VR1–VR5 contract** (standard-bearer inversion).
- **Panel:** 5 lenses from `iii/what/context/canvas_reviewers.yaml` — domain architect · quant/rigor · skeptical
  executive · information designer · accuracy auditor (invariant: ≥1 rigor + 1 accuracy lens, always).
- **Target:** `canvas_standard_whitepaper.canvas` (2 pages / 27 nodes / 23 edges); `profile: long_document`.
- **Audience parameter:** aDNA/Canvas technical reader (self-referential dog-food about the Standard).

## INSPECT — findings

**Structural metadata present (precondition — PASS):** every node carries `component_types[*].semantic_type`;
`panel_link` has typed `edges` (reading_order / sequence / adjacency), exactly one `canonical` surface (`doc_root`),
per-page regions with `extent.unit: pages` + a document `extent.unit: words`; `isStartNode` on `page0`; the
`sequence` chain `seq_0` is acyclic; `context_object.refs` present. **First exercise of the `code` component class**
(degrades_to `text`, fenced) — clean. Figure→file (vault path) and figure→link (http) both carry `degrades_to`. The
review surface is real.

| ID | Lens / trap | Location | Severity | Finding |
|----|-------------|----------|----------|---------|
| F-E41-001 | accuracy auditor + info designer | all 5 citation `link` nodes | **Low** | The authored `sources[].label`s (e.g. "JSON Canvas 1.0 specification", "adr_003 — Standard governance") degrade to **bare URL `link` nodes** — baseline JSON Canvas link nodes have no anchor-text slot — so provenance is present in-spec but renders label-less. **Recurrence of `CANVAS-L-001`** (first seen E5.1 on brief_consumer); now seen across **2 sessions / 2 producers** → ACCUMULATE bump (freq 2). |
| F-E41-002 | information designer | producer layout (`layout.py` / `blocks.py`) | **Low** | The E4.1 layout is a **single-pass deterministic vertical stack**: it does not reflow or re-paginate, so a content-heavy page can overflow its fixed page box (content extends past `page{p}` bounds). Conformance is unaffected (geometry is positional; pages stay within `doc_root`), but visual fidelity needs real pagination. New candidate `CANVAS-L-002`; the reflow/auto-pagination engine is an **E4.2 / PT-P5** layout concern. |
| F-E41-003 | CV-PENDING-01 (GRAPH-GAP) | `page0` Fig 1 (vault path) + `page1` Fig 2 (http) | **Deferred** | Both figures reference assets that need not resolve at build (intentional per the `.yaml` — conformance + image→file/link degradation are what's tested). Logged to GRAPH-GAP: **at PT P5 the render loop must gate asset resolution via CV-PENDING-01** (no page ships "done" with an unresolved figure). Mirrors deck F-E51-004. |

**Not firing (checked, clean):** CV-CONFIDENCE-01 — every present-tense claim verifies against the in-vault specs
(3 monotone levels per `validate.py`; closed taxonomy = `COMPONENT_CLASSES` frozenset; source/view authority per the
round-trip docstring; `adna-canvas-std` zero-dep per its `pyproject`; the embedded `from canvas_std import …` snippet
uses only real exports; LIP/semver governance per `adr_003`) · CV-TEMPLATE-01 (Standard-specific, not filler) ·
CV-AUDIENCE-01 (one mode — dense technical whitepaper) · CV-INSIDER-CONTEXT-01 (Abstract sets the premise; aDNA-Native
is defined in the levels table before it is leaned on) · CV-HIERARCHY-01 (heading `typography_run` + `## ` + color vs
body `text` vs `caption` — distinct) · CV-COHERENCE-01 (node typing consistent; **containment holds** — pages within
`doc_root` bounds, verified: doc h=2432 ⊇ page1 bottom=2352).

## Spec-gap errata candidates surfaced (the E4.3/E4.4 "consumer reveals a Standard gap" pattern)

Building the first **§5 long-form** consumer surfaced three Standard/impl gaps. **Recorded, not fixed** — any real fix
is a governed LIP (`adr_003` §2); filed to STATE watch items + the mission AAR:

1. **Orphan/anchor + `naming_convention` validator absent (headline).** `spec_panel_link_semantics` §5.3/§6 says the
   Standard **owns** link-existence ("a validator **MUST** check … no orphaned anchors" + `naming_convention`), but
   `canvas_std/reserved.py::validate_panel_link` implements **no** anchor/orphan/naming sub-check. A spec-vs-impl
   conformance gap; the long-form profile is exactly where cross-references live. → **v2.0.x erratum (A-5 sub-check).**
2. **No dedicated `quote`/`blockquote` or `footnote` component class.** Long-form quote rides on `text` +
   `semantic_type=quote` (+ a `> ` markdown prefix); a footnote/endnote has no class and an ambiguous degrade target.
   → component-model **erratum candidate** (additive class, or a documented "rides on text" convention).
3. **`sequence`-unit ambiguity for paginated multi-section docs.** §5.1 expresses order-lock as a `sequence` chain over
   **section-panels**; this consumer chains `sequence` over **pages** (deck-analog) and uses `reading_order` across
   sections, leaving the `region` component class unexercised. → spec-clarity **erratum** (which unit owns `sequence`
   when pages *and* sections are both ordered).

## INTROSPECT — calibration

- **Honest gradient:** findings are Low/editorial/spec-gap, not inflated. The artifact was carefully authored and is
  green on `canvas_std` (18/18 tests); a credible review finds *real Low* + *real spec gaps*, not nothing and not theatre.
- **Denominator:** F-E41-001 rests on **all 5** citation nodes + the structural inevitability (baseline link nodes lack
  a label slot) — and it now recurs across two independent producers, which is the real signal.
- **No cross-voice escalation:** no single location drew 2+ lenses at Med+, so nothing escalates (registry rule).
- **Structural-only honesty:** VR1 pixels + the render/pagination traps are recorded as **deferred**, never marked pass.

## IMPROVE — dispositions (human gate)

All findings are **Low**; none blocks ship. Per III (IMPROVE → human gate → ACCUMULATE), nothing is force-applied —
the package + its 18 tests are left **green and untouched** (this review wires the gate; it is not a content-churn pass).

| ID | Proposed fix | Owner | Disposition |
|----|--------------|-------|-------------|
| F-E41-001 | Producer-side: emit an adjacent caption/`text` node carrying the label, or fold it into `component_types[node].qualities.label`; **or** a Standard-side link-label-carry errata. Do **not** force a label into the baseline link node. | document_generator / Standard | Errata — accepted, deferred (= `CANVAS-L-001`) |
| F-E41-002 | Add reflow/auto-pagination (measure content, break pages) — naturally an E4.2 format-contract concern (`length_window` → page breaks) and a PT-P5 render concern. | document_generator (E4.2/P5) | Errata — accepted, deferred (= `CANVAS-L-002`) |
| F-E41-003 | At PT P5, gate figure asset resolution via CV-PENDING-01 in the render loop. | PT P5 (`canvas_presentation`) | GRAPH-GAP — deferred to P5 |
| Errata 1–3 | Address via the `adr_003` LIP process (orphan validator / component classes / sequence-unit clarity). | Standard (Canvas.aDNA) | v2.0.x erratum candidates — logged, not fixed |

## ACCUMULATE

- **`CANVAS-L-001`** bumped frequency 1 → **2** (+ this session + the whitepaper surface). The cross-session bar (≥ 2
  sessions) is now met; graduation still needs frequency ≥ 3 + acceptance ≥ 0.80 + Stanley/Argus gate (III ADR-003 §3)
  — **not** met; stays local.
- **`CANVAS-L-002`** (`fixed_stack_overflow_no_repagination`) written as a new local candidate (freq 1).
- Canonical III store untouched (read-only from the consumer side; md5 `5adb0dfa38d9224649c3b2cba83852ae` invariant).

## Verdict

**0 High / 0 Med across all structural lenses → SHIP.** The document_generator is green on `canvas_std` (18/18) and now
carries the quality gate. 2 Low + 1 GRAPH-GAP tracked as errata; 3 spec-gap erratum candidates filed for the LIP queue.
The long-form profile is proven end-to-end (multi-page, `code` first-use, round-trip-stable, degrades to a valid
Obsidian canvas), with the pixel/render + pagination half correctly deferred to PT P5.

## Deferred to PT P5 (canvas_presentation render loop)

VR1 text-readability (font/contrast pixels) · long-form pagination (reflow, orphan/widow, page breaks — see F-E41-002) ·
the 24-criterion scoring + hard gates · CV-CONTRAST-01 · CV-PENDING-01 (figure resolution, see F-E41-003) ·
CV-DIMENSION-VISIBILITY-01 pixel viewport (structure already carries page dims).

## Related
- Method: `what/production/document_generator/iii_quality_contract.md` · Panel: `iii/what/context/canvas_reviewers.yaml` ·
  Store: `iii/what/context/canvas_iii_learning_store.jsonl` · Wrapper: `iii/CLAUDE.md` (v0.5.0).
- Prior review: [[feedback_2026_06_19_canvas_consumers]] (E5.1, brief + deck). Engine: `III.aDNA/how/skills/skill_iii_review.md`.
