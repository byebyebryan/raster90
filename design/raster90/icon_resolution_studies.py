"""Raster 90 icon-resolution evidence and selected solid-grid matrices.

Direction A keeps genuinely 8x8 artwork and assumes solid contiguous pixels.
Direction B is authored directly at 16x16 for the earlier 3-pitch/2-lit
fictional display. The selected runtime promotes the same true 16x16 matrices
with solid 3x3 cells; this module remains their authoritative, reviewable
source so the generator and design studies cannot drift.
"""

from __future__ import annotations

from typing import Final, Mapping, Sequence

from matrices import (
    WEATHER_CONDITIONS,
    WEATHER_DAY_RESOLUTION,
    WEATHER_NIGHT_RESOLUTION,
    WEATHER_SPRITES,
    WEATHER_STALE,
)


Matrix = tuple[str, ...]


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
    condition: WEATHER_SPRITES[sprite_name]
    for condition, sprite_name in enumerate(WEATHER_DAY_RESOLUTION)
}
EIGHT_WEATHER_NIGHT: Final[Mapping[int, Matrix]] = {
    condition: WEATHER_SPRITES[sprite_name]
    for condition, sprite_name in enumerate(WEATHER_NIGHT_RESOLUTION)
}


def _overlay(*layers: Sequence[str]) -> Matrix:
    """Combine same-sized direct-authored layers without resampling."""

    size = 16
    output = [["." for _x in range(size)] for _y in range(size)]
    for layer in layers:
        if len(layer) != size or any(len(row) != size for row in layer):
            raise ValueError("16x16 weather layer has invalid dimensions")
        for y, row in enumerate(layer):
            for x, symbol in enumerate(row):
                if symbol != ".":
                    output[y][x] = symbol
    return tuple("".join(row) for row in output)


SIXTEEN_UTILITY_ICONS: Final[Mapping[str, Matrix]] = {
    "date": (
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
    ),
    "steps": (
        "................",
        ".......11.......",
        "......1111......",
        "......1111......",
        ".......11.......",
        "................",
        "....11.11.11....",
        "...11..11..11...",
        "....1..11..1....",
        ".......11.......",
        "......1111......",
        ".....11..11.....",
        "....11....11....",
        "...11......11...",
        "..111......111..",
        "................",
    ),
    "battery": (
        "................",
        "................",
        "................",
        "................",
        ".111111111111...",
        ".1..........1...",
        ".1..........111.",
        ".1..........111.",
        ".1..........111.",
        ".1..........111.",
        ".1..........1...",
        ".111111111111...",
        "................",
        "................",
        "................",
        "................",
    ),
}


_CLOUD_16: Final[Matrix] = (
    "................",
    "......WWW.......",
    "....WW...WW.....",
    "...W.......W....",
    "...W........WW..",
    "..W...........W.",
    ".W.............W",
    ".W.............W",
    "..WWWWWWWWWWWW..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
)

_PARTLY_CLOUD_16: Final[Matrix] = (
    "................",
    "................",
    "................",
    "................",
    "................",
    "........WWW.....",
    "......WW...WW...",
    ".....W.......W..",
    "..WWW.........W.",
    ".W.............W",
    ".W.............W",
    "..WWWWWWWWWWWW..",
    "................",
    "................",
    "................",
    "................",
)

_RAIN_16: Final[Matrix] = (
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "...B....B....B..",
    "..B....B....B...",
    "................",
    "....B....B......",
    "...B....B.......",
    "................",
)

_HEAVY_RAIN_16: Final[Matrix] = (
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "...B...B...B....",
    "..B...B...B.....",
    ".B...B...B...B..",
    "...B...B...B....",
    "..B...B...B.....",
    ".B...B...B...B..",
    "................",
)

_SNOW_16: Final[Matrix] = (
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "...C......C.....",
    "..CCC....CCC....",
    "...C......C.....",
    ".......C........",
    "......CCC.......",
    ".......C........",
)

_HEAVY_SNOW_16: Final[Matrix] = (
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "..C....C....C...",
    ".CCC..CCC..CCC..",
    "..C....C....C...",
    "................",
    "....C.....C.....",
    "...CCC...CCC....",
    "....C.....C.....",
)

_SLEET_16: Final[Matrix] = (
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "...B......C.....",
    "..B......CCC....",
    ".........C......",
    "......C......B..",
    ".....CCC....B...",
    "......C.........",
)

_THUNDER_16: Final[Matrix] = (
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    ".......Y........",
    "......YY........",
    ".....YY.........",
    ".......Y........",
    "......Y.........",
    ".....Y..........",
    "................",
)

