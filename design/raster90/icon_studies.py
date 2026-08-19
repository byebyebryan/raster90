"""Project-owned Raster 90 icon-study matrices and layout definitions.

This module is deliberately separate from :mod:`matrices`.  It is a design
study, not a production asset source: the renderer below imports these
matrices to make comparable review sheets, while the WFF resource generator
continues to use the established V1 matrices unchanged.

Every icon uses the existing fine lattice (5-unit pitch, 4-unit lit square).
The two weather families use the existing four-entry flat palette; utility
icons are binary white-on-black in the rendered studies.
"""

from __future__ import annotations

from typing import Final, Mapping


Matrix = tuple[str, ...]

CANVAS: Final = 466
ACTIVE_ORIGIN: Final = (8, 8)
ACTIVE_SIZE: Final = 450
FINE_PITCH: Final = 5
FINE_LIT: Final = 4
COARSE_PITCH: Final = 10
COARSE_LIT: Final = 8
SAFE_CENTER: Final = (225, 225)
SAFE_RADIUS: Final = 210


# Utility icon alternatives.  These are intentionally sparse silhouettes,
# rather than downsampled or traced images from an external icon set.
CALENDAR_ICONS: Final[Mapping[str, Matrix]] = {
    # A page silhouette with two raised binding marks, a solid header band,
    # and three body rows.  This is the strongest calendar candidate at the
    # actual 40-unit utility size.
    "page": (
        "01001000",
        "01111110",
        "01111110",
        "01000010",
        "01011010",
        "01000010",
        "01100110",
        "01111110",
    ),
    "outline": (
        "00111100",
        "01111110",
        "01000010",
        "01111110",
        "01010010",
        "01000110",
        "01111110",
        "00000000",
    ),
    "grid": (
        "01011010",
        "01111110",
        "01000010",
        "01111110",
        "01010110",
        "01111110",
        "01010110",
        "01111110",
    ),
}

STEP_ICONS: Final[Mapping[str, Matrix]] = {
    # A denser walking silhouette keeps a head, shoulders, torso, hips, and
    # two diagonally separated legs connected at native size.
    "walking_person": (
        "00110000",
        "01111000",
        "00110000",
        "01111000",
        "00111000",
        "01100000",
        "11000110",
        "10000110",
    ),
    "walking_person_dense": (
        "00110000",
        "01111000",
        "10110000",
        "00110000",
        "01111000",
        "00111000",
        "01100000",
        "11001000",
    ),
    "walking_person_sparse": (
        "00110000",
        "00110000",
        "01111000",
        "00110000",
        "01111000",
        "00001100",
        "00011000",
        "00110000",
    ),
    "walking_person_alt": (
        "00110000",
        "00110000",
        "01111000",
        "00110000",
        "01110000",
        "01001000",
        "11000110",
        "10000001",
    ),
    "shoe": (
        "00000000",
        "00000000",
        "00000000",
        "00111000",
        "00111100",
        "01111110",
        "11111110",
        "11111111",
    ),
    "shoe_tread": (
        "00000000",
        "00000000",
        "00011000",
        "00111100",
        "01111110",
        "01111110",
        "11111111",
        "10101010",
    ),
}


BATTERY_STYLES: Final[Mapping[str, Mapping[str, Matrix]]] = {}


def _frame_battery(level: int, charging: bool = False) -> Matrix:
    """Return a vertical battery with a bottom-up four-cell fill."""

    rows = [
        list("00110000"),
        list("01111110"),
        list("01000010"),
        list("01000010"),
        list("01000010"),
        list("01000010"),
        list("01111110"),
        list("00000000"),
    ]
    if charging:
        # A small angular bolt remains legible in the unfilled interior.
        for y, x in ((2, 4), (3, 3), (3, 4), (4, 2), (4, 3), (5, 2)):
            rows[y][x] = "1"
    else:
        for y in range(5, 1, -1):
            if y >= 6 - level:
                for x in range(2, 6):
                    rows[y][x] = "1"
    return tuple("".join(row) for row in rows)


