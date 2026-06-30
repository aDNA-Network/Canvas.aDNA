---
type: review
created: 2026-06-22
updated: 2026-06-22
status: active
last_edited_by: agent_stanley
reviewer: iii (structural)
campaign: campaign_canvas_palette
tags: [iii, review, canvas, palette, letter, post, structural]
---

# III structural review — Operation Palette producers (letter + post)

Structural review of the two net-new Operation Palette producers + their worked examples, via the `iii/` wrapper
(structural lens; pixel/visual-render scoring stays PT-P5-gated). Scope: `letter_generator` + `post_generator` and
their example canvases. Consistent with the Atelier review (`iii/feedback_2026_06_21_atelier_producers.md`).

## Artifacts reviewed
- `what/production/letter_generator/examples/example_letter.canvas` (10 nodes / 8 edges; one-page letter).
- `what/production/post_generator/examples/example_post_single.canvas` (2 nodes / 0 edges).
- `what/production/post_generator/examples/example_post_thread.canvas` (5 nodes / 3 edges; 3-panel thread w/ 1 image).
- The producers' `iii_quality_contract.md` (letter: correctness·tone·legibility·rigor·accuracy; post:
  correctness·hook·platform-fit·rigor·accuracy).

## Findings

**0 High · 0 Med.**

Lows / notes (non-blocking):
- **L1 (letter):** `text`-block geometry uses a rough line-count heuristic (`layout.py`); pixel-accurate fit is
  PT-P5 render-scoring territory, not structural. No action.
- **L2 (post):** `char_budget` is advisory (carried in `component_types[post_root].qualities`), not enforced as
  truncation — correct per the contract (a quality dimension, not a baseline constraint). No action.
- **L3 (post):** image panels are `text` placeholders carrying `qualities.image_prompt` (no render) — correct C8
  boundary (ComfyUI owns pixels); flagged only so a future render wiring knows where the prompt lives.

## Conformance checks (structural)
- Both producers emit **aDNA-Native**; `validate(...) == []`; `validate_suite` `meets_declared`/`ok`.
- Exactly one canonical surface each (A-5), id resolves to a node; `component_types` keys ⊆ node ids.
- Degradation D-1/D-2/D-3 all True; `strip` → CORE + EXTENDED valid (degrades to a plain Obsidian canvas).
- `post_generator` thread chain uses `sequence` (linear, acyclic) + `adjacency` for post→image; `letter_generator`
  uses `reading_order` down the blocks.
- **Firewall:** `canvas_std` git-diff 0 — no Standard touch.

## Verdict
**SHIP.** Both producers are structurally conformant and degrade cleanly; the family (7 producers) passes the
cross-producer sweep (305 passed). Pixel/visual review deferred to PT P5 per doctrine.
