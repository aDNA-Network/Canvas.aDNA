"""Shared fixtures — a single post + a thread (with one image) + the default built canvas doc (the thread)."""

from __future__ import annotations

import pytest

from post_generator.consume import build_post
from post_generator.model import Post, PostPanel


@pytest.fixture
def single_post() -> Post:
    return Post(
        title="Single post — Canvas.aDNA",
        id="urn:adna:canvas:post:single",
        platform="twitter",
        panels=(PostPanel(text="A canvas reduces any 2D output to a grid of typed components. Fork, don't drift."),),
        refs=("[[spec_adna_canvas_standard]]",),
    )


@pytest.fixture
def thread() -> Post:
    return Post(
        title="Thread — the canvas grammar",
        id="urn:adna:canvas:post:thread",
        platform="linkedin",
        panels=(
            PostPanel(text="1/ A canvas is a near-universal output primitive: typed components on a surface."),
            PostPanel(
                text="2/ Decks, comics, documents, diagrams, letters, posts — one producer pipeline.",
                image_prompt="a Mondrian grid of primary-color rectangles forming media panels",
                alt="a grid of primary-color panels, Mondrian style",
            ),
            PostPanel(text="3/ aDNA-native canvases degrade to plain Obsidian canvases. Fork, don't drift."),
        ),
        refs=("[[spec_federation_contract]]",),
    )


@pytest.fixture
def post(thread: Post) -> Post:
    return thread


@pytest.fixture
def doc(post: Post) -> dict:
    return build_post(post)