def _bar_battery(level: int, charging: bool = False) -> Matrix:
    """Return a rectangular horizontal battery with a right-side terminal."""

    rows = [
        list("01111110"),
        list("01000010"),
        list("01000010"),
        list("01000011"),
        list("01000011"),
        list("01000010"),
        list("01111110"),
        list("00000000"),
    ]
    if charging:
        for y, x in ((1, 4), (2, 3), (2, 4), (3, 2), (3, 3), (4, 2)):
            rows[y][x] = "1"
    else:
        for x in range(2, 6):
            if x < 2 + level:
                for y in range(1, 6):
                    rows[y][x] = "1"
    return tuple("".join(row) for row in rows)


_BATTERY_LEVELS = ("empty", "low", "mid", "high", "full")
BATTERY_STYLES.update(
    {
        "frame": {
            **{name: _frame_battery(index) for index, name in enumerate(_BATTERY_LEVELS)},
            "charging": _frame_battery(0, charging=True),
        },
        "bar": {
            **{name: _bar_battery(index) for index, name in enumerate(_BATTERY_LEVELS)},
            "charging": _bar_battery(0, charging=True),
        },
    }
)


# Weather study sprites are authored at both permitted canvas sizes.  The
# symbols Y/C/B/W map to the existing yellow/cyan/blue/white weather palette;
# dots are transparent.  ``unavailable`` is a neutral framed question mark,
# not a guessed condition.
WEATHER_8: Final[Mapping[str, Matrix]] = {
    "clear_day": (
        "..Y.....",
        "Y.Y.Y...",
        ".Y...Y..",
        "...Y....",
        ".Y...Y..",
        "Y.Y.Y...",
        "..Y.....",
        "........",
    ),
    "partly_cloudy": (
        "..Y.....",
        ".Y.Y....",
        "..Y.....",
        "....C...",
        "..WWWC..",
        ".WWWWWW.",
        "WWWWWW..",
        ".BBBB...",
    ),
    "rain": (
        "........",
        "..WWWW..",
        ".WWWWWW.",
        "WWWWWWWW",
        ".WWWWWW.",
        "..B..B..",
        ".B..B...",
        "........",
    ),
    "clear_night": (
        "...CCC..",
        "..CC....",
        ".CC.....",
        ".CC.....",
        ".CC..C..",
        "..CCC...",
        "...C....",
        "........",
    ),
    "unavailable": (
        "..WWWW..",
        ".WW..WW.",
        ".....WW.",
        "....WW..",
        "...WW...",
        "..WW....",
        "........",
        "..WW....",
    ),
}

WEATHER_12: Final[Mapping[str, Matrix]] = {
    "clear_day": (
        ".....Y......",
        "..Y..Y..Y...",
        ".Y.......Y..",
        "...Y.Y.Y....",
        "...YYYYY....",
        "..YYYYYYY...",
        ".YYYYYYYYY..",
        "...YYYYYY...",
        "...Y.Y.Y....",
        "..Y..Y..Y...",
        ".Y...Y...Y..",
        ".....Y......",
    ),
    "partly_cloudy": (
        "..Y.Y.......",
        ".Y.Y.Y......",
        "..Y.Y.......",
        "...Y...YY...",
        "......CCCC..",
        ".....CCCCCC.",
        "...WWWWWWWW.",
        "..WWWWWWWWWW",
        ".WWWWWWWWWW.",
        "..BBBBBBBB..",
        "...BBBBBB...",
        "....BBBB....",
    ),
    "rain": (
        "...WWWWWW...",
        "..WWWWWWWW..",
        ".WWWWWWWWWW.",
        "WWWWWWWWWWWW",
        ".WWWWWWWWWW.",
        "..WWWWWWWW..",
        "...B..B..B..",
        "..B..B..B...",
        ".B..B..B....",
        "...B..B..B..",
        "..B..B..B...",
        "...B..B.....",
    ),
    "clear_night": (
        "....CCC.....",
        "...CC....C..",
        "..CC........",
        "..CC.....C..",
        "..CC........",
        "...CCC......",
        "....CC..C...",
        ".....C......",
        "....C....C..",
        "........C...",
        "..C.........",
        ".....C......",
    ),
    "unavailable": (
        "...WWWW.....",
        "..WWWWWW....",
        ".WW....WW...",
        ".......WW...",
        "......WW....",
        ".....WW.....",
        "....WW......",
        "...WW.......",
        "...WW.......",
        "............",
        "...WW.......",
        "...WW.......",
    ),
}


