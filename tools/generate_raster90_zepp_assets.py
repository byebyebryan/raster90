#!/usr/bin/env python3
"""Generate the deterministic Raster 90 Amazfit Balance asset surface.

The Zepp watch-face runtime does not consume the Android WFF resources.  This
adapter renders the same project-owned matrices into the PNG resources expected
by a Zeus v3 watch-face package:

    python3 -B tools/generate_raster90_zepp_assets.py
    python3 -B tools/generate_raster90_zepp_assets.py --check

Only the Python standard library is required.  Keeping the PNG writer here
also makes the asset provenance and generated closure independently checkable
without Pillow or ImageMagick.
"""

from __future__ import annotations

import argparse
import binascii
import struct
import sys
import zlib
from pathlib import Path
from typing import Callable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fonts.raster90.family import (  # noqa: E402  (path is intentionally set above)
    PRIMARY_COLON,
    PRIMARY_COLON_CELLS,
    PRIMARY_DIGITS,
    PRIMARY_DIGIT_CELLS,
    PRIMARY_LINE_CELLS,
    RUNTIME_SECONDARY_GLYPHS,
)
from icons.raster90.family import (  # noqa: E402  (canonical icon source)
    BATTERY_COLOR_BANDS,
    LAST_DRAWABLE_CELL,
    MATRIX_CELLS,
    PALETTE,
    SELECTED_UTILITY_ICONS,
    WEATHER_DAY,
    WEATHER_DAY_RESOLUTION,
    WEATHER_NIGHT,
)


RGBA = tuple[int, int, int, int]
PixelGrid = list[list[RGBA]]

# Balance is a native 480x480 round target.  The selected Raster 90 frame is
# still exactly 450x450 (the same fictional 150x150 grid used by WFF), now
# centered with a 15-pixel border on every side.
CANVAS = 480
ACTIVE_ORIGIN = (15, 15)
ACTIVE_SIZE = 450
PICKER_PREVIEW = 324
CELL_PITCH = 3
CELL_LIT = 3

TIME_DIGIT_WIDTH = PRIMARY_DIGIT_CELLS * CELL_PITCH
TIME_COLON_WIDTH = PRIMARY_COLON_CELLS * CELL_PITCH
TIME_HEIGHT = PRIMARY_LINE_CELLS * CELL_PITCH
TIME_WIDTH = 4 * TIME_DIGIT_WIDTH + TIME_COLON_WIDTH

FINE_GLYPH_CELLS = 5
FINE_ADVANCE_CELLS = 6
FINE_SPACE_ADVANCE_CELLS = 2
FINE_WIDTH = FINE_ADVANCE_CELLS * CELL_PITCH
FINE_SPACE_WIDTH = FINE_SPACE_ADVANCE_CELLS * CELL_PITCH
FINE_HEIGHT = 7 * CELL_PITCH

ICON_SIZE = MATRIX_CELLS * CELL_PITCH
WEATHER_SIZE = ICON_SIZE

ASSET_ROOT_REL = Path("watchfaces/raster90-zepp/assets/balance.r")
IMAGE_ROOT_REL = ASSET_ROOT_REL / "images"

TRANSPARENT: RGBA = (0, 0, 0, 0)
OPAQUE_BLACK: RGBA = (0, 0, 0, 255)
OPAQUE_WHITE: RGBA = PALETTE["W"]


