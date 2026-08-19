#!/usr/bin/env python3
"""Focused standard-library checks for packaged Raster 90 resources."""

from __future__ import annotations

import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_raster90_assets as generator  # noqa: E402
from matrices import FINE_GLYPHS, SINGLE_GRID_WEATHER_DAY  # noqa: E402


class Raster90AssetGeneratorTests(unittest.TestCase):
    def test_single_grid_dimensions_and_exact_asset_surface(self) -> None:
        self.assertEqual((generator.FINE_PITCH, generator.FINE_LIT), (3, 2))
        self.assertEqual((generator.ICON_SIZE, generator.ICON_SIZE), (48, 48))
        self.assertEqual((generator.TIME_WIDTH, generator.TIME_HEIGHT), (342, 96))
        self.assertEqual(
            generator.ROW_WIDTHS,
            {"weather": 162, "date": 150, "steps": 162, "battery": 126},
        )

    def test_integer_icon_scaling_preserves_opposing_edge_weight(self) -> None:
        unknown = SINGLE_GRID_WEATHER_DAY[0]
        self.assertEqual(unknown[0], unknown[1])
        self.assertEqual(unknown[-2], unknown[-1])
        self.assertEqual(unknown[0], unknown[-1])
        self.assertEqual(
            generator.ROW_X,
            {"weather": 162, "date": 150, "steps": 153, "battery": 171},
        )
        self.assertEqual(
            generator.ROW_BANDS,
            {
                "weather": (45, 93),
                "date": (111, 159),
                "time": (177, 273),
                "steps": (291, 339),
                "battery": (357, 405),
            },
        )

        expected = generator._expected_pngs()
        self.assertEqual(len(expected), 90)
        self.assertFalse(any(name.startswith("raster_coarse_") for name in expected))
        self.assertEqual(
            sum(name.startswith("raster_weather_day_") for name in expected), 16
        )
        self.assertEqual(
            sum(name.startswith("raster_weather_night_") for name in expected), 16
        )
        self.assertEqual(
            {name for name in expected if name.startswith("raster_icon_")},
            {
                "raster_icon_calendar.png",
                "raster_icon_steps.png",
                "raster_icon_battery.png",
            },
        )

        generator._validate_expected(ROOT, expected)

    def test_watchface_xml_keeps_runtime_geometry_and_ambient_boundary(self) -> None:
        path = ROOT / "watchfaces/raster90/src/main/res/raw/watchface.xml"
        root = ET.parse(path).getroot()

        def box(element: ET.Element) -> tuple[int, int, int, int]:
            return tuple(
                int(element.attrib[key]) for key in ("x", "y", "width", "height")
            )

        self.assertEqual((root.attrib["width"], root.attrib["height"]), ("466", "466"))
        expected_groups = {
            "weather_region": (162, 45, 162, 48),
            "date_region": (150, 111, 150, 48),
            "steps_region": (153, 291, 162, 48),
            "battery_region": (171, 357, 126, 48),
        }
        for name, expected in expected_groups.items():
            element = root.find(f".//Group[@name='{name}']")
            self.assertIsNotNone(element, name)
            self.assertEqual(box(element), expected, name)

        unavailable = root.find(".//Group[@name='weather_unavailable_view']")
        self.assertIsNotNone(unavailable)
        self.assertEqual(box(unavailable), (18, 0, 90, 48))
        weather = root.find(".//Group[@name='weather_region']")
        self.assertIsNotNone(weather)
        self.assertEqual(int(weather.attrib["x"]) + int(unavailable.attrib["x"]), 180)

        clock = root.find(".//DigitalClock")
        self.assertIsNotNone(clock)
        self.assertEqual(box(clock), (54, 177, 342, 96))
        time_text = clock.find("TimeText")
        self.assertIsNotNone(time_text)
        self.assertEqual(box(time_text), (0, 0, 342, 96))
        time_font = time_text.find("BitmapFont")
        self.assertIsNotNone(time_font)
        self.assertEqual(
            (time_font.attrib["family"], time_font.attrib["size"]),
            ("raster_time", "96"),
        )

        interactive = root.find(".//Group[@name='interactive_information']")
        self.assertIsNotNone(interactive)
        variants = root.findall(".//Variant")
        self.assertEqual(len(variants), 1)
        self.assertIn(variants[0], list(interactive))
        for group in root.findall(".//Group"):
            if group is not interactive:
                self.assertIsNone(group.find("Variant"), group.attrib.get("name"))

    def test_dimensions_and_palette_are_binary_for_every_generated_png(self) -> None:
        expected = generator._expected_pngs()
        for name, data in expected.items():
            width, height, pixels = generator.decode_png(data)
            generator._check_palette(name, width, height, pixels)
            if name.startswith("raster_weather_") and name != "raster_weather_stale.png":
                self.assertEqual((width, height), (48, 48))
            elif name.startswith("raster_icon_"):
                self.assertEqual((width, height), (48, 48))
            elif name.startswith("raster_time_"):
                self.assertEqual(
                    (width, height),
                    (30 if name.endswith("colon.png") else 78, 96),
                )

    def test_degree_mark_is_closed_and_time_boxes_use_same_source_pitch(self) -> None:
        degree = FINE_GLYPHS["°"]
        self.assertEqual(degree[0], "01110")
        self.assertEqual(degree[3], "01110")
        for rows in generator.TIME_DIGITS.values():
            self.assertEqual((len(rows), len(rows[0])), (32, 26))
        self.assertEqual((len(generator.TIME_COLON), len(generator.TIME_COLON[0])), (32, 10))

    def test_check_rejects_corruption_and_stale_extra(self) -> None:
        expected = generator._expected_pngs()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.assertEqual(generator._write_expected(root, expected), len(expected))
            generator._validate_expected(root, expected)

            corrupt = root / generator.ASSET_DIR_REL / "raster_time_0.png"
            data = bytearray(corrupt.read_bytes())
            data[-1] ^= 0x01
            corrupt.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "asset drift detected"):
                generator._validate_expected(root, expected)

            corrupt.write_bytes(expected["raster_time_0.png"])
            stale = root / generator.ASSET_DIR_REL / "raster_coarse_0.png"
            stale.write_bytes(b"stale")
            with self.assertRaisesRegex(ValueError, "unexpected PNG assets"):
                generator._validate_expected(root, expected)


if __name__ == "__main__":
    unittest.main()
