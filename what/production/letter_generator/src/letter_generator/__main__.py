"""``letter-generator`` CLI — build a one-page-letter ``.canvas`` from a letter spec.

    letter-generator build <input.yaml|.json> <output.canvas>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from letter_generator.consume import build_letter
from letter_generator.model import load_letter


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3 or argv[0] != "build":
        print("usage: letter-generator build <input.yaml|.json> <output.canvas>", file=sys.stderr)
        return 2
    _, inp, out = argv
    letter = load_letter(inp)
    doc = build_letter(letter)
    Path(out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"letter-generator: wrote {out} ({len(doc['nodes'])} nodes, {len(doc['edges'])} edges)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
