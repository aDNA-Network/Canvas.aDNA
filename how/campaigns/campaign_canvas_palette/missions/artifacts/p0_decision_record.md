---
type: decision_record
created: 2026-06-21
updated: 2026-06-21
status: ratified
last_edited_by: agent_stanley
campaign_id: campaign_canvas_palette
mission: mission_p0_charter_triage
tags: [canvas, production, palette, decision, p0, factory, letter, post]
---

# P0 Decision Record — factory + producer triage (Operation Palette)

**Purpose:** resolve the six governance/scope questions that gate the producer factory and the letter/post builds,
**before any code**. Each decision carries a doctrine-aligned **recommended default** and rationale. The operator
ratifies (accept / edit) at the **P0→P1 gate**; ratification **activates** Operation Palette and authorizes the P1
factory build.

> **Landscape (confirmed):** no `letter_generator`/`post_generator` (or poster/one-pager) exists in `what/production/`;
> no dedicated `spec_letter_*`/`spec_post_*` in `what/specs/`. **Letter** appears only as a worked-consumer *sketch*
> (`spec_federation_contract §6.3`: one-page, `profiles_used: [document]`, single region `flow: vertical`,
> `pagination: paged`, `extent: {unit: pages, max: 1}`) plus incidental mentions in `spec_component_model` /
> `spec_panel_link_semantics`. **Post/social** appears only incidentally in `spec_federation_contract`. **No new
> Standard spec is required** — both producers operate entirely within ratified specs + the `_reserved` namespace
> (profiles producer-side). The short *post domain* model (D4) is producer-side scope, not a Standard spec.

---

## D1 — Codename / slug

**Recommended: Operation Palette / `campaign_canvas_palette`.** *Palette* = completing the full set of primary outputs
(Mondrian's primary-color palette; the "full palette" of 2D outputs the thesis names). Complements Keystone (structural
reference impl) and Atelier (production studio). Cosmetic; rename freely.

---

## D2 — Factory artifact homes (skill + scaffold)

**Recommended: skill at `how/skills/skill_canvas_producer_build.md` (single-file `agent` skill via `template_skill.md`)
+ scaffold at `what/production/_scaffold/`.**

- **Skill** operationalizes `context_canvas_producer_pattern.md` into a step-by-step runbook: the 4-step pipeline,
  package shape, the "four+1" suite, the venv recipe, the conformance-vocabulary checklist (`BASELINE_TYPES`,
  `PL_EDGE_KINDS` — only `sequence` acyclicity-checked, `PL_EXTENT_UNITS={words,pages,slides}`, `VALID_SHAPES`, A-5),
  and the firewall + `iii/` gate. Registered in the CLAUDE.md skills inventory + `how/skills/AGENTS.md` examples at close.
- **Scaffold** lives at **producer depth** (`what/production/_scaffold/`) so the `../../code/canvas_std` relative paths
  in `pyproject.toml`/venv recipe stay valid on clone (a `how/templates/` home would break them). Inert copy-me
  skeleton: `pyproject.toml`, `README.md`, `AGENTS.md`, `iii_quality_contract.md`, `.gitignore`,
  `src/<name>/{model,consume,layout,__main__,__init__}.py` (TODO-stubbed), `tests/` (conftest + four+1 as TODO stubs),
  `examples/`. **Excluded from the cross-producer sweep** (the sweep enumerates named producers; `_scaffold` ships
  TODO-stub/skipped tests and no committed `.venv`).

*Rationale:* the scaffold-at-producer-depth keeps clones path-valid; the underscore prefix marks it a non-producer.

*Alternative considered:* scaffold under `how/templates/template_producer_scaffold/` — rejected (relative-path breakage
on clone; templates dir is markdown-template-shaped, not a runnable package).

---

## D3 — Letter conformance level

