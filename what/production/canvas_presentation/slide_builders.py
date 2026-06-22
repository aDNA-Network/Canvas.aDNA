"""SlideBuilderMixin — 16 slide-type creation methods for PresentationBuilder.

Migrated from lattice-protocol/extensions/canvas/canvas_slide_builders.py.
Imports adjusted: substrate symbols from canvas_core, deck layout from
canvas_presentation.layout.

Populated in M-2a-01 (Phase 2a — Deck Application Extraction).
"""

from __future__ import annotations

from canvas_core import CanvasBuilder, VALID_ROLES, ImageFormat, PendingImage

from .layout import SlideLayout


class SlideBuilderMixin:
    """Mixin providing all slide creation methods for PresentationBuilder.

    Expects the host class to provide:
    - ``self._cb``: CanvasBuilder instance
    - ``self._slides``: list of slide metadata dicts
    - ``self._pending_images``: dict mapping id -> PendingImage
    - ``self._layout``: LayoutStrategy instance
    - ``self._slide_layout``: SlideLayout instance
    """

    def _slide_position(self, index: int) -> tuple[float, float]:
        return self._layout.slide_position(index)

    @staticmethod
    def _apply_role(cb: CanvasBuilder, node_id: str, role: str | None) -> None:
        if role is None:
            return
        if role not in VALID_ROLES:
            raise ValueError(f"Invalid role {role!r}. Valid roles: {sorted(VALID_ROLES)}")
        node = cb.get_node(node_id)
        if node:
            sa = node.setdefault("styleAttributes", {})
            sa["latticeRole"] = role

    # --- 1. Title ---

    def add_title_slide(self, title: str, subtitle: str | None = None,
                        color: str | None = None, role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        sw, sh = self._layout.slide_width, self._layout.slide_height
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy, width=sw, height=sh, color=color)
        title_node_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=title_node_id, text=f"# {title}",
                               x=sx + sl.margin_side, y=sy + int(sh * 0.18),
                               width=sl.content_width, height=200, text_align="center")
        self._apply_role(self._cb, title_node_id, role)
        nodes = [title_node_id]
        if subtitle:
            sub_id = CanvasBuilder.generate_id()
            sub_width = int(sl.content_width * 0.65)
            sub_x = sx + (sw - sub_width) // 2
            self._cb.add_text_node(id=sub_id, text=subtitle, x=sub_x, y=sy + int(sh * 0.41),
                                   width=sub_width, height=150, text_align="center")
            nodes.append(sub_id)
        self._slides.append({"id": slide_id, "type": "title", "title": title, "node_ids": nodes, "role": role})
        return slide_id

    # --- 2. Content ---

    def add_content_slide(self, title: str, body: str, color: str | None = None,
                          role: str | None = None, max_words: int | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy,
                           width=self._layout.slide_width, height=self._layout.slide_height, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        bp = sl.compute_stacked(1)[0]
        body_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=body_id, text=body, x=sx + bp.x, y=sy + bp.y,
                               width=int(bp.width), height=int(min(bp.height, 400)))
        self._apply_role(self._cb, body_id, role)
        self._slides.append({"id": slide_id, "type": "content", "title": title,
                             "node_ids": [heading_id, body_id], "role": role, "max_words": max_words})
        return slide_id

    # --- 3. Comparison ---

    def add_comparison_slide(self, title: str, left_label: str, left_content: str,
                             right_label: str, right_content: str,
                             color: str | None = None, role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy,
                           width=self._layout.slide_width, height=self._layout.slide_height, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        left_p, right_p = sl.compute_split(0.5)
        left_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=left_id, text=f"### {left_label}\n\n{left_content}",
                               x=sx + left_p.x, y=sy + left_p.y,
                               width=int(left_p.width), height=int(min(left_p.height, 400)))
        self._apply_role(self._cb, left_id, role)
        right_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=right_id, text=f"### {right_label}\n\n{right_content}",
                               x=sx + right_p.x, y=sy + right_p.y,
                               width=int(right_p.width), height=int(min(right_p.height, 400)), border="dashed")
        self._apply_role(self._cb, right_id, role)
        self._slides.append({"id": slide_id, "type": "comparison", "title": title,
                             "node_ids": [heading_id, left_id, right_id], "role": role})
        return slide_id

    # --- 4. Diagram ---

    @staticmethod
    def _mermaid_complexity(src: str) -> str:
        lines = [ln.strip() for ln in src.strip().split("\n") if ln.strip() and not ln.strip().startswith("%%")]
        n = len(lines)
        return "small" if n <= 5 else "medium" if n <= 15 else "large"

    def add_diagram_slide(self, title: str, diagram_file: str | None = None,
                          caption: str | None = None, color: str | None = None,
                          role: str | None = None, mermaid: str | None = None,
                          alt_text: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        sw, sh = self._layout.slide_width, self._layout.slide_height
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy, width=sw, height=sh, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        diagram_w = int(sl.content_width * 0.74)
        diagram_h = int(sl.body_height * 0.65)
        if mermaid:
            complexity = self._mermaid_complexity(mermaid)
            if complexity == "small":
                diagram_w = int(sl.content_width * 0.55)
                diagram_h = int(sl.body_height * 0.50)
            elif complexity == "large":
                diagram_w = int(sl.content_width * 0.90)
                diagram_h = int(sl.body_height * 0.80)
        diagram_x = sl.margin_side + (sl.content_width - diagram_w) // 2
        content_id = CanvasBuilder.generate_id()
        if mermaid:
            self._cb.add_text_node(id=content_id, text=f"```mermaid\n{mermaid}\n```",
                                   x=sx + diagram_x, y=sy + sl.body_top + 30,
                                   width=diagram_w, height=diagram_h)
        elif diagram_file:
            self._cb.add_file_node(id=content_id, file=diagram_file,
                                   x=sx + diagram_x, y=sy + sl.body_top + 30,
                                   width=diagram_w, height=diagram_h)
        else:
            raise ValueError("Either diagram_file or mermaid must be provided")
        nodes = [heading_id, content_id]
        self._apply_role(self._cb, content_id, role)
        if caption:
            cap_id = CanvasBuilder.generate_id()
            cap_w = int(sl.content_width * 0.74)
            cap_x = sl.margin_side + (sl.content_width - cap_w) // 2
            self._cb.add_text_node(id=cap_id, text=f"*{caption}*", x=sx + cap_x,
                                   y=sy + sl.body_top + 30 + diagram_h + 10,
                                   width=cap_w, height=100, text_align="center")
            nodes.append(cap_id)
        self._slides.append({"id": slide_id, "type": "diagram", "title": title,
                             "node_ids": nodes, "role": role, "alt_text": alt_text})
        if alt_text is None and hasattr(self, "_accessibility_warnings"):
            self._accessibility_warnings.append(f"Slide '{title}' (diagram) missing alt_text")
        return slide_id

    # --- 5. Image ---

    def add_image_slide(self, title: str, image_path: str | None = None,
                        image_url: str | None = None, prompt: str | None = None,
                        caption: str | None = None, color: str | None = None,
                        role: str | None = None, format: str | None = None,
                        background: bool = False, alt_text: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        sw, sh = self._layout.slide_width, self._layout.slide_height
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy, width=sw, height=sh, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        img_node_id = CanvasBuilder.generate_id()
        nodes = [heading_id, img_node_id]
        if background:
            img_w, img_h, img_x, img_y = sw, sh, 0, sy
        elif format:
            fmt_w, fmt_h = ImageFormat.get(format)
            scale = min(sl.content_width / fmt_w, sl.body_height * 0.8 / fmt_h)
            img_w, img_h = int(fmt_w * scale), int(fmt_h * scale)
            img_x = sl.margin_side + (sl.content_width - img_w) // 2
            img_y = sy + sl.body_top + 30
        else:
            img_w = int(sl.content_width * 0.74)
            img_h = int(sl.body_height * 0.65)
            img_x = sl.margin_side + (sl.content_width - img_w) // 2
            img_y = sy + sl.body_top + 30
        if image_path:
            self._cb.add_file_node(id=img_node_id, file=image_path,
                                   x=sx + img_x, y=img_y, width=img_w, height=img_h)
        elif image_url:
            self._cb.add_link_node(id=img_node_id, url=image_url,
                                   x=sx + img_x, y=img_y, width=img_w, height=img_h)
        elif prompt:
            target = f"how/presentations/{self._cb.name}/images/slide_{idx}.png"
            pending = PendingImage(id=img_node_id, prompt=prompt, target_path=target,
                                  slide_id=slide_id, format=format or "landscape_16_9")
            self._pending_images[img_node_id] = pending
            self._cb.add_text_node(id=img_node_id, text=f"[Pending Image]\n\n{prompt}",
                                   x=sx + img_x, y=img_y, width=img_w, height=img_h)
        else:
            self._cb.add_text_node(id=img_node_id, text="[No image specified]",
                                   x=sx + img_x, y=img_y, width=img_w, height=img_h)
        self._apply_role(self._cb, img_node_id, role)
        if caption:
            cap_id = CanvasBuilder.generate_id()
            cap_w = int(sl.content_width * 0.74)
            cap_x = sl.margin_side + (sl.content_width - cap_w) // 2
            self._cb.add_text_node(id=cap_id, text=f"*{caption}*", x=sx + cap_x,
                                   y=sy + sl.body_top + 30 + img_h + 10,
                                   width=cap_w, height=100, text_align="center")
            nodes.append(cap_id)
        image_source = "url" if image_url else "vault" if image_path else "prompt" if prompt else "none"
        self._slides.append({"id": slide_id, "type": "image", "title": title, "node_ids": nodes,
                             "role": role, "alt_text": alt_text, "image_source": image_source})
        if alt_text is None and hasattr(self, "_accessibility_warnings"):
            self._accessibility_warnings.append(f"Slide '{title}' (image) missing alt_text")
        return slide_id

    # --- 6. Quote ---

    def add_quote_slide(self, title: str, quote: str, attribution: str | None = None,
                        color: str | None = None, role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        sw, sh = self._layout.slide_width, self._layout.slide_height
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy, width=sw, height=sh, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        quote_text = f"> {quote}"
        if attribution:
            quote_text += f"\n\n*\u2014 {attribution}*"
        quote_w = int(sl.content_width * 0.83)
        quote_x = (sw - quote_w) // 2
        quote_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=quote_id, text=quote_text, x=sx + quote_x, y=sy + int(sh * 0.23),
                               width=quote_w, height=350, text_align="center",
                               color=color or "6", shape="pill")
        self._apply_role(self._cb, quote_id, role)
        self._slides.append({"id": slide_id, "type": "quote", "title": title,
                             "node_ids": [heading_id, quote_id], "role": role})
        return slide_id

    # --- 7. Section Divider ---

    def add_section_divider(self, title: str, subtitle: str | None = None,
                            color: str | None = None, role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        sw, sh = self._layout.slide_width, self._layout.slide_height
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy, width=sw, height=sh, color=color or "3")
        title_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=title_id, text=f"# {title}", x=sx + sl.margin_side,
                               y=sy + int(sh * 0.27), width=sl.content_width, height=200,
                               text_align="center", color=color or "3")
        self._apply_role(self._cb, title_id, role)
        nodes = [title_id]
        if subtitle:
            sub_id = CanvasBuilder.generate_id()
            sub_w = int(sl.content_width * 0.74)
            sub_x = (sw - sub_w) // 2
            self._cb.add_text_node(id=sub_id, text=f"*{subtitle}*", x=sx + sub_x,
                                   y=sy + int(sh * 0.59), width=sub_w, height=100, text_align="center")
            nodes.append(sub_id)
        self._slides.append({"id": slide_id, "type": "section_divider", "title": title,
                             "node_ids": nodes, "role": role})
        return slide_id

    # --- 8. Stats ---

    def add_stats_slide(self, title: str, stats: list[tuple[str, str]],
                        color: str | None = None, role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        sw, sh = self._layout.slide_width, self._layout.slide_height
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy, width=sw, height=sh, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        capped = stats[:4]
        stat_placements = sl.compute_grid(len(capped), cols=len(capped))
        nodes = [heading_id]
        for j, (value, label) in enumerate(capped):
            sp = stat_placements[j]
            stat_id = CanvasBuilder.generate_id()
            self._cb.add_text_node(id=stat_id, text=f"# {value}\n\n*{label}*",
                                   x=sx + sp.x, y=sy + sp.y, width=int(sp.width),
                                   height=int(min(sp.height, 250)), text_align="center",
                                   shape="pill", color=color or "5")
            self._apply_role(self._cb, stat_id, role)
            nodes.append(stat_id)
        self._slides.append({"id": slide_id, "type": "stats", "title": title,
                             "node_ids": nodes, "role": role})
        return slide_id

    # --- 9. Video ---

    def add_video_slide(self, title: str, url: str, caption: str | None = None,
                        color: str | None = None, role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        sw, sh = self._layout.slide_width, self._layout.slide_height
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy, width=sw, height=sh, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        link_id = CanvasBuilder.generate_id()
        link_w = min(1000, sl.content_width - 80)
        link_h = int(link_w * 9 / 16)
        link_x = (sw - link_w) // 2
        link_y = sy + sl.body_top + 30
        self._cb.add_link_node(id=link_id, url=url, x=sx + link_x, y=link_y, width=link_w, height=link_h)
        self._apply_role(self._cb, link_id, role)
        nodes = [heading_id, link_id]
        if caption:
            cap_id = CanvasBuilder.generate_id()
            cap_w = int(sl.content_width * 0.74)
            cap_x = (sw - cap_w) // 2
            self._cb.add_text_node(id=cap_id, text=f"*{caption}*", x=sx + cap_x,
                                   y=sy + sl.body_top + 30 + link_h + 10,
                                   width=cap_w, height=100, text_align="center")
            nodes.append(cap_id)
        self._slides.append({"id": slide_id, "type": "video", "title": title,
                             "node_ids": nodes, "role": role})
        return slide_id

    # --- 10. Timeline ---

    def add_timeline_slide(self, title: str, events: list[tuple[str, str]],
                           color: str | None = None, role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        sw, sh = self._layout.slide_width, self._layout.slide_height
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy, width=sw, height=sh, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        capped = events[:6]
        n = len(capped)
        nodes = [heading_id]
        item_gap = 15
        item_w = (sl.content_width - (n - 1) * item_gap) // n
        event_y = sy + sl.body_top + 30
        for j, (label, desc) in enumerate(capped):
            event_x = sx + sl.margin_side + j * (item_w + item_gap)
            eid = CanvasBuilder.generate_id()
            self._cb.add_text_node(id=eid, text=f"**{label}**\n\n{desc}", x=event_x, y=event_y,
                                   width=item_w, height=int(sl.body_height * 0.6),
                                   text_align="center", shape="pill", color=color or "4")
            nodes.append(eid)
        for j in range(len(nodes) - 2):
            self._cb.add_edge(id=CanvasBuilder.generate_id(), from_node=nodes[j + 1],
                              to_node=nodes[j + 2], from_side="right", to_side="left")
        self._slides.append({"id": slide_id, "type": "timeline", "title": title,
                             "node_ids": nodes, "role": role})
        return slide_id

    # --- 11. Process ---

    def add_process_slide(self, title: str, steps: list[str],
                          color: str | None = None, role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        sw, sh = self._layout.slide_width, self._layout.slide_height
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy, width=sw, height=sh, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        capped = steps[:6]
        n = len(capped)
        nodes = [heading_id]
        cols = min(3, n)
        step_placements = sl.compute_grid(n, cols=cols)
        for j, step_text in enumerate(capped):
            sp = step_placements[j]
            step_id = CanvasBuilder.generate_id()
            self._cb.add_text_node(id=step_id, text=f"**Step {j + 1}**\n\n{step_text}",
                                   x=sx + sp.x, y=sy + sp.y, width=int(sp.width),
                                   height=int(min(sp.height, 300)), color=color or "4")
            self._apply_role(self._cb, step_id, role)
            nodes.append(step_id)
        for j in range(len(nodes) - 2):
            self._cb.add_edge(id=CanvasBuilder.generate_id(), from_node=nodes[j + 1], to_node=nodes[j + 2])
        self._slides.append({"id": slide_id, "type": "process", "title": title,
                             "node_ids": nodes, "role": role})
        return slide_id

    # --- 12. Three Column ---

    def add_three_column_slide(self, title: str, columns: list[tuple[str, str]],
                               color: str | None = None, role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy,
                           width=self._layout.slide_width, height=self._layout.slide_height, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        col_placements = sl.compute_grid(3, cols=3)
        nodes = [heading_id]
        for j, (col_title, col_content) in enumerate(columns[:3]):
            cp = col_placements[j]
            col_id = CanvasBuilder.generate_id()
            self._cb.add_text_node(id=col_id, text=f"### {col_title}\n\n{col_content}",
                                   x=sx + cp.x, y=sy + cp.y,
                                   width=int(cp.width), height=int(min(cp.height, 500)))
            self._apply_role(self._cb, col_id, role)
            nodes.append(col_id)
        self._slides.append({"id": slide_id, "type": "three_column", "title": title,
                             "node_ids": nodes, "role": role})
        return slide_id

    # --- 13. Key Value ---

    def add_key_value_slide(self, title: str, pairs: list[tuple[str, str]],
                            color: str | None = None, role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy,
                           width=self._layout.slide_width, height=self._layout.slide_height, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        capped = pairs[:8]
        body_text = "\n\n".join(f"**{key}**: {value}" for key, value in capped)
        bp = sl.compute_stacked(1)[0]
        body_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=body_id, text=body_text, x=sx + bp.x, y=sy + bp.y,
                               width=int(bp.width), height=int(min(bp.height, 600)))
        self._apply_role(self._cb, body_id, role)
        self._slides.append({"id": slide_id, "type": "key_value", "title": title,
                             "node_ids": [heading_id, body_id], "role": role})
        return slide_id

    # --- 14. Matrix ---

    def add_matrix_slide(self, title: str, rows: list[str], cols: list[str],
                         cells: list[list[str]], color: str | None = None,
                         role: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy,
                           width=self._layout.slide_width, height=self._layout.slide_height, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        capped_rows = rows[:4]
        capped_cols = cols[:4]
        grid_rows = len(capped_rows) + 1
        grid_cols = len(capped_cols) + 1
        placements = sl.compute_grid(grid_rows * grid_cols, cols=grid_cols)
        nodes = [heading_id]
        for i in range(grid_rows):
            for j in range(grid_cols):
                cell_idx = i * grid_cols + j
                p = placements[cell_idx]
                cell_id = CanvasBuilder.generate_id()
                if i == 0 and j == 0:
                    text = ""
                elif i == 0:
                    text = f"**{capped_cols[j - 1]}**"
                elif j == 0:
                    text = f"**{capped_rows[i - 1]}**"
                else:
                    r, c = i - 1, j - 1
                    text = cells[r][c] if r < len(cells) and c < len(cells[r]) else ""
                self._cb.add_text_node(id=cell_id, text=text, x=sx + p.x, y=sy + p.y,
                                       width=int(p.width), height=int(min(p.height, 200)),
                                       text_align="center")
                nodes.append(cell_id)
        self._apply_role(self._cb, heading_id, role)
        self._slides.append({"id": slide_id, "type": "matrix", "title": title,
                             "node_ids": nodes, "role": role})
        return slide_id

    # --- 15. Collage ---

    def add_collage_slide(self, title: str, hero_image: str, thumbnails: list[str],
                          caption: str | None = None, color: str | None = None,
                          role: str | None = None, alt_text: str | None = None) -> str:
        slide_id = CanvasBuilder.generate_id()
        idx = len(self._slides)
        sx, sy = self._slide_position(idx)
        sl = self._slide_layout
        sw, sh = self._layout.slide_width, self._layout.slide_height
        self._cb.add_group(id=slide_id, label=title, x=sx, y=sy, width=sw, height=sh, color=color)
        h = sl.heading()
        heading_id = CanvasBuilder.generate_id()
        self._cb.add_text_node(id=heading_id, text=f"## {title}", x=sx + h.x, y=sy + h.y,
                               width=int(h.width), height=int(h.height))
        hero_p, thumbs_p = sl.compute_asymmetric(golden=True)
        hero_id = CanvasBuilder.generate_id()
        self._cb.add_file_node(id=hero_id, file=hero_image, x=sx + hero_p.x, y=sy + hero_p.y,
                               width=int(hero_p.width), height=int(hero_p.height))
        self._apply_role(self._cb, hero_id, role)
        nodes = [heading_id, hero_id]
        capped = thumbnails[:6]
        if capped:
            thumb_gap = 10
            thumb_cols = min(2, len(capped))
            thumb_rows = (len(capped) + thumb_cols - 1) // thumb_cols
            thumb_w = (int(thumbs_p.width) - (thumb_cols - 1) * thumb_gap) // thumb_cols
            thumb_h = (int(thumbs_p.height) - (thumb_rows - 1) * thumb_gap) // thumb_rows
            for j, thumb_path in enumerate(capped):
                tr = j // thumb_cols
                tc = j % thumb_cols
                thumb_id = CanvasBuilder.generate_id()
                self._cb.add_file_node(id=thumb_id, file=thumb_path,
                                       x=sx + thumbs_p.x + tc * (thumb_w + thumb_gap),
                                       y=sy + thumbs_p.y + tr * (thumb_h + thumb_gap),
                                       width=thumb_w, height=thumb_h)
                nodes.append(thumb_id)
        self._slides.append({"id": slide_id, "type": "collage", "title": title,
                             "node_ids": nodes, "role": role, "alt_text": alt_text})
        if alt_text is None and hasattr(self, "_accessibility_warnings"):
            self._accessibility_warnings.append(f"Slide '{title}' (collage) missing alt_text")
        return slide_id

    # --- 16. Media (unified dispatcher) ---

    def add_media_slide(self, title: str, source: str | None = None,
                        caption: str | None = None, color: str | None = None,
                        role: str | None = None) -> str:
        if source is None:
            return self.add_image_slide(title, caption=caption, color=color, role=role)
        video_hosts = ("youtube.com", "youtu.be", "vimeo.com", "loom.com")
        if any(host in source.lower() for host in video_hosts):
            return self.add_video_slide(title, url=source, caption=caption, color=color, role=role)
        is_url = source.lower().startswith(("http://", "https://"))
        image_exts = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")
        if any(source.lower().endswith(ext) for ext in image_exts):
            if is_url:
                return self.add_image_slide(title, image_url=source, caption=caption, color=color, role=role)
            return self.add_image_slide(title, image_path=source, caption=caption, color=color, role=role)
        if is_url:
            return self.add_image_slide(title, image_url=source, caption=caption, color=color, role=role)
        return self.add_image_slide(title, prompt=source, caption=caption, color=color, role=role)
