---
type: backlog
idea_id: idea_rfc1918_authored_path_census
title: "An RFC1918 census line in the gate manifest, scoped to AUTHORED paths only: ADR-012's 'discipline, no enforcement surface' failed on ADR-012's own door"
created: 2026-10-16
updated: 2026-10-16
status: open   # awaiting operator ruling; it would be a new decision beside ADR-012, not an amendment to it
priority: medium
origin: "Vernier, 2026-10-16: the ADR-012 re-probe before its ratification"
executor_tier: sonnet
token_budget_estimated: "half a session: one Gate entry + a path classifier + a planted-probe test both ways"
tags: [backlog, publication_boundary, rfc1918, adr_012, gate_manifest, census, discipline]
---

# Idea — an RFC1918 census line for authored paths

## Why

ADR-012 (ratified 2026-10-16) rules that overlay addresses, ports and node inventory are **never re-inlined
into this repo**. Its Decision 5 is honest that **no enforcement surface is claimed**: the remedy is
authoring discipline. On the evidence, that discipline has failed once and nearly failed a second time:

1. **Failed once.** The `adr_012_ratification` and `operator_queue_20260916` doors, rendered 2026-09-16 (after
   the ADR was written on 09-04), quote the overlay subnet in their own analysis text. They were pushed public on
   09-17. The ADR's own body is clean; the door that asked for its signature was not.
2. **Nearly failed twice.** Memo #29's first draft (2026-10-16) quoted the same subnet. It was caught before
   commit only because the author happened to grep.

Both slips have the same shape: an agent describing the defect writes the defect. ⇒ ***the sentence that
names a forbidden literal is the likeliest place to contain one.***

## What it would be

A `gate_manifest.py` entry, `publication_boundary`, that runs a PCRE census of the RFC1918 class over tracked
files and **fails only on authored paths**. Records are exempt by ADR-012 Decision 2 (correspondence sent and
received, `how/sessions/`, `state_archive_*`, closed-campaign artifacts, **ruled** door records). The census
prints the records it skipped, so the exemption is visible on the line rather than silent.

⚠ Two traps measured while scoping this, both to be encoded as tests:
- `git grep -E` with `\b` **silently returned 0** on this vault (ERE has no `\b`), a cross-check that cannot
  fail. Use `-P`, and test with a planted literal both ways.
- The template-inherited `how/skills/skill_l1_upgrade.md` is authored-but-not-ours (`.adna/` is Rule 1). It
  needs an explicit, named allowlist row pointing to memo #29, so it is not a permanent red light and not a
  silent pass either.

## What it would not be

Not a secret scanner. gitleaks is right to pass an IP: it is not a credential. Not a fleet tool, because
Ilmarinen named the gap as having no enforcement surface anywhere and this vault does not claim one for the
fleet. Not a history rewrite (ADR-012 Decision 1). This is a local gate on this vault's own next write.

## Operator decision needed

Adopt (a new ADR or a P6 hygiene objective) · defer · decline. If adopted, ADR-012 Decision 5's *"no
enforcement surface is claimed"* gains a dated note: *a local one exists, scoped to authored paths.*
