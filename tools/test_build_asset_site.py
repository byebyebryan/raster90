"""Verify exports against canonical art and reject unpublished/drifting output."""

from pathlib import Path
import tempfile
import unittest

import build_asset_site as site
from fonts.raster90 import family as fonts
from icons.raster90 import animation


class AssetSiteTests(unittest.TestCase):
    def test_export_keeps_complete_artwork_and_exact_motion_frames(self):
        catalog = site.catalog()
        self.assertEqual(catalog["fonts"]["compact"]["glyphs"], dict(fonts.SECONDARY_GLYPHS))
        self.assertEqual(catalog["fonts"]["legacy"]["glyphs"][":"], fonts.PRIMARY_LEGACY_FINE_CHAMFER_COLON)
        self.assertEqual(catalog["motion"]["families"], dict(animation.WEATHER_ANIMATION_FRAMES))
        self.assertEqual(len(catalog["weather"]), 32)
        self.assertEqual(len(catalog["captures"]), 4)
        self.assertTrue(all("source" not in capture for capture in catalog["captures"]))
        for item in catalog["weather"]:
            if item["condition"] != 0:
                self.assertIsNotNone(item["motion"])
                self.assertEqual(item["rows"], catalog["motion"]["families"][item["motion"]][0])

    def test_repeatable_outputs_and_exact_file_closure(self):
        expected = site.expected_outputs()
        self.assertEqual(expected, site.expected_outputs())
        self.assertNotIn(b"<!-- CATALOG -->", expected["index.html"])
        self.assertNotIn(b"outputs/raster90/captures", expected["index.html"])
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for name, data in expected.items():
                path = output / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            site.validate_build(output, expected)
            (output / "unexpected.apk").write_bytes(b"private")
            with self.assertRaisesRegex(ValueError, "closure"):
                site.validate_build(output, expected)
            (output / "unexpected.apk").unlink()
            (output / "app.js").write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "drift"):
                site.validate_build(output, expected)


if __name__ == "__main__":
    unittest.main()
