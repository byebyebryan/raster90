#!/usr/bin/env python3
"""Focused contracts for the canonical Raster 90 icon component."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
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

BATTERY_ROWS = (
    "................",
    "................",
    "................",
    "................",
    ".111111111111...",
    ".1..........1...",
    ".1..........111.",
    ".1..........111.",
    ".1..........111.",
    ".1..........111.",
    ".1..........1...",
    ".111111111111...",
    "................",
    "................",
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
        self.assertEqual(family.BATTERY_ICON, BATTERY_ROWS)
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

    def test_battery_color_contract_and_declarative_xml_branches(self) -> None:
        expected_bands = (
            ("white", 50, None, (255, 255, 255, 255)),
            ("yellow", 25, 50, (255, 216, 0, 255)),
            ("orange", 10, 25, (255, 133, 0, 255)),
            ("red", None, 10, (255, 48, 48, 255)),
        )
        self.assertEqual(family.BATTERY_COLOR_BANDS, expected_bands)
        self.assertEqual(
            [
                (minimum, maximum)
                for _name, minimum, maximum, _color in family.BATTERY_COLOR_BANDS
            ],
            [(50, None), (25, 50), (10, 25), (None, 10)],
        )

        def state_for(percent: int) -> str:
            matches = [
                state_name
                for state_name, minimum, maximum, _color in family.BATTERY_COLOR_BANDS
                if (minimum is None or percent > minimum)
                and (maximum is None or percent <= maximum)
            ]
            self.assertEqual(len(matches), 1, percent)
            if matches:
                return matches[0]
            raise AssertionError(f"no battery state for {percent}%")

        self.assertEqual(
            {percent: state_for(percent) for percent in (100, 51, 50, 26, 25, 11, 10, 0)},
            {
                100: "white",
                51: "white",
                50: "yellow",
                26: "yellow",
                25: "orange",
                11: "orange",
                10: "red",
                0: "red",
            },
        )

        path = ROOT / "watchfaces/raster90/src/main/res/raw/watchface.xml"
        root = ET.parse(path).getroot()
        battery_region = root.find(".//Group[@name='battery_region']")
        self.assertIsNotNone(battery_region)
        condition = battery_region.find("Condition")
        self.assertIsNotNone(condition)
        expressions = {
            expression.attrib["name"]: "".join(expression.itertext()).strip()
            for expression in condition.findall("./Expressions/Expression")
        }
        self.assertEqual(
            expressions,
            {
                "battery_white": "[BATTERY_PERCENT] > 50",
                "battery_yellow": "[BATTERY_PERCENT] > 25 && [BATTERY_PERCENT] <= 50",
                "battery_orange": "[BATTERY_PERCENT] > 10 && [BATTERY_PERCENT] <= 25",
            },
        )

        def tint_hex(color: tuple[int, int, int, int]) -> str:
            red, green, blue, alpha = color
            return f"#{alpha:02x}{red:02x}{green:02x}{blue:02x}"

        compares = condition.findall("Compare")
        self.assertEqual(len(compares), 3)
        expected_geometry = {"x": "0", "y": "0", "width": "48", "height": "48"}
        for compare, (state_name, _minimum, _maximum, color) in zip(
            compares, family.BATTERY_COLOR_BANDS[:3]
        ):
            self.assertEqual(compare.attrib["expression"], f"battery_{state_name}")
            image = compare.find("PartImage")
            self.assertIsNotNone(image, state_name)
            self.assertEqual(
                {key: image.attrib[key] for key in expected_geometry},
                expected_geometry,
                state_name,
            )
            self.assertEqual(image.attrib["tintColor"], tint_hex(color), state_name)
            resource = image.find("Image")
            self.assertIsNotNone(resource, state_name)
            self.assertEqual(resource.attrib, {"resource": "raster_icon_battery"}, state_name)

        default = condition.find("Default")
        self.assertIsNotNone(default)
        red_image = default.find("PartImage")
        self.assertIsNotNone(red_image)
        self.assertEqual(red_image.attrib["tintColor"], tint_hex(expected_bands[-1][3]))
        self.assertEqual(red_image.find("Image").attrib, {"resource": "raster_icon_battery"})

        # The percentage remains a separate white text part, outside the
        # condition branches, and therefore cannot be recolored by tinting.
        value = battery_region.find("PartText[@name='battery_value']")
        self.assertIsNotNone(value)
        self.assertIsNone(condition.find("PartText[@name='battery_value']"))
        value_font = value.find("Text/BitmapFont")
        self.assertIsNotNone(value_font)
        self.assertEqual(value_font.attrib["color"], "#ffffffff")
        self.assertEqual(
            value.find("Text/BitmapFont/Template/Parameter").attrib["expression"],
            "clamp([BATTERY_PERCENT], 0, 100)",
        )

        # The battery remains inside the existing interactive-only boundary;
        # no branch introduces an ambient variant or geometry change.
        interactive = root.find(".//Group[@name='interactive_information']")
        self.assertIsNotNone(interactive)
        self.assertIsNotNone(interactive.find(".//Group[@name='battery_region']"))
        self.assertIsNone(condition.find("Variant"))

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
        battery_path = ROOT / generator.ASSET_DIR_REL / "raster_icon_battery.png"
        self.assertEqual(
            hashlib.sha256(battery_path.read_bytes()).hexdigest(),
            "0f18e0a85d52ad21f57059f68ed175b52aedfc3161ef8944dba1417e4ae86314",
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
        self.assertIn("Battery icon tint contract", document)
        for state_name, _minimum, _maximum, color in family.BATTERY_COLOR_BANDS:
            self.assertIn(state_name, document)
            self.assertIn("#%02X%02X%02X" % color[:3], document)
        self.assertNotIn("http://", document)
        self.assertNotIn("https://", document)

        utility_pixels = generator.decode_png(expected[presentation.UTILITY_SHEET_NAME])[2]
        utility_colors = {pixel for row in utility_pixels for pixel in row}
        for _state_name, _minimum, _maximum, color in family.BATTERY_COLOR_BANDS:
            self.assertIn(color, utility_colors)

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
