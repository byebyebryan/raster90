#!/usr/bin/env python3
"""Generate and check the tracked Raster 90 icon-family presentation.

The canonical matrices live in ``icons/raster90/family.py`` and
``icons/raster90/animation.py``. This tool writes
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
from icons.raster90.animation import (  # noqa: E402
    FRAME_COUNT,
    FRAME_RATE,
    WEATHER_ANIMATION_FRAMES,
)
from icons.raster90.family import (  # noqa: E402
    APPROVED_STEP_ICON,
    BATTERY_ICON,
    BATTERY_COLOR_BANDS,
    DRAWABLE_CELLS,
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
DRAWABLE_FIELD_BG: RGBA = (22, 48, 64, 255)
OUTPUT_DIR_REL = Path("icons/raster90/preview")

UTILITY_SHEET_NAME = "icon-family-utility-sheet.png"
WEATHER_SHEET_NAME = "icon-family-weather-day-night-sheet.png"
ANIMATION_SHEET_NAME = "icon-family-weather-animation-sheet.png"
ANIMATION_PREVIEW_NAME = "icon-family-weather-animation-preview.gif"
STATE_SHEET_NAME = "icon-family-unavailable-stale-sheet.png"
MATRIX_SHEET_NAME = "icon-family-matrix-3x3-inspection.png"
NATIVE_FACE_NAME = "icon-family-native-face-466.png"
MAGNIFIED_FACE_NAME = "icon-family-magnified-face-932.png"
HTML_NAME = "index.html"

UTILITY_LABELS = {"steps": "STEPS", "battery": "BATTERY"}

ANIMATION_PREVIEW_PHASES: tuple[int, ...] = tuple(range(FRAME_COUNT)) + (0, 0, 0)
ANIMATION_PREVIEW_DELAYS: tuple[int, ...] = (25,) * len(ANIMATION_PREVIEW_PHASES)
ANIMATION_PREVIEW_COLUMNS = 4
ANIMATION_PREVIEW_ROWS = (
    len(WEATHER_ANIMATION_FRAMES) + ANIMATION_PREVIEW_COLUMNS - 1
) // ANIMATION_PREVIEW_COLUMNS
ANIMATION_PREVIEW_MARGIN = 24
ANIMATION_PREVIEW_HEADER = 76
ANIMATION_PREVIEW_CELL_WIDTH = 174
ANIMATION_PREVIEW_CELL_HEIGHT = 184
ANIMATION_PREVIEW_WIDTH = (
    2 * ANIMATION_PREVIEW_MARGIN
    + ANIMATION_PREVIEW_COLUMNS * ANIMATION_PREVIEW_CELL_WIDTH
)
ANIMATION_PREVIEW_HEIGHT = (
    ANIMATION_PREVIEW_HEADER
    + ANIMATION_PREVIEW_ROWS * ANIMATION_PREVIEW_CELL_HEIGHT
    + ANIMATION_PREVIEW_MARGIN
)

GIF_PALETTE: tuple[RGBA, ...] = (
    BLACK,
    WHITE,
    PALETTE["Y"],
    PALETTE["C"],
    PALETTE["B"],
    DRAWABLE_FIELD_BG,
    BLACK,
    BLACK,
)
GIF_COLOR_INDEX = {color: index for index, color in enumerate(GIF_PALETTE[:6])}
GIF_INFINITE_LOOP_EXTENSION = b"\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00"


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


def _gif_lzw(indices: Sequence[int], minimum_code_size: int = 3) -> bytes:
    """Emit the deterministic bounded-dictionary GIF stream used by previews."""

    if not indices:
        raise ValueError("cannot encode an empty GIF frame")
    clear_code = 1 << minimum_code_size
    end_code = clear_code + 1
    code_size = minimum_code_size + 1
    next_code = end_code + 1
    dictionary = {(index,): index for index in range(clear_code)}
    if any(value < 0 or value >= clear_code for value in indices):
        raise ValueError("GIF pixel index exceeds code space")
    codes: list[tuple[int, int]] = [(clear_code, code_size)]
    phrase = (indices[0],)
    for value in indices[1:]:
        extended = phrase + (value,)
        if extended in dictionary:
            phrase = extended
            continue
        codes.append((dictionary[phrase], code_size))
        if next_code < 4096:
            dictionary[extended] = next_code
            next_code += 1
            if next_code > (1 << code_size) and code_size < 12:
                code_size += 1
        else:
            codes.append((clear_code, code_size))
            dictionary = {(index,): index for index in range(clear_code)}
            next_code = end_code + 1
            code_size = minimum_code_size + 1
        phrase = (value,)
    codes.extend(((dictionary[phrase], code_size), (end_code, code_size)))

    packed = bytearray()
    bit_buffer = 0
    bit_count = 0
    for code, width in codes:
        bit_buffer |= code << bit_count
        bit_count += width
        while bit_count >= 8:
            packed.append(bit_buffer & 0xFF)
            bit_buffer >>= 8
            bit_count -= 8
    if bit_count:
        packed.append(bit_buffer & 0xFF)
    return bytes(packed)


def encode_gif(frames: Sequence[PixelGrid], delays: Sequence[int]) -> bytes:
    """Encode a deterministic infinitely looping, full-frame presentation GIF."""

    if not frames or len(frames) != len(delays):
        raise ValueError("GIF requires matching non-empty frames and delays")
    height = len(frames[0])
    width = len(frames[0][0]) if height else 0
    if not width or not height:
        raise ValueError("GIF frames cannot be empty")
    indexed_frames: list[list[int]] = []
    for frame_index, frame in enumerate(frames):
        if len(frame) != height or any(len(row) != width for row in frame):
            raise ValueError(f"GIF frame {frame_index} has inconsistent dimensions")
        try:
            indexed_frames.append(
                [GIF_COLOR_INDEX[pixel] for row in frame for pixel in row]
            )
        except KeyError as error:
            raise ValueError(f"GIF frame uses a non-presentation color: {error.args[0]}") from error

    data = bytearray(b"GIF89a")
    data.extend(struct.pack("<HHBBB", width, height, 0xF2, 0, 0))
    for red, green, blue, _alpha in GIF_PALETTE:
        data.extend((red, green, blue))
    data.extend(GIF_INFINITE_LOOP_EXTENSION)
    for indices, delay in zip(indexed_frames, delays):
        if not 1 <= delay <= 0xFFFF:
            raise ValueError(f"GIF delay outside uint16 range: {delay}")
        data.extend(b"\x21\xF9\x04\x00")
        data.extend(struct.pack("<H", delay))
        data.extend(b"\x00\x00\x2C")
        data.extend(struct.pack("<HHHHB", 0, 0, width, height, 0))
        compressed = _gif_lzw(indices)
        data.append(3)
        for offset in range(0, len(compressed), 255):
            block = compressed[offset : offset + 255]
            data.append(len(block))
            data.extend(block)
        data.append(0)
    data.append(0x3B)
    return bytes(data)


def _gif_dimensions(data: bytes) -> tuple[int, int]:
    if data[:6] not in (b"GIF87a", b"GIF89a") or len(data) < 10:
        raise ValueError("invalid GIF header")
    return struct.unpack("<HH", data[6:10])


def _gif_delays(data: bytes) -> tuple[int, ...]:
    """Read frame delays from the fixed full-frame GIF subset emitted above."""

    _gif_dimensions(data)
    offset = 13
    packed = data[10]
    if packed & 0x80:
        offset += 3 * (2 ** ((packed & 0x07) + 1))
    delays: list[int] = []
    while offset < len(data):
        marker = data[offset]
        if marker == 0x3B:
            break
        if marker == 0x21:
            if offset + 2 >= len(data):
                raise ValueError("truncated GIF extension")
            label = data[offset + 1]
            if label == 0xF9:
                if data[offset + 2] != 4 or offset + 8 > len(data):
                    raise ValueError("invalid GIF graphic control extension")
                delays.append(struct.unpack("<H", data[offset + 4 : offset + 6])[0])
                offset += 8
                continue
            offset += 2
            while True:
                if offset >= len(data):
                    raise ValueError("truncated GIF extension sub-block")
                block_size = data[offset]
                offset += 1
                if block_size == 0:
                    break
                offset += block_size
            continue
        if marker != 0x2C or offset + 10 > len(data):
            raise ValueError(f"unexpected GIF block at offset {offset}")
        local_packed = data[offset + 9]
        offset += 10
        if local_packed & 0x80:
            offset += 3 * (2 ** ((local_packed & 0x07) + 1))
        if offset >= len(data):
            raise ValueError("truncated GIF LZW minimum code size")
        offset += 1
        while True:
            if offset >= len(data):
                raise ValueError("truncated GIF image sub-block")
            block_size = data[offset]
            offset += 1
            if block_size == 0:
                break
            offset += block_size
    return tuple(delays)


def _validate_animation_preview(data: bytes) -> None:
    if _gif_dimensions(data) != (
        ANIMATION_PREVIEW_WIDTH,
        ANIMATION_PREVIEW_HEIGHT,
    ):
        raise ValueError("animation preview GIF dimensions drifted")
    if _gif_delays(data) != ANIMATION_PREVIEW_DELAYS:
        raise ValueError("animation preview GIF cadence drifted")
    if GIF_INFINITE_LOOP_EXTENSION not in data[:128]:
        raise ValueError("animation preview GIF is missing its presentation loop")


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


def _draw_icon_matrix(
    pixels: PixelGrid,
    rows: Sequence[str],
    *,
    x: int,
    y: int,
    pitch: int,
    lit: int,
    color_for: ColorFor,
) -> None:
    """Draw one icon over a presentation-only 15x15 field tint."""

    field_size = DRAWABLE_CELLS * pitch
    for target_y in range(y, y + field_size):
        for target_x in range(x, x + field_size):
            _set_pixel(pixels, target_x, target_y, DRAWABLE_FIELD_BG)
    _draw_matrix(
        pixels,
        rows,
        x=x,
        y=y,
        pitch=pitch,
        lit=lit,
        color_for=color_for,
    )


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


def _rgb_hex(color: RGBA) -> str:
    """Format a canonical RGBA color using the review palette's RGB spelling."""

    return "#%02X%02X%02X" % color[:3]


