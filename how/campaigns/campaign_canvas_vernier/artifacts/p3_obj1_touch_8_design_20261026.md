---
type: artifact
artifact_kind: design
created: 2026-10-26
updated: 2026-10-26
status: proposed
last_edited_by: agent_mondrian
campaign: campaign_canvas_vernier
phase: P3
mission: mission_vernier_p3_freshness_both_ways
objective: 1
authored_in: session_stanley_20261026_001833_n2_19_hygiene (unattended; Automator Night 2 row N2-19)
binds: nothing. This is a draft for the touch-#8 signature door, not a ruling. canvas_std stays at diff 0 until the operator signs
tags: [vernier, p3, check_sync, firewall_touch_8, design, proposed, freshness, blind_spot]
---

# P3 objective 1: the `check-sync` design, with touch #8 named row by row

The P3 mission says touch #8 is not authorised yet. As with #7, every file is named row by row and the operator signs before `canvas_std` moves, at a door rendered from objective 1's design. This file is that design. Nothing it names has been built. Line numbers were VERIFIED by grep and sed on 2026-10-26 at HEAD `1667b24`.

## 1. The contract: `canvas-std check-sync`

```
canvas-std check-sync <canvas> [--source <path>] [--json]
```

The command runs every leg it can without the generator. It prints one line per leg, and every line names what that leg cannot see:

| Leg | Compares | Runs when | Cannot see |
|---|---|---|---|
| **topology** | `compute_sync_hash(doc)` with the stored `_reserved.sync.sync_hash` (`roundtrip.py:32`) | the canvas declares a `sync_hash` | any change that keeps the node ids and the `from->to` pairs: a prose typo, a relabel, a geometry or layout-engine change |
| **source** | `compute_source_sha256(--source)` with the stored `_reserved.sync.source_sha256` (`roundtrip.py:50`) | `--source` is given and the canvas declares a `source_sha256` | generator drift with the same input (the F-PL-6 shape). It also cannot tell a material byte change from an immaterial one: any changed byte reads as stale |
| *rebuild* | not run here | never in this CLI | *(printed as a footer)* rebuild-and-compare needs the generator, so it is gate #9's leg and runs in the owning vault |

**Exit codes.** `0` means every leg that ran reads fresh. `1` means a leg that can fail reads stale (see D-2). `2` means unreadable input, or **no leg could run**. A run that checks nothing must not exit 0. This vault has learned that twice already: *a cross-check that cannot fail looks exactly like a cross-check that passed* (P2b), and F-V-9. A leg that cannot run prints `n/a (<reason>)`.

## 2. Decision points for the door (recommendations, not rulings)

- **D-1: where `check_sync()` lives.** (i) In `conformance.py` beside the CLI, with no new package export. This is the smallest touch, and `__init__.py` stays at diff 0. (ii) In `roundtrip.py` beside the two hash functions, plus an `__all__` export so third parties can call it from Python. **Rec: (i).** The CLI is the third-party face that the mission names. An export can follow in a later touch if someone asks for it.
- **D-2: does a topology mismatch fail `check-sync`?** **Rec: no.** Print it as an advisory and exit 1 only on a stale **source** leg. This mirrors the signed D-1 (i) of LIP-0011, under which the topology check is advisory at both tiers. ⛩ **The exit gate depends on this choice.** The mission's exit gate says *"Terminal's 8 pass from outside their tree"*. P1 measured Terminal at **8/8 source-hash · 0/8 topology** (REPORTED from the 10-12 re-derivation; re-derive at build). Terminal migrates once, after P4 (their 10-12 reply). So if a topology mismatch exits 1, the P3 exit gate cannot be met until after P4, and the phase order would then be wrong. If D-2 is ruled "yes, fail", the exit gate's Terminal clause moves to P4 by a dated amendment. It is never quietly dropped.
- **D-3: no LIP.** Touch #8 is tooling and corpus only. No Standard text changes, and the Standard stays **v2.5.0**. If the operator reads it otherwise, a LIP comes first and the touch waits.

## 3. Touch #8: the rows, inside the firewall (`what/code/canvas_std/`)

