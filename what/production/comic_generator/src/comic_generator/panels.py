"""Panel builders — map each ``Panel`` to an interior baseline canvas node + its ``image`` component entry.

The 2D-grid analog of ``document_generator.blocks`` / ``diagram_generator.diagrams``. Each ``Panel`` becomes a single
baseline node:
  * an already-rendered panel (``image_path`` set) -> a ``file`` node; ``qualities.status = "rendered"``;
  * an un-rendered panel -> a ``text`` placeholder ``**Panel <type>**\\n\\n<scene excerpt>``; ``status = "prompt_only"``.

In ``_reserved.component_types`` every panel is ``{class: "image", semantic_type: <panel_type>, degrades_to:
"file"|"text", qualities: {substrate: "raster", aspect_ratio, image_prompt: <assembled 6-layer text>,
spatial_layout?: <mermaid str>, status, ...}}``. The Mermaid shape/style/aspect ride ONLY in ``qualities`` — never on
the baseline node (so the canvas degrades cleanly; ``image`` is a §6 class, ``degrades_to`` ∈ baseline types).

The assembled prompt is built by ``prompt.generate_panel_prompt`` (the 6-layer pure function); the dual-prompt
concatenation (text + spatial grammar + PART-3) is recorded too via ``panel_layout.assemble_dual_prompt``. NEVER
renders an image — emits the PROMPT text as metadata. ``canvas_std`` is not imported here.

Component classes come from ``canvas_std.reserved.COMPONENT_CLASSES`` and every ``degrades_to`` is a baseline node type
(text/file/link/group). Geometry is supplied by ``layout.py``; this module fills the node payload + component entries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from comic_generator import panel_layout, prompt
from comic_generator.layout import Box
from comic_generator.model import Page, Panel, SpreadColorScript, SpreadStoryState

_SCENE_EXCERPT = 200  # chars of scene shown in a placeholder text node


@dataclass
class PanelBuild:
    nodes: list[dict[str, Any]]
    component_types: dict[str, dict[str, Any]] = field(default_factory=dict)
    panel_ids: list[str] = field(default_factory=list)  # in reading order (the page's Z-path)


def _placeholder_text(panel: Panel) -> str:
    body = panel.scene[:_SCENE_EXCERPT] if panel.scene else f"[{panel.panel_type} panel — no content set]"
    return f"**Panel {panel.panel_type}**\n\n{body}"


def build_panels(
    page: Page,
    pid: str,
    page_box: Box,
    boxes: list[Box],
    *,
    character_bible: dict[str, str],
    color_script: SpreadColorScript | None,
    story_state: SpreadStoryState | None,
    comic_default_style: str,
    rlhf_character_hints: dict[str, str] | None = None,
    rlhf_camera_nuances: dict[str, str] | None = None,
) -> PanelBuild:
    """Build the interior baseline nodes (one per ``Panel``) + their ``image`` component entries for one page.

    ``boxes`` are the per-panel boxes in page-local space (parallel to ``page.panels``); they are translated to
    absolute canvas coordinates against ``page_box``. ``pid`` is the page node id; panel node ids are ``{pid}_pN``.
    The assembled image PROMPT (6-layer) + the dual-prompt + the spatial layout (if any) ride in ``qualities``.
    """
    pb = PanelBuild(nodes=[])
    for n, (panel, lbox) in enumerate(zip(page.panels, boxes)):
        nid = f"{pid}_p{n}"
        abox = Box(lbox.x + page_box.x, lbox.y + page_box.y, lbox.w, lbox.h)

        # Assemble the panel's image PROMPT (text only — never a pixel) + the dual-prompt concatenation.
        ip = prompt.generate_panel_prompt(
            panel,
            page,
            character_bible=character_bible,
            color_script=color_script,
            story_state=story_state,
            comic_default_style=comic_default_style,
            rlhf_character_hints=rlhf_character_hints,
            rlhf_camera_nuances=rlhf_camera_nuances,
        )
        dual_prompt = panel_layout.assemble_dual_prompt(ip)

        quals: dict[str, Any] = {
            "substrate": "raster",
            "aspect_ratio": ip.aspect_ratio,
            "image_prompt": ip.text,
            "dual_prompt": dual_prompt,
            "panel_type": panel.panel_type,
        }
        if ip.mermaid_layout:
            quals["spatial_layout"] = ip.mermaid_layout
        if panel.compositional_intent:
            quals["compositional_intent"] = panel.compositional_intent

        if panel.image_path:
            pb.nodes.append({"id": nid, "type": "file", "file": panel.image_path, **abox.as_node()})
            degrades = "file"
            quals["status"] = "rendered"
        else:
            pb.nodes.append({"id": nid, "type": "text", "text": _placeholder_text(panel), **abox.as_node()})
            degrades = "text"
            quals["status"] = "prompt_only"

        pb.component_types[nid] = {
            "class": "image",
            "semantic_type": panel.panel_type,
            "degrades_to": degrades,
            "qualities": quals,
        }
        pb.panel_ids.append(nid)
    return pb
