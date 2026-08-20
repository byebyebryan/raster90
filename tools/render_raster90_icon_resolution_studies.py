#!/usr/bin/env python3
"""Render comparable true-8x8 and true-16x16 Raster 90 icon sheets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "design" / "raster90"))
sys.path.insert(0, str(ROOT / "tools"))

from icon_resolution_studies import (  # noqa: E402
    EIGHT_UTILITY_ICONS,
    EIGHT_WEATHER_DAY,
    EIGHT_WEATHER_NIGHT,
    SIXTEEN_UTILITY_ICONS,
    SIXTEEN_WEATHER_DAY,
    SIXTEEN_WEATHER_NIGHT,
    STALE_MARKER,
    WEATHER_CONDITIONS,
    validate_icon_resolution_studies,
)
from matrices import (  # noqa: E402
    FINE_GLYPHS,
    PALETTE,
    SINGLE_GRID_TIME_COLON_CELLS,
    SINGLE_GRID_TIME_DIGIT_CELLS,
    TIME_COLON,
    TIME_DIGITS,
)
from render_raster90_single_grid_study import (  # noqa: E402
    BLACK,
    WHITE,
    PixelGrid,
    _blank,
    _draw_matrix,
    _draw_text,
    _text_width,
    encode_png,
)
from single_grid_study import ROW_BANDS as FACE_ROW_BANDS  # noqa: E402


OUTPUT_DIR_REL = Path("outputs/raster90/studies/icon-resolution")
SHEET_WIDTH = 1248
SHEET_HEIGHT = 950
REVIEW_ICON_SIZE = 96
FACE_CANVAS = 466
FACE_ACTIVE_ORIGIN = (8, 8)
FACE_ACTIVE_SIZE = 450
FACE_BASE_SOURCE_SIZE = 150
FACE_ICON_CELLS = 16
FACE_TEXT_LINE_CELLS = 8
FACE_ICON_TEXT_GAP_CELLS = 2
SINGLE_ROW_TEXT = {
    "weather": "WX 21°C",
    "date": "SAT 15 AUG",
    "steps": "STP 03642",
    "battery": "BAT 82%",
}
ICON_LED_TEXT = {
    # Selected available-state copy: icons replace redundant field headers.
    "weather": "21°C",
    "date": "SAT 15 AUG",
    "steps": "03642",
    "battery": "82%",
}
TWO_LINE_STUDY_TEXT = {
    "weather": ("WX", "21°C"),
    "date": ("SAT", "15 AUG"),
    "steps": ("STP", "03642"),
    "battery": ("BAT", "82%"),
}


def _weather_color(symbol: str):
    try:
        return PALETTE[symbol]
    except KeyError as error:
        raise ValueError(f"unknown weather palette symbol {symbol!r}") from error


def _build_sheet(
    *,
    title: str,
    subtitle: str,
    source_size: int,
    pitch: int,
    lit: int,
    utility_icons: Mapping[str, Sequence[str]],
    weather_day: Mapping[int, Sequence[str]],
    weather_night: Mapping[int, Sequence[str]],
) -> PixelGrid:
    pixels = _blank(SHEET_WIDTH, SHEET_HEIGHT)
    _draw_text(pixels, title, x=24, line_y=18)
    _draw_text(pixels, subtitle, x=24, line_y=48)
    _draw_text(pixels, "UTILITY", x=24, line_y=82)

    column_width = 300
    utility_y = 138
    for column, (label, rows) in enumerate(utility_icons.items()):
        card_x = 24 + column * column_width
        _draw_text(pixels, label.upper(), x=card_x, line_y=108)
        _draw_matrix(
            pixels,
            rows,
            x=card_x,
            y=utility_y,
            pitch=pitch,
            lit=lit,
            color_for=lambda _symbol: WHITE,
        )

    stale_x = 24 + 3 * column_width
    _draw_text(pixels, "WX STALE MARK", x=stale_x, line_y=108)
    _draw_matrix(
        pixels,
        weather_day[14],
        x=stale_x,
        y=utility_y,
        pitch=pitch,
        lit=lit,
        color_for=_weather_color,
    )
    stale_offset = (source_size - len(STALE_MARKER)) * pitch
    _draw_matrix(
        pixels,
        STALE_MARKER,
        x=stale_x + stale_offset,
        y=utility_y,
        pitch=pitch,
        lit=lit,
        color_for=lambda _symbol: WHITE,
    )

    _draw_text(pixels, "WFF CONDITIONS  DAY AND NIGHT", x=24, line_y=250)
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
            (weather_day[condition], day_x),
            (weather_night[condition], night_x),
        ):
            _draw_matrix(
                pixels,
                rows,
                x=x,
                y=icon_y,
                pitch=pitch,
                lit=lit,
                color_for=_weather_color,
            )

        day_width = _text_width("DAY")
        night_width = _text_width("NIGHT")
        _draw_text(
            pixels,
            "DAY",
            x=day_x + (REVIEW_ICON_SIZE - day_width) // 2,
            line_y=card_y + 130,
        )
        _draw_text(
            pixels,
            "NIGHT",
            x=night_x + (REVIEW_ICON_SIZE - night_width) // 2,
            line_y=card_y + 130,
        )
    return pixels


def build_true_8x8_sheet() -> PixelGrid:
    """Render 8x8 sources with solid contiguous 12x12 review pixels."""

    return _build_sheet(
        title="DIRECTION A  TRUE 8X8 SOLID PIXELS",
        subtitle="NO GUTTERS  48X48 WATCH BAY  2X REVIEW",
        source_size=8,
        pitch=12,
        lit=12,
        utility_icons=EIGHT_UTILITY_ICONS,
        weather_day=EIGHT_WEATHER_DAY,
        weather_night=EIGHT_WEATHER_NIGHT,
    )


def build_true_16x16_sheet() -> PixelGrid:
    """Render direct 16x16 sources with the 3-pitch/2-lit display cell."""

    return _build_sheet(
        title="DIRECTION B  TRUE 16X16 DOT MATRIX",
        subtitle="3X2 CELLS  48X48 WATCH BAY  2X REVIEW",
        source_size=16,
        pitch=6,
        lit=4,
        utility_icons=SIXTEEN_UTILITY_ICONS,
        weather_day=SIXTEEN_WEATHER_DAY,
        weather_night=SIXTEEN_WEATHER_NIGHT,
    )


def build_true_16x16_solid_sheet() -> PixelGrid:
    """Render the same direct 16x16 sources with solid 3x3 watch cells."""

    return _build_sheet(
        title="DIRECTION C  TRUE 16X16 SOLID PIXELS",
        subtitle="NO GUTTERS  48X48 WATCH BAY  2X REVIEW",
        source_size=16,
        pitch=6,
        lit=6,
        utility_icons=SIXTEEN_UTILITY_ICONS,
        weather_day=SIXTEEN_WEATHER_DAY,
        weather_night=SIXTEEN_WEATHER_NIGHT,
    )


def _solid_text_width_cells(text: str) -> int:
    return sum(2 if character == " " else 6 for character in text)


def _draw_solid_text(
    pixels: PixelGrid,
    text: str,
    *,
    x: int,
    y: int,
    cell_size: int,
) -> None:
    cursor = x
    for character in text:
        try:
            rows = FINE_GLYPHS[character]
        except KeyError as error:
            raise ValueError(f"face mock uses undefined glyph {character!r}") from error
        _draw_matrix(
            pixels,
            rows,
            x=cursor,
            y=y,
            pitch=cell_size,
            lit=cell_size,
            color_for=lambda _symbol: WHITE,
        )
        cursor += (2 if character == " " else 6) * cell_size


def _face_row_bands(source_size: int) -> Mapping[str, tuple[int, int]]:
    offset = (source_size - FACE_BASE_SOURCE_SIZE) // 2
    return {
        name: (start + offset, end + offset)
        for name, (start, end) in FACE_ROW_BANDS.items()
    }


def _draw_solid_information_row(
    pixels: PixelGrid,
    name: str,
    *,
    cell_size: int,
    source_size: int,
    row_bands: Mapping[str, tuple[int, int]],
) -> None:
    first_line, second_line = TWO_LINE_STUDY_TEXT[name]
    icon = (
        SIXTEEN_WEATHER_DAY[14]
        if name == "weather"
        else SIXTEEN_UTILITY_ICONS[name]
    )
    text_width_cells = max(
        _solid_text_width_cells(first_line),
        _solid_text_width_cells(second_line),
    )
    total_width_cells = (
        FACE_ICON_CELLS + FACE_ICON_TEXT_GAP_CELLS + text_width_cells
    )
    x = FACE_ACTIVE_ORIGIN[0] + (source_size - total_width_cells) // 2 * cell_size
    y = FACE_ACTIVE_ORIGIN[1] + row_bands[name][0] * cell_size
    _draw_matrix(
        pixels,
        icon,
        x=x,
        y=y,
        pitch=cell_size,
        lit=cell_size,
        color_for=_weather_color if name == "weather" else (lambda _symbol: WHITE),
    )
    text_x = x + (FACE_ICON_CELLS + FACE_ICON_TEXT_GAP_CELLS) * cell_size
    _draw_solid_text(
        pixels,
        first_line,
        x=text_x,
        y=y,
        cell_size=cell_size,
    )
    _draw_solid_text(
        pixels,
        second_line,
        x=text_x,
        y=y + FACE_TEXT_LINE_CELLS * cell_size,
        cell_size=cell_size,
    )


def solid_single_row_width_cells(
    name: str,
    row_text: Mapping[str, str] = SINGLE_ROW_TEXT,
) -> int:
    return (
        FACE_ICON_CELLS
        + FACE_ICON_TEXT_GAP_CELLS
        + _solid_text_width_cells(row_text[name])
    )


def _draw_solid_single_information_row(
    pixels: PixelGrid,
    name: str,
    *,
    cell_size: int,
    source_size: int,
    row_bands: Mapping[str, tuple[int, int]],
    row_text: Mapping[str, str],
) -> None:
    icon = (
        SIXTEEN_WEATHER_DAY[14]
        if name == "weather"
        else SIXTEEN_UTILITY_ICONS[name]
    )
    total_width_cells = solid_single_row_width_cells(name, row_text)
    x = FACE_ACTIVE_ORIGIN[0] + (source_size - total_width_cells) // 2 * cell_size
    y = FACE_ACTIVE_ORIGIN[1] + row_bands[name][0] * cell_size
    _draw_matrix(
        pixels,
        icon,
        x=x,
        y=y,
        pitch=cell_size,
        lit=cell_size,
        color_for=_weather_color if name == "weather" else (lambda _symbol: WHITE),
    )
    text_x = x + (FACE_ICON_CELLS + FACE_ICON_TEXT_GAP_CELLS) * cell_size
    # A 7-cell glyph line has nine spare cells inside the 16-cell icon row.
    # Four cells above and five below keep every edge on the base grid.
    text_y = y + 4 * cell_size
    _draw_solid_text(
        pixels,
        row_text[name],
        x=text_x,
        y=text_y,
        cell_size=cell_size,
    )


def _draw_solid_time(
    pixels: PixelGrid,
    *,
    cell_size: int,
    source_size: int,
    row_bands: Mapping[str, tuple[int, int]],
    value: str = "10:08",
) -> None:
    width_cells = sum(
        SINGLE_GRID_TIME_COLON_CELLS
        if character == ":"
        else SINGLE_GRID_TIME_DIGIT_CELLS
        for character in value
    )
    x = FACE_ACTIVE_ORIGIN[0] + (source_size - width_cells) // 2 * cell_size
    y = FACE_ACTIVE_ORIGIN[1] + row_bands["time"][0] * cell_size
    cursor = x
    for character in value:
        rows = TIME_COLON if character == ":" else TIME_DIGITS[character]
        _draw_matrix(
            pixels,
            rows,
            x=cursor,
            y=y,
            pitch=cell_size,
            lit=cell_size,
            color_for=lambda _symbol: WHITE,
        )
        cursor += len(rows[0]) * cell_size


def build_solid_grid_face_mock(cell_size: int) -> PixelGrid:
    """Render one honest solid-cell face without changing matrix resolution."""

    if cell_size not in (2, 3):
        raise ValueError("solid face mock cell size must be 2 or 3")
    if FACE_ACTIVE_SIZE % cell_size:
        raise ValueError("solid face mock must divide the active frame exactly")
    source_size = FACE_ACTIVE_SIZE // cell_size
    row_bands = _face_row_bands(source_size)
    pixels = _blank(FACE_CANVAS, FACE_CANVAS)
    _draw_solid_information_row(
        pixels,
        "weather",
        cell_size=cell_size,
        source_size=source_size,
        row_bands=row_bands,
    )
    _draw_solid_information_row(
        pixels,
        "date",
        cell_size=cell_size,
        source_size=source_size,
        row_bands=row_bands,
    )
    _draw_solid_time(
        pixels,
        cell_size=cell_size,
        source_size=source_size,
        row_bands=row_bands,
    )
    _draw_solid_information_row(
        pixels,
        "steps",
        cell_size=cell_size,
        source_size=source_size,
        row_bands=row_bands,
    )
    _draw_solid_information_row(
        pixels,
        "battery",
        cell_size=cell_size,
        source_size=source_size,
        row_bands=row_bands,
    )
    return pixels


def build_solid_grid_single_row_face_mock(
    cell_size: int = 3,
    *,
    row_text: Mapping[str, str] = SINGLE_ROW_TEXT,
) -> PixelGrid:
    """Render a solid-cell face with one joined text line per 16-cell icon."""

    if cell_size not in (2, 3):
        raise ValueError("solid face mock cell size must be 2 or 3")
    if FACE_ACTIVE_SIZE % cell_size:
        raise ValueError("solid face mock must divide the active frame exactly")
    source_size = FACE_ACTIVE_SIZE // cell_size
    row_bands = _face_row_bands(source_size)
    pixels = _blank(FACE_CANVAS, FACE_CANVAS)
    for name in ("weather", "date"):
        _draw_solid_single_information_row(
            pixels,
            name,
            cell_size=cell_size,
            source_size=source_size,
            row_bands=row_bands,
            row_text=row_text,
        )
    _draw_solid_time(
        pixels,
        cell_size=cell_size,
        source_size=source_size,
        row_bands=row_bands,
    )
    for name in ("steps", "battery"):
        _draw_solid_single_information_row(
            pixels,
            name,
            cell_size=cell_size,
            source_size=source_size,
            row_bands=row_bands,
            row_text=row_text,
        )
    return pixels


def build_solid_grid_icon_led_face_mock(cell_size: int = 3) -> PixelGrid:
    """Render one line per icon without redundant WX, STP, or BAT headers."""

    return build_solid_grid_single_row_face_mock(
        cell_size,
        row_text=ICON_LED_TEXT,
    )


def centered_date_width_cells() -> int:
    return _solid_text_width_cells(ICON_LED_TEXT["date"])


def build_solid_grid_no_calendar_face_mock(cell_size: int = 3) -> PixelGrid:
    """Render the icon-led face with centered date text and no calendar icon."""

    if cell_size not in (2, 3):
        raise ValueError("solid face mock cell size must be 2 or 3")
    if FACE_ACTIVE_SIZE % cell_size:
        raise ValueError("solid face mock must divide the active frame exactly")
    source_size = FACE_ACTIVE_SIZE // cell_size
    row_bands = _face_row_bands(source_size)
    pixels = _blank(FACE_CANVAS, FACE_CANVAS)
    _draw_solid_single_information_row(
        pixels,
        "weather",
        cell_size=cell_size,
        source_size=source_size,
        row_bands=row_bands,
        row_text=ICON_LED_TEXT,
    )

    date_width_cells = centered_date_width_cells()
    date_x = (
        FACE_ACTIVE_ORIGIN[0]
        + (source_size - date_width_cells) // 2 * cell_size
    )
    date_y = (
        FACE_ACTIVE_ORIGIN[1]
        + (row_bands["date"][0] + 4) * cell_size
    )
    _draw_solid_text(
        pixels,
        ICON_LED_TEXT["date"],
        x=date_x,
        y=date_y,
        cell_size=cell_size,
    )

    _draw_solid_time(
        pixels,
        cell_size=cell_size,
        source_size=source_size,
        row_bands=row_bands,
    )
    for name in ("steps", "battery"):
        _draw_solid_single_information_row(
            pixels,
            name,
            cell_size=cell_size,
            source_size=source_size,
            row_bands=row_bands,
            row_text=ICON_LED_TEXT,
        )
    return pixels


def build_solid_grid_face_comparison() -> PixelGrid:
    label_height = 54
    gap = 24
    pixels = _blank(FACE_CANVAS * 2 + gap, FACE_CANVAS + label_height)
    _draw_text(pixels, "2X2 SOLID  225X225 GRID", x=24, line_y=18)
    _draw_text(
        pixels,
        "3X3 SOLID  150X150 GRID",
        x=FACE_CANVAS + gap + 24,
        line_y=18,
    )
    for source, x in (
        (build_solid_grid_face_mock(2), 0),
        (build_solid_grid_face_mock(3), FACE_CANVAS + gap),
    ):
        for source_y, row in enumerate(source):
            for source_x, pixel in enumerate(row):
                pixels[label_height + source_y][x + source_x] = pixel
    return pixels


def build_solid_grid_row_layout_comparison() -> PixelGrid:
    label_height = 54
    gap = 24
    pixels = _blank(FACE_CANVAS * 2 + gap, FACE_CANVAS + label_height)
    _draw_text(pixels, "3X3 SOLID  DOUBLE ROW", x=24, line_y=18)
    _draw_text(
        pixels,
        "3X3 SOLID  SINGLE ROW",
        x=FACE_CANVAS + gap + 24,
        line_y=18,
    )
    for source, x in (
        (build_solid_grid_face_mock(3), 0),
        (build_solid_grid_single_row_face_mock(3), FACE_CANVAS + gap),
    ):
        for source_y, row in enumerate(source):
            for source_x, pixel in enumerate(row):
                pixels[label_height + source_y][x + source_x] = pixel
    return pixels


def build_solid_grid_header_comparison() -> PixelGrid:
    label_height = 54
    gap = 24
    pixels = _blank(FACE_CANVAS * 2 + gap, FACE_CANVAS + label_height)
    _draw_text(pixels, "SINGLE ROW  HEADERS", x=24, line_y=18)
    _draw_text(
        pixels,
        "SINGLE ROW  ICON LED",
        x=FACE_CANVAS + gap + 24,
        line_y=18,
    )
    for source, x in (
        (build_solid_grid_single_row_face_mock(3), 0),
        (build_solid_grid_icon_led_face_mock(3), FACE_CANVAS + gap),
    ):
        for source_y, row in enumerate(source):
            for source_x, pixel in enumerate(row):
                pixels[label_height + source_y][x + source_x] = pixel
    return pixels


def build_solid_grid_calendar_comparison() -> PixelGrid:
    label_height = 54
    gap = 24
    pixels = _blank(FACE_CANVAS * 2 + gap, FACE_CANVAS + label_height)
    _draw_text(pixels, "WITH CALENDAR", x=24, line_y=18)
    _draw_text(
        pixels,
        "DATE TEXT ONLY",
        x=FACE_CANVAS + gap + 24,
        line_y=18,
    )
    for source, x in (
        (build_solid_grid_icon_led_face_mock(3), 0),
        (build_solid_grid_no_calendar_face_mock(3), FACE_CANVAS + gap),
    ):
        for source_y, row in enumerate(source):
            for source_x, pixel in enumerate(row):
                pixels[label_height + source_y][x + source_x] = pixel
    return pixels


def expected_output_bytes() -> dict[str, bytes]:
    validate_icon_resolution_studies()
    sheets = {
        "raster90-true-8x8-solid-icon-sheet.png": build_true_8x8_sheet(),
        "raster90-true-16x16-dot-matrix-icon-sheet.png": build_true_16x16_sheet(),
        "raster90-true-16x16-solid-icon-sheet.png": build_true_16x16_solid_sheet(),
        "raster90-solid-grid-2x2-face-466.png": build_solid_grid_face_mock(2),
        "raster90-solid-grid-3x3-face-466.png": build_solid_grid_face_mock(3),
        "raster90-solid-grid-face-comparison.png": build_solid_grid_face_comparison(),
        "raster90-solid-grid-3x3-single-row-face-466.png": (
            build_solid_grid_single_row_face_mock(3)
        ),
        "raster90-solid-grid-3x3-row-layout-comparison.png": (
            build_solid_grid_row_layout_comparison()
        ),
        "raster90-solid-grid-3x3-icon-led-face-466.png": (
            build_solid_grid_icon_led_face_mock(3)
        ),
        "raster90-solid-grid-3x3-header-comparison.png": (
            build_solid_grid_header_comparison()
        ),
        "raster90-solid-grid-3x3-no-calendar-face-466.png": (
            build_solid_grid_no_calendar_face_mock(3)
        ),
        "raster90-solid-grid-3x3-calendar-comparison.png": (
            build_solid_grid_calendar_comparison()
        ),
    }
    allowed = {BLACK, WHITE, *PALETTE.values()}
    for name, pixels in sheets.items():
        if any(pixel not in allowed for row in pixels for pixel in row):
            raise ValueError(f"{name}: unexpected palette value")
    return {name: encode_png(pixels) for name, pixels in sheets.items()}


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
    output_dir = root / OUTPUT_DIR_REL
    for name, expected in expected_output_bytes().items():
        path = output_dir / name
        if not path.exists():
            raise ValueError(f"missing icon-resolution output: {path}")
        if path.read_bytes() != expected:
            raise ValueError(f"stale or corrupt icon-resolution output: {path}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.check:
            check_outputs(root)
            print("Raster 90 icon-resolution study outputs OK")
        else:
            changed = generate_outputs(root)
            print(f"Raster 90 icon-resolution study outputs generated ({changed} changed)")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Raster 90 icon-resolution study failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
