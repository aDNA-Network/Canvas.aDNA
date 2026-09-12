---
type: spec
spec_id: spec_conformance_suite
title: "aDNA Canvas conformance suite — checks for Core / Extended / aDNA-Native"
standard_version: "2.4.0"
status: ratified
created: 2026-06-12
updated: 2026-06-23
last_edited_by: agent_stanley
phase: P3
tags: [spec, canvas, conformance, validator, genesis, p3, interface, salon]
---

# aDNA Canvas Conformance Suite

> **Status: RATIFIED 2026-06-12 (operator, P2 gate) — P3 deliverable, HELD at the P3 exit gate.** Specifies the
> checks a validator runs for each conformance level + the degradation tests. It is a **contract**, not an engine —
> the reference validator is built later in `what/code/canvas_std/` (Option P / [[adr_001_canvasforge_relationship]]).
> Binds to [[adr_003_standard_governance]] §3 and [[spec_adna_canvas_standard]] §10. RFC 2119 keywords.

## 1. Validator contract

1.1. A conformant validator exposes `validate(doc, level) → {ok, level_reached, errors[]}` and
`strip(doc) → doc'` (removes `_reserved`). It lives in `what/code/canvas_std/` (the Standard ships its reference
tooling, Option P) — **not** in any producer.

1.2. Conformance is **monotone**: aDNA-Native ⊃ Extended ⊃ Core. `level_reached` is the highest level all of
whose checks pass. A document **MUST** declare its target level in `_reserved.conformance_level`; the validator
**MUST** verify the declared level is actually reached.

## 2. Core checks (C-*)

| ID | Check |
|----|-------|
| C-1 | Valid JSON; top-level `nodes` + `edges` arrays present. |
| C-2 | Every node has unique `id`, `type` ∈ {text,file,group,link}, integer `x`,`y`,`width`,`height`. |
| C-3 | Every edge has `id`, `fromNode`, `fromSide`∈sides, `toNode`, `toSide`∈sides; `fromNode`/`toNode` resolve. |
| C-4 | Every **directed** edge sets top-level `toEnd:"arrow"` ([[spec_adna_canvas_standard]] §5.2). |
| C-5 | `color` (if present) ∈ `"0".."6"` or `#`-hex. |

A Core-valid document **MUST** be a valid JSON Canvas 1.0 file (the degradation floor).

## 3. Extended checks (E-*)

| ID | Check |
|----|-------|
| E-1 | All of Core. |
| E-2 | `styleAttributes.shape`/`border`/`textAlign` ∈ the [[spec_adna_canvas_standard]] §6 enums. |
| E-3 | edge `styleAttributes.path`/`arrow`/`pathfindingMethod` ∈ §6 enums. |
| E-4 | Top-level `isStartNode`/`collapsed` are boolean; `portal`/`dynamicHeight` well-formed if present. |

## 4. aDNA-Native checks (A-*)

| ID | Check |
|----|-------|
| A-1 | All of Extended. |
| A-2 | `_reserved.adna_version` present + semver; `conformance_level` = `adna_native`. |
| A-3 | `_reserved.component_types` valid per [[spec_component_model]] §7 (keys resolve; `class`∈taxonomy; profile tokens∈§6; `degrades_to`∈baseline types). |
| A-4 | `_reserved.semantic_bindings` profiles use only §6 tokens; the built-in `lattice` profile is unmodified ([[spec_component_model]] §4.2). |
| A-5 | `_reserved.panel_link` valid per [[spec_panel_link_semantics]] §6 (region/edge + id-bearing surface ids resolve; `sequence` acyclic; exactly one `canonical` surface whose id resolves; a `role: derived` surface MAY omit its id — pure metadata, LIP-0008; no orphaned anchors). |
| A-6 | `_reserved.sync` present; `sync_hash` matches `compute_sync_hash(source)` **or** the canvas is flagged stale ([[spec_roundtrip_protocol_v2]] §3). |
| A-7 | `_reserved.context_object` (if present) valid per [[spec_context_object]] §4 (stable `id`; semver `version`; well-formed `refs`). |
| A-8 | `_reserved.authority` ∈ {`dual_channel`, `view`} and `_reserved.production` ∈ {`hand_authored`, `generated`} — the diagrammatic-context axes (LIP-0010 Option D, **cut into Standard v2.4.0** at Operation Gridline P1). Both **optional**, each validated **only if present**; one **asymmetric** cross-key rule: `authority` **requires** `production`, while `production` **alone is conformant**. |

