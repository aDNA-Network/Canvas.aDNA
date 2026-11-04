---
type: backlog
idea_id: idea_canvas_std_version_banner_single_source
title: "canvas-std prints three Standard versions in one install; derive every banner from STANDARD_VERSION (Lavoisier G4)"
category: tooling
status: proposed
priority: medium
effort: quick
proposed_by: agent_mondrian
proposed_date: 2026-11-04
updated: 2026-11-04
plan_id:
owner: mondrian
executor_tier: sonnet
target: "canvas_std strings: the next canvas_std firewall touch (operator-signed); the two READMEs: diagram_generator 0.2.0 / the same touch"
origin: "Aeneas memo coord_2026_11_03_aeneas_to_mondrian_diagram_gaps G4 (Operation Lavoisier M07 s1); verified session_stanley_20261104_083033_diagram_gaps_intake"
relates: [idea_diagram_readme_install_surface]
tags: [backlog, canvas_std, version_drift, banner, single_source, firewall, lavoisier]
---

# One install, three Standard versions

## Problem / Opportunity

`canvas_std/__init__.py:31` sets `STANDARD_VERSION = "2.5.0"`, and `canvas-std validate` prints it
(`conformance.py:110`). Hand-typed strings disagree: the argparse description "aDNA Canvas Standard v2.4.0 reference
tooling" (`conformance.py:87`), the `schema` help "print the v2.4.0 JSON Schema" (`conformance.py:94`), the
`json_schema` docstring (`conformance.py:69`), and `canvas_std/README.md:3,6` (v2.4.0). The producer README says
**v2.0.0** (`diagram_generator/README.md:3,5,35`), not v2.5.0 as the memo had it. Reproduced 2026-11-04 with the
producer venv: `--help` v2.4.0, `validate` 2.5.0.

## Proposed Solution

- `conformance.py`: build the description and help strings from `STANDARD_VERSION`; a test that `--help` contains it.
  This is inside `what/code/canvas_std/`, so it rides the next firewall touch, never a producer release.
- READMEs: state the Standard version once, or point to `canvas-std validate`'s banner as the authority.

## Discussion

- 2026-11-04 (agent_mondrian): The same family Datum hunted (a claim left beside its remedy). Small; not pressed by
  the migration.

## Decision
