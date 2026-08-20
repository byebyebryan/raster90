"""Focused checks for the Raster 90 step-outline design study."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import render_raster90_step_icon_outline_study as renderer
from step_icon_outline_study import STEP_OUTLINE_CANDIDATES, bounds, lit_cells


class Raster90StepIconOutlineStudyTests(unittest.TestCase):
    def test_candidates_preserve_placement_and_reduce_weight(self) -> None:
        control_weight = lit_cells(STEP_OUTLINE_CANDIDATES["solid-control"])
        self.assertEqual(bounds(STEP_OUTLINE_CANDIDATES["solid-control"]), (1, 0, 14, 13))
        for name, rows in STEP_OUTLINE_CANDIDATES.items():
            self.assertEqual((len(rows), len(rows[0])), (16, 16), name)
            if name != "solid-control":
                self.assertLess(lit_cells(rows), control_weight, name)

    def test_renderer_outputs_are_deterministic_and_complete(self) -> None:
        expected = renderer.expected_output_bytes()
        self.assertEqual(
            set(expected),
            {
                "step-outline-candidate-sheet.png",
                "step-outline-toe-treatment-sheet.png",
                "step-outline-big-toe-orientation-sheet.png",
                "step-outline-native-row-comparison.png",
                "step-outline-face-comparison.png",
                "step-outline-toe-treatment-face-comparison.png",
                "step-outline-big-toe-orientation-face-comparison.png",
                "step-outline-metrics.txt",
                *{
                    f"step-outline-{name}-face-466.png"
                    for name in STEP_OUTLINE_CANDIDATES
                },
            },
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.assertEqual(renderer.generate_outputs(root), len(expected))
            self.assertEqual(renderer.generate_outputs(root), 0)
            renderer.check_outputs(root)


if __name__ == "__main__":
    unittest.main()
