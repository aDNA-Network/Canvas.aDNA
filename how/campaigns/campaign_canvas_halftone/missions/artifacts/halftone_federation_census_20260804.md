---
type: artifact
artifact_type: consumer_census
campaign_id: campaign_canvas_halftone
phase: HF
title: "Canvas federation wrapper census — fleet-wide, 2026-08-04"
created: 2026-08-04
updated: 2026-08-04
last_edited_by: agent_mondrian
status: active
method: "filesystem scan of */how/federation/*/ (+ Archive) filtered to canvas/canvasforge/canvas_*; every wrapper's federation_ref + frontmatter + body read; format per III's iii_consumer_census_20260704 precedent"
tags: [artifact, census, federation, wrappers, halftone, hf, g8]
---

# Canvas Federation Wrapper Census — 2026-08-04

> The G8 evidence base for phase HF. Scan run 2026-08-04 (read-only, fleet-wide). Successor-facing index:
> [`how/federation/federation_index.md`](../../../../how/federation/federation_index.md) (the living document —
> update THAT, not this census; this artifact is the dated snapshot).

## 1. Headline (corrects the 2026-08-03 snapshot's *mechanism*)

**Counts confirmed: 14 Canvas-identity + 6 CanvasForge-identity wrappers + 1 empty (Bearly).** But the "6 target
legacy CanvasForge.aDNA" claim is imprecise: in **all six**, the machine-readable `federation_ref.source_vault`
(or `target:`) **already reads `Canvas.aDNA`** — the drift lives in **`wrapper_for:` frontmatter,
`substrate_pin:`, prose bodies, runtime/import paths, and live `~/aDNA/CanvasForge.aDNA/…` cross-references**
(now an archive shim). Refederation memos therefore ask for **identity + pin + path + dir-name refits**, not
target flips. Compliance summary: `source_vault` clean everywhere · **zero broken machine refs** · only
**Emacs** clean at v2.3.0 · **Oration has no wrapper at all** (the G7 incident's enabling condition).

## 2. Group A — Canvas-identity wrappers (14)

| # | Consumer · wrapper | Identity | Pin | Policy | Created/Updated | Verdict |
|---|---|---|---|---|---|---|
| 1 | `Emacs.aDNA/how/federation/canvas` | Canvas.aDNA | **2.3.0** (`adna_native`) | minor | 07-13 / 07-13 | ✅ **CLEAN — the reference wrapper** |
| 2 | `Network.aDNA/how/federation/canvas` | Canvas.aDNA | 2.2.0 | — | (no fm) | 🟡 pin lag |
| 3 | `aDNANetwork.aDNA/how/federation/canvas` | (no `wrapper_for`) | 2.2.0 | — | (no fm) | 🟡 pin lag; **rename-alias of Network** |
| 4 | `LatticeNetwork.aDNA/how/federation/canvas` | (title says Network) | 2.2.0 | — | (no fm) | 🟡 pin lag; **rename-alias of Network** |
| 5 | `GOTFN.aDNA/how/federation/canvas` | Canvas.aDNA | genesis (`surface_status: planned`) | minor | 07-18 / 07-18 | 🟢 genesis; current |
| 6 | `Home.aDNA/how/federation/canvas` | consumes "CanvasForge's canvas_core" | `builder_version: 1.0.0` | minor | 05-31 / 05-31 | 🟠 **STALE RUNTIME PATH** — imports via `../CanvasForge.aDNA/what/code` (shim) — highest functional risk |
| 7 | `WebForge.aDNA/how/federation/canvas` | `wrapper_for: Canvas.aDNA`; body says CanvasForge | 1.1.0 @ `3783f57` | minor | 05-21 / 05-21 | 🟠 stale body + old pin |
| 8 | `Websites.aDNA/how/federation/canvas` | (clone of #7) | 1.1.0 @ `3783f57` | minor | 05-21 / 05-21 | 🟠 **rename-alias of WebForge** |
| 9 | `ScienceStanley.aDNA/how/federation/canvas_deck` | Canvas.aDNA (M-PL2-reconciled) | ~1.0 | minor | 04-07 / **07-18** | ✅ reconciled (paths ls-verified) |
| 10 | `ScienceStanley.aDNA/how/federation/canvas_comic` | Canvas.aDNA (M-PL2-reconciled) | ~1.0 | minor | 04-15 / **07-18** | ✅ reconciled; ⚠ carries an **archive-only** `context_ref` (`CanvasForge…/comic_book_design/`) flagged for the M-PL3 resurrect decision |
| 11 | `ContextCommons.aDNA/how/federation/canvas_deck` | body cites live CanvasForge | ~1.0 | minor | 04-12 / 04-30 | 🟠 stale body (not M-PL2-reconciled) |
| 12 | `Videos.aDNA/how/federation/canvas_deck` | title "Videos → CanvasForge…" | ~1.0 | minor | 05-08 / 06-10 | 🟠 stale title/body |
| 13 | `VideoForge.aDNA/how/federation/canvas_deck` | (byte-identical to #12) | ~1.0 | minor | 05-08 / 06-10 | 🟠 **rename-alias of Videos** — *the Videos shim's named retire-condition is exactly this wrapper refederation (workspace router row)* |
| 14 | `Obsidian.aDNA/how/federation/canvasforge` | `wrapper_for: Canvas.aDNA` (reconcile note) | provisional ("verify at M09") | minor | 06-23 / 06-23 | 🟢 target reconciled; dir-name `canvasforge/` kept per their ADR-010; rename → `canvas/` flagged post-P3 |

## 3. Group B — CanvasForge-identity wrappers (6 — the refederation-memo set)

| # | Consumer · wrapper | Stale identity signal | Pin | Created | Verdict |
|---|---|---|---|---|---|
| 15 | `ZenZachary.aDNA/how/federation/canvas` | `wrapper_for: CanvasForge.aDNA` · `substrate_pin: "CanvasForge.aDNA v1.2"` · x-ref live CanvasForge | ~1.2.0 | 05-27 | 🔴 stale identity (visual_dna schema consumer) |
| 16 | `ZenZachary.aDNA/how/federation/canvas_comic` | same class | ~1.2.0 | 05-27 | 🔴 stale identity |
| 17 | `ZenZachary.aDNA/how/federation/canvas_deck` | same class | ~1.2.0 | 05-27 | 🔴 stale identity |
| 18 | `Astro.aDNA/how/federation/canvasforge` | `wrapper_for: CanvasForge.aDNA`; body "SiteForge…CanvasForge.aDNA" | 1.1.0 @ `3783f57` | 05-21 | 🔴 stale identity; **byte-identical clone pair with #19** |
| 19 | `SiteForge.aDNA/how/federation/canvasforge` | (canonical of the #18 clone) | 1.1.0 @ `3783f57` | 05-21 | 🔴 **rename-alias of Astro** |
| 20 | `SuperLeague.aDNA/how/federation/canvasforge` | body: "canonical forge `~/aDNA/CanvasForge.aDNA/`", "when CanvasForge graduates…" (`target: Canvas.aDNA` is already correct) | genesis-planning | 04-28 | 🔴 stale body; engagement-scoped (archives at W4) |

## 4. Group C — empty / absent

- `Bearly.aDNA/how/federation/canvas` — **EMPTY** (no CLAUDE.md/federation_ref). Seam DESIGNED at Bearly
  P4/M4.1 (`seam_canvas.md`); population is Bearly's call at their pace (their `how/federation/AGENTS.md`
  records the intent; source: Canvas.aDNA · Mondrian).
- `Oration.aDNA/how/federation/` — **NO canvas wrapper** (`git/` + `iii/` only). The G7 enabling condition:
  `canvas_oration_map.canvas` bypassed stages 3–5 entirely. → the adopt-a-wrapper memo.

**Not counted:** `Canvas.aDNA/how/federation/comfyui/` (reverse direction — Canvas *consuming* ComfyUI; 0.2.0 @
`a8a4356`, indexed in the federation index per Vulcan follow-up #3). Archive.aDNA holds no consumer wrappers
(only the archived predecessors themselves).

## 5. Pin distribution

**2.3.0** ×1 (Emacs) · **2.2.0** ×3 (the Network trio) · **~1.2.0** ×3 (ZenZachary) · **1.1.0** ×4
(WebForge/Websites + Astro/SiteForge pairs) · **~1.0** ×5 (SS ×2 · ContextCommons · Videos pair) · **1.0.0
builder** ×1 (Home) · **genesis/provisional** ×3 (GOTFN · SuperLeague · Obsidian). Version policy is `minor`
nearly everywhere — under `spec_federation_contract` §3, minor consumers may auto-adopt up to v2.3.0 **but a
major hop (1.x → 2.x) REQUIRES re-validation** through the 5-stage gate (incl. Amendment 1's visual gate) —
that is precisely what the refederation memos ask for.

## 6. Dedupe note (rename tails)

Astro≡SiteForge, Videos≡VideoForge, and Network≡aDNANetwork≡LatticeNetwork are **rename-pair/trio aliases**
(byte-identical or verbatim copies via workspace shims). The index carries each as ONE consumer with alias
rows; each memo covers its whole alias set so a refit lands once, not thrice.
