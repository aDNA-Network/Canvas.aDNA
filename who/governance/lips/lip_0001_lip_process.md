---
type: lip
lip_number: "LIP-0001"
title: "LIP Purpose and Guidelines"
author: "Stanley Bishop"
status: accepted
created: 2026-03-07
updated: 2026-07-02
last_edited_by: agent_mondrian
migrated_from: "Archive.aDNA/lattice-labs/how/governance/lips/lip_0001_lip_process.md"
migrated_on: 2026-07-02
tags: [lip, governance, process, canvas]
---

# LIP-0001: LIP Purpose and Guidelines

> **Canvas-local working copy of the global LIP process** (LIP-0001, CC0), forked into the Canvas.aDNA governance home
> at Operation Beacon Phase B4 (2026-07-02). The predecessor lived at `lattice-labs/how/governance/lips/` (archived
> reader-only 2026-06-27 → `Archive.aDNA/lattice-labs/…`). The **global LIP number line is registrar'd by aDNA.aDNA**
> (D3 — handshake pending; see `who/coordination/coord_2026_07_02_lip_registrar_handshake.md`). Canvas stewards the
> Canvas-scoped LIPs (LIP-0008, LIP-0009) under their **global** numbers and holds their content + ratification. Paths
> below are adapted to the Canvas `who/governance/lips/` home.

## Abstract

A Lattice Improvement Proposal (LIP) is a design document providing information to the Lattice Protocol community, describing a new feature, process, or standard for the protocol. This LIP defines the LIP process itself.

## Motivation

As the Lattice Protocol matures toward progressive decentralization, changes to the protocol, aDNA standard, and governance processes need a transparent, documented, and community-accessible proposal mechanism. The LIP process provides this mechanism, modeled after established improvement proposal systems (BIP, EIP, PEP) but adapted for the Lattice context.

## Specification

### LIP Types

| Type | Description | Examples |
|------|-------------|---------|
| **Standard** | Changes to the protocol specification, aDNA standard, or federation primitives | New data types, API changes, schema modifications |
| **Process** | Changes to governance, operational procedures, or organizational structure | Council voting rules, campaign protocol amendments |
| **Informational** | Design guidelines, recommendations, or ecosystem information | Best practices, architectural rationale |

### LIP Lifecycle

```
Draft → Review → Accepted → Implemented → Final
                    ↓
                 Rejected
                    ↓
                Withdrawn
```

| Status | Description | Authority |
|--------|-------------|-----------|
| **Draft** | Initial proposal, open for feedback | Any contributor may author |
| **Review** | Formal review period (minimum 7 days) | Steward: Protocol (or FA if seat empty) opens review |
| **Accepted** | Approved for implementation | FA (Phase 0); Council vote (Phase 1+) |
| **Implemented** | Implementation merged/deployed | Author or assignee confirms |
| **Final** | Complete and immutable | Steward: Protocol (or FA) declares final |
| **Rejected** | Not accepted, with documented rationale | Reviewing authority |
| **Withdrawn** | Retracted by author | Author |

### LIP Numbering

- Sequential integers: LIP-0001, LIP-0002, etc.
- Numbers are never reused, even for rejected or withdrawn LIPs
- LIP-0001 through LIP-0009 are reserved for foundational process LIPs
- **The global number line is registrar'd by aDNA.aDNA** (D3, 2026-07-02). A stewarding vault (e.g. Canvas.aDNA)
  holds the *content* of its own LIPs under their globally-assigned numbers; the registrar arbitrates number
  assignment across vaults so the sequence stays collision-free.

### LIP Format

All LIPs use the template at `who/governance/lips/lip_template.md` and include:
- YAML frontmatter with type, number, title, author, status
- Abstract, Motivation, Specification, Rationale sections (mandatory)
- Backwards Compatibility, Reference Implementation, Security Considerations (as applicable)

### LIP Registry

The `who/governance/lips/lip_registry.md` file maintains the canonical index of the LIPs a vault stewards. The
cross-vault master index is maintained by the registrar (aDNA.aDNA).

### Review Process

1. **Author** creates LIP as Draft in `who/governance/lips/`
2. **Steward: Protocol** (or FA) reviews for completeness and opens formal Review period
3. **Community** provides feedback via vault notes or designated communication channel
4. **Reviewing authority** accepts, requests changes, or rejects with documented rationale
5. **Author** implements accepted LIP
6. **Steward: Protocol** (or FA) declares LIP Final when implementation is complete and verified

### Phase-Dependent Authority

| Phase | Draft Authority | Acceptance Authority |
|-------|----------------|---------------------|
| Phase 0 | Any contributor | Founding Architect |
| Phase 1 | Any contributor | Council simple majority |
| Phase 2+ | Any contributor | Council simple majority (Standard), supermajority (Process) |

## Rationale

The LIP process borrows from proven improvement proposal systems while keeping the overhead appropriate for a small founding team. Key adaptations: vault-native storage (not a separate repository), phase-dependent authority (grows with decentralization), and integration with the existing campaign/mission execution hierarchy.

## Backwards Compatibility

This is the first LIP. No backwards compatibility concerns. (This Canvas-local copy is a faithful fork of the global
process; it introduces no process change beyond adapting storage paths to the `who/governance/` tree and recording the
aDNA.aDNA registrar arrangement, which is itself pending the D3 handshake.)

## Copyright

This LIP is placed in the public domain via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

---
*LIP-0001 v1.0 | Campaign: campaign_org_genesis M6 | 2026-03-07 · Canvas-local fork: Operation Beacon B4, 2026-07-02*
