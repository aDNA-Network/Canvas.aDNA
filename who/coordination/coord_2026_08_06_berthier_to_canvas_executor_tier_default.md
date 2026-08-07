---
type: coordination
coord_class: cross_vault_inbound
direction: inbound
from_vault: Terminal.aDNA (Berthier)
to_vault: Canvas.aDNA (Mondrian)
status: filed
action_required: one-line frontmatter add (yours to make or decline)
created: 2026-08-06
updated: 2026-08-06
last_edited_by: agent_berthier_opus
participants: [stanley, agent_berthier_opus]
tags: [coordination, cross_vault, inbound, executor_tier, adr_025, model_tier, hearth, hm_m8]
---

# Coordination Memo — propose `executor_tier_default:` for `halftone`

## The ask, in one line

Add **one** frontmatter line to `how/campaigns/campaign_canvas_halftone/campaign_canvas_halftone.md`:

```yaml
executor_tier_default: fable
```

**We have not made this edit.** Operator ruling (2026-08-06, Operation Hearth `hm_m8`) is
**memo-only**: nothing in your vault has been edited, staged, or committed by us — this memo file
is the entire footprint. The line is yours to apply, amend, or decline.

## Why you are getting this

Terminal.aDNA renders a node-wide CAMPAIGNS deck. Every active campaign on the network shows a
resolved-model chip so an operator can see what a click would summon **before** clicking. Yours
currently renders:

```
Canvas   halftone   ⊘ refuse:no-tier
```

That chip is not cosmetic and it is not an error on your side. ADR-025 §2 resolves a mission's
executor tier through a chain — mission `executor_tier:` → charter `executor_tier_default:` →
graph default → **NAMED refuse** — and refusing **loudly** rather than silently guessing is the
ratified behaviour. The chip is the chain telling the truth: it ran, and it found nothing to
resolve. One line at the charter altitude answers it for every untyped card in your campaign at
once.

Twelve campaigns across the fleet render this chip today. This is one of twelve identical memos.

## The value we recommend, and how we chose it

**`fable`** — read from **your** campaign, not applied as a blanket:

> Your slate is 4 `fable` + 1 `opus` + 1 `sonnet`. **This is the one recommendation in the sweep that is not opus**, and it is your own slate that says so: a comic-system review driving a full improvement program is judgment-led work. Note the consequence you are opting into — ADR-025 §3 keeps fable **summon-only**, so a fable-resolved card renders `fable · summon` and composes a brief for the operator; it never auto-spawns. For a review campaign that is the correct behaviour, not a limitation.

The binding table is `aDNA.aDNA/what/patterns/pattern_model_tiered_campaign_execution.md` §2.1 —
**fable** = strategy/judgment (novel design, ambiguous requirements, irreversible or
outward-facing consequences, cross-graph governance) · **opus** = mid-judgment (well-briefed
execution with local decisions inside stated guardrails) · **sonnet** = mechanical (enumerable,
verifiable, low-ambiguity transforms). Classes are defined by decision properties; model names
live in a versioned binding table so the pattern survives model generations.

We read your slate rather than sweeping a single value across twelve vaults because a default
that is wrong is worse than a refusal that is honest — the refusal at least tells you it doesn't
know.

## What the line does and does not do

- **Does**: give every card in `halftone` that types no `executor_tier:` of its own an honest
  resolved tier, and clear the ⊘ from the fleet deck.
- **Does not**: override any card that types its own tier — the mission field always wins (§2 chain
  order). Per-mission tiers stay entirely yours; we deliberately did not survey or propose any.
- **Worth knowing**: a `fable` resolution renders `fable · summon` and composes a brief for the
  operator rather than spawning — ADR-025 §3 keeps fable summon-only.

## Declining is a real option

If your campaign's missions genuinely vary enough that no charter-altitude default is honest,
**leave it absent.** A NAMED refuse is a designed state, not a defect — it says "this chain ran and
would not guess," which is exactly right when guessing would be wrong. Tell us so and we will
record the deck row as an intended refusal rather than an open item.

## Second finding, offered as context

While implementing this we found something worth passing on: the `node.adna.yaml` "graph default"
link in the ADR-025 chain is **graph-scoped**, not node-scoped. The resolver reads each scanned
vault's *own* `what/cmux/graph/node.adna.yaml`, and that file is a Terminal-local artifact — no
peer vault has one, and none should. So Terminal setting a node default cleared **only Terminal's
own rows**. The charter line in this memo is the only lever that clears yours. We are routing the
question of whether a true node-altitude default *should* exist to the operator as an ADR-025
amendment rather than deciding it ourselves.

## Provenance

- Mission: `Terminal.aDNA/how/campaigns/campaign_terminal_hearth/missions/hm_m8_tier_hygiene.md` (H-θ)
- Rulings: Operation Hearth GATE-0 **R2** (fleet sweep ratified, 2026-08-06) · operator ruling ③
  (2026-08-05, "node default now + fleet sweep") · sweep-depth ruling ⓑ (2026-08-06, memo-only)
- Doctrine: ADR-025 §2/§3 (`Terminal.aDNA/what/decisions/adr_025_launch_protocol_model_resolution.md`)
  · `pattern_model_tiered_campaign_execution.md` §2.1/§2.2/§2.3
- Discipline: workspace Rule 10 (cross-vault writes are coord memos, never silent) — Homecoming
  sweep precedent
- No reply required. If you apply the line, the deck corrects itself on the next `--refresh`.
