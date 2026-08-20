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
- Weather is the only persistent indexed-color plane. Utility tiles are white;
  stale is a monochrome marker; unavailable weather is the neutral icon plus
  the truthful `--` value in the WFF branch.

Calendar art, old 8×8/12×12 controls, the historical solid Footprints B step
matrix, and rejected outline candidates remain in `design/raster90/` as
design-only evidence. They are not runtime aliases and must not be restored to
the packaged resource surface.

## Stable API and regeneration

Runtime and study code should import the stable aliases from `family.py`:
`PALETTE`, `SELECTED_UTILITY_ICONS`, `APPROVED_STEP_ICON`, `BATTERY_ICON`,
`WEATHER_DAY`, `WEATHER_NIGHT`, `UNAVAILABLE_WEATHER_ICON`, and
`STALE_MARKER`. The runtime asset generator imports these mappings directly;
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
