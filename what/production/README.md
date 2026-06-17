---
type: context
created: 2026-06-17
updated: 2026-06-17
status: active
last_edited_by: agent_stanley
tags: [canvas, production, deck, comic, diagram, pt09, canvasforge_merge]
---

# Canvas.aDNA — Production Layers (deck · comic · diagram)

**Origin:** absorbed from `CanvasForge.aDNA` at Production Tidy **pt09** (2026-06-17), reversing the E3.4 federated-producer split. Hermes (CanvasForge) merged into **Mondrian**; Canvas.aDNA now owns the Standard **and** its production.

## Status: governance merge landed; code arrives at P5

pt09 is a **governance merge** (mirrors pt08 Layer-1/Layer-2). Canvas owns the production layers as of pt09; the **code has not yet moved** — it stays in the archived source and relocates here in Production Tidy **P5**:

| Layer | Code (relocates P5 → here) | P5 source location |
|---|---|---|
| deck | `canvas_presentation/` | `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_presentation/` |
| comic | `canvas_comic/` (9 py) | `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_comic/` |
| diagram + core | `canvas_core/` (80 py) | `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_core/` |

**In-code shim:** `canvasforge.canvas_core → canvas_std` (deprecation re-export, grace to 2027-06-13) folds into the merge — registered in the Home.aDNA §C shim ledger (#29), owner Mondrian, 12-mo window.

**Consumer wrappers:** ~8 vaults / ~11 wrappers federate to `CanvasForge.aDNA` (`source_vault: CanvasForge.aDNA`). They resolve via the merge-archive shim (`~/aDNA/CanvasForge.aDNA → Archive.aDNA/CanvasForge.aDNA`) until **P5 wrapper-refederation** repoints them to Canvas.

**Keystone interaction:** Operation Keystone (active, held E3→E4) is reconciled by Mondrian — the "CanvasForge as separate federated producer" premise is folded; E4's net-new-consumer + LF-successor work continues in-vault.

Producer knowledge (typography · color · composition · scoring · the courier-loop) is preserved verbatim in the archived source: `Archive.aDNA/CanvasForge.aDNA/`.
