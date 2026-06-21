---
type: decision
artifact_type: lip_draft
title: "LIP DRAFT — quote / footnote: dedicated component classes vs ride-on-text (B2)"
status: resolved
created: 2026-06-20
updated: 2026-06-20
last_edited_by: agent_stanley
phase: post-keystone
target_process: "lattice-labs/how/governance/lips/lip_0001_lip_process.md"
tags: [lip, draft, canvas, component-model, quote, footnote, errata, b2]
---

# LIP DRAFT — `quote` / `footnote`: dedicated classes vs ride-on-text (B2)

> **RESOLVED 2026-06-20 — option (ii) ride-on-text, applied as PATCH in v2.0.1.** Staged in Canvas.aDNA as the B2
> decision vehicle (LIP queue, `lip_queue_disposition.md`). The operator chose ride-on-text, which is a PATCH
> clarification (maintainer discretion, [[adr_003_standard_governance]] §2 — no lattice-labs LIP required). See
> **Disposition** below; the original options + recommendation are retained as the decision record.

## Disposition — RESOLVED 2026-06-20 (operator)

**Operator chose option (ii) — formalize ride-on-text.** Applied as a **PATCH** (errata) and folded into **v2.0.1**:
`spec_component_model.md` **§4.4** registers the canonical long-form `semantic_type` values (`quote`,
`block_quote`, `footnote`, `attribution`) on `class: text` plus the two SHOULDs; `canvas_std.reserved`
**`LONGFORM_SEMANTIC_TYPES`** gives the set a code home; the corpus fixture `adna_longform_quote.canvas` +
`tests/test_longform.py` lock the convention (a footnote's `qualities.ref` resolves via B1's `validate_anchors`).
Option (i) (dedicated `quote`/`footnote` classes, MINOR) was **not taken** — the §2 taxonomy stays at 14 classes
(Mondrian reduction). The draft body below is retained as the decision record.

## Summary

`spec_component_model §2` enumerates the component taxonomy — `text, typography_run, image, video, shape, embed,
group/panel, link/edge, table, code, caption, region` — with **no** `quote` / `blockquote` / `footnote` class.
Long-form quotes and footnotes currently ride on `class: text` + a `semantic_type` (`document_generator/blocks.py`
builds quote/citation as `text` nodes). Decide whether to add dedicated classes or to formalize the ride-on-text
pattern.

## Motivation

Discovered building `document_generator` (E4.1/E4.2): the long-form element set needs quote (+ attribution) and
footnote semantics, but the taxonomy offers no first-class home, so they degrade-by-default to anonymous `text`.
This is harmless to rendering but leaves "this block is a pull-quote" / "this is a footnote" implicit, which
weakens round-trip fidelity, citation tooling, and quality-lens targeting (III's figure/quote/citation checks).
Low severity — long-form already ships — but worth resolving so the grammar is explicit.

## Options

- **(i) Add `quote` + `footnote` component classes.** Extend `COMPONENT_CLASSES` (in `canvas_std/reserved.py`)
  and `spec_component_model §2` with two rows: `quote` (baseline carrier: `text`/`group`; degrades_to `text`) and
  `footnote` (carrier: `text`; degrades_to `text`). **MINOR** (v2.1.0) — additive to the taxonomy. Pros:
  first-class, self-describing; symmetrical with `caption`/`code`. Cons: grows the taxonomy (against the "reduce
  to the smallest grammar" doctrine); two more classes the conformance corpus + every consumer must learn.

- **(ii) Formalize ride-on-text *(recommended)*.** Keep the taxonomy at 14 classes; **register canonical
  `semantic_type` values** `quote`, `block_quote`, `footnote` (and `attribution`) for `class: text` in a
  documented long-form profile, with a SHOULD that quote blocks carry `qualities.attribution` and footnotes carry
  an explicit anchor reference (`qualities.ref` — already validated by B1's anchor check). **PATCH**
  (clarification). Pros: zero new classes; matches what already ships (E4.1/E4.2); non-breaking; the B1 anchor
  validator already gives footnote refs teeth. Cons: "quote" is a value, not a class — discoverability is via the
  profile registry, not the class list.

## Recommendation

**(ii) Formalize ride-on-text.** It honors the Mondrian reduction principle (the smallest grammar that expresses
the output), matches the shipped design, is non-breaking, and — via B1 — already has a resolution check for
footnote anchors. Re-evaluate (i) only if a downstream surface needs `quote`/`footnote` as a registry-level
first-class identity. **Operator decides.**

## Backwards compatibility

Both options are C4-safe (`text` carrier degrades cleanly). (i) is additive (no existing canvas invalidated).
(ii) changes nothing structural — it documents a convention + a SHOULD; existing canvases remain valid.

## Reference / related

- `spec_component_model.md §2` (taxonomy) · `spec_component_model.md §4` (semantic_bindings / profiles) ·
  `document_generator/src/document_generator/blocks.py` (current quote/citation-as-text) · `lip_queue_disposition.md`
  (B2 row) · B1 anchor validator (`canvas_std/reserved.py::validate_anchors`) — gives footnote refs resolution.
