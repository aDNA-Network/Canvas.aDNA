"""III RLHF bridge — map Canvas selection records to ADR-005 signals.

Closes the HITL feedback loop for image generation: each operator
variant-pick captured as a ``sel_*.json`` becomes an ADR-005 §2-compliant
signal in the Canvas-local III learning store at
``how/federation/iii/what/context/canvas_iii_learning_store.jsonl``
(reached below via the vault-root ``iii`` symlink). Single-vault
start per ``campaign_canvasforge_v1_2_planning`` Q3=b — writes to the
local store only; cross-vault graduation defers to ADR-003 §3 with
standard frequency ≥ 3 + acceptance ≥ 80% criteria. *(Store default
repointed 2026-08-04, Halftone HR — the pre-merge ``canvasforge_…`` name
had gone stale against the live store.)*

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
  Nested-object shape matches the M-V1-2-G-01 F3-migration precedent.
  *(Ground truth 2026-08-09, Halftone H6: the live store at
  ``DEFAULT_LEARNING_STORE`` holds a ``_meta`` header line plus two III
  learning-PATTERN entries — ``CANVAS-L-001``/``-002``, the
  ``lens``/``pattern``/``graduated`` idiom — and zero RLHF signals so far.
  The store is heterogeneous BY DESIGN; readers discriminate on the
  consumer-namespace ``selection_id``, never on line position. See
  ``what/specs/spec_rlhf_seam.md`` §2a.)*

**Re-merge rationale** (CR7+SO7):
``lattice-labs/who/coordination/coord_2026_04_16_forge_split.md``.

Created in M-V1-2-E-01 S1.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .selection import SelectionRecord, validate_selection_record

# Canvas.aDNA root: this file is at .../what/production/canvas_core/rlhf/iii_bridge.py
# so 5 parents up reaches the vault root.
_VAULT_ROOT = Path(__file__).resolve().parents[4]

DEFAULT_LEARNING_STORE = (
    _VAULT_ROOT / "iii" / "what" / "context" / "canvas_iii_learning_store.jsonl"
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

# The reject counterpart (S-1, spec_rlhf_seam §4). A separate trap rather than a flag on the pick
# trap: ADR-003 §3 graduation scores on ``(trap, pattern)`` frequency, and folding rejects into the
# pick trap would let "this variant was refused" accumulate toward "this register is working".
TRAP_IMAGE_GENERATION_VARIANT_REJECT = "image_generation_variant_reject"

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
        # ``accepted`` = the REVIEWER'S VERDICT (Argus ruling, 2026-09-07 — reading (b);
        # ``coord_2026_09_07_argus_to_mondrian_accepted_semantics_ruling.md``). ``True`` is correct
        # HERE and only here: a Schema-A record exists because the operator picked a variant, so the
        # reviewer genuinely did accept. The reject path deliberately writes ``False`` — see the S-4
        # block below. **That asymmetry is the whole content of the ruling; it is not an
        # inconsistency to tidy up.**
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


# ============================================================================================
# S-1 / S-2 — the reject path (spec_rlhf_seam §4, ratified 2026-08-09)
#
# Why this exists: ``RLHF_SIGNAL_TYPE_REJECT`` was declared when this bridge was written and was
# never emitted — line 190 below hard-codes ``accept``. Combined with Schema-A structurally
# requiring a pick, a reject-only review pass produced no Schema-A record and therefore **no III
# signal at all**. The rejection stayed durable in ``responses[]`` and invisible to every learning
# consumer. "None of these six is acceptable" is a stronger preference signal than "this one is
# best", and it was the one being dropped.
#
# The routing rule (§1): a reject signal derives from ``responses[]``, NOT from Schema-A. Schema-A
# stays approval-only and unchanged — no schema edit, no migration.
# ============================================================================================

REJECT_VERDICTS = frozenset({"reject", "rejected", "no", "decline", "declined"})

# S-4 GATE — ✅ RULED AND OPEN as of 2026-09-07. History kept, not rewritten:
#
#   [2026-08-09 — the question, as asked] spec_rlhf_seam §5 requires ADR-005 vocabulary
#   confirmation with Argus (III.aDNA) **before first emission** — the signal shape is III's, not
#   ours (§1 corollary). Specifically: whether ``accepted`` means "this entry was admitted to the
#   store" (our reading, so ``true`` on a reject) or "the reviewer accepted the image" (in which
#   case a reject must carry ``false``). The two readings produce opposite training signal from the
#   same line. So the reject path is BUILT and TESTED but does not write to the shared store by
#   default. This is a guard rather than a note-to-self because "we'll remember not to run it" is
#   not a mechanism.
#
#   [2026-09-07 — the ruling] Argus ruled **(b): ``accepted`` = the reviewer's verdict.** Rationale,
#   theirs: ADR-003 §3's graduation gate computes acceptance ≥80% over this field; under reading (a)
#   every stored entry is vacuously ``accepted: true`` and the gate measures *store admission*
#   rather than *operator judgment* — refusals would accumulate toward "this register is working",
#   which is precisely what the distinct-trap choice was made to avoid. Verdict semantics keep the
#   channels orthogonal: ``rlhf_signal_type`` = what the signal *is*; ``accepted`` = what the
#   reviewer *ruled*. Our three consumer-namespace choices were blessed as made — no change to the
#   distinct reject trap, the ``response_id`` dedup key, or the explicit no-rationale marking.
#   Memo: ``who/coordination/coord_2026_09_07_argus_to_mondrian_accepted_semantics_ruling.md``
#   (in reply to ``coord_2026_08_09_mondrian_to_argus_reject_signal_vocabulary.md``).
#
# ⚠ Flipping this constant ARMS the path; it does not emit anything by itself. At the flip the HR
# pilot held 0 rejects, so nothing was emitted that day. The intended first emitter is the P4
# ComfyUI variant-selection board (the pilot's second consumer).
REJECT_VOCABULARY_CONFIRMED = True

# The collector emits ONE response per selected defect tag on ``<vid>.defect`` (singular) — the
# multi-select control fans out rather than logging a list (review-surface spec §2).
DEFECT_AFFORDANCE_SUFFIX = "defect"


def response_id(
    canvas_stem: str, variant_id: str, approver: str, turn: str, at: str
) -> str:
    """Deterministic dedup key for a reject signal (S-2): ``rej_YYYYMMDD_HHMMSS_<4hex>``.

    Mirrors ``review_collect._selection_id``'s shape so the two id families read alike in the
    store, with a distinct prefix so they can never be confused. Derived entirely from the
    response's own coordinates, which is what makes re-collecting the same verdict a no-op.
    """
    stamp = datetime.fromisoformat(at).strftime("%Y%m%d_%H%M%S")
    digest = hashlib.sha256(
        f"{canvas_stem}|{variant_id}|{approver}|{turn}".encode()
    ).hexdigest()[:4]
    return f"rej_{stamp}_{digest}"


def fold_variant_responses(
    responses: list[dict[str, Any]],
    variant_id: str,
    *,
    participant_id: str | None = None,
    turn: str | None = None,
) -> dict[str, Any]:
    """Gather the per-affordance ``responses[]`` entries for one variant into one verdict view.

    The capture substrate logs one entry per *affordance* (``<vid>.verdict``, ``<vid>.rating``,
    ``<vid>.defect_tags``, ``<vid>.note``), so a single human judgement is scattered across
    several append-only rows. This folds them back into the judgement that was actually made.

    Later entries win on scalar fields (the log is append-only, so a corrected verdict appears as
    a *new* row rather than an edit); defect tags accumulate, since the control is multi-select and
    the collector logs **one response per tag** (``<vid>.defect``, singular — spec §2). Reading
    that affordance as if it carried a list is the obvious way to get this wrong.
    """
    view: dict[str, Any] = {"variant_id": variant_id, "defect_tags": []}
    prefix = f"{variant_id}."
    for entry in responses:
        if not isinstance(entry, dict):
            continue
        aff = str(entry.get("affordance") or "")
        if not aff.startswith(prefix):
            continue
        if turn is not None and entry.get("turn") != turn:
            continue
        if participant_id is not None and (
            (entry.get("participant") or {}).get("id") != participant_id
        ):
            continue
        field = aff[len(prefix):]
        value = entry.get("value")
        if field == DEFECT_AFFORDANCE_SUFFIX:
            if value not in (None, "") and value not in view["defect_tags"]:
                view["defect_tags"].append(value)
        else:
            view[field] = value
        if entry.get("at") and (field == "verdict" or "at" not in view):
            view["at"] = str(entry["at"]) if field == "verdict" else view.get("at", str(entry["at"]))
    return view


def is_reject(view: dict[str, Any]) -> bool:
    return str(view.get("verdict") or "").strip().lower() in REJECT_VERDICTS


def _reject_rationale(view: dict[str, Any]) -> str:
    """The rationale field — ``defect_tags`` + ``note`` are the CONTENT of the rejection (§4.5).

    Without them a reject signal says only "no", which is not learnable. With them it says what
    was wrong, which is the whole reason the ruling routes rejects to III at all.
    """
    parts = ["verdict=reject"]
    tags = view.get("defect_tags") or []
    if tags:
        parts.append(f"defects={list(tags)}")
    if view.get("rating") not in (None, ""):
        parts.append(f"rating={view['rating']}/5")
    note = str(view.get("note") or "").strip()
    if note:
        parts.append(f"note={note[:200]!r}")
    if not tags and not note:
        parts.append("no defect tags or note given — rejection reason not captured")
    return "; ".join(parts)


def response_to_iii_signal(
    responses: list[dict[str, Any]],
    *,
    variant_id: str,
    canvas_stem: str,
    session_id: str,
    register: str,
    approver: str,
    turn: str,
    prompt: str = "",
) -> dict[str, Any] | None:
    """``responses[]`` -> an ADR-005 reject signal, or None when this variant was not rejected.

    Returning None rather than raising is deliberate: the collector walks every variant, and "this
    one was approved" is an ordinary outcome of asking, not an error.
    """
    view = fold_variant_responses(responses, variant_id, participant_id=approver, turn=turn)
    if not is_reject(view):
        return None
    at = _normalize_iso8601_utc(str(view.get("at") or datetime.now(timezone.utc).isoformat()))
    rid = response_id(canvas_stem, variant_id, approver, turn, at)

    entry: dict[str, Any] = {
        "id": f"{ENTRY_ID_PREFIX}{rid}",
        "trap": TRAP_IMAGE_GENERATION_VARIANT_REJECT,
        "pattern": f"image_gen_reject_{_derive_pattern(register).removeprefix('image_gen_pick_')}",
        "description": (
            f"Operator rejected image variant {variant_id} for register {register}"
        ),
        "example": _truncate(_reject_rationale(view)),
        "source_review": f"HR review surface {canvas_stem}",
        "source_finding": rid,
        "frequency": 1,
        # ⛩ THE FIELD THE S-4 RULING CHANGED (Argus, 2026-09-07 — reading (b)). This read ``True``
        # from H3 until the ruling, on the reading that ``accepted`` meant "admitted to the store".
        # It does not: it is the reviewer's verdict, so a reject carries ``False``. Under the old
        # value ADR-003 §3's ≥80% graduation gate would have scored every refusal as evidence the
        # register was working — the exact inversion the distinct reject trap exists to prevent.
        # The pick path at ``selection_to_iii_signal`` still writes ``True``, correctly.
        "accepted": False,
        "created": at[:10],
        "rlhf_signal_type": RLHF_SIGNAL_TYPE_REJECT,
        "rlhf_session_id": session_id,
        "rlhf_captured_at": at,
        "rlhf_reviewer_persona": approver,
    }
    entry["rlhf_consumer_namespace"] = {
        "canvasforge": {
            "image_generation": {
                "prompt": prompt,
                "register": register,
                "variant_id": variant_id,
                "verdict": "reject",
                "defect_tags": list(view.get("defect_tags") or []),
                "note": str(view.get("note") or ""),
                "rating": view.get("rating"),
                # The dedup key. NOT ``selection_id``: there is no SelectionRecord behind a
                # reject, and naming one would be a lie the store cannot detect.
                "response_id": rid,
                "derived_from": "interaction.responses",
                "bridge_module": "canvas_core.rlhf.iii_bridge",
            }
        }
    }
    return entry


def _consumer_namespace_selection_id(entry: dict[str, Any]) -> str | None:
    """Extract the dedup key from the nested consumer-namespace projection.

    Two keys can carry it, and which one is present says what kind of signal this is:

    - ``selection_id`` — an **accept**, keyed by its Schema-A ``SelectionRecord``.
    - ``response_id``  — a **reject** (S-2), keyed by a deterministic id derived from the
      ``responses[]`` entries themselves. A reject has no ``SelectionRecord`` to borrow an id from
      (Schema-A structurally requires a pick), and writing its id into the ``selection_id`` slot
      would name a record that does not exist. Separate key, same slot in the dedup logic.
    """
    ns = (
        entry.get("rlhf_consumer_namespace", {})
        .get("canvasforge", {})
        .get("image_generation", {})
    )
    return ns.get("selection_id") or ns.get("response_id")


def _existing_selection_ids(store_path: Path) -> set[str]:
    """Read jsonl and collect the dedup keys already present (``selection_id`` OR ``response_id``).

    Used by ``accumulate`` for idempotency (refuse to double-append). Lines that fail to parse or
    carry neither key are silently skipped — the store is **heterogeneous by design**
    (spec_rlhf_seam §2a): it also holds a ``_meta`` header and III learning-pattern entries
    (``CANVAS-L-*``), which carry no consumer-namespace key and are correctly ignored rather than
    corrupting the check.
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
            "signal missing rlhf_consumer_namespace.canvasforge.image_generation."
            "{selection_id|response_id}"
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
