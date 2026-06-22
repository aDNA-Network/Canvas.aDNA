"""``diagram-generator`` CLI — build a diagram ``.canvas`` from a diagram spec.

    diagram-generator build <input.yaml|.json> <output.canvas>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from diagram_generator.consume import build_diagram
from diagram_generator.model import load_diagram


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3 or argv[0] != "build":
        print("usage: diagram-generator build <input.yaml|.json> <output.canvas>", file=sys.stderr)
        return 2
    _, inp, out = argv
    d = load_diagram(inp)
    doc = build_diagram(d)
    Path(out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"diagram-generator: wrote {out} ({d.diagram_type}, {len(doc['nodes'])} nodes, "
          f"{len(doc['edges'])} edges)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
