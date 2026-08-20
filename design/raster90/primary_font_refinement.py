"""Controlled primary-font refinements for Raster 90 design review.

The canonical runtime cut remains in ``fonts/raster90/family.py``. The study
preserves the 26x32 digit boxes, 10x32 colon, and solid 3x3 physical cells while
comparing the reviewed square construction with a minimally edited chamfered
cut authored directly on its 3x-expanded fine raster.
"""

from __future__ import annotations

from typing import Final, Mapping

from fonts.raster90.family import (
    PRIMARY_COLON,
    PRIMARY_DIGIT_CELLS,
    PRIMARY_DIGITS,
    PRIMARY_LINE_CELLS,
    PRIMARY_SOURCE_DIGITS,
    _expand_source_matrix,
)


Matrix = tuple[str, ...]
Coordinate = tuple[int, int]

CONTENT_LEFT: Final = (PRIMARY_DIGIT_CELLS - 7 * 3) // 2
CONTENT_TOP: Final = (PRIMARY_LINE_CELLS - 9 * 3) // 2
CONTENT_WIDTH: Final = 7 * 3
CONTENT_HEIGHT: Final = 9 * 3


def _square_digits() -> Mapping[str, Matrix]:
    return {
        digit: _expand_source_matrix(
            rows,
            box_width=PRIMARY_DIGIT_CELLS,
        )
        for digit, rows in PRIMARY_SOURCE_DIGITS.items()
    }


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


def _clean_chamfer(square_digits: Mapping[str, Matrix]) -> Mapping[str, Matrix]:
    """Apply the reviewed fine-raster edits without changing the skeleton."""

    digits: dict[str, Matrix] = {}
    for digit, square in square_digits.items():
        rows = [list(row) for row in square]
        for x, y in CLEAN_CHAMFER_ADDITIONS[digit]:
            rows[CONTENT_TOP + y][CONTENT_LEFT + x] = "1"
        for x, y in CLEAN_CHAMFER_REMOVALS.get(digit, ()):
            rows[CONTENT_TOP + y][CONTENT_LEFT + x] = "0"
        digits[digit] = tuple("".join(row) for row in rows)
    return digits


SQUARE_DIGITS: Final[Mapping[str, Matrix]] = _square_digits()

CANDIDATES: Final[Mapping[str, Mapping[str, Matrix]]] = {
    "clean-square": SQUARE_DIGITS,
    "clean-chamfer": _clean_chamfer(SQUARE_DIGITS),
    "current-fine-chamfer": PRIMARY_DIGITS,
}

CANDIDATE_LABELS: Final[Mapping[str, str]] = {
    "clean-square": "CLEAN SQUARE",
    "clean-chamfer": "CLEAN CHAMFER",
    "current-fine-chamfer": "CURRENT FINE CHAMFER",
}


def _uses_only_complete_macro_cells(rows: Matrix) -> bool:
    """Return whether the centered 7x9 construction cells remain whole 3x3s."""

    left = (PRIMARY_DIGIT_CELLS - 7 * 3) // 2
    top = (PRIMARY_LINE_CELLS - 9 * 3) // 2
    for macro_y in range(9):
        for macro_x in range(7):
            cells = {
                rows[top + macro_y * 3 + y][left + macro_x * 3 + x]
                for y in range(3)
                for x in range(3)
            }
            if len(cells) != 1:
                return False
    return True


def _has_single_cell_tip(rows: Matrix) -> bool:
    """Detect lit cells with fewer than two orthogonally connected neighbors."""

    height = len(rows)
    width = len(rows[0])
    for y, row in enumerate(rows):
        for x, symbol in enumerate(row):
            if symbol != "1":
                continue
            neighbors = sum(
                0 <= adjacent_x < width
                and 0 <= adjacent_y < height
                and rows[adjacent_y][adjacent_x] == "1"
                for adjacent_x, adjacent_y in (
                    (x - 1, y),
                    (x + 1, y),
                    (x, y - 1),
                    (x, y + 1),
                )
            )
            if neighbors < 2:
                return True
    return False


def validate_primary_refinement() -> None:
    if tuple(CANDIDATES) != (
        "clean-square",
        "clean-chamfer",
        "current-fine-chamfer",
    ):
        raise ValueError("primary refinement candidate order drifted")
    for candidate, digits in CANDIDATES.items():
        if tuple(digits) != tuple("0123456789"):
            raise ValueError(f"{candidate}: expected exactly digits 0-9")
        for digit, rows in digits.items():
            if len(rows) != PRIMARY_LINE_CELLS:
                raise ValueError(f"{candidate}/{digit}: wrong height")
            if any(len(row) != PRIMARY_DIGIT_CELLS for row in rows):
                raise ValueError(f"{candidate}/{digit}: wrong width")
            if any(set(row) - {"0", "1"} for row in rows):
                raise ValueError(f"{candidate}/{digit}: invalid matrix symbol")

    if not all(
        _uses_only_complete_macro_cells(rows)
        for rows in CANDIDATES["clean-square"].values()
    ):
        raise ValueError("clean-square: contains a partial 3x3 construction cell")

    if all(
        _uses_only_complete_macro_cells(rows)
        for rows in CANDIDATES["current-fine-chamfer"].values()
    ):
        raise ValueError("control unexpectedly contains no fine-cell corner cuts")
    chamfered = CANDIDATES["clean-chamfer"]
    square = CANDIDATES["clean-square"]
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
                if not (0 <= x < CONTENT_WIDTH and 0 <= y < CONTENT_HEIGHT):
                    raise ValueError(f"clean chamfer {digit}: edit outside content")
                if square[digit][CONTENT_TOP + y][CONTENT_LEFT + x] != value:
                    raise ValueError(f"clean chamfer {digit}: edit does not change square")

    if {digit for digit in square if chamfered[digit] != square[digit]} != set(
        "0123456789"
    ):
        raise ValueError("clean chamfer must contain the complete reviewed edit set")
    if any(_has_single_cell_tip(rows) for rows in chamfered.values()):
        raise ValueError("clean chamfer contains a single-cell extrusion")

    two = chamfered["2"]
    diagonal_starts = [two[y].index("1") for y in range(9, 23)]
    if diagonal_starts != list(range(16, 2, -1)):
        raise ValueError("digit 2 diagonal does not follow one straight line")
    if any(two[y].count("1") != 6 for y in range(9, 23)):
        raise ValueError("digit 2 diagonal stroke weight drifted")

    seven = chamfered["7"]
    diagonal_starts = [seven[y].index("1") for y in range(6, 18)]
    if diagonal_starts != list(range(16, 4, -1)):
        raise ValueError("digit 7 diagonal does not follow one straight line")
    if any(seven[y].count("1") != 6 for y in range(6, 18)):
        raise ValueError("digit 7 diagonal stroke weight drifted")

    if len(PRIMARY_COLON) != PRIMARY_LINE_CELLS:
        raise ValueError("shared primary colon height drifted")


validate_primary_refinement()
