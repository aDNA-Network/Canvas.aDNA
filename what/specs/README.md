# The aDNA Canvas Standard — normative specifications

This directory holds the **9 ratified specs** that jointly define the **aDNA Canvas Standard** (current version
**v2.2.0**). Start with the core spec; the rest are normative companions referenced from it.

> **Not to be confused with** the generic *aDNA Universal Standard* — the knowledge-architecture convention for
> `who/` · `what/` · `how/` vaults — at [`../docs/adna_standard.md`](../docs/adna_standard.md). *This* directory
> is the **Canvas** Standard: the 2D-output / canvas file format. New readers should start at the repo
> [README](../../README.md) and the [Canvas Standard Explainer](../docs/canvas_standard_explainer.md).

## The specs

| Spec | Defines |
|------|---------|
| [`spec_adna_canvas_standard.md`](spec_adna_canvas_standard.md) | **The core** — file format, document/node/edge schema, the `_reserved` carrier, conformance levels, the degradation contract |
| [`spec_component_model.md`](spec_component_model.md) | The typed component model (14 classes) |
| [`spec_panel_link_semantics.md`](spec_panel_link_semantics.md) | Panel/link semantics — flow, pagination, reading-order, anchors |
| [`spec_roundtrip_protocol_v2.md`](spec_roundtrip_protocol_v2.md) | The source ↔ `.canvas` round-trip contract |
| [`spec_context_object.md`](spec_context_object.md) | Canvas as a context object (`id` / `version` / `refs`) |
| [`spec_canvas_context_loading.md`](spec_canvas_context_loading.md) | Loading/traversing a canvas *as context*, without rendering (leg 2) |
| [`spec_interface_surface.md`](spec_interface_surface.md) | Canvas as a human↔AI interaction surface (leg 3) |
| [`spec_conformance_suite.md`](spec_conformance_suite.md) | The conformance / certification suite |
| [`spec_federation_contract.md`](spec_federation_contract.md) | The consumer federation contract |

All specs are `status: ratified`, `standard_version: 2.2.0`. Changes go through the LIP process
([`../decisions/adr_003_standard_governance.md`](../decisions/adr_003_standard_governance.md)). The runnable
reference implementation — validators, round-trip, conformance harness, the `canvas-std` CLI — is at
[`../code/canvas_std/`](../code/canvas_std/).
