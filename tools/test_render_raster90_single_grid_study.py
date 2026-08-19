#!/usr/bin/env python3
"""Focused checks for the Raster 90 solid single-grid study renderer."""

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
        self.assertEqual((report["pixel_pitch"], report["pixel_lit"]), (3, 3))
        self.assertEqual(report["cell_fill"], "solid")
        self.assertEqual(report["fixture_temperature_unit"], "C")
        self.assertEqual(report["degree_mark"], "closed ring")
        self.assertEqual(report["safe_circle_coordinate_space"], "active-framebuffer")
        self.assertEqual(report["rows"]["weather"]["active_band"], [45, 93])
        self.assertEqual(report["rows"]["date"]["required_width"], 156)
        self.assertTrue(report["all_safe"])
        geometry = study.geometry_text(report)
        self.assertIn("Deterministic runtime geometry mirrored by this study renderer.", geometry)
        self.assertNotIn("Design-only geometry", geometry)

    def test_face_renders_native_and_scaled_without_palette_drift(self) -> None:
        native = study.render_face()
        scaled = study.resize_nearest(native, 454)
        self.assertEqual((len(native[0]), len(native)), (466, 466))
        self.assertEqual((len(scaled[0]), len(scaled)), (454, 454))
        allowed = {study.BLACK, study.WHITE, *study.WEATHER_PALETTE.values()}
        self.assertTrue(all(pixel in allowed for row in native for pixel in row))
        self.assertTrue(all(pixel in allowed for row in scaled for pixel in row))

        text_origins = {
            "weather": (
                study.ACTIVE_ORIGIN[0]
                + 162
                + study.ICON_CELLS * study.PIXEL_PITCH
                + 2 * study.PIXEL_PITCH,
                "21°C",
            ),
            "date": (study.ACTIVE_ORIGIN[0] + 147, "SAT 15 AUG"),
            "steps": (
                study.ACTIVE_ORIGIN[0]
                + 153
                + study.ICON_CELLS * study.PIXEL_PITCH
                + 2 * study.PIXEL_PITCH,
                "03642",
            ),
            "battery": (
                study.ACTIVE_ORIGIN[0]
                + 171
                + study.ICON_CELLS * study.PIXEL_PITCH
                + 2 * study.PIXEL_PITCH,
                "82%",
            ),
        }
        for name, (text_x, text) in text_origins.items():
            row_y = study.ACTIVE_ORIGIN[1] + study.ROW_BANDS[name][0] * study.PIXEL_PITCH
            text_width = study._text_width(text)
            lit_y = [
                y
                for y in range(row_y, row_y + 48)
                for x in range(text_x, text_x + text_width)
                if native[y][x] == study.WHITE
            ]
            self.assertEqual(min(lit_y), row_y + study.COMPACT_ROW_TEXT_Y, name)

    def test_information_rows_use_selected_icon_led_surface(self) -> None:
        self.assertEqual(set(study.ICONS), {"weather", "steps", "battery"})
        self.assertEqual(
            study.STUDY_TEXT,
            {
                "weather": "21°C",
                "date": "SAT 15 AUG",
                "steps": "03642",
                "battery": "82%",
            },
        )
        for rows in study.ICONS.values():
            self.assertEqual((len(rows), len(rows[0])), (16, 16))

    def test_selected_utility_geometry_has_balanced_strokes(self) -> None:
        battery = study.ICONS["battery"]
        self.assertEqual(battery[4], battery[11])
        self.assertEqual(battery[5], battery[10])
        self.assertTrue(all(row[1] == "1" for row in battery[4:12]))
        self.assertTrue(all(row[13:15] == "11" for row in battery[6:10]))
        self.assertTrue(all(row[15] == "." for row in battery))

        steps = study.ICONS["steps"]
        self.assertEqual(
            steps,
            (
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
            ),
        )

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
