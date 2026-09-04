---
type: session
session_id: session_stanley_20260904_blueprint_p2_open_and_the_licensing_act
created: 2026-09-04
updated: 2026-09-04
status: completed
tier: 2
persona: mondrian
operator: stanley
campaign: campaign_canvas_blueprint
phase: P2
executor_tier: opus
last_edited_by: agent_mondrian
tags: [session, canvas, blueprint, p2, authoring_rail, dogfood, licensing, adr_024, publication_boundary, adr_016, memo_intake]
---

# Session — Blueprint P2 open · three inbound memos · the licensing act

## Intent

Cold-start orientation found three converging items, only one of which `STATE.md` predicted:

1. **Three untracked inbound memos** in `who/coordination/`, never intaken — one with
   `ack_required: true`.
2. **Canvas has been publicly distributed under all-rights-reserved since 2026-06-22.** No
   `LICENSE`/`COPYING` at root; the forge reports `license=NULL`. Sharper here than anywhere else
   in the fleet: *a standard published all-rights-reserved is a standard nobody is permitted to
   implement from.*
3. **Blueprint P2 at HOLD**, with a real dogfood gap — the vault ships **zero** dual-channel context
   canvases of its own.

## Operator rulings (plan gate, 2026-09-04)

| Item | Ruling |
|---|---|
| License | **MIT, network default** (ADR-024) — copy the verified Exchange bytes, do not compose |
| P2 scope | **Rail + dogfood**; conversion memos #10/#11 deferred to a second P2 session |
| Push | **GO** — single operator-gated batch |
| Drop-box | **Adopt** — `who/coordination/inbox/` |

## Scope declaration (Tier 2)

Writes: `LICENSE` (new) · `who/coordination/` (memo intake + inbox + 1 reply + 1 ruling record) ·
`how/federation/comfyui/CLAUDE.md` (redaction of our own authored literal) ·
`how/skills/skill_canvas_context_diagram.md` (new) · `what/production/diagram_generator/`
(additive passthrough + test) · two new `.canvas` + spec YAMLs beside their prose ·
`how/campaigns/campaign_canvas_blueprint/` (mission + phase status) · `STATE.md`.

**Firewall:** `what/code/canvas_std/` is NOT in scope — `git diff --stat` there must be 0 at close.

