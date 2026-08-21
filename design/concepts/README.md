# Exploratory Concept Artwork

These generated bitmap studies explore mood, hierarchy, information density,
and low-frame-rate behavior. They are not production watch-face resources and
must not be used to infer exact cells, glyphs, spacing, palette entries, or WFF
renderer behavior.

Current studies:

- `interactive-indexed-weather.png`: interactive hierarchy with localized
  indexed-color weather;
- `indexed-weather-refresh.png`: a small weather-plane write event;
- `on-visible-four-frame-storyboard.png`: a discrete four-frame reveal; and
- `ambient-monochrome.png`: reduced monochrome ambient presentation.

The images are 1254×1254 concept renders rather than the 466×466 target canvas.
Their prompts and generated pixels are non-authoritative. The current design
contract, selected solid-grid geometry, mathematical fit budget, and validation
boundaries live in [Watch Face Design Direction](../../docs/watchface-design.md).
The provisional two-tier raster and calibration face are historical evidence;
production glyphs and sprites are generated deterministically from the
project-owned font and icon matrices. These concept images are not production
resources or emulator/physical-runtime evidence.
