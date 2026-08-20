"""Authoritative project-owned Raster 90 bitmap font family.

The family has two optical cuts on the same solid source-cell grid, plus a
retained legacy control:

* ``PRIMARY_SQUARE_DIGITS`` is the unmodified square construction from the
  reviewed 7x9 time silhouettes.
* ``PRIMARY_CLEAN_CHAMFER_DIGITS`` is the reviewed fine-raster optical cut.
  ``PRIMARY_DIGITS`` aliases this mapping as the stable selected-runtime API.
* ``PRIMARY_LEGACY_FINE_CHAMFER_DIGITS`` retains the earlier algorithmic
  one-cell/global chamfer as a clearly named comparison control.
* ``SECONDARY_GLYPHS`` is the complete 5x7 text cut.  Its runtime subset is
  deliberately selected by the asset generator; the source vocabulary stays
  complete here for review sheets and future source-only composition work.

This module lives with the tracked font component rather than the exploratory
design studies. Runtime generators consume it directly; do not duplicate glyph
matrices under ``design/`` or the Android resource module.

Rows contain source cells (``1`` is lit and ``0`` is unlit), not physical
pixels.  The WFF generator expands each cell to one solid 3x3 square.
"""

from __future__ import annotations

from typing import Final, Mapping, Sequence


Matrix = tuple[str, ...]
Coordinate = tuple[int, int]

SECONDARY_SYMBOLS: Final[tuple[str, ...]] = ("+", "-", "%", "°", "?")
SECONDARY_PUNCTUATION: Final[tuple[str, ...]] = (
    ".",
    ",",
    ":",
    ";",
    "!",
    "'",
    '"',
    "/",
    "(",
    ")",
    "#",
    "&",
    "=",
    "_",
)
SECONDARY_KEYS: Final[tuple[str, ...]] = (
    (" ",)
    + SECONDARY_SYMBOLS
    + tuple("0123456789")
    + tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    + tuple("abcdefghijklmnopqrstuvwxyz")
    + SECONDARY_PUNCTUATION
)

# Runtime WFF expressions currently emit space, minus, percent, degree, all
# decimal digits, and uppercase Latin (date names).  The complete design
# vocabulary above remains source-only until a runtime field needs it.
RUNTIME_SECONDARY_KEYS: Final[tuple[str, ...]] = (
    (" ", "-", "%", "°")
    + tuple("0123456789")
    + tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
)


