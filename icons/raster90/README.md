# Raster 90 Icon Family

This directory is the first-class, project-owned icon component for Raster 90.
It is the source of the selected runtime surfaces, not a dump of exported
Android resources or a replacement for the historical design studies.

## Ownership and dimensions

- `family.py` is authoritative for the exact indexed weather palette, all 16
  WFF condition IDs with day/night resolution maps, the selected 16×16 steps
  and battery tiles, the neutral unavailable-weather icon, and the 2×2 stale
  marker.
- The approved steps alias is `four-toe-vertical`: each footprint has a closed
  tapered sole, one 1×2 vertical big-toe mark, and three separated 1×1 toe
  marks. `SELECTED_UTILITY_ICONS` contains only `steps` and `battery`.
- Every matrix is authored directly at 16×16 source-cell resolution. The WFF
  generator renders each lit cell as one solid 3×3 square into a 48×48 tile;
  it never integer-expands an old 8×8 source or uses fractional resampling.
- The selected weather refresh uses a centered, star-free cyan outline for
  clear night and a smaller open half-circle behind the partly-night cloud.
  Fog keeps the common white cloud cap above straight haze bars; mist is the
  cloud-free three-bar form; windy uses two upward terminal curls and one
  shorter straight run.
- Rain conditions use identical two-cell `/` strokes in a 2 / 4 / 6
  progression for light / normal / heavy. Snow uses complete five-cell plus
  flakes in a staggered 2 / 3 / 5 progression. Sleet alternates two of those
  rain strokes with two flakes. IDs 11–13 resolve to distinct `light_snow`,
  `light_rain`, and `mist` sprites rather than aliases of the normal families.
- Weather is the only persistent indexed-color plane. Utility resources remain
  monochrome: steps stay white, while the battery icon receives the canonical
  coarse state tint (`>50%` white, `>25%` yellow, `>10%` orange, `0–10%` red).
  Stale is a monochrome marker; unavailable weather is the neutral icon plus
  the truthful `--` value in the WFF branch.

Calendar art, old 8×8/12×12 controls, the historical solid Footprints B step
matrix, and rejected outline candidates remain in `design/raster90/` as
design-only evidence. They are not runtime aliases and must not be restored to
the packaged resource surface.

## Stable API and regeneration

Runtime and study code should import the stable aliases from `family.py`:
`PALETTE`, `BATTERY_COLOR_BANDS`, `SELECTED_UTILITY_ICONS`,
`APPROVED_STEP_ICON`, `BATTERY_ICON`, `WEATHER_DAY`, `WEATHER_NIGHT`,
`UNAVAILABLE_WEATHER_ICON`, and `STALE_MARKER`. The runtime asset generator
imports these mappings directly;
the design modules retain compatibility aliases only for historical renderers.

Regenerate and byte-check both the tracked icon presentation and the 87 PNG
runtime surface from the repository root:

```sh
rtk python3 -B tools/render_raster90_icon_family.py
rtk python3 -B tools/render_raster90_icon_family.py --check
rtk python3 -B tools/generate_raster90_assets.py
rtk python3 -B tools/generate_raster90_assets.py --check
```

`preview/index.html` is self-contained: it embeds the generated sheets, native
466×466 face, 2× magnified face, source matrices, and palette without external
URLs. The PNG sheets are deterministic and should be regenerated rather than
edited by hand. Their presentation is review evidence; it does not claim a
fresh emulator or physical-watch validation.
