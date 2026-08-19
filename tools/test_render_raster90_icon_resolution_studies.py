#!/usr/bin/env python3
"""Focused checks for the Raster 90 icon-resolution studies."""

from __future__ import annotations

import math
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import render_raster90_icon_resolution_studies as study  # noqa: E402


class IconResolutionStudyTests(unittest.TestCase):
    def test_source_matrices_validate(self) -> None:
        study.validate_icon_resolution_studies()
        for rows in study.EIGHT_UTILITY_ICONS.values():
            self.assertEqual((len(rows[0]), len(rows)), (8, 8))
        for rows in study.SIXTEEN_UTILITY_ICONS.values():
            self.assertEqual((len(rows[0]), len(rows)), (16, 16))

    def test_both_directions_use_same_review_footprint(self) -> None:
        self.assertEqual(8 * 12, study.REVIEW_ICON_SIZE)
        self.assertEqual(16 * 6, study.REVIEW_ICON_SIZE)

    def test_polished_utility_geometry_is_balanced(self) -> None:
        calendar = study.SIXTEEN_UTILITY_ICONS["date"]
        live = [
            (x, y)
            for y, row in enumerate(calendar)
            for x, symbol in enumerate(row)
            if symbol == "1"
        ]
        self.assertEqual(
            (min(x for x, _y in live), max(x for x, _y in live)),
            (2, 13),
        )
        self.assertEqual(
            (min(y for _x, y in live), max(y for _x, y in live)),
            (1, 14),
        )

        battery = study.SIXTEEN_UTILITY_ICONS["battery"]
        self.assertEqual(len(set(battery[6:10])), 1)
        self.assertTrue(all(row[13:15] == "11" for row in battery[6:10]))
        self.assertTrue(all(row[15] == "." for row in battery))

    def test_sheets_render_without_palette_drift(self) -> None:
        allowed = {study.BLACK, study.WHITE, *study.PALETTE.values()}
        for pixels in (
            study.build_true_8x8_sheet(),
            study.build_true_16x16_sheet(),
            study.build_true_16x16_solid_sheet(),
        ):
            self.assertEqual(
                (len(pixels[0]), len(pixels)),
                (study.SHEET_WIDTH, study.SHEET_HEIGHT),
            )
            self.assertTrue(all(pixel in allowed for row in pixels for pixel in row))

    def test_solid_grid_face_mocks_are_native_and_comparable(self) -> None:
        allowed = {study.BLACK, study.WHITE, *study.PALETTE.values()}
        for cell_size in (2, 3):
            pixels = study.build_solid_grid_face_mock(cell_size)
            self.assertEqual((len(pixels[0]), len(pixels)), (466, 466))
            self.assertTrue(all(pixel in allowed for row in pixels for pixel in row))
        comparison = study.build_solid_grid_face_comparison()
        self.assertEqual((len(comparison[0]), len(comparison)), (956, 520))

    def test_two_pixel_mock_honestly_uses_the_smaller_content_scale(self) -> None:
        def live_bounds(pixels):
            live = [
                (x, y)
                for y, row in enumerate(pixels)
                for x, pixel in enumerate(row)
                if pixel != study.BLACK
            ]
            return (
                min(x for x, _y in live),
                min(y for _x, y in live),
                max(x for x, _y in live),
                max(y for _x, y in live),
            )

        two = live_bounds(study.build_solid_grid_face_mock(2))
        three = live_bounds(study.build_solid_grid_face_mock(3))
        self.assertLess(two[2] - two[0], three[2] - three[0])
        self.assertLess(two[3] - two[1], three[3] - three[1])

    def test_single_row_mock_is_native_and_fits_the_safe_circle(self) -> None:
        pixels = study.build_solid_grid_single_row_face_mock(3)
        self.assertEqual((len(pixels[0]), len(pixels)), (466, 466))
        comparison = study.build_solid_grid_row_layout_comparison()
        self.assertEqual((len(comparison[0]), len(comparison)), (956, 520))

        expected_width_cells = {
            "weather": 56,
            "date": 70,
            "steps": 68,
            "battery": 56,
        }
        for name, width_cells in expected_width_cells.items():
            self.assertEqual(study.solid_single_row_width_cells(name), width_cells)
            start, end = study.FACE_ROW_BANDS[name]
            edge = max((start * 3, end * 3), key=lambda y: abs(y - 225))
            safe_chord = 2 * math.sqrt(210**2 - (edge - 225) ** 2)
            self.assertLessEqual(width_cells * 3, safe_chord)

    def test_icon_led_mock_removes_only_redundant_headers(self) -> None:
        self.assertEqual(
            study.ICON_LED_TEXT,
            {
                "weather": "21°C",
                "date": "SAT 15 AUG",
                "steps": "03642",
                "battery": "82%",
            },
        )
        pixels = study.build_solid_grid_icon_led_face_mock(3)
        self.assertEqual((len(pixels[0]), len(pixels)), (466, 466))
        comparison = study.build_solid_grid_header_comparison()
        self.assertEqual((len(comparison[0]), len(comparison)), (956, 520))

        expected_width_cells = {
            "weather": 42,
            "date": 70,
            "steps": 48,
            "battery": 36,
        }
        for name, width_cells in expected_width_cells.items():
            self.assertEqual(
                study.solid_single_row_width_cells(name, study.ICON_LED_TEXT),
                width_cells,
            )
            self.assertLessEqual(
                width_cells,
                study.solid_single_row_width_cells(name),
            )

    def test_no_calendar_mock_centers_date_text_without_changing_its_data(self) -> None:
        self.assertEqual(study.ICON_LED_TEXT["date"], "SAT 15 AUG")
        self.assertEqual(study.centered_date_width_cells(), 52)
        self.assertLess(
            study.centered_date_width_cells(),
            study.solid_single_row_width_cells("date", study.ICON_LED_TEXT),
        )
        pixels = study.build_solid_grid_no_calendar_face_mock(3)
        self.assertEqual((len(pixels[0]), len(pixels)), (466, 466))
        comparison = study.build_solid_grid_calendar_comparison()
        self.assertEqual((len(comparison[0]), len(comparison)), (956, 520))

    def test_check_rejects_corrupt_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            study.generate_outputs(root)
            path = (
                root
                / study.OUTPUT_DIR_REL
                / "raster90-true-8x8-solid-icon-sheet.png"
            )
            data = bytearray(path.read_bytes())
            data[-1] ^= 0x01
            path.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "stale or corrupt"):
                study.check_outputs(root)


if __name__ == "__main__":
    unittest.main()
