---
type: session
session_id: session_stanley_20260813_eyegate_and_r5_canvas_slice
user: stanley
persona: Mondrian
tier: 2
campaign: campaign_canvas_halftone
mission: mission_h3_first_light
created: 2026-08-13
updated: 2026-08-13
status: completed
last_edited_by: agent_mondrian
executor_tier: opus
token_budget_estimated: "~1 session"
tags: [session, halftone, h3, eye_gate, rosetta_stone, r5, imagen_deadline, artifact_preservation]
---

# Session: the eye-gate ruling, page preservation, and Canvas's R5 slice

## Intent

Three objectives, in dependency order:

- **O1** — record the operator's **eye-gate ruling: PASS, close H3**. Four documents currently tell a
  fresh reader it is still pending.
- **O2** — get the H3 run **out of volatile `/tmp`**. 166 MB of first-light evidence behind a $3.618
  spend has been living in `/tmp/h3run` for three days; a reboot deletes it.
- **O3** — **Canvas's R5 slice**: zero `imagen-4.0-*` call sites left in this vault, four days before
  the family shuts down (2026-08-17).

## Operator rulings (this session)

| Decision | Ruling |
|---|---|
| **H3 eye-gate** (page 1 presented 2026-08-10, unruled since) | ✅ **PASS — close H3** |
| Lane selection | **Canvas's R5 slice + preserve the pages** (over fleet-R5 / H4-live / H6-close) |

## Scope declaration (tier 2)

Writes: `STATE.md` · `how/campaigns/campaign_canvas_halftone/` (master, CLAUDE.md, `mission_h3_first_light.md`)
· `what/production/demos/` · `what/artifacts/` (gitignored) · `what/production/canvas_core/tests/conftest.py`
· `what/production/comic_render/tests/test_backends_gemini.py`.

**Not touched:** `what/code/canvas_std/` (campaign firewall — verified diff-0 at close) · any other vault
(Rule 10; the fleet migration is surfaced, not executed).

**No spend.** The migration is verified statically and with the free probe. The H3 spend gate covered
one run, not a second.

## Conflict scan

`how/sessions/active/` was empty at session start. `git status` clean at `74c0e5a`.

## Progress

| # | Objective | Status |
|---|-----------|--------|
| O1 | Record the eye-gate ruling (mission · campaign master · campaign CLAUDE.md · STATE) | ✅ |
| O2 | Preserve the H3 run out of volatile `/tmp` + evidence README | ✅ |
| O3 | Canvas's R5 slice — three scripts off `imagen-4.0-*` onto the shared layer | ✅ |

## Findings

**F-1 — `build_comic_parity.py` has been broken since PT-P5.** It set
`CODE_ROOT = parents[2] / "code"` and imported `canvas_comic`/`canvas_core`, which relocated to
`what/production/` about two months ago. It failed at **import**, before ever reaching an image call.
Nobody noticed, because nothing runs it and it is gitignored. Migrating only its model literal would
have been theatre — the path is fixed too, and it imports again.

*Generalisation worth carrying:* the bootstrap this session added deliberately **searches upward**
for the shelf rather than counting `parents[n]`, and this script is the independent proof of why —
a hardcoded ancestor index is a silent time bomb that goes off at the next relocation.

**F-2 — the RLHF corpus was attributing judgements to a generator that was never called.**
`VariantInfo.model` defaulted to `"imagen-4-ultra"` at `cost_usd = 0.06`, in the dataclass **and** in
`SelectionRecord.from_dict`'s fallback. That string was never a real model ID (the real one is
`imagen-4.0-ultra-generate-001`). So any variant recorded without an explicit model — and any on-disk
record missing the key, on every load — silently acquired a **fictional** generator at an unverified
price. `mvp_imagen_fidelity.py` had the same defect at its call site, recording `imagen-4-ultra`/$0.06
while actually calling `imagen-4.0-generate-001` at $0.04.

Fixed at the source: defaults now describe **absence** (`"unknown"` / `0.0`, reusing the sentinel
`review_collect.py` already used rather than inventing a second vocabulary). Enforced by **a test that
fails if any default ever names a model again** — the H3 `REJECT_VOCABULARY_CONFIRMED` lesson applied:
a constraint that says "don't put a model name here" gets a mechanism, not a comment.

