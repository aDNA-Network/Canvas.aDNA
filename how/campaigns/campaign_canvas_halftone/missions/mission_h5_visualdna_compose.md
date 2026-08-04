---
type: mission
mission_id: mission_h5_visualdna_compose
campaign_id: campaign_canvas_halftone
phase: H5
status: completed
owner: stanley
persona: Mondrian
executor_tier: fable
token_budget_estimated: "1 session slice (shared with HR/HF) — 1 new module + 4 edits + ~20 tests + docs + 1 staged memo"
created: 2026-08-04
updated: 2026-08-04
last_edited_by: agent_mondrian
relates: ["halftone_roadmap.md §1 (manifest characters[]) + §2 H5 row", "halftone_gap_register.md G2", "coord_2026_07_28_callisto_to_mondrian_lorales_compose_and_dispatch_seam.md", "coord_2026_08_03_mondrian_to_callisto_h5_and_seam_reply.md"]
tags: [mission, halftone, h5, visualdna, compose, lora_less, reference_images, comic_generator]
---

# Mission: H5 — VisualDNA auto-compose (`compose_input.py`)

## Intent

Close gap **G2** (VisualDNA never composed into comics): bundles → enriched ComicInput + per-panel manifest
`characters[]` (`{name, trigger_word?, lora_ref?, reference_images[]?}`). Gate: the 2026-08-04 plan approval
(HV/H2 precedent). **Exit criterion (operator-locked, 2026-08-03 amendment): LoRA-less compose
(reference-images-only) exercised + tested — Bearly's *required* path (rights-HELD LoRA); notify Bearly at close**
(memo staged; delivery = per-send GO).

Placement ruling (AST-guard-driven): compose lives in **comic_generator** (comic_render may never import the
producer; handoff stays file-shaped — producer emits `qualities.characters`, `comic_render/extract.py:240`
already lifts it).

**G2 register reconciliation (recorded):** the register's "Stanley v0.3.1 · 6 reference images · trained-LoRA
belief" is stale — the live bundle is **v0.1.13** (2026-08-04), dozens of references across categories, and both
`lora_refs.entries` remain `PENDING_TRAINING` (`trained_at: null`). Bearly's bundle is v0.1.0 draft,
`lora_refs: []` **⛔ rights-HELD**, sole portrait `canonical: false`, paths **vault-root-relative** (vs Stanley's
bundle-dir-relative) — both live conventions must compose.

## Objectives

| # | Objective | Status |
|---|-----------|--------|
| **O1** | `compose_input.py` (content-layer: stdlib+yaml only): `load_bundle` (4 live `lora_refs` shapes: list · `entries:` mapping · placeholder string · absent; draft/non-character warnings) · `select_lora` (**pair-only**: `trigger_word`+`lora_ref` emitted together iff one entry is `TRAINED\|VALIDATED`; PENDING_TRAINING ⇒ both omitted — untrained trigger tokens are inert/harmful, spec §5) · `select_reference_images` (**canonical-first**, categories `{portraits, expressions, scenes}` + override; `restricted`+`discarded` excluded by substring; bundle-dir-then-vault-root resolution; **workspace-root-relative** emission; warn+skip / `--strict-refs`; cap 6) · `derive_descriptor` (compressed → portrait → full_prompt_inline; >800-char warning) · `match_bundle_to_character` (explicit `name=path` wins; direction-safe heuristic; ambiguity = hard error; panel-only chars get auto bible rows) · `enrich_comic_dict` (raw-YAML-dict enrichment; in.yaml descriptor wins; `composed_from:` provenance) | ✅ |
| **O2** | `model.py`: `CharacterDescriptor` + optional `trigger_word`/`lora_ref`/`reference_images`; `from_dict` mapping; `ComicInput.character_assets()` | ✅ |
| **O3** | `panels.py` + `consume.py`: emit `qualities.characters` **only** for panel characters with ≥1 asset field (key omitted otherwise — existing tests + committed comic_render fixture untouched by construction) | ✅ |
| **O4** | `__main__.py`: argparse refactor (`build` byte-compatible incl. exit codes) + `compose <in.yaml> -o <out.yaml> --bundle [name=]<path>…` + `build --bundle` one-shot | ✅ |
| **O5** | Tests: `test_compose_input.py` (incl. the named **`test_lora_less_compose_reference_images_only`** exit-criterion test; committed YAML fixture bundles + tmp `.aDNA` trees + generated 1-px PNGs; live Stanley/Bearly smokes skip-if-absent) · `compose_input.py` appended to `CONTENT_MODULES` (`test_model_neutrality.py`) · +1 `comic_render/tests/test_extract.py` lift test | ✅ |
| **O6** | Docs: README + AGENTS.md (pairing invariant · compose-before-plan ordering) · `what/docs/comic_prompt_contract.md` dated amendment (`qualities.characters` = structured asset channel, distinct from Layer-2 text) | ✅ |
| **O7** | Verification (producer suite + sweep + comic_render + firewall 0) + staged Callisto close-notify memo | ✅ |

