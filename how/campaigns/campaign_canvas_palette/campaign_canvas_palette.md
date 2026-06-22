---
campaign_id: campaign_canvas_palette
type: campaign
title: "Operation Palette — Complete the canvas output family (letter, post) + harden the producer factory"
owner: stanley
status: active
activated: 2026-06-21
phase_count: 5
mission_count: 1
estimated_sessions: "6-9"
estimation_class: build-broad
priority: medium
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
predecessor: campaign_canvas_production
tags: [campaign, build, canvas, production, producer-factory, letter, post, palette]
---

# Campaign: Operation Palette (complete the output family + harden the factory)

> **EXECUTION campaign — close the two Mondrian-owned gaps the cross-campaign retrospective surfaced.** Successor to
> Operation Atelier (`campaign_canvas_production`, completed 2026-06-21), which built diagram + comic and left **five**
> in-vault producers green on `canvas_std`. The CLAUDE.md thesis names six 2D outputs — "paper, deck, comic, **letter**,
> site, **post**" — but **letter** is only spec-sketched (`spec_federation_contract §6.3`) and **post** is unspec'd
> (site = Astro, out of scope). Separately, the producer pattern is proven **5×** yet still hand-cloned each time. This
> campaign (1) **graduates the pattern into a reusable factory** (a skill + a copy-me scaffold), then (2) **builds
> `letter_generator` and `post_generator` with it** — each self-contained on the already-shipped `canvas_std`, Standard
> untouched. **No external gates** (independent of PT P5 and LIP-0008/0009). Approved plan:
> `~/.claude/plans/please-read-the-claude-md-sleepy-minsky.md`.

## Goal

A reusable producer factory (`how/skills/skill_canvas_producer_build.md` + `what/production/_scaffold/`) **used to
build** at least `letter_generator` and `post_generator`, each conformant (degrading to a valid Obsidian canvas),
round-trippable, and green — so the canvas output family covers the thesis list. The two-shelf firewall holds
(`what/code/canvas_std/` git-diff 0) and the close `iii/` structural review is 0 High / 0 Med.

## Context

Operation Keystone shipped the aDNA Canvas Standard (now v2.0.2) + the immutable `canvas_std` reference impl + three
producers (`deck_generator` 16 · `brief_consumer` 10 · `document_generator` 37); Operation Atelier added
`diagram_generator` 36 + `comic_generator` 87 — **266 tests green, firewall git-diff 0 throughout**. Both campaigns
proved the "reduce to the grammar / fork, don't drift" thesis: every output reduced to one producer pipeline and the
Standard needed **zero new features**. What remains for the *output* leg of the thesis is breadth (letter, post) and
making the next producer cheap (the factory). The mature pattern doc `what/context/context_canvas_producer_pattern.md`
(graduated at Atelier A3) is the spec the factory operationalizes. (The under-exercised *context-object* and *interface*
legs of the thesis are deferred to a separate future campaign — see Notes.)

## Scope

### In Scope (BUILD)
- **Factory:** `how/skills/skill_canvas_producer_build.md` (agent skill operationalizing the 4-step pipeline, package
  shape, "four+1" suite, venv recipe, conformance-vocabulary checklist, firewall/`iii` gate) + `what/production/_scaffold/`
  (an inert copy-me producer skeleton at producer depth, so `../../code/canvas_std` paths stay valid on clone).
- **`what/production/letter_generator/`** — a net-new minimal producer (LetterInput → v2.0.0 `.canvas`): single
  canonical surface, one `region` `{flow: vertical, pagination: paged, extent: {unit: pages, max: 1}}`,
  `profile: document`. Pilots the scaffold.
- **`what/production/post_generator/`** — a net-new producer (PostInput → `.canvas`): single canonical surface; post
  panels as short-form `text` + optional `image`-class node carrying `qualities.image_prompt`; thread = `sequence`
  chain (acyclic); platform profile producer-side.
- Per-producer test suites (conformance · round-trip · degradation · components · coverage + model-neutrality) +
  worked examples + `iii_quality_contract.md`.
- Cross-producer no-regression sweep + structural `iii/` review at close; context graduation.

