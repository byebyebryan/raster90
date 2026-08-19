"""Human-readable Raster 90 bitmap matrices.

The matrices describe source cells, not display pixels. The asset generator
expands each lit cell into an exact solid square. Keeping these definitions as
plain strings makes a glyph or sprite reviewable without an image editor.
"""

from __future__ import annotations

from typing import Sequence

# Fine information plane: five columns by seven rows for ordinary glyphs.
# Each source cell is expanded by the selected runtime generator to the single
# 3-unit pitch with a solid 3x3 illuminated square. The generator gives every
# ordinary glyph a six-cell advance by adding one empty column to the image
# width; the literal space is deliberately only two source cells wide.
FINE_GLYPHS = {
    " ": (
        "00",
        "00",
        "00",
        "00",
        "00",
        "00",
        "00",
    ),
    "+": (
        "00100",
        "00100",
        "00100",
        "11111",
        "00100",
        "00100",
        "00100",
    ),
    "-": (
        "00000",
        "00000",
        "00000",
        "11111",
        "00000",
        "00000",
        "00000",
    ),
    "%": (
        "11001",
        "11010",
        "00000",
        "00100",
        "00000",
        "01011",
        "10011",
    ),
    "°": (
        "01110",
        "10001",
        "10001",
        "01110",
        "00000",
        "00000",
        "00000",
    ),
    "?": (
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "00000",
        "00100",
    ),
    "0": (
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ),
    "1": (
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110",
    ),
    "2": (
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "01000",
        "11111",
    ),
    "3": (
        "11110",
        "00001",
        "00001",
        "01110",
        "00001",
        "00001",
        "11110",
    ),
    "4": (
        "10010",
        "10010",
        "10010",
        "11111",
        "00010",
        "00010",
        "00010",
    ),
    "5": (
        "11111",
        "10000",
        "10000",
        "11110",
        "00001",
        "00001",
        "11110",
    ),
    "6": (
        "01110",
        "10000",
        "10000",
        "11110",
        "10001",
        "10001",
        "01110",
    ),
    "7": (
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000",
    ),
    "8": (
        "01110",
        "10001",
        "10001",
        "01110",
        "10001",
        "10001",
        "01110",
    ),
    "9": (
        "01110",
        "10001",
        "10001",
        "01111",
        "00001",
        "00001",
        "01110",
    ),
    "A": (
        "01110",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ),
    "B": (
        "11110",
        "10001",
        "10001",
        "11110",
        "10001",
        "10001",
        "11110",
    ),
    "C": (
        "01111",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "01111",
    ),
    "D": (
        "11110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "11110",
    ),
    "E": (
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "11111",
    ),
    "F": (
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "10000",
    ),
    "G": (
        "01111",
        "10000",
        "10000",
        "10111",
        "10001",
        "10001",
        "01111",
    ),
    "H": (
        "10001",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ),
    "I": (
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "11111",
    ),
    "J": (
        "00111",
        "00010",
        "00010",
        "00010",
        "10010",
        "10010",
        "01100",
    ),
    "K": (
        "10001",
        "10010",
        "10100",
        "11000",
        "10100",
        "10010",
        "10001",
    ),
    "L": (
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "11111",
    ),
    "M": (
        "10001",
        "11011",
        "10101",
        "10101",
        "10001",
        "10001",
        "10001",
    ),
    "N": (
        "10001",
        "11001",
        "10101",
        "10011",
        "10001",
        "10001",
        "10001",
    ),
    "O": (
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ),
    "P": (
        "11110",
        "10001",
        "10001",
        "11110",
        "10000",
        "10000",
        "10000",
    ),
    "Q": (
        "01110",
        "10001",
        "10001",
        "10001",
        "10101",
        "10010",
        "01101",
    ),
    "R": (
        "11110",
        "10001",
        "10001",
        "11110",
        "10100",
        "10010",
        "10001",
    ),
    "S": (
        "01111",
        "10000",
        "10000",
        "01110",
        "00001",
        "00001",
        "11110",
    ),
    "T": (
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
    ),
    "U": (
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ),
    "V": (
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01010",
        "00100",
    ),
    "W": (
        "10001",
        "10001",
        "10101",
        "10101",
        "10101",
        "11011",
        "10001",
    ),
    "X": (
        "10001",
        "01010",
        "00100",
        "00100",
        "00100",
        "01010",
        "10001",
    ),
    "Y": (
        "10001",
        "01010",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
    ),
    "Z": (
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "10000",
        "11111",
    ),
}