# Focused second-pass candidates.  These deliberately separate canvas size
# from optical weight: all weather candidates retain a 12x12 transparent
# canvas, but their live artwork is held to a compact internal footprint.
# This lets a later layout study overlap transparent padding into the existing
# row gaps instead of treating every 12x12 resource as a solid 60-unit tile.
FOCUS_CALENDAR_ICONS: Final[Mapping[str, Matrix]] = {
    "tearoff": (
        "01010000",
        "11111100",
        "10000100",
        "11111100",
        "10000100",
        "10000100",
        "10000100",
        "11111100",
    ),
    "rings": (
        "01001000",
        "11111110",
        "10000010",
        "11111110",
        "10000010",
        "10000010",
        "10000010",
        "11111110",
    ),
    "day_card": (
        "00110000",
        "01111000",
        "11001100",
        "10000100",
        "10110100",
        "10100100",
        "10000100",
        "11111100",
    ),
}

FOCUS_STEP_ICONS: Final[Mapping[str, Matrix]] = {
    "footprints": (
        "01100000",
        "11100000",
        "01000000",
        "00100000",
        "00000110",
        "00001110",
        "00000100",
        "00000010",
    ),
    "bootprint": (
        "00000010",
        "00000110",
        "00001100",
        "00011000",
        "00110000",
        "01111000",
        "11111100",
        "00111110",
    ),
    "sneaker": (
        "00000000",
        "00010000",
        "00111000",
        "00111100",
        "01111110",
        "11111111",
        "11111111",
        "00111111",
    ),
}

FOCUS_STEP_12: Final[Mapping[str, Matrix]] = {
    "walker_a": (
        "............",
        ".....11.....",
        ".....11.....",
        "....1111....",
        "..11.11.11..",
        "...1.11.1...",
        ".....11.....",
        "....1..1....",
        "...11..11...",
        "..11....11..",
        ".11......11.",
        "............",
    ),
    "walker_b": (
        "............",
        ".....11.....",
        ".....11.....",
        "....1111....",
        "...1.11.1...",
        "..11.11..11.",
        ".....11.....",
        "....1..1....",
        "...11...1...",
        "..11....11..",
        ".11......11.",
        "............",
    ),
}


def _compact_battery(_level: int, charging: bool = False) -> Matrix:
    """Return a light battery mark centered inside an 8x8 canvas.

    The adjacent percentage already communicates level, so normal states keep
    the outline hollow instead of duplicating the value as a heavy filled bar.
    """

    rows = [
        list("00000000"),
        list("00000000"),
        list("01111100"),
        list("01000110"),
        list("01000110"),
        list("01111100"),
        list("00000000"),
        list("00000000"),
    ]
    if charging:
        for y, x in ((2, 4), (3, 3), (3, 4), (4, 2), (4, 3), (5, 2)):
            rows[y][x] = "1"
    return tuple("".join(row) for row in rows)


FOCUS_BATTERY_ICONS: Final[Mapping[str, Matrix]] = {
    "empty": _compact_battery(0),
    "low": _compact_battery(1),
    "mid": _compact_battery(2),
    "high": _compact_battery(3),
    "full": _compact_battery(3),
    "charging": _compact_battery(0, charging=True),
}


