---
type: artifact
artifact_kind: card
created: 2026-10-26
updated: 2026-10-26
status: built   # 2026-10-26 08:2x, rows 1-5 in one commit after the second seat's SOUND; was: proposed
last_edited_by: agent_mondrian
campaign: campaign_canvas_vernier
phase: P3
mission: mission_vernier_p3_freshness_both_ways
objective: 2
executor_tier: opus
authored_in: session_stanley_20261026_011316_n2_j_p3_obj2 (unattended; Automator Night 2, judgement grant N2-J)
seat_verdict: "UNSOUND, 2026-10-26T01:44-07:00. One read-only opus seat that did not build; 1 blocking finding (text-only), 8 non-blocking. The text it read is commit f4c6b32"
revision: "Revised after the seat (5c018ce). The seat's findings are applied as text in §2-§6 and recorded in §8. ~~NOT re-reviewed: build only after a fresh seat reads this revision sound~~ Re-reviewed 2026-10-26 08:24 by a fresh seat at f817de9: SOUND, 6 non-blocking, applied as text and recorded in §9"
seat_verdict_2: "SOUND, 2026-10-26T08:24-07:00. A fresh read-only opus seat that did not build; 0 blocking, 6 non-blocking. The text it read is commit f817de9"
rulings: "D-O2-7 RULED 2026-10-26, stands as recommended (his morning word 08:02, Automator RULED row 11112). The rest of the card is still proposed and needs a fresh seat before any row is built"
binds: "nothing. No signature is needed: every row is outside the firewall (what/code/canvas_std/ stays at diff 0). ~~Nothing here is built~~ Built 2026-10-26 (rows 1-5, one commit; session_stanley_20261026_081247_m3_morning_word)"
tags: [vernier, p3, gate_9, dual_channel_freshness, source_leg, f_v_16, card, proposed, blind_spot, seat_unsound]
---

# P3 objective 2: gate #9 gains its source leg, and each leg names what it cannot see

> ✅ **2026-10-26 08:24: a fresh seat read the revision (at `f817de9`) SOUND** (0 blocking, 6 non-blocking; §9). Its findings are applied as text before the build.
>
> ⛔ **The reviewer seat read the first version of this card UNSOUND** (2026-10-26 01:44; the text it read is `f4c6b32`). Its one blocking finding: neither leg reads the prose channel, and the card never said so. Under the brief of this sitting, objective 2 stops at this card. The findings are applied below as text. **This revision has not been re-reviewed.** The next sitting seats a fresh reviewer over it before any row is built.

The N2-19 sitting held this card at 0.80 R (its surety 5): the law allowed it, but it re-pins the gate line and needs a full run on a machine at 20%. It is the objective 2 draft that sitting pointed at (obj 1 design §4), re-derived at HEAD `be15ce4` on 2026-10-26 01:1x-01:2x. Every figure below names its probe.

## 1. Finding F-V-16: the source leg as drafted has nothing to read in this vault

The obj 1 design §4 says: *"For every canvas that carries `sync.source_sha256` and a resolvable source, recompute the hash."*

- Neither of this vault's two dual-channel canvases carries `sync.source_sha256`. Both `sync` blocks hold exactly `{source_name, source_version, sync_hash}` (VERIFIED: a parse of `metadata.frontmatter._reserved.sync`, 01:1x; re-derived by the seat).
- The only canvas in the vault that carries one is a `canvas_std` test fixture, `tests/fixtures/adna_city_twin_shape.canvas`, which is not a pair (VERIFIED, grep over every `.canvas`).
- `diagram_generator` cannot write one: `build_diagram(d)` takes a parsed `DiagramInput`, which has no path field; only the CLI (`__main__.main`) holds the path (VERIFIED, read; re-derived by the seat).

So the drafted leg would run over a population of **0**, find nothing stale, and print a green-shaped line. That is this vault's own finding, a third time: *a cross-check that cannot fail looks exactly like a cross-check that passed* (P2b, F-V-9). The leg needs a population before it can have a verdict.

