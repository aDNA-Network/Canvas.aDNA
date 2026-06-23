"""Leg-3 interaction surface — a read-only extension of ``canvas_context`` (Operation Salon P4 POC).

Reference realization of ``spec_interface_surface.md`` (ratified 2026-06-22) §3.1 record shapes + the
``I-1``/``I-2``/``I-3``/``I-D`` conformance family. It **composes** the proven leg-2 ``ContextGraph`` — an
:class:`InteractionSurface` *has-a* ``ContextGraph`` and exposes ``affordances()`` / ``surface_state()`` accessors
over it (spec §10.2) — so the leg-2 loader is left byte-unchanged.

Two clearly-separated halves:

* **Reader (the *read* step — strictly read-only):** :func:`load_interaction_surface`, :class:`InteractionSurface`,
  :func:`validate_interaction_block`. Discovers affordances + surface state from ``_reserved.interaction`` over a
  leg-2 load (IX4); no renderer, capture runtime, or transport.
* **Reducer (the *act* + *re-read* steps):** :func:`apply_response` — a pure, **append-only** fold that logs a
  response and recomputes the surface state (IX5/IX6). It advances the **view** only (spec §7.2); it is **NOT** a
  capture runtime (that boundary is ISS's, ADR-006 §2), not a renderer, not a transport, and it never writes the
  authoritative ``.lattice.yaml`` (the governed round-trip write is ``spec_roundtrip_protocol_v2``'s job, §2).

Firewall (D6): ``canvas_std`` is imported **read-only** (public API incl. ``validate_interaction`` — the harness
I-* validator the consumer now delegates to, wired in at Armature P2) and is never mutated. The dependency is
one-way: ``canvas_context -> canvas_std``.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from canvas_std import ConformanceLevel, strip, validate_interaction
from canvas_std import validate as core_validate

from canvas_context.loader import load_context_graph
from canvas_context.model import ContextGraph

# The four affordance kinds partition what a participant can do at a point (spec §3.3 / IX3 — a *closed* enum).
# I-1/I-2/I-3 validation now lives in canvas_std (Armature P2, adr_007); this module keeps the enum it re-exports
# and the act-time value/kind guard apply_response() uses (_value_kind_errors).
AFFORDANCE_KINDS: tuple[str, ...] = ("input", "choice", "annotation", "action")


# --- §3.1 record shapes -------------------------------------------------------------------------


@dataclass
class Affordance:
    """One per ``_reserved.interaction.affordances[id]`` (spec §3.1). Declared statically with the canvas."""

    id: str
    anchor: str | None                                  # node id OR a panel_link.anchors label (§5; MUST resolve)
    kind: str | None                                    # input | choice | annotation | action (closed, §3.3)
    prompt: str | None = None                           # optional participant-facing label (not a render instruction)
    options: list[str] | None = None                    # REQUIRED iff kind == choice; else null/absent
    required: bool = False                              # whether a turn completes without a response here


@dataclass
class Response:
    """One per ``_reserved.interaction.responses[]`` (spec §3.1). Append-only; immutable once logged."""

    affordance: str | None                              # MUST reference a declared affordance
    value: Any                                          # kind-consistent (§4 IX5); null iff kind == action
    participant: dict[str, Any] | None = None           # {kind, id} — optional; surface works with kind=None (§7.1)
    turn: str | None = None                             # the read->act->re-read cycle this belongs to
    at: str | None = None                               # optional iso-8601; advisory


@dataclass
class SurfaceState:
    """The re-read target — the leg-2 graph folded with the response log (spec §3.1/§6). Recomputable (IX6)."""

    turn: str | None
    open: list[str]                                     # affordances still awaiting a response this turn


# --- the read face ------------------------------------------------------------------------------


class InteractionSurface:
    """A leg-2 :class:`ContextGraph` + an additive ``_reserved.interaction`` overlay (spec §3.1). Read-only.

    Construct via :func:`load_interaction_surface`. ``.graph`` is the underlying leg-2 read face; the accessors
    here are pure, side-effect-free reads over it. A canvas with no ``_reserved.interaction`` is a valid,
    *non-interactive* surface (``affordances() == []``); that is not an error (spec §8).
    """

    def __init__(self, graph: ContextGraph, doc: dict[str, Any], interaction: dict[str, Any] | None) -> None:
        self.graph = graph
        self._doc = doc  # raw canvas doc, kept by reference for re-derivation; never mutated here
        block = interaction if isinstance(interaction, dict) else {}
        self.interaction_version = block.get("interaction_version")
        self._affordances: dict[str, Affordance] = {}
        for aid, entry in (block.get("affordances") or {}).items():
            if isinstance(entry, dict):
                self._affordances[aid] = Affordance(
                    id=aid,
                    anchor=entry.get("anchor"),
                    kind=entry.get("kind"),
                    prompt=entry.get("prompt"),
                    options=entry.get("options"),
                    required=bool(entry.get("required", False)),
                )
        self._responses: list[Response] = []
        for r in block.get("responses") or []:
            if isinstance(r, dict):
                self._responses.append(
                    Response(
                        affordance=r.get("affordance"),
                        value=r.get("value"),
                        participant=r.get("participant"),
                        turn=r.get("turn"),
                        at=r.get("at"),
                    )
                )
        st = block.get("state") if isinstance(block.get("state"), dict) else {}
        self._declared_state = SurfaceState(turn=st.get("turn"), open=list(st.get("open") or []))

    def is_interactive(self) -> bool:
        return self.interaction_version is not None or bool(self._affordances)

    def affordances(self) -> list[Affordance]:
        return list(self._affordances.values())

    def affordance(self, affordance_id: str) -> Affordance | None:
        return self._affordances.get(affordance_id)

    def responses(self) -> list[Response]:
        return list(self._responses)

    def current_turn(self) -> str | None:
        """The current/latest turn — the declared ``state.turn`` if present, else the last responded turn."""
        if self._declared_state.turn is not None:
            return self._declared_state.turn
        turns = [r.turn for r in self._responses if r.turn]
        return turns[-1] if turns else None

    def open_affordances(self, turn: str | None = None) -> list[str]:
        """Required affordances with no response in ``turn`` (derivable; the loop's open set)."""
        turn = turn if turn is not None else self.current_turn()
        answered = {r.affordance for r in self._responses if turn is None or r.turn == turn}
        return [a.id for a in self._affordances.values() if a.required and a.id not in answered]

    def surface_state(self, turn: str | None = None) -> SurfaceState:
        """The re-read target, **recomputed** (IX6) — never trusted from the declared block alone (§9 SHOULD)."""
        turn = turn if turn is not None else self.current_turn()
        return SurfaceState(turn=turn, open=self.open_affordances(turn))

    def turn_complete(self, turn: str | None = None) -> bool:
        """A turn is complete when every ``required`` affordance in it has a response (spec §4 IX6)."""
        return not self.open_affordances(turn)

    def validate_interaction(self) -> list[str]:
        """I-1/I-2/I-3 failures ([] == conformant). Delegates to :func:`validate_interaction_block`."""
        return validate_interaction_block(self._doc, self.graph)


# --- loading (the read step) --------------------------------------------------------------------


def _read_doc(source: str | Path | dict[str, Any]) -> dict[str, Any]:
    if isinstance(source, dict):
        return source
    return json.loads(Path(source).read_text(encoding="utf-8"))


def _reserved(doc: dict[str, Any]) -> dict[str, Any]:
    block = doc.get("metadata", {}).get("frontmatter", {}).get("_reserved", {})
    return block if isinstance(block, dict) else {}


def _interaction_block(doc: dict[str, Any]) -> dict[str, Any]:
    block = _reserved(doc).get("interaction")
    return block if isinstance(block, dict) else {}


def load_interaction_surface(
    source: str | Path | dict[str, Any], *, resolver: Any | None = None, validate: bool = True
) -> InteractionSurface:
    """Load a ``.canvas`` as an :class:`InteractionSurface` — a leg-2 load (the *read* step, IX4) + the overlay.

    ``source`` is a path or an already-parsed canvas ``dict``. The leg-2 ``ContextGraph`` is produced by
    :func:`canvas_context.load_context_graph` (no rendering); the ``_reserved.interaction`` overlay is parsed on
    top. Never mutates ``source``.
    """
    doc = _read_doc(source)
    graph = load_context_graph(doc, resolver=resolver, validate=validate)
    return InteractionSurface(graph, doc, _interaction_block(doc))


# --- conformance (I-1 / I-2 / I-3) --------------------------------------------------------------


def _value_kind_errors(aid: str, entry: dict[str, Any], value: Any) -> list[str]:
    """IX5 value↔kind consistency: ``choice`` ∈ options · ``action`` ⇒ null · ``input``/``annotation`` non-null."""
    errors: list[str] = []
    kind = entry.get("kind")
    if kind == "action":
        if value is not None:
            errors.append(f"I-3: action affordance {aid!r} response must carry no value (got {value!r})")
    elif kind == "choice":
        options = entry.get("options") or []
        if value not in options:
            errors.append(f"I-3: choice affordance {aid!r} value {value!r} not in declared options {list(options)}")
    elif kind in ("input", "annotation"):
        if value is None:
            errors.append(f"I-3: {kind} affordance {aid!r} response value must not be null")
    # an unknown kind is already flagged by I-2; no value check possible
    return errors


def validate_interaction_block(doc: dict[str, Any], graph: ContextGraph | None = None) -> list[str]:
    """Realize ``I-1``/``I-2``/``I-3`` (spec_interface_surface §9.1) over a doc's ``_reserved.interaction``.

    A **thin delegate** to ``canvas_std.validate_interaction`` — Armature P2 (``adr_007``) wired the family into the
    harness, so the Standard's reference validator is now the single source of the logic (the consumer no longer
    duplicates it). Returns human-readable failures ([] == conformant); a canvas with no ``_reserved.interaction`` is
    vacuously conformant (a non-interactive surface, §8). The ``graph`` parameter is retained for API stability
    (``InteractionSurface.validate_interaction`` passes it) — resolution uses the doc path, which is equivalent for a
    well-formed surface (the graph is derived from the same doc).
    """
    return validate_interaction(_reserved(doc), doc)


# --- the act + re-read steps (a pure append-only fold) ------------------------------------------


def apply_response(
    surface_or_doc: InteractionSurface | dict[str, Any],
    affordance_id: str,
    value: Any,
    *,
    participant: dict[str, Any] | None = None,
    turn: str | None = None,
    at: str | None = None,
) -> dict[str, Any]:
    """Log a response and recompute the surface state — the *act* + *re-read* steps (IX5/IX6). Returns a NEW doc.

    A pure, **append-only** fold: it deep-copies the input, appends to ``_reserved.interaction.responses[]`` (it
    never mutates or deletes a logged response), and recomputes ``state.{turn,open}``. It advances the **view**
    only (spec §7.2) — no disk write, no rendering, no transport, no ``canvas_std`` mutation, and no reconciliation
    against the authoritative ``.lattice.yaml`` (that is ``spec_roundtrip_protocol_v2``'s job, §2). Raises
    ``ValueError`` on a non-conformant act: an undeclared affordance or a kind-inconsistent value (IX5).
    """
    src = surface_or_doc._doc if isinstance(surface_or_doc, InteractionSurface) else surface_or_doc
    new_doc = copy.deepcopy(src)
    reserved = new_doc.setdefault("metadata", {}).setdefault("frontmatter", {}).setdefault("_reserved", {})
    block = reserved.get("interaction")
    if not isinstance(block, dict):
        raise ValueError("apply_response: canvas carries no _reserved.interaction overlay")
    affs = block.get("affordances") or {}
    entry = affs.get(affordance_id)
    if not isinstance(entry, dict):
        raise ValueError(f"apply_response: undeclared affordance {affordance_id!r} (IX5)")
    kind_errors = _value_kind_errors(affordance_id, entry, value)
    if kind_errors:
        raise ValueError("; ".join(kind_errors))

    if turn is None:
        st = block.get("state") if isinstance(block.get("state"), dict) else {}
        turn = st.get("turn") or "t1"

    responses = block.setdefault("responses", [])
    if not isinstance(responses, list):
        raise ValueError("apply_response: responses is not a list (cannot append)")
    record: dict[str, Any] = {"affordance": affordance_id, "value": value, "turn": turn}
    if participant is not None:
        record["participant"] = participant
    if at is not None:
        record["at"] = at
    responses.append(record)  # append-only — an existing entry is never mutated or removed

    # recompute state (IX6): open = required affordances with no response in this turn
    answered = {r.get("affordance") for r in responses if isinstance(r, dict) and r.get("turn") == turn}
    open_ids = [
        aid for aid, e in affs.items() if isinstance(e, dict) and e.get("required") and aid not in answered
    ]
    block["state"] = {"turn": turn, "open": open_ids}
    return new_doc


# --- degradation / round-trip-to-baseline (I-D, §8.2) -------------------------------------------


def strip_interaction(doc: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with **only** ``_reserved.interaction`` removed (spec §8.2).

    The rest of ``_reserved`` is preserved — the result is a valid output canvas / leg-2 context graph carrying
    no affordances (a non-interactive surface). Contrast ``canvas_std.strip``, which removes the whole
    ``_reserved`` block (the I-D Core baseline).
    """
    bare = copy.deepcopy(doc)
    reserved = bare.get("metadata", {}).get("frontmatter", {}).get("_reserved")
    if isinstance(reserved, dict):
        reserved.pop("interaction", None)
    return bare


def is_round_trip_safe(doc: dict[str, Any], level: ConformanceLevel = ConformanceLevel.CORE) -> bool:
    """I-D — ``validate(strip(doc), level)`` passes with ``_reserved`` removed (round-trip-to-baseline, §9.1).

    Reuses the conformance-suite §5 D-1 strip (``canvas_std.strip`` — removes the whole ``_reserved`` block) and
    validates the result at ``level`` (Core by default — the baseline floor).
    """
    return core_validate(strip(doc), level) == []
