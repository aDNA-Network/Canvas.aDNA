---
type: artifact
artifact_id: p2b_conversion_census_20260907
campaign: campaign_canvas_blueprint
phase: P2b
mission: mission_b2b_conversion_offers
title: "P2b conversion census — re-derived, not re-read (Operations + ScienceStanley)"
created: 2026-09-07
updated: 2026-09-07
status: active
last_edited_by: agent_mondrian
tags: [artifact, census, blueprint, p2b, conversion, operations, sciencestanley, c4, toEnd, f_hr_1]
---

# P2b conversion census — re-derived 2026-09-07

> **Method.** Every file located with `find`, classified by reading its JSON, and validated with
> `canvas-std validate <f> --level core` (canvas-std 2.3.0). Nothing in this document is carried
> over from the charter's figures; where the charter and the measurement disagree, the measurement
> is shown **and the charter's number is struck at source**.
>
> **Population statements** (Hopper ADR-011 A8 §5): counts are over `find <vault> -name "*.canvas"`
> in the **working tree** at 2026-09-07, **all classes, no exclusions** — including gitignored and
> untracked files, which is exactly where the interesting half turned out to live.

## 0. The headline correction

| Source | Operations | ScienceStanley |
|---|---|---|
| Charter / STATE (`P2b` scope, 2026-08-22) | ~~"5 standard-blind C08 canvases"~~ | ~~"29 bare files"~~ |
| **Measured 2026-09-07** | **10 files** (two populations) | **33 files** (three classes) |

⛩ **F-P2b-1 — "md5-differ" is a literal measurement; "diverged" is a class claim, and I nearly
shipped the second while holding only the first.** At plan time I measured that all five Operations
C08 diagrams differ by md5 between their two locations and wrote *"divergence, not duplication"* into
the plan. Re-deriving *what* differs shows that framing was wrong in both directions: **two of the
five are byte-different but semantically identical** (serialization only — same nodes, same text,
same geometry, same edges), and the other three diverge in a way far more specific and more useful
than "diverged". Same class as F-P2-8 and its five siblings; the fix is the same one — **re-derive,
don't re-read** — applied this time to a number I had produced myself four hours earlier.

## 1. Operations.aDNA — 10 files, two populations, and only one of them is the source

**Population A — `how/campaigns/C08-LIAISON/artifacts/canvas/` (5 files, git-TRACKED).**

| File | nodes | edges | `--level core` |
|---|---|---|---|
| `c08_claim_lease_flow` | 11 | 9 | `[OK]` → `level_reached=extended` |
| `c08_dispatch_package_anatomy` | 10 | 8 | `[OK]` → `extended` |
| `c08_graph_sync_plane` | 8 | 5 | `[OK]` → `extended` |
| `c08_ledger_memorialization` | 8 | 5 | `[OK]` → `extended` |
| `c08_two_node_topology` | 17 | 8 | `[OK]` → `extended` |

**5/5 clean, zero errors** — which independently reproduces Operations' own claim at authoring time
(`562c2fa`, S97: *"5 canvas teaching diagrams (canvas-std 5/5 zero findings)"*). Their canvases are
good. This census does not find otherwise, and the memo must not imply it does.

**Population B — `what/c08-liaison-package/canvas/` (5 files, GITIGNORED at `.gitignore:33`).**

| File | `--level core` | C-4 | C-3 |
|---|---|---|---|
| `c08_claim_lease_flow` | `[OK]` → `extended` | 0 | 0 |
| `c08_two_node_topology` | `[OK]` → `extended` | 0 | 0 |
| `c08_graph_sync_plane` | **FAIL** | 5 | 0 |
| `c08_ledger_memorialization` | **FAIL** | 5 | 0 |
| `c08_dispatch_package_anatomy` | **FAIL** | 9 | **1** |

### What actually differs — measured node-by-node

Across all five pairs: **zero nodes added or removed, zero node-text differences.** The content is
identical. What differs:

| File | `toEnd` keys (tracked → projected) | geometry-drifted nodes | edges |
|---|---|---|---|
| `c08_claim_lease_flow` | 9/9 → **9/9** | 0 | identical |
| `c08_two_node_topology` | 8/8 → **8/8** | 0 | identical |
| `c08_graph_sync_plane` | 5/5 → **0/5** | 1 | identical |
| `c08_ledger_memorialization` | 5/5 → **0/5** | 2 | identical |
| `c08_dispatch_package_anatomy` | 8/8 → **0/9** | 3 | **+1 edge, dangling** |

⛩ **F-P2b-2 — the projection was opened in Obsidian, and Obsidian's re-save un-conformed it. Canvas
diagnosed this exact mechanism in its own vault on 2026-08-23 and has carried the fix, untouched,
ever since.** The three failing files lost **100% of their explicit `toEnd` keys** (not some — all),
while the two clean files kept 100%. That signature is **F-HR-1**, recorded at HR gate 3/3:
*"Obsidian's re-save dropped the explicit `toEnd` keys — an interaction pass can un-conform a
canvas."* STATE has carried the remedy (`normalize-on-collect`) as open item 4 through P2, P2c and
into this session, described each time as *"a `canvas_context` interaction concern"*.

**It is not only ours.** A second vault has now been bitten by it, in a shipped teaching package, and
neither vault noticed — because the files still *render correctly*. ⇒ The normalizer is not a Canvas
housekeeping nicety; it is the fix that keeps a conformant canvas conformant across a human editing
pass anywhere in the fleet. This census re-prioritizes carried item 4 rather than restating it.

