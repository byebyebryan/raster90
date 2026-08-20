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
    PRIMARY_CLEAN_CHAMFER_DIGITS,
    PRIMARY_CONTENT_HEIGHT,
    PRIMARY_CONTENT_LEFT,
    PRIMARY_CONTENT_TOP,
    PRIMARY_CONTENT_WIDTH,
    PRIMARY_DIGIT_CELLS,
    PRIMARY_LEGACY_FINE_CHAMFER_DIGITS,
    PRIMARY_LINE_CELLS,
    PRIMARY_SQUARE_DIGITS,
    CLEAN_CHAMFER_ADDITIONS,
    CLEAN_CHAMFER_REMOVALS,
)


Matrix = tuple[str, ...]

CONTENT_LEFT: Final = PRIMARY_CONTENT_LEFT
CONTENT_TOP: Final = PRIMARY_CONTENT_TOP
CONTENT_WIDTH: Final = PRIMARY_CONTENT_WIDTH
CONTENT_HEIGHT: Final = PRIMARY_CONTENT_HEIGHT

SQUARE_DIGITS: Final[Mapping[str, Matrix]] = PRIMARY_SQUARE_DIGITS
CLEAN_CHAMFER_DIGITS: Final[Mapping[str, Matrix]] = PRIMARY_CLEAN_CHAMFER_DIGITS
LEGACY_FINE_CHAMFER_DIGITS: Final[Mapping[str, Matrix]] = (
    PRIMARY_LEGACY_FINE_CHAMFER_DIGITS
)

CANDIDATES: Final[Mapping[str, Mapping[str, Matrix]]] = {
    "clean-square": SQUARE_DIGITS,
    "clean-chamfer": CLEAN_CHAMFER_DIGITS,
    "legacy-fine-chamfer": LEGACY_FINE_CHAMFER_DIGITS,
}

CANDIDATE_LABELS: Final[Mapping[str, str]] = {
    "clean-square": "CLEAN SQUARE",
    "clean-chamfer": "CLEAN CHAMFER",
    "legacy-fine-chamfer": "LEGACY FINE CHAMFER",
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
        "legacy-fine-chamfer",
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
        for rows in CANDIDATES["legacy-fine-chamfer"].values()
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
