---
type: decision_record
created: 2026-06-22
updated: 2026-06-22
status: ratified
last_edited_by: agent_stanley
campaign_id: campaign_canvas_armature
mission: mission_p0_charter
tags: [canvas, armature, leg3, runtime, interface, decision, p0, firewall]
---

# P0 Decision Record — leg-3 interface runtime charter (Operation Armature)

**Purpose:** resolve the eight governance/scope questions that gate the leg-3 *runtime* build — **before any code**.
Each decision carries a **recommended default** (or the operator's planning-session **choice**, for D1 + D3) + rationale
+ the alternative considered. The operator ratifies (accept / edit) at the **P0→P1 gate**; ratification **activates**
Operation Armature (`status: active`) and authorizes Phase P1 (the governed write runtime). Ratifying this record also
accepts the **phase arc P0–P3** as charted in `campaign_canvas_armature.md` **and** `adr_007` (the firewall-touch ADR,
ratified together with this record per D3).

> **Foundation (confirmed this session):** Operation Salon (closed 2026-06-22) **ratified** the leg-3 interface-surface
> spec ([[../../../../what/specs/spec_interface_surface|spec_interface_surface.md]]) and **demonstrated** the
> `read → act → re-read` loop with a read-only POC (`interaction.py` v0.2.0; `canvas_context` 50 passed). Three gaps
> remain (Salon §Descoped): the POC's `apply_response` is a **view-only append-fold** (no governed `.lattice.yaml`
> write); the `I-1/I-2/I-3/I-D` family is realized in the **consumer** (`validate_interaction_block`), forward-pointed
> into the `canvas_std` harness; and `interaction_version 1.0` is **uncut** as a Standard version. The existing
> `canvas_std.roundtrip` already ships `diff`/`merge`/`preserve_positions`/`compute_sync_hash`/`from_canvas`/`to_canvas`;
> `spec_roundtrip_protocol_v2 §1.2` mandates the reverse path is **advisory-only** (no silent source write). `adr_007`
> confirmed the next free ADR number; `campaign_canvas_armature` does not collide with an existing slug.

---

## D1 — Codename / slug  *(operator-chosen, planning session)*

**Chosen: Operation Armature / `campaign_canvas_armature`.** An **armature** is the load-bearing internal frame a
sculpture is built on — the structure that makes a form *stand up*. Apt for a *runtime*: it is the structural frame that
makes the Salon interaction *surface* (a contract + a POC) actually stand as a live, governed loop. Art/sculpture
register, of a piece with Mondrian; complements Keystone (reference impl), Atelier (production studio), Palette (output
family), Salon (the surface itself).

*Alternatives considered (AskUserQuestion):* **Operation Mainspring** (the clockwork driver — runtime-as-engine);
**Operation Loom** (weaving the loop). Cosmetic; a rename is a one-line `git mv` before P1.

---

## D2 — Campaign type & phase arc

**Recommended: a 4-phase *build* campaign (the Keystone model), P0–P3, each human-gated.** Unlike Salon (a
Cartography-model *planning* arc — leg 3 was greenfield + under-specified), the runtime's design space is already closed:
the spec is ratified, the loop is demonstrated, the round-trip machinery exists. The remaining work is **building** a
known design. P0 (charter + decisions + ADR) → **P1** (governed write runtime, firewall-clean) → **P2** (the firewall
touch + version cut, separately gated) → **P3** (close). The firewall touch gets its **own phase** so the operator can
approve or defer it at the P1→P2 gate independently of the rest.

*Alternative:* a single combined build phase (write + firewall touch together). Rejected — it would couple the
firewall-clean work to the sensitive `canvas_std` edit, removing the operator's ability to land the governed write and
*then* decide on the firewall touch.

---

## D3 — Firewall posture  *(operator-chosen, planning session — the load-bearing decision)*

