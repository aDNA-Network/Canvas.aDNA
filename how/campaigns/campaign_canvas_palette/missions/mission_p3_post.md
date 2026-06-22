---
plan_id: mission_p3_post
type: plan
title: "P3 — post_generator (single + thread; the multi-panel path)"
owner: stanley
status: completed
campaign_id: campaign_canvas_palette
campaign_phase: 3
campaign_mission_number: 4
mission_class: build
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, production, palette, post, social, producer]
---

# Mission: P3 — post_generator (single + thread)

**Campaign**: [[how/campaigns/campaign_canvas_palette/campaign_canvas_palette|campaign_canvas_palette]]
**Phase**: 3 — Social post producer
**Mission**: 4 of 5

## Goal

Build `what/production/post_generator/` on `canvas_std` via the factory — a social-post producer covering a **single
post** and a **thread**, emitting aDNA-Native, with image prompts as metadata (never rendered). Exercises the
multi-panel/`sequence` path the letter (single-surface) didn't.

## P3a — Post model (producer-side; not a Standard spec)

Settled from P0 D4:
- **Shape:** one canonical `group` surface `post_root` holding **post panels**. A single post = 1 panel; a **thread**
  = N panels chained by `sequence` edges (strictly linear, **acyclic** — A-5 safe; `isStartNode` on panel 0).
- **Panel:** a baseline `text` node `post{i}` (the copy), `class: text`, `semantic_type: post_copy`. An optional
  image rides as a **separate** `image`-class node `img{i}` (`type: text` placeholder carrying alt text;
  `degrades_to: text`; the prompt in `qualities.image_prompt`) linked to its post by an `adjacency` edge. The producer
  **never renders** (ComfyUI owns pixels, C8).
- **Platform profiles (producer-side):** a `PLATFORM_PROFILES` table (`twitter`/`x`·`linkedin`·`instagram` →
  `char_budget` + `aspect`) carried in `component_types[post_root].qualities` (`platform`, `char_budget`, `aspect`).
  `semantic_bindings` stays the bare `{"profile": "post"}` (A-4 safe; platform never goes in semantic_bindings or
  `canvas_std.schema`). Char budget is **advisory** (a quality-contract dimension), not hard-enforced.
- **Region:** `post_root` `{flow: vertical, pagination: "none", surface: "social_post"}` — no `extent` (a post is not
  paginated; AT-1 says omit `extent` when no unit fits; `panels` is not a `PL_EXTENT_UNITS` member).

## Exit Gate (P3→P4, HUMAN)

Full post four+1 suite green + `ruff` clean; both worked examples (single + thread) validate `adna_native [OK]` and
degrade (D-1/D-2/D-3); thread `sequence` chain is acyclic; firewall `git diff --stat -- what/code/canvas_std/` empty;
AAR GO. **HELD before P4 (close).**

## Objectives

### 1. Build post_generator
- **Status**: completed
- **Session**: session_stanley_20260622_003226_palette_p3_post
- **Description**: Clone `_scaffold` → `post_generator`; `model.py` (`Post` + `PostPanel` + `PLATFORM_PROFILES` + `load_post`); `consume.py` (`build_post`: `post_root` surface; `post{i}` copy nodes; optional `img{i}` image nodes w/ `qualities.image_prompt`; `sequence` thread chain + `adjacency` post→img; platform qualities); `layout.py`; CLI.
- **Files**: `what/production/post_generator/**`
- **Depends on**: none

### 2. Tests + worked examples
- **Status**: completed
- **Session**: session_stanley_20260622_003226_palette_p3_post
- **Description**: four+1 suite + a `test_post` coverage test (single = 1 panel/0 sequence edges; thread = N panels/N-1 sequence edges, acyclic, isStartNode on 0; image panel carries `qualities.image_prompt` + no file render; platform char_budget applied). Two examples: `example_post_single.yaml`, `example_post_thread.yaml` (one with an image). venv + `pytest` green; `ruff` clean; `canvas-std validate` → `adna_native [OK]`.
- **Files**: `what/production/post_generator/tests/**`, `examples/**`
- **Depends on**: 1

### 3. Verify
- **Status**: completed
- **Session**: session_stanley_20260622_003226_palette_p3_post
- **Description**: Firewall empty; degradation all-True on both examples; fold any factory friction back into P1 artifacts. HOLD at P3→P4.
- **Files**: (verification)
- **Depends on**: 1, 2

## Campaign Context

### Previous Mission Outputs
- P1 factory + P2 `letter_generator` (single-surface exemplar). P0 D4 settled the post model (above).

### Next Mission Inputs
- P4 — cross-producer sweep (now 7 producers) + `iii/` review + context graduation + close.

## Notes

Post is the multi-panel/thread path (letter was single-surface). `sequence` is acyclicity-checked — keep the thread
strictly linear. Image is metadata-only (C8). Firewall: never edit `canvas_std`.

## Completion Summary

### Deliverables
- **`what/production/post_generator/`** — net-new social-post producer on `canvas_std`: `model.py` (`Post`/`PostPanel` + producer-side `PLATFORM_PROFILES` + `load_post`), `consume.py` (`build_post`: `post_root` canonical surface; `post{i}` copy nodes chained by `sequence`; optional `img{i}` image-class nodes carrying `qualities.image_prompt`; `adjacency` post→img; platform qualities; `isStartNode` set post-hoc on `post0`), deterministic `layout.py`, `post-generator` CLI.
- **Suite green: 20 passed**, `ruff` clean. Two worked examples — `example_post_single.yaml` (2 nodes/0 edges) + `example_post_thread.yaml` (5 nodes/3 edges incl. an image) — both validate **`adna_native [OK]`** + degrade (D-1/D-2/D-3). **`canvas_std` firewall git-diff 0.**
- Post-specific `README.md` / `AGENTS.md` / `iii_quality_contract.md` (lenses: correctness · hook · platform-fit · rigor · accuracy).

### Descoped
- None. Char-budget enforcement stays advisory (a quality-contract dimension, not baseline truncation).

### Key Findings
- The multi-panel/thread path reused the proven contract 1:1; `sequence` for the (linear, acyclic) thread + `adjacency` for post→image; image as a `qualities.image_prompt` text-placeholder (no render, C8) mirrors the comic producer.
- **The skill's "set Advanced fields post-hoc" note earned its keep:** `to_canvas` drops source-only fields, so `isStartNode` must be set on the output node after `to_canvas` — initially mis-set on the source node, a test caught it.

### Scope Changes
- None. Built directly (not delegated) after the P2 build-agent session-limit interruption.

## AAR

- **Worked**: building directly off the `letter_generator` exemplar + the factory skill made the larger (multi-panel) producer fast and green; tests caught both the `isStartNode` placement bug and a `"post_root".startswith("post")` test-filter bug immediately.
- **Didn't**: first run had 3 reds — one real (`isStartNode` pre-`to_canvas`), two test-only (root-group counted as a panel); all fixed in one pass.
- **Finding**: the factory generalizes from single-surface (letter) to multi-panel/thread (post) with no new substrate need — the Standard still needed zero changes (7 producers, firewall git-diff 0).
- **Change**: none to the factory; the skill's post-hoc-Advanced-fields guidance is validated (keep it prominent).
- **Follow-up**: P4 — cross-producer sweep (7 producers + `canvas_std`) + `iii/` review + context graduation + close ([[how/campaigns/campaign_canvas_palette/missions/mission_p4_close|mission]]).