FOCUS_WEATHER_12: Final[Mapping[str, Mapping[str, Matrix]]] = {
    "outline": {
        "clear_day": (
            "............",
            ".....Y......",
            "..Y..Y..Y...",
            "...YYYYY....",
            "...Y...Y....",
            ".YYY...YYY..",
            "...Y...Y....",
            "...YYYYY....",
            "..Y..Y..Y...",
            ".....Y......",
            "............",
            "............",
        ),
        "partly_cloudy": (
            "............",
            "...Y.Y......",
            "..YYYYY.....",
            "...Y.Y.C....",
            "......CCC...",
            "....WWWWWW..",
            "...WW....WW.",
            "..WW......WW",
            "..WWWWWWWWWW",
            "...C.C.C.C..",
            "....B.B.B...",
            "............",
        ),
        "rain": (
            "............",
            "....WWW.....",
            "..WW...WW...",
            ".WW.....WW..",
            ".WWWWWWWWW..",
            "............",
            "...B..B..B..",
            "..B..B..B...",
            "...B..B..B..",
            "............",
            "............",
            "............",
        ),
        "clear_night": (
            "............",
            "....CCC.....",
            "...CC.......",
            "..CC........",
            "..CC.....C..",
            "..CC........",
            "...CC.......",
            "....CCC.....",
            "......C.....",
            ".........C..",
            "............",
            "............",
        ),
        "unavailable": (
            "............",
            "....WWWW....",
            "...WW..WW...",
            ".......WW...",
            "......WW....",
            ".....WW.....",
            "....WW......",
            "............",
            "....WW......",
            "............",
            "............",
            "............",
        ),
    },
    "sprite": {
        "clear_day": (
            "............",
            ".....Y......",
            "...Y.Y.Y....",
            "..Y.YYY.Y...",
            "...YYYYY....",
            ".YYYYYYYYY..",
            "...YYYYY....",
            "..Y.YYY.Y...",
            "...Y.Y.Y....",
            ".....Y......",
            "............",
            "............",
        ),
        "partly_cloudy": (
            "............",
            "...YYY......",
            "..YYYYY.....",
            "...YYY.C....",
            "......CCCC..",
            "....WWCCCCC.",
            "...WWWWWWWW.",
            "..WWWWWWWWWW",
            "...CCCCCCCC.",
            "....BBBBBB..",
            "............",
            "............",
        ),
        "rain": (
            "............",
            "....WWW.....",
            "..WWWWWWW...",
            ".WWWWWWWWW..",
            "..CCCCCCC...",
            "...CCCCCC...",
            "............",
            "...B..B..B..",
            "..BB.BB.BB..",
            "...B..B..B..",
            "............",
            "............",
        ),
        "clear_night": (
            "............",
            "....CCC.....",
            "...CCCC..C..",
            "..CCCC......",
            "..CCC.......",
            "..CCCC...C..",
            "...CCCC.....",
            "....CCCC....",
            "......C.....",
            ".........C..",
            "............",
            "............",
        ),
        "unavailable": (
            "............",
            "....WWWW....",
            "...WW..WW...",
            ".......WW...",
            "......WW....",
            ".....WW.....",
            "....WW......",
            "............",
            "....WW......",
            "............",
            "............",
            "............",
        ),
    },
}


STUDY_VARIANTS: Final[Mapping[str, Mapping[str, object]]] = {
    "all8": {
        "label": "A: ALL 8x8",
        "description": "8x8 weather, calendar page, walking-person, and horizontal battery bar",
        "weather_size": 8,
        "bands": {
            "weather": (60, 100),
            "date": (120, 160),
            "time": (180, 270),
            "steps": (290, 330),
            "battery": (350, 390),
        },
        "icon_set": {
            "calendar": "page",
            "steps": "walking_person",
            "battery": "bar",
        },
        "time_center_offset": 0,
    },
    "mixed12": {
        "label": "B: 12x12 WEATHER",
        "description": "12x12 weather feature with the same 8x8 utility vocabulary and horizontal battery bar",
        "weather_size": 12,
        "bands": {
            "weather": (60, 120),
            "date": (140, 180),
            "time": (200, 290),
            "steps": (310, 350),
            "battery": (370, 410),
        },
        "icon_set": {
            "calendar": "page",
            "steps": "walking_person",
            "battery": "bar",
        },
        # The 12x12 top feature consumes 20 more units vertically than the
        # 8x8 row.  Keeping every gap at 20 shifts the time center down 20.
        "time_center_offset": 20,
    },
}


