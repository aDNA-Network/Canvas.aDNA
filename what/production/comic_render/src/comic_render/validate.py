"""Stage 6 — validate: the hard gate on ``issue.rendered.canvas`` (roadmap §1).

Green means ALL of: ``canvas_std.validate_suite`` reaches **aDNA-Native** with the declared level
met · degradation **D-1/D-2/D-3** all true (strip → a clean baseline canvas) · every ``file``
node's target exists under the vault root · the topology-only sync hash still equals the
manifest's. Effective-DPI below 200 is a **warning**, not a failure (R7: accept it on the v0
proof page; the refine/upscale chain addresses it later).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from canvas_core.print import effective_dpi
from canvas_std import ConformanceLevel, compute_sync_hash, validate_suite

from comic_render.extract import load_canvas, reserved_block
from comic_render.manifest import RenderManifest, rendered_canvas_path_for
from comic_render.png_meta import read_png_size
from comic_render.vault import resolve_vault_root

DPI_WARNING_THRESHOLD = 200  # mirrors canvas_core.print — panels below this warn


class BridgeValidationError(RuntimeError):
    """The rendered canvas failed the stage-6 gate."""


def run_validate(
    manifest: RenderManifest,
    manifest_path: str | Path,
    *,
    vault_root: str | Path | None = None,
) -> dict[str, Any]:
    manifest_path = Path(manifest_path)
    base = manifest_path.parent
    rendered_path = rendered_canvas_path_for(base / manifest.source_canvas)
    if not rendered_path.exists():
        raise BridgeValidationError(f"{rendered_path.name} not found — run write-back first")

    doc = load_canvas(rendered_path)
    failures: list[str] = []
    warnings: list[str] = []

    # 1. Conformance: declared level (the producer emits adna_native) + degradation.
    declared_name = reserved_block(doc).get("conformance_level", "adna_native")
    declared = ConformanceLevel(declared_name)
    report = validate_suite(doc, declared)
    if not report.meets_declared:
        failures += [f"conformance: {f['msg']}" for f in report.failed]
    if declared is ConformanceLevel.ADNA_NATIVE:
        if report.level_reached is not ConformanceLevel.ADNA_NATIVE:
            failures.append(
                f"conformance: level_reached "
                f"{report.level_reached.value if report.level_reached else None} != adna_native"
            )
        for check, ok in report.degradation.items():
            if not ok:
                failures.append(f"degradation: {check} failed (strip is not baseline-clean)")

    # 2. Topology: the rendered view must still hash to the manifest's source topology.
    got_hash = compute_sync_hash(doc)
    if got_hash != manifest.source_sync_hash:
        failures.append(f"sync_hash {got_hash} != manifest {manifest.source_sync_hash}")

    # 3. Every file node's target exists (vault-relative resolution).
    root = resolve_vault_root(rendered_path, vault_root)
    files_checked = 0
    for node in doc.get("nodes", []):
        if isinstance(node, dict) and node.get("type") == "file":
            files_checked += 1
            target = root / node.get("file", "")
            if not target.exists():
                failures.append(f"file node {node.get('id')!r}: missing target {node.get('file')}")

    # 4. Effective DPI per rendered panel (warning-only, R7).
    by_id = {n["id"]: n for n in doc.get("nodes", []) if isinstance(n, dict) and "id" in n}
    for panel in manifest.panels:
        node = by_id.get(panel.panel_id)
        if not node or node.get("type") != "file":
            continue
        target = root / node.get("file", "")
        if not target.exists():
            continue  # already a failure above
        try:
            src_w, src_h = read_png_size(target)
        except ValueError:
            continue  # non-PNG (H3+ formats) — DPI check is PNG-scoped at H2
        eff = min(
            effective_dpi(src_w, panel.target_px["w"]),
            effective_dpi(src_h, panel.target_px["h"]),
        )
        if 0 < eff < DPI_WARNING_THRESHOLD:
            warnings.append(
                f"panel {panel.panel_id}: effective DPI {eff:.1f} < {DPI_WARNING_THRESHOLD} "
                f"(source {src_w}x{src_h} vs target {panel.target_px['w']}x{panel.target_px['h']})"
            )

    if failures:
        raise BridgeValidationError(
            f"{rendered_path.name} failed the stage-6 gate ({len(failures)}): "
            + "; ".join(failures)
        )
    return {
        "ok": True,
        "rendered_canvas": rendered_path.name,
        "level_reached": report.level_reached.value if report.level_reached else None,
        "degradation": report.degradation,
        "files_checked": files_checked,
        "warnings": warnings,
    }
