---
mission_id: mission_b4_comfyui_seam
type: mission
campaign: campaign_canvas_blueprint
phase: P4
title: "The ComfyUI canvas seam — the build half, and the instrument the gate needed all along"
owner: stanley
persona: mondrian
status: completed
created: 2026-09-08
updated: 2026-09-08
completed: 2026-09-08
completion_note: "complete-with-open-item — the build half shipped and all three ship-gate checks were met on both new surfaces, including the agent-confirmed render for the first time in this vault. Open: the mermaid trust grant is the operator's; the H4 live chain is unauthorized and should be asked for jointly when ComfyUI's M-RD1 emitter lands."
last_edited_by: agent_mondrian
executor_tier: opus
token_budget_estimated: ~150k
session: session_stanley_20260908_blueprint_p4_comfyui_seam
tags: [mission, blueprint, p4, comfyui, canvas_emission, variant_board, tuning_surface, visual_capture, amendment_1, rlhf, dispatch_contract]
---

# Mission B4 — the ComfyUI canvas seam (build half)

## Gate

Opened at the operator's plan gate, **2026-09-08** — the second session of the day, after P3 closed
at `7543e65`. The charter's P4 row is gated on *"ComfyUI standing AND a fresh operator spend
authorization"*; **STATE has always said the build half is venue-independent**, and the spec's own
§4.2 sequences it *"against fixture manifests, offline"*. That half opens now. The live H4 chain
does not.

## Three operator rulings taken at the gate

| Question | Ruling | Consequence |
|---|---|---|
| **P4 scope** | **Build half + close the render gate** | The capture port is objective 0, not a side quest — P4's own deliverable is a file-node board, and check 3 of its ship gate is unmeetable without it. |
| **Capture instrument** | **Port into Canvas + memo Hestia** | Credited at source; Home's copy untouched and still working (Rule 10). Its docstring already names this vault as its D-A eventual home. |
| **H4 spend** | **Not now** | Requested when the fixtures prove out. Their emitter does not exist yet either. |

## The finding that set objective 0

⛩ **F-P4-1 — a constraint on a method was inherited as a constraint on the capability.**

`STATE.md` has carried the Amendment-1 agent-confirmed render as unmet **four times** (P2, P2b, P2c,
P3), each time on the stated ground: *"Needs a window-scoped capture … whole-screen `screencapture`
is ruled out: it captured a third party's private messages."*

Both halves of that sentence are true. The conclusion drawn from them — that this node has no safe
capture path — is **false**, and was false when first written. `Home.aDNA/what/code/window_helpers.py`
has carried `capture_window()` since Prytaneion M1.3: it resolves a window **id** via a Swift
`CGWindowList` probe (optionally pinned by title), then calls `screencapture -l <window_id>`. It
captures one window. It cannot capture a third party's messages, because it never captures a screen.

Three things compound it:

1. The tool's own module docstring records **operator decision D-A (2026-06-02): eventual home =
   `CanvasForge.aDNA`, upstreamed at Prytaneion M6.3.** CanvasForge merged into this vault at pt09.
   The instrument was *already assigned here* and the assignment was never executed.
2. Canvas has **zero** window-capture code — verified first-hand, not assumed
   (`grep -rn screencapture what/production/ what/code/` → no hits; only `visual_review.py`'s
   Playwright HTML path exists).
3. `spec_canvas_review_surface` §5 states the HTML renderer is **file-node-blind by design**, so a
   file-node board *"can only be sight-certified live"*. P4's deliverable is a file-node board.
   Shipping it without the port means shipping a surface that structurally cannot pass its own gate.

⇒ ***a constraint on a method is not a constraint on the capability.*** Fourth instance of the
verify-the-blocker class in recent memory, and the one with the longest carry.

## Counterpart standing (read-only probe, ComfyUI.aDNA)

- Seam **accepted in principle 2026-08-23**, keyed to their **M-RD1** (their `STATE.md` consumer
  table): *"our whole cost is one JSON run manifest per batch"*.
