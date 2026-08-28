#!/usr/bin/env python3
"""Generate and verify Raster 90's deterministic bitmap resources.

The watch face deliberately uses resource-backed bitmap fonts rather than a
runtime font renderer.  This script is the only producer of those resources:

    python3 tools/generate_raster90_assets.py
    python3 tools/generate_raster90_assets.py --check

The implementation is standard-library-only.  Its small PNG reader is used by
``--check`` so drift, palette violations, alpha filtering, and accidental
resource additions are caught without depending on Pillow or ImageMagick.
"""

from __future__ import annotations

import argparse
import binascii
import struct
import sys
import zlib
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "design" / "raster90"))

from matrices import (  # noqa: E402  (path is intentionally set above)
    SINGLE_GRID_LIT,
    SINGLE_GRID_PITCH,
)
from icons.raster90.family import (  # noqa: E402  (canonical icon source)
    LAST_DRAWABLE_CELL,
    MATRIX_CELLS,
    PALETTE,
    SELECTED_UTILITY_ICONS,
    STALE_MARKER,
    WEATHER_DAY,
    WEATHER_NIGHT,
)
from icons.raster90.animation import (  # noqa: E402  (canonical motion source)
    WEATHER_ANIMATION_FRAMES,
    animation_resource_name,
)
from fonts.raster90.family import (  # noqa: E402  (authoritative font source)
    PRIMARY_COLON,
    PRIMARY_COLON_CELLS,
    PRIMARY_DIGITS,
    PRIMARY_DIGIT_CELLS,
    PRIMARY_LINE_CELLS,
    RUNTIME_SECONDARY_GLYPHS,
)
from single_grid_study import (  # noqa: E402  (selected layout inputs)
    ROW_BANDS as STUDY_ROW_BANDS,
)


RGBA = tuple[int, int, int, int]
PixelGrid = list[list[RGBA]]

CANVAS = 466
ACTIVE_ORIGIN = (8, 8)
ACTIVE_SIZE = 450

FINE_PITCH = SINGLE_GRID_PITCH
FINE_LIT = SINGLE_GRID_LIT
# Ordinary fine glyph matrices use five source cells and receive one trailing
# blank cell for their 18-unit advance.  The literal space is authored as two
# blank source cells and intentionally keeps that 6-unit width.
FINE_GLYPH_CELLS = 5
FINE_ADVANCE_CELLS = 6
FINE_SPACE_ADVANCE_CELLS = 2
FINE_WIDTH = FINE_ADVANCE_CELLS * FINE_PITCH
FINE_SPACE_WIDTH = FINE_SPACE_ADVANCE_CELLS * FINE_PITCH
FINE_HEIGHT = 7 * FINE_PITCH
# WFF places each available compact value at this local offset within its
# 48-unit information band. The preview uses the same physical coordinate.
COMPACT_ROW_TEXT_Y = 13

TIME_PITCH = SINGLE_GRID_PITCH
TIME_LIT = SINGLE_GRID_LIT
TIME_DIGITS = PRIMARY_DIGITS
TIME_COLON = PRIMARY_COLON
TIME_DIGIT_CELLS = PRIMARY_DIGIT_CELLS
TIME_DIGIT_WIDTH = TIME_DIGIT_CELLS * TIME_PITCH
TIME_COLON_CELLS = PRIMARY_COLON_CELLS
TIME_COLON_WIDTH = TIME_COLON_CELLS * TIME_PITCH
TIME_LINE_CELLS = PRIMARY_LINE_CELLS
TIME_HEIGHT = TIME_LINE_CELLS * TIME_PITCH
TIME_WIDTH = 4 * TIME_DIGIT_WIDTH + TIME_COLON_WIDTH

ICON_PITCH = SINGLE_GRID_PITCH
ICON_LIT = SINGLE_GRID_LIT
ICON_CELLS = MATRIX_CELLS
ICON_SIZE = ICON_CELLS * ICON_PITCH
WEATHER_SIZE = ICON_SIZE

# The selected asset mapping is deliberately bound to the canonical component
# rather than a design study. ``ICONS`` adds the representative available
# weather tile only for the native face preview; the packaged weather assets
# below use the complete canonical day/night maps directly.
ICONS = {
    "weather": WEATHER_DAY[14],
    **SELECTED_UTILITY_ICONS,
}