| # | File | Change | Why |
|---|---|---|---|
| 1 | `src/canvas_std/conformance.py` | Add a `check-sync` subparser to `_cli` (:82), plus `check_sync()` (D-1 (i)) | objective 1 |
| 2 | `src/canvas_std/conformance.py` | Add `ConformanceReport.advisories: list[str]` (additive, default empty), filled from `validate.advisories(doc, declared)` (`validate.py:187`). `_report_dict` carries it. The `validate` CLI prints each advisory as a warning, and the exit code never changes because of one | touch-#7 residue (LIP-0011 §As implemented) |
| 3 | `src/canvas_std/conformance.py` | Change three strings from v2.4.0 to v2.5.0: the `json_schema` docstring (:69), the CLI description (:87) and the `schema` help (:94). Better: derive them from `STANDARD_VERSION`, as `canvas_context` was at 10-13 | touch-#7 residue |
| 4 | `README.md` | Change four v2.4.0 mentions to v2.5.0 (:3 · :6 · :8 · :37), and add a `check-sync` usage block that names both blind spots | touch-#7 residue + objective 1 |
| 5 | `tests/test_check_sync.py` (new) | Test exit 0 / 1 / 2. Every leg line names its blind spot. "No leg ran" exits 2. Objective 3's pair, written as tests: a prose typo gives source stale and topology fresh; a layout-only change gives source fresh and topology fresh (and the footer names rebuild as unseen) | objectives 1 + 3 |
| 6 | `tests/test_conformance.py` | Test that the advisories field is present and the CLI prints it, and that an advisory never changes the exit code | row 2 |
| 7 | `tests/fixtures/` + `manifest.json` | Add fixture(s) that exercise every `edge.styleAttributes.arrow` value (`schema.py:71`) and both `edge.fromEnd` values (`schema.py:93`) | queue ③, ruled 2026-10-16 |
| 8 | `tests/test_schema_conformance.py` | `KNOWN_ENUM_VALUE_COVERAGE` (:92) moves from 12 to the **measured** figure. 21 is expected (12 + 7 + 2), but it is predicted only, so measure it. The "12 of 40" paragraph (:24-27) gets a dated line. Its text is not rewritten | row 7 |
| 9 | `CHANGELOG.md` | One entry naming rows 1 to 8 | house practice |

**Left at diff 0 (named so the signature is informed):** `validate.py` · `reserved.py` · `schema.py` · `roundtrip.py` · `__init__.py` (under D-1 (i)) · `data/adna_canvas_v2.schema.json` · `certify.py`. Every spec under the Standard is also left untouched (D-3).

**Pins re-derived after the touch, by stash/restore and never predicted:** the `canvas_std` count (236/22 today) and certification (15/15 today, if row 7 adds corpus files). These are gate-manifest pins, outside the firewall.

## 4. Outside the firewall: P3 objectives 2 to 4 (no signature; the P3 gate is the operator's)

