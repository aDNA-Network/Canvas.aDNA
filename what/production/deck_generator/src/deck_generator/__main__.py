"""``deck-generator`` CLI — build a deck ``.canvas`` from a deck spec.

    deck-generator build <input.yaml|.json> <output.canvas>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from deck_generator.consume import build_deck
from deck_generator.model import load_deck


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3 or argv[0] != "build":
        print("usage: deck-generator build <input.yaml|.json> <output.canvas>", file=sys.stderr)
        return 2
    _, inp, out = argv
    doc = build_deck(load_deck(inp))
    Path(out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n_slides = sum(1 for n in doc["nodes"] if n.get("id", "").startswith("slide") and n.get("type") == "group")
    print(f"deck-generator: wrote {out} ({n_slides} slides, {len(doc['nodes'])} nodes, {len(doc['edges'])} edges)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