## 2. The contract: gate #9 with two legs

**What the legs read, stated first (the seat's blocking finding).** A dual-channel pair has three files: the prose `.md`, the structure `.diagram.yaml`, and the generated `.canvas`. Both legs read **only the `.diagram.yaml` and the `.canvas`**. Neither reads the prose. The producer uses the prose path only for its file stem, as a wikilink (`consume.py:140-143`, VERIFIED). So an edit to `adr_004_production_code_layout.md` reads fresh on both legs. In this vault, "source hash" first meant a hash of the *prose* (Armor's and Terminal's sources are markdown documents, `p1_armor_dogfood.md:118`). A line reading "source 2/2" would therefore read as prose coverage, which the campaign forbids (*"must not let a cheap pre-filter read as coverage"*, `campaign_canvas_vernier.md:120`). Prose-to-structure drift stays what it was: a gate-review obligation (`skill_canvas_context_diagram` §4, REQ-O05).

Pairs are found as today: every `*.diagram.yaml` under the vault (not `.git`, not `_archive`, not a symlink) with its sibling `.canvas`. **Both legs run on every pair, every time:**

| Leg | Compares | Role | Fresh when | Cannot see |
|---|---|---|---|---|
| **yaml source** | `canvas_std.compute_source_sha256(<.diagram.yaml>)`, run as a subprocess under the runner `PYTHON`, with the stored `_reserved.sync.source_sha256` | the cheap pre-filter, and the one a third party can run without the generator | the two are equal | the prose channel; generator drift with the same input (F-PL-6); whether a changed byte matters (a YAML comment reads as stale) |
| **rebuild** | the generator re-run into a temp dir, with the view; `sync.source_sha256` removed from both documents before the parsed comparison | the authority | the two parsed documents are equal | the prose channel; a source edit that leaves the generated view unchanged (a comment, or a typo outside every rendered field) |

**Population.** `n` counts pairs with a canvas beside the yaml. An **orphan** (a yaml with no canvas) is listed and fails the gate, and is not counted in `n`, as today. **Zero pairs** fails the gate: *a gate that checks nothing is not green*.

**Cannot run.** A leg that cannot run on a pair fails that pair, and is reported as `cannot run`, never as fresh or stale. That covers no digest recorded, a digest recompute that fails (the subprocess errs, or the source is unreadable), and a rebuild that fails. This vault cannot import `canvas_std` in the gate's own process: the documented `python3` is homebrew 3.14.6, and `canvas_std` lives in the anaconda 3.12 runner env (VERIFIED, 01:2x). The digest is therefore computed in a subprocess, by the Standard's one function, never by a hashlib line here (F-V-13).

**The verdict (D-O2-7).** A pair passes when its **rebuild** (the authority) reads fresh and its source leg ran. A stale digest beside a fresh rebuild is the pre-filter's own false positive (P1: *"stale when the canvas is fine"*). It is printed on every run with the pair named, and it does not fail the gate. Two legs *disagree* only when both ran and differ. A disagreement is never averaged into the headline.

**What prints.**
- The run prints one line per leg after the table on every run, green or red. Each line names its count, its role and its blind spot, and ends `prose channel: neither leg reads it`.
- The pasted gate line names its population on its face: `dual-channel freshness **f/n** (yaml source s/n · rebuild r/n; prose unread)`. Here `f` counts passing pairs, and `s` and `r` count the pairs on which that leg **read fresh** (a leg that could not run is not fresh, and is counted apart on the always-printed lines; second seat #3). A red gate keeps the existing ` ⛔ FAIL` suffix. This departs from the Exit Gate's literal `(source · rebuild)` only by stating what "source" is; the door or the next seat may rule the shorter form instead.

## 3. The rows (all outside the firewall; no signature needed)

| # | File | Change |
|---|---|---|
| 1 | `what/production/diagram_generator/src/diagram_generator/consume.py` | `build_diagram(d, *, source_sha256=None)`. When given, set `_reserved.sync.source_sha256`. Without it the output is byte-identical to today, so every existing caller and test is unchanged |
| 2 | `what/production/diagram_generator/src/diagram_generator/__main__.py` | The CLI passes `canvas_std.compute_source_sha256(<input>)`, the Standard's one definition (touch #7), not a second copy |
| 3 | `what/production/diagram_generator/tests/test_cli_source_digest.py` (new) | The CLI's digest equals `compute_source_sha256(input)`. The stamped canvas validates at `adna_native`. The digest is the only difference from `build_diagram` without it. A comment-only source edit moves the digest and nothing else |
| 4 | `how/gates/gate_manifest.py` | Gate #9 as in §2. The leg logic moves into helpers that take a pair list, so the probe in §5 runs it over planted pairs and never over the vault. A new flag, `--probe-freshness` (runs no suites). `PRODUCER_EXPECT["diagram_generator"]` re-pinned to the **measured** figure, derived in the comment as house practice requires. The reporter is rewritten with it (`markdown_gate_line`'s gate #9 branch, which today prints `checked - meta["stale"]`, and the `meta` the scorer fills): a pair stale on the source and fresh on the rebuild must not raise the stale count (second seat #4) |
| 5 | `what/context/context_canvas_surface_legs.canvas` · `what/decisions/adr_004_production_code_layout.canvas` | Regenerated with the gate's own build command. Both are byte-equal to a rebuild at HEAD today (VERIFIED, `cmp`, 01:2x), so the diff should be exactly the one added key per file. That is checked, not assumed, on the **parsed** documents; a text diff shows two lines per file, because the preceding `sync` key gains a comma (second seat #6) |

**Rows 2, 4 and 5 land in one commit** (seat #3), with rows 1 and 3. Split, gate #9 reads red in between: a stamped rebuild against an unstamped view, or a two-leg gate over unstamped canvases.

**The building sitting's `scope_declared` must name** `what/production/diagram_generator/**` and both vault canvases before its first write (seat #5).

**Left at diff 0:** everything under `what/code/canvas_std/` (the firewall; touch #8 is unsigned) · every spec · every door · `how/gates/AGENTS.md` (objective 4's row).

⚠ **Side effect, routed to the touch-8 door (seat #4).** The fixture `canvas_std/tests/fixtures/adna_canvas_adr_004.canvas` is the same git blob as the vault's ADR-004 canvas today (`8335fe3`, VERIFIED). `manifest.json:142` calls it a *"BYTE-COPY of"* that file. Its bytes are the vault file's as last changed at `93e5638` (2026-09-10), copied into the corpus at `2b3b70a` (2026-10-16) (VERIFIED, `git log`). After row 5 the note becomes a past-tense truth written in the present tense, and the Canvas row of the corpus no longer shows Canvas's own practice. No `canvas_std` test reads a vault path (VERIFIED, grep), so nothing breaks. A dated line on that note belongs to touch #8 row 7, which already edits `manifest.json`. This sitting routes the rider there by a dated note on the obj 1 design. The rider stays the door's to carry and his to sign.

## 4. Decisions this card takes (each reversible by `git revert`; the next seat reviews them)

- **D-O2-1. Where the digest is written:** the producer's CLI (rec). Rejected: a sidecar ledger in `how/gates/`. That would be a second, non-Standard home for a value the Standard placed in `sync.source_sha256` (V-1 (b), LIP-0011 §2).
- **D-O2-2. The rebuild leg masks `sync.source_sha256`** (rec). Without the mask, every source byte change also fails the rebuild leg for a stamped pair. "Source stale · rebuild fresh" could then never be observed.
- **D-O2-3. No digest means `cannot run`, which fails the pair** (rec). A leg that cannot run is not a leg that passed.
- **D-O2-4. Both legs run every time.** This follows from the Exit Gate's *"the two legs can disagree"*, so the earlier version's word "binding" is withdrawn (seat #2). The mission title says "pre-filter". A literal pre-filter (skip the rebuild when the source is fresh) would reopen exactly F-PL-6, which was generator drift under unchanged sources.
- **D-O2-5 (revised). The pasted line states its population** (rec), in the form given in §2. The inner `·` repeats the line's own separator. Nothing parses the line but the manifest itself (VERIFIED, grep over `*.py`; the seat widened it to `py/sh/js/json/yaml` in Canvas and Automator).
- **D-O2-6. `sync.generator` is not stamped now** (rec). No leg reads it. It is a later card if a consumer asks.
- **D-O2-8 (new, the second seat's #2, taken by the builder). A source leg that disagrees with the rebuild's own stamp cannot run.** Under D-O2-7 a broken recompute that always reads stale could never turn the gate red. So the leg's recompute is also compared with the `sync.source_sha256` the rebuild just stamped (the same function on the same bytes, in the runner env). If they differ, the leg is a tool fault: `cannot run`, which fails the pair. This is not the strict alternative: a truly stale digest beside a fresh rebuild still passes, printed.
- **D-O2-7 (new, seat #2). The verdict follows the authority** (rec): see §2. P1 records the plan-gate ruling as *"source hash as a cheap pre-filter, rebuild-compare as the authority"* (`p1_armor_dogfood.md:122`). The first version failed the gate on any stale leg, which gave the pre-filter a veto. **The strict alternative** (a stale digest beside a fresh rebuild also fails) is defensible, because a stale digest is a false claim that every third-party checker reads. It is one predicate in row 4. ~~The choice is the next seat's to confirm and his to overrule.~~ ⛩ **RULED 2026-10-26: D-O2-7 stands, as recommended** (his morning word, 08:02, Automator RULED row 11112, label verbatim: *"(a) All four: D3 flipped, v2.5.0 tagged on this GO, the touch-8 amendment dated, D-O2-7 stands (Recommended) [P-F-001, P-F-005]"*). **The verdict follows the rebuild, the authority**, and that is the rebuild leg's authority for the building sitting; the strict alternative is not taken. The next seat reviews the card's other text, not this choice. *(Struck text kept, not deleted.)*

## 5. Tests

- **The producer (row 3):** pytest, inside the `diagram_generator` gate. HEAD measured **53/0** before any edit (VERIFIED, `pytest -q`, 01:2x). The new pin is the measured tree figure, and the delta must reconcile with the new file's cases.
- **The gate (row 4), `--probe-freshness`:** planted pairs in a temp dir, seeded from a real `.diagram.yaml` and the generator's own stamped build. The **control is in the probe's code**: one case carries a deliberately wrong expectation, and the probe must report it as a mismatch on every run (seat #5). **The probe exits 0 if and only if every real case matched its expectation and scored as expected, and the control mismatched; otherwise it exits 1** (restored from the first version; second seat #1). Each case shows its two leg verdicts and the gate's score for that pair alone, and checks the words of its report (the detail when red, the always-printed leg lines when green):

  | Case | Legs (source · rebuild) | Gate | Proves |
  |---|---|---|---|
  | clean copy | fresh · fresh | OK | fresh reads fresh |
  | a YAML comment appended | **stale** · fresh | OK, the disagreement printed | the pre-filter's false positive is shown and does not fail (D-O2-7) |
  | one node's `x` moved in the view | fresh · **stale** | FAIL, "the legs disagree" | the rebuild sees what the source cannot |
  | the digest removed from the view | cannot run · fresh | FAIL, "cannot run" | D-O2-3 |
  | a label changed in the source | stale · stale | FAIL | the legs agree when both see it |
  | an orphan yaml (no canvas) | n/a | FAIL, listed | the population rule |
  | a yaml that will not build | stale or fresh · cannot run | FAIL, "cannot run" | a failed rebuild is not a fresh one |
  | an unreadable source | cannot run · cannot run | FAIL | a failed recompute is not a match |
  | the control (wrong expectation) | n/a | reported as a mismatch | the probe can fail |
  | no pairs at all | n/a | FAIL | zero population is not green |

  *Feasibility (not a test of record):* a scratch draft of rows 1 to 4 ran the first five cases, the control and the zero case on 2026-10-26 01:28-01:43, read-only against the vault: every verdict was as expected, and the control failed when it had to. Over the real pairs, before any regeneration, it read `source 0/2 · rebuild 2/2 ⛔ FAIL`, which is D-O2-3 on live data. The draft is not committed; the building sitting writes the rows from this card.
- **The vault baseline:** gate #9 reads **2/2** today in the committed manifest's own line. That is three full `gate_manifest.py --markdown` runs at HEAD `be15ce4`, 01:30, 01:41 and 01:43, identical, ALL GATES GREEN (seat #5: it is not only a scratch script's reading). After row 5, gate #9 alone must read `yaml source 2/2 · rebuild 2/2`. Then the full `--markdown` run is **pasted in the building sitting's session record and its STATE banner**, as a measurement. **No phase-gate claim:** the P3 gate is his. Its exit test cannot read met in P3 in any case. `check-sync` needs touch #8. ~~and the Exit Gate's *"Terminal's 8 pass from outside their tree"* waits on Terminal's one regeneration after P4: none of their 8 carries `sync.source_sha256` (seat #6; REPORTED, the seat's grep of their tree).~~ *(Struck 2026-10-26, not deleted: that clause moved to P4's Exit Gate on his word, RULED row 11112; second seat #5.)*

## 6. Overlap and order

- **Objective 3's "prose typo" is a re-reading here, and it is named, not slipped in** (seat #1). The mission's pair, *"a prose typo → source stale, rebuild fresh"*, came from Armor and Terminal, where the markdown **is** the source. For Canvas's pairs the source is the `.diagram.yaml`. A typo in the prose `.md` reads **fresh on both legs**: that is the blind spot of both, stated in §2. So objective 3 derives "source stale · rebuild fresh" with a YAML comment, and says that the prose case is a third blind spot, not the first half of the pair.
- Objective 3's second half (a real layout-engine change) is only analogued here, by a view-side edit. Objective 3 keeps the true derivation. A scratch trial showed it is derivable: a view built with the layout gaps +1 differs from the real build (`cmp`, 01:38).
- Objective 4 (the `how/gates/AGENTS.md` row) waits for this card to land.

## 7. Surety (LIVE FORM)

- *(First version, superseded.)* Card and start objective 2 as drafted. Predicted *accept* · 0.85 · R, in the 0.75 to 0.90 band, so it could act only on a sound verdict. **The seat read it UNSOUND, so it did not act.**
  `surety: {"dp": "canvas.p3_obj2.card", "predicted": "accept, built as carded", "confidence": 0.85, "keys": [], "class": "R"}`
- This revision, carded `proposed` with the seat's findings, nothing built (the brief's own branch). Predicted *accept* · 0.92 · S. Reversal: `git revert` the revision commit; the first version stays at `f4c6b32`.
  `surety: {"dp": "canvas.p3_obj2.card_revised_proposed", "predicted": "accept; re-seat before build", "confidence": 0.92, "keys": [], "class": "S"}`
- D-O2-7, the verdict follows the authority. Predicted *accept* · 0.80 · R. It is not acted on: the card is not built. Next seat.
  `surety: {"dp": "canvas.p3_obj2.d_o2_7", "predicted": "accept the authority reading over the strict one", "confidence": 0.8, "keys": [], "class": "R"}`
  ⛩ **Outcome 2026-10-26: ruled as predicted** (his word, RULED row 11112, "D-O2-7 stands (Recommended)"). Recorded in §4 by `session_stanley_20261026_081247_m3_morning_word`.
- *(2026-10-26, the building sitting.)* Build rows 1-5 in one commit, on the second seat's SOUND verdict, with its six findings applied as text first. Predicted *accept* · 0.85 · R: the 0.75 to 0.90 band, acting on a seat that did not build. Reversal: `git revert` the build commit (it is one commit by rule; the two canvases return to their unstamped bytes with it).
  `surety: {"dp": "canvas.p3_obj2.build", "predicted": "accept, built as carded after the second seat", "confidence": 0.85, "keys": [], "class": "R"}`
- *(Same sitting.)* D-O2-8, the tool-fault check, taken from the second seat's offer. Predicted *accept* · 0.85 · R, same seat. Reversal: one predicate in row 4, reverted with the build.
  `surety: {"dp": "canvas.p3_obj2.d_o2_8", "predicted": "accept the tool-fault check", "confidence": 0.85, "keys": [], "class": "R"}`

## 8. The reviewer seat's verdict (from its own report, 2026-10-26 01:44)

**VERDICT: UNSOUND.** One read-only opus seat that did not build; 75 tool uses, 19.8 min, nothing written. *"The card is unsound as written because of one blocking gap (finding 1), and the fix is text-only."*

What it re-derived and found holding (VERIFIED by the seat):
- F-V-16;
- `build_diagram` never sees the source path;
- the ADR-004 fixture is one blob with the vault canvas (`8335fe3`);
- no `canvas_std` test reads a vault path;
- nothing parses the gate line but the manifest;
- every row is outside the firewall, with no Standard text, door or ratification;
- D-O2-1, 2, 3, 5 and 6 are right;
- after row 5 each leg has a population of 2 and can go red alone;
- the probe can fail;
- obj 1's line numbers are correct at `be15ce4`.

| # | Class | On | Finding (abridged) | Disposition here |
|---|---|---|---|---|
| 1 | **BLOCKING** | obj 2 | Neither leg reads the prose channel, and the card never says so. "Source" first meant the prose in this vault, so the line would read as prose coverage, against `campaign_canvas_vernier.md:120` and the mission's "state the population on the face of the number". §6 re-read objective 3's "prose typo" without flagging it | §2 states it first, §2's leg lines print it, the pasted line names the population, and §6 names the re-reading |
| 2 | non-blocking | obj 2 | "FAIL if either leg is stale" gives the source leg a veto against "rebuild-compare as the authority". Make it D-O2-7. D-O2-4 is not "binding" | D-O2-7 added (rec: the authority), "binding" withdrawn |
| 3 | non-blocking | obj 2 | The source leg runs as a subprocess under the runner `PYTHON`. A failed recompute reads cannot-run, which is a FAIL. Define `n`, orphans and rebuild failures. Rows 2, 4 and 5 land in one commit | §2 *Population* and *Cannot run*; §3 one commit |
| 4 | non-blocking | obj 2 | The fixture rider is named but not routed to obj 1 row 7. "The 2026-10-16 file" is imprecise | §3 corrected (`93e5638`, copied at `2b3b70a`); routed by a dated note on the obj 1 design |
| 5 | non-blocking | obj 2 | The scope omits the producer and the canvases. Put the wrong-expectation control in the probe's code. Add orphan, rebuild-failure and unreadable cases. The 2/2 baseline came from scratch. Say where the line is pasted | §3 scope line; §5 table and baseline |
| 6 | non-blocking (blocks the door) | obj 1 | D-2's exit-gate dependency is false. None of Terminal's 8 carries `sync.source_sha256`, so check-sync's source leg cannot run on any of them under either D-2 ruling. The clause waits on Terminal's regeneration after P4. Mission line 54 and STATE line 22 repeat the claim | obj 1 design dated note; mission and STATE struck and corrected, not deleted |
| 7 | non-blocking | obj 1 vs obj 2 | The exit code is undefined when only an advisory leg ran; read literally, a canvas with no digest and a fresh topology exits 0, against D-O2-3 and obj 1's own line 35. Exit 2 exceeds the Exit Gate's "0/1"; the door should name it | obj 1 design dated note |
| 8 | non-blocking | obj 1 | The topology leg compares the canvas with its own stored hash, so it misses every source change, topology included. Obj 1 line 64 is false for a rendered-field typo | obj 1 design dated note |
| 9 | non-blocking | obj 1 | README line 8 is history; only lines 3, 6 and 37 are live pins. Stale counts at 9-10 (142/10, 12/12) and 30 (146/10) would sit under "current to v2.5.0". The door must carry the rider from #4 | obj 1 design dated note (VERIFIED by this desk, `sed -n`) |

The seat's closing line: *"Must change before building: say the source leg reads the `.diagram.yaml` and print 'prose channel: neither leg reads it' on both leg lines (blocking); also flag the objective-3 re-reading, add D-O2-7, specify the subprocess and the cannot-run/orphan/one-commit handling, route the rider into obj1 row 7, and amend the session scope."* Each of these is applied in the text above. **Applying a finding is not the same as a seat reading it sound.**

## 9. The second reviewer seat's verdict (from its own report, 2026-10-26 08:24)

**VERDICT: SOUND.** A fresh read-only opus seat that did not build (`session_stanley_20261026_081247_m3_morning_word`, under N2-J); 26 tool uses, about 4.8 min, nothing written. It read this card at `f817de9` (the revision `5c018ce` plus his D-O2-7 ruling), with D-O2-7 not put to it. *"The text resolves the earlier blocking finding and implements D-O2-7 consistently. Rows 1 to 5 can be built against the code at HEAD."*

Re-derived and holding (VERIFIED by the seat, by reading): the blocking finding resolved (§2's "what the legs read", both blind spots, both printed lines); every row buildable (`build_diagram` has no path, the CLI holds it, `compute_source_sha256` is exported, gate #9's `rglob` and `PYTHON -m` rebuild, `PYTHON -c` subprocesses are the manifest's own way, the new test lands in an existing gated surface); the D-O2-2 mask correct and sufficient (`sync_hash` is topology only, the digest the only byte-dependent field, A-6 accepts 64 hex); all ten probe cases score as D-O2-7 predicts (zero pairs is a real change: today's code reads OK at 0); no other gate moves (the ADR-004 fixture is a separate path sharing a blob, no test reads the vault canvases, the advisory unchanged); one commit sufficient.

| # | Class | Finding (abridged) | Disposition |
|---|---|---|---|
| 1 | non-blocking | The probe's exit-0 rule was dropped in the revision; a probe could exit 0 with a real case wrong | §5 restored: exit 0 iff every real case matched and scored, and the control mismatched |
| 2 | non-blocking | Under D-O2-7 a broken recompute that always reads stale can never turn the gate red; offered: compare the recompute with the digest the rebuild stamped, as a tool-fault check | taken by the builder as **D-O2-8** (§4) |
| 3 | non-blocking | `s` and `r` undefined on the pasted line | §2: both count legs that read fresh |
| 4 | non-blocking | Row 4 must rewrite the reporter (`checked - stale`) and `meta`, or a source-stale pair undercounts the headline | row 4 names it |
| 5 | non-blocking | §5 still gave the Terminal clause as a reason; it moved to P4 | struck, not deleted |
| 6 | non-blocking | Row 5's "one key" holds parsed, not as text (a comma); the mask hides a CLI that stops stamping, which row 3 covers | row 5 says parsed; row 3 unchanged |

Not checked by the seat (it would have had to run something): row 5's `cmp` byte-equality claim and the homebrew/anaconda claim. Both are re-measured by the building sitting.
