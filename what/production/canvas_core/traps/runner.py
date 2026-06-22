"""III trap pack runner — iterate registry, call implemented traps, aggregate findings.

Provides ``run_all_traps(canvas_data)`` which invokes every trap in the
TRAP_PACK_REGISTRY that has ``status: implemented`` or ``status: graduated``
and a non-null ``module`` field.

Migrated: N/A (new in M-5-01)
"""

from __future__ import annotations

import importlib
import inspect
import logging
from typing import Any

from . import TRAP_PACK_REGISTRY, TrapFinding

logger = logging.getLogger(__name__)


def run_all_traps(
    canvas_data: dict[str, Any],
    *,
    r11_node_ids: set[str] | None = None,
    **trap_kwargs: Any,
) -> list[TrapFinding]:
    """Run all implemented/graduated traps against canvas data.

    Args:
        canvas_data: Parsed canvas JSON (must have 'nodes' key).
        r11_node_ids: Optional set of node IDs under R11 gating.
            Passed through to each trap's ``check()`` for honor-by-construction
            of Critical Rule 7 (R11 substrate gate). Default ``None`` preserves
            backward compatibility for existing callers that don't pass kwarg.
        **trap_kwargs: Optional per-trap kwargs threaded through to each trap's
            ``check()`` after per-trap signature filtering. Traps that do not
            declare a given kwarg silently ignore it (no TypeError). Enables
            e.g. ``asset_root`` to reach CV-IMAGE-ASPECT-RATIO-01 without
            forcing every trap to accept the same surface area. Substrate-
            additive per M-V1-2-E-01 D3 fold-in (ADR-007 amendment-history).

    Returns:
        Aggregated list of TrapFinding from all invoked traps, sorted by
        severity (critical first).
    """
    findings: list[TrapFinding] = []
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}

    for trap_id, meta in TRAP_PACK_REGISTRY.items():
        status = meta.get("status", "scaffolded")
        module_path = meta.get("module")

        if status not in ("implemented", "graduated"):
            continue
        if not module_path:
            logger.debug("Trap %s is %s but has no module — skipping", trap_id, status)
            continue

        try:
            mod = importlib.import_module(module_path)
            check_fn = getattr(mod, "check", None)
            if check_fn is None:
                logger.warning("Trap %s module %s has no check() function", trap_id, module_path)
                continue

            accepted = inspect.signature(check_fn).parameters
            filtered = {k: v for k, v in trap_kwargs.items() if k in accepted}
            trap_findings = check_fn(canvas_data, r11_node_ids=r11_node_ids, **filtered)
            findings.extend(trap_findings)
            logger.debug("Trap %s produced %d findings", trap_id, len(trap_findings))

        except Exception as e:
            logger.error("Trap %s failed: %s", trap_id, e)
            findings.append(TrapFinding(
                trap_id=trap_id,
                condition="runner_error",
                node_ids=[],
                severity="low",
                message=f"Trap runner error: {e}",
            ))

    findings.sort(key=lambda f: severity_order.get(f.severity, 99))
    return findings
