---
type: session
session_id: session_stanley_20260809_211323_halftone_h6_offline
user: stanley
persona: Mondrian
tier: 2
campaign: campaign_canvas_halftone
mission: mission_h6_close
created: 2026-08-09
updated: 2026-08-09
status: completed
last_edited_by: agent_mondrian
tags: [session, halftone, h6, print, spread, cmyk, dpi, rlhf_seam, dispatch_contract, authoring_contract, visual_check_profile, canvas_comic]
---

# Session: Halftone H6 — the offline pass

## Intent

Open **H6** and execute everything in it that needs neither real pixels nor the campaign close.
Plan approval 2026-08-09 = the H6 gate (HV/H2/H4/H5 precedent). H6 ends this pass **partial** —
Halftone cannot close while H3 is open.

The trigger: three unconsumed Callisto memos were sitting untracked in `who/coordination/`, and the
2026-08-07 one **discharges the Bearly P5 evidence dependency** that HR's dispatch contract and H6's
RLHF seam doc were explicitly parked behind. The parked work is now buildable.

## Operator rulings at plan approval

| Decision | Ruling |
|---|---|
| Lane | **H6-offline pass**; H3 + campaign close stay with Luke's lane |
| Print scope | **Include print E2E** — spread compose · `export_spread` wiring · deterministic CMYK · DPI policy |
| Open decision **#3** (`canvas_comic`) | **Reader-only freeze now**; archive after H3; port `ComicReport` only if the scoring loop revives |
| Open decision **#4** (RLHF routing) | **Both sinks with a named boundary** — Canvas owns capture substrate, III owns signal schema; ISS-vs-III resolves for III on signal |

## Scope declaration (Tier 2 — shared-config edits)

**Writes into (single-writer):**
- `what/specs/spec_rlhf_seam.md` (NEW) · `what/specs/spec_canvas_review_surface.md` (§6 amendment) · `what/specs/AGENTS.md`
- `what/docs/comic_authoring_contract.md` (NEW) · `what/docs/canvas_authoring_guidance.md`
- `what/decisions/` — `canvas_comic` disposition record (NEW)
- `what/production/canvas_core/traps/cli.py` · `canvas_core/print.py` · `canvas_core/tests/{test_visual_check_cli,test_print}.py`
- `what/production/comic_render/src/comic_render/compose.py` · `tests/test_compose.py` · `tests/fixtures/mini_issue.canvas`
- `how/federation/federation_index.md`
- `how/campaigns/campaign_canvas_halftone/` — `missions/mission_h6_close.md` (NEW) · master · CLAUDE.md · `missions/artifacts/halftone_dev_lanes.md`
- `who/coordination/` — three inbound memos filed; one reply memo **staged**
- `STATE.md` · this file

**Conflict scan:** `how/sessions/active/` held only `.gitkeep` at session open (peer-verified by
Callisto at their s031). Origin at parity `feda532`, working tree clean but for the three untracked memos.

## Out of scope (recorded, not silently dropped)

- **H3** — no `backends/gemini.py`, no geometry-aspect implementation, no live dispatch, **no spend**.
  Held for Luke's lane. *Flagged:* `GEMINI_API_KEY` is present on this node (Keychain + env, name only) —
  the phase is held by **ruling**, not blocked by credential.
- **Campaign close / final AAR** — impossible while H3 is open.
- Real-pixel evidence: DPI-on-real-renders · `CV-COMIC-STYLE-01` calibration · the HR pilot's second consumer.
- **The operator's HR review pass** — re-verified this session: all six sidecar verdicts still `null`.
- Any code move for `canvas_comic` (record only, per the ruling).
- D3 Rosetta registrar ack (standing, non-blocking).

## Firewall

`what/code/canvas_std/` — zero touches; `git diff --stat` empty at the gate. AST no-diffusion guard
stays green; PIL reached only via `canvas_core.print`. Cross-vault writes: none (Rule 10).

## Objectives

