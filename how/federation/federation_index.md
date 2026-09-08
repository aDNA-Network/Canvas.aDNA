---
type: federation_index
title: "Canvas.aDNA federation index — consumers of the Standard + Canvas's own consumed wrappers"
created: 2026-08-04
updated: 2026-09-08
last_edited_by: agent_mondrian
status: active
standard_version: "2.3.0"
source_census: how/campaigns/campaign_canvas_blueprint/artifacts/p3_federation_census_20260908.md
superseded_census: how/campaigns/campaign_canvas_halftone/missions/artifacts/halftone_federation_census_20260804.md
tags: [federation, index, wrappers, consumers, canvas_standard]
---

# Canvas Federation Index

> **The living registry** (G8 closure, Halftone HF): who consumes the aDNA Canvas Standard, at what pin, in
> what health — plus the wrappers Canvas itself consumes. Born from the dated
> [2026-08-04 census](../campaigns/campaign_canvas_halftone/missions/artifacts/halftone_federation_census_20260804.md);
> **update THIS file** when wrappers change (last-verified column), and re-census only when drift is suspected
> fleet-wide. Contract every consumer conforms to: [`spec_federation_contract.md`](../../what/specs/spec_federation_contract.md)
> (§2.1 required `federation_ref` fields · §3 version policy — **a 1.x→2.x hop REQUIRES 5-stage re-validation** ·
> §4 gates incl. **Amendment 1's visual gate**: `canvas-std validate` + `canvas-visual-check` + agent-confirmed render).

> ## ⛩ Corrected 2026-09-08 against a full re-derivation (Blueprint P3)
>
> Every row below was **re-measured at the object**. This index was wrong **in both directions** — it
> carried a consumer that does not appear (**WGS**, adopted 2026-08-10) and reported an adoption as a
> refusal (**Oration**, adopted 2026-08-04, recorded as *"the G7 enabling condition"* for five weeks).
> Corrections are **struck in place with their dates**, never silently rewritten: an index that is wrong
> in two directions is itself the finding.
>
> ⭐ **Why it drifted, measured rather than guessed (F-P3-8).** `spec_federation_contract` §2.1 specifies
> `version:`. Across 15 vaults the pin is written **six ways** — `version` · `standard_version` ·
> `substrate_pin` (prose) · `builder_version` · `pin` (non-semver label) · `pinned_version` — plus Videos,
> which deliberately keeps pins in `MANIFEST.md` only (the Callisto ruling, **better practice than our own
> §2.1**). ⇒ No refresh of this file can be mechanised against six spellings, so each one required a human
> to read fifteen documents and interpret each; **a human who skips one leaves no trace.** WGS was missed
> for that reason, not from carelessness. The durable fix is to name the canonical field and make this
> table *derivable* — carried to Rosetta as memo #13, not imposed on consumers, since five of the six
> local forms are perfectly reasonable.
>
> ⚠ **This index measures the wrong axis on its own.** It answers *"who holds a wrapper?"* — see the new
> **§1b**, which answers *"who emits canvases with no seam at all?"* Ten vaults were invisible here by
> construction.
>
> Full derivation + commands of record:
> [`p3_federation_census_20260908.md`](../campaigns/campaign_canvas_blueprint/artifacts/p3_federation_census_20260908.md).

## 1. Consumers of the Standard (canvas wrappers, deduped by rename-alias)

| Consumer (aliases) | Wrapper(s) | Pin | Policy | Health — **re-measured 2026-09-08** | Last verified |
|---|---|---|---|---|---|
| **Emacs.aDNA** *(Archimedes)* | `canvas/` | **2.3.0** `adna_native` | minor | ✅ **clean, and re-confirmed the only one**: 6 authored canvases, **0 conformance errors**. The reference wrapper, and the dual-channel existence proof the whole campaign rests on | **2026-09-08 (measured)** |
| **Network.aDNA** *(← aDNANetwork; `LatticeNetwork.aDNA` **does not exist** — measured)* | `canvas/` | **2.2.0** (`standard_version:`) `adna_native` | — | 🟡 pin lag confirmed. ⚠ *"×3 aliases"* was a miscount: `aDNANetwork.aDNA` is a **symlink to this vault**, so there is **one** wrapper, seen three times. Carries **25 C-4** errors | **2026-09-08 (measured)** |
| **GOTFN.aDNA** *(Snorri)* | `canvas/` | `pin: genesis` | minor | 🟢 correct for its stage; nothing rendered yet (their P4 carries the surface contracts) | **2026-09-08 (measured)** |
| **Home.aDNA** *(Hestia)* | `canvas/` | **`builder_version: 1.0.0`** — pins the **substrate library**, not the Standard | minor | 🟠 unchanged; the wrapper itself names the `what/canvasforge/`→`what/canvas/` rename as an open tail. **0 conformance errors** on its 1 authored canvas | **2026-09-08 (measured)** |
| **WebForge.aDNA** *(← Websites, a symlink to this vault)* | `canvas/` | **1.1.0** | minor | 🔴 stale body + old pin **+ 3 dead path refs**, incl. `~/aDNA/node.aDNA/…` — a vault name retired **2026-06-11** | **2026-09-08 (measured)** |
| **ScienceStanley.aDNA** | `canvas_deck/` · `canvas_comic/` | `version: "~1.0"` ×2 | minor | 🟠 M-PL2-reconciled 2026-07-18; comic wrapper still carries an archive-only `context_ref` (**M-PL3 is Canvas-side and still open**). 29 authored canvases, **21 C-4 errors over 5 files**; memo #11 delivered 2026-09-07 | **2026-09-08 (measured)** |
| **ContextCommons.aDNA** | `canvas_deck/` | `version: "~1.0"` | minor | 🔴 worse than recorded: `type: **governance**` (not `federation_wrapper`), titled *"PresentationForge Wrapper"*, **untouched since 2026-04-30**, 2 dead `CanvasForge.aDNA` paths. **0 conformance errors** on its 4 canvases — the wrapper is stale, the output is not | **2026-09-08 (measured)** |
| **Videos.aDNA** *(successor vault, re-genesis Operation Lumière 2026-08-16; predecessor + its `canvas_deck/` wrappers archived → `Archive.aDNA/VideosOld.aDNA`)* | `canvas/` — `stub_pending_execution` (instantiates at their X0+) | — | — | 🟢 seam re-founded: consumes `comic_render` per-panel PNGs **as-is** under `spec_panel_export_contract.md` v1.0 (2026-08-22); timeline/encode/1080×1920 Videos-owned; the old ~1.0 `canvas_deck/` rows retired with the predecessor | 2026-08-22 |
| **WGS.aDNA** *(Berthier)* | `canvas/` | **2.2.0** `adna_native` | minor | 🟡 **one minor behind.** ⛩ **Added 2026-09-08 — this row did not exist.** The wrapper was created **2026-08-10** (mission RS-D, ADR-035; `graft_manifest.yaml` records **zero grafts**) and this index was updated **2026-08-22**, twelve days later, without it. **F-P3-1.** Producer scope is deliberately narrow: one generated artifact family (the EMER binding-surface canvas), regenerated from code, drift-tested at their M-RS-14 | **2026-09-08 (measured)** |
| **Obsidian.aDNA** | `canvasforge/` (dir-rename → `canvas/` flagged post-their-P3) | ~~provisional~~ → **2.0.0** *(measured: `substrate_pin` reads "aDNA Canvas Standard v2.0.0")* | minor | 🟠 **three minors behind** — was recorded as 🟢 "target reconciled". `wrapper_for` **is** canonical (`Canvas.aDNA`), so the *identity* half was right; the **pin** was never verified, only deferred to "their M09". ⛩ **F-P3-9:** the wrapper justifies keeping the directory name on *"the `ZenZachary.aDNA/canvasforge/` sibling precedent"* — **that directory no longer exists** (ZenZachary is at `how/federation/canvas*/`). Their own P3 closed 2026-06-23, so the condition their note set for a rename is met | **2026-09-08 (measured)** |
| **ZenZachary.aDNA** *(Pygmalion)* | `canvas/` · `canvas_comic/` · `canvas_deck/` | `substrate_pin: "CanvasForge.aDNA v1.2"` ×3 | minor | 🔴 stale identity ×3 confirmed — the 2026-08-04 memo **was** delivered (verified at source — no delivery defect, R3 disposed); #12 **staged** at time of writing, delivery recorded in §4. ⭐ Their dir-rename to `canvas*/` is **done**, which is what breaks Obsidian's cited precedent (F-P3-9) | **2026-09-08 (measured)** |
| **Astro.aDNA** *(← SiteForge, a symlink to this vault)* | `canvasforge/` | **1.1.0**, `wrapper_for: **CanvasForge.aDNA**` | minor | 🔴 the most drifted wrapper in the fleet: stale identity **+** stale pin **+** dir-name **+ 3 dead paths** (`CanvasForge.aDNA` ×2, `node.aDNA`). 2026-08-04 memo verified delivered; #12 **staged**, delivery recorded in §4 | **2026-09-08 (measured)** |
| **SuperLeague.aDNA** *(Janus)* | `canvasforge/` | `pinned_version: "genesis-planning"` | per-target | 🔴 stale body + dir-name + 2 dead paths (`lattice-labs` — ⚠ **the shim resolves and the file is gone**, so a shim-health check reports green over a dead ref). **Largest C-4 carrier in the fleet: 204 errors over 13 canvases**, all mechanically clearable; plus 20 invalid `"center"` side values in one file | **2026-09-08 (measured)** |
| **Bearly.aDNA** | `canvas/` (EMPTY) | — | — | 🟢 **wrapper still empty, but the busiest live consumer we have** — consumes `canvas_std.validate` + the H5 `compose_input.py` path read-only via PYTHONPATH (their P5a precedent, zero writes into this vault). Five `comic_page` contracts (17/17) cite our compose invocation of record; bundle 0.1.1 closed the framing-lock gap. Supplied the **F-S030-1** clause (→ dispatch contract **D5**) + the **mode L** venue shape (→ **D6**). Wrapper population still at Bearly's pace — read-only consumption has not needed one | 2026-08-09 |
| **Oration.aDNA** *(Kennedy)* | ~~**NONE**~~ → **`canvas/`** | **2.3.0** `extended` | minor | ⛩ **CORRECTED 2026-09-08 — this row was wrong for five weeks. F-P3-2.** It read *"🔴 the G7 enabling condition — adopt-a-wrapper memo staged"*. Kennedy adopted **on 2026-08-04, the same day the memo was sent** (`version: 2.3.0`, `version_policy: minor`, `conformance_target: extended`, root symlink alongside `git`/`iii`). Their gate is honestly at **2 of 3** — schema ✅, geometry ✅ (2 HIGH accepted at their G4-6), **render deferred** to an operator-present session rather than counted: *"I would rather your gate be accurate than convenient."* ⇒ **G7 should not be booked end-to-end until that lands** — their words, and we should honour them. ✅ current | **2026-09-08 (measured)** |

**Machine-ref compliance:** `federation_ref.source_vault` reads `Canvas.aDNA` in every populated wrapper — zero
broken refs. ⚠ **Re-scoped 2026-09-08:** that sentence was true and load-bearing-in-the-wrong-place. `source_vault`
is machine-clean everywhere, and **11 of 62 `~/aDNA/…` path references in the same wrappers do not resolve** —
including `~/aDNA/node.aDNA/` (Astro · WebForge), a vault name retired 2026-06-11. ⇒ *"Zero broken refs"* was a
statement about **one field**, read as a statement about **the wrapper**. Drift is identity/pin/prose/path-level
**and path-level drift is real** (census §2).

## 1b. Canvas emitters with **no** federation seam — *the population this index could not see*

> ⛩ **New section, 2026-09-08.** Opened by Berthier's 2026-09-07 reply: Operations emits ten canvases, has **no**
> `how/federation/canvas/` wrapper, and no canvas check anywhere in its tree — *"the clean tree is clean by low
> traffic, not by construction."* §1 recorded **Oration** as the last vault in this condition; F-P3-2 shows that
> one closed on 2026-08-04, **and nobody counted the rest.** Being *in* this index meant *"has a wrapper"*, so the
> vaults with the least supervision were exactly the ones it was structurally unable to list.

**10 vaults · 49 authored canvases · zero seam** (template-inherited `what/lattices/examples/` files excluded —
those are the `adr_011` set, 200 files across 47 vaults, governed by Rosetta's migration offer, not by a wrapper):

| Vault | Authored `.canvas` | Conformance (measured, `--level core`) |
|---|---|---|
| **Regenesis.aDNA** | 11 | 🔴 **11/11 FAIL** — 85 errors, **all C-4**, all mechanically clearable |
| **Operations.aDNA** *(Berthier)* | 10 | 🟠 3 FAIL — 19 C-4 + **the fleet's one genuine dangling edge** (ruled `DELETE` 2026-09-07, routes to its author by PR) |
| **LatticeProtocol.aDNA** *(Noether)* | 7 | 🟠 3 FAIL — 76 errors, 72 C-4 |
| **aDNALabs.aDNA** *(Berthier)* | 5 | ✅ 0 errors |
| **Hardware.aDNA** *(Babbage)* | 4 | ✅ 0 errors |
| **LAVentureGraph.aDNA** *(Cartographer)* | 4 | 🔴 **4/4 FAIL — 1175 errors**, a different class entirely: float node coordinates (C-2). **71% of all fleet errors sit in this one vault**, 1161 of them in two files |
| **WilhelmAI.aDNA** *(Hygieia)* | 3 | 🟠 2 FAIL — 4 C-4 |
| **Molecules.aDNA** *(Franklin)* | 2 | 🟠 2/2 FAIL — 19 C-4 |
| **PercySleep.aDNA** *(Hypnos)* | 2 | ✅ 0 errors |
| **RareArchive.aDNA** *(Mnemosyne)* | 1 | ✅ 0 errors |

⚠ **Do not read this table as a to-do list of ten memos.** Five of the ten are already clean, and a wrapper is a
*commitment to gates*, not a badge — pressing one onto a vault that emits four clean diagrams a year would be the
"doctrine without adopters" risk (R6) in reverse. The two that warrant an approach on the evidence are
**Regenesis** (11/11 failing, one mechanical class) and **LAVentureGraph** (a distinct 1175-error class nobody has
ever reported to them). Operations already has the finding, carded their side as `20260907220000`.

## 2. Wrappers Canvas.aDNA consumes

| Wrapper | Source vault (persona) | Pin | Policy | Notes |
|---|---|---|---|---|
| `comfyui/` | ComfyUI.aDNA (Vulcan) | **0.2.0** @ `a8a4356` (2026-08-03) | tracking | Restores the ex-`comfyforge/` consumer seam. **Vulcan follow-up #3 (index the wrapper): SATISFIED by this row.** **#1 CLOSED 2026-08-06 (H4)** — `skills_used`/`workflows_used` now record actual Canvas consumption (ComfyUI = the chain's *refine* stage; generation is the cloud backend's, ADR-003), plus `workflows_requested: comic_panel_refine` and `server_endpoints.override_env`. **#2 pending an operator/Vulcan call** — Canvas recommends leaving the archived LoRA-dispatch runner archived (staged memo `coord_2026_08_06_…_comic_panel_refine_ask.md`). Live consumption: `COMIC_RENDER_COMFY_ENDPOINT` → else the declared `l1_local`. Sibling exemplars: WebForge + ZenZachary `comfyui/` wrappers. |
| `git/` | Git.aDNA (Grace Hopper) | per declaration | — | Git-ops federation (GitHub-public since P6 Wave 2). |
| `iii/` | III.aDNA (Argus Panoptes) | per declaration | — | Quality loop; live learning store `iii/what/context/canvas_iii_learning_store.jsonl` (the `iii` symlink resolves here; `iii_bridge` default repointed 2026-08-04, HR). **Store pin, 2026-09-07 — two objects, do not conflate:** Canvas's **wrapper store** = this file, **6 lines**, md5 `dca90b37757c1fa365a49daaaab18a98`; III's **canonical store** = theirs, **30 entries** (rotated 28→30 at their Noria DP-1), md5 `a28ec2a1815cf3cc08b375a40a23aca3`. Canvas has **no graduation scan** to re-pin today — the canonical hash is recorded so one starts from the right number. **S-4 gate RULED + OPEN 2026-09-07** (Argus: `accepted` = the reviewer's verdict; `spec_rlhf_seam` §6b). |

## 3. Standing drift ledger (non-memo items — fold into consumers' next natural touch)

1. **Home runtime path** (§1) — flagged to Hestia in the refederation wave's courtesy notes; the import should
   land on `Canvas.aDNA/what/production/canvas_core` (post-pt09 home), not the archive shim.
2. **Network trio pin 2.2.0 → 2.3.0** — minor-policy auto-adopt is legal (§3); a one-line pin bump + re-run of
   stage 3 suffices; fold into the next Network session.
3. **ScienceStanley comic `context_ref`** — archive-only target; the resurrect-vs-repoint decision is
   Canvas-side (M-PL3 flag stands).
4. **Obsidian dir-rename** (`canvasforge/` → `canvas/`) — post-their-P3, per their ADR-010 note.
   ⛩ *Updated 2026-09-08:* their P3 **closed 2026-06-23**, so the condition is met; and the cited
   `ZenZachary.aDNA/canvasforge/` precedent **no longer exists** (F-P3-9). Raised to Seshat as an ask, not a
   ledger item — the ruling is theirs (Rule 10).
5. **Rename-alias dedupe** — Astro≡SiteForge · Videos≡VideoForge · Network≡aDNANetwork ~~≡LatticeNetwork~~:
   each refit lands once and the alias copies retire with their shims (Home §C windows).
   ⛩ *Corrected 2026-09-08:* **`LatticeNetwork.aDNA` does not exist** — measured, not assumed. Six root
   aliases are symlinks (`aDNANetwork`→Network · `SiteForge`→Astro · `Websites`→WebForge · `Cmux`→Terminal ·
   `VideoForge`/`VideosOld`→the archive). Counting a symlink as a separate wrapper is what produced the
   phantom *"×3 aliases"* and *"×2 aliases"* columns in the old §1.

### New at P3 (2026-09-08)

6. ⭐ **Six spellings of the pin field** (**F-P3-8**) — the structural cause of this index's drift, and the one
   item here that is **ours, not a consumer's**. `spec_federation_contract` §2.1 says `version:`; the fleet
   writes `version` / `standard_version` / `substrate_pin` / `builder_version` / `pin` / `pinned_version`, and
   Videos correctly indirects to `MANIFEST.md`. Until a canonical field is named, **this table cannot be
   derived and must be hand-read** — which is how a whole consumer went unlisted for four weeks. → memo #13
   (Rosetta), proposing `version:` canonical **with the alternatives explicitly accepted**, since most of the
   local forms are locally right.
7. **11 dead `~/aDNA/…` path refs across 5 wrappers** — `CanvasForge.aDNA` ×4 (archived at pt09) ·
   `node.aDNA` ×2 (**a vault name that has never existed since 2026-06-11**) · `lattice-labs` ×2 ·
   `ZenZachary.aDNA/canvasforge/` ×1. ⚠ The `lattice-labs` pair is the instructive one: **the shim resolves
   and the file underneath is gone**, so any check that stops at the symlink reports green over a dead
   reference.
8. **`spec_federation_contract` §2.1a** *(shipped this session)* — `conformance_target` vs `declared` vs
   `level_reached`, on Kennedy's Finding 1, which had cost Oration a reversed ruling. A document **may**
   self-declare `extended` with a one-key `_reserved` block; the enum in §2.1 was also too short and is
   corrected. Consumers filling in `conformance_target` at re-pin should read it first.

## 4. P3 memo wave — delivery record (2026-09-08)

Each recipient's quiescence was **re-probed at act time**, not trusted from an earlier probe (five other
vaults were being written by concurrent operator sessions during this one). Every memo copied byte-unchanged,
**md5-verified at source and destination**, and **left untracked** — the read-receipt commit is the
recipient's to make. No recipient tree was otherwise modified.

| # | To | Vault | Carries | Status |
|---|---|---|---|---|
| — | Kennedy | Oration | the 34-day-uncollected reply answered; both their findings verified as already-true; §2.1a shipped on their Finding 1; G7 **not** booked end-to-end, per their request | ✅ delivered |
| #12 | Seshat | Obsidian | the dead sibling precedent (F-P3-9) + pin measured at **2.0.0** where we had recorded green. **`ack_required: true`** — one rename ruling | ✅ delivered |
| #12 | Pygmalion | ZenZachary **+** VisualDNA | `wrapper_for: CanvasForge.aDNA` ×3 + the visual-DNA schema pointer aimed at an archive; and F-P3-4 (`skill_lockstep_flip` never built — **our** charter defect, reported because it names their vault) | ✅ delivered ×2 |
| #12 | — | Astro | most drifted wrapper: identity + pin + dir-name + 3 dead paths incl. `node.aDNA` | ✅ delivered |
| #12 | Vitruvius | WebForge | the **identical** dead-path set to Astro's, same edit date ⇒ a common ancestor's error, not two careless vaults | ✅ delivered (their drop-box) |
| #12 | Janus | SuperLeague | 204 of 224 errors clear mechanically; the other 20 need a ruling. Explicitly **not** a tidy-up list for an engagement archiving at W4 | ✅ delivered |
| §1b | Persephone | Regenesis | 11/11 failing, 85 errors, one class, all mechanical. Explicitly **not** a wrapper ask | ✅ delivered |
| §1b | Cartographer | LAVentureGraph | 1175 → **2** by rounding floats — and the 2 survivors are **duplicate node ids** (one of them the empty string) in an entity graph. Never previously contacted | ✅ delivered |
| **#13** | **Rosetta** | aDNA.aDNA | F-P3-8 (six pin spellings) + §2.1a + the template set at **200/47** | ⛔ **STAGED** — their lease was live at act time and they publish no drop-box; the same condition that refused E2 for two days at P2. Re-probe next session. |

⚠ **Two rows in §1 briefly claimed delivery before the act** and were corrected before commit. A record that
runs ahead of the thing it records is the failure mode this whole phase exists to fix.

