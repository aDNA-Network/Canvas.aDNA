"""CanvasOpener — Obsidian canvas control layer.

Detects available Obsidian control methods and provides a unified API
to open, deliver, and batch-process canvas files.

Control method detection order:
  1. REST API — Local REST API plugin on https://127.0.0.1:27124/.
         Uses openLinkText() internally. Most reliable for new files.
         API key auto-discovered from plugin config or ~/.lattice/secrets.json.
  2. CLI — /Applications/Obsidian.app/Contents/MacOS/Obsidian or `obsidian` in PATH.
         Most capable (open, eval, screenshot). Requires Catalyst license.
  3. URI Scheme — obsidian://open?vault=<vault>&file=<path>.
         Always works on macOS. Open-only, no read/write.
         Unreliable for newly-created files (file watcher race).

Part of campaign_advanced_canvas Phase 3 (M7).
"""

from __future__ import annotations

import json
import shutil
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from enum import Enum
from pathlib import Path
from typing import Any, Literal


class ControlMethod(Enum):
    """Available Obsidian control methods, ordered by capability."""

    CLI = "cli"
    REST = "rest"
    URI = "uri"


# Default locations
_CLI_PATHS: dict[str, list[str]] = {
    "darwin": ["/Applications/Obsidian.app/Contents/MacOS/Obsidian"],
    "linux": [],
    "win32": [],
}

_REST_BASE = "https://127.0.0.1:27124"
_REST_TIMEOUT = 3  # seconds


