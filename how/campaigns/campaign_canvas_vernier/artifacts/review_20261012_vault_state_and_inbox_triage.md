---
type: artifact
artifact_id: review_20261012_vault_state_and_inbox_triage
campaign_id: campaign_canvas_vernier
title: "Review 2026-10-12 — the vault after 24 idle days: state re-derived, 17 memos triaged, and the Standard's next version being designed in other vaults' ADRs while ours sat at a gate"
created: 2026-10-12
updated: 2026-10-12
status: complete
last_edited_by: agent_mondrian
session: session_stanley_20261012_vernier_review_and_inbox
executor_tier: opus
tags: [review, aar, vernier, inbox, sync_hash, state, governance, standard_v240, memorialisation, ailedger]
---

# Review 2026-10-12 — vault state, inbox triage, findings

> **Every figure below was re-derived this session**, read-only, before it was written here. Where a
> figure in STATE.md or the Vernier charter disagreed with the re-derivation, the re-derivation wins and
> the disagreement is recorded (git HEAD > cached read > memory > assumption).

## 0. One paragraph

HEAD was `483bc61` (2026-09-18) for **24 days**. In that window the Standard's first external consumer
was **archived under the campaign** (Armor.aDNA → `Archive.aDNA/`, 2026-09-24; live successor
`Terminal.aDNA/what/canvas/`, now **8** canvases, regenerated the morning of this review), **17 inbound
memos** arrived and sat untracked (the inbox's own rule says an uncommitted memo is an unread one),
**four of them asked the same question** Vernier's P1 had already found (V-1: what `sync_hash` hashes)
and LatticeProtocol **carded `gen-canvas` on our answer** while its own ADR-018 and the LinkML Profile
v0.1 defined the field for us. Four operator doors were pending for 26 days with the receiver down.
Nothing is red: ten gates green, firewall diff 0, re-derivation of the dogfood reproduces exactly. The
exposure was never a failing check — it was an **unwatched front door** and an **unruled gate**.

## 1. State review — re-derived

| Surface | Claimed (STATE/charter, 2026-09-17) | Re-derived 2026-10-12 | Δ |
|---|---|---|---|
| Gate set | 10 green | **10 green, exit 0** — `canvas_std` 170/10 · certification 12/12 · `canvas_core` 1039/4 · `canvas_presentation` 57/2 · `canvas_context` 58 · producers 275/7 · `comic_render` 154/2 · firewall 0 · census 11/11 · freshness 2/2 | none (`canvas_core` 1039/4 is the Obsidian-closed split, F-DT-5) |
| Vernier subject | `Armor.aDNA`, 7 canvases, no git repo, absent from router | **`Terminal.aDNA/what/canvas/`** @ `319b770`, **8** canvases (+`bastide_design_system`, b03); Armor archived 2026-09-24, its history *was* Terminal's (74/75 files byte-identical to `346f9cb`); shim `~/aDNA/Armor.aDNA` retires on our ack (window ≈2026-10-24) | subject moved; "no git repo" dissolved; "absent from router" was true of the staging dir and is moot |
| P1 table | 7/7 canonical · 7/7 A-8 · 7/7 source-hash · 0/7 topology · 7/7 native-flip | **8/8 · 8/8 · 8/8 · 0/8 · 8/8**, `generator` key 8/8, declared-tier `[OK]` 8/8; **Terminal tree untouched** (`git status -uall` 0) | reproduces, one row larger |
| Unpushed | "a fresh batch GO is owed" | **2** (`4931819`, `483bc61`) + this session's | GO owed |
| Doors | 4 pending | **4 `.pending`, 0 `.output.json`**, sentinels dated 09-16; receiver **DOWN** at open; **restarted this session → `:8767`** (`/health` body names our root); the four doors **re-rendered** because the port moved (the `round_trip.js` 8765 trap) | port drift found and fixed |
| Memo #20 → Rosetta | staged, moves with `adr_011` | still staged; `adr_011` still unsigned | unchanged |
| `CLAUDE.md` *Current state* | — | names **Armature (2026-06-23)**; nine campaigns since | stale, fixed this session |
| `STATE.md` | — | **79 KB / ~11.9K words**, six closed-campaign banners in the top block, `updated: 2026-09-16` | Rule 7 bloat → P6 compaction |
| Datum findings | "11, F-DT-1…F-DT-11" | **F-DT-10 is never defined** (one dangling forward reference in the 09-15 session file) | record ≠ count → P6 |
| `canvas_context/__init__.py:48` | — | declares **`2.2.0`** against Standard 2.4.0 | pin drift → P6 |
| LIP hygiene | queue empty | `lip_draft_canvas_as_primitive` + `lip_draft_derived_surface_metadata` still `submitted` (superseded by LIP-0009/0008); `lip_queue_disposition` still `active`; D3 registrar ack still `#needs-human` | → P6 |
| Session filing | — | 17 September sessions filed; `history/2026-10/` did not exist (no October session until this one) | fine |
| Home `topology.canvas` (Berthier's FYI) | — | **confirmed**: `_reserved` at `metadata._reserved` (non-canonical), `authority: "generator"`, no `production` | V-3 second instance; owner Hestia |
| AILedger ↔ Canvas | — | no `how/federation/canvas/` wrapper; Canvas is **lab-estate** (ADR-027), not in the genesis unification map (ADR-008); AILedger already an **indirect consumer** (4 lite-paper figure twins via Design's `--canvas-twin`, Folio dossier pointers into `deck_generator` + `lattice_presentation_canvas.lattice.yaml`); finding **F-S078-04** (`TB` direction token raises in our loader) never reached us | → P5 |

## 2. Inbox triage — 17 memos, one table

Classes: **R** receipt only · **A** ack + act now · **D** ruling at the door (`vernier_p1_exit_20261012`) · **M** mission.

| # | Memo | From | Asks | Class | Owed | Deadline state |
|---|---|---|---|---|---|---|
| 1 | 09-21 `socials_repin_v240` (parent dir) | Stentor · Socials | binds `iii_quality_contract`? social formats today? C2PA allocation | **D** V-8 + **M** P7 | #25 | pre-SG-4 (re-asked 10-06) |
| 2 | 07-20 `comic_panel_in_vault` | SS | none — informational | **R** | answered 08-22 (`in_reply_to`) | — |
| 3 | 08-28 `ack_rosetta_googleai_migration` | SS | none — closing ack | **R** | — | — |
| 4 | 09-10 `seven_lamps` | SS (Berthier-edited) | review III request-trajectory contract vs shared generation; self-described **undelivered** | **M** P6 | review in P6 | "before G1; not a blocker" |
| 5 | 09-24 `dual_mode_schema_packs_and_the_graph_canvas_standard` | Berthier · Automator (Boulogne) | ① B14 pack as T2 item ② B18 overlay placement ③ `_reserved` grandfathering; FYI Home `topology.canvas` | **D** V-4/V-5/V-6 | #24 | "on your clock"; defaults name us *counterparty, not consenting* |
| 6 | 09-24 `armor_archived_shim_for_vernier` | Hestia · Home | ack + repoint `subject_vault` → shim retires | **A** | #26 + repoint **done** (§C) | shim ≈2026-10-24 |
| 7 | 09-24 `the_clause_is_in` | Rosetta · aDNA | none — closes our #19 | **R** | — | — |
| 8 | 09-25 `gate_sentinels_adr_017` | Hestia · Home | none — 4 sentinels on census; Home ADR-017 hygiene | **R** (operator item) | — | — |
| 9 | 09-26 `graph_canvas_overlay_viewer` | Ledoux · City | 1a `source_sha256` admissible? 1b which hash? 1c `generated` (self-ruled) · 2 floorplan read · 3 layout hints · 4 where B14 lives | **D** V-1/V-4/V-5 | #23 | before City ⛩ G-DESIGN |
| 10 | 09-26 `canvas_twin_and_sync_hash` | Vauban · Terminal | ack proposal: move to `compute_sync_hash(doc)`, source hash → `source_version`; `adnaterm` as 2nd viewer; twin waits on `gen-canvas` | **D** V-1 | #21 | none stated; LP waits on same |
| 11 | 10-03 `m10_canvas_gatehouse_count_only` | Ledoux · City | none — Canvas drawn sealed (`data_bearing: unruled`), 4-pending beacon | **R** → **M** P6 (`data_bearing` ruling) | — | — |
| 12 | 10-03 `profile_v0_1` | Noether · LP | add `CanvasAnnotation` keys same release or wait for P3 ADR? (default: wait) | **R** (default accepted) | in #22 | — |
| 13 | 10-06 `rlhf_seam_and_style_ref` | Stentor · Socials | (1) social formats today? (2) `style_ref` by reference (3) read-only ADR-005 rows | **D** V-8 + **M** P7 | #25 | (1) blocks SG-4 |
| 14 | 10-07 `canvas_lattice_dispositions` | Noether · LP | confirm/amend/decline 4 rows: our 2 lattice files + example = not-a-lattice → "Canvas format"; 16 elsewhere-owned files → ours? home? | **D** V-7 | #22 | **overdue** (before P3; P3 opened 10-10) |
| 15 | 10-08 `canvas_condition_cel_migration` | Noether · LP | confirm/amend/decline 4 CEL rewrites | **D** V-7 | #22 | **overdue** (same) |
| 16 | 10-10 `interim_notice_p3_open` | Noether · LP | none — repeats 10-08 ack | **R** | — | — |
| 17 | 10-12 `sync_hash_alignment` | Noether · LP | **Q1** what goes in `sync_hash` on a LinkML-generated twin (master bytes vs topology) **Q2** standard full-digest key? | **D** V-1 | #22 | **`gen-canvas` M-B1 carded on the answer** |

**Drawn once:** memos 5 · 9 · 10 · 17 are **one decision with four waiters** — the `sync_hash` semantic
(V-1) plus a full-digest key (Noether Q2 = City's `source_sha256` = Terminal's "source hash somewhere").
Memos 14 + 15 are **one decision with one waiter** whose deadline has passed. Memos 1 + 13 are one
producer question (V-8) whose honest answer is measurable and is *"not yet"*.

### Measurements the replies rest on (re-derived this session)

- **`compute_sync_hash`** (`canvas_std/roundtrip.py:30-37`) hashes sorted node ids + sorted
  `fromNode->toNode` pairs, 16 hex. **A-6** (`reserved.py:186-188`) checks 16 hex **only**. The spec
  lists `sync: {sync_hash, source_name, source_version}` and never says what is hashed. Terminal: 8/8
  source-hash, 0/8 topology. City: topology + a non-standard `source_sha256`. LP ADR-018 + Profile v0.1:
  master-file bytes. ⇒ **three readings, all passing.**
- **Our two lattice files** (`what/lattices/lattice_{comic,presentation}_canvas.lattice.yaml`): consumers
  = `what/production/tests/test_federation_validation.py` + an **archived** smoke test + **AILedger
  Folio's dossier pointer** (`ailedger_design_wt/.../folio_context_dossier.md:197-200`). No runtime
  executes them. They are **documentation of producer pipelines**. The Canvas Standard has **no home**
  for workflow descriptions — it describes canvases, not the pipelines that make them.
- **`post_generator`** (`model.py`): `PLATFORM_PROFILES` = advisory `char_budget` + `aspect` hints
  (twitter/x 16:9 · linkedin 1.91:1 · instagram 1:1), permissive default; **no pixel envelopes, no
  carousel / quote-card / thumbnail formats, no `style_ref`**. Socials' question (1) answers *"not yet"*.
- **`spec_rlhf_seam.md` §6b**: `accepted` = reviewer's verdict; Canvas owns capture, III owns the
  store schema. Read-only access to Canvas-side capture sidecars under a consumer's own namespace is
  within Canvas's gift; access to the III store is Argus's.

## 3. Findings — F-V-1 … F-V-6

Form: worked / didn't / finding / change / follow-up.

**F-V-1 — The inbox was a registry with no consumer, for three weeks.**
Worked: the drop-box convention (`open_unilaterally`, 2026-09-04) — six vaults used it correctly and left
their memos untracked as asked. Didn't: nothing on our side *consumed* it; "we commit it on receipt" is a
promise with no instrument behind it, and the vault was idle. Finding: ***the drop-box inverted the
F-P3-6 failure (an uncollected reply in THEIR outbox) into its mirror (an unread memo in OUR inbox) — the
channel moved, the exposure did not.*** Change: receipt commit `9ea73ca`, byte-unchanged. Follow-up: **gate
#11 `inbox_receipt`** (P6) — an untracked file under `who/coordination/inbox/` older than N days is a ⛔
on the gate line, so the manifest fails on an unread memo the way it fails on an omitted suite.

**F-V-2 — The subject vault was archived under the campaign, and the charter still names it.**
Worked: Hestia's memo said exactly what to do and left the shim for us. Didn't: the charter's
`subject_vault` and STATE's banner named `Armor.aDNA` for 18 days after it ceased to exist as a live
graph. Finding: ***a campaign pinned to a vault name is a claim about the fleet, and the fleet moves
while the campaign waits at a gate*** — the sibling of F-PL-2 (*a memo is a measurement with a
timestamp*) applied to a charter. Change: subject repointed to `Terminal.aDNA/what/canvas/` with
`Archive.aDNA/Armor.aDNA` as the frozen P1 measurement; Hestia acked (#26) so the shim can retire.
Follow-up: charters pin `subject_vault` with a `superseded when:` clause like memo `pins:` do.

**F-V-3 — The Standard's next version was being designed in other vaults' ADRs while ours sat at a gate.**
Worked: every peer built *against* v2.4.0 and told us — LP ADR-018, Profile v0.1, City's
`make_canvas_twin.py`, Terminal's `build_canvases.py`, Boulogne B14/B18. Didn't: V-1 waited 25 days for
a human gate, and in that time three implementations chose three semantics. Finding: ***a validated shape
with an undefined semantic acquires one meaning per implementer, and the number of implementers is now
the fleet*** (Vernier Principle 4b, measured at n=4). Change: the P1-exit door is rendered today with
the migration priced per option; the interim acks say which option Canvas recommends and that it is a
recommendation, not a signature. Follow-up: LIP-0011 (P2b) — the fix is additive and lands as v2.5.0.

**F-V-4 — The governance surfaces that orient a cold start were the stalest things in the vault.**
Worked: STATE's banner block is exhaustive. Didn't: `CLAUDE.md` *Current state* named a campaign nine
closes old; STATE was 79 KB with six closed banners in its top block; Datum's AAR counts eleven findings
and defines ten. Finding: ***the orientation surface rots fastest because every close appends to it and
none restructures it — Rule 7 for the workspace router, re-found inside a vault.*** Change: `CLAUDE.md`
paragraph rewritten today; STATE gets a dated banner today and a **compaction** in P6 (archive →
`how/state_archive_20261012.md`). Follow-up: F-DT-10 defined or struck with its reason (P6).

**F-V-5 — The receiver's port moved, and four live doors pointed at the old one.**
Worked: the 09-16 wrapper note *"read the sidecar; never hardcode the port"* and the recorded
`round_trip.js` 8765 trap. Didn't: the receiver was down at open; when restarted it landed on **8767**
(Home's receiver, which had held 8767, is no longer running), so all four rendered doors carried
`data-receiver-url=…:8768` — a verdict POSTed through them would have gone nowhere. Finding: ***a door is
rendered against a port, and a port is a lease, not an address.*** Change: receiver restarted, `/health`
body verified to name our root, four doors re-rendered (html only — sentinels untouched, their age is
data). Follow-up: P6 adds a `--check-doors` to the manifest that compares every `.html`'s receiver URL
to the sidecar.

**F-V-6 — Memorialisation stopped being a deferred idea and nobody told the deferral.**
Worked: Lodestar's C-iii deferral stated its reason — *"zero consumer pressure"* — which is exactly what
makes it re-evaluable. Didn't: five live instances now exist (Bastide dual-memorialised · City's
LinkML→canvas twin · LP `gen-canvas` · Boulogne B14/B18 · AILedger lite-paper figure twins + the C08
ledger-memorialization canvas) and no Canvas record reopened the item. Finding: ***a deferral with a
stated unblock condition is a trigger someone has to evaluate, and nobody did*** (the LIP-0010 lesson,
one level up). Change: P5 chartered — `context_canvas_memorialisation.md`, the pattern proposal, the
AILedger offer memo, Canvas's own `graph.canvas`. Follow-up: Lodestar C-iii row updated to point at P5.

## 4. What this review does NOT do

- It rules nothing. V-1…V-8 and the firewall are at `how/gates/vernier_p1_exit_20261012` (§7.7 — agents
  author, operators ratify; rule at the door, not in chat).
- It touches no firewalled file (`what/code/canvas_std/` diff 0 at close).
- It writes into no peer vault except untracked memo drops into declared inboxes, md5-verified.
- It does not compact STATE — today adds a dated banner; P6 restructures.

## Reproduce

```bash
cd ~/aDNA/Canvas.aDNA && python3 how/gates/gate_manifest.py --markdown          # 10 gates
# Terminal re-derivation (read-only; prints 8 rows source=True topology=False, native flip OK ×8)
python3 - <<'PY'
import json,glob,hashlib,os,sys,copy
sys.path.insert(0,'what/code/canvas_std/src')
from canvas_std.roundtrip import compute_sync_hash; from canvas_std import validate
T=os.path.expanduser('~/aDNA/Terminal.aDNA')
for f in sorted(glob.glob(T+'/what/canvas/*.canvas')):
    d=json.load(open(f)); r=d['metadata']['frontmatter']['_reserved']
    src=hashlib.sha256(open(os.path.join(T,r['sync']['source_name']),'rb').read()).hexdigest()[:16]
    dd=copy.deepcopy(d); dd['metadata']['frontmatter']['_reserved']['conformance_level']='adna_native'
    print(os.path.basename(f), r['sync']['sync_hash']==src, r['sync']['sync_hash']==compute_sync_hash(d), bool(validate(dd,level='adna_native')))
PY
git status --short -uall | grep inbox | wc -l   # 0 after the receipt commit
```