# Zepp's documented weather sensor uses a 29-value index, while Raster 90's
# authored family has 16 day/night-resolved families.  Each source condition
# therefore has one explicit nearest truthful family.  Unknown remains the
# neutral icon; no condition is fabricated for an unavailable/no-data result.
ZEPP_WEATHER_TO_FAMILY: Mapping[int, str] = {
    0: "cloudy",          # Cloudy
    1: "rain",            # Showers
    2: "snow",            # Snow Showers
    3: "clear_day",       # Sunny
    4: "cloudy",          # Overcast
    5: "light_rain",      # Light Rain
    6: "light_snow",      # Light Snow
    7: "rain",            # Moderate Rain
    8: "snow",            # Moderate Snow
    9: "heavy_snow",      # Heavy Snow
    10: "heavy_rain",     # Heavy Rain
    11: "windy",          # Sandstorm (nearest authored wind family)
    12: "sleet",           # Rain and Snow
    13: "fog",             # Fog
    14: "mist",            # Hazy
    15: "thunderstorm",   # T-Storms
    16: "heavy_snow",      # Snowstorm
    17: "mist",            # Floating dust
    18: "heavy_rain",      # Very Heavy Rainstorm
    19: "heavy_rain",      # Rain and Hail
    20: "thunderstorm",   # T-Storms and Hail
    21: "heavy_rain",      # Heavy Rainstorm
    22: "mist",            # Dust
    23: "windy",           # Heavy sand storm (nearest authored wind family)
    24: "heavy_rain",      # Rainstorm
    25: "unknown",         # Unknown
    26: "cloudy",          # Cloudy Nighttime
    27: "rain",            # Showers Nighttime
    28: "clear_night",     # Sunny Nighttime
}


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = binascii.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)


def encode_png(pixels: PixelGrid) -> bytes:
    """Encode an RGBA grid with deterministic filter-zero scanlines."""

    if not pixels or not pixels[0]:
        raise ValueError("cannot encode an empty PNG")
    width = len(pixels[0])
    height = len(pixels)
    if any(len(row) != width for row in pixels):
        raise ValueError("pixel rows have inconsistent widths")
    raw = bytearray()
    for row in pixels:
        raw.append(0)
        for red, green, blue, alpha in row:
            raw.extend((red, green, blue, alpha))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", ihdr)
        + _png_chunk(b"IDAT", zlib.compress(bytes(raw), level=9))
        + _png_chunk(b"IEND", b"")
    )


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
    """Decode the RGBA PNG subset emitted by :func:`encode_png`.

    The decoder accepts all standard non-interlaced filter types so ``--check``
    can diagnose a hand-edited resource as well as byte-for-byte drift.
    """

    signature = b"\x89PNG\r\n\x1a\n"
    if not data.startswith(signature):
        raise ValueError("not a PNG")
    offset = len(signature)
    width = height = None
    bit_depth = color_type = interlace = None
    compressed = bytearray()
    saw_iend = False
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
            saw_iend = True
            break
        offset = end + 4
    if width is None or height is None or not saw_iend:
        raise ValueError("PNG is missing IHDR or IEND")
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


def _blank(width: int, height: int, fill: RGBA = TRANSPARENT) -> PixelGrid:
    return [[fill for _ in range(width)] for _ in range(height)]


def _paint_cells(
    rows: Sequence[str],
    *,
    width_cells: int,
    color_for: Callable[[str], RGBA],
) -> PixelGrid:
    """Expand source cells to solid 3x3 pixels while retaining the gutter."""

    if len(rows) == 0 or any(len(row) != width_cells for row in rows):
        raise ValueError("source matrix has inconsistent dimensions")
    pixels = _blank(width_cells * CELL_PITCH, len(rows) * CELL_PITCH)
    for cell_y, row in enumerate(rows):
        for cell_x, symbol in enumerate(row):
            if symbol in ("0", "."):
                continue
            color = color_for(symbol)
            pixel_x = cell_x * CELL_PITCH
            pixel_y = cell_y * CELL_PITCH
            for y in range(pixel_y, pixel_y + CELL_LIT):
                for x in range(pixel_x, pixel_x + CELL_LIT):
                    pixels[y][x] = color
    return pixels


