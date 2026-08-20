"""Focused contracts for the formal Raster 90 bitmap family."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "design" / "raster90"))
sys.path.insert(0, str(ROOT / "tools"))

from fonts.raster90 import family as fonts  # noqa: E402
import generate_raster90_assets as assets  # noqa: E402
import render_raster90_font_family as presentation  # noqa: E402


class Raster90FontFamilyTests(unittest.TestCase):
    def test_complete_family_and_primary_contract(self) -> None:
        fonts.validate_font_family()
        self.assertEqual(
            set(fonts.SECONDARY_GLYPHS),
            set(fonts.SECONDARY_KEYS),
        )
        self.assertEqual(len(fonts.SECONDARY_GLYPHS), 82)
        self.assertEqual(len(fonts.RUNTIME_SECONDARY_GLYPHS), 40)
        self.assertEqual(set(fonts.RUNTIME_SECONDARY_GLYPHS), set(fonts.RUNTIME_SECONDARY_KEYS))
        self.assertEqual(set(fonts.PRIMARY_DIGITS), set("0123456789"))
        self.assertEqual(
            tuple(fonts.PRIMARY_DIGIT_VARIANTS),
            ("square", "clean-chamfer", "legacy-fine-chamfer"),
        )
        self.assertIs(fonts.PRIMARY_DIGITS, fonts.PRIMARY_CLEAN_CHAMFER_DIGITS)
        self.assertIs(fonts.PRIMARY_COLON, fonts.PRIMARY_CLEAN_CHAMFER_COLON)
        self.assertNotEqual(fonts.PRIMARY_SQUARE_DIGITS, fonts.PRIMARY_DIGITS)
        self.assertNotEqual(
            fonts.PRIMARY_LEGACY_FINE_CHAMFER_DIGITS,
            fonts.PRIMARY_DIGITS,
        )
        self.assertEqual(fonts.PRIMARY_TIME_WIDTH_CELLS, 114)
        for rows in fonts.PRIMARY_DIGITS.values():
            self.assertEqual((len(rows), len(rows[0])), (32, 26))
        self.assertEqual((len(fonts.PRIMARY_COLON), len(fonts.PRIMARY_COLON[0])), (32, 10))

        zero = fonts.PRIMARY_DIGITS["0"]
        self.assertFalse(any("1" in row[8:17] for row in zero[8:-8]))
        colon_lit = sum(row.count("1") for row in fonts.PRIMARY_COLON)
        self.assertEqual(colon_lit, 2 * 6 * 6)

    def test_secondary_runtime_surface_isolated_from_complete_source(self) -> None:
        expected = assets._expected_pngs()
        packaged = {
            name.removeprefix("raster_fine_").removesuffix(".png")
            for name in expected
            if name.startswith("raster_fine_")
        }
        names = {
            {
                " ": "space",
                "-": "minus",
                "%": "percent",
                "°": "degree",
            }.get(character, character.lower())
            for character in fonts.RUNTIME_SECONDARY_KEYS
        }
        self.assertEqual(packaged, names)
        self.assertNotIn("plus", packaged)
        self.assertNotIn("question", packaged)
        # Lowercase names intentionally collide with uppercase resource names
        # when normalized for Android identifiers; the expected surface is
        # still keyed by the runtime subset above, never by lowercase glyphs.
        self.assertEqual(len(packaged), len(fonts.RUNTIME_SECONDARY_KEYS))

    def test_primary_cut_keeps_daily_ambient_occupancy_bounded(self) -> None:
        colon_cells = sum(row.count("1") for row in fonts.PRIMARY_COLON)
        peak_cells = -1
        peak_times: list[str] = []
        for hour in range(24):
            for minute in range(60):
                digits = f"{hour:02d}{minute:02d}"
                cells = colon_cells + sum(
                    sum(row.count("1") for row in fonts.PRIMARY_DIGITS[digit])
                    for digit in digits
                )
                time = f"{hour:02d}:{minute:02d}"
                if cells > peak_cells:
                    peak_cells = cells
                    peak_times = [time]
                elif cells == peak_cells:
                    peak_times.append(time)

        self.assertEqual((peak_cells, peak_times), (1526, ["08:08"]))
        self.assertLess(peak_cells * 9, 159043 * 0.15)

    def test_presentation_outputs_are_deterministic_and_complete(self) -> None:
        expected = presentation._expected_outputs()
        self.assertEqual(
            set(expected),
            {
                presentation.PRIMARY_SHEET_NAME,
                presentation.PRIMARY_SQUARE_SHEET_NAME,
                presentation.SECONDARY_SHEET_NAME,
                presentation.FAMILY_SHEET_NAME,
                presentation.NATIVE_FACE_NAME,
                presentation.INSPECTION_NAME,
                presentation.HTML_NAME,
            },
        )
        self.assertEqual(expected, presentation._expected_outputs())
        self.assertEqual(expected[presentation.NATIVE_FACE_NAME][:8], b"\x89PNG\r\n\x1a\n")
        self.assertIn(b"466", expected[presentation.HTML_NAME])

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.assertEqual(presentation._write_expected(root, expected), len(expected))
            presentation._validate_expected(root, expected)
            self.assertEqual(presentation._write_expected(root, expected), 0)

    def test_html_is_self_contained_escaped_and_exposes_surfaces(self) -> None:
        expected = presentation._expected_outputs()
        document = expected[presentation.HTML_NAME].decode("utf-8")
        self.assertIn("<!doctype html>", document)
        self.assertIn("const FONT_DATA =", document)
        self.assertIn("Interactive local preview", document)
        self.assertIn("Complete primary/display matrix surface", document)
        self.assertIn("Complete secondary/text matrix surface", document)
        self.assertIn("data:image/png;base64,", document)
        self.assertNotIn("http://", document)
        self.assertNotIn("https://", document)
        self.assertIn("&quot;", document)
        self.assertIn("&amp;", document)
        self.assertEqual(
            presentation.preview_line_metrics("primary", 6),
            {"glyph_height": 32 * 6, "line_height": 34 * 6},
        )
        self.assertEqual(
            presentation.preview_line_metrics("secondary", 6),
            {"glyph_height": 7 * 6, "line_height": 9 * 6},
        )
        self.assertIn("lineHeight: geometry.lineCells * scale", document)
        self.assertIn('"primary":{"glyphCells":32,"lineCells":34}', document)
        self.assertNotIn("const fallback", document)
        self.assertEqual(document.count("const rows = previewRows(source, cut, character);"), 2)
        self.assertIn("if (!rows) { continue; }", document)
        self.assertNotIn("x += 2 * scale", document)
        escaped = presentation._matrix_markup("<unsafe>", ("00000",) * 7)
        self.assertIn("&lt;unsafe&gt;", escaped)
        self.assertNotIn("<unsafe>", escaped)
        for character in fonts.SECONDARY_KEYS:
            self.assertIn(
                presentation.html.escape(character, quote=True),
                document,
            )

    def test_check_rejects_corruption_and_stale_extra(self) -> None:
        expected = presentation._expected_outputs()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            presentation._write_expected(root, expected)
            path = root / presentation.OUTPUT_DIR_REL / presentation.HTML_NAME
            path.write_bytes(path.read_bytes() + b"\n<!-- drift -->\n")
            with self.assertRaisesRegex(ValueError, "drift detected"):
                presentation._validate_expected(root, expected)

            path.write_bytes(expected[presentation.HTML_NAME])
            (root / presentation.OUTPUT_DIR_REL / "stale.txt").write_text("stale")
            with self.assertRaisesRegex(ValueError, "unexpected font presentation outputs"):
                presentation._validate_expected(root, expected)


if __name__ == "__main__":
    unittest.main()
