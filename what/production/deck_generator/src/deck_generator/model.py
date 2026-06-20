"""Input model — a structured deck spec (ordered slides).

A substrate-free producer-side domain model: a human/agent authors a deck (title + ordered slides of a handful of
types), and the consumer (``consume.py``) maps it onto the aDNA Canvas Standard (each slide → a group node). No
``canvas_std`` import here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Lean KEEP subset of CanvasForge's 16 slide types (the rest are P5/engine concerns).
SLIDE_TYPES: frozenset[str] = frozenset({"title", "content", "section", "image", "table", "quote"})


@dataclass(frozen=True)
class Slide:
    type: str
    title: str = ""
    subtitle: str = ""        # title slide
    body: str = ""            # content / image caption fallback
    bullets: list[str] = field(default_factory=list)  # content
    image: str = ""           # image slide: a vault path (-> file node) or http url (-> link node)
    caption: str = ""         # image slide caption
    table: Any = None         # table slide: a markdown string OR {headers:[...], rows:[[...]]}
    attribution: str = ""     # quote slide

    def __post_init__(self) -> None:
        if self.type not in SLIDE_TYPES:
            raise ValueError(f"unknown slide type {self.type!r}; expected one of {sorted(SLIDE_TYPES)}")


@dataclass(frozen=True)
class DeckInput:
    title: str
    id: str
    version: str
    slides: list[Slide]
    refs: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DeckInput:
        slides = [
            Slide(
                type=str(s["type"]),
                title=str(s.get("title", "")),
                subtitle=str(s.get("subtitle", "")),
                body=str(s.get("body", "")).strip(),
                bullets=[str(b) for b in s.get("bullets", [])],
                image=str(s.get("image", "")),
                caption=str(s.get("caption", "")),
                table=s.get("table"),
                attribution=str(s.get("attribution", "")),
            )
            for s in d.get("slides", [])
        ]
        if not slides:
            raise ValueError("deck has no slides")
        return cls(
            title=str(d["title"]),
            id=str(d["id"]),
            version=str(d.get("version", "0.1.0")),
            refs=[str(r) for r in d.get("refs", [])],
            slides=slides,
        )


def load_deck(path: str | Path) -> DeckInput:
    """Load a deck from ``.yaml``/``.yml`` (PyYAML) or ``.json``."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        import yaml

        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"deck input {p} did not parse to a mapping")
    return DeckInput.from_dict(data)
