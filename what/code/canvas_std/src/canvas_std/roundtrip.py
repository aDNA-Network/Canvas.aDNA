"""Round-trip Protocol v2 — authoritative-source <-> view.

E0.1: signatures frozen; bodies raise NotImplementedError (E1.2 / E1.3).
``to_canvas``/``from_canvas`` are the public names (a P1 finding: the legacy CanvasBuilder used
``build``/``read_back`` — aliased here so the API matches the conformance vocabulary).
Spec: spec_roundtrip_protocol_v2.
"""

from __future__ import annotations

from typing import Any


def to_canvas(source: dict[str, Any]) -> dict[str, Any]:
    """Forward (authoritative source -> .canvas view), deterministic. (legacy: ``build``) — E1.2."""
    raise NotImplementedError("to_canvas(): implemented at Keystone E1.2")


def from_canvas(canvas: dict[str, Any]) -> dict[str, Any]:
    """Reverse (.canvas view -> authoritative-source DRAFT), advisory only. (legacy: ``read_back``) — E1.2/E1.3."""
    raise NotImplementedError("from_canvas(): implemented at Keystone E1.2/E1.3")


def compute_sync_hash(source: dict[str, Any]) -> str:
    """16-hex SHA-256 over the topology (sorted node ids + sorted from->to edges). Spec §3 — E1.2."""
    raise NotImplementedError("compute_sync_hash(): implemented at Keystone E1.2")


def diff(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """Structured topology/position diff for the advisory reverse path. Spec §5 — E1.3."""
    raise NotImplementedError("diff(): implemented at Keystone E1.3")


def merge(source: dict[str, Any], canvas: dict[str, Any], *, strategy: str = "yaml_wins") -> dict[str, Any]:
    """Three-way merge (source semantics win; canvas positions win; conflicts flagged). Spec §5 — E1.3."""
    raise NotImplementedError("merge(): implemented at Keystone E1.3")
