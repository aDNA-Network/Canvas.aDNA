---
type: spec
spec_id: spec_interface_surface
title: "aDNA Canvas interface-surface contract — a canvas as a human↔AI / human↔human interaction surface (Salon leg 3)"
standard_version: "2.0.2"
interaction_version: "1.0"
status: draft
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
phase: P3
campaign_id: campaign_canvas_salon
resolves: "leg-3 interface-surface contract (the third leg of the ADR-000 thesis; greenfield, spec-only per Salon D4)"
supersedes:
superseded_by:
tags: [spec, canvas, interface, surface, interaction, leg3, salon, rfc2119, context-object, boundary]
---

# aDNA Canvas Interface-Surface Contract (Salon leg 3)

> **Status: DRAFT — authored at Operation Salon P3 (`campaign_canvas_salon`), pending the operator ratification
> gate.** The third leg of the [[adr_000_canvas_identity|ADR-000]] three-leg thesis: legs 1 (output, Operation Palette)
> and 2 (context object, [[spec_canvas_context_loading|Salon P2]]) are **proven**; this spec **specifies-and-bounds**
> leg 3. It is **spec-only** this campaign (Salon **D4**) — a **contract**, never a rendering engine, capture runtime,
> federation transport, or cross-surface router (bounded by [[adr_006_canvas_surface_boundary|ADR-006]]). It rides the
> namespaced `_reserved.interaction` carrier **additively** — no core-schema change, no canvas-as-primitive re-opening
> (Δ2 / LIP-0009 untouched). RFC 2119 keywords (MUST / SHOULD / MAY).
>
> **OIP grounding note.** ADR-000 names an external "OIP/interface thesis" doc to ground leg-3 vocabulary; at P3 open
> that doc **does not yet exist** (it is a future `aDNA.aDNA` OIP-unification deliverable). Per the operator decision at
> this gate, this spec is authored **first-principles, Canvas-scoped (v1)** — grounded on ADR-006, the proven leg-2
> model, and ISS as a concrete exemplar — and re-anchors to the OIP thesis when it lands (a `v1.x` alignment pass). The
> D8 heads-up memos go out at P3 (`seam: Canvas ↔ OIP` / `seam: Canvas ↔ ISS`).

## 1. Purpose & relationship

1.1. An aDNA canvas is named three things ([[adr_000_canvas_identity]] §Context): an **output primitive**, a
first-class **context object**, and a **human↔AI / human↔human interaction surface**. This spec governs the third. Leg 2
([[spec_canvas_context_loading]]) defined *read-AS-context* — how an agent loads and traverses a canvas as a navigable
`ContextGraph` **without rendering**. This spec defines *act-ON-surface* — what it means for a **participant** (human or
AI) to **interact** with a canvas, expressed as a loop over that same leg-2 context graph.

1.2. The central move: **interaction is a `read → act → re-read` loop over the leg-2 `ContextGraph`, not a new object
model.** A participant reads the surface as context (leg 2), acts on a declared interaction point, and the act yields a
new context-graph **state** that the next reader re-reads. Leg 3 is therefore a thin, additive overlay riding on proven
machinery — exactly what [[adr_006_canvas_surface_boundary|ADR-006]] §1 authorizes ("a contract, not an engine").

1.3. It builds directly on already-ratified structure and does **not** introduce a parallel model: the `anchor`
primitive reuses the `_reserved.panel_link.anchors` map ([[spec_panel_link_semantics]] §5.3) and its orphan check
(`canvas_std::validate_anchors`); the **surface state** is a leg-2 `ContextGraph`; the read step is a leg-2 load. Leg 3
*formalizes the interaction semantics* of constructs that already exist; it reinvents nothing.

1.4. It does not re-open the canvas-as-primitive question (Δ2 / LIP-0009); a canvas remains a *view of the `lattice`
primitive* (aDNA Decision 9), and all interaction metadata rides in `_reserved.interaction` — no core-primitive change.

## 2. Scope

**In scope.** The abstract **interaction-surface model**; the **five interaction primitives** (`anchor`, `affordance`,
`response`, `surface state`, `turn`); the additive `_reserved.interaction` carrier shape; the normative
`read → act → re-read` loop contract; the conformance rules (including the **round-trip-to-baseline** guarantee); and a
reference-implementation forward-pointer.

