---
type: context_guide
topic: canvas
subtopic: topology_graphs
created: 2026-06-24
updated: 2026-06-24
sources: ["Operation Prytaneion Phase 2 (Home.aDNA topology-canvas exemplar)", "Home.aDNA/what/context/context_canvas_design_research.md", "arXiv 1209.4227", "USPTO 10424096", "Holten edge bundling", "Sugiyama layered drawing", "Wong/ColorBrewer", "Cleveland-McGill"]
context_version: "1.0"
token_estimate: ~3200
last_edited_by: agent_hestia
tags: [context, canvas, graph, topology, node_link, edge_routing, prytaneion, contributed]
---

# Canvas: Node-Link / Topology Graphs

> **Contributed by Home.aDNA (Hestia) — Operation Prytaneion M6.3.** The existing `advanced_canvas/` corpus is strong but **deck/slide-centric** (color/WCAG/CVD, typography, Tufte, composition). This chapter adds the **node-graph-specific** layer those docs leave as gaps. Every recommendation carries a **worked example** from Home's 94-node `topology.canvas` (the live fleet map: 54 vaults over the WHO/WHAT/HOW triad, 8 category bands), which Prytaneion Phase 2 raised to an exemplar bar.

## Key Principles

1. **Edge-crossing minimization is the dominant readability lever.** Crossing number, swing amplitude, and short-edge preference predict legibility more than any cosmetic choice. Fix crossings *first*.
2. **On a generated `.canvas`, the lever is node placement + edge dimming — NOT routing.** (The hard-won constraint; see Anti-Patterns.) Advanced Canvas styles loaded edges but **does not recompute pathfinding for edges authored outside its own UI.** Plan your readability budget around placement, not orthogonal routes.
3. **Categorical = hue; ordinal/state = luminance.** One base hue per category (cap ~6–8, then add a second channel), state on a single-hue light→dark ramp. Never encode ordered state with rainbow hue (Cleveland–McGill: position > length > … > luminance > hue).
4. **Enclosure beats proximity beats similarity (Gestalt).** A *manually-laned* canvas with bounded regions reads as grouped far better than a force layout — which is exactly why curated dependency graphs should be laid out, not simulated.
5. **Size encodes topological importance.** Hubs/roots larger than leaves (degree/centrality → area).

## Recommendations (the 10 gap items)

### 1. Crossing reduction (orthogonal routing → placement de-spaghetti)
Ideal is orthogonal/right-angle routing along shared tracks. **On agent-generated canvases that is not achievable** (constraint below), so reduce crossings by **layout** instead: (a) order category bands so the densest edge flows are adjacent; (b) within a band, sort nodes by **barycenter** of their neighbors; (c) dim the high-volume edge class at rest.
- **Worked example (M2.2):** band reorder + within-band barycenter + federation-edge dimming took the fleet map from **154 → 85 crossings (−45%)** with zero routing changes. Placement floors at ~85; the dimming carries the rest of the readability.

### 2. Edge bundling (+ the ambiguity tradeoff)
Bundle many-to-one flows (consumers → a hub) into trunks **only on the dense layer**, never on sparse relations. Bundling trades clutter for **ambiguity** (you lose which-connects-to-which) and reduces angular resolution — use ambiguity-aware/straightenable bundling + link-fanning at endpoints.
- **Worked example:** the 34 federation edges converge on hubs (III, Astro, Canvas); they are the *only* bundle/dim candidate. The 4 kinship + succession/sequencing edges stay crisp and unbundled.

### 3. Opacity-by-focus + weighted stroke
Resting state: dim the high-volume edge class to ~15–25%. On hover/select: spotlight that node's edges, fade the rest. Weight by importance (thick primary, hairline incidental); when >4 lines overlap, reveal one at a time.
- **Worked example (M2.2):** federation edges dimmed at rest (`#3a5a6b`) is what makes the 85-crossing map *read* clean — the single highest-leverage cosmetic move after placement.

### 4. Gestalt enclosure (swimlane / common-region)
Bound each category as a closed region (a GROUP / tinted band), and give the canvas one **persistent orientation rail** rather than a floating legend.
- **Worked example (M2.2 S2):** the legend moved from a free node on the far right → a bounded **"Legend · how to read this canvas" GROUP** anchored beneath the WHO/WHAT/HOW triad — one common-region rail that reads via adjacency + shared column.

### 5. State-luminance ramp doctrine
Within each category hue: **active = full · genesis = mid · pending = desaturated · not-instantiated = ghost.** This is the dataviz-correct ordinal channel and belongs in the standard as doctrine (the prior corpus documents palette *types* but no state ramp).
- **Worked example:** node fills carry category hue; status pills + luminance carry state — so a band of vaults reads category-at-a-glance and maturity-on-inspection.

