"""Deck scoring — 24-criterion PresentationScoringMixin.

Migrated from lattice-protocol/extensions/canvas/canvas_scoring.py
(PresentationScoringMixin class, lines 190-1543).

Dataclass definitions (CriterionScore, CategoryScore, PresentationReport)
remain in canvas_core.scoring per ADR 001.  This module provides only the
scoring LOGIC as a mixin.

Review Ordering Contract (M-1-04, G6): review() calls
_apply_structural_fixes() before scoring.

Populated in M-2a-03 (Phase 2a — Deck Application Extraction).
"""

from __future__ import annotations

import re
import statistics
from typing import Any

from canvas_core import (
    CriterionScore,
    CategoryScore,
    PresentationReport,
    containment_check,
    detect_overlaps,
)
from canvas_core.design_tokens import check_wcag_aa, contrast_ratio as _cr

from .config_deck import (
    _WHITESPACE_TARGETS,
    THEME_PALETTES,
    MAX_SLIDES,
    MIN_SLIDES,
)


class PresentationScoringMixin:
    """Mixin providing 24-criterion scoring for PresentationBuilder.

    Categories: structural (S1-S5), content (C1-C5), design (D1-D5),
    storytelling (T1-T5), accessibility (A1-A4).

    Mixed into PresentationBuilder which provides: _slides, _audience,
    _arc, _cb, _density_multiplier, _pending_images, _review_history,
    _theme, _effective_word_limit, _compute_whitespace, _get_slide_text,
    _count_slide_words, auto_section, _apply_structural_fixes.
    """

    # ------------------------------------------------------------------ S --

    def _score_s1_slide_count(self) -> CriterionScore:
        n = len(self._slides)
        ranges = {"keynote": (8, 20), "pitch": (10, 14), "meeting": (5, 12),
                  "async": (6, 15), "reference": (5, 25)}
        aud_name = self._audience.name if self._audience else ""
        lo, hi = ranges.get(aud_name, (3, 15))
        issues: list[str] = []
        if lo <= n <= hi:
            score = 1.0
        elif n < lo:
            score = max(0.0, 1.0 - (lo - n) * 0.2)
            issues.append(f"Too few slides: {n} (target {lo}-{hi})")
        else:
            score = max(0.0, 1.0 - (n - hi) * 0.1)
            issues.append(f"Too many slides: {n} (target {lo}-{hi})")
        return CriterionScore(id="S1", name="Slide Count Appropriateness",
                              score=round(score, 2), weight=0.15, issues=issues)

    def _score_s2_navigation(self) -> CriterionScore:
        n = len(self._slides)
        issues: list[str] = []
        if n <= 1:
            return CriterionScore(id="S2", name="Navigation Completeness", score=1.0, weight=0.25)
        slide_ids = {s["id"] for s in self._slides}
        connected: set[str] = set()
        for edge in self._cb.edges:
            if edge["fromNode"] in slide_ids:
                connected.add(edge["fromNode"])
            if edge["toNode"] in slide_ids:
                connected.add(edge["toNode"])
        orphan_ratio = len(slide_ids - connected) / len(slide_ids)
        has_start = bool(self._cb._start_node)
        score = 0.7 * (1.0 - orphan_ratio) + 0.3 * (1.0 if has_start else 0.0)
        if orphan_ratio > 0:
            issues.append(f"Orphaned slides (no navigation edges): {slide_ids - connected}")
        if not has_start:
            issues.append("No startNode set")
        return CriterionScore(id="S2", name="Navigation Completeness",
                              score=round(score, 2), weight=0.25, issues=issues)

    def _score_s3_section_grouping(self) -> CriterionScore:
        n = len(self._slides)
        issues: list[str] = []
        dividers = [s for s in self._slides if s["type"] == "section_divider"]
        if not dividers:
            score = 1.0 if n <= 8 else 0.3
            if score < 1.0:
                issues.append(f"No section dividers in {n}-slide deck")
        else:
            sections: list[list[dict[str, Any]]] = []
            current: list[dict[str, Any]] = []
            for s in self._slides:
                if s["type"] == "section_divider":
                    if current:
                        sections.append(current)
                    current = []
                else:
                    current.append(s)
            if current:
                sections.append(current)
            if not sections:
                score = 1.0
            else:
                sizes = [len(sec) for sec in sections]
                evenness = 1.0 - (max(sizes) - min(sizes)) / max(max(sizes), 1)
                score = 0.5 + 0.5 * evenness
        return CriterionScore(id="S3", name="Section Grouping",
                              score=round(score, 2), weight=0.20, issues=issues)

    def _score_s4_start_node(self) -> CriterionScore:
        issues: list[str] = []
        start = self._cb._start_node
        if not start:
            if not self._slides:
                return CriterionScore(id="S4", name="Start Node Validity", score=1.0, weight=0.15)
            issues.append("No startNode set")
            return CriterionScore(id="S4", name="Start Node Validity", score=0.0, weight=0.15, issues=issues)
        slide_ids = [s["id"] for s in self._slides]
        if start not in slide_ids:
            return CriterionScore(id="S4", name="Start Node Validity", score=0.3, weight=0.15,
                                  issues=["startNode points to a non-slide node"])
        if start == slide_ids[0] and self._slides[0]["type"] == "title":
            return CriterionScore(id="S4", name="Start Node Validity", score=1.0, weight=0.15)
        if start == slide_ids[0]:
            return CriterionScore(id="S4", name="Start Node Validity", score=0.85, weight=0.15)
        return CriterionScore(id="S4", name="Start Node Validity", score=0.7, weight=0.15,
                              issues=["startNode is not the first slide"])

    def _score_s5_type_variety(self) -> CriterionScore:
        n = len(self._slides)
        if n < 4:
            return CriterionScore(id="S5", name="Slide Type Variety", score=1.0, weight=0.25)
        types_used = {s["type"] for s in self._slides} - {"title"}
        issues: list[str] = []
        if len(types_used) == 0:
            score, issues = 0.0, ["No non-title slide types used"]
        elif len(types_used) == 1:
            score, issues = 0.4, ["Low slide type variety"]
        elif len(types_used) == 2:
            score = 0.8
        else:
            score = 1.0
        return CriterionScore(id="S5", name="Slide Type Variety", score=score, weight=0.25, issues=issues)

    # ------------------------------------------------------------------ C --

    def _score_c1_word_density(self) -> CriterionScore:
        issues: list[str] = []
        penalties = 0.0
        total = 0
        for slide in self._slides:
            total += 1
            limit = self._effective_word_limit(slide["type"], slide.get("max_words"))
            words = sum(len(self._cb.get_node(nid).get("text", "").split())
                        for nid in slide.get("node_ids", [])
                        if self._cb.get_node(nid) and self._cb.get_node(nid).get("type") == "text")
            if words > limit:
                penalties += min((words - limit) / limit, 1.0)
                issues.append(f"Slide '{slide['title']}': {words} words (max {limit})")
            elif words < limit * 0.1 and slide["type"] not in ("title", "section_divider"):
                penalties += 0.5
                issues.append(f"Slide '{slide['title']}': only {words} words")
        score = max(0.0, 1.0 - penalties / max(total, 1))
        return CriterionScore(id="C1", name="Word Density Compliance",
                              score=round(score, 2), weight=0.20, issues=issues)

    def _score_c2_title_quality(self) -> CriterionScore:
        issues: list[str] = []
        scores: list[float] = []
        _vp = re.compile(r"\b(is|are|was|were|has|have|had|do|does|did|will|would|should|can|could|"
                         r"shall|may|might|must|need|get|make|build|create|drive|reduce|increase|"
                         r"improve|deliver|achieve|show|reveal|enable|transform|discover|accelerate|"
                         r"optimize|unlock)\b", re.IGNORECASE)
        _np = re.compile(r"\d")
        for slide in self._slides:
            if slide["type"] == "section_divider":
                continue
            title = slide.get("title", "")
            if not title or len(title.split()) <= 1:
                scores.append(0.0)
                issues.append(f"Missing or single-word title: '{title}'")
            elif _vp.search(title) or _np.search(title):
                scores.append(1.0)
            elif len(title.split()) >= 3:
                scores.append(0.7)
            else:
                scores.append(0.2)
                issues.append(f"Generic title: '{title}'")
        score = statistics.mean(scores) if scores else 1.0
        return CriterionScore(id="C2", name="Title Quality", score=round(score, 2), weight=0.20, issues=issues)

    def _score_c3_bullet_discipline(self) -> CriterionScore:
        issues: list[str] = []
        node_scores: list[float] = []
        for slide in self._slides:
            for nid in slide.get("node_ids", []):
                node = self._cb.get_node(nid)
                if not node or node.get("type") != "text":
                    continue
                bullets, max_depth = 0, 0
                for line in node.get("text", "").split("\n"):
                    stripped = line.lstrip()
                    if stripped.startswith("- ") or stripped.startswith("* "):
                        bullets += 1
                        max_depth = max(max_depth, (len(line) - len(stripped)) // 4 + 1)
                if bullets == 0:
                    continue
                ns = 0.3 if bullets > 8 or max_depth > 3 else 0.7 if bullets > 5 or max_depth > 2 else 1.0
                if ns < 1.0:
                    issues.append(f"Excessive bullets ({bullets}) or nesting ({max_depth}) in '{slide['title']}'")
                node_scores.append(ns)
        return CriterionScore(id="C3", name="Bullet Depth and Count",
                              score=round(statistics.mean(node_scores) if node_scores else 1.0, 2),
                              weight=0.20, issues=issues)

    def _score_c4_visual_ratio(self) -> CriterionScore:
        if not self._slides:
            return CriterionScore(id="C4", name="Content-to-Visual Ratio", score=1.0, weight=0.20)
        visual_count = sum(1 for s in self._slides if any(
            self._cb.get_node(nid) and self._cb.get_node(nid).get("type") in ("file", "link")
            for nid in s.get("node_ids", [])
        ) or s["type"] in ("image", "diagram", "collage"))
        ratio = visual_count / len(self._slides)
        targets = {"keynote": 0.40, "pitch": 0.30, "meeting": 0.15, "async": 0.10, "reference": 0.05}
        target = targets.get(self._audience.name if self._audience else "", 0.15)
        score = 1.0 if ratio >= target else (ratio / target if target > 0 else 1.0)
        issues = [f"Visual ratio {ratio:.0%} below target {target:.0%}"] if score < 0.8 else []
        return CriterionScore(id="C4", name="Content-to-Visual Ratio",
                              score=round(score, 2), weight=0.20, issues=issues)

    def _score_c5_info_hierarchy(self) -> CriterionScore:
        issues: list[str] = []
        violations, total_nodes = 0, 0
        for slide in self._slides:
            for nid in slide.get("node_ids", []):
                node = self._cb.get_node(nid)
                if not node or node.get("type") != "text":
                    continue
                levels = [len(l) - len(l.lstrip("#")) for l in node.get("text", "").split("\n")
                          if l.lstrip().startswith("#") and len(l.lstrip()) - len(l.lstrip().lstrip("#")) > 0]
                total_nodes += len(levels)
                for i in range(1, len(levels)):
                    if levels[i] > levels[i - 1] + 1:
                        violations += 1
                        issues.append(f"Heading jump in '{slide['title']}': h{levels[i-1]}->h{levels[i]}")
        score = max(0.0, 1.0 - violations / max(total_nodes, 1)) if total_nodes else 1.0
        return CriterionScore(id="C5", name="Information Hierarchy",
                              score=round(score, 2), weight=0.20, issues=issues)

    # ------------------------------------------------------------------ D --

    def _score_d1_whitespace(self) -> CriterionScore:
        issues: list[str] = []
        slide_scores: list[float] = []
        ws_shift = 0.0
        if self._audience:
            ws_shift = {"keynote": 0.10, "pitch": 0.05, "meeting": 0.0,
                        "async": -0.05, "reference": -0.10}.get(self._audience.name, 0.0)
        for slide in self._slides:
            ws = self._compute_whitespace(slide)
            targets = _WHITESPACE_TARGETS.get(slide["type"], (0.30, 0.60))
            lo = targets[0] * (2.0 - self._density_multiplier) + ws_shift
            hi = min(1.0, targets[1] * (2.0 - self._density_multiplier) + ws_shift)
            if lo <= ws <= hi:
                slide_scores.append(1.0)
            else:
                s = max(0.0, 1.0 - min(abs(ws - lo), abs(ws - hi)) * 3)
                slide_scores.append(s)
                if s < 0.8:
                    issues.append(f"Whitespace {ws:.0%} in '{slide['title']}' (target {lo:.0%}-{hi:.0%})")
        return CriterionScore(id="D1", name="Whitespace Ratio",
                              score=round(statistics.mean(slide_scores) if slide_scores else 1.0, 2),
                              weight=0.25, issues=issues)

    def _score_d2_color_coherence(self) -> CriterionScore:
        n = len(self._slides)
        colors_used: set[str] = set()
        slides_with_color = 0
        for slide in self._slides:
            node = self._cb.get_node(slide["id"])
            if node and node.get("color"):
                colors_used.add(node["color"])
                slides_with_color += 1
        consistency = 0.7 if 0 < slides_with_color < n else 1.0
        issues: list[str] = []
        if 0 < slides_with_color < n:
            issues.append("Inconsistent colors: some slides colored, some not")
        nc = len(colors_used)
        if nc <= 3:
            score = consistency
        elif nc <= 5:
            score = 0.8 * consistency
        else:
            score = max(0.2, 0.5 * consistency)
            issues.append(f"Too many colors ({nc})")
        return CriterionScore(id="D2", name="Color Coherence",
                              score=round(score, 2), weight=0.20, issues=issues)

    def _check_pacing(self) -> float:
        if len(self._slides) < 4:
            return 0.0
        max_run, current_run = 1, 1
        for i in range(1, len(self._slides)):
            if self._slides[i]["type"] == self._slides[i - 1]["type"]:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 1
        return 0.3 if max_run >= 5 else 0.15 if max_run >= 4 else 0.0

    def _score_d3_visual_weight_sequence(self) -> CriterionScore:
        if len(self._slides) < 3:
            return CriterionScore(id="D3", name="Visual Weight Sequencing", score=1.0, weight=0.15)
        weights = []
        for slide in self._slides:
            na, wc = 0.0, 0
            for nid in slide.get("node_ids", []):
                node = self._cb.get_node(nid)
                if node:
                    na += node.get("width", 0) * node.get("height", 0)
                    if node.get("type") == "text":
                        wc += len(node.get("text", "").split())
            weights.append(na + wc * 100)
        avg = statistics.mean(weights)
        if avg <= 0:
            return CriterionScore(id="D3", name="Visual Weight Sequencing", score=1.0, weight=0.15)
        std = statistics.stdev(weights) if len(weights) >= 2 else 0.0
        variation = std / avg
        score = 1.0 if variation > 0.25 else 0.7 if variation > 0.15 else 0.4
        issues: list[str] = []
        if score < 0.7:
            issues.append("Visual weight too monotone")
        pacing = self._check_pacing()
        if pacing > 0:
            score = max(0.0, score - pacing)
            issues.append("Monotonous slide sequence")
        return CriterionScore(id="D3", name="Visual Weight Sequencing",
                              score=round(score, 2), weight=0.15, issues=issues)

    def _score_d4_image_text_balance(self) -> CriterionScore:
        issues: list[str] = []
        balance_scores: list[float] = []
        for slide in self._slides:
            img_area, text_area, has_img, has_text = 0.0, 0.0, False, False
            for nid in slide.get("node_ids", []):
                node = self._cb.get_node(nid)
                if not node:
                    continue
                area = node.get("width", 0) * node.get("height", 0)
                if node.get("type") in ("file", "link"):
                    img_area += area; has_img = True
                elif node.get("type") == "text":
                    text_area += area; has_text = True
            if not (has_img and has_text):
                continue
            total = img_area + text_area
            if total <= 0:
                continue
            ir = img_area / total
            if 0.30 <= ir <= 0.70:
                balance_scores.append(1.0)
            else:
                s = max(0.0, 1.0 - min(abs(ir - 0.30), abs(ir - 0.70)) * 3)
                balance_scores.append(s)
                if s < 0.8:
                    issues.append(f"Image-text imbalance in '{slide['title']}': {ir:.0%}")
        return CriterionScore(id="D4", name="Image-Text Balance",
                              score=round(statistics.mean(balance_scores) if balance_scores else 1.0, 2),
                              weight=0.20, issues=issues)

    def _score_d5_typography_consistency(self) -> CriterionScore:
        issues: list[str] = []
        type_map: dict[str, int] = {}
        violations, total = 0, 0
        for slide in self._slides:
            if not slide.get("node_ids"):
                continue
            node = self._cb.get_node(slide["node_ids"][0])
            if not node or node.get("type") != "text":
                continue
            fl = node.get("text", "").split("\n")[0].lstrip()
            if not fl.startswith("#"):
                continue
            level = len(fl) - len(fl.lstrip("#"))
            total += 1
            stype = slide["type"]
            if stype in type_map:
                if type_map[stype] != level:
                    violations += 1
                    issues.append(f"Inconsistent heading in '{stype}': h{type_map[stype]} vs h{level}")
            else:
                type_map[stype] = level
        return CriterionScore(id="D5", name="Typography Consistency",
                              score=round(max(0.0, 1.0 - violations / max(total, 1)), 2),
                              weight=0.20, issues=issues)

    # ------------------------------------------------------------------ T --

    def _score_t1_narrative_arc(self) -> CriterionScore:
        if not self._slides:
            return CriterionScore(id="T1", name="Narrative Arc Compliance", score=0.0, weight=0.25, issues=["No slides"])
        if self._arc is not None:
            return self._score_t1_arc_aware()
        n = len(self._slides)
        setup_types = {"title", "section_divider"}
        contrast_types = {"content", "comparison", "stats", "process", "diagram", "timeline", "three_column", "matrix"}
        resolution_types = {"content", "stats", "key_value", "quote"}
        has_setup = any(s["type"] in setup_types for s in self._slides[:max(2, n // 3)])
        mid_s, mid_e = max(1, n // 4), max(2, 3 * n // 4)
        has_contrast = any(s["type"] in contrast_types for s in self._slides[mid_s:mid_e])
        has_resolution = any(s["type"] in resolution_types for s in self._slides[max(0, n - max(2, n // 3)):])
        phases = sum([has_setup, has_contrast, has_resolution])
        score = {3: 1.0, 2: 0.6, 1: 0.3}.get(phases, 0.0)
        issues = []
        if score < 1.0:
            missing = [x for x, h in [("setup", has_setup), ("contrast", has_contrast), ("resolution", has_resolution)] if not h]
            issues.append(f"Missing narrative phases: {', '.join(missing)}")
        return CriterionScore(id="T1", name="Narrative Arc Compliance", score=score, weight=0.25, issues=issues)

    def _score_t1_arc_aware(self) -> CriterionScore:
        assert self._arc is not None
        sections = self._arc.sections
        slide_idx, matched = 0, 0
        matched_names: list[str] = []
        for section in sections:
            while slide_idx < len(self._slides):
                if self._slides[slide_idx]["type"] in section.slide_types or self._slides[slide_idx]["type"] == "content":
                    matched += 1
                    matched_names.append(section.name)
                    slide_idx += 1
                    break
                slide_idx += 1
        score = matched / len(sections) if sections else 1.0
        missing = [s.name for s in sections if s.name not in matched_names]
        issues = [f"Missing arc sections: {', '.join(missing)}"] if missing else []
        return CriterionScore(id="T1", name="Narrative Arc Compliance",
                              score=round(score, 2), weight=0.25, issues=issues)

    def _score_t2_opening_impact(self) -> CriterionScore:
        if not self._slides:
            return CriterionScore(id="T2", name="Opening Impact", score=0.0, weight=0.15, issues=["No slides"])
        if self._slides[0]["type"] != "title":
            return CriterionScore(id="T2", name="Opening Impact", score=0.3, weight=0.15,
                                  issues=[f"Opens with '{self._slides[0]['type']}' — use title slide"])
        if len(self._slides) < 2:
            return CriterionScore(id="T2", name="Opening Impact", score=0.7, weight=0.15)
        engaging = {"content", "image", "stats", "quote"}
        score = 1.0 if self._slides[1]["type"] in engaging else 0.5 if self._slides[1]["type"] == "section_divider" else 0.7
        return CriterionScore(id="T2", name="Opening Impact", score=score, weight=0.15)

    def _score_t3_star_moment(self) -> CriterionScore:
        star_count = 0
        for slide in self._slides:
            if slide.get("role") == "critical" or slide["type"] == "quote":
                star_count += 1
            elif slide["type"] == "stats":
                text = self._get_slide_text(slide)
                if re.search(r"\d+[%x×]|\d+\.\d+x", text):
                    star_count += 1
            elif slide["type"] in ("image", "collage") and self._count_slide_words(slide) < 15:
                star_count += 1
        score = 1.0 if star_count >= 2 else 0.7 if star_count == 1 else 0.0
        issues = [] if star_count >= 2 else ["Only one STAR moment" if star_count == 1 else "No STAR moment"]
        return CriterionScore(id="T3", name="STAR Moment Presence", score=score, weight=0.20, issues=issues)

    def _score_t4_audience_density(self) -> CriterionScore:
        if not self._slides:
            return CriterionScore(id="T4", name="Audience-Density Alignment", score=1.0, weight=0.20)
        avg_words = statistics.mean([self._count_slide_words(s) for s in self._slides])
        expectations = {"keynote": (10, 25), "pitch": (20, 50), "meeting": (40, 80),
                        "async": (60, 120), "reference": (80, 150)}
        lo, hi = expectations.get(self._audience.name if self._audience else "", (30, 80))
        issues: list[str] = []
        if lo <= avg_words <= hi:
            score = 1.0
        elif avg_words < lo:
            score = max(0.0, 1.0 - (lo - avg_words) / max(lo, 1))
            issues.append(f"Average {avg_words:.0f} words below {lo}-{hi}")
        else:
            score = max(0.0, 1.0 - (avg_words - hi) / max(hi, 1))
            issues.append(f"Average {avg_words:.0f} words above {lo}-{hi}")
        return CriterionScore(id="T4", name="Audience-Density Alignment",
                              score=round(score, 2), weight=0.20, issues=issues)

    def _score_cta_slide(self, slide: dict[str, Any]) -> float:
        text = self._get_slide_text(slide).lower()
        cta_verbs = {"join", "try", "start", "contact", "visit", "sign up", "get started",
                     "schedule", "book", "download", "explore", "register", "apply", "demo",
                     "request", "subscribe", "reach out"}
        contact_patterns = {"@", "http", ".com", ".io", ".org", "linkedin", "github"}
        if any(v in text for v in cta_verbs) or any(p in text for p in contact_patterns):
            return 1.0
        if re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text):
            return 1.0
        if any(w in text for w in ("takeaway", "summary", "recap", "key point", "remember")):
            return 0.7
        if any(g in text for g in ("thank you", "thanks", "questions", "q&a")):
            return 0.3
        return 0.0

    def _score_t5_closing_cta(self) -> CriterionScore:
        if not self._slides:
            return CriterionScore(id="T5", name="Closing Call-to-Action", score=0.0, weight=0.20, issues=["No slides"])
        last_score = self._score_cta_slide(self._slides[-1])
        if last_score < 1.0 and len(self._slides) >= 2:
            pen = self._score_cta_slide(self._slides[-2])
            if pen >= 1.0 and last_score >= 0.3:
                last_score = 0.85
        issues = [] if last_score >= 0.7 else (["Generic closing — add CTA"] if last_score > 0 else ["No closing signal"])
        return CriterionScore(id="T5", name="Closing Call-to-Action", score=last_score, weight=0.20, issues=issues)

    # ------------------------------------------------------------------ A --

    def _score_a1_alt_text(self) -> CriterionScore:
        visual = [s for s in self._slides if s["type"] in ("image", "diagram", "collage")]
        if not visual:
            return CriterionScore(id="A1", name="Alt Text Coverage", score=1.0, weight=0.35)
        covered = sum(1 for s in visual if s.get("alt_text"))
        score = covered / len(visual)
        issues = [f"Missing alt text: {len(visual) - covered} visual slide(s)"] if covered < len(visual) else []
        return CriterionScore(id="A1", name="Alt Text Coverage", score=round(score, 2), weight=0.35, issues=issues)

    def _score_a2_heading_hierarchy(self) -> CriterionScore:
        issues: list[str] = []
        jumps = 0
        for slide in self._slides:
            for nid in slide.get("node_ids", []):
                node = self._cb.get_node(nid)
                if not node or node.get("type") != "text":
                    continue
                levels = [len(l) - len(l.lstrip("#")) for l in node.get("text", "").split("\n")
                          if l.lstrip().startswith("#") and len(l.lstrip()) - len(l.lstrip().lstrip("#")) > 0]
                for i in range(len(levels) - 1):
                    if levels[i + 1] - levels[i] > 1:
                        jumps += 1
                        issues.append(f"Heading jump in '{slide['title']}': h{levels[i]}->h{levels[i+1]}")
                        break
        return CriterionScore(id="A2", name="Heading Hierarchy",
                              score=round(1.0 if jumps == 0 else max(0.0, 1.0 - jumps * 0.25), 2),
                              weight=0.20, issues=issues)

    def _score_a3_text_density_ceiling(self) -> CriterionScore:
        if not self._slides:
            return CriterionScore(id="A3", name="Text Density Ceiling", score=1.0, weight=0.20)
        expectations = {"keynote": 50, "pitch": 100, "meeting": 160, "async": 240, "reference": 300}
        ceiling = expectations.get(self._audience.name if self._audience else "", 200)
        issues: list[str] = []
        violations = sum(1 for s in self._slides if self._count_slide_words(s) > ceiling)
        if violations:
            issues.append(f"{violations} slide(s) exceed {ceiling}-word ceiling")
        return CriterionScore(id="A3", name="Text Density Ceiling",
                              score=round(1.0 if violations == 0 else max(0.0, 1.0 - violations / len(self._slides)), 2),
                              weight=0.20, issues=issues)

    def _score_a4_contrast(self) -> CriterionScore:
        theme_name = self._theme.name if hasattr(self, "_theme") and self._theme else ""
        palette = THEME_PALETTES.get(theme_name)
        if palette is None:
            return CriterionScore(id="A4", name="Contrast (WCAG AA)", score=1.0, weight=0.25,
                                  suggestions=["No theme palette — contrast not checked"])
        pairs = [("text", palette.text, palette.bg), ("text_dim", palette.text_dim, palette.bg),
                 ("text", palette.text, palette.bg_lighter), ("text_dim", palette.text_dim, palette.bg_lighter)]
        failures = sum(1 for _, fg, bg in pairs if not check_wcag_aa(fg, bg, large_text=True))
        issues = [f"{label} ({fg}) on {bg}: {_cr(fg, bg):.1f}:1 fails WCAG AA"
                  for label, fg, bg in pairs if not check_wcag_aa(fg, bg, large_text=True)]
        return CriterionScore(id="A4", name="Contrast (WCAG AA)",
                              score=round(1.0 if failures == 0 else max(0.0, 1.0 - failures / len(pairs)), 2),
                              weight=0.25, issues=issues)

    # ---------------------------------------------------------------- Gates --

    def _run_hard_gates(self) -> list[str]:
        gate_issues: list[str] = []
        unresolved = [p for p in self._pending_images.values() if p.status == "pending"]
        if unresolved:
            gate_issues.append(f"Unresolved pending images: {len(unresolved)}")
        for slide in self._slides:
            interior = [self._cb.get_node(nid) for nid in slide.get("node_ids", [])
                        if self._cb.get_node(nid) is not None]
            if interior:
                if detect_overlaps(interior):
                    gate_issues.append(f"Overlapping nodes in '{slide['title']}'")
                group = self._cb.get_node(slide["id"])
                if group and containment_check(group, interior):
                    gate_issues.append(f"Nodes outside parent in '{slide['title']}'")
        return gate_issues

    # -------------------------------------------------------------- Review --

    def review(self) -> PresentationReport:
        """Review presentation quality across 5 categories, 24 weighted criteria.

        Per M-1-04 G6 Review Ordering Contract: structural fixes run first.
        """
        if self._slides:
            self._apply_structural_fixes()

        categories = {
            "structural": CategoryScore(name="structural", criteria=[
                self._score_s1_slide_count(), self._score_s2_navigation(),
                self._score_s3_section_grouping(), self._score_s4_start_node(),
                self._score_s5_type_variety(),
            ]),
            "content": CategoryScore(name="content", criteria=[
                self._score_c1_word_density(), self._score_c2_title_quality(),
                self._score_c3_bullet_discipline(), self._score_c4_visual_ratio(),
                self._score_c5_info_hierarchy(),
            ]),
            "design": CategoryScore(name="design", criteria=[
                self._score_d1_whitespace(), self._score_d2_color_coherence(),
                self._score_d3_visual_weight_sequence(), self._score_d4_image_text_balance(),
                self._score_d5_typography_consistency(),
            ]),
            "storytelling": CategoryScore(name="storytelling", criteria=[
                self._score_t1_narrative_arc(), self._score_t2_opening_impact(),
                self._score_t3_star_moment(), self._score_t4_audience_density(),
                self._score_t5_closing_cta(),
            ]),
            "accessibility": CategoryScore(name="accessibility", criteria=[
                self._score_a1_alt_text(), self._score_a2_heading_hierarchy(),
                self._score_a3_text_density_ceiling(), self._score_a4_contrast(),
            ]),
        }

        gate_issues = self._run_hard_gates()
        cat_scores = [cat.weighted_score for cat in categories.values()]
        score = statistics.mean(cat_scores) if cat_scores else 0.0
        all_issues = list(gate_issues)
        for cat in categories.values():
            for c in cat.criteria:
                all_issues.extend(c.issues)

        suggestions = self._generate_suggestions(categories)
        report = PresentationReport(score=round(score, 2), issues=all_issues,
                                    categories=categories, suggestions=suggestions)
        self._review_history.append(report)
        return report

    def _generate_suggestions(self, categories: dict[str, CategoryScore]) -> list[str]:
        suggestions: list[str] = []
        for name, cat in categories.items():
            if cat.weighted_score < 0.5:
                suggestions.append(f"Priority: {name.title()} needs attention ({cat.weighted_score:.0%})")
        for cat in categories.values():
            for c in cat.criteria:
                if c.status == "fail":
                    suggestions.extend(c.suggestions)
        n = len(self._slides)
        if n < MIN_SLIDES:
            suggestions.append(f"Add {MIN_SLIDES - n} more slide(s)")
        if n > MAX_SLIDES:
            suggestions.append("Consider consolidating slides")
        if n >= 5 and len({s["type"] for s in self._slides}) <= 2:
            suggestions.append("Mix slide types for engagement")
        if self._slides and self._slides[0]["type"] != "title":
            suggestions.append("Start with a title slide")
        return suggestions

    @property
    def review_history(self) -> list[PresentationReport]:
        return list(self._review_history)

    def score_delta(self) -> float | None:
        if len(self._review_history) < 2:
            return None
        return self._review_history[-1].score - self._review_history[-2].score

    def suggest(self) -> list[str]:
        return self.review().suggestions
