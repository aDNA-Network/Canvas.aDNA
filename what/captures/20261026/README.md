---
type: capture_note
created: 2026-10-26
updated: 2026-10-26
status: active
last_edited_by: agent_mondrian
tags: [capture, build_report, vernier, p3, dual_channel, source_sha256]
---

# Captures — 2026-10-26 (for the human build report)

## `context_canvas_surface_legs_geometry.png`

- **What it is:** `what/context/context_canvas_surface_legs.canvas` as it stands at `a881ceb`. That is one of the two dual-channel canvases regenerated at `8191348` (Vernier P3 objective 2), now carrying `_reserved.sync.source_sha256`. It is drawn **at its own geometry**: 16 nodes at their `x/y/width/height`, the `diagram_root` group behind them, and 15 edges as straight lines between their named sides.
- **What it is not:** an Obsidian render. Text is shown as source (markdown not rendered), so the `mermaid_src` node shows its Mermaid source. Edge labels are not drawn, because they live in the Mermaid source and in `_reserved.panel_link`.
- **How it was made:** a scratch script, not vault tooling. It wrote a self-contained HTML page with no scripts, and headless Chromium (anaconda Playwright) screenshotted it from `file://`. **Every non-`file://` request was routed to abort; 0 were attempted.** 1786×2005 px, 204349 B, md5 `364cd8873bccf73c7339de9ffac63865`.
- **Why not the vault's own render path:** `canvas_core.html_renderer` (via `visual_inspector.prepare_screenshots`) is deck-oriented. It lays the nodes out as a slide grid without geometry or edges, and its page loads Mermaid from a CDN, which an offline capture cannot use. A first attempt through that path did fetch it, and is recorded in `session_stanley_20261026_093240_d1_obj3`. The vault's sight-certified render remains the Obsidian window capture (`canvas_core.visual_capture`), which was not used, because it drives the desktop.
- **Made in:** `session_stanley_20261026_093240_d1_obj3` (Mondrian, under the Automator day-order grant D1-J).