**Out of scope.**
- **Cross-surface routing** — *when* to surface an interaction on a canvas vs an ISS gate vs a Terminal prompt vs a web
  page is the future `aDNA.aDNA` **OIP** layer's decision-tree ([[adr_006_canvas_surface_boundary|ADR-006]] §3, the
  load-bearing line). This spec **MUST NOT** encode routing logic.
- **Rendering & capture** — no HTML/gate rendering, no rasterization, no input-capture runtime. Affordances are
  *declared*, not *rendered*; responses are *logged*, not *captured by a runtime* (ISS owns the gate engine, ADR-006 §2).
- **Federation network transport** — cross-vault fetch of a referenced surface is the resolver / federation layer's job
  (same posture as [[spec_canvas_context_loading]] §2), not this spec's.
- **Mutation / round-trip write mechanics** — this spec declares *that* a response advances surface state and *what* the
  new state means; the write/reconcile path against the authoritative `.lattice.yaml` is governed by
  [[spec_roundtrip_protocol_v2|spec_roundtrip_protocol_v2.md]] (§7), not here.
- **Canvas-as-primitive change** — no core-schema edit (Δ2 / LIP-0009); leg 3 rides `_reserved` only.
- **The ISS gate runtime** — HTML rendering, RLHF schema, and the 4-tier round-trip belong to ISS
  (`aDNA.aDNA`, [[adr_028_iss_architecture]]). Canvas owns the *grammar* an ISS gate may one day be authored on
  (ADR-006 §2), not the gate engine.

## 3. The interaction-surface model (abstract)

3.1. A canvas is an **interaction surface** when it carries an additive `_reserved.interaction` overlay declaring one or
more **affordances** — named points at which a participant (human or AI) may submit a **response** that advances the
**surface state**. The surface *is* the canvas; the interaction layer is metadata over the same baseline nodes. A
conformant reader produces, alongside the leg-2 `ContextGraph`, the following conceptual record shapes (a reference
implementation realizes them in its host language):

```
InteractionSurface:                                  # a leg-2 ContextGraph + an additive interaction overlay
  graph:             ContextGraph                     # the leg-2 read face (spec_canvas_context_loading §3)
  interaction_version: <semver | null>                # _reserved.interaction.interaction_version; null ⇒ non-interactive
  affordances:       [ Affordance ]                   # declared interaction points (keyed by id)
  responses:         [ Response ]                      # submitted values (append-only log)
  state:             SurfaceState                      # the current snapshot (derivable; §6)

Affordance:                                          # one per _reserved.interaction.affordances[id]
  id:                <affordance id>
  anchor:            <anchor-label | node id>          # MUST resolve (§5); reuses panel_link.anchors
  kind:              input | choice | annotation | action   # closed enum (§3.3); contrast: surface label is OPEN (AT-2)
  prompt:            <string | null>                   # optional participant-facing label (NOT a render instruction)
  options:           [ <string> ] | null               # REQUIRED iff kind == choice; else null/absent
  required:          <bool>                             # whether a turn completes without a response here (default false)

Response:                                            # one per _reserved.interaction.responses[] (append-only)
  affordance:        <affordance id>                   # MUST reference a declared affordance
  value:             <string | label | structured | null>   # kind-consistent (§4 IX5); null iff kind == action
  participant:       { kind: human | ai | null, id: <string | null> }   # optional; surface works with kind=null (§7)
  turn:              <turn id>                          # the read→act→re-read cycle this response belongs to
  at:                <iso-8601 | null>                  # optional timestamp; advisory

SurfaceState:                                        # the re-read target — leg-2 graph folded with the response log
  turn:              <turn id>                          # current/latest turn
  open:              [ <affordance id> ]                # affordances still awaiting a response this turn (derivable)
```

3.2. The **baseline + leg-2 layers MUST be derivable with `_reserved.interaction` stripped** — the overlay is purely
additive ([[spec_adna_canvas_standard]] §11; [[spec_canvas_context_loading]] §3.1). This is the hook for the
round-trip-to-baseline guarantee (§8/§9): an interactive canvas with its interaction layer removed is a valid output
canvas and a valid context graph carrying no affordances — i.e. a non-interactive surface.

3.3. **Two reductive grammars.** Leg 3 fixes two closed vocabularies, in the Mondrian "reduce to the grammar" ethos —
deliberately contrasting the **open** `surface`-subclass vocabulary ([[spec_panel_link_semantics]] §4, AT-2):
- **The four affordance `kind`s** partition what a participant can do at a point: supply a value (`input`), pick from a
  declared set (`choice`), attach unstructured commentary (`annotation`), or fire a valueless trigger (`action`). This
  is a closed enum (§4 IX3) because each kind maps to a distinct conformance rule.
