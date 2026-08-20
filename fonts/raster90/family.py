"""Authoritative project-owned Raster 90 bitmap font family.

The family has two optical cuts on the same solid source-cell grid:

* ``PRIMARY_DIGITS``/``PRIMARY_COLON`` are the dense fixed-width display cut.
  They are derived once from the reviewed 7x9 time silhouettes, expanded into
  their 26x32/10x32 boxes, then given the approved one-cell convex-corner
  chamfer.
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
PRIMARY_CHAMFER_PASSES: Final = 1
PRIMARY_COLON_DOT_CELLS: Final = 6


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


PRIMARY_DIGITS: Final[Mapping[str, Matrix]] = {
    digit: _chamfer_one_cell(
        _expand_source_matrix(rows, box_width=PRIMARY_DIGIT_CELLS)
    )
    for digit, rows in PRIMARY_SOURCE_DIGITS.items()
}
PRIMARY_COLON: Final[Matrix] = _primary_colon()


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

    if tuple(PRIMARY_DIGITS) != tuple("0123456789"):
        raise ValueError("primary display cut must contain exactly digits 0-9")
    for digit, rows in PRIMARY_DIGITS.items():
        _validate_matrix(f"primary/{digit}", rows, PRIMARY_DIGIT_CELLS, PRIMARY_LINE_CELLS)
    _validate_matrix("primary/colon", PRIMARY_COLON, PRIMARY_COLON_CELLS, PRIMARY_LINE_CELLS)
    _validate_plain_zero(PRIMARY_DIGITS["0"])

    # Colon dots are intentionally exactly two 6x6 blocks, aligned to the
    # center of their 10x32 fixed box, with no stray lit cells.
    expected_colon = _primary_colon()
    if PRIMARY_COLON != expected_colon:
        raise ValueError("primary colon dots drifted from the numeral stroke weight")
    if PRIMARY_TIME_WIDTH_CELLS != 114:
        raise ValueError("primary time geometry must remain 114 source cells")


validate_font_family()
