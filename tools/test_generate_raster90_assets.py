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
from icon_resolution_studies import (  # noqa: E402
    SIXTEEN_UTILITY_ICONS,
    SIXTEEN_WEATHER_DAY,
    SIXTEEN_WEATHER_NIGHT,
    validate_icon_resolution_studies,
)
from matrices import FINE_GLYPHS  # noqa: E402


class Raster90AssetGeneratorTests(unittest.TestCase):
    def test_single_grid_dimensions_and_exact_asset_surface(self) -> None:
        self.assertEqual((generator.FINE_PITCH, generator.FINE_LIT), (3, 3))
        self.assertEqual((generator.ICON_SIZE, generator.ICON_SIZE), (48, 48))
        self.assertEqual((generator.TIME_WIDTH, generator.TIME_HEIGHT), (342, 96))
        self.assertEqual(
            generator.ROW_WIDTHS,
            {"weather": 162, "date": 156, "steps": 162, "battery": 126},
        )

        expected = generator._expected_pngs()
        self.assertEqual(len(expected), 87)
        self.assertFalse(any(name.startswith("raster_coarse_") for name in expected))
        self.assertEqual(
            sum(name.startswith("raster_weather_day_") for name in expected), 16
        )
        self.assertEqual(
            sum(name.startswith("raster_weather_night_") for name in expected), 16
        )
        self.assertEqual(
            {name for name in expected if name.startswith("raster_icon_")},
            {"raster_icon_steps.png", "raster_icon_battery.png"},
        )
        self.assertNotIn("raster_icon_calendar.png", expected)
        generator._validate_expected(ROOT, expected)

    def test_true16_icon_family_covers_conditions_without_resampling(self) -> None:
        validate_icon_resolution_studies()
        self.assertEqual(set(SIXTEEN_WEATHER_DAY), set(range(16)))
        self.assertEqual(set(SIXTEEN_WEATHER_NIGHT), set(range(16)))
        for rows in SIXTEEN_UTILITY_ICONS.values():
            self.assertEqual((len(rows), len(rows[0])), (16, 16))
        for rows in (*SIXTEEN_WEATHER_DAY.values(), *SIXTEEN_WEATHER_NIGHT.values()):
            self.assertEqual((len(rows), len(rows[0])), (16, 16))

    def test_solid_cell_assets_have_no_gutters_or_partial_cells(self) -> None:
        expected = generator._expected_pngs()
        for name, data in expected.items():
            if not (
                name.startswith("raster_fine_")
                or name.startswith("raster_time_")
                or name.startswith("raster_icon_")
                or (
                    name.startswith("raster_weather_")
                    and name != "raster_weather_stale.png"
                )
            ):
                continue
            width, height, pixels = generator.decode_png(data)
            if name.startswith("raster_fine_"):
                pitch = generator.FINE_PITCH
            elif name.startswith("raster_time_"):
                pitch = generator.TIME_PITCH
            else:
                pitch = generator.ICON_PITCH
            for y in range(0, height, pitch):
                for x in range(0, width, pitch):
                    block = {
                        pixels[yy][xx]
                        for yy in range(y, min(y + pitch, height))
                        for xx in range(x, min(x + pitch, width))
                    }
                    self.assertEqual(len(block), 1, f"partial source cell in {name}")

    def test_selected_rows_are_centered_and_fallback_remains_structural(self) -> None:
        self.assertEqual(
            generator.ROW_X,
            {"weather": 162, "date": 147, "steps": 153, "battery": 171},
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

        path = ROOT / "watchfaces/raster90/src/main/res/raw/watchface.xml"
        root = ET.parse(path).getroot()

        def box(element: ET.Element) -> tuple[int, int, int, int]:
            return tuple(
                int(element.attrib[key]) for key in ("x", "y", "width", "height")
            )

        expected_groups = {
            "weather_region": (162, 45, 162, 48),
            "date_region": (147, 111, 156, 48),
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

        self.assertIsNone(root.find(".//PartImage[@name='calendar_icon']"))
        self.assertIsNone(root.find(".//Image[@resource='raster_icon_calendar']"))
        for name in ("weather_label", "steps_label", "battery_label"):
            self.assertIsNone(root.find(f".//PartText[@name='{name}']"))
        available_values = {
            "weather_temperature": "weather",
            "date_value": "date",
            "steps_six_digit_value": "steps",
            "steps_padded_value": "steps",
            "battery_value": "battery",
        }
        for node_name in available_values:
            node = root.find(f".//PartText[@name='{node_name}']")
            self.assertIsNotNone(node, node_name)
            self.assertEqual(
                (node.attrib["y"], node.attrib["height"]),
                (str(generator.COMPACT_ROW_TEXT_Y), "21"),
                node_name,
            )
        date_text = root.find(".//PartText[@name='date_value']")
        self.assertIsNotNone(date_text)
        self.assertEqual(date_text.attrib["y"], "13")
        self.assertEqual(date_text.find("Text").attrib["align"], "CENTER")
        self.assertIn("%s %d %s", "".join(date_text.itertext()))
        self.assertIsNone(root.find(".//PartText[@name='weather_unavailable_label']"))
        unavailable_value = root.find(
            ".//PartText[@name='weather_unavailable_value']"
        )
        self.assertIsNotNone(unavailable_value)
        self.assertEqual(
            (unavailable_value.attrib["x"], unavailable_value.attrib["y"]),
            ("54", str(generator.COMPACT_ROW_TEXT_Y)),
        )
        self.assertEqual(
            (unavailable_value.attrib["width"], unavailable_value.attrib["height"]),
            ("36", "21"),
        )
        self.assertEqual(unavailable_value.find("Text").attrib["align"], "START")
        self.assertEqual("".join(unavailable_value.itertext()).strip(), "--")

        preview = generator.decode_png(generator._expected_pngs()["preview.png"])[2]
        text_origins = {
            "weather": (
                generator.ACTIVE_ORIGIN[0]
                + generator.ROW_X["weather"]
                + generator.ICON_SIZE
                + 2 * generator.FINE_PITCH,
                "21°C",
            ),
            "date": (generator.ACTIVE_ORIGIN[0] + generator.ROW_X["date"], "SAT 15 AUG"),
            "steps": (
                generator.ACTIVE_ORIGIN[0]
                + generator.ROW_X["steps"]
                + generator.ICON_SIZE
                + 2 * generator.FINE_PITCH,
                "03642",
            ),
            "battery": (
                generator.ACTIVE_ORIGIN[0]
                + generator.ROW_X["battery"]
                + generator.ICON_SIZE
                + 2 * generator.FINE_PITCH,
                "82%",
            ),
        }
        for name, (text_x, text) in text_origins.items():
            row_y = generator.ACTIVE_ORIGIN[1] + generator.ROW_BANDS[name][0]
            text_width = generator._fine_string_width(text)
            lit_y = [
                y
                for y in range(row_y, row_y + 48)
                for x in range(text_x, text_x + text_width)
                if preview[y][x] == generator.OPAQUE_WHITE
            ]
            self.assertEqual(min(lit_y), row_y + generator.COMPACT_ROW_TEXT_Y, name)

    def test_watchface_xml_keeps_time_geometry_and_ambient_boundary(self) -> None:
        path = ROOT / "watchfaces/raster90/src/main/res/raw/watchface.xml"
        root = ET.parse(path).getroot()

        def box(element: ET.Element) -> tuple[int, int, int, int]:
            return tuple(
                int(element.attrib[key]) for key in ("x", "y", "width", "height")
            )

        self.assertEqual((root.attrib["width"], root.attrib["height"]), ("466", "466"))
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

    def test_temperature_unit_configuration_is_celsius_default_and_editable(
        self,
    ) -> None:
        watchface_path = ROOT / "watchfaces/raster90/src/main/res/raw/watchface.xml"
        info_path = ROOT / "watchfaces/raster90/src/main/res/xml/watch_face_info.xml"
        strings_path = ROOT / "watchfaces/raster90/src/main/res/values/strings.xml"

        watchface = ET.parse(watchface_path).getroot()
        configurations = watchface.find("UserConfigurations")
        self.assertIsNotNone(configurations)
        self.assertEqual(len(configurations), 1)

        configuration = configurations.find("ListConfiguration")
        self.assertIsNotNone(configuration)
        self.assertEqual(
            {
                "id": "temperatureUnit",
                "displayName": "temperature_unit_label",
                "screenReaderText": "temperature_unit_label",
                "defaultValue": "CELSIUS",
            },
            configuration.attrib,
        )
        options = configuration.findall("ListOption")
        self.assertEqual(len(options), 2)
        self.assertEqual(
            [option.attrib for option in options],
            [
                {
                    "id": "CELSIUS",
                    "displayName": "temperature_unit_celsius",
                    "screenReaderText": "temperature_unit_celsius",
                },
                {
                    "id": "FAHRENHEIT",
                    "displayName": "temperature_unit_fahrenheit",
                    "screenReaderText": "temperature_unit_fahrenheit",
                },
            ],
        )

        info = ET.parse(info_path).getroot()
        editable = info.find("Editable")
        self.assertIsNotNone(editable)
        self.assertEqual(editable.attrib, {"value": "true"})

        strings = {
            string.attrib["name"]: "".join(string.itertext())
            for string in ET.parse(strings_path).getroot().findall("string")
        }
        self.assertEqual(
            {
                "temperature_unit_label": "Temperature unit",
                "temperature_unit_celsius": "Celsius",
                "temperature_unit_fahrenheit": "Fahrenheit",
            },
            {
                name: strings[name]
                for name in strings
                if name.startswith("temperature_unit")
            },
        )

    def test_temperature_value_converts_provider_units_and_labels_selection(
        self,
    ) -> None:
        path = ROOT / "watchfaces/raster90/src/main/res/raw/watchface.xml"
        root = ET.parse(path).getroot()
        temperature = root.find(".//PartText[@name='weather_temperature']")
        self.assertIsNotNone(temperature)
        parameters = temperature.findall("./Text/BitmapFont/Template/Parameter")
        self.assertEqual(len(parameters), 2)
        value_expression, unit_expression = [
            parameter.attrib["expression"] for parameter in parameters
        ]

        celsius_value = (
            '[CONFIGURATION.temperatureUnit] == "CELSIUS" ? '
            '([WEATHER.TEMPERATURE_UNIT] == 1 ? [WEATHER.TEMPERATURE] : '
            'round(([WEATHER.TEMPERATURE] - 32) * 5 / 9)) : '
            '([WEATHER.TEMPERATURE_UNIT] == 2 ? [WEATHER.TEMPERATURE] : '
            'round([WEATHER.TEMPERATURE] * 9 / 5 + 32))'
        )
        self.assertEqual(value_expression, celsius_value)
        self.assertEqual(
            unit_expression,
            '[CONFIGURATION.temperatureUnit] == "CELSIUS" ? "C" : "F"',
        )
        self.assertIn("[WEATHER.TEMPERATURE_UNIT] == 1", value_expression)
        self.assertIn("[WEATHER.TEMPERATURE_UNIT] == 2", value_expression)
        self.assertIn(
            "round(([WEATHER.TEMPERATURE] - 32) * 5 / 9)", value_expression
        )
        self.assertIn("round([WEATHER.TEMPERATURE] * 9 / 5 + 32)", value_expression)

        def output_temperature(
            provider_value: int, provider_unit: int, selected: str
        ) -> int:
            if selected == "CELSIUS":
                return (
                    provider_value
                    if provider_unit == 1
                    else round((provider_value - 32) * 5 / 9)
                )
            return (
                provider_value
                if provider_unit == 2
                else round(provider_value * 9 / 5 + 32)
            )

        self.assertEqual(output_temperature(21, 1, "CELSIUS"), 21)
        self.assertEqual(output_temperature(63, 2, "CELSIUS"), 17)
        self.assertEqual(output_temperature(68, 2, "FAHRENHEIT"), 68)
        self.assertEqual(output_temperature(20, 1, "FAHRENHEIT"), 68)

        # The same available weather row remains the only source of the
        # formatted value; unavailable weather still renders its neutral --
        # fallback and never reaches these conversion expressions.
        self.assertIsNotNone(root.find(".//Group[@name='weather_unavailable_view']"))
        unavailable_value = root.find(
            ".//PartText[@name='weather_unavailable_value']/Text/BitmapFont"
        )
        self.assertIsNotNone(unavailable_value)
        self.assertEqual("".join(unavailable_value.itertext()).strip(), "--")

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
            stale = root / generator.ASSET_DIR_REL / "raster_icon_calendar.png"
            stale.write_bytes(b"stale")
            with self.assertRaisesRegex(ValueError, "unexpected PNG assets"):
                generator._validate_expected(root, expected)


if __name__ == "__main__":
    unittest.main()
