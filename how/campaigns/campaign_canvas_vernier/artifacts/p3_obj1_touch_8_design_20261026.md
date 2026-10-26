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