### 6. Graph-hub sizing (degree → size)
Size nodes by degree/centrality so hubs are visually dominant. Use discrete tiers (not continuous) to stay legible.
- **Worked example (M2.3):** a shelf-packer with three tiers — **hub 256×132 · standard 204×108 · leaf 176×96** — makes the high-degree hubs (the frameworks/platforms many vaults federate against) pop without a layout engine.

### 7. Swimlane / snap-grid (Sugiyama) layout
Place nodes in horizontal registers (layered drawing), uniform gutters, snap-grid to kill jitter. Crossings minimized by band order + within-band barycenter (#1).
- **Worked example:** 8 category bands + 3 triad lanes (WHO/WHAT/HOW) on a consistent gutter/grid = the canonical layered view.

### 8. Force-directed vs layered (decision guidance)
**Layered/curated is canonical** for a dependency ladder (imposed structure = meaning). Force-directed destroys imposed structure (proximity ≠ similarity) but reveals emergent clusters — offer it as a **toggle/explore view only**, never the default for a governance graph.

### 9. Graph legend / left-rail / direct-labeling
Prefer **direct labeling** (surface edge-type meaning on hover) over legend lookup; keep the edge-type key + triad in the persistent rail (#4). Externally-generated edges can't carry rendered routing, but they *can* carry labels + dash/arrow styles (once AC's `edgesStylingFeatureEnabled` is on).

### 10. Minimap / large-canvas navigation
A satellite/minimap is what makes a 90+-node canvas orientable. **Honest status: not achievable in current Obsidian + Advanced Canvas** (no minimap surface) — parked for the Obsidian.aDNA plugin campaign. Until then, the persistent left-rail (#4) + band structure is the orientation substitute.

## The generated-canvas constraint (read this first)

**The single most important lesson Home learned, and the one most likely to save the next producer weeks:**

> Advanced Canvas (v6.1.4) + the JSON Canvas format **do** support `pathfindingMethod` / `path` (dash) / `label` / styled `arrow` — but AC **does not recompute pathfinding routing for edges authored outside its own UI.** It applies line-styles + labels to loaded edges; it does **not** reroute them. Emitting `pathfindingMethod="square"` yields correct JSON and a better attach-side metric, but the rendered edges **stay diagonal**. (Also: AC must be *configured* — `edgesStylingFeatureEnabled`, off by default — for even dash/label styles to apply.)

**Implication for any `canvas_std` producer that emits a node-link graph:** do not budget readability on orthogonal routing. Budget it on **node placement (band order + barycenter) + edge dimming + tiered sizing + a persistent rail.** Those are fully under a generator's control and delivered Home's −45% crossing reduction. The open solution space (reroute-on-load trigger · bake computed routes as edge geometry · node-placement bezier de-spaghetti) is owned by the Obsidian.aDNA plugin campaign.

## Anti-Patterns

- **Trusting `pathfindingMethod` on a generated canvas** to straighten edges — it won't render (above). Place nodes instead.
- **Bundling sparse relations** — only the dense hub-convergent layer should bundle; bundling kinship/succession destroys the which-connects-to-which you need.
- **Rainbow hue for state** — state is ordinal → luminance ramp, not hue.
- **>8 categorical hues** — cap ~6–8 (Wong/ColorBrewer), then add shape/border/icon as a second channel.
- **Brand accent as node/edge text** — e.g. `#663399` is 2.03:1 on `#1a1b26`; chrome/focus only, never text (carry the existing `color_accessibility.md` audit into graphs).
- **Force layout as the default** for a curated dependency graph — it erases the structure that *is* the message.

## Visual-in-the-loop (companion capability)

No node-link canvas should ship without an **agent-confirmed render**. Home's Prytaneion M1.1 hardened a live-Obsidian variant of the visual loop: *design → render in live Obsidian → screenshot (non-disruptive) → agent reads the image → edit → re-render.* The standard it establishes: **"no canvas ships without an agent-confirmed Obsidian screenshot."** Capability detail + the producer-side playbook: see `context_canvas_visual_in_the_loop.md` (companion, contributed alongside this chapter).

## Sources

**Worked examples:** Home.aDNA Operation Prytaneion Phase 2 — `mission_p2_m2_1_color_edge_despaghetti.md` (F-M2.1-A/B/C, the generated-canvas constraint), `mission_p2_m2_2*` (band reorder + barycenter + dimming + legend rail; 154→85), `mission_p2_m2_3*` (degree-tiered re-pack). Grounding research: `Home.aDNA/what/context/context_canvas_design_research.md`.
**External:** arXiv 1209.4227 (ordered-bundle routing) · USPTO 10424096 (orthogonal routing) · Holten hierarchical edge bundles · UC Davis ambiguity-free bundling · Sugiyama / layered graph drawing · Wong / ColorBrewer Set2 · Cleveland–McGill encoding hierarchy · Cambridge Intelligence (force vs layered) · Cytoscape navigation.
**Internal (this vault):** `advanced_canvas/` corpus (`color_accessibility`, `data_visualization`, `diagram_patterns`, `design_tufte`, `composition_patterns`).
