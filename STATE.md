---
type: state
created: 2026-06-06
updated: 2026-09-09
status: active
last_edited_by: agent_mondrian
last_session: session_stanley_20260909_blueprint_p5_close
tags: [state, governance, canvas, blueprint_closed, p5_close, campaign_close, canvas_emission, comfyui_seam, gate_manifest, m_pl3, imagen_wiring, ss_conform, p3_repin_wave, federation_index, wrapper_census, pin_field_spellings, conformance_target, p2b_conversion_offers, conform, f_hr_1, rlhf_s4_gate, argus, p2c_producer_regate, layout_fit, trap_profiles, advisory_traps, p2_authoring_rail, dogfood, dual_channel, diagrammatic_context, licensing, adr_012, adr_024, publication_boundary, federation, standard]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

> **▶ 2026-09-09 — 🏁 OPERATION BLUEPRINT COMPLETE · the campaign that set out to fix a federation problem and found an epistemic one · three memos delivered, one of them freed after a day staged (Mondrian, `session_stanley_20260909_blueprint_p5_close`).** Cold start found **an untracked inbound memo from Vulcan** — caught by the `-uall` rule, and it had been delivered to `who/coordination/` rather than the drop-box, so a collapsed listing would have shown that directory unchanged. **(A) THE SEAM HAS TWO HALVES, AND WE MEASURED THEIRS.** ComfyUI's `emit_run_manifest.py` v0.1.0 shipped 2026-09-09 — **keyed to their M-RD1 until our five P4 fixtures made it venue-independent, whereupon their operator ruled it forward and it shipped the same sitting.** *The plan's claim that building the consumer first turns §3 from a paragraph into fixtures an emitter can run against was load-bearing, not rhetorical.* Their memo reports 12/12; we **re-derived it rather than repeated it** (it is a claim about *our* code) and got **15/15** — their twelve plus three they did not run: the committed record is byte-identical to the live manifest, **every path resolved and every PNG was genuinely probed** (20 × real `(1024,1024)`, zero zero-dims — that check exists because P4 shipped traps that *skipped while printing `0 findings [OK]`*), and on-disk md5 == recorded md5 all 20. Their tree `-uall` **0 entries** after every run. ⛩ **F-P5-1 — a manifest is only loadable where its pixels are:** their *committed* copy raises `ManifestError` (25 skipped) from where it sits, and the copy that loads lives under a gitignored `.local_dataplane/`. ⇒ **the version-controlled half of the seam's evidence cannot be re-derived by anyone who does not already hold the gitignored pixels.** Not a defect — `partially_failed.json`'s contract behaving exactly right, and our own `adr_010` makes the identical trade. Raised as an observation for their v1.0 provenance story; **no spec change proposed.** **(B) THE SS DEBT DISCHARGED — and their figures reproduced exactly**, which is worth saying because ours have not always: **20 canvases / 5 failing / 21 errors / all C-4**, exactly as the charter said. All five → `extended [OK]`; `unresolved_edges` ran and found **0**; their tree read-only throughout. ⛩ **F-P5-2 — the first version of that handover was 1436 changed lines.** `normalize_edges` works on a parsed document and is exactly as mechanical as we told them; **the serialization is not.** `json.dumps(indent=2)` is correct JSON and reformats every line of a file written compact and one-node-per-line — and *they land it under their own commit*, so a reviewer would have had to take *"only `toEnd` changed"* on our word from a diff showing everything change. Rewritten as a textual insertion: **42 lines**, tabs/key-order/spacing/missing-trailing-newline preserved, and every output **parsed and asserted equal to `normalize_edges`'s own result** because clever text surgery on JSON breaks quietly. ⇒ ***a mechanical fix delivered as a whole-file rewrite is not mechanical as far as the person reviewing it is concerned.*** **(C) BOTH CARRIED TAILS RE-DERIVED, NEITHER EXECUTED ON ITS OLD PREMISE.** ⛩ The **`ImagenWiring`** tail was false in **both** clauses — *"no live caller"* (it is imported and instantiated at `comic_render/dispatch.py:18,77` and is a public export) and *"uses only `generate_variants`"* (it uses two methods). The **real dead surface is larger than claimed**: the whole selection-surface cluster, **10 methods, zero call sites**, one of them already fenced by a test asserting no module may reference it. Two name collisions recorded so nobody re-derives them. Carried to backlog **with the measurement attached** — deprecating a live public export on close day without a fleet consumer sweep is a change dressed as housekeeping. **M-PL3: dossier STAGED, not ruled** — the charter said *"ruling"*, SS asked for a joint sitting and was right to; corpus measured at the object (**14 files, ~2619 lines**), four options with costs, **none recommended**. The strongest fact recorded both ways: Halftone shipped a working comic system *without* this corpus, which is either redundancy or unclaimed knowledge, and asserting which without an overlap audit would repeat F-P2b-3. **(D) ⛩ F-P5-3 — THE CLOSE RAN `canvas_context` AND FOUND IT RED FOR TWO DAYS.** The leg-2 proof. Cause entirely benign: **P2c legitimately regenerated** `document_generator`'s whitepaper — section-atomic pagination split it **5 pages → 6** — taking it 32/23/8 → **35/25/9** and staling four literals pinned since Salon. **It survived three consecutive phase closes (P2b · P3 · P4), each publishing an all-green gate line, none of them lying:** `canvas_context` was in the gate set at Armature and **silently dropped out**; no commit removed it, each close copied the previous close's list. ⇒ **F-P2-11's family with a nastier variant — a skipped test prints `s`; a suite nobody invoked prints nothing at all.** Repaired so it cannot rot the same way: structural counts **derived from the file** (asserting the loader is *lossless*, which is the real claim), `reading_order` kept literal because that one **is** the leg-2 claim. `idea_runnable_gate_manifest` filed: the fix is a manifest that **fails on omission**. **(E) THREE MEMOS DELIVERED**, md5-verified, left untracked, quiescence re-probed at act time — **and #13 finally went**, one day after P3 staged it on Rosetta's live lease. ⭐ **A staged memo is not a refused one, and the re-probe is what makes that true** — both refusal conditions in this campaign (a live lease, no drop-box) are **transient**. ⚠ #15's own `delivery_basis` was **corrected before sending**: it still described the live SS lease that had by then been released — a memo whose header contradicts the act that delivered it is P3's index failure one layer in. **Gates: `canvas_std` 115/10 · certification 11/11 · `canvas_core` 1035/3 · `canvas_context` 58 (restored) · producers 267/7 packages · `comic_render` 154/2 · firewall diff 0 (verified from the vault root — a persisted `cd` makes that check return empty, i.e. indistinguishable from clean).** ⛔ **H4 live chain still not asked and spend never requested** — by both vaults' agreement, the ask is joint when their M-RD1 venue manifest lands. ▶ **No active campaign. No successor chartered** (operator ruling).

