"""Input model — a structured long-form document spec (ordered pages of ordered sections).

A substrate-free producer-side domain model: a human/agent authors a document (title + ordered pages, each an ordered
list of sections; each section a heading + body + rich blocks + citations), and the consumer (``consume.py``) maps it
onto the aDNA Canvas Standard (each page -> a group node; sections + blocks -> interior nodes). No ``canvas_std``
import here.

The block set is a lean KEEP subset — the long-form elements the Standard's component model already covers
(figure/table/code/quote/list). Genre-specific structure (per-genre section templates, trap-packs, voices) is
producer-side config for E4.2, not modeled here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Rich block kinds beyond a section's heading + body prose.
BLOCK_TYPES: frozenset[str] = frozenset({"figure", "table", "code", "quote", "list"})


@dataclass(frozen=True)
class Source:
    """A citation: a human label + a URL (-> a ``link`` node, ``citation`` component)."""

    label: str = ""
    url: str = ""


@dataclass(frozen=True)
class Block:
    """A rich block within a section. ``type`` selects which fields are meaningful."""

    type: str
    image: str = ""          # figure: a vault path (-> file node) or http url (-> link node)
    caption: str = ""        # figure caption
    table: Any = None        # table: a markdown string OR {headers:[...], rows:[[...]]}
    code: str = ""           # code block source
    lang: str = ""           # code block language hint (e.g. "python")
    text: str = ""           # quote text
    attribution: str = ""    # quote attribution
    items: list[str] = field(default_factory=list)  # list items

    def __post_init__(self) -> None:
        if self.type not in BLOCK_TYPES:
            raise ValueError(f"unknown block type {self.type!r}; expected one of {sorted(BLOCK_TYPES)}")


@dataclass(frozen=True)
class Section:
    """An order-locked section: a heading, optional body prose, ordered rich blocks, and citations."""

    heading: str
    body: str = ""
    blocks: list[Block] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)


@dataclass(frozen=True)
class Page:
    """A printed page (a paginated panel) holding one or more sections."""

    sections: list[Section]


@dataclass(frozen=True)
class Document:
    title: str
    id: str
    version: str
    pages: list[Page]
    refs: list[str] = field(default_factory=list)

    def word_count(self) -> int:
        """Approximate prose word count (LF ``length_window``) — body + list + quote + caption + heading text."""
        n = 0
        for page in self.pages:
            for sec in page.sections:
                n += len(sec.heading.split()) + len(sec.body.split())
                for blk in sec.blocks:
                    n += len(blk.text.split()) + len(blk.caption.split())
                    n += sum(len(it.split()) for it in blk.items)
        return n

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Document:
        pages: list[Page] = []
        for pg in d.get("pages", []):
            sections = [
                Section(
                    heading=str(s["heading"]),
                    body=str(s.get("body", "")).strip(),
                    blocks=[_block_from_dict(b) for b in s.get("blocks", [])],
                    sources=[
                        Source(label=str(c.get("label", "")), url=str(c.get("url", "")))
                        for c in s.get("sources", [])
                    ],
                )
                for s in pg.get("sections", [])
            ]
            if not sections:
                raise ValueError("page has no sections")
            pages.append(Page(sections=sections))
        if not pages:
            raise ValueError("document has no pages")
        return cls(
            title=str(d["title"]),
            id=str(d["id"]),
            version=str(d.get("version", "0.1.0")),
            refs=[str(r) for r in d.get("refs", [])],
            pages=pages,
        )


def _block_from_dict(b: dict[str, Any]) -> Block:
    return Block(
        type=str(b["type"]),
        image=str(b.get("image", "")),
        caption=str(b.get("caption", "")),
        table=b.get("table"),
        code=str(b.get("code", "")),
        lang=str(b.get("lang", "")),
        text=str(b.get("text", "")).strip(),
        attribution=str(b.get("attribution", "")),
        items=[str(x) for x in b.get("items", [])],
    )


def load_document(path: str | Path) -> Document:
    """Load a document from ``.yaml``/``.yml`` (PyYAML) or ``.json``."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        import yaml

        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"document input {p} did not parse to a mapping")
    return Document.from_dict(data)
