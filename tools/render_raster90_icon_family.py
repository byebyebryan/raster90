#!/usr/bin/env python3
"""Generate and check the tracked Raster 90 icon-family presentation.

The canonical matrices live in ``icons/raster90/family.py``. This tool writes
only the reviewable presentation beneath ``icons/raster90/preview/``:

    python3 -B tools/render_raster90_icon_family.py
    python3 -B tools/render_raster90_icon_family.py --check

The HTML embeds every generated PNG and the source matrices, so the component
remains useful when opened directly from a checkout without a network or
browser dependency beyond local file rendering.
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
from typing import Callable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from fonts.raster90.family import SECONDARY_GLYPHS  # noqa: E402
from icons.raster90.family import (  # noqa: E402
    APPROVED_STEP_ICON,
    BATTERY_ICON,
    PALETTE,
    SELECTED_UTILITY_ICONS,
    STALE_MARKER,
    UNAVAILABLE_WEATHER_ICON,
    WEATHER_CONDITIONS,
    WEATHER_DAY,
    WEATHER_NIGHT,
)
import generate_raster90_assets as runtime_assets  # noqa: E402


RGBA = tuple[int, int, int, int]
PixelGrid = list[list[RGBA]]
ColorFor = Callable[[str], RGBA]

BLACK: RGBA = (0, 0, 0, 255)
WHITE: RGBA = (255, 255, 255, 255)
TRANSPARENT: RGBA = (0, 0, 0, 0)
OUTPUT_DIR_REL = Path("icons/raster90/preview")

UTILITY_SHEET_NAME = "icon-family-utility-sheet.png"
WEATHER_SHEET_NAME = "icon-family-weather-day-night-sheet.png"
STATE_SHEET_NAME = "icon-family-unavailable-stale-sheet.png"
MATRIX_SHEET_NAME = "icon-family-matrix-3x3-inspection.png"
NATIVE_FACE_NAME = "icon-family-native-face-466.png"
MAGNIFIED_FACE_NAME = "icon-family-magnified-face-932.png"
HTML_NAME = "index.html"

UTILITY_LABELS = {"steps": "STEPS", "battery": "BATTERY"}


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = binascii.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)


def encode_png(pixels: PixelGrid) -> bytes:
    """Encode an opaque RGBA grid using deterministic filter-zero scanlines."""

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


def _set_pixel(pixels: PixelGrid, x: int, y: int, color: RGBA) -> None:
    if 0 <= y < len(pixels) and 0 <= x < len(pixels[0]):
        pixels[y][x] = color


def _draw_matrix(
    pixels: PixelGrid,
    rows: Sequence[str],
    *,
    x: int,
    y: int,
    pitch: int,
    lit: int,
    color_for: ColorFor,
) -> None:
    for source_y, row in enumerate(rows):
        for source_x, symbol in enumerate(row):
            if symbol in ("0", "."):
                continue
            color = color_for(symbol)
            for target_y in range(y + source_y * pitch, y + source_y * pitch + lit):
                for target_x in range(x + source_x * pitch, x + source_x * pitch + lit):
                    _set_pixel(pixels, target_x, target_y, color)


def _draw_text(pixels: PixelGrid, text: str, *, x: int, y: int, scale: int = 3) -> None:
    """Draw compact labels from the project-owned 5x7 text family."""

    cursor = x
    for character in text:
        try:
            rows = SECONDARY_GLYPHS[character]
        except KeyError as error:
            raise ValueError(f"presentation label uses undefined glyph {character!r}") from error
        _draw_matrix(
            pixels,
            rows,
            x=cursor,
            y=y,
            pitch=scale,
            lit=scale,
            color_for=lambda _symbol: WHITE,
        )
        cursor += (2 if character == " " else 6) * scale


def _weather_color(symbol: str) -> RGBA:
    try:
        return PALETTE[symbol]
    except KeyError as error:
        raise ValueError(f"unknown weather palette symbol {symbol!r}") from error


def _utility_color(_symbol: str) -> RGBA:
    return WHITE


def _scale_nearest(source: PixelGrid, factor: int) -> PixelGrid:
    if factor < 1:
        raise ValueError("scale factor must be positive")
    return [
        [pixel for pixel in row for _x in range(factor)]
        for row in source
        for _y in range(factor)
    ]


def render_utility_sheet() -> PixelGrid:
    """Show selected utility matrices at source and solid 3x3 review scales."""

    width, height = 980, 420
    pixels = _blank(width, height)
    _draw_text(pixels, "RASTER 90 SELECTED UTILITY ICONS", x=24, y=24)
    _draw_text(pixels, "PROJECT-OWNED 16X16 MATRICES / SOLID 3X3 CELLS", x=24, y=54)
    for index, name in enumerate(("steps", "battery")):
        card_x = 24 + index * 470
        _draw_text(pixels, UTILITY_LABELS[name], x=card_x, y=110)
        rows = SELECTED_UTILITY_ICONS[name]
        _draw_matrix(
            pixels,
            rows,
            x=card_x,
            y=150,
            pitch=12,
            lit=12,
            color_for=_utility_color,
        )
        _draw_text(pixels, "16X16 SOURCE", x=card_x, y=350)
        _draw_matrix(
            pixels,
            rows,
            x=card_x + 250,
            y=150,
            pitch=3,
            lit=3,
            color_for=_utility_color,
        )
        _draw_text(pixels, "48X48 RUNTIME TILE", x=card_x + 250, y=350, scale=2)
    return pixels


def render_weather_sheet() -> PixelGrid:
    """Show every WFF condition as a day/night pair."""

    width = 1248
    card_width = 300
    card_height = 184
    title_height = 92
    rows_per_column = 4
    height = title_height + card_height * rows_per_column
    pixels = _blank(width, height)
    _draw_text(pixels, "RASTER 90 WEATHER FAMILY", x=24, y=18)
    _draw_text(pixels, "ALL 16 WFF CONDITIONS / DAY + NIGHT / TRUE 16X16", x=24, y=48)
    for condition, condition_name in enumerate(WEATHER_CONDITIONS):
        column = condition % 4
        row = condition // 4
        card_x = 24 + column * card_width
        card_y = title_height + row * card_height
        _draw_text(
            pixels,
            f"{condition:02d} {condition_name.replace('_', ' ').upper()}",
            x=card_x,
            y=card_y,
        )
        day_x = card_x + 18
        night_x = card_x + 170
        icon_y = card_y + 36
        _draw_matrix(
            pixels,
            WEATHER_DAY[condition],
            x=day_x,
            y=icon_y,
            pitch=4,
            lit=4,
            color_for=_weather_color,
        )
        _draw_matrix(
            pixels,
            WEATHER_NIGHT[condition],
            x=night_x,
            y=icon_y,
            pitch=4,
            lit=4,
            color_for=_weather_color,
        )
        _draw_text(pixels, "DAY", x=day_x + 10, y=icon_y + 70)
        _draw_text(pixels, "NIGHT", x=night_x + 2, y=icon_y + 70)
    return pixels


def render_state_sheet() -> PixelGrid:
    """Show truthful unavailable and stale treatments without semantic drift."""

    width, height = 1000, 420
    pixels = _blank(width, height)
    _draw_text(pixels, "TRUTHFUL WEATHER STATES", x=24, y=24)
    _draw_text(pixels, "NEUTRAL UNAVAILABLE ICON + -- / STALE MARKER", x=24, y=54)
    cards = (
        ("UNAVAILABLE", UNAVAILABLE_WEATHER_ICON, "--", False),
        ("AVAILABLE", WEATHER_DAY[14], "21°C", False),
        ("STALE", WEATHER_DAY[14], "21°C", True),
    )
    for index, (label, rows, value, stale) in enumerate(cards):
        card_x = 24 + index * 320
        _draw_text(pixels, label, x=card_x, y=118)
        _draw_matrix(
            pixels,
            rows,
            x=card_x,
            y=166,
            pitch=12,
            lit=12,
            color_for=_weather_color,
        )
        if stale:
            _draw_matrix(
                pixels,
                STALE_MARKER,
                x=card_x,
                y=166,
                pitch=12,
                lit=12,
                color_for=_utility_color,
            )
        _draw_text(pixels, value, x=card_x, y=370)
    return pixels


def render_matrix_sheet() -> PixelGrid:
    """Expose exact 16x16 cells beside their 3x3 physical rendering."""

    width, height = 1100, 520
    pixels = _blank(width, height)
    _draw_text(pixels, "MATRIX / PHYSICAL CELL INSPECTION", x=24, y=20)
    _draw_text(pixels, "SOURCE GRID IS 16X16; EVERY LIT CELL IS A SOLID 3X3", x=24, y=50)
    entries = (
        ("STEPS", APPROVED_STEP_ICON, _utility_color),
        ("BATTERY", BATTERY_ICON, _utility_color),
        ("WEATHER 14 DAY", WEATHER_DAY[14], _weather_color),
    )
    for index, (label, rows, color_for) in enumerate(entries):
        x = 24 + index * 350
        _draw_text(pixels, label, x=x, y=112)
        _draw_matrix(pixels, rows, x=x, y=154, pitch=12, lit=12, color_for=color_for)
        _draw_text(pixels, "16X16 / 12X REVIEW", x=x, y=362)
        _draw_matrix(pixels, rows, x=x + 196, y=154, pitch=3, lit=3, color_for=color_for)
        _draw_text(pixels, "3X3 CELLS", x=x + 196, y=220)
    # An isolated calibration strip makes solid-cell boundaries unambiguous.
    _draw_text(pixels, "CELL CALIBRATION", x=24, y=424)
    calibration = ("100010001000", "000000000000", "111111111111")
    _draw_matrix(
        pixels,
        calibration,
        x=240,
        y=460,
        pitch=12,
        lit=12,
        color_for=_utility_color,
    )
    return pixels


def render_native_face() -> PixelGrid:
    """Reuse the exact native WFF preview from the runtime generator."""

    return runtime_assets._preview_pixels()


def _matrix_markup(rows: Sequence[str]) -> str:
    return "\n".join(
        f"<code>{html.escape(row)}</code>" for row in rows
    )


def _html_document(images: Mapping[str, bytes]) -> bytes:
    image_data = {
        name: "data:image/png;base64," + base64.b64encode(data).decode("ascii")
        for name, data in images.items()
    }
    matrix_data = {
        "steps": list(APPROVED_STEP_ICON),
        "battery": list(BATTERY_ICON),
        "unavailable": list(UNAVAILABLE_WEATHER_ICON),
        "weather_day": {str(index): list(rows) for index, rows in WEATHER_DAY.items()},
        "weather_night": {str(index): list(rows) for index, rows in WEATHER_NIGHT.items()},
    }
    matrix_json = json.dumps(matrix_data, indent=2, sort_keys=True)
    sections = [
        (UTILITY_SHEET_NAME, "Selected utility icons", "steps and battery are the only persistent utility tiles."),
        (WEATHER_SHEET_NAME, "Complete weather resolution", "Every WFF condition ID has a day and night mapping."),
        (STATE_SHEET_NAME, "Truthful weather states", "Unavailable uses the neutral icon plus --; stale keeps a marker distinct from an unavailable value."),
        (MATRIX_SHEET_NAME, "True 16x16 / solid 3x3 inspection", "The matrix views expose project-owned source cells and their physical tile expansion."),
        (NATIVE_FACE_NAME, "Native 466x466 face", "This is the deterministic runtime preview, not fresh emulator or physical-watch evidence."),
        (MAGNIFIED_FACE_NAME, "Magnified face", "A 2x nearest-neighbour view for inspecting cell edges and placement."),
    ]
    cards = "\n".join(
        f'<article><h2>{html.escape(title)}</h2><p>{html.escape(description)}</p>'
        f'<img alt="{html.escape(title)}" src="{image_data[name]}"></article>'
        for name, title, description in sections
    )
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Raster 90 icon family</title>
<style>
body {{ background:#111; color:#eee; font:16px system-ui,sans-serif; margin:2rem; }}
main {{ max-width:1300px; margin:auto; }}
article {{ border:1px solid #444; margin:1.5rem 0; padding:1rem; background:#181818; }}
img {{ background:#000; image-rendering:pixelated; max-width:100%; height:auto; }}
code {{ display:block; font:13px ui-monospace,monospace; line-height:1.2; white-space:pre; }}
.matrix {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1rem; }}
.note {{ color:#ccc; }}
</style>
</head>
<body><main>
<h1>Raster 90 icon family</h1>
<p class="note">Project-owned runtime-selected matrices. The Android bundle consumes
<code>icons/raster90/family.py</code> directly; historical calendar, 8x8/12x12,
and rejected step alternatives remain design-only controls.</p>
<p class="note">Palette: {html.escape(json.dumps(dict(PALETTE), sort_keys=True))}</p>
{cards}
<h2>Embedded source matrices</h2>
<div class="matrix">
<section><h3>Steps / approved four-toe-vertical</h3>{_matrix_markup(APPROVED_STEP_ICON)}</section>
<section><h3>Battery</h3>{_matrix_markup(BATTERY_ICON)}</section>
<section><h3>Unavailable neutral weather</h3>{_matrix_markup(UNAVAILABLE_WEATHER_ICON)}</section>
</div>
<script>const ICON_FAMILY_DATA = {matrix_json};</script>
</main></body></html>
"""
    return document.encode("utf-8")