> **▶ STANDARD PINS + OPEN TAIL (live).** Canvas Standard **v2.3.0** · `canvas_std` **115/10** · certification **11/11** · firewall clean · **LICENSE: MIT © aDNA Labs (root, 2026-09-04)**. **Open tail (non-blocking): D3 Rosetta registrar ack** (`#needs-human`) — on ack, flip `adr_003` Amendment 1 + `lip_registry` "pending" → ratified.

> *(Closed campaign banners / build history: [`how/state_archive_20260803.md`](how/state_archive_20260803.md) [Keystone→Beacon] · [`how/state_archive_20260822.md`](how/state_archive_20260822.md) [Halftone] · [`how/state_archive_20260909.md`](how/state_archive_20260909.md) [**Blueprint P1–P4 + Polyglot**, relocated verbatim at this close] — nothing deleted, SO-3/SO-7.)*

## ▶ Resume Here — **no active campaign.** Operation Blueprint ✅ CLOSED 2026-09-09

Blueprint ran **2026-08-22 → 2026-09-09**: 7 phases, 6 missions, 9 sessions, closed **complete**.
Records: [`campaign_canvas_blueprint.md`](how/campaigns/campaign_canvas_blueprint/campaign_canvas_blueprint.md)
§Completion Summary · [AAR rollup](how/campaigns/campaign_canvas_blueprint/missions/artifacts/blueprint_campaign_aar_rollup.md).
**No successor campaign was chartered** — operator ruling at the P5 gate. Every tail below is a named
watch item or a backlog idea with an owner and an unblock condition.

