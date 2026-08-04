---
type: mission
mission_id: mission_hr_review_surface
campaign_id: campaign_canvas_halftone
phase: HR
status: built_gate_pending
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
| **O1** | `what/specs/spec_canvas_review_surface.md` (draft): normative control↔affordance table (verdict→`choice[approve/reject/skip]` · rating→`choice["1".."5"]` single-axis v1.0 · defect_tags→`choice`(10-term Bearly vocab, one response per tag) · note→`annotation` · prompt_edit→`input` · regenerate/pin/escalate→`action` intent flags) · sidecar frontmatter schema (+ collector ledger keys) · verbatim JS-less Meta Bind snippets · three-sink collector contract + idempotency + participant attribution · **§ `review_dispatch_contract v0` NAMED STUB** · H6 forward-pointer (open decision #4) · +1 row `what/specs/AGENTS.md` | ✅ |
| **O2** | `iii_bridge.py`: `DEFAULT_LEARNING_STORE` filename → `canvas_iii_learning_store.jsonl` (live store) + stale docstring paths; **`DEFAULT_CORPUS_DIR` untouched** (test-coupled); regression test | ✅ |
| **O3** | `canvas_core/rlhf/review_canvas.py` (builder + `_main`): consumes `variations.manifest.json` → `what/artifacts/review_surface_pilot/{ss_variant_review.canvas, sidecars/var_1..6.md, README.md}`; trap-derived int geometry (exact-aspect image nodes; `**bold**` leads, no `#`; labels in budget); 8×6 namespaced affordances anchored on sidecar node ids; self-check `validate(doc, ADNA_NATIVE) == []`; refuses to overwrite verdict-bearing sidecars | ✅ |
| **O4** | Pilot generated + `.obsidian/app.json` `propertiesInDocument: "hidden"` (operator-consented in-plan) + `canvas-std validate` green + `canvas-visual-check` clean (or expected-only, documented) | ✅ |
| **O5** | `canvas_core/rlhf/review_collect.py`: guarded bootstrap → `canvas_context.interaction.apply_response` (collector owns doc write-back) · `verdict == approve` → Schema-A record per approved variant (all 6 as variants[], F-36 vault-relative, deterministic `selection_id`) → **real corpus** `what/artifacts/image_gen_dataset/` · III `accumulate` to the live store · reject-only → responses only (bridge charter is accept-only; reject→III = H6 decision #4) · 4-layer idempotency · `--dry-run`/`--force`/`--turn` | ✅ |
| **O6** | Tests: `test_review_canvas.py` + `test_review_collect.py` (tmp vault fixture w/ hidden-properties app.json; idempotent + ledger-loss replays; dry-run byte-identical; F-36 + I-3 green post-write; reject-only path; `{kind: ai}` participants only — never forged as human) | ✅ |
| **O7** | Live proof: `{kind: ai}` plumbing pass on a tmp copy ✅ · full canvas_core suite + firewall 0 ✅ · **spec RATIFIED 2026-08-04** (GO-wave plan approval = the §7.7 signature) ✅ · remaining at the gate: **agent-confirmed Obsidian render** (link handed to the operator at the GO wave) + the operator's real review pass (at leisure; collector idempotent) | 🟡 gate (1 of 3 items closed) |

## Verification (build side, run 2026-08-04 — all green)

- **`canvas_core` 800 passed / 3 skipped** (787 baseline + 13 new; `ruff` clean; `test_iii_bridge` unaffected
  by the store-default repoint — regression test added).
- **The pilot is REAL and gate-ready**: `what/artifacts/review_surface_pilot/` — `ss_variant_review.canvas`
  (6 variants, 48 affordances, `adna_native` **[OK]** with D-1/2/3 green) + 6 Meta Bind sidecars + README.
  `canvas-visual-check`: **0 findings** — the first draft fired 10 medium findings (CV-GROUP-PADDING-01
  width-fill 94% + CV-IMAGE-ASPECT-RATIO-01 slot-underfill 17%); the geometry was reworked to clear the
  measured gates (content span 88.9% < 90%; fit-box images ≥ 20% slot area at exact ratios) — **the HV rail
  gated its own second consumer, again**.
- **CLI plumbing E2E (scratchpad copy, `{kind: ai}`)**: dry-run byte-identical + correct would-write report →
  real run fans one simulated verdict into all three sinks (3 responses w/ `ai` attribution · 1 Schema-A
  record + audit line · 1 III line) → **replay = complete no-op** (0/0/0; `skipped: 6`); `state.open`
  correctly drops the answered verdict. Idempotency layers proven in tests incl. **ledger-loss replay**
  (canvas `at` = fallback clock → same deterministic `selection_id`).
- `.obsidian/app.json` `propertiesInDocument: "hidden"` set (operator-consented in-plan); Meta Bind 1.4.10
  `enableJs: false` preserved (no JS anywhere in the surface).
- **Firewall: `what/code/canvas_std/` diff 0 · `what/code/canvas_context/` diff 0** (import-only via the
  guarded bootstrap).

## AAR (SO-5)

- **Worked:** the assembled-from-existing-layers thesis held — `apply_response`, Schema-A, `iii_bridge`,
  `CanvasBuilder`, and the trap pack were consumed unmodified; the only genuinely new logic is the fan-out +
  layered idempotency, and the whole surface landed with 13 tests in one slice.
- **Didn't:** my "trap-derived" first-draft geometry failed its own gate — 10 medium findings on generation
  (group width-fill 94%, 1:1 slot-underfill 17%); and the `min(iw, 640)` width cap was a latent
  exact-aspect breaker the fit-box rule replaced.
- **Finding:** the visual rail keeps proving itself on its own builders — HV's traps corrected H2's
  consumer (binary targets) and now HR's (slot/padding budgets); "trap-derived by intention" ≠ "trap-clean by
  measurement" — generate, check, rework is the loop.
- **Change:** selection stamps fall back to the canvas's earliest verdict-response `at` when the sidecar
  ledger is lost — the canvas itself became the durable clock, making the deterministic `selection_id`
  survive every idempotency-layer failure mode we could construct.
- **Follow-up:** (1) at the gate: spec ratification + agent-confirmed Obsidian render (buttons-vs-toggles
  resolved there) + the operator's first real pass; (2) H6: the RLHF seam doc anchors on this spec + Bearly
  P5 evidence (open decision #4: reject→III routing); (3) re-run the surface on the first H3 renders (the
  second consumer, roadmap decision #6); (4) Meta Bind input/button templates could graduate into
  `.obsidian` config once the pilot pattern settles.
