---
type: coordination
created: 2026-06-06
updated: 2026-06-06
status: open
last_edited_by: agent_stanley
tags: [coordination, naming, persona, exception, genesis]
---

# Coordination — Canvas.aDNA Naming & Persona Exceptions (genesis P0)

Audit-transparency record for two `skill_project_fork`/governance exceptions taken at genesis.

## 1. Naming exception (ADR-009 §3)

- **Directory:** `Canvas.aDNA/` (CamelCase).
- **`skill_project_fork` Step 1** validates `[a-z][a-z0-9_]*` (snake_case). `Canvas` fails the pattern (leading uppercase).
- **Override:** operator-directed (architect brief: `project_name = Canvas → Canvas.aDNA/`). This is the standard **ADR-009 §3 grandfathered exception class** used by every sibling `*.aDNA` vault (CanvasForge.aDNA, LiteratureForge.aDNA, III.aDNA, …). No remote/path-style implications.
- **Disposition:** accepted; no action required.

## 2. Persona — ✅ RESOLVED (Mondrian, locked at P0 2026-06-06)

- **Locked: Mondrian** (operator, P0 gate). Seshat / Mercator considered and set aside. See `adr_000` §2.
- Working persona set to **Mondrian** (operator's prior pick in the planning exchange).
- Per the architect brief, **persona locks at the P0 gate** by the operator. Candidates carried for the lock:
  - **Mondrian** — universal visual language from minimal grid elements (canvas-as-composition).
  - **Seshat** — Egyptian goddess of measurement, records, and "stretching the cord" (laying foundations); the measure-and-record counterpart to LiteratureForge's **Thoth**. Strong standard-bearer/records fit.
  - **Mercator** — cartographer/projection; thematically matches the campaign codename "Operation Cartography."
- Distinctness check vs existing personas (Berthier, Hermes, Iris, Argus, Ariadne, Pygmalion, Asclepius, Mnemosyne, Hygieia, Daedalus, Spock, Thoth, Franklin, Mentor, Venus, Hypnos, …): all three candidates are non-overlapping.
- **Disposition:** ✅ locked **Mondrian** at the P0 gate (`what/decisions/adr_000_canvas_identity.md` §2, ratified 2026-06-06).
