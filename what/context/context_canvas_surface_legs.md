---
type: context
subtype: context_guide
created: 2026-06-22
updated: 2026-06-23
status: active
last_edited_by: agent_stanley
context_version: "1.1"
token_estimate: ~3300
quality_score: 4.3
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
total). The leg-3 **runtime** was then completed in **Operation Armature**: a governed *advisory-reverse* `.lattice.yaml`
write (a reviewed draft, never a silent write); the `I-*` family **wired into the `canvas_std` harness** under a bounded
firewall-touch ADR; and `interaction_version 1.0` cut into a Standard version. Use this when building **any**
read-as-context, interaction-surface, or governed-write capability over `canvas_std` — including the first authorized
edits *to* the Standard's reference tooling.

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

6. **A governed write is governed *because* it is advisory.** When the loop must reach the authoritative source
   (`.lattice.yaml`), do **not** write it silently (`spec_roundtrip_protocol_v2 §1.2` forbids it). Model "act →
   reconcile" as: advance the view (append-fold) → diff the view against the source's canonical view → three-way **merge
   into a draft** → restore the source-only lossy fields the merge drops → surface the response log + a staleness verdict
   + conflicts for review. Emit a `_draft` / `requires_review` artifact on a **separate** path; promotion to the
   authoritative source is an explicit human action. A test asserts the on-disk source is **byte-unchanged** after the
   loop. Reuse the round-trip engine (`diff` / `merge` / `compute_sync_hash`) read-only — the governance layer (the §6
   lossy-field restore + the never-touch-source discipline + the review payload) is the only net-new code.

7. **Lift the firewall as a bounded ADR, never ad hoc.** The immutable reference tree stays git-diff 0 by default. When
   a capability genuinely belongs *in* the Standard's reference tooling (a conformance check, a version cut — **not** a
   renderer / transport / router), lift the firewall with a **ratifiable ADR** that names: the single phase it applies
   to, the exact bounded purposes, why it's within the tree's legitimate remit (exercising the remit, not widening it),
   and the **replacement gate** — swap `git-diff 0` for **full-regression-green** while lifted. Every other phase holds
   git-diff 0 (even a CHANGELOG/doc edit counts as a touch). This keeps a "first-ever edit" small, isolated, reviewable.

8. **Graduate consumer logic into the harness as a thin delegate.** When a conformance family first lives in a consumer
   (to preserve the firewall) and a later ratified touch wires it into the Standard, make the consumer's function a
   **thin delegate / re-export** of the harness implementation — one source of truth, no duplicated logic. Preserve the
   consumer's public signature for API stability even if a parameter becomes vestigial. Watch for the harness-vs-consumer
   substrate gap: the harness resolves from the **doc** (it must not import the consumer's graph types — the dependency
   stays one-way), so port the *doc path*, and do **not** re-run a check the harness already runs on the same branch.

9. **Land the logic, prove no regression, then cut the version.** Sequence a firewall touch so the new behaviour lands
   *behind the existing version's tests first* — the suite stays green at the **old** version, proving the addition is
   non-breaking — and only then cut the version as a separate, mechanical pass: bump **every** version-string site (impl
   constant · schema title + `x-standard-version` · CLI · spec frontmatters · CHANGELOG), keep the schema `$id` if the
   structural schema is unchanged, reserve a held minor for an in-review LIP, and **leave fixtures at their authored
   version** to prove version-independent validation (why downstream producers don't regress).

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
  the consumer first** (preserving the firewall), reusing `canvas_std.strip`/`validate`/`validate_anchors`; wire `I-*`
  **into the `canvas_std` harness only under a ratified firewall-touch ADR** (Armature's `adr_007`) — after which the
  consumer becomes a thin delegate (Principle 8) and `interaction_version` is cut into a Standard version (Principle 9).
- **Governed write = advisory reverse.** Build it as a thin governance layer over the round-trip engine, imported
  read-only: `reconcile(view, source) → Reconciliation{draft, responses, topology_delta, conflicts, stale}`;
  `governed_apply` = `apply_response` then `reconcile`; `write_source_draft` writes a `_draft` artifact to a **separate**
  path, never the authoritative source. Take a **parsed** source dict (the caller parses YAML) so the consumer stays
  stdlib-only, mirroring how the loader takes a parsed canvas (Principle 6).
- **Keep the boundary fenced.** A surface consumer is **not** a capture runtime, renderer, transport, or cross-surface
  router (ADR-006 §2–§3). Expose refs/affordances and delegate; routing belongs to the OIP layer, the gate engine to
  ISS, pixels to ComfyUI. The harness touch stays in lane too: a conformance check + a version cut, never an engine.

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
- **A silent authoritative write** from the runtime — conflates the governed reverse path with a direct mutation. Emit a
  reviewed `_draft`; never overwrite the source. The headline guarantee (and test) is "source byte-unchanged."
- **Touching the reference tree outside the bounded firewall phase** — editing `canvas_std` (even a CHANGELOG or a doc
  line) during a git-diff-0 phase breaks the firewall; defer it to the next authorized touch. A `_draft` back-fill that
  *should* land in the Standard waits for a phase that lifts the firewall.

## Sources

- Operation Salon campaign + missions (`how/campaigns/campaign_canvas_salon/`), P0–P5 (legs 2 + 3 spec/POC).
- Operation Armature campaign + missions (`how/campaigns/campaign_canvas_armature/`), P0–P3 — the leg-3 **runtime** +
  the **firewall touch**; `what/decisions/adr_007_leg3_firewall_touch.md` (the bounded-lift ADR, Principle 7).
- `what/decisions/adr_006_canvas_surface_boundary.md` (the boundary); `adr_000_canvas_identity.md` §Context (the thesis).
- `what/specs/spec_canvas_context_loading.md` (leg-2 L1–L7); `what/specs/spec_interface_surface.md` (leg-3 contract);
  `spec_conformance_suite.md §4.1` (the `I-*` family); `spec_roundtrip_protocol_v2.md §1.2/§5` (the advisory reverse path).
- `what/code/canvas_context/` — the leg-2 loader, the leg-3 `interaction.py` reader, and `reconcile.py` (the governed
  advisory-reverse write); `what/code/canvas_std/src/canvas_std/reserved.py::validate_interaction` (the harness wiring).
- Companion guide: `context_canvas_producer_pattern.md` (the **output** leg's build pattern).
