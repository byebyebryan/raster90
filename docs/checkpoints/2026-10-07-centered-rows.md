# Raster 90 centered-row physical checkpoint — 2026-10-07

The Wear OS weather, steps, and battery rows now center their complete formatted
width. The weather icon, animation, stale marker, and converted temperature move
as one group. Row heights and vertical positions remain unchanged.

- The update passed 56 Python tests, exact asset/font/icon presentation checks,
  debug assembly and lint, WFF validator 1.7.0 for format v2, and the official
  memory gate. The evaluator reported 1,863,648 maximum active bytes and 155,520
  maximum ambient bytes; no PNG resources changed.
- Both identity-proven Wear OS 5 emulators rendered the updated tree without
  clipping at native 466×466 and scaled 454×454. Captures prove centered `100%`
  battery rows on both and a centered red `9%` row on the native target. These
  battery values were emulator-controlled. Weather remained truthfully
  unavailable; signed-temperature and five/six-digit step boundaries were
  checked by the source/runtime placement tests.
- The physical target was freshly verified as `OPWWE251`, Android 14 / API 34,
  466×466 at 320 dpi, with the watch and WFF runtime features. Its previous APK
  was retained for rollback, and the replacement used the same signing
  certificate. Wireless pairing was renewed; pairing credentials and transient
  endpoints are not retained in checkpoint files.
- The built and installed APKs both had SHA-256
  `9d3b9efe5865a8dc955cd3a447169bf4dc8b8c195a84fff127f697c964f32cf2`.
  The unobscured `Awake` capture rendered live night-family weather at `13°C`,
  `WED 7 OCT`, `03218` steps, and `89%` battery with complete rows. Both the
  before and after window evidence identified `DeclarativeWatchFaceRuntime0`.
- This proves current-tree physical interactive rendering. A still image does
  not establish motion playback, and this checkpoint adds no sustained AOD,
  stale-weather, physical low-battery, or battery-impact evidence. Wearer
  acceptance of the centering change remains separate.

The unretouched physical capture, identity, installed/rollback APKs, source diff,
and provenance are retained under
`outputs/raster90/captures/2026-10-07-centered-rows-physical/`. Emulator captures
and the memory report are under
`outputs/raster90/captures/2026-10-07-centered-rows-emulators/`.
