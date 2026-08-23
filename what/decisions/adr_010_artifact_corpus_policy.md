---
type: decision
adr_id: "010"
title: "Artifact corpus policy — gitignored, canonical on-node, backup-registered"
status: proposed
created: 2026-08-22
updated: 2026-08-22
last_edited_by: agent_mondrian
signed_by:
supersedes:
superseded_by:
phase: halftone-close
resolves: "PT-P5 residual call #1 (what/artifacts/ git-tracking) · Lumière RM-09 standing risk · Iris panel-export question (b)"
tags: [adr, artifacts, corpus, git, backup, data_plane, halftone]
---

# ADR-010 — Artifact corpus policy

## Status

**proposed** — authored at the 2026-08-22 review-integration session under the operator-approved plan
(which selected this option at plan time); awaiting the §7.7 signature.

## Context

`what/artifacts/` is the vault's rendered-evidence shelf: **292 MB** on disk as of 2026-08-22, including the
H3 first-light corpus (`h3_first_light/`, 166 MB, 42 files SHA-256-verified, $3.618 of paid renders), the HR
review-surface pilot, calibration runs, and pre-Halftone evidence. It has been **gitignored since v7.0**
(`.gitignore:72`, publishing-pipeline rule).

Three independent inbound threads converged on this one unmade decision:

1. **Hestia's relocation-complete memo, open call #1** (`coord_2026_06_22_hestia_to_mondrian_canvas_relocation_complete.md`) —
   gitignored = lean repo, but the 957-green suite run depends on local data; tracked = reproducible-on-clone
   at +125 MB (now +292 MB and growing).
2. **Lumière RM-09 standing risk** — a node rebuild loses the H3 corpus.
3. **Iris's panel-export question (b)** — is the corpus fetchable off-node? (Videos' X1 mitigation already
   assumes "no": run on this node or name their own corpus location.)

Constraints: the repo is **GitHub-public** (Git.aDNA P6 Wave 2); render runs will keep growing the shelf
(H3 alone was 27 images; a 32-page book at scale is R9 territory); Home.aDNA **WI-16** records that no node
backup destination exists yet and that the candidate volume is ExFAT (no symlinks — file-copy backups are
already ruled out fleet-wide; `tar`/`restic`-class only).

## Decision

**`what/artifacts/` stays gitignored. It is the canonical on-node corpus location. Durability is a backup
concern, not a git concern.**

1. **Gitignored, permanently.** Rendered pixels are data-plane, not context. A GitHub-public repo does not
   carry a growing image corpus; git history is the wrong durability mechanism for artifacts that are
   append-only evidence, not collaboratively-edited text.
2. **Canonical location.** `Canvas.aDNA/what/artifacts/` is the corpus's one authoritative home on this node.
   Consumers that need the pixels off-node name their own corpus location and copy at their seam (Iris's X1
   mitigation is the endorsed pattern).
3. **Backup-registered.** The corpus is declared **in scope for the node backup** (Home WI-16). The relocation
   ack memo to Hestia carries this registration; the backup mechanism (tar/restic-class, ExFAT-safe) is
   Hestia's to implement — Canvas's obligation is to keep the shelf's layout stable and its evidence
   SHA-256-manifested so a restore is verifiable.
4. **No off-node fetch path today.** None is promised. If one materializes later (e.g. a private corpus
   remote, a Nextcloud share under the Keystone cohort), it arrives as its own decision — this ADR does not
   pre-commit to one.
5. **Provenance floor.** Every paid-render corpus directory carries (as `h3_first_light/` already does) a
   README + hash manifest sufficient to detect loss or tamper after a restore.

## Consequences

**Accepted:**
- A fresh clone cannot re-run evidence-dependent checks without the node's corpus (or a restored backup).
  The full test suites (`canvas_std` 115/10, producers, `comic_render`) do **not** depend on the corpus;
  only evidence-replay does. That trade is knowingly kept.
- Durability now depends on WI-16 actually closing. Until a backup destination exists, the corpus remains
  single-disk — this ADR converts that from an unowned risk into Hestia's named backlog item.

**Reversibility:** high. Nothing prevents a later decision to snapshot a specific corpus into a dedicated
archive repo; this ADR only rules that the *working shelf* is not git-tracked.

## Alternatives considered

- **Track in git** — reproducible-on-clone, but +292 MB on a public repo, growing per render run; git is a
  poor store for large binary evidence. Rejected.
- **Separate corpus repo / annex** — fetchable off-node if remoted, but more moving parts and still needs a
  private remote decision the fleet hasn't made. Deferred, not rejected (see Decision 4).

## Ratification (§7.7)

| Field | Value |
|-------|-------|
| Decision | `what/artifacts/` gitignored · canonical on-node · backup-registered (WI-16 scope) · no off-node fetch path promised |
| Ratified by | _(pending)_ |
| Date | _(pending)_ |
| Status | **proposed** |
