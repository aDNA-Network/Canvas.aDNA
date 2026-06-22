"""``comic-generator`` CLI — build a multi-page comic ``.canvas`` from a comic spec.

    comic-generator build <input.yaml|.json> <output.canvas>

Emits image PROMPTS as ``_reserved`` metadata only — never renders pixels.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from comic_generator.consume import build_comic
from comic_generator.model import load_comic


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3 or argv[0] != "build":
        print("usage: comic-generator build <input.yaml|.json> <output.canvas>", file=sys.stderr)
        return 2
    _, inp, out = argv
    comic = load_comic(inp)
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
