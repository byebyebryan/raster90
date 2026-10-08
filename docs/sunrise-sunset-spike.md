# Sunrise/sunset spike — deferred

## Decision (2026-10-07)

Park sunrise/sunset display after the quick Wear OS feasibility spike. The
native data route works, but reliable contextual presentation still has
unresolved behavior. The owner judged the added value insufficient to justify
further work now, given Raster 90's intentional simplicity. No implementation or
further investigation is scheduled.

The idea was to show the next solar event near its occurrence, potentially
reusing the weather row rather than adding a permanent information band. The
spike tested data access and font compatibility, not that product layout or its
switching logic. A companion app was not established as necessary.

## Findings

An isolated, resource-only WFF v2 probe was tested on the physical OnePlus
Watch 3 (`OPWWE251`, Android 14 / API 34, 466×466 at 320 dpi). Its default
`SUNRISE_SUNSET` / `SHORT_TEXT` policy resolved to:

```text
com.heytap.wearable.weather/.complication.wearos.SunriseSunsetProviderService
```

- The provider returned `6:17`, then `7:17`. Both values rendered in the
  diagnostic system font and Raster 90's project-owned bitmap font; exact
  bitmap pixel-mask checks passed for both. Basic native solar-time display
  therefore worked on this device without a custom service or phone companion.
- With the watch's observed 12-hour setting, the text had no AM/PM suffix.
  `TITLE` was empty. The returned image depicted sunrise with an upward arrow
  and yellow sun; there was no sunset sample.
- The one-hour update was unexplained. Astronomical accuracy, location,
  timezone handling, and freshness were not established.
- The documented WFF `SHORT_TEXT` fields provide formatted text, optional
  title, and optional image, rather than a numeric event timestamp or event-kind
  flag. A reliable "within 60 minutes" rule and selection of Raster 90's own
  sunrise/sunset artwork remain unproven.
- A separate EMPTY-default control produced a black capture despite saved
  Awake power state and a WFF runtime window. Its cause was not established;
  unavailable-data rendering is **inconclusive**, not validated.
- Sunset, 24-hour formatting, other locales, updates across an actual event,
  no-data transitions, ambient mode, and integration into the production
  composition were not tested.

The probe packaged the complete 82-glyph secondary vocabulary. Production uses
a smaller subset; a future solar-time feature would need the existing compact
colon glyph packaged, plus any characters required by other provider formats.
The native provider image also differs from Raster 90's authored 3-pixel grid.

## Validation and cleanup

Both isolated probes passed Gradle build/lint, the official WFF XML validator
1.7.0 in format-v2 mode, and the memory-footprint gate. They declared
`android:hasCode="false"` and contained no authored Java/Kotlin classes; debug
DEX contents were limited to generated resource-ID `R` classes. The successful
native-provider capture was an unobscured physical interactive sample, not
accuracy or full feature acceptance.

The baseline was `ac8e6faeb4ed7342c8c4a49e9c34622c8d23b718`. Production code and
assets were unchanged. Raster 90 was restored and visually verified while
Awake; its installed APK matched the pre-spike backup byte-for-byte (SHA-256
`9d3b9efe5865a8dc955cd3a447169bf4dc8b8c195a84fff127f697c964f32cf2`). Both
temporary probe packages were uninstalled and their absence verified.

## Evidence

The retained local artifacts are Git-ignored and may not exist in a fresh
checkout. This document preserves the findings and decision without requiring
those files:

- `outputs/raster90/studies/sunrise-provider-spike-20261007/`: diagnostic
  source/builds and the detailed local report.
- `outputs/raster90/captures/sunrise-provider-spike-20261007/`: physical
  identity, native-provider screenshots/logs, inconclusive EMPTY capture,
  restored Raster 90 capture, APK backups, and hashes in `provenance.json`.

## References

- [SUNRISE_SUNSET system source](https://developer.android.com/reference/androidx/wear/watchface/complications/SystemDataSources#DATA_SOURCE_SUNRISE_SUNSET)
- [WFF complication fields](https://developer.android.com/reference/wear-os/wff/complication/complication)
- [WFF default-provider policy](https://developer.android.com/reference/wear-os/wff/complication/default-provider-policy)
