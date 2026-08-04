"""HR review collector — sidecar frontmatter verdicts -> the three sinks (canvas · Schema-A · III).

The capture half of ``spec_canvas_review_surface.md`` §4: the operator reviews in Obsidian (Meta Bind writes
sidecar **frontmatter**; ``enableJs: false``); this collector then fans each verdict into:

1. **Canvas** — one ``apply_response`` per answered control (``canvas_context.interaction`` — the ratified
   append-only fold; the collector owns the single disk write-back the pure function doesn't do);
2. **Schema-A** — a ``SelectionRecord`` per **approved** variant into the real corpus
   (``what/artifacts/image_gen_dataset/``; reject-only sessions write none — Schema-A structurally requires a
   pick, and the III bridge's charter is ``accept``-only; the rejection signal stays durable in
   ``interaction.responses[]`` + the sidecars. The reject→III seam is H6 open decision #4);
3. **III** — ``selection_to_iii_signal`` + ``accumulate`` into the live learning store.

Idempotency is layered (spec §4.3): the sidecar ``collected_at`` ledger (primary; ``--force`` or clearing it
re-opens a variant) → the response dedup key ``(affordance, value, participant.id, turn)`` (an identical replay
is a no-op even with a lost ledger) → the deterministic ``selection_id`` + existence check (no duplicate dataset
records / audit lines) → ``accumulate``'s native ``selection_id`` dedup. A mid-run crash self-heals on re-run
(per-variant writes are ordered canvas → dataset → III → ledger-last).

Participant attribution is honest by construction: ``--participant-kind ai`` marks agent plumbing runs
(``{kind: "ai"}``) — agent-simulated verdicts are never recorded as human signal.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from importlib.util import find_spec
from pathlib import Path
from typing import Any

import yaml

from .backprop import write_selection
from .iii_bridge import DEFAULT_LEARNING_STORE, accumulate, selection_to_iii_signal
from .selection import SelectionRecord, VariantInfo

_VAULT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_DATASET_ROOT = _VAULT_ROOT / "what" / "artifacts" / "image_gen_dataset"
DEFAULT_REGISTER = "ss_character"

# Sidecar control key -> affordance suffix + kind (spec §2/§3). Actions carry value None (I-3).
_ACTION_FLAGS = {"regenerate_requested": "regenerate", "pin_requested": "pin", "escalate": "escalate"}


def _ensure_canvas_context() -> Any:
    """Guarded bootstrap for the ``canvas_context`` interaction runtime (unpackaged, ``what/code/`` shelf).

    Mirrors the shelf's ``comic_render`` self-bootstrap precedent. Import-only — the firewall on
    ``what/code/`` holds (nothing there is modified); re-implementing the append here would drift from the
    ratified I-3 value/kind guard + IX6 state recompute, so the real module is used.
    """
    if find_spec("canvas_context") is None:
        sys.path.insert(0, str(_VAULT_ROOT / "what" / "code" / "canvas_context" / "src"))
    from canvas_context import interaction  # noqa: PLC0415

    return interaction


# ============================================================================================================
# Sidecar IO.
# ============================================================================================================

def split_sidecar(text: str) -> tuple[dict[str, Any], str]:
    """Frontmatter mapping + the verbatim remainder (body bytes preserved for the ledger rewrite)."""
    if not text.startswith("---"):
        raise ValueError("sidecar has no frontmatter block")
    _, fm_text, body = text.split("---", 2)
    fm = yaml.safe_load(fm_text) or {}
    if not isinstance(fm, dict):
        raise ValueError("sidecar frontmatter is not a mapping")
    return fm, body


def _write_ledger(path: Path, fm: dict[str, Any], body: str) -> None:
    """Rewrite frontmatter only — the body (Meta Bind controls) is preserved byte-verbatim."""
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000)
    path.write_text("---\n" + fm_text + "---" + body, encoding="utf-8")


def load_sidecars(sidecar_dir: Path) -> list[tuple[Path, dict[str, Any], str]]:
    """All review sidecars in the directory, ordered by ``variant_id`` (orphans without one error loudly)."""
    out: list[tuple[Path, dict[str, Any], str]] = []
    for p in sorted(sidecar_dir.glob("*.md")):
        fm, body = split_sidecar(p.read_text(encoding="utf-8"))
        if fm.get("type") != "review_sidecar":
            continue
        if not fm.get("variant_id"):
            raise ValueError(f"{p}: review_sidecar without a variant_id (orphan — refusing to guess)")
        out.append((p, fm, body))
    if not out:
        raise ValueError(f"{sidecar_dir}: no review sidecars found")
    return sorted(out, key=lambda t: str(t[1]["variant_id"]))


# ============================================================================================================
# Response planning (pure).
# ============================================================================================================

def planned_responses(fm: dict[str, Any]) -> list[tuple[str, Any]]:
    """The ordered ``(affordance_id, value)`` acts one sidecar's frontmatter implies. Empty/None = unanswered."""
    vid = str(fm["variant_id"])
    acts: list[tuple[str, Any]] = []
    verdict = fm.get("verdict")
    if verdict:
        acts.append((f"{vid}.verdict", str(verdict)))
    rating = fm.get("rating")
    if rating not in (None, ""):
        acts.append((f"{vid}.rating", str(rating)))
    for tag in fm.get("defect_tags") or []:
        acts.append((f"{vid}.defect", str(tag)))  # multi = one response per tag (spec §2)
    note = str(fm.get("note") or "").strip()
    if note:
        acts.append((f"{vid}.note", note))
    edit = str(fm.get("prompt_edit") or "").strip()
    if edit:
        acts.append((f"{vid}.prompt_edit", edit))
    for key, suffix in _ACTION_FLAGS.items():
        if fm.get(key):
            acts.append((f"{vid}.{suffix}", None))
    return acts


