"""Failure-path checks for the documentation and public-media gates."""

import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest

import check_repository as checks


class RepositoryChecks(unittest.TestCase):
    def test_links_validate_fragments_and_skip_fenced_examples(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "target.md").write_text("# Repeated\n\n## Repeated\n")
            doc = root / "README.md"
            doc.write_text('[Valid](target.md#repeated-1)\n\n```md\n[Example](missing.md)\n```\n')
            self.assertEqual(checks.check_docs(root, ["README.md", "target.md"]), 2)
            doc.write_text("[Broken](target.md#missing)\n")
            with self.assertRaisesRegex(ValueError, "missing heading"):
                checks.check_docs(root, ["README.md"])

    def test_external_links_and_explicit_html_ids(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text('<a id="sample"></a>\n[Here](#sample)\n[Web](https://example.com/)\n')
            self.assertEqual(checks.check_docs(root, ["README.md"]), 1)

    def test_media_rejects_retouching_and_unlisted_captures(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "docs/media"
            media.mkdir(parents=True)
            (root / "record.md").write_text("# Record\n")
            data = b"\x89PNG\r\n\x1a\n" + b"\0\0\0\rIHDR" + struct.pack(">II", 1, 1)
            capture = {
                "file": "capture.png", "source": "outputs/original.png",
                "sha256": hashlib.sha256(data).hexdigest(), "width": 1, "height": 1,
                "checkpoint": "record.md", "date": "2026-10-07", "target": "test",
                "kind": "test", "mode": "interactive", "claim": "test fixture",
            }
            (media / "manifest.json").write_text(json.dumps({"schema_version": 1, "captures": [capture]}))
            (media / "capture.png").write_bytes(data)
            self.assertEqual(len(checks.validate_media(root)), 1)
            (media / "capture.png").write_bytes(data + b"retouched")
            with self.assertRaisesRegex(ValueError, "hash drift"):
                checks.validate_media(root)
            (media / "capture.png").write_bytes(data)
            (media / "extra.png").write_bytes(data)
            with self.assertRaisesRegex(ValueError, "exact PNG closure"):
                checks.validate_media(root)

    def test_resource_only_boundary_rejects_code_and_private_artifacts(self):
        for name in ("outputs/capture.png", "watchfaces/raster90/src/main/Foo.kt", "secret.keystore"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                checks.check_boundaries(checks.ROOT, [name])
        checks.check_boundaries(checks.ROOT, [])


if __name__ == "__main__":
    unittest.main()