**Chosen: LIFT the `canvas_std` firewall in a gated P2 (and only there), governed by `adr_007`.** This is the
*first-ever* proposed edit to `canvas_std` (held git-diff 0 across all 5 prior campaigns) — the **inverse** of Salon's
D6, which *preserved* it for leg 2. The operator chose to lift it (AskUserQuestion) precisely because the leg-3 thesis
needs `I-*` to be a **real Standard conformance check** (validated by the `canvas-std` CLI), not just consumer code, and
`interaction_version 1.0` to graduate into a **real Standard version**. The lift is bounded: it happens **only in P2**,
**only** for the two purposes `adr_007` names (wire `I-1/I-2/I-3` into `validate.py`'s aDNA-Native path reusing
`reserved.validate_anchors`; cut the Standard version), behind the P1→P2 human gate. At that gate the firewall check
**changes** from `git status -s -- what/code/canvas_std/` clean to **full regression green** (`canvas_std` +
`canvas_context` + 7 producers + D-1..D-3 on an interaction golden). P0/P1/P3 stay git-diff 0. `adr_007` is the citable
instrument of the lift and is ratified with this record.

*Alternative:* stay firewall-clean this round — build only the governed write, keep `I-*` in the consumer, defer the
version cut again. Defensible (preserves the perfect firewall record), but it leaves the leg-3 thesis incomplete (`I-*`
never becomes a checked Standard family) and merely re-defers the version cut. Rejected by the operator at the planning
gate.

---

## D4 — Governed-write semantics

**Recommended: advisory-reverse — a reviewed `.lattice.yaml` draft, never a silent authoritative write.** This is not a
free choice: [[../../../../what/specs/spec_roundtrip_protocol_v2|spec_roundtrip_protocol_v2]] §1.2 (ratified) makes the
reverse direction (view → source) **advisory only** — "a tool **MUST NOT** silently propagate canvas edits back to the
source." So "governed round-trip write" means the runtime **closes the loop to source through the §5 reverse path**:
`apply_response` advances the view → `compute_sync_hash` staleness check (§3.2) → `from_canvas` draft → `diff` vs current
source → three-way `merge` (`yaml_wins`) → emit a **reviewed draft** (`_draft`/`_merged`-marked; restore §6 lossy fields)
→ a **human-review gate** → regenerate the view (`to_canvas` + `preserve_positions`). The authoritative `.lattice.yaml`
is *never* mutated by the runtime; a P1 test asserts it is byte-unchanged after `reconcile`. The honesty the POC bought
with a view-only fold, the runtime keeps with a review gate.

*Alternative:* a direct authoritative write (the runtime commits the response to source). **Rejected — it violates the
ratified §1.2** and would make the canvas the authority over the lattice, inverting aDNA Decision 9.

---

## D5 — Runtime home (impl placement)

**Recommended: extend `canvas_context` (a new `reconcile` module beside `interaction.py`).** The runtime is the
interaction surface *made live* — conceptually continuous with the POC, and it must keep the same one-way dependency
(`canvas_context → canvas_std`, read-only). Extending the existing package keeps that dependency graph simple, reuses
the POC's `apply_response` + reader directly, and avoids a third package's scaffolding. The new code is a `reconcile`
module + glue, not a new core.

*Alternative:* a new sibling package `canvas_runtime` (depends on both `canvas_context` + `canvas_std`). Cleaner naming
("runtime" ≠ "context loader") and a crisper layering story, but more scaffolding for little gain at this size, and it
splits the leg-3 code across two packages. Reconsider if the runtime grows beyond a reconcile path (e.g. a turn-lifecycle
service). Trivial to extract later.

---

## D6 — Standard-version coordination

**Recommended: cut `interaction_version 1.0` into Standard `v2.2.0`, by maintainer discretion (not a fresh LIP),
reserving `v2.1.0` for the in-review LIP-0008.** Two sub-decisions:
- **Which version.** **LIP-0008** (the A-5 relaxation) is in FA review → **v2.1.0** on Final (review closes 2026-06-27).
  Cutting the interaction layer into the *same* version would collide two unrelated changes; default reserves v2.1.0 for
  LIP-0008 and cuts the interaction layer into **v2.2.0** (a separate MINOR — additive + conformance-optional per
  `adr_003 §3`). If LIP-0008 has already landed by the P2 gate, folding into v2.1.0 is reconsidered then.
- **LIP or maintainer discretion.** The `I-*` family was **already ratified into the spec** at Salon P3
  (`spec_conformance_suite §4.1` + `spec_interface_surface §9.1`, operator-ratified), and the spec's ratification **Q7**
  authorized "the operator cuts the Standard version at a deliberate release." So this is the **implementation of an
  already-ratified spec addition + the authorized version cut** — `adr_003 §2` maintainer-discretion territory (the
  normative decision is done), **not** a new normative change needing its own LIP. Default: cut by operator-countersigned
  release at the P2 gate, no new LIP.

