"""Window-scoped capture — the instrument the agent-confirmed-render gate needed all along.

`spec_federation_contract` §4 Amendment 1 makes every shipped canvas pass three checks: schema
(``canvas-std validate``), geometry (``canvas-visual-check``), and an **agent-confirmed Obsidian
render**. Canvas could satisfy the first two and never the third, because the vault's only
rendering path is Playwright over ``canvas_core.html_renderer`` — which
``spec_canvas_review_surface`` §5 records as **file-node-blind by design**. A board made of
``file`` nodes can only be sight-certified live.

The gate therefore sat unmet through Blueprint P2, P2b, P2c and P3, on this recorded ground:
*"needs a window-scoped capture — whole-screen ``screencapture`` is ruled out: it captured a third
party's private messages."* Both clauses are true. The conclusion drawn from them — that no safe
capture exists on this node — was false when it was written (**F-P4-1**): a constraint on one
*method* had been inherited as a constraint on the *capability*.

**Provenance.** This is a port, not an invention. The window-id probe and the ``screencapture -l``
call are ``Home.aDNA/what/code/window_helpers.py`` (Hestia; Operation Prytaneion M1.1–M1.3,
including their Finding I: pin the window by title, because a blind capture once grabbed the
``aDNALabs.aDNA`` window). The JPEG compression step is their ``iii_runner.capture_obsidian``.
Their operator decision **D-A (2026-06-02)** already named ``CanvasForge.aDNA`` — merged into this
vault at pt09 — as this code's eventual home; the assignment was simply never executed. Home's
copy is untouched and keeps working.

**The safety property is structural, not behavioural.** Exactly one function in this module builds
a ``screencapture`` argv (:func:`_screencapture_argv`), it refuses to build one without a resolved
window id, and every argv it returns carries ``-l <id>``. ``test_visual_capture.py`` asserts both
the argv invariant *and* that the literal string ``screencapture`` appears nowhere else in this
file — so a future edit that reintroduces a whole-screen path fails a test rather than a review.

**Two deliberate divergences from the source**, both hardening:

1. **No cross-vault fallback.** Home's ``resolve_vault_id`` falls back to a hard-coded id when the
   registry lookup misses. Here an unmatched vault **raises** — a fallback id would navigate a
   *different vault*, which is the failure mode the title pin exists to prevent.
2. **Swift interpolation is validated.** ``app_name``/``title_contains`` are interpolated into
   Swift source upstream; a value containing a quote or backslash would break out of the string
   literal. Here they are rejected up front.

Platform: macOS only (Swift + ``screencapture`` + ``osascript``). Off-darwin raises
:class:`CaptureError` with an actionable message; the tests skip rather than fail.
"""

from __future__ import annotations

import json
import platform
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

_VAULT_ROOT = Path(__file__).resolve().parents[3]

#: Default window-title pin. Obsidian titles read ``<file> - <vault> - Obsidian <version>``, so the
#: vault name selects this vault's window when several vaults are open (Home's Finding I).
DEFAULT_TITLE_PIN = "Canvas.aDNA"
DEFAULT_APP = "Obsidian"

#: Longest side of the JPEG handed to the agent, in px.
#:
#: **Not Home's 1280** (F-P4-2). A window capture on this node is Retina-backed — measured
#: 3216×1984 for a 1496×880 logical window — so ``sips -Z 1280`` discards ~2.4× of linear
#: resolution. That is the right trade for their use (a whole-window overview fed to a vision
#: model) and the wrong one for reading a canvas, so the default here preserves the detail.
JPEG_LONG_EDGE = 2200

#: Canvas render is heavier than a markdown note — Home measured 2.5s as the workable settle.
DEFAULT_RENDER_WAIT = 2.5

#: Settle after zoom-to-fit before capturing.
DEFAULT_ZOOM_WAIT = 1.5

