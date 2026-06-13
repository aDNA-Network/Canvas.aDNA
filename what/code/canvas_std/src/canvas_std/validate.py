"""Validation + the degradation strip.

E0.1: signatures frozen; bodies raise NotImplementedError (E1.1 / E1.5).
Spec: spec_adna_canvas_standard §10, spec_conformance_suite §2–§5.
"""

from __future__ import annotations

from enum import Enum
from typing import Any


class ConformanceLevel(str, Enum):
    CORE = "core"
    EXTENDED = "extended"
    ADNA_NATIVE = "adna_native"


class ValidationError(Exception):
    """Raised (or collected) when a document fails its declared conformance level."""


def validate(doc: dict[str, Any], level: ConformanceLevel = ConformanceLevel.CORE) -> list[str]:
    """Return a list of human-readable errors ([] == valid at ``level``).

    Checks per spec_conformance_suite: C-* (Core), E-* (Extended), A-* (aDNA-Native).
    Implemented at E1.1 (Core/Extended) + E1.4 (the ``_reserved`` A-* checks).
    """
    raise NotImplementedError("validate(): implemented at Keystone E1.1 (+ E1.4 for _reserved)")


def strip(doc: dict[str, Any]) -> dict[str, Any]:
    """Return ``doc`` with ``metadata.frontmatter._reserved`` removed.

    The C4 degradation operation: ``validate(strip(doc), CORE)`` must pass for any aDNA-Native
    document (spec_adna_canvas_standard §11, spec_conformance_suite D-1..D-3). Implemented at E1.5.
    """
    raise NotImplementedError("strip(): implemented at Keystone E1.5")
