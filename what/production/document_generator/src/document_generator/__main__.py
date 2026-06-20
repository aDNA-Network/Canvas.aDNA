"""``document-generator`` CLI — build a multi-page document ``.canvas`` from a document spec.

    document-generator build <input.yaml|.json> <output.canvas>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from document_generator.consume import build_document
from document_generator.model import load_document


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3 or argv[0] != "build":
        print("usage: document-generator build <input.yaml|.json> <output.canvas>", file=sys.stderr)
        return 2
    _, inp, out = argv
    doc = build_document(load_document(inp))
    Path(out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n_pages = sum(1 for n in doc["nodes"] if n.get("id", "").startswith("page") and n.get("type") == "group")
    print(f"document-generator: wrote {out} ({n_pages} pages, {len(doc['nodes'])} nodes, {len(doc['edges'])} edges)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
