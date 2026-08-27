"""Authoritative, project-owned Raster 90 icon family.

The watch-face runtime consumes this module directly.  Every matrix is an
exact source-cell grid: a lit icon cell becomes one solid 3x3 physical pixel
square in the WFF generator.  No matrix in this module is traced, downsampled,
or expanded from an older icon study.

The public aliases intentionally keep the runtime/study boundary explicit:

``SELECTED_UTILITY_ICONS``
    The only persistent utility tiles currently packaged (steps and battery).
``BATTERY_COLOR_BANDS``
    Mutually-exclusive lower-exclusive/upper-inclusive ranges and RGBA tints
    for the existing battery resource; the final row is the low range.
``WEATHER_DAY`` / ``WEATHER_NIGHT``
    Complete condition-ID mappings for the 16 WFF weather values.
``UNAVAILABLE_WEATHER_ICON``
    The neutral ``unknown`` sprite used with ``--`` when data is unavailable.
``STALE_MARKER``
    A two-cell monochrome marker overlaid by the weather data branch.

Calendar art, 8x8/12x12 controls, and rejected step treatments remain under
``design/raster90/`` as historical evidence and are deliberately absent from
the selected utility mapping here.
"""

from __future__ import annotations

from typing import Final, Mapping, Sequence


Matrix = tuple[str, ...]
RGBA = tuple[int, int, int, int]

# This is the exact indexed weather palette used by the WFF assets.  The four
# opaque entries are intentionally flat and stable; utility tiles use white
# as their resource color.  The battery icon's state tints are declared below
# so the runtime and review presentation share one explicit contract.
PALETTE: Final[Mapping[str, RGBA]] = {
    "Y": (255, 216, 0, 255),    # #FFD800 yellow
    "C": (73, 223, 255, 255),   # #49DFFF pale cyan
    "B": (36, 116, 255, 255),   # #2474FF blue
    "W": (255, 255, 255, 255),  # white
}
WEATHER_PALETTE = PALETTE

# Mutually-exclusive battery tint ranges.  Each row is
# ``(name, minimum_exclusive, maximum_inclusive, RGBA)``; ``None`` denotes an
# open bound, and the final row is the 0..10% red range for the valid battery
# source domain.  Keeping these bounds and RGBA values here lets XML checks
# and deterministic presentation derive their expectations from one source.
BatteryColorBand = tuple[str, int | None, int | None, RGBA]
BATTERY_COLOR_BANDS: Final[tuple[BatteryColorBand, ...]] = (
    ("white", 50, None, PALETTE["W"]),
    ("yellow", 25, 50, PALETTE["Y"]),
    ("orange", 10, 25, (255, 133, 0, 255)),    # #FF8500 orange
    ("red", None, 10, (255, 48, 48, 255)),     # #FF3030 red
)

# WFF weather condition IDs, in the order consumed by the declarative data
# source.  Day/night resolution is complete even where the selected artwork
# intentionally reuses a truthful neutral family member.
WEATHER_CONDITIONS: Final[tuple[str, ...]] = (
    "unknown",
    "clear",
    "cloudy",
    "fog",
    "heavy_rain",
    "heavy_snow",
    "rain",
    "snow",
    "sunny",
    "thunderstorm",
    "sleet",
    "light_snow",
    "light_rain",
    "mist",
    "partly_cloudy",
    "windy",
)

WEATHER_DAY_RESOLUTION: Final[tuple[str, ...]] = (
    "unknown",
    "clear_day",
    "cloudy",
    "fog",
    "heavy_rain",
    "heavy_snow",
    "rain",
    "snow",
    "clear_day",
    "thunderstorm",
    "sleet",
    "snow",
    "rain",
    "fog",
    "partly_day",
    "windy",
)
WEATHER_NIGHT_RESOLUTION: Final[tuple[str, ...]] = (
    "unknown",
    "clear_night",
    "cloudy",
    "fog",
    "heavy_rain",
    "heavy_snow",
    "rain",
    "snow",
    "clear_night",
    "thunderstorm",
    "sleet",
    "snow",
    "rain",
    "fog",
    "partly_night",
    "windy",
)
# Descriptive aliases kept stable for renderers and external review scripts.
CONDITIONS = WEATHER_CONDITIONS
DAY_RESOLUTION = WEATHER_DAY_RESOLUTION
NIGHT_RESOLUTION = WEATHER_NIGHT_RESOLUTION

