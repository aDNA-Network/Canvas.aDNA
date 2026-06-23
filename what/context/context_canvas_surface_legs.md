---
type: context
subtype: context_guide
created: 2026-06-22
updated: 2026-06-22
status: active
last_edited_by: agent_stanley
context_version: "1.0"
token_estimate: ~2400
quality_score: 4.2
signal_density: 4
actionability: 5
coverage_uniformity: 4
source_diversity: 4
cross_topic_coherence: 4
freshness_category: stable
tags: [context, canvas, surface, context-object, interface, leg2, leg3, salon, guide]
---

# Canvas Surface Legs (context-object + interface)

How to exercise the **non-output** legs of the three-leg Canvas thesis (ADR-000): a canvas as a **context object**
(leg 2 — load + traverse without rendering) and a canvas as an **interface surface** (leg 3 — a `read → act → re-read`
interaction loop). Proven in **Operation Salon** (2026-06-22): leg 2 by the `what/code/canvas_context/` loader (28/28),
leg 3 by `spec_interface_surface.md` (ratified) + `canvas_context/interaction.py` v0.2.0 (the read-only POC, 50/50
total). Use this when building **any** read-as-context or interaction-surface capability over `canvas_std`.

## Key Principles

1. **Compose, don't extend.** To add a capability over the immutable `canvas_std`, make the new package a *has-a*
   **consumer** that imports `canvas_std` read-only (via pytest `pythonpath`, **never** an editable install — `-e`
   writes `*.egg-info` into the frozen tree). `canvas_context` *has-a* the Standard's public API; the leg-3
   `InteractionSurface` *has-a* a `ContextGraph`. The dependency is one-way (`consumer → canvas_std`). This keeps the
   two-shelf firewall (D6) at **git-diff 0 for free** — verify `git status -s -- what/code/canvas_std/` is clean at
   every gate. (Contrast the producer pattern, which depends on the *installed* `adna-canvas-std`; a context/interaction
   consumer resolves it via pythonpath so nothing installs into the immutable tree.)

2. **Load without rendering.** A canvas-as-context-object is a navigable **graph** (components · panels · edges · refs),
   not pixels. The loader parses structure into a `ContextGraph` and exposes `reading_order()` traversal **with no
   render pipeline invoked** — no rasterizer, image generator, or layout-to-pixels (PIL / cairosvg / torch never
   imported). `file` / `image` / `video` components are carried **by reference only**. The proof is loading a *real
   producer* `.canvas` (a known-good fixture), not a synthetic one.

3. **A view-only append-fold proves an interaction loop honestly.** An honest `read → act → re-read` loop wants a write
   — but you do not need the *authoritative* write to prove the loop. Model "act" as a **pure append-only fold** that
   advances the **view** (a re-read snapshot recomputed from the appended response), not the governed `.lattice.yaml`.
   The loop closes live; the governed round-trip write (`spec_roundtrip_protocol_v2`) stays cleanly out of scope and
   becomes the follow-on runtime's job.

4. **Spec the contract first-principles when the upstream doesn't exist.** Fix the **boundary ADR first** (what the
   surface owns vs neighbours + the future routing layer), then author the spec grounded on what you *have* (the
   boundary + the proven lower leg + an exemplar), scoped `v1`. Design a **semver re-anchor seam** (`interaction_version`)
   so a future upstream thesis re-aligns additively, not by re-litigation.

5. **Ride `_reserved` additively.** Both legs use the namespaced `_reserved` extension carrier
   (`doc["metadata"]["frontmatter"]["_reserved"]`). A canvas **without** `_reserved` MUST still load (degradation) — so
   no core-schema change, and a valid aDNA canvas always degrades to a valid baseline canvas.

## Recommendations

- **Package shape** (a read-only consumer of `canvas_std`):
  ```
  what/code/<consumer>/
    pyproject.toml   # name "adna-canvas-<x>"; dependencies = [] (stdlib + canvas_std via pythonpath);
                     # [tool.pytest.ini_options] pythonpath = ["src", "../canvas_std/src"]
    src/<consumer>/  model.py loader.py resolver.py traversal.py [interaction.py]
    tests/  test_pilot.py (the real-.canvas proof) + conformance suites + fixtures/
    AGENTS.md CHANGELOG.md README.md .gitignore   # .gitignore: .venv/ *.egg-info/ + any demo-generated fixture
  ```
