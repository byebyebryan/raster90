#!/usr/bin/env python3
"""Render the deterministic Raster 90 icon-led design study.

The output is intentionally design-only.  It never writes under a packaged
resource directory; all generated review files go beneath ``outputs/``.  The
study compares an all-8x8 composition with a mixed composition containing one
12x12 weather feature and the same 8x8 utility icons at native 466x466 and a
nearest-neighbour 454x454 design approximation.

Examples::

    python3 -B tools/render_raster90_icon_studies.py
    python3 -B tools/render_raster90_icon_studies.py --check

``--check`` recomputes every PNG and report byte-for-byte, while validating
matrices, geometry, and the binary/flat-palette rules without rewriting outputs.
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
sys.path.insert(0, str(ROOT / "design" / "raster90"))

from icon_studies import (  # noqa: E402 (path intentionally set above)
    ACTIVE_ORIGIN,
    ACTIVE_SIZE,
    BATTERY_STYLES,
    CALENDAR_ICONS,
    CANVAS,
    COARSE_LIT,
    COARSE_PITCH,
    FINE_LIT,
    FINE_PITCH,
    FOCUS_BATTERY_ICONS,
    FOCUS_CALENDAR_ICONS,
    FOCUS_STEP_12,
    FOCUS_WEATHER_12,
    SAFE_CENTER,
    SAFE_RADIUS,
    STEP_ICONS,
    STUDY_STATES,
    STUDY_VARIANTS,
    WEATHER_8,
    WEATHER_12,
    validate_study_matrices,
)

from matrices import COARSE_COLON, COARSE_DIGITS, FINE_GLYPHS, PALETTE  # noqa: E402


RGBA = tuple[int, int, int, int]
PixelGrid = list[list[RGBA]]

BLACK: RGBA = (0, 0, 0, 255)
WHITE: RGBA = (255, 255, 255, 255)
WEATHER_COLORS: Mapping[str, RGBA] = PALETTE

OUTPUT_DIR_REL = Path("outputs/raster90/studies/iconography")
STATES = ("available", "unavailable", "worst")
VARIANTS = ("all8", "mixed12")
TARGETS = (466, 454)


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
    return [[fill for _ in range(width)] for _ in range(height)]


def _set_pixel(pixels: PixelGrid, x: int, y: int, color: RGBA) -> None:
    if 0 <= y < len(pixels) and 0 <= x < len(pixels[0]):
        pixels[y][x] = color


def _draw_matrix(
    pixels: PixelGrid,
    rows: Sequence[str],
    *,
    x: int,
    y: int,
    pitch: int = FINE_PITCH,
    lit: int = FINE_LIT,
    color_for,
) -> None:
    """Paint source cells with hard square edges and no antialiasing."""

    for cell_y, row in enumerate(rows):
        for cell_x, symbol in enumerate(row):
            if symbol in ("0", "."):
                continue
            color = color_for(symbol)
            for pixel_y in range(y + cell_y * pitch, y + cell_y * pitch + lit):
                for pixel_x in range(x + cell_x * pitch, x + cell_x * pitch + lit):
                    _set_pixel(pixels, pixel_x, pixel_y, color)


def _fine_advance(character: str) -> int:
    return 10 if character == " " else 30


def _fine_width(text: str) -> int:
    return sum(_fine_advance(character) for character in text)


def _draw_fine_text(pixels: PixelGrid, text: str, *, x: int, y: int) -> None:
    cursor = x
    for character in text:
        try:
            rows = FINE_GLYPHS[character]
        except KeyError as error:
            raise ValueError(f"study text uses undefined fine glyph {character!r}") from error
        _draw_matrix(
            pixels,
            rows,
            x=cursor,
            y=y,
            pitch=FINE_PITCH,
            lit=FINE_LIT,
            color_for=lambda _symbol: WHITE,
        )
        cursor += _fine_advance(character)


def _draw_coarse_time(pixels: PixelGrid, *, x: int, y: int) -> None:
    """Paint the existing coarse ``10:08`` artwork without changing it."""

    cursor = x
    for character in "10:08":
        if character == ":":
            rows = COARSE_COLON
            width = 3 * COARSE_PITCH
        else:
            rows = COARSE_DIGITS[character]
            width = 8 * COARSE_PITCH
        _draw_matrix(
            pixels,
            rows,
            x=cursor,
            y=y,
            pitch=COARSE_PITCH,
            lit=COARSE_LIT,
            color_for=lambda _symbol: WHITE,
        )
        cursor += width


def _weather_rows(variant_name: str, condition: str) -> Sequence[str]:
    source = WEATHER_8 if STUDY_VARIANTS[variant_name]["weather_size"] == 8 else WEATHER_12
    return source[condition]


def _weather_color(symbol: str) -> RGBA:
    try:
        return WEATHER_COLORS[symbol]
    except KeyError as error:
        raise ValueError(f"unknown study weather palette symbol {symbol!r}") from error


def _centered_group_x(width: int) -> int:
    if width > ACTIVE_SIZE:
        raise ValueError(f"study group is wider than active frame: {width}")
    return ACTIVE_ORIGIN[0] + (ACTIVE_SIZE - width) // 2


def _draw_icon_value_row(
    pixels: PixelGrid,
    *,
    rows: Sequence[str],
    text: str,
    band: tuple[int, int],
    icon_pitch: int = FINE_PITCH,
    icon_lit: int = FINE_LIT,
    icon_color_for,
) -> int:
    icon_size = len(rows) * icon_pitch
    text_width = _fine_width(text)
    total_width = icon_size + 10 + text_width
    x = _centered_group_x(total_width)
    start, end = band
    band_height = end - start
    icon_y = ACTIVE_ORIGIN[1] + start + (band_height - icon_size) // 2
    text_y = ACTIVE_ORIGIN[1] + start + (band_height - 35) // 2
    _draw_matrix(
        pixels,
        rows,
        x=x,
        y=icon_y,
        pitch=icon_pitch,
        lit=icon_lit,
        color_for=icon_color_for,
    )
    _draw_fine_text(pixels, text, x=x + icon_size + 10, y=text_y)
    return total_width


def render_variant_state(variant_name: str, state_name: str) -> PixelGrid:
    """Render one native 466x466 study state."""

    validate_study_matrices()
    variant = STUDY_VARIANTS[variant_name]
    state = STUDY_STATES[state_name]
    pixels = _blank(CANVAS, CANVAS)
    active_y = ACTIVE_ORIGIN[1]
    bands = variant["bands"]
    icon_set = variant["icon_set"]

    weather_rows = _weather_rows(variant_name, state["weather"])
    _draw_icon_value_row(
        pixels,
        rows=weather_rows,
        text=state["temperature"],
        band=bands["weather"],
        icon_color_for=_weather_color,
    )
    _draw_icon_value_row(
        pixels,
        rows=CALENDAR_ICONS[icon_set["calendar"]],
        text=state["date"],
        band=bands["date"],
        icon_color_for=lambda _symbol: WHITE,
    )

    _draw_coarse_time(pixels, x=ACTIVE_ORIGIN[0] + 50, y=active_y + bands["time"][0])

    _draw_icon_value_row(
        pixels,
        rows=STEP_ICONS[icon_set["steps"]],
        text=state["steps"],
        band=bands["steps"],
        icon_color_for=lambda _symbol: WHITE,
    )
    _draw_icon_value_row(
        pixels,
        rows=BATTERY_STYLES[icon_set["battery"]][state["battery_level"]],
        text=state["battery"],
        band=bands["battery"],
        icon_color_for=lambda _symbol: WHITE,
    )
    return pixels


def resize_nearest(pixels: PixelGrid, target_size: int) -> PixelGrid:
    """Scale a native study image with nearest-neighbour sampling.

    The result is a design approximation of the official 454x454 target.  It
    intentionally avoids antialiasing; the Wear renderer remains authoritative
    for actual WFF scaling and cell placement.
    """

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


def _draw_label(
    pixels: PixelGrid,
    text: str,
    *,
    x: int,
    y: int,
    cell_scale: int = 2,
    color: RGBA = WHITE,
) -> None:
    """Draw a tiny hard-edged label using the existing fine glyph vocabulary."""

    cursor = x
    for character in text.upper():
        rows = FINE_GLYPHS.get(character, FINE_GLYPHS["?"])
        for row_index, row in enumerate(rows):
            for column_index, symbol in enumerate(row):
                if symbol == "1":
                    for dy in range(cell_scale):
                        for dx in range(cell_scale):
                            _set_pixel(
                                pixels,
                                cursor + column_index * cell_scale + dx,
                                y + row_index * cell_scale + dy,
                                color,
                            )
        cursor += (6 if character != " " else 2) * cell_scale


def _draw_panel(
    target: PixelGrid,
    source: PixelGrid,
    *,
    x: int,
    y: int,
) -> None:
    for row_index, row in enumerate(source):
        for column_index, pixel in enumerate(row):
            _set_pixel(target, x + column_index, y + row_index, pixel)


def build_comparison_sheet(target_size: int) -> PixelGrid:
    """Build a two-column, three-state comparison sheet."""

    label_height = 24
    gap = 10
    panel_width = target_size
    width = 2 * panel_width + gap
    row_height = target_size + label_height + gap
    pixels = _blank(width, len(STATES) * row_height - gap)
    for state_index, state_name in enumerate(STATES):
        row_y = state_index * row_height
        for variant_index, variant_name in enumerate(VARIANTS):
            panel_x = variant_index * (panel_width + gap)
            label = f"{variant_name} {state_name} {target_size}"
            _draw_label(pixels, label, x=panel_x + 4, y=row_y + 3, cell_scale=2)
            rendered = render_variant_state(variant_name, state_name)
            if target_size != CANVAS:
                rendered = resize_nearest(rendered, target_size)
            _draw_panel(target=pixels, source=rendered, x=panel_x, y=row_y + label_height)
    return pixels


def _icon_entries() -> list[tuple[str, Sequence[str], object]]:
    entries: list[tuple[str, Sequence[str], object]] = []
    entries.extend((f"CALENDAR {name.replace('_', ' ')}", rows, "utility") for name, rows in CALENDAR_ICONS.items())
    entries.extend((f"STEPS {name.replace('_', ' ')}", rows, "utility") for name, rows in STEP_ICONS.items())
    for style_name, states in BATTERY_STYLES.items():
        for state_name in ("empty", "low", "mid", "high", "full", "charging"):
            entries.append((f"BAT {style_name.replace('_', ' ')} {state_name.replace('_', ' ')}", states[state_name], "utility"))
    for size, group in ((8, WEATHER_8), (12, WEATHER_12)):
        for condition in ("clear_day", "partly_cloudy", "rain", "clear_night", "unavailable"):
            entries.append((f"WX {size} {condition.replace('_', ' ')}", group[condition], "weather"))
    return entries


def _icon_label_lines(label: str) -> tuple[str, ...]:
    """Split candidate labels without making the matrix itself ambiguous."""

    words = label.split()
    if len(words) <= 2:
        return (label,)
    split = 2 if words[0] == "BAT" else 1
    return (" ".join(words[:split]), " ".join(words[split:]))


def build_icon_sheet() -> PixelGrid:
    """Build an enlarged matrix comparison sheet for human review."""

    panel_width = 280
    panel_height = 292
    columns = 5
    entries = _icon_entries()
    rows = (len(entries) + columns - 1) // columns
    pixels = _blank(columns * panel_width, rows * panel_height)
    icon_scale = 18
    label_scale = 2
    for index, (label, matrix, role) in enumerate(entries):
        panel_x = (index % columns) * panel_width
        panel_y = (index // columns) * panel_height
        icon_size = len(matrix) * icon_scale
        icon_x = panel_x + (panel_width - icon_size) // 2
        icon_y = panel_y + 22
        color_for = _weather_color if role == "weather" else (lambda _symbol: WHITE)
        _draw_matrix(
            pixels,
            matrix,
            x=icon_x,
            y=icon_y,
            pitch=icon_scale,
            lit=icon_scale - 2,
            color_for=color_for,
        )
        # Labels are split at the final semantic boundary so they remain
        # readable under the largest 12x12 specimens.
        lines = _icon_label_lines(label)
        for line_index, line in enumerate(lines):
            label_width = sum((6 if char != " " else 2) * label_scale for char in line)
            _draw_label(
                pixels,
                line,
                x=panel_x + (panel_width - label_width) // 2,
                y=panel_y + 238 + line_index * 18,
                cell_scale=label_scale,
            )
    return pixels


def build_actual_size_icon_sheet() -> PixelGrid:
    """Render every candidate at the real 5-unit pitch for native-size review."""

    panel_width = 170
    panel_height = 88
    columns = 5
    entries = _icon_entries()
    rows = (len(entries) + columns - 1) // columns
    pixels = _blank(columns * panel_width, rows * panel_height)
    for index, (label, matrix, role) in enumerate(entries):
        panel_x = (index % columns) * panel_width
        panel_y = (index // columns) * panel_height
        icon_size = len(matrix) * FINE_PITCH
        icon_x = panel_x + (panel_width - icon_size) // 2
        icon_y = panel_y + max(2, (62 - icon_size) // 2)
        color_for = _weather_color if role == "weather" else (lambda _symbol: WHITE)
        _draw_matrix(
            pixels,
            matrix,
            x=icon_x,
            y=icon_y,
            pitch=FINE_PITCH,
            lit=FINE_LIT,
            color_for=color_for,
        )
        lines = _icon_label_lines(label)
        for line_index, line in enumerate(lines):
            label_scale = 1
            label_width = sum((6 if char != " " else 2) * label_scale for char in line)
            _draw_label(
                pixels,
                line,
                x=panel_x + (panel_width - label_width) // 2,
                y=panel_y + 66 + line_index * 9,
                cell_scale=label_scale,
            )
    return pixels


def _focus_icon_entries() -> list[tuple[str, Sequence[str], object]]:
    """Return baseline and second-pass candidates for isolated review."""

    entries: list[tuple[str, Sequence[str], object]] = [
        ("CAL BASELINE", CALENDAR_ICONS["page"], "utility"),
        ("STEPS BASELINE", STEP_ICONS["walking_person"], "utility"),
        ("BAT BASELINE HIGH", BATTERY_STYLES["bar"]["high"], "utility"),
    ]
    entries.extend(
        (f"CAL {name.replace('_', ' ')}", rows, "utility")
        for name, rows in FOCUS_CALENDAR_ICONS.items()
        if name in ("tearoff", "rings")
    )
    entries.append(("STEPS SHOE 8", STEP_ICONS["shoe"], "utility"))
    entries.extend(
        (f"STEPS {name.replace('_', ' ')} 12", rows, "utility")
        for name, rows in FOCUS_STEP_12.items()
    )
    for state_name in ("high", "charging"):
        entries.append(
            (
                f"BAT COMPACT {state_name.replace('_', ' ')}",
                FOCUS_BATTERY_ICONS[state_name],
                "utility",
            )
        )
    for condition in ("clear_day", "partly_cloudy", "rain", "clear_night", "unavailable"):
        entries.append((f"WX DENSE {condition.replace('_', ' ')}", WEATHER_12[condition], "weather"))
    for family_name, family in FOCUS_WEATHER_12.items():
        for condition in ("clear_day", "partly_cloudy", "rain", "clear_night", "unavailable"):
            entries.append(
                (
                    f"WX {family_name.replace('_', ' ')} {condition.replace('_', ' ')}",
                    family[condition],
                    "weather",
                )
            )
    return entries


def build_focus_icon_sheet(*, actual_size: bool) -> PixelGrid:
    """Render only the focused icon alternatives, including their baseline."""

    entries = _focus_icon_entries()
    columns = 5
    if actual_size:
        panel_width = 190
        panel_height = 96
        icon_pitch = FINE_PITCH
        icon_lit = FINE_LIT
        icon_area_height = 66
        label_y = 70
        label_scale = 1
    else:
        panel_width = 280
        panel_height = 286
        icon_pitch = 17
        icon_lit = 15
        icon_area_height = 220
        label_y = 236
        label_scale = 2
    row_count = (len(entries) + columns - 1) // columns
    pixels = _blank(columns * panel_width, row_count * panel_height)
    for index, (label, matrix, role) in enumerate(entries):
        panel_x = (index % columns) * panel_width
        panel_y = (index // columns) * panel_height
        icon_width = len(matrix[0]) * icon_pitch
        icon_height = len(matrix) * icon_pitch
        icon_x = panel_x + (panel_width - icon_width) // 2
        icon_y = panel_y + max(2, (icon_area_height - icon_height) // 2)
        color_for = _weather_color if role == "weather" else (lambda _symbol: WHITE)
        _draw_matrix(
            pixels,
            matrix,
            x=icon_x,
            y=icon_y,
            pitch=icon_pitch,
            lit=icon_lit,
            color_for=color_for,
        )
        for line_index, line in enumerate(_icon_label_lines(label)):
            label_width = sum((6 if character != " " else 2) * label_scale for character in line)
            _draw_label(
                pixels,
                line,
                x=panel_x + (panel_width - label_width) // 2,
                y=panel_y + label_y + line_index * (9 * label_scale),
                cell_scale=label_scale,
            )
    return pixels


def _focus_context_entries() -> list[tuple[str, Sequence[str], str, object]]:
    return [
        ("CAL BASELINE", CALENDAR_ICONS["page"], "SAT 15 AUG", "utility"),
        ("CAL TEAROFF", FOCUS_CALENDAR_ICONS["tearoff"], "SAT 15 AUG", "utility"),
        ("CAL RINGS", FOCUS_CALENDAR_ICONS["rings"], "SAT 15 AUG", "utility"),
        ("STEPS BASELINE", STEP_ICONS["walking_person"], "03642", "utility"),
        ("STEPS SHOE 8", STEP_ICONS["shoe"], "03642", "utility"),
        ("STEPS WALKER A 12", FOCUS_STEP_12["walker_a"], "03642", "utility"),
        ("STEPS WALKER B 12", FOCUS_STEP_12["walker_b"], "03642", "utility"),
        ("BAT BASELINE", BATTERY_STYLES["bar"]["high"], "82%", "utility"),
        ("BAT COMPACT", FOCUS_BATTERY_ICONS["high"], "82%", "utility"),
        ("WX DENSE", WEATHER_12["partly_cloudy"], "21°C", "weather"),
        ("WX OUTLINE", FOCUS_WEATHER_12["outline"]["partly_cloudy"], "21°C", "weather"),
        ("WX SPRITE", FOCUS_WEATHER_12["sprite"]["partly_cloudy"], "21°C", "weather"),
    ]


def build_focus_row_context_sheet() -> PixelGrid:
    """Show candidates beside real row text without composing a full face."""

    entries = _focus_context_entries()
    columns = 2
    panel_width = 430
    panel_height = 92
    row_count = (len(entries) + columns - 1) // columns
    pixels = _blank(columns * panel_width, row_count * panel_height)
    for index, (label, matrix, value, role) in enumerate(entries):
        panel_x = (index % columns) * panel_width
        panel_y = (index // columns) * panel_height
        _draw_label(pixels, label, x=panel_x + 4, y=panel_y + 3, cell_scale=1)
        icon_width = len(matrix[0]) * FINE_PITCH
        icon_height = len(matrix) * FINE_PITCH
        content_top = panel_y + 22
        content_height = 66
        icon_x = panel_x + 26
        icon_y = content_top + (content_height - icon_height) // 2
        color_for = _weather_color if role == "weather" else (lambda _symbol: WHITE)
        _draw_matrix(
            pixels,
            matrix,
            x=icon_x,
            y=icon_y,
            pitch=FINE_PITCH,
            lit=FINE_LIT,
            color_for=color_for,
        )
        _draw_fine_text(
            pixels,
            value,
            x=icon_x + icon_width + 10,
            y=content_top + (content_height - 35) // 2,
        )
    return pixels


def _matrix_metrics(matrix: Sequence[str]) -> tuple[int, int, int, int, int]:
    live = [
        (x, y)
        for y, row in enumerate(matrix)
        for x, symbol in enumerate(row)
        if symbol not in ("0", ".")
    ]
    if not live:
        return 0, 0, 0, 0, 0
    min_x = min(x for x, _y in live)
    max_x = max(x for x, _y in live)
    min_y = min(y for _x, y in live)
    max_y = max(y for _x, y in live)
    return len(live), min_x, min_y, max_x, max_y


def focus_metrics_text() -> str:
    """Describe canvas use so visual mass can be reviewed explicitly."""

    lines = [
        "Raster 90 focused icon metrics",
        "==============================",
        "Counts measure live source cells, not rendered 4x4 subpixels.",
        "A 12x12 canvas does not imply a 12x12 live bounding box.",
        "",
    ]
    for label, matrix, _role in _focus_icon_entries():
        count, min_x, min_y, max_x, max_y = _matrix_metrics(matrix)
        width = max_x - min_x + 1 if count else 0
        height = max_y - min_y + 1 if count else 0
        canvas_cells = len(matrix) * len(matrix[0])
        lines.append(
            f"{label:30s} canvas={len(matrix[0])}x{len(matrix)} "
            f"live={count:3d}/{canvas_cells:3d} bbox={width}x{height} "
            f"origin=({min_x},{min_y})"
        )
    return "\n".join(lines) + "\n"


def _chord_at(y: float) -> float:
    distance = abs(y - SAFE_CENTER[1])
    if distance > SAFE_RADIUS:
        return 0.0
    return 2.0 * math.sqrt(SAFE_RADIUS**2 - distance**2)


def _row_widths(variant_name: str, state_name: str) -> Mapping[str, int]:
    variant = STUDY_VARIANTS[variant_name]
    state = STUDY_STATES[state_name]
    weather_size = int(variant["weather_size"])
    return {
        "weather": weather_size * FINE_PITCH + 10 + _fine_width(state["temperature"]),
        "date": 8 * FINE_PITCH + 10 + _fine_width(state["date"]),
        "time": 350,
        "steps": 8 * FINE_PITCH + 10 + _fine_width(state["steps"]),
        "battery": 8 * FINE_PITCH + 10 + _fine_width(state["battery"]),
    }


def build_geometry_report() -> dict[str, object]:
    """Return machine-readable geometry and palette evidence."""

    variants: dict[str, object] = {}
    for variant_name in VARIANTS:
        variant = STUDY_VARIANTS[variant_name]
        bands = variant["bands"]
        rows: dict[str, object] = {}
        for region in ("weather", "date", "time", "steps", "battery"):
            start, end = bands[region]
            state_widths = {
                state_name: _row_widths(variant_name, state_name)[region]
                for state_name in STATES
            }
            required_width = max(state_widths.values())
            edge_candidates = (start, end)
            safe_y = max(edge_candidates, key=lambda value: abs(value - SAFE_CENTER[1]))
            chord = _chord_at(safe_y)
            margin = chord - required_width
            margin_total = round(margin, 3)
            rows[region] = {
                "y_band": [start, end],
                "state_widths": state_widths,
                "required_width": required_width,
                "safe_chord_at_farthest_edge": round(chord, 3),
                "safe_edge_y": safe_y,
                "safe_margin_total": margin_total,
                "safe_margin_per_side": round(margin_total / 2, 3),
                "valid": margin >= 0,
            }
        gap_values = []
        ordered = ("weather", "date", "time", "steps", "battery")
        for previous, current in zip(ordered, ordered[1:]):
            gap_values.append(bands[current][0] - bands[previous][1])
        variants[variant_name] = {
            "label": variant["label"],
            "description": variant["description"],
            "weather_size": variant["weather_size"],
            "icon_set": dict(variant["icon_set"]),
            "bands": {region: list(bands[region]) for region in ordered},
            "gaps": gap_values,
            "time_center_offset_from_active_center": variant["time_center_offset"],
            "rows": rows,
            "all_safe_margins_nonnegative": all(row["valid"] for row in rows.values()),
        }
    return {
        "study": "Raster 90 icon-led design study",
        "design_only": True,
        "native_canvas": [CANVAS, CANVAS],
        "scaled_canvas": [454, 454],
        "scaled_canvas_note": "454 output uses nearest-neighbour resampling as a design approximation; the Wear renderer remains authoritative.",
        "active_origin": list(ACTIVE_ORIGIN),
        "active_size": ACTIVE_SIZE,
        "fine_pitch": FINE_PITCH,
        "fine_lit": FINE_LIT,
        "coarse_pitch": COARSE_PITCH,
        "coarse_lit": COARSE_LIT,
        "safe_circle": {"center": list(SAFE_CENTER), "radius": SAFE_RADIUS},
        "weather_palette": {key: list(value) for key, value in WEATHER_COLORS.items()},
        "states": {name: dict(value) for name, value in STUDY_STATES.items()},
        "variants": variants,
    }


def geometry_text(report: Mapping[str, object]) -> str:
    lines = [
        "Raster 90 icon-led design study geometry",
        "==========================================",
        "Design-only artifacts; no WFF runtime geometry is changed.",
        "Native canvas: 466x466; active frame: 450x450 at (8,8).",
        "Fine lattice: 5-unit pitch / 4-unit lit cell; coarse lattice: 10/8.",
        "Safe circle: center (225,225), radius 210; total margin is chord minus required width, and per-side margin is half of total.",
        "454 outputs are nearest-neighbour design approximations; emulator/physical watch remain authoritative.",
        "",
    ]
    variants = report["variants"]
    for variant_name in VARIANTS:
        variant = variants[variant_name]
        lines.append(f"{variant['label']} ({variant_name})")
        lines.append(f"  {variant['description']}")
        lines.append(
            f"  icons={variant['icon_set']} bands={variant['bands']} gaps={variant['gaps']} "
            f"time-center-offset={variant['time_center_offset_from_active_center']}"
        )
        for region in ("weather", "date", "time", "steps", "battery"):
            row = variant["rows"][region]
            widths = ", ".join(f"{key}={value}" for key, value in row["state_widths"].items())
            lines.append(
                f"  {region:7s} y={row['y_band'][0]}..{row['y_band'][1]} "
                f"edge-y={row['safe_edge_y']} width={row['required_width']} ({widths}) "
                f"chord={row['safe_chord_at_farthest_edge']:.3f} "
                f"margin-total={row['safe_margin_total']:.3f} "
                f"margin-per-side={row['safe_margin_per_side']:.3f} valid={row['valid']}"
            )
        lines.append(f"  all safe margins nonnegative: {variant['all_safe_margins_nonnegative']}")
        lines.append("")
    all8_margin = variants["all8"]["rows"]["weather"]["safe_margin_total"]
    mixed12_margin = variants["mixed12"]["rows"]["weather"]["safe_margin_total"]
    lines.extend(
        [
            "Tradeoffs:",
            f"  A keeps the original row stack and has a {all8_margin:.3f}-unit weather margin at the worst edge.",
            f"  B gives weather a real 60-unit feature bay, leaving a {mixed12_margin:.3f}-unit weather margin and moving time down 20 units.",
            "  Both retain 20-unit gaps, truthfully show unavailable weather, and fit the conservative safe circle.",
            "  Candidate alternatives remain unresolved; the study does not select a product icon family.",
        ]
    )
    return "\n".join(lines) + "\n"


def _validate_rendered_pixels(pixels: PixelGrid, *, variant_name: str) -> None:
    allowed_weather = set(WEATHER_COLORS.values())
    for row in pixels:
        for pixel in row:
            if pixel not in {BLACK, WHITE, *allowed_weather}:
                raise ValueError(f"{variant_name}: unexpected rendered palette value {pixel!r}")


def expected_output_bytes() -> dict[str, bytes]:
    """Recompute every deterministic study artifact without touching disk."""

    expected: dict[str, bytes] = {}
    for variant_name in VARIANTS:
        for state_name in STATES:
            for target_size in TARGETS:
                native = render_variant_state(variant_name, state_name)
                _validate_rendered_pixels(native, variant_name=variant_name)
                rendered = native if target_size == CANVAS else resize_nearest(native, target_size)
                name = f"raster90-icon-study-{variant_name}-{state_name}-{target_size}.png"
                expected[name] = encode_png(rendered)

    sheets = {
        "raster90-icon-study-comparison-466.png": build_comparison_sheet(466),
        "raster90-icon-study-comparison-454.png": build_comparison_sheet(454),
        "raster90-icon-study-icon-sheet.png": build_icon_sheet(),
        "raster90-icon-study-actual-size-icons.png": build_actual_size_icon_sheet(),
        "raster90-icon-focus-actual-size.png": build_focus_icon_sheet(actual_size=True),
        "raster90-icon-focus-enlarged.png": build_focus_icon_sheet(actual_size=False),
        "raster90-icon-focus-row-context.png": build_focus_row_context_sheet(),
    }
    for name, pixels in sheets.items():
        expected[name] = encode_png(pixels)

    report = build_geometry_report()
    expected["raster90-icon-study-geometry.json"] = (
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    ).encode()
    expected["raster90-icon-study-geometry.txt"] = geometry_text(report).encode()
    expected["raster90-icon-focus-metrics.txt"] = focus_metrics_text().encode()
    return expected


def generate_outputs(root: Path) -> int:
    output_dir = root / OUTPUT_DIR_REL
    output_dir.mkdir(parents=True, exist_ok=True)
    expected = expected_output_bytes()
    changed = 0
    for name, data in expected.items():
        path = output_dir / name
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
            changed += 1
    check_outputs(root)
    return changed


def check_outputs(root: Path) -> None:
    validate_study_matrices()
    report = build_geometry_report()
    for variant_name in VARIANTS:
        variant = report["variants"][variant_name]
        if not variant["all_safe_margins_nonnegative"]:
            raise ValueError(f"{variant_name}: geometry leaves the safe circle")
        if variant["gaps"] != [20, 20, 20, 20]:
            raise ValueError(f"{variant_name}: row gaps drifted from 20 units")
        for region in ("weather", "date", "time", "steps", "battery"):
            if not variant["rows"][region]["valid"]:
                raise ValueError(f"{variant_name}/{region}: invalid safe margin")

    output_dir = root / OUTPUT_DIR_REL
    expected = expected_output_bytes()
    for name, expected_data in expected.items():
        path = output_dir / name
        if not path.exists():
            raise ValueError(f"missing study output: {path}")
        actual_data = path.read_bytes()
        if actual_data != expected_data:
            raise ValueError(f"stale or corrupt study output: {path}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check existing ignored outputs without rewriting")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (defaults to this checkout)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.check:
            check_outputs(root)
            print("Raster 90 icon study outputs OK")
        else:
            changed = generate_outputs(root)
            print(f"Raster 90 icon study outputs generated ({changed} changed)")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"Raster 90 icon study failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
