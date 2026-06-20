"""Input model — a structured one-page technical brief.

A substrate-free producer-side domain model: a human/agent authors a brief (title + ordered sections, each with a
heading, body, and optional external sources), and the consumer (``consume.py``) maps it onto the aDNA Canvas
Standard. No ``canvas_std`` import here — the model knows nothing about canvases.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Source:
    """An external reference (degrades to a JSON-Canvas ``link`` node)."""

    label: str
    url: str


@dataclass(frozen=True)
class Section:
    heading: str
    body: str
    sources: list[Source] = field(default_factory=list)


@dataclass(frozen=True)
class BriefInput:
    """A one-page brief. ``id``/``version``/``refs`` populate the canvas ``_reserved.context_object``."""

    title: str
    id: str
    version: str
    sections: list[Section]
    refs: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BriefInput:
        sections = [
            Section(
                heading=str(s["heading"]),
                body=str(s.get("body", "")).strip(),
                sources=[
                    Source(label=str(src["label"]), url=str(src["url"]))
                    for src in s.get("sources", [])
                ],
            )
            for s in d.get("sections", [])
        ]
        return cls(
            title=str(d["title"]),
            id=str(d["id"]),
            version=str(d.get("version", "0.1.0")),
            refs=[str(r) for r in d.get("refs", [])],
            sections=sections,
        )


def load_brief(path: str | Path) -> BriefInput:
    """Load a brief from ``.yaml``/``.yml`` (PyYAML) or ``.json``."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        import yaml  # producer-side dep; canvas_std stays stdlib-only

        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"brief input {p} did not parse to a mapping")
    return BriefInput.from_dict(data)
