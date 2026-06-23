"""Leg-3 governed write — advisory-reverse reconciliation (Operation Armature P1).

Promotes the Salon P4 POC's **view-only** ``apply_response`` into a **governed runtime** that closes the
``read -> act -> re-read`` loop to the authoritative source (the ``.lattice.yaml``) via the *advisory* reverse path
(``spec_roundtrip_protocol_v2`` §1.2/§5): a response advances the **view**, and :func:`reconcile` produces a
**reviewed source DRAFT**. The runtime **never** writes the authoritative source — §1.2 is explicit that a tool
**MUST NOT** silently propagate canvas edits back to the source. Promoting a draft to the authoritative source is an
explicit human action *outside* this runtime.

What this adds over ``canvas_std.roundtrip`` (which it reuses, never rebuilds): the **governance layer** the reference
round-trip left to "a higher layer" — the staleness gate (§3.2), the §6 lossy-field restoration (§5 step 5), the
interaction-response review payload, and the never-touch-the-source discipline. ``merge`` / ``diff`` / ``to_canvas`` /
``compute_sync_hash`` do the topology work.

Firewall (D6): ``canvas_std`` is imported **read-only** (public API) and never mutated; the dependency is one-way
(``canvas_context -> canvas_std``). Serialization boundary: this takes the **parsed** source dict (the production
``.lattice.yaml`` is parsed by the caller — this package stays stdlib-only), mirroring how ``load_context_graph``
takes a parsed canvas.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from canvas_std import compute_sync_hash, diff, merge, to_canvas

from canvas_context.interaction import apply_response

# spec_roundtrip_protocol_v2 §6 — source-only fields NOT recoverable from the canvas view; they MUST be restored
# from the authoritative source on a reverse merge (the step ``merge``/``from_canvas`` deliberately drop at top level).
LOSSY_TOP_FIELDS: tuple[str, ...] = (
    "execution", "execution_mode", "fair", "federation", "federation_ref", "config", "lattice_type",
)
LOSSY_NODE_FIELDS: tuple[str, ...] = ("config", "data_mapping", "port", "type", "description")


@dataclass
class Reconciliation:
    """The result of an advisory reverse reconcile (``spec_roundtrip_protocol_v2`` §5).

    Carries a source **DRAFT** for human review — NOT an authoritative write. ``requires_review`` is always True
    (§1.2). Nothing here has been written to the authoritative source.
    """

    draft: dict[str, Any]                                       # merged source draft (_draft/_merged; §6 restored)
    responses: list[dict[str, Any]] = field(default_factory=list)   # interaction log, surfaced for review (NOT in source)
    topology_delta: dict[str, Any] = field(default_factory=dict)   # diff(source canonical view, view) — §5 step 3
    conflicts: list[dict[str, Any]] = field(default_factory=list)  # three-way merge conflicts (§5 merge rule)
    stale: bool = False                                         # view sync_hash != compute_sync_hash(source) (§3.2)
    requires_review: bool = True                                # reverse is advisory — a draft for human review (§1.2)


# --- helpers ------------------------------------------------------------------------------------


def _reserved(doc: dict[str, Any]) -> dict[str, Any]:
    block = doc.get("metadata", {}).get("frontmatter", {}).get("_reserved", {})
    return block if isinstance(block, dict) else {}


def _view_sync_hash(view: dict[str, Any]) -> str | None:
    sync = _reserved(view).get("sync")
    h = sync.get("sync_hash") if isinstance(sync, dict) else None
    return h if isinstance(h, str) else None


def _interaction_responses(view: dict[str, Any]) -> list[dict[str, Any]]:
    block = _reserved(view).get("interaction")
    responses = block.get("responses") if isinstance(block, dict) else None
    return [r for r in responses if isinstance(r, dict)] if isinstance(responses, list) else []


def _restore_lossy(draft: dict[str, Any], source: dict[str, Any]) -> None:
    """Restore the §6 source-only fields onto the draft (top-level + per-node).

    These are not recoverable from the canvas view, so a reverse merge MUST carry them through from the authoritative
    source (§5 step 5). Top-level (``fair``/``federation``/``execution``/…) is the genuine gap — ``merge`` returns only
    ``{name, version, nodes, edges, conflicts}``; the per-node pass is a defensive guard (``merge`` already starts each
    existing node from its source entry, so per-node fields are usually present — restored only if a node lacks them).
    """
    for key in LOSSY_TOP_FIELDS:
        if key in source and key not in draft:
            draft[key] = copy.deepcopy(source[key])
    src_nodes = {n["id"]: n for n in source.get("nodes", []) if isinstance(n, dict) and "id" in n}
    for node in draft.get("nodes", []):
        if not isinstance(node, dict):
            continue
        src = src_nodes.get(node.get("id"))
        if not isinstance(src, dict):
            continue  # a node introduced on the view has no source-only fields to restore
        for key in LOSSY_NODE_FIELDS:
            if key in src and key not in node:
                node[key] = copy.deepcopy(src[key])


# --- the governed reverse path ------------------------------------------------------------------


def reconcile(view: dict[str, Any], source: dict[str, Any], *, strategy: str = "yaml_wins") -> Reconciliation:
    """Reconcile a response-advanced view back to its authoritative source — **ADVISORY** (spec §1.2/§5).

    Produces a reviewed source DRAFT (never a write to the authoritative source): a three-way ``merge`` of the source
    with the edited view, with the §6 lossy fields restored, plus the interaction response log, a topology ``diff``
    delta, flagged conflicts, and a staleness verdict — all surfaced for human review. Mutates neither ``view`` nor
    ``source`` (``merge``/``diff``/``to_canvas`` are pure; ``_restore_lossy`` deep-copies).
    """
    # 1. staleness gate (§3.2) — has the source's topology changed since this view was generated?
    stored = _view_sync_hash(view)
    stale = stored is not None and compute_sync_hash(source) != stored

    # 2. topology delta (§5 step 3) — what the view changed vs the source's canonical view
    topology_delta = diff(to_canvas(source), view)

    # 3. merged source draft (§5 step 4) — three-way merge; conflicts flagged
    draft = merge(source, view, strategy=strategy)

    # 4. restore the §6 lossy fields (§5 step 5) + mark as a draft requiring review
    _restore_lossy(draft, source)
    draft["_draft"] = True

    # 5. surface the interaction responses — for review, NEVER written into the authoritative source
    responses = _interaction_responses(view)

    return Reconciliation(
        draft=draft,
        responses=responses,
        topology_delta=topology_delta,
        conflicts=list(draft.get("conflicts", [])),
        stale=stale,
        requires_review=True,
    )


def governed_apply(
    view: dict[str, Any],
    source: dict[str, Any],
    affordance_id: str,
    value: Any,
    *,
    participant: dict[str, Any] | None = None,
    turn: str | None = None,
    at: str | None = None,
    strategy: str = "yaml_wins",
) -> tuple[dict[str, Any], Reconciliation]:
    """The governed *act*: :func:`~canvas_context.interaction.apply_response` (advance the view, append-only) THEN
    :func:`reconcile` to an advisory source draft. Returns ``(advanced_view, reconciliation)``. Writes nothing to
    disk and mutates no input (``apply_response`` deep-copies; ``reconcile`` is pure)."""
    advanced = apply_response(view, affordance_id, value, participant=participant, turn=turn, at=at)
    return advanced, reconcile(advanced, source, strategy=strategy)


def write_source_draft(
    reconciliation: Reconciliation, path: str | Path, *, reviewed_by: str | None = None
) -> Path:
    """Write the DRAFT to ``path`` — a **separate** artifact (e.g. ``<source>.draft.json``), **never** the
    authoritative source. Stamps ``reviewed_by`` when a human has reviewed it (the §1.2 review gate). Promoting a
    draft to the authoritative source is an explicit human action OUTSIDE this runtime — the tool never does it
    silently. Returns the path written. (Refuses to overwrite anything but a ``*.draft.json`` sibling is the caller's
    discipline; this function only ever writes the draft it is given.)"""
    out = dict(reconciliation.draft)
    out["requires_review"] = True
    if reviewed_by is not None:
        out["reviewed_by"] = reviewed_by
    p = Path(path)
    p.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return p
