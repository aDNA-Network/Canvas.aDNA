"""brief_consumer — a reference net-new consumer of the aDNA Canvas Standard v2.0.0 (Operation Keystone E4.3).

Producer code on the ``what/production/`` shelf: it *consumes* the Standard's reference tooling (``canvas_std``,
the installed ``adna-canvas-std``) and never modifies it. ``build_brief`` is the public entry point.
"""

from __future__ import annotations

from brief_consumer.consume import build_brief
from brief_consumer.model import BriefInput, Section, Source, load_brief

__version__ = "0.1.0"
STANDARD_VERSION = "2.0.0"  # the aDNA Canvas Standard version this consumer targets

__all__ = ["build_brief", "load_brief", "BriefInput", "Section", "Source", "__version__", "STANDARD_VERSION"]
