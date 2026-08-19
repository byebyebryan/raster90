#!/usr/bin/env python3
"""Focused checks for the Raster 90 3/2 single-grid study renderer."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import render_raster90_single_grid_study as study  # noqa: E402


class SingleGridStudyTests(unittest.TestCase):
    def test_grid_and_matrices_validate(self) -> None:
        study.validate_single_grid_study()
        report = study.geometry_report()
        self.assertEqual(report["source_framebuffer"], [150, 150])
        self.assertEqual((report["pixel_pitch"], report["pixel_lit"]), (3, 2))
        self.assertEqual(report["fixture_temperature_unit"], "C")
        self.assertEqual(report["degree_mark"], "closed ring")
        self.assertEqual(report["safe_circle_coordinate_space"], "active-framebuffer")
        self.assertEqual(report["rows"]["weather"]["active_band"], [45, 93])
        self.assertTrue(report["all_safe"])

    def test_face_renders_native_and_scaled_without_palette_drift(self) -> None:
        native = study.render_face()
        scaled = study.resize_nearest(native, 454)
        self.assertEqual((len(native[0]), len(native)), (466, 466))
        self.assertEqual((len(scaled[0]), len(scaled)), (454, 454))
        allowed = {study.BLACK, study.WHITE, *study.WEATHER_PALETTE.values()}
        self.assertTrue(all(pixel in allowed for row in native for pixel in row))
        self.assertTrue(all(pixel in allowed for row in scaled for pixel in row))

    def test_information_rows_use_uniform_icon_tiles(self) -> None:
        for name in ("weather", "date", "steps", "battery"):
            rows = study.ICONS[name]
            self.assertEqual(len(rows), 16)
            self.assertTrue(all(len(row) == 16 for row in rows))

    def test_utility_icon_structural_lines_have_symmetric_weight(self) -> None:
        battery = study.ICONS["battery"]
        self.assertEqual(battery[4:6], battery[10:12])
        self.assertTrue(all(row[2:4] == "11" for row in battery[4:12]))
        self.assertTrue(all(row[10:12] == "11" for row in battery[4:12]))

        calendar = study.ICONS["date"]
        self.assertEqual(calendar[2:4], calendar[14:16])
        self.assertTrue(all(row[2:4] == "11" for row in calendar[2:16]))
        self.assertTrue(all(row[12:14] == "11" for row in calendar[2:16]))

    def test_current_icon_sheet_covers_exact_runtime_icon_surface(self) -> None:
        sheet = study.build_current_icon_sheet()
        self.assertEqual(
            (len(sheet[0]), len(sheet)),
            (study.ICON_SHEET_WIDTH, study.ICON_SHEET_HEIGHT),
        )
        self.assertEqual(set(study.SINGLE_GRID_WEATHER_DAY), set(range(16)))
        self.assertEqual(set(study.SINGLE_GRID_WEATHER_NIGHT), set(range(16)))
        allowed = {study.BLACK, study.WHITE, *study.WEATHER_PALETTE.values()}
        self.assertTrue(all(pixel in allowed for row in sheet for pixel in row))

    def test_check_rejects_corrupt_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            study.generate_outputs(root)
            path = (
                root
                / "outputs/raster90/studies/single-grid"
                / "raster90-single-grid-face-466.png"
            )
            data = bytearray(path.read_bytes())
            data[-1] ^= 0x01
            path.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "stale or corrupt"):
                study.check_outputs(root)


if __name__ == "__main__":
    unittest.main()
