"""Stage 7 — compose: ``issue.rendered.canvas`` → print-ready page JPGs via ``PrintExporter``.

``canvas_core.print.PrintExporter`` duck-types legacy builder objects (``.pages`` +
``.get_panel``) and expects **print-canvas units** (the 687.5×1050 bleed page, 1" = 100 units).
The producer's canvas positions panels in **canvas-absolute** units on 663×1025 page groups —
the R5 geometry seam. This shim is the adapter: page-local remap (node − page origin) plus the
12.5-unit bleed margin, with a full-page panel promoted to a true full-bleed placement. PIL is
reached ONLY through ``canvas_core.print`` (boundary rule) — this module never imports it.

Trim/bleed derivation (canvas_comic lineage, mirrored in ``canvas_core.print`` constants):
trim = 662.5×1025 units (1988×3075 px @300), bleed = 687.5×1050 (2062×3150 px) → margin =
(687.5−662.5)/2 = **12.5 units** each side. Page groups are authored at 663×1025 (the 0.5-unit
slop is why the placement golden carries a ±1 px tolerance).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from canvas_core.print import BLEED_WIDTH, PrintExporter

from comic_render.extract import _nodes_by_id, _ordered_pages, load_canvas, reserved_block
from comic_render.manifest import RenderManifest, rendered_canvas_path_for
from comic_render.vault import resolve_vault_root

TRIM_UNITS_W = 662.5
TRIM_UNITS_H = 1025.0
BLEED_MARGIN_UNITS = 12.5  # (687.5 − 662.5) / 2 == (1050 − 1025) / 2
_FULL_PAGE_TOLERANCE_UNITS = 1.0  # producer authors pages at 663×1025 (trim + 0.5 rounding)


@dataclass
class _ShimPanel:
    """Duck-typed panel for ``PrintExporter`` (print-canvas units)."""

    id: str
    x: float
    y: float
    width: float
    height: float
    image_path: str | None
    bleed: bool = False
    span_rows: int = 1
    span_cols: int = 1


@dataclass
class _ShimPage:
    """Duck-typed page for ``PrintExporter``."""

    page_number: int
    id: str
    panel_ids: list[str] = field(default_factory=list)
    color_script: Any = None  # default background — page color scripts arrive with H5/H6


class _ShimBuilder:
    """The ``cpb`` duck: ``.pages`` + ``.get_panel(id)``."""

    def __init__(self, pages: list[_ShimPage], panels: dict[str, _ShimPanel]) -> None:
        self.pages = pages
        self._panels = panels

    def get_panel(self, panel_id: str) -> _ShimPanel | None:
        return self._panels.get(panel_id)


def _is_full_page(node: dict[str, Any], page: dict[str, Any]) -> bool:
    return all(
        abs(node.get(k, 0) - page.get(k, 0)) <= _FULL_PAGE_TOLERANCE_UNITS
        for k in ("x", "y", "width", "height")
    )


def build_shim(
    doc: dict[str, Any],
    manifest: RenderManifest,
    *,
    vault_root: Path,
) -> _ShimBuilder:
    """Adapt the rendered canvas + manifest into PrintExporter's duck-typed builder."""
    reserved = reserved_block(doc)
    component_types = reserved.get("component_types", {})
    nodes = _nodes_by_id(doc)

    page_ids = [
        nid for nid, spec in component_types.items()
        if spec.get("semantic_type") == "page" and nid in nodes
    ]
    ordered = _ordered_pages(doc, page_ids)
    page_of = {p.panel_id: p.page_number for p in manifest.panels}

    pages = [_ShimPage(page_number=i + 1, id=pid) for i, pid in enumerate(ordered)]
    panels: dict[str, _ShimPanel] = {}

    for spec in manifest.panels:
        node = nodes.get(spec.panel_id)
        page_index = page_of[spec.panel_id] - 1
        if node is None or not (0 <= page_index < len(pages)):
            continue
        page_node = nodes[ordered[page_index]]
        image_path: str | None = None
        if node.get("type") == "file" and node.get("file"):
            resolved = vault_root / node["file"]
            image_path = str(resolved) if resolved.exists() else None

        if node.get("width", 0) > BLEED_WIDTH * 1.5:
            raise NotImplementedError(
                f"panel {spec.panel_id!r} is a two-page spread — spread compose lands at H6"
            )
        if _is_full_page(node, page_node):
            panel = _ShimPanel(
                id=spec.panel_id, x=0.0, y=0.0,
                width=BLEED_WIDTH, height=TRIM_UNITS_H + 2 * BLEED_MARGIN_UNITS,
                image_path=image_path, bleed=True, span_rows=3, span_cols=2,
            )
        else:
            panel = _ShimPanel(
                id=spec.panel_id,
                x=(node.get("x", 0) - page_node.get("x", 0)) + BLEED_MARGIN_UNITS,
                y=(node.get("y", 0) - page_node.get("y", 0)) + BLEED_MARGIN_UNITS,
                width=node.get("width", 0),
                height=node.get("height", 0),
                image_path=image_path,
            )
        panels[spec.panel_id] = panel
        pages[page_index].panel_ids.append(spec.panel_id)

    return _ShimBuilder(pages, panels)


def run_compose(
    manifest: RenderManifest,
    manifest_path: str | Path,
    *,
    vault_root: str | Path | None = None,
    cmyk: bool = False,
    jpeg_quality: int = 95,
) -> dict[str, Any]:
    """Composite every page of the rendered canvas to ``runs/<comic_id>/pages/*.jpg``.

    ``cmyk`` defaults off at H2 (deterministic offline RGB; ICC conversion is machine-dependent) —
    the print-grade CMYK/DPI policy pass is H6 scope.
    """
    manifest_path = Path(manifest_path)
    base = manifest_path.parent
    rendered_path = rendered_canvas_path_for(base / manifest.source_canvas)
    if not rendered_path.exists():
        raise FileNotFoundError(f"{rendered_path.name} not found — run write-back first")

    doc = load_canvas(rendered_path)
    root = resolve_vault_root(rendered_path, vault_root)
    shim = build_shim(doc, manifest, vault_root=root)

    out_dir = base / (manifest.panels[0].output_dir if manifest.panels else f"runs/{manifest.comic_id}")
    out_dir = out_dir / "pages"
    exporter = PrintExporter(
        shim, out_dir, issue_name=manifest.comic_id, cmyk=cmyk, jpeg_quality=jpeg_quality
    )
    results = exporter.export_all()
    return {
        "pages": [
            {
                "page_number": r.page_number,
                "filename": r.filename,
                "path": r.path,
                "width": r.width,
                "height": r.height,
                "warnings": list(r.warnings),
            }
            for r in results
        ],
        "output_dir": str(out_dir),
        "warnings": [w for r in results for w in r.warnings],
    }
