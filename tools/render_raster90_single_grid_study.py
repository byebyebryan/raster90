#!/usr/bin/env python3
"""Render the deterministic Raster 90 solid single-grid design study.

The study is intentionally separate from packaged WFF resources.  It renders
the proposed 150x150 fictional framebuffer at native 466x466 and as a
nearest-neighbour 454x454 design approximation.  ``--check`` recomputes every
ignored output byte-for-byte without modifying it.
"""

from __future__ import annotations

import argparse
import binascii
import json
import math
import struct
import sys
import zlib
from pathlib import Path
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "design" / "raster90"))

from icons.raster90.family import (  # noqa: E402
    PALETTE,
    SELECTED_UTILITY_ICONS,
    STALE_MARKER,
    WEATHER_CONDITIONS,
    WEATHER_DAY,
    WEATHER_NIGHT,
)
from matrices import FINE_GLYPHS  # noqa: E402
from single_grid_study import (  # noqa: E402
    ACTIVE_ORIGIN,
    ACTIVE_SIZE,
    CANVAS,
    ICON_CELLS,
    ICON_TEXT_GAP_CELLS,
    ICONS,
    PIXEL_LIT,
    PIXEL_PITCH,
    ROW_BANDS,
    SAFE_CENTER,
    SAFE_RADIUS,
    SOURCE_SIZE,
    STUDY_TEXT,
    TEXT_LINE_CELLS,
    TIME_COLON,
    TIME_COLON_CELLS,
    TIME_DIGIT_CELLS,
    TIME_DIGITS,
    TIME_LINE_CELLS,
    WEATHER_PALETTE,
    validate_single_grid_study,
)

SIXTEEN_UTILITY_ICONS = SELECTED_UTILITY_ICONS
SIXTEEN_WEATHER_DAY = WEATHER_DAY
SIXTEEN_WEATHER_NIGHT = WEATHER_NIGHT
SINGLE_GRID_WEATHER_DAY = WEATHER_DAY
SINGLE_GRID_WEATHER_NIGHT = WEATHER_NIGHT


RGBA = tuple[int, int, int, int]
PixelGrid = list[list[RGBA]]

BLACK: RGBA = (0, 0, 0, 255)
WHITE: RGBA = (255, 255, 255, 255)
OUTPUT_DIR_REL = Path("outputs/raster90/studies/single-grid")
ICON_SHEET_WIDTH = 1248
ICON_SHEET_HEIGHT = 950
ICON_SHEET_PITCH = PIXEL_PITCH * 2
ICON_SHEET_LIT = PIXEL_LIT * 2
# Keep the deterministic study at the same local compact-text coordinate as
# the packaged WFF rows.
COMPACT_ROW_TEXT_Y = 13


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = binascii.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)


def encode_png(pixels: PixelGrid) -> bytes:
    if not pixels or not pixels[0]:
        raise ValueError("cannot encode an empty image")
    width = len(pixels[0])
    height = len(pixels)
    if any(len(row) != width for row in pixels):
        raise ValueError("inconsistent image row width")
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
    pitch: int = PIXEL_PITCH,
    lit: int = PIXEL_LIT,
    color_for,
) -> None:
    for source_y, row in enumerate(rows):
        for source_x, symbol in enumerate(row):
            if symbol in ("0", "."):
                continue
            color = color_for(symbol)
            for target_y in range(y + source_y * pitch, y + source_y * pitch + lit):
                for target_x in range(x + source_x * pitch, x + source_x * pitch + lit):
                    _set_pixel(pixels, target_x, target_y, color)


def _text_advance(character: str) -> int:
    return (2 if character == " " else 6) * PIXEL_PITCH


def _text_width(text: str) -> int:
    return sum(_text_advance(character) for character in text)


def _draw_text(pixels: PixelGrid, text: str, *, x: int, line_y: int) -> None:
    glyph_height = len(next(rows for character, rows in FINE_GLYPHS.items() if character != " "))
    line_height = TEXT_LINE_CELLS * PIXEL_PITCH
    y = line_y + (line_height - glyph_height * PIXEL_PITCH) // 2
    cursor = x
    for character in text:
        try:
            rows = FINE_GLYPHS[character]
        except KeyError as error:
            raise ValueError(f"study text uses undefined glyph {character!r}") from error
        _draw_matrix(
            pixels,
            rows,
            x=cursor,
            y=y,
            color_for=lambda _symbol: WHITE,
        )
        cursor += _text_advance(character)


def _icon_color(name: str, symbol: str) -> RGBA:
    if name != "weather":
        return WHITE
    try:
        return WEATHER_PALETTE[symbol]
    except KeyError as error:
        raise ValueError(f"unknown weather palette symbol {symbol!r}") from error


