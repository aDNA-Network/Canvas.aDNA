---
type: mission
mission_id: mission_h3_first_light
campaign_id: campaign_canvas_halftone
phase: H3
status: completed                  # rendered 2026-08-10: 27 images, $3.618, 4 pages. The 2026-08-09 'blocked on billing' call was a misdiagnosis — see §The "blocker".
owner: stanley
persona: Mondrian
executor_tier: opus
token_budget_estimated: "1 session — geometry-aspect in bridge core + 1 new backend + ~60 tests + S-1..S-4 + 2 staged memos + records"
created: 2026-08-09
updated: 2026-08-12
last_edited_by: agent_mondrian
relates: ["halftone_roadmap.md §1 (backends) + §2 H3 row + §4 open decision #1", "halftone_gap_register.md G1", "halftone_dev_lanes.md §3a", "what/specs/spec_rlhf_seam.md §5"]
tags: [mission, halftone, h3, first_light, gemini, aspect, spend_gate, rlhf, reject, imagen_deprecation]
---

# Mission: H3 — first light (and the ratification tail)

## Intent

Render the first real comic page this vault has ever produced. Everything else in Halftone was
built; `backends/gemini.py` raised `NotImplementedError` naming its phase, so the generate stage had
never produced a pixel.

**Gates**: the 2026-08-09 plan approval opened the phase (HV/H2/H4/H5/H6 precedent) **and** the
spend gate in the same ruling, **and** reassigned the phase in full to Mondrian (dev-lane annex
§3a). Three §7.7 ratifications were signed at the same gate.

## Objectives

