"""``comic-generator`` CLI — build a multi-page comic ``.canvas`` from a comic spec.

    comic-generator build <input.yaml|.json> <output.canvas> [--strict-paths]

``--strict-paths`` (Halftone H1): fail (exit 1) when any panel ``image_path`` does not resolve relative to the
input file's directory; without it, missing paths warn and the build proceeds. Emits image PROMPTS as
``_reserved`` metadata only — never renders pixels.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from comic_generator.consume import build_comic
from comic_generator.model import load_comic, validate_image_paths


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    strict_paths = "--strict-paths" in argv
    argv = [a for a in argv if a != "--strict-paths"]
    if len(argv) != 3 or argv[0] != "build":
        print("usage: comic-generator build <input.yaml|.json> <output.canvas> [--strict-paths]", file=sys.stderr)
        return 2
    _, inp, out = argv
    comic = load_comic(inp)
    if strict_paths:
        missing = validate_image_paths(comic, base_dir=Path(inp).parent)
        if missing:
            print(f"comic-generator: --strict-paths: {len(missing)} missing image_path(s): {missing}", file=sys.stderr)
            return 1
    doc = build_comic(comic)
    Path(out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n_pages = sum(
        1 for n in doc["nodes"]
        if n.get("type") == "group" and "_page" in n.get("id", "")
    )
    print(f"comic-generator: wrote {out} ({n_pages} pages, {comic.panel_count()} panels, "
          f"{len(doc['nodes'])} nodes, {len(doc['edges'])} edges)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
