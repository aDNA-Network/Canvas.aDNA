---
type: mission
mission_id: mission_h2_render_bridge
campaign_id: campaign_canvas_halftone
phase: H2
status: completed
owner: stanley
persona: Mondrian
executor_tier: fable
token_budget_estimated: "1 session (large) — new package (9 modules + CLI) + tests + E2E fixture + amended-exit verification"
created: 2026-08-03
updated: 2026-08-03
last_edited_by: agent_mondrian
relates: ["halftone_roadmap.md §1", "halftone_gap_register.md G1", "mission_hv_visual_fidelity.md (amended exit)", "halftone_dev_lanes.md (ratified 2026-08-03)"]
tags: [mission, halftone, h2, comic_render, bridge, manifest, fake_backend, writeback, compose, cli, ast_guard]
---

# Mission: H2 — the render bridge, offline (`what/production/comic_render/`)

## Intent

Close the core of gap **G1** offline: the comic pipeline dead-ends at rendering because nothing turns a built
`issue.canvas` into dispatched images and a composited page. H2 builds the bridge as a new production-shelf
package — manifest v0.1 (with `render_chain`) · extract · `backends/{fake}` · dispatch · select ·
write-back-to-NEW-file · validate · compose shim · CLI · AST no-diffusion guard — provable end-to-end with zero
network. Gate: the operator-approved 2026-08-03 plan (`~/.claude/plans/please-read-the-claude-md-warm-rocket.md`)
**is** the H2 gate (HV precedent). Ruled at the same approval: **open decision #5 = derived artifact**
(`issue.rendered.canvas` is a reproducible build output; YAML source + producer stay authoritative).

Boundary: **"Canvas dispatches, it does not diffuse"** — `what/code/canvas_std/` untouched (firewall git-diff 0);
`comic_render` never imports `comic_generator` (file-shaped handoff); PIL only via `canvas_core.print`.

## Objectives

| # | Objective | Status |
|---|-----------|--------|
| **O1** | Package scaffold (producer idiom, mirror `comic_generator`): `pyproject.toml` (`comic-render`, dep `adna-canvas-std` only, console script) · `src/comic_render/` · `tests/` · own `.venv` (editable self + canvas_std) · `AGENTS.md` · `iii_quality_contract.md` · guarded self-bootstrap for `canvas_core` (not pip-packaged) | ✅ |
| **O2** | `manifest.py` — render manifest v0.1: header (`comic_id` · `source_canvas` · `source_sync_hash` · `backend_policy` · `budget_cap`) + per-panel specs (status · prompt_text · `prompt_layers` incl. `negative` · aspect/target_px · characters[] · deterministic seed · `render_chain` = ordered stages, **chain not switch**) · JSON round-trip | ✅ |
| **O3** | `extract.py` — plan stage: `issue.canvas` → manifest (panel nodes via `component_types` class `image` · page groups · `reading_order` chain · staleness guard on `source_sync_hash`) | ✅ |
| **O4** | `backends/` — `base.py` (re-export `ImageClient`; new `RefineClient` Protocol, additive) · `fake.py` (deterministic pure-Python PNG, **no PIL**; `FakeRefineClient` proves the generate→refine chain offline); `gemini`/`comfy` = clean NotImplemented until H3/H4 | ✅ |
| **O5** | `dispatch.py` — chain executor over `render_chain` · `ImagenWiring` path planning (`runs/<comic_id>/<panel>_v{n}.png`) · idempotent (skip existing variants) · `budget_cap` accounting | ✅ |
| **O6** | `select.py` — deterministic offline policy → **Schema-A** `SelectionRecord` (F-36 vault-relative; `dataset_root=runs/<comic_id>/selections/` so fake runs never pollute the corpus) | ✅ |
| **O7** | `writeback.py` — NEW file `issue.rendered.canvas` (input immutable): `text→file` + `degrades_to: file` + `status: rendered` + `render_provenance`; never add/remove nodes/edges; `ANCHOR_REF_KEYS` never used; `_reserved.sync` byte-identical (asserted); idempotent | ✅ |
| **O8** | `validate.py` — stage-6 gate: `validate_suite` aDNA-Native green + D-1/2/3 + every `file` path exists + effective-DPI check + sync_hash equality | ✅ |
| **O9** | `compose.py` — `PrintExporter` shim: canvas nodes → duck-typed placement objects · canvas-absolute→page-local remap (R5) · page JPGs; `cli.py` — `plan|dispatch|refine|select|write-back|validate|compose` + `run --until`; manifest sidecar = resumable state | ✅ |
| **O10** | Tests: per-module + `test_boundary.py` (inverted AST guard: HTTP clients MAY · torch/diffusers/cv2/imageio/direct-PIL NEVER) + offline E2E (plan→…→composited page JPG) + goldens (sync_hash byte-identical · placement 1px · idempotent re-runs) — suite green | ✅ |
| **O11** | Amended exit (HV rail): `canvas-visual-check` on `issue.rendered.canvas` (expected findings only) + **agent-confirmed render** of the composited page (recorded below) · full regression (producers 236 · canvas_core 787/3 · canvas_std 115/10 · firewall 0) | ✅ |