| # | Objective | Status |
|---|-----------|--------|
| O0 | Record the three ratifications (`spec_rlhf_seam` · dispatch-contract amendment · `adr_009`) | ✅ |
| O1 | Geometry-derived aspect in bridge core (`extract.py` + `aspect.py` + manifest) | ✅ |
| O2 | `backends/gemini.py` + registry flip + `cloud` extra + contract fixtures | ✅ |
| O3 | SPEND GATE: verify model + pricing, then live dispatch | ✅ **2026-08-10** — 27 images, $3.618, 4 pages |
| O4 | Operator eye-gate on the composited page | 🟡 **presented 2026-08-10, not yet ruled** |
| O5 | S-1..S-4 reject→III (released by O0's ratification) | ✅ |
| O6 | H6 re-open + campaign close | ⛔ waits on the eye-gate (O4) |
| O7 | Dev-lane amendment + staged memos + records | ✅ |

## The "blocker" (O3) — reported 2026-08-09, ⚠️ **MISDIAGNOSED**, resolved 2026-08-10

**What this section said on 2026-08-09**, retained because a wrong call is worth keeping legible:

> `429 RESOURCE_EXHAUSTED — "Your prepayment credits are depleted."` Account-wide, reproduced on
> three models including a text-only call. The credential is valid. **This is a billing state.**
> Resolution is a top-up at `ai.studio/projects`, which is the operator's.

**Every observation there was true. The conclusion was wrong, and it was mine.**

The `429` was real. But `GEMINI_API_KEY` — the variable this backend read — is Home credential
**C05**, and `Home.aDNA/what/inventory/inventory_credentials.md` documents it as *credit-empty and
deliberately out of the render chain*. Meanwhile **C63** (`SS_GEMINI_VERTEX_SA`), a **funded Vertex
service account**, was configured and working on the same node — ScienceStanley had been rendering
through it since 2026-08-03.

**"Account-wide" was the reasoning error.** Reproducing the failure on three models proved only that
all three requests used *the same dead credential*. It felt like breadth; it was one lane tested
thrice. The check that would have settled it was reading the broker's own inventory — one tool call,
in this vault's own workspace.

**Cost of the error:** the operator was told to spend money that did not need spending, and H3 sat
"blocked" for a day for no reason.

**Resolved** 2026-08-10 by Operation Rosetta Stone
(`Home.aDNA/how/campaigns/campaign_rosetta_stone/`), which put credential-lane resolution in one
place so no call site chooses a credential again.

## What actually ran (O3, 2026-08-10)

```
comic-render plan|dispatch|select|write-back|validate|compose   # --chain "generate:gemini"
```

| | |
|---|---|
| Images | **27** (9 panels × 3 variants) |
| Spend | **$3.618** — exactly the pre-verified figure, inside the $5 cap |
| Lane | **C63 `SS_GEMINI_VERTEX_SA`** (Vertex, `location=global`) |
| Model | `gemini-3-pro-image` @ $0.134 (2K) |
| Pages | **4** × 2062×3150, `export_report.md` **0 warnings** |
| Round-trip | `sync_hash c56c73c08428f621` byte-identical; 16 nodes / 13 edges unchanged |
| Validate | `ok=True`, `adna_native`, D-1/2/3 green, 9 files, 0 warnings |

**A second finding surfaced mid-run:** the batch produced 5 images, hit `RESOURCE_EXHAUSTED`, and
succeeded on a retry moments later. That is a **rate limit wearing the same error string as spent
credit** — the second time in two days that message misled. Exponential backoff went into the shared
layer rather than here; the `aDNA.aDNA` runners turn out to have hand-rolled the same 10/20/40/80s
loop independently, which is corroboration.

**H4's remainder is still open**: the run was `generate:gemini` **only**. The
`generate:gemini,refine:comfy@0.4/comic_panel_refine` chain has never run live.

## Findings

**F-H3-1 — Imagen 4 dies on 2026-08-17, and the fleet's reference client is built on it.** Verified
live: the whole `imagen-4.0-*` family is deprecated with a shutdown date **eight days** after this
mission. `adna_lab.mcp.image.server.GeminiImageClient` — the precedent this backend was adapted
from, and the fleet's reference for image generation — calls `generate_images` against exactly that
family. Building H3 on the precedent as-written would have shipped a backend with a fortnight to
live. `comic_render` targets the Gemini native image models via `generate_content` +
`response_modalities=['Image']` instead: different call, different config object, different response
shape. **Fleet-relevant** — flagged to Berthier for Luke, and worth knowing in any vault that
generates images.

**F-H3-2 — the aspect menu is 14 entries, not 5, and asking cost nothing.** Sending a deliberately
invalid ratio returns a 400 that enumerates the valid set — rejected at validation, before
generation, so it is free and cannot go stale the way a hand-copied list does. The menu is
`1:1 · 1:4 · 1:8 · 2:3 · 3:2 · 3:4 · 4:1 · 4:3 · 4:5 · 5:4 · 8:1 · 9:16 · 16:9 · 21:9`. This
directly changed the output: the splash snaps to **2:3 (residual 0.030)** on Gemini's real menu
versus **9:16 (0.140)** on the conservative default. Making the menu belong to the backend rather
than hardcoding one paid for itself the first time it was used.

**F-H3-3 — the declared aspect and the drawn box disagree, and only the geometry is true.** The
mini-issue splash declares `3:4` (0.750) and is drawn 663×1025 (**0.647**); the wide establishing
panels declare `16:9` (1.778) and are drawn at **1.957**. The second case is the instructive one —
the *label is correct* and the panel is still ~9.6% off it, so a drift check that only compared
labels would report agreement. The warn threshold is set at ~8% for that reason.

**F-H3-4 — snapping bounds the crop; it does not remove it.** Backend menus are discrete and panel
geometry is not. Recording the residual is the deliverable; `CV-IMAGE-ASPECT-RATIO-01` remains the
instrument that measures what is left. Documented in `aspect.py` rather than left for a future
reader to discover by disappointment.

**F-H3-5 — the reject constant had never been reachable.** `RLHF_SIGNAL_TYPE_REJECT` was declared
when the III bridge was written and the accept path hard-coded `accept`, so a reject-only review
pass produced no Schema-A record and therefore **no III signal at all** — the rejection durable in
`responses[]` and invisible to every learning consumer. Built at O5 under the ratification that
released it.

**F-H3-6 — a spec constraint needs a mechanism, not a resolution.** `spec_rlhf_seam` §5 requires
Argus's vocabulary confirmation *before first emission*. Shipping code that emits by default and
trusting nobody runs the collector would violate the spec ratified the same morning. Hence
`REJECT_VOCABULARY_CONFIRMED = False`, two tests asserting the default holds, and a `rejects_held`
count that makes the hold visible in the run summary.

**F-H3-7 — breaking lists out of the CLI summary made `generated=[]` disappear.** An empty list
rendered as no lines at all, silently deleting the idempotency proof that a re-run did zero work.
Caught by `test_rerun_is_idempotent`. Empty lists stay in the summary; only non-empty ones become
detail lines.

## Verification

| Check | Result |
|-------|--------|
| `comic_render` | **154 passed, 2 skipped** (was 94/1) |
| `canvas_core` | **863 passed, 3 skipped** (was 841/3) |
| boundary guard | green — no render engine, no producer import |
| `canvas_std` firewall | `git diff --stat` **empty** |
| `ruff` | clean on `comic_render`; no new findings in `canvas_core` |
| live API surface | captured to `comic_render/tests/fixtures/gemini/api_surface_20260809.json` |
| **the composited page** | ❌ **not produced** — see the blocker |

Tests inverted rather than deleted (H6 precedent): `test_registry_fake_available_gemini_still_gated`
→ `..._now_live`; `test_reject_only_session_appends_responses_only` → `..._now_emits_a_signal`
(that one had been asserting the bug).

## AAR *(rewritten 2026-08-12 — the 2026-08-09 version is superseded and quoted below)*

- **Worked** — checking ground truth *against the service* before writing code. The Imagen
  deprecation and the real 14-entry aspect menu were both found by asking the API instead of
  trusting the precedent and the docs; each changed the design, and the free-400 trick for
  enumerating valid values is reusable.
- **Didn't** — **I diagnosed the blocker wrong and told the operator to spend money.** The `429` was
  real; "the account is out of credits" was not. The backend read `GEMINI_API_KEY` (**C05** —
  documented in this workspace as credit-empty and out of the render chain) while a **funded Vertex
  service account (C63)** sat working on the same node. I then "confirmed" it account-wide by
  retrying three models — which only re-tested the same dead credential. **Breadth of retries is not
  breadth of evidence.**
- **Finding** — the same error string means two different things. `RESOURCE_EXHAUSTED` was a dead
  credential on 2026-08-09 and a **rate limit** on 2026-08-10, mid-run, after 5 successful images.
  Neither is diagnosable from the message alone; both need the lane and a retry to tell apart.
- **Change** — credential selection left the call sites entirely
  (`Home.aDNA/what/code/googleai/credentials.py`), and a quota refusal now **names its lane and the
  untried funded alternatives**. The class of error is closed, not just this instance. Separately:
  spec constraints that say "before X" got a mechanism (`REJECT_VOCABULARY_CONFIRMED`) rather than a
  note — adopt that for the next "must confirm before" clause.
- **Follow-up** — the operator's **eye-gate** (presented, unruled) → **H6 re-open** for the campaign
  AAR and close · **H4's remainder** (the refine chain has still never run live) ·
  `CV-COMIC-STYLE-01` calibration, which now has the real pixels it was waiting for.

> **Superseded 2026-08-09 AAR lines, kept verbatim (SO-3/SO-7):**
> *"**Didn't** — the live render. Not for want of code: the account has no credits. It was also not
> discoverable from anything in the vault, which is the argument for probing early rather than at
> the end of the build."* · *"**Follow-up** — top up credits → one command closes O3, O4…"*
>
> Both are wrong in the same way, and the second clause of the first is wrong twice over: it **was**
> discoverable from the vault. `Home.aDNA/what/inventory/inventory_credentials.md` names C05 as
> depleted and C63 as the funded render credential. I did not read it.
