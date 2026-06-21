---
type: decision
title: "LIP queue disposition — the 4 post-Keystone spec-gap errata (B1–B4)"
status: active
created: 2026-06-20
updated: 2026-06-20
last_edited_by: agent_stanley
phase: post-keystone
tags: [decision, standard, lip, errata, governance, disposition]
---

# LIP Queue Disposition — B1–B4

> Triage of the 4 spec-gap errata handed off at Operation Keystone close
> (`how/campaigns/campaign_canvas_genesis/missions/artifacts/e6_3_handoff_register.md` §B), discovered while
> building the in-vault consumers (E4.1/E4.2). Governs the work in `how/missions/mission_lip_queue_errata.md`.
> Version policy reference: [[adr_003_standard_governance]] §1 — **MAJOR** baseline-incompatible (rare) ·
> **MINOR** additive `_reserved`/conformance-optional · **PATCH** clarifications/errata. Change process: §2 —
> normative changes ride a LIP; **editorial/errata may skip the full LIP at maintainer discretion (aDNA Labs)**.

## Summary table

| # | Erratum | Severity | Class | Version | This session |
|---|---------|----------|-------|---------|--------------|
| **B1** | Orphan-anchor + `naming_convention` validator absent (`spec_panel_link_semantics §5.3/§6` mandates it; `canvas_std::validate_panel_link` lacks it) | Med (headline) | Reference-impl gap + spec sharpening | **PATCH → v2.0.1** | **Implement** |
| **B3** | `sequence`-unit / pagination-construct ambiguity (region vs page-panel) | Med | Clarification | **PATCH → v2.0.1** | **Clarify in-spec** |
| **B2** | No dedicated `quote`/`blockquote`/`footnote` component class | Low | Design fork (taxonomy) | MINOR (v2.1.0) *or* PATCH | **Draft + gate** |
| **B4** | Derived-surface backing node — A-5 forces a synthetic `region` marker; allow surface-as-pure-metadata? | Low→Med | Design fork (conformance) | MINOR (v2.1.0) *or* PATCH | **Draft + gate** |

All four are **C4-safe**: each is `_reserved`-scoped (or a reference-impl check) — stripping `_reserved` still yields a valid baseline canvas; none touches a top-level node/edge key or a `styleAttributes` token. None blocks a valid v2.0.0.

## Closeout — operator decisions (2026-06-20)

The four gates were taken at the post-Keystone closeout (`session_stanley_20260620_200612_lip_queue_closeout`):
- **B1, B3** — implemented/clarified the prior session; **cut into v2.0.1** here.
- **B2** — operator chose **(ii) ride-on-text**; **applied as PATCH**, folded into **v2.0.1** (`spec_component_model`
  §4.4 + `canvas_std.reserved.LONGFORM_SEMANTIC_TYPES` + `adna_longform_quote` fixture/test). Draft
  `lip_draft_text_quote_footnote_class.md` → resolved.
- **B4** — operator chose **(ii) pure metadata**; a **MINOR** A-5 relaxation, so **direction locked but not applied**
  — it rides a lattice-labs LIP (≥7-day review) → **v2.1.0**. Draft `lip_draft_derived_surface_metadata.md` updated.
- **v2.0.1** — **cut 2026-06-20** (B1 + B3 + B2); see Release packaging.

---

## B1 — orphan-anchor + `naming_convention` validator  ·  PATCH → v2.0.1  ·  IMPLEMENT

