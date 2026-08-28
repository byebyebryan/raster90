# Raster 90 Icon Family

This directory is the first-class, project-owned icon component for Raster 90.
It is the source of the selected runtime surfaces, not a dump of exported
Android resources or a replacement for the historical design studies.

## Ownership and dimensions

- `family.py` is authoritative for the exact indexed weather palette, all 16
  WFF condition IDs with day/night resolution maps, the selected steps and
  battery tiles, the neutral unavailable-weather icon, and the 2×2 stale
  marker.
- `animation.py` is authoritative for the promoted eight-phase motion of all
  16 recognized day/night-resolved weather families. Every phase stays inside
  the same 15×15 drawable field, and phase 0 is byte-equivalent to its selected
  static matrix.
- The approved steps alias is `four-toe-vertical`: each footprint has a closed
  tapered sole, one 1×2 vertical big-toe mark, and three separated 1×1 toe
  marks. `SELECTED_UTILITY_ICONS` contains only `steps` and `battery`.
- Every selected icon uses a 16×16 storage matrix with a 15×15 drawable field
  centered on cell `(7,7)`. Row 15 and column 15 must remain empty as the trailing
  registration gutter, making source cell `(7,7)` the visual center. The WFF
  generator renders each lit cell as one solid 3×3 square into a stable 48×48
  tile and verifies the corresponding final three-pixel row and column are
  transparent; it never integer-expands an old 8×8 source or uses fractional
  resampling.
- The selected weather refresh uses a centered, star-free cyan outline for
  clear night and a smaller open half-circle behind the partly-night cloud.
  Fog keeps the common white cloud cap above straight haze bars; mist is the
  cloud-free three-bar form; windy uses two upward terminal curls and one
  shorter straight run. Bare cloudy uses a separate y=3–10 centered cloud;
  cloud-bearing fog and precipitation retain the shared y=1–8 top anchor.
- Rain conditions use identical two-cell `/` strokes in a 2 / 4 / 6
  progression for light / normal / heavy; all three rain fields use the
  reviewed one-cell-left placement. Snow uses complete five-cell plus flakes
  in a staggered 2 / 3 / 5 progression; normal and heavy snow use the reviewed
  one-cell-right placement while light snow remains unchanged. Sleet alternates
  two rain strokes with two flakes, with its upper-left rain stroke raised one
  cell and pulled two cells left. IDs 11–13 resolve to distinct `light_snow`,
  `light_rain`, and `mist` sprites rather than aliases of the normal families.
- Weather is the only persistent indexed-color plane. Utility resources remain
  monochrome: steps stay white, while the battery icon receives the canonical
  coarse state tint (`>50%` white, `>25%` yellow, `>10%` orange, `0–10%` red).
  Stale is a monochrome marker; unavailable weather is the neutral icon plus
  the truthful `--` value in the WFF branch.
- Fresh recognized weather alone receives one two-second, 4-fps `ON_VISIBLE`
  gesture. The controller does not repeat and restores the first frame after
  playback. Stale, unavailable, unknown, and ambient presentations remain
  static. Runtime sequence PNGs use an opaque black field behind the indexed
  pixels so moving cells replace, rather than reveal, the static icon below.

Calendar art, old 8×8/12×12 controls, the historical solid Footprints B step
matrix, and rejected outline candidates remain in `design/raster90/` as
design-only evidence. They are not runtime aliases and must not be restored to
the packaged resource surface.

## Stable API and regeneration

Static runtime and study code should import the stable aliases from `family.py`:
`PALETTE`, `BATTERY_COLOR_BANDS`, `SELECTED_UTILITY_ICONS`,
`APPROVED_STEP_ICON`, `BATTERY_ICON`, `WEATHER_DAY`, `WEATHER_NIGHT`,
`UNAVAILABLE_WEATHER_ICON`, and `STALE_MARKER`. The runtime asset generator
imports these mappings directly;
the design modules retain compatibility aliases only for historical renderers.
Animation consumers should import `WEATHER_ANIMATION_FRAMES`, `FRAME_COUNT`,
`FRAME_RATE`, and `animation_resource_name` from `animation.py`; the promoted
source no longer depends on an ignored study renderer.

Regenerate and byte-check both the tracked icon presentation and the 215 PNG
runtime surface from the repository root:

```sh
rtk python3 -B tools/render_raster90_icon_family.py
rtk python3 -B tools/render_raster90_icon_family.py --check
rtk python3 -B tools/generate_raster90_assets.py
rtk python3 -B tools/generate_raster90_assets.py --check
```

`preview/index.html` is self-contained: it embeds the generated static sheets,
the looping animation GIF, the exact eight-phase sheet, native 466×466 face, 2×
magnified face, source matrices, and palette without external URLs. The GIF's
one-second resting gap and infinite loop are presentation-only; the WFF runtime
still plays once. Presentation-only matrix views use a visible blue-gray fill
behind the 15×15 drawable field while leaving the trailing storage row and
column black; this tint is not packaged into runtime assets. All outputs are
deterministic and should be regenerated rather than edited by hand. Their
presentation is review evidence; it does not claim a fresh emulator or
physical-watch validation.