def _scale_nearest(source: PixelGrid, factor: int) -> PixelGrid:
    if factor < 1:
        raise ValueError("scale factor must be positive")
    return [
        [pixel for pixel in row for _x in range(factor)]
        for row in source
        for _y in range(factor)
    ]


def render_utility_sheet() -> PixelGrid:
    """Show selected utility matrices and all declarative battery tint states."""

    width, height = 980, 420
    pixels = _blank(width, height)
    _draw_text(pixels, "RASTER 90 SELECTED UTILITY ICONS", x=24, y=24)
    _draw_text(pixels, "16X16 STORAGE / 15X15 DRAWABLE / SOLID 3X3", x=24, y=54)
    for index, name in enumerate(("steps", "battery")):
        card_x = 24 + index * 470
        _draw_text(pixels, UTILITY_LABELS[name], x=card_x, y=110)
        rows = SELECTED_UTILITY_ICONS[name]
        _draw_icon_matrix(
            pixels,
            rows,
            x=card_x,
            y=150,
            pitch=12,
            lit=12,
            color_for=_utility_color,
        )
        _draw_text(pixels, "15X15 FIELD / 16X16 TILE", x=card_x, y=350, scale=2)
        if name == "battery":
            _draw_text(pixels, "ICON TINT STATES", x=card_x + 250, y=110, scale=1)
            for state_index, (state_name, _minimum, _maximum, state_color) in enumerate(
                BATTERY_COLOR_BANDS
            ):
                state_x = card_x + 250 + state_index * 54
                _draw_icon_matrix(
                    pixels,
                    rows,
                    x=state_x,
                    y=150,
                    pitch=3,
                    lit=3,
                    color_for=lambda _symbol, color=state_color: color,
                )
                label_x = state_x + (48 - len(state_name) * 6) // 2
                _draw_text(pixels, state_name.upper(), x=label_x, y=210, scale=1)
        else:
            _draw_icon_matrix(
                pixels,
                rows,
                x=card_x + 250,
                y=150,
                pitch=3,
                lit=3,
                color_for=_utility_color,
            )
            _draw_text(pixels, "48X48 RUNTIME TILE", x=card_x + 250, y=210, scale=2)
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
    _draw_text(pixels, "ALL 16 WFF CONDITIONS / DAY + NIGHT / 16X16 STORAGE / 15X15 DRAWABLE", x=24, y=48)
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
        _draw_icon_matrix(
            pixels,
            WEATHER_DAY[condition],
            x=day_x,
            y=icon_y,
            pitch=4,
            lit=4,
            color_for=_weather_color,
        )
        _draw_icon_matrix(
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


def render_animation_sheet() -> PixelGrid:
    """Show every promoted weather family across its eight runtime phases."""

    width = 900
    title_height = 112
    row_height = 84
    height = title_height + len(WEATHER_ANIMATION_FRAMES) * row_height + 16
    label_x = 24
    phase_x = 244
    phase_advance = 80
    pixels = _blank(width, height)
    _draw_text(pixels, "RASTER 90 WEATHER ANIMATION", x=24, y=18)
    _draw_text(
        pixels,
        f"{len(WEATHER_ANIMATION_FRAMES)} FAMILIES / {FRAME_COUNT} PHASES / {FRAME_RATE} FPS / ON VISIBLE ONCE",
        x=24,
        y=48,
    )
    for phase in range(FRAME_COUNT):
        _draw_text(pixels, f"P{phase}", x=phase_x + phase * phase_advance + 22, y=82)
    for family_index, (weather_family, frames) in enumerate(
        WEATHER_ANIMATION_FRAMES.items()
    ):
        row_y = title_height + family_index * row_height
        _draw_text(
            pixels,
            weather_family.replace("_", " ").upper(),
            x=label_x,
            y=row_y + 20,
            scale=2,
        )
        for phase, matrix in enumerate(frames):
            _draw_icon_matrix(
                pixels,
                matrix,
                x=phase_x + phase * phase_advance,
                y=row_y,
                pitch=4,
                lit=4,
                color_for=_weather_color,
            )
    return pixels


def render_animation_preview_frame(phase: int) -> PixelGrid:
    """Render one all-family phase for the compact looping presentation GIF."""

    if not 0 <= phase < FRAME_COUNT:
        raise ValueError(f"animation preview phase outside 0..{FRAME_COUNT - 1}")
    pixels = _blank(ANIMATION_PREVIEW_WIDTH, ANIMATION_PREVIEW_HEIGHT)
    _draw_text(pixels, "RASTER 90 WEATHER MOTION", x=ANIMATION_PREVIEW_MARGIN, y=18)
    _draw_text(
        pixels,
        "8 PHASES AT 4 FPS / 1 SECOND REST / PREVIEW LOOP ONLY",
        x=ANIMATION_PREVIEW_MARGIN,
        y=48,
        scale=2,
    )
    for family_index, (weather_family, frames) in enumerate(
        WEATHER_ANIMATION_FRAMES.items()
    ):
        column = family_index % ANIMATION_PREVIEW_COLUMNS
        row = family_index // ANIMATION_PREVIEW_COLUMNS
        cell_x = ANIMATION_PREVIEW_MARGIN + column * ANIMATION_PREVIEW_CELL_WIDTH
        cell_y = ANIMATION_PREVIEW_HEADER + row * ANIMATION_PREVIEW_CELL_HEIGHT
        _draw_text(
            pixels,
            weather_family.replace("_", " ").upper(),
            x=cell_x,
            y=cell_y,
            scale=1,
        )
        _draw_icon_matrix(
            pixels,
            frames[phase],
            x=cell_x,
            y=cell_y + 24,
            pitch=9,
            lit=9,
            color_for=_weather_color,
        )
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
        _draw_icon_matrix(
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
    """Expose 16x16 storage cells and the 15x15 drawable field beside 3x3 rendering."""

    width, height = 1100, 520
    pixels = _blank(width, height)
    _draw_text(pixels, "MATRIX / PHYSICAL CELL INSPECTION", x=24, y=20)
    _draw_text(pixels, "16X16 STORAGE / 15X15 DRAWABLE; EVERY LIT CELL IS A SOLID 3X3", x=24, y=50)
    entries = (
        ("STEPS", APPROVED_STEP_ICON, _utility_color),
        ("BATTERY", BATTERY_ICON, _utility_color),
        ("WEATHER 14 DAY", WEATHER_DAY[14], _weather_color),
    )
    for index, (label, rows, color_for) in enumerate(entries):
        x = 24 + index * 350
        _draw_text(pixels, label, x=x, y=112)
        _draw_icon_matrix(pixels, rows, x=x, y=154, pitch=12, lit=12, color_for=color_for)
        _draw_text(pixels, "15X15 ART / 12X REVIEW", x=x, y=362, scale=2)
        _draw_icon_matrix(pixels, rows, x=x + 196, y=154, pitch=3, lit=3, color_for=color_for)
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
        name: (
            "data:image/gif;base64,"
            if name.endswith(".gif")
            else "data:image/png;base64,"
        )
        + base64.b64encode(data).decode("ascii")
        for name, data in images.items()
    }
    matrix_data = {
        "steps": list(APPROVED_STEP_ICON),
        "battery": list(BATTERY_ICON),
        "battery_color_bands": [
            {
                "name": name,
                "minimum_exclusive": minimum,
                "maximum_inclusive": maximum,
                "rgba": list(color),
            }
            for name, minimum, maximum, color in BATTERY_COLOR_BANDS
        ],
        "unavailable": list(UNAVAILABLE_WEATHER_ICON),
        "weather_day": {str(index): list(rows) for index, rows in WEATHER_DAY.items()},
        "weather_night": {str(index): list(rows) for index, rows in WEATHER_NIGHT.items()},
        "weather_animation": {
            family: [list(rows) for rows in frames]
            for family, frames in WEATHER_ANIMATION_FRAMES.items()
        },
    }
    matrix_json = json.dumps(matrix_data, indent=2, sort_keys=True)
    battery_contract = ", ".join(
        f"{name} ({'0-10%' if minimum is None else f'>{minimum}%' if maximum is None else f'>{minimum}% through {maximum}%'}) {_rgb_hex(color)}"
        for name, minimum, maximum, color in BATTERY_COLOR_BANDS
    )
    sections = [
        (UTILITY_SHEET_NAME, "Selected utility icons", "steps and battery are the only persistent utility tiles; battery shows all four icon tint states."),
        (WEATHER_SHEET_NAME, "Complete weather resolution", "Every WFF condition ID has a day and night mapping."),
        (ANIMATION_PREVIEW_NAME, "Weather animation preview", "All promoted families loop together for inspection only: eight phases at 4 fps followed by a one-second resting gap. Runtime playback remains one-shot."),
        (ANIMATION_SHEET_NAME, "Promoted weather animation", "Every fresh recognized weather family gets one eight-phase, four-fps on-visible gesture and returns to its static first frame."),
        (STATE_SHEET_NAME, "Truthful weather states", "Unavailable uses the neutral icon plus --; stale keeps a marker distinct from an unavailable value."),
        (MATRIX_SHEET_NAME, "16x16 storage / 15x15 drawable / solid 3x3 inspection", "The matrix views expose project-owned storage cells, the drawable field, and their physical tile expansion."),
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
<code>icons/raster90/family.py</code> and <code>icons/raster90/animation.py</code>
directly; historical calendar, 8x8/12x12, and rejected step alternatives remain
design-only controls.</p>
<p class="note">Palette: {html.escape(json.dumps(dict(PALETTE), sort_keys=True))}</p>
<p class="note">Battery icon tint contract: {html.escape(battery_contract)}. The
percentage remains white and every state reuses the one existing battery resource.</p>
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
    animation_preview = [
        render_animation_preview_frame(phase) for phase in ANIMATION_PREVIEW_PHASES
    ]
    animation_preview_data = encode_gif(
        animation_preview,
        ANIMATION_PREVIEW_DELAYS,
    )
    _validate_animation_preview(animation_preview_data)
    images = {
        UTILITY_SHEET_NAME: encode_png(render_utility_sheet()),
        WEATHER_SHEET_NAME: encode_png(render_weather_sheet()),
        ANIMATION_PREVIEW_NAME: animation_preview_data,
        ANIMATION_SHEET_NAME: encode_png(render_animation_sheet()),
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
