---
type: mission
mission_id: mission_hv_visual_fidelity
campaign_id: campaign_canvas_halftone
phase: HV
status: completed
owner: stanley
persona: Mondrian
executor_tier: fable
token_budget_estimated: "1 session (large) — CLI + 4 traps + calibration + tests + doctrine + guidance + memos"
created: 2026-08-03
updated: 2026-08-03
last_edited_by: agent_mondrian
relates: ["coord_2026_08_03_kennedy_to_mondrian_canvas_visual_fidelity.md", "context_canvas_visual_in_the_loop.md (HOME-CV-3)"]
tags: [mission, halftone, hv, visual_fidelity, traps, cli, calibration, doctrine, kennedy]
---

# Mission: HV — the visual-fidelity rail (canvas-visual-check + doctrine adoption)

## Intent

Close gap **G7**: a canvas passed `canvas-std validate` `[OK]` and rendered unreadable (Kennedy/Oration,
2026-08-03) because the geometric traps had no CLI, the reviewer registry didn't know them, and the
agent-confirmed-render doctrine was never adopted. HV wires all three + publishes authoring guidance — entirely on
the production shelf (**`what/code/canvas_std/` untouched; firewall git-diff 0**). Gate: the operator-approved
2026-08-03 plan (`~/.claude/plans/please-read-the-claude-md-glistening-dewdrop.md`) **is** the HV gate.

## Objectives

| # | Objective | Status |
|---|-----------|--------|
| **O1** | New geometry traps (registry + per-trap tests, existing `cv_*_01` convention): `CV-LEAD-COST-01` · `CV-GROUP-LABEL-01` · `CV-EDGE-LABEL-01` (first edge-geometry trap, incl. collision) · `CV-FILE-PROPS-01` (vault_root-kwarg) | ✅ |
| **O2** | Calibration: `text_metrics.py` `OBSIDIAN_*` constants + `measure_obsidian_extent`/`obsidian_required_node_height` (Kennedy's `canvas_fit_check.py` absorbed with credit); `CV-TEXT-BOUNDS-01` overflow now Obsidian-calibrated (`calibration="obsidian"` default, `"legacy"` escape hatch); existing fixtures held — no re-fixturing needed | ✅ |
| **O3** | CLI `canvas_core/traps/cli.py` ("`canvas-visual-check`"): `--json` · `--strict` · `--vault-root` (auto-detect via nearest `.obsidian`) · `--all-traps` (default = visual-fidelity profile, presentation-workflow traps excluded) · fix hints · exit 0/1/2; `python -m` + direct-path self-bootstrap (adds production root + `canvas_std/src`); acceptance fixtures green (320×110+`##` FAILS · `**bold**`+340×200 PASSES) | ✅ |
| **O4** | Doctrine adoption: `skill_canvas_producer_build.md` steps 5/6 + Verification gain visual-check + agent-confirmed render; `spec_federation_contract.md` §4 **Amendment 1** (stages 2/3 + ratification block, operator 2026-08-03); `context_canvas_visual_in_the_loop.md` adoption step 1 marked EXECUTED (→ HOME-CV-3 disposition memo staged) | ✅ |
| **O5** | `canvas_reviewers.yaml` → **1.1.0**: 8 geometric traps under `trap_applicability.structural_now` (4 pre-existing + 4 new); CLI noted in ship_gate | ✅ |
| **O6** | `what/docs/canvas_authoring_guidance.md` — five rules with the measured numbers · three-checks table (schema/fit/sight) · known limitations (renderer file-node blindness; comic print-geometry padding findings expected-and-reviewed; CV-PENDING on prompt_only = correct) | ✅ |

## Verification (run 2026-08-03 — all green)

- `canvas_core` suite **784 passed / 3 skipped** (own `.venv`, reconstituted this mission — see AAR Finding).
- 7-producer sweep **236 passed** (10/16/37/36/100/17/20 — H1 baseline held) · `canvas_std` **115/10** ·
  `certify.py` **11/11** · firewall `git diff --stat -- what/code/canvas_std/` **empty** (porcelain empty too).
- CLI E2E: acceptance fixtures green (320×110+`##` FAILS incl. required-height hint · `**bold**`+340×200 PASSES) ·
  cross-vault direct-path invocation from `$HOME` works (self-bootstrap) · **Oration's reworked map =
  Kennedy-parity clean** — every fit_check fail class reports zero; `content_hidden` mediums correspond to his
  warn class; 2 additional highs are `CV-GROUP-PADDING-01` coverage his stopgap didn't carry (courtesy-flagged in
  the reply memo) · comic example: `CV-PENDING` (prompt_only) + print-geometry padding findings are
  **expected-and-reviewed** (documented in the guidance).

## AAR (SO-5)

- **Worked:** absorbing a contributed, *pre-validated* calibration (Kennedy's constants had been checked against
  operator-observed failures) made the trap build mostly a porting exercise — same-day intake of a cross-vault
  defect report, including doctrine adoption that had idled 40 days.
- **Didn't:** the plan assumed "run the suites" was trivial — in fact **no venv on the node could run the
  canvas_core suite** (post-pt09-P5 gap: producer venvs lack PIL/pyyaml/pytest-timeout; the "236" sweeps never
  included canvas_core's tests). Reconstitution (canvas_core/.venv + editable canvas_std + 5 deps) cost real
  session time. Also: two real-world CLI runs surfaced profile mismatches (CV-DIMENSION-VISIBILITY on every
  hand-authored canvas; GROUP-PADDING on deliberate comic print geometry) that the design hadn't anticipated —
  resolved as the default visual-fidelity profile + documented expected-findings.
- **Finding:** "conformance-green ≠ correct" generalizes to *test-suite-green ≠ suite-runnable-everywhere* — a
  relocated package whose tests ride no venv silently drops out of every sweep. Worth a fleet-level health check.
- **Change:** `canvas-visual-check` defaults to the visual-fidelity profile (deck-workflow traps opt-in via
  `--all-traps`) — a CLI for arbitrary canvases must not inherit producer-pipeline assumptions.
- **Follow-up:** (1) upstream idea candidate — venv-runnability check for relocated code-as-WHAT packages;
  (2) `canvas_core` console-script packaging; (3) Home harness graduation ruling at H2/HR; (4) `html_renderer`
  file-node preview fix; (5) H2 opens with the amended exit criteria.
