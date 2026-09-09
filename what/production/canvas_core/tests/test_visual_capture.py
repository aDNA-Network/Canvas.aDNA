"""Tests for canvas_core.visual_capture (Blueprint P4 b4.0).

The load-bearing tests here are the two safety ones. Whole-screen capture on this node recorded a
third party's private messages during Blueprint P2, which is why the agent-confirmed-render gate
went unmet for a month. The fix is not "remember not to do that" — it is that **no whole-screen
code path exists**, asserted structurally: one argv builder, always ``-l``, and the literal
``screencapture`` appears nowhere else in the module.
"""

from __future__ import annotations

import ast
import platform
import re
from pathlib import Path

import pytest

from canvas_core import visual_capture as vc

MACOS_ONLY = pytest.mark.skipif(
    platform.system() != "Darwin", reason="window-scoped capture is macOS-only"
)


# ================================================================================================
# The safety property — structural, not behavioural
# ================================================================================================

@pytest.mark.parametrize("window_id", [1, 7, 42, 99999, 2**31 - 1])
def test_every_argv_is_window_scoped(window_id: int) -> None:
    """Every constructed argv carries ``-l <window_id>`` — there is no whole-screen form."""
    argv = vc._screencapture_argv(window_id, Path("/tmp/x.png"))
    assert argv[0] == "screencapture"
    assert "-l" in argv, f"argv without -l would capture a whole screen: {argv}"
    assert argv[argv.index("-l") + 1] == str(window_id)


@pytest.mark.parametrize("bad_id", [0, -1, None, "3", 3.0, True])
def test_argv_refuses_without_a_resolved_window_id(bad_id: object) -> None:
    """No id, no capture. A fallback to a wider frame is the defect this module exists to prevent."""
    with pytest.raises(vc.CaptureError):
        vc._screencapture_argv(bad_id, Path("/tmp/x.png"))  # type: ignore[arg-type]


def test_every_capture_call_routes_through_the_argv_builder() -> None:
    """No ``subprocess.run`` in this module may pass a hand-built ``screencapture`` argv.

    This is the durable half of the guarantee. The literal string appears in prose and error
    messages too (that is fine and was the first version of this test's mistaken premise); what
    must hold is that every *invocation* goes through :func:`_screencapture_argv`, which cannot
    emit a whole-screen form. A future edit that hand-rolls a capture call fails here rather than
    passing a review.
    """
    tree = ast.parse(Path(vc.__file__).read_text(encoding="utf-8"))
    hand_rolled: list[int] = []
    routed = 0
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        if node.func.attr != "run" or not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.List) and first.elts:
            head = first.elts[0]
            if isinstance(head, ast.Constant) and head.value == "screencapture":
                hand_rolled.append(node.lineno)
        if isinstance(first, ast.Call) and getattr(first.func, "id", None) == "_screencapture_argv":
            routed += 1

    assert not hand_rolled, (
        f"hand-built screencapture argv at line(s) {hand_rolled} — every capture must route "
        "through _screencapture_argv, which cannot emit a whole-screen form"
    )
    assert routed == 1, f"expected exactly one builder-routed capture call, found {routed}"


# ================================================================================================
# Swift-interpolation guard (a hardening divergence from the Home source)
# ================================================================================================

@pytest.mark.parametrize("value", ['Canvas"', "a\\b", "x\ny", 'v" + evil + "'])
def test_swift_literal_guard_rejects_escapes(value: str) -> None:
    with pytest.raises(ValueError):
        vc._check_swift_literal(value, "title_contains")


@pytest.mark.parametrize("value", ["Canvas.aDNA", "Obsidian", "Home.aDNA", "my-vault_2", ""])
def test_swift_literal_guard_accepts_ordinary_names(value: str) -> None:
    assert vc._check_swift_literal(value, "title_contains") == value


def test_find_window_rejects_unsafe_title_pin() -> None:
    """The guard fires before any subprocess runs."""
    with pytest.raises(ValueError):
        vc.find_window(title_contains='"; rm -rf /; "')


# ================================================================================================
# Vault resolution — no cross-vault fallback
# ================================================================================================

@MACOS_ONLY
def test_resolve_vault_id_finds_this_vault() -> None:
    vault_id = vc.resolve_vault_id()
    assert re.fullmatch(r"[0-9a-f]{16}", vault_id), vault_id


def test_resolve_vault_id_raises_for_an_unregistered_path(tmp_path: Path) -> None:
    """Home's version falls back to a hard-coded id; ours raises.

    A fallback id navigates a *different vault* — the same class of error the title pin exists to
    prevent, arriving through the other door.
    """
    with pytest.raises(vc.CaptureError, match="not a registered Obsidian vault"):
        vc.resolve_vault_id(tmp_path)


# ================================================================================================
# Failure is loud
# ================================================================================================

@MACOS_ONLY
def test_capture_window_raises_when_no_window_matches(tmp_path: Path) -> None:
    """A capture that silently produced nothing would let an agent report a sight gate as met."""
    with pytest.raises(vc.CaptureError, match="no on-screen"):
        vc.capture_window(tmp_path / "out.png", title_contains="NoSuchVaultXYZ")


def test_platform_guard_is_explicit() -> None:
    if platform.system() == "Darwin":
        assert vc.is_supported_platform() is True
    else:
        assert vc.is_supported_platform() is False
        with pytest.raises(vc.CaptureError, match="macOS-only"):
            vc._require_macos()


def test_restore_frontmost_is_a_noop_on_empty_input() -> None:
    vc.restore_frontmost(None)
    vc.restore_frontmost("")


# ================================================================================================
# Live probe (skips when Obsidian is not open on this vault — never fails the suite for it)
# ================================================================================================

@MACOS_ONLY
def test_live_window_probe_is_title_pinned() -> None:
    win = vc.find_window()
    if win is None:
        pytest.skip("Obsidian is not open on Canvas.aDNA — live capture is operator-preconditioned")
    assert vc.DEFAULT_TITLE_PIN in win.title
    assert win.id > 0 and win.w > 0 and win.h > 0
