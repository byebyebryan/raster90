#!/usr/bin/env python3
"""Focused contracts for the canonical Raster 90 icon component."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "design" / "raster90"))
sys.path.insert(0, str(ROOT / "tools"))

from icons.raster90 import family  # noqa: E402
import generate_raster90_assets as generator  # noqa: E402
import render_raster90_icon_family as presentation  # noqa: E402
from single_grid_study import ICONS  # noqa: E402
from step_icon_outline_study import (  # noqa: E402
    FOUR_TOE_VERTICAL_BIG_OUTLINE,
    SOLID_CONTROL,
)


APPROVED_STEP_ROWS = (
    ".........1..1...",
    ".........1....1.",
    "...1..1........1",
    ".1....1..11111..",
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


class Raster90IconFamilyTests(unittest.TestCase):
    def test_selected_utility_dimensions_symbols_and_step_candidate(self) -> None:
        family.validate_icon_family()
        self.assertEqual(set(family.SELECTED_UTILITY_ICONS), {"steps", "battery"})
        self.assertIs(family.STEPS_ICON, family.APPROVED_STEP_ICON)
        self.assertIs(family.FOUR_TOE_VERTICAL_BIG_OUTLINE, family.APPROVED_STEP_ICON)
        self.assertIs(family.SELECTED_UTILITY_ICONS["steps"], family.APPROVED_STEP_ICON)
        self.assertEqual(family.APPROVED_STEP_ICON, APPROVED_STEP_ROWS)
        for name, rows in family.SELECTED_UTILITY_ICONS.items():
            self.assertEqual((len(rows), len(rows[0])), (16, 16), name)
            self.assertFalse(set("".join(rows)) - {".", "1"}, name)

        # The approved large toe is one vertical 1x2 line, and the canonical
        # source is not an integer-expanded 8x8 or 2x2 block construction.
        self.assertEqual(
            [(x, y) for y, row in enumerate(family.APPROVED_STEP_ICON)
             for x, cell in enumerate(row) if cell == "1" and x == 9 and y < 2],
            [(9, 0), (9, 1)],
        )
        self.assertFalse(all(
            len({family.APPROVED_STEP_ICON[y][x], family.APPROVED_STEP_ICON[y][x + 1],
                         family.APPROVED_STEP_ICON[y + 1][x], family.APPROVED_STEP_ICON[y + 1][x + 1]}) == 1
            for y in range(0, 16, 2)
            for x in range(0, 16, 2)
        ))

    def test_weather_maps_are_complete_and_aliases_stable(self) -> None:
        self.assertEqual(len(family.WEATHER_CONDITIONS), 16)
        self.assertEqual(set(family.WEATHER_DAY), set(range(16)))
        self.assertEqual(set(family.WEATHER_NIGHT), set(range(16)))
        self.assertEqual(len(family.WEATHER_DAY_RESOLUTION), 16)
        self.assertEqual(len(family.WEATHER_NIGHT_RESOLUTION), 16)
        for rows in (*family.WEATHER_DAY.values(), *family.WEATHER_NIGHT.values()):
            self.assertEqual((len(rows), len(rows[0])), (16, 16))
            self.assertFalse(set("".join(rows)) - {".", *family.PALETTE})
        self.assertIs(family.UNAVAILABLE_WEATHER_ICON, family.WEATHER_SPRITES["unknown"])
        self.assertEqual(family.STALE_MARKER, ("10", "01"))
        self.assertEqual(
            family.PALETTE,
            {
                "Y": (255, 216, 0, 255),
                "C": (73, 223, 255, 255),
                "B": (36, 116, 255, 255),
                "W": (255, 255, 255, 255),
            },
        )

    def test_runtime_binds_canonical_sources_and_surface_is_87_pngs(self) -> None:
        self.assertIs(generator.ICONS["steps"], family.APPROVED_STEP_ICON)
        self.assertIs(generator.ICONS["battery"], family.BATTERY_ICON)
        self.assertIs(generator.ICONS["weather"], family.WEATHER_DAY[14])
        self.assertIs(generator.WEATHER_DAY, family.WEATHER_DAY)
        self.assertIs(generator.WEATHER_NIGHT, family.WEATHER_NIGHT)
        expected = generator._expected_pngs()
        self.assertEqual(len(expected), 87)
        self.assertEqual(
            expected["raster_icon_steps.png"],
            generator.encode_png(generator._utility_pixels(family.APPROVED_STEP_ICON)),
        )
        self.assertEqual(
            expected["raster_icon_battery.png"],
            generator.encode_png(generator._utility_pixels(family.BATTERY_ICON)),
        )
        for condition in range(16):
            self.assertEqual(
                expected[f"raster_weather_day_{condition:02d}.png"],
                generator.encode_png(generator._weather_pixels(family.WEATHER_DAY[condition])),
            )
            self.assertEqual(
                expected[f"raster_weather_night_{condition:02d}.png"],
                generator.encode_png(generator._weather_pixels(family.WEATHER_NIGHT[condition])),
            )

    def test_study_imports_use_canonical_selected_surfaces(self) -> None:
        self.assertIs(ICONS["steps"], family.APPROVED_STEP_ICON)
        self.assertIs(FOUR_TOE_VERTICAL_BIG_OUTLINE, family.APPROVED_STEP_ICON)
        self.assertNotEqual(SOLID_CONTROL, family.APPROVED_STEP_ICON)

    def test_presentation_outputs_are_exact_self_contained_and_stale_detected(self) -> None:
        expected = presentation.expected_output_bytes()
        self.assertEqual(
            set(expected),
            {
                presentation.UTILITY_SHEET_NAME,
                presentation.WEATHER_SHEET_NAME,
                presentation.STATE_SHEET_NAME,
                presentation.MATRIX_SHEET_NAME,
                presentation.NATIVE_FACE_NAME,
                presentation.MAGNIFIED_FACE_NAME,
                presentation.HTML_NAME,
            },
        )
        for name, data in expected.items():
            if name.endswith(".png"):
                width, height, _pixels = generator.decode_png(data)
                self.assertGreater(width, 0, name)
                self.assertGreater(height, 0, name)
        document = expected[presentation.HTML_NAME].decode("utf-8")
        self.assertIn("const ICON_FAMILY_DATA", document)
        self.assertIn("data:image/png;base64,", document)
        self.assertIn("project-owned", document)
        self.assertNotIn("http://", document)
        self.assertNotIn("https://", document)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.assertEqual(presentation._write_expected(root, expected), len(expected))
            presentation._validate_expected(root, expected)
            self.assertEqual(presentation._write_expected(root, expected), 0)
            path = root / presentation.OUTPUT_DIR_REL / presentation.HTML_NAME
            path.write_bytes(path.read_bytes() + b"\n<!-- stale -->\n")
            with self.assertRaisesRegex(ValueError, "drift detected"):
                presentation._validate_expected(root, expected)


if __name__ == "__main__":
    unittest.main()
