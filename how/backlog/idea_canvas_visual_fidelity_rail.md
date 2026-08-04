---
type: idea
title: "Visual-fidelity rail — canvas-visual-check CLI + agent-confirmed-render doctrine"
created: 2026-08-03
updated: 2026-08-03
status: accepted
graduated_to: "campaign_canvas_halftone phase HV (2026-08-03 operator scope amendment)"
proposed_by: "robert_kennedy (Oration.aDNA) — inbound coord 2026-08-03; filed by Mondrian per Kennedy's ask #2"
last_edited_by: agent_mondrian
tags: [idea, visual_fidelity, traps, cli, doctrine, kennedy, graduated]
---

# Idea: Visual-fidelity rail — make "looks right in Obsidian" a checkable, doctrinal gate

## The problem (Kennedy/Oration incident, 2026-08-03)

`Oration.aDNA/what/artifacts/canvas_oration_map.canvas` (53 nodes) passed `canvas-std 2.3.0 … [OK]` and rendered
unreadable (~20/23 text nodes clipped; group labels ellipsised; edge labels as opaque boxes; file cards ~80%
Properties table). Root cause: Obsidian canvas text nodes are `display:flex; flex-direction:column` — margins
don't collapse; a `##` lead costs **98.9px** before any body text. Nothing in the standard, validator, producer
skill, or quickstart warns of this. Full evidence:
`who/coordination/coord_2026_08_03_kennedy_to_mondrian_canvas_visual_fidelity.md`.

## The idea (Kennedy's shape, ascending cost)

(a) execute the never-taken adoption step — agent-confirmed render as doctrine (`context_canvas_visual_in_the_loop.md`,
HOME-CV-3); (b) give the implemented traps a CLI — `canvas-visual-check`, sibling of `canvas-std validate` — and
register them in `canvas_reviewers.yaml`; (c) close the four uncovered gaps (edge-label geometry · group-label
truncation · file-node Properties preview · `text_metrics.py` calibration); (d) publish authoring guidance with
real numbers. Contributed working code: `Oration.aDNA/how/campaigns/campaign_ripple_of_hope/artifacts/canvas_fit_check.py`.

## Disposition

**Accepted + graduated 2026-08-03** — folded into Operation Halftone as phase **HV** (operator scope amendment;
executed at plan approval). Work register: `campaign_canvas_halftone` gap **G7**; mission
`mission_hv_visual_fidelity.md`. Renderer-side file-node preview fix remains a deferred follow-up (documented
limitation; the static trap covers the failure mode).
