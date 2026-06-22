"""Reference resolution — the resolver interface (spec_canvas_context_loading §5).

The loader defines and calls an abstract ``Resolver``; it does **not** implement transport itself. In-vault
``wikilink`` resolution SHOULD be supported by a default path resolver (vault-relative lookup). Cross-vault
``federation_ref`` resolution returns a *descriptor* — the loader MUST NOT cross the vault boundary to fetch content
(that is the federation layer's role, gated by ADR-006). A resolved handle MAY itself be loaded by recursively
applying the protocol (cycle-safety is the caller's + loader's responsibility, §5.2).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from canvas_context.model import UNRESOLVED, Ref

_WIKILINK = re.compile(r"^\[\[(.+?)\]\]$")


@dataclass(frozen=True)
class LocalHandle:
    """A resolved in-vault handle — a vault-relative path to a loadable canvas/doc (spec §5)."""

    path: str
    target: str


@dataclass(frozen=True)
class FederationDescriptor:
    """A cross-vault reference descriptor — NOT transported content (spec §5; transport is the federation layer's)."""

    target: str
    instance: str | None = None
    lattice: str | None = None
    node: str | None = None


@runtime_checkable
class Resolver(Protocol):
    """The abstract resolver contract: ``resolve(ref) -> handle | UNRESOLVED`` (spec §5.1)."""

    def resolve(self, ref: Ref) -> Any: ...


class DefaultPathResolver:
    """In-vault ``wikilink`` resolution via vault-relative lookup (spec §5.2, SHOULD).

    Resolves ``[[name]]`` to a :class:`LocalHandle` pointing at the first matching ``name.canvas`` / ``name.md`` under
    ``vault_root``. ``federation_ref`` is parsed into a :class:`FederationDescriptor` but **never fetched** (§5.2 /
    ADR-006). Scope ``vault_root`` narrowly — the lazy index walks it once.
    """

    def __init__(self, vault_root: str | Path, *, extensions: tuple[str, ...] = (".canvas", ".md")) -> None:
        self.vault_root = Path(vault_root)
        self.extensions = extensions
        self._index: dict[str, str] | None = None

    def resolve(self, ref: Ref) -> Any:
        if ref.form == "federation_ref":
            return _parse_federation(ref.target)
        if ref.form != "wikilink":
            return UNRESOLVED
        name = self._wikilink_name(ref.target)
        if not name:
            return UNRESOLVED
        rel = self._lookup(name)
        return LocalHandle(path=rel, target=ref.target) if rel else UNRESOLVED

    @staticmethod
    def _wikilink_name(target: str) -> str | None:
        m = _WIKILINK.match(target.strip())
        inner = (m.group(1) if m else target.strip())
        # drop an alias ([[name|alias]]) and a heading/anchor ([[name#section]]); a path-style link → its stem
        inner = inner.split("|", 1)[0].split("#", 1)[0].strip()
        return Path(inner).name or None

    def _lookup(self, name: str) -> str | None:
        return self._build_index().get(name)

    def _build_index(self) -> dict[str, str]:
        if self._index is None:
            idx: dict[str, str] = {}
            if self.vault_root.is_dir():
                for ext in self.extensions:
                    for p in sorted(self.vault_root.rglob(f"*{ext}")):
                        idx.setdefault(p.stem, str(p.relative_to(self.vault_root)))
            self._index = idx
        return self._index


def _parse_federation(target: str) -> FederationDescriptor:
    """Parse a ``lattice://instance/lattice[/node]`` reference into a descriptor (no transport)."""
    rest = target[len("lattice://"):] if target.startswith("lattice://") else target
    parts = [p for p in rest.split("/") if p]
    instance = parts[0] if len(parts) > 0 else None
    lattice = parts[1] if len(parts) > 1 else None
    node = parts[2] if len(parts) > 2 else None
    return FederationDescriptor(target=target, instance=instance, lattice=lattice, node=node)
