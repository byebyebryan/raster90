#!/usr/bin/env python3
"""Generate and check the deterministic Raster 90 font-family presentation.

The source matrices live in ``fonts/raster90/family.py``. This tool maintains
the tracked presentation beneath ``fonts/raster90/preview/``:

    python3 -B tools/render_raster90_font_family.py
    python3 -B tools/render_raster90_font_family.py --check

Everything is standard-library-only.  The HTML embeds both the generated PNG
artifacts and the source matrices, so it remains useful when opened directly
from a local checkout with no network or browser dependency.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import html
import json
import struct
import sys
import zlib
from pathlib import Path
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "design" / "raster90"))
sys.path.insert(0, str(ROOT / "tools"))

from fonts.raster90.family import (  # noqa: E402
    PRIMARY_COLON,
    PRIMARY_DIGIT_CELLS,
    PRIMARY_DIGITS,
    PRIMARY_LINE_CELLS,
    SECONDARY_GLYPHS,
    SECONDARY_KEYS,
)
import generate_raster90_assets as runtime_assets  # noqa: E402


RGBA = tuple[int, int, int, int]
PixelGrid = list[list[RGBA]]

BLACK: RGBA = (0, 0, 0, 255)
WHITE: RGBA = (255, 255, 255, 255)
OUTPUT_DIR_REL = Path("fonts/raster90/preview")

# Interactive preview line boxes include one source-cell of vertical breathing
# room above and below each cut.  Keep these metrics explicit so the generated
# JavaScript cannot accidentally use the secondary 9-cell line for the
# 32-cell primary display cut.
PREVIEW_GEOMETRY = {
    "primary": {"glyphCells": PRIMARY_LINE_CELLS, "lineCells": PRIMARY_LINE_CELLS + 2},
    "secondary": {"glyphCells": 7, "lineCells": 9},
}

PRIMARY_SHEET_NAME = "primary-display-cut.png"
SECONDARY_SHEET_NAME = "secondary-text-cut.png"
FAMILY_SHEET_NAME = "family-specimen.png"
NATIVE_FACE_NAME = "family-native-face-466.png"
INSPECTION_NAME = "primary-magnified-inspection.png"
HTML_NAME = "index.html"


def preview_line_metrics(cut: str, scale: int) -> dict[str, int]:
    """Return cut-aware source-cell geometry for the interactive preview."""

    if cut not in PREVIEW_GEOMETRY:
        raise ValueError(f"unknown preview cut: {cut!r}")
    if scale < 1:
        raise ValueError("preview scale must be positive")
    geometry = PREVIEW_GEOMETRY[cut]
    return {
        "glyph_height": geometry["glyphCells"] * scale,
        "line_height": geometry["lineCells"] * scale,
    }


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = binascii.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)


def encode_png(pixels: PixelGrid) -> bytes:
    """Encode an opaque RGBA grid with deterministic filter-zero scanlines."""

    if not pixels or not pixels[0]:
        raise ValueError("cannot encode an empty PNG")
    width = len(pixels[0])
    height = len(pixels)
    if any(len(row) != width for row in pixels):
        raise ValueError("pixel rows have inconsistent widths")
    raw = bytearray()
    for row in pixels:
        raw.append(0)
        for pixel in row:
            raw.extend(pixel)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", ihdr) + _png_chunk(
        b"IDAT", zlib.compress(bytes(raw), level=9)
    ) + _png_chunk(b"IEND", b"")


def _blank(width: int, height: int, fill: RGBA = BLACK) -> PixelGrid:
    return [[fill for _x in range(width)] for _y in range(height)]


def _paint_matrix(
    pixels: PixelGrid,
    rows: Sequence[str],
    *,
    x: int,
    y: int,
    scale: int,
) -> None:
    for source_y, row in enumerate(rows):
        for source_x, symbol in enumerate(row):
            if symbol != "1":
                continue
            for target_y in range(y + source_y * scale, y + (source_y + 1) * scale):
                for target_x in range(x + source_x * scale, x + (source_x + 1) * scale):
                    if 0 <= target_y < len(pixels) and 0 <= target_x < len(pixels[0]):
                        pixels[target_y][target_x] = WHITE


def _outline(pixels: PixelGrid, *, x: int, y: int, width: int, height: int) -> None:
    """Add a quiet white tile outline around a review-sheet cell."""

    right = x + width - 1
    bottom = y + height - 1
    for target_x in range(x, right + 1):
        if 0 <= y < len(pixels) and 0 <= target_x < len(pixels[0]):
            pixels[y][target_x] = WHITE
        if 0 <= bottom < len(pixels) and 0 <= target_x < len(pixels[0]):
            pixels[bottom][target_x] = WHITE
    for target_y in range(y, bottom + 1):
        if 0 <= target_y < len(pixels) and 0 <= x < len(pixels[0]):
            pixels[target_y][x] = WHITE
        if 0 <= target_y < len(pixels) and 0 <= right < len(pixels[0]):
            pixels[target_y][right] = WHITE


def render_primary_sheet(*, scale: int = 3) -> PixelGrid:
    """Render every primary glyph at the selected solid-cell scale."""

    gap = 4 * scale
    widths = [PRIMARY_DIGIT_CELLS * scale] * 10 + [len(PRIMARY_COLON[0]) * scale]
    width = sum(widths) + gap * (len(widths) + 1)
    height = PRIMARY_LINE_CELLS * scale + 2 * gap
    pixels = _blank(width, height)
    x = gap
    for digit in "0123456789":
        _outline(pixels, x=x, y=gap, width=widths[int(digit)], height=PRIMARY_LINE_CELLS * scale)
        _paint_matrix(pixels, PRIMARY_DIGITS[digit], x=x, y=gap, scale=scale)
        x += widths[int(digit)] + gap
    _outline(pixels, x=x, y=gap, width=widths[-1], height=PRIMARY_LINE_CELLS * scale)
    _paint_matrix(pixels, PRIMARY_COLON, x=x, y=gap, scale=scale)
    return pixels


def render_secondary_sheet(*, scale: int = 3) -> PixelGrid:
    """Render the complete secondary source vocabulary in a stable grid."""

    columns = 16
    tile_width = 10 * scale
    tile_height = 12 * scale
    gap = scale
    rows = (len(SECONDARY_KEYS) + columns - 1) // columns
    width = columns * tile_width + (columns + 1) * gap
    height = rows * tile_height + (rows + 1) * gap
    pixels = _blank(width, height)
    for index, character in enumerate(SECONDARY_KEYS):
        column = index % columns
        row = index // columns
        x = gap + column * (tile_width + gap)
        y = gap + row * (tile_height + gap)
        _outline(pixels, x=x, y=y, width=tile_width, height=tile_height)
        glyph_width = len(SECONDARY_GLYPHS[character][0]) * scale
        glyph_height = len(SECONDARY_GLYPHS[character]) * scale
        _paint_matrix(
            pixels,
            SECONDARY_GLYPHS[character],
            x=x + (tile_width - glyph_width) // 2,
            y=y + (tile_height - glyph_height) // 2,
            scale=scale,
        )
    return pixels


def render_family_sheet(*, scale: int = 3) -> PixelGrid:
    """Compose primary and complete secondary cuts into one native-scale sheet."""

    primary = render_primary_sheet(scale=scale)
    secondary = render_secondary_sheet(scale=scale)
    gap = 8 * scale
    width = max(len(primary[0]), len(secondary[0]))
    height = len(primary) + gap + len(secondary)
    pixels = _blank(width, height)
    for source, y in ((primary, 0), (secondary, len(primary) + gap)):
        for row_index, row in enumerate(source):
            pixels[y + row_index][: len(row)] = row
    return pixels


def render_primary_inspection() -> PixelGrid:
    """Render a large primary strip for close inspection of the chamfers."""

    return render_primary_sheet(scale=9)


def _json_data() -> dict[str, object]:
    return {
        "primary": {
            "digits": {digit: list(PRIMARY_DIGITS[digit]) for digit in "0123456789"},
            "colon": list(PRIMARY_COLON),
        },
        "secondary": {
            character: list(SECONDARY_GLYPHS[character]) for character in SECONDARY_KEYS
        },
        "runtimeSecondary": list(runtime_assets.FINE_GLYPHS),
    }


def _safe_json(value: object) -> str:
    """Serialize data for a script block without introducing HTML/script edges."""

    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def _matrix_markup(name: str, rows: Sequence[str]) -> str:
    escaped_name = html.escape(name, quote=True)
    body = html.escape("\n".join(rows), quote=False)
    return (
        f'<figure class="glyph-card"><figcaption><code>{escaped_name}</code>'
        f' <span class="dimensions">{len(rows[0])}×{len(rows)}</span></figcaption>'
        f'<pre aria-label="{escaped_name} matrix">{body}</pre></figure>'
    )


def render_html(images: Mapping[str, bytes]) -> bytes:
    """Build the self-contained local overview/preview document."""

    image_data = {
        name: "data:image/png;base64," + base64.b64encode(data).decode("ascii")
        for name, data in images.items()
        if name.endswith(".png")
    }
    primary_cards = "".join(
        _matrix_markup(digit, PRIMARY_DIGITS[digit]) for digit in "0123456789"
    ) + _matrix_markup(":", PRIMARY_COLON)
    secondary_cards = "".join(
        _matrix_markup(character, SECONDARY_GLYPHS[character]) for character in SECONDARY_KEYS
    )
    data_script = _safe_json(_json_data())
    native_src = image_data[NATIVE_FACE_NAME]
    inspection_src = image_data[INSPECTION_NAME]
    family_src = image_data[FAMILY_SHEET_NAME]
    primary_src = image_data[PRIMARY_SHEET_NAME]
    secondary_src = image_data[SECONDARY_SHEET_NAME]
    preview_geometry = _safe_json(PREVIEW_GEOMETRY)

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Raster 90 bitmap font family</title>
<style>
:root {{ color-scheme: dark; background: #000; color: #fff; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
body {{ max-width: 1180px; margin: 0 auto; padding: 2rem; background: #000; color: #fff; line-height: 1.45; }}
h1, h2, h3 {{ line-height: 1.15; }}
code, pre, textarea, input, select {{ font: inherit; }}
code, pre {{ color: #fff; }}
.lede, .contract {{ max-width: 78ch; }}
.contract {{ border-left: 3px solid #fff; padding-left: 1rem; }}
.artifact {{ max-width: 100%; height: auto; image-rendering: pixelated; background: #000; border: 1px solid #fff; }}
.scroll {{ overflow-x: auto; background: #000; padding: .5rem; }}
.glyph-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(8rem, 1fr)); gap: .75rem; }}
.glyph-card {{ margin: 0; border: 1px solid #fff; padding: .6rem; background: #000; }}
.glyph-card figcaption {{ display: flex; justify-content: space-between; gap: .5rem; }}
.glyph-card pre {{ margin: .5rem 0 0; font-size: .8rem; line-height: 1; letter-spacing: .08em; overflow: auto; }}
.dimensions {{ opacity: .75; font-size: .75rem; }}
.controls {{ display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; border: 1px solid #fff; padding: 1rem; }}
textarea {{ width: min(100%, 54rem); min-height: 5rem; background: #000; color: #fff; border: 1px solid #fff; padding: .5rem; }}
input, select {{ accent-color: #fff; background: #000; color: #fff; }}
canvas {{ display: block; max-width: 100%; height: auto; image-rendering: pixelated; border: 1px solid #fff; }}
.sr-only {{ position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }}
noscript {{ display: block; border: 1px solid #fff; padding: 1rem; }}
</style>
</head>
<body>
<header>
<h1>Raster 90 bitmap font family</h1>
<p class="lede">Approved project-owned two-cut family for the one solid 3×3 source-cell grid. This page is generated from the authoritative matrices and has no network or runtime-font dependency.</p>
</header>
<main>
<section class="contract" aria-labelledby="contract-heading">
<h2 id="contract-heading">Design contract</h2>
<ul>
<li>Primary/display cut: dense fixed-width 0–9 plus colon, one-cell convex-corner chamfer, plain closed zero, 26×32 digit boxes and 10×32 colon box.</li>
<li>Secondary/text cut: complete 5×7 space, symbols, digits, uppercase, lowercase, and common punctuation vocabulary.</li>
<li>All lit source cells expand to solid 3×3 squares. No glow, gradient, antialiasing, or downloaded runtime font is used.</li>
<li>The APK packages only the secondary glyphs current WFF expressions can emit; this page intentionally shows the complete source-only surface.</li>
</ul>
</section>
<section aria-labelledby="artifacts-heading">
<h2 id="artifacts-heading">Generated specimens</h2>
<p>Native 3×3 family sheet:</p><div class="scroll"><img class="artifact" src="{family_src}" alt="Raster 90 primary and complete secondary family sheet at native 3x3 scale"></div>
<p>Native 466×466 face preview using the selected runtime primary cut:</p><div class="scroll"><img class="artifact" src="{native_src}" alt="Raster 90 face with chamfered 10:08 time and information rows"></div>
<p>Magnified primary inspection:</p><div class="scroll"><img class="artifact" src="{inspection_src}" alt="Magnified primary digits and colon showing one-cell corner chamfers"></div>
<p>Separate primary sheet:</p><div class="scroll"><img class="artifact" src="{primary_src}" alt="Complete primary digits zero through nine and colon"></div>
<p>Separate secondary sheet:</p><div class="scroll"><img class="artifact" src="{secondary_src}" alt="Complete secondary text glyph surface"></div>
</section>
<section aria-labelledby="interactive-heading">
<h2 id="interactive-heading">Interactive local preview</h2>
<div class="controls">
<label for="cut">Cut <select id="cut"><option value="secondary">Secondary/text</option><option value="primary">Primary/display</option></select></label>
<label for="scale">Cell scale <input id="scale" type="range" min="3" max="15" value="6"><output id="scale-output" for="scale">6×</output></label>
</div>
<label for="preview-text">Preview text</label>
<textarea id="preview-text" spellcheck="false">10:08
21°C  SAT 15 AUG
03642  82%
--</textarea>
<canvas id="preview" width="600" height="220" role="img" aria-label="Interactive Raster 90 bitmap font preview"></canvas>
<noscript>JavaScript is disabled. The generated sheets and complete matrix cards above remain available.</noscript>
</section>
<section aria-labelledby="primary-heading">
<h2 id="primary-heading">Complete primary/display matrix surface</h2>
<div class="glyph-grid">{primary_cards}</div>
</section>
<section aria-labelledby="secondary-heading">
<h2 id="secondary-heading">Complete secondary/text matrix surface</h2>
<p>Runtime subset: <code>{html.escape(" ".join(runtime_assets.FINE_GLYPHS), quote=False)}</code></p>
<div class="glyph-grid">{secondary_cards}</div>
</section>
<section aria-labelledby="strings-heading">
<h2 id="strings-heading">Representative face strings</h2>
<p><code>10:08</code> · <code>21°C</code> · <code>SAT 15 AUG</code> · <code>03642</code> · <code>82%</code> · unavailable <code>--</code></p>
</section>
</main>
<script>
const FONT_DATA = {data_script};
const canvas = document.getElementById('preview');
const context = canvas.getContext('2d');
const textInput = document.getElementById('preview-text');
const cutInput = document.getElementById('cut');
const scaleInput = document.getElementById('scale');
const scaleOutput = document.getElementById('scale-output');
const PREVIEW_GEOMETRY = {preview_geometry};
function previewLineMetrics(cut, scale) {{
  const geometry = PREVIEW_GEOMETRY[cut] || PREVIEW_GEOMETRY.secondary;
  return {{ glyphHeight: geometry.glyphCells * scale, lineHeight: geometry.lineCells * scale }};
}}
function previewRows(source, cut, character) {{
  return cut === 'primary' ? (character === ':' ? source.colon : source.digits[character]) : source[character];
}}
function drawPreview() {{
  const scale = Number(scaleInput.value);
  const cut = cutInput.value;
  const source = cut === 'primary' ? FONT_DATA.primary : FONT_DATA.secondary;
  const metrics = previewLineMetrics(cut, scale);
  const lines = textInput.value.split('\\n');
  const margin = 3 * scale;
  const widths = lines.map(line => [...line].reduce((sum, character) => {{
    const rows = previewRows(source, cut, character);
    return rows ? sum + rows[0].length * scale + scale : sum;
  }}, 0));
  canvas.width = Math.max(320, Math.max(...widths, 0) + margin * 2);
  canvas.height = Math.max(120, lines.length * metrics.lineHeight + margin * 2);
  context.fillStyle = '#000';
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = '#fff';
  lines.forEach((line, lineIndex) => {{
    let x = margin;
    const y = margin + lineIndex * metrics.lineHeight + Math.max(0, (metrics.lineHeight - metrics.glyphHeight) / 2);
    for (const character of [...line]) {{
      const rows = previewRows(source, cut, character);
      if (!rows) {{ continue; }}
      rows.forEach((row, rowIndex) => [...row].forEach((cell, cellIndex) => {{
        if (cell === '1') context.fillRect(x + cellIndex * scale, y + rowIndex * scale, scale, scale);
      }}));
      x += rows[0].length * scale + scale;
    }}
  }});
  scaleOutput.value = `${{scale}}×`;
}}
[textInput, cutInput, scaleInput].forEach(element => element.addEventListener('input', drawPreview));
drawPreview();
</script>
</body>
</html>
"""
    return document.encode("utf-8")