def _fine_pixels(rows: Sequence[str]) -> PixelGrid:
    source_width = len(rows[0]) if rows else 0
    if source_width == FINE_GLYPH_CELLS:
        output_width = FINE_ADVANCE_CELLS
    elif source_width == FINE_SPACE_ADVANCE_CELLS:
        output_width = FINE_SPACE_ADVANCE_CELLS
    else:
        raise ValueError(f"fine glyph has unsupported source width {source_width}")
    if len(rows) != 7 or any(len(row) != source_width for row in rows):
        raise ValueError("fine glyph must be a 5x7 matrix (or 2x7 space)")
    if any(set(row) - {"0", "1"} for row in rows):
        raise ValueError("fine glyph contains an invalid source cell")
    pixels = _paint_cells(rows, width_cells=source_width, color_for=lambda _symbol: OPAQUE_WHITE)
    if output_width > source_width:
        pixels = [row + [TRANSPARENT] * ((output_width - source_width) * CELL_PITCH) for row in pixels]
    return pixels


def _time_pixels(rows: Sequence[str], width_cells: int) -> PixelGrid:
    if len(rows) != PRIMARY_LINE_CELLS or any(len(row) != width_cells for row in rows):
        raise ValueError("time glyph has an invalid source matrix")
    if any(set(row) - {"0", "1"} for row in rows):
        raise ValueError("time glyph contains an invalid source cell")
    return _paint_cells(rows, width_cells=width_cells, color_for=lambda _symbol: OPAQUE_WHITE)


def _icon_pixels(rows: Sequence[str], color_for: Callable[[str], RGBA]) -> PixelGrid:
    if len(rows) != MATRIX_CELLS or any(len(row) != MATRIX_CELLS for row in rows):
        raise ValueError("icon must be a 16x16 matrix")
    if any(rows[LAST_DRAWABLE_CELL + 1][x] != "." for x in range(MATRIX_CELLS)):
        raise ValueError("icon trailing row is not an empty gutter")
    if any(row[LAST_DRAWABLE_CELL + 1] != "." for row in rows):
        raise ValueError("icon trailing column is not an empty gutter")
    return _paint_cells(rows, width_cells=MATRIX_CELLS, color_for=color_for)


def _weather_pixels(rows: Sequence[str]) -> PixelGrid:
    return _icon_pixels(rows, color_for=lambda symbol: PALETTE[symbol])


def _weather_replacement_pixels(rows: Sequence[str]) -> PixelGrid:
    """Render an opaque plane that cleanly replaces the neutral fallback."""

    return [
        [OPAQUE_BLACK if pixel == TRANSPARENT else pixel for pixel in row]
        for row in _weather_pixels(rows)
    ]


def _utility_pixels(rows: Sequence[str], color: RGBA = OPAQUE_WHITE) -> PixelGrid:
    return _icon_pixels(rows, color_for=lambda _symbol: color)


def _concat_horizontal(left: PixelGrid, right: PixelGrid) -> PixelGrid:
    if len(left) != len(right):
        raise ValueError("cannot concatenate images of different heights")
    return [left_row + right_row for left_row, right_row in zip(left, right)]


def _text_name(character: str) -> str:
    names = {" ": "space", "-": "minus", "%": "percent", "°": "degree"}
    return names.get(character, character.lower())


def _fine_advance(character: str) -> int:
    return FINE_SPACE_WIDTH if character == " " else FINE_WIDTH


def _draw_matrix(
    pixels: PixelGrid,
    rows: Sequence[str],
    *,
    x: int,
    y: int,
    color_for: Callable[[str], RGBA],
) -> None:
    for cell_y, row in enumerate(rows):
        for cell_x, symbol in enumerate(row):
            if symbol in ("0", "."):
                continue
            color = color_for(symbol)
            for pixel_y in range(y + cell_y * CELL_PITCH, y + cell_y * CELL_PITCH + CELL_LIT):
                for pixel_x in range(x + cell_x * CELL_PITCH, x + cell_x * CELL_PITCH + CELL_LIT):
                    if 0 <= pixel_y < len(pixels) and 0 <= pixel_x < len(pixels[0]):
                        pixels[pixel_y][pixel_x] = color