### The one real defect

`c08_dispatch_package_anatomy` (projected copy) carries **C-3: edge `8f003ea92884e7af` toNode
`269b75cbca9331d4` does not resolve to a node.** The 10 node ids in that file do not include the
target. The edge originates at the `expires_at` node (*"the deadline that frees stuck work"*) and
points at nothing — drawn in the editor toward a node that was not kept. The tracked source has 8
edges and no such reference.

⚠ **Do not conflate C-3 with C-4 in the memo.** C-3 is a genuine broken reference. **C-4 is a
strictness rule of the aDNA Canvas Standard, not a rendering bug** — `validate.py:94` requires an
explicit top-level `toEnd` (*v1.0.0 "always include toEnd:arrow"*) where baseline JSON Canvas is
happy to default it. Every C-4 file renders correctly in Obsidian today. Saying otherwise would
overstate the finding, and the offer does not need the exaggeration.

**Conformance ceiling:** all 10 files are **BARE** — no `metadata` key at all, so no `_reserved` on
either the canonical or the legacy path. None reaches `adna_native`; the best any reaches is
`extended`. Unlike the 196 template files (`adr_011`), these are genuinely standard-blind.

## 2. ScienceStanley.aDNA — 33 files, three classes with different owners

| Class | Path | Count | `core` result | `_reserved` |
|---|---|---|---|---|
| **(a)** Site-visual-polish review boards | `how/campaigns/campaign_ss_site_visual_polish/canvases/` | **20** | 15 `[OK]` → `extended` · **5 FAIL** (21 × C-4) | none |
| **(b)** Comic outputs | `how/federation/canvas_comic/` | **9** | **9/9 `[OK]`** → `extended` | none |
| **(c)** Lattice examples | `what/lattices/examples/` | **4** | **4/4 `[OK]`** → `extended` | none |

The five failures in class (a) are `campaign_state_20260428` (5 × C-4),
`character_template_v2_pilot` + `_pregate` + `_pregate_round2` (4 each), `test_canvas_round0` (4).
**Every one is C-4** — the same class as Operations, the same mechanism.

⛩ **F-P2b-3 — 9 of the "bare ScienceStanley files" are Canvas's own output.** Class (b) sits under
the `canvas_comic/` **federation wrapper** and was produced by the `canvas_comic` producer **Canvas
archived at Halftone** (`adr_009`; now `what/production/_archive/canvas_comic/`). Today's
`comic_generator` emits canonical `metadata.frontmatter._reserved` — verified on
`comic_generator/examples/science_stanley_mini_issue.canvas` (keys: `sync`, `adna_version`,
`conformance_level`, `component_types`, `semantic_bindings`, `panel_link`, `context_object`). So
class (b) is bare **because of the producer we retired**, not because of anything SS did. For this
class the honest offer is **regeneration through the current producer**, and the honest framing is
disclosure, not a hygiene report. It also gives the standing federation-index flag its answer path:
SS's `canvas_comic/` wrapper carries an **archive-only `context_ref`**, with the M-PL3
resurrect-vs-repoint decision already marked Canvas-side.

**Class (c) is out of scope by design, and named rather than quietly dropped.** These are the `view`
row (`adr_011`) — visualizations of authoritative `.lattice.yaml`. Canvas's own standing order leaves
`what/lattices/examples/` untouched; extending to SS's copies of the same class would apply a rule to
them we decline to apply to ourselves.

**Charter reconciliation.** *"29 bare files"* ≈ 33 − 4 (class c), so the original figure most likely
already excluded the lattice examples but did not say so, and counted class (b) — Canvas's own
output — as ScienceStanley's problem. Both are population-statement failures, not arithmetic ones.

## 3. Unified picture — one defect class, two vaults

| | files failing `core` | C-4 | C-3 |
|---|---|---|---|
| Operations (projection only) | 3 | 19 | 1 |
| ScienceStanley (class a only) | 5 | 21 | 0 |
| **Total** | **8** | **40** | **1** |

**40 of the 41 errors across both vaults are one class.** That is the shape of the offer: not
"convert your canvases", but *"one mechanical fix clears 40 of 41, one real broken edge needs your
eyes, and we owe you the normalizer that stops it recurring."*

**What conversion to `adna_native` is actually worth here** — stated honestly, because 43 of the 43
files already reach `extended`:

1. **C-3 class defects get caught.** The dangling edge was live in a shipped teaching package and
   invisible to everyone; `--level core` found it in 40ms.
2. **`_reserved` carries identity + provenance** (`sync`, `context_object`, `authority`) so a canvas
   becomes a *context object* an agent can resolve, not just a picture.
3. **Interaction affordances** (`_reserved.interaction`, v2.2.0) turn a review board into a surface
   whose verdicts are machine-collectable — directly relevant to SS class (a), which is 20 boards of
   image variants awaiting human judgement.

## 4. What this census does NOT establish

- **Which Operations copy should win.** The tracked one is evidently the source and the gitignored
  one evidently a projection, but the projection is *ahead* on geometry in 3 files — someone moved
  those nodes deliberately. Whether that layout work is wanted back in the source is Berthier's call,
  not a conclusion this census may take.
- **Whether class (a)'s 20 boards are still live work.** Dated `20260428`; SS may consider the
  campaign closed. The offer is made, not assumed wanted.
- **Any claim about ScienceStanley's or Operations' intent.** Both vaults were read strictly
  read-only (Rule 10); nothing was written, and no wrapper or session file in either tree was opened
  for anything but measurement.