def _expected_outputs() -> dict[str, bytes]:
    images = {
        PRIMARY_SHEET_NAME: encode_png(render_primary_sheet()),
        SECONDARY_SHEET_NAME: encode_png(render_secondary_sheet()),
        FAMILY_SHEET_NAME: encode_png(render_family_sheet()),
        NATIVE_FACE_NAME: encode_png(runtime_assets._preview_pixels()),
        INSPECTION_NAME: encode_png(render_primary_inspection()),
    }
    return {**images, HTML_NAME: render_html(images)}


def _validate_expected(root: Path, expected: Mapping[str, bytes]) -> None:
    output_dir = root / OUTPUT_DIR_REL
    if not output_dir.is_dir():
        raise ValueError(f"font output directory is missing: {output_dir}")
    actual = {path.name for path in output_dir.iterdir() if path.is_file()}
    missing = sorted(set(expected) - actual)
    extra = sorted(actual - set(expected))
    if missing:
        raise ValueError("missing font presentation outputs: " + ", ".join(missing))
    if extra:
        raise ValueError("unexpected font presentation outputs: " + ", ".join(extra))
    for name, data in sorted(expected.items()):
        path = output_dir / name
        if path.read_bytes() != data:
            raise ValueError(f"font presentation drift detected: {path}")


def _write_expected(root: Path, expected: Mapping[str, bytes]) -> int:
    output_dir = root / OUTPUT_DIR_REL
    output_dir.mkdir(parents=True, exist_ok=True)
    changed = 0
    for name, data in sorted(expected.items()):
        path = output_dir / name
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
            changed += 1
    return changed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify outputs without writing")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    expected = _expected_outputs()
    try:
        if args.check:
            _validate_expected(root, expected)
            print(f"Raster 90 font presentation OK: {len(expected)} outputs")
        else:
            changed = _write_expected(root, expected)
            _validate_expected(root, expected)
            print(f"Raster 90 font presentation generated: {len(expected)} outputs ({changed} changed)")
    except (OSError, ValueError, struct.error, zlib.error) as error:
        print(f"Raster 90 font presentation check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