#: Fractional crop (left, top, right, bottom) that drops Obsidian's chrome — file-tree sidebar,
#: tab bar, right ribbon, bottom toolbar — keeping the canvas pane.
#:
#: ⚠ Layout-dependent, not universal: collapsing a sidebar moves these. They are a convenience,
#: never a correctness claim. The actual check is that **the agent can read the node text** in the
#: returned image; if it cannot, re-tune or pass ``crop=None`` and read the full window.
DEFAULT_PANE_CROP = (0.24, 0.06, 0.955, 0.90)

# Interpolated into Swift source: anything that could terminate a string literal is refused.
_SWIFT_SAFE = re.compile(r"^[A-Za-z0-9 ._\-]*$")


class CaptureError(RuntimeError):
    """No capturable window, an unresolvable vault, or an unsupported platform.

    Raised rather than returned: a capture that silently produces nothing is how an unmet visual
    gate gets reported as met.
    """


@dataclass(frozen=True)
class WindowInfo:
    """One on-screen window: its id, bounds and title."""

    id: int
    x: int
    y: int
    w: int
    h: int
    title: str


# ================================================================================================
# Platform + argument guards
# ================================================================================================

def is_supported_platform() -> bool:
    """True on macOS, where the Swift/``screencapture``/``osascript`` toolchain exists."""
    return platform.system() == "Darwin"


def _require_macos() -> None:
    if not is_supported_platform():
        raise CaptureError(
            f"window-scoped capture is macOS-only (this is {platform.system()}); it needs Swift, "
            "screencapture and osascript. On another platform, sight-certify by hand and record "
            "the reviewer — never mark the visual gate met without an actual look."
        )


def _check_swift_literal(value: str, field: str) -> str:
    """Refuse values that could break out of the Swift string literal they are interpolated into."""
    if not _SWIFT_SAFE.match(value):
        raise ValueError(
            f"{field}={value!r} contains characters that are unsafe to interpolate into Swift "
            "source (allowed: letters, digits, space, dot, underscore, hyphen)"
        )
    return value


# ================================================================================================
# Window discovery (Swift CGWindowList — non-disruptive, no focus steal)
# ================================================================================================

def _swift_source(app_name: str, title_contains: str) -> str:
    return f'''import Cocoa

let opts: CGWindowListOption = [.optionOnScreenOnly]
let wins = CGWindowListCopyWindowInfo(opts, kCGNullWindowID) as? [[String: Any]] ?? []
let titleFilter = "{title_contains}"

var bestId: Int = 0
var bestArea: Double = 0
var bestX: Int = 0
var bestY: Int = 0
var bestW: Int = 0
var bestH: Int = 0
var bestTitle: String = ""

for w in wins {{
  guard let owner = w[kCGWindowOwnerName as String] as? String else {{ continue }}
  if !owner.contains("{app_name}") {{ continue }}
  guard let bounds = w[kCGWindowBounds as String] as? [String: Double] else {{ continue }}
  let width = bounds["Width"] ?? 0
  let height = bounds["Height"] ?? 0
  let area = width * height
  if area < 100000 {{ continue }}
  let title = (w[kCGWindowName as String] as? String) ?? ""
  if !titleFilter.isEmpty && !title.contains(titleFilter) {{ continue }}
  if area > bestArea {{
    bestArea = area
    if let n = w[kCGWindowNumber as String] as? Int {{ bestId = n }}
    bestX = Int(bounds["X"] ?? 0)
    bestY = Int(bounds["Y"] ?? 0)
    bestW = Int(width)
    bestH = Int(height)
    bestTitle = title
  }}
}}

if bestId > 0 {{
  print("{{\\"id\\":\\(bestId),\\"x\\":\\(bestX),\\"y\\":\\(bestY),\\"w\\":\\(bestW),\\"h\\":\\(bestH),\\"title\\":\\"\\(bestTitle)\\"}}")
}}
'''