- **Run with the substrate's venv** (no separate venv needed): `PYTHONDONTWRITEBYTECODE=1 ../canvas_std/.venv/bin/python -m pytest -q`.
- **Leg-2 loader = a normative pipeline.** Spec it as discrete load stages (Salon's **L1–L7**: read → parse → resolve
  `_reserved` → build components/panels → resolve edges → resolve refs → assert no-render) with a `Resolver` protocol
  for in-vault wikilinks + cross-vault `federation_ref` (delegate the fetch; never transport in the loader).
- **Leg-3 surface = five primitives.** `anchor` (named region; reuse `panel_link.anchors` + `validate_anchors`) ·
  `affordance` (declared interaction point) · `response` (logged submission) · `surface state` (the re-read snapshot) ·
  `turn` (one read→act→re-read cycle). Realize conformance (`I-1/I-2/I-3` structure + `I-D` round-trip-to-baseline) **in
  the consumer**, reusing `canvas_std.strip`/`validate`/`validate_anchors` — do not wire `I-*` into the `canvas_std`
  harness until a ratified decision lifts the firewall.
- **Keep the boundary fenced.** A surface consumer is **not** a capture runtime, renderer, transport, or cross-surface
  router (ADR-006 §2–§3). Expose refs/affordances and delegate; routing belongs to the OIP layer, the gate engine to
  ISS, pixels to ComfyUI.

## Examples / Snippets

```python
# Leg 2 — load a real producer .canvas as context, no rendering:
from canvas_context import load_context_graph
g = load_context_graph("…/document_generator/examples/whitepaper.canvas")
assert g.reading_order() == ["page0", "page1", "page2", "page3", "page4"]   # traversal, not pixels
# PIL / cairosvg / torch are never imported on this path.

# Leg 3 — the read → act → re-read loop (view-only fold):
from canvas_context import load_interaction_surface, apply_response
s0 = load_interaction_surface("…/interaction_review.canvas")   # has-a ContextGraph
s1 = apply_response(s0, affordance_id="ann1", value="looks good")  # pure append-only fold
assert s1.surface_state().turns == s0.surface_state().turns + 1     # the *view* advanced
# .lattice.yaml is untouched — the governed write is the follow-on runtime's job.
```

## Anti-Patterns

- **Editable-installing the substrate** (`pip install -e ../canvas_std`) to "make imports work" — writes `*.egg-info`
  into the immutable tree and breaks the firewall. Use pythonpath.
- **Rendering to "prove" the load** — importing PIL/cairosvg to rasterize defeats the leg-2 claim. The proof is the
  *absence* of a render path; assert it in a test.
- **Writing the authoritative `.lattice.yaml` from the POC** — conflates the demonstrated loop with the governed runtime
  write; keep the POC a view-fold.
- **Stalling on a missing upstream** — if the doc you were told to ground against does not exist, fix the boundary and
  author `v1` first-principles with a re-anchor seam; do not block the campaign.
- **Encoding cross-surface routing** in the surface spec — that is the OIP layer; the surface defines *what it is*, not
  *when to choose it*.

## Sources

- Operation Salon campaign + missions (`how/campaigns/campaign_canvas_salon/`), P0–P5.
- `what/decisions/adr_006_canvas_surface_boundary.md` (the boundary); `adr_000_canvas_identity.md` §Context (the thesis).
- `what/specs/spec_canvas_context_loading.md` (leg-2 L1–L7); `what/specs/spec_interface_surface.md` (leg-3 contract);
  `spec_conformance_suite.md §4.1` (the `I-*` family).
- `what/code/canvas_context/` — the leg-2 loader + the leg-3 `interaction.py` reference impl + its `AGENTS.md`.
- Companion guide: `context_canvas_producer_pattern.md` (the **output** leg's build pattern).