def _draw_fine_string(pixels: PixelGrid, text: str, x: int, y: int) -> None:
    cursor = x
    for character in text:
        try:
            rows = RUNTIME_SECONDARY_GLYPHS[character]
        except KeyError as error:
            raise ValueError(f"preview uses an undefined fine glyph {character!r}") from error
        _draw_matrix(pixels, rows, x=cursor, y=y, color_for=lambda _symbol: OPAQUE_WHITE)
        cursor += _fine_advance(character)


def _draw_time(pixels: PixelGrid, text: str, x: int, y: int) -> None:
    if len(text) != 5 or text[2] != ":":
        raise ValueError(f"preview time must use HH:MM, got {text!r}")
    cursor = x
    for character in text:
        if character == ":":
            rows = PRIMARY_COLON
            width = TIME_COLON_WIDTH
            source_width = PRIMARY_COLON_CELLS
        else:
            rows = PRIMARY_DIGITS[character]
            width = TIME_DIGIT_WIDTH
            source_width = PRIMARY_DIGIT_CELLS
        _draw_matrix(pixels, rows, x=cursor, y=y, color_for=lambda _symbol: OPAQUE_WHITE)
        # ``_draw_matrix`` uses the source row width; ``source_width`` makes
        # the cursor advance explicit and protects this layout from accidental
        # assumptions about the glyph's pixel dimensions.
        if len(rows[0]) != source_width:
            raise ValueError("time source width drifted")
        cursor += width


def _family_matrix(family: str) -> Sequence[str]:
    if family == "clear_night":
        return WEATHER_NIGHT[1]
    try:
        condition = WEATHER_DAY_RESOLUTION.index(family)
    except ValueError as error:
        raise ValueError(f"unknown canonical weather family {family!r}") from error
    return WEATHER_DAY[condition]


def _preview_pixels() -> PixelGrid:
    """Render the picker preview from the same native coordinates and matrices."""

    pixels = _blank(CANVAS, CANVAS, OPAQUE_BLACK)
    origin_x, origin_y = ACTIVE_ORIGIN
    # Global native Balance coordinates are active origin + current WFF local
    # coordinates.  The 450x450 frame and every 3x3 cell therefore line up with
    # the runtime composition below.
    weather_x = origin_x + 162
    weather_y = origin_y + 45
    _draw_matrix(
        pixels,
        WEATHER_DAY[14],
        x=weather_x,
        y=weather_y,
        color_for=lambda symbol: PALETTE[symbol],
    )
    _draw_fine_string(pixels, "21°C", weather_x + 54, weather_y + 13)

    date_x = origin_x + 147
    date_y = origin_y + 111
    _draw_fine_string(pixels, "SAT 15 AUG", date_x, date_y + 13)

    _draw_time(
        pixels,
        "10:08",
        origin_x + (ACTIVE_SIZE - TIME_WIDTH) // 2,
        origin_y + 177,
    )

    steps_x = origin_x + 153
    steps_y = origin_y + 291
    _draw_matrix(
        pixels,
        SELECTED_UTILITY_ICONS["steps"],
        x=steps_x,
        y=steps_y,
        color_for=lambda _symbol: OPAQUE_WHITE,
    )
    _draw_fine_string(pixels, "03642", steps_x + ICON_SIZE + 6, steps_y + 13)

    battery_x = origin_x + 171
    battery_y = origin_y + 357
    _draw_matrix(
        pixels,
        SELECTED_UTILITY_ICONS["battery"],
        x=battery_x,
        y=battery_y,
        color_for=lambda _symbol: OPAQUE_WHITE,
    )
    _draw_fine_string(pixels, "82%", battery_x + ICON_SIZE + 6, battery_y + 13)
    return pixels


