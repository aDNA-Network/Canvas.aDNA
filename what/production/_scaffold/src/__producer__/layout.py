"""Producer-owned integer geometry (``canvas_std`` is geometry-agnostic).

TODO(clone): compute node ``x/y/width/height`` boxes for your domain. Keep it **deterministic** (no randomness, no
wall-clock) so the round-trip sync hash is stable across rebuilds. Single-surface producers can often inline trivial
geometry in ``consume.py`` and delete this module; multi-page producers benefit from a dedicated layout pass.
"""

from __future__ import annotations
