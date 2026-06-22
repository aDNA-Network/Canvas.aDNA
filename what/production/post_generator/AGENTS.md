---
type: directory_index
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [directory_index, canvas, production, post, social, producer]
---

# `post_generator/` — social-post producer (Operation Palette P3)

A net-new producer on `canvas_std`: a `Post` (single post or thread) → a v2.0.0 aDNA-Native social-post `.canvas`.
Built off the `_scaffold` factory; the multi-panel/thread companion to `letter_generator` (single-surface).

- **Pipeline:** `model.py` (`Post`/`PostPanel` + `PLATFORM_PROFILES`) → `consume.py` (`build_post`: `post_root` surface;
  `post{i}` copy nodes chained by `sequence`; optional `img{i}` image nodes carrying `qualities.image_prompt`;
  `adjacency` post→img) → `_reserved` enrich. CLI: `post-generator build <in> <out>`.
- **Tests:** four+1 + `test_post` (single vs thread, sequence chain acyclicity, image-as-metadata, platform profile).
- **Quality:** `iii_quality_contract.md` (a contract; review via the `iii/` wrapper).

Doctrine (SO): never edit `what/code/canvas_std/` (firewall — `git diff --stat` 0); profile + platform table stay
producer-side (never in `canvas_std.schema`); image is metadata only — emit `qualities.image_prompt`, never render
(C8; ComfyUI owns pixels). `sequence` is acyclicity-checked — keep the thread strictly linear. Pattern:
`what/context/context_canvas_producer_pattern.md`.