ROW_BANDS = {
    name: tuple(cell * SINGLE_GRID_PITCH for cell in band)
    for name, band in STUDY_ROW_BANDS.items()
}
ROW_X = {
    "weather": 162,
    "date": 147,
    "steps": 153,
    "battery": 171,
}
ROW_WIDTHS = {
    # Widths reserve the verified dynamic extremes: -100°F weather,
    # 31 DEC, six-digit steps, and 100% battery.
    "weather": 162,
    "date": 156,
    "steps": 162,
    "battery": 126,
}

UTILITY_ASSETS = {
    "steps": "raster_icon_steps",
    "battery": "raster_icon_battery",
}

OPAQUE_BLACK: RGBA = (0, 0, 0, 255)
TRANSPARENT: RGBA = (0, 0, 0, 0)
OPAQUE_WHITE: RGBA = PALETTE["W"]

# Keep the APK surface limited to glyphs that current WFF expressions can
# emit.  The complete family remains available to source-only presentation
# tooling through fonts/raster90/family.py.
FINE_GLYPHS = RUNTIME_SECONDARY_GLYPHS

ASSET_DIR_REL = Path("watchfaces/raster90/src/main/res/drawable-nodpi")


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = binascii.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)


def encode_png(pixels: PixelGrid) -> bytes:
    """Encode an RGBA grid using deterministic filter-zero scanlines."""

    if not pixels or not pixels[0]:
        raise ValueError("cannot encode an empty PNG")
    width = len(pixels[0])
    height = len(pixels)
    if any(len(row) != width for row in pixels):
        raise ValueError("pixel rows have inconsistent widths")
    raw = bytearray()
    for row in pixels:
        raw.append(0)  # PNG filter type: None
        for red, green, blue, alpha in row:
            raw.extend((red, green, blue, alpha))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", ihdr) + _png_chunk(
        b"IDAT", zlib.compress(bytes(raw), level=9)
    ) + _png_chunk(b"IEND", b"")


def _paeth(left: int, above: int, upper_left: int) -> int:
    estimate = left + above - upper_left
    left_distance = abs(estimate - left)
    above_distance = abs(estimate - above)
    upper_left_distance = abs(estimate - upper_left)
    if left_distance <= above_distance and left_distance <= upper_left_distance:
        return left
    if above_distance <= upper_left_distance:
        return above
    return upper_left


