"""``brief-consumer`` CLI — build a ``.canvas`` from a brief input.

    brief-consumer build <input.yaml|.json> <output.canvas>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from brief_consumer.consume import build_brief
from brief_consumer.model import load_brief


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3 or argv[0] != "build":
        print("usage: brief-consumer build <input.yaml|.json> <output.canvas>", file=sys.stderr)
        return 2
    _, inp, out = argv
    doc = build_brief(load_brief(inp))
    Path(out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"brief-consumer: wrote {out} ({len(doc['nodes'])} nodes, {len(doc['edges'])} edges)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