def _draw_information_row(pixels: PixelGrid, name: str) -> None:
    row_y = ACTIVE_ORIGIN[1] + ROW_BANDS[name][0] * PIXEL_PITCH
    text = STUDY_TEXT[name]
    text_width = _text_width(text)
    if name == "date":
        x = ACTIVE_ORIGIN[0] + (ACTIVE_SIZE - text_width) // 2
        _draw_text(
            pixels,
            text,
            x=x,
            line_y=row_y + COMPACT_ROW_TEXT_Y - 1,
        )
        return

    icon_width = ICON_CELLS * PIXEL_PITCH
    gap = ICON_TEXT_GAP_CELLS * PIXEL_PITCH
    total_width = icon_width + gap + text_width
    x = ACTIVE_ORIGIN[0] + (ACTIVE_SIZE - total_width) // 2
    _draw_matrix(
        pixels,
        ICONS[name],
        x=x,
        y=row_y,
        color_for=lambda symbol: _icon_color(name, symbol),
    )
    text_x = x + icon_width + gap
    _draw_text(
        pixels,
        text,
        x=text_x,
        line_y=row_y + COMPACT_ROW_TEXT_Y - 1,
    )


def _draw_time(pixels: PixelGrid, value: str = "10:08") -> None:
    width_cells = sum(
        TIME_COLON_CELLS if character == ":" else TIME_DIGIT_CELLS
        for character in value
    )
    x = ACTIVE_ORIGIN[0] + (ACTIVE_SIZE - width_cells * PIXEL_PITCH) // 2
    y = ACTIVE_ORIGIN[1] + ROW_BANDS["time"][0] * PIXEL_PITCH
    cursor = x
    for character in value:
        rows = TIME_COLON if character == ":" else TIME_DIGITS[character]
        _draw_matrix(
            pixels,
            rows,
            x=cursor,
            y=y,
            color_for=lambda _symbol: WHITE,
        )
        cursor += len(rows[0]) * PIXEL_PITCH


def render_face() -> PixelGrid:
    validate_single_grid_study()
    pixels = _blank(CANVAS, CANVAS)
    _draw_information_row(pixels, "weather")
    _draw_information_row(pixels, "date")
    _draw_time(pixels)
    _draw_information_row(pixels, "steps")
    _draw_information_row(pixels, "battery")
    return pixels


def resize_nearest(pixels: PixelGrid, target_size: int) -> PixelGrid:
    source_height = len(pixels)
    source_width = len(pixels[0])
    return [
        [
            pixels[min(source_height - 1, int(y * source_height / target_size))][
                min(source_width - 1, int(x * source_width / target_size))
            ]
            for x in range(target_size)
        ]
        for y in range(target_size)
    ]


def _draw_panel(target: PixelGrid, source: PixelGrid, *, x: int, y: int) -> None:
    for source_y, row in enumerate(source):
        for source_x, pixel in enumerate(row):
            _set_pixel(target, x + source_x, y + source_y, pixel)