**F-3 — the sweep's honest limit.** The R5 close criterion was stated as "a fresh `imagen-4` grep
returns zero". It does not, and it should not: the remaining hits are comments explaining the
retirement, migration docstrings, and one historical fixture. **Mutating those to make a grep read
zero would be theatre.** The criterion is recorded instead as *zero live call sites, defaults or
runtime literals* — which is met.

## Verification

| Check | Result |
|---|---|
| `canvas_core` | 863 → **867 passed / 3 skipped** (the 4 new guards) |
| `comic_render` | **143 / 2** unchanged |
| Producer sweep (7) | **259** unchanged |
| `canvas_std` | **115 / 10** unchanged |
| **Firewall** `git diff -- what/code/canvas_std/` | **0** ✅ |
| `ruff` on changed files | 23 → **21** findings (2 removed, **0 added**; remainder pre-existing) |
| All three migrated scripts import | ✅ incl. the parity script, for the first time since PT-P5 |
| Capability resolution | `image.pro` → `gemini-3-pro-image`, **$0.134** @2K, lane **C63** |
| Absent-Home failure path | ✅ actionable message naming the dependency + `GOOGLEAI_PATH` |
| Free drift probe | ✅ **"registry matches the live service"**; Imagen shutdown in 4d |
| O2 preservation | **42 files SHA-256 byte-identical** |
| **Spend** | **$0.00** — no image generated |

## SITREP

**Completed** — all three objectives. The eye-gate is ruled and recorded; H3 is closed and **H6
re-open is unblocked**. The first-light evidence is durable. Canvas's Imagen exposure is closed four
days before the deadline, and two latent defects were fixed on the way.

**In progress** — none.

**Next up** — **H6 re-open** (campaign AAR + close · `CV-COMIC-STYLE-01` calibration, which now has
durable pixels · real-DPI evidence · `canvas_comic` archive, noting two migrated scripts import it).

**Blockers** — none in this vault. ⚠️ **Outside it:** the fleet's Imagen migration is **unassigned with
4 days left** and the memo was **never delivered**. `#needs-human` — either GO the memo or authorise
central execution.

**Files touched** — `STATE.md` · campaign master + `CLAUDE.md` + `mission_h3_first_light.md` ·
**NEW** `what/production/_googleai.py` · `demos/mvp_comic_demo.py` · `demos/mvp_imagen_fidelity.py` ·
`canvas_core/rlhf/selection.py` · `canvas_core/tests/test_rlhf_paths.py` ·
`what/artifacts/parity_comic/build_comic_parity.py` (gitignored) · **NEW** `what/artifacts/h3_first_light/`
(gitignored) · this session file. **2 commits** (`23c581f`, `419c9c4`); **push not taken** — Canvas is
**18 ahead**, operator-gated.

## Next Session Prompt

Operation Halftone's next gate is **H6 re-open — the campaign close**, and it is unblocked: the H3
eye-gate passed 2026-08-13, which was its only dependency. H6 carries the campaign AAR + close,
**`CV-COMIC-STYLE-01` calibration** (it was deferred for lack of real comic pixels; those now exist,
durable, at `what/artifacts/h3_first_light/` — read that tree's README first, it records what the
eye-gate settled and what each consumer needs), real-pixel DPI evidence against the 300/200 policy
(the H3 export reported 0 warnings, so the 200 floor is cleared), the HR pilot's second consumer, and
the **`canvas_comic` archive** authorised by the ratified `adr_009` — sequence that last one carefully,
because `demos/mvp_comic_demo.py` and `what/artifacts/parity_comic/build_comic_parity.py` both import
`canvas_comic`. **Before any of that, surface the time-critical item:** the fleet's `imagen-4.0-*`
migration is unassigned with the shutdown on **2026-08-17**, and the memo at
`who/coordination/coord_2026_08_10_rosetta_google_model_layer_migration.md` is still
`staged_pending_GO` and has never been delivered — the operator must either GO it or authorise central
execution, and note the R5 roster under-counts (it misses 10+ Home consumers of `api_helpers.py`).
Canvas's own three sites are already migrated. Also open, unchanged: **H4's remainder** (one live
`generate:gemini,refine:comfy@0.4/comic_panel_refine` run — ComfyUI is not running, and it needs a
fresh spend authorisation), the HR review pass, `adr_010`'s §7.7 signature, four staged memo GOs, and
the push GO (Canvas is **18 commits ahead**). Read `STATE.md` top banner first — it is current as of
2026-08-13.
