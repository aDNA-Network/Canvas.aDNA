"""Substrate-free domain model — a one-page letter. Imports NO ``canvas_std`` (``test_model_neutrality`` AST-guards it).

Only this layer is canvas-agnostic; ``consume.py`` is the only module that touches the substrate. A ``Letter`` is plain
data: letterhead (sender) lines, a date, a recipient block, a salutation, body paragraphs, a closing, and signature
lines, plus optional reference paths. ``load_letter`` reads a ``.yaml``/``.json`` spec into a ``Letter``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Letter:
    """A one-page business/cover letter as plain data (no canvas concepts).

    Block order (reading order): ``sender`` (letterhead) -> ``date`` -> ``recipient`` -> ``salutation`` ->
    ``body`` (one node per paragraph) -> ``closing`` -> ``signature``. Multi-line blocks (sender / recipient /
    signature) are tuples of lines, joined with newlines when rendered into a node.
    """

    title: str
    id: str
    version: str = "0.1.0"
    sender: tuple[str, ...] = ()      # letterhead lines (name / address / contact)
    date: str = ""
    recipient: tuple[str, ...] = ()   # recipient block lines (name / org / address)
    salutation: str = ""              # e.g. "Dear Dr. Mac,"
    body: tuple[str, ...] = ()        # paragraphs, in order
    closing: str = ""                 # e.g. "Sincerely,"
    signature: tuple[str, ...] = ()   # name / title lines
    refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.title:
            raise ValueError("Letter.title must be non-empty")
        if not self.id:
            raise ValueError("Letter.id must be non-empty")

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Letter:
        def _lines(value: Any) -> tuple[str, ...]:
            """A multi-line block may be a list of lines or a single newline-delimited string."""
            if value is None:
                return ()
            if isinstance(value, str):
                return tuple(value.splitlines())
            return tuple(str(x) for x in value)

        return cls(
            title=str(d["title"]),
            id=str(d["id"]),
            version=str(d.get("version", "0.1.0")),
            sender=_lines(d.get("sender")),
            date=str(d.get("date", "")),
            recipient=_lines(d.get("recipient")),
            salutation=str(d.get("salutation", "")),
            body=_lines(d.get("body")),
            closing=str(d.get("closing", "")),
            signature=_lines(d.get("signature")),
            refs=tuple(str(r) for r in d.get("refs", [])),
        )


def load_letter(path: str | Path) -> Letter:
    """Load a letter from ``.yaml``/``.yml`` (PyYAML) or ``.json``. Imports no ``canvas_std``."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        import yaml

        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"letter input {p} did not parse to a mapping")
    return Letter.from_dict(data)
