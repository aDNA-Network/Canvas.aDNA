# aDNA Canvas Standard

**Canvas.aDNA** owns and ships the **aDNA Canvas Standard** — an agentic-context-native fork of Obsidian
**Advanced Canvas** (v5.6.6) and **JSON Canvas** (1.0), maintained by aDNA Labs.

> **Standard v2.2.0** · reference implementation `canvas_std` (105 passing / 10 skipped) · 9 ratified specs · 7 conformant producers.

## The thesis

A *canvas* — a possibly-linked set of panels carrying positioned **text · typography · image · video · shape ·
embed · link** components — is a near-universal **output primitive**. Papers, blog posts, sites, letters, pitch
decks, comics, PDFs, and slide decks are all assemblies of the same component classes with specified position
and qualities. By forking Advanced Canvas into an agentic-context-**native**, agentic-context-**developed**
standard, a canvas becomes simultaneously:

- **an output primitive** — one grammar for many 2D outputs (proven by 7 in-vault producers);
- **a context object** — read *as* context (load and traverse a canvas without rendering it), rendered *as* output;
- **an interaction surface** — a human↔AI / human↔human surface with typed affordances and an append-only response log.

The design rule is **fork, don't drift**: aDNA-native extensions live additively in a namespaced `_reserved`
block, so a valid aDNA canvas **degrades to a valid Obsidian canvas** — open it in vanilla Obsidian and it just
works.

## What's here

| Path | What |
|------|------|
| `what/specs/` | The normative Standard — **9 ratified specs** (core · component model · panel/link semantics · round-trip · context-object · conformance suite · federation contract · interface surface · context loading) |
| `what/code/canvas_std/` | The **reference implementation** — validators · round-trip converters · conformance harness · the `canvas-std` CLI · the JSON Schema |
| `what/production/` | 7 in-vault **producers** on `canvas_std` — `brief` · `deck` · `document` · `diagram` · `comic` · `letter` · `post` |
| `what/decisions/` | Architecture Decision Records (identity, governance, boundaries) |
| `how/` · `who/` | Operations (campaigns · skills · sessions) and governance |

## Quickstart

Validate a canvas against the Standard:

```bash
pip install -e what/code/canvas_std        # provides the canvas-std CLI
canvas-std validate path/to/file.canvas    # → "adna_native [OK]" | "core [OK]" | reported errors
```

- **Build a producer** (a generator that turns a domain spec into a conformant `.canvas`) — see the
  **[Producer Quickstart](what/docs/canvas_producer_quickstart.md)** (~15 minutes on the `_scaffold` skeleton).
- **New to the Standard?** Read the **[Canvas Standard Explainer](what/docs/canvas_standard_explainer.md)** for the what & why.
- **The normative text** lives in [`what/specs/spec_adna_canvas_standard.md`](what/specs/spec_adna_canvas_standard.md).

## Conformance levels

Every conformant document declares `_reserved.conformance_level`:

- **Core** — the baseline node/edge floor (round-trips to plain Obsidian).
- **Extended** — Core + styling / qualities.
- **aDNA-Native** — the full `_reserved` grammar (component model · panel/link semantics · context-object · interaction).

Higher levels **degrade** cleanly to lower ones; the certification fixtures
(`what/code/canvas_std/tests/fixtures/`) check exactly that.

## Governance & license

The Standard evolves through a **Lattice Improvement Proposal (LIP)** process — see
[`what/decisions/adr_003_standard_governance.md`](what/decisions/adr_003_standard_governance.md). The reference
implementation is MIT-licensed ([`what/code/canvas_std/LICENSE`](what/code/canvas_std/LICENSE)). To contribute,
see **[CONTRIBUTING.md](CONTRIBUTING.md)**.

---

*Canvas.aDNA is a **Platform.aDNA** standard-bearer (persona: Mondrian), maintained by aDNA Labs. Project
overview: [MANIFEST.md](MANIFEST.md) · operational state: [STATE.md](STATE.md).*
