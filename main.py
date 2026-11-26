#!/usr/bin/env python3
"""news-image-20261125 v3 entrypoint: write the finished newspaper image to /output/entry.png.

The image is rendered once from build/index.html (HTML + CSS + hand-drawn data charts
and a real world-map outline from Natural Earth / world-atlas land-110m) and committed
as entry.png; this program only copies it to the output directory, verifying its
SHA-256 first so a corrupt or swapped file can never be submitted.
Runs with no network. Two runs write the same bytes.
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "d4a89ab5f0dfcbcb0f695fca02103ea69913b35b97bd5b05b844971d3356e90d"

# Competition caps (RULES.txt): PNG or JPEG, at most 1 MiB, at most 1024x1024 px.
MAX_BYTES = 1048576
MAX_DIMENSION = 1024

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def png_dimensions(data: bytes) -> tuple:
    """Read width/height from a PNG IHDR chunk; raises ValueError if not a PNG."""
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk where expected")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def png_complete(data: bytes) -> None:
    """Walk the PNG chunk chain and confirm the file ends exactly at the IEND chunk.

    A truncated render or a stray trailing byte would otherwise pass the hash
    check only if the hash matched too; this catches a structurally incomplete
    file even before the hash is compared. Raises ValueError on any defect.
    """
    pos = 8  # skip the 8-byte PNG signature
    seen_iend = False
    while pos + 8 <= len(data):
        length = int.from_bytes(data[pos:pos + 4], "big")
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4  # length + type + data + CRC
        if end > len(data):
            raise ValueError(f"entry.png chunk {ctype!r} runs past the end of the file")
        if ctype == b"IEND":
            if length != 0:
                raise ValueError("entry.png IEND chunk must be empty")
            if end != len(data):
                raise ValueError("entry.png has trailing bytes after the IEND chunk")
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        raise ValueError("entry.png has no IEND chunk: file is truncated")


def main() -> int:
    with open(SRC, "rb") as f:
        data = f.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"entry.png sha256 mismatch: got {digest}, expected {EXPECTED_SHA256}", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png too large: {len(data)} bytes (cap {MAX_BYTES})", file=sys.stderr)
        return 1
    try:
        png_complete(data)
        width, height = png_dimensions(data)
    except ValueError as e:
        print(f"entry.png rejected: {e}", file=sys.stderr)
        return 1
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        print(f"entry.png too big: {width}x{height} (cap {MAX_DIMENSION}x{MAX_DIMENSION})", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    with open(DST, "rb") as f:
        written = f.read()
    if written != data:
        print("output entry.png does not match the verified source bytes", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
