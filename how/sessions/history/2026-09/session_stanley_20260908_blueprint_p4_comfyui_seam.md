---
type: session
session_id: session_stanley_20260908_blueprint_p4_comfyui_seam
created: 2026-09-08
updated: 2026-09-08
status: completed
tier: 2
persona: mondrian
operator: stanley
campaign: campaign_canvas_blueprint
phase: P4
executor_tier: opus
last_edited_by: agent_mondrian
tags: [session, canvas, blueprint, p4, comfyui, canvas_emission, variant_board, tuning_surface, visual_capture, amendment_1, rlhf]
---

# Session — Blueprint P4: the ComfyUI canvas seam (build half)

## Intent

Opened at the operator's plan gate 2026-09-08, the second session of the day (P3 closed at
`7543e65` this morning). P4 implements Canvas's side of `what/specs/spec_comfyui_canvas_emission.md`
v0.1 — the variant-selection board and the tuning surface — **against fixture manifests, offline**,
which is what the spec's own §4.2 sequences. The live H4 chain stays behind its spend gate.

## Cold-start ritual

| Check | Result |
|---|---|
| `how/sessions/active/` | empty (`.gitkeep` only) — no peer lease |
| `who/coordination/inbox/` drop-box | empty (`README.md` only) |
| `git status --porcelain -uall` | **zero** — no untracked inbound memo anywhere in the tree |
| `git log` HEAD | `7543e65` (P3 close) — tree clean |

Nothing arrived after the P3 close. The `-uall` sweep is run because the drop-box README makes it
binding on the session ritual, and because a collapsed-directory listing hid an inbound memo once
already.

> ⚠ **True at open, not at close.** ScienceStanley delivered their reply to memo #11 into the
> drop-box **mid-session** (17:15), while P4 was in flight. Found at the pre-commit `-uall` sweep
> and intaken byte-unchanged. The table above is left as measured at open rather than back-edited —
> a cold-start record that silently absorbed a later arrival would be the same defect P3 caught in
> itself (a record running ahead of the thing it records). The box working under an active session
> is exactly what it was opened for.

## Operator rulings taken at the gate

| Decision | Ruling |
|---|---|
| **P4 scope** | **Build half + close the render gate.** Live chain held. |
| **Capture instrument** | **Port into Canvas + memo Hestia.** Credited at source; Home's tree untouched (Rule 10). |
| **H4 spend** | **Not now** — request when the fixtures prove out. |

## Pre-planning finding (the one that set objective 0)

⛩ **F-P4-1 — the blocker carried four times is false as stated.** `STATE.md` has recorded the
Amendment-1 agent-confirmed render as unmet since 2026-09-04 on the ground that no safe
window-scoped capture exists on this node. **It exists**, and has since Prytaneion M1.3:
`Home.aDNA/what/code/window_helpers.py:capture_window()` shoots a single window **by id**
(`screencapture -l <window_id>`, title-pinned, no focus steal) and cannot capture a third party's
content. Its own docstring records operator decision **D-A (2026-06-02): eventual home =
CanvasForge.aDNA** — which merged into this vault at pt09.

What made it invisible: the true statement *"whole-screen `screencapture` is ruled out — it captured
a third party's private messages"* was carried forward as *"no capture is possible here"*. A
constraint on **one method** was inherited as a constraint on **the capability**.

It is not a side quest either. `spec_canvas_review_surface` §5 states the HTML renderer is
**file-node-blind by design**, so a file-node board "can only be sight-certified live" — and P4's
deliverable *is* a file-node board. Verified first-hand: `grep screencapture` over
`what/production/` + `what/code/` returns **nothing**; Canvas has only the Playwright HTML path. So
without the port, P4 would ship a surface that structurally cannot pass check 3 of its own
three-check ship gate.

⇒ ***a constraint on a method is not a constraint on the capability, and inheriting one as the
other is how a solved problem stays open for a month.*** Fourth instance of the verify-the-blocker
class.

## Counterpart standing (read-only, ComfyUI.aDNA)

Their side is **accepted in principle 2026-08-23** (their `STATE.md` consumer table) and keyed to
**M-RD1** — the manifest emitter **does not exist yet**, and their `rd_l1` node was flapping as
recently as 09-07 (`caae310`). No active lease there. Building Canvas's consumer first pins the
manifest contract in **executable fixtures** rather than prose, which is what their emitter then
has to satisfy.

## Objectives

See `how/campaigns/campaign_canvas_blueprint/missions/mission_b4_comfyui_seam.md`.

## Files touched

**Created** — `canvas_core/visual_capture.py` · `canvas_core/rlhf/{image_probe,run_manifest,variant_board,tuning_surface}.py` ·
`canvas_core/tests/test_{visual_capture,run_manifest,variant_board,tuning_surface}.py` ·
`canvas_core/tests/fixtures/run_manifests/` (5 manifests + 6 synthetic PNGs) ·
`missions/mission_b4_comfyui_seam.md` · 2 outbound memos · this session file.

