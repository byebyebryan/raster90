"""Raster 90 icon-resolution evidence and historical design controls.

The selected runtime family is authoritative under ``icons/raster90/family.py``.
This module retains the genuinely 8x8 comparison direction and the calendar
study control used by old decision sheets. Its selected true-16 compatibility
aliases point to the canonical family so design renderers cannot drift from
the packaged surfaces.
"""

from __future__ import annotations

from typing import Final, Mapping, Sequence

from icons.raster90.family import (
    PALETTE,
    SELECTED_UTILITY_ICONS,
    STALE_MARKER,
    WEATHER_CONDITIONS,
    WEATHER_DAY,
    WEATHER_DAY_RESOLUTION,
    WEATHER_NIGHT,
    WEATHER_NIGHT_RESOLUTION,
    WEATHER_SPRITES,
)
from matrices import (
    WEATHER_SPRITES as EIGHT_WEATHER_SPRITES,
    WEATHER_DAY_RESOLUTION as EIGHT_WEATHER_DAY_RESOLUTION,
    WEATHER_NIGHT_RESOLUTION as EIGHT_WEATHER_NIGHT_RESOLUTION,
)


Matrix = tuple[str, ...]


# Historical direction A: genuinely 8x8 artwork with solid contiguous cells.
EIGHT_UTILITY_ICONS: Final[Mapping[str, Matrix]] = {
    "date": (
        ".1..1...",
        "1111111.",
        "1.....1.",
        "1111111.",
        "1.....1.",
        "1.1.1.1.",
        "1.....1.",
        "1111111.",
    ),
    "steps": (
        ".11.....",
        "111.....",
        ".11.....",
        "..1.....",
        ".....11.",
        "....111.",
        ".....11.",
        ".....1..",
    ),
    "battery": (
        "........",
        "........",
        ".11111..",
        ".1...11.",
        ".1....11",
        ".1...11.",
        ".11111..",
        "........",
    ),
}

EIGHT_WEATHER_DAY: Final[Mapping[int, Matrix]] = {
    condition: EIGHT_WEATHER_SPRITES[sprite_name]
    for condition, sprite_name in enumerate(EIGHT_WEATHER_DAY_RESOLUTION)
}
EIGHT_WEATHER_NIGHT: Final[Mapping[int, Matrix]] = {
    condition: EIGHT_WEATHER_SPRITES[sprite_name]
    for condition, sprite_name in enumerate(EIGHT_WEATHER_NIGHT_RESOLUTION)
}


# Historical calendar-only control retained for the old icon-resolution sheet.
_HISTORICAL_DATE_ICON: Final[Matrix] = (
    "................",
    ".....1...1......",
    "..111111111111..",
    "..1..........1..",
    "..111111111111..",
    "..1..........1..",
    "..1..1..1..1.1..",
    "..1..........1..",
    "..1..1..1..1.1..",
    "..1..........1..",
    "..1..1..1..1.1..",
    "..1..........1..",
    "..1..1..1..1.1..",
    "..1..........1..",
    "..111111111111..",
    "................",
)

# The design surface intentionally keeps ``date`` for historical comparisons,
# but selected runtime utilities are imported by identity from the canonical
# component and contain no calendar key.
SIXTEEN_UTILITY_ICONS: Final[Mapping[str, Matrix]] = {
    "date": _HISTORICAL_DATE_ICON,
    **SELECTED_UTILITY_ICONS,
}
SIXTEEN_WEATHER_SPRITES: Final[Mapping[str, Matrix]] = WEATHER_SPRITES
SIXTEEN_WEATHER_DAY: Final[Mapping[int, Matrix]] = WEATHER_DAY
SIXTEEN_WEATHER_NIGHT: Final[Mapping[int, Matrix]] = WEATHER_NIGHT


def _validate_matrix(
    name: str,
    rows: Sequence[str],
    size: int,
    symbols: set[str],
) -> None:
    if len(rows) != size or any(len(row) != size for row in rows):
        raise ValueError(f"{name}: expected {size}x{size} matrix")
    used = set("".join(rows))
    if not used <= symbols:
        raise ValueError(f"{name}: unexpected symbols {sorted(used - symbols)}")
    if used <= {"0", "."}:
        raise ValueError(f"{name}: matrix is empty")


def _is_doubled_8x8(rows: Sequence[str]) -> bool:
    if len(rows) != 16 or any(len(row) != 16 for row in rows):
        return False
    return all(
        len({rows[y][x], rows[y][x + 1], rows[y + 1][x], rows[y + 1][x + 1]}) == 1
        for y in range(0, 16, 2)
        for x in range(0, 16, 2)
    )


def validate_icon_resolution_studies() -> None:
    """Validate both historical controls and canonical selected aliases."""

    if len(WEATHER_CONDITIONS) != 16:
        raise ValueError("expected all 16 WFF weather conditions")
    for name, rows in EIGHT_UTILITY_ICONS.items():
        _validate_matrix(f"8x8 utility {name}", rows, 8, {"0", "1", "."})
    for phase, sprites in (("day", EIGHT_WEATHER_DAY), ("night", EIGHT_WEATHER_NIGHT)):
        if set(sprites) != set(range(16)):
            raise ValueError(f"8x8 {phase}: incomplete WFF condition map")
        for condition, rows in sprites.items():
            _validate_matrix(
                f"8x8 {phase} {condition}",
                rows,
                8,
                {".", "Y", "C", "B", "W"},
            )
    for name, rows in SIXTEEN_UTILITY_ICONS.items():
        _validate_matrix(f"16x16 utility {name}", rows, 16, {"0", "1", "."})
        if _is_doubled_8x8(rows):
            raise ValueError(f"16x16 utility {name}: still consists of doubled 8x8 cells")
    for phase, sprites in (("day", SIXTEEN_WEATHER_DAY), ("night", SIXTEEN_WEATHER_NIGHT)):
        if set(sprites) != set(range(16)):
            raise ValueError(f"16x16 {phase}: incomplete WFF condition map")
        for condition, rows in sprites.items():
            _validate_matrix(
                f"16x16 {phase} {condition}",
                rows,
                16,
                {".", "Y", "C", "B", "W"},
            )
            if _is_doubled_8x8(rows):
                raise ValueError(f"16x16 {phase} {condition}: still consists of doubled 8x8 cells")
    if STALE_MARKER != ("10", "01"):
        raise ValueError("stale marker drifted")
    if PALETTE != {
        "Y": (255, 216, 0, 255),
        "C": (73, 223, 255, 255),
        "B": (36, 116, 255, 255),
        "W": (255, 255, 255, 255),
    }:
        raise ValueError("indexed palette drifted")