> ⭐ **The finding the campaign was actually about, carried forward as practice.** Nine times, in every
> phase and in both directions, the defect was **a stated fact nobody re-derived** — six census figures,
> an index row that reported a peer's cooperation as a refusal for five weeks, a charter dependency on an
> artifact that was never built, a blocker sentence that was false when written and cost four phases, and
> a gate line that was true of the six suites it listed while a seventh sat red. ⇒ ***state the population
> on the face of the number: tip or history · class or literal · tracked or working-tree.*** Hopper
> ratified the generic form as their ADR-011 A8 §5. **Re-reading never catches these; re-deriving does** —
> and when it works it is quiet: P3 re-derived all 11 published figures at close and every one reproduced;
> P5 re-derived the two it inherited and both reproduced.

### Carried tail — every item, its owner, and what unblocks it

| # | Item | Lands as | Unblocks when |
|---|---|---|---|
| 1 | **`b1.5` — the `authority` axis** (memo #9 2026-08-22 · erratum v2 08-24 · **E2** 09-07; all delivered, **none answered**) | watch · `#needs-human` | **Rosetta rules.** Blocks: LIP-0010's conversion trigger · the `_reserved` tier of both P2b offers · SS's live-batch consumer. Verified at source: no delivery defect. The phase never advanced on their silence and neither should this. |
| 2 | **H4 live chain** (`generate:gemini,refine:comfy@0.4/comic_panel_refine`) | watch | **ComfyUI's M-RD1 lands a venue manifest**, then a **joint** operator ask with Vulcan. Their emitter now exists (measured 15/15) — the remaining dependency is theirs, not ours. ⛔ **Do not request spend before there is a real manifest to spend it on.** |
| 3 | **Mermaid trust grant** (F-P4-3) | watch · **operator item** | one click in your own vault. Both dogfood canvases are sight-certified on geometry/typography/layout; the **diagram channel renders as raw source** to any first-open viewer until someone clicks Allow. An agent should not make a trust decision on your behalf. |
| 4 | **M-PL3 joint sitting** — `comic_book_design/` + the comic nine | dossier **staged** + watch | **SS flags us.** [`m_pl3_dossier.md`](how/campaigns/campaign_canvas_blueprint/artifacts/m_pl3_dossier.md) is ready: 14 files / ~2619 lines measured, four options with costs, **decision deliberately open**. No urgency from either side. |
| 5 | **Seshat — the `canvasforge/`→`canvas/` rename** | watch | their reply. **The only `ack_required: true` still outstanding** from the P3 wave. |
| 6 | **Cartographer — 2 duplicate node ids** (one the empty string) in an entity graph | watch | their reply. Real defects; the 1173 float-coordinate errors around them are cosmetic. |
| 7 | **`ImagenWiring` selection-surface deprecation** — 10 methods, 0 call sites, **measured** | [backlog idea](how/backlog/idea_imagenwiring_selection_surface_deprecation.md) | a **fleet consumer sweep** (it is a public `canvas_core` export). ⛩ The old premise — *"no live caller"* — was **false**; struck at source. |
| 8 | **Runnable gate manifest** (F-P5-3) | [backlog idea](how/backlog/idea_runnable_gate_manifest.md) | any session with budget. Must **fail on omission**, or it is a prettier prose list with the same failure mode. Upstream candidate. |
| 9 | **`skill_l1_upgrade.md` RFC1918 disposition** | watch · operator/Rosetta | **template-inherited**, so the literals sit in every forked vault; remediating our copy fixes one of many and the durable fix is upstream. Not remediated unilaterally. |
| 10 | **SS live-batch review surface** — a *named* second consumer of the P4 board form | watch | **item 1 rules.** Then flag SS; they asked to be flagged rather than left to ask. |
| 11 | **D3 Rosetta registrar ack** *(standing, pre-Blueprint)* | watch · `#needs-human` | on ack, flip `adr_003` Amendment 1 + `lip_registry` "pending" → ratified. |

### Operator items awaiting signature (§7.7 — agents author, operators ratify)

1. **`adr_010`** artifact corpus policy — option was operator-selected at the plan gate; authored `proposed` per doctrine.
2. **`adr_011`** legacy canvas interop reconciliation — rules the 2026-02 legacy as the Standard's `view` row; migration **verified and offered**, not performed.
3. **`adr_012`** publication boundary remedy — ⚠ **read the two 2026-09-07 corrections first** (F-P2-7): our own census was a *literal*-census, not a *class*-census, and §Decision 3 declared a category remediated in full that was not.
4. **`adr_010` (Home.aDNA — Google model layer)** §7.7, pending there, not here.
5. ~~Push GO~~ ✅ granted 2026-08-24. **This session's commits are unpushed** — a fresh batch GO is owed.

## Current Phase

**None — between campaigns.** Canvas Standard **v2.3.0**; the reference implementation, 7 producers, the
`canvas_context` loader, the interaction runtime and the ComfyUI seam are all shipped and green.

**History:** Cartography → Keystone (v2.0.x) → Atelier → Palette → Salon → Armature → Lodestar → Beacon
(v2.3.0) → **Halftone** (the comic system end-to-end real: 27 panels / $3.618 / 4 print-ready pages / eye
gate PASSED; panel export under contract v1.0) → **Blueprint** (chartered 2026-08-22, **CLOSED 2026-09-09**).

**What Blueprint shipped**, in one line each: the **authoring rail** + Canvas's first dual-channel canvases ·
`layout_fit.py` (producers stop guessing text height separately from the traps that measure it) ·
`conform.py` (`normalize_edges` clears the fleet's most common conformance failure mechanically;
`unresolved_edges` reports and never repairs) · `visual_capture.py` (the Amendment-1 render gate, **met on
its fifth carry**) · the **ComfyUI seam** (`run_manifest` + `variant_board` + `tuning_surface`, five fixtures
that now *are* the contract — and ComfyUI's emitter shipped against them the next day) · `adr_011` · `adr_012` ·
`spec_federation_contract` §2.1a · the federation index corrected **in both directions** + §1b · **MIT ©
aDNA Labs** at root, ending 74 days public-and-unlicensed.

## Verified Ground Truth (anchors)

- Substrate exports **PDF** + **Google Docs** (`canvas_core/{pdf,gdoc}_export.py`) — the "anything-2D" thesis is shipped code.
- **Panel export is contract**: `what/specs/spec_panel_export_contract.md` v1.0 (filenames · numeric-ordering derivation · 2048-class/1024-floor panels · 300/200 page DPI). Changing §2 terms = major bump + consumer memos.
- **Corpus policy is ruled**: `adr_010` — `what/artifacts/` gitignored, canonical on-node, backup-registered (WI-16), no fetch path promised. Consumed *documents* never live on that shelf (the visual_dna_schema relocation is the enforcement precedent).
- **Visual reality is machine-checked**: `canvas_core/traps/` (**14** implemented/graduated — CV-COMIC-STYLE-01 joined 2026-08-22, H3-calibrated) + `canvas-visual-check` + the agent-confirmed-render doctrine — **runnable since 2026-09-08** as `python -m canvas_core.visual_capture <canvas>`. ⚠ **Never `--no-zoom` for a gate**: Obsidian culls node text below a zoom threshold, so a pin-sharp capture can be evidentially empty. **And re-render after any fix** — F-P4-4 was a false positive that took two further renders to kill.
- **Runner environment**: production suites run on anaconda pytest (`/opt/anaconda3/bin/pytest`) with `adna-canvas-std` **editable-installed** (`pip install -e what/code/canvas_std`, required by `canvas_core/core.py:40`) + `PYTHONPATH=what/production:what/code/canvas_context/src`; producers run per-package. `pytest.ini` excludes `_archive/`.
- **The gate set is SEVEN suites, and the seventh is the one that goes missing**: `canvas_std` 115/10 · `certify.py` 11/11 · `canvas_core` 1035/3 · **`canvas_context` 58** · producers **267 across 7 packages** · `comic_render` 154/2 · firewall diff 0. ⚠ Two traps, both hit live at P5: the seventh producer package is named **`brief_consumer`**, not `brief_generator` (a `*_generator` loop silently returns 257 and looks right), and a `cd` into a package **persists**, so a later firewall `git diff` from the wrong cwd returns empty — **indistinguishable from clean**. Use absolute paths. Fix: [`idea_runnable_gate_manifest`](how/backlog/idea_runnable_gate_manifest.md).
- **LIP process** real; Canvas LIP home `who/governance/lips/` (LIP-0008/0009 Final; queue empty; registrar handshake pending D3).

## Active Blockers

- **None blocking.** Everything open is either an operator item or an external reply — see §Resume Here's
  carried-tail table, where each has a named owner and an unblock condition.
- ⚠ **Two are worth not losing in a table**: `b1.5` has sat with **Rosetta since 2026-08-22** with three
  delivered, unanswered artifacts (verified at source — *not* a delivery defect), and it gates four
  downstream things; and the **mermaid trust grant** is one click that turns both dogfood canvases from
  "diagram channel unverified" to fully certified.
- ~~**Gated — no reject signal may reach the III store**~~ ✅ **RESOLVED 2026-09-07.** Argus ruled `accepted`
  = **the reviewer's verdict** (reading b); gate open (`REJECT_VOCABULARY_CONFIRMED = True`). ⚠ **Open ≠
  flowing**: the flip *armed* the path and emitted nothing (0 rejects in the pilot, measured). First emitter
  is the P4 board — which now has a real 20-variant batch behind it, and still awaits a batch that **needs a
  pick**. `spec_rlhf_seam` §6b.
- ~~**PT-P5 residual**~~ ✅ **RESOLVED 2026-08-22** (call #1 ruled via `adr_010` · #2 endorsed to Argus ·
  #3 GO given; Hestia drives the §C shim ref-sweeps, grace 2027-06-13).

## Next Steps

**Blueprint is closed; there is no queued phase.** The next session picks from the carried tail or opens
something new. In rough order of what is actually actionable *by us*:

1. **A batch GO for the push.** This session's commits are unpushed, as are P5's. Pushes are operator-gated
   batches — check `@{u}..HEAD` authorship first.
2. **The four §7.7 signatures** (`adr_010` · `adr_011` · **`adr_012` — read its two 2026-09-07 corrections
   first**) and the mermaid trust grant. All four are yours, none is ours.
3. **Backlog, ours to run whenever**: the [runnable gate manifest](how/backlog/idea_runnable_gate_manifest.md)
   (F-P5-3 — a prose gate list cannot notice a suite that left it) and the
   [`ImagenWiring` deprecation](how/backlog/idea_imagenwiring_selection_surface_deprecation.md) (measurement
   done; needs a fleet consumer sweep before anything is touched).
4. **Watch, nothing owed by us**: Rosetta (`b1.5` + **memo #13, delivered 2026-09-09** after one day staged) ·
   Seshat (rename, the last `ack_required` outstanding) · Cartographer (2 duplicate node ids) · SS (M-PL3
   sitting when they flag us; the `toEnd` output is on the shelf awaiting their commit) · Vulcan (M-RD1 →
   then the **joint** H4 spend ask).
5. ⛔ **Do not request H4 spend before ComfyUI's M-RD1 venue manifest exists.** Both vaults have now
   independently restated this boundary. Five fixtures and one real 20-variant batch prove more than a
   hand-written manifest over borrowed pixels would.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000` and ends at **`adr_012`**. *(No ADR was authored at P3, P4 or P5 — censuses, a spec section, a collector hook, a seam, and memos; none of it needed a new ruling. Three of the twelve still await §7.7 signature.)*
- ⭐ **A stated fact nobody re-derived** — Blueprint's defining family, **nine instances** across every phase and in both directions: six census figures, an index row that reported a peer's cooperation as a refusal for five weeks, a charter dependency on an artifact never built, a blocker sentence false when written that cost four phases, and a gate line true of the six suites it listed while a seventh sat red. ⇒ ***state the population on the face of the number: tip or history · class or literal · tracked or working-tree.*** Hopper ratified the generic form as their ADR-011 A8 §5. **Re-reading never catches these; re-deriving does.**
- ⭐ **A check that is not run is not a check that passes — and unlike a skipped one it leaves no trace** (F-P5-3). A skipped test prints `s`; a suite nobody invoked prints nothing at all, and the gate line beside it reads exactly as green. `canvas_context` left the gate set after Armature, no commit removed it, and each close copied the previous close's list. The durable fix is a gate manifest that **fails on omission**, not a better-maintained sentence.
- ⭐ **A mechanical fix delivered as a whole-file rewrite is not mechanical to the person reviewing it** (F-P5-2). The tool can be exactly right and the handover still unreviewable: `normalize_edges` changes one key per edge; `json.dumps(indent=2)` changed 1436 lines saying so. What a caller owes a recipient is not covered by the correctness of the function it called.
- ⭐ **A staged memo is not a refused one** (P5). Both delivery-refusal conditions this campaign met — a live peer lease, no drop-box — are **transient**. Memo #13 sat one day and went out at the first probe that found Rosetta's lease clear; E2 sat two and cleared on the third. **Re-probe; do not escalate, and do not treat silence-by-staging as silence-by-choice.**
- ⚠ **A `_reserved` block is not the only thing that can be pinned to a generated artifact.** Test assertions pinned to a *generated* fixture's size are a claim about the fixture, not about the code — derive them where the real invariant is structural (F-P5-3), and keep literals only where the literal *is* the claim.
- ⭐ **A registry defines its own blind spot in its membership rule** (P3). `federation_index` answered *"who holds a wrapper?"*, so the **10 vaults emitting canvases with no seam at all** — the least-supervised surface in the fleet — were invisible **by construction**, and no amount of diligent maintenance would have surfaced them. A peer had to say it about their own vault: *"the clean tree is clean by low traffic, not by construction."* New **§1b** enumerates them.
- ⭐ **An uncollected reply is a finding you will pay full price to rediscover** (F-P3-6). Kennedy's sat `staged_unsent` in *their* outbox for 34 days and contained, in its closing paragraph, the exact conflict we independently rediscovered and fixed as **F-P2-9** a month later. Two of their three findings were **already true when written** — one shipped the day before, built partly from their own contributed tool. *Nobody was wrong; the channel was.* This is the argument for `who/coordination/inbox/`, made in arrears.
- ⚠ **`C-3` is a bucket id, not a defect** (P3): 20 of 21 fleet occurrences were invalid `"center"` side values in one file; exactly **one** was a genuinely dangling edge. Counting the id and naming it after its most alarming member would have been a **21× overstatement literally derived from our own validator's output**. `unresolved_edges` isolates the real class — the two tools do not disagree, one counts a bucket.
- ⚠ **`gitignore` is a claim about one repository's index, not about existence in version control** (Berthier's correction, 2026-09-07). A nested repo makes those readings come apart, and no measurement of the outer repo can distinguish them — you have to look for a second `.git`.
- **`_reserved` off the canonical path is worse than absent** (F-B1-1, 2026-08-24): a block at `metadata._reserved` carries semantics no tool reads while reporting a green `[OK]` at `core`. 196 files fleet-wide have been in that state since 2026-02. Canonical path: `metadata.frontmatter._reserved`.
- **`authority` is doctrine-enforced, not machine-enforced** (F-B1-2): `canvas_std` does not know the key — 0 of 21 in-vault `adna_native` canvases carry it, and an invented value passes silently. LIP-0010 holds the fix, deferred by design.
- The metaverse consumer pattern carries a dated §5.2 2D-consumer note (SS ruling A1-a); the 3D derivative classes stand for future 3D consumers.