**Modified** — `canvas_core/layout_fit.py` (+`fit_exact_aspect_box`) · `canvas_core/rlhf/review_canvas.py`
(helpers extracted; behaviour identical) · `canvas_core/rlhf/review_collect.py` (`selection_sidecar`) ·
`what/specs/spec_comfyui_canvas_emission.md` (0.1 → 0.2, +§3a) · `STATE.md` · campaign master.

**Intaken** — SS's reply to memo #11 (drop-box, byte-unchanged).

**Untracked in peer trees (read-receipt theirs)** — Hestia's memo in `Home.aDNA/who/coordination/inbox/`;
Vulcan's in `ComfyUI.aDNA/who/coordination/`.

⚠ **Reverted, deliberately** — `what/context/context_canvas_surface_legs.canvas` +
`what/decisions/adr_004_production_code_layout.canvas` showed as modified after the sight gate ran.
Investigated rather than committed: **JSON-equal to HEAD**, every `toEnd`/`fromSide`/node/edge
preserved — Obsidian had merely re-serialized (tabs + compact objects) on open. **Not F-HR-1**, but
worth recording: **running the third check is not read-only.** These canvases are generator-emitted
(`authority: generator`), so their canonical form is the generator's; committing Obsidian's
serialization would put the next generator run permanently in diff. Reverted; re-validated
`adna_native [OK]`.

## SITREP

**Completed.** Blueprint **P4 build half** — `mission_b4_comfyui_seam` closed complete-with-open-item.
The seam's three modules on five executable fixtures; the collector extended for slot sidecars; the
capture instrument ported and the **Amendment-1 render gate met for the first time in this vault**,
on its fifth carry. All gates green and re-derived at close: firewall diff 0 · `canvas_std` 115/10 ·
certification 11/11 · `canvas_core` 958→**1035**/3 (+77, exactly this session's four test files) ·
producers 267 · `comic_render` 154/2 · both new surfaces `adna_native [OK]` + 11 traps/0 findings
**with `--vault-root`** + agent-confirmed sight. Two memos delivered md5-verified; one inbound
intaken.

**In progress.** Nothing. P4's build half is complete; its live half was deliberately not opened.

**Next up.** *(1)* **Owed to SS**: run `normalize_edges` on their five and hand them the output —
they said yes and we have not done it. *(2)* **P5 (close)** at the operator's gate. *(3)* The joint
M-PL3 sitting when Blueprint reaches it.

**Blockers.** None. Two things wait on people, not on work: the **mermaid trust grant** is the
operator's one click, and **`b1.5`** still waits on Rosetta — now with a second consumer behind it,
since SS want a live batch as their first review-surface once the `authority` axis is ruled.

**Not done, deliberately.** The **H4 live chain**, and the spend request for it. ComfyUI's emitter
does not exist and their node was flapping on 09-07; five fixtures prove more than one hand-written
manifest over real pixels would. It is now a joint ask with Vulcan, not a Canvas-side blocker.

## Next Session Prompt

Canvas.aDNA (Mondrian). Operation Blueprint is at **P5 (close), HOLD** — P0–P4 all shipped
complete-with-open-item; P4's build half landed 2026-09-08 and its live H4 chain is still
unrequested by design. **Start with the debt, not the phase:** ScienceStanley's reply (intaken in
`who/coordination/inbox/`) accepted our §4 offer and asked us to run `canvas_core/conform.py`'s
`normalize_edges` over their five failing canvases and hand them the output — they land it under
their own commit, so this is an offer with files attached, never a write into their tree (Rule 10).
Their other two rulings need no action now: the comic nine are a **joint M-PL3 sitting** to stage
when Blueprint reaches it, and the 20 review boards are **declined as dead work** on a fact we did
not have (`campaign_ss_site_visual_polish` is `superseded`). Then P5 at the operator's gate: AAR
rollup, `federation_index` refresh, STATE close, and the carried tail (`ImagenWiring` panel-path
deprecation · `comic_book_design/` resurrect-or-archive). Two items wait on people: the **mermaid
trust grant** (operator, one click — both dogfood canvases currently show their diagram channel as
raw source to any first-time viewer) and **`b1.5`** with Rosetta, which now gates a *second*
consumer since SS want a live image batch as their first review surface. The sight gate is now
runnable — `python -m canvas_core.visual_capture <canvas>` from `what/production` — and two things
about it are load-bearing: never skip the zoom step (Obsidian culls node text below a zoom
threshold, so an unzoomed capture is evidentially empty), and **re-render after any fix**, because
it produced a false positive this session that cost two renders to kill. Opening a canvas also
re-serializes it; check any resulting canvas diff for JSON-equality before committing or reverting.