- **The five primitives** (§6) are the irreducible units of the loop. Each earns its place by being non-derivable from
  the others (§6 justification).

> **NOTE (terminology, ratification).** "Interaction surface" (this spec — the whole canvas as a medium of exchange) is
> distinct from the leg-2 `Surface` record (`_reserved.panel_link.surfaces`, an *output subclass* region). The two are
> orthogonal: an `affordance`'s `anchor` may sit inside a `panel_link` surface region, but the records do not overload.
> Kept distinct deliberately (the campaign + ADR-006 mandate the term "interaction surface"); disambiguated here.

## 4. The interaction contract (normative)

A conformant interaction surface satisfies these steps. Each step's MUST/SHOULD/MAY is binding. Together they specify the
`read → act → re-read` loop.

**IX1 — Declare additively.** The interaction layer **MUST** live entirely under `_reserved.interaction`. It **MUST NOT**
add or alter any baseline `nodes`/`edges` key, nor any `_reserved.panel_link` / `_reserved.component_types` semantics
([[spec_adna_canvas_standard]] §7, §11). `_reserved.interaction.interaction_version` **SHOULD** be present and semver.

**IX2 — Bind every affordance to a resolvable anchor.** Every `affordances[id].anchor` **MUST** resolve to an existing
baseline node `id`, directly or via a declared `_reserved.panel_link.anchors` label ([[spec_panel_link_semantics]] §5.3).
An affordance whose anchor does not resolve is **non-conformant** (orphaned affordance). This reuses the existing
anchor orphan check (`canvas_std::validate_anchors`, §5).

**IX3 — Constrain by kind.** `affordances[id].kind` **MUST** be one of `input | choice | annotation | action`. A `choice`
affordance **MUST** declare a non-empty `options[]`; the other three kinds **MUST NOT** declare `options`. (The `kind`
grammar is **closed** — contrast the **open** `surface` vocabulary, AT-2, which a validator MUST NOT enum-check.)

**IX4 — Read as context (the *read* step).** A reader **MUST** be able to load the surface as a leg-2 `ContextGraph`
**without rendering** ([[spec_canvas_context_loading]] §4 L7) and discover its `affordances` and current `state` from
`_reserved.interaction` — **without** a renderer, capture runtime, or transport. Discovery is a pure structural read.

**IX5 — Respond into the log (the *act* step).** A `response` **MUST** reference a declared `affordances` id, and its
`value` **MUST** be consistent with the affordance `kind`: a `choice` value **MUST** be one of the declared `options`; an
`input`/`annotation` value is a free string/structured value; an `action` **MUST** carry no value (`null`). The response
log is **append-only**: a conformant writer **MUST NOT** mutate or delete a logged response — it supersedes by appending
a new one in a later turn. The surface **MUST** function with `participant.kind = null` (participant-neutrality, §7).

**IX6 — Advance state and re-read (the *re-read* step).** The current **surface state** **MUST** be derivable as the
leg-2 `ContextGraph` folded with the response log up to the current `turn`. A `turn` is **complete** when every
`required` affordance in it has a response. The re-read of the advanced state **MUST** itself be a valid leg-2 load — the
loop closes onto leg 2. Reconciliation against the authoritative `.lattice.yaml` is **advisory and out of scope** here
(deferred to [[spec_roundtrip_protocol_v2]], as in [[spec_canvas_context_loading]] §7).

## 5. The affordance↔anchor binding contract

