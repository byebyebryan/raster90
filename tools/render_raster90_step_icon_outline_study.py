#!/usr/bin/env python3
"""Render native and enlarged Raster 90 step-outline comparisons."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "design" / "raster90"))
sys.path.insert(0, str(ROOT / "tools"))

import generate_raster90_assets as runtime_assets  # noqa: E402
from icons.raster90.family import BATTERY_ICON  # noqa: E402
from render_raster90_single_grid_study import (  # noqa: E402
    BLACK,
    WHITE,
    PixelGrid,
    _blank,
    _draw_matrix,
    _draw_text,
    _text_width,
    encode_png,
)
from single_grid_study import ICONS  # noqa: E402
from step_icon_outline_study import (  # noqa: E402
    BIG_TOE_ORIENTATION_CANDIDATES,
    STEP_OUTLINE_CANDIDATES,
    TOE_TREATMENT_CANDIDATES,
    bounds,
    lit_cells,
    validate_step_icon_outline_study,
)


OUTPUT_DIR_REL = Path("outputs/raster90/studies/step-icon-outline")
LABELS = {
    "solid-control": "SOLID CONTROL",
    "closed-outline": "CLOSED OUTLINE",
    "open-arch": "OPEN ARCH",
    "segmented": "SEGMENTED",
    "hollow-forefoot": "HOLLOW FOREFOOT",
    "outline-ball-heel": "OUTLINE BALL HEEL",
    "shoe-outline": "SHOE OUTLINE",
    "tapered-outline": "TAPERED OUTLINE",
    "light-toes": "LIGHT TOES",
    "three-line-toes": "THREE LINE TOES",
    "four-line-toes": "FOUR LINE TOES",
    "four-toe-arc": "FOUR TOE ARC",
    "four-toe-vertical": "VERTICAL BIG TOE",
}
FACE_SIZE = runtime_assets.CANVAS
FACE_LABEL_HEIGHT = 48
FACE_GAP = 18


def _copy(source: PixelGrid, destination: PixelGrid, *, x: int, y: int) -> None:
    for source_y, row in enumerate(source):
        for source_x, pixel in enumerate(row):
            destination[y + source_y][x + source_x] = pixel


def _render_candidate_sheet(
    candidates: Mapping[str, Sequence[str]],
    *,
    title: str,
    subtitle: str,
    column_count: int,
) -> PixelGrid:
    card_width = 360
    card_height = 260
    row_count = (len(candidates) + column_count - 1) // column_count
    width = card_width * column_count
    height = 72 + card_height * row_count
    pixels = _blank(width, height)
    _draw_text(pixels, title, x=18, line_y=12)
    _draw_text(pixels, subtitle, x=18, line_y=39)

    for index, (name, rows) in enumerate(candidates.items()):
        column = index % column_count
        row = index // column_count
        card_x = column * card_width
        card_y = 72 + row * card_height
        label = LABELS[name]
        _draw_text(
            pixels,
            label,
            x=card_x + (card_width - _text_width(label)) // 2,
            line_y=card_y,
        )
        _draw_matrix(
            pixels,
            rows,
            x=card_x + (card_width - 96) // 2,
            y=card_y + 36,
            pitch=6,
            lit=6,
            color_for=lambda _symbol: WHITE,
        )
        metric = f"{lit_cells(rows):02d} CELLS"
        _draw_text(
            pixels,
            metric,
            x=card_x + (card_width - _text_width(metric)) // 2,
            line_y=card_y + 148,
        )
        _draw_matrix(
            pixels,
            rows,
            x=card_x + (card_width - 48) // 2,
            y=card_y + 190,
            pitch=3,
            lit=3,
            color_for=lambda _symbol: WHITE,
        )
    return pixels


def render_candidate_sheet() -> PixelGrid:
    """Show all candidates enlarged and at native size."""

    return _render_candidate_sheet(
        STEP_OUTLINE_CANDIDATES,
        title="STEP ICON OUTLINE STUDY",
        subtitle="6X INSPECTION AND NATIVE 3X",
        column_count=3,
    )


def render_toe_treatment_sheet() -> PixelGrid:
    """Show the focused closed-outline toe treatments."""

    return _render_candidate_sheet(
        TOE_TREATMENT_CANDIDATES,
        title="CLOSED OUTLINE TOE TREATMENTS",
        subtitle="BIG TOE 2X1 AND FOUR TOE OPTIONS",
        column_count=4,
    )


def render_big_toe_orientation_sheet() -> PixelGrid:
    """Compare only horizontal and vertical large-toe treatments."""

    return _render_candidate_sheet(
        BIG_TOE_ORIENTATION_CANDIDATES,
        title="BIG TOE ORIENTATION",
        subtitle="THREE SMALL TOES REMAIN 1X1",
        column_count=2,
    )


def render_anchor_sheet() -> PixelGrid:
    """Compare actual-size candidates against weather and battery outlines."""

    width = 920
    row_height = 78
    height = 48 + row_height * len(STEP_OUTLINE_CANDIDATES)
    pixels = _blank(width, height)
    _draw_text(pixels, "NATIVE ROW WEIGHT", x=18, line_y=12)
    _draw_text(pixels, "STEP 03642", x=380, line_y=12)
    _draw_text(pixels, "WEATHER", x=650, line_y=12)
    _draw_text(pixels, "BATTERY", x=790, line_y=12)

    for index, (name, rows) in enumerate(STEP_OUTLINE_CANDIDATES.items()):
        y = 48 + index * row_height
        label = LABELS[name]
        _draw_text(pixels, label, x=18, line_y=y + 12)
        _draw_matrix(
            pixels,
            rows,
            x=380,
            y=y,
            pitch=3,
            lit=3,
            color_for=lambda _symbol: WHITE,
        )
        _draw_text(pixels, "03642", x=434, line_y=y + 12)
        _draw_matrix(
            pixels,
            ICONS["weather"],
            x=670,
            y=y,
            pitch=3,
            lit=3,
            color_for=lambda _symbol: WHITE,
        )
        _draw_matrix(
            pixels,
            BATTERY_ICON,
            x=806,
            y=y,
            pitch=3,
            lit=3,
            color_for=lambda _symbol: WHITE,
        )
    return pixels


def render_face(rows: Sequence[str]) -> PixelGrid:
    """Replace only the step tile in the canonical generated preview."""

    pixels = [row[:] for row in runtime_assets._preview_pixels()]
    x = runtime_assets.ACTIVE_ORIGIN[0] + runtime_assets.ROW_X["steps"]
    y = runtime_assets.ACTIVE_ORIGIN[1] + runtime_assets.ROW_BANDS["steps"][0]
    for pixel_y in range(y, y + runtime_assets.ICON_SIZE):
        for pixel_x in range(x, x + runtime_assets.ICON_SIZE):
            pixels[pixel_y][pixel_x] = runtime_assets.OPAQUE_BLACK
    runtime_assets._draw_matrix(
        pixels,
        rows,
        x=x,
        y=y,
        pitch=runtime_assets.ICON_PITCH,
        lit=runtime_assets.ICON_LIT,
        color_for=lambda _symbol: runtime_assets.OPAQUE_WHITE,
    )
    return pixels


def _render_face_comparison(
    candidates: Mapping[str, Sequence[str]],
) -> PixelGrid:
    width = FACE_SIZE * 2 + FACE_GAP
    card_height = FACE_LABEL_HEIGHT + FACE_SIZE
    row_count = (len(candidates) + 1) // 2
    height = card_height * row_count + FACE_GAP * (row_count - 1)
    pixels = _blank(width, height)
    for index, (name, rows) in enumerate(candidates.items()):
        column = index % 2
        row = index // 2
        x = column * (FACE_SIZE + FACE_GAP)
        y = row * (card_height + FACE_GAP)
        label = LABELS[name]
        _draw_text(
            pixels,
            label,
            x=x + (FACE_SIZE - _text_width(label)) // 2,
            line_y=y + 12,
        )
        _copy(render_face(rows), pixels, x=x, y=y + FACE_LABEL_HEIGHT)
    return pixels


def render_face_comparison() -> PixelGrid:
    """Render every treatment as actual 466x466 face crops."""

    return _render_face_comparison(STEP_OUTLINE_CANDIDATES)


def render_toe_treatment_face_comparison() -> PixelGrid:
    """Render the focused toe treatments as an actual-size face sheet."""

    return _render_face_comparison(TOE_TREATMENT_CANDIDATES)


def render_big_toe_orientation_face_comparison() -> PixelGrid:
    """Compare the two final toe orientations at actual face size."""

    return _render_face_comparison(BIG_TOE_ORIENTATION_CANDIDATES)


def render_metrics() -> bytes:
    lines = ["Raster 90 step icon outline study", ""]
    for name, rows in STEP_OUTLINE_CANDIDATES.items():
        lines.append(
            f"{name}: lit_cells={lit_cells(rows)} bounds={bounds(rows)}"
        )
    lines.extend(
        (
            "",
            "Footprint-derived candidates retain the current 16x16 tile placement.",
            "The shoe is an alternate symbol; light-toes deliberately reduces the large toe caps.",
            "Three/four-line toes make every toe 2x1; four-toe-arc uses one 2x1 big toe plus three single-cell toes.",
            "Four-toe-vertical rotates only the big toe to 1x2; its other three toes remain single cells.",
            "No candidate is selected by or packaged into the watch-face runtime.",
            "",
        )
    )
    return "\n".join(lines).encode()


def expected_output_bytes() -> dict[str, bytes]:
    validate_step_icon_outline_study()
    outputs = {
        "step-outline-candidate-sheet.png": encode_png(render_candidate_sheet()),
        "step-outline-toe-treatment-sheet.png": encode_png(render_toe_treatment_sheet()),
        "step-outline-big-toe-orientation-sheet.png": encode_png(
            render_big_toe_orientation_sheet()
        ),
        "step-outline-native-row-comparison.png": encode_png(render_anchor_sheet()),
        "step-outline-face-comparison.png": encode_png(render_face_comparison()),
        "step-outline-toe-treatment-face-comparison.png": encode_png(
            render_toe_treatment_face_comparison()
        ),
        "step-outline-big-toe-orientation-face-comparison.png": encode_png(
            render_big_toe_orientation_face_comparison()
        ),
        "step-outline-metrics.txt": render_metrics(),
    }
    for name, rows in STEP_OUTLINE_CANDIDATES.items():
        outputs[f"step-outline-{name}-face-466.png"] = encode_png(render_face(rows))
    return outputs


def check_outputs(root: Path) -> None:
    output_dir = root / OUTPUT_DIR_REL
    for name, expected in expected_output_bytes().items():
        path = output_dir / name
        if not path.exists():
            raise ValueError(f"missing step-outline output: {path}")
        if path.read_bytes() != expected:
            raise ValueError(f"stale or corrupt step-outline output: {path}")


def generate_outputs(root: Path) -> int:
    output_dir = root / OUTPUT_DIR_REL
    output_dir.mkdir(parents=True, exist_ok=True)
    changed = 0
    expected = expected_output_bytes()
    for name, data in expected.items():
        path = output_dir / name
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
            changed += 1
    for path in output_dir.iterdir():
        if path.is_file() and path.name not in expected:
            path.unlink()
            changed += 1
    check_outputs(root)
    return changed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.check:
            check_outputs(root)
            print("Raster 90 step-outline study outputs OK")
        else:
            changed = generate_outputs(root)
            print(f"Raster 90 step-outline study outputs generated ({changed} changed)")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Raster 90 step-outline study failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
