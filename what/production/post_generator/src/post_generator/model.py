"""Substrate-free domain model — a social post (single or thread). Imports NO ``canvas_std`` (AST-guarded).

A ``Post`` is plain data: a platform key + an ordered tuple of ``PostPanel`` (1 = single post, N = thread). Each panel
carries the post copy and an optional **image prompt** (a prompt, never a rendered file). ``PLATFORM_PROFILES`` is a
producer-side table of advisory character budgets + aspect hints (never registered in ``canvas_std.schema``).
``load_post`` reads a ``.yaml``/``.json`` spec.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Producer-side platform profiles (advisory char budgets + aspect hints). Extend freely — this is producer-side.
PLATFORM_PROFILES: dict[str, dict[str, Any]] = {
    "twitter": {"char_budget": 280, "aspect": "16:9"},
    "x": {"char_budget": 280, "aspect": "16:9"},
    "linkedin": {"char_budget": 3000, "aspect": "1.91:1"},
    "instagram": {"char_budget": 2200, "aspect": "1:1"},
}
DEFAULT_PROFILE: dict[str, Any] = {"char_budget": 0, "aspect": "1:1"}


def profile_for(platform: str) -> dict[str, Any]:
    """Return the advisory profile for ``platform`` (case-insensitive); a permissive default for unknown platforms."""
    return PLATFORM_PROFILES.get(platform.lower(), DEFAULT_PROFILE)


@dataclass(frozen=True)
class PostPanel:
    """One post in a single-post-or-thread. ``image_prompt`` is a prompt (ComfyUI renders later), not a file."""

    text: str
    image_prompt: str = ""
    alt: str = ""


@dataclass(frozen=True)
class Post:
    """A social post: one platform + an ordered tuple of panels (1 = single, N = thread)."""

    title: str
    id: str
    platform: str = "twitter"
    version: str = "0.1.0"
    panels: tuple[PostPanel, ...] = ()
    refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.title:
            raise ValueError("Post.title must be non-empty")
        if not self.id:
            raise ValueError("Post.id must be non-empty")
        if not self.panels:
            raise ValueError("Post must have at least one panel")

    @property
    def is_thread(self) -> bool:
        return len(self.panels) > 1

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Post:
        raw = d.get("panels")
        if raw is None:
            # single-panel shorthand: a top-level `text` (+ optional image_prompt/alt)
            raw = [{"text": d["text"], "image_prompt": d.get("image_prompt", ""), "alt": d.get("alt", "")}] \
                if "text" in d else []
        panels = tuple(
            PostPanel(
                text=str(p["text"]),
                image_prompt=str(p.get("image_prompt", "")),
                alt=str(p.get("alt", "")),
            )
            for p in raw
        )
        return cls(
            title=str(d["title"]),
            id=str(d["id"]),
            platform=str(d.get("platform", "twitter")),
            version=str(d.get("version", "0.1.0")),
            panels=panels,
            refs=tuple(str(r) for r in d.get("refs", [])),
        )


def load_post(path: str | Path) -> Post:
    """Load a post from ``.yaml``/``.yml`` (PyYAML) or ``.json``. Imports no ``canvas_std``."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        import yaml

        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"post input {p} did not parse to a mapping")
    return Post.from_dict(data)