# Approved runtime utility tile.  The big toe on each footprint is a 1x2
# vertical line; the three other toe marks on each footprint are 1x1.  The
# soles remain the reviewed closed, tapered contours.
APPROVED_STEP_NAME: Final[str] = "four-toe-vertical"
APPROVED_STEP_ICON: Final[Matrix] = (
    ".........1..1...",
    ".........1....1.",
    "...1..1........1",
    ".1....1..11111..",
    "1........1....1.",
    "..11111..1....1.",
    ".1....1..1...1..",
    ".1....1..1...1..",
    ".1...1....1..1..",
    "..1..1....1.1...",
    "..1..1....1.1...",
    "...1.1....111...",
    "...1.1..........",
    "...111..........",
    "................",
    "................",
)
# Preserve the focused study's descriptive source name as a stable alias while
# keeping the runtime-facing name concise.
FOUR_TOE_VERTICAL_BIG_OUTLINE: Final[Matrix] = APPROVED_STEP_ICON

BATTERY_ICON: Final[Matrix] = (
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
)

SELECTED_UTILITY_ICONS: Final[Mapping[str, Matrix]] = {
    "steps": APPROVED_STEP_ICON,
    "battery": BATTERY_ICON,
}
# Stable short aliases for generators and design studies.
UTILITY_ICONS = SELECTED_UTILITY_ICONS
STEPS_ICON = APPROVED_STEP_ICON
ICON_MATRICES = SELECTED_UTILITY_ICONS


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