def _resize_nearest(source: PixelGrid, width: int, height: int) -> PixelGrid:
    if not source or not source[0] or width <= 0 or height <= 0:
        raise ValueError("invalid nearest-neighbor resize dimensions")
    source_height = len(source)
    source_width = len(source[0])
    if any(len(row) != source_width for row in source):
        raise ValueError("source rows have inconsistent widths")
    return [
        [source[(out_y * source_height) // height][(out_x * source_width) // width]
         for out_x in range(width)]
        for out_y in range(height)
    ]


def expected_assets() -> dict[str, bytes]:
    """Return the complete deterministic ``images/`` closure."""

    assets: dict[str, bytes] = {}
    for character, rows in RUNTIME_SECONDARY_GLYPHS.items():
        assets[f"text/{_text_name(character)}.png"] = encode_png(_fine_pixels(rows))

    for digit, rows in PRIMARY_DIGITS.items():
        assets[f"time/{digit}.png"] = encode_png(_time_pixels(rows, PRIMARY_DIGIT_CELLS))
    assets["time/colon.png"] = encode_png(_time_pixels(PRIMARY_COLON, PRIMARY_COLON_CELLS))

    degree = _fine_pixels(RUNTIME_SECONDARY_GLYPHS["°"])
    assets["unit/celsius.png"] = encode_png(
        _concat_horizontal(degree, _fine_pixels(RUNTIME_SECONDARY_GLYPHS["C"]))
    )
    assets["unit/fahrenheit.png"] = encode_png(
        _concat_horizontal(degree, _fine_pixels(RUNTIME_SECONDARY_GLYPHS["F"]))
    )
    minus = _fine_pixels(RUNTIME_SECONDARY_GLYPHS["-"])
    assets["text/double-minus.png"] = encode_png(_concat_horizontal(minus, minus))

    assets["utility/steps.png"] = encode_png(_utility_pixels(SELECTED_UTILITY_ICONS["steps"]))
    assets["utility/battery.png"] = encode_png(_utility_pixels(SELECTED_UTILITY_ICONS["battery"]))
    for band_name, _minimum, _maximum, color in BATTERY_COLOR_BANDS:
        assets[f"utility/battery-{band_name}.png"] = encode_png(
            _utility_pixels(SELECTED_UTILITY_ICONS["battery"], color)
        )

    for condition in range(29):
        family = ZEPP_WEATHER_TO_FAMILY[condition]
        matrix = _family_matrix(family)
        assets[f"weather/{condition:02d}.png"] = encode_png(_weather_pixels(matrix))
        assets[f"weather-bound/{condition:02d}.png"] = encode_png(
            _weather_replacement_pixels(matrix)
        )

    preview = _resize_nearest(_preview_pixels(), PICKER_PREVIEW, PICKER_PREVIEW)
    assets["preview.png"] = encode_png(preview)
    return assets


def _role_for_asset(name: str) -> str:
    if name == "preview.png":
        return "preview"
    return name.split("/", 1)[0]


def _check_palette_and_size(name: str, width: int, height: int, pixels: PixelGrid) -> None:
    role = _role_for_asset(name)
    if role == "preview":
        allowed = {OPAQUE_BLACK, OPAQUE_WHITE, *PALETTE.values()}
        expected_size = (PICKER_PREVIEW, PICKER_PREVIEW)
        require_opaque = True
    elif role == "time":
        allowed = {TRANSPARENT, OPAQUE_WHITE}
        expected_size = (TIME_COLON_WIDTH if name.endswith("colon.png") else TIME_DIGIT_WIDTH, TIME_HEIGHT)
        require_opaque = False
    elif role == "text":
        allowed = {TRANSPARENT, OPAQUE_WHITE}
        if name.endswith("space.png"):
            expected_width = FINE_SPACE_WIDTH
        elif name.endswith("double-minus.png"):
            expected_width = 2 * FINE_WIDTH
        else:
            expected_width = FINE_WIDTH
        expected_size = (expected_width, FINE_HEIGHT)
        require_opaque = False
    elif role == "unit":
        allowed = {TRANSPARENT, OPAQUE_WHITE}
        expected_size = (2 * FINE_WIDTH, FINE_HEIGHT)
        require_opaque = False
    elif role == "utility":
        # A tinted battery is intentionally a separate static resource; this
        # keeps runtime support independent of optional color/tint APIs.
        allowed = {TRANSPARENT, OPAQUE_WHITE, *PALETTE.values(), (255, 133, 0, 255), (255, 48, 48, 255)}
        expected_size = (ICON_SIZE, ICON_SIZE)
        require_opaque = False
    elif role == "weather":
        allowed = {TRANSPARENT, *PALETTE.values()}
        expected_size = (WEATHER_SIZE, WEATHER_SIZE)
        require_opaque = False
    elif role == "weather-bound":
        allowed = {OPAQUE_BLACK, *PALETTE.values()}
        expected_size = (WEATHER_SIZE, WEATHER_SIZE)
        require_opaque = True
    else:
        raise ValueError(f"unrecognized generated asset role {role!r}")
    if (width, height) != expected_size:
        raise ValueError(f"{name}: expected {expected_size[0]}x{expected_size[1]}, got {width}x{height}")
    for row in pixels:
        for pixel in row:
            if pixel[3] not in (0, 255):
                raise ValueError(f"{name}: alpha must be binary, got {pixel[3]}")
            if require_opaque and pixel[3] != 255:
                raise ValueError(f"{name}: preview must be fully opaque")
            if pixel not in allowed:
                raise ValueError(f"{name}: disallowed palette value {pixel!r}")

    if role in {"weather", "utility"}:
        gutter_start = (LAST_DRAWABLE_CELL + 1) * CELL_PITCH
        gutter = (
            [pixels[y][x] for y in range(height) for x in range(gutter_start, width)]
            + [pixels[y][x] for y in range(gutter_start, height) for x in range(width)]
        )
        if any(pixel != TRANSPARENT for pixel in gutter):
            raise ValueError(f"{name}: trailing 3-pixel gutter is not transparent")
    elif role == "weather-bound":
        gutter_start = (LAST_DRAWABLE_CELL + 1) * CELL_PITCH
        gutter = (
            [pixels[y][x] for y in range(height) for x in range(gutter_start, width)]
            + [pixels[y][x] for y in range(gutter_start, height) for x in range(width)]
        )
        if any(pixel != OPAQUE_BLACK for pixel in gutter):
            raise ValueError(f"{name}: trailing 3-pixel replacement gutter is not opaque black")


def validate_expected(root: Path, expected: Mapping[str, bytes] | None = None) -> None:
    """Verify byte closure, dimensions, palette, and source-cell gutter."""

    if expected is None:
        expected = expected_assets()
    output_dir = root.resolve() / IMAGE_ROOT_REL
    if not output_dir.is_dir():
        raise ValueError(f"asset directory is missing: {output_dir}")
    actual = {
        path.relative_to(output_dir).as_posix()
        for path in output_dir.rglob("*.png")
        if path.is_file()
    }
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
        _check_palette_and_size(name, width, height, pixels)


def _write_expected(root: Path, expected: Mapping[str, bytes]) -> int:
    output_dir = root.resolve() / IMAGE_ROOT_REL
    output_dir.mkdir(parents=True, exist_ok=True)
    changed = 0
    for name, data in sorted(expected.items()):
        path = output_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
            changed += 1
    return changed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated PNGs without writing")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (defaults to this checkout)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    expected = expected_assets()
    try:
        if args.check:
            validate_expected(root, expected)
            print(f"Raster 90 Zepp assets OK: {len(expected)} PNGs")
        else:
            changed = _write_expected(root, expected)
            validate_expected(root, expected)
            print(f"Raster 90 Zepp assets generated: {len(expected)} PNGs ({changed} changed)")
    except (OSError, ValueError, struct.error, zlib.error) as error:
        print(f"Raster 90 Zepp asset check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
