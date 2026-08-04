"""``comic-render`` — the bridge CLI (roadmap §1).

``comic-render plan|dispatch|refine|select|write-back|validate|compose <canvas>`` plus
``run --until <stage>``. The manifest JSON sidecar is the resumable state; **every stage is
idempotent** — re-running skips completed work. Exit codes: 0 clean · 1 a gate/policy failure
(validation, budget cap, write-back invariant) · 2 usage or unreadable input.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from comic_render import __version__
from comic_render.compose import run_compose
from comic_render.dispatch import BudgetCapExceededError, run_generate, run_refine
from comic_render.extract import (
    DEFAULT_CHAIN,
    DEFAULT_VARIANT_COUNT,
    StaleManifestError,
    check_freshness,
    load_canvas,
    plan,
)
from comic_render.manifest import RenderManifest, manifest_path_for
from comic_render.select import DEFAULT_APPROVER, DEFAULT_PICK_REASON, run_select
from comic_render.validate import BridgeValidationError, run_validate
from comic_render.writeback import WritebackInvariantError, run_writeback

STAGE_ORDER = ["plan", "dispatch", "refine", "select", "write-back", "validate", "compose"]


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="comic-render",
        description=f"aDNA Canvas render bridge v{__version__} — dispatches, does not diffuse.",
    )
    p.add_argument("--json", action="store_true", dest="as_json", help="emit machine-readable JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    def stage(name: str, help_text: str) -> argparse.ArgumentParser:
        s = sub.add_parser(name, help=help_text)
        s.add_argument("canvas", help="path to the source issue.canvas")
        s.add_argument("--vault-root", default=None, help="vault root for file-node paths (default: nearest .obsidian, else the canvas dir)")
        return s

    s = stage("plan", "extract the render manifest from the canvas (staleness-guarded)")
    s.add_argument("--chain", default=DEFAULT_CHAIN, help='render chain, e.g. "generate:fake,refine:fake@0.4"')
    s.add_argument("--variants", type=int, default=DEFAULT_VARIANT_COUNT, help="variants per panel")
    s.add_argument("--budget-cap", type=float, default=None, help="max spend in USD (None = uncapped)")
    s.add_argument("--register", default="comic_default", help="RLHF register recorded in selections")
    s.add_argument("--force", action="store_true", help="rebuild even if fresh")

    stage("dispatch", "execute each panel's generate stage (idempotent, budget-capped)")
    stage("refine", "execute each panel's refine stage(s) over generate outputs")

    s = stage("select", "pick one variant per panel + write the Schema-A SelectionRecord")
    s.add_argument("--pick-index", type=int, default=0)
    s.add_argument("--reason", default=DEFAULT_PICK_REASON)
    s.add_argument("--approver", default=DEFAULT_APPROVER)

    s = stage("write-back", "write issue.rendered.canvas (NEW file; input immutable)")
    s.add_argument("--force", action="store_true", help="overwrite an existing rendered canvas")

    stage("validate", "stage-6 gate: conformance + degradation + file existence + DPI")

    s = stage("compose", "composite pages to print JPGs via canvas_core PrintExporter")
    s.add_argument("--cmyk", action="store_true", help="convert pages to CMYK (H6 print pass)")
    s.add_argument("--quality", type=int, default=95, help="JPEG quality")

    s = stage("run", "run stages in order (plan → … → compose)")
    s.add_argument("--until", choices=STAGE_ORDER, default="compose", help="last stage to run")
    s.add_argument("--chain", default=DEFAULT_CHAIN)
    s.add_argument("--variants", type=int, default=DEFAULT_VARIANT_COUNT)
    s.add_argument("--budget-cap", type=float, default=None)
    s.add_argument("--register", default="comic_default")
    s.add_argument("--pick-index", type=int, default=0)
    s.add_argument("--reason", default=DEFAULT_PICK_REASON)
    s.add_argument("--approver", default=DEFAULT_APPROVER)
    s.add_argument("--cmyk", action="store_true")
    s.add_argument("--quality", type=int, default=95)
    s.add_argument("--force", action="store_true", help="force plan rebuild + write-back overwrite")
    return p


def _load_state(canvas: str) -> tuple[RenderManifest, Path, dict[str, Any]]:
    canvas_path = Path(canvas)
    doc = load_canvas(canvas_path)
    mpath = manifest_path_for(canvas_path)
    if not mpath.exists():
        raise FileNotFoundError(f"no manifest {mpath.name} — run plan first")
    manifest = RenderManifest.load(mpath)
    check_freshness(manifest, doc)
    return manifest, mpath, doc


def _emit(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2))
        return
    stage_name = payload.pop("stage", "?")
    print(f"[{stage_name}] " + ", ".join(f"{k}={v}" for k, v in payload.items()))


def _run_stage(name: str, args: argparse.Namespace) -> dict[str, Any]:
    if name == "plan":
        manifest, mpath = plan(
            args.canvas,
            chain=args.chain,
            variant_count=args.variants,
            budget_cap=args.budget_cap,
            register=args.register,
            force=args.force,
        )
        return {
            "stage": "plan",
            "manifest": mpath.name,
            "comic_id": manifest.comic_id,
            "panels": len(manifest.panels),
            "dispatchable": len(manifest.dispatchable()),
            "sync_hash": manifest.source_sync_hash,
        }
    manifest, mpath, _doc = _load_state(args.canvas)
    if name == "dispatch":
        return {"stage": "dispatch", **run_generate(manifest, mpath)}
    if name == "refine":
        return {"stage": "refine", **run_refine(manifest, mpath)}
    if name == "select":
        return {
            "stage": "select",
            **run_select(
                manifest, mpath,
                pick_index=args.pick_index, pick_reason=args.reason, approver_id=args.approver,
            ),
        }
    if name == "write-back":
        out, summary = run_writeback(
            manifest, mpath, vault_root=args.vault_root, force=getattr(args, "force", False)
        )
        return {"stage": "write-back", "output": out.name, **summary}
    if name == "validate":
        return {"stage": "validate", **run_validate(manifest, mpath, vault_root=args.vault_root)}
    if name == "compose":
        result = run_compose(
            manifest, mpath,
            vault_root=args.vault_root, cmyk=args.cmyk, jpeg_quality=args.quality,
        )
        return {
            "stage": "compose",
            "pages": len(result["pages"]),
            "output_dir": result["output_dir"],
            "warnings": result["warnings"],
        }
    raise ValueError(f"unknown stage {name!r}")


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.cmd == "run":
            until = STAGE_ORDER.index(args.until)
            for name in STAGE_ORDER[: until + 1]:
                _emit(_run_stage(name, args), args.as_json)
        else:
            _emit(_run_stage(args.cmd, args), args.as_json)
        return 0
    except (BridgeValidationError, WritebackInvariantError, BudgetCapExceededError,
            StaleManifestError, NotImplementedError) as exc:
        print(f"comic-render: GATE FAIL — {exc}", file=sys.stderr)
        return 1
    except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"comic-render: error — {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
