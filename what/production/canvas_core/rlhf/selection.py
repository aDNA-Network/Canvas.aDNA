"""SelectionRecord — canonical schema for variant-selection decisions.

Per skill_canvas_variant_selection.md § 5:
- selection_id format: sel_YYYYMMDD_HHMMSS_<4-hex>
- Schema-violation is hard-fail, not silent-skip
- Corpus integrity is load-bearing for post-v1.0 training

Created in M-5-07.

Path schema (F-36 amendment 2026-05-03 per M-CAMPAIGN-REFRESH-02):
    Variant ``image_path`` MUST be vault-relative (e.g., ``what/artifacts/...``)
    rather than absolute (``/Users/.../...``). Absolute paths are operator-
    specific and break corpus portability across machines + operators. Per
    ADR-003 D4, the corpus is load-bearing for post-v1.0 style-transfer
    training; portability is a precondition. ``validate_selection_record``
    treats absolute ``image_path`` values as schema violations.
"""

from __future__ import annotations

import json
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class VariantInfo:
    """Metadata for one image variant."""

    image_path: str
    model: str = "imagen-4-ultra"
    cost_usd: float = 0.06
    seed: int | None = None


@dataclass
class SelectionRecord:
    """Canonical record of a human variant-selection decision.

    Schema per skill_canvas_variant_selection.md § 5.
    Schema-violation is hard-fail — a malformed record is worse than no record.
    """

    prompt: str
    register: str
    variants: list[VariantInfo]
    pick_index: int
    pick_reason: str
    approver_id: str
    selection_id: str = ""
    timestamp: str = ""
    budget_class: str = "standard"
    register_compliance_score: float | None = None
    vr_scores: dict[str, float] | None = None

    def __post_init__(self) -> None:
        if not self.selection_id:
            self.selection_id = _generate_selection_id()
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict."""
        return {
            "selection_id": self.selection_id,
            "timestamp": self.timestamp,
            "prompt": self.prompt,
            "register": self.register,
            "budget_class": self.budget_class,
            "variants": [
                {
                    "image_path": v.image_path,
                    "model": v.model,
                    "cost_usd": v.cost_usd,
                    "seed": v.seed,
                }
                for v in self.variants
            ],
            "pick_index": self.pick_index,
            "pick_reason": self.pick_reason,
            "approver_id": self.approver_id,
            "register_compliance_score": self.register_compliance_score,
            "vr_scores": self.vr_scores,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SelectionRecord:
        """Deserialize from a JSON-compatible dict produced by ``to_dict``.

        Inverse of ``to_dict``; preserves ``selection_id`` + ``timestamp`` from
        the source (no regeneration). Used by ``canvas_core.rlhf.iii_bridge``
        to round-trip on-disk ``sel_*.json`` records into typed objects without
        re-emitting fresh ids. Missing-key handling defers to the dataclass —
        only fields with defaults survive omissions; required fields raise
        ``TypeError`` from the dataclass constructor.
        """
        variants = [
            VariantInfo(
                image_path=v["image_path"],
                model=v.get("model", "imagen-4-ultra"),
                cost_usd=v.get("cost_usd", 0.06),
                seed=v.get("seed"),
            )
            for v in data["variants"]
        ]
        return cls(
            prompt=data["prompt"],
            register=data["register"],
            variants=variants,
            pick_index=data["pick_index"],
            pick_reason=data["pick_reason"],
            approver_id=data["approver_id"],
            selection_id=data.get("selection_id", ""),
            timestamp=data.get("timestamp", ""),
            budget_class=data.get("budget_class", "standard"),
            register_compliance_score=data.get("register_compliance_score"),
            vr_scores=data.get("vr_scores"),
        )


def _is_absolute_path(path: str) -> bool:
    """Detect whether a path string is absolute (operator-specific).

    Absolute on POSIX: starts with ``/`` or ``~``. Used by ``validate_selection_record``
    to enforce vault-relative path policy per F-36 of M-CAMPAIGN-REFRESH-02.
    """
    if not path:
        return False
    return path.startswith("/") or path.startswith("~")


def validate_selection_record(record: SelectionRecord) -> list[str]:
    """Validate a SelectionRecord against the canonical schema.

    Returns a list of validation errors. Empty list = valid.
    Raises nothing — caller decides whether to hard-fail.

    Path policy (F-36 amendment 2026-05-03): every variant's ``image_path``
    MUST be vault-relative. Absolute paths (``/...``, ``~/...``) surface as
    validation errors so the corpus stays portable per ADR-003 D4.
    """
    errors: list[str] = []

    if not record.selection_id.startswith("sel_"):
        errors.append(f"selection_id must start with 'sel_', got '{record.selection_id}'")

    if not record.timestamp:
        errors.append("timestamp is required")

    if not record.prompt:
        errors.append("prompt is required")

    if not record.register:
        errors.append("register is required")

    if not record.variants:
        errors.append("variants list is empty")

    if record.pick_index < 0 or record.pick_index >= len(record.variants):
        errors.append(
            f"pick_index {record.pick_index} out of range "
            f"(0..{len(record.variants) - 1})"
        )

    if not record.pick_reason:
        errors.append("pick_reason is required")

    if not record.approver_id:
        errors.append("approver_id is required")

    # F-36: vault-relative image_path enforcement.
    for idx, variant in enumerate(record.variants):
        if _is_absolute_path(variant.image_path):
            errors.append(
                f"variants[{idx}].image_path must be vault-relative "
                f"(e.g., 'what/artifacts/...'); got absolute path "
                f"'{variant.image_path}' (per F-36 / ADR-003 D4 corpus portability)"
            )

    return errors


def _generate_selection_id() -> str:
    """Generate a globally unique selection ID.

    Format: sel_YYYYMMDD_HHMMSS_<4-hex>
    """
    now = datetime.now(timezone.utc)
    hex_suffix = secrets.token_hex(2)
    return f"sel_{now.strftime('%Y%m%d_%H%M%S')}_{hex_suffix}"


def write_selection_record(record: SelectionRecord, output_dir: Path) -> Path:
    """Validate (hard-fail) then write a selection record JSON file.

    Returns the path written. Calls ``validate_selection_record`` first; if
    any errors surface, raises ``ValueError`` with the full error list (per
    the schema-violation-is-hard-fail doctrine in the module docstring; F-36
    vault-relative-path enforcement applies).

    The output file is named ``<selection_id>.json`` and lives in
    ``output_dir``; the directory is created on first run if missing.
    """
    errors = validate_selection_record(record)
    if errors:
        raise ValueError(
            f"SelectionRecord schema violations ({len(errors)}): " + "; ".join(errors)
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"{record.selection_id}.json"
    target.write_text(json.dumps(record.to_dict(), indent=2) + "\n")
    return target
