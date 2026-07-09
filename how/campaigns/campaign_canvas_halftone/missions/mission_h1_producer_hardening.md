---
type: mission
mission_id: mission_h1_producer_hardening
campaign_id: campaign_canvas_halftone
phase: H0-H1
status: completed
owner: stanley
persona: Mondrian
created: 2026-07-09
updated: 2026-07-09
last_edited_by: agent_mondrian
tags: [mission, halftone, h1, comic_generator, prompt_layers, validation, adr-port, prompt-contract]
---

# Mission: Operation Halftone — H0 charter + H1 producer hardening & governance rail 1

## Intent

Charter the campaign + file the review (H0), then close gap **G5** (producer validation gaps) and the H1 half of
**G6** (governance tail) — making `comic_generator` bridge-ready. The `prompt_layers` split is the **contract
prerequisite** for the H2 render manifest (ComfyUI needs a separate negative channel; photorealistic registers need
a configurable negative suffix). Zero `canvas_std` touches.

## Objectives

| # | Objective | Status |
|---|-----------|--------|
| **O1** | H0 — charter `campaign_canvas_halftone` (master + CLAUDE.md) + file `halftone_{gap_register,roadmap}.md` + STATE reconcile | ✅ |
| **O2** | `qualities.prompt_layers` — additive structured emission alongside `image_prompt`; negative configurable via `ComicInput.negative_suffix`; join-invariant locked; example regenerated (9/9 panels carry it; validates aDNA-Native, D-1/2/3) | ✅ |
| **O3** | Validation: `image_path` existence (`load_comic` warns; CLI `--strict-paths` fails) · `spread_number` vs declared spreads (+ dangling declared pages) · splash+N-panels warns · `story_state` unknown-character warns | ✅ |
| **O4** | Tests: `test_hardening.py` (+13) — layers/negative/validations/RLHF-E2E/full-span; **suite 87 → 100**; RLHF hints threaded end-to-end through `build_comic` (register + hint kwargs; the dormant path is now activatable) | ✅ |
| **O5** | Governance 1: **consolidated adoption** — `adr_008_comic_render_doctrine.md` re-anchors CF ADR-003/005/008's operative decisions (provenance + supersession map; stale mission machinery retired) — one live cite instead of three 250-line verbatim ports; Mermaid-dup + prompt_layers notes in `AGENTS.md` | ✅ |
| **O6** | `what/docs/comic_prompt_contract.md` — canvas locations · 6-layer table · `prompt_layers` channel contract (negative→CLIP encode) · dual-prompt PART 1/2/3 · aspect derivation · manifest forward-contract | ✅ |
| **O7** | Verified: 7 producers **236 passed** (brief 10 · deck 16 · document 37 · diagram 36 · **comic 100** · letter 17 · post 20) + `canvas_std` **115/10** + **firewall diff empty**; AAR below; SITREP + HOLD at H1→H2 | ✅ |

## Notes

- **Additive only**: `prompt_layers` rides beside `image_prompt` (no consumer breaks); validation failures are
  warnings by default with a strict mode — existing example inputs must stay green.
- Ported ADRs continue Canvas-local numbering (next free `adr_00N`) and carry `ported_from:` provenance frontmatter;
  the archive originals stay read-only (SO-6).
- The prompt contract doc is production-side documentation (not a spec; graduates via LIP only if it ever needs
  Standard status).

## AAR

- **Worked:** the `prompt_layers` design (dict-of-channels built first, `text` joined from it) made the
  back-compat guarantee *structural* — the join-invariant test proves assembled and structured forms can never
  disagree, and all 87 prior tests passed untouched. Guard-rails-as-warnings (splash, story_state) tightened
  authoring without breaking any legal input; the spread cross-check only arms when spreads are declared.
- **Didn't:** the plan's "port 3 quarry ADRs" became **one consolidated adoption ADR** (adr_008) — verbatim ports
  would have dragged ~700 lines of dead CanvasForge mission machinery (ContextPack gates, never-built v1.1
  orchestrator, per-mission SHAs) into live governance. Deviation judged better-than-plan; provenance +
  supersession map preserve the audit trail; archive originals stay the full record.
- **Finding:** the RLHF-hints path was doubly dormant — hints kwargs existed on `build_panels` but `register` was
  never threadable and `build_comic` accepted none of the three, so the mechanism was unreachable from the top-level
  entry. Now threaded end-to-end (default-inert) + E2E-tested; the H2 bridge can activate it without producer edits.
- **Change:** comic suite 87 → **100**; producers total 223 → **236**; the example canvas now ships `prompt_layers`
  on all 9 panels; `negative` is instance data (photorealistic registers unblocked); Canvas has a live render
  doctrine (adr_008) + a handable prompt contract for the Vulcan memo.
- **Follow-up:** H2 builds `comic_render` against `comic_prompt_contract.md` §6 (manifest fields already named);
  the quarry `canvas_comic` disposition (its duplicate parser + 99 tests) is the H6 gate; ADR-004/006/007
  (visual-QA/RLHF loop) dispositions ride the H6 RLHF-seam doc.