def _already_logged(doc: dict[str, Any], aff: str, value: Any, participant_id: str, turn: str) -> bool:
    responses = (
        doc.get("metadata", {}).get("frontmatter", {}).get("_reserved", {})
        .get("interaction", {}).get("responses", [])
    )
    for r in responses:
        if not isinstance(r, dict):
            continue
        if (
            r.get("affordance") == aff
            and r.get("value") == value
            and r.get("turn") == turn
            and (r.get("participant") or {}).get("id") == participant_id
        ):
            return True
    return False


def _selection_id(stamp_iso: str, canvas_stem: str, variant_id: str, approver: str, turn: str) -> str:
    """Deterministic ``sel_YYYYMMDD_HHMMSS_<4hex>`` — stable across re-runs once ``collected_at`` is set."""
    stamp = datetime.fromisoformat(stamp_iso).strftime("%Y%m%d_%H%M%S")
    digest = hashlib.sha256(f"{canvas_stem}|{variant_id}|{approver}|{turn}".encode()).hexdigest()[:4]
    return f"sel_{stamp}_{digest}"


def _first_verdict_at(doc: dict[str, Any], vid: str, participant_id: str, turn: str) -> str | None:
    """The earliest logged verdict-response ``at`` for this variant/participant/turn — makes the selection
    stamp (and so the selection_id) survive a LOST sidecar ledger: the canvas is the fallback clock."""
    responses = (
        doc.get("metadata", {}).get("frontmatter", {}).get("_reserved", {})
        .get("interaction", {}).get("responses", [])
    )
    for r in responses:
        if (
            isinstance(r, dict)
            and r.get("affordance") == f"{vid}.verdict"
            and r.get("turn") == turn
            and (r.get("participant") or {}).get("id") == participant_id
            and r.get("at")
        ):
            return str(r["at"])
    return None


def _pick_reason(fm: dict[str, Any]) -> str:
    parts = ["HR review-surface pilot: verdict=approve"]
    if fm.get("rating") not in (None, ""):
        parts.append(f"rating={fm['rating']}/5")
    tags = fm.get("defect_tags") or []
    if tags:
        parts.append(f"tags={list(tags)}")
    note = str(fm.get("note") or "").strip()
    if note:
        parts.append(f"note={note[:200]!r}")
    return "; ".join(parts)


# ============================================================================================================
# The collection run.
# ============================================================================================================