def find_window(
    app_name: str = DEFAULT_APP,
    title_contains: str = DEFAULT_TITLE_PIN,
) -> WindowInfo | None:
    """Largest on-screen window of ``app_name`` whose title contains ``title_contains``, else None.

    Read-only and non-disruptive: enumerates windows, steals no focus, captures nothing.
    """
    _require_macos()
    _check_swift_literal(app_name, "app_name")
    _check_swift_literal(title_contains, "title_contains")
    try:
        proc = subprocess.run(
            ["swift", "-"], input=_swift_source(app_name, title_contains),
            capture_output=True, text=True, timeout=30,
        )
        out = proc.stdout.strip()
        if not out:
            return None
        raw = json.loads(out.splitlines()[-1])
    except (subprocess.TimeoutExpired, json.JSONDecodeError, ValueError, FileNotFoundError):
        return None
    return WindowInfo(
        id=int(raw["id"]), x=int(raw["x"]), y=int(raw["y"]),
        w=int(raw["w"]), h=int(raw["h"]), title=str(raw.get("title", "")),
    )


# ================================================================================================
# Capture — the ONLY place a screencapture argv is constructed
# ================================================================================================

def _screencapture_argv(
    window_id: int,
    out_path: Path,
    *,
    suppress_sound: bool = True,
    no_attached: bool = True,
) -> list[str]:
    """Build the capture argv. **Always window-scoped** — there is no whole-screen branch.

    A non-positive window id raises: without a resolved id there is nothing safe to capture, and
    the one thing this module must never do is fall back to a wider frame.
    """
    if not isinstance(window_id, int) or isinstance(window_id, bool) or window_id <= 0:
        raise CaptureError(
            f"refusing to build a capture argv without a resolved window id (got {window_id!r}); "
            "there is no whole-screen fallback by design"
        )
    argv = ["screencapture", "-l", str(window_id)]
    if suppress_sound:
        argv.append("-x")
    if no_attached:
        argv.append("-a")
    argv.append(str(out_path))
    return argv


