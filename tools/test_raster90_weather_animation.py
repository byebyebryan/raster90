#!/usr/bin/env python3
"""Production contracts for Raster 90's promoted weather animation."""

from __future__ import annotations

import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from icons.raster90 import animation  # noqa: E402
from icons.raster90 import family  # noqa: E402
import generate_raster90_assets as generator  # noqa: E402


class Raster90WeatherAnimationTests(unittest.TestCase):
    def test_promoted_frames_are_complete_and_rest_on_static_art(self) -> None:
        animation.validate_weather_animation()
        self.assertEqual(animation.FRAME_COUNT, 8)
        self.assertEqual(animation.FRAME_RATE, 4)
        self.assertEqual(
            set(animation.WEATHER_ANIMATION_FAMILIES),
            set(family.WEATHER_SPRITES) - {"unknown"},
        )
        self.assertNotIn("unknown", animation.WEATHER_ANIMATION_FRAMES)

        for weather_family, frames in animation.WEATHER_ANIMATION_FRAMES.items():
            with self.subTest(family=weather_family):
                self.assertEqual(len(frames), animation.FRAME_COUNT)
                self.assertEqual(frames[0], family.WEATHER_SPRITES[weather_family])
                self.assertGreater(len(set(frames)), 1)
                for matrix in frames:
                    family.validate_drawable_matrix(weather_family, matrix)

    def test_generated_frame_assets_are_exact_and_complete(self) -> None:
        expected = generator._expected_pngs()
        animation_assets = {
            name: data
            for name, data in expected.items()
            if name.startswith("raster_weather_anim_")
        }
        self.assertEqual(
            len(animation_assets),
            len(animation.WEATHER_ANIMATION_FAMILIES) * animation.FRAME_COUNT,
        )
        for weather_family, frames in animation.WEATHER_ANIMATION_FRAMES.items():
            for phase, matrix in enumerate(frames):
                name = f"{animation.animation_resource_name(weather_family, phase)}.png"
                self.assertEqual(
                    animation_assets[name],
                    generator.encode_png(generator._weather_animation_pixels(matrix)),
                    name,
                )
                _width, _height, pixels = generator.decode_png(animation_assets[name])
                self.assertTrue(
                    all(pixel[3] == 255 for row in pixels for pixel in row),
                    name,
                )

    def test_wff_plays_one_fresh_gesture_and_keeps_fallbacks_static(self) -> None:
        root = ET.parse(
            ROOT / "watchfaces/raster90/src/main/res/raw/watchface.xml"
        ).getroot()
        interactive = root.find(".//Group[@name='interactive_information']")
        self.assertIsNotNone(interactive)
        self.assertEqual(
            interactive.find("Variant[@mode='AMBIENT']").attrib,
            {"mode": "AMBIENT", "target": "alpha", "value": "0"},
        )

        animated_parts = interactive.findall(".//PartAnimatedImage")
        self.assertEqual(len(animated_parts), len(animation.WEATHER_ANIMATION_FAMILIES))
        self.assertEqual(
            {part.attrib["name"].removeprefix("weather_animation_") for part in animated_parts},
            set(animation.WEATHER_ANIMATION_FAMILIES),
        )
        for part in animated_parts:
            weather_family = part.attrib["name"].removeprefix("weather_animation_")
            self.assertEqual(
                {key: part.attrib[key] for key in ("x", "y", "width", "height")},
                {"x": "0", "y": "0", "width": "48", "height": "48"},
            )
            thumbnail = part.find("Thumbnail")
            self.assertEqual(
                thumbnail.attrib["resource"],
                animation.animation_resource_name(weather_family, 0),
            )
            controller = part.find("AnimationController")
            self.assertEqual(
                controller.attrib,
                {
                    "play": "ON_VISIBLE",
                    "repeat": "FALSE",
                    "loopCount": "1",
                    "resumePlayBack": "FALSE",
                    "beforePlaying": "FIRST_FRAME",
                    "afterPlaying": "FIRST_FRAME",
                },
            )
            sequence = part.find("SequenceImages")
            self.assertEqual(
                sequence.attrib,
                {"loopCount": "1", "frameRate": str(animation.FRAME_RATE)},
            )
            self.assertEqual(
                [image.attrib["resource"] for image in sequence.findall("Image")],
                [
                    animation.animation_resource_name(weather_family, phase)
                    for phase in range(animation.FRAME_COUNT)
                ],
            )

        weather_error = next(
            condition
            for condition in root.findall(".//Condition")
            if condition.find("./Expressions/Expression[@name='weather_error']")
            is not None
        )
        stale_branch = weather_error.find("Compare[@expression='weather_error']")
        self.assertIsNotNone(stale_branch.find("PartImage[@name='weather_stale_marker']"))
        self.assertIsNone(stale_branch.find(".//PartAnimatedImage"))
        fresh_branch = weather_error.find("Default")
        self.assertEqual(
            len(fresh_branch.findall(".//PartAnimatedImage")),
            len(animation.WEATHER_ANIMATION_FAMILIES),
        )
        fresh_condition = fresh_branch.find("Condition")
        self.assertIsNotNone(fresh_condition)
        condition_ids = sorted(
            int(value)
            for expression in fresh_condition.findall("./Expressions/Expression")
            for value in re.findall(r"\[WEATHER\.CONDITION\] == (\d+)", expression.text)
        )
        self.assertEqual(condition_ids, list(range(1, 16)))
        self.assertIsNone(fresh_condition.find("Default"))

        unavailable = root.find(".//Group[@name='weather_unavailable_view']")
        self.assertIsNotNone(unavailable)
        self.assertIsNone(unavailable.find(".//PartAnimatedImage"))
        self.assertEqual(
            unavailable.find(".//Image").attrib["resource"],
            "raster_weather_day_00",
        )


if __name__ == "__main__":
    unittest.main()
