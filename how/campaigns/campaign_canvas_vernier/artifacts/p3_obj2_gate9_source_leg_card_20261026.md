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
objective: 2
executor_tier: opus
authored_in: session_stanley_20261026_011316_n2_j_p3_obj2 (unattended; Automator Night 2, judgement grant N2-J)
binds: "nothing until a reviewer seat that did not build reads it sound (LIVE FORM, 0.75-0.90 band). It needs no signature: every row is outside the firewall (what/code/canvas_std/ stays at diff 0)"
tags: [vernier, p3, gate_9, dual_channel_freshness, source_leg, f_v_16, card, proposed, blind_spot]
---

# P3 objective 2: gate #9 gains its source leg, and each leg names what it cannot see

The N2-19 sitting held this card at 0.80 R (its surety 5): the law allowed it, but it re-pins the gate line and needs a full run on a machine at 20%. The machine is on AC now. This card is the objective 2 draft that sitting pointed at (obj 1 design §4), re-derived at HEAD `be15ce4` on 2026-10-26 01:1x-01:2x. Every figure below names its probe.

## 1. Finding F-V-16: the source leg as drafted has nothing to read in this vault

The obj 1 design §4 says: *"For every canvas that carries `sync.source_sha256` and a resolvable source, recompute the hash."*

- Neither of this vault's two dual-channel canvases carries `sync.source_sha256`. Both `sync` blocks hold exactly `{source_name, source_version, sync_hash}` (VERIFIED: a parse of `metadata.frontmatter._reserved.sync` in `what/context/context_canvas_surface_legs.canvas` and `what/decisions/adr_004_production_code_layout.canvas`, 01:1x).
- The only canvas in the vault that carries one is a `canvas_std` test fixture, `tests/fixtures/adna_city_twin_shape.canvas` (VERIFIED, grep over every `.canvas`).
- `diagram_generator` cannot write one: `build_diagram(d)` takes a parsed `DiagramInput` and never sees the source path; only the CLI (`__main__.main`) holds it (VERIFIED, read).

So the drafted leg would run over a population of **0**, find nothing stale, and print a green-shaped line. That is this vault's own finding, a third time: *a cross-check that cannot fail looks exactly like a cross-check that passed* (P2b, F-V-9). The card below therefore gives the leg a population before it gives it a verdict.

## 2. The contract: gate #9 with two legs

Pairs are found as today: every `*.diagram.yaml` under the vault (not `.git`, not `_archive`, not a symlink) with its sibling `.canvas`. For each pair, **both legs always run**:

| Leg | Compares | Fresh when | Cannot see |
|---|---|---|---|
| **source** | `canvas_std.compute_source_sha256(<.diagram.yaml>)`, run in the runner env, with the stored `_reserved.sync.source_sha256` | the two are equal | generator drift with the same input (the F-PL-6 shape); and whether a changed byte matters (a comment reads as stale) |
| **rebuild** | the generator re-run into a temp dir, with the view; `sync.source_sha256` removed from both documents before the parsed comparison | the two parsed documents are equal | a source edit that leaves the generated view unchanged (a comment, or a typo outside every rendered field) |

- **A pair whose canvas carries no digest** fails its source leg as `no digest recorded (the source leg cannot run)`. It is never `n/a` and never fresh.
- **Zero pairs found** fails the gate: `no dual-channel pair found; a gate that checks nothing is not green`.
- **The status** is FAIL when any pair is not fresh on both legs. The detail names each such pair with both leg verdicts. Where the legs disagree, it says so in words (`source stale · rebuild fresh` reads "the source moved and the view did not"; `source fresh · rebuild stale` reads "the view moved and the source did not: generator drift, or a hand edit"). Nothing is averaged.
- **The run output** prints one line per leg after the table, every run, green or red. Each line names its count and its blind spot.
- **The pasted gate line** reads `dual-channel freshness **f/n** (source s/n · rebuild r/n)`. `f` counts pairs fresh on both legs. A red gate keeps the existing ` ⛔ FAIL` suffix.

## 3. The rows (all outside the firewall; no signature needed)

| # | File | Change |
|---|---|---|
| 1 | `what/production/diagram_generator/src/diagram_generator/consume.py` | `build_diagram(d, *, source_sha256=None)`. When given, set `_reserved.sync.source_sha256`. Without it the output is byte-identical to today, so every existing caller and test is unchanged |
| 2 | `what/production/diagram_generator/src/diagram_generator/__main__.py` | The CLI passes `canvas_std.compute_source_sha256(<input>)`. That is the Standard's one definition (touch #7), not a second copy |
| 3 | `what/production/diagram_generator/tests/test_cli_source_digest.py` (new) | The CLI's digest equals `compute_source_sha256(input)`. The stamped canvas validates at `adna_native`. The digest is the only difference from `build_diagram` without it. A comment-only source edit moves the digest and nothing else |
| 4 | `how/gates/gate_manifest.py` | Gate #9 as in §2. The leg logic moves into helpers that take a pair list, so the probe in §5 runs it over planted pairs and never over the vault. A new flag, `--probe-freshness` (runs no suites). `PRODUCER_EXPECT["diagram_generator"]` re-pinned to the **measured** figure, derived in the comment as house practice requires |
| 5 | `what/context/context_canvas_surface_legs.canvas` · `what/decisions/adr_004_production_code_layout.canvas` | Regenerated with the gate's own build command. Both are byte-equal to a rebuild at HEAD today (VERIFIED, `cmp`, 01:2x), so the diff should be exactly the one added key per file. That is checked, not assumed |

