"""``comic-generator`` CLI — build a multi-page comic ``.canvas`` from a comic spec.

    comic-generator build   <input.yaml|.json> <output.canvas> [--strict-paths] [--bundle [NAME=]PATH ...]
    comic-generator compose <input.yaml|.json> -o <enriched.yaml> --bundle [NAME=]PATH ... \
                            [--strict-refs] [--max-refs N] [--ref-category CAT ...]

``build`` is byte-compatible with the pre-H5 single-command CLI (``--strict-paths`` fails exit 1 when any panel
``image_path`` does not resolve relative to the input file's directory). ``compose`` (Halftone H5) enriches the
input with VisualDNA bundle assets — descriptor fill + the LoRA pair-gate + reference images — and writes the
enriched YAML (file-shaped, inspectable; a derived artifact). ``build --bundle`` composes in-memory then builds.
Emits image PROMPTS as ``_reserved`` metadata only — never renders pixels.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from comic_generator import compose_input
from comic_generator.consume import build_comic
from comic_generator.model import ComicInput, load_comic, validate_image_paths


def _add_bundle_args(sp: argparse.ArgumentParser) -> None:
    sp.add_argument(
        "--bundle",
        action="append",
        default=[],
        metavar="[NAME=]PATH",
        help="a VisualDNA character bundle YAML; prefix with NAME= to bind it to a specific input character "
        "(else heuristic display_name/id matching). Repeatable.",
    )
    sp.add_argument(
        "--strict-refs",
        action="store_true",
        help="fail when a bundle reference image does not resolve (default: warn + skip)",
    )
    sp.add_argument(
        "--max-refs",
        type=int,
        default=compose_input.DEFAULT_REF_CAP,
        help="max reference images composed per character (default %(default)s)",
    )
    sp.add_argument(
        "--ref-category",
        action="append",
        default=None,
        metavar="CAT",
        help="reference categories to compose (repeatable; default: portraits expressions scenes; "
        "canonical items of other list categories are always eligible)",
    )


def _parse_bundle_specs(specs: list[str]) -> list[tuple[str | None, compose_input.Bundle]]:
    out: list[tuple[str | None, compose_input.Bundle]] = []
    for spec in specs:
        name, sep, rest = spec.partition("=")
        if sep and name.strip() and "/" not in name and "\\" not in name:
            out.append((name.strip(), compose_input.load_bundle(rest)))
        else:
            out.append((None, compose_input.load_bundle(spec)))
    return out


def _enrich(args: argparse.Namespace) -> dict:
    raw = compose_input.load_raw_input(args.input)
    bundles = _parse_bundle_specs(args.bundle)
    categories = tuple(args.ref_category) if args.ref_category else compose_input.DEFAULT_REF_CATEGORIES
    return compose_input.enrich_comic_dict(
        raw, bundles, categories=categories, cap=args.max_refs, strict_refs=args.strict_refs
    )


def _cmd_build(args: argparse.Namespace) -> int:
    if args.bundle:
        enriched = _enrich(args)
        comic = ComicInput.from_dict(enriched)
    else:
        comic = load_comic(args.input)
    if args.strict_paths:
        missing = validate_image_paths(comic, base_dir=Path(args.input).parent)
        if missing:
            print(
                f"comic-generator: --strict-paths: {len(missing)} missing image_path(s): {missing}",
                file=sys.stderr,
            )
            return 1
    doc = build_comic(comic)
    Path(args.output).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n_pages = sum(
        1 for n in doc["nodes"]
        if n.get("type") == "group" and "_page" in n.get("id", "")
    )
    print(f"comic-generator: wrote {args.output} ({n_pages} pages, {comic.panel_count()} panels, "
          f"{len(doc['nodes'])} nodes, {len(doc['edges'])} edges)")
    return 0


def _cmd_compose(args: argparse.Namespace) -> int:
    enriched = _enrich(args)
    comic = ComicInput.from_dict(enriched)  # sanity: the enriched input must still load
    compose_input.dump_enriched(enriched, args.output)
    n_assets = len(comic.character_assets())
    n_refs = sum(len(c.reference_images) for c in comic.characters)
    print(f"comic-generator: wrote {args.output} ({len(comic.characters)} characters, "
          f"{n_assets} with composed assets, {n_refs} reference images)")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="comic-generator", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="command", required=True)

    b = sub.add_parser("build", help="build a .canvas from a comic spec")
    b.add_argument("input", help="comic spec (.yaml/.yml/.json)")
    b.add_argument("output", help="output .canvas path")
    b.add_argument("--strict-paths", action="store_true",
                   help="fail when a panel image_path does not resolve (default: warn)")
    _add_bundle_args(b)
    b.set_defaults(func=_cmd_build)

    c = sub.add_parser("compose", help="enrich a comic spec with VisualDNA bundle assets (Halftone H5)")
    c.add_argument("input", help="comic spec (.yaml/.yml/.json)")
    c.add_argument("-o", "--output", required=True, help="enriched YAML output path")
    _add_bundle_args(c)
    c.set_defaults(func=_cmd_compose)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(sys.argv[1:] if argv is None else argv)
    if args.command == "compose" and not args.bundle:
        print("comic-generator compose: at least one --bundle is required", file=sys.stderr)
        return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
