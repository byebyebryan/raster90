#!/usr/bin/env python3
"""Render deterministic Raster 90 primary-font corner-treatment comparisons."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "design" / "raster90"))
sys.path.insert(0, str(ROOT / "tools"))

from fonts.raster90.family import (  # noqa: E402
    PRIMARY_COLON,
    PRIMARY_COLON_CELLS,
    PRIMARY_DIGIT_CELLS,
    PRIMARY_LINE_CELLS,
    PRIMARY_SOURCE_DIGITS,
)
from primary_font_refinement import (  # noqa: E402
    CANDIDATES,
    CANDIDATE_LABELS,
    CONTENT_HEIGHT,
    CONTENT_LEFT,
    CONTENT_TOP,
    CONTENT_WIDTH,
    validate_primary_refinement,
)
import generate_raster90_assets as assets  # noqa: E402
import render_raster90_font_family as family_renderer  # noqa: E402


RGBA = tuple[int, int, int, int]
PixelGrid = list[list[RGBA]]
Matrix = tuple[str, ...]

OUTPUT_DIR_REL = Path("outputs/raster90/studies/primary-font-refinement")
CLEAN_SQUARE_SOURCE_1X_NAME = "clean-square-source-1x.png"
CLEAN_SQUARE_SOURCE_3X_NAME = "clean-square-source-3x.png"
CLEAN_CHAMFER_SOURCE_3X_NAME = "clean-chamfer-3x.png"
NATIVE_COMPARISON_NAME = "primary-corner-treatment-native.png"
MAGNIFIED_COMPARISON_NAME = "primary-corner-treatment-magnified.png"
FACE_NAMES = {
    candidate: f"{candidate}-face-466.png" for candidate in CANDIDATES
}

SOURCE_MARGIN = 2
SOURCE_GAP = 2
SOURCE_DIGIT_WIDTH = 7
SOURCE_DIGIT_HEIGHT = 9


def _copy_panel(target: PixelGrid, source: PixelGrid, *, x: int, y: int) -> None:
    for source_y, row in enumerate(source):
        for source_x, pixel in enumerate(row):
            target[y + source_y][x + source_x] = pixel


def _render_primary_sheet(
    digits: Mapping[str, Matrix], *, scale: int
) -> PixelGrid:
    gap = 4 * scale
    widths = [PRIMARY_DIGIT_CELLS * scale] * 10 + [PRIMARY_COLON_CELLS * scale]
    width = sum(widths) + gap * (len(widths) + 1)
    height = PRIMARY_LINE_CELLS * scale + 2 * gap
    pixels = family_renderer._blank(width, height)
    x = gap
    for digit in "0123456789":
        family_renderer._outline(
            pixels,
            x=x,
            y=gap,
            width=PRIMARY_DIGIT_CELLS * scale,
            height=PRIMARY_LINE_CELLS * scale,
        )
        family_renderer._paint_matrix(
            pixels, digits[digit], x=x, y=gap, scale=scale
        )
        x += PRIMARY_DIGIT_CELLS * scale + gap
    family_renderer._outline(
        pixels,
        x=x,
        y=gap,
        width=PRIMARY_COLON_CELLS * scale,
        height=PRIMARY_LINE_CELLS * scale,
    )
    family_renderer._paint_matrix(pixels, PRIMARY_COLON, x=x, y=gap, scale=scale)
    return pixels


def render_clean_square_source_sheet(*, scale: int) -> PixelGrid:
    """Render 0-9 directly from the original 7x9 source cells."""

    digit_count = len(PRIMARY_SOURCE_DIGITS)
    width = (
        2 * SOURCE_MARGIN
        + digit_count * SOURCE_DIGIT_WIDTH
        + (digit_count - 1) * SOURCE_GAP
    ) * scale
    height = (2 * SOURCE_MARGIN + SOURCE_DIGIT_HEIGHT) * scale
    pixels = family_renderer._blank(width, height)
    x = SOURCE_MARGIN * scale
    for digit in "0123456789":
        family_renderer._paint_matrix(
            pixels,
            PRIMARY_SOURCE_DIGITS[digit],
            x=x,
            y=SOURCE_MARGIN * scale,
            scale=scale,
        )
        x += (SOURCE_DIGIT_WIDTH + SOURCE_GAP) * scale
    return pixels


def render_clean_chamfer_source_sheet() -> PixelGrid:
    """Render the reviewed fine-raster edits in the same 3x sheet geometry."""

    width = (
        2 * SOURCE_MARGIN
        + len(CANDIDATES["clean-chamfer"]) * SOURCE_DIGIT_WIDTH
        + (len(CANDIDATES["clean-chamfer"]) - 1) * SOURCE_GAP
    ) * 3
    height = (2 * SOURCE_MARGIN + SOURCE_DIGIT_HEIGHT) * 3
    pixels = family_renderer._blank(width, height)
    x = SOURCE_MARGIN * 3
    for digit in "0123456789":
        boxed = CANDIDATES["clean-chamfer"][digit]
        content = tuple(
            row[CONTENT_LEFT : CONTENT_LEFT + CONTENT_WIDTH]
            for row in boxed[CONTENT_TOP : CONTENT_TOP + CONTENT_HEIGHT]
        )
        family_renderer._paint_matrix(
            pixels,
            content,
            x=x,
            y=SOURCE_MARGIN * 3,
            scale=1,
        )
        x += (SOURCE_DIGIT_WIDTH + SOURCE_GAP) * 3
    return pixels


def render_comparison(*, scale: int) -> PixelGrid:
    validate_primary_refinement()
    sheets = {
        candidate: _render_primary_sheet(digits, scale=scale)
        for candidate, digits in CANDIDATES.items()
    }
    label_height = 10 * assets.FINE_PITCH
    gap = 4 * scale
    width = max(len(sheet[0]) for sheet in sheets.values())
    height = sum(label_height + len(sheet) for sheet in sheets.values()) + gap * 2
    pixels = family_renderer._blank(width, height)
    y = 0
    for index, (candidate, sheet) in enumerate(sheets.items()):
        assets._draw_fine_string(
            pixels,
            CANDIDATE_LABELS[candidate],
            x=12,
            y=y + (label_height - assets.FINE_HEIGHT) // 2,
        )
        y += label_height
        _copy_panel(pixels, sheet, x=0, y=y)
        y += len(sheet)
        if index < len(sheets) - 1:
            y += gap
    return pixels


def render_face(digits: Mapping[str, Matrix], value: str = "12:08") -> PixelGrid:
    pixels = assets._preview_pixels()
    time_y = assets.ACTIVE_ORIGIN[1] + assets.ROW_BANDS["time"][0]
    for y in range(time_y, time_y + assets.TIME_HEIGHT):
        for x in range(assets.CANVAS):
            pixels[y][x] = assets.OPAQUE_BLACK

    time_x = assets.ACTIVE_ORIGIN[0] + (assets.ACTIVE_SIZE - assets.TIME_WIDTH) // 2
    cursor = time_x
    for character in value:
        rows = PRIMARY_COLON if character == ":" else digits[character]
        width = assets.TIME_COLON_WIDTH if character == ":" else assets.TIME_DIGIT_WIDTH
        assets._draw_matrix(
            pixels,
            rows,
            x=cursor,
            y=time_y,
            pitch=assets.TIME_PITCH,
            lit=assets.TIME_LIT,
            color_for=lambda _symbol: assets.OPAQUE_WHITE,
        )
        cursor += width
    return pixels


def _expected_outputs() -> Mapping[str, bytes]:
    outputs = {
        CLEAN_SQUARE_SOURCE_1X_NAME: family_renderer.encode_png(
            render_clean_square_source_sheet(scale=1)
        ),
        CLEAN_SQUARE_SOURCE_3X_NAME: family_renderer.encode_png(
            render_clean_square_source_sheet(scale=3)
        ),
        CLEAN_CHAMFER_SOURCE_3X_NAME: family_renderer.encode_png(
            render_clean_chamfer_source_sheet()
        ),
        NATIVE_COMPARISON_NAME: family_renderer.encode_png(
            render_comparison(scale=3)
        ),
        MAGNIFIED_COMPARISON_NAME: family_renderer.encode_png(
            render_comparison(scale=6)
        ),
    }
    outputs.update(
        {
            FACE_NAMES[candidate]: family_renderer.encode_png(render_face(digits))
            for candidate, digits in CANDIDATES.items()
        }
    )
    return outputs


def _validate_expected(root: Path, expected: Mapping[str, bytes]) -> None:
    output_dir = root / OUTPUT_DIR_REL
    if not output_dir.is_dir():
        raise ValueError(f"primary refinement output directory is missing: {output_dir}")
    actual = {path.name for path in output_dir.iterdir() if path.is_file()}
    if actual != set(expected):
        missing = sorted(set(expected) - actual)
        extra = sorted(actual - set(expected))
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if extra:
            details.append("unexpected: " + ", ".join(extra))
        raise ValueError("; ".join(details))
    for name, data in expected.items():
        if (output_dir / name).read_bytes() != data:
            raise ValueError(f"stale or corrupt primary refinement output: {name}")


def _write_expected(root: Path, expected: Mapping[str, bytes]) -> int:
    output_dir = root / OUTPUT_DIR_REL
    output_dir.mkdir(parents=True, exist_ok=True)
    changed = 0
    for name, data in expected.items():
        path = output_dir / name
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
            changed += 1
    return changed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify without writing")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    expected = _expected_outputs()
    try:
        if args.check:
            _validate_expected(root, expected)
            print(f"Raster 90 primary refinement outputs OK: {len(expected)}")
        else:
            changed = _write_expected(root, expected)
            _validate_expected(root, expected)
            print(
                "Raster 90 primary refinement outputs generated: "
                f"{len(expected)} ({changed} changed)"
            )
    except (OSError, ValueError) as error:
        print(f"Raster 90 primary refinement failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
