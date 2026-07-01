# Vision: Canvas as a Universal Output Primitive

*How a disciplined grammar of typed panels becomes the shared substrate for everything an agent draws, writes,
and shows.*

---

## The premise

Look closely at the things software produces on a two-dimensional surface — a paper, a blog post, a website, a
letter, a pitch deck, a comic, a PDF, a slide. They present as different formats with different tools. Underneath,
they are the same thing: **positioned panels carrying a small set of component classes** — text, typography,
image, video, shape, embed, link — with qualities, and with links between them.

Canvas.aDNA takes that observation seriously. If every 2D output is an assembly of the same components, there
should be **one grammar** for all of them — one schema, one validator, one round-trip contract, one quality loop
— and each specific output (a deck, a comic, a letter) becomes a *producer* on top of that grammar rather than a
bespoke reinvention of layout semantics. That grammar is the **aDNA Canvas Standard**, and this vault is its
standard-bearer.

Named for Piet Mondrian — who reduced composition to a grid of straight lines and primary fields in pursuit of a
*universal* visual language built from the fewest possible elements — the work here does the same for agentic
media: it reduces any 2D output to the smallest rigorous set of typed components on a canvas.

## Why a canvas, and why now

Agents are becoming the primary authors of documents, decks, diagrams, and pages. An agent needs an output it can
do more than *emit*: it needs one it can **read back as context**, **reason over**, **hand to a human to edit**,
and **learn from**. A flat rendered artifact (a PDF, a PNG) is a dead end — you cannot traverse it, diff it, or
capture what a human did to it.

A canvas is different. It is structured, spatial, round-trippable, and human-editable. Forking Obsidian's open
Advanced Canvas / JSON Canvas format — rather than inventing a new one — means every aDNA canvas is *also* a
document a person can open and edit in a tool they already have. We add exactly what agentic use needs, and
nothing that breaks that compatibility.

## Three legs

The ambition is that a canvas is not merely an output *format* but a first-class agentic primitive along three
axes — all three now built and runtime-enabled:

1. **Output primitive** — one grammar expresses many 2D outputs (proven by seven producers today).
2. **Context object** — a canvas can be loaded and traversed *as context*, without rendering, so an agent can
   assemble it directly into a prompt.
3. **Interaction surface** — a canvas carries typed affordances and an append-only record of what a human did on
   it, making it a place where human and agent meet, not just a thing the agent ships.

## The operating philosophy

- **Reduce to the grammar.** Find the smallest set of typed components and rules that expresses every 2D output.
  Application-specific behavior belongs in producers, never in the Standard.
- **Fork, don't drift.** aDNA-native extensions live additively in a namespaced `_reserved` block; a valid aDNA
  canvas always degrades to a valid Obsidian canvas. Round-trip compatibility is non-negotiable.
- **Specify contracts, not engines.** The Standard writes the contracts; rendering, image generation, and quality
  loops stay in their owning vaults (ComfyUI, Astro, III). Substrate-neutrality is the test for every rule.
- **Degrade, always.** Every richer conformance level degrades cleanly to a simpler one — and degradation is a
  *tested* property, not an aspiration.

## Where this is going

The Standard is technically strong and largely complete; the frontier is **articulation and evidence**, not
engineering. So the near-term path is deliberately staged:

- **Name what already exists.** The most differentiated capability — a canvas as a **preference-capture
  substrate**, an anchored, participant-tagged, append-only record of human judgment on a surface — is built and
  working in one domain. The Standard owns the *capture* grammar; the quality framework (III) owns the
  *training-signal* interpretation. Making that seam explicit turns a buried capability into a named one.
- **Articulate the prompting seam.** Serializing a canvas traversal into an ordered, budgeted context block is a
  thin, additive contract on the proven context loader — the cleanest next specification.
- **Keep the largest claim honest.** Whether a canvas should become a standalone *primitive* in the aDNA core
  (rather than a view of the lattice primitive) is a real question — but one we hold open until a concrete
  consumer *needs* it, not one we assert ahead of the evidence. The articulation work above is how that evidence
  gets built.

## Stewardship

Canvas.aDNA governs the Standard through a **Lattice Improvement Proposal (LIP)** process
([`what/decisions/adr_003_standard_governance.md`](../../what/decisions/adr_003_standard_governance.md)) and ships
its **runnable reference implementation** ([`what/code/canvas_std/`](../../what/code/canvas_std/)) so that
"conformant" means *testable*, not *asserted*. The Standard is versioned with semver; changes are reviewed, not
improvised; and the reference tooling is the arbiter of conformance.

## Start here

- The landing page: [`README.md`](../../README.md).
- The what & why: [Canvas Standard Explainer](../../what/docs/canvas_standard_explainer.md).
- The normative text: [`spec_adna_canvas_standard.md`](../../what/specs/spec_adna_canvas_standard.md).
- Build something: [Producer Quickstart](../../what/docs/canvas_producer_quickstart.md).

---

*This document states the long-term vision for the aDNA Canvas Standard. The three-leg foundation is built and
runtime-enabled; the positioning and adoption it enables are the work ahead.*
