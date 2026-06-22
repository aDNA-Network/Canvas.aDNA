"""Vault path discovery — symlink-safe resolution."""

from __future__ import annotations

from pathlib import Path


def find_vault_root() -> Path:
    """Discover vault root — works with both symlink and direct repo layouts."""
    # Try unresolved parent chain (works when imported through symlink)
    candidate = Path(__file__).parents[2].parent
    if (candidate / "what").exists():
        return candidate
    # Standard vault locations per skill_machine_setup
    for loc in [
        Path.home() / "Projects" / "LATTICE-PROTOCOL",
        Path.home() / "LATTICE-PROTOCOL",
    ]:
        if (loc / "what").exists():
            return loc
    return candidate


def find_repo_root() -> Path:
    """Return the lattice-protocol repo root."""
    return Path(__file__).resolve().parents[2]


VAULT_ROOT = find_vault_root()
REPO_ROOT = find_repo_root()
