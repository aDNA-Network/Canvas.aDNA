"""``python -m comic_render`` — delegate to the CLI."""

from comic_render.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