STUDY_STATES: Final[Mapping[str, Mapping[str, str]]] = {
    "available": {
        "weather": "partly_cloudy",
        "temperature": "21°C",
        "date": "SAT 15 AUG",
        "steps": "03642",
        "battery": "82%",
        "battery_level": "high",
    },
    "unavailable": {
        "weather": "unavailable",
        "temperature": "--",
        "date": "SAT 15 AUG",
        "steps": "03642",
        "battery": "82%",
        "battery_level": "high",
    },
    "worst": {
        "weather": "clear_day",
        "temperature": "-100°C",
        "date": "SAT 15 AUG",
        "steps": "999999",
        "battery": "100%",
        "battery_level": "full",
    },
}


def validate_study_matrices() -> None:
    """Raise ``ValueError`` if a study matrix violates its fixed vocabulary."""

    utility_groups = {
        "calendar": CALENDAR_ICONS,
        "steps": STEP_ICONS,
        "focus-calendar": FOCUS_CALENDAR_ICONS,
        "focus-steps": FOCUS_STEP_ICONS,
        "focus-battery": FOCUS_BATTERY_ICONS,
    }
    for group_name, group in utility_groups.items():
        for name, rows in group.items():
            if len(rows) != 8 or any(len(row) != 8 for row in rows):
                raise ValueError(f"{group_name}/{name}: expected 8x8 matrix")
            if set("".join(rows)) - {"0", "1"}:
                raise ValueError(f"{group_name}/{name}: utility cells must be binary")

    for style_name, states in BATTERY_STYLES.items():
        for state_name, rows in states.items():
            if len(rows) != 8 or any(len(row) != 8 for row in rows):
                raise ValueError(f"battery/{style_name}/{state_name}: expected 8x8 matrix")
            if set("".join(rows)) - {"0", "1"}:
                raise ValueError(f"battery/{style_name}/{state_name}: utility cells must be binary")

    for size, group in ((8, WEATHER_8), (12, WEATHER_12)):
        for name, rows in group.items():
            if len(rows) != size or any(len(row) != size for row in rows):
                raise ValueError(f"weather/{size}/{name}: expected {size}x{size} matrix")
            if set("".join(rows)) - {".", "Y", "C", "B", "W"}:
                raise ValueError(f"weather/{size}/{name}: unknown palette cell")

    for family_name, group in FOCUS_WEATHER_12.items():
        for name, rows in group.items():
            if len(rows) != 12 or any(len(row) != 12 for row in rows):
                raise ValueError(f"focus-weather/{family_name}/{name}: expected 12x12 matrix")
            if set("".join(rows)) - {".", "Y", "C", "B", "W"}:
                raise ValueError(
                    f"focus-weather/{family_name}/{name}: unknown palette cell"
                )

    for name, rows in FOCUS_STEP_12.items():
        if len(rows) != 12 or any(len(row) != 12 for row in rows):
            raise ValueError(f"focus-steps-12/{name}: expected 12x12 matrix")
        if set("".join(rows)) - {"0", "1", "."}:
            raise ValueError(f"focus-steps-12/{name}: utility cells must be binary")

    for variant_name, variant in STUDY_VARIANTS.items():
        bands = variant["bands"]
        previous_end = None
        for region in ("weather", "date", "time", "steps", "battery"):
            start, end = bands[region]
            if end <= start:
                raise ValueError(f"{variant_name}/{region}: invalid band")
            if previous_end is not None and start - previous_end != 20:
                raise ValueError(f"{variant_name}: row gap before {region} is not 20")
            previous_end = end


validate_study_matrices()
