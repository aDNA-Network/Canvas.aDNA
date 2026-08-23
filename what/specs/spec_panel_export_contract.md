---
type: specification
spec_id: panel_export_contract
title: "Panel Export Contract — comic_render per-panel output surface"
version: "1.0"
status: active
created: 2026-08-22
updated: 2026-08-22
last_edited_by: agent_mondrian
consumers: ["Videos.aDNA (Iris) — first named consumer, seam_contracts_2026_08.md §1"]
source_of_truth: "what/production/comic_render/src/comic_render/ (dispatch.py, extract.py, compose.py) · canvas_core/print.py DPI policy"
tags: [spec, comic_render, panel_export, contract, federation, videos]
---

# Panel Export Contract v1.0

**Purpose.** Iris (Videos.aDNA, `coord_2026_08_20_iris_to_mondrian_panel_export_contract.md`) asked whether
three properties of `comic_render`'s per-panel output are *contract* or *convention*. This spec promotes them
to **contract** — it changes no code; it writes down what the implementation already does and binds Canvas to
version-bump this spec before changing any of it. Verified against the H3 first-light corpus
(`what/artifacts/h3_first_light/`, 27 panels, export report 0 warnings) on 2026-08-22.

## 1. Scope

Covers the **per-panel raster output** of the `comic_render` pipeline (the 7-stage render bridge) and the
**per-page composite output**. Explicitly out of scope, Videos-owned by their own declaration: video frame
targets (1080×1920), timeline/sequence schema, encoding. No video-aware export mode exists or is planned —
the seam is correct precisely because it is thin.

## 2. Contract terms

### 2.1 Filenames (CONTRACT)

```
runs/<comic_id>/<panel_id>_v<n>.png          # per-panel variants, n = 1..N (1-based)
runs/<comic_id>/pages/<comic_id>_<page>.jpg  # per-page composites
runs/<comic_id>/pages/export_report.md       # export evidence (sizes, colour, warnings)
runs/<comic_id>/selections/...               # selection sidecars (RLHF seam; not for consumers)
```

- `<panel_id>` is structured: `spread<S>_page<P>_p<K>` (spread index, page-within-spread, panel-within-page;
  all 0-based, **unpadded**). H3 examples: `spread0_page1_p2_v3.png`.
- `<n>` is the variant index, 1-based, unpadded.
- Format: panels are **PNG**; page composites are **JPG** (RGB unless CMYK export is requested and
  reproducible).

### 2.2 Ordering (CONTRACT, with one warning)

- **Authority for reading order is the render manifest / source canvas**, not the filesystem: explicit
  reading-order edges in the canvas's `_reserved` block when present, else geometric fallback (sort by `y`,
  then `x`) — `extract.py:_reading_order`.
- The `panel_id` components (`S`, `P`, `K`) are **faithful to that order** — parsing the three integers and
  sorting numerically `(S, P, K, n)` reproduces reading order. **This numeric derivation is contract.**
- ⚠ **Lexicographic filename sort is NOT contract**: indices are unpadded, so string ordering breaks at
  double digits (`spread10` < `spread2`). Consumers MUST sort on parsed integers (or consume the manifest),
  never on raw string order.

### 2.3 Resolution floor (CONTRACT)

- **Per-panel:** panels are generated at the backend's native size for the requested aspect ratio; for the
  current hybrid chain (Gemini `image.pro` generate) that is **2048×2048 at 1:1** (H3 evidence), and
  ≥ **1024 px on the short edge is the guaranteed floor** for any aspect. Ken-Burns crops into a 2048-class
  panel reach 1080×1920 output comfortably.
- **Per-page composites:** **300 DPI target, 200 effective-DPI floor** (`canvas_core/print.py` DPI policy,
  declared at Halftone H6) — a panel whose source falls below 200 effective DPI raises an export warning.
  H3 pages: 2062×3150, 0 warnings.
- A future backend change that lowers the panel floor is a **breaking change to this spec** (major bump +
  consumer memo before it ships).

### 2.4 Corpus location (INFORMATION, per ADR-010)

`runs/` output under `what/artifacts/` is **node-local by ruling** (`adr_010_artifact_corpus_policy.md`):
gitignored, canonical on this node, backup-registered, **no off-node fetch path promised**. Consumers that
need pixels off-node name their own corpus location and copy at their seam (Iris's X1 mitigation is the
endorsed pattern).

## 3. Change discipline

This spec follows the federation version policy (`spec_federation_contract.md` §3): additive changes are
minor bumps; any change to §2.1–§2.3 terms is a major bump preceded by a memo to every consumer named in
frontmatter. Consumers pin `version: "1.0"` in their wrapper/seam records.
