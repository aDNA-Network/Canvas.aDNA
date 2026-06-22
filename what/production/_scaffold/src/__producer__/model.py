"""Substrate-free domain model — imports NO canvas_std (``test_model_neutrality.py`` AST-guards this).

Only this layer is allowed to be canvas-agnostic; ``consume.py`` is the only module that touches the substrate.
TODO(clone): define your domain dataclasses + a ``load_input`` that reads a YAML/JSON spec into them.
"""

from __future__ import annotations

from dataclasses import dataclass, field  # noqa: F401  (field is handy for tuple/list defaults)


@dataclass(frozen=True)
class ProducerInput:
    """TODO(clone): the domain input (e.g. ``Letter``, ``Post``). Keep it plain data — no canvas concepts."""

    title: str
    id: str
    version: str = "0.1.0"
    refs: tuple[str, ...] = ()
    # TODO(clone): add domain fields (e.g. body paragraphs, recipient, platform, panels...).


def load_input(path: str) -> ProducerInput:
    """TODO(clone): read a ``.yaml``/``.json`` spec into ``ProducerInput``.

    Use ``json`` / ``yaml`` here (imported locally); do NOT import ``canvas_std`` anywhere in this file.
    """
    raise NotImplementedError("TODO(clone): implement load_input()")