# Reviewed V1 time silhouettes: seven columns by nine rows.  These matrices are
# retained as source art for the post-V1 expanded 26x32/10x32 candidate below;
# they are not a second physical runtime raster.
COARSE_DIGITS = {
    "0": (
        "0111110",
        "1100011",
        "1100011",
        "1100011",
        "1100011",
        "1100011",
        "1100011",
        "1100011",
        "0111110",
    ),
    "1": (
        "0011000",
        "0111000",
        "0011000",
        "0011000",
        "0011000",
        "0011000",
        "0011000",
        "0011000",
        "1111111",
    ),
    "2": (
        "0111110",
        "1100011",
        "0000011",
        "0000110",
        "0001100",
        "0011000",
        "0110000",
        "1100000",
        "1111111",
    ),
    "3": (
        "1111110",
        "0000011",
        "0000011",
        "0000110",
        "0011110",
        "0000011",
        "0000011",
        "0000011",
        "1111110",
    ),
    "4": (
        "0001100",
        "0011100",
        "0111100",
        "1101100",
        "1101100",
        "1111111",
        "0001100",
        "0001100",
        "0001100",
    ),
    "5": (
        "1111111",
        "1100000",
        "1100000",
        "1111110",
        "0000011",
        "0000011",
        "0000011",
        "1100011",
        "0111110",
    ),
    "6": (
        "0011110",
        "0110000",
        "1100000",
        "1100000",
        "1111110",
        "1100011",
        "1100011",
        "1100011",
        "0111110",
    ),
    "7": (
        "1111111",
        "0000011",
        "0000110",
        "0001100",
        "0011000",
        "0110000",
        "0110000",
        "0110000",
        "0110000",
    ),
    "8": (
        "0111110",
        "1100011",
        "1100011",
        "0111110",
        "1100011",
        "1100011",
        "1100011",
        "1100011",
        "0111110",
    ),
    "9": (
        "0111110",
        "1100011",
        "1100011",
        "1100011",
        "0111111",
        "0000011",
        "0000011",
        "0000110",
        "0111100",
    ),
}

COARSE_COLON = (
    "000",
    "000",
    "110",
    "110",
    "000",
    "000",
    "110",
    "110",
    "000",
)

# Post-V1 single-grid time resources. The source silhouettes remain the reviewed
# V1 7x9 matrices above; they are expanded onto the one approved physical
# raster so the packaged face never introduces a second pixel tier. Their
# authorship remains provisional for the selected solid-grid pass.
SINGLE_GRID_PITCH = 3
SINGLE_GRID_LIT = 3
SINGLE_GRID_TIME_DIGIT_CELLS = 26
SINGLE_GRID_TIME_COLON_CELLS = 10
SINGLE_GRID_TIME_LINE_CELLS = 32


def _expand_single_grid_time(
    rows: Sequence[str], *, box_width: int, box_height: int = SINGLE_GRID_TIME_LINE_CELLS
) -> tuple[str, ...]:
    """Center a reviewed V1 time silhouette in a solid-grid source box."""

    factor = 3
    expanded_rows: list[str] = []
    for row in rows:
        expanded = "".join(symbol * factor for symbol in row)
        expanded_rows.extend(expanded for _copy in range(factor))
    content_width = len(expanded_rows[0])
    content_height = len(expanded_rows)
    if content_width > box_width or content_height > box_height:
        raise ValueError("single-grid time silhouette exceeds its line box")
    left = (box_width - content_width) // 2
    top = (box_height - content_height) // 2
    output = [["0" for _x in range(box_width)] for _y in range(box_height)]
    for y, row in enumerate(expanded_rows):
        for x, symbol in enumerate(row):
            output[top + y][left + x] = symbol
    return tuple("".join(row) for row in output)


TIME_DIGITS = {
    digit: _expand_single_grid_time(rows, box_width=SINGLE_GRID_TIME_DIGIT_CELLS)
    for digit, rows in COARSE_DIGITS.items()
}
TIME_COLON = _expand_single_grid_time(
    COARSE_COLON, box_width=SINGLE_GRID_TIME_COLON_CELLS
)

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