- **Objective 2** (`how/gates/gate_manifest.py`, gate #9 at :200 and :530). Add a source leg beside the rebuild leg. For every canvas that carries `sync.source_sha256` and a resolvable source, recompute the hash. The line becomes `dual-channel freshness N/N (source · rebuild)`, with each leg counted separately. When the legs disagree, the line prints the disagreement and never averages it. **It does not depend on touch #8**, because it uses only `compute_source_sha256`, which shipped at touch #7. Under this vault's law it can run before the signature. It re-pins the gate line, so it needs a full `--markdown` run to close.
- **Objective 3.** The false-positive / false-negative pair, by derivation: a typo in the source gives source stale and rebuild fresh; a layout-engine change gives source fresh and rebuild stale.
- **Objective 4.** The gate #9 row in `how/gates/AGENTS.md`, covering both legs and what each one cannot see.

## 5. The door (next step, not rendered tonight)

The door is `how/gates/p3_touch_8_signature_<date>`, rendered by `skill_create_iss` from this file. It has four sections: the nine rows · D-1 · D-2 (with the exit-gate dependency) · D-3. Before anyone is asked to rule it, it is **proven at the page** in Chromium and Firefox (F-V-9), with short labels (F-V-14), and `--check-doors` reads it (F-V-5).

It was not rendered in the unattended sitting because the door is a request for a ruling. It should be proven and opened in a sitting where he can rule it. The receiver and port check also belong to that sitting.

## 6. A reviewer seat's findings on this design (dated note, 2026-10-26 01:4x; the text above is unchanged)

A read-only opus seat that did not build read this design beside the objective 2 card (session `session_stanley_20261026_011316_n2_j_p3_obj2`, Automator N2-J). The objective 2 card holds its whole report in §8. It found this design's line numbers correct at `be15ce4`. The four findings below concern this design, and the door rendered from it **must carry them**. None of them moves `canvas_std`, and none is a ruling.

1. **D-2's exit-gate claim is false as written (the seat's #6).** §2 says the Terminal clause *"holds in P3 only if D-2 rules the topology leg advisory"*. Terminal keeps `sha256(source)[:16]` in `sync.sync_hash` (`p1_armor_dogfood.md:52-62`, VERIFIED by this desk). None of their 8 canvases carries `sync.source_sha256` (REPORTED: the seat's grep of their tree, 0 each). So `check-sync`'s source leg cannot run on any of the 8. Under either D-2 ruling, none of them reaches a truthful exit 0 in P3. The clause waits on Terminal's one regeneration after P4. It does not wait on D-2. The door should offer the dated amendment that moves the clause to P4, and should not present D-2 as the lever.
2. **The exit code when only an advisory leg ran is undefined (#7).** Read literally, §1 lets a canvas with no digest and a fresh topology exit 0, although no leg that can fail has run. The fix is one line: exit `2` when **no failable leg** ran, which matches the gate's own rule (obj 2 card, D-O2-3). Exit `2` goes beyond the Exit Gate's *"exits 0/1"*, so the door should name that extension.
3. **The topology leg's blind spot is understated (#8).** The leg compares the canvas with its **own** stored hash. It never sees the source at all, so it misses every source change, a topology change included, and not only "a prose typo, a relabel, a geometry change". Separately, §4's objective 3 line, *"a typo in the source gives source stale and rebuild fresh"*, is false for a typo in a rendered field: a changed label makes both legs stale. Objective 2's card names the narrower case, a YAML comment, and the prose re-reading (its §6).
4. **Row 4 (`README.md`) needs re-cutting (#9).** Line 8 is history ("the v2.4.0 LIP-0010 … axes"); only lines 3, 6 and 37 are live version pins (VERIFIED by this desk, `sed -n`). Lines 9-10 (`142 passed / 10 skipped`, `CERTIFIED 12/12`) and line 30 (`146 passed / 10 skipped`) carry stale counts. Those would then sit under a "current to v2.5.0" banner. The row should name them, measured at build.

**A rider for row 7, routed here from the objective 2 card (#4).** `tests/fixtures/manifest.json:142` calls `adna_canvas_adr_004.canvas` a *"BYTE-COPY of"* the vault's ADR-004 canvas. Today it is the same blob (`8335fe3`): the vault file's bytes as last changed at `93e5638` (2026-09-10), copied into the corpus at `2b3b70a` (2026-10-16). Objective 2's row 5 will regenerate the vault file with a `sync.source_sha256`. After that, the note is a past-tense truth written in the present tense. Row 7 already edits `manifest.json`, so a dated line on that note can ride it. Whether the Canvas row of the corpus should then show Canvas's own practice (the digest) is a corpus question for the same signature.

## 7. Ruled on his morning word (dated note, 2026-10-26 08:18; the text above is unchanged)

His word of 2026-10-26 08:02, recorded by the Automator duty-officer station as RULED row 11112, label verbatim: *"(a) All four: D3 flipped, v2.5.0 tagged on this GO, the touch-8 amendment dated, D-O2-7 stands (Recommended) [P-F-001, P-F-005]"*.

- **§6.1 is ruled: the Terminal exit-gate clause moved to P4**, by a dated amendment (`../campaign_canvas_vernier.md` §P3 exit-gate amendment — 2026-10-26; both missions' Exit Gates edited, struck not deleted). The touch-8 door therefore **carries the amendment as ruled, not as a question**, and D-2 is offered on its own merits only: §2's sentence tying the exit gate to D-2 is history (§6.1), not a door item.
- Nothing else here is ruled. D-1 · D-2 · D-3, the nine rows and the §6.2-§6.4 findings still go to the door, and **touch #8 is unsigned**: `canvas_std` stays at diff 0.