def decode_png(data: bytes) -> tuple[int, int, PixelGrid]:
    """Read the RGBA PNG subset produced by this script (with full filters)."""

    signature = b"\x89PNG\r\n\x1a\n"
    if not data.startswith(signature):
        raise ValueError("not a PNG")
    offset = len(signature)
    width = height = None
    color_type = bit_depth = interlace = None
    compressed = bytearray()
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError("truncated PNG chunk")
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        kind = data[offset + 4 : offset + 8]
        start = offset + 8
        end = start + length
        if end + 4 > len(data):
            raise ValueError("truncated PNG payload")
        payload = data[start:end]
        expected_crc = struct.unpack(">I", data[end : end + 4])[0]
        actual_crc = binascii.crc32(kind + payload) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ValueError(f"bad CRC in {kind!r} chunk")
        if kind == b"IHDR":
            if len(payload) != 13:
                raise ValueError("invalid IHDR")
            width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(
                ">IIBBBBB", payload
            )
            if compression or filtering:
                raise ValueError("unsupported PNG compression/filter method")
        elif kind == b"IDAT":
            compressed.extend(payload)
        elif kind == b"IEND":
            break
        offset = end + 4
    if width is None or height is None:
        raise ValueError("PNG has no IHDR")
    if bit_depth != 8 or color_type != 6 or interlace != 0:
        raise ValueError("expected a non-interlaced 8-bit RGBA PNG")
    try:
        raw = zlib.decompress(bytes(compressed))
    except zlib.error as error:
        raise ValueError(f"invalid PNG data stream: {error}") from error
    row_bytes = width * 4
    expected_length = height * (row_bytes + 1)
    if len(raw) != expected_length:
        raise ValueError("PNG scanline data has the wrong length")

    rows: PixelGrid = []
    previous = bytearray(row_bytes)
    cursor = 0
    for _ in range(height):
        filter_type = raw[cursor]
        cursor += 1
        encoded = raw[cursor : cursor + row_bytes]
        cursor += row_bytes
        row = bytearray(row_bytes)
        for index, value in enumerate(encoded):
            left = row[index - 4] if index >= 4 else 0
            above = previous[index]
            upper_left = previous[index - 4] if index >= 4 else 0
            if filter_type == 0:
                reconstructed = value
            elif filter_type == 1:
                reconstructed = (value + left) & 0xFF
            elif filter_type == 2:
                reconstructed = (value + above) & 0xFF
            elif filter_type == 3:
                reconstructed = (value + ((left + above) // 2)) & 0xFF
            elif filter_type == 4:
                reconstructed = (value + _paeth(left, above, upper_left)) & 0xFF
            else:
                raise ValueError(f"unsupported PNG filter type {filter_type}")
            row[index] = reconstructed
        rows.append([tuple(row[index : index + 4]) for index in range(0, row_bytes, 4)])
        previous = row
    return width, height, rows


def _validate_rows(
    name: str,
    rows: Sequence[str],
    width: int,
    symbols: set[str],
    expected_height: int | None = None,
) -> None:
    if expected_height is None:
        expected_height = {5: 7, 7: 9, 8: 8}.get(width)
    if expected_height is None:
        raise ValueError(f"{name}: expected row count is unspecified for width {width}")
    if len(rows) != expected_height:
        raise ValueError(f"{name}: expected a fixed row count, got {len(rows)}")
    for row in rows:
        if len(row) != width:
            raise ValueError(f"{name}: row {row!r} is not {width} cells wide")
        unexpected = set(row) - symbols
        if unexpected:
            raise ValueError(f"{name}: unexpected cell symbols {sorted(unexpected)}")


def _validate_icon_drawable_field(name: str, rows: Sequence[str]) -> None:
    """Keep the serialized 16x16 tile's final row/column as a gutter."""

    if len(rows) != MATRIX_CELLS or any(len(row) != MATRIX_CELLS for row in rows):
        raise ValueError(f"{name}: expected {MATRIX_CELLS}x{MATRIX_CELLS} matrix")
    trailing = LAST_DRAWABLE_CELL + 1
    if any(rows[trailing][x] != "." for x in range(MATRIX_CELLS)):
        raise ValueError(f"{name}: trailing row {trailing} must be empty")
    if any(row[trailing] != "." for row in rows):
        raise ValueError(f"{name}: trailing column {trailing} must be empty")


def _blank(width: int, height: int, fill: RGBA = TRANSPARENT) -> PixelGrid:
    return [[fill for _ in range(width)] for _ in range(height)]


def _paint_cells(
    rows: Sequence[str],
    *,
    pitch: int,
    lit: int,
    width_cells: int,
    color_for: callable,
) -> PixelGrid:
    height_cells = len(rows)
    pixels = _blank(width_cells * pitch, height_cells * pitch)
    for cell_y, row in enumerate(rows):
        for cell_x, symbol in enumerate(row):
            if symbol in ("0", "."):
                continue
            color = color_for(symbol)
            pixel_x = cell_x * pitch
            pixel_y = cell_y * pitch
            for y in range(pixel_y, pixel_y + lit):
                for x in range(pixel_x, pixel_x + lit):
                    pixels[y][x] = color
    return pixels


def _fine_pixels(rows: Sequence[str]) -> PixelGrid:
    source_width = len(rows[0]) if rows else 0
    if source_width == FINE_GLYPH_CELLS:
        output_width = FINE_ADVANCE_CELLS
    elif source_width == FINE_SPACE_ADVANCE_CELLS:
        output_width = FINE_SPACE_ADVANCE_CELLS
    else:
        raise ValueError(
            "fine glyph: expected five source cells or the two-cell literal space, "
            f"got {source_width}"
        )
    _validate_rows("fine glyph", rows, source_width, {"0", "1"}, expected_height=7)
    return _paint_cells(
        rows,
        pitch=FINE_PITCH,
        lit=FINE_LIT,
        width_cells=output_width,
        color_for=lambda symbol: OPAQUE_WHITE,
    )


def _time_pixels(rows: Sequence[str], width_cells: int) -> PixelGrid:
    _validate_rows(
        "time glyph",
        rows,
        width_cells,
        {"0", "1"},
        expected_height=TIME_LINE_CELLS,
    )
    return _paint_cells(
        rows,
        pitch=TIME_PITCH,
        lit=TIME_LIT,
        width_cells=width_cells,
        color_for=lambda symbol: OPAQUE_WHITE,
    )


def _weather_pixels(rows: Sequence[str]) -> PixelGrid:
    _validate_rows(
        "weather sprite",
        rows,
        ICON_CELLS,
        set(PALETTE) | {"."},
        expected_height=ICON_CELLS,
    )
    _validate_icon_drawable_field("weather sprite", rows)
    return _paint_cells(
        rows,
        pitch=ICON_PITCH,
        lit=ICON_LIT,
        width_cells=ICON_CELLS,
        color_for=lambda symbol: PALETTE[symbol],
    )


def _weather_animation_pixels(rows: Sequence[str]) -> PixelGrid:
    """Render an opaque replacement tile so the static icon cannot ghost through."""

    return [
        [OPAQUE_BLACK if pixel == TRANSPARENT else pixel for pixel in row]
        for row in _weather_pixels(rows)
    ]


def _utility_pixels(rows: Sequence[str]) -> PixelGrid:
    _validate_rows(
        "utility icon",
        rows,
        ICON_CELLS,
        {".", "0", "1"},
        expected_height=ICON_CELLS,
    )
    _validate_icon_drawable_field("utility icon", rows)
    return _paint_cells(
        rows,
        pitch=ICON_PITCH,
        lit=ICON_LIT,
        width_cells=ICON_CELLS,
        color_for=lambda symbol: OPAQUE_WHITE,
    )


def _stale_pixels() -> PixelGrid:
    _validate_rows("stale marker", STALE_MARKER, 2, {"0", "1"}, expected_height=2)
    return _paint_cells(
        STALE_MARKER,
        pitch=ICON_PITCH,
        lit=ICON_LIT,
        width_cells=2,
        color_for=lambda symbol: OPAQUE_WHITE,
    )


def _fine_name(character: str) -> str:
    names = {
        " ": "space",
        "+": "plus",
        "-": "minus",
        "%": "percent",
        "°": "degree",
        "?": "question",
    }
    return f"raster_fine_{names.get(character, character.lower())}"


def _fine_advance(character: str) -> int:
    """Return the authored fine-tier advance for one character."""

    return FINE_SPACE_WIDTH if character == " " else FINE_WIDTH


def _fine_string_width(text: str) -> int:
    """Return a fine string's rendered width from its variable advances."""

    return sum(_fine_advance(character) for character in text)


def _centered_fine_x(text: str) -> int:
    """Return the active-frame x offset for a centered fine string."""

    return (ACTIVE_SIZE - _fine_string_width(text)) // 2


def _time_name(character: str) -> str:
    return "raster_time_colon" if character == ":" else f"raster_time_{character}"


def _weather_name(day_or_night: str, condition: int) -> str:
    return f"raster_weather_{day_or_night}_{condition:02d}"


def _expected_pngs() -> dict[str, bytes]:
    assets: dict[str, bytes] = {}
    for character, rows in FINE_GLYPHS.items():
        assets[f"{_fine_name(character)}.png"] = encode_png(_fine_pixels(rows))
    for digit, rows in TIME_DIGITS.items():
        assets[f"{_time_name(digit)}.png"] = encode_png(
            _time_pixels(rows, TIME_DIGIT_CELLS)
        )
    assets[f"{_time_name(':')}.png"] = encode_png(
        _time_pixels(TIME_COLON, TIME_COLON_CELLS)
    )

    for condition, rows in WEATHER_DAY.items():
        assets[f"{_weather_name('day', condition)}.png"] = encode_png(
            _weather_pixels(rows)
        )
    for condition, rows in WEATHER_NIGHT.items():
        assets[f"{_weather_name('night', condition)}.png"] = encode_png(
            _weather_pixels(rows)
        )
    for family, frames in WEATHER_ANIMATION_FRAMES.items():
        for phase, rows in enumerate(frames):
            assets[f"{animation_resource_name(family, phase)}.png"] = encode_png(
                _weather_animation_pixels(rows)
            )
    for name, asset_name in UTILITY_ASSETS.items():
        assets[f"{asset_name}.png"] = encode_png(_utility_pixels(ICONS[name]))
    assets["raster_weather_stale.png"] = encode_png(_stale_pixels())
    assets["preview.png"] = encode_png(_preview_pixels())
    return assets


def _draw_matrix(
    pixels: PixelGrid,
    rows: Sequence[str],
    *,
    x: int,
    y: int,
    pitch: int,
    lit: int,
    color_for: callable,
) -> None:
    for cell_y, row in enumerate(rows):
        for cell_x, symbol in enumerate(row):
            if symbol in ("0", "."):
                continue
            color = color_for(symbol)
            for pixel_y in range(y + cell_y * pitch, y + cell_y * pitch + lit):
                for pixel_x in range(x + cell_x * pitch, x + cell_x * pitch + lit):
                    if 0 <= pixel_y < len(pixels) and 0 <= pixel_x < len(pixels[0]):
                        pixels[pixel_y][pixel_x] = color


def _draw_fine_string(pixels: PixelGrid, text: str, x: int, y: int) -> None:
    cursor = x
    for character in text:
        try:
            rows = FINE_GLYPHS[character]
        except KeyError as error:
            raise ValueError(f"preview uses an undefined fine glyph {character!r}") from error
        _draw_matrix(
            pixels,
            rows,
            x=cursor,
            y=y,
            pitch=FINE_PITCH,
            lit=FINE_LIT,
            color_for=lambda symbol: OPAQUE_WHITE,
        )
        cursor += _fine_advance(character)


def _draw_time(pixels: PixelGrid, text: str, x: int, y: int) -> None:
    if len(text) != 5 or text[2] != ":":
        raise ValueError(f"preview time must use HH:MM, got {text!r}")
    cursor = x
    for character in text:
        if character == ":":
            rows = TIME_COLON
            width = TIME_COLON_WIDTH
        else:
            try:
                rows = TIME_DIGITS[character]
            except KeyError as error:
                raise ValueError(f"preview uses an undefined time glyph {character!r}") from error
            width = TIME_DIGIT_WIDTH
        _draw_matrix(
            pixels,
            rows,
            x=cursor,
            y=y,
            pitch=TIME_PITCH,
            lit=TIME_LIT,
            color_for=lambda symbol: OPAQUE_WHITE,
        )
        cursor += width


def _icon_color(name: str, symbol: str) -> RGBA:
    if name == "weather":
        try:
            return PALETTE[symbol]
        except KeyError as error:
            raise ValueError(f"preview uses an unknown weather symbol {symbol!r}") from error
    return OPAQUE_WHITE


def _draw_information_row(pixels: PixelGrid, name: str, text: str) -> None:
    icon_width = ICON_SIZE
    row_y = ACTIVE_ORIGIN[1] + ROW_BANDS[name][0]
    x = ACTIVE_ORIGIN[0] + ROW_X[name]
    if name == "date":
        text_x = x
        _draw_fine_string(
            pixels,
            text,
            text_x,
            row_y + COMPACT_ROW_TEXT_Y,
        )
        return

    _draw_matrix(
        pixels,
        ICONS[name],
        x=x,
        y=row_y,
        pitch=ICON_PITCH,
        lit=ICON_LIT,
        color_for=lambda symbol: _icon_color(name, symbol),
    )
    text_x = x + icon_width + 2 * FINE_PITCH
    _draw_fine_string(
        pixels,
        text,
        text_x,
        row_y + COMPACT_ROW_TEXT_Y,
    )


def _preview_pixels() -> PixelGrid:
    """Render the fixed review preview from the same source matrices."""

    pixels = _blank(CANVAS, CANVAS, OPAQUE_BLACK)
    _draw_information_row(pixels, "weather", "21°C")
    _draw_information_row(pixels, "date", "SAT 15 AUG")
    _draw_time(
        pixels,
        "10:08",
        ACTIVE_ORIGIN[0] + (ACTIVE_SIZE - TIME_WIDTH) // 2,
        ACTIVE_ORIGIN[1] + ROW_BANDS["time"][0],
    )
    _draw_information_row(pixels, "steps", "03642")
    _draw_information_row(pixels, "battery", "82%")
    return pixels


def _asset_role(name: str) -> str:
    if name == "preview.png":
        return "preview"
    if name == "raster_weather_stale.png":
        return "stale"
    if name.startswith("raster_weather_anim_"):
        return "weather_animation"
    if name.startswith("raster_weather_"):
        return "weather"
    if name.startswith("raster_time_"):
        return "time"
    if name.startswith("raster_icon_"):
        return "icon"
    return "fine"


def _check_palette(name: str, width: int, height: int, pixels: PixelGrid) -> None:
    role = _asset_role(name)
    if role == "preview":
        allowed = {OPAQUE_BLACK, OPAQUE_WHITE, *PALETTE.values()}
        require_opaque = True
    elif role == "weather_animation":
        allowed = {OPAQUE_BLACK, *PALETTE.values()}
        require_opaque = True
    elif role == "weather":
        allowed = {TRANSPARENT, *PALETTE.values()}
        require_opaque = False
    else:
        allowed = {TRANSPARENT, OPAQUE_WHITE}
        require_opaque = False
    for row in pixels:
        for pixel in row:
            if pixel[3] not in (0, 255):
                raise ValueError(f"{name}: alpha must be binary, got {pixel[3]}")
            if require_opaque and pixel[3] != 255:
                raise ValueError(f"{name}: {role} must be fully opaque")
            if pixel not in allowed:
                rgba = "#%02X%02X%02X%02X" % pixel
                raise ValueError(f"{name}: disallowed palette value {rgba}")

    expected_size = {
        "preview": (CANVAS, CANVAS),
        "fine": (
            FINE_SPACE_WIDTH if name.endswith("space.png") else FINE_WIDTH,
            FINE_HEIGHT,
        ),
        "time": (
            TIME_COLON_WIDTH if name.endswith("colon.png") else TIME_DIGIT_WIDTH,
            TIME_HEIGHT,
        ),
        "icon": (ICON_SIZE, ICON_SIZE),
        "weather": (WEATHER_SIZE, WEATHER_SIZE),
        "weather_animation": (WEATHER_SIZE, WEATHER_SIZE),
        "stale": (2 * ICON_PITCH, 2 * ICON_PITCH),
    }[role]
    if (width, height) != expected_size:
        raise ValueError(f"{name}: expected {expected_size[0]}x{expected_size[1]}, got {width}x{height}")
    if role in {"icon", "weather", "weather_animation"}:
        gutter_start = (LAST_DRAWABLE_CELL + 1) * ICON_PITCH
        gutter_pixels = (
            [pixels[y][x] for y in range(height) for x in range(gutter_start, width)]
            + [pixels[y][x] for y in range(gutter_start, height) for x in range(width)]
        )
        expected_gutter = OPAQUE_BLACK if role == "weather_animation" else TRANSPARENT
        if any(pixel != expected_gutter for pixel in gutter_pixels):
            raise ValueError(f"{name}: trailing 3-pixel gutter is not empty")


def _validate_expected(root: Path, expected: dict[str, bytes]) -> None:
    output_dir = root / ASSET_DIR_REL
    if not output_dir.is_dir():
        raise ValueError(f"asset directory is missing: {output_dir}")
    actual = {path.name for path in output_dir.glob("*.png")}
    expected_names = set(expected)
    missing = sorted(expected_names - actual)
    extra = sorted(actual - expected_names)
    if missing:
        raise ValueError("missing generated assets: " + ", ".join(missing))
    if extra:
        raise ValueError("unexpected PNG assets: " + ", ".join(extra))

    for name, expected_data in sorted(expected.items()):
        path = output_dir / name
        actual_data = path.read_bytes()
        if actual_data != expected_data:
            raise ValueError(f"asset drift detected: {path}")
        width, height, pixels = decode_png(actual_data)
        _check_palette(name, width, height, pixels)


def _write_expected(root: Path, expected: dict[str, bytes]) -> int:
    output_dir = root / ASSET_DIR_REL
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
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed PNGs without writing files",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="repository root (defaults to this checkout)",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    expected = _expected_pngs()
    try:
        if args.check:
            _validate_expected(root, expected)
            print(f"Raster 90 assets OK: {len(expected)} PNGs")
        else:
            changed = _write_expected(root, expected)
            _validate_expected(root, expected)
            print(f"Raster 90 assets generated: {len(expected)} PNGs ({changed} changed)")
    except (OSError, ValueError, struct.error, zlib.error) as error:
        print(f"Raster 90 asset check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
