"""The post generator: ``Post`` -> a v2.0.0-conformant, aDNA-Native social-post ``.canvas`` (single post or thread).

Single-surface, native-primary mapping (mirrors ``letter_generator``/``diagram_generator``). The whole post is ONE
``group`` node = ``post_root`` = the single canonical surface. Each panel's copy is an interior baseline ``text`` node
(``post{i}``); an optional image rides as a SEPARATE ``image``-class node (``img{i}`` — a baseline ``text`` placeholder
carrying the alt text, the prompt in ``qualities.image_prompt``). The producer NEVER renders (ComfyUI owns pixels, C8).

Edges (respect the A-5 acyclicity check — only ``sequence`` is acyclicity-checked):
  * thread reading order -> ``sequence`` chain ``post0 -> post1 -> ...`` (strictly linear, acyclic; ``isStartNode`` on
    ``post0``);
  * each image is tied to its post by an ``adjacency`` edge (spatial neighbour; cycles permitted, not that there are any).

Platform profile (advisory char budget + aspect) rides in ``component_types[post_root].qualities``; the bare
``{"profile": "post"}`` stays in ``semantic_bindings`` (A-4 safe). ``canvas_std`` is never mutated (C8).

Pipeline: assemble ``{name, version, nodes, edges}`` -> ``to_canvas`` -> enrich ``_reserved``.
"""

from __future__ import annotations

from typing import Any

from canvas_std import to_canvas

from post_generator import layout
from post_generator.model import Post, profile_for

ADNA_VERSION = "2.0.0"
ROOT_ID = "post_root"
PROFILE = "post"
SURFACE = "social_post"


def build_post(post: Post) -> dict[str, Any]:
    """Map a ``Post`` to a v2.0.0 aDNA-Native social-post ``.canvas`` document (a plain dict)."""
    prof = profile_for(post.platform)
    boxes, root_box = layout.stack(post.panels)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    component_types: dict[str, dict[str, Any]] = {}
    panel_link_edges: dict[str, dict[str, str]] = {}

    # The single canonical surface: a group enclosing the whole post/thread.
    nodes.append({"id": ROOT_ID, "type": "group", "label": post.title, **root_box.as_node()})
    component_types[ROOT_ID] = {
        "class": "panel",
        "semantic_type": "post",
        "degrades_to": "group",
        "qualities": {
            "platform": post.platform,
            "char_budget": prof["char_budget"],
            "aspect": prof["aspect"],
            "thread": post.is_thread,
        },
    }

    post_ids: list[str] = []
    for i, (panel, (post_box, img_box)) in enumerate(zip(post.panels, boxes)):
        pid = f"post{i}"
        nodes.append({"id": pid, "type": "text", "text": panel.text, **post_box.as_node()})
        component_types[pid] = {
            "class": "text",
            "semantic_type": "post_copy",
            "degrades_to": "text",
            "qualities": {"chars": len(panel.text)},
        }
        post_ids.append(pid)

        # Optional image: a separate image-class node carrying the PROMPT as metadata (no render).
        if panel.image_prompt and img_box is not None:
            iid = f"img{i}"
            nodes.append({"id": iid, "type": "text", "text": panel.alt or "(image)", **img_box.as_node()})
            component_types[iid] = {
                "class": "image",
                "semantic_type": "post_image",
                "degrades_to": "text",
                "qualities": {"image_prompt": panel.image_prompt, "alt": panel.alt, "aspect": prof["aspect"]},
            }
            aeid = f"adj{i}"
            edges.append({"id": aeid, "fromNode": pid, "toNode": iid, "fromSide": "right", "toSide": "left"})
            panel_link_edges[aeid] = {"kind": "adjacency"}

    # Thread chain: sequence between consecutive posts (linear, acyclic).
    for i in range(len(post_ids) - 1):
        seid = f"seq{i}"
        edges.append({"id": seid, "fromNode": post_ids[i], "toNode": post_ids[i + 1],
                      "fromSide": "bottom", "toSide": "top"})
        panel_link_edges[seid] = {"kind": "sequence"}

    source = {"name": post.id, "version": post.version, "nodes": nodes, "edges": edges}
    doc = to_canvas(source)

    # Advanced field set post-hoc (to_canvas does not carry source-only fields): mark the thread start.
    for out in doc["nodes"]:
        if out["id"] == "post0":
            out["isStartNode"] = True
            break

    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    reserved["adna_version"] = ADNA_VERSION
    reserved["conformance_level"] = "adna_native"
    reserved["component_types"] = component_types
    reserved["semantic_bindings"] = {"profile": PROFILE}
    reserved["panel_link"] = {
        "edges": panel_link_edges,
        "regions": {ROOT_ID: {"flow": "vertical", "pagination": "none", "surface": SURFACE}},
        "surfaces": [{"id": ROOT_ID, "role": "canonical"}],
    }
    reserved["context_object"] = {"id": post.id, "version": post.version, "refs": list(post.refs)}
    return doc
