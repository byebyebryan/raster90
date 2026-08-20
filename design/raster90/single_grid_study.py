"""Reviewable source matrices for the Raster 90 solid single-grid runtime.

This is the reviewable source for the 450-unit active frame treated as one
150x150 source framebuffer. A source pixel has a 3-unit pitch and a solid 3x3
lit square. The selected true16 utility and weather tiles, plus the reviewed
clean-chamfer primary time boxes, are shared with the packaged resource
generator. The square construction and legacy fine-chamfer controls remain
canonical source variants for comparison.

The utility and weather matrices are authored directly at true 16x16. The
primary time cut uses the canonical reviewed clean-chamfer matrices on the
same source grid; the square construction and legacy global fine-chamfer remain
available as named comparison controls.
"""

from __future__ import annotations

from typing import Final, Mapping

from icon_resolution_studies import (
    SIXTEEN_UTILITY_ICONS,
    SIXTEEN_WEATHER_DAY,
    SIXTEEN_WEATHER_NIGHT,
)
from matrices import (
    FINE_GLYPHS,
    PALETTE,
    SINGLE_GRID_TIME_COLON_CELLS,
    SINGLE_GRID_TIME_DIGIT_CELLS,
    SINGLE_GRID_TIME_LINE_CELLS,
    SINGLE_GRID_LIT,
    TIME_COLON,
    TIME_DIGITS,
)
from fonts.raster90.family import validate_font_family


Matrix = tuple[str, ...]

CANVAS: Final = 466
ACTIVE_ORIGIN: Final = (8, 8)
ACTIVE_SIZE: Final = 450
SOURCE_SIZE: Final = 150
PIXEL_PITCH: Final = 3
PIXEL_LIT: Final = SINGLE_GRID_LIT
SAFE_CENTER: Final = (225, 225)
SAFE_RADIUS: Final = 210

TEXT_LINE_CELLS: Final = 8
ICON_CELLS: Final = 16
TIME_LINE_CELLS: Final = SINGLE_GRID_TIME_LINE_CELLS
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

STUDY_TEXT: Final[Mapping[str, str]] = {
    "weather": "21°C",
    "date": "SAT 15 AUG",
    "steps": "03642",
    "battery": "82%",
}

WEATHER_PALETTE = PALETTE


ICONS: Final[Mapping[str, Matrix]] = {
    # Condition 14 is the documented representative partly-cloudy day state;
    # its direct-authored tile is also used by the packaged preview.
    "weather": SIXTEEN_WEATHER_DAY[14],
    "steps": SIXTEEN_UTILITY_ICONS["steps"],
    "battery": SIXTEEN_UTILITY_ICONS["battery"],
}

SINGLE_GRID_WEATHER_DAY = SIXTEEN_WEATHER_DAY
SINGLE_GRID_WEATHER_NIGHT = SIXTEEN_WEATHER_NIGHT


TIME_DIGIT_CELLS: Final = SINGLE_GRID_TIME_DIGIT_CELLS
TIME_COLON_CELLS: Final = SINGLE_GRID_TIME_COLON_CELLS


def validate_single_grid_study() -> None:
    validate_font_family()
    if ACTIVE_SIZE != SOURCE_SIZE * PIXEL_PITCH:
        raise ValueError("active frame is not an exact 150-cell source grid")
    if PIXEL_LIT != PIXEL_PITCH:
        raise ValueError("selected solid source pixels must fill their pitch")

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

    if set(ICONS) != {"weather", "steps", "battery"}:
        raise ValueError("selected runtime icon set must omit the calendar icon")
    for name, rows in ICONS.items():
        if len(rows) != ICON_CELLS or any(len(row) != ICON_CELLS for row in rows):
            raise ValueError(f"{name}: expected a 16x16 icon canvas")
        vocabulary = {".", "Y", "C", "B", "W"} if name == "weather" else {".", "0", "1"}
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
