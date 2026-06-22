"""Canvas visual III trap pack registry.

Canonical registry of all canvas-visual traps. Each trap is substrate-scoped
(applies to both deck and comic applications) unless explicitly tagged otherwise.

Scaffolded in M-0-03 (Phase 0 Foundation). Trap implementations are added
during Phase 1+ missions. M-1-07 adds CV-TEXT-BOUNDS-01 as the first
implemented trap with a check() callable.

Registry shape:
    TRAP_PACK_REGISTRY[trap_id] = {
        "scope": "substrate" | "deck-specific" | "comic-specific",
        "status": "scaffolded" | "implemented" | "graduated" | "retired",
        "graduated": bool,
        "cycles_fired": int,
        "cycles_accepted": int,
        "module": str | None,  # e.g. "canvas_core.traps.cv_text_bounds_01"
        "severity_default": "low" | "medium" | "high" | "critical",
        "description": str,
    }
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TrapFinding:
    """Standard output record for a III trap check.

    Every trap's ``check()`` function returns a list of TrapFinding instances.
    Consumed by the III aggregate scoring pipeline and by M-1-08
    agent-autonomous critique.
    """

    trap_id: str        # e.g. "CV-TEXT-BOUNDS-01"
    condition: str      # trap-specific condition key
    node_ids: list[str]  # affected canvas node IDs
    severity: str       # "low" | "medium" | "high" | "critical"
    message: str        # human-readable description


TRAP_PACK_REGISTRY = {
    "CV-COHERENCE-01": {
        "scope": "substrate",
        "status": "implemented",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": "canvas_core.traps.cv_coherence_01",
        "severity_default": "medium",
        "description": "Visual consistency drift between slides/panels",
    },
    "CV-AUDIENCE-01": {
        "scope": "deck-specific",
        "status": "implemented",
        "graduated": False,
        "cycles_fired": 2,
        "cycles_accepted": 0,
        "module": "canvas_core.traps.cv_audience_01",
        "severity_default": "high",
        "description": "Audience-presentation fit ambiguity (live vs async)",
    },
    "CV-CONFIDENCE-01": {
        "scope": "substrate",
        "status": "scaffolded",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": None,
        "severity_default": "medium",
        "description": "Content confidence inflation (projective claims as fact)",
    },
    "CV-HIERARCHY-01": {
        "scope": "substrate",
        "status": "implemented",
        "graduated": False,
        "cycles_fired": 1,
        "cycles_accepted": 0,
        "module": "canvas_core.traps.cv_hierarchy_01",
        "severity_default": "medium",
        "description": "Visual hierarchy inconsistency (heading weight collapse)",
    },
    "CV-TEMPLATE-01": {
        "scope": "substrate",
        "status": "scaffolded",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": None,
        "severity_default": "medium",
        "description": "Template voice / generic filler (boilerplate copy)",
    },
    "CV-CONTRAST-01": {
        "scope": "substrate",
        "status": "scaffolded",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": None,
        "severity_default": "high",
        "description": "WCAG contrast failures (accessibility/readability)",
    },
    "CV-PENDING-01": {
        "scope": "substrate",
        "status": "graduated",
        "graduated": True,
        "cycles_fired": 3,
        "cycles_accepted": 3,
        "module": "canvas_core.traps.cv_pending_01",
        "severity_default": "critical",
        "description": "Unresolved placeholders shipped as done (PendingImage/PendingPanel)",
    },
    "CV-COMIC-STYLE-01": {
        "scope": "comic-specific",
        "status": "scaffolded",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": None,
        "severity_default": "high",
        "description": "Comic style lock drift (character/palette/rendering inconsistency)",
    },
    "CV-INSIDER-CONTEXT-01": {
        "scope": "substrate",
        "status": "scaffolded",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": None,
        "severity_default": "medium",
        "description": "Insider-context contamination (reviewers filling gaps the deliverable doesn't carry)",
    },
    "CV-DIMENSION-VISIBILITY-01": {
        "scope": "substrate",
        "status": "implemented",
        "graduated": False,
        "cycles_fired": 1,
        "cycles_accepted": 0,
        "module": "canvas_core.traps.cv_dimension_visibility_01",
        "severity_default": "medium",
        "description": "Slide dimensions hidden from reviewers (aspect ratio not visible)",
    },
    "CV-TEXT-BOUNDS-01": {
        "scope": "substrate",
        "status": "implemented",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": "canvas_core.traps.cv_text_bounds_01",
        "severity_default": "medium",
        "description": "Text node overflow, overlap, or group-boundary escape (ADR 004 D2)",
    },
    # CV-GENERAL-01 registered 2026-05-03 per F-25 of M-CAMPAIGN-REFRESH-02.
    # Catch-all used by critique prompt template (cv_trap_findings.txt:18) when a
    # finding doesn't match an enumerated trap ID. Registered as scaffolded with
    # severity_default: medium so downstream severity-defaulting works correctly.
    # Rejected alternative: remove from prompt template + ask model to use
    # closest-match. Rejected because catch-all is a real schema need (model returns
    # findings outside the 11 enumerated traps); registering preserves backward compat.
    "CV-GENERAL-01": {
        "scope": "substrate",
        "status": "scaffolded",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": None,
        "severity_default": "medium",
        "description": "Catch-all for critique findings that don't match an enumerated trap ID (used by cv_trap_findings.txt template)",
    },
    # CV-NODE-DENSITY-01 + CV-IMAGE-ASPECT-RATIO-01 + CV-GROUP-PADDING-01 added
    # 2026-05-25 by M-V1-2-G-02 (Python impl follow-up to M-V1-2-G-01 trap cards).
    # All three close adjacent failure modes to operator complaint 2026-05-25
    # ("too much text/images for the size of the panel they were placed on"):
    # CV-NODE-DENSITY-01 is the direct hit (aggregate fill-ratio); the other two
    # close adjacent failure modes (image distortion/under-fill + edge-bleed/
    # no-breathing-room). Per coord_2026_04_16_forge_split.md re-merge rationale,
    # all three traps are canvas-substrate-resident — consumable by any future
    # canvas application (topology diagrams, sequence diagrams, comparison
    # matrices) without modification.
    "CV-NODE-DENSITY-01": {
        "scope": "substrate",
        "status": "implemented",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": "canvas_core.traps.cv_node_density_01",
        "severity_default": "medium",
        "description": "Aggregate content-to-container fill ratio excess (closes operator complaint 2026-05-25 re too-much-content-for-panel-size)",
    },
    "CV-IMAGE-ASPECT-RATIO-01": {
        "scope": "substrate",
        "status": "implemented",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": "canvas_core.traps.cv_image_aspect_ratio_01",
        "severity_default": "medium",
        "description": "Image aspect drift or hero-slot under-fill (source dims via PIL fallback; consumer-agnostic per M-V1-2-G-02 D2)",
    },
    "CV-GROUP-PADDING-01": {
        "scope": "substrate",
        "status": "implemented",
        "graduated": False,
        "cycles_fired": 0,
        "cycles_accepted": 0,
        "module": "canvas_core.traps.cv_group_padding_01",
        "severity_default": "medium",
        "description": "Content bleeds to container frame edge (aggregate fill > 0.90 OR per-node padding-min violation per design-token resolution)",
    },
}
