---
type: context
created: 2026-06-30
updated: 2026-06-30
status: active
last_edited_by: agent_mondrian
tags: [docs, explainer, canvas, standard, thesis, context_object, rlhf, conformance]
---

# The aDNA Canvas Standard — what it is and why it exists

> A narrative companion to the normative spec ([`spec_adna_canvas_standard.md`](../specs/spec_adna_canvas_standard.md)).
> The spec is the contract; this is the *why*.

## In one paragraph

The **aDNA Canvas Standard** is an agentic-context-native fork of Obsidian **Advanced Canvas** (v5.6.6) and
**JSON Canvas** (1.0). It treats a *canvas* — a set of positioned, possibly-linked panels carrying **text ·
typography · image · video · shape · embed · link** components — as a **near-universal output primitive**, and
then makes that primitive first-class for agents: something an AI can *read as context*, *render as output*, and
*interact through*. Canvas.aDNA owns the Standard and ships its runnable reference tooling (`canvas_std`).

## Why fork instead of invent

Papers, blog posts, websites, letters, pitch decks, comics, PDFs, and slide decks look like different formats,
but they are all **assemblies of the same component classes with position and qualities**. Building a separate
generator, schema, and quality loop for each one duplicates the same 2D-layout semantics over and over.

Obsidian's Advanced Canvas / JSON Canvas already solves the hard part — an open, human-editable spatial document
format with nodes, edges, and groups. Rather than reinvent it, the aDNA Canvas Standard **forks it** and adds
exactly what agentic use needs: typed components, reading-order and pagination semantics for non-DAG outputs, a
context-object model, and an interaction grammar. One grammar, many outputs.

## Fork, don't drift — the `_reserved` contract

The single most important design rule: **a valid aDNA canvas must degrade to a valid Obsidian canvas.** Open any
aDNA `.canvas` in vanilla Obsidian and it renders — no errors, no special plugin required.

This holds because every aDNA-native extension lives **additively** in a namespaced **`_reserved`** block that a
baseline reader simply ignores. The Standard introduces **no** new top-level node or edge types; the baseline
floor (nodes, edges, groups) is untouched, and all the richer semantics ride in `_reserved`. That is what "fork,
don't drift" means: the Standard evolves without ever breaking round-trip compatibility with its upstream.

## Source and view

A canvas has two faces:

- an **authoritative source** (a `.lattice.yaml` / source contract — the structured truth), and
- a **`.canvas` view** (the spatial, Obsidian-renderable layer).

The **Round-Trip Protocol** keeps them in sync (a stable `sync_hash`, a `diff`/`merge` contract). This split is
what lets a canvas be *both* a machine-readable context object *and* a human-editable visual document without
either one drifting from the other — edits to the view reconcile back to a reviewed source draft, never a silent
overwrite.

## Conformance levels

A document declares its level in `_reserved.conformance_level`:

| Level | What it carries | Degrades to |
|-------|-----------------|-------------|
| **Core** | the baseline node/edge floor | plain Obsidian |
| **Extended** | Core + styling / qualities | Core |
| **aDNA-Native** | the full `_reserved` grammar — component model · panel/link semantics · context-object · interaction | Extended → Core |

The conformance harness (`what/code/canvas_std/tests/fixtures/`) checks that each level validates *and* that it
degrades cleanly to the one below — degradation is a tested property, not a hope.

## Substrate-neutrality — contracts, not engines

The Standard specifies **contracts**, never rendering engines. Application-specific rendering, layout,
composition, and image generation are **out of scope** and belong to producers. This is the substrate-neutrality
test: if a rule is about *how a particular output looks*, it belongs in a producer; if it is about *what a canvas
means*, it belongs in the Standard.

In practice: the in-vault `what/production/` generators build canvases; **ComfyUI** renders images (a producer
puts the assembled prompt in the canvas as metadata and never renders it); **Astro** owns web; the `iii/` quality
framework owns review. The Standard writes the contracts they conform to.

## The three legs

The thesis is that a canvas is not just an output format but a first-class agentic primitive along three axes —
all three now runtime-enabled:

1. **Output primitive.** One grammar expresses many 2D outputs. Proven by **7 conformant producers** (brief,
   deck, document, diagram, comic, letter, post) — each a domain spec → an aDNA-Native `.canvas`, with the
   Standard's floor untouched.
2. **Context object.** A canvas can be **loaded and traversed *as context* — without rendering it**. The
   `canvas_context` loader turns a `.canvas` into a traversable `ContextGraph` (`reading_order()`, `refs()`,
   `summary()`), so an agent can assemble a canvas into a prompt/context window directly.
3. **Interaction surface.** A canvas is a **human↔AI / human↔human interaction surface** — typed affordances
   (`input` / `choice` / `annotation` / `action`) anchored to nodes, plus an append-only **response log**. A
   response advances the *view* and reconciles to a reviewed source draft (never a silent write). This layer was
   cut into **Standard v2.2.0**.

### The capture-substrate story

The interaction leg is quietly the most differentiated: it makes a canvas a **preference-capture substrate**.
An anchored, participant-tagged, append-only record of *what was presented and what a human did* — a selection,
an edit, an annotation — is exactly the raw material of preference learning. The Standard **owns the capture
grammar**; the *training-signal interpretation* (how a capture becomes an RLHF signal) is owned by the quality
framework (III). A working instance already exists for the image domain, where human selections project into the
III learning store. Canvas owns the substrate; III owns the schema; the seam between them is a projection.

## How the Standard evolves

Normative changes go through a **Lattice Improvement Proposal (LIP)** — propose → review → ratify — recorded in a
LIP registry (`adr_003_standard_governance.md`). Editorial/errata changes may skip the full LIP at the
maintainer's discretion. Versioning is semver at the Standard level (currently **v2.2.0**), distinct from the
reference-implementation package version.

## Where to go next

- The normative text: [`spec_adna_canvas_standard.md`](../specs/spec_adna_canvas_standard.md) (+ the 8 companion specs in [`what/specs/`](../specs/)).
- Build something: the [Producer Quickstart](canvas_producer_quickstart.md).
- The identity decision: [`adr_000_canvas_identity.md`](../decisions/adr_000_canvas_identity.md).
- The reference implementation: [`what/code/canvas_std/`](../code/canvas_std/).
