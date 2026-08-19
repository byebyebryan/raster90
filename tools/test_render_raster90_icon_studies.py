#!/usr/bin/env python3
"""Focused standard-library checks for the Raster 90 icon study renderer."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import render_raster90_icon_studies as study  # noqa: E402


class IconStudyTests(unittest.TestCase):
    def test_project_owned_matrices_and_layouts_validate(self) -> None:
        study.validate_study_matrices()
        report = study.build_geometry_report()
        for variant_name in study.VARIANTS:
            variant = report["variants"][variant_name]
            self.assertEqual(variant["gaps"], [20, 20, 20, 20])
            self.assertTrue(variant["all_safe_margins_nonnegative"])
            for row in variant["rows"].values():
                self.assertGreaterEqual(row["safe_margin_total"], 0)
                self.assertEqual(row["safe_margin_per_side"], round(row["safe_margin_total"] / 2, 3))

    def test_every_state_renders_native_without_palette_drift(self) -> None:
        allowed = {study.BLACK, study.WHITE, *study.WEATHER_COLORS.values()}
        for variant_name in study.VARIANTS:
            for state_name in study.STATES:
                pixels = study.render_variant_state(variant_name, state_name)
                self.assertEqual((len(pixels[0]), len(pixels)), (466, 466))
                self.assertTrue(all(pixel in allowed for row in pixels for pixel in row))

    def test_scaled_preview_is_nearest_neighbour_454(self) -> None:
        native = study.render_variant_state("mixed12", "worst")
        scaled = study.resize_nearest(native, 454)
        self.assertEqual((len(scaled[0]), len(scaled)), (454, 454))
        # No blend colors can appear during the design approximation.
        self.assertTrue(all(pixel in {study.BLACK, study.WHITE, *study.WEATHER_COLORS.values()} for row in scaled for pixel in row))

    def test_check_rejects_same_dimension_corruption(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            study.generate_outputs(root)
            path = (
                root
                / "outputs/raster90/studies/iconography"
                / "raster90-icon-study-all8-available-466.png"
            )
            data = bytearray(path.read_bytes())
            data[-1] ^= 0x01
            path.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "stale or corrupt study output"):
                study.check_outputs(root)


if __name__ == "__main__":
    unittest.main()
