"""Stage 5 — write-back: selections → ``issue.rendered.canvas`` (a NEW file; input immutable).

Safe by construction (roadmap §1): the topology-only sync hash (sorted node ids + edge pairs —
``canvas_std/roundtrip.py``) is untouched because write-back NEVER adds or removes nodes/edges.
Per selected panel: node ``type text→file`` (vault-relative path, ``text`` payload dropped),
``component_types[nid].degrades_to → "file"``, ``qualities.status → "rendered"``, and a
``render_provenance`` block. ``_reserved.sync`` must come out byte-identical — asserted, not
assumed. The five ``ANCHOR_REF_KEYS`` are never introduced as qualities keys — also asserted.

``issue.rendered.canvas`` is a **derived artifact** (operator ruling 2026-08-03): the YAML source
+ producer stay authoritative; re-render rather than merge back.
"""

from __future__ import annotations

import copy
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from canvas_std import compute_sync_hash
from canvas_std.reserved import ANCHOR_REF_KEYS

from comic_render.extract import load_canvas, reserved_block
from comic_render.manifest import (
    STATUS_PROMPT_ONLY,
    STATUS_RENDERED,
    RenderManifest,
    prompt_hash,
    rendered_canvas_path_for,
)
from comic_render.vault import resolve_vault_root


class WritebackInvariantError(RuntimeError):
    """A write-back invariant (topology / sync-block immutability / anchor keys) was violated."""


def run_writeback(
    manifest: RenderManifest,
    manifest_path: str | Path,
    *,
    vault_root: str | Path | None = None,
    force: bool = False,
) -> tuple[Path, dict[str, Any]]:
    """Produce ``issue.rendered.canvas`` beside the source. Idempotent: skips if already written."""
    manifest_path = Path(manifest_path)
    base = manifest_path.parent
    canvas_path = base / manifest.source_canvas
    out_path = rendered_canvas_path_for(canvas_path)
    summary: dict[str, Any] = {"rendered": [], "already_rendered": [], "skipped_policy": []}

    if out_path.exists() and not force:
        summary["unchanged"] = out_path.name
        return out_path, summary

    source_doc = load_canvas(canvas_path)
    source_hash = compute_sync_hash(source_doc)
    if source_hash != manifest.source_sync_hash:
        raise WritebackInvariantError(
            f"source canvas hash {source_hash} != manifest {manifest.source_sync_hash} — re-plan"
        )

    doc = copy.deepcopy(source_doc)
    reserved = reserved_block(doc)
    sync_before = json.dumps(reserved.get("sync"), sort_keys=True)
    nodes = {n["id"]: n for n in doc.get("nodes", []) if isinstance(n, dict) and "id" in n}
    component_types = reserved.get("component_types", {})
    root = resolve_vault_root(canvas_path, vault_root)

    missing_selection: list[str] = []
    for panel in manifest.panels:
        if panel.status == STATUS_RENDERED:
            summary["already_rendered"].append(panel.panel_id)  # producer-rendered — untouched
            continue
        if panel.status != STATUS_PROMPT_ONLY:
            summary["skipped_policy"].append(panel.panel_id)
            continue
        selection = panel.results.get("selection")
        if not selection:
            missing_selection.append(panel.panel_id)
            continue

        node = nodes[panel.panel_id]
        image_abs = (base / selection["selected"]).resolve()
        if not image_abs.exists():
            raise WritebackInvariantError(
                f"selected image missing for {panel.panel_id!r}: {image_abs}"
            )
        node["type"] = "file"
        node["file"] = Path(os.path.relpath(image_abs, root)).as_posix()
        node.pop("text", None)

        entry = component_types.setdefault(panel.panel_id, {})
        entry["degrades_to"] = "file"
        qualities = entry.setdefault("qualities", {})
        provenance = {
            "backend_chain": [
                {k: v for k, v in vars(s).items() if v is not None} for s in panel.render_chain
            ],
            "model": panel.results.get("model", "unknown"),
            "seed": panel.seed,
            "prompt_hash": prompt_hash(panel.prompt_text),
            "generated_at": datetime.now(UTC).isoformat(),
            "selection_record": selection["selection_record"],
        }
        qualities["status"] = STATUS_RENDERED
        qualities["render_provenance"] = provenance

        leaked = set(qualities) & set(ANCHOR_REF_KEYS)
        if leaked:
            raise WritebackInvariantError(
                f"qualities for {panel.panel_id!r} would carry anchor-checked keys {sorted(leaked)}"
            )
        summary["rendered"].append(panel.panel_id)

    if missing_selection:
        raise WritebackInvariantError(
            f"panels without selections (run select first): {missing_selection}"
        )

    # --- Invariants: topology + sync block byte-identical; no node/edge churn ---
    if compute_sync_hash(doc) != source_hash:
        raise WritebackInvariantError("sync_hash changed — write-back must never alter topology")
    if json.dumps(reserved_block(doc).get("sync"), sort_keys=True) != sync_before:
        raise WritebackInvariantError("_reserved.sync changed — write-back must not touch it")
    if len(doc.get("nodes", [])) != len(source_doc.get("nodes", [])) or len(
        doc.get("edges", [])
    ) != len(source_doc.get("edges", [])):
        raise WritebackInvariantError("node/edge count changed — write-back must never add/remove")

    out_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    summary["written"] = out_path.name
    return out_path, summary
