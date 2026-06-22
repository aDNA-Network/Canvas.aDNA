"""III RLHF bridge — map CanvasForge selection records to ADR-005 signals.

Closes the HITL feedback loop for image generation: each operator
variant-pick captured as a ``sel_*.json`` becomes an ADR-005 §2-compliant
signal in the CanvasForge-local III learning store at
``iii/what/context/canvasforge_iii_learning_store.jsonl``. Single-vault
start per ``campaign_canvasforge_v1_2_planning`` Q3=b — writes to the
local store only; cross-vault graduation defers to ADR-003 §3 with
standard frequency ≥ 3 + acceptance ≥ 80% criteria.

**Scope (Pillar E S1+S2)**:
- Input: Schema-A ``sel_*.json`` records (the 11-field shape produced by
  ``canvas_core.rlhf.selection.SelectionRecord.to_dict``). Schemas B (the
  minimal 6-field shape from ``image_generation.py``
  ``write_selection_record``) and C (the visual-style RLHF runner's
  pre-shaped ADR-005 form) are deferred — see ADR-006 § 5.
- Output: append-only writes to the local learning store. Idempotent on
  ``selection_id`` — re-running on the same corpus produces no new lines.
- Signal type: ``accept`` only today (the operator picked something).
  ``reject`` / ``defer`` / ``accept_with_modification`` deferred per
  ``mission_shape: iterate_per_generation_type``.

**Schema target** (per III.aDNA ADR-005 §2 + §3, ADR-003 §4):
- ADR-003 §4 base correction fields: ``id``, ``trap``, ``pattern``,
  ``description``, ``example``, ``source_review``, ``source_finding``,
  ``frequency``, ``accepted``, ``created``.
- ADR-005 §2 required-min RLHF fields: ``rlhf_signal_type``,
  ``rlhf_session_id``, ``rlhf_captured_at`` (ISO 8601 ``Z``-suffixed UTC).
- ADR-005 §2 optional-open: ``rlhf_reviewer_persona`` when
  ``approver_id`` is present.
- ADR-005 §3 consumer-namespace: ``rlhf_consumer_namespace.canvasforge.
  image_generation.*`` nested-object projection of the full sel record.
  Nested-object shape matches the M-V1-2-G-01 F3-migration precedent
  already in the local store (4 entries; canonical post-G-02 close).

**Re-merge rationale** (CR7+SO7):
``lattice-labs/who/coordination/coord_2026_04_16_forge_split.md``.

Created in M-V1-2-E-01 S1.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .selection import SelectionRecord, validate_selection_record

# CanvasForge.aDNA root: this file is at .../what/code/canvas_core/rlhf/iii_bridge.py
# so 5 parents up reaches the vault root.
_VAULT_ROOT = Path(__file__).resolve().parents[4]

DEFAULT_LEARNING_STORE = (
    _VAULT_ROOT / "iii" / "what" / "context" / "canvasforge_iii_learning_store.jsonl"
)
DEFAULT_CORPUS_DIR = _VAULT_ROOT / "what" / "artifacts" / "image_gen_dataset" / "2026-05"

# ADR-005 §2 enum values
RLHF_SIGNAL_TYPE_ACCEPT = "accept"
RLHF_SIGNAL_TYPE_REJECT = "reject"
RLHF_SIGNAL_TYPE_DEFER = "defer"
RLHF_SIGNAL_TYPE_ACCEPT_WITH_MODIFICATION = "accept_with_modification"

# Vault-local trap name per ADR-005 §3 rule 1 (consumer-namespace fields never
# trigger ADR-005 amendment; a trap value scoped to image-generation picks is
# a consumer-specific extension). Distinguished from the canvas-visual traps
# loaded via the bridge_pack (CV-*).
TRAP_IMAGE_GENERATION_VARIANT_PICK = "image_generation_variant_pick"

# Entry id prefix — C-CFE-* (CanvasForge Pillar E); distinguishes bridge-emitted
# entries from G-01 F3-migrated entries (C-NEW-*) and from canonical entries
# (C-NNN per ADR-003 §4 — only Argus mints).
ENTRY_ID_PREFIX = "C-CFE-"


def _normalize_iso8601_utc(timestamp: str) -> str:
    """Normalize Python-isoformat UTC timestamp to ADR-005 §2 ``Z`` form.

    ADR-005 §2 specifies ``YYYY-MM-DDTHH:MM:SSZ``. The
    ``SelectionRecord.timestamp`` field uses ``datetime.now(timezone.utc).
    isoformat()`` which produces ``...+00:00`` with microseconds; this
    function strips microseconds and replaces the offset with ``Z``.
    """
    parsed = datetime.fromisoformat(timestamp)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    parsed = parsed.astimezone(timezone.utc).replace(microsecond=0)
    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ")


def _derive_pattern(register: str) -> str:
    """Derive a stable snake_case pattern name from ``register``.

    The pattern field is a per-pattern equivalence-class identifier per
    ADR-007 §1 (``a 'pattern' is a single correction-entry equivalence class
    identified by ``pattern: snake_case_id```). Bridge-emitted patterns are
    derived deterministically so that re-runs on the same input produce the
    same pattern (idempotency) and graduation-candidate scans can group
    equivalent picks across sessions.

    Format: ``image_gen_pick_<register_normalized>``. The register alone is
    the equivalence-class key — picks within the same voice register collapse
    to one pattern, even when their ``pick_reason`` text differs. Per-pick
    uniqueness lives on the ``id`` field (derived from ``selection_id``);
    ``pattern`` is the class label that the ADR-003 §3 graduation gate scores
    on (frequency ≥ 3 across ≥ 2 sessions). See ADR-007 §3 footnote and
    M-V1-2-F-01 S1 finding F-F-01.S1.C / F-E-01.S2.B for rationale.
    """
    register_normalized = (
        register.lower().replace("+", "_").replace("-", "_").replace(" ", "_")
    )
    return f"image_gen_pick_{register_normalized}"


def _derive_entry_id(selection_id: str) -> str:
    """Bridge-entry id derived from selection_id (idempotent + traceable)."""
    return f"{ENTRY_ID_PREFIX}{selection_id}"


def _truncate(text: str, *, limit: int = 280) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def selection_to_iii_signal(sel: SelectionRecord, *, session_id: str) -> dict[str, Any]:
    """Map a ``SelectionRecord`` to an ADR-005 §2-compliant III learning-store signal.

    Validates the input via ``validate_selection_record`` first; raises
    ``ValueError`` on schema violation (hard-fail per
    ``canvas_core.rlhf.selection`` module doctrine).

    Returns a dict ready for jsonl append. The shape carries:
    - ADR-003 §4 base correction fields (``id``, ``trap``, ``pattern``,
      ``description``, ``example``, ``source_review``, ``source_finding``,
      ``frequency=1``, ``accepted=True``, ``created``).
    - ADR-005 §2 required-min (``rlhf_signal_type=accept``,
      ``rlhf_session_id``, ``rlhf_captured_at``).
    - ADR-005 §2 optional-open (``rlhf_reviewer_persona`` from
      ``approver_id`` when present).
    - ADR-005 §3 consumer-namespace (``rlhf_consumer_namespace.canvasforge.
      image_generation.*``) nested-object projection of the rich
      sel-record context.

    ``frequency`` is always 1 at write — cross-session aggregation is
    derived at graduation-candidate scan time by grouping entries on
    ``(trap, pattern)`` per ADR-003 §3 + ADR-007 §1
    inference-from-observable-fields. The bridge does not mutate
    pre-existing entries.

    Re-merge rationale (CR7+SO7):
    ``lattice-labs/who/coordination/coord_2026_04_16_forge_split.md``.
    """
    errors = validate_selection_record(sel)
    if errors:
        raise ValueError(
            f"SelectionRecord schema violations ({len(errors)}): " + "; ".join(errors)
        )
    selected_variant = sel.variants[sel.pick_index]
    pattern = _derive_pattern(sel.register)

    entry: dict[str, Any] = {
        # ADR-003 §4 base correction fields
        "id": _derive_entry_id(sel.selection_id),
        "trap": TRAP_IMAGE_GENERATION_VARIANT_PICK,
        "pattern": pattern,
        "description": (
            f"Operator picked image variant {sel.pick_index + 1}/{len(sel.variants)} "
            f"for register {sel.register}"
        ),
        "example": _truncate(sel.pick_reason),
        "source_review": f"M-V1-VAL-01 image_gen_dataset {sel.selection_id}",
        "source_finding": sel.selection_id,
        "frequency": 1,
        "accepted": True,
        "created": _normalize_iso8601_utc(sel.timestamp)[:10],
        # ADR-005 §2 required-min RLHF fields
        "rlhf_signal_type": RLHF_SIGNAL_TYPE_ACCEPT,
        "rlhf_session_id": session_id,
        "rlhf_captured_at": _normalize_iso8601_utc(sel.timestamp),
    }
    # ADR-005 §2 optional-open
    if sel.approver_id:
        entry["rlhf_reviewer_persona"] = sel.approver_id
    # ADR-005 §3 consumer-namespace — nested-object shape per M-V1-2-G-01 F3
    # migration precedent already in the local store.
    entry["rlhf_consumer_namespace"] = {
        "canvasforge": {
            "image_generation": {
                "prompt": sel.prompt,
                "register": sel.register,
                "budget_class": sel.budget_class,
                "variants_offered": len(sel.variants),
                "pick_index": sel.pick_index,
                "pick_reason": sel.pick_reason,
                "register_compliance_score": sel.register_compliance_score,
                "vr_scores": sel.vr_scores,
                "selection_id": sel.selection_id,
                "selected_variant_path": selected_variant.image_path,
                "selected_variant_model": selected_variant.model,
                "selected_variant_cost_usd": selected_variant.cost_usd,
                "bridge_module": "canvas_core.rlhf.iii_bridge",
            }
        }
    }
    return entry


def _consumer_namespace_selection_id(entry: dict[str, Any]) -> str | None:
    """Extract selection_id from the nested consumer-namespace projection."""
    return (
        entry.get("rlhf_consumer_namespace", {})
        .get("canvasforge", {})
        .get("image_generation", {})
        .get("selection_id")
    )


def _existing_selection_ids(store_path: Path) -> set[str]:
    """Read jsonl and collect ``selection_id`` values already present.

    Used by ``accumulate`` for idempotency (refuse to double-append). Lines
    that fail to parse or carry no consumer-namespace ``selection_id`` are
    silently skipped — pre-existing entries (e.g., the 4 G-01 F3-migrated
    ``C-NEW-*`` entries) don't carry one and are correctly ignored.
    """
    if not store_path.exists():
        return set()
    ids: set[str] = set()
    with store_path.open() as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            sid = _consumer_namespace_selection_id(entry)
            if sid:
                ids.add(sid)
    return ids


def accumulate(
    signal: dict[str, Any], *, store_path: Path = DEFAULT_LEARNING_STORE
) -> bool:
    """Append a single signal to the local learning store.

    Idempotent on the consumer-namespace ``selection_id`` — re-running on a
    signal already in the store is a no-op. Returns True if a new line was
    written; False if the entry was already present.

    Raises ``ValueError`` if the signal lacks the consumer-namespace
    ``selection_id`` (such a signal cannot be deduplicated and so cannot be
    safely accumulated under this contract).
    """
    selection_id = _consumer_namespace_selection_id(signal)
    if not selection_id:
        raise ValueError(
            "signal missing rlhf_consumer_namespace.canvasforge.image_generation.selection_id"
        )
    existing = _existing_selection_ids(store_path)
    if selection_id in existing:
        return False
    store_path.parent.mkdir(parents=True, exist_ok=True)
    with store_path.open("a") as handle:
        handle.write(json.dumps(signal, ensure_ascii=False) + "\n")
    return True


def accumulate_directory(
    directory: Path,
    *,
    session_id: str,
    store_path: Path = DEFAULT_LEARNING_STORE,
) -> dict[str, list[str]]:
    """Scan ``directory`` for Schema-A ``sel_*.json`` records; map + accumulate each.

    Schema discrimination is by presence of Schema-A required keys; records
    that don't conform (Schema-B from ``image_generation.write_selection_record``
    or Schema-C from the visual-style RLHF runner) are skipped without
    error — they're flagged in the returned report for downstream
    handling.

    Returns a report dict with three lists keyed by outcome.
    """
    accumulated: list[str] = []
    skipped_duplicate: list[str] = []
    skipped_non_schema_a: list[str] = []
    for path in sorted(directory.glob("sel_*.json")):
        try:
            raw = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            skipped_non_schema_a.append(path.name)
            continue
        try:
            sel = SelectionRecord.from_dict(raw)
        except (KeyError, TypeError):
            skipped_non_schema_a.append(path.name)
            continue
        try:
            signal = selection_to_iii_signal(sel, session_id=session_id)
        except ValueError:
            skipped_non_schema_a.append(path.name)
            continue
        if accumulate(signal, store_path=store_path):
            accumulated.append(path.name)
        else:
            skipped_duplicate.append(path.name)
    return {
        "accumulated": accumulated,
        "skipped_duplicate": skipped_duplicate,
        "skipped_non_schema_a": skipped_non_schema_a,
    }


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m canvas_core.rlhf.iii_bridge",
        description=(
            "Backfill the CanvasForge-local III learning store from existing "
            "sel_*.json records. See ADR-006 (bridge contract). Live-wire "
            "ingest at write_selection time is a Pillar F follow-up."
        ),
    )
    parser.add_argument(
        "--backfill",
        action="store_true",
        help="Scan corpus directory and accumulate Schema-A sel records",
    )
    parser.add_argument(
        "--directory",
        type=Path,
        default=DEFAULT_CORPUS_DIR,
        help=f"Corpus directory (default: {DEFAULT_CORPUS_DIR})",
    )
    parser.add_argument(
        "--session-id",
        required=True,
        help="Active session id, used as rlhf_session_id on emitted signals",
    )
    parser.add_argument(
        "--store",
        type=Path,
        default=DEFAULT_LEARNING_STORE,
        help=f"Learning store path (default: {DEFAULT_LEARNING_STORE})",
    )
    args = parser.parse_args(argv)
    if not args.backfill:
        parser.error("specify --backfill (live-wire ingest is Pillar F scope)")
    report = accumulate_directory(
        args.directory, session_id=args.session_id, store_path=args.store
    )
    print(f"accumulated: {len(report['accumulated'])} records")
    for name in report["accumulated"]:
        print(f"  + {name}")
    if report["skipped_duplicate"]:
        print(f"skipped (duplicate selection_id): {len(report['skipped_duplicate'])}")
        for name in report["skipped_duplicate"]:
            print(f"  · {name}")
    if report["skipped_non_schema_a"]:
        print(f"skipped (not Schema-A): {len(report['skipped_non_schema_a'])}")
        for name in report["skipped_non_schema_a"]:
            print(f"  · {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
