# Canvas Overview

The canvas is the substrate primitive of CanvasForge. Every artifact —
deck slide, comic page, topology diagram, sequence canvas — is a canvas
being carried from intent to delivery.

## Substrate vs application

Substrate code lives in `canvas_core/`. Application code (deck, comic,
diagram) layers on top via lattice configuration.

## Voice register governance

Wrappers declare their voice register via the `voice_register:` block at
the lattice level. R11 (Patient's Voice) gating is canonical substrate
capability.

## Federation pattern

Consumers create lightweight wrapper directories that pin canvas-forge
lattice versions via `federation_ref:` blocks.
