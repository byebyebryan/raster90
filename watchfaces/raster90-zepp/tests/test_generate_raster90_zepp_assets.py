#!/usr/bin/env python3
"""Focused contract tests for the Balance asset adapter."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[1]
ADAPTER_PATH = REPO_ROOT / "tools" / "generate_raster90_zepp_assets.py"
spec = importlib.util.spec_from_file_location("raster90_zepp_asset_generator", ADAPTER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load asset adapter: {ADAPTER_PATH}")
adapter = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = adapter
spec.loader.exec_module(adapter)


class Raster90ZeppAssetTests(unittest.TestCase):
    def test_zepp_weather_mapping_is_complete_and_explicit(self) -> None:
        self.assertEqual(set(adapter.ZEPP_WEATHER_TO_FAMILY), set(range(29)))
        self.assertEqual(adapter.ZEPP_WEATHER_TO_FAMILY[3], "clear_day")
        self.assertEqual(adapter.ZEPP_WEATHER_TO_FAMILY[12], "sleet")
        self.assertEqual(adapter.ZEPP_WEATHER_TO_FAMILY[25], "unknown")
        self.assertEqual(adapter.ZEPP_WEATHER_TO_FAMILY[28], "clear_night")

    def test_generated_closure_is_byte_exact(self) -> None:
        expected = adapter.expected_assets()
        self.assertEqual(len(expected), 119)
        adapter.validate_expected(REPO_ROOT, expected)

    def test_native_and_picker_dimensions(self) -> None:
        expected = adapter.expected_assets()
        for relative, encoded in expected.items():
            width, height, _pixels = adapter.decode_png(encoded)
            if relative == "preview.png":
                self.assertEqual((width, height), (324, 324), relative)
            elif relative.startswith("time/"):
                self.assertEqual((width, height), (30 if relative.endswith("colon.png") else 78, 96), relative)
            elif relative.startswith("text/"):
                if relative.endswith("space.png"):
                    expected_width = 6
                elif relative.endswith("double-minus.png"):
                    expected_width = 36
                else:
                    expected_width = 18
                self.assertEqual((width, height), (expected_width, 21), relative)
            elif relative.startswith("unit/"):
                self.assertEqual((width, height), (36, 21), relative)
            else:
                self.assertTrue(
                    relative.startswith(("utility/", "weather/", "weather-bound/")),
                    relative,
                )
                self.assertEqual((width, height), (48, 48), relative)

    def test_preview_and_runtime_share_the_centered_frame(self) -> None:
        self.assertEqual(adapter.CANVAS, 480)
        self.assertEqual(adapter.ACTIVE_ORIGIN, (15, 15))
        self.assertEqual(adapter.ACTIVE_SIZE, 450)
        self.assertEqual(adapter.TIME_WIDTH, 342)
        self.assertEqual(adapter.TIME_HEIGHT, 96)
        preview = adapter.expected_assets()["preview.png"]
        width, height, pixels = adapter.decode_png(preview)
        self.assertEqual((width, height), (324, 324))
        self.assertTrue(all(pixel[3] == 255 for row in pixels for pixel in row))

    def test_app_declares_balance_v3_target(self) -> None:
        app = json.loads((PACKAGE_ROOT / "app.json").read_text(encoding="utf-8"))
        self.assertEqual(app["configVersion"], "v3")
        self.assertEqual(app["app"]["appId"], 1125469)
        self.assertEqual(app["app"]["appType"], "watchface")
        self.assertEqual(app["permissions"], ["data:user.hd.step"])
        self.assertEqual(app["runtime"]["apiVersion"]["target"], "3.7.0")
        self.assertEqual(app["targets"]["balance"]["designWidth"], 480)
        self.assertFalse(app["debug"])
        self.assertEqual(
            app["targets"]["balance"]["module"]["watchface"]["path"],
            "watchface/balance/index",
        )

    def test_runtime_is_static_and_aod_is_time_only(self) -> None:
        runtime = (PACKAGE_ROOT / "watchface" / "balance" / "index.js").read_text(encoding="utf-8")
        self.assertIn("hmUI.widget.IMG_TIME", runtime)
        self.assertIn("hmUI.widget.IMG_LEVEL", runtime)
        self.assertIn("hmUI.widget.TEXT_IMG", runtime)
        self.assertIn("hmUI.show_level.ONAL_AOD", runtime)
        self.assertIn("show_level: ONLY_NORMAL", runtime)
        self.assertIn("minute_zero: 1", runtime)
        self.assertIn("minute_startX: ORIGIN_X + 240", runtime)
        self.assertIn("minute_startY: ORIGIN_Y + 177", runtime)
        self.assertIn("minute_array: [", runtime)
        self.assertIn("image('time/colon.png')", runtime)
        self.assertNotIn("minute_follow", runtime)
        self.assertNotIn("AnimationController", runtime)
        self.assertNotIn("SequenceImages", runtime)
        self.assertNotIn("STALE", runtime)
        self.assertNotIn("stale", runtime.lower())
        self.assertNotIn("weather/29.png", runtime)

    def test_runtime_sensor_lifecycle_uses_module_events_and_resume_refresh(self) -> None:
        runtime = (PACKAGE_ROOT / "watchface" / "balance" / "index.js").read_text(encoding="utf-8")
        self.assertIn("import * as hmUI from '@zos/ui'", runtime)
        self.assertIn("import { Battery, Step, Time } from '@zos/sensor'", runtime)
        self.assertIn("import { log } from '@zos/utils'", runtime)
        self.assertIn("timeSensor = new Time()", runtime)
        self.assertIn("stepSensor = new Step()", runtime)
        self.assertIn("batterySensor = new Battery()", runtime)
        self.assertIn("timeSensor.getDate()", runtime)
        self.assertIn("timeSensor.getMonth()", runtime)
        self.assertIn("timeSensor.getDay()", runtime)
        self.assertIn("stepSensor.getCurrent()", runtime)
        self.assertIn("batterySensor.getCurrent()", runtime)
        self.assertIn("dateTimer = setInterval(updateDate, 60 * 1000)", runtime)
        self.assertIn("hmUI.widget.WIDGET_DELEGATE", runtime)
        self.assertIn("resume_call", runtime)
        self.assertIn("updateDate()\n      updateSteps()\n      updateBattery()", runtime)
        self.assertIn("stepSensor.onChange(stepChangeCallback)", runtime)
        self.assertIn("stepSensor.offChange(stepChangeCallback)", runtime)
        self.assertIn("batterySensor.onChange(batteryChangeCallback)", runtime)
        self.assertIn("batterySensor.offChange(batteryChangeCallback)", runtime)
        self.assertNotIn("new Weather()", runtime)
        self.assertNotIn("getForecastWeather", runtime)
        self.assertNotIn("updateWeather", runtime)
        self.assertNotIn("weatherTimer", runtime)
        self.assertNotIn("hmSensor", runtime)

    def test_runtime_weather_uses_native_watchface_binding(self) -> None:
        runtime = (PACKAGE_ROOT / "watchface" / "balance" / "index.js").read_text(encoding="utf-8")
        self.assertIn("image_array: weatherAssets", runtime)
        self.assertIn("image_length: weatherAssets.length", runtime)
        self.assertIn("type: hmUI.data_type.WEATHER", runtime)
        self.assertIn("type: hmUI.data_type.WEATHER_CURRENT", runtime)
        self.assertIn("invalid_image: image('text/double-minus.png')", runtime)

    def test_runtime_date_widths_and_steps_preserve_fixed_width_text(self) -> None:
        runtime = (PACKAGE_ROOT / "watchface" / "balance" / "index.js").read_text(encoding="utf-8")
        self.assertIn("var widths = [18, 18, 18, 6, 18, 18, 6, 18, 18, 18]", runtime)
        self.assertIn("text: '00000'", runtime)
        self.assertIn("while (result.length < 5) result = '0' + result", runtime)
        self.assertIn("Math.min(99999, Math.floor(current))", runtime)

    def test_runtime_has_no_copied_shared_polyfills(self) -> None:
        app_source = (PACKAGE_ROOT / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("shared/", app_source)
        self.assertFalse((PACKAGE_ROOT / "shared").exists())

    def test_asset_surface_has_no_animation_or_stale_resources(self) -> None:
        names = adapter.expected_assets()
        self.assertFalse(any("animation" in name for name in names))
        self.assertFalse(any("stale" in name for name in names))
        weather = sorted(name for name in names if name.startswith("weather/"))
        self.assertEqual(weather, [f"weather/{index:02d}.png" for index in range(29)])
        weather_bound = sorted(name for name in names if name.startswith("weather-bound/"))
        self.assertEqual(weather_bound, [f"weather-bound/{index:02d}.png" for index in range(29)])
        for name in weather_bound:
            _width, _height, pixels = adapter.decode_png(names[name])
            self.assertTrue(all(pixel[3] == 255 for row in pixels for pixel in row), name)


if __name__ == "__main__":
    unittest.main()
