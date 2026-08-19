"""Reviewable source matrices for the Raster 90 3/2 single-grid study.

This is design-study input, not the packaged watch-face asset source.  The
study treats the 450-unit active frame as one 150x150 source framebuffer.  A
source pixel has a 3-unit pitch, a 2x2 lit square, and a one-unit gutter.

The existing icon candidates are normalized only to test the proposed pixel
size and common 16x16 registration.  They are placeholders, not selected
production art.  Likewise, the time expands the proven V1 silhouettes onto the
finer source grid so pitch can be judged before new high-resolution numerals
are authored.
"""

from __future__ import annotations

from typing import Final, Mapping, Sequence

from icon_studies import (
    FOCUS_BATTERY_ICONS,
    FOCUS_CALENDAR_ICONS,
    FOCUS_STEP_12,
    FOCUS_WEATHER_12,
)
from matrices import COARSE_COLON, COARSE_DIGITS, FINE_GLYPHS, PALETTE


Matrix = tuple[str, ...]

CANVAS: Final = 466
ACTIVE_ORIGIN: Final = (8, 8)
ACTIVE_SIZE: Final = 450
SOURCE_SIZE: Final = 150
PIXEL_PITCH: Final = 3
PIXEL_LIT: Final = 2
SAFE_CENTER: Final = (225, 225)
SAFE_RADIUS: Final = 210

TEXT_LINE_CELLS: Final = 8
ICON_CELLS: Final = 16
TIME_LINE_CELLS: Final = 32
ROW_GAP_CELLS: Final = 6
EDGE_MARGIN_CELLS: Final = 15
ICON_TEXT_GAP_CELLS: Final = 2

# Source-frame bands.  Their sequence is 15 + 16 + 6 + 16 + 6 + 32 + 6 +
# 16 + 6 + 16 + 15 = 150 cells.
ROW_BANDS: Final[Mapping[str, tuple[int, int]]] = {
    "weather": (15, 31),
    "date": (37, 53),
    "time": (59, 91),
    "steps": (97, 113),
    "battery": (119, 135),
}

STUDY_TEXT: Final[Mapping[str, tuple[str, str]]] = {
    "weather": ("WX", "21°C"),
    "date": ("SAT", "15 AUG"),
    "steps": ("STP", "03642"),
    "battery": ("BAT", "82%"),
}

WEATHER_PALETTE = PALETTE


def _live_bounds(rows: Sequence[str]) -> tuple[int, int, int, int]:
    points = [
        (x, y)
        for y, row in enumerate(rows)
        for x, symbol in enumerate(row)
        if symbol not in ("0", ".")
    ]
    if not points:
        raise ValueError("cannot normalize an empty icon")
    return (
        min(x for x, _y in points),
        min(y for _x, y in points),
        max(x for x, _y in points),
        max(y for _x, y in points),
    )


def _normalize_icon(
    rows: Sequence[str],
    *,
    empty: str,
    canvas: int = ICON_CELLS,
    live_extent: int = 14,
) -> Matrix:
    """Crop and nearest-resample an icon into a common review canvas."""

    min_x, min_y, max_x, max_y = _live_bounds(rows)
    cropped = tuple(row[min_x : max_x + 1] for row in rows[min_y : max_y + 1])
    source_height = len(cropped)
    source_width = len(cropped[0])
    scale = live_extent / max(source_width, source_height)
    target_width = max(1, round(source_width * scale))
    target_height = max(1, round(source_height * scale))
    resized = tuple(
        "".join(
            cropped[min(source_height - 1, int(y * source_height / target_height))][
                min(source_width - 1, int(x * source_width / target_width))
            ]
            for x in range(target_width)
        )
        for y in range(target_height)
    )
    left = (canvas - target_width) // 2
    top = (canvas - target_height) // 2
    output = [[empty for _x in range(canvas)] for _y in range(canvas)]
    for y, row in enumerate(resized):
        for x, symbol in enumerate(row):
            output[top + y][left + x] = empty if symbol in ("0", ".") else symbol
    return tuple("".join(row) for row in output)


