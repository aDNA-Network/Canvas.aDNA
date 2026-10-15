---
type: lip
lip_number: "LIP-0011"
title: "Sync semantics — what `sync.sync_hash` hashes, a full source digest, a provenance carrier, and A-8 at `extended` (v2.5.0)"
author: "Stanley Bishop (Mondrian-drafted; Canvas.aDNA standard-bearer)"
status: draft
created: 2026-10-15
updated: 2026-10-15
requires: ["LIP-0010"]
replaces: []
last_edited_by: agent_mondrian
resolution: "DRAFT — awaiting §7.7 signature at the door how/gates/lip_0011_signature_20261015. Instructed by the Vernier P2 verdicts V-1 (b) · V-2 at extended · V-3 sync.generator (how/gates/vernier_p1_exit_20261012.output.json, ruled 2026-10-15, Tier 2). canvas_std is at diff-0 and stays there until signed."
related: ["campaign_canvas_vernier", "mission_vernier_p2b_lip_0011_sync_semantics", "lip_0010_assessment_diagrammatic_context", "spec_roundtrip_protocol_v2", "spec_conformance_suite"]
tags: [lip, standard, canvas, canvas_standard, sync_hash, source_sha256, sync_generator, a6, a8, extended_tier, vernier, p2b, v250]
---

# LIP-0011: Sync semantics — what `sync.sync_hash` hashes

> **Status: draft.** This LIP turns three ruled verdicts into the Standard. The verdicts are not in question
> here; they were ruled 2026-10-15 (`how/gates/vernier_p1_exit_20261012.output.json`). What the signature
> decides is **the shape of the change**, including one sub-question the door deliberately left to this LIP
> (D-1, §3.3) and one file its firewall list missed (row 6, `validate.py`). `what/code/canvas_std/` is at **git-diff 0** and does not move before §7.7.

---

## §0 · What measuring the change found, before a line of it was written