- The emitter **does not exist yet**. Their recent work is M-RD4/M-RD5 (LoRA eval, canon-bridge).
- Their `rd_l1` node was flapping as recently as **09-07** (`caae310`).
- No active lease there; last commit `8250eac`.

⇒ Building the consumer first is not working ahead of them — it **pins the manifest contract in
executable fixtures** instead of prose, which is exactly what their emitter then has to satisfy.

## Objectives

| # | Objective | Status |
|---|---|---|
| **b4.0** | Port window-scoped capture → `canvas_core/visual_capture.py`; encode *no whole-screen path exists* as a **test**, not a discipline. | ✅ 28 tests |
| **b4.0b** | Close the 4×-carried Amendment-1 gate: sight-certify the two dogfood canvases. | ✅ **geometry certified**; mermaid sub-channel open (F-P4-3) |
| **b4.1** | Run-manifest v0.1 loader (spec §3) + extract the shared PNG/aspect helpers out of `review_canvas.py`. | ✅ 17 tests · 5 fixtures |
| **b4.2** | Variant-selection board builder — one `choice` **per slot**, provenance floor in `component_types`, sized through `layout_fit`. | ✅ 17 tests · all 3 checks |
| **b4.3** | Tuning surface + **D1 request records** (a record, never a dispatch). | ✅ 15 tests · all 3 checks |
| **b4.4** | Fixtures, full gate run, close (AAR · STATE · master · memos to Hestia + Vulcan). | ✅ both memos delivered |

## Standing constraints

- `what/code/canvas_std/` **untouched** — firewall diff-0 verified at the gate. The v2.2.0
  interaction layer already carries everything §1 needs; that is spec §5's stated point.
- **No dispatcher.** `review_dispatch_contract v0` §"Still out of scope at v0" holds in full: no
  HTTP client, no render call, no transport. **D5** (refusal atomicity — guards before any append,
  line-count-invariant across every sink) is asserted by test.
- Peer vaults **read-only**; memos left untracked for the recipient's read-receipt (Rule 10).
- Every published figure **re-derived at close**, not re-read.

## Findings

### ⭐ F-P4-2 — the sight gate was defeated by **level-of-detail culling**, not by resolution

The first capture through the new instrument was **window-scoped, correct, and useless**: Obsidian
opens a canvas at its accept-viewport zoom (~25%), and below a zoom threshold it **does not draw
node text at all** — bodies render as grey placeholder bars. Measured, not inferred: a native
**3128×1896** capture of the unzoomed canvas is pin-sharp and completely illegible.

Two things follow, and the second is the one worth keeping.

1. The inherited compression step is wrong for this use. Home's ``sips -Z 1280`` discards ~2.4× of
   linear resolution on a Retina-backed capture. That is the right trade for *their* consumer (a
   whole-window overview fed to a vision model) and the wrong one for reading a canvas. Default
   raised to 2200 here.
2. **No amount of resolution or cropping recovers text that was never rendered.** I spent a crop
   and a native re-capture proving that before the mechanism was obvious. The fix is a **zoom**
   step, not a sharper picture.

Home recorded Shift+1 zoom-to-fit as *"does not fire headlessly"* and worked around it by cropping
their own canvas to fractions tuned by hand. Re-measured here: **it fires reliably**, provided the
app is activated first — and `obsidian://open` already leaves the canvas leaf focused, so **no
click is needed** (the first canvas was clicked; the second, deliberately, was not, and behaved
identically). Their workaround was load-bearing for their layout and was carried as a limitation of
the method.

⇒ ***a capture that is technically correct can still be evidentially empty; "did the instrument
run?" and "can the gate be judged from what it produced?" are different questions.***

### ⚠ F-P4-3 — sight caught what both machine checks passed: the mermaid channel renders as source

Both dogfood canvases present their mermaid node as a **raw code block behind an un-actioned
per-vault trust prompt** — *"Display Mermaid diagrams in this vault? Only allow if you trust this
vault's contents."* (Obsidian 1.14.0). `canvas-std validate` is green, `canvas-visual-check` is
green, and the artifact a human actually sees is **unrendered source**.

