---
type: mission
mission_id: mission_h6_close
campaign_id: campaign_canvas_halftone
phase: H6
title: "H6 — authoring contract · print E2E · governance close (offline pass)"
owner: stanley
persona: Mondrian
status: partial
executor_tier: opus
token_budget_estimated: ~180k
created: 2026-08-09
updated: 2026-08-09
last_edited_by: agent_mondrian
session: session_stanley_20260809_211323_halftone_h6_offline
gate: "plan approval 2026-08-09 = the H6 gate (HV/H2/H4/H5 precedent)"
relates: ["halftone_roadmap.md §4 #3 #4", "halftone_gap_register.md G6", "spec_canvas_review_surface.md §6", "lodestar_recommendations.md R4.2"]
tags: [mission, halftone, h6, print, spread, cmyk, dpi, rlhf_seam, dispatch_contract, authoring_contract, visual_check_profile, canvas_comic]
---

# Mission H6 — the close phase, offline half

## Status: PARTIAL — and that is the design, not a shortfall

H6 is the campaign's close phase. It cannot close the campaign, because **H3 has never run** — no comic page has
been rendered from real pixels, which was Halftone's stated proof milestone. What H6 *can* do without real
pixels is everything else, and this mission did that.

**Left open, explicitly:** the campaign AAR and close · real-pixel DPI evidence · `CV-COMIC-STYLE-01`
calibration · the RLHF pilot's second consumer (H3 renders) · the operator's HR review pass.

## Gate + rulings (operator, at plan approval 2026-08-09)

| Decision | Ruling |
|---|---|
| Lane | H6-offline pass; **H3 and the campaign close stay with Luke's cloud lane** |
| Print scope | **include** print E2E (spread compose · `export_spread` wiring · deterministic CMYK · DPI policy) |
| Open decision **#3** (`canvas_comic`) | **reader-only freeze now**, archive after H3 → `adr_009` |
| Open decision **#4** (RLHF routing) | **both sinks, named boundary**; III for signal → `spec_rlhf_seam` §4 |

## Objectives