The mission's exit gate says the backward-compatibility claim is a **command that is run**, not a sentence
(F-GL-6: LIP-0010's *"25 of 25 keep passing"* measured 23 of 25). The command is
`python3 how/gates/sync_semantics_census.py`. Its first run changed the draft in four places:

| # | Finding | What it changes |
|---|---|---|
| **F-V-10** | **Canvas ships two "topology" encodings.** `canvas_std.compute_sync_hash` concatenates sorted ids and `from->to` pairs; `canvas_core.CanvasBuilder.compute_sync_hash` hashes `json.dumps({"nodes": …, "edges": …}, sort_keys=True)`. Same topology, **different digest**. The RLHF producers (`variant_board`, `tuning_surface`, `review_canvas`) use the second. Census: **3 Canvas canvases carry the builder encoding**. | Reading (b) — "`sync_hash` is topology" — had a fifth semantic hiding inside it, in our own tree. The Standard must name **one** encoding (§1.1), and CanvasBuilder must delegate to it (§6, ours, outside the firewall). |
| **F-V-11** | **`_reserved.generator` was not Terminal's invention — it was ours.** `canvas_presentation.PresentationBuilder` has written `"generator": "PresentationBuilder"` for months; the fleet holds **61** canvases with a top-level `generator` key, Canvas **16**, LatticeProtocol 2 (copies of our deck), Archive 30, LAVentureGraph 4, Terminal 8, QuantumProteins 1. V-3's *"Terminal invented it (8/8)"* undercounted by 53. | V-3's verdict stands (`sync.generator`) — the evidence for it is stronger, not weaker. The migration table gains a Canvas row. The top-level key stays **legal** (§7.3 unknown-key preservation); this LIP deprecates it, it does not reject it. |
| **F-V-12** | **The door's recommended hard topology check would fail 3 of our own canvases and 0 of anyone else's.** The candidate rule *"`production: generated` ⇒ `sync_hash` equals the recomputed topology"* at `adna_native`: population **20**, match **16**; the 4 non-matches are 2 builder-encoded RLHF fixtures (F-V-10), 1 `canvas_std` test fixture with a hand-set hash, and 1 QuantumProteins canvas that already fails on other grounds. | D-1 below. The check is cheap for the fleet and costs Canvas three regenerations — but it also promotes a **proxy** to a MUST (§3.3), which is the real question. |
| **V-2 price** | **PercySleep's `percy_topology.canvas`** (`extended`, `authority: view`, no `production`) fails when A-8 runs at `extended`. Same canvas, same reason as the committed `axis_tier_census.py` reported to the door. | The mission's *"0 new failures"* exit gate is **not met and cannot be**: the operator ruled V-2 with this one canvas priced on the door. This LIP reports it rather than re-scoping the population to hide it (§5). |

> ⇒ ***A verdict instructs the change; it does not measure it.*** All three verdicts survive the census.
> Two of their premises did not (F-V-10, F-V-11), and one of the door's sub-recommendations is now a real
> choice (F-V-12).

---

## Abstract

`_reserved.sync.sync_hash` has had a validated **shape** (16 hex) and no defined **semantic** since v2.0.0, and
four vaults filled the gap three ways (topology · source-document bytes · master-file bytes). This LIP, per V-1
(b), defines `sync_hash` as the 16-hex topology digest computed by `canvas_std.compute_sync_hash` — the reading
the spec's §8.1 and the round-trip protocol §3.1 already state — and registers **`sync.source_sha256`** (64 hex)
for the source-bytes question. Per V-3 it registers **`sync.generator`** as the provenance carrier. Per V-2 it
runs the A-8 axis check at `extended` as well as `adna_native`. All three are additive; the Standard moves
**v2.4.0 → v2.5.0**.

## Motivation

- **V-1 (F-V-3, Principle 4b at n=4).** Terminal stores `sha256(source markdown)[:16]`; City stores topology
  and a non-standard `source_sha256`; LatticeProtocol's ADR-018 and LinkML Profile v0.1 define the master file's
  bytes; `canvas_std` computes topology. All pass A-6, because A-6 checks only the shape.
  ⇒ *a validated shape with an undefined semantic acquires one meaning per implementer*.
- **V-2.** A-8 runs only at `adna_native`. Terminal's 8 canvases declare `extended`, carry a correct
  `authority: view` + `production: generated` pair, and nothing checks it; an invented value would also pass.
  The axes answer *who owns the meaning · how is it made* — questions about any derived canvas, not an
  aDNA-Native one.
- **V-3.** Provenance (*what made this*) has no registered home, so implementers put it at the top of
  `_reserved` (61 canvases, F-V-11) or, worse, in the `authority` axis (Home's `authority: "generator"`,
  struck from the axis by LIP-0010).

## Specification

### §1 · `sync.sync_hash` — the topology digest (V-1 (b))

1.1. `sync.sync_hash` **MUST** be `canvas_std.compute_sync_hash(S)` where `S` is the authoritative source's
topology. The encoding, stated exactly because F-V-10 proves two can coexist:

```
ids   = sorted(str(node.id) for node in S.nodes)
pairs = sorted(f"{edge.fromNode}->{edge.toNode}" for edge in S.edges)
sync_hash = sha256(("".join(ids) + "".join(pairs)).encode("utf-8")).hexdigest()[:16]
```

1.2. A forward view that preserves the source's node ids and edges (every `canvas_std.to_canvas` output, and
every producer that builds from its own model) therefore satisfies `sync_hash == compute_sync_hash(canvas)`.
That identity is what §3 checks.

1.3. **Known limitation, stated rather than fixed.** The concatenation has no separator, so distinct topologies
can collide (`["ab","c"]` vs `["a","bc"]`), and 16 hex is 64 bits. `sync_hash` is a **staleness detector, not an
integrity proof**. Changing the encoding would invalidate every conformant canvas, which is a major bump and not
this LIP. The integrity question has its own key (§2).