def expected_output_bytes() -> dict[str, bytes]:
    """Return every tracked presentation artifact, deterministically."""

    native = render_native_face()
    magnified = _scale_nearest(native, 2)
    images = {
        UTILITY_SHEET_NAME: encode_png(render_utility_sheet()),
        WEATHER_SHEET_NAME: encode_png(render_weather_sheet()),
        STATE_SHEET_NAME: encode_png(render_state_sheet()),
        MATRIX_SHEET_NAME: encode_png(render_matrix_sheet()),
        NATIVE_FACE_NAME: encode_png(native),
        MAGNIFIED_FACE_NAME: encode_png(magnified),
    }
    return {**images, HTML_NAME: _html_document(images)}


def _expected_outputs() -> dict[str, bytes]:
    """Compatibility name matching the font-family presentation tooling."""

    return expected_output_bytes()


def _validate_expected(root: Path, expected: Mapping[str, bytes]) -> None:
    output_dir = root / OUTPUT_DIR_REL
    if not output_dir.is_dir():
        raise ValueError(f"icon presentation directory is missing: {output_dir}")
    actual = {path.name for path in output_dir.iterdir() if path.is_file()}
    expected_names = set(expected)
    missing = sorted(expected_names - actual)
    extra = sorted(actual - expected_names)
    if missing:
        raise ValueError("missing icon-family presentation outputs: " + ", ".join(missing))
    if extra:
        raise ValueError("unexpected icon-family presentation outputs: " + ", ".join(extra))
    for name, data in expected.items():
        path = output_dir / name
        if path.read_bytes() != data:
            raise ValueError(f"icon presentation drift detected: {path}")


def _write_expected(root: Path, expected: Mapping[str, bytes]) -> int:
    output_dir = root / OUTPUT_DIR_REL
    output_dir.mkdir(parents=True, exist_ok=True)
    changed = 0
    for name, data in expected.items():
        path = output_dir / name
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
            changed += 1
    for path in output_dir.iterdir():
        if path.is_file() and path.name not in expected:
            path.unlink()
            changed += 1
    _validate_expected(root, expected)
    return changed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        expected = expected_output_bytes()
        if args.check:
            _validate_expected(root, expected)
            print(f"Raster 90 icon-family presentation OK: {len(expected)} outputs")
        else:
            changed = _write_expected(root, expected)
            print(f"Raster 90 icon-family presentation generated ({changed} changed)")
    except (OSError, ValueError, KeyError, TypeError, zlib.error) as error:
        print(f"Raster 90 icon-family presentation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
