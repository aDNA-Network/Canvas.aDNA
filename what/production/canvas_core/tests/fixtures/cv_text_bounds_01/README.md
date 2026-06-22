# CV-TEXT-BOUNDS-01 Fixture: SS Issue 01 Page 1

Evidence-only copy of Science Stanley Issue 01, page 1 (Cover Matter).

## Provenance

- **Source**: `lattice-labs/how/pipelines/pipeline_comic_production/05_generate/issue_01_review_with_text.canvas`
- **Extracted**: 2026-04-22 during M-1-07 (CV-TEXT-BOUNDS-01 trap implementation)
- **Subset**: Page 1 group (`01c9bf5bd8ee8c15`, 662.5x1025) + spatially contained children
- **Purpose**: Demonstrate trap firing on known M01 failure mode (text overflow in 200x40 boxes)

## Known Findings

The page 1 text nodes (`**SCIENCE STANLEY**`, `**Issue 1: The Context of Context Graphs**`, `**Your friendly neighborhood AI scientist**`) are all declared at 200x40 px. The text content — even after markdown stripping — exceeds 200px width at any reasonable font size, triggering the overflow condition.

The file node (`page_01_panel_01.png`, 687.5x1050) also exceeds the parent group bounds (662.5x1025), but the text-bounds trap focuses on `type=="text"` nodes. File-node containment is a separate concern.