This is not a canvas defect and not a layout defect — the geometry certifies clean (see below).
It is a **first-open consumer condition**: the dual-channel pattern's whole claim is that the
diagram channel is *read*, and until someone clicks Allow, in any vault, it is not. Canvas's
`.obsidian/app.json` carries the `propertiesInDocument: "hidden"` precondition
(`spec_canvas_review_surface` §5) but there is no recorded trust grant, and the prompt is new
enough that no prior gate could have caught it.

**Not actioned unilaterally** — granting mermaid trust is a trust decision in the operator's vault,
not an agent's to make. Surfaced instead.

⇒ ***the third check is not ceremony: two green machine checks and an unreadable artifact is
exactly the state the gate exists to detect, and it took one look to find.***

### ⛩ F-P4-4 — a false positive found by sight, and caught by sight

The first agent-confirmed render of the variant board showed the slot sidecar with a scrollbar and
its lower controls below the fold. That was written up as a clipping defect of the class P2c
removed from six producers — a guessed constant — and "fixed" by deriving the node height from
``fit_text_height(body)`` ≈ **1580px** against the inherited **520**.

The next render refuted it on three counts:

1. A canvas embed **scrolls**. Nothing was unreachable; there was no defect.
2. ``fit_text_height`` measures **raw markdown**, and Meta Bind renders those fences as compact
   widgets — so 1580 was never the required height either.
3. The taller node grew the board past the zoom at which Obsidian still draws node text, so
   **every caption on the board** reverted to placeholder bars. A cosmetic non-problem was traded
   for a whole-surface legibility one. A second attempt at 900 failed the same way. Reverted to
   520, re-rendered, confirmed restored.

⇒ ***the sight gate produces false positives too, and what catches them is the same discipline
that catches the true ones: render again after the fix and compare.*** Had this shipped on the
strength of one look, the board would have been strictly worse and this record would have called
it a repair. The three findings above it (F-P4-2, F-P4-3, and the F-P2-11 path bug below) are real;
this one is the reminder that the instrument is not an oracle.

### Other defects the build surfaced