def build_comparison_sheet() -> PixelGrid:
    native = render_face()
    scaled = resize_nearest(native, 454)
    gap = 12
    pixels = _blank(CANVAS + gap + 454, CANVAS)
    _draw_panel(pixels, native, x=0, y=0)
    _draw_panel(pixels, scaled, x=CANVAS + gap, y=(CANVAS - 454) // 2)
    return pixels


def build_calibration_sheet() -> PixelGrid:
    """Show representative solid cells and content at actual physical size."""

    pixels = _blank(900, 350)
    _draw_text(pixels, "3X3 PIXEL", x=24, line_y=18)

    # Isolated cells, adjacent cells, and a checker expose solid cell edges.
    calibration = (
        "1000100010001000",
        "0000000000000000",
        "1100110011001100",
        "1100110011001100",
        "0000000000000000",
        "1010101010101010",
        "0101010101010101",
    )
    _draw_matrix(
        pixels,
        calibration,
        x=24,
        y=55,
        color_for=lambda _symbol: WHITE,
    )
    _draw_text(pixels, "21°C SAT 15 AUG", x=180, line_y=48)
    _draw_text(pixels, "03642 82%", x=180, line_y=75)

    icon_x = 24
    for name in ("weather", "steps", "battery"):
        _draw_matrix(
            pixels,
            ICONS[name],
            x=icon_x,
            y=120,
            color_for=lambda symbol, icon_name=name: _icon_color(icon_name, symbol),
        )
        icon_x += 72

    # The time uses the exact proposed solid source pixel, not a magnified tier.
    time_x = 24
    time_y = 210
    for character in "10:08":
        rows = TIME_COLON if character == ":" else TIME_DIGITS[character]
        _draw_matrix(
            pixels,
            rows,
            x=time_x,
            y=time_y,
            color_for=lambda _symbol: WHITE,
        )
        time_x += len(rows[0]) * PIXEL_PITCH
    return pixels


def build_current_icon_sheet() -> PixelGrid:
    """Render every icon matrix currently consumed by the packaged face."""

    pixels = _blank(ICON_SHEET_WIDTH, ICON_SHEET_HEIGHT)
    _draw_text(pixels, "RASTER 90 SELECTED ICONS", x=24, line_y=18)
    _draw_text(pixels, "EXACT MATRICES  2X REVIEW SCALE", x=24, line_y=48)
    _draw_text(pixels, "UTILITY", x=24, line_y=82)

    column_width = 300
    utility_y = 138
    for column, (label, rows) in enumerate(
        (name, SIXTEEN_UTILITY_ICONS[name]) for name in ("steps", "battery")
    ):
        card_x = 24 + column * column_width
        _draw_text(pixels, label.upper(), x=card_x, line_y=108)
        _draw_matrix(
            pixels,
            rows,
            x=card_x,
            y=utility_y,
            pitch=ICON_SHEET_PITCH,
            lit=ICON_SHEET_LIT,
            color_for=lambda _symbol: WHITE,
        )

    stale_x = 24 + 2 * column_width
    _draw_text(pixels, "STALE MARKER", x=stale_x, line_y=108)
    # Preserve the marker's true size relative to a 16x16 icon tile.
    stale_offset = (16 - len(STALE_MARKER)) * ICON_SHEET_PITCH // 2
    _draw_matrix(
        pixels,
        STALE_MARKER,
        x=stale_x + stale_offset,
        y=utility_y + stale_offset,
        pitch=ICON_SHEET_PITCH,
        lit=ICON_SHEET_LIT,
        color_for=lambda _symbol: WHITE,
    )

    _draw_text(pixels, "WFF CONDITIONS  DAY AND NIGHT", x=24, line_y=250)
    icon_size = 16 * ICON_SHEET_PITCH
    for condition, condition_name in enumerate(WEATHER_CONDITIONS):
        column = condition % 4
        row = condition // 4
        card_x = 24 + column * column_width
        card_y = 282 + row * 166
        label = f"{condition:02d} {condition_name.replace('_', ' ').upper()}"
        _draw_text(pixels, label, x=card_x, line_y=card_y)

        day_x = card_x + 24
        night_x = card_x + 164
        icon_y = card_y + 30
        for rows, x in (
            (SIXTEEN_WEATHER_DAY[condition], day_x),
            (SIXTEEN_WEATHER_NIGHT[condition], night_x),
        ):
            _draw_matrix(
                pixels,
                rows,
                x=x,
                y=icon_y,
                pitch=ICON_SHEET_PITCH,
                lit=ICON_SHEET_LIT,
                color_for=lambda symbol: _icon_color("weather", symbol),
            )

        day_label_width = _text_width("DAY")
        night_label_width = _text_width("NIGHT")
        _draw_text(
            pixels,
            "DAY",
            x=day_x + (icon_size - day_label_width) // 2,
            line_y=card_y + 130,
        )
        _draw_text(
            pixels,
            "NIGHT",
            x=night_x + (icon_size - night_label_width) // 2,
            line_y=card_y + 130,
        )
    return pixels


def _chord_at(active_y: int) -> float:
    distance = abs(active_y - SAFE_CENTER[1])
    return 2.0 * math.sqrt(SAFE_RADIUS**2 - distance**2)


def geometry_report() -> dict[str, object]:
    widths: dict[str, int] = {}
    for name, text in STUDY_TEXT.items():
        if name == "date":
            widths[name] = _text_width(text)
        else:
            widths[name] = (
                ICON_CELLS * PIXEL_PITCH
                + ICON_TEXT_GAP_CELLS * PIXEL_PITCH
                + _text_width(text)
            )
    widths["time"] = (
        4 * TIME_DIGIT_CELLS + TIME_COLON_CELLS
    ) * PIXEL_PITCH

    rows: dict[str, object] = {}
    for name in ("weather", "date", "time", "steps", "battery"):
        start_cells, end_cells = ROW_BANDS[name]
        start = start_cells * PIXEL_PITCH
        end = end_cells * PIXEL_PITCH
        edge = max((start, end), key=lambda y: abs(y - SAFE_CENTER[1]))
        chord = _chord_at(edge)
        margin = chord - widths[name]
        rows[name] = {
            "source_band": [start_cells, end_cells],
            "active_band": [start, end],
            "required_width": widths[name],
            "safe_edge_y": edge,
            "safe_chord": round(chord, 3),
            "safe_margin_total": round(margin, 3),
            "safe_margin_per_side": round(margin / 2, 3),
            "valid": margin >= 0,
        }
    return {
        "study": "Raster 90 solid single-grid runtime",
        "design_only": True,
        "canvas": [CANVAS, CANVAS],
        "active_origin": list(ACTIVE_ORIGIN),
        "active_size": ACTIVE_SIZE,
        "source_framebuffer": [SOURCE_SIZE, SOURCE_SIZE],
        "pixel_pitch": PIXEL_PITCH,
        "pixel_lit": PIXEL_LIT,
        "cell_fill": "solid",
        "icon_canvas": [ICON_CELLS, ICON_CELLS],
        "text_line_cells": TEXT_LINE_CELLS,
        "time_line_cells": TIME_LINE_CELLS,
        "safe_circle_coordinate_space": "active-framebuffer",
        "fixture_temperature_unit": "C",
        "degree_mark": "closed ring",
        "rows": rows,
        "all_safe": all(row["valid"] for row in rows.values()),
    }


def geometry_text(report: Mapping[str, object]) -> str:
    lines = [
        "Raster 90 solid single-grid runtime",
        "======================================",
        "Deterministic runtime geometry mirrored by this study renderer.",
        "466x466 canvas; 450x450 active frame at (8,8); 150x150 source cells.",
        "Every source pixel has 3-unit pitch and solid 3x3 light with no gutter.",
        "Fixtures default to Celsius and use a closed degree ring.",
        "",
    ]
    for name in ("weather", "date", "time", "steps", "battery"):
        row = report["rows"][name]
        lines.append(
            f"{name:7s} cells={row['source_band'][0]}..{row['source_band'][1]} "
            f"active={row['active_band'][0]}..{row['active_band'][1]} "
            f"width={row['required_width']} chord={row['safe_chord']:.3f} "
            f"margin-total={row['safe_margin_total']:.3f} "
            f"margin-per-side={row['safe_margin_per_side']:.3f} valid={row['valid']}"
        )
    lines.extend(
        [
            "",
            f"All rows fit the conservative circle: {report['all_safe']}",
            "The time silhouette is an expanded V1 placeholder for pitch review, not final numeral art.",
            "Weather, steps, and battery are direct-authored true16 matrices; the calendar icon is not packaged.",
        ]
    )
    return "\n".join(lines) + "\n"


def expected_output_bytes() -> dict[str, bytes]:
    native = render_face()
    scaled = resize_nearest(native, 454)
    allowed = {BLACK, WHITE, *WEATHER_PALETTE.values()}
    for name, pixels in (("native", native), ("scaled", scaled)):
        if any(pixel not in allowed for row in pixels for pixel in row):
            raise ValueError(f"{name}: unexpected palette value")

    report = geometry_report()
    if not report["all_safe"]:
        raise ValueError("single-grid study exceeds the conservative safe circle")
    return {
        "raster90-single-grid-face-466.png": encode_png(native),
        "raster90-single-grid-face-454.png": encode_png(scaled),
        "raster90-single-grid-comparison.png": encode_png(build_comparison_sheet()),
        "raster90-single-grid-calibration.png": encode_png(build_calibration_sheet()),
        "raster90-current-icon-sheet.png": encode_png(build_current_icon_sheet()),
        "raster90-single-grid-geometry.json": (
            json.dumps(report, indent=2, sort_keys=True) + "\n"
        ).encode(),
        "raster90-single-grid-geometry.txt": geometry_text(report).encode(),
    }


def generate_outputs(root: Path) -> int:
    output_dir = root / OUTPUT_DIR_REL
    output_dir.mkdir(parents=True, exist_ok=True)
    changed = 0
    for name, data in expected_output_bytes().items():
        path = output_dir / name
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
            changed += 1
    check_outputs(root)
    return changed


def check_outputs(root: Path) -> None:
    validate_single_grid_study()
    output_dir = root / OUTPUT_DIR_REL
    for name, expected in expected_output_bytes().items():
        path = output_dir / name
        if not path.exists():
            raise ValueError(f"missing single-grid output: {path}")
        if path.read_bytes() != expected:
            raise ValueError(f"stale or corrupt single-grid output: {path}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.check:
            check_outputs(root)
            print("Raster 90 single-grid study outputs OK")
        else:
            changed = generate_outputs(root)
            print(f"Raster 90 single-grid study outputs generated ({changed} changed)")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"Raster 90 single-grid study failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
