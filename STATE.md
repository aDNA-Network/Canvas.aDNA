---
type: state
created: 2026-06-06
updated: 2026-10-15
status: active
last_edited_by: agent_mondrian
last_session: session_stanley_20261013_vernier_p2_door_p2b
tags: [state, governance, canvas, vernier, p6, inbox_receipt_gate, check_doors, state_compaction, scope_amendment, inbox_receipt, sync_hash, lip_0011, memorialisation, gridline, standard_v240, a8, lip_0010_final, reserved_keys, gate_reporting, plumbline, authority_axis, production_axis, b1_5_ruled, gate_manifest, runnable_gates, f_gm_1, canvas_presentation, blueprint_closed, p5_close, campaign_close, canvas_emission, comfyui_seam, gate_manifest, m_pl3, imagen_wiring, ss_conform, p3_repin_wave, federation_index, wrapper_census, pin_field_spellings, conformance_target, p2b_conversion_offers, conform, f_hr_1, rlhf_s4_gate, argus, p2c_producer_regate, layout_fit, trap_profiles, advisory_traps, p2_authoring_rail, dogfood, dual_channel, diagrammatic_context, licensing, adr_012, adr_024, publication_boundary, federation, standard]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

> **▶ 2026-10-15 — P2 RULED, 9/9 AS RECOMMENDED, AND THE DOOR HAD NEVER WORKED (Mondrian, `session_stanley_20261013_vernier_p2_door_p2b`).** First, the V-2 count was measured with a committed census, `how/gates/axis_tier_census.py`, which classifies with the real `_validate_axes`: **16 `extended` carriers · 15 valid · 1 would newly fail** (PercySleep `percy_topology`). It went onto the door (`023b1e4` · `25fd3f8`, GO ① corrected to the live push count). The door then took **no clicks in Zen**, and the operator asked to rule in chat. **Ruled Tier 2 via `AskUserQuestion`:** V-1 (b) · V-2 at `extended` · V-3 `sync.generator` · V-4 B14 as T2 · V-5 second file · V-6 spec as written · V-7 confirm 3 / CEL / decline 16 · V-8 bundle · firewall #7 list acked · **GOs ①②③ granted**. Record: [`vernier_p1_exit_20261012.output.json`](how/gates/vernier_p1_exit_20261012.output.json), `interaction_mode: tier2_auq`. ⛩ **F-V-9 — the door, not the browser:** the rendered script read `const SECTION_COUNT = ;` (data.json lacked `section_count`, and `generator.py` substitutes `""` silently). That SyntaxError leaves every handler undefined **in every browser**. It was there in all three renders of this door and in `operator_queue_20260916` since 09-16. The 10-12 `_zz_` round trip POSTed straight to the receiver and never loaded the page. ⇒ ***a round trip proven at the receiver is not a round trip proven at the page.*** **Same day, after the ruling:** pushed `0b4e503..b739b92` (GO ①) · both doors fixed + **proven at the page** (headless Chromium + Firefox; a probe submitted through the page → receiver), `4e2fdfa` · **Zen works**: the operator submitted a probe in Zen, and it landed via the receiver (T1A); the Local Network Access worry did not fire · memo **#27 → Astro**, corroborating Vitruvius's unported 08-07 `_coerce_count` fix (Astro: 17 untracked memos, HEAD 08-28) · F-V-7's Vulcan memo finally arrived and was receipted, `9bdd55c`. ⛔ **Gate line RED at `canvas_core` 1039/3**: the CLT is half-updated (SDK 27.0 built with Swift 6.4, compiler 6.3.3), so the Swift window-lister in `visual_capture.find_window` hangs → 1 test times out. **Node issue (Home), `#needs-human`: reinstall/update the Command Line Tools.** No Canvas code changed. **Next: P2b LIP-0011** once the gate line is green again.
>
> **▶ 2026-10-13 — P6 RAN AHEAD OF THE VERDICT, AND THE DROP-BOX GOT ITS CONSUMER (Mondrian, `session_stanley_20261013_vernier_receipt_door_refresh_p6`).** The door was still unruled at open (`.pending` present, no `.output.json`, `:8767` healthy). Operator ruling at the plan gate: **door refresh + P6's verdict-independent objectives**, recorded as a dated phase-order amendment, with the P6 gate still human. **Done:** three 10-12 replies receipted byte-unchanged (`db21711`; Noether **withdraws (a)**, Terminal accepts (b) + V-3 and migrates **once, after P4**, Socials says no date forces P7) · the replies folded into the door's V-1 · V-3 · V-8 as **evidence** (recommendations unchanged; V-8 gains a fifth sub-question on Socials' direct image bridge), re-rendered `e2ddf15` · **gate #11 `inbox_receipt`** (an untracked inbox memo older than 7 d, counted from `delivered_on`, is ⛔) + **`--check-doors`** (pending door port == sidecar, and `/health` names our root), both verified both ways with planted probes · **F-S078-04** `TB`→`TD` alias (+1 test, failing against HEAD first) · `canvas_context` `STANDARD_VERSION` **derived** (was `2.2.0` through two cuts) · LIP drafts → `superseded`, queue → `completed` · **F-DT-10 defined** from the 09-15 evidence (it had a count and no paragraph) · **ImagenWiring sweep: 0 external call sites across 114 live dirs** · Seven Lamps **disposition written** · **STATE 433 → 131 lines (12.3K → 3.3K words)** at the relocation commit `431fbc3`, 157 after this update; relocated verbatim to [`how/state_archive_20261012.md`](how/state_archive_20261012.md) in its own commit, reconstruction byte-equal to HEAD. ⛩ **F-V-7:** Vulcan's 10-08 endpoint memo is addressed to us and reached only **City's** inbox. Our copy is still staged in ComfyUI's outbox, and gate #11 cannot see a memo that never arrived. ⚠ **Two self-caught slips, recorded:** the new gate line first counted one overdue memo on both sides of the threshold, and a Seven Lamps table row said "none" where the grep had printed five. **Gates: 11, all green** (pasted below). ⛔ **Nothing ruled.**
>
> **▶ 2026-10-12 — ⛩ THE VAULT WAS IDLE 24 DAYS, THE WORLD MOVED, AND THE INBOX WAS A REGISTRY WITH NO CONSUMER (Mondrian, `session_stanley_20261012_vernier_review_and_inbox`).** Cold start at `483bc61` (2026-09-18). Found and **re-derived before writing**: **17 inbound memos untracked** (09-21 → 10-12; six `ack_required: true`; zero replies — by the drop-box's own rule, uncommitted = unread) · **Vernier's subject vault archived under the campaign** (`Armor.aDNA` → `Archive.aDNA/`, 09-24; live successor **`Terminal.aDNA/what/canvas/`**, now **8** canvases, regenerated the morning of this review) · **the V-1 question asked independently by four vaults** (Vauban · Ledoux · Berthier/Automator · Noether — whose `gen-canvas` M-B1 is **carded on our answer**, and whose ADR-018 + the LinkML Profile v0.1 define `sync_hash` as the master's bytes while we compute topology and City writes both) · Noether's two deadlines **passed** (P3 opened 10-10) · **4 doors pending 26 days, receiver DOWN** · 2 unpushed · `CLAUDE.md` current-state **nine campaigns stale** · STATE 79 KB · **F-DT-10 never defined** · `canvas_context` pins `2.2.0`. **Nothing red**: gates **10/10 green, exit 0**, reproduced the published line exactly; Terminal re-derivation **8/8 canonical · 8/8 A-8 · 8/8 source-hash · 0/8 topology · 8/8 native-flip [OK]**, their tree untouched. **Done this sitting:** receipt commit `9ea73ca` (byte-unchanged) · [review artifact](how/campaigns/campaign_canvas_vernier/artifacts/review_20261012_vault_state_and_inbox_triage.md) (F-V-1…F-V-6) · **Vernier scope amended** (fold-not-sibling): subject repointed, V-1 widened, **V-4…V-8** added (B14 pack · B18 `graph.canvas` + overlay · `_reserved` placement · LP dispositions + CEL · Socials formats/`style_ref`/RLHF), phases **6 → 8**, six missions chartered (P2b LIP-0011 → **v2.5.0** · P3 freshness both ways · P4 doctrine + memos · **P5 canvas memorialisation** · **P6 vault review & hygiene** · **P7 `post_generator` for Socials**) · **ruling door rendered** `how/gates/vernier_p1_exit_20261012` (9 sections, round-trip proven with a `_zz_` probe, removed) · receiver restarted → **`:8767`** (the port moved; Home's receiver no longer holds it) and the four old doors **re-rendered** — they had carried `:8768` and would have POSTed nowhere · `CLAUDE.md` current-state rewritten (prior struck) · six interim memos **#21–#26** (Terminal · LP · City · Automator · Socials · Hestia), each saying *recommendation, door rendered, not a signature*. ⇒ ***An inbox nobody commits from is a registry with no consumer*** (F-V-1, → gate #11 in P6) · ***a charter pinned to a vault name is a claim about the fleet, and the fleet moves while the campaign waits at a gate*** (F-V-2) · ***a validated shape with an undefined semantic acquires one meaning per implementer, and the number of implementers is now the fleet*** (F-V-3, Principle 4b at n=4) · ***a door is rendered against a port, and a port is a lease*** (F-V-5). ⛔ **Nothing ruled.** ▶ **Live operator items: FIVE doors** (`adr_010` · `adr_011` · `adr_012` · `operator_queue_20260916` · **`vernier_p1_exit_20261012`**), the push GO (2 + this session's commits), the memo-delivery GO for the P4 substantive replies. Lodestar's C-iii memorialisation deferral is **re-opened on evidence** (F-V-6 → P5).
>
> *(Four closed-campaign banners, 2026-09-09 → 2026-09-11 (Blueprint close · runnable gate manifest · Plumbline · Gridline), relocated verbatim → [`how/state_archive_20261012.md`](how/state_archive_20261012.md) §A, 2026-10-13.)*

> **▶ STANDARD PINS + OPEN TAIL (live).** Canvas Standard **v2.4.0 — CUT 2026-09-11** (LIP-0010 Option D **Final**; A-8 `authority`/`production`, both optional, `authority` requires `production`) · `canvas_std` **170/10** *(146 → 151 at Datum P2 → 156 at P3 → 170 at P4b; every step derived by stash/restore, never predicted)* · certification **12/12** · firewall clean · **LICENSE: MIT © aDNA Labs (root, 2026-09-04)**. **Open tail (non-blocking): D3 Rosetta registrar ack** (`#needs-human`) — on ack, flip `adr_003` Amendment 1 + `lip_registry` "pending" → ratified.

> *(Closed campaign banners / build history: [`how/state_archive_20260803.md`](how/state_archive_20260803.md) [Keystone→Beacon] · [`how/state_archive_20260822.md`](how/state_archive_20260822.md) [Halftone] · [`how/state_archive_20260909.md`](how/state_archive_20260909.md) [**Blueprint P1–P4 + Polyglot**, relocated verbatim at this close] — nothing deleted, SO-3/SO-7.)*

## ▶ Resume Here — **[Operation Vernier](how/campaigns/campaign_canvas_vernier/campaign_canvas_vernier.md) ACTIVE · scope amended 2026-10-12** · Datum ✅ 2026-09-15 · Gridline · Plumbline ✅ 2026-09-11

> ⛩ **Vernier — chartered 2026-09-17, amended 2026-10-12.** Subject: **`Terminal.aDNA/what/canvas/`** (8 canvases;
> `Archive.aDNA/Armor.aDNA` is P1's frozen measurement — Armor was archived 09-24, Hestia acked #26).
> ▶ **P0 · P1 · P1b CLOSED. Next: the operator rules V-1…V-8 + the firewall at the door
> [`how/gates/vernier_p1_exit_20261012`](how/gates/vernier_p1_exit_20261012.html)** (receiver live on the
> sidecar port — read `how/gates/.gate_receiver.port`, never hardcode). Then **P2b LIP-0011** from the
> `.output.json`. [Review + triage](how/campaigns/campaign_canvas_vernier/artifacts/review_20261012_vault_state_and_inbox_triage.md) ·
> [P1 artifact](how/campaigns/campaign_canvas_vernier/artifacts/p1_armor_dogfood.md) · missions in `how/campaigns/campaign_canvas_vernier/missions/`.
>
> **The items, one line each (recommendation → door):** **V-1** `sync_hash` semantic — three readings pass
> (topology · source bytes · master bytes); rec **(b)** topology stays + `sync.source_sha256` registered ·
> **V-2** A-8 at `extended` (rec yes, pending fleet count) · **V-3** `generator` → `sync.generator` (rec
> adopt; Home `topology.canvas` confirmed 3 counts) · **V-4** B14 pack → pack profile + loading modes (rec
> accept T2) · **V-5** B18 overlay → second file keyed by node id, Canvas eats `graph.canvas` first · **V-6**
> `_reserved` spec as written, grandfathering = migration note · **V-7** LP dispositions: our three
> not-a-lattice/documentation, the sixteen declined (no home, by design), four CEL rewrites accepted ·
> **V-8** Socials: *not yet* + P7 chartered, `style_ref` accepted, RLHF read-only yes (ours), contract binding.
>
> **Memos:** #21 Vauban/Terminal · #22 Noether (five receipted, two overdue — ours) · #23 Ledoux/City
> (staged on two live leases at authoring) · #24 Berthier/Automator · #25 Stentor/Socials · #26 Hestia —
> **interim**, each marked *recommendation, not a signature*. **#20 → Rosetta still staged with `adr_011`.**
> Substantive replies carrying verdicts = P4.
> **Replies in (2026-10-13 receipt `db21711`):** Noether (re #22) · Vauban (re #21) · Stentor (re #25), all three
> **waiting on the door's `.output.json`**, none acting on the interim. ⇒ **3 of the 4 vaults asking V-1 are aligned on
> (b) by their own statements** (LP · Terminal in prose, City in code). Automator is silent. The P4 wave also owes:
> the Seven Lamps reply ([disposition](how/campaigns/campaign_canvas_vernier/artifacts/p6_seven_lamps_disposition.md)) ·
> a visual verdict on a real panel seed for Vulcan (F-V-7) · Stentor's bridge question answered from V-8 ⑤.
>
> ▶ **P6 progress (run ahead of P2 by ruling, 2026-10-13):** obj 1–5 ✅ · obj 6: Seven Lamps ✅ · ImagenWiring
> sweep ✅ · **`data_bearing: false` OPERATOR-RULED 2026-10-13** (MANIFEST frontmatter; `what/artifacts/` shelf named as the exception). Home's next projection run picks it up and City un-seals; that is their act, not a write of ours · RFC1918 + D3 →
> one Rosetta memo, batched with #20 after `adr_011` · obj 7 (door archival) waits for verdicts.

> *(Closed-campaign blocks (the 09-15/16 stretch · Datum · Gridline · Plumbline · Blueprint and its carried finding) relocated verbatim → [`how/state_archive_20261012.md`](how/state_archive_20261012.md) §B, 2026-10-13. AARs and campaign docs remain the records of record.)*

### Carried tail — every item, its owner, and what unblocks it

| # | Item | Lands as | Unblocks when |
|---|---|---|---|
| 1 | **`b1.5` — the `authority` axis.** ⛩ **RULED 2026-09-11 — ADOPTED, with the axis SPLIT.** All four memos answered in one reply (#9 · erratum v2 · E2 · #13). The ruled shape: **`authority`** {`dual_channel`, `view`} = *who owns the meaning* · **`production`** {`hand_authored`, `generated`} = *how it is made* — **E2's larger fix**, which E2 named and declined to propose. | ✅ **cleared → Operation Plumbline** | ⭐ **The blocker cleared and made Canvas its own blocker.** The ruled `production` axis is **unknown to every tool we ship**; `conform.py:50` still pins the superseded 3-value set and *requires* a field the pattern rules optional; **2 of our 4 carriers declare `generator`**, no longer an `authority` value. ⚠ **Two inversions caught by re-deriving**: (i) the ruling **inverted** LIP-0010's trigger rather than firing it (both conjuncts broken) — so on the memo's own evidence *nothing* cleared; (ii) §3's *"NOT YET AUTHORED"* was **true at 00:55Z and false when read** — the pattern exists at `67ad713`, the commit right after the `860c59e` the memo pins as *"superseded when: our next commit."* ⇒ ***a memo is a measurement with a timestamp.*** |
| 2 | **H4 live chain** (`generate:gemini,refine:comfy@0.4/comic_panel_refine`) | watch | ⛩ **2026-10-13: a venue of record now exists** — ComfyUI 0.39.2 on Anduril's RTX 3090, `comic_panel_refine` 9/9 *mechanically*, and Vulcan asks us for a **visual verdict on a real panel seed** (memo `coord_2026_10_08_outbound_vulcan_to_mondrian_vitruvius_ledoux_anduril_endpoint`, read in City's inbox; our copy is still staged in ComfyUI's outbox, **F-V-7**). Reach is via an ssh forward until Nebula passes 8188. *Prior text:* **ComfyUI's M-RD1 lands a venue manifest**, then a **joint** operator ask with Vulcan. Their emitter now exists (measured 15/15) — the remaining dependency is theirs, not ours. ⛔ **Do not request spend before there is a real manifest to spend it on.** |
| 3 | **Mermaid trust grant** (F-P4-3) | watch · **operator item** | one click in your own vault. Both dogfood canvases are sight-certified on geometry/typography/layout; the **diagram channel renders as raw source** to any first-open viewer until someone clicks Allow. An agent should not make a trust decision on your behalf. |
| 4 | **M-PL3 joint sitting** — `comic_book_design/` + the comic nine | dossier **staged** + watch | **SS flags us.** [`m_pl3_dossier.md`](how/campaigns/campaign_canvas_blueprint/artifacts/m_pl3_dossier.md) is ready: 14 files / ~2619 lines measured, four options with costs, **decision deliberately open**. No urgency from either side. |
| 5 | **Seshat — the `canvasforge/`→`canvas/` rename** | watch | their reply. **The only `ack_required: true` still outstanding** from the P3 wave. |
| 6 | **Cartographer — 2 duplicate node ids** (one the empty string) in an entity graph | watch | their reply. Real defects; the 1173 float-coordinate errors around them are cosmetic. |
| 7 | **`ImagenWiring` selection-surface deprecation** — 10 methods, 0 call sites, **measured** | [backlog idea](how/backlog/idea_imagenwiring_selection_surface_deprecation.md) | ✅ **sweep run 2026-10-13: 0 external call sites across 114 live root dirs** (1 docstring mention, Home). Step 2 (deprecate with a named sunset) is unblocked and **not done**. *Was:* a **fleet consumer sweep** (it is a public `canvas_core` export). ⛩ The old premise — *"no live caller"* — was **false**; struck at source. |
| 8 | ~~**Runnable gate manifest** (F-P5-3)~~ | ✅ **SHIPPED 2026-09-10** | `how/gates/gate_manifest.py` + [`AGENTS.md`](how/gates/AGENTS.md). Fails on omission (exit 3), verified by derivation. Found an eighth suite on first run (**F-GM-1**, `canvas_presentation`). **Upstream candidate remains open** — mention at a natural pause, file only if the operator approves. |
| 9 | **`skill_l1_upgrade.md` RFC1918 disposition** | watch · operator/Rosetta | **template-inherited**, so the literals sit in every forked vault; remediating our copy fixes one of many and the durable fix is upstream. Not remediated unilaterally. |
| 10 | **SS live-batch review surface.** ⚠ **Corrected 2026-09-11:** this row read *"a named **second** consumer of the **P4 board form**"* — **that phrasing was ours, not theirs.** SS said the review-surface form would be *"the right **first** consumer … **on our side**"*, which is a different claim, and ours quietly upgraded the commitment. ⛔ **And the compatibility is unmeasured**: `variant_board.py` consumes a ComfyUI **run manifest**; SS's pending batch is *"built as an HTML gate."* The older path (`spec_canvas_review_surface` + `_reserved.interaction` + `review_collect.py`) may be the actual fit. Flagged to them as a real question, not a formality. | watch → **Plumbline P3** | ⛩ **Item 1 ruled 2026-09-11 and it CLEARED.** Memo #15 promised *"flagged when it clears, not left to ask"* — the flag is Plumbline **P3, memo #17**, and it carries the honest caveat that Canvas's own tooling enforced the superseded axis until P1. ⚠ **Two obligations were welded in this row and only one was ever item 1's**: the *promise* (ours, now dischargeable) and the *conversion* (needs P1's under-coverage ruling first — SS's boards are hand-authored primary artifacts, the population where all three old values were wrong). |
| 11 | **D3 Rosetta registrar ack** *(standing, pre-Blueprint)* | watch · `#needs-human` | on ack, flip `adr_003` Amendment 1 + `lip_registry` "pending" → ratified. |

### ⛩ 2026-09-16 — the operator-owed tail became doors

*(Relocated verbatim → [`how/state_archive_20261012.md`](how/state_archive_20261012.md) §C, 2026-10-13. The ADR-011 amendment story now lives on its door, `how/gates/adr_011_ratification.html`, and in the ADR itself; read `§What this ADR says today` first.)*

### Operator items awaiting signature (§7.7 — agents author, operators ratify)

1. ~~⛩ **LIP-0010 → Canvas Standard v2.4.0** *(NEW 2026-09-11, and the live one)*~~ ✅ **SIGNED 2026-09-11 at the Gridline plan gate; LIP-0010 Final, v2.4.0 cut.** *(Struck 2026-10-13. It had read as live for a month after it was discharged.)* — **Option D**: `authority` {`dual_channel`, `view`} + `production` {`hand_authored`, `generated`}, both optional, validated only if present, **two keys or neither**. The four-file firewall touch is named in the LIP so the signature is informed. ⛔ **The firewall does not move without this.** ⚠ Signing does **not** mandate either key on any canvas — the ruled pattern declines that and so does the LIP.
2. **`adr_010`** artifact corpus policy — option was operator-selected at the plan gate; authored `proposed` per doctrine.
2. **`adr_011`** legacy canvas interop reconciliation — rules the 2026-02 legacy as the Standard's `view` row; migration **verified and offered**, not performed.
3. **`adr_012`** publication boundary remedy — ⚠ **read the two 2026-09-07 corrections first** (F-P2-7): our own census was a *literal*-census, not a *class*-census, and §Decision 3 declared a category remediated in full that was not.
4. **`adr_010` (Home.aDNA — Google model layer)** §7.7, pending there, not here.
5. ✅ **Push GO granted + executed 2026-10-13**: 18 commits → `origin` `e44a9aa..0b4e503`, gitleaks clean, authorship uniform (the 17 asked for + the close commit recording the rulings). ⚠ This line's own correction is **1 unpushed commit**; count with `git rev-list --count @{u}..HEAD`, never `head -N`.
6. ~~**`vernier_p1_exit_20261012`** — V-1…V-8 + firewall touch #7 + three GOs~~ ✅ **RULED 2026-10-15**: 9/9 approve, Tier 2 (the web door was dead, F-V-9). P2b unblocked. *(Struck the day it was discharged.)*

## Current Phase

⛩ **2026-10-15: P2 RULED (9/9 as recommended, Tier 2). Next: P2b LIP-0011 → v2.5.0; ⛔ four doors still pending (`adr_010` · `adr_011` · `adr_012` · `operator_queue_20260916`, the last one script-dead until re-rendered, F-V-9).** The paragraph below is the 10-13 state.

⛩ **Operation Vernier ACTIVE. P1b closed 2026-10-12; P6 objectives 1–6 run 2026-10-13 ahead of P2 by ruling (the P6 gate is not
closed).** The next act is still the operator's: the V-1…V-8 + firewall verdicts at `how/gates/vernier_p1_exit_20261012` (evidence
refreshed 10-13). Then P2b (LIP-0011 → v2.5.0). ⛔ **Five operator doors pending** (`adr_010` · `adr_011` · `adr_012` ·
`operator_queue_20260916` · `vernier_p1_exit_20261012`), all 5/5 on the live receiver per `gate_manifest.py --check-doors`.
Memo **#20** stays staged with `adr_011`. **Pushed 2026-10-13** (`e44a9aa..0b4e503`); one local correction commit after it.

<details><summary>Prior text (2026-10-12), superseded by the paragraph above and kept verbatim</summary>

⛩ **Operation Vernier ACTIVE — P1b closed 2026-10-12 (review · receipt · amendment · door · interim memos).
Next act is the operator's: the V-1…V-8 + firewall verdicts at `how/gates/vernier_p1_exit_20261012`.** Then
P2b (LIP-0011 → v2.5.0). ⛔ **Five operator doors pending** (`adr_010` · `adr_011` · `adr_012` · `operator_queue_20260916` ·
`vernier_p1_exit_20261012`) — all re-rendered today against the live receiver port.
Memo **#20** stays staged with `adr_011`; **#21–#26 delivered/staged 2026-10-12** per their `delivery_path_basis`.
**Push GO owed** for `4931819`, `483bc61` + this session's commits.

</details>

### Prior campaigns

*(Datum's close, its three-item residue, the Gridline close and the history line relocated verbatim → [`how/state_archive_20261012.md`](how/state_archive_20261012.md) §D, 2026-10-13. Datum's residue — corpus 12/40 · F-DT-8 · memo #20 — is carried on the door `operator_queue_20260916`.)*

## Verified Ground Truth (anchors)

- Substrate exports **PDF** + **Google Docs** (`canvas_core/{pdf,gdoc}_export.py`) — the "anything-2D" thesis is shipped code.
- **Panel export is contract**: `what/specs/spec_panel_export_contract.md` v1.0 (filenames · numeric-ordering derivation · 2048-class/1024-floor panels · 300/200 page DPI). Changing §2 terms = major bump + consumer memos.
- **Corpus policy is ruled**: `adr_010` — `what/artifacts/` gitignored, canonical on-node, backup-registered (WI-16), no fetch path promised. Consumed *documents* never live on that shelf (the visual_dna_schema relocation is the enforcement precedent).
- **Visual reality is machine-checked**: `canvas_core/traps/` (**14** implemented/graduated — CV-COMIC-STYLE-01 joined 2026-08-22, H3-calibrated) + `canvas-visual-check` + the agent-confirmed-render doctrine — **runnable since 2026-09-08** as `python -m canvas_core.visual_capture <canvas>`. ⚠ **Never `--no-zoom` for a gate**: Obsidian culls node text below a zoom threshold, so a pin-sharp capture can be evidentially empty. **And re-render after any fix** — F-P4-4 was a false positive that took two further renders to kill.
- **Runner environment**: production suites run on anaconda pytest (`/opt/anaconda3/bin/pytest`) with `adna-canvas-std` **editable-installed** (`pip install -e what/code/canvas_std`, required by `canvas_core/core.py:40`) + `PYTHONPATH=what/production:what/code/canvas_context/src`; producers run per-package. `pytest.ini` excludes `_archive/`.
- **The gate set is RUNNABLE — do not retype it from here.** `python3 how/gates/gate_manifest.py --markdown` runs every suite and emits the gate line; a close **pastes generated output**. Contract + rationale: [`how/gates/AGENTS.md`](how/gates/AGENTS.md). It **fails on omission** (exit 3) as well as on disagreement (2), suite failure (1) and precondition fault (4) — because the prose version could not notice a suite that left it (F-P5-3). ⚠ **A disagreement is a finding to investigate, not a number to edit into the manifest.** Current: **ELEVEN gates**, all green 2026-10-13 (Vernier P6), **pasted from `--markdown`** — `canvas_std` **170/10** · certification **12/12** · `canvas_core` **1039/4** · `canvas_presentation` **57/2** · `canvas_context` **58** · producers **276 across 7 packages** · `comic_render` **154/2** · firewall diff **0** · registry census **11/11** keys · dual-channel freshness **2/2** · inbox receipt **0 overdue** (0 untracked within 7 d). *(Was TEN at the Datum close, 2026-09-15, with producers at 275. 275 → 276 is the F-S078-04 test, derived.)* ⛩ **Gate #11 `inbox_receipt` added 2026-10-13 (F-V-1)**, with `--check-doors` (F-V-5) beside it as a flag. ⚠ **`certification` 12/12 is a narrower claim than it reads** (Datum P4b): it exercises the **validator's** verdicts, and the JSON Schema is an independent second copy whose fixture-corpus coverage is **12 of 40 enum values**, two enums at zero — printed by `test_schema_conformance.py` on every run so the limit travels with the number. ⚠ **`canvas_core` reads 1039/4 here and 1040/3 elsewhere, and that is not a discrepancy** — F-DT-5: one test skips when Obsidian is not open on this vault, so `Gate.env_skips` allows the split to move while requiring the **total (1043)** to match exactly. ⇒ *a pinned passed/skipped split is a claim about the runner, not about the code.* ⛩ **Gate #10 `registry_census` added 2026-09-13 (Datum P2)**, and at **P3** it stopped deriving its own fault classes — the census now names them and the gate **consumes** them, because a second derivation of a cause is a second thing that can disagree with the first (**F-DT-6** one level up). ⛩ **Three defects in the manifest itself were fixed at Gridline P1** and they change how this line may be trusted: the `firewall` check ran `git diff` (**unstaged only** — blind to staged *and* untracked breaches, two of three classes); the producers row printed a hardcoded `267`; and `markdown_gate_line()` **hardcoded green for all three non-pytest gates** — `"firewall diff **0**"` was a *constant string* and printed clean while the firewall was FAILING. ⇒ ***the report is part of the check.*** A non-OK gate now renders `⛔ <status>`, so this line **cannot be pasted as green while red**. ⛩ **Gate #9 `dual_channel_freshness` added 2026-09-11 (F-PL-6)** — rebuilds every `*.diagram.yaml` into a temp dir and compares parsed documents. It is the first gate here that checks an **artifact** rather than a **suite**, and it exists because both dual-channel pairs had been stale for four days behind five all-green gate lines. ⚠ Discovery is now `find -P` and **reports every symlink it skips** — the population line counts **things, not names**. The two P5 traps are now encoded in the script rather than remembered: the seventh producer package is **`brief_consumer`**, not `brief_generator` (a `*_generator` glob silently returns 257 and looks right), and a persisted `cd` makes a firewall `git diff` return empty — **indistinguishable from clean** (the script never `chdir()`s; regression-tested from a deep subdirectory).
- **LIP process** real; Canvas LIP home `who/governance/lips/` (LIP-0008/0009 Final; queue empty; registrar handshake pending D3).

## Active Blockers

- **None blocking.** Everything open is either an operator item or an external reply — see §Resume Here's
  carried-tail table, where each has a named owner and an unblock condition.
- ~~⚠ `b1.5` has sat with **Rosetta since 2026-08-22** with three delivered, unanswered artifacts~~
  ✅ **ANSWERED 2026-09-11** — all four memos in one reply. ⭐ **They measured the cause and it is worth
  carrying into our own practice, not just noting**: their reply-owed sweep filtered on
  **`ack_required: true`**, and every Canvas memo sets it `false` — correctly, by our lights, because we
  were not demanding a courtesy. So the sweep reported *nothing owed to Canvas*, four times, while memo
  #13 sat in their tree saying *"still awaits your ruling."* ⇒ ***`ack_required` states the sender's
  expectation; it cannot state whether a question was asked.*** **This is a finding about us**: our
  outbound default is `false`, and it is now known to be invisible to at least one peer's sweep.
- ⚠ **Still worth not losing in a table**: the **mermaid trust grant** is one click that turns both
  dogfood canvases from "diagram channel unverified" to fully certified.
- ~~**Gated — no reject signal may reach the III store**~~ ✅ **RESOLVED 2026-09-07.** Argus ruled `accepted`
  = **the reviewer's verdict** (reading b); gate open (`REJECT_VOCABULARY_CONFIRMED = True`). ⚠ **Open ≠
  flowing**: the flip *armed* the path and emitted nothing (0 rejects in the pilot, measured). First emitter
  is the P4 board — which now has a real 20-variant batch behind it, and still awaits a batch that **needs a
  pick**. `spec_rlhf_seam` §6b.
- ~~**PT-P5 residual**~~ ✅ **RESOLVED 2026-08-22** (call #1 ruled via `adr_010` · #2 endorsed to Argus ·
  #3 GO given; Hestia drives the §C shim ref-sweeps, grace 2027-06-13).

## Next Steps

1. **Operator:** rule `vernier_p1_exit_20261012` (P2), and the other four doors when convenient. The receiver is on the sidecar port; run `--check-doors` first.
2. **On the verdict:** P2b LIP-0011 → v2.5.0 (firewall touch #7, named on the door), then the P4 memo wave carrying verdicts (Terminal · LP · City · Automator · Socials · SS Seven Lamps · Vulcan F-V-7 · Rosetta #20 + RFC1918 + D3).
3. **Verdict-independent, ours:** ImagenWiring step 2 (deprecate) · the P5 survey (read-only) · `canvas_context` `pyproject.toml` version drift (0.2.0 vs 0.3.2).

*(The Blueprint-era list relocated verbatim → [`how/state_archive_20261012.md`](how/state_archive_20261012.md) §E, 2026-10-13. Current next steps: §Resume Here.)*

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000` and ends at **`adr_012`**. *(No ADR was authored at P3, P4 or P5 — censuses, a spec section, a collector hook, a seam, and memos; none of it needed a new ruling. Three of the twelve still await §7.7 signature.)*
- *(The lesson bullets — 24 of them, Datum back to Blueprint P3 — relocated verbatim → [`how/state_archive_20261012.md`](how/state_archive_20261012.md) §F, 2026-10-13. Graduated doctrine lives in `what/context/` (e.g. `context_registry_derivability.md`, `context_canvas_surface_legs.md`).)*
- The metaverse consumer pattern carries a dated §5.2 2D-consumer note (SS ruling A1-a); the 3D derivative classes stand for future 3D consumers.