def capture_window(
    out_path: str | Path,
    *,
    app_name: str = DEFAULT_APP,
    title_contains: str = DEFAULT_TITLE_PIN,
) -> Path:
    """Capture one window to ``out_path`` (PNG). Raises :class:`CaptureError` if there is none.

    Fails loudly on purpose. A capture that quietly produced nothing would let an agent report a
    sight gate as met without having looked at anything.
    """
    _require_macos()
    out = Path(out_path)
    win = find_window(app_name, title_contains)
    if win is None:
        raise CaptureError(
            f"no on-screen {app_name} window matching title {title_contains!r}. Open {app_name} "
            f"with the {title_contains} vault and retry — live capture is the point of this gate, "
            "so there is no fallback to a wider frame."
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(_screencapture_argv(win.id, out), capture_output=True, timeout=30)
    if proc.returncode != 0 or not out.exists() or out.stat().st_size <= 1000:
        raise CaptureError(
            f"screencapture failed for window {win.id} ({win.title!r}): rc={proc.returncode} "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    return out


def compress_to_jpeg(
    png_path: Path,
    jpeg_path: Path | None = None,
    *,
    long_edge: int = JPEG_LONG_EDGE,
) -> Path:
    """Downscale + convert a capture to JPEG via ``sips`` so an agent can read it cheaply."""
    _require_macos()
    png = Path(png_path)
    jpg = Path(jpeg_path) if jpeg_path else png.with_suffix(".jpg")
    subprocess.run(["sips", "-Z", str(long_edge), str(png), "--out", str(png)],
                   capture_output=True, timeout=30)
    subprocess.run(["sips", "-s", "format", "jpeg", str(png), "--out", str(jpg)],
                   capture_output=True, timeout=30)
    if not jpg.exists():
        raise CaptureError(f"sips produced no JPEG for {png}")
    return jpg


def crop_fractional(image_path: Path, box: tuple[float, float, float, float]) -> Path:
    """Crop ``image_path`` in place to fractional ``(left, top, right, bottom)`` of its own size."""
    try:
        from PIL import Image
    except ImportError:
        return Path(image_path)          # PIL absent → leave the full-window shot untouched
    path = Path(image_path)
    with Image.open(path) as im:
        width, height = im.size
        left, top, right, bottom = box
        im.crop((int(width * left), int(height * top),
                 int(width * right), int(height * bottom))).save(path)
    return path


# ================================================================================================
# Obsidian navigation (focus is borrowed, then given back)
# ================================================================================================

def resolve_vault_id(vault_path: Path | str = _VAULT_ROOT) -> str:
    """Obsidian's own vault id for ``vault_path``, from its registry.

    **No fallback.** Home's version falls back to a hard-coded id; here an unmatched vault raises,
    because a fallback id navigates a *different vault* — the exact failure the title pin exists
    to prevent, arriving through the other door.
    """
    registry = Path.home() / "Library/Application Support/obsidian/obsidian.json"
    target = str(Path(vault_path).resolve())
    try:
        vaults = json.loads(registry.read_text(encoding="utf-8")).get("vaults", {})
    except (OSError, json.JSONDecodeError) as exc:
        raise CaptureError(f"cannot read Obsidian's vault registry at {registry}: {exc}") from exc
    for vault_id, info in vaults.items():
        if str(Path(info.get("path", "")).resolve()) == target:
            return vault_id
    raise CaptureError(
        f"{target} is not a registered Obsidian vault. Open it in Obsidian once so it registers; "
        "no fallback id is used, because that would navigate someone else's vault."
    )


def get_frontmost_app() -> str | None:
    """Name of the frontmost application, or None."""
    if not is_supported_platform():
        return None
    try:
        proc = subprocess.run(
            ["osascript", "-e",
             'tell application "System Events" to name of first process whose frontmost is true'],
            capture_output=True, text=True, timeout=10)
        return proc.stdout.strip() or None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def restore_frontmost(app_name: str | None) -> None:
    """Return focus to ``app_name`` (no-op when falsy or off-platform)."""
    if not app_name or not is_supported_platform():
        return
    _check_swift_literal(app_name, "app_name")
    subprocess.run(["osascript", "-e", f'tell application "{app_name}" to activate'],
                   capture_output=True, timeout=10)


def open_canvas_in_obsidian(
    canvas: str | Path,
    *,
    vault_id: str | None = None,
    render_wait: float = DEFAULT_RENDER_WAIT,
    reopen: bool = True,
    restore_focus: bool = True,
) -> None:
    """Open a ``.canvas`` in live Obsidian via the URL scheme, then wait for it to render.

    ``canvas`` is reduced to a **basename** — Obsidian's open URI matches by name, not by
    vault-relative path (Home verified a path 404s as "File not found"), so the basename must be
    unique in the vault. ``reopen`` nudges off the canvas leaf first, because Obsidian does not
    reliably hot-reload a ``.canvas`` that was rewritten on disk under a focused leaf.

    Precondition: Obsidian's *"Run action from external link?"* prompt must have been accepted once
    with "Don't ask again", or the call blocks on a modal.
    """
    _require_macos()
    name = Path(canvas).name
    if not name.endswith(".canvas"):
        name += ".canvas"
    vid = vault_id or resolve_vault_id()
    previous = get_frontmost_app() if restore_focus else None
    if reopen:
        subprocess.run(["open", f"obsidian://open?vault={vid}&file=STATE"],
                       check=False, capture_output=True, timeout=15)
        time.sleep(0.6)
    subprocess.run(["open", f"obsidian://open?vault={vid}&file={quote(name)}"],
                   check=False, capture_output=True, timeout=15)
    time.sleep(render_wait)
    if previous and previous != DEFAULT_APP:
        restore_frontmost(previous)


def zoom_to_fit(*, app_name: str = DEFAULT_APP, settle: float = DEFAULT_ZOOM_WAIT) -> None:
    """Send Obsidian's canvas **Zoom to fit** (Shift+1), briefly borrowing focus.

    **This step is not cosmetic — without it the capture contains no text to read** (F-P4-2).
    Obsidian's canvas culls detail by zoom level: at the accept-viewport zoom a freshly opened
    canvas lands on (~25%), node bodies draw as grey placeholder bars. Measured here: a native
    3128×1896 capture of an unzoomed canvas is pin-sharp *and* completely illegible, because the
    text was never rendered. No crop and no resolution recovers what was not drawn — only zoom.

    Home recorded Shift+1 as *"does not fire headlessly"* and worked around it by cropping their
    own canvas. Measured on this node: it fires reliably **provided Obsidian is activated first**
    and the canvas leaf holds focus, which ``obsidian://open`` already gives it — so no click is
    needed (verified against both dogfood canvases, 2026-09-08).
    """
    _require_macos()
    _check_swift_literal(app_name, "app_name")
    subprocess.run(["osascript", "-e", f'tell application "{app_name}" to activate'],
                   capture_output=True, timeout=10)
    time.sleep(0.8)
    subprocess.run(
        ["osascript", "-e", 'tell application "System Events" to keystroke "1" using {shift down}'],
        capture_output=True, timeout=10)
    time.sleep(settle)


def capture_canvas(
    canvas: str | Path,
    out_dir: str | Path,
    *,
    navigate: bool = True,
    zoom_fit: bool = True,
    crop: tuple[float, float, float, float] | None = DEFAULT_PANE_CROP,
    render_wait: float = DEFAULT_RENDER_WAIT,
    long_edge: int = JPEG_LONG_EDGE,
    title_contains: str = DEFAULT_TITLE_PIN,
    vault_id: str | None = None,
) -> Path:
    """Open a canvas in live Obsidian, capture that window, return a JPEG for the agent to read.

    This is the third check of the ship gate, and only the third: ``canvas-std validate`` is
    schema, ``canvas-visual-check`` is fit, and **neither is sight**. Producing the file is not
    passing the gate — the image has to be looked at. It earns its keep: the first two runs of
    this function certified the geometry of both dogfood canvases *and* showed their mermaid
    channel rendering as raw source behind an un-actioned trust prompt, which both machine checks
    had passed green (F-P4-3).

    Focus is borrowed for the zoom step and returned to whatever held it before.
    """
    _require_macos()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = Path(canvas).stem
    previous = get_frontmost_app()
    try:
        if navigate:
            open_canvas_in_obsidian(canvas, vault_id=vault_id, render_wait=render_wait,
                                    restore_focus=False)
        if zoom_fit:
            zoom_to_fit()
        png = capture_window(out / f"{stem}.png", title_contains=title_contains)
    finally:
        if previous and previous != DEFAULT_APP:
            restore_frontmost(previous)
    if crop:
        crop_fractional(png, crop)
    return compress_to_jpeg(png, out / f"{stem}.jpg", long_edge=long_edge)


def _main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(
        prog="python -m canvas_core.visual_capture",
        description="Window-scoped capture of a live Obsidian canvas (the sight check).",
    )
    ap.add_argument("canvas", nargs="?", help="path or basename of a .canvas to open and capture")
    ap.add_argument("--out", type=Path, default=Path("/tmp/canvas_visual_gate"))
    ap.add_argument("--title-pin", default=DEFAULT_TITLE_PIN)
    ap.add_argument("--no-navigate", action="store_true",
                    help="capture whatever is already on screen (no Obsidian navigation)")
    ap.add_argument("--no-zoom", action="store_true",
                    help="skip zoom-to-fit — the capture will be LOD-culled and unreadable (F-P4-2)")
    ap.add_argument("--no-crop", action="store_true", help="keep Obsidian's chrome in the frame")
    ap.add_argument("--info", action="store_true", help="report the window/vault probe and exit")
    args = ap.parse_args(argv)

    if args.info or not args.canvas:
        win = find_window(title_contains=args.title_pin)
        print(f"vault id: {resolve_vault_id()}")
        print(f"window:   {win}" if win else
              f"window:   NONE matching {args.title_pin!r} — is Obsidian open on that vault?")
        return 0 if win else 1

    jpeg = capture_canvas(args.canvas, args.out, navigate=not args.no_navigate,
                          zoom_fit=not args.no_zoom,
                          crop=None if args.no_crop else DEFAULT_PANE_CROP,
                          title_contains=args.title_pin)
    print(jpeg)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
