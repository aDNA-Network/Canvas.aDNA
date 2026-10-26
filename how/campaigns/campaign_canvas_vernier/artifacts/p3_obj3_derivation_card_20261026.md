---
type: artifact
artifact_kind: card
created: 2026-10-26
updated: 2026-10-26
status: built   # 2026-10-26, after the seat's SOUND (§7); was: proposed
last_edited_by: agent_mondrian
seat_verdict: "SOUND, 2026-10-26T09:3x-07:00. A read-only opus seat that did not build; 0 blocking, 7 non-blocking, applied as text (§7). The text it read is commit d86bfdc"
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
- **Expected:** yaml source **fresh** · rebuild **fresh**, gate **OK**, and the always-printed leg lines carry *"prose channel: neither leg reads it"*. Neither leg opens the `.md`; the producer uses only its stem (`consume.py:150-153` at HEAD; ~~`:140-143`~~ was the pre-`8191348` line, seat #1). This case cannot discover anything: it **demonstrates** the blind spot that §2 of the obj 2 card states, so the mission's literal "prose typo" has a recorded outcome, and that outcome is *both fresh*, not *source stale*.
- **Where the copy sits does not matter** (seat #2): nothing resolves the `prose:` path (`model.py` stores it as a string, `load_diagram` reads only the yaml, `consume.py` uses only the stem), so a typo anywhere reads both fresh. The copy is placed beside the pair only so the planted triple looks like a real one; the code comment says so.
- **What this case does and does not show** (seat #3): its words check (`PROSE_UNREAD`) is a fixed string printed on every green run, so the case shows the outcome, not a mechanism that could catch prose drift. It prints *"(demonstration)"* in its own name, `how/gates/AGENTS.md` lists it apart from the derived cases, and the mission note records that the mission's literal first half (*"a prose typo → source stale"*) reads **both fresh** here: shown false for Canvas's pairs, not derived.

## 3. Rows (outside the firewall; no signature needed)

| # | File | Change |
|---|---|---|
| 1 | `how/gates/gate_manifest.py` | Two more `--probe-freshness` cases (§2.1, §2.2). The perturbed build is a helper beside the probe; nothing in `run_gate`, the scorer or the reporter moves |
| 2 | `how/gates/AGENTS.md` | The gate #9 row's probe list gains the two cases, and one sentence recording the derived pair |
| 3 | the P3 mission | A dated note: objective 3's derivation, with the probe output pasted |

**Left at diff 0:** `what/code/canvas_std/**`, `what/production/**` (no producer change), every canvas, every spec, every door. The gate line does not move.

## 4. Tests

- `--probe-freshness` exits **0** with both new cases (13 of 13: the 11 of today plus two).
- **Each new case must be able to fail:** in scratch, flip each new case's expectation in turn (engine: expect *fresh · fresh*; prose: expect *stale · fresh*) and the probe must exit **1** each time; and set the perturbation to 0, so the D-O3-1 guard must fire (seat's optional test). Not committed.
- The full gate line is re-run after the build and pasted as a measurement; it must read as it read after the obj 2 build, `8191348` (~~`a881ceb`'s build~~, seat #7; the probe is not a gate). No phase-gate claim.

## 7. The reviewer seat's verdict (from its own report, 2026-10-26 09:3x)

**VERDICT: SOUND.** A read-only opus seat that did not build (`session_stanley_20261026_093240_d1_obj3`, under D1-J); 16 tool uses, about 2.7 min, nothing written; it read this card at `d86bfdc`. Re-derived and holding (VERIFIED by reading): the patch reaches the layout (module globals read at call time; `consume.py` imports the module and calls `layout.layout`; no from-import binds `GAP_`); the seed moves on both axes; the perturbed build stamps the same digest, so the source leg reads fresh and D-O2-8 finds no tool fault; the real rebuild reads stale and the pair FAILs with both report words; the 11 existing cases, the exit rule and the gate-line claim are right; both flip tests would exit 1.

| # | Class | Finding (abridged) | Disposition |
|---|---|---|---|
| 1 | non-blocking | `consume.py:140-143` is now `:150-153` | corrected in §2.2 |
| 2 | non-blocking | The prose copy is not the file the field names; nothing resolves the path, so placement does not matter | §2.2 says so, and the code comment |
| 3 | non-blocking | The prose case only re-runs the clean copy; its words check is a fixed string | labelled a demonstration in its name, kept apart in AGENTS.md, the mission note says the literal half reads both fresh |
| 4 | non-blocking | D-O3-1 should compare as the rebuild leg does, and assert the same digest | §5 and the code |
| 5 | non-blocking | A failed perturbed build must raise `RuntimeError` | it does (no `check=True`; returncode checked) |
| 6 | non-blocking | The engine case's report words are shared with the hand-edit case | noted in D-O3-1 |
| 7 | non-blocking | Name `8191348`, not `a881ceb` | §4 corrected |
| opt. | — | A flip test with the perturbation set to 0 | run (scratch): the guard fires, the probe exits 1 |

## 5. Decisions this card takes (each reversible by `git revert`; the seat reviews them)

- **D-O3-1. The perturbation is +1 on both gaps**, the smallest change that moves geometry. A larger perturbation proves nothing more; a perturbation of a constant no node uses would prove nothing at all, so the plant checks, before scoring, that the perturbed view **differs** from the real one compared as the rebuild leg compares (parsed, digest masked), and that it carries the **same** `sync.source_sha256` as the real build. Either check failing raises a named planting failure, never a verdict (seat #4). A failed perturbed build raises the same way (seat #5). Note (seat #6): the report words *"the legs disagree"* and *"generator drift"* are shared with the hand-edit case; what makes this the F-PL-6 shape is the plant, not the words.
- **D-O3-2. The prose case is coded, not only stated**, so the mission's literal case has a measured outcome. It is labelled a demonstration in its own output.
- **D-O3-3. No new gate.** The pair is derived in the probe flag. Making it a gate would put a perturbed build into every gate run for no new protection: the live gate already fails a stale rebuild.

## 6. Surety (LIVE FORM)

- Card and build as carded. Predicted *accept* · 0.85 · R: the 0.75 to 0.90 band, so it acts only on a sound verdict from a seat that did not build. Reversal: `git revert` the build commit.
  `surety: {"dp": "canvas.p3_obj3.card", "predicted": "accept, built as carded", "confidence": 0.85, "keys": [], "class": "R"}`
- The P3 gate. Not fired: its exit test needs `check-sync` (touch #8, unsigned) and is his (D1 round list).