SECONDARY_GLYPHS: Final[Mapping[str, Matrix]] = {
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
    # Lowercase and punctuation begin at the baseline, following the reviewed
    # source-only proposal.  Ascenders/descenders remain visible in this
    # intentionally compact 7-row text cut.
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "10110", "11001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01111", "10000", "10000", "10000", "01111"),
    "d": ("00001", "00001", "01101", "10011", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01111"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "10110", "11001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "10110", "11001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "11110", "10001", "10001", "11110", "10000", "10000"),
    "q": ("00000", "01111", "10001", "10001", "01111", "00001", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11110", "01000", "01000", "01001", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "10001", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    ".": ("00000", "00000", "00000", "00000", "00000", "00000", "00100"),
    ",": ("00000", "00000", "00000", "00000", "00000", "00100", "01000"),
    ":": ("00000", "00100", "00100", "00000", "00100", "00100", "00000"),
    ";": ("00000", "00100", "00100", "00000", "00100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "10100", "00000", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "#": ("01010", "11111", "01010", "01010", "11111", "01010", "01010"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "=": ("00000", "11111", "00000", "11111", "00000", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
}

RUNTIME_SECONDARY_GLYPHS: Final[Mapping[str, Matrix]] = {
    character: SECONDARY_GLYPHS[character] for character in RUNTIME_SECONDARY_KEYS
}


# Reviewed V1 7x9 display silhouettes.  These are source art for the primary
# cut only; they are not packaged as a second physical raster.
PRIMARY_SOURCE_DIGITS: Final[Mapping[str, Matrix]] = {
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

PRIMARY_SOURCE_COLON: Final[Matrix] = (
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

PRIMARY_DIGIT_CELLS: Final = 26
PRIMARY_COLON_CELLS: Final = 10
PRIMARY_LINE_CELLS: Final = 32
PRIMARY_TIME_WIDTH_CELLS: Final = 4 * PRIMARY_DIGIT_CELLS + PRIMARY_COLON_CELLS
# The old global algorithm remains available only as the named comparison
# control below. Keep the historical constant as a compatibility alias.
PRIMARY_LEGACY_CHAMFER_PASSES: Final = 1
PRIMARY_CHAMFER_PASSES: Final = PRIMARY_LEGACY_CHAMFER_PASSES
PRIMARY_COLON_DOT_CELLS: Final = 6
PRIMARY_CONTENT_LEFT: Final = (PRIMARY_DIGIT_CELLS - 7 * 3) // 2
PRIMARY_CONTENT_TOP: Final = (PRIMARY_LINE_CELLS - 9 * 3) // 2
PRIMARY_CONTENT_WIDTH: Final = 7 * 3
PRIMARY_CONTENT_HEIGHT: Final = 9 * 3


def _expand_source_matrix(
    rows: Sequence[str], *, box_width: int, box_height: int = PRIMARY_LINE_CELLS
) -> Matrix:
    """Expand a reviewed 7x9 silhouette by three and center it in its box."""

    expanded_rows: list[str] = []
    for row in rows:
        expanded = "".join(symbol * 3 for symbol in row)
        expanded_rows.extend(expanded for _copy in range(3))
    content_width = len(expanded_rows[0])
    content_height = len(expanded_rows)
    if content_width > box_width or content_height > box_height:
        raise ValueError("primary source silhouette exceeds its line box")
    left = (box_width - content_width) // 2
    top = (box_height - content_height) // 2
    output = [["0" for _x in range(box_width)] for _y in range(box_height)]
    for y, row in enumerate(expanded_rows):
        for x, symbol in enumerate(row):
            output[top + y][left + x] = symbol
    return tuple("".join(row) for row in output)


def _chamfer_one_cell(rows: Matrix) -> Matrix:
    """Remove one cell from each convex outer corner of a binary matrix."""

    mask = [[symbol == "1" for symbol in row] for row in rows]
    height = len(mask)
    width = len(mask[0])

    def lit(source: Sequence[Sequence[bool]], x: int, y: int) -> bool:
        return 0 <= x < width and 0 <= y < height and source[y][x]

    previous = [row[:] for row in mask]
    for y in range(height):
        for x in range(width):
            if not previous[y][x]:
                continue
            up = lit(previous, x, y - 1)
            down = lit(previous, x, y + 1)
            left = lit(previous, x - 1, y)
            right = lit(previous, x + 1, y)
            convex = (
                (not up and not left and down and right)
                or (not up and not right and down and left)
                or (not down and not left and up and right)
                or (not down and not right and up and left)
            )
            if convex:
                mask[y][x] = False
    return tuple("".join("1" if cell else "0" for cell in row) for row in mask)


def _primary_colon() -> Matrix:
    """Build two 6x6 source-cell dots with the numeral stroke's mass."""

    rows = [["0" for _x in range(PRIMARY_COLON_CELLS)] for _y in range(PRIMARY_LINE_CELLS)]
    left = (PRIMARY_COLON_CELLS - PRIMARY_COLON_DOT_CELLS) // 2
    for top in (8, 20):
        for y in range(top, top + PRIMARY_COLON_DOT_CELLS):
            for x in range(left, left + PRIMARY_COLON_DOT_CELLS):
                rows[y][x] = "1"
    return tuple("".join(row) for row in rows)


# The reviewed chamfer was authored against the 21x27 fine raster inside each
# 26x32 digit box.  Keep these edits here with the canonical source matrices;
# design studies import them rather than carrying a second source of truth.
CLEAN_CHAMFER_ADDITIONS: Final[Mapping[str, tuple[Coordinate, ...]]] = {
    "0": (
        (2, 1), (18, 1),
        (1, 2), (2, 2), (18, 2), (19, 2),
        (1, 24), (2, 24), (18, 24), (19, 24),
        (2, 25), (18, 25),
    ),
    "1": ((5, 1), (4, 2), (5, 2)),
    "2": (
        (2, 1), (18, 1),
        (1, 2), (2, 2), (18, 2), (19, 2),
        (14, 7), (13, 8), (14, 8),
        (11, 10), (10, 11), (11, 11),
        (8, 13), (7, 14), (8, 14),
        (5, 16), (4, 17), (5, 17),
        (2, 19), (1, 20), (2, 20),
    ),
    "3": (
        (18, 1), (18, 2), (19, 2),
        (18, 9), (19, 9), (18, 10),
        (18, 13), (18, 14), (19, 14),
        (18, 24), (19, 24), (18, 25),
    ),
    "4": (
        (8, 1), (7, 2), (8, 2),
        (5, 4), (4, 5), (5, 5),
        (2, 7), (1, 8), (2, 8),
    ),
    "5": (
        (18, 10), (18, 11), (19, 11),
        (6, 22), (6, 23), (7, 23),
        (1, 24), (2, 24), (18, 24), (19, 24),
        (2, 25), (18, 25),
    ),
    "6": (
        (5, 1), (4, 2), (5, 2),
        (2, 4), (1, 5), (2, 5),
        (18, 13), (18, 14), (19, 14),
        (1, 24), (2, 24), (18, 24), (19, 24),
        (2, 25), (18, 25),
    ),
    "7": (
        (14, 4), (13, 5), (14, 5),
        (11, 7), (10, 8), (11, 8),
        (8, 10), (7, 11), (8, 11),
        (5, 13), (4, 14), (5, 14),
    ),
    "8": (
        (2, 1), (18, 1),
        (1, 2), (2, 2), (18, 2), (19, 2),
        (1, 9), (2, 9), (18, 9), (19, 9),
        (2, 10), (18, 10),
        (1, 11), (2, 11), (18, 11), (19, 11),
        (1, 24), (2, 24), (18, 24), (19, 24),
        (2, 25), (18, 25),
    ),
    "9": (
        (2, 1), (18, 1),
        (1, 2), (2, 2), (18, 2), (19, 2),
        (1, 12), (2, 12), (2, 13),
        (18, 21), (19, 21), (18, 22),
        (15, 24), (16, 24), (15, 25),
    ),
}

CLEAN_CHAMFER_REMOVALS: Final[Mapping[str, tuple[Coordinate, ...]]] = {
    "2": (
        (5, 4), (4, 5), (5, 5),
        (20, 7), (19, 8), (20, 8),
        (17, 10), (16, 11), (17, 11),
        (14, 13), (13, 14), (14, 14),
        (11, 16), (10, 17), (11, 17),
        (8, 19), (7, 20), (8, 20),
    ),
    "3": ((12, 9), (13, 9), (12, 10)),
    "6": ((8, 4), (7, 5), (8, 5)),
    "7": (
        (20, 4), (19, 5), (20, 5),
        (17, 7), (16, 8), (17, 8),
        (14, 10), (13, 11), (14, 11),
        (11, 13), (10, 14), (11, 14),
    ),
    "9": ((12, 21), (13, 21), (12, 22)),
}


def _apply_clean_chamfer(square_digits: Mapping[str, Matrix]) -> Mapping[str, Matrix]:
    """Apply the reviewed fine-raster edits without changing the skeleton."""

    digits: dict[str, Matrix] = {}
    for digit, square in square_digits.items():
        rows = [list(row) for row in square]
        for x, y in CLEAN_CHAMFER_ADDITIONS[digit]:
            rows[PRIMARY_CONTENT_TOP + y][PRIMARY_CONTENT_LEFT + x] = "1"
        for x, y in CLEAN_CHAMFER_REMOVALS.get(digit, ()):
            rows[PRIMARY_CONTENT_TOP + y][PRIMARY_CONTENT_LEFT + x] = "0"
        digits[digit] = tuple("".join(row) for row in rows)
    return digits


PRIMARY_SQUARE_DIGITS: Final[Mapping[str, Matrix]] = {
    digit: _expand_source_matrix(rows, box_width=PRIMARY_DIGIT_CELLS)
    for digit, rows in PRIMARY_SOURCE_DIGITS.items()
}
PRIMARY_CLEAN_CHAMFER_DIGITS: Final[Mapping[str, Matrix]] = _apply_clean_chamfer(
    PRIMARY_SQUARE_DIGITS
)
PRIMARY_LEGACY_FINE_CHAMFER_DIGITS: Final[Mapping[str, Matrix]] = {
    digit: _chamfer_one_cell(rows)
    for digit, rows in PRIMARY_SQUARE_DIGITS.items()
}

PRIMARY_SQUARE_COLON: Final[Matrix] = _primary_colon()
PRIMARY_CLEAN_CHAMFER_COLON: Final[Matrix] = PRIMARY_SQUARE_COLON
PRIMARY_LEGACY_FINE_CHAMFER_COLON: Final[Matrix] = PRIMARY_SQUARE_COLON

PRIMARY_DIGIT_VARIANTS: Final[Mapping[str, Mapping[str, Matrix]]] = {
    "square": PRIMARY_SQUARE_DIGITS,
    "clean-chamfer": PRIMARY_CLEAN_CHAMFER_DIGITS,
    "legacy-fine-chamfer": PRIMARY_LEGACY_FINE_CHAMFER_DIGITS,
}
PRIMARY_COLON_VARIANTS: Final[Mapping[str, Matrix]] = {
    "square": PRIMARY_SQUARE_COLON,
    "clean-chamfer": PRIMARY_CLEAN_CHAMFER_COLON,
    "legacy-fine-chamfer": PRIMARY_LEGACY_FINE_CHAMFER_COLON,
}

# Stable selected-runtime aliases.  Generator consumers intentionally import
# these names directly so changing a review-only variant never changes the
# WFF resource surface implicitly.
PRIMARY_DIGITS: Final[Mapping[str, Matrix]] = PRIMARY_CLEAN_CHAMFER_DIGITS
PRIMARY_COLON: Final[Matrix] = PRIMARY_CLEAN_CHAMFER_COLON


def _validate_matrix(name: str, rows: Sequence[str], width: int, height: int) -> None:
    if len(rows) != height:
        raise ValueError(f"{name}: expected {height} rows, got {len(rows)}")
    for row in rows:
        if len(row) != width:
            raise ValueError(f"{name}: expected {width} columns, got {len(row)}")
        if set(row) - {"0", "1"}:
            raise ValueError(f"{name}: matrix must contain only 0 and 1 cells")


def _validate_plain_zero(rows: Matrix) -> None:
    # A plain closed zero has an uninterrupted hollow interior: no slash,
    # dash, or isolated mark can appear inside the side strokes.
    # The expanded side strokes are six cells wide at x=2..7 and x=17..22;
    # leave those shared stroke cells out of the hollow check.
    interior = [row[8:17] for row in rows[8:-8]]
    if any("1" in row for row in interior):
        raise ValueError("primary zero must remain plain and closed")
    if not any("1" in row for row in rows[:8]) or not any("1" in row for row in rows[-8:]):
        raise ValueError("primary zero must have closed top and bottom strokes")


def validate_font_family() -> None:
    """Validate the complete source family and fixed primary geometry."""

    if tuple(SECONDARY_GLYPHS) != SECONDARY_KEYS:
        raise ValueError("secondary glyph keys drifted from the complete vocabulary")
    if len(set(SECONDARY_KEYS)) != len(SECONDARY_KEYS):
        raise ValueError("secondary glyph vocabulary contains duplicate keys")
    if any(character not in SECONDARY_GLYPHS for character in RUNTIME_SECONDARY_KEYS):
        raise ValueError("runtime secondary subset is not contained in the full family")
    for character, rows in SECONDARY_GLYPHS.items():
        _validate_matrix(
            f"secondary/{character!r}",
            rows,
            2 if character == " " else 5,
            7,
        )

    expected_variants = ("square", "clean-chamfer", "legacy-fine-chamfer")
    if tuple(PRIMARY_DIGIT_VARIANTS) != expected_variants:
        raise ValueError("primary variant order drifted")
    if tuple(PRIMARY_COLON_VARIANTS) != expected_variants:
        raise ValueError("primary colon variant order drifted")
    for variant, digits in PRIMARY_DIGIT_VARIANTS.items():
        if tuple(digits) != tuple("0123456789"):
            raise ValueError(f"primary/{variant} must contain exactly digits 0-9")
        for digit, rows in digits.items():
            _validate_matrix(
                f"primary/{variant}/{digit}",
                rows,
                PRIMARY_DIGIT_CELLS,
                PRIMARY_LINE_CELLS,
            )
        _validate_plain_zero(digits["0"])
    for variant, rows in PRIMARY_COLON_VARIANTS.items():
        _validate_matrix(
            f"primary/{variant}/colon",
            rows,
            PRIMARY_COLON_CELLS,
            PRIMARY_LINE_CELLS,
        )

    if PRIMARY_DIGITS is not PRIMARY_CLEAN_CHAMFER_DIGITS:
        raise ValueError("PRIMARY_DIGITS must alias the reviewed clean chamfer")
    if PRIMARY_COLON is not PRIMARY_CLEAN_CHAMFER_COLON:
        raise ValueError("PRIMARY_COLON must alias the reviewed clean chamfer")

    if tuple(CLEAN_CHAMFER_ADDITIONS) != tuple("0123456789"):
        raise ValueError("clean chamfer additions must cover digits 0-9 in order")
    if set(CLEAN_CHAMFER_REMOVALS) - set(CLEAN_CHAMFER_ADDITIONS):
        raise ValueError("clean chamfer removals contain an unknown digit")
    for digit, additions in CLEAN_CHAMFER_ADDITIONS.items():
        removals = CLEAN_CHAMFER_REMOVALS.get(digit, ())
        if len(set(additions)) != len(additions) or len(set(removals)) != len(removals):
            raise ValueError(f"clean chamfer {digit}: duplicate edit coordinate")
        if set(additions) & set(removals):
            raise ValueError(f"clean chamfer {digit}: conflicting edit coordinate")
        for value, coordinates in (("0", additions), ("1", removals)):
            for x, y in coordinates:
                if not (
                    0 <= x < PRIMARY_CONTENT_WIDTH
                    and 0 <= y < PRIMARY_CONTENT_HEIGHT
                ):
                    raise ValueError(f"clean chamfer {digit}: edit outside content")
                if (
                    PRIMARY_SQUARE_DIGITS[digit][PRIMARY_CONTENT_TOP + y][
                        PRIMARY_CONTENT_LEFT + x
                    ]
                    != value
                ):
                    raise ValueError(
                        f"clean chamfer {digit}: edit does not change square"
                    )
    if {
        digit
        for digit in PRIMARY_SQUARE_DIGITS
        if PRIMARY_CLEAN_CHAMFER_DIGITS[digit] != PRIMARY_SQUARE_DIGITS[digit]
    } != set("0123456789"):
        raise ValueError("clean chamfer must contain the complete reviewed edit set")

    # Legacy is intentionally a separate control, not an accidental runtime
    # alias. It should retain at least one fine-cell corner cut.
    if all(
        all(
            len(
                {
                    rows[PRIMARY_CONTENT_TOP + macro_y * 3 + y][
                        PRIMARY_CONTENT_LEFT + macro_x * 3 + x
                    ]
                    for y in range(3)
                    for x in range(3)
                }
            )
            == 1
            for macro_y in range(9)
            for macro_x in range(7)
        )
        for rows in PRIMARY_LEGACY_FINE_CHAMFER_DIGITS.values()
    ):
        raise ValueError("legacy fine chamfer unexpectedly contains no fine-cell cuts")

    # Colon dots are intentionally exactly two 6x6 blocks, aligned to the
    # center of their 10x32 fixed box, with no stray lit cells.
    expected_colon = _primary_colon()
    if any(rows != expected_colon for rows in PRIMARY_COLON_VARIANTS.values()):
        raise ValueError("primary colon dots drifted from the numeral stroke weight")
    if PRIMARY_TIME_WIDTH_CELLS != 114:
        raise ValueError("primary time geometry must remain 114 source cells")


validate_font_family()