**Left at diff 0:** everything under `what/code/canvas_std/` (the firewall; touch #8 is unsigned) · every spec · every door · `how/gates/AGENTS.md` (objective 4's row).

⚠ **Side effect, named for the touch-8 door.** The fixture `canvas_std/tests/fixtures/adna_canvas_adr_004.canvas` is the same git blob as the vault's ADR-004 canvas today (`8335fe3`, VERIFIED, `git rev-parse`), and `manifest.json` calls it a *"BYTE-COPY of"* that file. After row 5 it is a byte-copy of the 2026-10-16 file, not of today's. No `canvas_std` test reads a vault path (VERIFIED, grep), so nothing breaks. But the note becomes a past-tense truth written in the present tense, and the Canvas row of the corpus no longer shows Canvas's own practice. A dated line on that note can ride touch #8 row 7, which already edits `manifest.json`. That rider is the door's to carry and his to sign. This card does not touch it.

## 4. Decisions this card takes (each reversible by `git revert`; the seat reviews them)

- **D-O2-1. Where the digest is written:** the producer's CLI (rec). Rejected: a sidecar ledger in `how/gates/`. That would be a second, non-Standard home for a value the Standard placed in `sync.source_sha256` (V-1 (b), LIP-0011 §2), invented by the standard-bearer in its own vault.
- **D-O2-2. The rebuild leg masks `sync.source_sha256`** (rec). Without the mask, every source byte change also fails the rebuild leg for a stamped pair. "Source stale · rebuild fresh" could then never be observed, and the exit gate's *"the two legs can disagree"* would be false by construction.
- **D-O2-3. No digest means FAIL, not n/a** (rec). A leg that cannot run is not a leg that passed.
- **D-O2-4. The source leg is not a pre-filter** (binding). The mission title says "pre-filter". A literal pre-filter (skip the rebuild when the source is fresh) would reopen exactly F-PL-6, which was generator drift under unchanged sources. Both legs run every time.
- **D-O2-5. The pasted line keeps the mission's own form** `(source s/n · rebuild r/n)` (rec). The blind-spot prose goes on the run's per-leg lines, not into the pasted STATE line. The inner `·` repeats the line's own separator, and nothing in the vault parses the line but the manifest itself (VERIFIED, grep over `*.py`).
- **D-O2-6. `sync.generator` is not stamped now** (rec). No leg reads it, and it is one more field to defend. It is a later card if a consumer asks.

## 5. Tests

- **The producer (row 3):** pytest, inside the `diagram_generator` gate. HEAD measured **53/0** before any edit (VERIFIED, `pytest -q`, 01:2x). The new pin is the measured tree figure, and the delta must reconcile with the new file's cases.
- **The gate (row 4), `--probe-freshness`:** planted pairs in a temp dir, seeded from a real `.diagram.yaml` and the generator's own stamped build. Expected verdicts (source, rebuild):

  | Case | Expected | Proves |
  |---|---|---|
  | clean copy | fresh · fresh | the legs read fresh when fresh |
  | a comment appended to the source | **stale** · fresh | the source leg sees what the rebuild cannot (disagreement printed) |
  | one node's `x` moved in the view | fresh · **stale** | the rebuild leg sees what the source cannot (the F-PL-6 signature; a real layout-engine change is objective 3's derivation) |
  | the digest removed from the view | cannot run · fresh | D-O2-3 |
  | a label changed in the source | stale · stale | the legs agree when both see it |
  | no pairs at all | gate FAIL | zero population is not green |

  Exit 0 only when every planted verdict matches. A probe that cannot fail is the defect this card exists to remove, so the probe is checked both ways: one deliberately wrong expectation must make it exit 1.
- **The vault:** gate #9 alone after row 5 must read source 2/2 · rebuild 2/2. Then the full `gate_manifest.py --markdown` runs, and its line is pasted, never retyped. That is a measurement, not a phase-gate claim. **The P3 gate stays his.** Its exit test cannot read met tonight anyway: `check-sync` needs touch #8.

## 6. Overlap and order

Objective 3's first half (a typo outside the rendered fields: source stale, rebuild fresh) is the probe's second case. Its second half (a real layout-engine change) is only analogued here, by a view-side edit. Objective 3 keeps the true derivation. Objective 4 (the `how/gates/AGENTS.md` row) waits for this to land.

## 7. Surety (LIVE FORM)

- Card and start objective 2 as drafted. Predicted *accept* · 0.85 · R. This is in the 0.75 to 0.90 band, so it acts only on a sound verdict from a seat that did not build.
  `surety: {"dp": "canvas.p3_obj2.card", "predicted": "accept, built as carded", "confidence": 0.85, "keys": [], "class": "R"}`
- Regenerate the ADR-004 canvas (the fixture note goes past-tense; the rider is his, at the touch-8 door). Predicted *accept* · 0.85 · R. This rides the same seat.
  `surety: {"dp": "canvas.p3_obj2.regen_adr_004", "predicted": "accept; rider to touch 8 row 7", "confidence": 0.85, "keys": [], "class": "R"}`

## 8. The reviewer seat's verdict

*(To be filled from the seat's own report. Not pre-filled.)*