### Out of Scope
- Modifying `canvas_std` (two-shelf firewall; any Standard change goes through the LIP process, `adr_003`).
- **Canvas-as-surface** (the context-object + interface legs) — a separate strategic campaign; needs a boundary ADR.
- **PT P5** (`canvas_core` relocation + ~8 wrapper refederations + registry registration) — Hestia/Home.aDNA. New
  producers mirror the existing five: depend on the *installed* `adna-canvas-std`; the formal `canvas/` wrapper rides
  on FU1/PT-P5, not invented here.
- **LIP-0008/0009 → v2.1.0** (FA review closes 2026-06-27) — lands independently.
- Image **rendering** (ComfyUI), render/visual scoring (`canvas_presentation`, PT-P5), web/`site` output (Astro).
- Registering `letter`/`post` as built-in profiles in `canvas_std.schema` (touches the immutable substrate → a LIP).
  Profiles stay producer-side.

## Phases & Missions

> Missions kept thin until phase entry (SO-3); objectives authored at entry. Phase exits are **human gates** (SO-1) —
> report a SITREP and HOLD. The factory is built first; `letter` pilots it (warm-up); `post` is the larger build (needs
> a short spec). Each producer is self-contained on `canvas_std` with **zero PT-P5 dependency**.

### Phase P0 — Charter & decision record (cheap; no code)
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| P0.1 | Charter scaffold + a decision record (the 6 Decision Points below); confirm no letter/post producer or spec exists beyond §6.3 | ≤1 | ✅ **done 2026-06-21** — 6 decisions ratified (all defaults); campaign activated ([[how/campaigns/campaign_canvas_palette/missions/mission_p0_charter_triage\|mission]]) |

**Phase exit gate (P0→P1, HUMAN):** operator ratifies the P0 decision record (codename/slug, factory artifact homes,
letter conformance level, post domain model, producer names, optional stretch). **This ratification activates the
campaign** (`status: active`) and authorizes the P1 factory build.

### Phase P1 — Factory hardening
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| P1 | Build `skill_canvas_producer_build.md` (via `template_skill.md`) + `what/production/_scaffold/` (inert stubs; excluded from the sweep) | 1-2 | ✅ **done 2026-06-21** — skill + 17-file scaffold; py_compile clean; firewall git-diff 0 ([[how/campaigns/campaign_canvas_palette/missions/mission_p1_factory\|mission]]) |

**Phase exit gate (P1→P2, HUMAN):** skill reads as a faithful runbook of the pattern doc; scaffold clones cleanly
(relative paths valid); `canvas_std` firewall git-diff 0; AAR GO. **HELD before letter (P2 pilots the scaffold).**

> **Phase progress (2026-06-21) — PHASE P1 COMPLETE ✅ (factory built):** shipped
> `how/skills/skill_canvas_producer_build.md` (the runbook) + `what/production/_scaffold/` (17 files; inert copy-me
> producer skeleton at producer depth, `consume.py` carrying the canonical 4-step contract; `tests/` skip at module
> level so the template never false-fails). All scaffold `.py` `py_compile` clean; `_scaffold` (underscore) excluded
> from the named-producer sweep; **`canvas_std` firewall git-diff 0.** **⛔ HELD at the P1→P2 phase gate (human gate)** —
> do not start the letter build (P2) without the operator. P2 clones `_scaffold` → `letter_generator` as the factory's
> live acceptance test.

### Phase P2 — Letter producer (warm-up; pilots the scaffold)
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| P2 | Clone `_scaffold` → `letter_generator`; substrate-free `model.py` (letterhead/date/recipient/salutation/body/closing/signature); `consume.py` single surface + one paged region; four+1 suite + worked example | 1-2 | ✅ **done 2026-06-22** — `letter_generator` 17/17 aDNA-Native; example `[OK]` + degrades; firewall git-diff 0 ([[how/campaigns/campaign_canvas_palette/missions/mission_p2_letter\|mission]]) |

**Phase exit gate (P2→P3, HUMAN):** full letter suite green; example validates at its ratified level + degrades
(D-1/D-2/D-3); firewall git-diff 0; AAR GO. **HELD.**