> **A-8 in one line each.** `authority` answers *who owns the meaning?* (both values name an **other** channel that
> owns it); `production` answers *how is the picture made?* — and the **"never hand-edit; regenerate" discipline
> attaches to `production: generated`, to no value on the authority axis**. That split is the whole reason there are
> two keys: Canvas's own first two dual-channel canvases were `dual_channel` **and** machine-generated at once, and
> under the superseded three-value enum they could declare only the former. `generator` is **not** an `authority`
> value — it never answered that question.
>
> **Why the cross-key rule is normative, and why it is ASYMMETRIC.** `authority` with no `production` would let a
> canvas be *validly* `dual_channel` — *another channel owns my meaning* — while silently omitting the only field
> that says *do not hand-edit me*. That is the defect the axis split exists to remove, so that direction is a
> failure. The converse is **not**: `production` alone states complete information, and for an artifact no other
> channel owns it is the **correct** block.
>
> ⛩ **This row shipped symmetric ("two keys or neither") for the length of one phase, and that was a misreading
> corrected at the Gridline P1 exit gate** (F-GL-5, operator ruling 2026-09-11). LIP-0010's table cited the ruling's
> *"both become binding together"* — but that sentence is about **validation scope** (*if you validate either key you
> must validate both*, the argument for separating the fields at all), and LIP-0010 states it correctly four lines
> earlier as *"a two-key change or none"* before sliding into a per-document requirement.
> ⭐ **The symmetric rule was self-defeating, and this vault's own code is the proof**: `variant_board.py` and
> `tuning_surface.py` emit `production: generated` and deliberately omit `authority`, with a written reason (*a board
> built from a run manifest has no prose twin and no `.lattice.yaml`, so the authority question does not arise: the
> key is ABSENT, not a placeholder*). Under the symmetric rule their output was nonconformant **and could not be made
> conformant by regeneration** — only by inventing an authority value, which `conform.py` names as *"passing a value
> to make a number go green… the defect this signature used to force."* ⇒ ***a co-requirement read symmetrically
> forced back the defect it was written to prevent.***
>
> Source: [`pattern_diagrammatic_context`](../../aDNA.aDNA/what/patterns/pattern_diagrammatic_context.md) (aDNA.aDNA,
> ruled 2026-09-11, `status: draft` at 2 adoptions).
>
> ⚠ **A-8 requires nothing of a canvas that declares neither key**, and that is the correct answer rather than a
> concession: a **hand-authored primary artifact** — whose meaning nothing else owns — is out of the pattern's scope
> entirely ([`p1_under_coverage_ruling`](../../how/campaigns/campaign_canvas_plumbline/artifacts/p1_under_coverage_ruling.md),
> Plumbline P1). At the v2.4.0 cut, **21 of 25** in-vault aDNA-Native canvases carried neither key and all 25 pass.

### 4.1 Interaction-surface checks (I-*) — aDNA-Native (`_reserved.interaction`, optional)

Added at Operation Salon **P3** ratification (2026-06-22) for the leg-3 interface-surface contract
([[spec_interface_surface]] §4/§9). The family is **additive + optional** — a canvas without `_reserved.interaction`
satisfies I-1 vacuously, so existing aDNA-Native documents are unaffected. It rides `interaction_version: 1.0`,
**cut into Standard v2.2.0** at Operation Armature **P2** ([[adr_007_leg3_firewall_touch|adr_007]]). The reference
validator is **implemented in `canvas_std`** (`validate_interaction` on the aDNA-Native `validate()` path, surfaced
through `validate_suite` + the `canvas-std` CLI); I-2's anchor resolution **reuses the existing
`canvas_std::validate_anchors`** (now in-tree alongside it). The consumer (`canvas_context`) delegates to it — one
source of truth.

| ID | Check |
|----|-------|
| I-1 | `_reserved.interaction` (if present) valid per [[spec_interface_surface]] §4 — `interaction_version` semver; well-formed `affordances` / `responses` / `state`. |
| I-2 | Every `affordances[*].anchor` resolves (reuse `validate_anchors`); `kind ∈ {input, choice, annotation, action}`; `options[]` present **iff** `choice`. |
| I-3 | Every `responses[*].affordance` references a declared affordance; `value` is `kind`-consistent (`action` ⇒ null; `choice` ⇒ ∈ `options`); the response log is append-only-shaped. |

**Degradation** of the interaction layer is covered by §5: `strip(doc)` removes **all** `_reserved` (including
`_reserved.interaction`), so D-1..D-3 already prove **round-trip-to-baseline** for an interaction-bearing canvas
([[spec_interface_surface]] §8.2, the headline property) — no separate I-D row is needed.

## 5. Degradation tests (D-*) — the C4 contract

| ID | Check |
|----|-------|
| D-1 | `validate(strip(doc), core)` passes — stripping `_reserved` yields a valid Core/Obsidian canvas. |
| D-2 | `strip(doc)` introduces **no** new top-level node/edge keys and **no** `styleAttributes` token outside §6 (no-baseline-overload, [[spec_adna_canvas_standard]] §11.3). |
| D-3 | A vanilla JSON-Canvas reader opens `doc` without error (round-trip-to-baseline). |

A suite run **MUST** include D-1..D-3 for every aDNA-Native document — degradation is a first-class conformance property, not an afterthought.

## 6. Quality contract (separate from format conformance)

Format conformance (§2–§5) is distinct from **output quality**. Visual/narrative quality is reviewed via the
III framework against the **canvas review contract** Canvas.aDNA owns — the VR1–VR5 rubric + the canvas-visual
trap schema — specified in [[iii/CLAUDE]] (`iii/` wrapper). The conformance suite checks *format*; III checks
*quality*; the engines for both stay out of producers (`canvas_std` for format, III.aDNA for quality).

## 7. Conformance report

`validate` returns a report: `{ standard_version, level_reached, declared_level, passed: [ids], failed: [{id, node/edge, msg}], degradation: {D-1,D-2,D-3} }`. Producers attach it to a build artifact as evidence (feeds the P3 federation 5-stage gates §3 — `spec_federation_contract.md`).

## 8. Related
- [[adr_003_standard_governance]] §3 (levels) · [[spec_adna_canvas_standard]] §10 (validation) · [[spec_component_model]] · [[spec_panel_link_semantics]] · [[spec_roundtrip_protocol_v2]] · [[spec_interface_surface]] (leg-3 interface-surface contract — the `I-*` family §4.1) · `spec_federation_contract.md` · `what/code/canvas_std/` (reference validator, P-Option).