- **A latent overflow in the inherited image sizer.** ``review_canvas._node_size`` read
  ``max(1, min(max_w // rw, max_h // rh))``, which returns **one whole ratio unit** when no
  integer multiple fits — i.e. a node *larger than its own fit box*. Unreachable in the HR pilot
  (~1024px square variants); reachable immediately for real output, since a 2062×3150 print panel
  — Halftone's actual page size — reduces to 1031×1575 and would have been emitted whole into a
  640×460 slot. Fixed in the shared ``layout_fit.fit_exact_aspect_box``: exactness is the goal,
  staying inside the box is the constraint, and where they conflict the constraint wins.
- **Manifest-relative paths in file nodes** (F-P2-11 again). The manifest's ``path`` is relative to
  the manifest — that is the seam's contract — so writing it straight into a node produced a canvas
  whose images resolved for the builder's cwd and nowhere else. Worse, the file-resolution traps
  then **skipped** rather than failed: *"11 traps run (no vault root — file-resolution traps
  skipped) … 0 findings [OK]"*. A green run over checks that never executed. Now vault-relative,
  and the gate is run with ``--vault-root`` so all 11 actually execute.
- **The plan's "no new collector needed" was wrong.** The collector is variant-keyed on
  ``verdict``; the spec's board is slot-keyed on ``pick``. Adding ``selection_sidecar`` support was
  the honest cost, and one sub-decision inside it mattered: a rejection recorded as
  ``<slot_id>.reject`` would have appended cleanly to the canvas and been **invisible** to
  ``fold_variant_responses``, which gathers by the ``<variant_id>.`` prefix — a rejection that
  looks recorded and reaches no sink. Rejects are keyed on the variant.

### ✅ What the gate actually certified (2026-09-08)

Read at 2200px by the executing agent, both canvases: **titles, group labels, every node body,
every edge path legible; no overlaps; no truncation; no off-canvas content; lead/heading treatment
as authored.** Evidence on the artifact shelf (gitignored, canonical on-node per `adr_010`):
`what/artifacts/visual_gate_20260908/`.

**Honest scope of the claim:** geometry, typography and layout are **agent-confirmed**; the mermaid
sub-channel is **unverified pending the trust grant**. Reported as two states, not averaged into
one — the practice E2 and the rail skill both insist on (*"never report (b) as if it were (c)"*).

## Gates at close (re-derived, not re-read)

| Gate | Result | Against baseline |
|---|---|---|
| `canvas_std` firewall | `git diff --stat` **empty** | diff 0 held |
| `canvas_std` suite | **115 passed / 10 skipped** | unchanged |
| certification (`certify.py`) | **11/11 fixtures agree** (core 1 · extended 4 · adna_native 5) | unchanged |
| `canvas_core` | **1035 passed / 3 skipped** | 958 → 1035 = **+77**, exactly this session's four test files (28 + 17 + 17 + 15) |
| producers | **267** — brief 10 · deck 16 · document 37 · diagram 44 · comic 123 · letter 17 · post 20 | unchanged |
| `comic_render` | **154 passed / 2 skipped** | unchanged |
| `canvas_presentation` | 57 passed / 2 skipped | — |
| new surfaces, schema | board + tuning both `declared=adna_native level_reached=adna_native [OK]` | — |
| new surfaces, visual | **11 traps run with `--vault-root`, 0 findings** each | file-resolution traps actually ran (F-P2-11) |
| new surfaces, **sight** | board + tuning **agent-confirmed**, legible, Meta Bind controls live | first time this check has been met in this vault |

⚠ **Population stated on the face of the number.** "267 producers" is the seven producer packages
only. It excludes `canvas_core`, `canvas_presentation`, `comic_render` and `canvas_std`, which are
counted separately above. The `+77` is arithmetic, not an estimate: every added test is in a file
this mission created.

## Memos

| # | To | Ack | Status |
|---|---|---|---|
| — | **Hestia** (Home.aDNA) — the capture port came home to its D-A destination; two loop measurements back | no | **DELIVERED** `f6321e5a…` into their **drop-box** (live lease; the box's README makes that explicitly safe) |
| — | **Vulcan** (ComfyUI.aDNA) — the consumer exists; the contract is five runnable fixtures | no | **DELIVERED** `6dacc0a8…` (no lease, no drop-box, quiescent — re-probed at act time) |

Both left **untracked** in the recipients' trees for their own read-receipt; both trees read-only
otherwise.

## AAR

**Worked.** Verifying the blocker instead of inheriting it. The single highest-value act of the
session was reading `Home.aDNA/what/code/window_helpers.py` — about two minutes — which dissolved a
gate that had been carried, in writing, four times. The three-check gate then earned its keep
immediately and repeatedly: sight found the mermaid channel rendering as raw source behind a trust
prompt (F-P4-3) that both machine checks passed green, and sight found the LOD-culling mechanism
(F-P4-2) that made the *first* correct capture evidentially empty.

**Didn't.** I found a defect by sight that wasn't one, and "fixed" it twice, each time making the
board worse — the second attempt degrading every caption on the surface to placeholder bars
(F-P4-4). What saved it was re-rendering after the fix rather than trusting the fix. I also carried
a wrong claim into the plan — *"collection needs no new collector"* — which was true for the HR
pilot's shape and false for the spec's, and I only found out by reading `fold_variant_responses`
closely enough to see that a slot-keyed reject would have appended cleanly to the canvas and reached
no sink at all.

**Finding.** ⭐ **A constraint on a method is not a constraint on the capability.** The recorded
blocker — *"whole-screen capture is ruled out, it captured a third party's private messages"* — was
true in every word and false in its conclusion. Nobody re-read it for a month because it *sounded*
like a limit of the machine rather than a limit of one approach. This is the fourth blocker in
recent memory to dissolve on being verified, and the one with the longest carry.

**Change.** The instrument now lives here, its safety property is pinned by an **AST-walking test**
rather than by discipline (exactly one `screencapture` call site, always window-scoped) — because
discipline is precisely what failed for a month. Two hardenings over the source were taken and
offered back: no cross-vault fallback in vault-id resolution, and validated Swift interpolation.

**Follow-up.** *(a)* **Mermaid trust grant is the operator's** — both dogfood canvases render their
diagram channel as source until someone clicks Allow, in any vault; not actioned unilaterally.
*(b)* **The H4 live chain remains unauthorized** and should be asked for jointly when ComfyUI's
M-RD1 emitter lands — a hand-written manifest over real pixels would prove less than the fixtures
already do. *(c)* Home may want the two loop measurements: `sips -Z 1280` discards ~2.4× of a
Retina capture, and Shift+1 *does* fire headlessly given an `activate` first — their cadence may be
critiquing LOD-culled frames. *(d)* `b1.5` still open on Rosetta; memo #13 still staged.

⭐ **The finding that outlives this mission.** ***A capture that is technically correct can still be
evidentially empty.*** "Did the instrument run?" and "can the gate be judged from what it produced?"
are different questions, and only the second one is the gate. The first capture of the session was
window-scoped, correctly framed, pin-sharp at 3128×1896 — and contained no readable text anywhere,
because Obsidian had never drawn any. A green run is not evidence; a *readable* one is.

---

## Addendum, 2026-09-09 (Blueprint P5 close) — the other half of the seam exists, and we measured it

**Follow-up (b) resolved on one side, and it moved faster than the mission predicted.** ComfyUI
delivered an untracked memo to `who/coordination/` the day after this mission closed
(`coord_2026_09_09_outbound_vulcan_to_mondrian_emitter_exists_validates_against_your_fixtures`,
intaken byte-unchanged at `677b65b`, `ack_required: false`).

**Their emitter shipped, and this mission's sequencing is why.** `emit_run_manifest.py` v0.1.0 was
keyed to their **M-RD1** milestone. Reading the five fixtures made it venue-independent, their
operator ruled it forward at the next plan gate, and it shipped the same sitting. The plan's claim
— *"building the consumer first turns §3 from a paragraph into five fixtures an emitter can run
against"* — was load-bearing rather than rhetorical.

**We re-derived their 12/12 rather than repeating it**, because it is a claim about *our* code and
this campaign's defining finding is that stated facts do not verify themselves. An independent
script (our loader, their manifest; no import of their emitter, no run of their validator):

**15/15** — their 12 plus three checks they did not run: the committed record is byte-identical to
the live manifest (`332b27fed1a7`); **every path resolved and every PNG was genuinely probed** (20 ×
real `(1024, 1024)`, zero zero-dims — the check exists because P4 shipped traps that *skipped while
printing `0 findings [OK]`*); and on-disk md5 == recorded md5 for all 20, verified from our side
too. `ComfyUI.aDNA` `git status -uall` was **0 entries** after every run.

⛩ **F-P5-1 — a manifest is only loadable where its pixels are.** Loading their **committed** copy
from `campaign_rd_forge/artifacts/` raises `ManifestError: no slot has a variant image on disk (25
skipped)` — 20 variants excluded-and-named plus 5 emptied slots reported-not-vanished, which is
`partially_failed.json`'s contract behaving exactly right. Not a defect. But it means the **durable**
half of the seam's evidence does not load, and the half that loads (beside the pixels, under a
gitignored `.local_dataplane/`) is not durable. ⇒ ***the version-controlled record of a run cannot
be re-derived by anyone who does not already hold the gitignored pixels.*** Our own `adr_010` makes
the identical trade deliberately, so this is a shared property of how both vaults store heavy
artifacts, not their fault. Raised to them as an observation for their v1.0 provenance story
(memo #16), with two cheap options and **no spec change proposed**.

**Follow-up (b) still stands on the live chain**: their emitter exists; their **M-RD1 venue
manifest** does not. Both vaults independently restated the same boundary — the ask is joint when it
lands. Spend was never requested and Blueprint closed without requesting it.

Follow-ups *(a)* mermaid trust, *(c)* the two loop measurements for Home, and *(d)* `b1.5` + memo #13
carry past the close as named STATE watch items.