> **Phase progress (2026-06-22) — PHASE P2 COMPLETE ✅ (letter producer built; factory validated):**
> `what/production/letter_generator/` built on `canvas_std` by cloning `_scaffold` + following
> `skill_canvas_producer_build.md` (the factory's live acceptance test — **passed**). Single `letter_root` canonical
> surface; per-block baseline `text` nodes (letterhead/date/recipient/salutation/body₀..ₙ/closing/signature) chained
> `reading_order`; one paged region `{unit: pages, max: 1}`, `profile: document`. Suite **17/17**, `ruff` clean; worked
> example (10 nodes/8 edges) validates **`adna_native [OK]`** + degrades (D-1/D-2/D-3); **`canvas_std` firewall
> git-diff 0**; no regression (canvas_std + other producers untouched). **Factory needs no changes.** **⛔ HELD at the
> P2→P3 phase gate (human gate)** — do not start the post build (P3) without the operator.

### Phase P3 — Social post producer (the larger build)
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| P3 | P3a short post spec/decision (from P0); P3b build `post_generator` — single + thread; short-form text panels + optional image-prompt metadata; platform profile producer-side; four+1 suite + worked examples | 2-3 | ✅ **done 2026-06-22** — `post_generator` 20/20 (single+thread); both examples `[OK]`; firewall git-diff 0 ([[how/campaigns/campaign_canvas_palette/missions/mission_p3_post\|mission]]) |

**Phase exit gate (P3→P4, HUMAN):** full post suite green (single + thread); no regression in the other suites;
firewall git-diff 0; AAR GO. **HELD.**

> **Phase progress (2026-06-22) — PHASE P3 COMPLETE ✅ (post producer built):** `what/production/post_generator/`
> built on `canvas_std` (the multi-panel/thread path; built directly off the `letter_generator` exemplar + the factory
> skill after the P2 build-agent hit a session limit). One `post_root` canonical surface; `post{i}` copy nodes chained
> `sequence` (linear/acyclic; `isStartNode` post-hoc on `post0`); optional `img{i}` image-class nodes carrying
> `qualities.image_prompt` (no render — ComfyUI) tied by `adjacency`; producer-side platform profiles. Suite **20/20**,
> `ruff` clean; two examples (single 2/0 · thread 5/3) validate **`adna_native [OK]`** + degrade; **`canvas_std`
> firewall git-diff 0**. **7 in-vault producers now green.** **⛔ HELD at the P3→P4 phase gate (human gate)** — P4 is
> the cross-producer sweep + `iii/` review + context graduation + close.

### Phase P4 — Validation & close (+ optional stretch)
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| P4 | Optional poster/one-pager if budget; full cross-producer sweep + structural `iii/` review; context graduation; doc currency; Completion Summary + AAR + `status: completed` | 1-2 | ⏳ pending P3 |

**Campaign close gate (HUMAN / operator disposition):** all 7 producer suites + `canvas_std` green; `iii/` artifacts
filed; graduation run; STATE + CLAUDE.md + README currency; `status: completed`.

> Letter alone (P0+P1+P2) is an independently shippable deliverable (~3-4 sessions) if post slips — it also proves the
> factory end-to-end.

## Decision Points

| # | When | Decision | Plan default | Status |
|---|------|----------|--------------|--------|
| 1 | P0→P1 gate | Codename / slug | Operation Palette / `campaign_canvas_palette` | ✅ ratified 2026-06-21 |
| 2 | P0→P1 gate | Factory artifact homes | skill `how/skills/skill_canvas_producer_build.md` + scaffold `what/production/_scaffold/` (producer depth) | ✅ ratified 2026-06-21 |
| 3 | P0→P1 gate | Letter conformance level | `adna_native` (family uniformity) over the §6.3 `extended` minimal-proof sketch | ✅ ratified 2026-06-21 |
| 4 | P0→P1 gate | Post domain model | single post **and** thread (chain of `sequence` panels); platform profiles producer-side (char budget + aspect ratio); image support via `qualities.image_prompt` (ComfyUI renders) | ✅ ratified 2026-06-21 |
| 5 | P0→P1 gate | Producer names | `letter_generator`, `post_generator` (mirror `*_generator`) | ✅ ratified 2026-06-21 |
| 6 | P0→P1 gate | Optional stretch (poster / one-pager) | Defer to P4-if-budget; not committed | ✅ ratified 2026-06-21 |

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Scaffold at wrong depth breaks `../../code/canvas_std` relative paths on clone | Medium | Place `_scaffold` at `what/production/_scaffold/` (same depth as real producers); P2 clone is the live test. |
| Scaffold stub tests pollute the cross-producer sweep | Low | Sweep enumerates named producers explicitly; `_scaffold` tests are TODO-stub/skipped; exclude `_scaffold` from the sweep. |
| Post "thread" edges mis-tagged → A-5 acyclicity failure | Medium | Thread chain = `sequence` (strictly linear, acyclic); never cycle; a round-trip test exercises a 3-panel thread. |
| Post image boundary leak (rendering creeps in) | Medium | Emit prompt as `qualities.image_prompt` only; no ComfyUI import, no image I/O (C8). |
| Letter `extent.unit` / single-page region mismatch | Low | One paged region `{unit: pages, max: 1}`; degradation test asserts no out-of-enum baseline leak. |
| Accidental edit to immutable `canvas_std` | High | Verify `git -C what/code/canvas_std diff --stat` empty at every phase gate. |
| Factory drifts from the real pattern (skill says X, producers do Y) | Medium | P1 skill is authored *from* `context_canvas_producer_pattern.md`; P2 validates the skill by following it to build letter. |

## Verification Strategy

### Per-Mission
| Check | Method | Gate? |
|-------|--------|-------|
| SITREP filed | Session closure protocol | Yes |
| AAR produced | 5-step AAR | Yes |
| Producer suite green + `ruff` clean | `pytest` in the producer `.venv` | Yes |
| Example builds + validates | `<producer> build … && canvas-std validate …` → `[OK]` | Yes |
| `canvas_std` firewall git-diff 0 | `git -C what/code/canvas_std diff --stat` | Yes |
| Files committed | Git status clean | Yes |

### Per-Phase
| Check | Method | Gate? |
|-------|--------|-------|
| All mission AARs GO | Review AAR readiness | Yes |
| Phase exit criteria met | This doc's phase exit gate | Yes — operator approval |
| Degradation report all-True | `degradation_report(doc)` D-1/D-2/D-3 | Yes |
| Scope changes documented | Scope / Notes | Yes |

### Campaign Validation
| Check | Method |
|-------|--------|
| All 7 production suites + `canvas_std` green | Cross-producer no-regression run (P4) |
| Factory used end-to-end | `letter_generator` (and `post_generator`) built by following the skill/scaffold |
| Structural `iii/` review of new examples | `iii/` wrapper, target 0 High / 0 Med |
| Context graduation run | `skill_context_graduation` — update `context_canvas_producer_pattern.md` (letter/post mappings) |
| Doc currency | STATE.md + CLAUDE.md (Current state + skills inventory) + `what/production/README.md` + `how/skills/AGENTS.md` |

## Timeline

| Phase | Missions | Sessions |
|-------|----------|----------|
| P0 — Charter | P0.1 | ≤1 |
| P1 — Factory | P1 | 1-2 |
| P2 — Letter | P2 | 1-2 |
| P3 — Post | P3 | 2-3 |
| P4 — Close | P4 | 1-2 |
| **Total** | **5 missions** | **6-9 sessions** |

## Notes

- **Activation (2026-06-21):** operator ratified all 6 P0 decisions (defaults) at the P0→P1 gate
  (`session_stanley_20260621_234513_palette_p1_factory`); campaign `status: active`; Phase P1 opened.
- **Two-shelf doctrine:** `what/code/` = the Standard (immutable); `what/production/` = producers (depend on the
  installed `adna-canvas-std`). Both new producers + the scaffold live on the production shelf.
- **Factory-then-pilot:** P1 builds the skill + scaffold; P2 *uses* them to build letter — that build is the factory's
  acceptance test. If the skill/scaffold are awkward, fix them in P2 before P3.
- **Profiles producer-side:** `{"profile": "document"}` (letter) / `{"profile": "post"}` declared by the producer; no
  out-of-enum inline bindings (A-4 safe).
- **Deferred thesis legs:** this campaign completes the *output* leg only. Canvas-as-context-object and
  canvas-as-interface-surface (the other two legs the retrospective flagged as unexercised) are a candidate next
  strategic campaign — recorded here so the gap isn't lost.
- Technical designs (canvas mappings, `_reserved` enrichment, test plans) are carried into the P1/P2/P3 mission files
  at phase entry (SO-3), seeded from the approved plan + `context_canvas_producer_pattern.md`.