## Verification (run 2026-08-03 — all green)

- **`comic_render` suite 72 passed** (own `.venv`, Python 3.14; `ruff` clean) — per-module + boundary
  AST guard + CLI + two E2Es (default chain · hybrid generate→refine chain).
- Full regression: 7-producer sweep **236** (10/16/37/36/100/17/20, all unaffected) · `canvas_core`
  **787 passed / 3 skipped** (784 baseline + 3 new CV-FILE-PROPS-01 binary-target regression tests) ·
  `canvas_std` **115/10** · `certify.py` **11/11** · **firewall `git diff --stat -- what/code/canvas_std/`
  empty**.
- **E2E proof (CLI, offline)**: `comic-render run --until compose` on the committed mini-issue fixture —
  9 panels → 27 fake variants → 9 Schema-A records → `mini_issue.rendered.canvas` (aDNA-Native green,
  D-1/2/3 green, sync_hash `c56c73c08428f621` byte-identical) → **4 composited 2062×3150 page JPGs**.
  Re-run = zero new work (idempotent); hybrid chain re-run: 27 generate + 27 refine, selections over
  `refined/`, reproducible byte-for-byte across directories (E2E golden).
- **`canvas-visual-check` on the rendered canvas**: runs clean (no runner errors) after the
  CV-FILE-PROPS-01 binary-target fix. Findings = the documented **expected-and-reviewed comic
  print-geometry classes** (padding/density/fill — identical classes on the source canvas, per
  `canvas_authoring_guidance.md`) **minus** the source's CV-HIERARCHY/title findings (text→file flips
  resolved them) **plus 3 medium `CV-IMAGE-ASPECT-RATIO-01` aspect-drift findings** — a REAL new
  signal, recorded below for H3.
- **Agent-confirmed render (adopted doctrine, executed)**: I read the composited page JPGs directly.
  Page 1: the splash fills the full bleed canvas edge-to-edge (true full-bleed placement). Page 2:
  establishing panel top-wide, dialogue + close-up below with a clean gutter, correct bleed margins on
  the dark page ground, empty lower third faithful to the source geometry. Three distinct deterministic
  colors = three distinct prompts flowing the chain. **Confirmed: the composited pages faithfully
  reflect the canvas geometry.**

### Findings for later phases (recorded, non-blocking)

1. **Aspect drift (H3 design note)**: the producer declares `aspect_ratio: "3:4"`/`"16:9"` while
   authoring 663×1025 / 638×326 node geometry (0.647 / 1.957) — a faithful backend honoring the
   declared ratio produces ~10–14% cover-crop at compose. H3 should either request the
   geometry-derived aspect or the producer should emit geometry-consistent ratios. The
   `CV-IMAGE-ASPECT-RATIO-01` trap catches it exactly as designed.
2. **R7 confirmed empirically**: 2K source on a full-bleed page = 199.8 effective DPI → the warning
   fires at validate AND compose (accepted at v0; the refine/upscale chain is the fix path).
3. **CV-FILE-PROPS-01 hardened** (canvas_core): the HV trap assumed markdown targets; the fleet's
   first binary file nodes (this bridge's write-back) crashed its utf-8 read. Now: media targets get
   the existence check only; markdown keeps full embed/Properties semantics (+3 regression tests).

## AAR (SO-5)

- **Worked:** the substrate-reuse doctrine paid out in full — `ImagenWiring` (fan-out + paths),
  Schema-A `rlhf` (records + audit log), `PrintExporter` (compose), and `canvas_std` hashing were
  consumed as-is with zero re-abstraction; the whole 9-module bridge + 72 tests landed in one
  session and the first full-pipeline smoke ran green end-to-end.
- **Didn't:** the amended exit's `canvas-visual-check` immediately crashed a trap — CV-FILE-PROPS-01
  read PNG targets as utf-8 (the HV build had only ever seen markdown file nodes). The visual rail
  gated its own new consumer; fixed in canvas_core with regression tests, but it cost a loop the
  plan hadn't budgeted.
- **Finding:** the first real consumer of a "universal" gate finds the gate's own assumptions —
  HV's trap pack was calibrated on text/deck canvases, and the first image-bearing canvas broke one
  trap and lit a genuinely new signal (aspect drift) the producers had carried silently all along.
- **Change:** the fake backend salts variant colors with the variant FILENAME, not the absolute
  path — byte-reproducibility across working directories became a testable golden instead of a
  hand-wave.
- **Follow-up:** (1) H3: resolve the declared-vs-geometry aspect policy before real spend (finding
  #1); (2) H3: `backends/gemini.py` behind the SPEND gate (registry slot + NotImplemented guard
  already in place); (3) H4: bind `RefineClient` to Vulcan's `comic_panel_refine` (protocol +
  chain executor ready); (4) H6: spread compose (`export_spread` path deferred with a clean
  NotImplementedError); (5) `canvas_comic` disposition unchanged (H6).