| # | Objective | Result |
|---|-----------|--------|
| **O1** | Intake — consume/file three unconsumed Callisto memos; stage the reply | ✅ |
| **O2** | RLHF seam spec (Lodestar R4.2 · G6) | ✅ `what/specs/spec_rlhf_seam.md`, `proposed` |
| **O3** | `review_dispatch_contract v0` — stub → real contract | ✅ six clauses D1–D6, amendment `proposed` |
| **O4** | Comic-domain visual-check profile (H4 finding #4) | ✅ `--profile`; 24 → 0 source, 21 → 3 rendered |
| **O5** | Print E2E — spread compose · CMYK policy · DPI policy | ✅ three defects fixed |
| **O6** | Comic authoring contract (T3′) | ✅ `what/docs/comic_authoring_contract.md` |
| **O7** | Governance close-out | ✅ `adr_009` · records · this mission |

## What was actually found

The pass turned up **four defects of one family** — code that was written, looked correct, and had never
executed the path it claimed:

1. **`export_spread` was unreachable.** A correct two-page-spread exporter had sat in `canvas_core/print.py`
   since the CanvasForge lineage; `export_all` only ever called `export_page`, so nothing could reach it. Every
   spread would have exported as two independent pages, each fitting the whole 4124px spread into one 2062px
   page — **silently squashed 2:1**, with nothing in the output saying so.
2. **CMYK was machine-dependent.** `_convert_to_cmyk` fell through a bare `except: pass` to Pillow's soft
   `convert("CMYK")`. Same canvas, different bytes depending on whether the host had ColorSync profiles, and
   nothing in the result, the report or the logs said which you got. **This node has the profiles**, which is
   exactly why it stayed invisible.
3. **`RLHF_SIGNAL_TYPE_REJECT` was declared and never emitted.** Combined with Schema-A structurally requiring a
   pick, a reject-only review pass produced no Schema-A record and **no III signal at all** — and "none of these
   six is acceptable" is a stronger preference signal than "this one is best".
4. **The visual-check gate always failed on comics.** All 24 source findings came from exactly three traps, all
   knowledge-canvas *aesthetics*, none a defect. A gate that always fails is not a gate.

Plus two stale-claim corrections: the `iii_bridge` docstring cited 4 store entries (the live store holds a
`_meta` line + 2 pattern entries and zero RLHF signals), and the campaign CLAUDE.md called the dev-lane annex
"draft pending ratification" when the artifact had carried `status: ratified` since 2026-08-03.

## Verification

| Check | Result |
|---|---|
| `canvas_core` | 824/3 → **841 passed / 3 skipped** (+17) |
| `comic_render` | 92/1 → **94 passed / 1 skipped** (deferred test **inverted**, not deleted) |
| `canvas_comic` | **99** + 11 subtests (unchanged) |
| 7-producer sweep | **259** (unchanged — untouched) |
| `canvas_std` | **115 / 10 skipped** · certification **11/11** |
| **Firewall** | `git diff --stat` on `canvas_std` **and** `canvas_context` = **0** |
| `ruff` | clean on every changed file (12 pre-existing findings in the frozen `canvas_comic` tests left per `adr_009`) |
| Offline E2E | `sync_hash c56c73c08428f621` **byte-identical** → 4 composited pages; `--cmyk` verified as a real ICC separation (mode CMYK, 2062×3150, 300dpi) |
| Visual check | `--profile comic`: source 24 → **0**; rendered 21 → **3**, and all 3 survivors are `CV-IMAGE-ASPECT-RATIO-01` — the trap that caught the real H2 drift |

## The doctrine earned its keep a third time

The first spread render **passed every assertion** — two 2062×3150 halves, `is_spread_half=True`, page count
correct — on **two flat green rectangles**. The fake backend emits solid colour, and a solid colour splits
identically however you cut it. The assertions could not tell a correct split from no split at all.

Re-run with a structured source (horizontal gradient · yellow centre seam · white left marker · black right
marker · ruler ticks): left half carries the white marker with the seam at its right edge, right half the black
marker with the seam at its left, the gradient runs continuously across the join, and the centre tick is
bisected. **The markers are round** — which is the actual proof, because the pre-H6 double-fit would have
squashed them 2:1.

Third time in three phases that looking caught what asserting could not (H2's aspect drift, H4's picture of
nothing, now this).

## AAR (SO-5)

- **Worked** — measuring before fixing. The visual-check profile was scoped by *running* the check and counting
  which traps fired (three, all aesthetic), not by reasoning about which ought to. That turned an open question
  into a ten-line change with a provable delta.
- **Didn't** — the plan said the dev-lane annex "still reads draft pending ratification". It didn't; the
  campaign CLAUDE.md pointer did. Reading the pointer instead of the artifact put a wrong claim in an approved
  plan. Cheap here, but the same slip is how a stale index becomes load-bearing.
- **Finding** — three of the four defects were *unreachable or unemitted code*, not wrong logic. Suites cannot
  see them: every test passed the whole time. What surfaces them is asking "has this line ever run?" — the same
  question that found the H4 timeout ceiling. Worth making a standing review prompt.
- **Change** — `--profile comic` replaces the authoring guidance's advice to "review the findings rather than
  auto-failing". Advice where a mechanism belonged is a bug in the docs.
- **Follow-up** — S-1..S-4 (reject→III implementation) held until `spec_rlhf_seam` is ratified · `what/docs/`
  index full refresh · `CV-COMIC-STYLE-01` needs H3 pixels · `canvas_comic` archive after H3 · **the campaign
  close itself**.

## Next

H3 (Luke's cloud lane; spend-gated; params pre-ruled) → then re-open H6 for the campaign AAR + close, with the
real-pixel evidence this pass could not produce.
