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
contract, provisional two-tier raster, mathematical fit budget, and calibration
requirements live in [Watch Face Design Direction](../../docs/watchface-design.md).
Production glyphs and sprites will be generated deterministically only after
renderer calibration.
