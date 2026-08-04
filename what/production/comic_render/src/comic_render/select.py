"""Stage 4 — select: choose one variant per panel + write the **Schema-A** ``SelectionRecord``.

Records go through ``canvas_core.rlhf`` exclusively (roadmap R8): ``SelectionRecord`` +
``backprop.write_selection`` (atomic write + audit log). NEVER ``ImagenWiring``'s
``{item_id}.selection.json`` sidecar — that is Schema-B, which the III bridge deliberately skips.

H2's policy is deterministic-offline (default: first variant); H3's operator eye-gate rides the
same call with a real ``approver_id`` + ``pick_reason``. Fake-run records land under the run dir
(``runs/<comic_id>/selections/``) so the real RLHF corpus (`what/artifacts/image_gen_dataset`)
never sees offline noise; image paths are stored relative to the manifest dir (F-36: never
absolute).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from canvas_core.rlhf import SelectionRecord
from canvas_core.rlhf.backprop import write_selection
from canvas_core.rlhf.selection import VariantInfo

from comic_render.manifest import RenderManifest

DEFAULT_PICK_REASON = "deterministic offline pick (H2 fake pipeline)"
DEFAULT_APPROVER = "comic_render_auto"


def run_select(
    manifest: RenderManifest,
    manifest_path: str | Path,
    *,
    pick_index: int = 0,
    pick_reason: str = DEFAULT_PICK_REASON,
    approver_id: str = DEFAULT_APPROVER,
    dataset_root: str | Path | None = None,
) -> dict[str, Any]:
    """Select per panel among ``final_outputs`` (refined if present, else variants)."""
    manifest_path = Path(manifest_path)
    base = manifest_path.parent
    summary: dict[str, Any] = {"selected": [], "skipped": [], "records": []}

    for panel in manifest.dispatchable():
        existing = panel.results.get("selection")
        if existing and (base / existing["record_path"]).exists():
            summary["skipped"].append(panel.panel_id)
            continue

        outputs = panel.final_outputs()
        if not outputs:
            raise RuntimeError(f"select before dispatch for panel {panel.panel_id!r} — no outputs")
        if not 0 <= pick_index < len(outputs):
            raise ValueError(
                f"pick_index {pick_index} out of range for {panel.panel_id!r} "
                f"({len(outputs)} outputs)"
            )
        chosen = outputs[pick_index]

        record = SelectionRecord(
            prompt=panel.prompt_text,
            register=manifest.register,
            variants=[
                VariantInfo(
                    image_path=v,  # relative to the manifest dir — F-36: never absolute
                    model=panel.results.get("model", "unknown"),
                    cost_usd=panel.results.get("cost_per_image", 0.0),
                    seed=panel.seed,
                )
                for v in outputs
            ],
            pick_index=pick_index,
            pick_reason=pick_reason,
            approver_id=approver_id,
        )
        root = Path(dataset_root) if dataset_root else base / panel.output_dir / "selections"
        record_path = Path(write_selection(record, dataset_root=root))
        try:
            stored_record_path = str(record_path.relative_to(base))
        except ValueError:
            stored_record_path = str(record_path)

        panel.results["selection"] = {
            "selected": chosen,
            "pick_index": pick_index,
            "selection_record": record.selection_id,
            "record_path": stored_record_path,
        }
        summary["selected"].append(panel.panel_id)
        summary["records"].append(record.selection_id)
        manifest.save(manifest_path)

    manifest.save(manifest_path)
    return summary