5.1. The single load-bearing sub-contract: **every affordance binds to a resolvable anchor** (the leg-3 analogue of
leg-2's "every ref is exposed; resolution is delegated"). An `anchor` value is **either** a baseline node `id` **or** a
label declared in `_reserved.panel_link.anchors` (which itself maps a label → a baseline node `id`,
[[spec_panel_link_semantics]] §5.3). This is the same dual form `panel_link` already allows for component
cross-references (a `qualities` key in `{ref, anchor, anchor_ref, cites, for}`).

5.2. Because the substrate is the existing anchor layer, the existing **orphan check** already covers affordance
binding: a validator **MUST** confirm every `affordances[*].anchor` resolves to a node `id` or a declared anchor label —
**no orphaned affordance** — reusing `canvas_std::validate_anchors` ([[spec_panel_link_semantics]] §6). Leg 3 adds no new
anchor machinery; it piggybacks on the ratified one.

## 6. Interaction primitives (the act contract)

A conformant interaction surface is expressed in exactly **five** primitives (names illustrative; semantics binding).

| Primitive | Denotes | Binds to / carried in | Lifecycle |
|-----------|---------|------------------------|-----------|
| `anchor` | A named, addressable region — the *where*. | A baseline node `id`, optionally via a `panel_link.anchors` label (§5). | Static (declared with the canvas). |
| `affordance` | A declared interaction *point* — the *what-can-be-done* (one of four `kind`s). | `_reserved.interaction.affordances[id]`; MUST bind to an `anchor` (§5). | Static (declared); "open" or "answered" within a turn. |
| `response` | A participant's submitted value bound to an affordance — the *act*. | `_reserved.interaction.responses[]` (append-only). | Created when a participant acts; immutable once logged. |
| `surface state` | The current snapshot — the leg-2 `ContextGraph` folded with responses so far; the *re-read* target. | The whole canvas at a point in time; pointer in `_reserved.interaction.state`. | Advances by one per completed turn; recomputable from the log. |
| `turn` | One `read → act → re-read` cycle — the *unit* of interaction. | A `turn` id referenced by responses and by `state.turn`. | Opens on read; completes when the turn's `required` affordances are answered. |

6.1. **Why these five.** `anchor` and `affordance` are distinct because *where* and *what* vary independently (two
affordances may target one anchor; one kind may appear at many anchors). `response` is distinct from `affordance` because
the *declaration* (what can be done) and the *act* (what was done) are different lifecycle objects — the same split ISS
draws between a gate's `options[]` and the operator's submitted `decisions[]` ([[adr_028_iss_architecture]]). `surface
state` is the loop's defining primitive: an act changes what the next reader reads, and it is the explicit bridge back to
leg 2 (a surface state *is* a `ContextGraph` you can run leg-2 traversal over) — it MUST be recomputable, so it can never
go authoritatively stale. `turn` bounds *one cycle*, making the loop (not a single exchange) the unit.

## 7. Authority & participants

7.1. **Participant-neutrality.** The contract is identical for a human participant and an AI participant — this is what
makes one model serve both human↔AI *and* human↔human interaction. A `response` MAY carry a `participant` descriptor
(`{kind, id}`, both optional/advisory), but the surface **MUST NOT** require a participant *kind* to function (a
`response` with `participant.kind = null` is valid).

7.2. **State authority.** Per aDNA Decision 9 and [[spec_roundtrip_protocol_v2]], the authoritative source of a canvas is
its `.lattice.yaml`; the `.canvas` is the **view**. A `response` advances the **view** (the surface state); the canonical
surface ([[spec_panel_link_semantics]] §5.2) is the round-trip authority for any later reconciliation. Leg 3 declares the
*meaning* of the mutation (a logged response → a new surface state); it does not perform reconciliation (that is
[[spec_roundtrip_protocol_v2]]'s role).

## 8. Degradation (canvases without `_reserved.interaction`)

8.1. A canvas with no `_reserved.interaction` block is a **non-interactive surface** — a pure output / context artifact.
It **MUST** still be a valid canvas and a valid leg-2 `ContextGraph`; the interaction layer's absence is valid, not an
error (it mirrors [[spec_canvas_context_loading]] §8 and the Standard's degradation contract,
[[spec_adna_canvas_standard]] §11).

8.2. Conversely — the **headline property** — stripping `_reserved.interaction` from an interactive canvas **MUST** yield
a valid output canvas (and a valid leg-2 graph) carrying no affordances. **Round-trip-to-baseline**: interaction is
additive enrichment over the same baseline nodes, never an overload of them ([[spec_adna_canvas_standard]] §11.3,
no-baseline-overload).

## 9. Conformance

A **conformant interaction surface**:

- **MUST** degrade to a valid output canvas when `_reserved.interaction` is stripped — round-trip-to-baseline (§8.2);
- **MUST** remain a valid leg-2 context graph both with the interaction layer present and with it stripped (§3.2);
- **MUST** bind every affordance to an anchor that resolves to an existing baseline node — no orphaned affordance
  (§4 IX2 / §5);
- **MUST** constrain affordance `kind` to `{input, choice, annotation, action}` and declare `options[]` **iff** `choice`
  (§4 IX3);
- **MUST** ensure every `response` references a declared affordance and carries a `kind`-consistent `value`, with an
  append-only log (§4 IX5);
- **MUST** make the **surface state** recomputable as the leg-2 graph folded with the response log (§4 IX6, §6);
- **MUST NOT** require a specific renderer, capture runtime, or transport to read affordances/state (§4 IX4; ADR-006);
- **MUST NOT** require a particular participant *kind* — identical for human and AI participants (§7.1);
- **MUST NOT** encode cross-surface routing logic (ADR-006 §3 — the load-bearing line);
- **SHOULD** declare `_reserved.interaction.state` for reader convenience (but it MUST stay recomputable, never
  authoritative-only);
- **SHOULD** carry an `interaction_version` (semver) on the overlay;
- **MAY** carry `participant` descriptors and `at` timestamps (advisory);
- **MAY** be read by an extension of the leg-2 `canvas_context` loader; a dedicated runtime is **not** required
  (spec-only, D4).

9.1. **Conformance family (proposed `I-*`).** Interaction conformance is an **aDNA-Native** feature, paralleling the
single-row `A-5` (panel_link) and `A-7` (context_object) families in [[spec_conformance_suite]] §4. Proposed rows (to be
added to the suite **at ratification**, not edited in by this draft):

| ID | Check |
|----|-------|
| I-1 | `_reserved.interaction` (if present) valid per this spec §4 — `interaction_version` semver; well-formed `affordances`/`responses`/`state`. |
| I-2 | Every `affordances[*].anchor` resolves (reuse `validate_anchors`); `kind ∈ {input,choice,annotation,action}`; `options[]` present **iff** `choice`. |
| I-3 | Every `responses[*].affordance` references a declared affordance; `value` is `kind`-consistent (`action` ⇒ null; `choice` ⇒ ∈ `options`); log is append-only-shaped. |
| I-D | `validate(strip(doc), core)` still passes with `_reserved.interaction` removed (round-trip-to-baseline — the [[spec_conformance_suite]] §5 `D-1` contract, generalized to the interaction layer). |

9.2. **Fixtures.** The conformance set extends the `canvas_std` golden fixtures with one interaction-bearing fixture
(declaring at least one affordance of each kind) and reuses the degradation fixtures to prove `I-D` round-trip-to-baseline.
(Any executable suite lands with a reference reader, not in this spec-only phase — §10.)

9.3. **Format ≠ quality.** As with the rest of the Standard ([[spec_conformance_suite]] §6), the conformance family
checks *format*; the *quality* of an interaction surface (is the interaction well-designed?) is the III framework's
concern via the `iii/` wrapper, not this spec's.

## 10. Reference implementation (forward-pointer)

10.1. Leg 3 is **spec-only this campaign** (Salon **D4**): **no runtime is built here.** The contract stands on its own;
a conformant reader is optional in this phase.

10.2. The stretch **P4 POC** (if budget remains, D4) is the minimal `read → act → re-read` loop named in the campaign:
an operator annotates a canvas → an agent re-reads it as context → responds. If built, a reference reader extends the
leg-2 `canvas_context` loader **read-only** (e.g. `affordances()` / `surface_state()` accessors over the existing
`ContextGraph`), preserving the `canvas_std` **firewall** (D6) — it **MUST NOT** become a capture runtime (that boundary
is ISS's, ADR-006 §2). A full leg-3 *build* is deferred to a follow-on charter (Salon P5).

## 11. Boundary (ADR-006)

11.1. This spec defines a **contract** — not a runtime, a transport, or a router. The deferred turf, with citations:

| Concern | Owner (not Canvas) | Citation |
|---------|--------------------|----------|
| **When** to surface an interaction on a canvas vs ISS / Terminal / web (cross-surface routing) | future **OIP** layer (`aDNA.aDNA`) | ADR-006 §3 — the load-bearing line |
| HTML gate **rendering + capture + RLHF schema + 4-tier round-trip** | **ISS** (`aDNA.aDNA`) | ADR-006 §2; [[adr_028_iss_architecture]] |
| Web **publication** (canvas → deployed website) | **Astro.aDNA** | ADR-006 §2 |
| **CLI/TUI** node orchestration | **Terminal.aDNA** | ADR-006 §2 |
| **Federation transport** (cross-vault fetch of a referenced surface) | the **federation layer** | ADR-006 §1; [[spec_canvas_context_loading]] §2 |
| **Mutation / round-trip write** + source reconciliation | [[spec_roundtrip_protocol_v2]] | §7 defers |
| Core-schema / **canvas-as-primitive** change | Δ2 / **LIP-0009** | ADR-006 (Neutral); rides `_reserved` only |
| Output **quality** of an interaction surface | **III** (`iii/` wrapper) | [[spec_conformance_suite]] §6 |

11.2. **The clean seam (ADR-006 §2):** **Canvas owns the affordance / anchor / response / turn *grammar*; ISS owns the
gate *engine* that may one day consume it.** A gate may be *authored on a canvas archetype* (Canvas owns that artifact
grammar), but ISS owns the gate runtime — no overlap while Canvas stays "grammar" and ISS stays "gate engine."

11.3. **Coordination courtesy (ADR-006 §4 / Salon D8).** Because leg 3 bears on (a) how the OIP layer will characterize
the canvas surface and (b) how an ISS gate might be authored on a canvas archetype, the heads-up memos go to `aDNA.aDNA`
(OIP) and Argus/ISS through the coordination channel, tagged `seam: Canvas ↔ OIP` / `seam: Canvas ↔ ISS` (sent at P3
open). Routine evolution touching neither needs no external sign-off.

## 12. Related

- [[spec_canvas_context_loading]] (leg 2 — the loop's *read* step; the `ContextGraph` a surface state is)
- [[spec_context_object]] (leg-2 context-object metadata)
- [[spec_panel_link_semantics]] (§5.3 `anchors` + §5.2 `surfaces` that this formalizes; `validate_anchors`)
- [[spec_adna_canvas_standard]] (§7 `_reserved` carrier; §11 degradation / no-baseline-overload contract)
- [[spec_roundtrip_protocol_v2]] (authority matrix + the write/reconcile path leg 3 defers to)
- [[spec_conformance_suite]] (where the `I-*` family folds in; format-vs-quality boundary §6)
- [[adr_006_canvas_surface_boundary]] (the binding boundary) · [[adr_000_canvas_identity]] (the three-leg thesis)
- `aDNA.aDNA/how/skills/skill_create_iss.md` + [[adr_028_iss_architecture]] (the ISS contrast exemplar)
- `aDNA.aDNA/how/backlog/idea_campaign_operator_interaction_patterns_unification.md` (the future OIP routing layer)
- `how/campaigns/campaign_canvas_salon/campaign_canvas_salon.md` (P3: this spec)

## Open questions (for the ratification gate)

These are flagged for the operator at the P3 ratification gate; each carries a proposed default (the draft adopts the
default unless the operator directs otherwise).

1. **Primitive naming — `affordance`.** Precise and kind-neutral, but heavier than `anchor`/`response`/`turn`. Default:
   keep `affordance` (alternatives `field`/`gate` are input-biased or collide with ISS).
2. **Concrete vs abstract shape.** This draft **fixes** the `_reserved.interaction` shape (§3.1) + the `I-*` family —
   the operator-chosen option, mirroring how leg-2 fixed `context_object`. The shape carries `interaction_version: 1.0`
   so it can evolve.
3. **`surface` name collision.** "Interaction surface" (whole canvas) vs `panel_link.surfaces` (output-subclass region).
   Default: keep both, disambiguate in prose (§3.3 NOTE).
4. **Is `surface state` a real primitive or derived sugar?** Largely a fold over the log. Default: keep it (the loop's
   re-read referent + the bridge to leg 2), MUST-be-recomputable so it never goes authoritatively stale.
5. **Four affordance kinds — right cut?** Is `choice` just constrained `input`? Default: keep four (each maps to a
   distinct `I-*` rule; the `options`-iff-`choice` check needs the distinction).
6. **Conformance home.** Fold `I-*` into [[spec_conformance_suite]] (default, matches `A-5`/`A-7` precedent) vs. a
   standalone leg-3 suite. If folded, the suite gains an `I-*` family **at ratification** (a separate ratified edit).
7. **Version bump.** Ratifying leg-3 adds a new `_reserved.interaction` key (additive, like `context_object` landed).
   Default: ship `standard_version: 2.0.2` + `interaction_version: 1.0`; the operator cuts the Standard version at a
   deliberate release.
8. **Participant identity model.** Default: minimal `{kind, id}`, both optional/advisory; richer identity/authz is out
   of scope (closer to OIP/ISS turf).
9. **P4 POC.** Confirm the stretch POC is the minimal loop (operator annotates → agent re-reads as context → responds),
   built as a read-only extension of `canvas_context`, not a capture runtime. Default: yes, if budget remains (D4).