**Gap.** `spec_panel_link_semantics` §6 says a validator **MUST** check "no orphaned anchors"; §5.3 says `caption` components + cross-references use a `naming_convention` + an orphan check. `canvas_std/reserved.py::validate_panel_link` checks edges/regions/surfaces resolution, sequence acyclicity, and the one-canonical-surface rule — but carries **no** anchor / orphan / `naming_convention` code (the strings don't appear anywhere in `canvas_std`).

**Anchor model (pinned from the E4.2 consumer).** The producer (`document_generator`) emits, into `_reserved.semantic_bindings.{format,visual}`:
- `naming_convention` (F7/X8) = `{label_form: descriptive|legacy, migration_rule: <str>}` — how figure/section **labels** are formed.
- `orphan_detector` (X2) = `{mode: label_ref|src_cited, threshold: <0..1>}` — config selecting *how* orphans are found. `model.py:128` explicitly defers the **traversal engine** to "a p3_08/PT-P5 voice."
- `caption` components are text nodes positioned by the figure; they carry **no** explicit `ref` today.

**Disposition — the Standard owns the *declaration*, not the *engine* (C8).** The reference validator enforces the declarative anchor layer:
1. `naming_convention.label_form ∈ {descriptive, legacy}`; `migration_rule` is a string — wherever declared (`semantic_bindings.format`/`visual`, or `panel_link`).
2. `orphan_detector.mode ∈ {label_ref, src_cited}`; `threshold` a number in `[0,1]` — when present.
3. Every **explicit** component anchor-reference resolves (a component `qualities` key in {`ref`, `anchor`, `anchor_ref`, `cites`, `for`} must point at an existing node id or a declared `panel_link.anchors` label) — **no orphaned anchor**.
4. Optional `panel_link.anchors` map (label → node id): every entry resolves.

The orphan-**traversal** engine (scanning prose for "Figure 2" refs per `orphan_detector.mode`) stays producer/PT-P5 — consistent with `model.py:128` and the Standard's recurring "fixes the declaration, not the engine" rule (§4/C8).

**Why PATCH.** No spec *rule* changes — §6 already mandates the check; this fills the reference-impl gap and **sharpens** §5.3/§6 to define the (previously under-specified) anchor model. Errata; skippable-LIP at maintainer discretion. A well-formed canvas still validates (every existing consumer canvas declares well-formed conventions with no explicit anchor-refs → passes vacuously); only a malformed declaration or an unresolved explicit ref newly fails — and those were already non-conformant under §6.

---

## B3 — pagination-construct clarification  ·  PATCH → v2.0.1  ·  CLARIFY

**Ambiguity.** Which construct "owns" pagination — a `region` or a page-`panel`? Sharpened once E4.2 exercised the `region` class.

**Resolution (the spec is already nearly explicit; make it normative).** A **page/slide is a `panel`** (a `group` component, §2) that **carries `region` pagination properties** (`flow`/`pagination`/`extent`, §4). Pagination is **declared on the region**; inter-page/section order is a **`sequence` chain** whose unit is the **section-panel** (§5.1). The shipped `document_generator` confirms this exactly: each `page{g}` is `{class: panel, semantic_type: page}` **and** carries a `regions[page]` entry with `pagination: paged`, linked by `seq_{i}` `sequence` edges (`consume.py:178–201`). No structural change — added clarifying text to §4 + §5.1.

**Why PATCH.** Clarification/errata of existing rules; no new feature.

---

## B2 — no dedicated `quote`/`blockquote`/`footnote` class  ·  MINOR or PATCH  ·  DRAFT + GATE

**Gap.** `spec_component_model §2` has `text, typography_run, image, video, shape, embed, group/panel, link/edge, table, code, caption, region` — **no** `quote`/`blockquote`/`footnote`. Long-form rides on `text` + `semantic_type` (`document_generator/blocks.py` builds quote/citation as `text`).

**Design fork (operator decides — `lip_draft_text_quote_footnote_class.md`):**
- **(i) Add `quote` + `footnote` component classes** — MINOR (v2.1.0); touches `COMPONENT_CLASSES`, `spec_component_model §2`, and the conformance corpus.
- **(ii) Formalize ride-on-text** — register canonical `semantic_type`s `quote`/`footnote` (degrade to `text`) in a documented profile — clarification (PATCH).

**Recommendation: (ii).** It matches the design already shipped (E4.1/E4.2 long-form rides on `text` + `semantic_type`), keeps the taxonomy minimal (Mondrian "reduce to the grammar"), and is non-breaking. **Gated** — not applied this session.

---

## B4 — derived-surface backing node  ·  MINOR or PATCH  ·  DRAFT + GATE

**Gap.** A-5 (`spec_conformance_suite`) requires every `panel_link.surfaces[].id` to resolve to a node. A **derived** surface (`html`, `funder_portal`) has no content, so `document_generator/consume.py:126–135` mints a **synthetic `region`-class marker** node (`surface_<name>`, `role: derived_surface`) purely to satisfy A-5.

**Design fork (operator decides — `lip_draft_derived_surface_metadata.md`):**
- **(i) Keep requiring a backing node** — document the `region`-class `derived_surface` marker pattern as canonical; optionally teach the validator to recognize `role: derived_surface`. Clarification (PATCH).
- **(ii) Relax A-5** — allow `role: derived` surfaces to be **pure metadata** (no id / no node), so producers stop minting marker nodes. Additive conformance-optional (MINOR, v2.1.0); touches `validate_panel_link` surface check + A-5 + §5.2.

**Recommendation: lean (ii)** (removes a synthetic-node wart; the canonical surface remains the single round-trip authority so a metadata-only derived surface is harmless) — but this is a genuine conformance call; **operator decides.** Not applied this session.

---

## Release packaging

- **v2.0.1 — CUT 2026-06-20** (operator authorized). B1 (validator + §5.3/§6 sharpen) + B3 (§4/§5.1 clarification)
  + **B2** (ride-on-text §4.4 + `LONGFORM_SEMANTIC_TYPES`) bumped `STANDARD_VERSION` `2.0.0` → `2.0.1` (the
  reference impl's *reported* version + schema identity-title + test assertions). **One-shot bump applied at:**
  `STANDARD_VERSION` (`canvas_std/__init__.py`) · schema `title` + `x-standard-version` (keep `$id` — structural
  schema unchanged) · `conformance.py` CLI/doc strings · `test_smoke.py` (×2) + `test_conformance.py` (×1)
  assertions · the 7 `what/specs/spec_*.md` `standard_version` frontmatters · `spec_federation_contract.md` §2.1
  example — all `2.0.0` → `2.0.1`. Fixtures' `_reserved.adna_version` stays `2.0.0` (a 2.0.0 canvas stays valid
  under the 2.0.1 validator). Then re-run `pytest`/`ruff` (expect green) + the 4 example-canvas validations.
- **v2.1.0 (next):** **B4** pure-metadata (operator-approved direction 2026-06-20) lands here as a **MINOR** A-5
  relaxation via the LIP process (Draft → submit to lattice-labs → review ≥7d → Final). B2 already landed in v2.0.1 (PATCH).
- **Alternative considered:** hold the *whole* errata until B2/B4 are decided and cut one release. **Rejected** —
  the B1 conformance content (the silent §6 gap) is done now; only the version *label* waits on the operator.