**Recommended: `adna_native` (family uniformity)** over the `spec_federation_contract §6.3` `extended` minimal-proof
sketch. All five existing producers emit `adna_native`; building letter at the same level keeps the family uniform,
exercises the full enrichment pipeline (so it's a true factory acceptance test), and still degrades to a valid Obsidian
canvas. The §6.3 geometry is otherwise adopted verbatim: single canonical surface, one `region`
`{flow: vertical, pagination: paged, extent: {unit: pages, max: 1}}`, `profile: document`.

*Alternative:* honor §6.3's `extended` "minimal producer" framing (less `_reserved`, proves a thin producer also
conforms). Rejected as default — uniformity + full-pipeline exercise are worth more than a minimality demo, and a
degradation test already proves the thin path.

---

## D4 — Post domain model

**Recommended: model BOTH a single post and a thread; platform profiles producer-side; image support as metadata.**

- **Shape:** one canonical `group` surface containing **post panels**. A single post = one panel; a **thread** = an
  ordered chain of panels linked by `sequence` (strictly linear, **acyclic** — A-5 safe; never `adjacency`-cycle).
- **Platform profiles (producer-side):** `{"profile": "post"}` in `semantic_bindings`, with a producer-side profile
  table (e.g. `twitter`/`x`, `linkedin`, `instagram`) carrying **char budget** + **aspect-ratio/geometry** hints. No
  registration in `canvas_std.schema` (substrate stays immutable).
- **Image support:** a post panel may carry an optional `image`-class node whose `qualities.image_prompt` holds the
  prompt; the producer **never renders** (ComfyUI owns pixels) — mirrors `comic_generator` exactly (C8).
- **Char limits:** advisory in the profile + surfaced in the `iii_quality_contract.md` (a *contract* dimension), not
  hard-enforced in baseline fields.

*Rationale:* threads are the high-value social shape and reuse the proven multi-panel `sequence` pattern; platform
variation is exactly what producer-side profiles are for; the image boundary matches existing doctrine.

*P3a note:* a short producer-side `post` model doc is authored at P3 entry (not a Standard spec).

---

## D5 — Producer names

**Recommended: `letter_generator`, `post_generator`** (mirror `deck_generator`/`diagram_generator`/`comic_generator`;
`*_consumer` is reserved for the brief's consume-only framing).

---

## D6 — Optional stretch producers (poster / one-pager)

**Recommended: DEFER to P4-if-budget; not committed.** The campaign's committed scope is the factory + letter + post.
Poster/one-pager are layout-driven single-surface producers that the factory should make cheap; pick them up at P4 only
if context budget remains, else log to backlog for a future "fill-in-the-blanks" pass.

---

## Ratification

| # | Decision | Default | Operator disposition |
|---|----------|---------|----------------------|
| D1 | Codename / slug | Operation Palette / `campaign_canvas_palette` | ✅ Accepted (default) 2026-06-21 |
| D2 | Factory artifact homes | skill `skill_canvas_producer_build.md` + scaffold `what/production/_scaffold/` | ✅ Accepted (default) 2026-06-21 |
| D3 | Letter conformance level | `adna_native` (not §6.3 `extended`) | ✅ Accepted (default) 2026-06-21 |
| D4 | Post domain model | single + thread; platform profiles producer-side; image as metadata | ✅ Accepted (default) 2026-06-21 |
| D5 | Producer names | `letter_generator`, `post_generator` | ✅ Accepted (default) 2026-06-21 |
| D6 | Optional stretch | Defer poster/one-pager to P4-if-budget | ✅ Accepted (default) 2026-06-21 |

On ratification: set this record `status: ratified`, update the campaign Decision Points, complete mission P0.1 (+AAR),
set the campaign `status: active`, and open Phase P1 (author the P1 mission — build `skill_canvas_producer_build.md`
+ `what/production/_scaffold/` from the approved plan + `context_canvas_producer_pattern.md`).

> **✅ RATIFIED 2026-06-21** — the operator accepted all 6 defaults at the P0→P1 gate
> (`session_stanley_20260621_234513_palette_p1_factory`). Campaign activated (`status: active`); Phase P1 opened;
> the factory build (`skill_canvas_producer_build.md` + `what/production/_scaffold/`) is authorized.
