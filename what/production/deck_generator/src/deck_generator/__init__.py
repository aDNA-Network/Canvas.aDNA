"""deck_generator — a reference deck consumer of the aDNA Canvas Standard v2.0.0 (Operation Keystone E4.4).

Producer code on the ``what/production/`` shelf: it *consumes* the Standard's reference tooling (``canvas_std``, the
installed ``adna-canvas-std``) and never modifies it. ``build_deck`` is the public entry point. Sibling to the E4.3
``brief_consumer`` (the single-page precedent); this one is multi-slide (slides = group nodes).
"""

from __future__ import annotations

from deck_generator.consume import build_deck
from deck_generator.model import DeckInput, Slide, load_deck

__version__ = "0.1.0"
STANDARD_VERSION = "2.0.0"

__all__ = ["build_deck", "load_deck", "DeckInput", "Slide", "__version__", "STANDARD_VERSION"]
