"""Human-readable Raster 90 bitmap matrices.

The matrices describe source cells, not display pixels. The asset generator
expands each lit cell into an exact solid square. Keeping these definitions as
plain strings makes a glyph or sprite reviewable without an image editor.
"""

from __future__ import annotations

# Typography is defined once in the focused font-family module.  These aliases
# preserve the historical matrix import surface used by design studies while
# keeping all glyph data authoritative in fonts/raster90/family.py.
from fonts.raster90.family import (
    PRIMARY_COLON,
    PRIMARY_DIGITS,
    PRIMARY_SOURCE_COLON,
    PRIMARY_SOURCE_DIGITS,
    SECONDARY_GLYPHS,
    PRIMARY_COLON_CELLS,
    PRIMARY_DIGIT_CELLS,
    PRIMARY_LINE_CELLS,
)  # noqa: E402

FINE_GLYPHS = SECONDARY_GLYPHS
COARSE_DIGITS = PRIMARY_SOURCE_DIGITS
COARSE_COLON = PRIMARY_SOURCE_COLON
SINGLE_GRID_PITCH = 3
SINGLE_GRID_LIT = 3
SINGLE_GRID_TIME_DIGIT_CELLS = PRIMARY_DIGIT_CELLS
SINGLE_GRID_TIME_COLON_CELLS = PRIMARY_COLON_CELLS
SINGLE_GRID_TIME_LINE_CELLS = PRIMARY_LINE_CELLS
TIME_DIGITS = PRIMARY_DIGITS
TIME_COLON = PRIMARY_COLON

# Weather sprites are eight fine cells square.  A dot is transparent; the
# other symbols are mapped to the fixed indexed-style palette by the
# generator.  Day/night sets intentionally differ only for clear and partly
# cloudy conditions; all other states reuse a truthful neutral sprite.
WEATHER_SPRITES = {
    "unknown": (
        "WWWWWWWW",
        "W......W",
        "W.W..W.W",
        "W...W..W",
        "W..W...W",
        "W......W",
        "W...W..W",
        "WWWWWWWW",
    ),
    "clear_day": (
        "...Y....",
        ".Y.Y.Y..",
        "Y..Y..Y.",
        "...Y....",
        "Y..Y..Y.",
        ".Y.Y.Y..",
        "...Y....",
        "........",
    ),
    "clear_night": (
        "...CCC..",
        "..CC....",
        ".CC.....",
        ".CC.....",
        ".CC.....",
        "..CC....",
        "...CCC..",
        "........",
    ),
    "partly_day": (
        "..Y.....",
        ".Y.Y....",
        "..Y..C..",
        "....CCC.",
        ".WWWWCCC",
        "WWWWWW..",
        ".BBBB...",
        "........",
    ),
    "partly_night": (
        "...CCC..",
        "..CC....",
        ".CC.....",
        ".CC..C..",
        ".WWWWCCC",
        "WWWWWW..",
        ".BBBB...",
        "........",
    ),
    "cloudy": (
        "........",
        "..WWWW..",
        ".WWWWWW.",
        "WWWWWWWW",
        ".WWWWWW.",
        "........",
        "........",
        "........",
    ),
    "fog": (
        "........",
        ".WWWWWW.",
        "........",
        "..WWWWWW",
        "........",
        ".WWWWWW.",
        "........",
        "........",
    ),
    "heavy_rain": (
        "........",
        "..WWWW..",
        ".WWWWWW.",
        "WWWWWWWW",
        ".WWWWWW.",
        "..B..B..",
        ".B..B...",
        "B..B....",
    ),
    "heavy_snow": (
        "........",
        "..WWWW..",
        ".WWWWWW.",
        "WWWWWWWW",
        ".WWWWWW.",
        "..C..C..",
        ".C..C...",
        "..C..C..",
    ),
    "rain": (
        "........",
        "..WWWW..",
        ".WWWWWW.",
        "WWWWWWWW",
        ".WWWWWW.",
        "..B..B..",
        "...B..B.",
        "........",
    ),
    "snow": (
        "........",
        "..WWWW..",
        ".WWWWWW.",
        "WWWWWWWW",
        ".WWWWWW.",
        "..C..C..",
        "...C..C.",
        "........",
    ),
    "thunderstorm": (
        "........",
        "..WWWW..",
        ".WWWWWW.",
        "WWWWWWWW",
        ".WWWYWW.",
        "..WY....",
        "..Y.....",
        "........",
    ),
    "sleet": (
        "........",
        "..WWWW..",
        ".WWWWWW.",
        "WWWWWWWW",
        ".WWWWWW.",
        "..B..C..",
        ".C..B...",
        "........",
    ),
    "windy": (
        "........",
        ".CCCCCC.",
        "........",
        "..BBBBBB",
        "........",
        ".CCCCCC.",
        "........",
        "........",
    ),
}

# WFF condition values, in the order defined by the v2 weather data source.
WEATHER_CONDITIONS = (
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

WEATHER_DAY_RESOLUTION = (
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

WEATHER_NIGHT_RESOLUTION = (
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


# Opaque colors are deliberately limited to the four visible weather entries
# in the product contract. The generator uses transparent pixels outside the
# selected direct-authored cells.
PALETTE = {
    "Y": (255, 216, 0, 255),    # #FFD800 yellow
    "C": (73, 223, 255, 255),   # #49DFFF pale cyan
    "B": (36, 116, 255, 255),   # #2474FF blue
    "W": (255, 255, 255, 255),  # white
}

# The stale marker is overlaid as a 6x6 corner detail inside the 48x48 weather
# tile. It is intentionally a two-cell diagonal rather than a text glyph so it
# remains legible without introducing a fifth color or a second sprite plane.
WEATHER_STALE = (
    "10",
    "01",
)