*Alternative:* file a leg-3 LIP for parity with LIP-0008. Rejected as default — it re-litigates a spec decision the
operator already ratified at Salon P3; surfaced here so the operator can choose LIP-parity if preferred.

---

## D7 — Capture / turn-lifecycle / operator-annotation scope

**Recommended: a thin pilot path only — the gate/capture *engine* stays ISS's.** The runtime needs *enough* of a
turn-lifecycle + operator-annotation ingest to run the pilot end-to-end (operator annotates a canvas → agent re-reads as
context → responds → reviewed draft). Build exactly that thin path on the POC's append-only `apply_response` + the
spec §6 `turn` primitive — and **no more**. The HTML gate rendering, input capture, RLHF schema, and the 4-tier
round-trip are the **ISS** gate engine's (ADR-006 §2; the D8 ISS seam memo). The affordance-execution boundary vs ISS is
**coordinated, not absorbed** (idea stub scope-seed).

*Alternative:* build a full turn-lifecycle service + a capture runtime. Rejected — it crosses the ADR-006 §2 boundary
into ISS turf and over-builds beyond what the runtime thesis needs.

---

## D8 — OIP `v1.x` re-anchor posture

**Recommended: deferred stub — file it, don't build it.** The spec was authored Canvas-scoped v1 with the OIP re-anchor
designed in as an additive `interaction_version` semver pass (spec §OIP-grounding note). The future `aDNA.aDNA`
OIP-unification campaign (`idea_campaign_operator_interaction_patterns_unification.md`) is **unopened**; the runtime
builds on the ratified v1 spec **without** it (idea stub §Discussion — "the runtime can build on the ratified
Canvas-scoped v1 spec without it; the re-anchor pass waits for it"). At P3 close, file a deferred backlog stub for the
`v1.x` alignment pass, gated on the OIP campaign landing.

*Alternative:* block the campaign on the OIP campaign, or attempt the re-anchor now. Rejected — there is no OIP thesis
doc to anchor to yet; blocking would stall a campaign that has no hard dependency on it.

---

## Ratification

| # | Decision | Default / Choice | Operator disposition |
|---|----------|------------------|----------------------|
| D1 | Codename / slug | Operation Armature / `campaign_canvas_armature` (operator-chosen) | **ratified** (at rec) |
| D2 | Campaign type & arc | 4-phase build campaign P0–P3 (Keystone model), each human-gated | **ratified** (at rec) |
| D3 | Firewall posture | **Lift** `canvas_std` in a gated P2 via `adr_007` (operator-chosen) — inverse of Salon D6 | **ratified** (at rec) |
| D4 | Governed-write semantics | Advisory-reverse / reviewed draft (no silent source write; spec_roundtrip §1.2) | **ratified** (at rec) |
| D5 | Runtime home | Extend `canvas_context` (new `reconcile` module) vs new `canvas_runtime` sibling | **ratified** — extend `canvas_context` |
| D6 | Standard-version coordination | Cut `interaction_version 1.0` into **v2.2.0** by maintainer discretion (reserve v2.1.0 for LIP-0008) | **ratified** — v2.2.0, maintainer discretion |
| D7 | Capture / turn-lifecycle scope | Thin pilot path only (gate/capture engine stays ISS's, ADR-006 §2) | **ratified** (at rec) |
| D8 | OIP `v1.x` re-anchor | Deferred stub (cross-vault dep; file at P3, don't build) | **ratified** (at rec) |

> **✅ RATIFIED 2026-06-22 (operator, P0→P1 gate).** All eight decisions accepted at the agent's recommended
> values (D5 = extend `canvas_context`; D6 = cut `interaction_version 1.0` into **v2.2.0** by maintainer discretion,
> reserving v2.1.0 for the in-review LIP-0008 — no fresh leg-3 LIP, since the `I-*` family was already ratified into the
> spec at Salon P3 and the version cut is spec-authorized per Q7). This activates Operation Armature (`status: active`)
> and opens Phase P1 (the governed write runtime). `adr_007` ratified together with this record. Recorded in
> `session_stanley_20260622_193153_armature_scaffold_p0` (continued). **The firewall stays git-diff 0 until P2** (the
> lift takes effect only there, under the now-ratified `adr_007`).
