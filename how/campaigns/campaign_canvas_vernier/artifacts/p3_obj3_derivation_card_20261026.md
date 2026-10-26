---
type: artifact
artifact_kind: card
created: 2026-10-26
updated: 2026-10-26
status: proposed
last_edited_by: agent_mondrian
campaign: campaign_canvas_vernier
phase: P3
mission: mission_vernier_p3_freshness_both_ways
objective: 3
executor_tier: opus
authored_in: session_stanley_20261026_093240_d1_obj3 (Automator day order D1-4, judgement grant D1-J)
drafted_from: "the N2-J sitting's scratch draft (canvas/obj3_card_draft.md, 2026-10-26 01:38), re-derived at HEAD a881ceb"
binds: "nothing. Outside the firewall (what/code/canvas_std/ stays at diff 0); no producer change; no signature needed; the gate line does not move (the probe is a flag, not a gate)"
tags: [vernier, p3, gate_9, derivation, f_pl_6, false_positive, false_negative, prose_channel, probe_freshness, card, proposed]
---

# P3 objective 3: the false-positive / false-negative pair, derived rather than described

The mission's objective 3 reads: *"Prove the false-positive / false-negative pair by derivation: a prose typo → source stale, rebuild fresh; a layout-engine change → source fresh, rebuild stale (the F-PL-6 shape)."* (`missions/mission_vernier_p3_freshness_both_ways.md`, Objectives §3.)

## 1. What objective 2 already derives, and what it does not

`--probe-freshness` (built at `8191348`) runs gate #9's own helpers over planted pairs. It already derives:
- **source stale · rebuild fresh**, the pre-filter's false positive, with *a YAML comment appended to the source* (gate OK, the disagreement printed). This is the mission's first half **re-read**: for Canvas's pairs the source is the `.diagram.yaml`, not the prose (obj 2 card §6, the first seat's #1). The mission's literal "prose typo" is a different case, §2.2 below.
- only an **analogue** of the second half: *one node's x moved in the view* (fresh · stale). That is a hand edit of the view, not a change of engine. F-PL-6 was the engine changing under unchanged sources (2026-09-07, the P2c re-gate), and the probe does not yet build anything with a different engine.

## 2. The two new probe cases

### 2.1 The layout engine changed after the build (the F-PL-6 shape, for real)

- **Plant:** build the planted view with a **perturbed engine**: `diagram_generator.layout.GAP_X` and `GAP_Y` each +1, in a subprocess under the runner `PYTHON` that patches the module and then calls the CLI's own `main` (so the view is stamped with the same digest as every real build). The vault's engine is never patched; the perturbation lives only in that subprocess.
- **Check:** gate #9's legs with the **real** engine, exactly as `run_gate` runs them.
- **Expected:** yaml source **fresh** (the same bytes, so the digest the perturbed build stamped equals the recompute, and D-O2-8 finds no tool fault) · rebuild **stale** (the real engine's view differs). The gate scores the pair **FAIL**, and its report says *"the legs disagree"* and names *"generator drift"*. This is the false negative of the pre-filter, derived: the source leg alone would have called this pair fresh.
- `GAP_X` and `GAP_Y` are module globals read at call time (`layout.py:21-22`, used at `:122-145`), so a module-level patch reaches the layout (VERIFIED, read). The N2-J sitting's scratch trial (01:38) showed a +1 build differs from the real one (`cmp`); this card re-derives it in the probe itself.

### 2.2 A typo in the prose beside the pair (the third blind spot, derived rather than stated)

- **Plant:** a copy of the seed's prose `.md` (the file the seed's `prose:` field names, under its own stem) beside the planted pair; the view built; then a typo appended to the `.md`.
- **Expected:** yaml source **fresh** · rebuild **fresh**, gate **OK**, and the always-printed leg lines carry *"prose channel: neither leg reads it"*. Neither leg opens the `.md`; the producer uses only its stem (`consume.py:140-143`). This case cannot discover anything: it **demonstrates** the blind spot that §2 of the obj 2 card states, so the mission's literal "prose typo" has a recorded outcome, and that outcome is *both fresh*, not *source stale*.

## 3. Rows (outside the firewall; no signature needed)

| # | File | Change |
|---|---|---|
| 1 | `how/gates/gate_manifest.py` | Two more `--probe-freshness` cases (§2.1, §2.2). The perturbed build is a helper beside the probe; nothing in `run_gate`, the scorer or the reporter moves |
| 2 | `how/gates/AGENTS.md` | The gate #9 row's probe list gains the two cases, and one sentence recording the derived pair |
| 3 | the P3 mission | A dated note: objective 3's derivation, with the probe output pasted |

**Left at diff 0:** `what/code/canvas_std/**`, `what/production/**` (no producer change), every canvas, every spec, every door. The gate line does not move.

## 4. Tests

- `--probe-freshness` exits **0** with both new cases (13 of 13: the 11 of today plus two).
- **Each new case must be able to fail:** in scratch, flip each new case's expectation in turn (engine: expect *fresh · fresh*; prose: expect *stale · fresh*) and the probe must exit **1** each time. Not committed.
- The full gate line is re-run after the build and pasted as a measurement; it must read as it read at `a881ceb`'s build (the probe is not a gate). No phase-gate claim.

## 5. Decisions this card takes (each reversible by `git revert`; the seat reviews them)

- **D-O3-1. The perturbation is +1 on both gaps**, the smallest change that moves geometry. A larger perturbation proves nothing more; a perturbation of a constant no node uses would prove nothing at all, so the case also checks that the perturbed view differs from the real one before scoring it (a planted "engine change" that changes nothing must read as a planting failure, not as fresh).
- **D-O3-2. The prose case is coded, not only stated**, so the mission's literal case has a measured outcome. It is labelled a demonstration in its own output.
- **D-O3-3. No new gate.** The pair is derived in the probe flag. Making it a gate would put a perturbed build into every gate run for no new protection: the live gate already fails a stale rebuild.

## 6. Surety (LIVE FORM)

- Card and build as carded. Predicted *accept* · 0.85 · R: the 0.75 to 0.90 band, so it acts only on a sound verdict from a seat that did not build. Reversal: `git revert` the build commit.
  `surety: {"dp": "canvas.p3_obj3.card", "predicted": "accept, built as carded", "confidence": 0.85, "keys": [], "class": "R"}`
- The P3 gate. Not fired: its exit test needs `check-sync` (touch #8, unsigned) and is his (D1 round list).