| # | Objective | Status |
|---|-----------|--------|
| O1 | Intake — consume/file the three Callisto memos; stage the reply | ✅ |
| O2 | RLHF seam spec (Lodestar R4.2 · G6) | ✅ |
| O3 | `review_dispatch_contract v0` — stub → real contract | ✅ |
| O4 | Comic-domain visual-check profile (H4 finding #4) | ✅ |
| O5 | Print E2E — spread compose · CMYK policy · DPI policy | ✅ |
| O6 | Comic authoring contract (T3′) | ✅ |
| O7 | Governance close-out (partial H6) | ✅ |

## Files touched

**Created (7)** — `what/specs/spec_rlhf_seam.md` · `what/docs/comic_authoring_contract.md` ·
`what/decisions/adr_009_canvas_comic_disposition.md` ·
`how/campaigns/campaign_canvas_halftone/missions/mission_h6_close.md` ·
`who/coordination/coord_2026_08_09_mondrian_to_callisto_dispatch_contract_bound.md` (**staged**) · this file ·
(+ the three inbound memos first tracked at `e27755d`).

**Modified (22)** — `what/production/canvas_core/{print.py,traps/cli.py,rlhf/iii_bridge.py,rlhf/review_collect.py}` ·
`canvas_core/tests/{test_print.py,test_visual_check_cli.py}` ·
`comic_render/src/comic_render/{compose.py,cli.py}` · `comic_render/tests/test_compose.py` ·
`canvas_comic/tests/test_comic_builder.py` (one line) ·
`what/specs/{spec_canvas_review_surface.md,spec_interface_surface.md,AGENTS.md}` ·
`what/docs/{canvas_authoring_guidance.md,AGENTS.md}` · `how/federation/federation_index.md` ·
`how/campaigns/campaign_canvas_halftone/{campaign_canvas_halftone.md,CLAUDE.md,missions/artifacts/halftone_roadmap.md}` ·
`who/coordination/` ×3 (disposition blocks) · `STATE.md`.

**Commits (6)**: `e27755d` (memos as-delivered) → `c545203` (O1–O3) → `60bb3de` (O4) → `72d931c` (O5) →
`1d3f015` (O6) → `0e7065c` (O7). 29 files, +1833/−148. **Not pushed** — origin stays `feda532` (push is an
operator-gated batch).

## SITREP

**Completed** — the full H6 offline half, all seven objectives. Four defects found and fixed, all of one
family: **code that was written, looked correct, and had never executed the path it claimed.**
`export_spread` unreachable (spreads would have squashed 2:1, silently) · CMYK's `except: pass` soft-convert
making output machine-dependent · `RLHF_SIGNAL_TYPE_REJECT` declared and never emitted (reject-only passes
produced no signal at all) · the visual-check gate failing every conformant comic page. Plus two stale-claim
corrections (an `iii_bridge` docstring; the dev-lane pointer).

**In progress** — none. Every objective closed.

**Next up** — **H3 is now the only phase between Halftone and its close.** One live
`--chain "generate:gemini,refine:comfy@0.4/comic_panel_refine"` run closes H3 *and* H4's remainder. Then H6
re-opens for the campaign AAR + close with real-pixel evidence.

**Blockers** — none technical. Awaiting the operator: three §7.7 ratifications (`spec_rlhf_seam` — its
implementation S-1..S-4 is deliberately held until signature · the dispatch-contract §6 amendment · `adr_009`)
· the Callisto memo GO · the push GO · the HR review pass (six verdicts still `null`) · **the H3 gate call**.

**Correction worth carrying** — the approved plan said the dev-lane annex still read "draft pending
ratification". It didn't: the artifact had carried `status: ratified` since 2026-08-03; the campaign CLAUDE.md
*pointer* was stale. Reading a pointer instead of the artifact put a wrong claim into an approved plan.

**Verification** — canvas_core **841/3** · comic_render **94/1** · canvas_comic **99** (+11 subtests) ·
producers **259** · `canvas_std` **115/10** · certification **11/11** · **firewall diff 0** (`canvas_std` AND
`canvas_context`, measured across the whole session) · AST no-diffusion guard green · ruff clean on every
changed file · E2E `sync_hash c56c73c08428f621` **byte-identical** → 4 composited pages · `--cmyk` a real ICC
separation (mode CMYK, 2062×3150, 300dpi) · **both the spread split and the four pages confirmed by looking**.

**The doctrine, third phase running** — the spread split passed *every* assertion on two flat green
rectangles before a structured source revealed whether it was correct at all. A solid colour splits
identically however you cut it. Assertions cannot see.

## Next Session Prompt

> Canvas.aDNA (Mondrian), Operation Halftone. **H6's offline half is done** (`mission_h6_close`,
> `status: partial`, 2026-08-09) — RLHF seam spec, dispatch contract v0 bound, comic visual-check profile,
> print E2E (spread compose · deterministic CMYK · DPI policy), authoring contract, `adr_009`. **H3 is the
> only phase left before the campaign close**: build `comic_render/backends/gemini.py` + implement the
> geometry-derived aspect ruling in `extract.py`, then one live
> `--chain "generate:gemini,refine:comfy@0.4/comic_panel_refine"` run → operator eye-gate → the fleet's first
> real composited page (this also closes H4's remainder). H3 is **SPEND-gated** ($5 cap · Gemini pro-image ·
> 3 variants/panel, all pre-ruled 2026-08-04) and was **held for Luke's cloud lane** — but `GEMINI_API_KEY` is
> present on this node, so confirm with the operator whose lane it is before starting. Three specs await §7.7
> signature (`spec_rlhf_seam` gates its own S-1..S-4 implementation). One memo is staged for a per-send GO.
> Origin is `feda532`; six local commits await an operator-gated batch push. Read `STATE.md` →
> `how/campaigns/campaign_canvas_halftone/` → `missions/mission_h6_close.md`. HOLD at every gate (SO-1).