1.4. The `sha256:`-prefixed and source-bytes values in the fleet (Terminal's 8) are **not** topology digests.
They stay A-6-valid in shape and become **stale** by §1.1's definition, which §3 reports as an advisory.

### §2 · `sync.source_sha256` — the full source digest (V-1 (b))

2.1. OPTIONAL. When present it **MUST** match `^[0-9a-f]{64}$`: the SHA-256 of the source document's bytes as
read from disk, no normalisation.

2.2. It answers *"has my source moved?"* for a `view` canvas, and it is third-party verifiable without
`canvas_std`. City and LatticeProtocol already write it (census: 1 + 1, both well-formed).

2.3. The reference implementation gains `canvas_std.roundtrip.compute_source_sha256(path) -> str`.

### §3 · A-6 additions

3.1. `sync.source_sha256`, if present, is checked per §2.1 — **hard**, at `extended` and `adna_native`.

3.2. `sync.generator`, if present, **MUST** be a non-empty string — **hard**, at both tiers.

3.3. **Topology consistency (D-1).** When `production: generated`, the validator recomputes
`compute_sync_hash(canvas)` and compares it to `sync.sync_hash`.
- At `extended`: **advisory** (a warning, not an error). This part is not in question.
- At `adna_native`: **D-1 — the operator chooses.**
  - **D-1 (i), recommended: advisory at both tiers in v2.5.0.** Additive in fact as well as in name. §1.2 holds
    only for views that **preserve** source topology, so a MUST would forbid a generator from ever adding a
    decorative node. That is a design constraint the fleet has not been asked about, and a proxy should not
    become a MUST by default. Hardening is a later LIP, to be considered once the advisory count at
    `adna_native` is 0.
  - **D-1 (ii): hard at `adna_native`**, as the P1-exit door recommended. Fleet cost is 0 external canvases;
    Canvas regenerates 2 artifacts after the F-V-10 fix and corrects 1 test fixture. It is stronger, and it
    pre-commits every future generator to topology-preserving views.

### §4 · `sync.generator` — the provenance carrier (V-3)

4.1. OPTIONAL string: a path relative to the producing vault's root, or a URN, naming what made the canvas
(e.g. `what/canvas/build_canvases.py`, `canvas_presentation.PresentationBuilder`).

4.2. A top-level `_reserved.generator` is **deprecated, not invalid**: §7.3 requires that unknown keys be preserved, and
61 canvases carry it (F-V-11). Tools **SHOULD** write `sync.generator` instead. `authority: "generator"` stays
**invalid** (LIP-0010).

4.3. `sync.generator` does not create a 12th reserved key. `RESERVED_KEYS` stays at 11, and `sync` gains a
property.

### §5 · A-8 at `extended` (V-2)

5.1. When a canvas declares `conformance_level: extended` **and** carries a `metadata.frontmatter._reserved`
block, the validator runs A-8 (`_validate_axes`) on it. The keys stay optional. The rule is unchanged, including
LIP-0010's asymmetric co-requirement.

5.2. No other `_reserved` check moves down a tier. `core` is unchanged, so the 414 template-legacy (count: `axis_tier_census.py`, 2026-10-15)
`authority: view` canvases with undeclared level are untouched (ADR-011's `view` row; `.adna/` is Rule 1).

### §6 · Migration — per implementer, every count from the census below

| Implementer | Carriers (level) | Today | What moves | Owner · when |
|---|---|---|---|---|
| **Terminal** (Vauban) | 8 (`extended`) | 8 pass; `sync_hash` = source bytes (0/8 topology); top-level `generator` 8 | `sync_hash` → topology · source hash → `sync.source_sha256` (full 64) · `generator` → `sync.generator`. **One regeneration**, after P4 by their reply. Until then: 8 advisories, 0 failures. | theirs · after P4 |
| **City** (Ledoux) | 9 (`adna_native`) | 9/9 topology; 1 already writes `source_sha256` | nothing | — |
| **LatticeProtocol** (Noether) | 1 (`adna_native`) + 2 `core` decks | `lattice_core.canvas` already writes topology + `source_sha256` + `sync.generator` | nothing for `gen-canvas`; 2 copied decks inherit our deprecated top-level `generator` (§4.2, legal). Their ADR-018 point 6 + LinkML profile line amend at M-B1, per their reply. | theirs · M-B1 |
| **Home** (Hestia) | 5, all at non-canonical `metadata._reserved` | not read by the validator, before or after | nothing under this LIP. `topology.canvas`'s three problems are V-6's business | theirs · V-6 |
| **Canvas** (us) | 26 `adna_native` · 17 `core` · 4 non-canonical | 25/26 pass (the 1 is the deliberate A-5 negative fixture); of 27 `sync` carriers: 17 canvas_std topology · 3 builder-encoded · 7 hand-set test fixtures | **F-V-10:** `CanvasBuilder.compute_sync_hash` delegates to `canvas_std.compute_sync_hash`, then regenerate the 3 builder-encoded artifacts. **F-V-11:** `PresentationBuilder` writes `sync.generator`. Under D-1 (ii) only: correct `tests/fixtures/adna_axes.canvas`'s hash. | ours · the implementation touch |
| **PercySleep** (Hypnos) | 1 (`extended`) | passes | ⛔ **new failure under §5**: add `production` (`hand_authored` or `generated`, theirs to say). One line. | theirs · memo at P4 |
| **Archive** (Armor, frozen) | 7 (`extended`) | 7 pass | 7 advisories, 0 failures; no migration (SO-7) | — |
| **QuantumProteins** | 1 (`adna_native`) | **already fails** (C-4; `sync_hash: null`) | not a new failure; FYI line in the P4 wave | theirs |

## Backwards Compatibility

**The claim is this command and its output, not this sentence.** Re-run it at signature and again at the firewall
touch, and paste the result; never retype it.

```
python3 how/gates/sync_semantics_census.py      # exit 0 = no new failures · 1 = at least one
```

<!-- census:begin — pasted output; regenerate, never edit -->
```
$ python3 how/gates/sync_semantics_census.py   # exit 1
sync_semantics_census  2026-10-15T23:31Z  /Users/stanley/aDNA/*/**/*.canvas with a _reserved block (non-symlink tops, -P, excl. ['llama.cpp'])
  symlinked tops skipped: 26
      77    of which carry sync
     562  _reserved carriers
     667  files
       4  unparseable
  HEADs: Terminal 4a755a6 · City 6ff4511 · LatticeProtocol da949c8 · Home 4d9498f · Canvas f48fc52
per implementer (_reserved carriers · level · current ok · proposed ok · topology match · source_sha256 · sync.generator · top-level generator · advisories):
  Canvas.aDNA            adna_native  canonical          n=  26 cur=  25 prop=  22 topo=  17 src256=  0 sync.gen=  0 top.gen=  0 adv=  0
  Canvas.aDNA            core         canonical          n=  17 cur=   1 prop=   1 topo=   0 src256=  0 sync.gen=  0 top.gen= 16 adv=  0
  Canvas.aDNA            core         metadata._reserved n=   4 cur=   4 prop=   4 topo=   0 src256=  0 sync.gen=  0 top.gen=  0 adv=  0
  City.aDNA              adna_native  canonical          n=   9 cur=   9 prop=   9 topo=   9 src256=  1 sync.gen=  0 top.gen=  0 adv=  0
  City.aDNA              core         canonical          n=   4 cur=   4 prop=   4 topo=   0 src256=  0 sync.gen=  0 top.gen=  0 adv=  0
  Home.aDNA              core         metadata._reserved n=   5 cur=   5 prop=   5 topo=   0 src256=  0 sync.gen=  0 top.gen=  0 adv=  0
  LatticeProtocol.aDNA   adna_native  canonical          n=   1 cur=   1 prop=   1 topo=   1 src256=  1 sync.gen=  1 top.gen=  0 adv=  0
  LatticeProtocol.aDNA   core         canonical          n=   2 cur=   0 prop=   0 topo=   0 src256=  0 sync.gen=  0 top.gen=  2 adv=  0
  LatticeProtocol.aDNA   core         metadata._reserved n=   4 cur=   4 prop=   4 topo=   0 src256=  0 sync.gen=  0 top.gen=  0 adv=  0
  Terminal.aDNA          extended     canonical          n=   8 cur=   8 prop=   8 topo=   0 src256=  0 sync.gen=  0 top.gen=  8 adv=  8
  other                  adna_native  canonical          n=  25 cur=  24 prop=  24 topo=  23 src256=  0 sync.gen=  0 top.gen=  1 adv=  0
  other                  core         canonical          n= 108 cur=  87 prop=  87 topo=   0 src256=  0 sync.gen=  0 top.gen= 27 adv=  0
  other                  core         metadata._reserved n= 341 cur= 327 prop= 327 topo=   0 src256=  0 sync.gen=  0 top.gen=  0 adv=  0
  other                  extended     canonical          n=   8 cur=   8 prop=   7 topo=   0 src256=  0 sync.gen=  0 top.gen=  7 adv=  7
sync_hash encoding (which digest the stored value actually is):
       3  Canvas.aDNA            CanvasBuilder topology (json)
      17  Canvas.aDNA            canvas_std topology
       7  Canvas.aDNA            neither (source bytes, stale, or hand-set)
       9  City.aDNA              canvas_std topology
       1  LatticeProtocol.aDNA   canvas_std topology
       8  Terminal.aDNA          neither (source bytes, stale, or hand-set)
      23  other                  canvas_std topology
       8  other                  neither (source bytes, stale, or hand-set)
       1  other                  no sync_hash
adna_native · production: generated: 20 · topology match 16 (the HARD leg's whole population)
LIP-0011 ⇒ passers today: 507 · still pass under the proposal: 503 · NEW FAILURES: 4
  ✗ Canvas.aDNA/what/artifacts/b4_board_fixture/board_run_wellformed_20260908.canvas  level=adna_native production='generated' authority=None
      A-6: sync.sync_hash does not match the recomputed topology (production: generated)
  ✗ Canvas.aDNA/what/artifacts/b4_tuning_fixture/tuning_run_wellformed_20260908.canvas  level=adna_native production='generated' authority=None
      A-6: sync.sync_hash does not match the recomputed topology (production: generated)
  ✗ Canvas.aDNA/what/code/canvas_std/tests/fixtures/adna_axes.canvas  level=adna_native production='generated' authority='dual_channel'
      A-6: sync.sync_hash does not match the recomputed topology (production: generated)
  ✗ PercySleep.aDNA/what/presentation/percy_first_glimpse/percy_topology.canvas  level=extended production=None authority='view'
      A-8: 'authority' is present without 'production' — `authority` REQUIRES `production` (LIP-0010 Option D as corrected 2026-09-11). Declaring that anoth
advisories (would warn, not fail): 15
  ~ Archive.aDNA/Armor.aDNA/what/canvas/bastide_system_composition.canvas
  ~ Archive.aDNA/Armor.aDNA/what/canvas/bastide_node_topology.canvas
  ~ Archive.aDNA/Armor.aDNA/what/canvas/bastide_session_lifecycle.canvas
  ~ Archive.aDNA/Armor.aDNA/what/canvas/bastide_ecosystem_seams.canvas
  ~ Archive.aDNA/Armor.aDNA/what/canvas/bastide_port_map.canvas
  ~ Archive.aDNA/Armor.aDNA/what/canvas/bastide_campaign_map.canvas
  ~ Archive.aDNA/Armor.aDNA/what/canvas/bastide_data_flows.canvas
  ~ Terminal.aDNA/what/canvas/bastide_system_composition.canvas
  ~ Terminal.aDNA/what/canvas/bastide_node_topology.canvas
  ~ Terminal.aDNA/what/canvas/bastide_session_lifecycle.canvas
  ~ Terminal.aDNA/what/canvas/bastide_ecosystem_seams.canvas
  ~ Terminal.aDNA/what/canvas/bastide_port_map.canvas
  ~ Terminal.aDNA/what/canvas/bastide_campaign_map.canvas
  ~ Terminal.aDNA/what/canvas/bastide_data_flows.canvas
  ~ Terminal.aDNA/what/canvas/bastide_design_system.canvas
```
<!-- census:end -->

**Reading it.** The census evaluates the **D-1 (ii)** rule set, the strictest on the table, so its `NEW FAILURES`
line is an upper bound:
- Under **D-1 (ii)**, 4 canvases newly fail: 3 are Canvas's own and fixed in the touch, 1 is PercySleep.
- Under **D-1 (i)**, recommended, the 3 Canvas rows become advisories, and the only new failure is
  **PercySleep's, the one the operator ruled V-2 knowing**.
- No canvas outside these two vaults changes verdict under either choice.

## Firewall touch #7 — named file by file, so the signature is informed

The door acknowledged five files (`firewall_and_gos`). Implementing V-2 needs a sixth, plus the tests and
docs that every touch carries. They are named here so that nothing is added under the signature unseen.

| # | File (under `what/code/canvas_std/` unless noted) | Change | On the door's list? |
|---|---|---|---|
| 1 | `src/canvas_std/reserved.py` | A-6: `source_sha256` 64-hex · `sync.generator` non-empty string · topology consistency per D-1; `validate_reserved` returns advisories separately from errors | ✅ |
| 2 | `src/canvas_std/roundtrip.py` | `compute_source_sha256(path)`; `compute_sync_hash` docstring cites §1.1 (no behaviour change) | ✅ |
| 3 | `src/canvas_std/data/adna_canvas_v2.schema.json` | `$defs.reserved.properties.sync.properties` gains `source_sha256` (`pattern ^[0-9a-f]{64}$`) + `generator` (`string, minLength 1`); `x-standard-version` → `2.5.0` | ✅ |
| 4 | `what/specs/spec_adna_canvas_standard.md` §7.2 / §8.1 (+ `spec_roundtrip_protocol_v2` §3.1, `spec_conformance_suite` A-6/A-8 rows) | the definitions above | ✅ (§7.2/§8.1); the two sibling-spec rows are **added here** |
| 5 | `src/canvas_std/__init__.py` | `STANDARD_VERSION = "2.5.0"`; export `compute_source_sha256` | ✅ |
| 6 | `src/canvas_std/validate.py` | at `extended`, when a `_reserved` block is present, run `_validate_axes` (V-2) and the §3 sync checks | ⚠ **not on the door's list — added here.** V-2 cannot be implemented without it. |
| 7 | `tests/` + `tests/fixtures/` + certification corpus | new A-6/A-8-at-extended cases; one Terminal canvas (copied, attribution kept), one City twin, one Canvas native, per the mission | ⚠ implied by the mission, named here |
| 8 | `CHANGELOG` | the v2.5.0 entry | ⚠ named here |

The `RESERVED_KEYS` registry stays at 11 (§4.3). `test_registry_consistency.py` must stay green: that is the F-GL-1
discipline, one definition and consumed.

**Outside the firewall, ours, in the same phase:** `canvas_core/core.py` (F-V-10 delegation) ·
`canvas_presentation/presentation.py` (F-V-11) · regenerating the three builder-encoded artifacts.

## Rationale

- **Why (b) and not (a) or (c)** was ruled at V-1 and is not reopened. The door's priced migrations stand, and
  three of the four asking vaults are aligned on (b) in their own words or code.
- **Why advisory for the topology check (D-1 (i)).** §1.2's identity is true of every generator measured today, but
  only because none adds nodes. A MUST at `adna_native` makes that accident a rule. The cheap, reversible move is
  to report it now and harden it when the measured advisory count is 0. Hardening later is a one-line LIP;
  un-hardening is a breaking change.
- **Why `sync.generator` and not top-level** — V-3: provenance belongs beside `source_name`/`source_version`,
  and it keeps the namespace at 11.

## Reference Implementation

Implemented after the signature, in Vernier P2b objectives 2–3. The census
(`how/gates/sync_semantics_census.py`) already evaluates the candidate rules outside the firewall, reusing
the real `validate`, `_validate_axes` and `compute_sync_hash`.

## Security Considerations

`sync_hash` is 64 bits over an ambiguous encoding (§1.3). No consumer may treat it as tamper evidence;
`source_sha256` is the full digest for that. Neither key carries secrets. Both are derived from content already in
the vault.

## Status

**draft.** Awaiting §7.7 at `how/gates/lip_0011_signature_20261015`. `canvas_std` is at diff-0.

### Ratification (§7.7) — required before any firewall touch

| Field | Value |
|-------|-------|
| Decision | *(unsigned)* LIP-0011 §1–§5 as written; **D-1** = (i) advisory both tiers *or* (ii) hard at `adna_native`; firewall touch #7 = the eight-row table above, including row 6 (`validate.py`), which is not on the P1-exit list; v2.5.0 |
| Ratified by | — |
| Date | — |
| Status | draft |

**What signing does not do.** It does not mandate `source_sha256` or `sync.generator` on any canvas. It does not
migrate anyone's tree; every row of §6 that says *theirs* is a memo, not a write. It does not reopen V-1…V-3.

## Copyright

This LIP is placed in the public domain via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
