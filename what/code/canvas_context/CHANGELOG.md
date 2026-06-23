# Changelog — adna-canvas-context

All notable changes to the leg-2 reference context-loader.

## [0.3.0] — 2026-06-22

Operation Armature **P1** — the leg-3 **governed advisory-reverse write runtime**. Promotes the Salon P4 POC's
view-only `apply_response` into a runtime that closes the `read → act → re-read` loop to the authoritative source via
the **advisory** reverse path (`spec_roundtrip_protocol_v2` §1.2/§5): a response advances the view, and the runtime
emits a **reviewed source draft** — never a silent write to the authoritative source. Reuses `canvas_std.roundtrip`
(`merge`/`diff`/`to_canvas`/`compute_sync_hash`); `canvas_std` untouched (D6 firewall — the P2 lift is `adr_007`'s).

### Added
- `reconcile.py` — the governed write:
  - **`reconcile(view, source)`** → `Reconciliation` — the advisory reverse: a staleness gate (§3.2), a topology
    `diff` delta (§5 step 3), a three-way `merge` source draft (§5 step 4), the §6 lossy-field restoration (§5 step 5 —
    `fair`/`federation`/`execution`/per-node `config`, the step `merge`/`from_canvas` drop), and the interaction
    response log surfaced for review. Marks the draft `_draft` + `requires_review`; mutates no input.
  - **`governed_apply(view, source, …)`** → `(advanced_view, Reconciliation)` — the governed *act*: `apply_response`
    (advance the view, append-only) then `reconcile`. Writes nothing to disk.
  - **`write_source_draft(recon, path, *, reviewed_by=None)`** — writes the draft to a **separate** artifact, **never**
    the authoritative source (the §1.2 human-review gate).
- `tests/fixtures/review_request.source.json` (+ `_build_review_source.py` generator) — the authoritative source paired
  with `interaction_review.canvas`; topology-matched so `compute_sync_hash(source)` equals the view's stored hash (the
  staleness baseline). Carries the §6 source-only fields.
- `tests/test_reconcile.py` — the **headline source-byte-unchanged** guarantee, the `_draft`/`requires_review` marking,
  lossy-field restoration, response surfacing, the staleness gate, round-trip-to-baseline, and input purity.
- `tests/pilot_governed_write.py` — a runnable on-disk demo of the governed loop (the authoritative source byte-unchanged).

### Notes
- The governed write is governed **because** it is advisory — `spec_roundtrip_protocol_v2 §1.2` forbids silent source
  propagation; the runtime makes the reverse path safe + reviewable (draft + delta + staleness + conflicts), never a
  silent mutation. The value-add over `roundtrip.py` is the governance layer it left to "a higher layer" (§6 restore +
  the never-touch-source discipline + the response review payload).
- Firewall (D6) held — `canvas_std` imported read-only, git-diff 0. Wiring `I-*` into the `canvas_std` harness + the
  `interaction_version` Standard-version cut are **P2** (the `adr_007` firewall touch), not here.

## [0.2.0] — 2026-06-22

Operation Salon **P4** — leg-3 interaction-loop POC. A read-only extension realizing `spec_interface_surface.md`
(ratified 2026-06-22) §3.1 + the `I-1`/`I-2`/`I-3`/`I-D` conformance family. The leg-2 surface is unchanged
(additive only).

### Added
- `interaction.py` — the leg-3 interaction surface, composing the leg-2 `ContextGraph`:
  - **Reader (read step):** `load_interaction_surface()` + `InteractionSurface` (`affordances()` / `surface_state()` /
    `responses()` / `open_affordances()` / `turn_complete()` / `validate_interaction()`); record shapes `Affordance`,
    `Response`, `SurfaceState`.
  - **Reducer (act + re-read):** `apply_response()` — a pure, append-only fold that logs a response and recomputes
    surface state (IX5/IX6); advances the **view** only (no disk write, no rendering, no `canvas_std` mutation).
  - **Conformance:** `validate_interaction_block()` (I-1/I-2/I-3, reusing `canvas_std::validate_anchors`);
    `strip_interaction()` (§8.2) + `is_round_trip_safe()` (I-D, reusing `canvas_std.strip` + `validate`).
- `tests/fixtures/interaction_review.canvas` (+ `_build_interaction_review.py` generator) — an interaction-bearing
  golden declaring one affordance of each of the four kinds (`input`/`choice`/`annotation`/`action`), anchored via
  both the node-id and `panel_link.anchors` label forms.
- `tests/test_interaction.py` (I-1/I-2/I-3), `tests/test_interaction_loop.py` (the read→act→re-read proof + the
  no-render assertion), `tests/test_interaction_degradation.py` (I-D round-trip-to-baseline).
- `tests/pilot_interaction_loop.py` — a runnable on-disk demo of the loop (not a runtime).

### Notes
- Boundary (ADR-006 §2 / spec §10.2): a read-only extension + a view-fold — **not** a capture runtime (ISS's turf),
  renderer, or transport. The governed round-trip write (`.lattice.yaml`) stays out of scope (`spec_roundtrip_protocol_v2`).
- Firewall (D6) held — `canvas_std` imported read-only, git-diff 0. First code realization of the `I-*` family
  (housed in the consumer, not wired into the `canvas_std` harness).

## [0.1.0] — 2026-06-22

Initial implementation — Operation Salon P2 (leg-2 proof). Reference realization of
`spec_canvas_context_loading.md` (ratified 2026-06-22).

### Added
- `model.py` — the context-graph record shapes (spec §3): `ContextGraph`, `Component`, `Panel`, `Relation`, `Ref`,
  `Surface`, `Conformance`.
- `loader.py` — `load_context_graph()` implementing the normative **L1–L7** load pipeline (spec §4): parse & validate
  (refuse Core-invalid) → baseline graph → additive `_reserved` overlay → context identity → ref classification →
  advisory staleness → **no rendering**. Cycle-safe recursive resolution.
- `resolver.py` — the abstract `Resolver` contract (spec §5) + `DefaultPathResolver` for in-vault wikilinks;
  `federation_ref` returns a descriptor (transport deferred).
- `traversal.py` — the reading-order walk (kind ∈ {reading_order, sequence} from `isStartNode`; geometry fallback)
  behind the §6 read-only traversal primitives.
- `tests/` — `test_loader.py`, `test_traversal.py`, and `test_pilot.py` (the leg-2 proof: loads
  `document_generator/examples/canvas_standard_whitepaper.canvas` as a context graph without rendering).

### Notes
- Read-only consumer of `canvas_std`'s public API (D6 firewall — `canvas_std` untouched).
- Bounded by ADR-006: a contract realization + reference loader, never a runtime/transport/router.
