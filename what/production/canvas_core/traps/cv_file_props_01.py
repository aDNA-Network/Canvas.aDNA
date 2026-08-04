"""CV-FILE-PROPS-01 — file-node target resolution + embed rendering reality.

An Obsidian file card renders: a header bar carrying the filename, then the
target's own markdown — the H1 at 2.3em, and (unless the vault sets
``propertiesInDocument: "hidden"``) a YAML **Properties table** ahead of any
content. A card sized for body text therefore clips its own title and reads
as a rendering bug; a frontmatter-bearing target renders as ~80% Properties
table (the Oration M-R5 failure mode).

``html_renderer.py`` models file nodes as image-or-placeholder only and is
**blind to this by construction** — no amount of scoring the HTML render will
catch it, which is why this trap checks statically.

Conditions:
  (a) **file_missing** — the target path does not exist (high).
  (b) **title_clips** — the embed header + the target's H1 alone exceed the
      card's usable height: the title itself clips (high).
  (c) **content_hidden** — the H1 renders but no content line follows
      (medium; reads as "there's more, click through" — often acceptable).
  (d) **properties_exposed** — >= 1 targeted file carries YAML frontmatter
      while the vault's ``.obsidian/app.json`` does not set
      ``propertiesInDocument: "hidden"`` — cards render Properties tables
      instead of content (high; one finding listing the affected nodes).

Requires ``vault_root`` (threaded via ``run_all_traps(**trap_kwargs)`` or the
``canvas-visual-check --vault-root`` flag) to resolve ``file`` paths; returns
``[]`` when absent rather than guessing.

New in Halftone HV (2026-08-03). Substrate-neutral — zero application imports.
"""

from __future__ import annotations

import json
import math
import os

from ..text_metrics import (
    OBSIDIAN_BODY_LINE,
    OBSIDIAN_EMBED_HEADER,
    OBSIDIAN_H1_FACTOR,
    OBSIDIAN_H1_LINE,
    OBSIDIAN_SAFE_FILL,
    _strip_markdown,
    obsidian_chars_per_line,
)
from . import TrapFinding

TRAP_ID = "CV-FILE-PROPS-01"

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _has_frontmatter(path: str) -> bool:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.readline().strip() == "---"
    except OSError:
        return False


def _embed_body(path: str) -> tuple[str | None, str | None]:
    """Return ``(h1_text, first_content_block)`` as an Obsidian embed shows them."""
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except OSError:
        return None, None
    i = 0
    if lines and lines[0].strip() == "---":  # skip frontmatter
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    h1, first = None, None
    for line in lines[i:]:
        s = line.strip()
        if not s:
            continue
        if h1 is None:
            if s.startswith("# "):
                h1 = _strip_markdown(s).strip()
                continue
            h1 = ""
            first = _strip_markdown(s).strip()
            break
        first = _strip_markdown(s).strip()
        break
    return h1, first


def _file_card_required(path: str, width: float) -> tuple[float, float, str] | None:
    """Height an embed needs for header + full H1 (+ first content line)."""
    h1, first = _embed_body(path)
    if h1 is None:
        return None
    need_title = OBSIDIAN_EMBED_HEADER
    if h1:
        need_title += (
            math.ceil(len(h1) / obsidian_chars_per_line(width, OBSIDIAN_H1_FACTOR))
            * OBSIDIAN_H1_LINE
        )
    need_full = need_title + (
        math.ceil(len(first) / obsidian_chars_per_line(width)) * OBSIDIAN_BODY_LINE
        if first else 0.0
    )
    return need_title, need_full, h1


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
    vault_root: str | os.PathLike | None = None,
) -> list[TrapFinding]:
    """Run CV-FILE-PROPS-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating (severity +1).
        vault_root: Vault root directory for resolving file-node paths and
            reading ``.obsidian/app.json``. **Required** — the trap returns
            ``[]`` (skips) when absent.

    Returns:
        List of :class:`TrapFinding` instances (may be empty).
    """
    if vault_root is None:
        return []
    root = os.fspath(vault_root)

    file_nodes = [
        n for n in canvas_data.get("nodes", [])
        if n.get("type") == "file" and n.get("file")
    ]
    if not file_nodes:
        return []

    props_hidden = False
    app_json = os.path.join(root, ".obsidian", "app.json")
    if os.path.isfile(app_json):
        try:
            with open(app_json, encoding="utf-8") as fh:
                props_hidden = json.load(fh).get("propertiesInDocument") == "hidden"
        except (OSError, ValueError):
            pass

    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()
    frontmatter_nodes: list[str] = []

    for node in file_nodes:
        node_id = node.get("id", "<unknown>")
        rel = node["file"]
        target = os.path.join(root, rel)
        if not os.path.isfile(target):
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="file_missing",
                node_ids=[node_id],
                severity="high",
                message=f"File node target does not exist: {rel}",
            ))
            continue

        if _has_frontmatter(target):
            frontmatter_nodes.append(node_id)

        width = float(node.get("width", 0))
        height = float(node.get("height", 0))
        if width <= 0 or height <= 0:
            continue
        card = _file_card_required(target, width)
        if card is None:
            continue
        need_title, need_full, h1 = card
        avail = OBSIDIAN_SAFE_FILL * height
        if need_title > avail:
            fix_h = math.ceil(need_title / OBSIDIAN_SAFE_FILL / 10) * 10
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="title_clips",
                node_ids=[node_id],
                severity="high",
                message=(
                    f"Target's H1 (\"{(h1 or '')[:40]}…\", {len(h1 or '')} chars) needs "
                    f"{need_title:.0f}px with the embed header but the card has "
                    f"{avail:.0f}px — the title itself clips. Set height >= {fix_h}"
                ),
            ))
        elif need_full > avail:
            fix_h = math.ceil(need_full / OBSIDIAN_SAFE_FILL / 10) * 10
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="content_hidden",
                node_ids=[node_id],
                severity="medium",
                message=(
                    f"H1 renders, but no content line follows (needs {need_full:.0f}px "
                    f"for title+first block, has {avail:.0f}px). Height {fix_h} "
                    f"would show content"
                ),
            ))

    if frontmatter_nodes and not props_hidden:
        findings.append(TrapFinding(
            trap_id=TRAP_ID,
            condition="properties_exposed",
            node_ids=frontmatter_nodes,
            severity="high",
            message=(
                f"{len(frontmatter_nodes)} file node(s) target files with YAML "
                f"frontmatter while .obsidian/app.json propertiesInDocument != "
                f"\"hidden\" — cards will render a Properties table instead of "
                f"content"
            ),
        ))

    if r11:
        for finding in findings:
            if any(nid in r11 for nid in finding.node_ids):
                finding.severity = _escalate_severity(finding.severity)

    return findings