def collect(
    canvas_path: Path,
    *,
    sidecar_dir: Path | None = None,
    approver: str,
    participant_kind: str = "human",
    register: str = DEFAULT_REGISTER,
    dataset_root: Path = DEFAULT_DATASET_ROOT,
    store_path: Path = DEFAULT_LEARNING_STORE,
    session_id: str | None = None,
    turn: str | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> dict[str, int]:
    """Run one collection pass. Returns counts ``{variants, responses, selections, iii_lines, skipped}``."""
    interaction = _ensure_canvas_context()
    if not approver:
        raise ValueError("an --approver is required (no silent default identity)")

    doc = json.loads(canvas_path.read_text(encoding="utf-8"))
    block = doc.get("metadata", {}).get("frontmatter", {}).get("_reserved", {}).get("interaction")
    if not isinstance(block, dict):
        raise ValueError(f"{canvas_path}: no _reserved.interaction overlay — not a review surface")
    turn = turn or (block.get("state") or {}).get("turn") or "t1"
    if session_id is None:
        session_id = f"review_{canvas_path.stem}_{datetime.now(timezone.utc).strftime('%Y%m%d')}"

    sidecar_dir = sidecar_dir or canvas_path.parent / "sidecars"
    sidecars = load_sidecars(sidecar_dir)
    all_variants = [
        VariantInfo(image_path=str(fm.get("image_path", "")), model=str(fm.get("model", "") or "unknown"))
        for _, fm, _ in sidecars
    ]
    participant = {"kind": participant_kind, "id": approver}
    now_iso = datetime.now(timezone.utc).isoformat()

    counts = {"variants": 0, "responses": 0, "selections": 0, "iii_lines": 0, "skipped": 0}
    for index, (path, fm, body) in enumerate(sidecars):
        if not fm.get("verdict"):
            counts["skipped"] += 1
            continue
        if fm.get("collected_at") and not force:
            counts["skipped"] += 1
            continue
        counts["variants"] += 1

        # (a) canvas sink — append-only acts via the ratified fold; collector owns the disk write.
        for aff, value in planned_responses(fm):
            if _already_logged(doc, aff, value, approver, turn):
                continue
            doc = interaction.apply_response(
                doc, aff, value, participant=participant, turn=turn, at=now_iso
            )
            counts["responses"] += 1
        if not dry_run:
            canvas_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        # (b) Schema-A sink — approvals only; one record per approved variant (multi-approve legal).
        sid: str | None = None
        if str(fm.get("verdict")).lower() == "approve":
            vid = str(fm["variant_id"])
            stamp = str(
                fm.get("collected_at")
                or _first_verdict_at(doc, vid, approver, turn)
                or now_iso
            )
            sid = _selection_id(stamp, canvas_path.stem, str(fm["variant_id"]), approver, turn)
            record = SelectionRecord(
                prompt=str(fm.get("prompt") or f"{register} {fm['variant_id']}"),
                register=register,
                variants=list(all_variants),
                pick_index=index,
                pick_reason=_pick_reason(fm),
                approver_id=approver,
                selection_id=sid,
                timestamp=stamp,
            )
            rating = fm.get("rating")
            if rating not in (None, ""):
                record.vr_scores = {"overall": float(rating)}
            month = record.timestamp[:7]
            existing = dataset_root / month / f"{sid}.json"
            if not existing.exists() and not dry_run:
                write_selection(record, dataset_root=dataset_root)
                counts["selections"] += 1
            elif not existing.exists():
                counts["selections"] += 1  # dry-run: would write

            # (c) III sink — accept-only by bridge charter; natively idempotent on selection_id.
            signal = selection_to_iii_signal(record, session_id=session_id)
            if dry_run:
                if sid not in _existing_store_ids(store_path):
                    counts["iii_lines"] += 1
            elif accumulate(signal, store_path=store_path):
                counts["iii_lines"] += 1

        # ledger last — a crash before this line re-runs clean (layers 2–4 dedup the replay).
        if not dry_run:
            fm["collected_at"] = fm.get("collected_at") or now_iso
            fm["selection_id"] = sid
            fm["review_turn"] = turn
            _write_ledger(path, fm, body)
    return counts


def _existing_store_ids(store_path: Path) -> set[str]:
    from .iii_bridge import _existing_selection_ids

    return _existing_selection_ids(store_path)


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m canvas_core.rlhf.review_collect",
        description="Collect review-surface verdicts into the three sinks (canvas · Schema-A · III).",
    )
    ap.add_argument("canvas", type=Path, help="the review .canvas (its sidecars/ sit beside it by default)")
    ap.add_argument("--sidecar-dir", type=Path, default=None)
    ap.add_argument("--approver", required=True, help="reviewer identity for participant + approver_id")
    ap.add_argument("--participant-kind", choices=("human", "ai"), default="human",
                    help="attribution kind — agent plumbing runs MUST pass 'ai' (never forged as human)")
    ap.add_argument("--register", default=DEFAULT_REGISTER)
    ap.add_argument("--dataset-root", type=Path, default=DEFAULT_DATASET_ROOT)
    ap.add_argument("--store-path", type=Path, default=DEFAULT_LEARNING_STORE)
    ap.add_argument("--session-id", default=None)
    ap.add_argument("--turn", default=None, help="override the surface turn (re-review = t2, t3, …)")
    ap.add_argument("--dry-run", action="store_true", help="report what would be written; write nothing")
    ap.add_argument("--force", action="store_true", help="re-collect variants whose ledger is already set")
    args = ap.parse_args(argv)
    counts = collect(
        args.canvas,
        sidecar_dir=args.sidecar_dir,
        approver=args.approver,
        participant_kind=args.participant_kind,
        register=args.register,
        dataset_root=args.dataset_root,
        store_path=args.store_path,
        session_id=args.session_id,
        turn=args.turn,
        dry_run=args.dry_run,
        force=args.force,
    )
    mode = "DRY-RUN — nothing written" if args.dry_run else "written"
    print(
        f"review-collect ({mode}): {counts['variants']} variant(s) collected · "
        f"responses appended: {counts['responses']} · selections: {counts['selections']} · "
        f"iii lines: {counts['iii_lines']} · skipped: {counts['skipped']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