_CLOUD: Final[Matrix] = (
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
_PARTLY_CLOUD: Final[Matrix] = (
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
_RAIN: Final[Matrix] = (
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
_HEAVY_RAIN: Final[Matrix] = (
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
_SNOW: Final[Matrix] = (
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
_HEAVY_SNOW: Final[Matrix] = (
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
_SLEET: Final[Matrix] = (
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
_THUNDER: Final[Matrix] = (
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

WEATHER_SPRITES: Final[Mapping[str, Matrix]] = {
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
        _PARTLY_CLOUD,
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
        _PARTLY_CLOUD,
    ),
    "cloudy": _CLOUD,
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
    "heavy_rain": _overlay(_CLOUD, _HEAVY_RAIN),
    "heavy_snow": _overlay(_CLOUD, _HEAVY_SNOW),
    "rain": _overlay(_CLOUD, _RAIN),
    "snow": _overlay(_CLOUD, _SNOW),
    "thunderstorm": _overlay(_CLOUD, _THUNDER),
    "sleet": _overlay(_CLOUD, _SLEET),
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

WEATHER_DAY: Final[Mapping[int, Matrix]] = {
    condition: WEATHER_SPRITES[sprite_name]
    for condition, sprite_name in enumerate(WEATHER_DAY_RESOLUTION)
}
WEATHER_NIGHT: Final[Mapping[int, Matrix]] = {
    condition: WEATHER_SPRITES[sprite_name]
    for condition, sprite_name in enumerate(WEATHER_NIGHT_RESOLUTION)
}
# Stable descriptive aliases used by existing studies and external checks.
SIXTEEN_WEATHER_SPRITES = WEATHER_SPRITES
SIXTEEN_WEATHER_DAY = WEATHER_DAY
SIXTEEN_WEATHER_NIGHT = WEATHER_NIGHT
WEATHER_DAY_MAPPING = WEATHER_DAY
WEATHER_NIGHT_MAPPING = WEATHER_NIGHT

UNAVAILABLE_WEATHER_ICON: Final[Matrix] = WEATHER_SPRITES["unknown"]
NEUTRAL_WEATHER_ICON = UNAVAILABLE_WEATHER_ICON
UNAVAILABLE_ICON = UNAVAILABLE_WEATHER_ICON
STALE_MARKER: Final[Matrix] = ("10", "01")
WEATHER_STALE = STALE_MARKER


def _validate_matrix(
    name: str,
    rows: Sequence[str],
    width: int,
    height: int,
    symbols: set[str],
) -> None:
    if len(rows) != height or any(len(row) != width for row in rows):
        raise ValueError(f"{name}: expected {width}x{height} matrix")
    used = set("".join(rows))
    if not used <= symbols:
        raise ValueError(f"{name}: unexpected symbols {sorted(used - symbols)}")
    if used <= {"0", "."}:
        raise ValueError(f"{name}: matrix is empty")


def _is_doubled_8x8(rows: Sequence[str]) -> bool:
    """Return whether a 16x16 matrix is only an integer-expanded 8x8 grid."""

    if len(rows) != 16 or any(len(row) != 16 for row in rows):
        return False
    return all(
        len({rows[y][x], rows[y][x + 1], rows[y + 1][x], rows[y + 1][x + 1]}) == 1
        for y in range(0, 16, 2)
        for x in range(0, 16, 2)
    )


def validate_icon_family() -> None:
    """Validate the complete selected runtime family and its stable aliases."""

    if len(WEATHER_CONDITIONS) != 16:
        raise ValueError("expected all 16 WFF weather conditions")
    if len(WEATHER_DAY_RESOLUTION) != len(WEATHER_CONDITIONS):
        raise ValueError("day weather resolution map is incomplete")
    if len(WEATHER_NIGHT_RESOLUTION) != len(WEATHER_CONDITIONS):
        raise ValueError("night weather resolution map is incomplete")
    if set(WEATHER_SPRITES) != {
        "unknown",
        "clear_day",
        "clear_night",
        "partly_day",
        "partly_night",
        "cloudy",
        "fog",
        "heavy_rain",
        "heavy_snow",
        "rain",
        "snow",
        "thunderstorm",
        "sleet",
        "windy",
    }:
        raise ValueError("weather sprite vocabulary drifted")
    for phase, resolution, mapping in (
        ("day", WEATHER_DAY_RESOLUTION, WEATHER_DAY),
        ("night", WEATHER_NIGHT_RESOLUTION, WEATHER_NIGHT),
    ):
        if set(mapping) != set(range(16)):
            raise ValueError(f"{phase} weather map is incomplete")
        for condition, sprite_name in enumerate(resolution):
            if sprite_name not in WEATHER_SPRITES:
                raise ValueError(f"{phase} weather condition {condition} is unmapped")
            rows = mapping[condition]
            _validate_matrix(
                f"16x16 weather {phase} {condition}",
                rows,
                16,
                16,
                set(PALETTE) | {"."},
            )
            if _is_doubled_8x8(rows):
                raise ValueError(f"16x16 weather {phase} {condition} is doubled 8x8 art")
    if set(SELECTED_UTILITY_ICONS) != {"steps", "battery"}:
        raise ValueError("selected utility surface must contain only steps and battery")
    for name, rows in SELECTED_UTILITY_ICONS.items():
        _validate_matrix(f"16x16 utility {name}", rows, 16, 16, {".", "0", "1"})
        if _is_doubled_8x8(rows):
            raise ValueError(f"16x16 utility {name} is doubled 8x8 art")
    if STEPS_ICON is not APPROVED_STEP_ICON:
        raise ValueError("steps stable alias is not the approved icon")
    if SELECTED_UTILITY_ICONS["steps"] is not APPROVED_STEP_ICON:
        raise ValueError("steps runtime mapping is not directly bound to the approved icon")
    if SELECTED_UTILITY_ICONS["battery"] is not BATTERY_ICON:
        raise ValueError("battery runtime mapping is not directly bound to its source")
    _validate_matrix("neutral unavailable weather", UNAVAILABLE_WEATHER_ICON, 16, 16, set(PALETTE) | {"."})
    _validate_matrix("stale marker", STALE_MARKER, 2, 2, {"0", "1"})
    if UNAVAILABLE_WEATHER_ICON is not WEATHER_SPRITES["unknown"]:
        raise ValueError("unavailable weather alias drifted")
    if len(PALETTE) != 4 or PALETTE != {
        "Y": (255, 216, 0, 255),
        "C": (73, 223, 255, 255),
        "B": (36, 116, 255, 255),
        "W": (255, 255, 255, 255),
    }:
        raise ValueError("indexed weather palette drifted")
    if BATTERY_COLOR_BANDS != (
        ("white", 50, None, PALETTE["W"]),
        ("yellow", 25, 50, PALETTE["Y"]),
        ("orange", 10, 25, (255, 133, 0, 255)),
        ("red", None, 10, (255, 48, 48, 255)),
    ):
        raise ValueError("battery color-state contract drifted")


validate_icon_family()