SIXTEEN_WEATHER_SPRITES: Final[Mapping[str, Matrix]] = {
    "unknown": (
        "....WWWWWWWW....",
        "..WW........WW..",
        ".W............W.",
        ".W....WWW.....W.",
        ".W...W...W....W.",
        ".W.......W....W.",
        ".W......W.....W.",
        ".W.....W......W.",
        ".W.....W......W.",
        ".W............W.",
        ".W.....W......W.",
        ".W............W.",
        ".W............W.",
        "..WW........WW..",
        "....WWWWWWWW....",
        "................",
    ),
    "clear_day": (
        ".......Y........",
        "..Y....Y....Y...",
        "...Y...Y...Y....",
        ".....YYYYY......",
        "....Y.....Y.....",
        "....Y.....Y.....",
        "YYY.Y.....Y.YYY.",
        "....Y.....Y.....",
        "....Y.....Y.....",
        ".....YYYYY......",
        "...Y...Y...Y....",
        "..Y....Y....Y...",
        ".......Y........",
        "................",
        "................",
        "................",
    ),
    "clear_night": (
        "......CC........",
        "....CCCC........",
        "...CCC.......C..",
        "..CCC...........",
        "..CC............",
        ".CCC........C...",
        ".CCC.......CCC..",
        ".CCC........C...",
        ".CCC............",
        "..CC............",
        "..CCC.......C...",
        "...CCC..........",
        "....CCCC........",
        "......CC........",
        "................",
        "................",
    ),
    "partly_day": _overlay(
        (
            "....Y...........",
            ".Y..Y..Y........",
            "..YYYYY.........",
            "..Y...Y.........",
            ".YY...YY........",
            "..Y...Y.........",
            "..YYYYY.........",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
        ),
        _PARTLY_CLOUD_16,
    ),
    "partly_night": _overlay(
        (
            "...CCC..........",
            "..CC............",
            ".CC.............",
            ".CC........C....",
            ".CC.......CCC...",
            "..CC.......C....",
            "...CCC..........",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
        ),
        _PARTLY_CLOUD_16,
    ),
    "cloudy": _CLOUD_16,
    "fog": (
        "................",
        "................",
        "...WWWWWWW......",
        "..W.......WW....",
        "................",
        ".....CCCCCC.....",
        "...CC......CC...",
        "................",
        "..BBBBBBBBBB....",
        ".B..........BBB.",
        "................",
        "....CCCCCCCC....",
        "...C........CC..",
        "................",
        "................",
        "................",
    ),
    "heavy_rain": _overlay(_CLOUD_16, _HEAVY_RAIN_16),
    "heavy_snow": _overlay(_CLOUD_16, _HEAVY_SNOW_16),
    "rain": _overlay(_CLOUD_16, _RAIN_16),
    "snow": _overlay(_CLOUD_16, _SNOW_16),
    "thunderstorm": _overlay(_CLOUD_16, _THUNDER_16),
    "sleet": _overlay(_CLOUD_16, _SLEET_16),
    "windy": (
        "................",
        "....CCCC........",
        "..CC....CCC.....",
        ".C........C.....",
        "..........CC....",
        "......BBBB......",
        "...BBB....BBBB..",
        "..B...........B.",
        ".........BBBB...",
        ".....BBBB.......",
        "..CCC...........",
        ".C....CCCCCCCC..",
        "..CCC...........",
        "................",
        "................",
        "................",
    ),
}

SIXTEEN_WEATHER_DAY: Final[Mapping[int, Matrix]] = {
    condition: SIXTEEN_WEATHER_SPRITES[sprite_name]
    for condition, sprite_name in enumerate(WEATHER_DAY_RESOLUTION)
}
SIXTEEN_WEATHER_NIGHT: Final[Mapping[int, Matrix]] = {
    condition: SIXTEEN_WEATHER_SPRITES[sprite_name]
    for condition, sprite_name in enumerate(WEATHER_NIGHT_RESOLUTION)
}

STALE_MARKER: Final[Matrix] = WEATHER_STALE


def _validate_matrix(name: str, rows: Sequence[str], size: int, symbols: set[str]) -> None:
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
    if len(WEATHER_CONDITIONS) != 16:
        raise ValueError("expected all 16 WFF weather conditions")
    for name, rows in EIGHT_UTILITY_ICONS.items():
        _validate_matrix(f"8x8 utility {name}", rows, 8, {"0", "1", "."})
    for phase, sprites in (
        ("day", EIGHT_WEATHER_DAY),
        ("night", EIGHT_WEATHER_NIGHT),
    ):
        if set(sprites) != set(range(16)):
            raise ValueError(f"8x8 {phase}: incomplete WFF condition map")
        for condition, rows in sprites.items():
            _validate_matrix(f"8x8 {phase} {condition}", rows, 8, {".", "Y", "C", "B", "W"})

    for name, rows in SIXTEEN_UTILITY_ICONS.items():
        _validate_matrix(f"16x16 utility {name}", rows, 16, {"0", "1", "."})
        if _is_doubled_8x8(rows):
            raise ValueError(f"16x16 utility {name}: still consists of doubled 8x8 cells")
    for phase, sprites in (
        ("day", SIXTEEN_WEATHER_DAY),
        ("night", SIXTEEN_WEATHER_NIGHT),
    ):
        if set(sprites) != set(range(16)):
            raise ValueError(f"16x16 {phase}: incomplete WFF condition map")
        for condition, rows in sprites.items():
            _validate_matrix(f"16x16 {phase} {condition}", rows, 16, {".", "Y", "C", "B", "W"})
            if _is_doubled_8x8(rows):
                raise ValueError(
                    f"16x16 {phase} {condition}: still consists of doubled 8x8 cells"
                )
