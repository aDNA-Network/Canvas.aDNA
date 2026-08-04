"""Stage 1 — plan: ``issue.canvas`` → render manifest (staleness-guarded).

Reads the producer's aDNA-Native canvas (file-shaped handoff — this package never imports
``comic_generator``): panel nodes come from ``_reserved.component_types`` entries with
``class: "image"``; page order from the ``sequence`` edge chain over page groups; per-page reading
order from the ``reading_order`` edges declared in ``_reserved.panel_link``; page membership by
geometric containment. Idempotent: re-planning against an unchanged canvas (same topology-only
sync hash) keeps the existing manifest — with ``force`` it is rebuilt from scratch.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from canvas_core.print import canvas_units_to_px
from canvas_std import compute_sync_hash

from comic_render.manifest import (
    STATUS_PROMPT_ONLY,
    STATUS_RENDERED,
    PanelSpec,
    RenderManifest,
    RenderStage,
    default_seed,
    manifest_path_for,
)

DEFAULT_VARIANT_COUNT = 3
DEFAULT_CHAIN = "generate:fake"


class StaleManifestError(RuntimeError):
    """The canvas topology changed after the manifest was planned — re-plan required."""


def load_canvas(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def reserved_block(doc: dict[str, Any]) -> dict[str, Any]:
    """The aDNA-Native extension block (canonical location: ``metadata.frontmatter._reserved``)."""
    return doc.get("metadata", {}).get("frontmatter", {}).get("_reserved", {})


def check_freshness(manifest: RenderManifest, canvas_doc: dict[str, Any]) -> None:
    """Every post-plan stage calls this: refuse to act on a manifest planned for other topology."""
    current = compute_sync_hash(canvas_doc)
    if current != manifest.source_sync_hash:
        raise StaleManifestError(
            f"canvas sync_hash {current} != manifest.source_sync_hash "
            f"{manifest.source_sync_hash} — the canvas changed; re-run plan"
        )


def parse_chain(spec: str) -> list[RenderStage]:
    """Parse ``"generate:fake,refine:fake@0.4"`` → ordered RenderStages (chain, not switch)."""
    stages: list[RenderStage] = []
    for part in (s.strip() for s in spec.split(",") if s.strip()):
        stage_name, _, backend_part = part.partition(":")
        if not backend_part:
            raise ValueError(f"chain stage {part!r} must be '<stage>:<backend>[@denoise]'")
        backend, _, denoise_part = backend_part.partition("@")
        denoise = float(denoise_part) if denoise_part else None
        stages.append(RenderStage(stage=stage_name, backend=backend, denoise=denoise))
    if not stages:
        raise ValueError(f"empty render chain spec {spec!r}")
    return stages


# ---------------------------------------------------------------------------
# Canvas topology readers
# ---------------------------------------------------------------------------


def _nodes_by_id(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {n["id"]: n for n in doc.get("nodes", []) if isinstance(n, dict) and "id" in n}


def _contains(outer: dict[str, Any], inner: dict[str, Any]) -> bool:
    """Geometric containment test — inner's center inside outer's bounds."""
    cx = inner.get("x", 0) + inner.get("width", 0) / 2
    cy = inner.get("y", 0) + inner.get("height", 0) / 2
    return (
        outer.get("x", 0) <= cx <= outer.get("x", 0) + outer.get("width", 0)
        and outer.get("y", 0) <= cy <= outer.get("y", 0) + outer.get("height", 0)
    )


def _ordered_pages(doc: dict[str, Any], page_ids: list[str]) -> list[str]:
    """Order page groups by the ``sequence`` edge chain; fall back to reading position (y, x)."""
    page_set = set(page_ids)
    seq = {
        e["fromNode"]: e["toNode"]
        for e in doc.get("edges", [])
        if isinstance(e, dict) and e.get("fromNode") in page_set and e.get("toNode") in page_set
    }
    targets = set(seq.values())
    starts = [pid for pid in page_ids if pid in seq and pid not in targets]
    if len(starts) == 1:
        ordered = [starts[0]]
        while ordered[-1] in seq and len(ordered) <= len(page_ids):
            nxt = seq[ordered[-1]]
            if nxt in ordered:
                break  # cycle guard
            ordered.append(nxt)
        if len(ordered) == len(page_ids):
            return ordered
    nodes = _nodes_by_id(doc)
    return sorted(page_ids, key=lambda pid: (nodes[pid].get("y", 0), nodes[pid].get("x", 0)))


def _reading_order(doc: dict[str, Any], panel_ids: list[str], reserved: dict[str, Any]) -> list[str]:
    """Order a page's panels by its ``reading_order`` edge chain; fall back to (y, x)."""
    kinds = reserved.get("panel_link", {}).get("edges", {})
    panel_set = set(panel_ids)
    ro = {
        e["fromNode"]: e["toNode"]
        for e in doc.get("edges", [])
        if isinstance(e, dict)
        and kinds.get(e.get("id"), {}).get("kind") == "reading_order"
        and e.get("fromNode") in panel_set
        and e.get("toNode") in panel_set
    }
    targets = set(ro.values())
    starts = [pid for pid in panel_ids if pid in ro and pid not in targets]
    if len(starts) == 1:
        ordered = [starts[0]]
        while ordered[-1] in ro and len(ordered) <= len(panel_ids):
            nxt = ro[ordered[-1]]
            if nxt in ordered:
                break
            ordered.append(nxt)
        if len(ordered) == len(panel_ids):
            return ordered
    nodes = _nodes_by_id(doc)
    return sorted(panel_ids, key=lambda pid: (nodes[pid].get("y", 0), nodes[pid].get("x", 0)))


