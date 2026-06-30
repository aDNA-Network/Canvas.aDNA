---
type: artifact
artifact_type: positioning_assessment
mission_id: mission_lodestar_review
campaign_id: campaign_canvas_lodestar
created: 2026-06-30
updated: 2026-06-30
status: active
last_edited_by: agent_mondrian
tags: [lodestar, review, positioning, rlhf, primitive, context_graph, lip_0009]
---

# Lodestar Positioning Assessment

> **Deliverable 2 of 3** (Operation Lodestar P1 review) — the headline. Where Canvas sits vs the operator's vision; built vs genuinely-new; per-framing verdicts; the **D1 ambition** recommendation; the **D2 LIP-0009 re-open** recommendation. Evidence-based — the review *recommends*; the operator *decides* at P2.

## The vision, restated

The operator's framing: the aDNA Canvas Standard is *larger than* a fork of Advanced Canvas / JSON Canvas — it is a **core primitive of prompting / interaction / pattern-memorialization / RLHF** for aDNA, the Lattice Protocol, and context-graph systems generally.

## The one-sentence finding

**The vision is right, and most of it is already built — but it is unarticulated (and in one case, buried in a producer). The gap is naming and speccing, not engineering.** Every framing is *served today* by the `_reserved`-over-lattice-view model with git-diff-0 firewall discipline; nothing is blocked. That single fact shapes every verdict below — including the recommendation *not* to make the boldest claim yet.

---

## Per-framing verdicts

### (i) Prompting primitive — **spec-it**
- **Built:** the leg-2 `canvas_context` loader produces a `ContextGraph` with `reading_order()`, `summary()`, `refs()`, and traversal — it loads and traverses a canvas **as context, without rendering it** (`spec_canvas_context_loading.md`; `what/code/canvas_context/src/canvas_context/{model.py,loader.py}`). That is precisely the substrate for assembling a canvas into a prompt.
- **Gap:** no standard-level spec for *canvas → prompt / context-window assembly* — nothing defines how a traversal flattens into an **ordered, budgeted** context block.
- **Genuinely-new or unarticulated?** Unarticulated. The hard part (load+traverse without render) is done; "serialize a `ContextGraph` to a prompt" is one more reduction.
- **Why spec-it:** cleanest of the four — a thin, additive contract on a proven loader; rides `_reserved`; no core change.

### (ii) RLHF / feedback-signal — **spec-it (the seam)**
- **Built — and *operational*, not adjacent:** a full **Canvas-as-RLHF-surface** package exists at `what/production/canvas_core/rlhf/` — `SelectionRecord` (`schemas/selection_record.json`), `backprop.py` (atomic corpus writes + audit log), `iii_bridge.py::selection_to_iii_signal` (a pick → an III **ADR-005** RLHF signal), and `canvas_comic/_rlhf_hints.py` (reads the III store **back into prompt assembly**). **13 live selection records** at `what/artifacts/image_gen_dataset/`. For the image domain, the feedback loop already closes.
- **Also built — generic but thin:** the leg-3 `_reserved.interaction` append-only `response` log + the `reconcile.py` advisory-reverse draft.
- **Gap:** the two substrates are **unconnected**; there is no generic `response`→RLHF-signal bridge analogous to `selection_to_iii_signal`; and the capability is undocumented as a *Standard* capability (the leg-3 spec frames the log as a "logged submission," underselling it).
- **Verdict:** spec the **seam** and generalize the *already-proven* bridge. The headline deliverable is a contract, not new architecture.

### (iii) Pattern memorialization — **defer**
- **Built:** the producer pattern proven 7× (`how/skills/skill_canvas_producer_build.md` + `what/production/_scaffold/`); `context_object` gives stable `id`+`version`+`refs`; "Registry Awareness" doctrine (`latlab lattice publish/pull/compose`).
- **Gap:** no capture/versioning/discovery **system** — `_scaffold/` is a *code* skeleton (not a content-pattern library), and the registry half is the **external** `latlab` registry, not Canvas-owned.
- **Why defer:** least-built, registry-dependent, **zero consumer pressure**. Building it now is gold-plating ahead of demand. (A thin "canvas-pattern = `context_object` + a `pattern` role + registry publish" spec is the cheapest first move *if* the operator wants momentum here — but it is not recommended now.)

