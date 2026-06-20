"""document_generator — a reference long-form document consumer of the aDNA Canvas Standard v2.0.0.

The **LF-successor** (Operation Keystone E4.1): the in-vault successor to the wound-down LiteratureForge, built on the
``what/production/`` shelf. It *consumes* the Standard's reference tooling (``canvas_std``, the installed
``adna-canvas-std``) and never modifies it (ADR-005 / ADR-004 two-shelf firewall). ``build_document`` is the public
entry point. Sibling to the E4.3 ``brief_consumer`` (single-page) and the E4.4 ``deck_generator`` (deck); this one is
**multi-page long-form** (pages = group nodes; profile ``long_document``).

The genre/writing pipeline (trap-packs, reviewer voices, reward rubrics) stays producer-side and is *absent* here —
it lands as producer-side config in E4.2 (the LF visual/format-contract migration), never in the Standard.
"""

from __future__ import annotations

from document_generator.consume import build_document
from document_generator.model import Block, Document, Page, Section, Source, load_document

__version__ = "0.1.0"
STANDARD_VERSION = "2.0.0"

__all__ = [
    "build_document",
    "load_document",
    "Document",
    "Page",
    "Section",
    "Block",
    "Source",
    "__version__",
    "STANDARD_VERSION",
]