def comic_id_of(doc: dict[str, Any], canvas_path: str | Path) -> str:
    """Comic id: last segment of ``_reserved.sync.source_name`` (urn), else the canvas file stem."""
    source_name = reserved_block(doc).get("sync", {}).get("source_name") or ""
    if source_name:
        return str(source_name).rsplit(":", 1)[-1]
    return Path(canvas_path).stem


# ---------------------------------------------------------------------------
# Plan
# ---------------------------------------------------------------------------


def plan(
    canvas_path: str | Path,
    *,
    chain: str = DEFAULT_CHAIN,
    variant_count: int = DEFAULT_VARIANT_COUNT,
    budget_cap: float | None = None,
    register: str = "comic_default",
    force: bool = False,
) -> tuple[RenderManifest, Path]:
    """Build (or idempotently keep) the render manifest for ``canvas_path``.

    Returns ``(manifest, manifest_path)``. If a manifest already exists and the canvas topology is
    unchanged, the existing manifest is returned untouched (resumable state preserved) unless
    ``force`` rebuilds it.
    """
    canvas_path = Path(canvas_path)
    doc = load_canvas(canvas_path)
    sync_hash = compute_sync_hash(doc)
    out_path = manifest_path_for(canvas_path)

    if out_path.exists() and not force:
        existing = RenderManifest.load(out_path)
        if existing.source_sync_hash == sync_hash:
            return existing, out_path  # fresh — keep resumable state

    reserved = reserved_block(doc)
    component_types = reserved.get("component_types", {})
    nodes = _nodes_by_id(doc)

    page_ids = [
        nid for nid, spec in component_types.items()
        if spec.get("semantic_type") == "page" and nid in nodes
    ]
    panel_ids = [
        nid for nid, spec in component_types.items()
        if spec.get("class") == "image" and nid in nodes
    ]
    if not panel_ids:
        raise ValueError(f"{canvas_path}: no image-class panel components found in _reserved")

    ordered_pages = _ordered_pages(doc, page_ids)
    page_number = {pid: i + 1 for i, pid in enumerate(ordered_pages)}

    panels_by_page: dict[str, list[str]] = {pid: [] for pid in ordered_pages}
    unassigned: list[str] = []
    for nid in panel_ids:
        for pid in ordered_pages:
            if _contains(nodes[pid], nodes[nid]):
                panels_by_page[pid].append(nid)
                break
        else:
            unassigned.append(nid)
    if unassigned:
        raise ValueError(f"{canvas_path}: panels not contained by any page group: {unassigned}")

    comic_id = comic_id_of(doc, canvas_path)
    default_chain = parse_chain(chain)
    output_dir = f"runs/{comic_id}"

    specs: list[PanelSpec] = []
    missing_prompts: list[str] = []
    for pid in ordered_pages:
        reading = _reading_order(doc, panels_by_page[pid], reserved)
        for idx, nid in enumerate(reading):
            node = nodes[nid]
            q = component_types.get(nid, {}).get("qualities", {})
            status = q.get("status", STATUS_PROMPT_ONLY)
            prompt_text = q.get("image_prompt", "")
            if status == STATUS_PROMPT_ONLY and not prompt_text:
                missing_prompts.append(nid)
            specs.append(
                PanelSpec(
                    panel_id=nid,
                    page_number=page_number[pid],
                    reading_index=idx,
                    status=status,
                    prompt_text=prompt_text,
                    prompt_layers=q.get("prompt_layers"),
                    dual_prompt=q.get("dual_prompt"),
                    spatial_layout=q.get("spatial_layout"),
                    compositional_intent=q.get("compositional_intent"),
                    aspect_ratio=q.get("aspect_ratio", "1:1"),
                    target_px={
                        "w": canvas_units_to_px(node.get("width", 0)),
                        "h": canvas_units_to_px(node.get("height", 0)),
                    },
                    characters=list(q.get("characters", [])),  # populated by H5 compose
                    seed=default_seed(comic_id, nid),
                    variant_count=variant_count,
                    output_dir=output_dir,
                    existing_image_path=node.get("file") if status == STATUS_RENDERED else None,
                    render_chain=[RenderStage(**vars(s)) for s in default_chain],
                )
            )
    if missing_prompts:
        raise ValueError(
            f"{canvas_path}: prompt_only panels missing image_prompt: {missing_prompts} "
            "(producer contract: every panel carries a non-empty image_prompt)"
        )

    manifest = RenderManifest(
        comic_id=comic_id,
        source_canvas=canvas_path.name,
        source_sync_hash=sync_hash,
        backend_policy={
            "default_chain": [
                {k: v for k, v in vars(s).items() if v is not None} for s in default_chain
            ],
            "allow_fallback": False,
        },
        budget_cap=budget_cap,
        register=register,
        panels=specs,
    )
    manifest.save(out_path)
    return manifest, out_path