### (iv) "The" context-graph primitive — **hold-open (re-open-LIP-0009: not yet)**
- **Built:** the `ContextGraph` model *is* a context-graph abstraction, and the three legs (output ×7 · context-object loader · interface runtime) together *are* "render / edit / interact." But it is **implied, never claimed** — every spec keeps canvas "a view of the `lattice` primitive" (`spec_interface_surface.md §1.4/§11`; `spec_context_object.md §3`).
- **Gap:** the architectural *claim* would elevate canvas view → primitive (the LIP-0009 question); it depends on the **unwritten** `aDNA.aDNA` OIP thesis (`adr_006 §3`; the leg-3 spec's OIP-grounding note); and the LIP-0009 evidence bar is unmet (D2).
- **Why hold-open:** this framing *is* the LIP-0009 question. Keep the door legibly open; it is the staged path's re-open target, not a now-action.

---

## The RLHF seam (framing ii — the subtle one, stated against what is on disk)

A clean boundary, so the spec-it follow-on inherits a contract rather than a contradiction:

- **Canvas owns the *capture substrate*** — the on-canvas grammar of "what was presented + what the human did": the leg-3 `_reserved.interaction` grammar (`affordance`·`anchor`·`response`·`turn`), the production `SelectionRecord` (prompt·variants·`pick_index`·`pick_reason`·`vr_scores`·`approver_id`), and the advisory-reverse `reconcile` draft (a human's *edits* as a structured, review-gated topology diff). These are anchored, participant-tagged, append-only records of human judgment on a 2D surface — a **preference-capture substrate, not merely an audit trail**.
- **III / ISS owns the *training-signal schema*** — the RLHF interpretation (`rlhf_signal_type`, session id, captured-at, consumer-namespace), the learning store, the graduation/frequency gates (`adr_006 §2`; `spec_interface_surface §11.1` defer "RLHF schema" to ISS).
- **The seam = a projection: a Canvas capture record → an III/ISS RLHF signal.** It **already exists** for images (`selection_to_iii_signal`); it is **missing** for the generic leg-3 `response` log.
- **⚠ One unreconciled ambiguity for the operator:** the docs name **ISS** as the RLHF-schema owner, but the live code routes through **III's ADR-005** learning store. Ownership is *unsettled in the docs but settled in code (III)*. The spec-it follow-on should resolve this explicitly, not inherit it.

**Net on (ii):** the "audit trail" framing is decisively underselling a latent (image-domain: realized) capability. `adr_006` still holds — III/ISS keep the *signal schema*; Canvas owns and should *name* the *capture substrate*.

---

## D1 — Ambition recommendation: **(c) Staged** — document/articulate now, re-position on evidence

*(Operator decides at P2. D1 was held open at P0 — "let the review recommend, evidence-based." Here is the evidence-based call.)*

- **The build is strong — not the gap.** 9 ratified specs, reference impl + CLI + JSON Schema, full C/E/A/I/D conformance, 7 producers, leg-2 loader + leg-3 runtime (386 tests green). Option (a)'s premise ("strengthen what exists") is largely *already true* on the engineering axis.
- **The framings are unarticulated/buried, not unbuilt.** The bottleneck is naming and speccing — exactly the spec-it verdicts above + the Track-B documentation work.
- **Option (b) "re-position as *the* context-graph primitive" is premature on two independent counts:** (1) it needs a LIP-0009 re-open whose bar is unmet (D2); (2) it depends on the **unwritten** `aDNA.aDNA` OIP thesis and modifies the core primitive set (owned by aDNA.aDNA, high blast radius) — ahead of both governance and its own dependency.
- **(c) is strictly (a)-now + an explicit evidence-gated path to (b) — and the articulation work *generates* the evidence.** Speccing (i) canvas-in-prompt and (ii) the RLHF seam, and documenting the build (Track B), create the very consumer surfaces that could later produce the concrete evidence LIP-0009 demands. (c) is not "do less" — it delivers value now *and* builds the evidence base for the larger claim, while keeping an explicit, legible re-open trigger.

**Why not (a) alone:** under-serves the operator's correct thesis and discards the re-open trigger. **Why not (b):** unmet bar + unwritten OIP dependency + core blast radius. **Therefore (c).**

Concretely, **(c) = spec-it (i) · spec-it-the-seam (ii) · defer (iii) · hold-open (iv) + the Track-B documentation sprint** that makes the strong build externally legible.

---

## D2 — LIP-0009 re-open recommendation: **No / not-yet** (keep Option V)

**The re-open bar, verbatim** (`Archive.aDNA/lattice-labs/how/governance/lips/lip_0009_canvas_as_primitive.md` §3):

> "Re-open **P** when a concrete consumer use-case forces it — i.e. a consumer needs canvas as a standalone primitive identity that a lattice-view demonstrably cannot serve. The reopening LIP carries that evidence."

**Against the three prongs:**

1. **"A concrete consumer use-case"** — *not met.* The four framings are strategic positioning, not consumers. The real consumers on disk (7 in-vault producers; external wrapper vaults in Astro/Websites/Network/Obsidian/…) consume canvas as **produced output / a federated producer**, not as a registry primitive.
2. **"Needs canvas as a standalone primitive identity"** — *not met.* No consumer needs canvas to be a 4th deployable type. Only framing (iii) even gestures at registry/federation identity, and it is unbuilt + registry-dependent.
3. **"That a lattice-view demonstrably cannot serve"** — *not met, and actively contradicted.* Every shipped capability rides `_reserved` over a lattice view with no core change — including the production RLHF package (which routes through III, not a canvas primitive). Six campaigns demonstrate the *opposite* of "cannot serve."

**Recommendation:** do **not** re-open Option P now; LIP-0009 records the canvas-stays-a-view deferral (Option V) as it already recommends. The operator's framing is positioning, not the concrete-consumer evidence the bar demands.

**The path to a future "yes" (keep the door legibly open):** the re-open runs through **framing (iii)**, *not* (i)/(ii). If a concrete consumer emerges that must **publish / pull / federate canvases as first-class registry entities** (the standalone primitive identity of prong 2), *that* is the evidence. The spec-it work on (i)/(ii) is firmly served by the view model and will **not** generate re-open evidence — only a real registry/federation consumer for canvas-as-pattern would.

**Adjacent blocker:** even were the bar met, there is **no LIP-governance home** today (A2/D3 — LIP-0008/0009 frozen in the archived vault, review clock lapsed). A re-open would have nowhere to route until D3 resolves. This reinforces "not now."

---

## Bottom line for the operator

Your thesis is correct and largely *already built*. The highest-value moves are to **articulate and document** what exists (Track B + spec-it (i)/(ii)), not to make the boldest claim (canvas-as-primitive) — that claim is unmet on the evidence bar, depends on an unwritten upstream thesis, and is best reached *after* the articulation work creates a real consumer. **Stage it.** The one genuinely-buried asset worth surfacing first: the working **Canvas-as-RLHF-surface** — name it, generalize its seam, and it becomes the most differentiated story Canvas can tell.
