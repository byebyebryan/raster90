"""Reviewable true-16x16 outline candidates for the Raster 90 step icon.

This study retains the pre-promotion solid Footprints B matrix as a historical
control while the approved vertical-big-toe candidate is imported from the
canonical runtime family.  The study remains design evidence; the generator
binds the selected icon directly from ``icons/raster90/family.py``.
"""

from __future__ import annotations

from typing import Final, Mapping

from icons.raster90.family import APPROVED_STEP_ICON


Matrix = tuple[str, ...]

# Historical Footprints B control from before the outline promotion. Keep this
# literal in the study so its comparison remains stable and cannot silently
# become the selected runtime icon.
SOLID_CONTROL: Final[Matrix] = (
    ".........11.1...",
    ".........11...1.",
    "...1.11.........",
    ".1...11..11111..",
    ".........111111.",
    "..11111..111111.",
    ".111111..11111..",
    ".111111..11111..",
    ".11111....1111..",
    "..1111....111...",
    "..1111....111...",
    "...111....111...",
    "...111..........",
    "...111..........",
    "................",
    "................",
)

# Preserve the selected footprint placement and solid toe pads, but hollow each
# sole into a continuous one-cell contour.
CLOSED_OUTLINE: Final[Matrix] = (
    ".........11.1...",
    ".........11...1.",
    "...1.11.........",
    ".1...11..11111..",
    ".........1....1.",
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

# Open the inner arch of each closed contour.  The outside edge and heel stay
# intact, reducing weight without fragmenting the footprint into separate pads.
OPEN_ARCH_OUTLINE: Final[Matrix] = (
    ".........11.1...",
    ".........11...1.",
    "...1.11.........",
    ".1...11..11111..",
    ".........1....1.",
    "..11111..1....1.",
    ".1....1..1...1..",
    ".1....1......1..",
    ".1........1..1..",
    "..1.......1.1...",
    "..1.......1.1...",
    "...1.1....111...",
    "...1.1..........",
    "...111..........",
    "................",
    "................",
)

# Treat each sole as a separated forefoot and heel print.  This is the most
# literal footprint construction and the closest in density to the battery
# outline, but intentionally departs further from the current continuous sole.
SEGMENTED_OUTLINE: Final[Matrix] = (
    ".........11.1...",
    ".........11...1.",
    "...1.11.........",
    ".1...11..11111..",
    ".........1....1.",
    "..11111..1....1.",
    ".1....1..11111..",
    ".1....1.........",
    "..1111....111...",
    "..........1.1...",
    "...111....1.1...",
    "...1.1....111...",
    "...1.1..........",
    "...111..........",
    "................",
    "................",
)

# Hollow only the broad forefoot and leave the tapered arch/heel solid.  This
# hybrid preserves more of Footprints B's readable mass while substantially
# reducing the top-heavy block of each sole.
HOLLOW_FOREFOOT: Final[Matrix] = (
    ".........11.1...",
    ".........11...1.",
    "...1.11.........",
    ".1...11..11111..",
    ".........1....1.",
    "..11111..1....1.",
    ".1....1..1...1..",
    ".1....1..1...1..",
    ".1...1....1111..",
    "..1111....111...",
    "..1111....111...",
    "...111....111...",
    "...111..........",
    "...111..........",
    "................",
    "................",
)

# Separate an outlined ball from a compact solid heel.  Real footprints often
# break at the arch, so this retains outline-family weight without asking a
# long hollow loop to carry the entire silhouette.
OUTLINED_BALL_SOLID_HEEL: Final[Matrix] = (
    ".........11.1...",
    ".........11...1.",
    "...1.11.........",
    ".1...11..11111..",
    ".........1....1.",
    "..11111..1....1.",
    ".1....1..11111..",
    ".1....1.........",
    ".11111....111...",
    "..........111...",
    "...111....111...",
    "...111....111...",
    "...111..........",
    "...111..........",
    "................",
    "................",
)

# A single side-view shoe is the clean outline alternative if paired footprint
# contours remain ambiguous at native size.  It intentionally uses a different
# internal silhouette while staying inside the same 16x16 utility tile.
SHOE_OUTLINE: Final[Matrix] = (
    "................",
    "................",
    "................",
    "................",
    ".........111....",
    ".........1.1....",
    ".......111.1....",
    ".....11....1....",
    "...11......1....",
    ".11.........11..",
    ".1............1.",
    ".11111111111111.",
    "................",
    "................",
    "................",
    "................",
)

# Keep a closed outlined forefoot but collapse each long hollow heel into a
# two-cell tapered stroke.  This is a resolution-aware compromise: the icon is
# predominantly outlined, while the narrow heel cannot support useful interior
# negative space at 16x16.
TAPERED_OUTLINE: Final[Matrix] = (
    ".........11.1...",
    ".........11...1.",
    "...1.11.........",
    ".1...11..11111..",
    ".........1....1.",
    "..11111..1....1.",
    ".1....1..1...1..",
    ".1....1..1...1..",
    ".1...1....1..1..",
    "..1..1....1.1...",
    "...1.1.....11...",
    "....11.....11...",
    "....11..........",
    "....11..........",
    "................",
    "................",
)

# Keep the continuous closed sole contour but reduce each large 2x2 toe pad to
# a two-cell cap.  This is the strictest attempt to match the family's thin
# outline weight without changing the selected footprint geometry.
LIGHT_TOES_OUTLINE: Final[Matrix] = (
    ".........11.1...",
    "..............1.",
    "...1.11.........",
    ".1.......11111..",
    ".........1....1.",
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

# Make all three existing toe marks explicit 2x1 lines.  The soles stay in
# their original positions and each toe remains separated by at least one
# source cell vertically or horizontally.
THREE_LINE_TOES_OUTLINE: Final[Matrix] = (
    ".........11.11..",
    "..............11",
    "..11.11.........",
    "11.......11111..",
    ".........1....1.",
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

# Add a fourth 2x1 toe line per foot.  Both sole contours move down one source
# row so the staggered toe pairs have a blank separation row and do not fuse
# into the forefoot at the selected solid 3x3 runtime scale.
FOUR_LINE_TOES_OUTLINE: Final[Matrix] = (
    "........11..11..",
    "................",
    "..11..11..11..11",
    "................",
    "11..11...11111..",
    ".........1....1.",
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
)

# Use a 2x1 cap for the large toe and three single-cell toes descending around
# the outside edge.  This gives each foot four distinct toe marks without
# widening or lowering the selected closed sole contours.
FOUR_TOE_ARC_OUTLINE: Final[Matrix] = (
    ".........11.1...",
    "..............1.",
    "...1.11........1",
    ".1.......11111..",
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

# The approved candidate is one source of truth, not a copied study matrix.
FOUR_TOE_VERTICAL_BIG_OUTLINE: Final[Matrix] = APPROVED_STEP_ICON

STEP_OUTLINE_CANDIDATES: Final[Mapping[str, Matrix]] = {
    "solid-control": SOLID_CONTROL,
    "closed-outline": CLOSED_OUTLINE,
    "open-arch": OPEN_ARCH_OUTLINE,
    "segmented": SEGMENTED_OUTLINE,
    "hollow-forefoot": HOLLOW_FOREFOOT,
    "outline-ball-heel": OUTLINED_BALL_SOLID_HEEL,
    "shoe-outline": SHOE_OUTLINE,
    "tapered-outline": TAPERED_OUTLINE,
    "light-toes": LIGHT_TOES_OUTLINE,
    "three-line-toes": THREE_LINE_TOES_OUTLINE,
    "four-line-toes": FOUR_LINE_TOES_OUTLINE,
    "four-toe-arc": FOUR_TOE_ARC_OUTLINE,
    "four-toe-vertical": FOUR_TOE_VERTICAL_BIG_OUTLINE,
}

TOE_TREATMENT_CANDIDATES: Final[Mapping[str, Matrix]] = {
    "closed-outline": CLOSED_OUTLINE,
    "light-toes": LIGHT_TOES_OUTLINE,
    "three-line-toes": THREE_LINE_TOES_OUTLINE,
    "four-line-toes": FOUR_LINE_TOES_OUTLINE,
    "four-toe-arc": FOUR_TOE_ARC_OUTLINE,
    "four-toe-vertical": FOUR_TOE_VERTICAL_BIG_OUTLINE,
}

BIG_TOE_ORIENTATION_CANDIDATES: Final[Mapping[str, Matrix]] = {
    "four-toe-arc": FOUR_TOE_ARC_OUTLINE,
    "four-toe-vertical": FOUR_TOE_VERTICAL_BIG_OUTLINE,
}


def lit_cells(rows: Matrix) -> int:
    return sum(row.count("1") for row in rows)


def bounds(rows: Matrix) -> tuple[int, int, int, int]:
    coordinates = [
        (x, y)
        for y, row in enumerate(rows)
        for x, value in enumerate(row)
        if value == "1"
    ]
    if not coordinates:
        raise ValueError("step candidate must not be empty")
    xs = [coordinate[0] for coordinate in coordinates]
    ys = [coordinate[1] for coordinate in coordinates]
    return min(xs), min(ys), max(xs), max(ys)


def validate_step_icon_outline_study() -> None:
    expected = (
        "solid-control",
        "closed-outline",
        "open-arch",
        "segmented",
        "hollow-forefoot",
        "outline-ball-heel",
        "shoe-outline",
        "tapered-outline",
        "light-toes",
        "three-line-toes",
        "four-line-toes",
        "four-toe-arc",
        "four-toe-vertical",
    )
    if tuple(STEP_OUTLINE_CANDIDATES) != expected:
        raise ValueError("step outline candidate order drifted")
    if SOLID_CONTROL == APPROVED_STEP_ICON:
        raise ValueError("historical solid control must remain distinct from the approved icon")
    if FOUR_TOE_VERTICAL_BIG_OUTLINE is not APPROVED_STEP_ICON:
        raise ValueError("approved vertical candidate must alias the canonical icon")
    for name, rows in STEP_OUTLINE_CANDIDATES.items():
        if len(rows) != 16 or any(len(row) != 16 for row in rows):
            raise ValueError(f"{name}: expected a 16x16 matrix")
        if set("".join(rows)) - {".", "1"}:
            raise ValueError(f"{name}: matrix must be binary")
        expected_bounds = (
            (1, 4, 14, 11)
            if name == "shoe-outline"
            else (0, 0, 15, 14)
            if name == "four-line-toes"
            else (0, 0, 15, 13)
            if name in ("four-toe-arc", "four-toe-vertical")
            else (0, 0, 15, 13)
            if name == "three-line-toes"
            else (1, 0, 14, 13)
        )
        if bounds(rows) != expected_bounds:
            raise ValueError(f"{name}: footprint placement drifted")
    if len(set(STEP_OUTLINE_CANDIDATES.values())) != len(STEP_OUTLINE_CANDIDATES):
        raise ValueError("step outline candidates must be distinct")
    control_weight = lit_cells(SOLID_CONTROL)
    for name, rows in STEP_OUTLINE_CANDIDATES.items():
        if name != "solid-control" and lit_cells(rows) >= control_weight:
            raise ValueError(f"{name}: outline must be lighter than the control")


validate_step_icon_outline_study()
