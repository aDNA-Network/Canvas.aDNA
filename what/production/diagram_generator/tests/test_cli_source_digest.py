"""The CLI stamps ``_reserved.sync.source_sha256`` (Vernier P3 objective 2, 2026-10-26; F-V-16).

Gate #9's source leg compares a stored digest of the source file's bytes with a recomputation. Until
this card, no canvas this producer built carried one: ``build_diagram`` takes a parsed
``DiagramInput`` and never sees the path, so the leg had nothing to read in this vault. The CLI holds
the path, so the CLI stamps it, through ``canvas_std``'s own definition (LIP-0011 §2, touch #7) rather
than a second copy of it.

What these pin:

- the stamped value IS ``canvas_std.compute_source_sha256(input)``;
- the stamped canvas still validates at ``adna_native`` (A-6 checks the 64-hex shape hard);
- the digest is the ONLY difference from ``build_diagram`` without it (so every other caller, and
  every older test, sees byte-identical output);
- a comment-only edit moves the digest and nothing else: the source leg's blind spot ("whether a
  changed byte matters") and the rebuild leg's ("a view-neutral edit") are the same fact seen from
  the two sides.
"""

from __future__ import annotations

import json
from pathlib import Path

from canvas_std import ConformanceLevel, compute_source_sha256, validate

from diagram_generator.__main__ import main
from diagram_generator.consume import build_diagram
from diagram_generator.model import load_diagram

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "canvas_standard_flow.yaml"


def _sync(doc: dict) -> dict:
    return doc["metadata"]["frontmatter"]["_reserved"]["sync"]


def _cli_build(src: Path, out: Path) -> dict:
    assert main(["build", str(src), str(out)]) == 0
    return json.loads(out.read_text(encoding="utf-8"))


def test_cli_stamps_the_standards_own_digest(tmp_path):
    doc = _cli_build(EXAMPLE, tmp_path / "out.canvas")
    assert _sync(doc)["source_sha256"] == compute_source_sha256(EXAMPLE)
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_the_digest_is_the_only_difference(tmp_path):
    stamped = _cli_build(EXAMPLE, tmp_path / "out.canvas")
    bare = json.loads(json.dumps(build_diagram(load_diagram(EXAMPLE))))  # the CLI's own JSON round trip
    assert "source_sha256" not in _sync(bare)
    _sync(stamped).pop("source_sha256")
    assert stamped == bare


def test_a_comment_moves_the_digest_and_nothing_else(tmp_path):
    edited = tmp_path / "flow.yaml"
    edited.write_bytes(EXAMPLE.read_bytes() + b"\n# a comment: outside every rendered field\n")
    before = _cli_build(EXAMPLE, tmp_path / "before.canvas")
    after = _cli_build(edited, tmp_path / "after.canvas")
    assert _sync(after)["source_sha256"] != _sync(before)["source_sha256"]
    _sync(before).pop("source_sha256")
    _sync(after).pop("source_sha256")
    assert after == before