class CanvasOpener:
    """Control layer for opening and delivering Obsidian canvas files.

    Usage::

        opener = CanvasOpener("/path/to/vault")
        status = opener.check_obsidian()
        opener.open("what/lattices/my_lattice.canvas")

        # Deliver a CanvasBuilder output
        from canvas_core.core import CanvasBuilder
        cb = CanvasBuilder("demo", "1.0.0")
        cb.add_text_node("n1", "Hello", x=0, y=0)
        opener.deliver(cb.build(), "what/lattices/demo.canvas")
    """

    def __init__(
        self,
        vault_root: str | Path,
        vault_name: str = "LATTICE-PROTOCOL",
        rest_api_key: str | None = None,
        preferred_method: ControlMethod | None = None,
        auto_discover_rest: bool = True,
    ):
        self.vault_root = Path(vault_root).resolve()
        self.vault_name = vault_name
        self.rest_api_key = rest_api_key
        if self.rest_api_key is None and auto_discover_rest:
            self.rest_api_key = self._discover_rest_api_key(self.vault_root)
        self.preferred_method = preferred_method
        self._detected: dict[ControlMethod, dict[str, Any]] | None = None

    @staticmethod
    def _discover_rest_api_key(vault_root: Path) -> str | None:
        """Auto-discover REST API key from plugin config or secrets file.

        Search order:
          1. Plugin config: {vault_root}/.obsidian/plugins/obsidian-local-rest-api/data.json
          2. Secrets file: ~/.lattice/secrets.json → obsidian_rest_api_key
        """
        # 1. Plugin config
        plugin_config = (
            vault_root / ".obsidian" / "plugins" / "obsidian-local-rest-api" / "data.json"
        )
        if plugin_config.is_file():
            try:
                data = json.loads(plugin_config.read_text())
                key = data.get("apiKey")
                if key:
                    return key
            except (json.JSONDecodeError, OSError):
                pass

        # 2. Secrets file
        secrets_path = Path.home() / ".lattice" / "secrets.json"
        if secrets_path.is_file():
            try:
                data = json.loads(secrets_path.read_text())
                key = data.get("obsidian_rest_api_key")
                if key:
                    return key
            except (json.JSONDecodeError, OSError):
                pass

        return None

    # ------------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------------

    def _find_cli(self) -> str | None:
        """Find the Obsidian CLI binary."""
        # Check PATH first
        which = shutil.which("obsidian")
        if which:
            return which

        # Check platform-specific locations
        platform_paths = _CLI_PATHS.get(sys.platform, [])
        for path in platform_paths:
            if Path(path).is_file():
                return path

        return None

    def _probe_cli(self, cli_path: str) -> bool:
        """Verify CLI is responsive."""
        try:
            result = subprocess.run(
                [cli_path, "vault"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

    def _probe_rest(self) -> bool:
        """Check if REST API is responding."""
        if not self.rest_api_key:
            return False

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            f"{_REST_BASE}/",
            headers={"Authorization": f"Bearer {self.rest_api_key}"},
        )
        try:
            with urllib.request.urlopen(req, timeout=_REST_TIMEOUT, context=ctx) as resp:
                return resp.status == 200
        except (urllib.error.URLError, OSError, TimeoutError):
            return False

    def _detect_methods(self) -> dict[ControlMethod, dict[str, Any]]:
        """Probe all control methods and return available ones."""
        methods: dict[ControlMethod, dict[str, Any]] = {}

        # 1. CLI
        cli_path = self._find_cli()
        if cli_path and self._probe_cli(cli_path):
            methods[ControlMethod.CLI] = {"path": cli_path}

        # 2. REST API
        if self._probe_rest():
            methods[ControlMethod.REST] = {
                "base_url": _REST_BASE,
                "api_key": self.rest_api_key,
            }

        # 3. URI scheme — always available on macOS
        if sys.platform == "darwin":
            methods[ControlMethod.URI] = {}

        return methods

    def _get_methods(self) -> dict[ControlMethod, dict[str, Any]]:
        """Return cached detection results, probing if needed."""
        if self._detected is None:
            self._detected = self._detect_methods()
        return self._detected

    def _best_method(self) -> ControlMethod | None:
        """Return the best available control method."""
        if self.preferred_method and self.preferred_method in self._get_methods():
            return self.preferred_method

        # Detection order: REST > CLI > URI
        for method in (ControlMethod.REST, ControlMethod.CLI, ControlMethod.URI):
            if method in self._get_methods():
                return method

        return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def check_obsidian(self) -> dict[str, Any]:
        """Probe available control methods.

        Returns::

            {
                "running": True/False,
                "methods": ["cli", "rest", "uri"],
                "best": "cli" | "rest" | "uri" | None,
                "details": {
                    "cli": {"path": "/Applications/..."},
                    "rest": {"base_url": "https://..."},
                    "uri": {},
                }
            }
        """
        # Force re-detection
        self._detected = None
        methods = self._get_methods()

        best = self._best_method()

        return {
            "running": len(methods) > 0,
            "methods": [m.value for m in methods],
            "best": best.value if best else None,
            "details": {m.value: d for m, d in methods.items()},
        }

    def open(
        self,
        canvas_path: str | Path,
        *,
        open_in: Literal["active", "new_tab", "new_window"] = "new_tab",
    ) -> bool:
        """Open a canvas file via the best available method.

        Args:
            canvas_path: Vault-relative path to the .canvas file.
            open_in: Where to open the canvas. ``"active"`` replaces the
                active leaf (legacy behavior); ``"new_tab"`` opens in a new
                leaf; ``"new_window"`` opens in a new window where supported.
                Default ``"new_tab"`` — silent active-leaf clobber on
                sequential opens is a load-bearing bug, so the default
                changed at v1.0.1. ``"new_window"`` falls back to
                ``"new_tab"`` on the REST path because the Obsidian Local
                REST API plugin does not expose a new-window flag; CLI and
                URI scheme paths inherit the platform default.

        Returns:
            True if the open command was issued successfully.

        Raises:
            RuntimeError: If no control method is available.
        """
        canvas_path = str(canvas_path)
        new_leaf = open_in != "active"

        best = self._best_method()
        if best is None:
            raise RuntimeError(
                "No Obsidian control method available. "
                "Ensure Obsidian is running or URI scheme is registered."
            )

        # Try the best method, fall back through the chain
        methods_to_try = [best]
        for m in (ControlMethod.REST, ControlMethod.CLI, ControlMethod.URI):
            if m != best and m in self._get_methods():
                methods_to_try.append(m)

        for method in methods_to_try:
            success = self._open_via(method, canvas_path, new_leaf=new_leaf)
            if success:
                return True

        return False

    def open_batch(
        self,
        canvas_paths: list[str | Path],
        delay: float = 0.5,
        *,
        open_in: Literal["active", "new_tab", "new_window"] = "new_tab",
    ) -> dict[str, Any]:
        """Open multiple canvas files sequentially.

        Args:
            canvas_paths: List of vault-relative paths.
            delay: Seconds between opens to avoid overwhelming Obsidian.
            open_in: See ``open()``. Default ``"new_tab"`` so all canvases
                stay visible in separate leaves — the original v1.0 default
                silently clobbered the active leaf, hiding everything but
                the last opened canvas.

        Returns::

            {"opened": ["path1.canvas", ...], "failed": ["path2.canvas", ...]}
        """
        opened: list[str] = []
        failed: list[str] = []

        for i, path in enumerate(canvas_paths):
            path_str = str(path)
            try:
                if self.open(path_str, open_in=open_in):
                    opened.append(path_str)
                else:
                    failed.append(path_str)
            except RuntimeError:
                failed.append(path_str)

            # Delay between opens (but not after the last one)
            if delay > 0 and i < len(canvas_paths) - 1:
                time.sleep(delay)

        return {"opened": opened, "failed": failed}

    def deliver(
        self,
        canvas_dict: dict[str, Any],
        destination_path: str | Path,
        overwrite: bool = False,
        backup: bool = True,
        open_after: bool = True,
        *,
        open_in: Literal["active", "new_tab", "new_window"] = "new_tab",
    ) -> Path:
        """Write canvas JSON to vault and optionally open it.

        Args:
            canvas_dict: Canvas data (from CanvasBuilder.build()).
            destination_path: Vault-relative path for the .canvas file.
            overwrite: If False, raise FileExistsError when file exists.
            backup: If True, back up existing file before overwriting.
            open_after: If True, open the canvas after writing.
            open_in: See ``open()``. Default ``"new_tab"``.

        Returns:
            Absolute path to the written file.

        Raises:
            ValueError: If path resolves outside vault root.
            FileExistsError: If file exists and overwrite=False.
        """
        dest = self._validate_path(destination_path)

        # Handle existing file
        if dest.exists():
            if not overwrite:
                raise FileExistsError(
                    f"Canvas already exists: {dest}. Set overwrite=True to replace."
                )
            if backup:
                self._backup_file(dest)

        # Write canvas JSON
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(canvas_dict, indent=2) + "\n")

        # Open in Obsidian
        if open_after:
            vault_rel = str(dest.relative_to(self.vault_root))
            best = self._best_method()
            if best == ControlMethod.URI:
                time.sleep(0.5)  # Allow Obsidian file watcher to index new file
            try:
                self.open(vault_rel, open_in=open_in)
            except RuntimeError:
                pass  # Delivery succeeded even if open fails

        return dest

    def deliver_batch(
        self,
        deliveries: list[dict[str, Any]],
        overwrite: bool = False,
        backup: bool = True,
        open_after: bool = True,
        delay: float = 0.5,
        *,
        open_in: Literal["active", "new_tab", "new_window"] = "new_tab",
    ) -> dict[str, Any]:
        """Deliver multiple canvases.

        Args:
            deliveries: List of dicts with keys:
                - ``canvas_dict``: Canvas data
                - ``destination_path``: Vault-relative path
            overwrite: Default overwrite setting.
            backup: Default backup setting.
            open_after: Default open_after setting.
            delay: Seconds between deliveries.
            open_in: See ``open()``. Default ``"new_tab"`` so all delivered
                canvases stay visible in separate leaves.

        Returns::

            {"delivered": ["path1.canvas", ...], "failed": [{"path": "...", "error": "..."}]}
        """
        delivered: list[str] = []
        failed: list[dict[str, str]] = []

        for i, delivery in enumerate(deliveries):
            path_str = str(delivery["destination_path"])
            try:
                self.deliver(
                    canvas_dict=delivery["canvas_dict"],
                    destination_path=delivery["destination_path"],
                    overwrite=overwrite,
                    backup=backup,
                    open_after=open_after,
                    open_in=open_in,
                )
                delivered.append(path_str)
            except Exception as e:
                failed.append({"path": path_str, "error": str(e)})

            if delay > 0 and i < len(deliveries) - 1:
                time.sleep(delay)

        return {"delivered": delivered, "failed": failed}

    # ------------------------------------------------------------------
    # Control Method Implementations
    # ------------------------------------------------------------------

    def _open_via(
        self,
        method: ControlMethod,
        canvas_path: str,
        new_leaf: bool = True,
    ) -> bool:
        """Open a canvas using a specific control method.

        ``new_leaf`` is honored by REST (``?newLeaf=<bool>`` query parameter).
        CLI and URI scheme paths inherit the platform default (which on macOS
        already opens a new tab); the asymmetry is intentional — see ``open()``
        docstring for the open_in→new_leaf mapping.
        """
        if method == ControlMethod.CLI:
            return self._open_cli(canvas_path)
        elif method == ControlMethod.REST:
            return self._open_rest(canvas_path, new_leaf=new_leaf)
        elif method == ControlMethod.URI:
            return self._open_uri(canvas_path)
        return False

    def _open_cli(self, canvas_path: str) -> bool:
        """Open canvas via Obsidian CLI."""
        details = self._get_methods().get(ControlMethod.CLI)
        if not details:
            return False

        try:
            result = subprocess.run(
                [details["path"], "open", f"path={canvas_path}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

    def _open_rest(self, canvas_path: str, new_leaf: bool = True) -> bool:
        """Open canvas via REST API by executing the open command.

        ``new_leaf=True`` adds ``?newLeaf=true`` so the Obsidian REST plugin
        opens the link in a new leaf instead of replacing the active leaf.
        Default ``True`` because silent active-leaf clobber on sequential
        opens is a load-bearing bug for side-by-side review workflows.
        """
        details = self._get_methods().get(ControlMethod.REST)
        if not details:
            return False

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Use the REST API's /open/{path} endpoint, which calls
        # app.workspace.openLinkText() internally. The ?newLeaf flag tells
        # openLinkText() to open in a new leaf instead of the active one.
        encoded_path = urllib.parse.quote(canvas_path, safe="")
        new_leaf_str = "true" if new_leaf else "false"
        url = f"{_REST_BASE}/open/{encoded_path}?newLeaf={new_leaf_str}"

        req = urllib.request.Request(
            url,
            method="POST",
            headers={
                "Authorization": f"Bearer {details['api_key']}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=_REST_TIMEOUT, context=ctx) as resp:
                return resp.status == 200
        except (urllib.error.URLError, OSError, TimeoutError):
            return False

    def _open_uri(self, canvas_path: str) -> bool:
        """Open canvas via obsidian:// URI scheme."""
        # Build URI: obsidian://open?vault=NAME&file=PATH
        params = urllib.parse.urlencode(
            {
                "vault": self.vault_name,
                "file": canvas_path,
            }
        )
        uri = f"obsidian://open?{params}"

        try:
            if sys.platform == "darwin":
                result = subprocess.run(
                    ["open", uri],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                return result.returncode == 0
            elif sys.platform == "linux":
                result = subprocess.run(
                    ["xdg-open", uri],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                return result.returncode == 0
            elif sys.platform == "win32":
                result = subprocess.run(
                    ["cmd", "/c", "start", "", uri],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    shell=False,
                )
                return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

        return False

    # ------------------------------------------------------------------
    # Path Validation
    # ------------------------------------------------------------------

    def _validate_path(self, relative_path: str | Path) -> Path:
        """Resolve a vault-relative path and verify it stays within vault root.

        Args:
            relative_path: Path relative to vault root.

        Returns:
            Absolute resolved path.

        Raises:
            ValueError: If resolved path escapes vault root.
        """
        # Resolve the full path
        full = (self.vault_root / relative_path).resolve()

        # Path traversal check
        if not str(full).startswith(str(self.vault_root)):
            raise ValueError(
                f"Path escapes vault root: {relative_path!r} "
                f"resolves to {full}, outside {self.vault_root}"
            )

        return full

    def _backup_file(self, path: Path) -> Path:
        """Create a timestamped backup of an existing file.

        Returns:
            Path to the backup file.
        """
        stem = path.stem
        suffix = path.suffix
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_name = f"{stem}_backup_{timestamp}{suffix}"
        backup_path = path.parent / backup_name
        shutil.copy2(path, backup_path)
        return backup_path

    # ------------------------------------------------------------------
    # URI Encoding Helper
    # ------------------------------------------------------------------

    @staticmethod
    def build_obsidian_uri(
        vault_name: str,
        file_path: str,
    ) -> str:
        """Build an obsidian:// URI for opening a file.

        Args:
            vault_name: Obsidian vault name.
            file_path: Vault-relative file path.

        Returns:
            Properly encoded obsidian:// URI string.
        """
        params = urllib.parse.urlencode(
            {
                "vault": vault_name,
                "file": file_path,
            }
        )
        return f"obsidian://open?{params}"
