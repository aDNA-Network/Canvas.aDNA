"""Pure-Python PNG helpers — dimension reads and deterministic solid-color writes.

Exists so the bridge NEVER imports PIL (boundary: PIL only via ``canvas_core.print``). The fake
backend writes real, valid PNGs with ``struct`` + ``zlib`` only; the validate stage reads IHDR
dimensions the same way for the effective-DPI check.
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_png_size(path: str | Path) -> tuple[int, int]:
    """Return ``(width, height)`` from a PNG's IHDR chunk. Raises ``ValueError`` on non-PNG."""
    data = Path(path).read_bytes()
    if len(data) < 33 or not data.startswith(_PNG_SIGNATURE) or data[12:16] != b"IHDR":
        raise ValueError(f"not a PNG file: {path}")
    width, height = struct.unpack(">II", data[16:24])
    return int(width), int(height)


def _chunk(tag: bytes, payload: bytes) -> bytes:
    body = tag + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def write_solid_png(path: str | Path, width: int, height: int, rgb: tuple[int, int, int]) -> Path:
    """Write a valid 8-bit RGB PNG filled with ``rgb``. Deterministic byte-for-byte."""
    if width <= 0 or height <= 0:
        raise ValueError(f"invalid PNG dimensions {width}x{height}")
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit, truecolor RGB
    row = b"\x00" + bytes(rgb) * width  # filter byte 0 per scanline
    idat = zlib.compress(row * height, level=6)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(_PNG_SIGNATURE + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b""))
    return out
