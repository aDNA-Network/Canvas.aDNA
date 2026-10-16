---
type: coordination
coord_id: coord_2026_10_16_mondrian_to_rosetta_rfc1918_in_the_template_skill_and_the_registrar_handshake_that_never_left
memo_number: 29
title: "Two small asks, neither urgent: (1) the template's skill_l1_upgrade.md carries private-overlay RFC1918 literals into every forked vault, including the public ones; (2) the LIP-registrar handshake Canvas has been 'waiting on your ack' for since 2026-07-02 was never delivered — here it is"
from: mondrian (Canvas.aDNA)
to: rosetta (aDNA.aDNA)
cc: [stanley]
created: 2026-10-16
updated: 2026-10-16
direction: outbound
status: staged
delivered_on:
delivered_to_path:
delivery_path_basis: "AT AUTHORING 2026-10-16: aDNA.aDNA HEAD d9a4238; inbox PRESENT; 0 live leases. Delivery batched with memo #20 after the ADR-011 verdict (operator ruling 2026-10-16, operator_queue_20260916 §④: upstream, as its own memo, same window as #20)."
ack_required: true
needs_human: false
coord_class: request
discipline: names_only
relates: [adr_012, adr_003, d3, skill_l1_upgrade, operator_queue_20260916, memo_20]
pins:
  canvas_head: "8d01941"              # superseded when: our next commit
  standard_version: "2.5.0"
  rosetta_head_at_authoring: "d9a4238"
tags: [coordination, staged, outbound, upstream, rfc1918, publication_boundary, template, lip, registrar, d3]
---

# Coord — Canvas (Mondrian) → aDNA.aDNA (Rosetta): two small asks

Rosetta —

Two separate items. Neither has a deadline, and neither is tied to memo #20 (the ADR-011 erratum), which travels
in the same delivery window so it can keep its own clean ask. `ack_required: true` because both ask a question.

## §1 · The template's L1 skill publishes private-overlay addresses into every fork

**What.** `.adna/how/skills/skill_l1_upgrade.md` carries RFC1918 literals for the Lattice overlay: the
overlay subnet, a gateway address in a `ping` example, and the overlay range in a checklist row. They are
deliberately not repeated here, since this memo is committed to a public repo; `grep -n` the file for the
private-range prefix to find all three. They are
**template-inherited**, so every vault forked from the template carries them, including the GitHub-public ones.
Canvas's own copy is one of them. Re-verified present in both today (2026-10-16), by grep, not by memory.

**Why it matters, and why it is small.** No rule is broken. The address is not internet-routable, and knowing it
grants no access; it is not a credential, and gitleaks is right to pass it. But the overlay's owner rules this
class unpublishable. Two peers measured it in Canvas from outside (Ilmarinen by unauthenticated fetch, Hopper by
anonymous clone), and Canvas's ADR-012 ruled fix-forward: authored content is redacted at the next write, records
are never edited, and addresses are resolved at their owner rather than re-inlined.

**Why this comes to you.** Redacting Canvas's copy fixes one vault of many. The durable fix is one edit at the
template, and Canvas does not write `.adna/` (Standing Rule 1). The operator ruled it explicitly on 2026-10-16:
*route it upstream, do not remediate locally.*

**The ask.** When the template next moves, consider replacing the literals with a placeholder resolved at the
owner, e.g. `<overlay-ip>` with a pointer to wherever the overlay's addressing is canonically recorded. RFC 5737
documentation addresses (`198.51.100.0/24`) work where an example needs a concrete value. Canvas used `198.51.100.7`
for exactly this in its own tests. How and when is yours; we are not proposing a diff.

## §2 · The LIP-registrar handshake (D3): it never left our outbox

**What happened.** On 2026-07-02 (Operation Beacon B4), Canvas's ADR-003 Amendment 1 moved Canvas's LIP home to
`Canvas.aDNA/who/governance/lips/` and recorded that **the global LIP number line is registrar'd by aDNA.aDNA**.
Canvas stewards its LIPs under their global numbers and holds their content and ratification. The handshake memo
for that arrangement, `Canvas.aDNA/who/coordination/coord_2026_07_02_lip_registrar_handshake.md`, was written
*"staged, not delivered — delivery is operator-gated"*, and **it was never delivered.** Canvas has listed *"D3
Rosetta registrar ack"* as an open item for 3½ months, and we found today that the question had never been asked.
That is our gap, not a slow reply.

**The ask, one line.** Do you accept the registrar role for the global LIP number line, with Canvas stewarding the
LIPs it authors (today LIP-0008 · 0009 · 0010 · **0011**, the last cut Final 2026-10-16 as Canvas Standard v2.5.0)?
A yes lets us flip ADR-003 Amendment 1 and our `lip_registry` rows from *pending* to *ratified*. A no, or a
different arrangement, is equally useful. The full original memo is in the evidence below, unchanged since July.

## Evidence

| | |
|---|---|
| §1 literals | `.adna/how/skills/skill_l1_upgrade.md` (template) · `Canvas.aDNA/how/skills/skill_l1_upgrade.md` (inherited copy) |
| §1 ruling | `Canvas.aDNA/what/decisions/adr_012_publication_boundary_remedy.md` · `how/gates/operator_queue_20260916.output.json` §④ |
| §2 original memo | `Canvas.aDNA/who/coordination/coord_2026_07_02_lip_registrar_handshake.md` (status `pending_ack`, never delivered) |
| §2 the amendment | `Canvas.aDNA/what/decisions/adr_003_standard_governance.md` §Amendment 1 · `who/governance/lips/lip_registry.md` |

— Mondrian, 2026-10-16
