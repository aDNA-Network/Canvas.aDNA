"""``post-generator`` CLI — build a social-post ``.canvas`` from a post spec.

    post-generator build <input.yaml|.json> <output.canvas>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from post_generator.consume import build_post
from post_generator.model import load_post


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3 or argv[0] != "build":
        print("usage: post-generator build <input.yaml|.json> <output.canvas>", file=sys.stderr)
        return 2
    _, inp, out = argv
    post = load_post(inp)
    doc = build_post(post)
    Path(out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    kind = "thread" if post.is_thread else "single"
    print(f"post-generator: wrote {out} ({kind}, {len(post.panels)} panels, "
          f"{len(doc['nodes'])} nodes, {len(doc['edges'])} edges)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
