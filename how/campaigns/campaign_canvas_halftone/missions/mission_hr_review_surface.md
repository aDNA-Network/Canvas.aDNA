---
type: mission
mission_id: mission_hr_review_surface
campaign_id: campaign_canvas_halftone
phase: HR
status: active
owner: stanley
persona: Mondrian
executor_tier: fable
token_budget_estimated: "1 session slice (shared with H5/HF) — 1 spec + 2 new canvas_core modules + pilot artifacts + tests + 1-key app.json"
created: 2026-08-04
updated: 2026-08-04
last_edited_by: agent_mondrian
relates: ["halftone_roadmap.md §6", "halftone_gap_register.md G9", "what/specs/spec_interface_surface.md", "Bearly.aDNA/what/specs/spec_bearly_rlhf_canvas.md (read-only precedent)", "coord_2026_07_28_callisto_to_mondrian_lorales_compose_and_dispatch_seam.md §2 (the dispatch seam)"]
tags: [mission, halftone, hr, rlhf, review_surface, metabind, interaction, schema_a, iii_bridge]
---

# Mission: HR — the RLHF review surface (spec + pilot + collector)

## Intent

Close gap **G9** (every layer exists — interaction runtime v1.0 · Schema-A + iii_bridge · Meta Bind fleet-wide ·
Bearly dry-run precedent — but no assembled operator surface). Gate: the 2026-08-04 plan approval. Deliver:
(1) canonical **`spec_canvas_review_surface.md`** (Meta Bind ↔ affordance kinds; `status: draft`, ratification at
the HR gate); (2) a **working pilot** review canvas over real images; (3) a **collector** fanning one sidecar
frontmatter verdict into three sinks (`interaction.responses` append · Schema-A `SelectionRecord` · III JSONL).
**Dispatch-side = NAMED CONTRACT STUB only** (the Callisto seam; awaits Bearly P5 evidence). `enableJs: false`
preserved throughout.

**Premise correction (roadmap §6 said "ComfyUI SS variants"):** ComfyUI.aDNA holds no SS variant images (3 banner
files total). The real, reviewable variant set is **in-vault**:
`what/artifacts/style_registry/ss_character/canonical/variations/` (6 `anchor_var_*.png` + a manifest with real
prompts, `model: imagen-4.0-ultra-generate-001`, vault-relative paths — F-36-clean). Pilot runs on it; the first
H3 renders become the second consumer.

Doc-shape anchor (verified): `_reserved` lives at `metadata.frontmatter._reserved` for builder, validator, and
`apply_response` alike. Pilot canvas declares `adna_native` (`adna_version` + nested `sync.sync_hash`) so
`canvas-std validate` exercises I-1/I-2/I-3.

## Objectives

| # | Objective | Status |
|---|-----------|--------|
| **O1** | `what/specs/spec_canvas_review_surface.md` (draft): normative control↔affordance table (verdict→`choice[approve/reject/skip]` · rating→`choice["1".."5"]` single-axis v1.0 · defect_tags→`choice`(10-term Bearly vocab, one response per tag) · note→`annotation` · prompt_edit→`input` · regenerate/pin/escalate→`action` intent flags) · sidecar frontmatter schema (+ collector ledger keys) · verbatim JS-less Meta Bind snippets · three-sink collector contract + idempotency + participant attribution · **§ `review_dispatch_contract v0` NAMED STUB** · H6 forward-pointer (open decision #4) · +1 row `what/specs/AGENTS.md` | ⬜ |
| **O2** | `iii_bridge.py`: `DEFAULT_LEARNING_STORE` filename → `canvas_iii_learning_store.jsonl` (live store) + stale docstring paths; **`DEFAULT_CORPUS_DIR` untouched** (test-coupled); regression test | ⬜ |
| **O3** | `canvas_core/rlhf/review_canvas.py` (builder + `_main`): consumes `variations.manifest.json` → `what/artifacts/review_surface_pilot/{ss_variant_review.canvas, sidecars/var_1..6.md, README.md}`; trap-derived int geometry (exact-aspect image nodes; `**bold**` leads, no `#`; labels in budget); 8×6 namespaced affordances anchored on sidecar node ids; self-check `validate(doc, ADNA_NATIVE) == []`; refuses to overwrite verdict-bearing sidecars | ⬜ |
| **O4** | Pilot generated + `.obsidian/app.json` `propertiesInDocument: "hidden"` (operator-consented in-plan) + `canvas-std validate` green + `canvas-visual-check` clean (or expected-only, documented) | ⬜ |
| **O5** | `canvas_core/rlhf/review_collect.py`: guarded bootstrap → `canvas_context.interaction.apply_response` (collector owns doc write-back) · `verdict == approve` → Schema-A record per approved variant (all 6 as variants[], F-36 vault-relative, deterministic `selection_id`) → **real corpus** `what/artifacts/image_gen_dataset/` · III `accumulate` to the live store · reject-only → responses only (bridge charter is accept-only; reject→III = H6 decision #4) · 4-layer idempotency · `--dry-run`/`--force`/`--turn` | ⬜ |
| **O6** | Tests: `test_review_canvas.py` + `test_review_collect.py` (tmp vault fixture w/ hidden-properties app.json; idempotent + ledger-loss replays; dry-run byte-identical; F-36 + I-3 green post-write; reject-only path; `{kind: ai}` participants only — never forged as human) | ⬜ |
| **O7** | Live proof: `{kind: ai}` plumbing pass on a tmp copy → **agent-confirmed Obsidian render with the operator** (html_renderer is file-node-blind by design; buttons-vs-toggles fallback resolved here) → operator invited to a real review pass (records land beside the existing 13) · full canvas_core suite + firewall 0 | ⬜ |

## Verification

*(filled at mission close with actual run results)*

## AAR (SO-5)

*(5-line AAR at mission close — SO-5)*