**Conflict scan:** `how/sessions/active/` held only `.gitkeep` at session start — no peer lease.
Working tree carried 3 untracked inbound memos (this session's A1) and no agent-dirty files.

## Measurements taken (recorded at the instrument, not remembered)

**Pre-push forge reading, 2026-09-04T16:07Z** — `gh api orgs/aDNA-Network/repos?type=public`:

```
aDNA               MIT
adna-legacy        MIT
aDNA.aDNA          MIT
Canvas.aDNA        NULL      <-- us
community-policies NULL
Git.aDNA           MIT
III.aDNA           NULL
spacemacs          GPL-3.0
world-genome       NULL
```
**Unlicensed count: 4.** Canvas is in the numerator.

⚠ Vantage note, recorded because it disagrees with an inbound memo: Hopper's 2026-08-24 memo §6
cites *"a forge-side enumeration found **20** public repos at `aDNA-Network`"*. This reading returns
**9**. Not reconciled here and not ours to reconcile — recorded so the post-push delta is measured
against a stated baseline rather than an assumed one.

## Log

**A · Intake, licensing, boundary**
1. Three inbound memos committed **byte-unchanged** (Hopper 08-24 licensing · Ilmarinen 08-26 address · Hopper 08-27 address, `ack_required: true`).
2. `LICENSE` installed at root — bytes copied from `Exchange.aDNA/LICENSE`, `md5 b189a96420df57c630764b57ba7ff2f4` verified **at both ends**. Never composed.
3. **F-P2-1** found: `canvas_std/LICENSE` + `canvas_context/LICENSE` tracked, public, byte-identical MIT since **2026-06-13 — nine days before the flip**. Only the root was bare, so the *reference implementation* was licensed and the *spec documents* were not.
4. `adr_012` authored (`proposed`) after an inside census **confirmed the peers' 2 occurrences exactly** and found a **second literal at 8 occurrences over 7 files** (**F-P2-2**). Authored content redacted in 3 files; records untouched.
5. Reply to Hopper delivered into their drop-box (`md5 7749e196abe895ef12cbb31eb58c9edd`). Ilmarinen owed nothing — no reply manufactured.
6. Drop-box adopted; the `-uall` collapse trap **run in this tree** before the README claimed it, then the README's example transcript corrected to the real output.

**B · Blueprint P2 (`mission_b2_authoring_rail`)**
7. `diagram_generator`: optional `authority` + `prose` passthrough, with the enum check that is **currently the only enforcement anywhere** (F-B1-2). 8 new tests.
8. Two dogfood canvases authored beside their prose. `canvas-std` caught a real defect first (prose `context_version: "1.1"` is not semver; A-7 rejects it → mapping rule `X.Y → X.Y.0` now in the rail).
9. **Visual gate FAILED** — and the generator's *own example* failed the same traps, since Atelier, at **~14% shown**. **F-P2-3**: `CV-HIERARCHY-01` and `CV-LEAD-COST-01` are mutually unsatisfiable; `####` is the only honest pass. **F-P2-4**: a fixed pad cannot satisfy a ratio threshold.
10. Generator repaired (title slot · content-sized code node · ratio-scaled group padding · title/rank overlap). All three canvases now `--strict` clean.
11. Rail authored: `how/skills/skill_canvas_context_diagram.md`. Erratum **E2** appended to the draft + memo authored; **delivery REFUSED** (aDNA.aDNA live lease, no drop-box).

**Amendment-1 render — attempted, abandoned, disclosed**
12. My plan said the render was at risk because "no Obsidian vault was found". **That was a bad probe** — I checked `~/Obsidian*`; the vault is this repo, and Obsidian was installed and working. Two capture attempts followed; the second recorded a third party's private Discord messages, because `screencapture` on a desktop app takes the whole screen. **Stopped, deleted both captures, restored the operator's Obsidian window to its original bounds (634,33 862×511).** Canvases ship `visual_gate: pending`.

## Gates at close

| Gate | Result |
|---|---|
| `canvas_std` | **115 passed / 10 skipped** (baseline held) |
| `diagram_generator` | **44** (36 baseline + 8 new) |
| Cross-producer sweep | **267** (10·16·37·44·123·17·20) |
| Firewall `git diff --stat -- what/code/canvas_std/` | **0** |
| Both dogfood canvases | `adna_native [OK]` · `canvas-visual-check --strict` **0 findings [OK]** |
| `ruff` (diagram_generator) | clean |
| Amendment-1 render | ⛔ **NOT met** — `visual_gate: pending`, see log 12 |

## SITREP

**Completed** — memo intake ×3 + one reply delivered · MIT `LICENSE` at root (byte-verified) · `adr_012` authored + 3-file redaction · drop-box adopted · Blueprint **P2 rail + dogfood shipped** · `diagram_generator` visual-gate repair · erratum E2 authored.

**In progress / handoff** — E2 undelivered (retry when aDNA.aDNA's lease clears) · dogfood `visual_gate: pending`.

**Next up** — operator picks **P2b** (conversion memos #10/#11, now backed by a used rail) or **P3** (federation re-pin wave).

**Blockers** — none blocking. Two operator signatures pending (`adr_010`, `adr_011`, and now `adr_012` §7.7). `#needs-human`: a **window-scoped screenshot path** is required before any canvas can clear Amendment 1 on a shared workstation.

**Files touched** — `LICENSE` (new) · `STATE.md` · `CLAUDE.md` (skills table) · `what/decisions/adr_012_*.md` (new) · `what/decisions/adr_004_*.{diagram.yaml,canvas}` (new) · `what/context/context_canvas_surface_legs.{diagram.yaml,canvas}` (new) · `how/skills/skill_canvas_context_diagram.md` (new) · `who/coordination/` (3 intaken + 2 authored + `inbox/README.md`) · `how/campaigns/campaign_canvas_blueprint/` (mission + master + draft E2) · `what/production/diagram_generator/` (model · consume · layout · +1 test file · example rebuilt) · `how/federation/comfyui/CLAUDE.md` · `what/production/canvas_core/comfyforge_adapter.py` · `what/production/comic_render/tests/test_backends_comfy.py`.

## Next Session Prompt

Canvas.aDNA is at **Operation Blueprint P2 ✅ complete-with-open-item**; P0/P1/P2 all closed, next gate is the operator's choice of **P2b** (the deferred conversion-offer memos #10 → Operations' 5 standard-blind C08 canvases and #11 → ScienceStanley's 29 bare files — now much stronger because `how/skills/skill_canvas_context_diagram.md` exists and has been used twice, so the offers can carry worked conversions) or **P3** (the federation re-pin wave, `mission_b3`: VisualDNA lockstep-flip mechanics, the `canvasforge/`→`canvas/` rename with Seshat, 5 stale + 3 misnamed wrappers — and **verify the "unanswered" 2026-08-04 memos at source first**, since this session found a live delivery refusal of our own). Four things are carried and must not be dropped: **(1)** the two dogfood canvases (`what/context/context_canvas_surface_legs.canvas`, `what/decisions/adr_004_production_code_layout.canvas`) are `visual_gate: pending` — Amendment 1 needs a **window-scoped** capture ported from `Home.aDNA`'s `canvas_visual_loop.py`, because whole-screen `screencapture` captured a third party's private messages and is ruled out; **(2)** the other six producers' shipped examples have never been re-gated against the grown trap corpus — `deck_generator` alone carries 19 findings incl. 2 HIGH, and only `diagram_generator` was repaired; **(3)** erratum **E2** to Rosetta is authored and staged at `who/coordination/coord_2026_09_04_mondrian_to_rosetta_erratum_e2_*.md` but was **refused at their door** (live lease, no drop-box) — retry when it clears; **(4)** F-HR-1 normalize-on-collect is still untouched. Read `STATE.md` first, then `how/campaigns/campaign_canvas_blueprint/missions/mission_b2_authoring_rail.md` for findings F-P2-1..4 and the AAR. Three ADRs await the operator's §7.7 signature: `adr_010`, `adr_011`, `adr_012`. Phase gates are human gates — HOLD.
