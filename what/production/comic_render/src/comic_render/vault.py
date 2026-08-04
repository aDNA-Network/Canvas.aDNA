"""Vault-root resolution for file-node paths (the traps/cli ``.obsidian`` convention).

Obsidian resolves ``file`` nodes from the VAULT root — write-back stores paths relative to it and
validate/compose resolve them against it. Outside a vault (test tmp dirs), the canvas's own
directory is the root: paths stay relative and portable either way.
"""

from __future__ import annotations

from pathlib import Path


def resolve_vault_root(canvas_path: str | Path, explicit: str | Path | None = None) -> Path:
    """Explicit override > nearest ancestor holding ``.obsidian`` > the canvas's directory."""
    if explicit is not None:
        return Path(explicit).resolve()
    start = Path(canvas_path).resolve().parent
    for candidate in (start, *start.parents):
        if (candidate / ".obsidian").is_dir():
            return candidate
    return start