## Verification (run 2026-08-04 — all green)

- **`comic_generator` 123 passed** (100 baseline + 23 new; `ruff` clean). The exit-criterion test
  **`test_lora_less_compose_reference_images_only`** proves both live bundle shapes (Stanley-like
  PENDING_TRAINING + Bearly-like `lora_refs: []`) compose to reference-images-only — zero
  `trigger_word`/`lora_ref` anywhere in the enriched dict OR the built canvas.
- **Live-bundle smokes green** (read-only cross-vault): Stanley v0.1.13 → LoRA-less, `ScienceStanley.aDNA/…`
  refs, portrait-subset descriptor; Bearly v0.1.0 → LoRA-less, `Bearly.aDNA/…` refs.
- **7-producer sweep 259** (10 · 16 · 37 · 36 · **123** · 17 · 20 — only comic moved). **`comic_render` 73**
  (72 + the new lift test; committed fixture + src untouched — the H2-reserved seam consumed as-designed).
- E2E CLI: `compose` → enriched YAML reloads via `load_comic` → `build` carries `qualities.characters`;
  `build --bundle` one-shot equivalent; provenance idempotent on recompose.
- **Firewall: `git diff --stat -- what/code/canvas_std/` empty** (and `canvas_context/` empty).

## AAR (SO-5)

- **Worked:** the H2-reserved seam (`PanelSpec.characters` + the `extract.py` lift) meant H5 landed entirely
  producer-side with zero `comic_render` src changes; raw-dict enrichment (no model round-trip) preserved
  unknown YAML keys by construction.
- **Didn't:** the plan-time design survived contact only because exploration had already overturned two of its
  rules — the spec's canonical list-form `lora_refs` exists in NO live bundle (Stanley nests `entries:`), and
  Bearly's sole portrait is `canonical: false`, killing canonical-ONLY selection before it shipped.
- **Finding:** "graceful degradation" clauses become real only when a consumer tests them — both live bundles
  are LoRA-less in practice (PENDING_TRAINING / rights-HELD), so reference-images-only is the fleet's *actual*
  path today; the pair-gate turns spec §5's label-hygiene warning into an enforced invariant.
- **Change:** reference selection went canonical-FIRST with category overrides (`--ref-category`) so Bearly's
  self-declared primary references (`series_panels`) are reachable without an anchor election.
- **Follow-up:** (1) H3+: dispatch/refine consumption of `characters[]` (the pro-image class accepts reference
  images — pre-ruled 2026-08-04); (2) recompose picks up a `TRAINED` flip atomically (documented in AGENTS);
  (3) VisualDNA `consumer_compat` has no `comic` consumer — read-only consumption needs no amendment; the
  ADR-004 extension is Pygmalion's call (offered in the staged Callisto memo); (4) per-panel style-register
  overrides vs comic-level LoRA selection — H6 refine-chain territory.