ICONS: Final[Mapping[str, Matrix]] = {
    "weather": _normalize_icon(
        FOCUS_WEATHER_12["outline"]["partly_cloudy"], empty="."
    ),
    "date": _normalize_icon(FOCUS_CALENDAR_ICONS["tearoff"], empty="0"),
    "steps": _normalize_icon(FOCUS_STEP_12["walker_a"], empty="0"),
    "battery": _normalize_icon(FOCUS_BATTERY_ICONS["high"], empty="0"),
}


def _expand_time_glyph(
    rows: Sequence[str], *, box_width: int, box_height: int = TIME_LINE_CELLS
) -> Matrix:
    """Expand a V1 silhouette onto fine pixels for pitch-only calibration."""

    factor = 3
    expanded_rows: list[str] = []
    for row in rows:
        expanded = "".join(symbol * factor for symbol in row)
        expanded_rows.extend(expanded for _copy in range(factor))
    content_width = len(expanded_rows[0])
    content_height = len(expanded_rows)
    left = (box_width - content_width) // 2
    top = (box_height - content_height) // 2
    output = [["0" for _x in range(box_width)] for _y in range(box_height)]
    for y, row in enumerate(expanded_rows):
        for x, symbol in enumerate(row):
            output[top + y][left + x] = symbol
    return tuple("".join(row) for row in output)


TIME_DIGIT_CELLS: Final = 26
TIME_COLON_CELLS: Final = 10
TIME_DIGITS: Final[Mapping[str, Matrix]] = {
    digit: _expand_time_glyph(rows, box_width=TIME_DIGIT_CELLS)
    for digit, rows in COARSE_DIGITS.items()
}
TIME_COLON: Final[Matrix] = _expand_time_glyph(
    COARSE_COLON, box_width=TIME_COLON_CELLS
)


def validate_single_grid_study() -> None:
    if ACTIVE_SIZE != SOURCE_SIZE * PIXEL_PITCH:
        raise ValueError("active frame is not an exact 150-cell source grid")
    if PIXEL_LIT >= PIXEL_PITCH:
        raise ValueError("source pixels need a visible gutter")

    ordered = ("weather", "date", "time", "steps", "battery")
    if ROW_BANDS[ordered[0]][0] != EDGE_MARGIN_CELLS:
        raise ValueError("top source-grid margin drifted")
    for previous, current in zip(ordered, ordered[1:]):
        gap = ROW_BANDS[current][0] - ROW_BANDS[previous][1]
        if gap != ROW_GAP_CELLS:
            raise ValueError(f"gap before {current} is {gap}, expected {ROW_GAP_CELLS}")
    if SOURCE_SIZE - ROW_BANDS[ordered[-1]][1] != EDGE_MARGIN_CELLS:
        raise ValueError("bottom source-grid margin drifted")

    expected_heights = {
        "weather": ICON_CELLS,
        "date": ICON_CELLS,
        "time": TIME_LINE_CELLS,
        "steps": ICON_CELLS,
        "battery": ICON_CELLS,
    }
    for name, expected_height in expected_heights.items():
        start, end = ROW_BANDS[name]
        if end - start != expected_height:
            raise ValueError(f"{name}: expected a {expected_height}-cell row")

    for name, rows in ICONS.items():
        if len(rows) != ICON_CELLS or any(len(row) != ICON_CELLS for row in rows):
            raise ValueError(f"{name}: expected a 16x16 icon canvas")
        vocabulary = {".", "Y", "C", "B", "W"} if name == "weather" else {"0", "1"}
        if set("".join(rows)) - vocabulary:
            raise ValueError(f"{name}: unknown icon cell")

    for digit, rows in TIME_DIGITS.items():
        if len(rows) != TIME_LINE_CELLS or any(
            len(row) != TIME_DIGIT_CELLS for row in rows
        ):
            raise ValueError(f"time/{digit}: invalid digit box")
    if len(TIME_COLON) != TIME_LINE_CELLS or any(
        len(row) != TIME_COLON_CELLS for row in TIME_COLON
    ):
        raise ValueError("time colon has an invalid box")

    degree = FINE_GLYPHS["°"]
    if degree[0] != "01110" or degree[3] != "01110":
        raise ValueError("degree glyph must be a closed ring")


validate_single_grid_study()
