"""post_generator — a social-post producer on canvas_std (Operation Palette P3).

A ``Post`` (single post or thread) -> a v2.0.0 aDNA-Native social-post ``.canvas``. Image prompts ride as metadata;
the producer never renders (ComfyUI owns pixels). See ``how/skills/skill_canvas_producer_build.md``.
"""


def _ensure_canvas_core() -> None:
    """Guarded self-bootstrap for the unpackaged ``canvas_core`` (``comic_render`` precedent).

    ``canvas_core`` is a bare directory-package on the production shelf (no pyproject) — importable
    only with ``what/production/`` on ``sys.path``. Under pytest the pyproject ``pythonpath``
    covers it; under the console script (or a direct ``python -m``) this inserts the shelf root,
    resolved from this file's real location (editable installs preserve it).
    """
    import importlib.util
    import sys
    from pathlib import Path

    if importlib.util.find_spec("canvas_core") is not None:
        return
    shelf = Path(__file__).resolve().parents[3]  # src/<pkg> → src → <producer> → production
    if (shelf / "canvas_core" / "__init__.py").exists() and str(shelf) not in sys.path:
        sys.path.insert(0, str(shelf))


_ensure_canvas_core()
