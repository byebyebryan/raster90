"""Contracts for the Raster 90 primary-font corner-treatment study."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "design" / "raster90"))
sys.path.insert(0, str(ROOT / "tools"))

from primary_font_refinement import (  # noqa: E402
    CANDIDATES,
    CLEAN_CHAMFER_ADDITIONS,
    CLEAN_CHAMFER_REMOVALS,
    CONTENT_HEIGHT,
    CONTENT_LEFT,
    CONTENT_TOP,
    CONTENT_WIDTH,
    _has_single_cell_tip,
    _uses_only_complete_macro_cells,
    validate_primary_refinement,
)
import render_raster90_primary_font_refinement as renderer  # noqa: E402


class Raster90PrimaryFontRefinementTests(unittest.TestCase):
    def test_square_baseline_and_reviewed_chamfer_contracts(self) -> None:
        validate_primary_refinement()
        self.assertTrue(
            all(
                _uses_only_complete_macro_cells(rows)
                for rows in CANDIDATES["clean-square"].values()
            )
        )
        self.assertTrue(
            any(
                not _uses_only_complete_macro_cells(rows)
                for rows in CANDIDATES["current-fine-chamfer"].values()
            )
        )
        square = CANDIDATES["clean-square"]
        chamfered = CANDIDATES["clean-chamfer"]
        self.assertEqual(
            {digit for digit in square if chamfered[digit] != square[digit]},
            set("0123456789"),
        )
        self.assertFalse(
            any(_has_single_cell_tip(rows) for rows in chamfered.values())
        )
        self.assertEqual(
            sum(len(edits) for edits in CLEAN_CHAMFER_ADDITIONS.values()),
            133,
        )
        self.assertEqual(
            sum(len(edits) for edits in CLEAN_CHAMFER_REMOVALS.values()),
            39,
        )

        two = chamfered["2"]
        self.assertEqual(
            [two[y].index("1") for y in range(9, 23)],
            list(range(16, 2, -1)),
        )
        self.assertTrue(all(two[y].count("1") == 6 for y in range(9, 23)))

        seven = chamfered["7"]
        self.assertEqual(
            [seven[y].index("1") for y in range(6, 18)],
            list(range(16, 4, -1)),
        )
        self.assertTrue(all(seven[y].count("1") == 6 for y in range(6, 18)))

    def test_comparisons_are_deterministic_and_complete(self) -> None:
        expected = renderer._expected_outputs()
        self.assertEqual(len(expected), 8)
        self.assertEqual(expected, renderer._expected_outputs())
        decoded_faces = {}
        for candidate, face_name in renderer.FACE_NAMES.items():
            width, height, pixels = renderer.assets.decode_png(expected[face_name])
            self.assertEqual((width, height), (466, 466), candidate)
            decoded_faces[candidate] = pixels

        time_y = (
            renderer.assets.ACTIVE_ORIGIN[1]
            + renderer.assets.ROW_BANDS["time"][0]
        )
        time_bottom = time_y + renderer.assets.TIME_HEIGHT
        control = decoded_faces["current-fine-chamfer"]
        for candidate, pixels in decoded_faces.items():
            for y in (*range(time_y), *range(time_bottom, renderer.assets.CANVAS)):
                self.assertEqual(pixels[y], control[y], (candidate, y))

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.assertEqual(renderer._write_expected(root, expected), len(expected))
            renderer._validate_expected(root, expected)
            self.assertEqual(renderer._write_expected(root, expected), 0)

    def test_clean_square_source_sheet_is_true_one_to_one_pixels(self) -> None:
        data = renderer._expected_outputs()[renderer.CLEAN_SQUARE_SOURCE_1X_NAME]
        width, height, pixels = renderer.assets.decode_png(data)
        self.assertEqual((width, height), (92, 13))

        for index, digit in enumerate("0123456789"):
            origin_x = renderer.SOURCE_MARGIN + index * (
                renderer.SOURCE_DIGIT_WIDTH + renderer.SOURCE_GAP
            )
            rows = renderer.PRIMARY_SOURCE_DIGITS[digit]
            for source_y, row in enumerate(rows):
                for source_x, symbol in enumerate(row):
                    expected_pixel = (
                        renderer.family_renderer.WHITE
                        if symbol == "1"
                        else renderer.family_renderer.BLACK
                    )
                    self.assertEqual(
                        pixels[renderer.SOURCE_MARGIN + source_y][
                            origin_x + source_x
                        ],
                        expected_pixel,
                        (digit, source_x, source_y),
                    )

    def test_clean_square_three_x_sheet_is_exact_nearest_neighbor_scale(self) -> None:
        outputs = renderer._expected_outputs()
        width_1x, height_1x, pixels_1x = renderer.assets.decode_png(
            outputs[renderer.CLEAN_SQUARE_SOURCE_1X_NAME]
        )
        width_3x, height_3x, pixels_3x = renderer.assets.decode_png(
            outputs[renderer.CLEAN_SQUARE_SOURCE_3X_NAME]
        )
        self.assertEqual((width_3x, height_3x), (276, 39))
        self.assertEqual((width_3x, height_3x), (width_1x * 3, height_1x * 3))
        for y, row in enumerate(pixels_1x):
            for x, pixel in enumerate(row):
                for scaled_y in range(y * 3, y * 3 + 3):
                    for scaled_x in range(x * 3, x * 3 + 3):
                        self.assertEqual(pixels_3x[scaled_y][scaled_x], pixel)

    def test_clean_chamfer_sheet_matches_candidate_fine_raster(self) -> None:
        data = renderer._expected_outputs()[renderer.CLEAN_CHAMFER_SOURCE_3X_NAME]
        width, height, pixels = renderer.assets.decode_png(data)
        self.assertEqual((width, height), (276, 39))

        for index, digit in enumerate("0123456789"):
            origin_x = renderer.SOURCE_MARGIN * 3 + index * (
                renderer.SOURCE_DIGIT_WIDTH + renderer.SOURCE_GAP
            ) * 3
            rows = CANDIDATES["clean-chamfer"][digit]
            for source_y in range(CONTENT_HEIGHT):
                for source_x in range(CONTENT_WIDTH):
                    symbol = rows[CONTENT_TOP + source_y][CONTENT_LEFT + source_x]
                    expected_pixel = (
                        renderer.family_renderer.WHITE
                        if symbol == "1"
                        else renderer.family_renderer.BLACK
                    )
                    self.assertEqual(
                        pixels[renderer.SOURCE_MARGIN * 3 + source_y][
                            origin_x + source_x
                        ],
                        expected_pixel,
                        (digit, source_x, source_y),
                    )

    def test_check_rejects_stale_extra_output(self) -> None:
        expected = renderer._expected_outputs()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            renderer._write_expected(root, expected)
            output_dir = root / renderer.OUTPUT_DIR_REL
            (output_dir / "stale.png").write_bytes(b"stale")
            with self.assertRaisesRegex(ValueError, "unexpected"):
                renderer._validate_expected(root, expected)


if __name__ == "__main__":
    unittest.main()
