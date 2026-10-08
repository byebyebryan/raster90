# Raster 90 simulated-weather emulator checkpoint — 2026-08-21

Freshly validated the then-current tracked runtime tree at HEAD `cf597af` on the
identity-proven native `wear5-opw3` target:

- The deterministic surface contained 87 assets; font and icon presentations,
  single-grid, icon-resolution, step-outline, and primary-refinement checks all
  passed. Fifty Python tests, `xmllint`, WFF validator 1.7.0 for format v2,
  fresh `--rerun-tasks` debug assembly, release assembly, lint, and the
  official memory gate also passed.
- The fresh debug APK SHA-256 was
  `be0aa8428bbe9b41ec94abd4be7cf556dd46180af11ff54bfacaf7d12bc0a640`.
- The target reported Wear OS 5 / Android 14 / API 34, circular 466×466 at
  320 dpi, with the watch and WFF runtime features. The unobscured WFF window
  was `com.google.wear.watchface.runtime.DeclarativeWatchFaceRuntime0`, and
  the interactive capture was Awake.
- Following Google's documented WFF weather-test route, a GPS test provider
  supplied simulated coordinates `37.773972,-122.431297`. Android location and
  fused providers recorded the mock location; the Wear weather provider fetched
  server data at `tempF=59`, notified the WFF runtime, and the Celsius-default
  face rendered a day-family weather icon with `15°C`.
- The fresh interactive capture proves clean-chamfer time, final
  `four-toe-vertical` footprints, current date, `00000` steps, `100%` battery,
  simulated available weather, complete rows, and no clipping. Confirmed
  `mWakefulness=Dozing` reduced the face to monochrome time only.

Ignored evidence is retained under
`outputs/raster90/captures/current-head-simulated-weather/`, including
`interactive-wear5-opw3-simulated-sf-466.png`,
`ambient-wear5-opw3-466.png`, `simulated-location-dumpsys.txt`,
`weather-provider-log.txt`, power/window dumps, and the APK hash.

This closed that exact-tree emulator capture gap and proves available
weather presentation through a simulated location. It is not live local or
physical weather, does not prove stale weather, and does not replace physical
current-art deployment, wearer review, sustained AOD, or battery validation.
